---
name: cue-sector-overview
displayName: 行业景气全景-cn
slug: cue-sector-overview
version: "0.1.35"
summary: "行业景气全景（A股口径）：六节固定形制，分析维度按行业动态生成 2–4 个——每个判断词当场答得出「凭什么：哪条序列、哪个口径、截至哪天」。"
description: "给行业名＋时间窗，产出六节固定景气度报告：维度不背框架库，由深研按行业动态生成 2–4 个；交付带可比序列锚的行业冷热证据——判断词当场可答凭哪条序列与口径、截至哪天，附代表 A 股公司清单与覆盖缺口。评级词零容忍，不出行业观点。不适合：荐股择时、承诺非公开数据覆盖。适合：行业开题、会前准备、尽调章节。Do NOT use for: stock picks or timing, promises of non-public coverage. 装：npx skills add huhoo/cue-awesome --skill sector-overview（装完重列清单核对）。"
tags: [投研, 行业研究, A股, 景气度]
license: MIT
consumes: []
produces:
  - industry-material-pack
  - run-log
  - sector-report
  - source-index
agent_created: true
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    envVars:
      - name: CUE_API_KEY
        required: false
        description: "可选凭据：缺位时本包按面文所述走用户直供与降级路径；带上才走渠道侧取证。"
  optionalSkills: ["cue-data-mcp", "cue-research", "cue-omni-reader"]
---

# sector-overview — 行业景气全景-cn（AI 初稿）

> 交付的是**带可比序列锚的行业冷热证据**，不是观点成品。本件与公开行业研报的差异不在篇幅，在纪律：
> **每一个判断词都当场答得出「凭什么」——凭哪条序列、哪个口径、截至哪天**。
> 分析维度不背框架库：每次运行先由深研按行业类型动态生成 2–4 个维度再取数（套件内核的行业镜像）。

## 0. 什么时候用 / 不用

| 你要 | 用什么 |
|---|---|
| 一个行业近 4 季的冷热证据简报（六节 ≤6 页） | **本 skill** |
| 某家公司财报深度点评 | `cn-earnings-note` |
| 见客户前 30 秒一页纸 | `tear-sheet` |
| 持仓的日期表 | `catalyst-calendar` |
| 「看好哪个行业」式建议 | 不做——评级词零容忍、无豁免区（铁律 3） |

## 1. 铁律（全流程有效）

1. **AI 初稿三声明**：自标题行起 6 行内含三字段——「AI 初稿」字样（代码只认这四字，不要求「本页为」前缀）、`asof:` 日期、通道用量计数（机检①；三字段的形状=checker 现值，见 §3 `+check` 那条自查命令）。「不构成投资建议」是契约要求你写的句子，机器不验它必填——它在机器侧的唯一作用是让道③把这句短语从禁词扫描里摘出（摘除后同句其余部分照扫）。
2. **判断词-锚同行（本件命门）**：哪些词算判断词**不靠本文列举**——判定=`check_sector.py` 里 `JUDGE_PHRASE` ∪ `JUDGE_SINGLE` 两条现值（常见例：回暖、承压、拐点、升、降；**例不穷尽**，全量随现值走，一条命令自查见 §3 `+check` 行）。命中即同句挂可比序列锚 `S<n>`（该锚由道④保证在 sources 双向可解析）；挂不上即走**态二逐字句**「无可比序列，不做景气判定」：逐字整句放行，改写句只要还带判断词或态二提示词（提示词族=`STATE2` 与 `STATE2_HINT_RE` 现值）就 FAIL；**两者都不带的含糊句（如把判断写成不在集内的说法）机检不认，属人工复核面**——本文不写成机器全捕。无源句软接另禁，见铁律 4。判断词无锚=幻觉句，与姊妹件的日期幻觉同族。
3. **评级词零容忍、豁免区=无**：行业层也不产「看好/推荐/减持某行业」表述；禁词族=`BANNED_RE` 现值（常见例：看好、建议、目标价、买入——**例不穷尽**，全量随现值走），扫描面含正文与 sources 的 ref/claim。机器唯一的摘除是 `NOT_INVEST_RE` 那一类「不构成…投资建议」声明短语，**除此之外零豁免**。
4. **缺数申报，禁补**：协会/产能口径无源即标「缺数」，无源句禁词=`GUESS_RE` 现值（常见例：据估计、市场预期——例不穷尽）命中即 FAIL、无补锚通道；research 件标可信级 L3（深研二手）入复核清单；**行业均值的预期类数字默认不取**（高危 oversell，引用即走 expectation-pool 契约含 source_tier）。
5. **花之前必问 + 维度动态生成**：research ≤1 次，发起前先报「预计耗时与消耗」再征询；**该次 deep-research 的产出之一是本行业 2–4 个分析维度**（如养殖看存栏/猪价，光伏看排产/组件价），维度写进台账再取数——不套上一个行业用过的清单。

## 2. 输入契约（≤3 问）

