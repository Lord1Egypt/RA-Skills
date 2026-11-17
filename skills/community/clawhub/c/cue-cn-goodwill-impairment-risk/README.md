# 商誉减值风险·逐条挂源

把一份年报／半年报或收购公告里的**商誉科目**拆成八节台账。每一行的金额与比例，都必须逐字回得到那句披露原文。

> 离线自检：`bash scripts/fixtures/run_fixtures.sh`——好样不发红、六枚坏样各发其码，三档全过，零网络。

## 它解决什么

商誉是 A 股并购留下的最大一块「说不清」的资产。看一份年报想知道：

- 这家公司商誉有多少？哪个标的占大头？
- 收购时承诺的业绩完成了没有？完成率多少？
- 减值测试用的折现率、增长率是多少？
- 今年计提了多少？累计计提多少？账面还剩多少？

这些数在年报里都有，但散在附注、董事会报告、审计报告三处，写法不同、口径不同。
本件把它们逐项摘成一张台账，**每一格都挂上原句与锚**，让你能自己回到那一页去核。

## 它不做什么（这一节比上一节重要）

| 不做 | 为什么 |
|---|---|
| 不判**会不会减值** | 这是投资判断，不是摘录。台账只报「披露说了什么」 |
| 不判**计提是否充分** | 同上。审计意见与监管问询才是这件事的裁判 |
| 不给评级、目标价，不预测股价 | 红线 |
| **不自己算减值额或计提比例** | 分母可能是商誉原值、账面价值、资产组口径——算错一个分母，整张表的读数全错。披露没写就写「未取到」，那是答案，不是失败 |
| 不代做会计处理、不代拟问询回复 | 不接代办 |

## 怎么用

```bash
# 1. 拿到年报/公告正文（PDF 或网页）
# 2. 按 SKILL.md 第三节的八节契约摘成台账 markdown
# 3. 自检
python3 -B scripts/check_goodwill.py 我的台账.md
```

退码 `0`＝全过；`1`＝有发红（逐条告诉你哪一行哪一格）；`3`＝文件不存在或不像本件台账。

## 五道机检

| 码 | 道 | 抓什么 |
|---|---|---|
| `GW-STRUCT` | 形制 | 八节齐不齐；头部三件在不在；四类数据行的要素有没有缺格 |
| `GW-QUOTE` | 原句与锚 | 每行的「」原句非空、`锚：` 非空、`[S#]` 在第七节有对应行且带 URL 与检索日 |
| `GW-LINE` | 红线 | 会不会减值／计提是否充分／评级目标价／股价预测／收益承诺／代办 |
| `GW-GAP` | 未取到与不得自算 | 申报数两向对账；「无减值／不适用」替披露下结论；**金额与百分比不在本行原句里＝自算** |
| `GW-BOUND` | 边界 | 口径写成重组或财报点评的，点名改走别的件 |

### 最要紧的那一格：判「逐字在场」，不判「数值相等」

`1,200.00 万元` 和 `1200 万元` 数值一样，但后者是卡面加工过的写法。单位换了（万元↔亿元）、
小数位补了、千分位去了——**都算不在原句里**。

理由：本件卖的就是「这枚数字回得到那一句」。一旦允许换算，「回得到」就变成了「算得出」，
那是两件事。

## 与现役的切割

| 件 | 它管什么 | 本件不碰 |
|---|---|---|
| `cn-restructuring-tracker` | 重组**事件**与对价的时间轴（停牌、预案、过会、实施） | 商誉科目这一组数 |
| `cn-earnings-note` | **已出财报的点评**（收入、利润、毛利率怎么变、为什么变） | 不评业绩，只把商誉科目挂到原句上 |
| `ma-restructuring-terms-cn` | 单份重组文件的**条款速读** | 商誉余额与减值测试 |

## 通道

取证腿是两枚可选辅助：`cue-data-mcp`（定位年报与收购公告）、`cue-omni-reader`（PDF／网页转可摘文本）。
通道实连走这条正路，域 id 与 routing url 现取现用，不抄死：

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
DOMAIN_ID="$(curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
print(rows[0]["id"])')"
ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
print(rows[0]["routing"]["url"])')"
curl -s -X POST "$ROUTING_URL" \
  -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  -w '\nHTTP %{http_code}\n'
```

三层互不等价：**装好 skill ≠ 已配凭据 ≠ 通道已连**。匿名 GET 只证目录可达；带 key 实连且
`tools/list` 有返回才证那把 key 被接受。连接报错不等于域无数据，如实报。

## 工件

- `consumes: []`（显式空——本件直接读用户给的文件，不消费上游工件）
- `inputs: announcement-doc / disclosure-file`
- `produces: structured-note`（在册 canonical，未新增任何工件名）

## 文件

- `SKILL.md` — 完整契约（八节、四形、五道）
- `SKILL.en.md` — 英文对照
- `README.md` / `README.en.md` — 本文件与英文版
- `CHANGELOG.md`
- `scripts/check_goodwill.py` — 五道机检（零网络、纯标准库）
- `scripts/fixtures/` — 好样 1 + 坏样 6 + `run_fixtures.sh`

## 许可

MIT
