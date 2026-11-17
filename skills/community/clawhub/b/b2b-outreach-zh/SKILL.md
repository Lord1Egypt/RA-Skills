---
name: b2b-outreach-zh
description: "B2B触达工具集：批量发送冷邮件与全球短信、采集Google Maps商户、并在触达前校验联系方式（手机/WhatsApp、邮箱、域名）。监控邮件/短信送达状态、清洗CRM联系人列表、开展端到端跨境触达活动。\n\nTrigger: 批量冷邮件, 发邮件, 邮件打开率追踪, 企业域名邮箱, 出口商群发邮件, 全球批量短信, 双向短信回复, 短信送达报告, 跨境短信营销, Google地图商户采集, 商户数据下载, 半径线索搜索, 经销商寻源, 手机号校验, WhatsApp状态检测, 邮箱校验, 域名有效性安全检测, CRM数据清洗, 群发短信预校验, B2B触达活动"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🚀","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# B2B 触达（Outreach）

聚合技能：**邮件** + **短信** + **地图商户采集** + **联系方式校验**。11 个脚本，扁平结构（脚本数少，直接列出，不加索引层）。

## 概览

四大能力组：

| 分组 | 脚本 | 用途 |
|------|------|------|
| 邮件 | mail_send, mail_task_list, mail_task_record_list | 批量冷邮件 + 送达跟踪 |
| 短信 | sms_send, sms_task_list, sms_task_record_list | 全球短信（双向）+ 送达跟踪 |
| 地图商户 | merchants_search, geography_list | Google Maps 商户数据采集 |
| 校验 | phone_validity_check, email_validity_check, domain_validity_check | 触达前清洗/校验联系方式 |

## 运行脚本

### 环境准备

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`

**重要**：始终用直接调用方式，如 `python scripts/mail_send.py`。**不要**用 `cd scripts && python mail_send.py` 这类 shell 复合命令。

## 脚本

### 邮件

#### `mail_send.py` - 发送邮件
向一个或多个收件人发送邮件。
- **参数**：见 [Email Send API](references/email-send-api.md)
```bash
python scripts/mail_send.py \
  --subject "Test Email" \
  --content "This is the email content" \
  --emails '["recipient@example.com"]'
```

#### `mail_task_list.py` - 邮件任务列表
查看邮件任务，支持时间范围/状态过滤。
- **参数**：见 [Email Task List API](references/email-task-list-api.md)
```bash
python scripts/mail_task_list.py --page_no 1 --page_size 10
```

#### `mail_task_record_list.py` - 邮件任务记录
查看某邮件任务的送达明细记录。
- **参数**：见 [Email Task Record List API](references/email-task-record-list-api.md)
```bash
python scripts/mail_task_record_list.py --task_id 1496 --page_no 1 --page_size 10
```

### 短信

#### `sms_send.py` - 发送短信
向手机号发送短信；`--channel_type 1` 开启双向（可回复）模式。
- **参数**：见 [SMS Send API](references/sms-send-api.md)
```bash
python scripts/sms_send.py \
  --content "This is SMS content" \
  --phones '["13800138000"]'
```

#### `sms_task_list.py` - 短信任务列表
- **参数**：见 [SMS Task List API](references/sms-task-list-api.md)
```bash
python scripts/sms_task_list.py --page_no 1 --page_size 10
```

#### `sms_task_record_list.py` - 短信任务记录
- **参数**：见 [SMS Task Record List API](references/sms-task-record-list-api.md)
```bash
python scripts/sms_task_record_list.py --task_id 1496 --page_no 1 --page_size 10
```

### 地图商户

#### `merchants_search.py` - 商户搜索
按关键词 + 地点搜索 Google Maps 商户。两种模式：国家/省/市搜索，或附近搜索（经纬度 + 半径，用 `geoDistance`）。
- **参数**：见 [Merchants Search API](references/merchants-search-api.md)
```bash
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"countryCodes":["BR"]}' \
  --query_count 100
