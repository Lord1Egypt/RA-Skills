# 腾讯 Skillhub 上架信息 · 邮件客服助手

---

## 基础信息

- **Skill名称**：邮件客服助手
- **副标题**：AI驱动的邮件智能分类与客服助手
- **分类**：办公效率 > 客服 > 邮件客服
- **Slug**: `email-customer-assistant`
- **定价 Token 前缀**：`EMAIL-FREE` / `EMAIL-STD` / `EMAIL-PRO` / `EMAIL-MAX`

---

## 详细功能描述

### 核心功能

**📥 邮件自动拉取**
- 通过IMAP协议连接任意邮箱（QQ邮箱、163邮箱、企业邮箱、Gmail等）
- 自动获取指定文件夹（默认INBOX）的新邮件
- 支持自定义检查间隔，灵活控制拉取频率

**🏷️ AI智能分类**
- 基于大语言模型对邮件内容进行语义分析
- 自动分类：咨询、投诉、订单、退款、技术支持、询价、合作、其他
- 支持自定义分类规则（PRO及以上套餐）

**🤖 回复建议生成**
- AI自动分析邮件内容，生成专业回复建议
- 支持多语言：中/英/日/韩（MAX套餐全语言支持）
- 用户确认后再发送，安全可控

**🔔 飞书推送**
- 紧急邮件实时推送（STD及以上套餐）
- 每日定时摘要卡片推送到飞书群或个人
- 支持关键词触发紧急判定（紧急、urgent、critical、宕机、故障等）

**📊 邮件摘要**
- 自动提取邮件关键信息：发件人、主题、摘要、紧急程度、建议分类
- 结构化输出，方便快速浏览

---

## 套餐说明

| 套餐 | 价格 | 功能权益 |
|------|------|----------|
| **FREE** | ¥0/月 | 邮件分类、飞书摘要推送（每日1次） |
| **STD** | ¥9.9/月 | + 回复建议生成、紧急邮件实时推送 |
| **PRO** | ¥29/月 | + 多邮箱支持、自定义分类规则 |
| **MAX** | ¥69/月 | + 全语言支持、API无限制、白标 |

### 功能对比表

| 功能 | FREE | STD | PRO | MAX |
|------|:----:|:---:|:---:|:---:|
| 邮件AI分类 | ✅ | ✅ | ✅ | ✅ |
| 飞书每日摘要 | ✅（每日1次） | ✅ | ✅ | ✅ |
| 回复建议生成 | ❌ | ✅ | ✅ | ✅ |
| 紧急邮件实时推送 | ❌ | ✅ | ✅ | ✅ |
| 多邮箱支持 | ❌ | ❌ | ✅ | ✅ |
| 自定义分类规则 | ❌ | ❌ | ✅ | ✅ |
| 全语言支持 | ❌ | ❌ | ❌ | ✅ |
| API无限制 | ❌ | ❌ | ❌ | ✅ |
| 白标 | ❌ | ❌ | ❌ | ✅ |

---

## 技术要求

### 系统要求
- Python 3.8 及以上
- 网络访问（IMAP + AI API）
- 已开启IMAP的邮箱账户

### Python依赖
```
imapclient>=2.3.0
email>=4.0.0
openai>=1.0.0
pyyaml>=6.0
requests>=2.28.0
```

### 配置项
- IMAP服务器地址/端口/认证信息
- AI API密钥（支持OpenAI/Claude/DeepSeek等兼容接口）
- 飞书Webhook地址或用户ID（用于推送）

---

## 上架前清理命令

上架前请运行以下命令清理测试数据：

```bash
# 删除测试配置文件（不删除 .example 模板）
cd /home/gem/workspace/agent/skills/email-customer-assistant/scripts
rm -f config.yaml test_emails.json debug.log

# 删除 __pycache__ 和缓存
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# 检查是否还有敏感信息
grep -r "password\|api_key\|token\|secret" --include="*.yaml" --include="*.py" --include="*.md" . || echo "No secrets found - OK"
```

---

## 快速开始

```bash
# 1. 进入脚本目录
cd /home/gem/workspace/agent/skills/email-customer-assistant/scripts

# 2. 安装依赖
pip install -r requirements.txt

# 3. 复制配置模板
cp config.yaml.example config.yaml
# 编辑 config.yaml，填入 IMAP、AI API、飞书推送配置

# 4. 单次运行
python check_emails.py

# 5. 设置定时任务（每小时检查一次）
crontab -e
# 添加：0 * * * * cd /home/gem/workspace/agent/skills/email-customer-assistant/scripts && python check_emails.py
```

---

## 文件结构

```
email-customer-assistant/
├── SKILL.md              # Skill定义
├── README.md             # 使用说明
├── CLAWHUB.md            # ClawHub上架信息（英文）
├── SKILLHUB.md           # 腾讯Skillhub上架信息（本文）
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

## 注意事项

1. **邮箱密码**：请使用邮箱"专用密码"（App Password），不要使用登录密码
2. **IMAP权限**：部分邮箱需要在设置中手动开启IMAP（如QQ邮箱、163邮箱）
3. **API额度**：建议设置 `max_tokens` 限制单次输出，避免过度消耗
4. **飞书Webhook**：Webhook地址只能往对应群推送，需先在飞书中添加自定义机器人
5. **检查频率**：`check_interval` 建议不低于60秒，避免触发频率限制
6. **数据安全**：配置文件中包含敏感信息，请勿提交到公开仓库
