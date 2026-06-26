# API 接口测试工作流参考

## 工作流程总览

```
接口文档（.md）
     ↓
解析入参字段（必填 / 选填 / 类型 / 枚举值）
     ↓
（可选）分析数据库结构，建立 db_fixture 配置
     ↓
设计测试用例（分组覆盖，数据库变量用 {{占位符}} 引用）
     ↓
生成/执行 run_api_test.py（读取 test_config.json）
     ├── 若有 db_fixture：连接数据库，取真实数据，替换占位符
     └── 逐条执行用例 → 发送请求 → 收集响应
          ↓
     校验结果 → 生成 HTML 可视化报告
```

---

## 测试用例分组规范

| 分组名称           | 覆盖场景                                        |
|--------------------|------------------------------------------------|
| 必填参数验证       | 缺少必填项、空字符串、null 值                   |
| 分页参数验证       | 正常值、边界值（最大/最小）、负数、超限         |
| 枚举参数验证       | 每个合法枚举值、非法枚举值                      |
| 精确查询           | 使用 db_fixture 注入真实主键/单号精确命中       |
| 日期范围筛选       | 正常范围、起止倒置、格式错误                    |
| 字符串模糊查询     | 正常关键词、超长字符串、特殊字符                |
| 数值范围筛选       | 正常范围、Min>Max 倒置、负数、零值              |
| 状态字段筛选       | 每个有效状态值                                  |
| 综合多条件组合     | 2~3 个字段组合、全量参数组合                    |
| 边界与异常参数     | 超长字段、空 body、类型错误（字符串传数字等）   |

---

## test_config.json 结构说明

```json
{
  "meta": {
    "title": "报告标题",
    "base_url": "http://host:port/path",
    "method": "接口方法名",
    "version": "版本号",
    "http_method": "POST",
    "timeout": 30,
    "url_params": {}
  },
  "fixed_params": {
    "taxNo": "91440606MA4WHN8C8X"
  },
  "db_fixture": {
    "connection": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "db_user",
      "password": "db_password",
      "database": "db_name",
      "charset": "utf8mb4"
    },
    "queries": [
      {
        "name": "query_group_name",
        "sql": "SELECT COL_A, COL_B FROM table WHERE condition LIMIT 1",
        "mapping": {
          "varName1": "COL_A",
          "varName2": "COL_B"
        }
      }
    ]
  },
  "test_cases": [
    {
      "id": "TC_001",
      "group": "分组名称",
      "name": "用例名称",
      "desc": "用例描述",
      "body": {
        "param1": "{{varName1}}",
        "param2": "fixed_value"
      },
      "expect": {
        "http_status": 200,
        "success": true,
        "has_response": true,
        "check_page_data": false
      }
    }
  ]
}
```

---

## db_fixture 详细说明

### 工作原理

1. 测试运行前，`run_api_test.py` 检查 `config["db_fixture"]` 是否存在
2. 若存在，按 `connection` 配置连接 MySQL，依次执行各 `queries` 中的 SQL
3. 将查询结果按 `mapping` 规则映射为 `{变量名: 真实值}` 字典（`fixture_vars`）
4. 执行每条测试用例时，对 `body` 中的 `{{变量名}}` 进行替换

### 占位符替换规则

| 用例 body 写法 | 替换行为 |
|----------------|---------|
| `"field": "{{varName}}"` | 整体替换，保留原始类型（字符串/数字）|
| `"field": "prefix_{{varName}}_suffix"` | 部分替换，结果为字符串拼接 |
| 变量不存在或查询无数据 | 保留占位符原样，不报错 |

### 依赖安装

```bash
pip install pymysql
```

若未安装 pymysql，db_fixture 会跳过（打印 WARN），测试继续执行，占位符保持原样。

### 最佳实践

- SQL 中加 `WHERE` 条件过滤到目标数据集（如 `BUYER_TAXNO='xxx'`）
- 始终加 `LIMIT 1`，避免取到多行数据
- 用 `name` 字段区分不同查询组，方便日志排查
- 涉及传统发票和数电票的接口，建议分两个 query 分别取样

---

## expect 字段说明

| 字段               | 类型    | 说明                                           |
|--------------------|---------|------------------------------------------------|
| http_status        | int     | 期望的 HTTP 状态码，默认 200                   |
| success            | bool    | 期望响应体中 success 字段的值                  |
| has_response       | bool    | 期望 model/response 字段存在且非 null          |
| response_field     | str     | 显式指定响应数据字段名（默认自动探测 model→response）|
| error_field_exists | bool    | 期望 errorResponse 字段存在                    |
| check_page_data    | bool    | 期望 model/response 为列表或对象，记录条数     |
| custom_checks      | list    | 自定义路径校验，见下方说明                     |

### custom_checks 格式

```json
"custom_checks": [
  {"path": "response.0.invoiceType", "op": "eq",        "value": "01"},
  {"path": "errorResponse.code",     "op": "exists"},
  {"path": "response",               "op": "contains",  "value": "invoiceNo"},
  {"path": "response.total",         "op": "gt",        "value": "0"}
]
```

支持的 `op`：`eq` / `ne` / `contains` / `exists` / `not_exists` / `gt` / `lt`

---

## 从接口文档快速提取测试用例的方法

1. **必填参数** → 每个必填字段生成 1 条缺失用例 + 1 条空字符串用例
2. **精确查询字段**（如发票号码、订单号）→ 配置 `db_fixture` 取真实值，用 `{{占位符}}` 引用
3. **枚举值字段** → 每个合法枚举值生成 1 条正向用例 + 1 条非法枚举用例
4. **日期字段（成对）** → 正常范围 + 起止倒置 + 格式错误
5. **数值范围字段（成对）** → 正常范围 + Min>Max + 负数
6. **字符串模糊查询** → 关键词查询 + 超长字符串（超过文档长度限制）
7. **状态/标记字段** → 每个文档中列出的合法值各建 1 条用例
8. **综合用例** → 3~5 个常用字段组合 + 全量字段组合

---

## 校验规则说明

### 基础校验（所有用例通用）
- HTTP 状态码是否为 200
- 响应是否为合法 JSON
- `success` 字段是否符合预期（true/false）

### 正向用例额外校验
- `model`/`response` 字段是否存在且非 null
- 如返回列表，记录条数

### 负向用例额外校验
- `errorResponse` 字段是否存在
- `success` 是否为 false
