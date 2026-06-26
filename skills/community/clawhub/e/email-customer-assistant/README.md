# Email Customer Assistant · 邮件客服助手

AI驱动的邮件智能分类与客服助手，自动连接邮箱IMAP，智能分类邮件，生成回复建议，推送摘要到飞书。

---

## 功能介绍

- 📥 **邮件拉取**：通过IMAP协议自动连接邮箱，获取最新邮件
- 🏷️ **智能分类**：基于AI对邮件进行分类（咨询、投诉、订单、退款、技术支持等）
- 🤖 **回复建议**：AI生成多语言回复建议（中/英/日/韩），用户确认后再发送
- 🔔 **飞书推送**：紧急邮件实时推送，每日定时摘要卡片推送到飞书
- 📊 **摘要生成**：自动提取邮件关键信息，生成结构化摘要

---

## 安装步骤

```bash
# 进入脚本目录
cd /home/gem/workspace/agent/skills/email-customer-assistant/scripts

# 安装Python依赖
pip install -r requirements.txt
```

---

## 配置说明

### 1. 复制配置模板

```bash
cp config.yaml.example config.yaml
```

### 2. 配置邮箱IMAP

编辑 `config.yaml`：

```yaml
imap:
  host: "imap.example.com"        # IMAP服务器地址
  port: 993                        # IMAP端口（SSL通常是993）
  username: "your@email.com"       # 邮箱账号
  password: "your_app_password"    # 邮箱专用密码（非登录密码）
  folders:
    - "INBOX"                      # 要检查的文件夹
  check_interval: 300              # 检查间隔（秒）
```

### 3. 配置AI API

```yaml
ai:
  provider: "openai"               # 或 "claude", "deepseek"
  api_key: "sk-xxxx"               # API密钥
  model: "gpt-4o-mini"             # 使用的模型
  base_url: "https://api.openai.com/v1"  # API地址（自托管用）
  max_tokens: 1000
  temperature: 0.7
```

### 4. 配置飞书推送

**方式一：Webhook（适合群聊）**

```yaml
feishu:
  webhook:
    url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"  # Webhook地址
    secret: ""                       # 签名密钥（如有）
```

**方式二：用户ID推送（适合单聊）**

```yaml
feishu:
  user_push:
    user_id: "ou_xxxxxxxx"          # 飞书用户Open ID
    app_token: "your_app_token"     # 飞书应用token
```

**紧急邮件规则**

```yaml
feishu:
  urgent_keywords:
    - "紧急"
    - "urgent"
    - "critical"
    - "宕机"
    - "故障"
  realtime_push: true               # 实时推送紧急邮件
  daily_digest: true                # 每日摘要推送
  digest_time: "09:00"              # 每日推送时间
```

---

## 快速开始

### 运行邮件检查（单次）

```bash
cd /home/gem/workspace/agent/skills/email-customer-assistant/scripts
python check_emails.py
```

### 设置定时任务（每小时检查一次）

```bash
crontab -e
# 添加以下行：
# 0 * * * * cd /home/gem/workspace/agent/skills/email-customer-assistant/scripts && python check_emails.py >> /var/log/email_assistant.log 2>&1
```

### 集成到OpenClaw

在OpenClaw中配置定时任务或工作流，调用 `check_emails.py` 脚本。

---

## 套餐说明

| 套餐 | 价格 | 功能 |
|------|------|------|
| FREE | ¥0 | 邮件分类、飞书摘要推送（每日1次） |
| STD | ¥9.9/月 | + 回复建议生成、紧急邮件实时推送 |
| PRO | ¥29/月 | + 多邮箱支持、自定义分类规则 |
| MAX | ¥69/月 | + 全语言支持、API无限制、白标 |

---

## 注意事项

1. **邮箱密码**：强烈建议使用邮箱"专用密码"（App Password），不要使用登录密码
2. **IMAP权限**：确保邮箱开启了IMAP服务，部分邮箱（如QQ邮箱）需要在设置中手动开启
3. **API额度**：AI回复生成会消耗API额度，建议设置 `max_tokens` 限制单次输出
4. **飞书Webhook**：Webhook地址只能往对应群推送，需要先在飞书中添加自定义机器人
5. **频率限制**：建议 `check_interval` 不低于60秒，避免触发邮箱服务频率限制
6. **数据安全**：配置文件包含敏感信息，请勿提交到公开仓库

---

## 文件结构

```
email-customer-assistant/
├── SKILL.md              # Skill定义文件
├── README.md             # 本文件
├── CLAWHUB.md            # ClawHub上架信息
├── SKILLHUB.md           # 腾讯Skillhub上架信息
└── scripts/
    ├── requirements.txt   # Python依赖
    ├── config.yaml.example # 配置模板
    ├── imap_client.py     # IMAP连接模块
    ├── classifier.py       # AI分类模块
    ├── check_emails.py    # 主检查脚本
    ├── feishu_pusher.py   # 飞书推送模块
    └── reply_generator.py # 回复生成模块
```

---

## 技术支持

如有问题，请提交Issue或联系开发者。
-e 
> 如需购买收费版，请访问 [YK-Global.com](https://yk-global.com)
