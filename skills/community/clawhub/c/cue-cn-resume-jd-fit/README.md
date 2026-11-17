# cn-resume-jd-fit

**一份简历对一枚 JD 的双向核对：每条要求挂回简历的一句原话，缺口分两栏点名，不排先后、不下录用结论。**

评价不缺，**缺的是能被人逐条回查的对应关系**。差异化在三道硬门禁：证据那句必须逐字在简历里（造的那句当场发红）、每条必须双锚、判了缺口必须点名。

**输入**：一份简历 ＋ 一枚 JD（本地文件，或经解析通道取回的 PDF／网页／截图正文）
**输出**：四节核对报告（一句话结论／逐条对齐／缺口两栏／来源带定位与解析日），一条要求一行，可直接带去讨论
**代价**：四节契约 + 一道机检；解析通道开没开，决定的是**远端那两份正文取不取得到**——「这两份是不是当前这一版」这一格两条路都不判（本件不读版本标记、不对发布链，由你指定基准版）；两条路各自缺什么、走哪条，写在 §二 与 §四
**机检**：`scripts/check_fit.py` 五道（形制与条数带／双锚与定位／两侧逐字回原文／缺口点名／录用与排序断言零命中），零网络、不执行任何一侧附带的代码

---

## 一、打开就干：今天这三步

| 步 | 动作 | 怎么做 | 不做会怎样 |
|---|---|---|---|
| ① | **先看形状**（30 秒、零网络、零计费） | `bash scripts/fixtures/run_fixtures.sh` —— 三档一次跑完：机检自测、七枚坏样逐枚单跑、采集器出骨架且该红就红。末行自报「档数=3｜合期望=3｜不合=0｜不可判=0」 | 没见过形状就上手，容易把「看着挺像那么回事」当成「每条都回得去」；这一档 30 秒就能看出差别 |
| ② | **排骨架，逐条对齐** | `python3 -B scripts/collect_fit.py --jd JD.md --resume 简历.md --out 核对.md` 把 JD 的要求逐条搬进第二节；每条后面把简历里的**逐字原话**抄进证据位，行末挂 `[S1]`（要求挂 `[S2]`） | 待填位没抄进去就红在 `E-QUOTE`（骨架不是核对报告）；只挂一枚锚、或来源行缺定位缺解析日，同样发红 |
| ③ | **过机检，再带去讨论** | `python3 -B scripts/check_fit.py 核对.md --jd JD.md --resume 简历.md`，按详行 `E-*` 码逐条改；报告里那句结论只说匹配到哪一层，录不录由人定 | 转述冒充原文、缺口不点名、把「建议录用」写进结论，都会跟着材料进到人的判断里——这三类都是形制层，机检能拦；内容层还得回原文 |

筛人、排序、给分、跨候选人比较**不在这三步里**——本件只对「这两份文档当下载着什么、能不能互相指回去」负责。

## 二、装上机 → 连通道 → 出结果

**装本件自己（主路）**：`npx skills add huhoo/cue-awesome --skill cn-resume-jd-fit`——这条只装本包；装完在你这一侧重列一次已安装 skill，清单里看得到 `cn-resume-jd-fit` 这个名字才算文件到位。没有 CLI 环境时的兜底是把本目录整个放进宿主支持的 skills 目录（`~/.workbuddy/skills/`）。

