---
name: api-test-reporter
description: This skill should be used when the user wants to perform automated API interface testing based on an interface document (Markdown or other format) and generate a visual HTML test report. It is suitable for any HTTP POST/GET interface that accepts JSON parameters. The skill guides the agent to parse interface documentation, design test cases by parameter groups (required fields, pagination, enums, date ranges, numeric ranges, status flags, combined scenarios, boundary/exception cases), execute all test cases, and generate a structured HTML report containing test case details, request parameters, response data, and validation results. Trigger phrases include: "接口测试", "API测试", "根据接口文档测试", "生成测试报告", "逐个验证参数", "自动化测试接口".
  This skill should be used when the user wants to perform automated API interface testing based on an interface document (Markdown or other format) and generate a visual HTML test report.
  It is suitable for any HTTP POST/GET interface that accepts JSON parameters. The skill guides the agent to parse interface documentation, design test cases by parameter groups (required fields, pagination, enums, date ranges, numeric ranges, status flags, combined scenarios, boundary/exception cases), execute all test cases, and generate a structured HTML report containing test case details, request parameters, response data, and validation results.
  Trigger phrases include: "接口测试", "API测试", "根据接口文档测试", "生成测试报告", "逐个验证参数", "自动化测试接口".
allowed-tools:
disable: true
---

# API 接口自动化测试报告 Skill

## 功能概述

将接口文档转化为一套完整的自动化测试，生成可视化 HTML 报告，报告包含：
- **测试用例**：ID、分组、名称、描述
- **入参**：每条用例发送的完整 JSON 请求体
- **返参**：响应耗时、完整响应 JSON
- **校验结果**：每条校验项的通过/失败明细

### 与 isp-api-tester 的关系

| 场景 | 使用的执行器 |
|------|------------|
| 百望 ISP 开放平台接口 | `isp-api-tester` 的 `run_isp_test.py`（内置动态签名） |
| 通用 HTTP 接口 | 本 skill 的 `run_api_test.py` |

**`generate_report.py` 和 `report_template.html` 被 `isp-api-tester` 跨 skill 引用。**

---

## 执行流程

### 第一步：解析接口文档

从 Markdown 文档提取：
- 请求地址、方式（POST/GET）
- 公共参数（method、version 等 URL query 参数）
- 业务请求参数（字段名、类型、是否必填、枚举值）

### 第二步：数据库取数（优先）

如果提供了数据库信息，先执行此步：
1. 连接数据库，找到对应业务表
2. 查询真实记录，注意发票类型字段规则（见下方）
3. 建立 DB 字段 → 接口入参字段 的映射关系

**发票类型字段规则：**

| 票种大类 | invoiceCode | invoiceNumber |
|---------|:-----------:|:-------------:|
| 数电票（31/32/51/59/61/83/84） | ❌ 不传 | `E_INV_NUM`（20位数电号码） |
| 税控票（01/03/04/08/10/11/14/15） | `INV_KIND` | `INV_NUM` |
| 数电纸票（85/86/87/88） | `INV_KIND` | `INV_NUM` |

> **数电票的 invoiceCode 必须完全不传**（传空串 `""` 会触发 704 参数为空错误）

### 第三步：设计测试用例

| 分组 | 策略 |
|------|------|
| 必填参数验证 | 每个必填字段：缺失1条 + 空字符串1条 |
| 分页参数验证 | 正常值 + 边界值 + 负数 |
| 枚举字段验证 | 每个合法枚举值1条 + 非法值1条 |
| 日期范围筛选 | 正常范围 + 起止倒置 + 格式错误 |
| 状态/标记字段 | 每个合法值各1条 |
| 综合多条件组合 | 2~3字段组合 + 全量字段组合 |
| 边界与异常参数 | 超长字段 + 空body + 类型错误 |

**正向用例（expect success=true）的入参字段值必须从数据库获取真实值。**

### 第四步：执行测试

**ISP 接口（需要动态签名）：**
```bash
python ~/.workbuddy/skills/isp-api-tester/scripts/run_isp_test.py --config test_config_xxx.json --output ./
```

**通用 HTTP 接口：**
```bash
python ~/.workbuddy/skills/api-test-reporter/scripts/run_api_test.py --config test_config.json --output ./
```

### 第五步：输出文件

