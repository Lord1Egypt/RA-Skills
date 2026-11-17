# cn-research-brief

**把一批中文来源整理成一份逐条挂源的研究速览：每条发现带一条可回查来源与检索日，未取到的逐条点名，判断位一律留人工。**

要点不稀缺，**稀缺的是每条要点都能回到一处带检索日的来源**。差异化不在排版，而在两道硬门禁：没有锚的要点进不了第二节，没点名的缺口过不了机检。

**输入**：一批中文来源（网页／公告／报道／解析件）＋主体与检索窗口，或一个待查问题
**输出**：四节速览（一句话结论／逐条发现／未取到与口径／来源）＋ `sources.jsonl` 那一层的来源行
**代价**：四节契约 + 一道机检；通道腿（深研／解析）开没开，决定的是多源取证与逐条出处那一层——两条路各自缺什么、走哪条，写在 §二 与 §四
**机检**：`scripts/check_brief.py` 四道（形制／锚／判断词／未取到两向点名），零网络；反证矩阵长在这支脚本里

---

## 一、打开就干：今天这三步

| 步 | 动作 | 怎么做 | 不做会怎样 |
|---|---|---|---|
| ① | **先看形状**（30 秒、零网络、零计费） | `bash scripts/fixtures/run_fixtures.sh` —— 三档一次跑完：机检自测、无通道骨架、骨架该红就红。末行自报「档数=3｜合期望=3｜不合=0｜不可判=0」 | 没见过形状就上手，容易把「排得整齐」当成「有出处」；这一档 30 秒就能看出两者的差别 |
| ② | **登记来源，逐条挂源** | 每个来源一行写进第四节：`- [S#] 标题（URL ｜检索日 YYYY-MM-DD）`；正文每条发现行末挂一个 `[S#]`。跨源不一致就两条都留，不合并、不取平均 | 缺检索日的来源行发 `E-ANCHOR`；没有锚的要点写进第二节同样发 `E-ANCHOR`——那时你要回来逐条补，比现在一条条挂贵 |
| ③ | **过机检，再交人** | `python3 -B scripts/check_brief.py <速览.md>`，按详行的 `E-*` 码逐条改；改完仍只是**草稿**：结论要不要下、怎么下，由人定 | 未取到没点名、判断词漏进正文、来源与锚对不上，都会跟着稿子进到人的判断里；这三类都是机检能拦的形制层，内容层还得回原文 |

一次性决议文件、评级与目标价、行情与持仓分析**不在这三步里**——本件只对「这一批来源被逐条挂实地排成一份速览」负责，且只对形制负责。

## 二、装上机 → 连通道 → 出结果

**装本件自己（主路）**：`npx skills add huhoo/cue-awesome --skill cn-research-brief`——这条只装本包；装完在你这一侧重列一次已安装 skill，清单里看得到 `cn-research-brief` 这个名字才算文件到位。没有 CLI 环境时的兜底是把本目录整个放进宿主支持的 skills 目录（`~/.workbuddy/skills/`）。

本件的取证腿是两枚可选辅助：`cue-research`（深研，跨源交叉验证）与 `cue-omni-reader`（解析，把 PDF／网页／音视频转成可摘的文本）。通道侧的实连走这条正路：

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
[print(r.get("id"), r.get("external_status"), (r.get("routing") or {}).get("url", "-")) for r in rows]'
DOMAIN_ID="<把这里换成上一行列出的那个域 id>"
ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
hit=[r["routing"]["url"] for r in rows if r.get("id")==sys.argv[1] and r.get("routing")]
print(*hit,sep="\n") if hit else sys.exit("未取到：该 id 不在目录现值里（或它没有 routing 里的 url 字段）——先跑上面那行列出现场的 id 再填")' "$DOMAIN_ID")"
[ -n "$ROUTING_URL" ] || { echo "取值失败：ROUTING_URL 为空——先跑上面那行列出现场 id，再把 DOMAIN_ID 换成其中之一" >&2; exit 1; }
curl -s -X POST "$ROUTING_URL" \
  -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  -w '\nHTTP %{http_code}\n'
