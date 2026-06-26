---
name: batch-send-mail
description: 批量发送个性化邮件技能。读取表格（CSV/Excel）中的邮箱列表和变量，替换邮件模板中的占位符后批量发送邮件。支持 HTML 格式、通用附件、SMTP 配置和干运行预览模式。当用户需要批量发送个性化邮件、邮件营销、通知邮件时触发，即使他们说"批量发邮件"、"群发邮件"、"批量发送邮件"也要使用此技能。
compatibility: Requires Python 3.6+, pandas, openpyxl (for Excel)
---

# batch-send-mail

批量发送个性化邮件技能。根据表格数据批量发送带有个性化变量替换的邮件。

## 功能特点

- **支持多种表格格式**：CSV 和 Excel (.xlsx/.xls)
- **灵活的变量替换**：第一列为邮箱，后续列依次对应模板中的 {variable1}, {variable2}, ...
- **HTML 支持**：支持发送 HTML 格式的富文本邮件
- **通用附件**：支持给所有邮件添加相同的附件文件
- **干运行模式**：可先预览替换结果，确认无误后再实际发送
- **自动保存配置**：首次使用交互式输入 SMTP 配置，自动保存，后续无需重复输入
- **可配置 SMTP**：支持配置 SMTP 服务器（支持 Gmail、Outlook、QQ、163 等常见邮箱）

## 使用场景

- 批量发送会议邀请
- 个性化邮件营销
- 给客户发送通知
- 课程作业邮件通知
- 活动邀请函批量发送

## 工作流程

```
用户提供 → 表格文件 + 邮件模板 + SMTP配置
    ↓
技能读取表格数据
    ↓
逐个替换模板变量
    ↓
干运行模式：输出预览，不发送
实际发送：连接SMTP，批量发送
    ↓
发送完成报告统计
```

## 输入格式

### 1. 表格文件

| 收件邮箱              | 抄送邮箱              | variable1 | variable2 |
|----------------------|----------------------|-----------|-----------|
| alice@example.com    | bob@example.com\|charlie@example.com | Alice     | 产品A     |
| bob@example.com      |                      | Bob       | 产品B     |

- **第一列**：收件邮箱地址（必填）
- **第二列**：抄送邮箱地址，多个邮箱用 `|` 分隔，留空表示不抄送
- **第三列**：替换模板中的 `{variable1}`
- **第四列**：替换模板中的 `{variable2}`
- **以此类推...**

### 2. 邮件模板

邮件模板使用 `{variable1}`, `{variable2}`, ... 作为占位符：

```
您好 {variable1}！

感谢您购买我们的 {variable2}。

如果您有任何问题，请随时联系我们。

此致，
团队
```

### 3. SMTP 配置

需要提供以下信息：

- **SMTP 服务器地址**（如 `smtp.gmail.com`, `smtp.qq.com`）
- **SMTP 端口**（通常 587 用于 TLS，465 用于 SSL）
- **发件人邮箱**
- **授权码/密码**

## 常见 SMTP 配置参考

| 邮箱 | SMTP 服务器 | 端口 | 备注 |
|------|------------|------|------|
| Gmail | smtp.gmail.com | 587 | 需要应用专用密码 |
| Outlook/Office365 | smtp.office365.com | 587 | |
| QQ邮箱 | smtp.qq.com | 587 | 使用授权码而非密码 |
| 163邮箱 | smtp.163.com | 587 | 使用授权码而非密码 |

## 使用说明

1. **准备文件**
   - 准备好表格文件（CSV 或 Excel）
   - 准备好邮件模板（文本或 HTML）

2. **配置信息**
   - 提供邮件主题（固定）
   - 提供 SMTP 配置信息
   - 可选：添加通用附件文件路径

3. **干运行预览**
   - 先使用干运行模式生成预览
   - 检查变量替换是否正确

4. **发送邮件**
   - 确认预览无误后，执行实际发送
   - 等待发送完成，查看发送报告

## 示例

参见 `examples/` 目录：
- `example_contacts.csv` - 示例联系人表格
- `example_template.txt` - 示例邮件模板

## 执行脚本

主脚本位于 `scripts/batch_send_mail.py`

### 命令行用法

**首次使用**（自动交互式配置）：
```bash
python scripts/batch_send_mail.py \
  --table contacts.csv \
  --template email_template.txt \
  --subject "您的订阅已确认" \
  --dry-run
```

按提示输入 SMTP 配置后，配置会自动保存到 `config/config.ini`，**后续使用无需再输入 SMTP 信息**：

```bash
python scripts/batch_send_mail.py \
  --table contacts.csv \
  --template email_template.txt \
  --subject "您的订阅已确认" \
  --dry-run
```

参数说明：
- `--table` - 表格文件路径 (CSV 或 .xlsx)
- `--template` - 邮件模板文件路径
- `--subject` - 邮件主题
- `--smtp-server` - SMTP 服务器地址（可选，覆盖配置文件）
- `--smtp-port` - SMTP 端口（可选，覆盖配置文件，默认: 587）
- `--sender-email` - 发件人邮箱（可选，覆盖配置文件）
- `--sender-password` - 发件人密码/授权码（可选，覆盖配置文件）
- `--attachments` - 可选，通用附件文件路径，多个用空格分隔
- `--dry-run` - 干运行模式，只预览不发送
- `--html` - 标记模板为 HTML 格式（默认是纯文本）
- `--show-config` - 显示当前配置并退出

### 配置文件

配置文件保存在 `config/config.ini`，格式如下：

```ini
[smtp]
server = smtp.qq.com
port = 587
sender_email = your-email@qq.com
sender_password = your-auth-code-or-password
```

你可以直接编辑这个文件修改配置。

## 变量替换规则

- **第一列**：收件邮箱
- **第二列**：抄送邮箱（多个用 `|` 分隔）
- **第三列**：替换模板中的 `{variable1}`
- **第四列**：替换模板中的 `{variable2}`
- **以此类推...**
- 你也可以使用 `{v1}`, `{v2}...` 作为简写
- 如果模板中变量数量多于表格变量列数，缺失的变量会被替换为空字符串
- 如果表格变量列数多于模板变量数量，多余列会被忽略

