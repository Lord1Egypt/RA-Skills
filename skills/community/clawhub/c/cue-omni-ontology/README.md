# cue-omni-ontology

**把公开资料变成可更新、可查证的业务知识。**

给 Agent 两份报告或公告，拿到三个结果：**有依据的回答、能展开原文的变化简报、下次可继续更新的知识包。** 适合财报跟踪、公开供应商尽调和产品/竞品公告监测。

**本文件为中文主面；英文版为包内 `README.en.md`（仓库内查阅，渠道页不解析相对链接）。**

## 先看实际价值

[微软两期公开披露实测](assets/public-example/live-preview.md)：新解析 → 抽取 → 建立/更新 → 带证据回答，已完整跑通。

| 你遇到的问题 | 这个 skill 交付什么 |
|---|---|
| 同一个指标为什么有两个数字？ | 保留期间、单位、口径及限定条件，列出各自依据。 |
| 新报告发布后，需要从头整理吗？ | 在旧知识包上更新，保留历史，标出新增支持与冲突。 |
| 这个结论从哪来，能核对吗？ | 搜索简报、展开原文摘录，回到真实来源和位置。 |
| 我想接入后续 Agent 工作流 | 复用结构化知识包；可导出 draft OKF 核心子集。 |
| 业绩会的视频/录音能不能进来？ | 能，但走的是**音视频素材（本地小段/切片≤256 MiB）**工作流：两场合共三枚 90 秒切片走通全链（build→update×2→validate→query→export-okf）、逐字回查 8/8；全长会议解析**未臻**——公开全长 URL 路五枪全拒、本地全长受 256 MiB 闸。口径见 `references/av-backtest.md`。 |

用户不需要先设计完整企业本体。默认从一个主体、2–5 份公开来源和一个明确问题开始。

## 第一次试用：无需 API key

安装后直接对 Agent 说：

> 使用 cue-omni-ontology，先用自带样例演示：加入新材料后，哪些事实新增、哪些冲突、依据在哪里？

也可以在技能目录运行一条命令（Python 3.10+）：

```sh
python3 scripts/ontology.py demo --out /path/to/work/cue-demo
```

把示例路径换成自己的**全新工作目录**，然后打开 `cue-demo/brief/brief.html`。不需要启动服务；浏览器可搜索、筛选新增/冲突、展开原文。不能打开 HTML 的客户端可以读取同目录 `brief.md` / `brief.json`。

演示明确使用虚构材料，不联网、不调用解析 API：上季收入 100 后被披露为 105，两个说法并存为冲突；本季 120 与调整后 115 分开；新版未提及的 Alpha 产品保留历史，不推断下线。

## 安装与真实资料

```sh
npx skills add huhoo/cue-awesome --skill cue-omni-ontology
```

