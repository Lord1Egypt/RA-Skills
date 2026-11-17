# 覆盖账本契约（coverage ledger）

> 解决的问题：深度点评天然是「连续剧」，但工具只演「单集」——上季说过什么指引、锚兑现没有、
> 风险项两季漂移没有，全凭人脑记。账本把这些进机器可断言的台账：`ledger-<period>.json`。
> **边界声明：这不是评级变化事件流。**账本记的是「公司自己说过的话与披露事实的跨期对账」，
> 不含也不生成任何评级动作；观点位永远 `[待人工]`（SKILL 铁律 1）。

契约锚：spec §F1（v2 字段规格，D1–D11 缺陷编号可溯）；回放双证=桌面手工版与机器版逐格相等
（`+recall` 于美的 2025AR→2026H1 实装，15 格全数相等或归因等价）。本文与生产机检
（`check_note.py --ledger/--prev-ledger`）同源；字段以 fixture 实装形状为准。

---

## 1. 文件与命名（每季一文件，历史永不改写）

- 文件名 `ledger-<period>.json`，period 词表同 SKILL §2（半年报 `2026H1`、年报纯年份 `2026`）；
- **当季 run 生成当季文件；历史文件永不原地改写**（append-only 原则 D1）——修史=新文件里追加解释，不改旧行；
- `ledger_of`：互链上一季账本或基线（如 `"earnings-000333-2025AR:baseline.json"`；首季=null）；
- `run`：本账归属 run_dir 短名（如 `earnings-000333-2026H1`）；**一切来源引用统一 `<run短名>:S##`**（D9），
  跨季引用带各自 run 前缀，不靠脑内上下文；
- `schema`：实现标签字符串（现值 `cn-earnings-note/ledger@0.2.0-draft`）。

## 2. 顶层结构与字段契约

```
{ schema, run, period, ledger_of,
  anchors:       [ {id, type, status, source, quote,
                    events?: [{date, ref, type}],
                    direction?: improving|worsening|flat,
                    next_check?: {period, field, operator, threshold, run_when?}} ],
  pending:       [ {id, carry_from?, question, verdict, revised_at?, exempt_from_gate?} ],
  linkage_checks:[ {metric, prev_period_end, this_period_begin, both_ref:[上季ref,本季ref]} ],
  risk_scan:     { <项名>: {result, evidence, values?:[{value, basis}] , history?:[{period,result,asof,ref}]} } }
```

- `anchors[].type`=锚种（dividend/guidance/buyback/hedge_convergence/…）；`quote`=公司原句（可含基数/日期）；
  `source`=该锚首见季的 `<run>:S##`；
- `events[]`=**方案变更登记**（D4）：`type=amendment`（变更）在场时该锚 `status=fulfilled` 即机检违规——
  自动降 `partial` 并加核对动作（「变更内容未抽取，兑现判断悬置」不许被算作已兑现）；
- `next_check`（D10）：可机判的下一验点（period/field/operator/threshold），替代自由文本；结构校验现阶段未强制；
- `pending[].carry_from`：对上季行（如 `2025AR:P2`）或 `new`（D7）；`verdict` **人回填、机器零造词**——
  无人回填=原样结转「无人回填，跳过」；回填只追加 `revised_at` 不清空；
  `exempt_from_gate:true`=设计即空的行（评级/目标价两位，D11），不入回填率统计（分母剔除后报，如 `0/8`）；
- `risk_scan.result` 五枚举（D8 语义分家）：`HIT`（命中）/`MISS`（工具在场零命中）/
  `NO_TOOL`（域面能力外，即 G8 缺位账来源——可由该枚举直接过滤生成缺位账，无需人工甄别）/
  `EXTRACT_FAILED`（抽取失败）/`NO_RESPONSE`（查询未达）；
- `values[].basis`（D6）：每个增速/变动值带口径标签 `accum|qtr|yoy_vs_period|vs_beginning`——
  年度同比与半年对期初两种口径**永不共槽**（防「+13.0% 与 +53.2% 同框误读」）；
- `direction`（D3）：趋势锚专用（improving/worsening/flat）。

## 3. 锚状态六态定义（判定即此语义）

| status | 定义 | 判据 |
| --- | --- | --- |
| `fulfilled` | 上季承诺本期完整兑现 | next_check 断言过 或 披露事实与原句逐项对上 |
| `unfulfilled` | 本期事实与承诺相悖 | 同上反向；须带证据 ref |
| `partial` | 部分兑现/含未抽变更/amendment 在场 | 默认保守档；G3 型（回购推进+方案变更未抽）必落此档 |
| `carried_forward` | 结转未回填（素材未到手，非失败） | 如指引原句连续两季未获取——「无法判定≠未兑现」 |
| `superseded` | 被后续事实作废/改写 | 如「新增来源」问句被本期净减改写 |
| `unverifiable` | 当期口径无法验证 | 与 carried_forward 区分：前者=本季验不了，后者=欠账在追 |

## 4. 操作规程：先读账，后落笔

1. **`+recall` 先于一切**（SKILL §3.0）：在 run_dir 同级找最近一期 `ledger-<period>.json`。
   找到→台账首节记「续账自 <period>」；未找到→记「首季建账」并跳过本节——**禁凭记忆或外搜"猜上季"**
   （不可再现时的 fallback 即此逐字句，宁空勿猜）。
2. 注入四路（读账在前、落笔在后）：§1 对照锚行加「上季预期基准」；§4 六项逐项带 history 结转列，
   HIT/MISS 变化必须显式说明；§5 事件日历先列 anchors.events；§7 待人工表按 carry_from 对账，
   已回填 verdict 原样结转只追加 revised_at。
3. **progress.md 账本段**：`+recall` 起手记「续账自 X / 首季建账」一行；`+draft` 每注入一路记一行；
   成稿后写 `ledger-<本期>.json`（本节契约），并在台账记落账行。
4. **note 引用格式**：账本支撑的句子在 `[L*]` 之外可并带 `<run>:S##`；跨季对照句两侧 ref 都给
   （linkage 行 `both_ref` 同旨）。
5. `+check` 必带 `--ledger <本期> --prev-ledger <上季>` 跑 linkage 断言——
   **本期期初 ≠ 上季期末即不交付**（D5，账本相对人眼的核心增值所在）。

## 5. 实证样例（美的 2025AR→2026H1，回放非新查询）

| linkage metric | 上季末 | 本季初 | refs |
| --- | --- | --- | --- |
| goodwill | 34,256,859 | 34,256,859 | `2025AR:S4` ↔ `2026H1:S2` |
| accounts_receivable | 40,450,097 | 40,450,097 | 同上 |
| contract_liability | 46,993,060 | 46,993,060 | 同上 |

三断言 EQUAL，exit 0；坏样（改一分）即 FAIL 并打印两值+双 refs。同帧实况：G3 回购 `events[amendment]`
在场→两季均 `partial`（机器断言禁 fulfilled）；G4 套保收敛 `unfulfilled + worsening`；
回填率 `0/8`（豁免位 H1P9 评级/H1P10 目标价不入分母）；`NO_TOOL` 三项恰对应 G8 缺位清单。

## 6. 不做

- 跨标的合并账本（一标的各季各自成链，多标的编排属未来产品位，非本契约）；
- 评级/目标价任何前瞻语义（见头图边界声明）；机器对 pending 只结转不造词；
- 账本不含付费终端指标；池快照若入账，按 `expectation-pool.md` 的 `source_tier` 口径整行携带。
