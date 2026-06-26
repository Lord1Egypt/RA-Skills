# Agent Error Logger 🦞

记录 Agent 犯过的错误，避免重复踩坑。

## 安装

```bash
# 克隆到 skills 目录
cd /home/gem/workspace/agent/skills
git clone https://github.com/YOUR_USERNAME/agent-error-logger.git

# 在配置文件启用
# skills.entries 添加:
# "agent-error-logger": { "enabled": true }

# 重启服务
sh scripts/restart.sh
```

## 使用

### 记录错误

```bash
python scripts/record_error.py \
  --task "发布小红书" \
  --error "图片文件不存在" \
  --cause "用户只提供了 URL，未下载" \
  --fix "发布前先下载 URL 图片" \
  --tags "#文件校验 #图片处理"
```

### 搜索错误

```bash
# 按关键词搜索
python scripts/search_errors.py --keyword "小红书"

# 按标签搜索
python scripts/search_errors.py --tag "#文件校验"

# 限制结果数
python scripts/search_errors.py --tag "#网络超时" --limit 5
```

## 文件结构

```
workspace/memory/
├── error-patterns.md       # 错误模式索引（长期）
└── error-log-YYYY-MM.md    # 月度详细日志
```

## 功能

- ✅ 自动记录任务失败
- ✅ 识别重复错误模式
- ✅ 主动提醒相似错误
- ✅ 月度统计报告

## 示例输出

```
✓ 错误 #003 已记录到 error-log-2026-03.md
  标签：#文件校验 #图片处理

✓ 找到 2 个匹配的错误:

--- 错误 1 ---
文件：error-log-2026-03.md
编号：003
标题：浏览器工具超时
内容:
- **时间**: 2026-03-11 12:00
- **任务**: 访问 GitHub
- **错误**: browser.snapshot 超时
...
```

## License

MIT
