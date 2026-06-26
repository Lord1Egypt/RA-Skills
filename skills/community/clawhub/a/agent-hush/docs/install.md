# Agent Hush 安装指南

按以下步骤安装 Agent Hush：

## 1. 安装 Skill

```bash
clawhub install agent-hush
```

如果 `clawhub` 未安装，先执行：

```bash
npm install -g clawhub
```

## 2. 验证安装

```bash
python3 ~/.openclaw/workspace/skills/agent-hush/scripts/sanitize.py scan . --quiet
```

如果输出 `✅ No sensitive data found!` 或 `⚠️ Found X sensitive items`，说明安装成功。

## 3. 没有第三步

装完后你不需要做任何事。Agent 会在你推代码、发布 Skill 时自动检查。

---

安装遇到问题？提 Issue：https://github.com/elliotllliu/agent-hush/issues