该安装方式需要 Node.js/npm；直接复制本目录到宿主支持的 skills 位置也可。离线工具只依赖 Python。真实解析复用官方 [cue-omni-reader](https://github.com/sensedeal/cue-skills/tree/main/cue-omni-reader)，按其 [setup](https://github.com/sensedeal/cue-skills/blob/main/cue-omni-reader/references/setup.md) 连接 MCP 并配置凭据。此包不自动安装或配置 Omni。key 放入自己的凭据设施，不发到聊天或 Issues。 这一腿的官方配置页只给指针、不复述步骤：<https://cuecue.cn/hub/omni-reader>；不连它会少什么，本面下面那一段已按原话写着（页锚与逐字定位缺位、来源记录只能到文件级），这里不复写一遍。本件面文没把结构化披露或横向深研列为取证腿，所以只给解析腿那一页，不塞没写过的腿。

通道那一腿的已连判据（本件的解析腿是宿主里的 omni-reader MCP，没有 curl 可以替代它）**按路分写**：宿主列工具走的是 MCP 的 `tools/list` 握手，**连上之后**那份返回里应当能看到这些名字——remote-only 那一面是 `parse`、`get_parse_status`、`cancel_parse` 三枚，带 Bridge 的那一面再加 `read_result`、`read_outline`、`discard_result`、`save_result`，共七枚；两路枚数不同，拿一个固定数去判两路必错一边。只装了 skill、列不到名字，就是没连（装 skill 与配凭据、连通道是三件事，别合成一件），本件随即只走「你把文本贴进来」那条路（代价：页锚与逐字定位缺位，来源记录只能到文件级）。名字在场只证它们被暴露，不证解析跑得通——URL 那一腿要拿一枚真实 URL 跑一次 parse 才证该路，本地文件那一腿要拿一枚真实本地文件跑一次 parse 才证该路（remote-only 不读本地件）；本件不自证也不代跑。解析消耗以服务端返回为准，本件不代估也不代付。

配置好后，给 Agent 真实来源与问题：

```text
使用 cue-omni-ontology，根据这两份公开报告回答：
1. 新一期新增了什么披露？
2. 哪些数字需要区分口径，不能直接比较？
3. 哪些问题缺少依据？
给我能展开原文的简报，并保存下次可更新的知识包。
```

第二次使用：

```text
把这份新公告加入已有知识包，给我变化简报。
保留旧记录，突出需要复核的冲突，不把“未提及”当成删除。
```

更多业务入口见 [task-recipes.md](references/task-recipes.md)。官方解析器负责读取资料，宿主模型负责语义抽取，离线工具负责证据定位、版本、查询和简报。协议兼容不代表每个客户端均已完成验收。

## 让 Agent 少做机械工作

Agent 可以逐字复制原文作为证据，不再手工计算哈希与 UTF-8 偏移。见 [quote-draft.json](assets/demo/quote-draft.json) 和[摘录输入说明](references/quote-input.md)：

```sh
python3 scripts/ontology.py prepare assets/demo/quote-draft.json --out /path/to/work/prepared
python3 scripts/ontology.py build /path/to/work/prepared/input.json --out /path/to/work/v1
python3 scripts/ontology.py update assets/demo/r2.json --base /path/to/work/v1 --out /path/to/work/v2
python3 scripts/ontology.py brief /path/to/work/v2 --base /path/to/work/v1 --out /path/to/work/brief
python3 scripts/ontology.py catalog /path/to/work/v2 --kind changes
python3 scripts/ontology.py query /path/to/work/v2 --concept metric:revenue --period 2026Q1 --with-evidence
```

重复摘录会要求增加上下文或明确出现次数。精确匹配失败时，`prepare` 会忽略表格竖线、空白和 Markdown 标记再定位一次，但证据仍指向原文逐字片段；仍有歧义就失败，不做语义模糊匹配。先用 `catalog` 看包里有哪些实体、概念和冲突（每个冲突带新旧两侧的原文摘录），`query` 遇到未知字段直接报错，不静默忽略。查询返回 `needs_scope` 时，可用口径、单位、有效期或返回的事实 ID 进一步选择。`--with-evidence` 附原文预览，截断时明确标注。匹配成功不证明语义正确，仍需核对表头、脚注及限定条件。

**真实 Omni 结果直接转来源**：把解析调用返回的 structuredContent 或完整 JSON 存成文件，然后：

```sh
python3 scripts/ontology.py omni-source /path/to/work/omni/r1.json --out /path/to/work --id source:r1 --url "https://..." --title "..." --accessed-at 2026-10-07
```

它逐字写出解析文本（核对 Omni 的 sha256）和带页码的来源记录，贴进 draft.json 后即可 `prepare`。只认源 PDF 页锚，不猜页；不发起解析、不读 key、不花额度。用 `save_result` 落盘或只存 Markdown 会丢页码，工具默认拒收。

**可选数字包**：宿主用确定性代码算出年报跨期变动、重述和勾稽检查，模型只抽叙述事项；`numeric-import` 只核对每个数字两年都有单位、页码和表格编号，摘录与来源页逐字一致，`numeric` 按审阅顺序（驱动因素 → 后果 → 已解释的正常事项）展示。它不打分、不预警。信用风险年报任务按[固定章节集](references/credit-risk-sections.md)抽取。

## 交付与验证

- **阅读入口**：离线 `brief.html`、Markdown 对应版，展示来源事实、范围、变化和证据摘录。
- **可复用知识**：`knowledge.json`、`sources.jsonl`、`changes.json`、`run.json`、精确证据快照。
- **抽取说明**：Agent 另写 `extraction-notes.md`，说明问题范围、失败来源及语义复核。
- **可选交换**：`export-okf` 输出 draft 概念文件，目标为 OKF 0.2 核心子集；外部消费者兼容性另行验证。

[验证记录](references/verification.md) 区分真实新解析、旧结果回放、独立合成任务和未验证范围。[微软实测](references/live-verification.md) 涉及两个来源、21 条来源断言，全部 11 条旧断言在更新后保留。它证明这一任务流程可完成，不代表通用准确率或已证实的客户 ROI。[留出集回测](references/verification.md)（40 份年报、7,598 页）中，证据有效率明显高于两种基线，但根因排序没有达到预设通过线，预警说法被证伪；三组数字与局限在验证记录中并列写明。

本地自检：

```sh
python3 -B scripts/test_ontology.py
python3 -B scripts/test_numeric.py
```

## 常见问题与反模式（你想这么用 → 本件不接，因为 → 替代去向）

判据以 `SKILL.md` 与 `references/knowledge-contract.md`、`references/update-policy.md` 现文为准，本文只归纳不作穷尽复述。

| 你想 | 本件接不接，为什么不接 | 替代去向 |
|---|---|---|
| 新材料没提到某事实，就当成已被删除 | **不接**。更新策略明写：不把「未提及」当成删除——沉默不是否定 | 只有披露里写出撤回/替代才记变化；未提及就保留旧对象并标注依据状态 |
| 同一个 ID 换一套含义接着用 | **不接**。更新器拒绝同 ID 偷换含义；定义与来源 ID 冲突时保留旧对象、提出新 ID 并解释 | 新语义开新 ID，旧记录留档，冲突并列保留 |
| 让脚本顺手把新旧值合并成一条结论 | **不接**。知识包只存**直接披露的断言**；计算与判断放在回答里说明输入与依据 | 冲突（如 100 与 105 并存）就在简报里并存，不静默覆盖 |
| 把 `ontology.py` 说成自动抽取器 | **不可以**。本件分工固定：官方解析器读资料，**宿主模型做语义抽取**，离线工具做结构与一致性校验 | 抽取说明另写 `extraction-notes.md`，讲清范围、失败来源与人工复核 |
| URL 长得像公开地址就算可访问 | **不接**。URL 形状不能证明公开可访问；检索补来源只在授权研究范围内，不另建爬虫 | 由用户明确提供文件/链接，或走 Cue 通道取回并留快照 |
| `export-okf` 输出直接接进外部系统 | **别当已验**。导出为 draft，目标 OKF 0.2 核心子集，外部消费者兼容性另行验证 | 先在对方侧验一次；本件只承诺生成的概念文件形状 |
| 逐句核对一段话或一个数字在公告原文第几页，或要一份带页码的线索稿 | **不是本件主业**。本件做可更新的知识包、变化简报和数字包 | 同仓库 [cue-lead-pieces](../cue-lead-pieces/README.md)：引文核对与线索稿 |
| 拿数字包或变化简报做违约预警、自动发现风险 | **不接**。留出集回测证伪了预警说法，根因排序也没过通过线；排序只是审阅顺序 | 由人基于逐字证据判断，见 [验证记录](references/verification.md) |

## 出错了怎么办（症状 → 原因 → 恢复动作）

**未见于本次返回的一律写「未检索到」**：参数名、字段名、枚举值没有出现在本次工具返回里的，不得凭印象填写；写「未检索到」并记入待核清单或覆盖率账，不得留空顶替。
按 `scripts/ontology.py` **当前实际出口**写（现跑所得）：校验类命令打印**一行 JSON**——
成功形如 `{"status": "valid", "counts": {...}, "semantic_verification": "not_established_by_scripts"}`（退 0）；
失败形如 `{"status": "invalid", "error": "<原因>"}`（退 2，走 stderr）；参数缺失走 argparse 的 usage 并退 2。

| 症状 | 原因 | 恢复动作 |
|---|---|---|
| `{"status": "invalid", "error": "knowledge integrity mismatch"}` | 知识包内容与其完整性记录不符（改过 `knowledge.json`、或新旧对象被手工替换成同 ID） | 不要手改包内文件：从来源重跑 `build` / `update`；确需修订就开新 ID 并保留旧记录 |
| `{"status": "invalid", "error": "source hash mismatch: <来源 ID>"}` | 来源快照与记录里的哈希不一致（原文变了或被替换） | 重新解析该来源生成新快照与新 run；旧快照留档，不改写历史 |
| `{"status": "invalid", "error": "[Errno 2] No such file or directory: '<路径>'"}` | 传给 `validate` 的不是一个完整知识包目录（缺 `knowledge.json` / `run.json` / `changes.json` 之一） | 指向 `build` 输出的包目录；`demo` 的产出在 `<out>/v1`、`<out>/v2` 这类版本子目录里 |
| 报错文案形如 `<标签>: invalid ID` / `<标签>: duplicate ID <键>` / `duplicate JSON key: <键>` / `invalid value for <类型>` | 结构与取值不合契约（ID 正则、重复键、值类型） | 按 `references/knowledge-contract.md` 的字段口径改；改完复跑同一条 validate |
| `usage: ontology.py [-h] {build,update,validate,query,catalog,export-okf,feedback,review,numeric-import,numeric,omni-source,prepare,brief,demo} ...` + `error: the following arguments are required: command` | 没给子命令或必传参数 | 先 `python3 scripts/ontology.py <子命令> --help` 看必传项（如 `demo` 必须 `--out`，且**输出目录必须是新目录**） |
| `omni-source` 报 `not JSON. Plain Markdown (or text written by save_result) has no grounding sidecar` | 存的是 Markdown 或 `save_result` 写出的文本，页码已丢 | 改存解析调用的 structuredContent 或完整 JSON；确实只有文本就加 `--text-only`（无页码） |
| `omni-source` 报 `the result has no source-PDF page anchors` | 结果是 detail=text、只有渲染页锚或非 PDF 来源 | 加 `--text-only` 按文本范围打包；grounded 重新解析会计费，先问用户 |
| `omni-source` 报 `Omni status is failed SOURCE_ACCESS_DENIED` / `DETAIL_CAPABILITIES_UNAVAILABLE` | Omni 取不到该网址（实测 SEC EDGAR），或该 Bridge 不支持本地文件 grounded 解析（实测 1.8.3） | 写进覆盖说明；自行取得文本，用 `manual_page` 或文本范围打包，不冒充 Omni 页码 |
| `omni-source` 报 `does not match its sha256 digest` 或 `read_result(...)` 过期 | artifact 读回不完整，或 Bridge 本地结果已过期 | 重读一次；过期后重新解析可能计费，先问用户 |
| `numeric-import` 报 `excerpt is not verbatim on FY<年> p<页>` / `page not in sources` | 摘录不是该页原文，或页码不在 `FY<年>.pages.jsonl` 里 | 从来源页照抄摘录、核对页码；不要改写数字格式 |
| 校验全过，但语义其实抽错了 | 脚本只校结构与一致性——`semantic_verification` 的值就是 `not_established_by_scripts`，脚本不证语义 | 逐条走 `review` 与展开原文的简报做人工复核；这是分工不是缺陷 |
| 想确认工具本身没坏 | — | 本地自检：`python3 -B scripts/test_ontology.py` 与 `python3 -B scripts/test_numeric.py`（README §交付与验证 已列，测项数以现跑为准） |

## 怎么开口（触发示例：三条正例 + 一条反例）

**开口请带上时点，输出标来源日期**：请求里给出报告期／基准日或回看窗口；成品首行标注**来源日期**，当它与用户所指日期不一致时，正文禁用「今日」「最新」，一律改写为「截至 <日期>」。
- **正例（首次试用，零凭据）**：「用 cue-omni-ontology 先拿自带样例演示：加入新材料后，哪些事实新增、哪些冲突、依据在哪里？」
  ——或直接一条命令 `python3 scripts/ontology.py demo --out <全新工作目录>`，不联网、不调解析 API，产出可展开原文的 `brief/brief.html`。
- **正例（真实两份材料）**：「根据这两份公开报告回答：①新增了什么披露；②哪些数字要区分口径不能直接比；
  ③哪些问题缺依据。给我能展开原文的简报，并保存下次可更新的知识包。」
  ——README §安装与真实资料 的那一条；来源与任务句柄分别保留，输出目录必须是新目录。
- **正例（复杂输入：第二次更新 + 边界要求）**：「把这份新公告加进已有知识包，出变化简报。
  保留旧记录，突出需要复核的冲突，**不把「未提及」当成删除**；单位、期间、口径、排除条件与有效期都进事实层，
  别替我合并成一个数。」——更新器按 update-policy 走：拒绝同 ID 偷换含义、保留冲突、去重相同陈述。
- **正例（英文说法）**：本件 frontmatter 的触发词面**已含中英两形**（`ontology extraction` / `disclosure tracking` /
  `evidence briefs` / `numeric pack` / 知识包 / 变化简报），中英任一句形起头都能命中。
- **反例（相邻需求，本件不接）**：「这两家公司谁更强，给个结论」→ 竞品决策的证据链是 `competitive-brief` 的活；
  「上市主体公开信息里的风险逐条带锚、查不到什么也记账」→ `dd-checklist`；「先翻译这本外文书再建索引」→
  `long-doc-translation`。本件只做「把公开资料变成可更新、可查证的知识包 + 变化简报」。

## 国内可达取证路径（境外站点取不到时怎么办）

本件的离线工具（`ontology.py`、`numeric.py`、`omni_source.py` 及两个测试）只依赖 Python 标准库，**demo 模式无需 API key、不联网**，
所以「先看看它是什么」这一步在国内环境没有任何额外门槛。真正取资料时有三条现成路径：

1. **用户明确提供的文件优先**：PDF、HTML、文本都可以直接作为来源进入解析与知识包——
   不依赖任何境外站点可达。国内公开材料（交易所与披露平台的公告、公司中文官网与文档站、行业协会发布的公开报告、
   公众号文章）按这一条最稳。
2. **境外站点取不到时不要绕**：把页面**由你导出成文件**再交给解析通道；本件不建爬虫，
   也不因为「URL 看起来是公开的」就假定可访问（URL 形状不能证明公开可访问）。
3. **需要横向补来源时走授权研究范围**：宿主检索工具只在授权范围内补来源，取回的内容同样留快照与出处。

三条路径**不改交付形制**：知识包仍只存直接披露的断言，冲突并列保留，快照与哈希可复核；
每个来源记 source ID 与解析日期。取不到的来源就标「未取得」，**不推断、不静默覆盖**——这与 update-policy
是同一条纪律，不因网络环境而放宽。本段不承诺任何未开放的数据域，也不承诺任何特定站点必然可达。

## 试用后，最希望听到什么？

**你的资料能否完成任务？你会不会加入第二份新材料再用一次？哪一步仍然需要大量纠错？** 这比下载量更能帮助我们改进产品。

可运行 `feedback PACKAGE --out NEW_FILE` 生成本地反馈草稿，检查后自行选择是否提交[公开问题](https://github.com/huhoo/cue-awesome/issues/new)。没有自动上传。内部材料、联系信息及商业背景通过与维护者另行约定的私有渠道交流。

如果你需要定期跟踪内部资料、接入现有 Agent/ERP/CRM、行业 schema 审阅或完整本地部署，请描述**具体任务、更新频率、当前查证成本和需要接入的流程**。这些是企业场景的讨论入口，不是此公开 skill 已交付的生产能力。

## 边界与许可

只保存直接披露的断言；计算与判断在回答中说明依据。音视频那条界是**能力带界**不是**无界**：「含音视频」只在「本地小段/切片（≤256 MiB）工作流」这个限定下成立（`references/av-backtest.md` 的 What this decides 段为唯一口径源）；逐字回查核对的是「摘录与解析产物一致」，属完整性，不等于语义为真。定义保持候选，审阅是本地记录，不提供企业 IAM 或自动行动权限。上传本地文件到云端解析不等于完整本地部署。

简报含有限长度的原文摘录；完整知识包含解析文本，分享前检查授权范围和来源使用条件。代码及说明为 [MIT](LICENSE)；公开可读不等于允许重分发整份报告。中文 README 为权威说明；Agent 指令以 `SKILL.md`（中文主）为准，`SKILL.en.md` 是其同步译文。判定=脚本现值，夹具只作已跑用例的例证、不保证穷尽。
