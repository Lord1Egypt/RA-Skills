# cn-table-to-chart

**一张表变成两样东西：能交给宿主画的图规格（图型／横轴／纵轴／序列，人来选）与读表要点（每条一个数，逐字回那一格）。不据图给投资建议、不判评级与目标价、不替你算表里没有的数。**

能画的图不缺工具，**缺的是「这个数确实在那一格」这一层核对**。差异化在三道硬门禁：数必须配列头逐字回那一格（表里没有的那个数当场发红，同一行里挪错列的那个数也当场发红——只有整行照序或 `「列头」=「数」` 两形之一才放行；表头被并成跨列表头时**连首格都不放行**，按列名对位就是猜）、同行给了页码又给行号时两个定位各比各的、四类限度必须逐类点名（沉默跳过＝漏）。断言那一面 0.1.4 起**不设引用豁免**：书名号里的内容同样参与判定——表里真有那句投资话，括成引用、写成第三方声音、或裸括着，都照样发红；逐字回表只证它出现过，不为它背书。合法出口只有一个：第三节点名、不括原话、带定位。代价写明：表内含投资倾向表述时引用它就红，**红的是引用行为不是造数**，这是选定的保守面。

**输入**：一张表的正文（本地文件，或经解析通道取回的 PDF／扫描件／照片里的表）
**输出**：四节产物（图的规格／读表要点／图的限度与未取到／来源与解析日），要点每条写成一行列表项（行首 `- ` 或 `* `），可直接交给宿主作图
**代价**：四节契约 + 一道机检；解析通道开没开，决定的是扫描件与远端那份表**取不取得到正文**——两条路各自缺什么、走哪条，写在 §二 与 §四
**机检**：`scripts/check_chart.py` 五道（形制与条数带／锚与定位／数逐字回那一格（全篇书名号都回表）／四类限度点名／投资与评级断言零命中），零网络、不代人算数、不执行表里提到的任何程序

---

## 一、打开就干：今天这三步

| 步 | 动作 | 怎么做 | 不做会怎样 |
|---|---|---|---|
| ① | **先看形状**（30 秒、零网络、零计费） | `bash scripts/fixtures/run_fixtures.sh` —— 三档一次跑完：机检自测（好样五枚须过、坏样十八枚须发红）、逐枚单跑 23 枚（逐枚报码集、发条数、靶位与判据段、用的是哪张表）、采集器出骨架且该红就红。末行自报「档数=3｜合期望=3｜不合=0｜不可判=0」 | 没见过形状就上手，容易把「画得出来」当成「数对得上」；这一档 30 秒就能看出差别 |
| ② | **排骨架，人来选规格** | `python3 -B scripts/collect_chart.py --source 那份表.md --out 图与要点.md` 把表里的数值按 `「列头」=「数」` 配对逐字搬进第二节并自带页码与行号（列头与该行格数对不上的走整行照序那一形）；第一节四件规格逐件填（图型要回答「我想看清什么关系」），第三节四类逐类填位置或写未见到 | 待核位没填就红在 `E-FORMAT` 与 `E-COVERAGE`（骨架不是产物）；要点行漏挂 `[S1]`、或来源行缺定位缺解析日，红在 `E-ANCHOR` |
| ③ | **过机检，再交给宿主画** | `python3 -B scripts/check_chart.py 图与要点.md --table 那份表.md`，按详行 `E-*` 码逐条改；画那一步在宿主或电子表格，本件不出图文件 | 凭印象写的数、悄悄少判的一类限度、把「这家可投」写进要点、或把表里真有的一句写进本文的结论位，都会跟着材料进到人的判断里——这些都属于形制层，机检能拦；数算得对不对还得回表 |

算同比、算占比、画文件、给投资结论**不在这三步里**——本件只对「这张表哪一格是多少、这张图立不立得住」负责。

## 二、装上机 → 连通道 → 出结果

