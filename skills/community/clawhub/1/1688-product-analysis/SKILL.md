---
id: 1688商品诊断
name: 1688-product-analysis
description: >-
  1688 商品全方位分析诊断工具，整合多数据源对指定商品进行深度分析，支持多店铺异常商品汇总、评分分层选品与单品诊断。
  覆盖能力：商品数据分析、销售表现诊断、流量问题排查、广告效果评估、商品优化建议、多店铺异常商品汇总、重点品评分分层、关键词搜索商品。
  适用场景：用户需要分析商品表现、诊断流量问题、查看多店铺异常商品、圈选重点运营商品、搜索店铺商品、获取商品优化建议时使用。
  触发词：分析这个商品、商品诊断、商品表现分析、为什么商品没流量、商品优化建议、最该优化的商品、最应该优化的商品、商品数据分析、多店铺商品、重点品查看、圈选重点品、圈选运营商品、今日运营重点、选品、推荐商品、商品分层、商品优先级、搜索商品、新品没流量怎么办、导出商品体检报告、导出当前已生成的报告、输出商品体检报告 Markdown、在当前对话输出商品体检报告。
  本 Skill 的核心流程已由 workflow `1688-product-analysis` 编排覆盖，包含明确商品 ID 诊断、异常商品选择、找问题品并诊断、关键词搜索、正向选品、同款商品分析、商品库推荐行动点与一键优化交接；单接口查询、自由组合或探索性分析回退加载本 SKILL.md。
metadata:
  engine: false
  openclaw:
    emoji: "🔬"
    requires:
      bins: ["python3"]
    primaryEnv: "ALI_1688_AK"
  interactions:
    - name: select_abnormal_offer
      type: table
      selectionType: product
      description: "从异常商品列表（及评分分层候选，如同时命中）中选择要诊断的商品。在执行 Step 0/Step 0.5 后展示，用户可多选需要诊断的商品。"
      required_data:
        title: "表格标题"
        columns: "列定义数组"
        rows: "多店汇总最多 20 条（硬封顶），按支付环比跌幅绝对值从大到小排序；单店无截断（原样返回）；每行字段：id, imageUrl, title, shop_name, reason, payAmount, changeRate, visitorCount, visitorChange, loginId（title 截断 30 个字符（Python len() 计数）；共 8 列定义，两入口都有结果时追加 discoverySource 发现来源列，id 和 loginId 不占显式列但为行必选字段）"
    - name: input_offer_id
      type: input
      selectionType: product
      description: "引导用户手动输入一个或多个商品 ID 进行诊断。"
      required_data:
        questions: "问题列表，包含一个输入框让用户填写商品 ID；多个 ID 可用空格或逗号分隔"
    - name: choose_product_locator
      type: card
      selectionType: requirement
      description: "当异常商品和评分分层均为成功零结果时，让用户选择通过商品 ID 或关键词继续定位商品。"
      required_data:
        questions: "一个单选问题，选项固定为输入商品 ID、关键词搜索"
    - name: input_search_keyword
      type: input
      selectionType: product
      description: "用户选择关键词搜索但尚未提供关键词时，引导输入商品关键词。"
      required_data:
        questions: "问题列表，包含一个商品关键词输入框"
    - name: select_products_from_scoring
      type: table
      selectionType: product
      description: "展示评分分层结果（Step 0.5 第二发现入口的 c_grade_candidates，或独立选品场景的 products），供用户选择"
      required_data:
        title: "表格标题"
        columns: "列定义数组，包含商品ID、标题、等级、分层、综合得分、支付金额、买家数、访客数"
        rows: "数据行数组，每行包含 id, title, level, levelName, totalScore, payAmount, buyerCount, uv"
    - name: select_products_from_search
      type: table
      selectionType: product
      description: "Step 1 情况B 关键词搜索结果，供用户选择目标商品"
      required_data:
        title: "表格标题，如'搜索结果: {keyword}'"
        columns: "列定义数组，包含图片、商品ID、标题、最低价、最高价、状态"
        rows: "数据行数组，每行包含 id, title, imageUrl, minPrice, maxPrice, status"
---

# 1688 商品诊断

## ⚠️ 强制约束

**Workflow 唯一入口（强制）**：商品体检、商品诊断、最该优化商品、异常商品选择、关键词搜索、明确商品 ID 诊断等核心商品诊断意图必须且只允许调用一次 workflow `1688-product-analysis`。必须把用户原始请求作为 workflow args 传入。workflow 只根据原始 query 判断执行意图，不识别真实调度来源：明确要求先选择、先询问或确认后执行时固定为 interactive；出现自动挑选/分析、无需反问或直接继续等无人值守候选语义时调用结构化模型节点，模型确认后为 automatic，“直接”不是必需词。若 query 已同时明确表达自动执行、完成诊断、在对话交付完整报告和逐商品优化建议，则即使模型返回 false、输出异常或调用失败也兜底为 automatic；普通诊断、搜索和选品仍为 interactive。主 Agent 不得自行判断模式、改写 query 或补充模式参数。组件“导出报告”按钮回填的 Markdown 导出请求是唯一例外：按第 21 条直接复用诊断流程预写的报告缓存文件或最近一次 workflow 返回的报告快照，禁止再次调用 workflow。禁止主 Agent 手工执行 `python3 cli.py`、手工拼装候选表格、读取交互协议后复刻流程，或在 workflow 正常结束后自动重试。只有用户明确请求单接口查询、自由组合或探索性分析时，才允许回退到本 SKILL.md 的 CLI 能力说明。

