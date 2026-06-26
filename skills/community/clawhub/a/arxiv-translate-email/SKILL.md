---
name: arxiv-translate-email
description: 从 arXiv 下载论文并翻译为中文，发送至邮箱。当用户说"下载并翻译论文"、"翻译这篇文献"、"下载xxx论文并发送到我邮箱"时使用此技能。支持同步和异步两种模式。
---

# arxiv-translate-email

## 两种工作模式

### ⚡ 异步队列模式（推荐，小Pi串行执行）

翻译任务进入队列，由后台 cron 定时触发 worker 串行执行。**同一时间只跑一个任务**，保护小Pi。

**添加任务：**
```bash
python3 /root/workspace/Remember/tasks/queue_manager.py add <arxiv_url> <邮箱> [论文标题]
```

**查看队列：**
```bash
python3 /root/workspace/Remember/tasks/queue_manager.py list
python3 /root/workspace/Remember/tasks/queue_manager.py pending  # 只看待处理数量
```

**清理已完成：**
```bash
python3 /root/workspace/Remember/tasks/queue_manager.py clear
```

**Cron 配置：** 每 3 分钟检查一次队列，有任务则执行。完成后通过 QQ 主动通知（announce 已修复，投递目标 qqbot:c2c:F6C87A75D65679207F9A41EA424742C6）。

---

### 🔧 同步直接执行

不走队列，直接执行，等完成再返回。阻塞主会话，适合临时单次使用。

---

## 环境配置

- **pdf2zh_next**：`/root/workspace/pdf2zh2/.venv/bin/pdf2zh_next`
- **代理**：`HTTPS_PROXY=http://127.0.0.1:7890 HTTP_PROXY=http://127.0.0.1:7890`
- **DeepSeek API**：`sk-aea81697cdc34baa8a11727b52bbb513`
- **邮件 SMTP**：QQ 邮箱 smtp.qq.com:465，用户 2794002698@qq.com，授权码 ydtmhlhcraqudhcc

## 核心脚本

| 脚本 | 作用 |
|------|------|
| `tasks/queue_manager.py` | 队列增删查改 |
| `tasks/arxiv_worker.py` | Worker，执行下载→翻译→发邮件 |
| `tasks/arxiv_translate_queue.json` | 队列状态文件 |

## 翻译命令模板（同步模式参考）

```bash
cd /root/workspace/pdf2zh2 && \
# 清理旧输出
rm -f translated/{slug}.*.pdf && \
HTTPS_PROXY=http://127.0.0.1:7890 HTTP_PROXY=http://127.0.0.1:7890 \
nohup env PYTHONUNBUFFERED=1 \
setsid .venv/bin/python -u .venv/bin/pdf2zh_next \
  --deepseek \
  --deepseek-api-key "sk-aea81697cdc34baa8a11727b52bbb513" \
  --deepseek-model deepseek-chat \
  --lang-in en \
  --lang-out zh \
  --pool-max-workers 4 \
  --qps 4 \
  --no-auto-extract-glossary \
  --output ./translated \
  source/{slug}.pdf > translate.log 2>&1 &
```

或者可以参考~/.config/pdf2zh2/config.v3.toml
**输出文件**：`translated/{slug}.zh.dual.pdf`（扁平目录，无子文件夹）

## 关键注意事项

- **doclayout 解析慢**：23 页论文约需 5-8 分钟，纯 CPU 密集，不要误以为卡死
- **完成后查询**：进程消失 + `ls -lh translated/*.pdf` 有文件即完成
- **发邮件**：附件路径是 `translated/{slug}.zh.dual.pdf`
- **串行保证**：lock 文件机制，同一时间只能有一个 processing 任务
- **QQ 通知**：任务完成后 cron worker 会通过 QQ 主动推送通知（已修复 announce 投递）

## 发送邮件脚本

见 `scripts/send_email.py`，用法：
```bash
python3 scripts/send_email.py <to_email> <subject> <body> <pdf_path> [attachment_name]
```

## 完整流程示例（同步）

1. 搜索：`curl "https://export.arxiv.org/api/query?search_query=ti:SearchR1&max_results=3"`
2. 下载：`curl -L "https://arxiv.org/pdf/2503.09516.pdf" -o source/search-r1.pdf`
3. 翻译：按上方模板，slug=search-r1
4. 等待 5-10 分钟，查询进程和文件
5. 发邮件：python3 scripts/send_email.py 1074741503@qq.com "Search-R1 中文翻译" "附件" translated/search-r1.zh.dual.pdf

## 异步队列示例

```bash
# 添加任务
python3 /root/workspace/Remember/tasks/queue_manager.py add "https://arxiv.org/abs/2503.09516" "1074741503@qq.com" "Search-R1"

# 查看队列
python3 /root/workspace/Remember/tasks/queue_manager.py list

# cron 触发 worker（自动每3分钟检查）
# 或手动触发一次：
openclaw session spawn --agent-id arxiv_worker  # 内部用
```