**装本件自己（主路）**：`npx skills add huhoo/cue-awesome --skill cn-table-to-chart`——这条只装本包；装完在你这一侧重列一次已安装 skill，清单里看得到 `cn-table-to-chart` 这个名字才算文件到位。没有 CLI 环境时的兜底是把本目录整个放进宿主支持的 skills 目录（`~/.workbuddy/skills/`）。

本件唯一的取证腿是 `cue-omni-reader`（解析）：表在远端（云盘 PDF、扫描件、披露照片）时，正文靠它取回成本地能读的那一份——**本机没有那份文件也能读，而且逐字带页码或行号正是这一腿的价值**，所以它是主路不是装饰。它的连上判据（纯解析腿，没有 curl 可以替代它）：宿主列工具走 MCP 的 `tools/list` 握手——**连上之后**那份返回里应当能看到这些名字：remote-only 那一面是 `parse`、`get_parse_status`、`cancel_parse` 三枚，带 Bridge 的那一面再加 `read_result`、`read_outline`、`discard_result`、`save_result` 共七枚；两路枚数不同，拿一个固定数判两路必错一边。名字在场只证它们被暴露，不证解析跑得通——URL 那一腿要拿一枚真实 URL 跑一次 parse 才证该路，本地文件那一腿要拿一枚真实本地文件跑一次 parse 才证该路（remote-only 不读本地件）；本件不自证也不代跑。配置指路：解析腿官方配置页 <https://cuecue.cn/hub/omni-reader>（本件只依赖这一条腿，数据腿那页不在本面上引）。列不到就是没连：本件照旧只读你手上那份本地文件，代价是扫描与照片那一侧的表读不进来（缺的是那一格的逐字正文，不是排版）。「手里这份是不是出数那一版」这一格两条路都不判——本件不读版本标记、不对披露链，基准版由你指定并对齐。三层各自能证到什么，互不等价：**装好 skill ≠ 已配凭据 ≠ 通道已连**。key 取自本地凭据设施，不进聊天、不在终端回显，本面不新增任何凭据读取动作；解析的消耗以服务端返回为准，本件不代估也不代付，花之前一定先问。

## 三、离线样例：30 秒看到形状

```bash
cd cn-table-to-chart
bash scripts/fixtures/run_fixtures.sh
# 档① 机检自测：好样五枚须过、坏样十八枚须各发它该发的那一道 → selftest: ALL GREEN
# 档② 逐枚单跑：一枚一行，逐行报「期望只发 E-X／实发码恰为 E-X／发条几条／靶位与判据段／用的是哪张表」，并自报注入生效与否
# 档③ 采集器出骨架：数值按「列头」=「数」配对搬进第二节，骨架过机检期望红在两道——规格四件与限度四类都还没人判
```

自己上手时同样两条命令：

```bash
python3 -B scripts/collect_chart.py --source 我的表.md --out 图与要点.md
python3 -B scripts/check_chart.py 图与要点.md --table 我的表.md
```

采集器只读、不代选：它认 markdown 管道行（分隔行的上一行按语义当列头、不当数据也不当要点），把每行的数值格按 `「列头」=「数」` 配对逐字括进第二节并自带两枚定位；列头与该行格数对不上（合并格／跨列表头）时它退回整行照序那一形，仍然不猜哪一格对哪一列。第一节的四件规格与第三节的四类限度一律留待核位——**图型取决于你想看清的关系，机器按列形状猜会把「能画」说成「该这么画」**，那一格留给人。认不出任何数值行、或原文是空的，它退 1 并说明；文件读不到、`--asof` 形制不对走退 3（取值域故障，不读成「零违例」）。列头模型与机检共用同一份（采集器 `from check_chart import table_model`），两处对「哪一格」的理解不许各写一套。

## 四、依赖与两条路的代价

