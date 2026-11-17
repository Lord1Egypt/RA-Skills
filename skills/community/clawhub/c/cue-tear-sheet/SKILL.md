---
name: cue-tear-sheet
displayName: 公司一页纸
slug: cue-tear-sheet
version: "0.1.22"
summary: "公司一页纸：五段形制机检钉死顺序——近四期双口径、事件≤4、风险1-3 只写直查命中，观点区三行 [待人工] 留白。"
description: "给你一家公司（名或代码），产出一页速览五段：身份三行（主营句取披露原文、禁自造简介）；近四期速览（营收/归母/扣非/经营现金流，累计+单季双口径带标签）；在场事件 ≤4 条（先过入类第一闸：明确披露日期或 statute 锚内条件可判）；风险 1–3 条仅收直查命中，无命中必写固定句「直查面内未命中≠无敞口」；观点区 [待人工] 空三行、一字不代填。默认零深研：有深研诉求即标注「深研未发起」转姊妹件，不中途发起。适合：初次接触一家公司、会前速备。不适合：深度尽调（转 dd-checklist）、投资意见。 Do NOT use for: investment advice."
tags: [投研, 一页纸, A股, 回客件]
license: MIT
consumes: []                     # 显式空：主体集由用户直供（第 45 行「主体集：官方中文全称或代码，≤5 个」），身份与四期走工具面直查（第 51 行 entity_data／disclosure_cn），面文无「读仓内某件产出」之说；第 39–40 行与第 62 行、第 94 行的 catalyst-calendar／cn-earnings-note 是向外指路而非读入，不构成入边（不是漏写）
inputs:
  - company-list
produces:
  - run-log
  - source-index
  - tear-sheet-page
agent_created: true
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    envVars:
      - name: CUE_API_KEY
        required: false
        desc: "可选凭据：本包的页面生成本身不直接读这枚变量（现读：包内代码级引用 0 枚件）；它属于伴生渠道的凭据，缺位时按 README 所述走用户直供。"
  optionalSkills: ["cue-data-mcp", "cue-omni-reader"]
---

# tear-sheet — 公司一页纸（AI 初稿）

> 交付的是**每行可锚的一页纸**，不是观点成品；也是套件的回客入口——它替你把「30 秒能确定的事实」先摆上桌。
> 铁律语法继承姊妹件；本件最大风险=**为凑一页而补数据**，全部形制约束围绕「宁缺毋滥」。

## 0. 什么时候用 / 不用

| 你要 | 用什么 |
|---|---|
| 见客户前 30 秒生成的一页速览（屏内读完，每行带锚） | **本 skill** |
| 未来三个月的日期表 | `catalyst-calendar` |
| 深度点评/连续剧对账 | `cn-earnings-note` |
| Excel 交付物、批量 >5 主体、评级/目标价 | 不做（frontmatter「不用于」句） |

## 1. 输入契约（≤3 问）

- **主体集**：官方中文全称或代码，**≤5 个**——超了拒绝并说明成本理由（回客件的定位=快与省，批量走姊妹件）；
- **用途**：`会前速览 | 客户简报` 二选一（只影响详略与排版密度，不改任何纪律）；
- **关注点**（可选，一句话）：如「现金流最近怎么样」→ 该主题在页内升加粗行，**不引入新数据源、不加新段**。

## 2. 一页纸固定形制（五段，顺序钉死=机检④）

1. **身份三行**：全称 / 代码 / 主营一句话（`entity_data`+`disclosure_cn`；**禁简介自造**——主营句取披露原文表述）；
2. **近四期速览表**：营收/归母/扣非/经营现金流 × 四期（**累计+单季双口径**，每值带 basis 标签，标签枚举=本包 `check_page.py` 里 `BASIS_ENUM` 现值；取数域与工具面一律运行时发现、以 catalog 现值为准，本文不抄域清单与工具名）；
3. **在场事件 ≤4 条**：只收已过入类第一闸的条目——①已有披露在场且含明确 `YYYY-MM-DD`，或②statute 规则推导且适用条件在锚内可判；任何日期算术、事后追记冒充前瞻、无事前日期的进度节点（回购 1%/2% 一类）都不入页（判定=本包 `check_page.py` 里 `FULL_DATE_RE` 与 `ESTIMATE_RE` 现值，一条命令见 §4 末）；本件页上不设类型枚举列，机检不判类型；
4. **风险 1–3 条**：仅 `fr_footnote`/`regulatory_cn` 直查命中项；无命中**必须**写固定句「直查面内未命中≠无敞口」；
5. **观点区**：`[待人工]` **×3 行**空位（行含义由使用者自定，本件不命名、一句不代填）。

**页眉三声明（缺任一 FAIL）**：生成 asof / 数据截止日 / 本次通道用量声明（如「research 0 次·omni 1 次·data-mcp 9 次」）。

## 3. 通道与成本纪律

