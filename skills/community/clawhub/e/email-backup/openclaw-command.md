# OpenClaw 一键安装命令

## 方法一：直接发送命令给 OpenClaw

在 OpenClaw 聊天界面中发送以下命令：

```
安装 email-backup skill
```

或者：

```
请帮我安装 Email Backup Skill，用于打包文件并发送到QQ邮箱
```

## 方法二：使用 OpenClaw 命令行

在终端中执行：

```bash
# 安装 Email Backup Skill
openclaw skill install email-backup

# 或者从本地安装
openclaw skill install ./email-backup-skill.tar.gz
```

## 方法三：使用 OpenClaw 脚本

创建一个 OpenClaw 脚本文件：

```bash
# 创建脚本目录
mkdir -p ~/.openclaw/scripts

# 创建安装脚本
cat > ~/.openclaw/scripts/install-email-backup.sh << 'EOF'
#!/bin/bash
# Email Backup Skill 安装脚本

echo "🚀 开始安装 Email Backup Skill..."

# 检查 OpenClaw
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装"
    exit 1
fi

# 创建 skills 目录
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
mkdir -p "$SKILLS_DIR"

# 下载 Skill（这里需要替换为实际的下载地址）
cd "$SKILLS_DIR"
echo "📥 正在下载 Email Backup Skill..."
# curl -L -o email-backup-skill.tar.gz https://example.com/email-backup-skill.tar.gz
# tar -xzf email-backup-skill.tar.gz

echo "✅ Email Backup Skill 安装完成！"
echo "📖 使用说明：请查看 SKILL.md 文件"
EOF

# 设置执行权限
chmod +x ~/.openclaw/scripts/install-email-backup.sh

# 执行安装
~/.openclaw/scripts/install-email-backup.sh
```

## 方法四：使用 OpenClaw 配置文件

在 OpenClaw 配置文件中添加 Skill：

```json
{
  "skills": {
    "email-backup": {
      "enabled": true,
      "path": "~/.openclaw/workspace/skills/email-backup",
      "autoLoad": true
    }
  }
}
```

## 方法五：使用 OpenClaw 插件系统

如果 OpenClaw 支持插件系统，可以创建一个插件：

```javascript
// ~/.openclaw/plugins/email-backup.js
module.exports = {
  name: 'email-backup',
  version: '1.0.0',
  description: 'QQ邮箱文件备份Skill',
  
  install: async function(openclaw) {
    console.log('正在安装 Email Backup Skill...');
    
    // 下载 Skill
    const skillUrl = 'https://example.com/email-backup-skill.tar.gz';
    const skillPath = `${openclaw.config.skillsDir}/email-backup`;
    
    // 安装逻辑
    // ...
    
    console.log('Email Backup Skill 安装完成！');
  },
  
  uninstall: async function(openclaw) {
    console.log('正在卸载 Email Backup Skill...');
    // 卸载逻辑
  }
};
```

## 方法六：使用 OpenClaw 命令模板

创建一个 OpenClaw 命令模板：

```yaml
# ~/.openclaw/commands/install-email-backup.yaml
name: install-email-backup
description: 安装 Email Backup Skill
command: |
  echo "🚀 开始安装 Email Backup Skill..."
  
  # 检查环境
  if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装"
    exit 1
  fi
  
  # 创建目录
  mkdir -p ~/.openclaw/workspace/skills
  
  # 下载 Skill
  cd ~/.openclaw/workspace/skills
  echo "📥 正在下载 Email Backup Skill..."
  # curl -L -o email-backup-skill.tar.gz https://example.com/email-backup-skill.tar.gz
  # tar -xzf email-backup-skill.tar.gz
  
  echo "✅ Email Backup Skill 安装完成！"
  
  # 显示使用说明
  echo ""
  echo "📖 使用说明："
  echo "1. 配置 QQ 邮箱"
  echo "2. 设置环境变量"
  echo "3. 使用命令：python3 scripts/backup_and_send.py /path/to/directory"
```

## 方法七：使用 OpenClaw 一键安装命令

在 OpenClaw 聊天界面中发送：

```
请执行以下命令安装 Email Backup Skill：

1. 创建 skills 目录：mkdir -p ~/.openclaw/workspace/skills
2. 下载 Skill：cd ~/.openclaw/workspace/skills && curl -L -o email-backup-skill.tar.gz https://example.com/email-backup-skill.tar.gz
3. 解压：tar -xzf email-backup-skill.tar.gz
4. 测试：cd email-backup && python3 scripts/backup_and_send.py --help
```

## 推荐方法

**推荐使用方法一或方法二**，因为：

1. **简单直接**：用户只需要发送一个命令
2. **自动化程度高**：OpenClaw 会自动处理安装过程
3. **错误处理**：OpenClaw 会自动处理安装过程中的错误
4. **用户友好**：不需要用户手动执行复杂的命令

## 注意事项

1. **网络连接**：安装过程需要网络连接
2. **权限问题**：可能需要管理员权限
3. **依赖检查**：确保 Python 3.6+ 已安装
4. **QQ邮箱配置**：安装后需要配置 QQ 邮箱 SMTP 授权码

## 故障排除

### 问题 1：OpenClaw 未安装

```bash
# 安装 OpenClaw
npm install -g openclaw
```

### 问题 2：Python 未安装

```bash
# Ubuntu/Debian
sudo apt install -y python3

# CentOS/RHEL
sudo yum install -y python3
```

### 问题 3：网络连接问题

```bash
# 使用代理
export https_proxy=http://proxy:port
export http_proxy=http://proxy:port
```

### 问题 4：权限不足

```bash
# 使用 sudo
sudo openclaw skill install email-backup
```

## 获取帮助

如果安装过程中遇到问题，可以：

1. 查看 OpenClaw 官方文档：https://docs.openclaw.ai
2. 加入 OpenClaw 社区：https://discord.com/invite/clawd
3. 提交 Issue：https://github.com/openclaw/openclaw/issues