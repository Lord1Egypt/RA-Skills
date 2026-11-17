# 改进提案：外部 MCP 化 + 引文追踪首类工作流（依据 Paper Search MCP 评测）

> **来源**：微信公众号「全息学术」2026-11-06 实测《试试这个文献检索 skill，没有找不到的论文！》—— 评测开源项目 `openags/paper-search-mcp`。
> **结论基线**：该 MCP 是薄封装层（多源检索 + 摘要整理 + OA 全文读取 + 引文关系追踪）。`ct-literature` v1.7.x **已覆盖其约 90% 功能面并在系统综述严谨度上显著领先**；其唯一真正差异化卖点是"以标准 MCP 协议对外暴露引擎，供任意 Agent 一键安装调用"。
> **本文目标**：把评测中可借鉴的点落成可迭代的设计提案（P0/P1），其余仅作验证确认（不改）。

---

## 0. 总体判断与优先级

| 项 | 优先级 | 是否新增能力 | 说明 |
|---|---|---|---|
| A. 引擎 MCP Server 对外暴露 | **P0** | 是（包装，非新算法） | 唯一真正差异化缺口；复用现有 HTTP 服务 |
| B. Snowball 升级为首类 NL 工作流 | **P0** | 否（已有 `--snowball`，需提级+种子驱动） | 当前默认关、关键词后附加步 |
| C. 「读→扩→链」引导剧本 | P1 | 否（拼装现有零件） | 对话状态机新增 guided sequence |
| D. 检索后按 PICO 重筛默认显式化 | P1 | 否（默认可见化） | 呼应"接缝护栏" |
| E. 多模型协作筛文献 | P2 | 研究前沿 | 暂不落地，仅路线储备 |
| 已领先项（多源广度/抗幻觉/PRISMA/零配置） | — | — | **验证通过，不改** |

---

## A. 提案 A：统一 ct-mcp-gateway 中的 ct-literature 命名空间 tool 设计（P0，受 §F 统一网关裁定约束）

> **与 §F 的关系（收敛声明）**：本提案**不**描述独立的 literature MCP server。literature 的 MCP 化在架构上 = 统一 `ct-mcp-gateway` 聚合 7 档 tool 方案中的 **`ct-literature` 命名空间**（首个优先实现命名空间）。§A.2 的两种传输方式是**网关的部署形态**，非 literature 专属 server。详见 §F.4。

### A.0 立项理由：为什么做 MCP（而非仅 WorkBuddy 内部复用）

**结论**：MCP 化对 ct-literature 本质是**传输层 / 路由层升级，不是引擎层能力增益**——好处集中在"标准化 + 跨生态复用 + 组合编排"，而非新增检索功能。是否值得做，判定标准只有一个：**是否真有 WorkBuddy 之外的 Agent 要调用它**；若唯一消费者仍是 WorkBuddy 自身，MCP 收益有限（技能已能在工作流内直接跑）。

#### 具体好处（按价值排序）

| 好处 | 含义 | 对 ct-literature 的意义 |
|---|---|---|
| 1. 打破 WorkBuddy 孤岛，跨 Agent 复用 | 任何支持 MCP 的客户端（Claude Desktop、Codex、Cursor、Cline 等）配一个 server 即可调用 | 把已有的**临床级**检索 / 去重 / 引文核验输出给全行业 Agent，而不只服务 WorkBuddy 内部——这是 Paper Search MCP 真正的差异化卖点 |
| 2. 能力即结构化工具，而非"再来一个聊天入口" | 函数变成带类型入参 / 出参的离散 tool，返回 JSON 而非散文 | 调用方拿到结构化 work 列表、验证状态，可直接进工作流；比 NL 往返稳定、可校验 |
| 3. 把既有"严谨度"变成公共基建 | 抗幻觉引用验证、DOI 审计、PRISMA、合法 OA 约束已就绪 | 外部工具不用再踩 Paper Search MCP 那种"无验证、混噪声"的坑——核心优势外溢 |
| 4. 编排 / 组合（orchestration） | MCP 客户端可把多个 tool 串成链路 | ct-registry（试验全景）→ ct-literature（已发表证据）→ ct-safety（FAERS）→ 综合 Agent 的链路可在任意主机**跨 Agent** 跑，不局限于 WorkBuddy 单技能内 |
| 5. 零新增检索逻辑，单一真相源 | 只做协议翻译，复用现有 `/api/*` 与 `adapters/` | 符合"同一语义禁止两套并行维护"纪律，不引入双轨 |
| 6. 一键安装与可发现性 | 标准 manifest 让用户在多客户端一键添加 | 对齐"给个 URL 即装"的体验 |
| 7. 鉴权 / 限流 / 合规继承 | 复用已发布服务的 token 与限流 | 不额外扩大安全面 |

#### 代价与边界（必须说清）