本件唯一的取证腿是 `cue-omni-reader`（解析）：简历或 JD 在远端（招聘页、云盘 PDF、截图）时，正文靠它取回成本地能读的那一份——**本机没有那份文件也能读**，这是主路不是装饰。它的连上判据（纯解析腿，没有 curl 可以替代它）：宿主列工具走 MCP 的 `tools/list` 握手——**连上之后**那份返回里应当能看到这些名字：remote-only 那一面是 `parse`、`get_parse_status`、`cancel_parse` 三枚，带 Bridge 的那一面再加 `read_result`、`read_outline`、`discard_result`、`save_result` 共七枚；两路枚数不同，拿一个固定数判两路必错一边。名字在场只证它们被暴露，不证解析跑得通——URL 那一腿要拿一枚真实 URL 跑一次 parse 才证该路，本地文件那一腿要拿一枚真实本地文件跑一次 parse 才证该路（remote-only 不读本地件）；本件不自证也不代跑。配置指路：解析腿官方配置页 <https://cuecue.cn/hub/omni-reader>（本件只依赖这一条腿，数据腿那页不在本面上引）。列不到就是没连：本件照旧只读你已有的那两份，代价是**远端那侧的正文读不进来**（缺的是那一份逐字正文，不是排版）。版本同一性另说：通道连上也不判——解析只按你指定的对象取正文，本件不读版本标记、不对发布链，「是不是对方现在用的那一版」由你指定基准版并对齐。三层各自能证到什么，互不等价：**装好 skill ≠ 已配凭据 ≠ 通道已连**。key 取自本地凭据设施，不进聊天、不在终端回显，本面不新增任何凭据读取动作；解析的消耗以服务端返回为准，本件不代估也不代付，花之前一定先问。

## 三、离线样例：30 秒看到形状

```bash
cd cn-resume-jd-fit
bash scripts/fixtures/run_fixtures.sh
# 档① 机检自测：好样须过、七枚坏样须各发它该发的那一道 → selftest: ALL GREEN（枚数由脚本现算自报）
# 档② 逐枚单跑：一枚一行，逐行报「期望只发 E-X／实发码恰为 E-X／发条几条」，并自报注入生效与否
# 档③ 采集器出骨架：scripts/collect_fit.py 把合成 JD 的 5 条要求搬进第二节，骨架过机检期望红在证据待填那 5 行
```

自己上手时同样两条命令：

```bash
python3 -B scripts/collect_fit.py --jd 我的JD.md --resume 我的简历.md --out 核对.md
python3 -B scripts/check_fit.py 核对.md --jd 我的JD.md --resume 我的简历.md
```

采集器只读、不代人匹配：它把要求段（节标题含「要求／资格」）逐条搬进第二节，证据位一律留待填；要求段用的是别的标题时带 `--require-keyword` 指定。两侧引号里的句子都必须能在对应文件里逐字找到——**这是本件最硬的一道判据**，转述冒称原文、凭印象造证据，都在这一格被抓。抽不出任何要求行时它退 1 并说明；文件读不到、日期形制不对走退 3（取值域故障，不读成「零违例」）。

## 四、依赖与两条路的代价

- `python3`：机检与采集器都用它，纯标准库、零网络、不发任何请求。
- 解析辅助 `cue-omni-reader` 是可选的：**不装不报错，代价是这份核对只能对你手上那两份文件负责**——远端那侧的正文读不进来。装了也不换一样东西：版本同一性两条路都不判（不读版本标记、不对发布链），要盯「是不是当前那一版」得由你指定基准版再对齐。装与不装都先问你要不要用，消耗花之前一定先问。
- 连了通道也不等于取到正文：扫描版 PDF、只给摘要不给全文、页面改版取不到那段的，一律落第三节点名，不拿常识补。
- 数据边界：报告里会带着两侧原文（含个人信息）。存放、转发、给谁看由你自己负责，**先告知当事人**；本件不上传、不落盘到本包之外，也不读任何人事系统。
- 行号会随文件改动失效：报告里的定位只在解析日那一刻成立，对方换了一版 JD，这份核对就得重做。

## 五、机检五道与自校验