1. **禁止编造数据**：所有数据必须来自 CLI 真实返回结果
2. **Workflow 内先取数再分析**：核心诊断由 workflow 内部调用 CLI 获取数据后再分析，不得跳过取数；单接口查询、自由组合或探索性分析的回退路径也必须先取得 CLI 真实返回
3. **如实区分失败与空数据**：返回 `success=false` 时按失败处理；只有 `success=true` 且结果集合为空才是成功零结果。失败不得伪装成零结果，也不得继续生成依赖该结果的内容
4. **交互表格数据精简 + 截断提示**：多店汇总 rows 不超过 20 条（硬封顶，由 `--max_total_rows` 控制）、title 截断 30 个字符（Python `len()` 计数）；单店无截断（原样返回 API 全量数据），title 同样截断 30 个字符。完整诊断上下文由用户选择商品后通过 `alibaba.1688.get.item.diagnosis.context --item_id <itemId>` 按需加载。**注意**：`offerTitle` 截断不在数据源层（service.py）做，而是在 Agent 构造交互表格 rows 时做——这样单店接口返回完整标题，不走表格的场景（如直接输出 markdown）不会丢失信息。**当 `multi_shop_product_analysis` 返回结果包含 `truncation_info` 字段时，Agent 必须在展示表格之前，用自然语言向用户提示截断信息**，格式为："⚠️ 当前共检测到 {total_before_truncation} 条异常商品，涉及店铺：{shops_with_items 列表，中文顿号分隔}。为保证展示效果，表格仅展示跌幅最严重的 {total_after_truncation} 条，如需查看其他商品可输入商品 ID 进行诊断。"**禁止**忽略 `truncation_info`、禁止仅展示表格而不提示截断情况。
5. **统一聚合诊断链路**：所有进入正式诊断的商品，无论来自显式 ID、异常选择、评分候选、关键词搜索还是手工输入，Workflow 对每个 `itemId` 都只允许调用一次 `alibaba.1688.get.item.diagnosis.context --item_id <itemId>`；调用方禁止传 `loginId`、`userId` 或 `NEWTON_SHOP_LOGIN_ID`。聚合 Tool 由 seller-agent 服务端实现：内部按 `itemId` 精确定位商品归属店（OfferQueryService）并校验调用者对该店的绑定权限，不做跨店遍历兜底。Tool 返回该 `itemId` 对应的归属 `loginId`，并在同一身份下聚合 profile、performance、同款和商品库行动点。基础诊断按第 16 条的 `delivery` 分支交付：interactive 先调用 `show_interaction(type="open_tab")` 唤起组件承载页，无论调用是否成功都继续输出固定命名的 `DATA-HIDDEN-PRODUCT-DIAGNOSIS-*` 隐藏数据区块；只有组件调用未返回明确失败且全部区块发送成功时才使用组件作为主交付，组件调用返回明确失败、抛异常或任一区块发送失败时都必须同时输出完整 Markdown 报告。automatic 是唯一例外：不调用组件、不发送隐藏区块，直接以完整 Markdown 交付。禁止主 Agent 自行构造或改写协议数据。
6. **多选商品滑动并行诊断 + 基础门禁**：用户多选商品时，必须处理所有选中商品，并仅对聚合 Tool 返回非空 profile 和非空 performance 的商品继续生成报告。完整诊断采用最大并发 5 的滑动队列，任一商品完成后立即补入下一件，禁止截断或丢弃第 6 个及之后的商品。profile 或 performance 任一失败、为空或无法验证时，该商品都不得生成报告、不得进入一键优化交接；同款或商品库增强失败不得阻断基础诊断。多选时跳过基础数据失败商品并继续其他任务，若全部失败则终止流程且不交接行动点。
7. **聚合 Tool 统一解析 loginId**：候选表格中的隐藏 `loginId` 继续保留用于组件兼容和候选来源展示，但不得作为核心诊断 Tool 的入参或身份依据。`alibaba.1688.get.item.diagnosis.context` 内部由 seller-agent 按 `itemId` 精确解析商品归属店并校验绑定权限，不做逐店试错。Tool 返回的 `loginId` 是该 `itemId` 本轮诊断的权威映射；profile、performance、同款和商品库行动点必须全部使用这一身份，诊断报告和一键优化交接按 `itemId` 反查该返回值，禁止按候选行、数组位置、当前循环下标或当前店铺猜测。
8. **发现意图互斥**：发现阶段必须先按下方规则归入且只归入一个分支。明确给出 10 位及以上商品 ID 时优先直达诊断；明确关键词搜索、正向选品、找问题品并诊断、纯诊断/异常查看各分支不得混跑。“诊断问题”“排查问题”“找出问题”“停止广告后诊断”等问题导向表达必须进入找问题品并诊断；正向词与问题词同时命中时，找问题品并诊断优先。
9. **增强区块按数据展示**：同款商品分析仅在返回有效 `v2Comparison` 时展示；商品库查询仅在精确命中商品且含非空 `actions` 时，把原始行动点并入下游一键优化任务清单，不再单独输出"商品库明细建议"区块，也不展示 `aiAnalysis` 或 `statusTag`。空数据、未命中或调用失败时，必须完全隐藏对应区块，禁止输出“暂无数据”等占位文案，也不得据此臆造分析或行动点。
10. **同款触发与隐私边界**：同款竞品查询只能在用户选定待诊断商品后由聚合 Tool 执行，禁止在异常发现、评分候选或关键词搜索阶段预查。网关从 AK 上下文注入当前用户身份并校验商品归属；聚合 Tool 必须把解析出的同一 `loginId` 用于同款竞品和商品库查询。竞品标题按接口返回原文完整展示，不得自行脱敏或改写；竞品商品 ID、店铺、链接和图片地址仍不展示。
11. **行动点来源与交接**：行动点合并三路数据：原商品诊断明确识别出的标题优化/主图优化、商品库精确命中商品的原始 `actions`、同二级类目竞品 V2 中有明确事实依据且受一键优化支持的候选行动。未识别到标题或主图方向时不得默认补标题优化；跨类目对比不得生成行动点。内部保留证据和来源用于准入判断与合并去重；商品体检在报告末尾按商品说明可执行行动，并提示商家下一条消息回复“进入一键优化”，当前轮不展示确认卡。价格/定价/调价可作为经营建议展示但禁止进入下游交接；认证、备案资质、广告预算、投放金额和效果增幅不得凭空建议或预测。相同 `(offer_id, canonicalAction)` 必须合并来源；商家下一条消息明确回复“进入一键优化”后，必须把 workflow 返回的完整 handoff JSON 字符串直接作为 Workflow args 交给 `1688-item-one-click`，禁止先用用户原话试探调用、包装成 query/params、空参数调用或重复调用，逐项“执行/跳过”由一键优化完成。
12. **商家可读的对话边界**：右侧对话是商家界面，不是 Agent 工作台。所有用户可见文本必须使用简洁中文和经营语言，只说明业务结论、必要的数据依据、下一步选择或失败原因；禁止输出或复述模型推理、自言自语、英文工作笔记（如 “Let me...”“I need...”“I see...”）、数据清洗/重建过程、字段枚举、行数计算、原始 JSON、内部步骤、工具名、CLI 命令、参数、代码、调试信息或执行计划。商品列表和行动选择的具体内容由交互组件承载，对话中不得重复罗列全量商品、商品 ID 或表格行。
13. **对话话术优先级**：进入商品选择前，只用一句商家可理解的话说明发现结果，例如“已找到 {N} 件需要关注的商品，请在下方选择要体检的商品”。工作流进度标题必须使用具体业务动作：“确定体检商品”“查看经营表现”“对比优秀同款”“整理诊断报告”“准备后续操作”，禁止使用“Step 1/2/3”“阶段一/二/三”或“数据采集与分析”等笼统标题。开始诊断时，先用一条话说明本 Skill 支持经营表现诊断、同款对比和商品库建议，再统一说明“共 {N} 件商品，将开始商品体检，完成后会逐件更新结果”。用户可见文案不得展示并发数、批次或排队等内部调度细节。经营表现必须明确覆盖流量、成交、加购和转化。多商品必须把每件商品的“经营数据、同款和商品库输入准备 → 报告生成”封装成独立任务，最多使用 5 个 Worker 通过 workflow `parallel` 同时执行；任一任务结束后立即领取下一件，某件失败不得中断其他商品，最终报告必须按原商品顺序回收。每件商品只在完整任务结束时显示“已完成/暂未完成 x/N 件商品诊断”，并带具体商品 ID；禁止逐商品播报经营数据读取、同款查询或报告生成等中间状态，不得把累计数量误写成商品序号。完成后对应输出最多 3 条业务里程碑：“商品经营表现检查完成”“同款对比和商品库建议核对完成”“已生成 {N} 件商品的完整诊断报告”。工作流过程消息是追加后永久保留的内容，只能写不会过时的能力范围、开始记录或完成状态，禁止写永久残留的“正在读取”“正在对比”“正在整理”。不得播报接口调用、字段解析、数据清洗、重试、模型推理或技术错误原文。报告中按“问题/影响/依据/建议”表达；只有无法继续的失败才简要说明原因和可执行的下一步。
14. **明确目标不得重复询问**：用户已给商品 ID 时直接校验并诊断，多个 ID 按输入顺序进入最大并发 5 的滑动队列，不得再要求输入 ID、关键词或重新选品；用户说“全店”时直接执行全店异常发现，不追问店铺或商品。用户明确数量时不展示候选选择表格，按优先级自动选择 Top-N；数量超过 5 件时同样按原顺序滑动补位并处理全部已选商品，不得截断，也不得让用户再次勾选。异常商品优先级为：违规/下架/处罚等高风险优先，其余按支付环比下跌幅度降序，同幅度按支付金额降序；评分分层候选按综合得分升序（最差优先）。只有用户未提供 ID、数量或关键词时才展示原候选选择表格。
15. **同款对比完整展示与弱参考门禁**：有效 `v2Comparison` 必须在主对话正文独立输出“同款商品分析”，禁止放在思考区、折叠区或仅输出摘要。无论二级类目是否一致，都必须按“商品素材 → 经营表现 → 流量来源 → 服务保障 → 口碑评价 → 热卖 SKU”的顺序，直接展示接口返回的所有有数据维度；对标对象来源和类目校验只用于内部准入判断，不在正文展示。类目不一致时仍完整展示事实维度，但不得基于跨类目差异生成一键优化行动、认证建议、广告预算或效果增幅预测。表格必须左对齐放在对应标题下，禁止嵌套进编号或项目列表。不得使用 `notice` 总结卡，不得再生成重复的“核心对比”摘要表，不得限制为 6 行、3 个流量来源或 3 条建议。缺失维度直接省略，禁止输出空表、`-` 占位行或“暂无数据”；竞品标题完整展示，不附加“标题已脱敏”等提示，但仍不展示竞品商品 ID、店铺、链接或图片地址。同款可借鉴经验仅在同二级类目时与基础建议合并去重后放在“综合优化建议”。
16. **报告交付最高优先级（按 workflow 返回的 delivery 分支）**：`delivery=component` 只允许在 interactive 的 `show_interaction(type="open_tab")` 未返回明确失败且全部隐藏区块发送成功时返回，此时结构化基础诊断以及行动点、定时任务入口均由组件及 `footer_actions` 承载，当前回复只把 `<same_offer_markdown>` 内的同款分析原样输出到主对话，禁止重复输出基础诊断、行动点、定时任务提示或总结改写，输出后立即结束回合；`delivery=markdown` 时，**完整报告是最高优先级且不可跳过**，下一条 assistant 内容的第一个 block 必须是普通文本并立即把 `<merchant_report>` 原样完整输出，报告正文没有完整出现在主对话，就视为本次商品体检未完成。automatic 是强制组件交付的唯一免组件特例：不调用 `show_interaction(type="open_tab")`、不发送六类 `DATA-HIDDEN-PRODUCT-DIAGNOSIS-*` 隐藏区块，固定 `delivery=markdown` 并直接交付完整报告；interactive 仍按既有 component/markdown 降级契约执行。即使 interactive 组件唤起失败，workflow 仍继续发送隐藏区块供联调和恢复消费，但不得把隐藏区块发送成功冒充为组件已成功承载。两种模式下都禁止在交付完成前调用 notice、card、`show_interaction`、一键优化、其他 skill/workflow 或定时任务；一键优化和定时任务必须等用户下一条消息明确发起。若 workflow 返回 `queryStatus=failed`、`AGENT_FAILED` 或明确终止，主 Agent 只能如实展示失败结果并结束当前回合，禁止重新加载本 Skill、手工调用 CLI、改走其他 workflow 或自行补写诊断。