```

#### `geography_list.py` - 地理列表
获取国家/省/市 ID，用于构造 `merchants_search` 参数。
```bash
python scripts/geography_list.py --type country
python scripts/geography_list.py --type province --country_id 1
python scripts/geography_list.py --type city --country_id 1
```
- 国家列表：[country-list](references/country-list-api.md) | 省份列表：[province-list](references/province-list-api.md) | 城市列表：[city-list](references/city-list-api.md)

### 联系方式校验

#### `phone_validity_check.py` - 手机号校验
校验手机号有效性、类型及 WhatsApp 注册状态。
- **参数**：见 [Phone Validity API](references/validity-phone-api.md)
```bash
python scripts/phone_validity_check.py --phones "+8613812345678 +14155551234"
```

#### `email_validity_check.py` - 邮箱校验
校验邮箱地址有效性/可送达性。
- **参数**：见 [Email Validity API](references/validity-email-api.md)
```bash
python scripts/email_validity_check.py --emails "a@example.com b@example.com"
```

#### `domain_validity_check.py` - 域名校验
校验域名有效性与安全性。
- **参数**：见 [Domain Validity API](references/validity-domain-api.md)
```bash
python scripts/domain_validity_check.py --domains "example.com foo.org"
```

## 核心工作流：触达前先校验

本聚合技能的标志性工作流（清洗 -> 触达 -> 监控）：

1. **收集联系方式** - 从 CRM 导出，或用 `merchants_search`（地图）采集，或由 `b2b-lead-generation`（决策人查询）提供。
2. **校验清洗** - 跑 `phone_validity_check` / `email_validity_check` / `domain_validity_check` 剔除无效联系方式。（减少浪费的发送与费用。）
3. **触达** - `mail_send`（冷邮件）和/或 `sms_send`（全球短信，双向可回复）。
4. **监控送达** - `mail_task_list` / `sms_task_list` -> `*_task_record_list` 查看送达状态。

> 校验本身也收费 -- 但远比发给无效联系方式划算。先告知用户校验费用。

## API 密钥与充值

本技能需要 API 密钥，存储在 `~/.upkuajing/.env`：
```bash
cat ~/.upkuajing/.env
```
```
UPKUAJING_API_KEY=your_api_key_here
```

### 未设置 API 密钥
先检查 `~/.upkuajing/.env` 是否有 `UPKUAJING_API_KEY`。若没有，提示用户选择：
1. 用户已有：用户提供（手动写入 `~/.upkuajing/.env`）
2. 用户没有：用 `auth.py --new_key` 申请（自动保存到 `~/.upkuajing/.env`）

等待用户选择。

### 账户充值
当 API 返回余额不足时：
1. 创建充值订单（`auth.py --new_rec_order`）
2. 把支付页面 URL 发给用户，引导其打开并支付；用户确认成功后再继续。

### 获取账户信息
`python scripts/auth.py --account_info`

新申请的密钥需在 [跨境魔方开放平台](https://developer.upkuajing.com/) 注册绑定。

### **上报Skill调用异常**
当API调用失败或返回异常数据（服务端错误、超时、响应格式错误等）时，先用自然语言向用户解释异常情况，并询问是否需要上报给平台追踪；用户确认后才执行上报：
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/mail/send","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"邮件发送失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 计费

**发送/搜索/校验调用均收费**；任务列表与记录列表查询免费。

**最新定价**：访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)，或运行：
```bash
python scripts/auth.py --price_info
```
（返回全部接口定价 -- 聚合版 auth.py 优先拉取全量定价列表，必要时回退到按原始技能名逐一查询。）

### 计费规则（概要）
- **邮件/短信发送**：按发送请求计费，费用随收件人数量递增。
- **商户搜索**：按调用次数计费，每次返回最多 100 条 -> 调用次数 = `ceil(query_count / 100)`。
- **手机/邮箱/域名校验**：按校验次数计费（每个号码/邮箱/域名）。
- **免费**：`geography_list`；所有 `*_task_list` / `*_task_record_list`。
- 各接口计费细则见对应 `references/<xxx>-api.md`。

### 计费确认原则

**任何收费操作必须先告知用户并在单独的消息中等待明确确认，不得在通知的同一消息中执行。** 当 `query_count` 超过一页时，先告知用户预计调用次数。

## 错误处理

- **API 密钥无效/不存在**：检查 `~/.upkuajing/.env` 中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数无效**：**必须先查 `references/` 下对应 API 文档**，从文档获取正确参数名/格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API 文档参考

**邮件**
- [email-send](references/email-send-api.md) | [email-task-list](references/email-task-list-api.md) | [email-task-record-list](references/email-task-record-list-api.md)

**短信**
- [sms-send](references/sms-send-api.md) | [sms-task-list](references/sms-task-list-api.md) | [sms-task-record-list](references/sms-task-record-list-api.md)

**地图商户**
- [merchants-search](references/merchants-search-api.md) | [country-list](references/country-list-api.md) | [province-list](references/province-list-api.md) | [city-list](references/city-list-api.md)

**校验**（加 `validity-` 前缀，与 email-send 等营销文档区分）
- [validity-phone](references/validity-phone-api.md) | [validity-email](references/validity-email-api.md) | [validity-domain](references/validity-domain-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 注意事项

- 邮件/短信发送为**同步提交、异步送达**：API 立即返回；通过任务记录查看 `status`。邮件状态：`0`-待发送 `1`-发送中 `2`-发送完成。短信状态：`1`-发送中 `2`-发送完成 `3`-失败 `4`-部分成功。
- `task_data/` 按 UUID 子目录存放结果。
- 国家代码使用 ISO 3166-1 alpha-2（如 CN、US、BR）。地图搜索关键词/行业须用**英文**。
- 所有平台文件路径使用正斜杠。
- **禁止输出技术参数格式**：回复中把代码式参数转为自然语言。
- **不要**估算每次调用费用 -- 用 `auth.py --price_info` 获取准确定价。
- **不要**猜测参数名 -- 先读 `references/<xxx>-api.md`。

## 关联技能

其他可能有用的 UpKuaJing 技能：

- b2b-lead-generation - 海关贸易情报、全球企业深度背调、LinkedIn 职业人脉（找待触达的线索）
- upkuajing-email-tool - 独立的邮件发送与任务跟踪
- upkuajing-sms-tool - 独立的短信发送与任务跟踪
- upkuajing-map-merchants-search - 独立的 Google Maps 商户采集
- upkuajing-contact-info-validity-check - 独立的联系方式校验（phone/email/domain）
- upkuajing-customs-trade-company-search（= upkuajing-trade-company-search）- 搜索有真实海关贸易记录的公司
- upkuajing-company-people-search（= upkuajing-global-company-people-search）- 快速浅层查公司/人 + 联系方式
