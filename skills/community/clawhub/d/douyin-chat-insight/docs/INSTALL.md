# 安装指南

## 写在前面

| 问题 | 答案 |
|------|------|
| 要不要阿里百炼 AppKey？ | **默认不要** |
| 要不要登录抖音/微信？ | **不要**（Skill 内） |
| 要不要先装 creator-insight？ | **不要** |
| 要不要 Docker？ | **不要** |
| 没有导出文件能分析吗？ | **不能**——请先自备导出 |

---

## 路径 A：全新用户（第一次装本系列任何 Skill）

### 1. 安装 Skill 文件

**发布后（ClawHub）：**

```bash
clawhub install douyin-chat-insight
```

**现在（源码）：**

```bash
git clone https://github.com/tars1230/douyin-chat-insight.git douyin-chat-insight
cd douyin-chat-insight
```

链到 Agent 能发现的目录，例如：

```bash
mkdir -p ~/.shared/skills
ln -sfn "$(pwd)" ~/.shared/skills/douyin-chat-insight
```

若使用 Hermes 多 Agent 链接脚本：

```bash
python3 ~/.shared/skills/publish-agent-skill/scripts/link_shared_skill.py douyin-chat-insight --apply
```

### 2. 首次配置（可选）

```bash
python3 scripts/setup.py
# 或非交互：
python3 scripts/setup.py --output-dir ~/Reports/douyin-chat-insight --owner-alias '你的昵称'
python3 scripts/setup.py --check
```

你会看到：

- 需要阿里百炼 AppKey: **否**
- 需要抖音登录: **否**

### 3. 准备一份导出

没有聊天文件就无法分析。任选：

1. 已有 ChatLab / JSONL
2. 第三方导出工具（见 `references/how-to-get-exports.md`）— **可选，非本包依赖**
3. 从客户端复制纪要另存为 `昵称: 内容` 文本

### 4. 跑通示例

```bash
python3 scripts/run.py --input tests/fixtures/sample_group.jsonl
python3 scripts/run.py --input tests/fixtures/sample_group.jsonl --conv 1
open output/douyin-chat-insight/latest.html   # macOS
```

### 5. 用你的数据

```bash
python3 scripts/run.py --input /path/to/your/export.jsonl
# 看概况表 → 选编号
python3 scripts/run.py --input /path/to/your/export.jsonl --conv 1 --owner-alias '群主昵称'
```

### 6. 在 Agent 对话里

> 用 douyin-chat-insight 分析这个导出：`/path/to/export`
> 先 inventory，不要直接深挖。

Agent 应 load 本 skill，遵守状态机。

---

## 路径 B：已经装过你的其他 Skill

例如已装 `douyin-creator-insight` 或收藏知识库。

### 会怎样？

1. **再装一份独立目录** `douyin-chat-insight`（不覆盖旧 skill）
2. **单独 setup**（输出目录建议不同，默认已是 `output/douyin-chat-insight`）
3. **不会**自动：
   - 读取收藏记录
   - 打开抖音 browser profile
   - 借用 creator 的 23:00 任务
   - 要求你再贴一次百炼 Key

### 可选复用

| 资源 | 行为 |
|------|------|
| `DASHSCOPE_API_KEY` 环境变量 | 核心路径仍不用；仅未来「分享视频转写」增强可能探测 |
| 已登录浏览器 profile | **不使用** |
| 导出工具已装在本机 | 你自己运行导出，把文件路径给本 skill |

### 建议命令

```bash
# 与 creator 并存
python3 scripts/setup.py --output-dir ~/Reports/douyin-chat-insight
python3 scripts/run.py -i /path/export --conv 1
```

---

## 校验安装成功

```bash
# 推荐：一键体检
python3 scripts/doctor.py

# 或分步
python3 -m unittest discover -s tests -v
python3 scripts/setup.py --check --json
python3 scripts/run.py -i tests/fixtures/sample_group.jsonl --json | head
```

期望：`doctor` 输出 `RESULT: READY`；`needs_bailian_appkey: false`。

---

## 常见失败

| 现象 | 处理 |
|------|------|
| `未指定会话` | 先 inventory，再 `--conv N` |
| 四块全空 | 检查是否全是系统消息/纯链接；放宽或换导出 |
| Agent 去登抖音 | 纠正路由：本 skill 禁止；见 routing-boundaries |
| 想分析公开主页 | 换 `douyin-creator-insight` |
| `doctor` FAIL | 看具体项：缺 fixture / 测试红 / 路径泄漏 |

---

## 卸载

删除 skills 目录中的 `douyin-chat-insight` 链接/文件夹。
可选删除 `~/.config/douyin-chat-insight/`。
不碰其他 skill 数据。