仅 interactive 的 workflow 先调用 `callTool('show_interaction', {type:"open_tab", url:"webComponent:csbc-newton-modules-seller-data-table?planCode=CDT_68lm5S", title:"AI商品诊断"})` 唤起组件，再通过 `emit` 按六类真实 section 一一输出固定隐藏数据围栏：`DATA-HIDDEN-PRODUCT-DIAGNOSIS-META`、`DATA-HIDDEN-PRODUCT-DIAGNOSIS-CATALOG`、`DATA-HIDDEN-PRODUCT-DIAGNOSIS-PRODUCT`、`DATA-HIDDEN-PRODUCT-DIAGNOSIS-OVERVIEW`、`DATA-HIDDEN-PRODUCT-DIAGNOSIS-ACTIONS`、`DATA-HIDDEN-PRODUCT-DIAGNOSIS-COMPLETED`。其中 `PRODUCT` 可按商品重复输出，其他围栏每份报告各输出一次。automatic 不调用该组件、也不发送本协议中的任何隐藏区块，直接输出完整 Markdown。JSON 由 workflow 程序化组装；主 Agent 不得改写、摘要、重新生成或在对话中复述这些代码块。
17. **报告末尾展示非阻塞后续操作**：interactive 在准备后续操作时通过 `check_auto_diagnosis_schedule` 只读当前 workspace 的定时任务状态。只有 `enabled=true` 且任务名称包含“1688商品自动体检”或“1688商品体检”，或者描述同时包含“1688商品体检”和自动找出待优化商品、生成商品诊断报告等业务语义时，才视为已配置，`enabled=false` 不算已配置。查询失败时按防重复原则隐藏定时任务提示。`delivery=component` 时，行动点和定时任务入口只由组件 `footer_actions` 承载，主对话不得重复；`delivery=markdown` 时，才在 `merchant_report` 末尾按商品列出“商品标题（ID）→ 可执行行动”，并提示“回复‘进入一键优化’”。一键优化 workflow 自己逐项确认执行/跳过，商品体检当前轮不再展示阻塞式确认卡。interactive 确认未配置相关任务时，Markdown 报告才追加“⏰需要我自动帮你找出需要优化的商品嘛？点击设置定时任务”和“回复‘设置定时任务’”；已配置或查询失败时不追加。automatic 必须跳过 `check_auto_diagnosis_schedule` 和定时任务入口，报告末尾不展示“设置定时任务”；可执行建议仍作为文字报告的一部分，但不得自动修改商品。触发词必须保持普通文本，禁止给“进入一键优化”或“设置定时任务”添加 `**`、`__`、反引号或其他 Markdown 包裹。当前轮禁止调用 notice、card 或定时任务表单。用户下一条消息明确回复“进入一键优化”时才调用一次 `1688-item-one-click` workflow；明确表达设置商品自动体检定时任务的意图（包括手动回复“设置定时任务”或组件按钮完整 prompt 回填）时，才收集执行频率和时间并调用 `show_interaction(type="schedule_task")`，只有返回 `action="execute"` 后才调用 `Schedule(action="create")`。主 Agent 禁止再次调用 `Schedule(action="list")`。新建任务名称建议为“1688商品自动体检”，任务 prompt 默认且完整使用“自动按优先级挑出【最该优化的 5 个商品】，完成诊断后直接在对话中输出完整报告和每个商品的优化建议”。定时任务只负责自动运行商品体检、输出报告和行动点，禁止自动修改商品。
18. **商家输出净化与诊断去重**：报告进入 `merchant_report` 前必须删除模型思考、自言自语、原始工具 JSON、TodoWrite/Edit 内容、协议标签、代码执行痕迹和内部调度信息。不得出现“Now let me”“I need to”“让我先”“接下来调用”等过程语句。组件 `product_result.reason` 只写流量、成交、加购、转化、广告等经营数据结论；`anomalies` 只写标题、类目、属性、合规或身份冲突等内容异常，同一问题不得在两处重复。净化只删除内部内容，不得压缩、总结或删减基础诊断、同款事实表格和综合优化建议。
19. **增强数据四态**：同款和商品库诊断必须分别记录 `success / no_data / unauthorized / tool_failed`。仅 `success` 数据可进入报告或行动点；`no_data` 隐藏对应区块；`unauthorized` 与 `tool_failed` 只记录在内部执行清单，不得伪装成无数据、不得据此生成建议，也不得阻断基础诊断。
20. **选品对象与诊断对象必须一致**：自动选品必须先完成确定性排序再截取 Top-N，候选表也使用同一排序。异常候选按高风险、支付跌幅绝对值、支付金额排序；C级候选按综合得分升序。候选的商品 ID、选择原因和排序指标必须随商品进入诊断。商品详情返回后重新核对标题；候选标题与详情标题不一致时，以详情标题和当前经营数据为准，报告明确提示数据不一致，不得沿用候选标题推断类目错放或商品问题。商品详情内部的标题、类目、描述和属性明显冲突时，只报告不受影响的经营指标并标记“商品资料存在数据一致性异常”，不得直接判为类目错放，也不得基于冲突文本生成优化建议。
21. **导出报告由 Skill 承接（缓存优先）**：诊断结束时 workflow 已把报告全文预写为 `.report-cache-<报告编号>.md`，默认落在 Agent 当前工作目录（即写入 `商品体检报告.md` 的目录），写不进去时回退到本 skill 根目录（`cli.py` 所在目录，本文档所有 CLI 命令的绝对路径前缀，形如 `.../skills/newton_seller/1688-product-analysis`）。组件“导出报告”按钮回填的 prompt 指明报告全文缓存在当前工作目录（缓存预写失败回退 skill 根目录时措辞随之变化），前端无需附加参数。缓存文件名为 `.report-cache-<报告编号>.md`，报告编号含诊断时间戳（形如 `pd_20260731151541_lqz3`），存在多份时取时间戳最新的一份。用户点击“导出报告”后，Agent 按回填消息指明的位置定位缓存文件：在工作目录时用 `.report-cache-*.md` 模式直接定位（一次精准 Glob 即可，禁止全盘搜索），在 skill 根目录时到 cli.py 所在目录定位；随后只允许两个工具调用——先 Read 缓存文件取得报告全文，再调用一次 `Write` 把读到的内容原样写入相对路径 `商品体检报告.md`，禁止改动、总结、删减或补充任何内容。回填消息中没有报告编号时（缓存预写失败），回退读取当前会话最近一次成功的 `1688-product-analysis` workflow 返回中的 `<export_report_markdown>` 标签并完整复制标签内 Markdown；组件降级时没有该标签，可使用最近一次成功返回的 `<merchant_report>`。导出是严格幂等流程：上下文中尚无该请求的 `Write` 成功结果时，只允许执行一次“Read 缓存 + Write”或一次 `Write`；Newton 会根据 Write 成功结果自动渲染文件卡，严禁调用 `present_files`。只要上下文已出现该文件的 Write 成功结果，就视为导出完成，绝对禁止再次调用任何工具；只回复“已导出商品体检报告.md。”并结束。禁止再次调用 workflow、商品查询、组件或模型；严禁全盘搜索文件系统，严禁读取或转换任何 JSON 文件、旧报告或其他工作区文件，严禁调用 Bash、Edit、`present_files`、`schedule_task`、`show_interaction` 或其他工具，禁止生成 JSON、中间文件或第二个附件，也不依赖 reportId 或会话外存储。缓存文件与两个标签都缺失或读取失败时，不得创建空文件、不得搜索文件或重建、编造报告，只回复“报告缓存已失效，请重新发起商品体检后再导出。”

## 数据查询命令

统一入口：`{python} {baseDir}/cli.py <command> [options]`

> `{python}` 表示本机可用的 Python 3 解释器，禁止硬编码 `python3`：macOS/Linux 用 `python3`；Windows 上 `python3` 通常不存在（会报 `'python3' 不是内部或外部命令`），必须按 `python3` → `python` → `py -3` 顺序尝试，第一个成功返回版本号的即可用（仅命令存在不算可用：Windows 商店的假 `python3.exe` 会打印 `Python was not found` 并非零退出）。workflow 内部已自动探测并缓存，本节命令仅在回退到手工执行 CLI 时使用。

`__userId__` 由 `cli.py` 通过解析 `ALI_1688_AK` 自动注入，命令本身无需感知卖家身份。

