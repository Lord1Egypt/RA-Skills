# Exec Inspector - 快速开始指南

## 🎉 恭喜！工具已就绪

exec-inspector 已经安装完成并可以使用了！

## ⚡ 1 分钟快速设置

### 第一步：添加别名（可选但推荐）

将以下内容复制到你的终端配置文件：

**对于 Zsh 用户** (`~/.zshrc`):
```bash
echo "# OpenClaw Exec History 别名" >> ~/.zshrc
echo "alias exec-history='~/.openclaw/scripts/exec-history.sh'" >> ~/.zshrc
echo "alias exec-list='~/.openclaw/scripts/exec-history.sh list'" >> ~/.zshrc
echo "alias exec-stats='~/.openclaw/scripts/exec-history.sh stats'" >> ~/.zshrc
echo "alias exec-today='~/.openclaw/scripts/exec-history.sh today'" >> ~/.zshrc
echo "alias exec-search='~/.openclaw/scripts/exec-history.sh search'" >> ~/.zshrc
source ~/.zshrc
```

**对于 Bash 用户** (`~/.bashrc`):
```bash
echo "# OpenClaw Exec History 别名" >> ~/.bashrc
echo "alias exec-history='~/.openclaw/scripts/exec-history.sh'" >> ~/.bashrc
echo "alias exec-list='~/.openclaw/scripts/exec-history.sh list'" >> ~/.bashrc
echo "alias exec-stats='~/.openclaw/scripts/exec-history.sh stats'" >> ~/.bashrc
echo "alias exec-today='~/.openclaw/scripts/exec-history.sh today'" >> ~/.bashrc
echo "alias exec-search='~/.openclaw/scripts/exec-history.sh search'" >> ~/.bashrc
source ~/.bashrc
```

### 第二步：立即尝试

```bash
# 查看最近执行的命令
exec-list

# 或者直接使用脚本（不需要别名）
~/.openclaw/scripts/exec-history.sh list
```

## 📖 常用命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `exec-list` | 查看最近 20 条命令 | `exec-list` |
| `exec-stats` | 查看命令使用统计 | `exec-stats` |
| `exec-today` | 查看今天的命令 | `exec-today` |
| `exec-search <关键字>` | 搜索命令 | `exec-search git` |
| `exec-history session` | 查看所有 sessions | `exec-history session` |
| `exec-history all-tools` | 查看所有工具统计 | `exec-history all-tools` |
| `exec-history chart` | 查看执行时间线 | `exec-history chart` |

## 🎯 快速示例

### 示例 1：查看最近执行了什么

```bash
$ exec-list

📋 Recent exec commands (last 20):
  1. 2026-02-10 15:30:45 | ls -la
  2. 2026-02-10 15:28:12 | git status
  3. 2026-02-10 15:25:33 | npm install
  ...
```

### 示例 2：分析命令使用情况

```bash
$ exec-stats

📊 Command usage statistics:

   4  null
   3  ls
   3  claude
   2  mc
   2  cd
   ...

Total exec commands: 19
```

### 示例 3：查找 git 相关命令

```bash
$ exec-search git

🔍 Searching for commands containing: git

  1. 2026-02-10 15:28:12 | git status
  2. 2026-02-10 14:45:30 | git pull origin main
  3. 2026-02-10 12:20:15 | git commit -m "update"
```

## 🔧 依赖检查

确保已安装 `jq`（JSON 处理工具）：

```bash
# 检查是否已安装
jq --version

# macOS 安装
brew install jq

# Ubuntu/Debian 安装
sudo apt-get install jq
```

## 📚 完整文档

- [README.md](./README.md) - 详细使用说明
- [SKILL.md](./SKILL.md) - Skill 技术文档

## 💡 提示

1. **不需要别名也能用**：即使没有设置别名，你也可以直接运行 `~/.openclaw/scripts/exec-history.sh`
2. **查看帮助**：运行 `exec-history help` 查看所有可用命令
3. **AI 助手集成**：直接在 OpenClaw 对话中说 "查看最近的 exec 执行记录"，AI 会自动帮你运行相应命令

## 🎉 开始使用吧！

现在就试试运行 `exec-list` 查看你的命令历史！

---

有问题？查看 [README.md](./README.md) 或在 OpenClaw 中直接问 AI 助手！