- `python3`：机检与采集器都用它，纯标准库、零网络、不发任何请求。
- 解析辅助 `cue-omni-reader` 是可选的：**不装不报错，代价是这份产物只能对你手上那一份文件负责**——扫描件与远端那侧的表读不进来。装与不装都先问你要不要用，消耗花之前一定先问。
- 连了通道也不等于取到正文：表格被裁断、合并单元格对不回列头、照片糊掉看不清那一格的，一律落第三节点名，不拿常识补、不拿上一年的数凑。机检按列头定位不到那一格就发红（详行点名是空值还是列头格数对不上），**列头被并时连首格都不放行**——把并列的列头默认对到第一格就是猜；这一行要么整行照序写、要么写进第三节。
- 算的那一步在宿主：同比、环比、占比、平均本件一个都不算——只搬表里已有的格，并把每格指回位置；表里没有的数进了要点发 `E-QUOTE`，数在表里却配错了列（拿同一行另一格的数顶你要说的那一格）同样发 `E-QUOTE`。
- 数据边界：产物带着表里的数与口径（披露表常含未公开口径）。存放、转发、给谁看由你自己负责；本件不上传、不落盘到本包之外。
- 定位会随文件改动失效：页码与行号只在解析日那一刻成立，对方换了一版披露，这份规格就得重做。

## 五、机检五道与自校验

| 道 | 码 | 卡什么 |
|---|---|---|
| 道一 形制 | `E-FORMAT` | 头部四件自标逐字在位；四节齐且有序；第一节四件规格齐在且都不是待核位；第二节要点 3–10 条——**按列表符计**（行首必须是 `- ` 或 `* `），节内只有普通行时详行点名「这一节没有以 - 或 * 起的行」 |
| 道二 锚 | `E-ANCHOR` | 每条要点行末尾一枚 `[S#]` 且这一行有定位；锚在第四节有对应行；来源行必须同时带定位与解析日——日期要挂在「解析日」标签下且是日历上存在的一天（换成「合同签署日」那种标签发红；机检只核这两件，核不了那天是否真是取回当天） |
| 道三 逐字 | `E-QUOTE` | 全篇任何一行里的「」都逐字在表里（条目行内外一样——非条目行括一句表里没有的话当场发红）；数还要落在所报那一行的那一格：`「列头」=「数」` 配对，或整行照序把那一行的数按列次序括全，两形之一才放行（挪同行另一格的数顶替、把空值「—」说成有数、跨表借列头都发红，详行点名是哪一支）；**配对形的前提是列头格数等于该行数据格数**——表头被并成跨列表头时连首格都不放行，按列名对位就是猜，那一行只认整行照序或落第三节；同一行既给页码又给行号时**两个定位各自成立**（只读其一会把假的那枚放过）；没给 `--table` 时明写不可判、不并入通过 |
| 道四 点名 | `E-COVERAGE` | 第三节四类限度逐类在位，每类要么给位置要么写未见到／未取到，待核不算点名；别处报了未读到而第三节没点名发红；第四节零来源行发红 |
| 道五 断言 | `E-ADVICE` | 投资建议、评级动作、目标价一类**单靠词就发条**（不要求情态词在场）；换了说法的判断也拦——最高级／比较级形态与投资结论对象词落在**同一语义段**即发条。语义段只按结构切：标题／列表项／表格／引用块另起段，**仅有缩进的普通续行并入上一段**（换行与缩进都不算躲开）。**0.1.4 起不设引用豁免**：书名号里的内容同样判——表里真有那句投资话，括成归属位（表注原文：「…」）、写成第三方声音（有人主张「…」）或裸括着都照样发红；逐字回表只证它出现过，不为它背书。合法出口只有一个：**第三节点名、不括原话、带定位**；代价是表内含投资倾向表述时引用它就红——**红的是引用行为不是造数，这是选定的保守面**；挂 `[待人工]` 要挂在同一语义段里 |