| 命令                           | 用法                                                                                                                          | 说明                                                                                          |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `get_bindlist`                 | `{python} {baseDir}/cli.py get_bindlist`                                                                                       | 查询当前用户绑定的多店铺列表（含各店铺 loginId）                                              |
| `multi_shop_product_analysis`  | `{python} {baseDir}/cli.py multi_shop_product_analysis [--shop_name <店铺名>] [--date_type <日期类型>] [--device <设备>] [--max_total_rows <行数>] [--no-lite]`         | 批量查询多店铺异常商品汇总（默认所有绑定店铺，支持指定店铺）                                   |
| `get_abnormal_offers`          | `{python} {baseDir}/cli.py get_abnormal_offers [--date_type <日期类型>] [--device <设备>] [--NEWTON_SHOP_LOGIN_ID <loginId>] [--no-lite]`     | 查询异常商品列表（支付下跌、访客下跌等），支持指定店铺                                          |
| `alibaba.1688.get.item.diagnosis.context`   | `{python} {baseDir}/cli.py alibaba.1688.get.item.diagnosis.context --item_id <itemId>`                                                       | 核心 Workflow 正式诊断入口；内部解析商品归属并聚合基础数据、同款和行动点，返回命中商品的 loginId |
| `alibaba.1688.get.offer.data`               | `{python} {baseDir}/cli.py alibaba.1688.get.offer.data --offer_id <商品ID> [--modules <模块列表>] [--NEWTON_SHOP_LOGIN_ID <loginId>]` | 兼容或自由查询商品模块；不再是核心 Workflow 正式诊断路径  |
| `get_item_overview`            | `{python} {baseDir}/cli.py get_item_overview`                                                                                  | 获取商品概览统计（商品总数、有销售商品数、总销售额等），Step 0.5 前置数据收集                  |
| `get_shop_data`                | `{python} {baseDir}/cli.py get_shop_data`                                                                                      | 获取店铺维度数据（支付金额、支付买家数、在线商品数），作为 `score_and_select` 的评分基准        |
| `score_and_select`             | `{python} {baseDir}/cli.py score_and_select --shop_total '<get_shop_data返回JSON>' [--strategy <策略>] [--limit <N>] [--top_n <N>]` | 五维度评分分层全店商品，返回 Top-N 高分排序商品（`products`，正向选品再筛 S/A/B）与全部 C 级候选（`c_grade_candidates`，供 Step 0.5 使用） |
| `search_offer_by_keyword`      | `{python} {baseDir}/cli.py search_offer_by_keyword --keyword <关键词> [--page <页码>] [--page_size <每页数量>]`                  | 通过关键词搜索店铺商品，用于 Step 1 情况B 辅助定位商品                                        |
| `get_same_offer_competition`   | `{python} {baseDir}/cli.py get_same_offer_competition --offer_id <商品ID> [--NEWTON_SHOP_LOGIN_ID <loginId>]`                    | 兼容或自由查询同款 V2 对标事实；核心 Workflow 由聚合 Tool 内部调用            |
| `get_offer_diagnosis_actions`  | `{python} {baseDir}/cli.py get_offer_diagnosis_actions --offer_id <商品ID> [--NEWTON_SHOP_LOGIN_ID <loginId>]`                   | 兼容或自由查询商品库行动点；核心 Workflow 由聚合 Tool 内部调用                              |

### alibaba.1688.get.item.diagnosis.context 参数说明

- `--item_id`：10 位及以上且在 Java Long 正数范围内的纯数字商品 ID（**必填**）
- 调用方只传 `itemId`；`userId` 由运行时上下文注入，禁止传 `loginId` 或 `NEWTON_SHOP_LOGIN_ID`
- Tool 内部（seller-agent 服务端）按 `itemId` 精确定位商品归属店并校验调用者绑定权限；商品不存在返回 `offer_not_found`，无权限返回 `unauthorized`，不做跨店遍历
- 返回命中商品的 `loginId`，并保证 profile、performance、同款和行动点都使用这一身份
- profile 与 performance 是基础门禁；同款和行动点分别返回 `success`、`no_data`、`unauthorized`、`tool_failed` 四态

输出 JSON：`itemId`、`loginId`、`shopName`、`title`、`imageUrl`、`offerData.profile`、`offerData.performance`、`enhancements.competition`、`enhancements.diagnosisActions`。

```bash
{python} {baseDir}/cli.py alibaba.1688.get.item.diagnosis.context --item_id 1048050628164
```

> `get_bindlist`、`alibaba.1688.get.offer.data`、`get_same_offer_competition`、`get_offer_diagnosis_actions` 继续保留，供兼容、单接口或自由组合查询使用；核心 Workflow 不再分别调用这些命令完成正式诊断。

### multi_shop_product_analysis 参数说明

- `--shop_name`：指定店铺名称（可选，模糊匹配 `companyName`），不传则查询所有绑定店铺
- `--date_type`：日期类型（可选，默认 `RECENT_7`）
  - 可选值：`RECENT_7`（近 7 天）、`RECENT_30`（近 30 天）
- `--device`：设备筛选（可选，默认 `ALL`）
  - 可选值：`ALL`（全部）、`PC`、`APP`
- `--max_total_rows`：多店汇总后全局硬封顶行数（可选，默认 `20`，超出则按跌幅绝对值排序后从尾部裁掉，硬性最大值 20 不可绕过）
- `--no-lite`：关闭 lite 裁剪模式（可选，默认开启 lite，删除 valueMap 中非映射 key 和 cycleCqc 子字段以减少 payload 体积）

> **多店铺逻辑**：内部自动调用 `get_bindlist` 获取绑定店铺列表，遍历各店铺通过 `NEWTON_SHOP_LOGIN_ID` 参数查询异常商品并汇总。Agent 只需传 `--shop_name`，不接触 loginId。

返回值示例：

```json
{
  "success": true,
  "data": {
    "truncation_info": {
      "total_before_truncation": 60,
      "total_after_truncation": 20,
      "shops_with_items": ["XX贸易有限公司", "YY科技有限公司", "ZZ五金厂"],
      "truncated": true
    },
    "shops": [
      {"shop_name": "XX贸易有限公司", "is_current": true, "count": 2, "items": [{"itemId": "...", "shop_name": "XX贸易有限公司", "loginId": "xxx", ...}]},
      {"shop_name": "YY科技有限公司", "is_current": false, "count": 1, "items": [{"itemId": "...", "shop_name": "YY科技有限公司", "loginId": "yyy", ...}]}
    ]
  }
}
```

> **注意**：`truncation_info` 仅在发生截断时出现（截断前总条数 > `max_total_rows`）；未截断时返回结构中无此字段。截断后每条 item 会包含 `shop_name` 和 `loginId` 永久字段。截断后 `count=0` 的店铺会从 `shops` 数组中移除（但 `truncation_info.shops_with_items` 仍会记录该店铺名，表示其也有异常商品但不够严重未入选）。

### get_abnormal_offers 参数说明

- `--date_type`：日期类型（可选，默认 `RECENT_7`）
  - 可选值：`RECENT_7`（近 7 天）、`RECENT_30`（近 30 天）
- `--device`：设备筛选（可选，默认 `ALL`）
  - 可选值：`ALL`（全部）、`PC`、`APP`
- `--NEWTON_SHOP_LOGIN_ID`：店铺登录ID（可选），指定查询的店铺。值为 `get_bindlist` 返回的对应店铺 `loginId`。不传则使用当前 AK 对应的默认店铺
- `--no-lite`：关闭 lite 裁剪模式（可选，默认开启 lite，删除 valueMap 中非映射 key 和 cycleCqc 子字段以减少 payload 体积）

返回值示例：

```json
{
  "success": true,
  "data": {
    "count": 20,
    "items": [
      {"itemId": "668758083302", "offerTitle": "...", "reason": "支付下跌", "valueMap": {...}},
      {"itemId": "779218424674", "offerTitle": "...", "reason": "访客下跌", "valueMap": {...}}
    ]
  }
}
```

### alibaba.1688.get.offer.data 参数说明

- `--offer_id`：商品 ID，字符串（**必填**）
- `--modules`：要获取的数据模块，逗号分隔（命令能力默认 `all`；该旧命令仅用于兼容、单接口或自由组合查询，核心 Workflow 正式诊断改用 `alibaba.1688.get.item.diagnosis.context`）
  - 可选值：`profile`（基础资料）、`performance`（表现）、`huopan`（货盘）、`search_issues`（搜推问题）、`purchase_factors`（购买因素）、`sycm_anomaly`（异常检测）、`ad_analysis`（广告分析）、`hotwords`（热搜词）、`hot_items`（热品）、`all`
- `--NEWTON_SHOP_LOGIN_ID`：店铺登录ID（可选），指定查询的店铺。值为 `get_bindlist` 返回的对应店铺 `loginId`。不传则使用当前 AK 对应的默认店铺

输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

示例：

```bash
# 兼容/自由查询基础资料与表现（当前店铺）
{python} {baseDir}/cli.py alibaba.1688.get.offer.data --offer_id 1048050628164 --modules profile,performance

# 仅获取表现 + 广告 + 搜推问题
{python} {baseDir}/cli.py alibaba.1688.get.offer.data --offer_id 1048050628164 --modules performance,ad_analysis,search_issues

# 多店场景：查询指定店铺的诊断数据
{python} {baseDir}/cli.py alibaba.1688.get.offer.data --offer_id 1048050628164 --modules profile,performance --NEWTON_SHOP_LOGIN_ID <loginId>
```

### score_and_select 参数说明

- `--shop_total`：店铺维度数据 JSON 字符串，由 `get_shop_data` 命令获取（**必填**）
- `--strategy`：查询策略（可选，默认 `comprehensive`）
  - 可选值：`comprehensive`（综合排序）、`sales`（按销售额）、`all`（全部商品）