```

`CATALOG` 是本面唯一一处目录入口字面（赋一次、散文不重抄）；`$ROUTING_URL` 是从该域 `routing` 里的 `url` 字段现取的逐字值，别把域名或路径抄死在这张面上。三层各自能证到什么，互不等价：**装好 skill ≠ 已配凭据 ≠ 通道已连**。匿名 `GET` 只证**目录可达**，本面不把它叫「已连」；带 key 实连且 `tools/list` 有返回才证那把 key 被接受，通过＝HTTP 200 且 `result.tools` 非空（只按形状认，本面不列工具名也不承诺枚数）。解析那一腿走宿主 MCP：**连上之后**宿主列出的工具里应当能看到这些名字——remote-only 那一面是 `parse`、`get_parse_status`、`cancel_parse` 三枚，带 Bridge 的那一面再加 `read_result`、`read_outline`、`discard_result`、`save_result`，共七枚；两路枚数不同，拿一个固定数判两路必错一边。名字在场只证它们被暴露，不证解析跑得通——URL 那一腿要拿一枚真实 URL 跑一次 parse 才证该路，本地文件那一腿要拿一枚真实本地文件跑一次 parse 才证该路（remote-only 不读本地件）；本件不自证也不代跑。目录返回里没有的域本面不装也不承诺；连接报错不等于域无数据，如实报。key 取自本地凭据设施，不进聊天、不在终端回显，本面不新增任何凭据读取动作；解析与深研的消耗以服务端返回为准，本件不代估也不代付，花之前一定先问。配置指路：数据腿官方配置页 <https://cuecue.cn/hub/mcp>、解析腿官方配置页 <https://cuecue.cn/hub/omni-reader>（本件两条腿都可能用上——目录发现走数据腿，远端正文取回走解析腿；深研那枚 `cue-research` 是独立入口、自带运行脚本，凭据同那把 key），取 key 走 <https://cuecue.cn/hub/api-key>。

## 三、离线样例：30 秒看到形状

```bash
cd cn-research-brief
bash scripts/fixtures/run_fixtures.sh
# 档① 机检自测：好样须过、四枚坏样须各发它该发的那一道 → selftest: ALL GREEN
# 档② 无通道骨架：scripts/make_outline.py 把 scripts/fixtures/sources.jsonl 排成一张待填骨架
# 档③ 骨架过机检：期望发 E-FORMAT——结论位仍是占位，骨架不该被当成速览交付
```

自己上手时同样两条命令：

```bash
python3 -B scripts/make_outline.py --sources 你的来源.jsonl --out 我的骨架.md
python3 -B scripts/check_brief.py 我的骨架.md
```

来源行必需三键：`title`／`url`／`asof`（检索日 `YYYY-MM-DD`），`id` 可省、缺省按行序给 `S1／S2…`。非法 JSON 行、缺键行、日期不是 `YYYY-MM-DD` 的行一律**未采信并逐行点名**，不静默跳行；一条可用行都没有时退 1——空清单不出骨架，那是没有出处，不是待填。

## 四、依赖与两条路的代价

- `python3`：机检与骨架发生器都用它，纯标准库、零网络、不发任何请求。
- 通道两枚辅助（`cue-research`／`cue-omni-reader`）是可选的：**不装不报错，代价是这份速览只剩你手上已有的来源**——多源取证与逐条出处那一层整块缺位（缺的是证据密度，不是排版），本件此时只出有形状的骨架、结论位留占位。装与不装都先问你要不要用，消耗花之前一定先问。
- 装了通道也不等于取到数：取数以实际返回为准；返货截断、字段缺失、只给摘要不给正文的，一律落第三节点名，不拿常识补。

## 五、机检四道与自校验

| 道 | 码 | 卡什么 |
|---|---|---|
| 道一 形制 | `E-FORMAT` | 头部四件自标逐字在位；四节齐且有序；一句话结论写成实句——占位串直接发红 |
| 道二 锚 | `E-ANCHOR` | 第二节每条发现行末带 `[S#]`；该编号在第四节有对应行；来源行必须同时带 URL 与检索日 |
| 道三 红线 | `E-BANWORD` | 评级／目标价／买卖与走势类断言零命中（同行挂 `[待人工]` 才放行）；改数词不得替数字打底 |
| 道四 未取到与计数 | `E-COVERAGE` | 正文写了「未取到／未检索到」的，第三节必须按名目**同指**逐条点名（剥括号注与标点后，字面全等、一方含另一方 ≥4 字、或汉字重合率 ≥0.6 算同指——同一件事换写法不判红）；第三节多列而正文没有同指表述的那一条同样发红；整节出现过「未取到」三字不算点过名；第四节一行来源都没有＝没有出处 |

```bash
python3 -B scripts/check_brief.py --help                              # 四道说明，零网络
python3 -B scripts/check_brief.py --selftest                           # 好样须过、四枚坏样须发红
python3 -B scripts/check_brief.py scripts/fixtures/good-brief.md       # 应 PASS
python3 -B scripts/check_brief.py scripts/fixtures/bad-no-anchor.md    # 应 FAIL：发现行没锚
python3 -B scripts/check_brief.py scripts/fixtures/bad-missing-section.md  # 应 FAIL：缺第三节
python3 -B scripts/check_brief.py scripts/fixtures/bad-rating-word.md  # 应 FAIL：判断词没挂待人工
python3 -B scripts/check_brief.py scripts/fixtures/bad-unsourced.md    # 应 FAIL：没有一行来源
python3 -B scripts/check_brief.py scripts/fixtures/good-brief.md --quiet   # 只报末行与计数
```

**枚数与行数一律取脚本自报行**（`FAIL: <文件>（N 条）`／`PASS: <文件>（…）` 后那行「扫过 N 行，发条 0 条」），本文不复写计数——一复写就成了第二个真值源。

## 六、包里有什么

```
SKILL.md                     主指令：定位/输入/四步/四节契约/通道与降级/红线/边界（必读）
README.md / README.en.md     本文件（中文权威／英文对照）
CHANGELOG.md                 版本记录
scripts/check_brief.py       机检四道（纯标准库，--help 可跑；判定全集在脚本，本文只指路）
scripts/make_outline.py      零通道骨架发生器（把来源清单排成待填骨架，不代填结论）
scripts/fixtures/            好样一枚＋坏样四枚＋来源样件＋离线三档 runner
```

## 七、常见问题与反模式

| 你想这么用 | 本件接不接 | 为什么 |
|---|---|---|
| 「把这三篇报道整理成一份要点清单」 | 接 | 多源、逐条挂源正是它的用途 |
| 「这一篇公告替我总结一下」 | 不接 | 单源是转述，不是多源速览——省事的代价是你以为交叉过了 |
| 「先给个结论，来源回头补」 | 不接 | 结论位靠后的来源补不上就是编；机检按设计发 `E-ANCHOR`／`E-FORMAT` |
| 「顺手写个目标价」 | 不接 | 判断位归人；写了就发 `E-BANWORD`，除非同行挂 `[待人工]` |
| 「没通道也先给我一份成品」 | 给的是骨架 | 缺的是多源取证那一层，不是排版——骨架过不了机检正是为了提醒这一步没做 |
