---
name: datayes-web-search
slug: datayes-web-search
description: >
  通用 AI 语义搜索技能，通过 Datayes gptMaterials/v2 API 执行结构化语义搜索。用户询问最新资讯、研报、公告、会议纪要、行业动态、指标背景材料时使用。优先通过仓库内 Python 脚本发起请求，不要手写 HTTP 请求，不要在 skill 中硬编码 token。
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["DATAYES_TOKEN"],
        "bins": ["python3"]
      }
    }
  }
---

# Datayes Web Search

## 前提条件

### 1. 获取 Datayes Token

访问 https://r.datayes.com/auth/login 登录 Datayes 账号，并在 Datayes 控制台获取可撤销的 API token。

### 2. 配置 Token

macOS / Linux:

```bash
export DATAYES_TOKEN='your-token'
```

Windows PowerShell:

```powershell
$env:DATAYES_TOKEN = "your-token"
```

Windows CMD:

```cmd
set DATAYES_TOKEN=your-token
```

## 直接使用

- 只用 `python3 scripts/datayes_web_search.py` 发请求。
- 只用 Python 标准库；不要额外安装依赖。
- 从环境变量 `DATAYES_TOKEN` 读取 token。脚本会自动带上 `Authorization: Bearer <token>`。
- 真实业务接口 URL 会先校验协议与主机名，只允许 Datayes 受信任域名，避免把 token 发到非 Datayes 地址。
- 默认 `rewrite=false`，保留用户原始查询，减少意外改写。

## 最小流程

1. 先查看接口规格。

```bash
python3 scripts/datayes_web_search.py spec
```

2. 直接搜索并输出前 15 条结果。

```bash
python3 scripts/datayes_web_search.py search "新能源车 渗透率 2026" --query-scope research
```

3. 需要更多结果时显式放大返回条数。

```bash
python3 scripts/datayes_web_search.py search "美国关税政策 2026" --query-scope news --top 30
```

## queryScope 参数

| 值 | 搜索范围 |
|---|---|
| *(不传)* | 综合全部类型（默认） |
| `research` | 券商研报 |
| `announcement` | 上市公司公告 |
| `news` | 财经资讯/新闻 |
| `meetingSummary` | 电话会/调研纪要 |
| `indicator` | 宏观/行业数据指标 |
| `researchTable` | 研报图表 |

## 选择规则

- 用户问新闻、政策变化、市场动态时，优先 `news`。
- 用户问卖方观点、行业深度、公司覆盖时，优先 `research`。
- 用户问公告原文或正式披露时，优先 `announcement`。
- 用户问调研纪要、电话会、专家交流时，优先 `meetingSummary`。
- 用户问宏观或行业指标背景材料时，可用 `indicator`。
- 用户没限定范围时，可不传 `queryScope` 做综合搜索。

## 输出要求

- 直接输出 API 返回的原始 JSON 数组，不做二次改写或字段重组。
- 搜索词尽量精确，涉及时效性问题时优先附带年份或月份。
- 若需要跨多种范围搜索，可分别调用多次，再由上层任务决定如何合并结果。