- `--limit`：获取商品数量上限（可选，默认 `100`）
- `--top_n`：输出排名前N的商品（可选，默认 `10`）

返回 `data.data` 结构：`total_scored`（评分商品总数）、`returned_count`、`products`（Top-N 商品，供正向选品过滤 S/A/B）、`summary`（S/A/B/C 各级数量）、`c_grade_candidates`（全部 C 级候选，按综合得分升序、最差优先，最多20条；即使已进入 products 也保留）。

### search_offer_by_keyword 参数说明

- `--keyword`：搜索关键词（可选）。仅当返回 `success=true` 且结果为空时，**让大模型尝试换几个简短的相似词来搜索，最多尝试 3 次**；`success=false` 是调用失败，必须展示失败信息，不得当作零结果换词搜索
- `--page`：页码（可选，默认 1）
- `--page_size`：每页数量（可选，默认 10）

## 参考文档

参考文档（按需查阅）：

| 文档     | 路径                                       |
| -------- | ------------------------------------------ |
| 分析维度 | `references/analysis-dimensions.md`        |
| 报告模板 | `references/report-template-simple.md`     |
| 交互规范 | `references/interaction-specs.md`          |
| 评分规则 | `references/scoring-rules.md`              |

## 安全声明

| 风险级别 | 命令                           | Agent 行为             |
| -------- | ------------------------------ | ---------------------- |
| **只读** | `get_bindlist`                 | 可直接执行，无需确认   |
| **只读** | `multi_shop_product_analysis`  | 可直接执行，无需确认   |
| **只读** | `get_abnormal_offers`          | 可直接执行，无需确认   |
| **只读** | `alibaba.1688.get.item.diagnosis.context`   | 可直接执行，无需确认   |
| **只读** | `alibaba.1688.get.offer.data`               | 可直接执行，无需确认   |
| **只读** | `get_item_overview`            | 可直接执行，无需确认   |
| **只读** | `get_shop_data`                | 可直接执行，无需确认   |
| **只读** | `score_and_select`             | 可直接执行，无需确认   |
| **只读** | `search_offer_by_keyword`      | 可直接执行，无需确认   |
| **只读** | `get_same_offer_competition`   | 可直接执行，无需确认   |
| **只读** | `get_offer_diagnosis_actions`  | 可直接执行，无需确认   |

## 输出约束（强制）

Agent 执行本 Skill 时，**对用户可见的正文**（非 `<aside>` 包裹的内容）禁止包含：

1. **工具名 / 函数名**：`show_interaction`、`read_file`、`Bash`、`get_bindlist`、`alibaba.1688.get.offer.data`、`multi_shop_product_analysis`、`score_and_select` 等
2. **CLI 命令原文**：`python3 cli.py ...` 等完整命令行
3. **接口 / 参数 / 字段名**：`NEWTON_SHOP_LOGIN_ID`、`valueMap`、`cycleCrc`、`truncation_info`、`c_grade_candidates`、`--modules`、`--max_total_rows` 等
4. **执行步骤编号**：禁止输出 "Step 1"、"Step 2" 等内部流程标记
5. **中间推理过程**：禁止输出 "正在解析参数"、"接口返回 success:true" 等推理痕迹

**允许输出的内容：**
- `<aside>` 包裹的简短过渡语（如 `<aside>正在获取商品数据...</aside>`）
- Final Answer 中的业务结果和分析报告

**正反示例：**

❌ "调用 show_interaction 展示异常商品表格，设置 selectionType='select_abnormal_offer'"
✅ "<aside>正在为您展示异常商品列表...</aside>" → 然后展示表格

❌ "执行 python3 cli.py alibaba.1688.get.offer.data --offer_id 668758083302 --NEWTON_SHOP_LOGIN_ID tb123456"
✅ "<aside>正在获取商品详细数据...</aside>" → 然后执行命令

❌ "Step 2：读取 references/analysis-dimensions.md 获取分析标准"
✅ "<aside>正在准备分析标准...</aside>" → 然后读取文件

❌ "接口返回 truncation_info.truncated=true，total_before_truncation=60"
✅ "⚠️ 当前共检测到 60 条异常商品，表格仅展示跌幅最严重的 20 条"

## 诊断执行步骤

### Step 0 + Step 0.5：互斥意图发现阶段

按以下优先级判断用户 query，命中后只执行对应分支，禁止跨分支补跑：

1. **显式商品 ID 直达诊断**：用户明确给出 10 位及以上商品 ID 时，跳过 Step 0、Step 0.5 和 Step 1，直接把该 ID 加入待诊断列表并进入 Step 2。归属校验与完整诊断统一复用该商品唯一一次 `alibaba.1688.get.item.diagnosis.context --item_id <itemId>` 调用，Workflow 不自行遍历店铺。
2. **明确关键词搜索**：用户明确要求按商品关键词搜索（如“搜索店铺里的蓝牙耳机”“查找关键词为保温杯的商品”），且未给出商品 ID 时，执行关键词搜索分支。搜索结果再决定是否进入 Step 2，禁止补跑评分或异常发现。
3. **找问题品并诊断**：命中“新品没流量 / 没有流量 / 没流量 / 低效 / 滞销 / 最需要优化 / 最该优化 / 最应该优化 / 优先优化 / 先改哪个 / 优化调整”等问题导向语义时，执行问题发现分支。即使同时命中“选品 / 推荐 / 圈选”等正向词，也优先归入本分支。
4. **正向选品**：用户想推荐或圈选值得投入的商品，且未命中任何问题导向语义时，执行正向选品分支。
5. **纯诊断 / 异常查看**：用户仅表达分析商品、商品诊断、查看异常等意图，且不满足前四项时，执行纯诊断分支。

#### 明确关键词搜索（仅搜索，按结果分流）

直接执行：

```bash
{python} {baseDir}/cli.py search_offer_by_keyword --keyword "<用户关键词>"
```

- 返回 `success=false` 时展示失败信息并立即终止；禁止把失败当作零结果，禁止补跑评分、异常发现、相似词或手工 ID 流程
- 返回 `success=true` 且结果 `>=2` 条时，触发 `select_products_from_search` 表格供用户勾选；用户选择后把所有选中商品加入待诊断列表并进入 Step 2
- 返回 `success=true` 且结果 `=1` 条时，不触发表格，直接把唯一商品的 ID 加入待诊断列表并进入 Step 2
- 返回 `success=true` 且结果 `=0` 条时，最多尝试 3 个简短相似词；每次仍严格区分失败与成功零结果。任一次失败立即终止；任一次得到结果则按 `>=2` 或 `=1` 分支处理；3 次均为成功零结果后再提供手工输入商品 ID
- 本分支禁止调用 `multi_shop_product_analysis`、`get_item_overview`、`get_shop_data` 或 `score_and_select`

#### 正向选品（仅评分，展示后结束）

`get_item_overview` 与 `get_shop_data` 无数据依赖，必须在同一轮并行执行：

```bash
{python} {baseDir}/cli.py get_item_overview
{python} {baseDir}/cli.py get_shop_data
```

只有 `get_item_overview` 与 `get_shop_data` 都返回 `success=true` 时，才允许执行：

```bash
{python} {baseDir}/cli.py score_and_select --shop_total '<get_shop_data返回的JSON>' [--strategy <策略>] [--top_n 10]
```

- 任一前置命令返回 `success=false` 时，先展示其失败信息并立即终止正向选品分支；禁止调用 `score_and_select`，禁止用失败结果评分
- `score_and_select success=false` 时展示失败信息并立即终止正向选品分支
- `score_and_select success=true` 后只读取 `products`，并仅保留等级为 S、A、B（兼容 `S级`、`A级`、`B级`）的商品作为值得重点运营候选；C/C级商品必须过滤，禁止称为“推荐商品”“重点品”或“引流款”。过滤后候选 `>=2` 个时用 `select_products_from_scoring` 展示“重点品圈选结果”；候选 `=1` 个时使用下方专用 Markdown 格式；候选 `=0` 个时只输出且只输出“当前没有合适的重点运营候选。”后立即结束。禁止追加异常商品汇总、诊断、建议、后续计划或行动引导
- 本分支禁止调用 `multi_shop_product_analysis`，禁止混入异常商品
- 正向选品输出只允许陈述 CLI 返回的数据事实、评分等级/分层和基于这些数据的入选理由；允许原样展示 `classification.name`（包括“重点推广品”），但禁止把分层名称扩写成建议语态或下一步动作，禁止生成“建议优化/调整/补充/推广/参加活动/提升/下架”等行动指令，也禁止脱离 CLI 数据推断“引流款”等货盘定位
- 无论过滤后的候选数量多少，都不触发聚合诊断 Tool、诊断报告或一键优化交接；完成对应展示或提示后立即结束。特别是候选 `=0` 时，禁止根据店铺整体数据补充运营诊断或“接下来怎么做”

正向选品只有 1 个候选时，必须使用以下专用格式，不得引用诊断报告模板，不得显示货盘标签：

```markdown
### [商品标题]

- 商品 ID：[offer_id]
- 评分分层：[classification.level] · [classification.name]
- 关键指标：[仅列出 score_and_select 对该商品真实返回的指标和值]
- 入选理由：[仅基于上述真实指标说明为何进入 S/A/B 候选]
```

