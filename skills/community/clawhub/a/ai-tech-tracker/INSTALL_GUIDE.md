# AI技术动向追踪 Skill 安装指南

## 快速安装

### 使用安装脚本（推荐）

```bash
# 1. 进入 Skill 目录
cd /path/to/ai-tech-tracker

# 2. 运行安装脚本
./install.sh

# 3. 重启 Claude Code
```

### 手动安装

```bash
# 1. 创建 Claude Code skills 目录
mkdir -p ~/.claude/skills

# 2. 复制 Skill 到该目录
cp -r /path/to/ai-tech-tracker ~/.claude/skills/

# 3. 重启 Claude Code
```

## 验证安装

安装完成后，启动 Claude Code 并测试：

```
用户：帮我整理一下本周AI领域的最新动态
```

或

```
用户：最近OpenAI和Google有什么新发布？
```

## 常见问题

### Q1: Skill 没有被识别

检查清单：
- [ ] SKILL.md 文件存在
- [ ] 目录名与 SKILL.md 中的 `name` 字段一致
- [ ] 目录权限正确

解决方法：
```bash
# 检查文件
cat ~/.claude/skills/ai-tech-tracker/SKILL.md

# 检查权限
chmod -R 755 ~/.claude/skills/ai-tech-tracker
```

### Q2: 如何更新 Skill

```bash
# 直接覆盖
cp -rf ai-tech-tracker ~/.claude/skills/

# 重启 Claude Code
```

### Q3: 如何卸载 Skill

```bash
rm -rf ~/.claude/skills/ai-tech-tracker
```

## 许可证

MIT License