```bash
python3 -B scripts/check_chart.py --help                                                        # 五道说明，零网络
python3 -B scripts/check_chart.py --selftest                                                     # 好样五枚须过、坏样十八枚须发红
python3 -B scripts/check_chart.py scripts/fixtures/good-chart.md --table scripts/fixtures/target-table.md          # 应 PASS
python3 -B scripts/check_chart.py scripts/fixtures/bad-spec.md --table scripts/fixtures/target-table.md            # 应 FAIL：图型仍是待核位
python3 -B scripts/check_chart.py scripts/fixtures/bad-no-anchor.md --table scripts/fixtures/target-table.md        # 应 FAIL：要点行没挂锚
python3 -B scripts/check_chart.py scripts/fixtures/bad-invented-number.md --table scripts/fixtures/target-table.md  # 应 FAIL：那个数表里没有
python3 -B scripts/check_chart.py scripts/fixtures/bad-unbound-quote.md --table scripts/fixtures/target-table.md    # 应 FAIL：非条目行括了一句表里没有的话
python3 -B scripts/check_chart.py scripts/fixtures/bad-cell-misplaced.md --table scripts/fixtures/target-table.md   # 应 FAIL：拿同一行另一格的数顶那一格
python3 -B scripts/check_chart.py scripts/fixtures/bad-no-header-pair.md --table scripts/fixtures/target-table.md    # 应 FAIL：数没配列头，也没整行照序
python3 -B scripts/check_chart.py scripts/fixtures/bad-cell-empty-zero.md --table scripts/fixtures/target-table.md   # 应 FAIL：把空值「—」那一格说成有数
python3 -B scripts/check_chart.py scripts/fixtures/bad-merged-bind.md --table scripts/fixtures/target-table-merged.md # 应 FAIL：表头被并还想按列名配到首格
python3 -B scripts/check_chart.py scripts/fixtures/good-merged-order.md --table scripts/fixtures/target-table-merged.md # 应 PASS：同一张跨列表头改走整行照序那一形
python3 -B scripts/check_chart.py scripts/fixtures/bad-quote-conclusion.md --table scripts/fixtures/target-table-noted.md # 应 FAIL：表注里真有这句，但被写进本文的结论位
python3 -B scripts/check_chart.py scripts/fixtures/bad-quote-source-only.md --table scripts/fixtures/target-table-noted.md # 应 FAIL：归属位引用（表注原文：「…」）——0.1.4 起不再豁免
python3 -B scripts/check_chart.py scripts/fixtures/bad-quote-third-party.md --table scripts/fixtures/target-table-noted.md # 应 FAIL：第三方声音括原话
python3 -B scripts/check_chart.py scripts/fixtures/bad-quote-bare.md --table scripts/fixtures/target-table-noted.md       # 应 FAIL：裸引表里的投资话
python3 -B scripts/check_chart.py scripts/fixtures/good-quoted-note.md --table scripts/fixtures/target-table-noted.md  # 应 PASS：合法出口——第三节点名、不括原话、双定位
python3 -B scripts/check_chart.py scripts/fixtures/good-plain-quote.md --table scripts/fixtures/target-table-noted.md   # 应 PASS：同上，单页码定位
python3 -B scripts/check_chart.py scripts/fixtures/good-third-party.md --table scripts/fixtures/target-table-noted.md   # 应 PASS：同上，单行号定位
python3 -B scripts/check_chart.py scripts/fixtures/bad-missing-limit.md --table scripts/fixtures/target-table.md    # 应 FAIL：四类限度少点一类
python3 -B scripts/check_chart.py scripts/fixtures/bad-advice.md --table scripts/fixtures/target-table.md           # 应 FAIL：写了目标价
python3 -B scripts/check_chart.py scripts/fixtures/bad-bare-outcome.md --table scripts/fixtures/target-table.md     # 应 FAIL：裸投资断言（无情态词）
python3 -B scripts/check_chart.py scripts/fixtures/bad-superlative.md --table scripts/fixtures/target-table.md      # 应 FAIL：换了说法的投资结论
python3 -B scripts/check_chart.py scripts/fixtures/bad-conclusion-crossline.md --table scripts/fixtures/target-table-noted.md  # 应 FAIL：「结论：」顶格、引文缩进在下一行（分行不算躲开）
python3 -B scripts/check_chart.py scripts/fixtures/bad-author-voice-verb.md --table scripts/fixtures/target-table-noted.md     # 应 FAIL：作者声音在旧词表外（表明），照样不豁免
python3 -B scripts/check_chart.py scripts/fixtures/good-chart.md --quiet                          # 只报末行与计数
```

