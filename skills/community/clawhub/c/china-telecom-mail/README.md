# China Telecom Mail Skill for OpenClaw

A skill to read and summarize emails from China Telecom mailbox via POP3.

## Quick Start

### 1. Install the Skill

Copy the entire `china-telecom-mail` folder to your OpenClaw skills directory:

```bash
# On Linux/macOS
cp -r china-telecom-mail ~/.openclaw/skills/

# On Windows
# Copy to C:\Users\<yourusername>\.openclaw\skills\china-telecom-mail
```

### 2. Configure Credentials

Edit the `config.toml` file in the skill directory:

```bash
cd ~/.openclaw/skills/china-telecom-mail
nano config.toml
```

修改配置内容：
```toml
[email]
server = "pop.chinatelecom.cn"
port = 995
username = "your_email@chinatelecom.cn"
password = "your_password"
```

### 3. Use the Skill

**列出今日邮件摘要：**
```bash
openclaw run --skill china-telecom-mail list-today
```

**读取指定邮件（按 ID）：**
```bash
openclaw run --skill china-telecom-mail read 21
```

**JSON 格式输出（适合自动化）：**
```bash
openclaw run --skill china-telecom-mail json-summary
```

**统计今日邮件数量：**
```bash
openclaw run --skill china-telecom-mail count
```

### 4. 直接用 Python 运行

```bash
uv run python ~/.openclaw/skills/china-telecom-mail/main.py list-today
```

## Directory Structure

```
china-telecom-mail/
├── SKILL.md          # OpenClaw skill 元数据
├── main.py           # 主程序
├── config.toml       # 配置文件（修改这个文件配置账号密码）
├── config.toml.example  # 配置模板
└── README.md         # 使用说明
```

## Requirements

- Python 3.8+
- uv (Python package manager)
- OpenClaw

## Features

- 列出今日邮件并显示摘要
- 读取完整邮件内容
- JSON 输出（适合自动化）
- 支持纯文本和 HTML 邮件
- 自动识别中文编码（GBK/UTF-8）
- 支持配置文件和环境变量两种配置方式

## Security Notes

- 不要将 config.toml 提交到版本控制
- 如果使用 Git，添加到 .gitignore：
```bash
echo "config.toml" >> .gitignore
```

## Troubleshooting

**连接被拒绝：**
- 检查 POP3 服务器是否可访问
- 确认端口 995 未被防火墙阻止

**认证失败：**
- 验证用户名和密码
- 中国电信可能需要使用授权码而非登录密码

**乱码问题：**
- Skill 已自动处理常见中文编码（GBK、UTF-8）
- 如果仍看到乱码，检查原始邮件编码