- **它是包装，不是能力**——若唯一消费者仍是 WorkBuddy 自身，MCP 收益有限。
- **维护面 +1**：多一个传输层要与后端同步；必须只做翻译、不复制检索逻辑（红线）。
- **真价值在"外部触达"**：衡量是否值得做的标准，是"是否真有 WorkBuddy 之外的 Agent 要调它"，而不是内部便利性。

#### 立项判定标准

> 投入 MCP 化的先决条件：**存在 WorkBuddy 生态之外的真实调用方需求**（如要在 Claude/Codex 工作流里复用 ct-literature 的临床级检索）。无此需求时，本提案 A 应降级为"待触发"，仅保留接口草案，不投工程资源。

### A.1 目标与复用资产
- **目标**：让非 WorkBuddy 生态的 Agent（Claude、Codex、Cursor 等支持 MCP 的客户端）经统一网关以标准协议调用 `ct-literature` 命名空间的临床级检索/去重/引文核验能力（网关另含 samplesize / registry / safety / search / pipeline / advisor 命名空间，见 §F）。
- **复用（不重建）**：
  - 已发布的 Python HTTP 服务 `https://ct-literature.app.workbuddy.host/`（appId `wbapp_WuOPnJ4caJ32GTquNlR7vc`，见 `references/published_app.md`）——作为**网关后端之一**；网关复用其 `/api/search`、`/api/tools`、`/api/lit-stream`、`/api/sources`、`/api/parse`。
  - 既有 MCP 规划文件 `references/zotero_mcp_adaptation_plan.docx`（Zotero 本地库 MCP 适配）——其传输与鉴权思路现应重定位为**网关内的 literature 命名空间适配**，而非独立 server。
  - 检索/去重/引文/PDF 核心逻辑全部在 `scripts/ct_literature.py` + `adapters/`，MCP 层只做**协议翻译 + 参数映射**，不触碰 Coze 检索层。

### A.2 网关传输形态（两种，按部署场景选）
> 以下两种均为**统一网关 `ct-mcp-gateway` 的部署形态**：网关是单一 server，内部聚合 7 档 A 档 tool（含本提案的 `ct-literature` 命名空间），**不是 literature 独占的 server**。
1. **stdio 本地桥**（推荐默认）：网关进程在本地拉起，内部以 HTTP 客户端调用各 A 档既有服务（`ct-literature.app.workbuddy.host` 等）。适配"用户本地 Agent 装个 URL 即可用"的体验。
2. **远程 HTTP MCP**（可选）：把网关包一层 MCP 端点（`/mcp`），复用各 A 档既有服务的鉴权与限流。

### A.3 工具清单（初版 4 个，参数映射现有 CLI/API）

| MCP tool | 对应现有能力 | 关键入参（映射） | 出参 |
|---|---|---|---|
| `literature_search` | `ct_literature.py --topic …` + 多源合并 | `topic`, `review_type`, `year_from`, `year_to`, `sources`（默认 `OpenAlex,EuropePMC,bioRxiv,medRxiv`），`depth`（quick/standard/deep），`concept`（PICO 数组），`safety`（bool），`verify`（all/top/none） | 归一化 work 列表（JSON）+ `evidence_log` 摘要 |
| `download_pdf` | `--download-pdf` + `pdf_download.py` | `dois` / `pmids` / `top_n`，`legal_only=true`（强制合法 OA） | 本地路径 + OA 来源；绝不逐个回传文件，只回"共同保存目录" |
| `snowball` | `--snowball` + `fetch_openalex.fetch_snowball` | `seed`（DOI/PMID/OpenAlex ID/题名），`direction`（references/cited_by/both），`seeds`（top-N），`max_per_seed` | 1-hop 扩展文献（已去重）+ 方向标注 |
| `verify_citations` | `verify_citations.py` + `--verify`/`--verify-dois` | `works`（merged.json 或 DOI 列表），`mode`（all/top） | 验证状态：`verified`/`mismatch`/`unresolved`/`bot_blocked` + DOI 审计表 |

> **约束**：所有工具沿用现有护栏——合法 OA 限定、无 key 自动降级（OpenAlex keyless 100/天）、PDF 下载后只给目录不逐个打开、不静默返回 0 条。`references/published_app.md` 的发布链（build→install marker→deploy，`publish.sh`）保持不变，MCP 包装作为**附加传输层**，不改动既有 Web 交付。

### A.4 安装体验对齐
- 提供 `mcp.json` / `README` 片段，使支持安装 Skill/MCP 的 Agent 可"给个 URL 即装"，对齐 Paper Search MCP 的卖点。
- 在 `SKILL.md` `triggers` / 顶部摘要补一句"亦可经 MCP 供外部 Agent 调用"，并在 `references/` 维护一份 `mcp_server.md`（安装、传输、工具表、鉴权）。

