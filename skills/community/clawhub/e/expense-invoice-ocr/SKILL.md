---
name: expense_invoice_ocr
description: 支持识别企业财务报销场景的19 种常见票据，包括：增值税发票,增值税卷票,出租车发票,火车票,航空运输电子客票行程单,机动车销售统一发票,定额发票,过路过桥费发票,医疗发票,税收完税证明,船票,非税票据,通用机打发票,汽车票,值税通行费发票,网约车行程单,银联POS签购单,医疗住院发票,医疗费用结算单识别。仅在用户明确要求识别某张本地票据图片时触发，调用前必须确认用户同意上传该文件到 Scnet 远程 OCR 服务。
version: 1.0.8
author: SCNet
license: MIT
tags:
  - OCR
  - 证件识别
  - 发票识别
  - 文字提取
required_env_vars:
  - SCNET_API_KEY
optional_env_vars:
  - SCNET_API_BASE
primary_credential: SCNET_API_KEY
dependencies:
  - python3
  - requests
permissions:
  - filesystem/read: 读取用户指定的本地图片/PDF 文件
  - network/outbound: 向 Scnet OCR API (api.scnet.cn) 上传文件并接收识别结果
input:
  - ocrType : 识别类型，可选值见下文
  - filePath : 待识别图片的本地路径
output: 结构化的 JSON 数据，包含识别结果和置信度
---
# Sugon-Scnet 通用 OCR 技能

> **⚠️ 数据安全警告**：本技能会将您指定的本地票据、发票、行程单、医疗单据等文件**完整上传**到第三方远程 OCR 服务 `https://api.scnet.cn`。这些文件可能包含个人身份信息（PII）、纳税人识别号、银行账号、金额、病史等敏感内容。请在每次调用前确认：
> 1. 该文件不包含受监管或机密信息；
> 2. 您或您所在的组织已授权将此类数据发送至 Scnet；
> 3. 您明确同意本次上传。
> 如不符合以上任一条件，请勿使用本技能。

本技能封装了 Sugon-Scnet 企业财务报销 OCR 服务，通过单一接口即可调用 19 种识别能力，高效提取文字及票据信息。

## 功能特性

- **财务票据**：覆盖增值税发票,增值税卷票,出租车发票,火车票,航空运输电子客票行程单,机动车销售统一发票,定额发票,过路过桥费发票,医疗发票,税收完税证明,船票,非税票据,通用机打发票,汽车票,值税通行费发票,网约车行程单,银联POS签购单,医疗住院发票,医疗费用结算单识别，自动提取关键字段。

## 前置配置

> **⚠️ 重要**：使用前需要申请 Scnet API Token

### 申请 API Token