**条数与发条数一律取脚本自报行**（`FAIL: <文件>（N 条）`／`PASS: <文件>（…）` 后那行「扫过 N 行，发条 0 条，不可判 M 项」），本文不复写计数——一复写就成了第二个真值源。

## 六、包里有什么

```
SKILL.md                        主指令：定位/输入/四步/四节契约/通道与降级/三条硬边界/边界（必读）
README.md / README.en.md        本文件（中文权威／英文对照）
CHANGELOG.md                    版本记录
scripts/check_chart.py          机检五道（纯标准库，--help 可跑；判定全集在脚本，本文只指路）
scripts/collect_chart.py        离线采集器（把表里的数逐字搬成四节骨架，不代选图型、不代人算数）
scripts/fixtures/               合成表三枚（默认／带表注／跨列表头）＋好样五枚＋坏样十八枚＋离线三档 runner
```

## 七、常见问题与反模式

| 你想这么用 | 本件接不接 | 为什么 |
|---|---|---|
| 「把这张表整理成能画图的规格」 | 接 | 规格四件＋数逐字回表正是它的用途 |
| 「顺手告诉我这数据说明什么」 | 不接 | 判断位归人；写成作者句子就发 `E-ADVICE`，除非同段挂 `[待人工]` |
| 「帮我算一下同比和占比」 | 不接 | 本件一个数都不算，只搬已有的格；算的那步交回宿主或电子表格 |
| 「图你直接画出来给我」 | 不接 | 产物是规格与要点，渲染在宿主——不在件里藏一个渲染器，画错了没人负责 |
| 「这个数我记得大概是 1.6，先写进去」 | 不接 | 写进「」就得逐字在那一格表里并配下列头——要么照抄那一格，要么写进第三节说未读到 |
| 「这一行里另一格的数，先顶成我要说的那一列」 | 不接 | 数要落在所报那一格：`「列头」=「数」` 配对或整行照序，两形之一；顶错列当场发 `E-QUOTE`（详行点名是格位哪一支） |
| 「表里没有的一句话，括进书名号就算引用」 | 不接 | 全篇书名号只有一个用途＝逐字引表里的原文；回不到表就发 `E-QUOTE`，道五也不给它照抄豁免 |
| 「表注里真有这句，我把它写成本文的话」 | 不接 | 逐字回表只证这话在表里出现过，不证它不是本文的结论——0.1.4 起书名号里也判：写进结论位、挂归属位、裸括着，同样发 `E-ADVICE`（除非同段挂 `[待人工]`）；换行、缩进、补一句「本件不判」都不改变这一句进了本文 |
| 「我没写谁说的，光把那句括起来总行」 | 不接 | 0.1.4 起不设引用豁免：裸引表里的投资话同样发 `E-ADVICE`——只证它逐字在表，不为它背书 |
| 「第三方说过的话，本文转述」 | 不接（指含投资倾向那句） | 出处或第三方主语写在框架里也不能把表里那句投资话括进本文；要处理它就走第三节点名、不括原话、带定位 |
| 「表里那句是原文，我照抄进归属位总行吧」 | 不接 | 归属位（表注原文：「…」）不再豁免——红的是引用行为本身；合法出口是第三节点名「表内含投资倾向的表述，本件不引用、不采信」并给位置 |
| 「表头被并了，按列名对到第一格总行得通」 | 不接 | 配对形的前提是列头格数等于该行数据格数；不等时首格也是猜，那一行只认整行照序，或写进第三节（发 `E-QUOTE`） |
| 「另一家公司的数也并进这张图」 | 不接 | 一次一张表；跨表拼接的对齐与口径问题不在这份形制里 |
| 「表是照片，我手上没有文件」 | 接，走解析通道 | 把正文取回本地再登记成来源行；拿不到就落第三节，不凭印象补格 |