### A.5 风险与护栏
- **不重建检索算法**：MCP 层纯协议翻译，避免与 Coze 检索层双轨维护（呼应你的"同一语义禁止两套并行"红线）。
- **鉴权**：远程 HTTP MCP 复用现有服务的 token/限流；stdio 桥默认仅本机回环。
- **合规**：数据源均为公开文献 API（A-tier），无涉密输入，与既有 network 策略一致。

---

## B. 提案 B：Snowball 升级为首类 NL 工作流（P0）

### B.1 现状
- 现有：`scripts/ct_literature.py` 有 `--snowball` / `--snowball-seeds`(默认 3) / `--snowball-max`(默认 10，上限 50)；`adapters/fetch_openalex.py::fetch_snowball(seed_work_id, direction="both", max_refs=20, …)` 支持 `references`(后向)/`cited_by`(前向)/`both`。
- 痛点：默认**关闭**；仅作为关键词检索后的附加步；无"以某篇种子论文为起点"的独立入口；用户不知有此能力。
- **小清理项**：adapter 默认 `max_refs=20` 与 CLI 默认 `--snowball-max=10` 不一致，统一为 10（或显式文档化差异）。

### B.2 改动
1. **新增触发词**（写入 `SKILL.md` triggers 与 `references/search_menu.md` 状态机）：
   - "追溯这篇论文的引用/被引"、"X 的前后向文献"、"以 X 为种子扩展文献网络"、"citation expand / snowball from <DOI/PMID/题名>"。
2. **种子输入多样化**：支持 DOI / PMID / OpenAlex ID / 题名模糊匹配 → 解析为 OpenAlex work ID 后调 `fetch_snowball`。非 OpenAlex 源种子（Europe PMC/S2）走现有降级（仅当有可用 ID）。
3. **方向显式化**：NL 中"被引"→`cited_by`，"参考文献"→`references`，"都看"→`both`（默认 both）。
4. **状态机分支**（`search_menu.md` §1 状态机）：在 `Complex` 分支下加 `Citation-Expand` 子意图，复用现有参数收集清单的精简版（仅需 seed + direction + depth + seeds/max）。
5. **可选可视化**（复用 PRISMA 的 inline-SVG 能力）：种子居中，前向/后向分两环，节点标注 `cited_by_count` 与 `relevance_score`，生成轻量引文关系图嵌入 `lit_report.html`。

---

## C. 提案 C：「读→扩→链」引导剧本（P1）

- 在 `references/dialogue.md` / `search_menu.md` 增加 **guided sequence 节点**，把现有零件串成文章演示的分段节奏：
  1. **读**：先 `--download-pdf` + `--anchor` 拉开放全文、落段落级溯源；
  2. **扩**：`--depth standard/deep` 扩摘要，必要时 `--snowball` 补网络；
  3. **链**：以高相关种子走 B 的 Citation-Expand。
- 不强制全跑；在预览确认菜单加一个"引导式检索剧本（读→扩→链）"开关（默认关，避免打扰简单查询）。

---

## D. 提案 D：检索后按 PICO 重筛默认显式化（P1）

- 文章诚实指出关键词检索必混噪声（医学考试、泛 AI 使用等），建议必做一道 AI 重筛。
- ct-literature 已有 `--rank relevance` + PRISMA 漏斗 + P0 引用验证，但重筛未作为**默认可见**环节。
- **改动**：在 `lit_report.html` 与 `lit_report.xlsx` 的结果区，默认展示"基于研究问题的相关性裁决"列（`relevance_score` + 简短裁决理由），PRISMA 漏斗在无 `--prisma` 时也给一个轻量 included/excluded 概览；绝不静默丢文献，异常一律放行并在 ledger 标注。
- 呼应你的"接缝护栏"原则：未核验的相关性裁决不得作为最终纳入/排除，只作排序与提示。

---

## E. 提案 E：多模型协作筛文献（P2，路线储备）

- 文章末提及相关论文（多模型一致性、投票/辩论/裁决）。属筛选自动化研究前沿。
- 当前 ct-literature 单遍。建议仅记入路线图，**暂不投入**；若后续做，须先定"多模型一致性 ≠ 最终裁决"的护栏，避免引入新幻觉面。

---

## F. 架构裁定：A 档技能"全量各自 MCP 化"列为反模式（不采纳）

### F.0 背景与 A 档枚举确认
- 用户确认 **"A 档技能"** = `ct-advisor` / `ct-samplesize` / `ct-literature` / `ct-search` / `ct-registry` / `ct-safety` / `ct-pipeline` 共 7 个用户-facing 顶层 + 已发布核心技能。
- 讨论起点：为缓解"ct 系列技能相互调用问题"，是否应将这 7 个 A 档技能**各自 MCP 化**。