| 文件 | 说明 |
|------|------|
| `test_report_<method>_<timestamp>.html` | 可视化报告（双击打开） |
| `__REPORT_DATA__.js` | 报告数据文件（与 HTML 同目录，不可删） |
| `test_results_<method>_<timestamp>.json` | 原始结果 JSON |

---

## test_config.json 格式

```json
{
  "meta": {
    "title": "接口测试报告标题",
    "base_url": "http://host/api/endpoint",
    "method": "baiwang.input.invoice.queryinvoicepool",
    "version": "6.0",
    "timeout": 30,
    "http_method": "POST",
    "url_params": {},
    "isp_auth": {
      "appKey": "1000139",
      "appSecret": "xxx",
      "username": "cpy001",
      "password": "Aa123456.",
      "userSalt": "xxx"
    }
  },
  "fixed_params": {
    "taxNo": "91440606MA4WHN8C8X"
  },
  "db_fixture": {
    "connection": {
      "host": "10.115.96.247", "port": 3306,
      "user": "jxindependent", "password": "Xj2zCkLJXTkEJ5j",
      "database": "jxindependent0", "charset": "utf8mb4"
    },
    "queries": [
      {
        "name": "tax_invoice_sample",
        "sql": "SELECT INV_KIND, INV_NUM FROM bw_jms_main1 WHERE INV_TYPE='01' LIMIT 1",
        "mapping": {
          "invoiceCode":   "INV_KIND",
          "invoiceNumber": "INV_NUM"
        }
      }
    ]
  },
  "test_cases": [
    {
      "id": "TC_001",
      "group": "正常流程",
      "name": "按发票号码查询",
      "desc": "使用数据库真实发票号码查询",
      "body": {
        "invoiceCode":   "{{invoiceCode}}",
        "invoiceNumber": "{{invoiceNumber}}"
      },
      "expect": {
        "success": true
      }
    },
    {
      "id": "TC_010",
      "group": "异常参数",
      "name": "缺少必填参数 taxNo",
      "desc": "不传 taxNo，期望返回 success=false",
      "remove_fixed": ["taxNo"],
      "body": {},
      "expect": {
        "success": false
      }
    }
  ]
}
```

---

## `expect` 校验规则速查

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 校验响应体 success 字段值 |
| `response.{field}` | any | 校验 response 节点下的字段，如 `"response.invoiceType": "31"` |
| `model.{field}` | any | 校验 model 节点下的字段 |
| `has_response` | bool | 期望 response/model 字段存在且非 null |
| `check_page_data` | bool | 期望返回列表/分页数据 |
| `error_field_exists` | bool | 期望 errorResponse 字段存在 |
| `custom_checks` | list | 自定义路径校验（见下方） |

**不使用 `http_status` 字段**（百望 ISP 接口测试不校验 HTTP 状态码）。

### 返参校验规则（ISP 接口）

1. **`success=true`** → 自动校验 invoiceList/response/model 非空
2. **`success=false`** → 只校验 success 字段，不校验数据
3. **不校验 HTTP 状态码**

### custom_checks 示例

```json
"custom_checks": [
  {"path": "response.invoiceType", "op": "eq",    "value": "31"},
  {"path": "errorResponse.code",   "op": "exists"},
  {"path": "response",             "op": "contains", "value": "invoiceNo"}
]
```

支持 `op`：`eq` / `ne` / `contains` / `exists` / `not_exists` / `gt` / `lt`

---

## 用例设计规范

1. 正向用例（`"success": true`）的入参**必须从数据库获取真实值**
2. 数电票用例 body 中**完全不传 invoiceCode**（数电票没有发票代码）
3. 时间范围参数使用近期日期（近3个月），避免数据量超500
4. 数据量可能超500的查询加 `pageNum` 参数
5. 需要排除某个 fixed_params 中的参数时，使用 `"remove_fixed": ["字段名"]`

---

## 报告架构（模板与数据分离）

- `report_template.html`：固定 HTML 骨架，不含测试数据，CSS/JS 全部内嵌
- `__REPORT_DATA__.js`：测试结果 JS 变量赋值文件（`var reportData = {...}`）
- HTML 通过 `<script src="__REPORT_DATA__.js">` 加载数据并渲染
- **不使用 fetch 加载 JSON**（`file://` 协议下 CORS 会阻止 fetch 本地文件）
- 两个文件必须在同一目录，双击 HTML 即可打开

---

## 依赖

```bash
pip install requests pymysql
```