#### 找问题品并诊断（异常发现 + 评分）

以下 3 个命令无数据依赖，必须在同一轮并行执行：

```bash
{python} {baseDir}/cli.py multi_shop_product_analysis [--shop_name "店铺名"]
{python} {baseDir}/cli.py get_item_overview
{python} {baseDir}/cli.py get_shop_data
```

异常源与评分源相互独立，分别按以下门禁处理：

- **异常源**：`multi_shop_product_analysis success=false` 时展示失败信息并将异常源标记为不可用，但不得阻断可用的评分源。外层 `success=true` 时仍必须检查 `shops`：若所有返回店铺都含 `error`（或顶层含 `error` 且无成功店铺），异常源同样不可用，禁止当作成功零结果；若只有部分店铺含 `error`，仅消费无 `error` 店铺的数据，并向用户提示失败店铺，异常源仍可用
- **评分源前置**：只有 `get_item_overview` 与 `get_shop_data` 都返回 `success=true` 时才允许执行 `score_and_select`。必须区分失败阶段：商品概览失败展示“商品概览数据暂时无法获取，已跳过评分候选”；店铺经营数据失败展示“店铺经营数据暂时无法获取，已跳过评分候选”。随后将评分源标记为不可用；禁止用失败结果评分，但不得阻断可用的异常源
- **评分执行**：前置成功后执行以下命令；`score_and_select success=true` 时评分源可用且只读取 `c_grade_candidates`；`success=false` 时展示“商品明细评分暂时无法完成，已跳过评分候选”，将评分源标记为不可用，但不得阻断可用的异常源。成功但候选为空是正常零结果，不得展示失败文案

```bash
{python} {baseDir}/cli.py score_and_select --shop_total '<get_shop_data返回的JSON>' [--strategy <策略>] [--top_n 10]
```

- 评分结果只读取 `c_grade_candidates`，禁止读取 `products`
- 两个来源都有候选时合并异常商品与 `c_grade_candidates`；只有一个来源有候选时仅使用该来源，随后进入 Step 1
- 两个来源都因失败而不可用时，必须展示异常源和评分源已有失败信息并立即终止本次自动发现；不得进入 Step 1 情况 C，不得构造候选、诊断报告或一键优化交接。可以提示用户稍后重试；只有用户另行明确输入商品 ID 后，才可将其作为新的显式 ID 请求从头开始
- 若至少一个来源 `success=true` 但最终两个来源都没有候选，则按成功零结果进入 Step 1 情况 C。该状态必须与双源失败区分，不得使用失败返回构造候选

#### 纯诊断 / 异常查看（仅异常发现）

只执行以下命令，禁止执行评分相关命令：

```bash
{python} {baseDir}/cli.py multi_shop_product_analysis [--shop_name "店铺名"]
```

返回结果沿用上方“异常源”门禁：全部店铺失败时展示错误并终止，部分店铺失败时只展示成功店铺结果并提示失败店铺；禁止把店铺 `error` 当作成功零结果。

> `--strategy`/`--limit` 由 `get_item_overview` 返回的商品总数决定：≤200 用 `--strategy all`；201-500 用默认 `comprehensive`；>500 加 `--limit 200`。此规则只适用于会执行评分的正向选品和找问题品并诊断分支。

#### Step 0 参数说明

- 用户未提店铺名 → 不传 `--shop_name`（遍历所有绑定店铺）
- 用户提了店铺名 → `--shop_name "店铺名称"`（仅查该店铺）
- 若无绑定店铺，命令内部不传 `login_id`，使用当前登录态执行

> **⚠️ 禁止行为**：当用户请求的是**商品诊断/异常商品汇总**类需求时，**严禁**先调用 `get_bindlist` 获取 loginId 再调 `get_abnormal_offers` 的备用链路。**必须**直接调用 `multi_shop_product_analysis [--shop_name "XX"]`。
>
> **✅ 允许行为**：当用户明确指定要查询**某个具体接口的数据**（如"查XX店铺的流量趋势"、"看XX店铺的广告效果"）且不属于商品诊断流程时，可以调用 `get_bindlist` 获取对应店铺的 loginId，再通过 `--NEWTON_SHOP_LOGIN_ID` 参数调用对应的单店铺接口。

绑定店铺路径下，Step 0 返回结果中每个异常商品都标明 `shop_name`（归属店铺）和对应的隐藏 `loginId`。构造多店表格时必须把 `offer_id` 和 `loginId` 一起保留到行数据以维持交互协议，但用户选择后正式诊断只把 `itemId` 传给 `alibaba.1688.get.item.diagnosis.context`；候选 `loginId` 不透传，最终归属以聚合 Tool 返回值为准。无绑定店铺时返回“当前店铺”降级结果，不含 `loginId` 属于正常情况，不阻断后续聚合诊断。

> **不再使用** `get_abnormal_offers` 作为首选命令，`multi_shop_product_analysis` 已完全替代其功能（无绑定店铺时行为一致）。

### Step 1: 交互选择（前置步骤）

> 本步骤只在 interactive 的**找问题品并诊断**或**纯诊断 / 异常查看**分支执行；正向选品已在上一步展示清单并结束，不会进入本步骤。automatic 不展示候选表、不要求输入商品 ID 或关键词：沿用现有优先级排序，按 `offerId` 去重后取最多 5 个候选；0 个候选正常结束，1–4 个全部进入诊断，5 个以上只诊断前 5 个。

根据 Step 0（异常商品汇总）与问题诊断分支的 Step 0.5（评分分层候选 `c_grade_candidates`，若触发）结果，分三种情况处理：

**情况 A：两个入口都有结果**

以 Table 组件展示合并后的候选商品：

- 设置 `name='select_abnormal_offer'`
- 把 Step 0 的 `items` 与 Step 0.5 的 `c_grade_candidates` 合并后按 `references/interaction-specs.md` 中 `select_abnormal_offer` 章节的"发现来源列"规则转换，`rows` 追加 `discoverySource` 字段（`"异常下跌"` 或 `"评分分层-C级"`）
- 每条商品标明归属店铺 `shop_name`（Step 0.5 的候选若无店铺概念，`shop_name` 填当前默认店铺名）
- **截断提示**：若 Step 0 返回结果包含 `truncation_info` 字段，按强制约束第 4 条提示截断信息

**情况 B：只有一个入口有结果**

按现有逻辑展示（不出现 `discoverySource` 列）：
- 只有 Step 0 有结果 → 沿用原 `select_abnormal_offer` 8 列展示
- 只有 Step 0.5 有结果 → 触发 `select_products_from_scoring`，`rows` 来自 `c_grade_candidates`

> ⚠️ **imageUrl 字段必须为完整 URL**（以 `https://` 开头），不得直接复制 CLI 返回的相对路径。CLI 已在数据源层完成 CDN 前缀补全，直接赋值 `offerImageUrl` 即可。若发现值不以 `http` 开头，必须拼接 `https://cbu01.alicdn.com/` 前缀。

用户明确指定诊断数量时，先按强制约束第 14 条排序并直接取 Top-N，禁止触发商品选择表格。未指定数量时，用户选择商品后只提取**所有**选中行的 `id`（即 `itemId`/`item_id`）组成待诊断列表；用户未选择或取消时结束本次体检，禁止默认选择第一行。多店表格中的隐藏 `loginId` 仅用于组件兼容和候选来源展示，不进入诊断任务；报告与行动阶段统一使用 `alibaba.1688.get.item.diagnosis.context` 返回的权威 `itemId -> loginId` 映射，禁止依赖候选行或数组位置关联。完整诊断进入最大并发 5 的滑动队列，任一商品完成后立即补入下一件，按既定排序处理全部商品，不得截断。

后续 Step 2 和 Step 3 把列表中的每个商品封装成独立任务，使用最大并发 5 的滑动队列执行，并按原始顺序回收结果。

**情况 C：两个入口都为空**

并列提供两种辅助定位方式，由用户选择其一。先触发 `choose_product_locator` Card 组件，选项固定为“输入商品 ID”“关键词搜索”；用户未选择时结束本次体检，禁止默认进入任一分支：

1. **手动输入商品ID**：用户选择后，以 Input 组件（`name='input_offer_id'`）引导输入一个或多个商品 ID；多个 ID 按空格或逗号拆分、去重，进入最大并发 5 的滑动校验队列，任一商品完成后按输入顺序立即补入下一件
2. **关键词搜索**：用户选择后，以 Input 组件（`name='input_search_keyword'`）获取关键词，再调用 `search_offer_by_keyword`。仅当 `success=true` 时按结果数量处理：结果 `>=2` 条时触发 `select_products_from_search` 表格供用户勾选；结果 `=1` 条时直接把唯一商品的 `id` 加入待诊断列表并进入 Step 2，不触发表格；结果 `=0` 条时才可尝试简短相似词恢复（最多 3 次），相似词仍为成功零结果后再提供手工 ID。`success=false` 必须展示调用失败并终止本次搜索，禁止当作零结果进入相似词或手工 ID 流程

