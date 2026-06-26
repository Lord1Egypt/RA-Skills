---
name: zeelin-deep-research
description: 调用Zeelin Deep Research API进行深度研究任务。完全异步处理：提交任务后立即返回，后台进程自动确认大纲并定时检查任务状态，任务完成后自动保存md文件。自动配置定时通知（每2分钟检查），任务完成后主动通知用户。使用前必须先询问用户思考模式和搜索范围。
---

# Zeelin Deep Research Skill

本skill用于调用Zeelin Deep Research API执行深度研究任务，采用完全异步处理模式。

## ⚠️ 重要：使用前必须先询问用户

当用户要求进行研究任务时，**必须先询问以下信息**：

1. **思考模式**（必选）：
   | 模式 | 说明 | 适用场景 |
   |------|------|----------|
   | smart | 普通模式 | 快速简单的问题 |
   | deep | 深度模式 (~5000字) | 论文、竞品调研、中度报告 |
   | major | 专家模式 (~10000+字) | 深度研究报告 |

2. **搜索范围**（必选）：
   | 范围 | 说明 |
   |------|------|
   | web | 全网搜索 |
   | academic | 学术搜索 |
   | selected | 精选 |

3. **研究主题**（必选）：用户想要研究的具体问题

## 配置 API Key

### 方式1：命令行设置（推荐）
```bash
python3 scripts/async_runner.py --set-key "YOUR_API_KEY"
```

### 方式2：配置文件
```bash
echo '{"api_key": "YOUR_API_KEY"}' > ~/.openclaw/zeelin-config.json
```

获取 API Key：https://desearch.zeelin.cn

## 使用方法

### 1. 检查 API Key
```bash
python3 scripts/async_runner.py --check-key
```

### 2. 提交任务
```bash
cd ~/.openclaw/workspace/skills/zeelin-deep-research
python3 scripts/async_runner.py -q "研究主题" -t deep -sr web
```

## 功能特性

1. **异步提交**：提交任务后立即返回，不阻塞
2. **自动确认大纲**：后台进程自动调用 confirmOutline
3. **定时检查**：每30秒检查一次任务状态
4. **自动通知**：cron 定时（每2分钟）检查任务完成状态，任务完成后主动通知用户
5. **自动保存**：完成后自动保存 md 文件到 /tmp/

## 结果文件

任务完成后，md 文件自动保存到：
```
~/.openclaw/workspace/skills/zeelin-deep-research/reports/zeelin_主题_时间戳.md
```

## Cron 定时器

- **间隔**：每1分钟
- **功能**：检查任务完成状态
- **通知**：任务完成后主动发送消息给用户