1. 访问 [Scnet 官网](https://www.scnet.cn) 注册/登录
2. 在控制台申请 API 密钥（格式：`sc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
3. 复制密钥备用

### 配置 Token

**手动配置（推荐）**
1. 在技能目录下创建 `config/.env` 文件，内容如下：
```ini
# =====  Sugon-Scnet OCR API 配置 =====
# 申请地址：https://www.scnet.cn
SCNET_API_KEY=your_scnet_api_key_here

# API 基础地址（一般无需修改）
SCNET_API_BASE=https://api.scnet.cn/api/llm/v1
```
2. 添加：`SCNET_API_KEY=你的密钥`
3. 设置文件权限为 600（仅所有者可读写）
**⚠️ 安全警告**：切勿将 API Key 直接粘贴到聊天对话中，否则可能被记录或泄露。

### Token 更新

Token 过期后调用会返回 401 或 403 错误。更新方法：重新申请 Token 并替换 config/.env 中的 SCNET_API_KEY。

### 依赖安装

本技能需要 Python 3.6+ 和 requests 库。请运行以下命令：

```bash
   pip install requests
```
---
### 使用方法

### 参数说明

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| ocrType | string | 是 | 识别类型枚举。必须为以下之一：<br>• UNIFIED_IDENTIFICATION_OF_FINANC（财务票据统一识别）<br>• VAT_INVOICE（增值税发票）<br>• VAT_TOLL_INVOICE（增值税通行费发票）<br>• VAT_ROLL_INVOICE（增值税卷票）<br>• TAXI_INVOICE（出租车发票）<br>• TRAIN_TICKET（火车票）<br>• AIRPORT_TICKET（航空运输电子客票行程单）<br>• VEHICLE_SALE_INVOICE（机动车销售统一发票）<br>• QUOTA_INVOICE（定额发票）<br>• TOLL_INVOICE（过路过桥费发票）<br>• MEDICAL_INVOICE（医疗发票）<br>• MEDICAL_INPATIENT_INVOICE（医疗住院发票）<br>• MEDICAL_EXPENSE_SETTLEMENT（医疗费用结算单）<br>• TAX_CERTIFICATE（税收完税证明）<br>• NON_TAX_BILL（非税票据）<br>• GENERAL_MACHINE_INVOICE（通用机打发票）<br>• SHIP_TICKET（船票）<br>• BUS_TICKET（汽车票）<br>• RIDE_HAILING_ITINERARY（网约车行程单）<br>• UNIONPAY_POS_RECEIPT（银联POS签购单） |
| filePath | string | 是 | 待识别图片的本地绝对路径。支持 jpg、png、pdf 等常见格式。 |

### 命令行调用示例

```bash
   python .claude/skills/expense_invoice_ocr/scripts/main.py VAT_INVOICE /path/to/invoice.jpg
```

### 在 AI 对话中使用

为避免自动触发导致用户文件被意外上传，**不要**仅根据关键词自动调用本技能。AI 必须在满足以下全部条件后再执行：

1. 用户明确请求识别/提取某张**具体本地文件**的票据信息；
2. 用户已确认了解并同意将 `filePath` 指向的文件上传到 Scnet 远程 OCR 服务；
3. 用户已确认该文件不包含其组织禁止外发的机密、受监管或敏感信息。

只有在用户给出明确同意（例如回复“确认上传并识别”）后，才可调用本技能。

示例场景：

- 用户说“提取这张发票的信息，路径是 /Users/name/Downloads/fapiao.png”，AI 应回复：“我将把 `/Users/name/Downloads/fapiao.png` 上传到 Scnet OCR 服务进行识别。该文件可能包含敏感财务信息，请确认您同意上传且该文件可外传。确认后请回复‘确认上传并识别’。”
- 用户明确回复“确认上传并识别”后，AI 再调用本技能。

### AI 调用建议
为避免触发 API 速率限制（10 QPS），请串行调用本技能，即等待前一个识别完成后再发起下一个请求。
如果使用 OpenClaw 的 exec 工具，建议设置 timeout 或 yieldMs 参数，让命令同步执行，避免多个命令同时运行导致并发。

### 配置选项

编辑 `config/.env` 文件：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| SCNET_API_KEY | 必需 | Scnet API 密钥 |
| SCNET_API_BASE | https://api.scnet.cn/api/llm/v1 | API 基础地址（一般无需修改） |

### 输出

- 标准输出：识别结果的 JSON 数据，结构与 API 文档一致，位于 `data` 字段内。
- 识别结果位于 data[0].result[0].elements 中，具体字段取决于 ocrType。
- 错误信息：如果发生错误，会输出以 `错误:` 开头的友好提示。

### 注意事项

- 本技能调用的 OCR API 有 10 QPS 的速率限制。
- 如果遇到 429 错误，请等待 2-3 秒后重试，不要连续发起请求。
- 建议在调用前确保图片已准备就绪，避免因网络问题导致重复调用。

### 故障排除

| 问题 | 解决方案 |
|------|----------|
| 配置文件不存在 | 创建 config/.env 并填入 Token（参考前置配置） |
| API Key 无效/过期 | 重新申请 Token 并更新 `.env` 文件 |
| 文件不存在 | 检查提供的文件路径是否正确 |
| 网络连接失败 | 检查网络连接或防火墙设置 |
| 不支持的文件类型 | 确保文件扩展名为允许的类型（参考 API 文档） |
| 401/403/Unauthorized | Token 无效或过期，重新申请并配置 |
| 429 Too Many Requests | 请求过于频繁，技能会自动等待并重试（最多 3 次）。若持续失败，请降低调用频率或联系服务方提高限额。 |