| 道 | 码 | 卡什么 |
|---|---|---|
| 道一 形制 | `E-FORMAT` | 头部四件自标逐字在位；四节齐且有序；一句话结论只一行且 ≤80 字符，并且这一行要有两件结构在场——**报到哪几条**（计数＋条）与**缺口点名**（未取到／无证据／只有部分证据一类），缺一发条；逐条对齐 3–15 行 |
| 道二 锚 | `E-ANCHOR` | 每条对齐行**两个锚**（要求一枚、证据一枚）且第四节都有对应行；来源行必须带 `文件:行号` 或 URL ＋ 解析日 |
| 道三 逐字 | `E-QUOTE` | 要求那句逐字在 JD 里、证据那句逐字在简历里；只给一侧原文时另一侧明写不可判，**不并入通过** |
| 道四 缺口 | `E-COVERAGE` | 第三节两栏都要在位；第二节判为无证据的要求必须在这一栏留名；第四节零来源行发红 |
| 道五 断言 | `E-RANK` | 推荐录用／建议录用／优先录用／淘汰／排名／排序／打分 一类零命中；换说法的名次同拦——最高级／比较级形态（最适合／更匹配／优于…）与结论对象词（本岗位／候选人／申请者…）同句同现即发条，带锚也不放行（同行挂 `[待人工]` 才放行；引号里的原话先剥再判，那是被引者说的）。**「结论」这一格另有一条**：第一节引原话必须在同一行写明是谁的话（简历自述／JD 原文一类），不写归属就发红——被引者的话搬进结论位就成了报告自己的名次，这一判与引号内容无关 |

```bash
python3 -B scripts/check_fit.py --help                                                        # 五道说明，零网络
python3 -B scripts/check_fit.py --selftest                                                     # 好样须过、七枚坏样须发红
python3 -B scripts/check_fit.py scripts/fixtures/good-fit.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md   # 应 PASS
python3 -B scripts/check_fit.py scripts/fixtures/bad-format.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # 应 FAIL：结论不是一句话
python3 -B scripts/check_fit.py scripts/fixtures/bad-no-anchor.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # 应 FAIL：证据没挂锚
python3 -B scripts/check_fit.py scripts/fixtures/bad-invented-evidence.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # 应 FAIL：证据那句是编的
python3 -B scripts/check_fit.py scripts/fixtures/bad-missing-gap.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # 应 FAIL：判了缺口不点名
python3 -B scripts/check_fit.py scripts/fixtures/bad-hire-verdict.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # 应 FAIL：下了录用断言
python3 -B scripts/check_fit.py scripts/fixtures/bad-concl-structure.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # 应 FAIL：结论位没结构（没报到哪几条、没点名缺口）
python3 -B scripts/check_fit.py scripts/fixtures/bad-concl-quote.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # 应 FAIL：结论位引原话没写归属
python3 -B scripts/check_fit.py scripts/fixtures/good-fit.md --quiet                            # 只报末行与计数
```

**枚数与行数一律取脚本自报行**（`FAIL: <文件>（N 条）`／`PASS: <文件>（…）` 后那行「扫过 N 行，发条 0 条，不可判 M 项」），本文不复写计数——一复写就成了第二个真值源。

## 六、包里有什么

```
SKILL.md                       主指令：定位/输入/四步/四节契约/通道与降级/红线/边界（必读）
README.md / README.en.md       本文件（中文权威／英文对照）
CHANGELOG.md                   版本记录
scripts/check_fit.py           机检五道（纯标准库，--help 可跑；判定全集在脚本，本文只指路）
scripts/collect_fit.py         离线采集器（把 JD 要求逐条搬成四节骨架，不代人匹配）
scripts/fixtures/              合成简历与合成 JD 各一枚＋好样一枚＋坏样七枚（含结论位缺结构、结论位引号无归属两支）＋离线三档 runner
```

## 七、常见问题与反模式

| 你想这么用 | 本件接不接 | 为什么 |
|---|---|---|
| 「这份简历配这枚 JD，帮我把对应关系列出来」 | 接 | 要求→证据逐条挂原话正是它的用途 |
| 「顺手告诉我录不录」 | 不接 | 判断位归人；写了就发 `E-RANK`，除非同行挂 `[待人工]` |
| 「给个匹配度百分比」 | 不接 | 那个数没人能回查；本件只交付能回到原文的对应关系 |
| 「这几份简历一起排个序」 | 不接 | 一次一份；批量与比较是另一条路，偏差问题不在本件形制里 |
| 「简历里那句我记得大概是这样，先写进去」 | 不接 | 加引号就得逐字——要么照抄那一句，要么写「无证据」落第三节点名 |
| 「JD 在招聘页上，我没有文件」 | 接，走解析通道 | 把正文取回本地再登记成来源行；拿不到就落第四节，不凭页面印象写 |
