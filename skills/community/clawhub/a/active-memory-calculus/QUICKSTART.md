# 快速开始指南

## 5分钟快速上手

### 第一步：安装

```bash
# 从 ClawHub 安装
clawhub install active-memory-calculus

# 或使用 OpenClaw CLI
openclaw skills add active-memory-calculus
```

### 第二步：配置

```bash
# 一键配置脚本
openclaw skills configure active-memory-calculus --enable

# 或手动配置
openclaw config set plugins.entries.active-memory-calculus.config.enabled true
openclaw config set plugins.entries.active-memory-calculus.config.mode recent
openclaw gateway restart
```

### 第三步：验证

```bash
# 检查状态
openclaw skills status active-memory-calculus

# 预期输出:
# active-memory-calculus: enabled ✓
#   Mode: recent
#   Dreaming: enabled (20m interval)
```

## 立即体验

### 场景1：自动记忆偏好

```
你: 我喜欢看GeoGebra动画
AI: [自动记录偏好]

你: (下次对话) 讲一下导数
AI: [自动使用动画演示]
```

### 场景2：掌握度追踪

```
你: (连续做对5题)
AI: [自动标记熟练]

你: 再出一道极限题
AI: [自动提升难度]
```

### 场景3：错误预警

```
你: (多次犯同样错误)
AI: ⚠️ 注意！这是你的常见易错点...
```

## 查看梦境摘要

学习20分钟后，自动生成的摘要位于：

```bash
# 查看今日梦境
cat ~/obsidian/calculus-memory/dreams/DREAMS_$(date +%Y-%m-%d).md

# 查看知识图谱
cat ~/obsidian/calculus-memory/knowledge-graph/calculus_knowledge_graph.json
```

## 故障排除

### 问题：记忆未生效

```bash
# 检查配置
openclaw config get plugins.entries.active-memory-calculus.config.enabled

# 检查日志
openclaw logs --follow | grep active-memory
```

### 问题：梦境未生成

```bash
# 手动触发测试
python3 ~/.openclaw/skills/active-memory-calculus/tools/dream_generator.py test_data.json

# 检查目录权限
ls -la ~/obsidian/calculus-memory/
```

### 问题：工具脚本错误

```bash
# 检查 Python 版本
python3 --version  # 需要 >= 3.8

# 安装依赖
pip3 install -r requirements.txt  # 如果有
```

## 下一步

- 阅读完整文档: [SKILL.md](SKILL.md)
- 查看示例: [examples/](examples/)
- 了解集成: [examples/example_integration.md](examples/example_integration.md)
- 参与贡献: [GitHub](https://github.com/daigxok/active-memory-calculus)

## 获取帮助

- GitHub Issues: https://github.com/daigxok/active-memory-calculus/issues
- ClawHub 社区: https://clawhub.ai/community
- 邮件: daigxok@example.com
