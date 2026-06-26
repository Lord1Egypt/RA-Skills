# Auto Memory - OpenClaw 自动记忆更新 Skill

让你的 agent 拥有持久记忆，不再忘记之前的对话。

## 简介

OpenClaw 会自动记录所有对话到 session 文件（`.jsonl`），但 agent 不会主动读取历史 session。这个 skill 解决了这个问题：

- ✅ 自动从 session 提取重要对话
- ✅ 更新 memory 文件
- ✅ 重建向量索引
- ✅ 支持 heartbeat 自动触发

## 快速开始

```bash
# 安装
npx clawhub@latest install auto-memory

# 手动触发
~/.openclaw/scripts/extract-memory.sh main
```

## 工作原理

```
Session (.jsonl) → 提取重要内容 → memory/YYYY-MM-DD.md → 向量索引
```

详细文档请查看 [SKILL.md](./SKILL.md)

## 许可证

MIT