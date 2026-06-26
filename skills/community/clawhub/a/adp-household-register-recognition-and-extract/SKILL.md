---
name: household-register-recognition-and-extract
description: 基于来也科技ADP平台的中国户口本智能识别与信息抽取Skill。支持户口本首页及个人页全量字段的精准抽取——户别、户主姓名、户号、住址、姓名、与户主关系、曾用名、性别、出生地、民族、籍贯、出生日期、本市其他住址、宗教信仰、身份证号码、身高、血型、文化程度、婚姻状况、服务处所、职业、登记日期、编号，输出结构化JSON，零配置开箱即用，适用于户籍核验、信息录入、开户审核等场景。
---

# 中国居民户口本识别与抽取 Skill

能力由来也科技 [ADP（Agentic Document Processing）智能体文档处理平台](https://adp.laiye.com/?utm_source=clawhub)提供，支持中国户口本的智能识别与关键信息抽取能力。本 Skill 调用来也科技 ADP 官方 CLI 工具，一条命令即可完成户口本图片/扫描件的结构化字段抽取，输出标准 JSON，无缝对接业务系统。

> 新用户注册即享每月 **100 免费积分**（每月刷新），相当于每月可免费抽取 **200 张户口本**。ADP 提供标准可商用 API，**1 小时即可快速集成接入业务系统**。
</br> 立即注册：[中国大陆](https://adp.laiye.com/?utm_source=clawhub) | [海外地区](https://adp-global.laiye.com/?utm_source=clawhub)

---

## 快速接入指南

### 核心工作流

1. **安装依赖**：首次执行时，安装 ADP CLI 工具。
2. **认证配置**：首次执行时，运行 `adp config get` 检查凭证。若未配置，提示用户提供 API Key。
3. **获取应用列表**：首次执行时，通过 `adp app-id list --app-type 0` 获取开箱即用应用列表，找到户口本抽取应用并记录其 `app_id`（以 `ootb_` 开头）。后续优先使用 `adp app-id cache`。
4. **执行抽取**：运行 `adp extract url <URL> --app-id <户口本抽取应用ID>` 或 `adp extract local <文件路径> --app-id <户口本抽取应用ID>`。
5. **结果处理**：解析返回的 JSON，提取户别、户主姓名、户号、住址、姓名、与户主关系、曾用名、性别、出生地、民族、籍贯、出生日期、本市其他住址、宗教信仰、身份证号码、身高、血型、文化程度、婚姻状况、服务处所、职业、登记日期、编号等结构化字段。
6. **错误处理**：命令失败时，解析 stderr JSON 确定错误类型和恢复操作。

### 场景 → 命令映射

**单张识别**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 识别一张户口本图片（URL） | `adp extract url <URL> --app-id <户口本抽取应用ID>` |
| 识别一张本地户口本图片 | `adp extract local <文件路径> --app-id <户口本抽取应用ID>` |
| 识别 Base64 编码的户口本 | `adp extract base64 <base64> --app-id <户口本抽取应用ID> --file-name hukou.jpg` |

**批量识别**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 批量识别本地文件夹内的户口本 | `adp extract local <文件夹路径> --app-id <户口本抽取应用ID>` |
| 批量识别多个 URL | `adp extract url <URL列表文件> --app-id <户口本抽取应用ID>` |

**异步处理**

| 用户意图 | 推荐命令 |
| :--- | :--- |
| 异步提交大文件 | `adp extract url <URL> --app-id <户口本抽取应用ID> --async` |
| 异步批量处理 | `adp extract local <文件夹路径> --app-id <户口本抽取应用ID> --async` |
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

## 第三步：获取户口本抽取应用 ID

ADP 为中国户口本提供了**开箱即用**的内置抽取应用，无需额外配置。

### 应用类型说明

ADP 应用分为两类，通过 `app_type` 字段区分：

| `app_type` | 类型 | 说明 |
| --- | --- | --- |
| `0` | 开箱即用应用（OOTB） | 平台内置，`app_id` 以 `ootb_` 开头，无需创建，直接使用 |
| `1` | 自定义应用 | 用户自行创建的抽取应用，`app_id` 为用户自定义标识 |

户口本识别属于**开箱即用应用**，可通过 `--app-type 0` 筛选查询。

### 查询并筛选户口本应用

```bash
# 仅查询开箱即用应用（推荐）
adp app-id list --app-type 0

# 或查询所有应用
adp app-id list
```

从返回列表中找到 `app_label` 包含 **"户口本"** 的应用，记录其 `app_id`：

```json
[
  {
    "app_id": "ootb_******xx",
    "app_label": ["户口本", "户口簿", "户籍", "个人证件", "信息提取"],
    "app_name": "户口本",
    "app_type": 0
  }
]
```

> 上例中 `"app_id": "ootb_******xx"` 即为户口本抽取应用。`app_type` 为 `0` 表示开箱即用应用，`1` 表示自定义应用。

### 缓存应用 ID（推荐）

首次查询后，后续优先使用缓存避免重复请求：

```bash
# 后续使用缓存
adp app-id cache
```

**重要提示**：每个账号下的 `app_id` 是唯一且固定的，除非用户主动删除应用，否则 `app_id` 不会变更。建议 Agent 将户口本应用的 `app_id` 保存在上下文中，下次直接使用。

---

## 第四步：执行户口本抽取

### 单张户口本抽取（URL）

```bash
adp extract url https://example.com/hukou-page.jpg --app-id <户口本抽取应用ID>
```

### 单张户口本抽取（本地文件）

```bash
adp extract local ./hukou-page.jpg --app-id <户口本抽取应用ID>
```

### 单张户口本抽取（Base64）

```bash
adp extract base64 <base64字符串> --app-id <户口本抽取应用ID> --file-name hukou.jpg
```

### 返回结果示例

ADP 户口本抽取统一返回结构化 JSON，支持户口本首页和个人页共 **23 个**关键字段识别抽取。

```json
[
  {
    "field_key": "household_type",
    "field_name": "户别",
    "field_values": [
      {
        "field_value": "非农业家庭户"
      }
    ]
  },
  {
    "field_key": "householder_name",
    "field_name": "户主姓名",
    "field_values": [
      {
        "field_value": "张三"
      }
    ]
  },
  {
    "field_key": "household_number",
    "field_name": "户号",
    "field_values": [
      {
        "field_value": "110108001234"
      }
    ]
  },
  {
    "field_key": "residential_address",
    "field_name": "住址",
    "field_values": [
      {
        "field_value": "北京市海淀区中关村大街1号"
      }
    ]
  },
  {
    "field_key": "member_name",
    "field_name": "姓名",
    "field_values": [
      {
        "field_value": "张三"
      }
    ]
  },
  {
    "field_key": "relationship_with_head_of_household",
    "field_name": "与户主关系",
    "field_values": [
      {
        "field_value": "户主"
      }
    ]
  },
  {
    "field_key": "previous_names",
    "field_name": "曾用名",
    "field_values": [
      {
        "field_value": "张小三"
      }
    ]
  },
  {
    "field_key": "gender",
    "field_name": "性别",
    "field_values": [
      {
        "field_value": "男"
      }
    ]
  },
  {
    "field_key": "place_of_birth",
    "field_name": "出生地",
    "field_values": [
      {
        "field_value": "北京市海淀区"
      }
    ]
  },
  {
    "field_key": "nationality",
    "field_name": "民族",
    "field_values": [
      {
        "field_value": "汉"
      }
    ]
  },
  {
    "field_key": "hometown",
    "field_name": "籍贯",
    "field_values": [
      {
        "field_value": "山东省济南市"
      }
    ]
  },
  {
    "field_key": "date_of_birth",
    "field_name": "出生日期",
    "field_values": [
      {
        "field_value": "1985年06月20日"
      }
    ]
  },
  {
    "field_key": "this_city_other_address",
    "field_name": "本市其他住址",
    "field_values": [
      {
        "field_value": "北京市朝阳区望京西路8号院"
      }
    ]
  },
  {
    "field_key": "religious_belief",
    "field_name": "宗教信仰",
    "field_values": [
      {
        "field_value": "无"
      }
    ]
  },
  {
    "field_key": "id_number",
    "field_name": "身份证号码",
    "field_values": [
      {
        "field_value": "110108198506201234"
      }
    ]
  },
  {
    "field_key": "height",
    "field_name": "身高",
    "field_values": [
      {
        "field_value": "175cm"
      }
    ]
  },
  {
    "field_key": "blood_type",
    "field_name": "血型",
    "field_values": [
      {
        "field_value": "A"
      }
    ]
  },
  {
    "field_key": "education_level",
    "field_name": "文化程度",
    "field_values": [
      {
        "field_value": "大学本科"
      }
    ]
  },
  {
    "field_key": "marital_status",
    "field_name": "婚姻状况",
    "field_values": [
      {
        "field_value": "已婚"
      }
    ]
  },
  {
    "field_key": "service_place",
    "field_name": "服务处所",
    "field_values": [
      {
        "field_value": "北京市某某科技有限公司"
      }
    ]
  },
  {
    "field_key": "occupation",
    "field_name": "职业",
    "field_values": [
      {
        "field_value": "工程师"
      }
    ]
  },
  {
    "field_key": "registration_date",
    "field_name": "登记日期",
    "field_values": [
      {
        "field_value": "2010年03月15日"
      }
    ]
  },
  {
    "field_key": "number",
    "field_name": "编号",
    "field_values": [
      {
        "field_value": "00123456"
      }
    ]
  }
]
```

### 抽取字段说明

ADP 户口本抽取返回以下字段：

| field_key | field_name | 说明 |
| --- | --- | --- |
| `household_type` | 户别 | 户口类别（如非农业家庭户、农业家庭户等） |
| `householder_name` | 户主姓名 | 户口本首页户主姓名 |
| `household_number` | 户号 | 户口本户号 |
| `residential_address` | 住址 | 户籍登记住址 |
| `member_name` | 姓名 | 当前页成员姓名 |
| `relationship_with_head_of_household` | 与户主关系 | 与户主的关系（如户主、配偶、子女、夫等） |
| `previous_names` | 曾用名 | 曾经使用过的姓名 |
| `gender` | 性别 | 男 / 女 |
| `place_of_birth` | 出生地 | 出生地信息 |
| `nationality` | 民族 | 民族名称 |
| `hometown` | 籍贯 | 籍贯信息 |
| `date_of_birth` | 出生日期 | 出生日期 |
| `this_city_other_address` | 本市其他住址 | 本市（县）其他住址 |
| `religious_belief` | 宗教信仰 | 宗教信仰 |
| `id_number` | 身份证号码 | 身份证号码 |
| `height` | 身高 | 身高（cm） |
| `blood_type` | 血型 | 血型 |
| `education_level` | 文化程度 | 文化程度（如大学本科、高中等） |
| `marital_status` | 婚姻状况 | 婚姻状况（如已婚、未婚、离异等） |
| `service_place` | 服务处所 | 工作单位名称 |
| `occupation` | 职业 | 职业 |
| `registration_date` | 登记日期 | 户口登记日期 |
| `number` | 编号 | 户口本编号 |

### 返回字段通用结构

每个字段遵循以下结构：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `field_key` | string | 字段标识（机器可读） |
| `field_name` | string | 字段名称（人类可读） |
| `field_values` | array | 抽取结果数组 |
| `field_values[].field_value` | string | 抽取值，未识别到时为空字符串 |

---

## 第五步：批量处理与异步模式

### 批量处理（本地文件夹）

```bash
adp extract local ./hukou-pages/ --app-id <户口本抽取应用ID> --export ./results/ 
```

返回摘要：
```json
{
  "total": 10,
  "success": 9,
  "failed": 1,
  "output_dir": "/absolute/path/to/results",
  "files": [
    {"input": "hukou-page-001.jpg", "output": "hukou-page-001.jpg.json", "status": "success"},
    {"input": "hukou-page-002.jpg", "output": "hukou-page-002.jpg.json", "status": "success"},
    {"input": "damaged.jpg", "output": "damaged.jpg.error.json", "status": "failed", "error": "..."}
  ]
}
```

### 异步处理

```bash
# 提交异步任务
adp extract url https://example.com/hukou-page.jpg --app-id <户口本抽取应用ID> --async

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

# 户口本抽取（URL）
adp extract url <文件URL> --app-id <户口本抽取应用ID>

# 户口本抽取（本地文件）
adp extract local <文件路径> --app-id <户口本抽取应用ID>

# 户口本抽取（Base64）
adp extract base64 <base64字符串> --app-id <户口本抽取应用ID> --file-name hukou.jpg

# 批量抽取
adp extract local <文件夹路径> --app-id <户口本抽取应用ID> --export <输出路径> 

# 异步抽取
adp extract url <文件URL> --app-id <户口本抽取应用ID> --async

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
| 户口本抽取费用 | **0.5 积分/张** |
| 新用户免费额度 | 每月赠送 **100 积分，相当于每月可免费处理 200 张户口本**，每月初重置 |
| 查询余额 | `adp credit` |
| 充值方式 | 登录 ADP 门户网站充值：[中国大陆及港澳台地区](https://adp.laiye.com/?utm_source=clawhub) \| [非中国大陆及港澳台地区](https://adp-global.laiye.com/?utm_source=clawhub) |

---

## 更多来也 ADP 文档处理能力

户口本识别只是来也科技 ADP 平台众多开箱即用能力之一。ADP 基于大模型通用理解能力，提供覆盖全品类文档的智能处理解决方案：

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
5. **应用 ID 复用**：户口本应用的 `app_id` 在账户下唯一且固定，建议记住后直接使用，无需每次查询。

---

##  支持与联系
- **CLI 使用指南：** [ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- **API 接口文档：** [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- **ADP 产品操作手册：** [公有云操作手册](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- **问题反馈：** [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues)
- **邮箱：** global_product@laiye.com
- **官网：** [来也科技](https://laiye.com/product/adp-platform)

Copyright © 2026 [来也科技（北京）有限公司] 保留所有权利。
