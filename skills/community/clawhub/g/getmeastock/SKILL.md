---
name: give-me-a-stock (Public)
description: 全面的A股股票分析工具，提供7大核心模块（核心财务、技术指标、估值分析、股东持股、市场热度、券商盈利预测、K线图表）+ 财报、公告、新闻资讯和交易所互动问答的多维度分析。
---
运行方式（任选其一；OpenClaw 等渠道可自行选用 Python 或 Node）：

- **Python 3**：`python3 scripts/prana_skill_client.py -m "…" [-t thread_id] [-b base_url]`
- **Node.js 18+**：先在包根目录执行 **`npm install`**，再执行 `node scripts/prana_skill_client.js -m "…" [-t thread_id] [-b base_url]`

## 付费技能说明

若本技能为付费技能，支付成功后请访问 [`https://claw-uat.ebonex.io/api/order/skills`](https://claw-uat.ebonex.io/api/order/skills) 获取购买记录。

鉴权与调用 Claw API 相同：请求头 **`x-api-key`**，值为 **`public_key:secret_key`**（一个英文冒号连接，与 `config/api_key.txt` 中单行凭证格式一致）。

