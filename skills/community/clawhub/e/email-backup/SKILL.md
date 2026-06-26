---
name: email-backup
description: QQ邮箱文件备份Skill - 打包文件并发送到QQ邮箱
metadata:
  emoji: 📧
  requires:
    bins: ["python3"]
    env: []
  primaryEnv: ""
license: MIT
---

# Email Backup Skill

QQ邮箱文件备份Skill，可以将指定目录打包成压缩包，并通过QQ邮箱SMTP发送到指定邮箱。

## 🚀 OpenClaw 安装此 Skill 指南

### 方法一：通过 ClawHub 安装（推荐）

如果你的 OpenClaw 已配置 ClawHub，可以直接安装：

```bash
# 搜索 Skill
clawhub search email-backup

# 安装 Skill
clawhub install email-backup
```

### 方法二：直接发送命令给 OpenClaw

在 OpenClaw 聊天界面中发送以下命令：

```
安装 email-backup skill
```

或者：

```
请帮我安装 Email Backup Skill，用于打包文件并发送到QQ邮箱
```

**OpenClaw 会自动执行以下操作：**
1. 检查 Python 是否安装
2. 创建 skills 目录
3. 下载并解压 Skill 文件
4. 设置执行权限
5. 测试安装是否成功

### 方法三：使用 OpenClaw 命令行

在终端中执行：

```bash
# 安装 Email Backup Skill
openclaw skill install email-backup

# 或者从本地安装
openclaw skill install ./email-backup-skill.tar.gz
```

### 方法四：手动安装

1. **下载 Skill 文件**
   ```bash
   # 创建 skills 目录（如果不存在）
   mkdir -p ~/.openclaw/workspace/skills
   
   # 下载并解压
   cd ~/.openclaw/workspace/skills
   tar -xzf email-backup-skill.tar.gz
   ```

2. **验证安装**
   ```bash
   # 检查文件结构
   ls -la ~/.openclaw/workspace/skills/email-backup/
   
   # 应该看到：
   # SKILL.md
   # README.md
   # scripts/
   ```

3. **测试运行**
   ```bash
   # 测试脚本是否正常工作
   cd ~/.openclaw/workspace/skills/email-backup
   python3 scripts/backup_and_send.py --help
   ```

## 📦 依赖说明

### 必需依赖

- **Python 3.6+**：脚本运行环境
- **tarfile 模块**：Python 内置模块，用于创建 tar.gz 压缩包（无需额外安装）
- **smtplib 模块**：Python 内置模块，用于 SMTP 邮件发送（无需额外安装）

### 可选依赖

- **QQ邮箱 SMTP 授权码**：用于发送邮件（需要在 QQ 邮箱设置中获取）

### 为什么不需要额外安装压缩工具？

本 Skill 使用 Python 内置的 `tarfile` 模块来创建 tar.gz 压缩包，**不需要安装额外的压缩工具**（如 tar、gzip 等）。`tarfile` 模块是 Python 标准库的一部分，所有 Python 安装都自带此模块。

**优势：**
- ✅ 无需安装额外软件
- ✅ 跨平台兼容（Windows、Linux、macOS）
- ✅ 纯 Python 实现，无外部依赖
- ✅ 支持压缩级别调节（1-9）


## 功能特性

- ✅ 支持打包任意目录为tar.gz压缩包
- ✅ 支持QQ邮箱SMTP发送（SSL加密）
- ✅ 支持敏感信息清理（API Key、密码等）
- ✅ 支持自定义邮件主题和正文
- ✅ 支持批量发送多个文件

## 安装要求

1. Python 3.6+
2. QQ邮箱SMTP授权码（需要在QQ邮箱设置中开启SMTP服务并获取授权码）

## 配置

### 1. 获取QQ邮箱SMTP授权码

1. 登录QQ邮箱 (mail.qq.com)
2. 进入「设置」→「账户」
3. 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」
4. 开启「IMAP/SMTP服务」
5. 生成授权码（16位字母数字组合）

### 2. 配置环境变量

```bash
# 设置QQ邮箱配置
export QQ_EMAIL="your-email@qq.com"
export QQ_SMTP_PASSWORD="your-auth-code"

# 或者直接在脚本中修改配置
```

## 使用方法

### 基本用法

```bash
# 打包目录并发送到邮箱
python3 scripts/backup_and_send.py /path/to/directory

# 指定收件人
python3 scripts/backup_and_send.py /path/to/directory --to recipient@qq.com

# 自定义邮件主题
python3 scripts/backup_and_send.py /path/to/directory --subject "我的备份文件"

# 清理敏感信息后发送
python3 scripts/backup_and_send.py /path/to/directory --clean
```

### 高级用法

```bash
# 打包多个目录
python3 scripts/backup_and_send.py /path/to/dir1 /path/to/dir2

# 排除特定文件
python3 scripts/backup_and_send.py /path/to/directory --exclude "*.log" "*.tmp"

# 设置压缩级别（1-9，9为最高压缩率）
python3 scripts/backup_and_send.py /path/to/directory --compression 9
```

## 脚本说明

### 1. backup_and_send.py

主脚本，整合打包和发送功能。

**参数：**
- `directories`: 要打包的目录（支持多个）
- `--to`: 收件人邮箱（默认：发件人邮箱）
- `--subject`: 邮件主题
- `--body`: 邮件正文
- `--clean`: 清理敏感信息
- `--exclude`: 排除的文件模式
- `--compression`: 压缩级别（1-9）

### 2. clean_sensitive.py

敏感信息清理脚本，用于清理API Key、密码等敏感信息。

**支持清理的敏感信息：**
- API Keys（sk-*, tvly-*等）
- 密码（PASSWORD=*, password=*等）
- 邮箱密码
- 用户ID
- 其他自定义敏感信息

### 3. send_email.py

邮件发送脚本，支持QQ邮箱SMTP发送。

**参数：**
- `--to`: 收件人邮箱
- `--subject`: 邮件主题
- `--body`: 邮件正文
- `--attachment`: 附件路径

## 安全注意事项

1. **不要将授权码提交到代码仓库**
2. **使用环境变量存储敏感信息**
3. **定期更换授权码**
4. **清理备份文件中的敏感信息**

## 示例

### 备份OpenClaw配置

```bash
# 备份OpenClaw配置并发送到邮箱
python3 scripts/backup_and_send.py ~/.openclaw/agents ~/.openclaw/workspace --clean
```

### 定期备份脚本

```bash
#!/bin/bash
# daily_backup.sh

# 设置环境变量
export QQ_EMAIL="your-email@qq.com"
export QQ_SMTP_PASSWORD="your-auth-code"

# 备份目录
BACKUP_DIRS=(
    "~/.openclaw/agents"
    "~/.openclaw/workspace"
    "~/important-docs"
)

# 执行备份
python3 ~/.openclaw/workspace/skills/email-backup/scripts/backup_and_send.py \
    "${BACKUP_DIRS[@]}" \
    --subject "每日备份 $(date +%Y-%m-%d)" \
    --clean
```

## 故障排除

### 1. SMTP连接失败

- 检查网络连接
- 确认SMTP服务器地址和端口
- 检查防火墙设置

### 2. 认证失败

- 确认授权码是否正确
- 检查邮箱是否开启了SMTP服务
- 尝试重新生成授权码

### 3. 附件过大

- QQ邮箱附件限制为50MB
- 考虑分卷压缩或使用云存储

## 更新日志

### v1.0.0 (2026-03-06)
- 初始版本
- 支持QQ邮箱SMTP发送
- 支持敏感信息清理
- 支持批量打包和发送

## 许可证

MIT License

## 作者

Author 🌸