- `data-mcp` 直查为主（工具与入参 schema 一律当场发现，域清单与工具面以 catalog 现值为准，本文不抄）；
- **默认 0 次 cue-research**——一页纸的成立不以深研为前提；需要深研的诉求出现时，降级标注「深研未发起」并指路姊妹件，**不中途烧**；
- `omni` 仅当需要摘要级原文且域面 section 全文不足时（三级路径同姊妹件）；配置指路：数据腿官方配置页 <https://cuecue.cn/hub/mcp>（本件的取证以 `data-mcp` 直查为主、默认 0 次 cue-research，见上面两条）、解析腿官方配置页 <https://cuecue.cn/hub/omni-reader>（按需的一腿——用得上的场合就是本句那一条：需要摘要级原文而域面 section 全文不足时）。
- **页眉通道用量声明与 `evidence/` 快照数逐笔对账（缺快照=缺声明，写进台账注因）；全流程 confirm-before-spend 弹窗至多一次**：所有可能计费的调用合并预演、一次问齐——成本可预期=回客件的前提。

## 4. 管线（三段+门禁）

`+scope`（消歧+用途定档）→ `+facts`（五段取数：身份/四期/事件闸内 ≤4/风险直查；**每笔域直查原始返回落 `evidence/`+台账 sha 行，零计费**）→ `+render`（按 §2 形制落 `page.md`，逐节追加同姊妹件纪律）。

收尾门禁（不过不出）：
```bash
python3 scripts/check_page.py <page.md> --sources <sources.jsonl> --subjects <n>
```
四道：①声明行（AI 初稿+asof+通道用量，缺任一 FAIL）②数字行列级锚+正文↔sources 双向（锚型白名单=本包 `check_page.py` 里 `ANCHOR_OK_RE` 现值）③禁词=`BANNED_RE` 现值**零容忍**（常见例：利好、目标价、建议——**例不穷尽**，全量随现值走，一条命令见本段末）——本页无评级概念④形制闸=五段顺序+每主体 ≤40 行+事件条目全过第一闸（日期形状=`FULL_DATE_RE` 现值、推测词族=`ESTIMATE_RE` 现值；类型不入判据）；主体数 >5 即 FAIL。
（词面域一条命令自查，任意目录整行粘贴即跑、命令自带安装后路径；装在别处把 `~/.workbuddy/skills/` 换成你的技能安装目录，Windows 路径形如 `C:\Users\<用户名>\.workbuddy\skills\tear-sheet\scripts\check_page.py`，两条命令都走 POSIX 工具，Windows 请在 Git Bash/WSL 内跑）：`grep -n -A3 "BANNED_RE = \|ESTIMATE_RE = \|ANCHOR_OK_RE = \|PERIOD_RE = \|BASIS_ENUM = " ~/.workbuddy/skills/tear-sheet/scripts/check_page.py`；守护样清单同形现跑：`bash ~/.workbuddy/skills/tear-sheet/scripts/run_fixtures.sh`——本文不抄域清单也不抄条数，跑什么是什么。**绿灯不证防线**：机检全过只证形状合规，不证数据取得。）

## 5. 输出契约

**开口请带上时点，输出标数据日期**：请求里给出报告期／基准日或回看窗口；成品首行标注**数据日期**，当它与用户所指日期不一致时，正文禁用「今日」「最新」，一律改写为「截至 <日期>」。

**未见于本次返回的一律写「未检索到」**：参数名、字段名、枚举值没有出现在本次工具返回里的，不得凭印象填写；写「未检索到」并记入待核清单或覆盖率账，不得留空顶替。
```
tearsheet-<日期>-<n>主体/
├── page.md          交付物：页眉三声明+每主体五段（≤40 行/主体）
├── sources.jsonl    行式同姊妹件契约（id/kind/ref/claim/confidence/asof）
├── evidence/        域直查原始快照（一笔查询一个文件 `evidence/<kind>-<query摘要≤40字>-<YYYYMMDDTHHMMSS>.json`，原样落盘禁转写摘要冒充，append-only 不覆盖；页眉通道用量与之对账）
└── progress.md      台账：取数面+弃行记录+通道用量实况
```

## 6. 边界与拒答

- 「帮我写成能直接发客户的推荐」→ 拒绝：观点区 `[待人工]` 是三行空位，代填=越界；
- 「加上 Excel/做个表格文件」→ 拒绝并指路（本件只产 md 回客页）；
- 主体 >5 → 拒绝并说明成本理由；批量日期场景引导 `catalyst-calendar`；
- 数据取不到 → 该行**删**并记台账弃行，**不以估计值凑页**——空行合法，编行违法。

## 7. 出处

- 基座：anthropics/financial-services `tear-sheet`（Apache-2.0）——一页纸的任务形态来源。
- 本包为**A股化重实现而非搬运**：数据层完全 Cue 通道化，形制（五段/双口径/第一闸/成本纪律）按本套件契约重建，无其代码。出处声明见仓库根 `NOTICE.md`。
