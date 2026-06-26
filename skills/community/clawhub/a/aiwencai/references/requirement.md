# hithink-basicinfo-query 构建要求文档

本文档为 skill-creator 提供构建 hithink-basicinfo-query skill 的完整指导。

---

## 1. Skill 基本信息

| 项目 | 内容 |
|------|------|
| **Skill 名称** | 基本资料查询 |
| **描述** | 同花顺基本资料数据查询skill。查询全品类标的（股票、指数、基金、期货、期权、转债、债券、理财、保险等）的基础信息、发行主体、机构资料、费率、上市地点、上市日期等静态信息，支持自然语言问句输入，返回相关基本资料数据结果 |
| **触发场景** | 当用户询问股票基本信息、基金资料、期货合约信息、债券资料、费率信息、上市日期等基本资料查询问题时，必须使用此技能 |

---

## 2. API 接口信息

### 2.1 接口基本信息

| 字段 | 值 |
|------|-----|
| 接口地址 | `https://openapi.iwencai.com/v1/query2data` |
| 请求方式 | POST |
| 认证方式 | API Key (Bearer Token) |

### 2.2 认证方式

请求头中需携带 API Key：
```
Authorization: Bearer {IWENCAI_API_KEY}
Content-Type: application/json
```

### 2.3 请求参数

**Headers:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Authorization | STRING | 是 | Bearer {IWENCAI_API_KEY} |
| Content-Type | STRING | 是 | application/json |

**Body:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| query | STRING | 是 | 用户问句，例如："同花顺上市日期？" |
| source | STRING | 否 | 来源，默认值：test |
| page | STRING | 否 | 分页参数，默认值：1 |
| limit | STRING | 否 | 分页参数，默认值：10 |
| is_cache | STRING | 否 | 缓存参数，默认值：1 |

**请求示例:**
```json
{
  "query": "同花顺上市日期？",
  "source": "test",
  "page": "1",
  "limit": "10",
  "is_cache": "1"
}
```

### 2.4 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| datas | ARRAY | 金融数据列表，对象数组，每个对象包含股票代码、股票简称、上市日期等字段 |

**响应示例:**
```json
{
  "datas": [
    {
      "股票代码": "300033.SZ",
      "股票简称": "同花顺",
      "上市日期": "20091225"
    }
  ]
}
```

**数据字段说明:**
- `datas` 是一个对象数组，每个对象代表一只标的
- 对象包含的字段根据查询内容不同而变化，常见字段包括：`股票代码`、`股票简称`、`上市日期`等
- 支持分页查询，通过 `page` 和 `limit` 参数控制

### 2.5 环境变量

- `IWENCAI_API_KEY`: 鉴权密钥

---

## 3. Skill 内部逻辑要求

### 3.1 核心处理流程

1. **接收用户 Query**: 接收用户的自然语言查询请求
2. **Query 改写**: 将用户问句适当改写为标准的金融查询问句，保持原意不变
3. **API 调用**: 调用金融查询接口获取数据
4. **数据解析**: 解析返回的 `datas` 数组，提取相关字段
5. **结果生成**: 将处理后的数据结果以文本形式返回给大模型
6. **回答用户**: 组织语言回答用户问题，如果改写了问句需特别说明

**Query 改写规则:**
- 保留用户核心意图（如：上市日期、基金费率、期货合约信息等）
- 将口语化表达转为标准金融术语
- 改写后需保持原意不变
- 不需要在空数据时改写问句和尝试

### 3.2 数据来源标注

- **重要**: 在模型回答过程中，如果引用了同花顺数据，**必须强调数据来源于同花顺问财**
- 如果没有查询到数据，**必须提示用户可以到同花顺问财web端查询**（https://www.iwencai.com/unifiedwap/chat）

### 3.3 错误处理

- API 调用失败时，给出友好的错误提示
- 无数据返回时，引导用户访问同花顺问财（https://www.iwencai.com/unifiedwap/chat）

---

## 4. CLI 设计要求

### 4.1 CLI 入口

CLI 入口文件: `scripts/cli.py`

### 4.2 支持的参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--query` | STRING | 是 | 直接传入查询字符串 |
| `--page` | STRING | 否 | 分页参数，默认值：1 |
| `--limit` | STRING | 否 | 每页条数，默认值：10 |
| `--is-cache` | STRING | 否 | 缓存参数，默认值：1 |
| `--source` | STRING | 否 | 来源参数，默认值：test |
| `--api-key` | STRING | 否 | API 密钥（可选，默认从环境变量读取）|

### 4.3 使用示例

```bash
# 直接查询（默认分页10条）
python scripts/cli.py --query "同花顺上市日期？"

# 指定分页参数
python scripts/cli.py --query "贵州茅台上市日期" --page "1" --limit "20"

# 指定API密钥
python scripts/cli.py --query "基金费率" --api-key "your-key"
```

---

## 5. 代码结构要求

### 5.1 目录结构

```
hithink-basicinfo-query/
├── SKILL.md              # Skill 配置文件
├── references/
│   ├── api.md            # API 接口文档
│   └── requirement.md     # 构建要求文档
└── scripts/
    └── cli.py             # CLI 入口（单一脚本）
```

### 5.2 代码要求

- **语言**: Python
- **依赖**: 使用 Python 标准库（urllib, json, argparse 等），尽量减少第三方依赖
- **可执行**: CLI 文件必须可直接执行，支持 `python scripts/cli.py` 或 `python -m scripts` 方式运行
- **单一脚本**: 所有逻辑（参数解析、API调用、数据处理、输出）均在 `cli.py` 一个文件中完成

### 5.3 cli.py 职责

- 解析命令行参数（--query, --page, --limit, --is-cache, --source, --api-key）
- 构造 API 请求参数（query, page, limit, source, is_cache）
- 发送 HTTP POST 请求到 `https://openapi.iwencai.com/v1/query2data`
- 解析响应中的 `datas` 字段
- 格式化输出数据结果

---

## 6. 输出文件格式

### 6.1 SKILL.md 格式

```yaml
---
name: 基本资料查询
description: 同花顺基本资料数据查询skill。查询全品类标的（股票、指数、基金、期货、期权、转债、债券、理财、保险等）的基础信息、发行主体、机构资料、费率、上市地点、上市日期等静态信息，支持自然语言问句输入，返回相关基本资料数据结果。
---
```

### 6.2 数据输出格式

- 直接通过接口返回 `datas` 数组数据
- 处理后以文本格式返回给大模型

---

## 7. 验收标准

1. ✅ SKILL.md 包含正确的 YAML frontmatter
2. ✅ CLI 支持 `--query` 参数
3. ✅ 使用 Python 标准库实现，无第三方依赖
4. ✅ 代码可以直接运行
5. ✅ 引用同花顺数据时标注来源
6. ✅ 无数据时提示访问同花顺问财
