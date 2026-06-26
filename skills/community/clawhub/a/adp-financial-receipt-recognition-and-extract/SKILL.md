---
name: financial-receipt-recognition-and-extract
description: 支持增值税专用发票、增值税普通发票、增值税电子发票、出租车票、火车票、飞机行程单、过路费发票、定额发票、客运汽车票、财政票据等30+常见国内票据类型的自动分类与全量字段抽取，输出结构化JSON，零配置开箱即用，适用于费用报销、财务记账、发票验真、差旅报销自动化等场景。
---

# 中国地区30+常用发票抽取与发票查验 Skill

能力由来也科技 [ADP（Agentic Document Processing）智能体文档处理平台](https://adp.laiye.com/?utm_source=clawhub)提供，支持中国国内 30+ 种常见财务票据的自动分类识别与关键信息抽取能力。本 Skill 调用来也科技 ADP 官方 CLI 工具，一条命令即可完成各类票据图片/扫描件/PDF 的结构化字段抽取，输出标准 JSON，无缝对接业务系统。

> 新用户注册后，每月可获得 **100 免费积分**（每月刷新），约可支持 120–150 张国内票据的字段抽取。ADP 以标准化商用 API 形式交付，业务系统最快 1 小时即可完成集成。即日起，前 100 名注册新用户在使用国内票据抽取功能时，还可在免费积分基础上**额外获得 1000 页免费处理额度**，帮助企业以更低门槛验证并落地 ADP 的文档处理能力。
</br> 立即注册：[中国大陆](https://adp.laiye.com/?utm_source=clawhub) | [海外地区](https://adp-global.laiye.com/?utm_source=clawhub)

---

## 快速接入指南

### 核心工作流

1. **安装依赖**：首次执行时，安装 ADP CLI 工具。
2. **认证配置**：首次执行时，运行 `adp config get` 检查凭证。若未配置，提示用户提供 API Key。
3. **获取应用列表**：首次执行时，通过 `adp app-id list --app-type 0` 获取开箱即用应用列表，找到国内票据抽取应用并记录其 `app_id`（以 `ootb_` 开头）。后续优先使用 `adp app-id cache`。
4. **执行抽取**：运行 `adp extract url <URL> --app-id <国内票据抽取应用ID>` 或 `adp extract local <文件路径> --app-id <国内票据抽取应用ID>`。
5. **结果处理**：解析返回的 JSON，系统自动识别票据类型并抽取对应字段（发票代码、发票号码、开票日期、购买方、销售方、金额、税额、价税合计、票据子类型等结构化字段）。
6. **错误处理**：命令失败时，解析 stderr JSON 确定错误类型和恢复操作。

### 支持的票据类型与验真能力

ADP 国内票据抽取**自动分类 + 全量抽取**一次完成，覆盖 **32 种常见票据类型**，其中 **11 种支持税局验真**（抽取的同时自动向**国家税务总局全国增值税发票查验平台**发起验真请求，结果以 `fpVerification` / `fpVerificationMsg` / `fpIsVoided` 三个字段直接返回在同一个 JSON 中，**无需二次调用，无需自行对接税局接口**）。每种票据返回的 `field_key` 集合不同，请根据 `document_type` / `type` 字段判断票据类型后再解析。

> 完整票据类型清单（32 种）与字段明细见：[examples/supported-invoice-types.md](examples/supported-invoice-types.md)

**常见票据类型 `type_key` 速查（✅ = 支持税局验真）**

| 票据类型 (`type_key`) | 票据名称 | 验真 |
| --- | --- | :---: |
| `vat_special_invoice` | 增值税专用发票 | ✅ |
| `vat_common_invoice` | 增值税普通发票 | ✅ |
| `vat_electronic_invoice` / `vat_electronic_invoice_new` | 电子普通发票（含全电） | ✅ |
| `vat_electronic_special_invoice` / `vat_electronic_special_invoice_new` | 电子专用发票（含全电） | ✅ |
| `vat_roll_invoice` | 增值税卷票 | ✅ |
| `taxi_ticket` | 出租车发票 | — |
| `train_ticket` | 火车票 | — |
| `electronic_train_ticket` | 铁路电子客票 | ✅ |
| `air_transport` | 机票行程单 | — |
| `electronic_air_transport` | 航空运输电子客票行程单 | ✅ |
| `vehicle_toll` | 过路过桥费 / 通行费 | — |
| `motor_vehicle_sale_invoice` | 机动车销售统一发票 | ✅ |
| `used_car_purchase_invoice` | 二手车销售统一发票 | ✅ |
| `quota_invoice` | 通用定额发票 | — |
| `medical_invoice` / `medical_electronic_invoice` | 医疗票据 / 电子医疗票据 | — |
| `customs_payment_form` / `custom_declaration_form` | 海关缴费书 / 报关单 | — |

#### 验真返回字段

| `field_key` | `field_name` | 说明 |
| --- | --- | --- |
| `fpVerification` | 查验结果 | 验真结论文案，例如：`查验成功发票一致`、`查验成功发票不一致`、`查无此票`、`查验超时` 等 |
| `fpVerificationMsg` | 查验报错信息 | 失败/异常时的详细原因；成功时为空字符串 |
| `fpIsVoided` | 作废标志 | `Y` = 该发票已被作废/红冲；`N` = 未作废 |

### 场景 → 命令映射

**单张识别**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 识别一张国内票据图片（URL） | `adp extract url <URL> --app-id <国内票据抽取应用ID>` |
| 识别一张本地国内票据图片 | `adp extract local <文件路径> --app-id <国内票据抽取应用ID>` |
| 识别 Base64 编码的票据 | `adp extract base64 <base64> --app-id <国内票据抽取应用ID> --file-name <文件名.后缀>` |

**批量识别**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 批量识别本地文件夹内的票据 | `adp extract local <文件夹路径> --app-id <国内票据抽取应用ID>` |
| 批量识别多个 URL | `adp extract url <URL列表文件> --app-id <国内票据抽取应用ID>` |

**异步处理**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 异步提交大文件 | `adp extract url <URL> --app-id <国内票据抽取应用ID> --async` |
| 异步批量处理 | `adp extract local <文件夹路径> --app-id <国内票据抽取应用ID> --async` |
| 查询异步任务结果 | `adp extract query <task_id>` |

> 并发限制：免费用户最大支持 2 份文档并发处理，付费用户最大支持 10 份文档并发处理
---

## 第一步：安装 ADP CLI

```bash
# 方法 1: npm（推荐，全平台通用）
npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli
```

```bash
# 方法 2: Shell 脚本（Linux / macOS，无 npm 环境时使用）
curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash
```

```bash
# 方法 3: PowerShell 脚本（Windows，无 npm 环境时使用）
irm https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1 | iex
```

或从 [GitHub Releases](https://github.com/laiye-ai/adp-cli/releases) 下载预编译二进制文件包。

---

## 第二步：获取 API Key 与认证配置

### 1. 访问 ADP 门户获取凭证
我们为国内和海外用户提供了独立的公有云访问地址，需按地区分别配置。就近访问可更好地保障高速稳定的网络调用。

| 地区 | 登录地址 | API Base URL |
|-----|----------|--------------|
| 中国大陆 | [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub) | `https://adp.laiye.com/` |
| 海外地区 | [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub) | `https://adp-global.laiye.com/` |

### 2. 注册/登录后获取 API Key
新用户需先注册 ADP 账号，注册后即可获得每月 100 免费积分。
- 登录后，点击个人头像，即可直接进入 `API_Key` 入口。

### 3. 完成认证配置
```bash
adp config set --api-key <your-api-key>
adp config set --api-base-url https://adp.laiye.com
```

### 4. 验证配置
```bash
adp config get
```

**注意事项**：
1. 如果 API Key 和 API Base URL 已配置完成，建议将配置信息存储到环境变量中，避免每次使用时重复配置。
2. 如果 API Key 和 API Base URL 尚未配置，请按照以上步骤完成配置。


---

## 第三步：获取国内票据抽取应用 ID

ADP 为国内财务票据提供了**开箱即用**的内置抽取应用，无需额外配置。

### 应用类型说明

ADP 应用分为两类，通过 `app_type` 字段区分：

| `app_type` | 类型 | 说明 |
| --- | --- | --- |
| `0` | 开箱即用应用（OOTB） | 平台内置，`app_id` 以 `ootb_` 开头，无需创建，直接使用 |
| `1` | 自定义应用 | 用户自行创建的抽取应用，`app_id` 为用户自定义标识 |

国内票据识别属于**开箱即用应用**，可通过 `--app-type 0` 筛选查询。

### 查询并筛选国内票据应用

```bash
# 仅查询开箱即用应用（推荐）
adp app-id list --app-type 0

# 或查询所有应用
adp app-id list
```

从返回列表中找到 `app_label` 包含 **"国内票据"** 或 **"增值税"** 的应用，记录其 `app_id`：

```json
[
  {
    "app_id": "ootb_******k4m7",
    "app_label": ["国内票据", "增值税发票", "财务凭证", "报销", "信息提取"],
    "app_name": "国内票据",
    "app_type": 0
  }
]
```

> 上例中 `"app_id": "ootb_******k4m7"` 即为国内票据抽取应用。`app_type` 为 `0` 表示开箱即用应用，`1` 表示自定义应用。

### 缓存应用 ID（推荐）

首次查询后，后续优先使用缓存避免重复请求：

```bash
# 后续使用缓存
adp app-id cache
```

**重要提示**：每个账号下的 `app_id` 是唯一且固定的，除非用户主动删除应用，否则 `app_id` 不会变更。建议 Agent 将国内票据应用的 `app_id` 保存在上下文中，下次直接使用。

---

## 第四步：执行国内票据抽取

### 单张票据抽取（URL）

```bash
adp extract url https://example.com/receipt.jpg --app-id <国内票据抽取应用ID>
```

### 单张票据抽取（本地文件）

```bash
adp extract local ./receipt.jpg --app-id <国内票据抽取应用ID>
```

### 单张票据抽取（Base64）

```bash
adp extract base64 <base64字符串> --app-id <国内票据抽取应用ID> --file-name <文件名.后缀>
```

### 返回结果示例

ADP 国内票据抽取统一返回结构化 JSON，系统**自动识别票据类型**（外层 `field_key` 即为「支持的票据类型与字段」表中的 `type_key`），抽取字段位于 `object_values[].extraction_result` 数组中。

以下以**电子发票（普通发票）** `vat_electronic_invoice_new` 为例，基于真实返回结果脱敏（购销方名称、纳税人识别号、发票号码、开票人等敏感字段已使用 `*` 遮挡），包含**全量抽取字段 + 验真字段**。未识别到的字段返回空字符串 `""`，置信度为 `0.0`。

**完整 JSON 示例** → [examples/vat-electronic-invoice-new.json](examples/vat-electronic-invoice-new.json)

下方为结构骨架示意（仅保留前 2 个字段，省略其余字段值）：

```json
[
  {
    "field_key": "vat_electronic_invoice_new",
    "field_name": "电子发票（普通发票）",
    "object_values": [
      {
        "document_type": "vat_electronic_invoice_new",
        "pages": [0],
        "extraction_result": [
          { "field_key": "vat_invoice_haoma_right_side", "field_name": "发票号码", "field_values": [{ "field_value": "254320000000********", "field_confidence": 0.99, "references": [] }] },
          { "field_key": "vat_invoice_issue_date_print", "field_name": "开票日期", "field_values": [{ "field_value": "2025-04-16",            "field_confidence": 0.99, "references": [] }] },
          // ... 约 30 个普通字段（详见 examples/vat-electronic-invoice-new.json）

          { "field_key": "goods", "field_name": "项目详情", "table_values": [[ /* 8 个明细子字段 */ ]] },

          { "field_key": "fpVerification",    "field_name": "查验结果",     "field_values": [{ "field_value": "查验成功发票一致", "confidence": 1.0 }] },
          { "field_key": "fpVerificationMsg", "field_name": "查验报错信息", "field_values": [{ "field_value": "",                 "confidence": 1.0 }] },
          { "field_key": "fpIsVoided",        "field_name": "作废标志",     "field_values": [{ "field_value": "N",                "confidence": 1.0 }] }
        ],
        "metadata": { "confidence": 1.0 }
      }
    ]
  }
]
```

> **脱敏说明**：以上示例中的发票号码、纳税人识别号、购销方名称、开票人姓名均做了 `*` 遮挡处理；真实返回中这些字段为完整明文，集成时请按贵司数据安全规范决定是否对外展示。

> **关键观察**：上例最后三个字段 `fpVerification` / `fpVerificationMsg` / `fpIsVoided` 即为**税局查验结果**，与抽取字段一起返回，无需二次调用。

### 返回字段说明：

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `[].field_key` | string | 票据类型标识，对应 `type_key`（如 `vat_electronic_invoice_new`） |
| `[].field_name` | string | 票据类型人类可读名称 |
| `[].object_values[]` | array | 同一票种的实例（多页/多票时多条） |
| `[].object_values[].document_type` | string | 票据类型，同外层 `field_key` |
| `[].object_values[].pages` | array&lt;number&gt; | 命中的 PDF 页码（0-based） |
| `[].object_values[].extraction_result[]` | array | 抽取字段数组（普通字段 + 表格字段 + 验真字段混合） |
| `[].object_values[].metadata.confidence` | number | 该票据整体置信度 0–1 |
| **普通字段（单值）** | | |
| `extraction_result[].field_key` | string | 字段标识（机器可读，参考 [字段表](#支持的票据类型与字段)） |
| `extraction_result[].field_name` | string | 字段名称（人类可读） |
| `extraction_result[].field_values[]` | array | 抽取结果数组（通常一项） |
| `extraction_result[].field_values[].field_value` | string | 抽取值，未识别到时为空字符串 `""` |
| `extraction_result[].field_values[].field_confidence` | number | 字段置信度 0–1，未识别为 `0.0` |
| `extraction_result[].field_values[].references` | array | 字段在原文档中的位置引用（OCR bbox 等），目前返回空数组 `[]` |
| **表格字段（如 `goods` 项目详情）** | | |
| `extraction_result[].table_values` | array&lt;array&lt;object&gt;&gt; | 表格二维数组：外层为行，内层为单元格 |
| `extraction_result[].table_values[][]` | object | 单元格对象，结构同普通字段（含 `field_key` / `field_name` / `field_values`） |
| **验真字段（`fpVerification` / `fpVerificationMsg` / `fpIsVoided`）** | | |
| `extraction_result[].field_values[].field_value` | string | 查验结果文本 / 报错信息 / 作废标志（`Y`/`N`） |
| `extraction_result[].field_values[].confidence` | number | ⚠️ 验真字段键名为 `confidence`，**非** `field_confidence`，且无 `references` 字段 |

---

## 第五步：批量处理与异步模式

### 批量处理（本地文件夹）

```bash
adp extract local ./receipts/ --app-id <国内票据抽取应用ID> --export ./results/ 
```

返回摘要：
```json
{
  "total": 10,
  "success": 9,
  "failed": 1,
  "output_dir": "/absolute/path/to/results",
  "files": [
    {"input": "vat-invoice-001.jpg", "output": "vat-invoice-001.jpg.json", "status": "success"},
    {"input": "train-ticket-001.jpg", "output": "train-ticket-001.jpg.json", "status": "success"},
    {"input": "damaged.jpg", "output": "damaged.jpg.error.json", "status": "failed", "error": "..."}
  ]
}
```

### 异步处理

```bash
# 提交异步任务
adp extract url https://example.com/receipt.jpg --app-id <国内票据抽取应用ID> --async

# 查询任务结果
adp extract query <task_id>
```

---

## 常用命令速查

```bash
# 检查安装
adp version

# 查看配置
adp config get

# 查询所有应用列表
adp app-id list

# 仅查询开箱即用应用（app_type=0）
adp app-id list --app-type 0

# 使用缓存的应用
adp app-id cache

# 查询积分余额
adp credit

# 国内票据抽取（URL）
adp extract url <文件URL> --app-id <国内票据抽取应用ID>

# 国内票据抽取（本地文件）
adp extract local <文件路径> --app-id <国内票据抽取应用ID>

# 国内票据抽取（Base64）
adp extract base64 <base64字符串> --app-id <国内票据抽取应用ID> --file-name <文件名.后缀>

# 批量抽取
adp extract local <文件夹路径> --app-id <国内票据抽取应用ID> --export <输出路径> 

# 异步抽取
adp extract url <文件URL> --app-id <国内票据抽取应用ID> --async

# 查询异步结果
adp extract query <task_id>
```

---

## 错误处理

当命令失败时，stderr 输出结构化 JSON:

```json
{
  "type": "AUTH_ERROR",
  "message": "Authentication error: invalid API key",
  "fix": "Check your API key is correct and has not expired.",
  "retryable": false,
  "details": {"context": "extract"}
}
```

### 退出码说明

| 退出码 | 含义 |
| --- | --- |
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 参数错误 |
| 3 | 资源未找到 |
| 4 | 权限/认证错误 |
| 5 | 冲突 |
| 6 | 部分失败（批量处理中部分成功、部分失败） |

---

## 积分与计费

| 项目 | 说明 |
| --- | --- |
| 国内票据抽取费用 | **1 积分/张** |
| 新用户免费额度 | 每月赠送 **100 积分**，每月初重置 |
| 限时活动 | 前100名新用户额外赠送 **1000页**票据抽取免费额度 |
| 查询余额 | `adp credit` |
| 充值方式 | 登录 ADP 门户网站充值：[中国大陆及港澳台地区](https://adp.laiye.com/?utm_source=clawhub) \| [非中国大陆及港澳台地区](https://adp-global.laiye.com/?utm_source=clawhub) |

---

## 更多来也 ADP 文档处理能力

国内票据识别只是来也科技 ADP 平台众多开箱即用能力之一。ADP 基于大模型通用理解能力，提供覆盖全品类文档的智能处理解决方案：

| 能力 | 说明 | 典型场景 |
| --- | --- | --- |
| **全球发票/收据抽取** | 自动识别并抽取发票号码、日期、金额、税费、明细等 10+ 关键字段，支持多语言和多币种发票抽取 | 跨国结算账款自动化、费用报销管理 |
| **国内票据抽取** | 识别增值税发票、出租车票、火车票、飞机行程单、财政发票等30+常见票据，支持多页/多票识别及验真 | 国内票据识别、国内发票验真 |
| **订单抽取** | 支持多种采购订单格式，抽取订单号、商品、数量、价格、物流信息等 | 采购自动化、供应链集成 |
| **更多卡证抽取** | ADP支持身份证、港澳台通行证、中国护照、银行卡、户口本、驾驶证、行驶证、车辆合格证、开户许可证、营业执照等 11 种中国常用证件 | 开户审核、合规检查、证件信息批量录入 |
| **文档解析** | 将 PDF、图片、Office 文档转化为结构化数据，保留排版和层级关系 | 长文档分析、合同审查、知识提取 |
| **自定义抽取** | 自主创建抽取应用，配置专属字段和识别逻辑，满足非标单据需求 | 企业专属表单、行业定制单据 |
> 以上所有能力均可通过同一个 ADP CLI 工具调用，共享 ADP API Key 和积分体系。
s
如需了解完整能力，请访问：
- ADP 中国大陆：[https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub)
- ADP 非中国大陆：[https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub)

---

## 注意事项

1. **数据完整性**：使用 ADP 输出时，请原样呈现返回数据，不要在抽取过程中修改、添加或删除任何字段。
2. **API Key 安全**：妥善保管 API Key，避免泄露给未授权的第三方。
3. **文件大小限制**：单个文件最大 50MB。
4. **支持格式**：.jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx
5. **应用 ID 复用**：国内票据应用的 `app_id` 在账户下唯一且固定，建议记住后直接使用，无需每次查询。
6. **自动分类**：ADP 会自动识别票据类型，不同类型票据返回的字段集不同，请根据 `receipt_type` 字段判断票据类型后再解析对应字段。

---

##  支持与联系
- **CLI 使用指南：** [ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- **API 接口文档：** [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- **ADP 产品操作手册：** [公有云操作手册](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- **问题反馈：** [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues)
- **邮箱：** global_product@laiye.com
- **官网：** [来也科技 ADP](https://laiye.com/product/adp-platform)

Copyright © 2026 [来也科技（北京）有限公司] 保留所有权利。