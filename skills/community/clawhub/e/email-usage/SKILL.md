---
name: email-usage
description: "使用本地邮件服务器收发我们自己域名的邮件。固定脚本位于 scripts/ 目录，直接执行即可。发送失败或密码遗忘时联系 小爪子。"
metadata: {"openclaw":{"emoji":"📧","requires":{"anyBins":["docker"]}}}
---

# Email 使用

## SMTP 发送（需要认证）

```bash
python3 skills/email-usage/scripts/send_email.py <收件人> <主题> <正文> <发件邮箱> <密码>
```

**参数**：收件人、主题、正文、发件邮箱、密码（向 小爪子 查询）

**示例**：
```bash
python3 skills/email-usage/scripts/send_email.py \
  'someone@example.com' '邮件标题' '邮件正文' \
  'test@axelhu.com' 'test1234'
```

## IMAP 读取

```bash
python3 skills/email-usage/scripts/read_email.py <用户名> <密码> [最新N封，默认5]
```

**示例**：
```bash
python3 skills/email-usage/scripts/read_email.py 'test@axelhu.com' 'test1234' 3
```

## 新增邮箱账号

```bash
python3 skills/email-usage/scripts/create_email.py <邮箱> <密码>
```

**示例**：
```bash
python3 skills/email-usage/scripts/create_email.py newuser@axelhu.com securepass
```

账号创建后，发件和收件使用同一套密码。

## 规则

- **不要**配置 SMTP/Postfix/amavis
- **不要**操作邮件队列（postqueue/postsuper）
- **不要**修改容器内配置
- 连接超时或发送失败 → 联系 小爪子
- 密码遗忘 → 联系 小爪子
