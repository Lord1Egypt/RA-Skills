---
name: id-card-recognition-and-extract
description: 基于来也科技ADP平台的中国居民身份证智能识别与信息抽取Skill。支持身份证正反面8大关键字段的精准抽取——姓名、性别、民族、出生、住址、身份证号码、签发机构、有效期限，输出结构化JSON，零配置开箱即用，适用于身份核验、信息录入、开户审核等场景。
---

# 身份证识别与抽取 Skill

能力由来也科技 [ADP（Agentic Document Processing）智能体文档处理平台](https://adp.laiye.com/?utm_source=clawhub)提供，支持中国居民身份证的智能识别与关键信息抽取能力。本 Skill 调用来也科技 ADP 官方 CLI 工具，一条命令即可完成身份证图片/扫描件的结构化字段抽取，输出标准 JSON，无缝对接业务系统。

---

## 快速接入指南

### 核心工作流

1. **安装依赖**：首次执行时，安装 ADP CLI 工具。
2. **认证配置**：首次执行时，运行 `adp config get` 检查凭证。若未配置，提示用户提供 API Key。
3. **获取应用列表**：首次执行时，通过 `adp app-id list --app-type 0` 获取开箱即用应用列表，找到身份证抽取应用并记录其 `app_id`（以 `ootb_` 开头）。后续优先使用 `adp app-id cache`。
4. **执行抽取**：运行 `adp extract url <URL> --app-id <身份证抽取应用ID>` 或 `adp extract local <文件路径> --app-id <身份证抽取应用ID>`。
5. **结果处理**：解析返回的 JSON，提取姓名、性别、民族、出生、住址、身份证号码、签发机构、有效期限等结构化字段（无论正面、反面还是正反面复印在同一页，均统一返回完整 8 字段）。
6. **错误处理**：命令失败时，解析 stderr JSON 确定错误类型和恢复操作。

### 场景 → 命令映射

**单张识别**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 识别一张身份证图片（URL） | `adp extract url <URL> --app-id <ID>` |
| 识别一张本地身份证图片 | `adp extract local <文件路径> --app-id <ID>` |
| 识别 Base64 编码的身份证 | `adp extract base64 <base64> --app-id <ID> --file-name id.jpg` |

**批量识别**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 批量识别本地文件夹内的身份证 | `adp extract local <文件夹路径> --app-id <ID>` |
| 批量识别多个 URL | `adp extract url <URL列表文件> --app-id <ID>` |

**异步处理**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 异步提交大文件 | `adp extract url <URL> --app-id <ID> --async` |
| 异步批量处理 | `adp extract local <文件夹路径> --app-id <ID> --async` |
| 查询异步任务结果 | `adp extract query <task_id>` |

并发限制：免费用户最大 2，付费用户最大 10
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

## 第三步：获取身份证抽取应用 ID

ADP 为中国居民身份证提供了**开箱即用**的内置抽取应用，无需额外配置。

### 应用类型说明

ADP 应用分为两类，通过 `app_type` 字段区分：

| `app_type` | 类型 | 说明 |
| --- | --- | --- |
| `0` | 开箱即用应用（OOTB） | 平台内置，`app_id` 以 `ootb_` 开头，无需创建，直接使用 |
| `1` | 自定义应用 | 用户自行创建的抽取应用，`app_id` 为用户自定义标识 |

身份证识别属于**开箱即用应用**，可通过 `--app-type 0` 筛选查询。

### 查询并筛选身份证应用

```bash
# 仅查询开箱即用应用（推荐）
adp app-id list --app-type 0

# 或查询所有应用
adp app-id list
```

从返回列表中找到 `app_label` 包含 **"身份证"** 的应用，记录其 `app_id`：

```json
[
  {
    "app_id": "ootb_******y2z5",
    "app_label": ["身份证", "大陆居民身份证", "身份凭证", "个人证件", "信息提取"],
    "app_name": "身份证",
    "app_type": 0
  }
]
```

> 上例中 `"app_id": "ootb_******y2z5"` 即为身份证抽取应用。`app_type` 为 `0` 表示开箱即用应用，`1` 表示自定义应用。

### 缓存应用 ID（推荐）

首次查询后，后续优先使用缓存避免重复请求：

```bash
# 后续使用缓存
adp app-id cache
```

**重要提示**：每个账号下的 `app_id` 是唯一且固定的，除非用户主动删除应用，否则 `app_id` 不会变更。建议 Agent 将身份证应用的 `app_id` 保存在上下文中，下次直接使用。

---

## 第四步：执行身份证抽取

### 单张身份证抽取（URL）

```bash
adp extract url https://example.com/id-card-front.jpg --app-id <身份证抽取应用ID>
```

### 单张身份证抽取（本地文件）

```bash
adp extract local ./id-card-front.jpg --app-id <身份证应用ID>
```

### 单张身份证抽取（Base64）

```bash
adp extract base64 <base64字符串> --app-id <身份证应用ID> --file-name id-card.jpg
```

### 返回结果示例

无论输入的是身份证正面、反面，还是正反面复印在同一页，ADP 均统一返回完整的 8 字段 JSON 结构，识别到的字段自动填充，无需调用方区分正反面。

```json
[
  {
    "field_key": "name",
    "field_name": "姓名",
    "field_values": [
      {
        "field_value": "程**"
      }
    ]
  },
  {
    "field_key": "gender",
    "field_name": "性别",
    "field_values": [
      {
        "field_value": "女"
      }
    ]
  },
  {
    "field_key": "ethnicity",
    "field_name": "民族",
    "field_values": [
      {
        "field_value": "汉"
      }
    ]
  },
  {
    "field_key": "birth_date",
    "field_name": "出生",
    "field_values": [
      {
        "field_value": "1990年01月15日"
      }
    ]
  },
  {
    "field_key": "address",
    "field_name": "住址",
    "field_values": [
      {
        "field_value": "河南省周口市项城市****镇***号"
      }
    ]
  },
  {
    "field_key": "id_number",
    "field_name": "身份证号码",
    "field_values": [
      {
        "field_value": "412702********3322"
      }
    ]
  },
  {
    "field_key": "issuing_authority",
    "field_name": "签发机构",
    "field_values": [
      {
        "field_value": "周口市公安局项城分局"
      }
    ]
  },
  {
    "field_key": "valid_period",
    "field_name": "有效期限",
    "field_values": [
      {
        "field_value": "2015.01.15-2035.01.15"
      }
    ]
  }
]
```

### 抽取字段说明

ADP 身份证抽取始终统一返回以下 8 个字段，无论输入图片包含正面、反面还是正反面合一：

| field_key | field_name | 说明 |
| --- | --- | --- |
| `name` | 姓名 | 持证人姓名 |
| `gender` | 性别 | 男 / 女 |
| `ethnicity` | 民族 | 民族名称 |
| `birth_date` | 出生 | 出生日期，格式如 "1990年01月15日" |
| `address` | 住址 | 户籍地址 |
| `id_number` | 身份证号码 | 18位身份证号码 |
| `issuing_authority` | 签发机构 | 签发公安机关名称 |
| `valid_period` | 有效期限 | 有效期起止日期 |

### 返回字段通用结构

每个字段遵循以下结构：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `field_key` | string | 字段标识（机器可读） |
| `field_name` | string | 字段名称（人类可读） |
| `field_values` | array | 抽取结果数组 |
| `field_values[].field_value` | string | 抽取值，该面未识别到时为空字符串 |

---

## 第五步：批量处理与异步模式

### 批量处理（本地文件夹）

```bash
adp extract local ./id-cards/ --app-id <身份证应用ID> --export ./results/ 
```

返回摘要：
```json
{
  "total": 10,
  "success": 9,
  "failed": 1,
  "output_dir": "/absolute/path/to/results",
  "files": [
    {"input": "id-front-001.jpg", "output": "id-front-001.jpg.json", "status": "success"},
    {"input": "id-front-002.jpg", "output": "id-front-002.jpg.json", "status": "success"},
    {"input": "damaged.jpg", "output": "damaged.jpg.error.json", "status": "failed", "error": "..."}
  ]
}
```

### 异步处理

```bash
# 提交异步任务
adp extract url https://example.com/id-card.jpg --app-id <身份证应用ID> --async

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

# 身份证抽取（URL）
adp extract url <文件URL> --app-id <身份证抽取应用ID>

# 身份证抽取（本地文件）
adp extract local <文件路径> --app-id <身份证抽取应用ID>

# 身份证抽取（Base64）
adp extract base64 <base64字符串> --app-id <身份证抽取应用ID> --file-name id.jpg

# 批量抽取
adp extract local <文件夹路径> --app-id <身份证抽取应用ID> --export <输出路径> 

# 异步抽取
adp extract url <文件URL> --app-id <身份证抽取应用ID> --async

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
| 身份证抽取费用 | **0.5 积分/张** |
| 新用户免费额度 | 每月赠送 **100 积分，相当于每月可免费处理 200 张身份证**，每月初重置 |
| 查询余额 | `adp credit` |
| 充值方式 | 登录 ADP 门户网站充值：[中国大陆及港澳台地区](https://adp.laiye.com/?utm_source=clawhub) \| [非中国大陆及港澳台地区](https://adp-global.laiye.com/?utm_source=clawhub) |

---

## 更多来也 ADP 文档处理能力

身份证识别只是来也科技 ADP 平台众多开箱即用能力之一。ADP 基于大模型通用理解能力，提供覆盖全品类文档的智能处理解决方案：

| 能力 | 说明 | 典型场景 |
| --- | --- | --- |
| **全球发票/收据抽取** | 自动识别并抽取发票号码、日期、金额、税费、明细等 10+ 关键字段，支持多语言和多币种发票抽取 | 跨国结算账款自动化、费用报销管理 |
| **国内票据抽取** | 识别增值税发票、出租车票、火车票、飞机行程单、财政发票等30+常见票据，支持多页/多票识别及验真 | 国内票据识别、国内发票验真 |
| **订单抽取** | 支持多种采购订单格式，抽取订单号、商品、数量、价格、物流信息等 | 采购自动化、供应链集成 |
| **更多卡证抽取** | ADP支持身份证、港澳台通行证、中国护照、银行卡、户口本、驾驶证、行驶证、车辆合格证、开户许可证、营业执照等 11 种中国常用证件 | 开户审核、合规检查、证件信息批量录入 |
| **文档解析** | 将 PDF、图片、Office 文档转化为结构化数据，保留排版和层级关系 | 长文档分析、合同审查、知识提取 |
| **自定义抽取** | 自主创建抽取应用，配置专属字段和识别逻辑，满足非标单据需求 | 企业专属表单、行业定制单据 |
以上所有能力均可通过同一个 ADP CLI 工具调用，共享 ADP API Key 和积分体系。

如需了解完整能力，请访问：
- ADP 中国大陆：[https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub)
- ADP 非中国大陆：[https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub)

---

## 注意事项

1. **数据完整性**：使用 ADP 输出时，请原样呈现返回数据，不要在抽取过程中修改、添加或删除任何字段。
2. **API Key 安全**：妥善保管 API Key，避免泄露给未授权的第三方。
3. **文件大小限制**：单个文件最大 50MB。
4. **支持格式**：.jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx
5. **应用 ID 复用**：身份证应用的 `app_id` 在账户下唯一且固定，建议记住后直接使用，无需每次查询。

---

##  支持与联系
- **CLI 使用指南：** [ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- **API 接口文档：** [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- **ADP 产品操作手册：** [公有云操作手册](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- **问题反馈：** [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues)
- **邮箱：** global_product@laiye.com
- **官网：** [来也科技](https://laiye.com/product/adp-platform)

Copyright © 2026 [来也科技（北京）有限公司] 保留所有权利。