- **行业名**：申万/中信一级或口语名；歧义按 entity 消歧同款流程列候选拒猜（如「芯片」→半导体/芯片设计列选）；
- **窗口**：缺省=近 4 个**完整**季度（未走完的当季不入序列比较）；
- **角度**（可选）：`量价 | 政策 | 竞争格局`，缺省全六节；指定角度只缩详略、不放松铁律 2。

## 3. 管线（五段+门禁，逐节追加同姊妹件；开工建 `progress.md`）

- `+scope`：行业名消歧定分类口径（申万 vs 中信选一注明）；窗口落表。
- `+series`：`macro` 域取行业量价序列（工具与入参 schema 一律当场发现，域清单与工具面以 catalog 现值为准，本文不抄）；同比/环比/累计三 basis 标签制照姊妹件；**表必带 asof，图不做**。
- `+research`：报成本征询后发起 ≤1 次——产出 ①本行业动态维度 ②协会口径数据/产能投放节奏（可信级 L3 入 sources；定义在同仓财报点评件面，本件只引用不另定义）；零命中或用户拒发→相关节直接走态二/缺数句。
- `+policy`：`statute`/`regulatory_cn` 建政策时间线（行规格与 statute 锚三件齐规格都在 `references/policy-timeline.md`；机器侧判据=`check_sector.py` 里 `STATUTE_SPEC_RE` 现值，两处不一致时以现值为准）。
- `+companies`：`disclosure_cn` 取 ≥3 家代表公司关键指标**聚合表**——只聚合、零点评，单司数字全走 `S<n>` 锚；成表后与 `+series` 互证（个体≠行业，背离要注记）。
- `+check`（不过不交付）：`python3 scripts/check_sector.py <report.md> --sources <sources.jsonl> --window <YYYY-MM-DD~YYYY-MM-DD>`——四道：①声明行 ②**判断词-锚同行机检**（含态二逐字句白名单）③禁词+评级零容忍 ④数字行锚+双向可解析+六节语义定位与顺序（锚型枚举=`KIND_ENUM`、保留节名=`RESERVED_H2`、数字形状=`NUM_CELL_RE` 与 `NUM_PROSE_RE`，一律以现值为准）。机检要点详 `references/section-skeleton.md` 尾节。（词面域一条命令自查，任意目录整行粘贴即可跑、命令自带安装后路径；装在别处把 `~/.workbuddy/skills/` 换成你的技能安装目录，Windows 路径形如 `C:\Users\<用户名>\.workbuddy\skills\sector-overview\scripts\check_sector.py`，两条命令都走 POSIX 工具，Windows 请在 Git Bash/WSL 内跑）：`grep -n -A3 "JUDGE_PHRASE = \|JUDGE_SINGLE = \|BANNED_RE = \|GUESS_RE = " ~/.workbuddy/skills/sector-overview/scripts/check_sector.py`；守护样清单同形现跑：`bash ~/.workbuddy/skills/sector-overview/scripts/run_fixtures.sh`——本文不抄域清单也不抄条数，跑什么是什么。

## 4. 输出契约

**开口请带上时点，输出标数据日期**：请求里给出报告期／基准日或回看窗口；成品首行标注**数据日期**，当它与用户所指日期不一致时，正文禁用「今日」「最新」，一律改写为「截至 <日期>」。

**未见于本次返回的一律写「未检索到」**：参数名、字段名、枚举值没有出现在本次工具返回里的，不得凭印象填写；写「未检索到」并记入待核清单或覆盖率账，不得留空顶替。
```
sector-<行业名>-<窗口>/
├── report.md        交付物：三声明页眉+六节（每节带 [执行蓝图] 落位）+ 附录来源索引
├── sources.jsonl    行式同姊妹件契约（序列行 kind=macro、ref=序列名+平台+asof；research 带 conv_id）
└── progress.md      台账：消歧结论+动态维度清单+缺数/弃句记录
```

## 5. 套件连携

本件的「行业素材段」（§2+§3 的带锚序列与政策时间线）可作外部写作的参考输入：带锚序列与政策时间线留在文件里，被引用时锚随行走，不得只搬结论。配置指针：数据腿官方配置页 <https://cuecue.cn/hub/mcp>、解析腿官方配置页 <https://cuecue.cn/hub/omni-reader>（本件取证腿＝`cue-data-mcp` 与 `cue-research`，`cue-omni-reader` 按需）。

## 6. 边界与拒答

- 「直接说这个行业能不能买」→ 拒绝并引铁律 3；
- 行业无可比序列在场 → 允许全篇态二（薄简报合法）——**空结论合法，无锚判断违法**；
- 窗口内协会数据断更 → 缺数申报+复核清单挂行，不回退旧值顶替。

## 7. 出处

- 基座：anthropics/financial-services `sector-overview`（Apache-2.0）——六节型任务结构来源。
- 本包为**A股化重实现而非搬运**：数据层完全 Cue 通道化；判断词-锚同行纪律、维度动态生成、政策锚三件齐规格为本套件自建（对照同类公开件于此零处——§5-7 区隔点）。出处声明见仓库根 `NOTICE.md`。
