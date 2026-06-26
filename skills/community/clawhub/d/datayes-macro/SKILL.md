---
name: datayes-macro
slug: datayes-macro
description: >
  查询 Datayes/通联的宏观与行业指标数据。用户询问 GDP、CPI、PPI、PMI、M2、社融、利率、就业、贸易、产量、价格等宏观或行业时间序列时使用。优先通过仓库内 Python 脚本搜索候选指标并拉取明细，不要手写 HTTP 请求。
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

# Datayes 宏观指标

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

- 只用 `python3 scripts/datayes_macro.py` 发请求。
- 只用 Python 标准库；不要额外安装依赖。
- 从环境变量 `DATAYES_TOKEN` 读取 token。脚本会自动带上 `Authorization: Bearer <token>`。
- 真实业务接口的 `httpUrl` 会先校验主机名，只允许 Datayes 受信任域名，避免把 token 发送到非 Datayes 地址。

## 最小流程

1. 先搜候选指标。

```bash
python3 scripts/datayes_macro.py search "M2同比" --top 5 --json
```

2. 结果明确时，直接一步查数据。

```bash
python3 scripts/datayes_macro.py query "M2同比" --begin-date 20240101 --limit 12 --json
```

3. 需要精确控制时，按 id 查明细。

```bash
python3 scripts/datayes_macro.py detail 1070000009 --begin-date 20240101 --limit 12 --json
```

## 选择规则

- 优先名称与用户问题最贴近的指标。
- 用户没说地区时，优先中国或全国口径。
- 用户没说频率时，优先月度，其次季度，再次年度。
- 搜索结果噪声大时，先缩短关键词再重试，例如去掉地区词或 `同比/环比` 修饰词。

## 输出要求

- 明确写出指标名称、频率、单位、来源、最新值和最近若干期数据。
- 命中多个合理口径时，先列候选再确认，不要混合不同指标。