**具体的数据结构请查阅 `references/interaction-specs.md` 中对应交互的章节。**

> 如果用户已明确提供了 10 位及以上商品 ID，必须跳过 Step 0、Step 0.5 和 Step 1，直接进入 Step 2。

### Step 2: 读取分析标准 + 收集商品数据（循环执行）

对直达诊断或 Step 1 产出的待诊断列表，把**每个商品封装成独立任务并放入最大并发 5 的滑动队列**，任一任务完成后立即补入下一件，最终按原商品顺序回收。无论候选来源是否携带隐藏 `loginId`，Workflow 都只把 `itemId` 传给聚合 Tool；同一 workflow 内同一 `itemId` 只调用一次并复用结果：

1. 首次循环时查阅分析标准（references/analysis-dimensions.md，仅读一次后续复用）
2. 调用 `alibaba.1688.get.item.diagnosis.context --item_id <itemId>`，禁止附加 `loginId`、`userId` 或 `NEWTON_SHOP_LOGIN_ID`。Tool 内部（seller-agent 服务端）按 `itemId` 精确定位归属店并校验绑定权限，返回该 `itemId` 对应的 `loginId`、店铺名、标题、图片和完整诊断上下文。候选标题与详情标题冲突时以详情为准并记录数据不一致提示。
3. Tool 在解析出商品归属后，profile、performance、同款竞品 V2 和商品库行动点全部使用同一个返回 `loginId`；Workflow 不再分别调用 `alibaba.1688.get.offer.data`、`get_bindlist`、`get_same_offer_competition` 或 `get_offer_diagnosis_actions`。用户可见文案不得展示内部调度顺序。
4. profile 和 performance 是基础门禁：聚合调用失败、任一分区为空或无法验证时，标注“数据暂不可用”并跳过当前商品，该商品不得进入 Step 3 或 Step 4。若列表中所有商品都失败，立即终止流程且不交接一键优化任务。同款和商品库分别分类为 `success / no_data / unauthorized / tool_failed`：只有 `success` 可参与报告或行动点，其余状态隐藏对应增强区块并保留在内部执行清单。

> 若待诊断列表只有 1 个商品（单选或手动输入），行为与单商品模式完全一致。
>
> Step 0 表格中的隐藏 `loginId` 不得透传给聚合 Tool；正式诊断与行动交接使用聚合 Tool 返回的 `itemId -> loginId` 映射。商品体检不直接执行写操作，确认后的交接由 `1688-item-one-click` 重新校验商品归属。

### Step 3: 输出完整报告（逐商品输出）

interactive 的组件交付模式（workflow 返回 `delivery=component`）下，单商品基础诊断经 `DATA-HIDDEN-PRODUCT-DIAGNOSIS-PRODUCT` 围栏内的 `product_result` 区块直出组件，不进入 `merchant_report`；同款商品分析仍完整进入主对话的 `<same_offer_markdown>`。`show_interaction(type="open_tab")` 返回明确失败或抛出异常时仍继续发送全部区块，但必须返回 `delivery=markdown` 让主对话输出完整报告；只有组件调用未返回明确失败且全部区块发送成功时才返回 `delivery=component`。区块中途发送失败时，workflow 仍尝试发送 `report_completed` 关闭 loading，再执行完整 Markdown 降级。automatic 是唯一例外：不调用组件、不发送任何隐藏区块，固定 `delivery=markdown`，将所有成功商品的完整报告一次性写入 `merchant_report` 并直接交付。automatic 的 Top 5 有部分商品未完成时，`merchant_report` 末尾必须追加“未完成商品”，只列商品 ID 和商家可理解的安全原因；不得静默少件。执行清单必须记录 `selectedCount`、`completed`、`failed` 和逐商品 `products` 状态。

仅对 Step 2 中通过基础门禁的商品，按照 `references/report-template-simple.md` 模板生成诊断报告；生成每份报告时都必须按该商品的 `itemId` 使用聚合 Tool 返回的 `loginId`。聚合调用失败、profile 或 performance 为空或无法验证的商品都不得生成成功报告。`delivery=markdown` 时所有成功商品报告先在 workflow 内汇总并净化，再通过唯一的 `merchant_report` 一次性完整交付，禁止把基础报告拆成普通 `emit` 文本。

每个商品使用独立标题和段落，禁止用编号列表嵌套整份报告；所有 Markdown 表格左对齐放在对应标题下。基础报告之后按以下顺序追加：

1. 同款查询状态为 `success` 且返回有效 `v2Comparison` 时，在主对话正文完整展示“同款商品分析”：直接依次输出所有有数据的商品素材、经营表现、流量来源、服务保障、口碑评价和热卖 SKU，不展示标杆来源或类目校验说明。禁止使用 `notice` 总结卡、重复的核心摘要表或行数截断。二级类目一致性只用于内部行动准入；所有已返回事实维度仍完整展示，类目不一致时不使用模型生成的跨类目“可借鉴经验”，不据此生成行动点。
2. 商品库查询精确命中当前 `offer_id` 且含非空 `actions` 时，把原始行动点并入下游一键优化任务清单；不再单独展示"商品库明细建议"区块，也不展示 `aiAnalysis` 或 `statusTag`。
3. 将基础诊断 `recommendations` 与同款 `lessonsToLearn` 规范化、去重，在全部同款表格之后统一输出一次“综合优化建议”；不得在基础报告前部保留“优化建议”，也不得再单独输出“可借鉴方向”。
4. 任一增强数据为空、未命中或调用失败时，完全隐藏对应区块，不输出占位文案，不影响基础报告或另一条可用增强数据。

多商品时按序号标注：

```
### 商品 1/3

**商品**：[商品名称]

**商品 ID**：[商品ID]

**货盘定位**：【货盘定位】（辅助解释，如新品；没有则省略括号）

**选择原因**：[为什么优化，用数据说话]

#### 同款商品分析

[按有数据维度展示表格]

#### 综合优化建议

- [基础建议与同款借鉴方向合并去重]

### 商品 2/3
[同样结构]
```

**要求**：

1. **货盘定位** - 标注主要定位；存在“新品”等辅助解释时使用【主要定位】（辅助解释），没有辅助解释时省略括号
2. **选择原因** - 1-2 句话说明核心问题，必须引用具体数据
3. **分层定位**（条件展示）- 仅当商品来自 Step 0.5 时展示，格式见 `references/report-template-simple.md`；不为此额外调用 `score_and_select`
4. **综合优化建议** - 每个商品把基础建议与同款借鉴方向合并去重后统一后置，要具体可执行
5. **优先级** - 违规问题 > 流量问题 > 转化问题 > 优化建议

### Step 4: 报告末尾操作提示与下一轮交接

至少有一个商品诊断成功时，interactive 的 workflow 只读本地定时任务状态并返回报告交付结果、后续操作和一键优化精确任务清单，不调用任何 notice、card 或其他 skill；automatic 跳过定时任务查询与入口，只返回完整 Markdown 报告和一键优化精确任务清单。Agent 必须按 workflow 返回的交付模式执行：`delivery=component` 时基础诊断、行动点和定时任务入口均由组件及 `footer_actions` 交付，主对话只原样输出完整同款分析；`delivery=markdown` 时把包含行动点文字的完整 `merchant_report` 原样输出到主对话，automatic 不附定时任务入口。输出后立即结束当前回复：