### F.1 裁定
**不采纳"7 个 A 档各自 MCP 化"（方案 X）。** 对 ct 系列的**内部相互调用**，全量 MCP 化增益有限且违反既有架构铁律；正确路线是 **"统一 `ct-mcp-gateway` 聚合 + 内部维持 Skill 委托"（方案 Y）**。

### F.2 依据（均来自 ct-base 规范，非主观判断）
| 依据 | 出处 | 对方案 X 的约束 |
|---|---|---|
| 家族只有两种合法架构，禁第三种跨技能调用形态 | `ct-base` §23.1.2 铁律 1 | 给每个技能加本地 MCP server = 第三种形态，违规 |
| 跨技能编排已是代码全自动 + 结构化委托协议 | §23.4.3 `CT_TOOL_DELEGATE` + `refine_answer.py --card-inline` | 内部"结构化 tool 调用"已被覆盖，MCP 增益低 |
| 本地薄客户端、云端唯一真相源，本地不保留第二引擎 | §23.1.3 / §23.2 R1 | 本地起 N 个 MCP server 扩大本地调用面与攻击面 |
| 契约治理已有统一底座 | §9C ct-qa 1702 PASS / 0 FAIL 覆盖 19 技能 | 内部漂移治契约，不治协议形态 |
| MCP 立项判定 = 外部调用方需求 | 本提案 §A.0 | 内部相互调用不满足此标准 |

### F.3 方案 X vs 方案 Y 权衡
| 维度 | X：7 个 A 档各自 MCP 化 | Y：统一网关 + 内部 Skill 委托 |
|---|---|---|
| 内部相互调用增益 | 低（委托协议已覆盖） | 不变（内部走既有机制） |
| 外部跨生态编排增益 | 有，但 N 个 server 各自维护 | 有，且单 server 聚合 7 档 tool |
| 架构合规 | **违反 §23 铁律** | 不碰内部架构，MCP 仅作对外传输层 |
| 维护面 | N 个传输层 + 同步 | 1 个网关 + 复用现有 coze 信封/HTTP |
| 红线风险 | 触碰 R1（本地第二调用面） | 仅翻译、不复制逻辑（符合 §A.0） |
| 单一真相源 | 易双轨 | 内部单轨，网关只翻译 |

### F.4 与 §A 的关系（收敛而非矛盾）
- §A 的 ct-literature MCP 化是**单技能对外暴露选项**，受 §A.0 立项标准约束（需外部调用方需求触发）。
- 若启动对外暴露，**优先实现统一网关**而非 7 个独立 server：§A 的 4 个 tool 重定位为网关内 `ct-literature` 命名空间的 tool 子集（`literature_search` / `download_pdf` / `snowball` / `verify_citations`），其余 6 档各贡献其 tool 组（如 `samplesize_compute` / `registry_query` / `safety_faers` / `pipeline_*` / `search_*` / `advisor_ask`）。
- 内部相互调用（advisor 编排 samplesize/literature 等）**继续走 `CT_TOOL_DELEGATE` 委托协议**，不被 MCP 化干扰。

### F.5 触发条件（何时才动 MCP）
- 仅当存在 **WorkBuddy 生态之外的真实编排需求**（外部 Agent 要串起多个 ct 技能）时，才启动"统一 `ct-mcp-gateway`"；否则 §A 保持草案态，不投工程资源。

### F.6 反模式标注
> **反模式（不采纳）**：为内部相互调用而给 `advisor` / `samplesize` / `literature` / `search` / `registry` / `safety` / `pipeline` 各自建独立 MCP server。正确做法 = **单一 `ct-mcp-gateway` 聚合 A 档 tool + 内部维持 Skill 委托协议**。

---

## 验收与下一步

1. **A（MCP）**：先出 `references/mcp_server.md` + 一个 stdio 桥原型（调用现有 `/api/search`），跑通 `literature_search` + `snowball` 两个 tool，再补 `download_pdf` / `verify_citations`。
2. **B（snowball 首类）**：在 `SKILL.md` triggers + `search_menu.md` 状态机加 `Citation-Expand`；实跑"以一篇已知 DOI 为种子"的端到端，验证 `references`/`cited_by` 两向均返回且去重正确。
3. **C/D**：在 `dialogue.md` 增加 guided sequence 与默认重筛展示；ctqa 回归覆盖新增 NL 触发。
4. **护栏回归**：所有新增不得破坏既有——无 key 降级、合法 OA、PDF 只给目录、不静默 0 条、四态 ledger 不归零。

> **🔴 发布纪律**：本提案任何落地改动**不自动推送**（git push / SkillHub / ClawHub 均等显式指令）；MCP 包装作为附加传输层，不得改动 `workbench/publish-kit/` 既有发布链，且必须 `assert shareLink == ct-literature.app.workbuddy.host`。