1. 原商品诊断有明确方向的标题/主图行动、商品库精确命中的原始 `actions` 与同二级类目竞品 V2 的明确候选行动按同一 `(offer_id, canonicalAction)` 合并；没有明确方向时不得默认补标题优化。未映射行动点仅保留在报告建议中、不交接；价格/定价/调价、广告预算、认证和效果预测始终不进入任务清单
2. 构造 `{source:"1688-product-analysis", tasks:[...]}`；每条 task 固定包含 `itemId`、标题、归属 `loginId`、one-click `opKey` 和行动名称，精确表达一个商品对应一个行动点
3. interactive 的 workflow 通过 `check_auto_diagnosis_schedule` 确定报告末尾是否保留定时任务提示，只有 `enabled=true` 才算已配置，`enabled=false` 仍保留设置入口，查询失败时隐藏该提示；automatic 跳过查询且不展示设置定时任务。Agent 禁止调用 `Schedule(action="list")` 或重新判断
4. 用户下一条消息明确表达一键优化意图（包括组件按钮按商品和优化项回填的普通文本，或手动回复“进入一键优化”）且 `tasks` 非空时，复制当前 workflow 返回的 `<one_click_handoff_json>` 原始 JSON 对象，将其 JSON.stringify 后的完整字符串直接作为 Workflow args 调用一次 `1688-item-one-click`。禁止依赖 `reportId` 或会话外存储，禁止先用用户原话试探调用，禁止包装成 query/params、空参数调用、增删任务、重新组合或重复调用；无法取得完整 handoff JSON 时提示用户重新发起商品诊断，不得猜测任务
5. 用户下一条消息要求导出商品体检报告 Markdown 文件时（手动输入的请求，消息中不含缓存文件路径），禁止再次调用 workflow、商品查询或除 `Write` 外的任何工具；直接读取最近一次成功 workflow 返回的 `<export_report_markdown>`，只调用一次 `Write` 写入相对路径 `商品体检报告.md`，文件内容必须完整复制标签内 Markdown。Write 成功后 Newton 会自动展示文件卡，不得调用 `present_files`；上下文已出现该文件的 Write 成功结果时必须停止调用工具，只回复“已导出商品体检报告.md。”。组件降级时可回退读取 `<merchant_report>`；上下文中无法取得标签全文（如已被压缩成只剩标签名提及）时视为丢失，禁止搜索文件系统、读取或转换任何 JSON 文件或旧报告、重建或编造报告，直接提示用户重新发起商品体检后再导出。禁止调用 Bash、Glob、Read、Edit、`schedule_task`、`show_interaction` 或处理其他 footer action，禁止在对话中重复正文，禁止生成 JSON、中间文件或第二个附件
6. 一键优化按精确 task 构造自己的 `one_click_task_list`，由该卡逐项确认“执行/跳过”，再执行归属校验和写操作；不得直接调用 `1688-item-image-optimizer` 或 `1688-item-title-optimizer`
7. 用户下一条消息明确表达设置商品自动体检定时任务的意图（包括手动回复“设置定时任务”或组件按钮完整 prompt 回填）后，才进入原生定时任务流程
8. interactive 组件模式下，「一键优化商品」必须是可用操作中的最高优先级（`order=1`），使用独立主按钮样式（`variant=primary`）。`footer_actions.ONE_CLICK_OPTIMIZE` 同时返回 `products` 和固定模板 prompt：`请帮我一键优化以下商品：${offers} 请逐项让我确认后再执行。`，其中 `${offers}` 只由 workflow 使用校验后的商品 ID 拼接，前端必须原样回填 `prompt`，不得二次拼接或改写。`footer_actions.EXPORT_REPORT` 返回两种 prompt：报告缓存预写成功时（默认），prompt 携带缓存文件名和位置（不暴露绝对路径）：`请将刚才的商品体检报告导出为一个 Markdown 文件，文件名固定为“商品体检报告.md”。全文已缓存在当前工作目录，Read 后调用一次 Write 原样写入`，缓存默认写在 Agent 当前工作目录，写不进去时回退 skill 根目录（prompt 措辞随之变为“本 skill 根目录（cli.py 所在目录）”），缓存文件名与多份取舍规则见第 21 条；缓存预写失败时回退为不带缓存信息的简短 prompt：`请将刚才的商品体检报告导出为一个 Markdown 文件，文件名固定为“商品体检报告.md”。`，由主 Agent 按第 21 条从 workflow 返回的 `<export_report_markdown>` 取内容；`footer_actions.SCHEDULE_TASK` 返回 prompt：`请帮我设置“1688商品自动体检”定时任务，任务执行内容固定为：“自动按优先级挑出【最该优化的 5 个商品】，完成诊断后直接在对话中输出完整报告和每个商品的优化建议”。请先询问执行频率和时间，再打开定时任务设置让我确认；不要自动修改商品。`。三个 footer action 的 prompt 均由前端原样回填，不得二次拼接或改写。automatic 不返回 footer action；主 Agent 识别一键优化意图后使用当前 workflow 返回的 `<one_click_handoff_json>` 调用一次 `1688-item-one-click`。前端不得拼 Skill 名、Workflow 名、结构化标签、`loginId` 或 `reportId`

> ⚠️ **interactive 的报告交付是硬门禁。只有 interactive 的 `show_interaction(type="open_tab")` 未返回明确失败且区块流全部发送成功时，才不得在主对话重复基础诊断；组件唤起失败不阻断区块流，但必须让下一条 assistant 内容先输出完整 Markdown 报告。任一区块发送失败时同样降级完整 Markdown。automatic 直接以完整 Markdown 交付，不受组件唤起或区块流成功条件约束。对应内容最后一个字符输出之前不得发起任何工具调用。**
>
> **独立选品场景**（Step 0.5 命中但用户只是要"选品清单"、不接诊断）：按 `products >=2 / =1 / =0` 规则分别展示交互表格、独立选品 Markdown 或无候选提示后结束，不触发一键优化交接，不输出优化项。

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **执行失败门禁**：`alibaba.1688.get.item.diagnosis.context` 返回失败，或 profile、performance 任一为空或无法验证时，该商品不得生成诊断报告、不得进入一键优化任务清单；多选时继续其他商品，全部失败时终止且不交接行动点
3. **终止型错误不重试**：无权限、商品不归属当前账号、参数非法、数据为空时立即停止当前命令/商品，禁止智能修改参数重试，禁止换商品伪装完成
4. **搜索失败不是零结果**：`search_offer_by_keyword success=false` 时按失败终止本次搜索；只有 `success=true` 且结果为空才能进入成功零结果处理
5. **再根据关键词追加引导**：

| markdown 关键词                              | Agent 额外动作                                                               |
| --------------------------------------------- | ------------------------------------------------------------------------------ |
| "AK 未配置"                                  | 提示用户在 OpenClaw 配置 `ALI_1688_AK`，或检查 `~/.openclaw/openclaw.json`  |
| "offer_id 不能为空" / "modules 取值非法"     | 提示用户使用合法的参数值并终止，不自动改参重试                               |
| "dateType 取值非法" / "device 取值非法"      | 提示用户使用合法的参数值                                                     |
| "无权限" / "商品不归属当前账号"              | 提示用户确认商品归属并终止，不更换商品                                       |
| "异常商品数据为空" / "商品数据为空" / "未获取到商品数据" | 提示用户确认账号是否已沉淀有效数据并终止，不更换商品                |
| "shop_total JSON 解析错误"                   | 提示用户该参数由 `get_shop_data` 返回值直接传入，无需手动构造               |
| "网络异常，已重试" / "请求被限流"          | 建议用户等待 1-2 分钟后重试                                                  |
| "未检测到可用的 Python 3 运行环境"           | 提示用户安装 Python 3 并加入 PATH（Windows 上 `python3` 不存在，需有 `python` 或 `py -3`），不改用其他命令重试 |
| 其他                                         | 仅输出 markdown 即可                                                         |

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量                  | 默认值                  | 说明                                                                |
| --------------------- | ----------------------- | ------------------------------------------------------------------- |
| `SKILL_NAME`          | `1688-product-analysis` | skill 名称                                                          |
| `SKILL_VERSION`       | `1.0.0`                 | skill 版本号                                                        |
| `SKILL_CHANNEL`       | `clawhubai`               | 发布渠道                                                            |
| `ALI_1688_AK`         | 由平台 OpenClaw 注入    | 1688 开放平台 AK，CLI 自动解析卖家身份并注入 `__userId__`           |
| `OPENCLAW_CONFIG_DIR` | `~/.openclaw`           | OpenClaw 配置文件目录（AK 兜底读取来源）                            |

> 已存在的系统环境变量优先级高于 `.env`，CI/CD 注入的变量不会被覆盖。

## 注意事项

- 核心诊断商品 ID 通过 `alibaba.1688.get.item.diagnosis.context --item_id` 传入；兼容单接口命令仍使用 `--offer_id`
- 报告中每一项数据都必须能追溯到 CLI 的真实输出
- 建议要具体可执行，结合 1688 平台特点和商家实际需求
- **异常发现入口**：找问题品并诊断、纯诊断 / 异常查看分支使用 `multi_shop_product_analysis` 命令，内部自动通过 `NEWTON_SHOP_LOGIN_ID` 参数指定店铺，Agent 只需传 `--shop_name`，不接触 loginId；正向选品分支禁止调用该命令
- **兼容/自由查询场景**：Agent 单独调用 `get_abnormal_offers` 或 `alibaba.1688.get.offer.data` 查询非当前 AK 默认店铺时，仍可手动传入 `--NEWTON_SHOP_LOGIN_ID`（值为 `get_bindlist` 返回的对应店铺 `loginId`）；核心 Workflow 禁止使用该路径
- 绑定店铺汇总结果中每个商品继续标明 `shop_name` 和隐藏 `loginId`，但正式诊断只传 `itemId`；报告、行动选择和下游调用使用聚合 Tool 返回的权威 `itemId -> loginId` 映射
- 无绑定店铺时，`multi_shop_product_analysis` 不传 `login_id`，使用当前登录态执行，行为与单店模式一致；该降级结果缺少 `loginId` 属于默认店铺语义，不阻断下游写操作
- **评分分层候选（`c_grade_candidates`）不含店铺归属信息**，与其他诊断来源一样只传 `itemId` 给聚合 Tool，由 Tool 解析并返回归属
- 绑定店铺来源、默认店铺降级结果、直接 ID、评分候选、关键词搜索和手工输入统一由聚合 Tool 执行“默认店铺优先、明确商品 miss/空/归属错时绑定店铺兜底”；商品体检交接给 one-click 后，由 one-click 再次校验商品归属并决定实际执行店铺
- 核心 Workflow 对每个商品只调用一次聚合 Tool；profile 与 performance 任一失败或为空即失败关闭，同款和行动点按四态独立降级
