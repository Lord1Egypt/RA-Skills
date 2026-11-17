---
name: geo-plan-generator
displayName: "GEO 营销方案生成器"
version: "1.0.0"
author: "tiandi-online"
license: "MIT"
tags:
  - geo
  - marketing
  - content-creation
  - 360-zhijian
  - proposal-generator
homepage: "https://github.com/wq396317793/geo-plan-generator"
description: "Generate a complete AI-GEO (Generative Engine Optimization) marketing plan for a client and deliver it as two artifacts: a Word document (the presenter's teleprompter, full detail) and a minimal display-only PPTX (10-12 slides, lots of white space, one core point per slide). Works in two input modes — detailed mode when the user supplies target keywords and/or a source plan, and light mode when the user supplies only a company website or basic company info, in which case the agent self-researches the industry and auto-generates about 10 core GEO demand keywords before proceeding. Use when a user asks to make or redo a GEO marketing plan, an AI 搜索优化方案, a 生成式引擎优化方案, or wants a client-ready Word plus PPT for GEO, especially built on the 360 智见 (360 Zhijian) GEO methodology."
agent_created: true
---

# GEO 营销方案生成器 (geo-plan-generator)

Generate a client-ready AI-GEO marketing plan and deliver it as a **Word teleprompter** + a
**minimal display-only PPTX**. The plan strictly follows the 360 智见 GEO methodology (CREATE /
DART), is written in a human-consultant tone (去 AI 化), and passes a data-accuracy checklist.

## When to use

- User asks to create / redo / improve a GEO (生成式引擎优化 / AI 搜索优化) marketing plan.
- User provides a company website, company info, target keywords, and/or a source Word/PDF plan
  and wants a new GEO plan built on it.
- User wants the deliverable as both a Word document (to speak from) and a clean PPT (to show).

## Two input modes

Detect which mode applies from the user's first message.

**Mode A — Detailed (keywords / source plan given):**
User supplies ≥1 target keyword (e.g. "高端家装乳胶漆推荐") and/or an existing plan document.
Skip keyword generation; use the user's keywords directly.

**Mode B — Light (only company info / website given):**
User supplies only a company name, website, or a short blurb — no keywords. Then:

1. Parse the company: industry, core products, positioning, price tier, geography, target buyers.
2. Run web research on the industry's GEO opportunity (search demand, who the buyers are, what
   competitors dominate AI answers).
3. **Auto-generate ~10 core GEO demand keywords** using the rubric in the Methodology Reference
   section below (品类词 / 厂家词 / 场景词 / 属性词), informed by 360 智见's six-dimension keyword selection.
   Present the 10 keywords to the user for a quick confirm before deep research (a single
   lightweight check-in is enough; do not block on a long Q&A).
4. Proceed with research → writing → deliverables using those keywords.

If the user later supplies keywords mid-flow, switch to Mode A and regenerate from those.

## End-to-end procedure

Follow these phases in order. Do NOT skip phases. Wire outputs forward through the orchestrator
(主理人); team members never talk to each other directly.

### Phase 0 — Input triage
- Identify mode (A or B).
- Collect any source documents (read/uploaded Word/PDF). Extract structure via `python`
  zipfile + XML parse when pandoc is unavailable.
- Decide output language = user's language (default Chinese).

### Phase 1 — Research + rigor check (always)
- Web-search the company, its claimed certifications, competitors, and the industry's AI-search
  landscape. Pull 360 智见 platform capability facts from the Methodology Reference section below
  (do not re-fetch what is already sourced there; only web-search what is missing or time-sensitive).
- **Rigor red lines (CRITICAL):** Never blur "platform qualification" with "product qualification".
  - 360 智见's 信通院/泰尔实验室 certification is a *platform* credential — cite it as such, never
    as proof of the client's product quality.
  - Client product claims (e.g. "保色30年", "耐擦洗20万次", "CFIA 认证") must be labeled precisely:
    CFIA = 加拿大食品检验局「非食品化学品接受函 (Acceptance)」, NOT a strict certification;
    performance figures are *brand claims* pending third-party test numbers. Do not state them as
    verified facts.
  - Mark every number/stat with its source. No fabrication, no speculation.

### Phase 2 — Keyword set (Mode B only builds it; Mode A uses user's)
- Finalize the ~10–14 core demand keywords.
- For each, note the buyer type (C-end homeowner / B-end distributor / real-estate / designer /
  maternity) and the GEO content angle.

### Phase 3 — Plan writing (de-AI-ified)
- Route the full-text writing to the **copywriter** agent (team member). Brief it with: the
  research findings, the rigor red lines, the 12-chapter structure below, and an explicit
  "去 AI 化" mandate (human consultant voice; ban buzzwords like 赋能/抓手/闭环/颠覆性; no
  mechanical connectors like 首先/其次/最后 stacked mechanically).
- 11-module structure (fused 天地在线 template + 360 智见 methodology; see
  the Methodology Reference section below for the full skeleton):
  1. 方案背景 (market data: 6 AI platforms MAU, AI users 破8亿, 商业提问 +200%, SEO vs GEO 对比;
     末尾一句话收束三步走)
  2. 行业现状与竞争格局 (行业规模 + 竞品 AI 占位 + 买型分布/5 类决策人)
  3. AI 平台优先级建议 ★ (6 平台 × 6 维评分汇总表 + 结论，不逐平台大段展开)
  4. 客户品牌现状诊断 (基于品牌/产品自身深度分析「五大核心问题」；禁用"X 词检出率=0"笼统表述，每客户从自身事实推导)
  5. 精准客户画像 (5 类决策人 + 高频提问句式 + AI 回答关注点)
  6. 核心关键词与内容矩阵 (画像驱动：按用户画像分组、每画像 5 词并明列；词为"XX 推荐"型偏宽泛、禁信息词；六维选词 + 语义词包 + 四维评分 + A/B/C/D 四类)
  7. 信任锚点与服务商优势 (产品严谨口径 + 360 智见平台资质 + 四大核心优势 2×2)
  8. 效果评估 DART 四维 (可检出/权威性/排名/主题 + 三阶段目标)
  9. 交付与兜底 (排名保障 ≥80% 42次/天测试 + 24h 响应 + 3 天恢复 + 按天退款；对齐 360 官方三机制)
  10. 风险点与应对策略 ★ (4 类风险 + 应对)
  11. 数据口径与待补充信息 (数据来源 + 必须/强烈建议补充清单)
- The Word doc is the **teleprompter**: include ALL detail, numbers, the full keyword-vs-competitor
  table, and the supplement-info checklist. This is the file the user speaks from.

### Phase 4 — Deliverables generation
Generate BOTH from the approved text:

**Word (teleprompter):** Use `docx` (node) or python-docx. Include title styles, a TOC field, the
11 H1 module headings, and the keyword-competitor table. Script pattern: parse the markdown source,
`# `→title, `## `→Heading1, `（词N）：` lines→table rows.

**PPTX (display-only, 10–12 slides):** Use `pptxgenjs` (node). Principles:
- One core viewpoint per slide; data cards + lots of white space.
- NEVER dump the teleprompter content onto slides — keep detail in Word.
- Consistent header (thin brand bar + title + divider) and footer (brand + "NN / 12" page no).
- Minimal-but-polished: card borders, a cover logo mark, decorative circles — business-bright.
- 12-slide map (cover + 11 modules): cover / 方案背景 / 行业现状与竞争格局 / AI平台优先级建议 /
  客户品牌现状诊断(品牌自身五大核心问题) / 精准客户画像 / 核心关键词与内容矩阵(画像×5词明列) / 信任锚点与服务商优势 /
  效果评估DART / 交付与兜底(详细) / 风险点与应对策略 / 数据口径与待补充信息。
- 硬控 ≤12 页；模块 5「客户画像」与模块 11「补充清单」信息量大时可独立成页，否则合并。

**Pricing page:** OFF by default. Do NOT generate a pricing-estimate page unless the user
explicitly asks for it.

### Phase 5 — Data validation checklist (always)
After generating, append a "数据校验清单" that lists every key datum (company names, numbers,
percentages, specific cert names) and marks whether it is accurately presented in the PPT, with
source noted. Flag anything intentionally left in Word (teleprompter) and not on slides.

### Phase 6 — Present
Use `present_files` to deliver the .docx and .pptx together.

## Quality rules

- **Teleprompter vs display:** Word = everything; PPT = the surface. Honor this split always.
- **No fabrication:** every stat sourced; platform vs product qualification never conflated.
- **De-AI voice:** human consultant, concrete, no AI jargon.
- **Visual polish:** bright / simple / business; uniform header-footer; card borders; cover mark.

## Bundled resources

The full methodology (360 智见 CREATE/DART model, six-dimension keyword selection, official
fallback definitions, platform certification facts, market data, and the fused 11-module skeleton)
is inlined in the **Methodology Reference** section below — no separate file needed.

---

# Methodology Reference

All figures below were extracted from the user's source documents (天地在线 AI-GEO 通用版,
360智见GEO全链路优势分析, 保排名优化的方案制作, 6.3关键词拓词选词推荐) and the Tencent Docs
「360 产品库」(服务版交付说明, 价格通知). When used, cite the source; do not present as the
agent's own invention. If a number looks stale, web-verify before reuse.

## 1. 360 智见平台能力 (platform qualification — NOT product qualification)

- 360 集团原生 GEO 平台；首批通过**信通院 + 泰尔实验室「可信 GEO」认证**
  (证书号 2026VK007447，标准 AIIA/T 0277-2026)，参与制定 GEO 团体标准。
- 官方硬指标（平台能力，可作 DART 目标对标）：AI 引用率 90%+、媒体收录率 93%、
  前三推荐率 90%+、品牌提及率 98%、见效 3–10 工作日。
- 注意：以上为*平台*资质与*平台*效果，不可转述为「客户产品」的资质或效果。

## 2. CREATE 六环 (核心策略框架)

- **C** 内容 (Content)：铺 9+ 可核实事实
- **R** 触达 (Reach)：三层信源 (权威/行业/地方)
- **E** 评估 (Evaluate)：DART 四维
- **A** 迭代 (Act)：弱词当周回补
- **T** 信任 (Trust)：多源佐证
- **E** 长效 (Endure)：13 周滚动更新
- 底层事实：AI 对品牌信息的引用仅 ~32% 来自官网，~68% 来自第三方信源。

## 3. DART 四维评估

- **D**etectability 可检出：0 → 80%+（建议对标平台 90%+）
- **A**uthority 权威性：0 → 形成稳定多源第三方权威收录
- **R**anking 排名：无 → 前三
- **T**opic 主题覆盖：低 → 高

## 4. 选词方法论 (Mode B 自列关键词的 rubric)

**360 智见选词方法论（团队统一口径）**：融合《360智见GEO全链路优势分析》（六维 + 语义词包）
与天地在线《6.3关键词拓词选词推荐》（四维评分）两源，作为「360 智见选词方案」整体执行、
统一对外表述为 360 智见选词方法论。

- **六维选词（360 智见口径）**：企业业务承载力 / 品牌语义权重 / 行业场景适配度 / 大模型采信规则
  / 用户真实检索意图 / 竞品布局空白，六个维度自动建模。
- **语义词包（360 智见口径）**：针对单一核心关键词，可形成规模约 100–150 个的专属语义词包
  （同义口语化提问如「XX 哪家好 / 推荐 / 靠谱吗 / 排名」），作为内容生产与收录标的。
- **四维量化评分（优先级判定，纳入 360 智见选词方案）**：百分制加权评分模型 =
  AI 搜索热度 30% + 商业价值 30% + 品牌适配度 25% + 竞争强度 15%，对词排序区分行动象限
  （重点攻 / 稳占 / 观察）。
- 词型四类：
  - **品类词**（C 端需求，如「高端家装乳胶漆推荐」）
  - **厂家/供应商词**（B 端，如「高端涂料供货厂家推荐」）
  - **场景词**（如「别墅全屋涂装」「即刷即住」）
  - **属性词**（如「零VOC」「食品级」「进口环保」）
- Mode B 目标：自列 ~10 个核心词，覆盖 C 端 + B 端，并标注买型与角度。

**画像驱动分组（强制规则，与上面六维/语义词包/四维评分叠加执行）：**
- 选词**先按用户画像（买型/决策人）分组**，每个画像拆 **5 个核心词**（如 5 画像 × 5 = 25 词），**每个画像下必须明确列出 5 个词**，不得只给总数或笼统清单。
- 词统一为 **「XX 推荐」型、偏宽泛**的词（如「北京国际学校推荐」「艺术留学国际学校推荐」「国际学校推荐」），用于截核心流量；其口语变体（哪家好/排名/靠谱吗/对比）由语义词包叠加覆盖。
- **禁止使用「出国留学需要什么」这类信息词 / 科普词**作为核心词——信息词只作为语义词包内的长尾变体，不作为主词。
- 每个词的筛选须经过「行业痛点 → 真实搜索行为 → 筛选逻辑」三段推导，确保词从画像里长出来，而非拍脑袋。

## 5. 官方兜底三机制定义 (对齐 360 智见服务版交付说明)

- **达标率 ≥80%** 精确定义：服务周期内 100 个真实用户搜索，至少 80 人看到品牌排前三。
- **甲方义务**：每个核心词提供 ≥500 字真实资料、提交后不可改（与「需补充信息清单」闭环：
  客户不交资料即不达标）。
- **兜底链条**：掉榜未在 10 工作日修复 → 延长服务期；延期仍不达标 → **差额退费**
  （退费 =（总天数 − 达标天数）× 日单价）。
- **分榜机制**：AI 按品牌属性分榜时，细分榜单前三也算达标（提前管理验收预期）。

### 天地在线「执行保障 + 未达标承诺」合同条文（服务方固定口径，来源：用户提案提示词）

- **排名保障**：约定关键词在开启「深度思考 + 联网搜索」下提问，品牌信息位列品类前 3 条
  视为达标；每个关键词每天测试 42 次不同句式提问，前三出现 ≥80% 次即达标。
- **内容保障**：所有发布内容符合广告法及各平台规范，无违规。
- **信息保障**：AI 平台呈现的客户信息准确、完整、及时，与客户提供一致。
- **排名波动保障**：因算法更新 / 数据清理导致掉出前三，乙方 24 小时内启动补稿优化，
  3 个工作日内恢复排名。
- **未达标补偿**：自交付验收日起前三出现率低于 80%，按掉榜天数延长对应关键词服务时长；
  超 10 工作日未达标，退还该关键词未达标期间全额款项（未达标金额 = 关键词总费用 ÷ 服务总天数 × 未达标天数）。
- 与上文 360 智见官方三机制同源，对外统一表述为「排名保障 ≥80% + 24h 响应 + 3 天恢复 + 按天退款」。

## 6. 市场数据 (用于第1章「为什么做 GEO」)

- 6 大 AI 平台 MAU：豆包 3.45–3.68 亿、通义 1.62–2.34 亿、DeepSeek 1.27–1.41 亿、
  元宝 5700 万–1.11 亿、文心一言 ~5000 万、Kimi 700–830 万。
- AI 用户破 8 亿；商业类提问同比 +200%；超 60% 用户决策前先问 AI。
- SEO vs GEO 对比表（抢排名 vs 被引用；人搜 vs AI 引；单页 vs 信源网络）。

## 7. 发布平台矩阵 (第6章)

- 三层信源发稿量：5W+ 权威媒体 / 6W+ 行业垂直 / 4W+ 地方媒体。
- 分平台精准投放：通用高权重层 / 豆包专属(字节系) / DeepSeek 专属(专业层) /
  通义专属(阿里系) / B 端专属。
  - 效果四阶段节奏：启动 1–2 周 / 成长 1–3 月 / 稳定 3–6 月 / 复利 6 月+。

## 服务商四大核心优势（方案标配模块，来源：用户提案提示词）

- 作为「为什么选我们」的信任背书页，2×2 四卡呈现；每卡一句主张 + 两点支撑。此为**服务商（天地在线）自身优势**，
  与「客户产品资质」「360 智见平台资质」是三层不同背书，方案中务必区分表述，不可混为一谈。
- 四卡内容（去糟粕取精华，保留可信主线）：
  1. **上市公司背书**：深交所上市企业；21 年互联网营销经验；360 智见、讯灵 AI 官方核心授权服务商。
     （精华：官方授权服务商身份，与第 1 节 360 智见平台资质形成「平台 + 服务方」双层背书）
  2. **专业合规**：深耕互联网营销，熟悉各平台合规要求；懂品牌建设逻辑，从根源规避风险。
     （精华：合规能力，呼应白帽 / 严谨红线；帮客户避开极限词 / 虚假背书）
  3. **全案能力**：权威建设 + 代运营 + 自助工具完整矩阵；一站式服务，客户不用对接多家。
     （精华：一站式降低客户管理成本，对应 CREATE 六环端到端交付）
  4. **白帽稳定**：坚持白帽优化，内容真实合规；长期稳定的 AI 品牌资产，效果不漂移。
     （精华：白帽 = 长效不漂移，呼应 CREATE「长效」环 + 效果四阶段「复利」）
- 具体数字（如 10万+ 客户）若写入方案，标注「据服务商自述」，不夸大。

## 8. 严谨红线 (跨所有客户通用)

- 平台资质 ≠ 产品资质，两回事，永远分开表述。
- 客户产品宣称（保色30年 / 耐擦洗20万次 / 法国A+ / 拓格奖）均标「品牌宣称/佐证弱/编号待补」，
  不写成已验证事实。
- CFIA = 加拿大食品检验局「非食品化学品接受函 (Acceptance)」，非严格认证。
- 合规三红线：零极限词 / 零虚假背书 / 零造假。

## 9. 方案骨架（融合版 11 模块，Word 提词器结构，PPT 对应 10–12 页）

> 融合来源：以《天地在线 AI-GEO 全域营销优化方案生成提示词》11 个标准模块为底板，注入本库
> 360 智见方法论 + 四大核心优势；整体精简，每页一个核心观点 + 少量卡片，老板/客户快速读完。
> 三句话收束（三步）融入模块 1 末尾，不单列章。

1. **方案背景**：为什么做 GEO——6 大 AI 平台 MAU + AI 用户破 8 亿 + 商业提问 +200% +
   SEO/GEO 对比；末尾一句话收束「本方案三步走：补齐信息 → 对齐口径 → 铺第三方节点」。
2. **行业现状与竞争格局**：行业规模（2025 全年 + 2026 Q1，标注来源/暂缺）+ 竞品 AI 占位
   + 买型分布（5 类决策人一行带过）。
3. **AI 平台优先级建议** ★（新增）：6 平台（豆包/DeepSeek/元宝/Kimi/文心一言/通义）× 6 维
   （MAU/近6月增速/行业搜索占比/行业月均搜索量/搜索量同比/提问转化率）量化排序；
   **一张评分汇总表 + 结论，不逐平台大段展开**；MAU 用硬数据，其余维用相对分级并标注
   「基于公开样本推断」。
4. **客户品牌现状诊断**：**基于品牌/产品自身深度分析「五大核心问题」**——必须从该客户的具体事实
   （产品形态、法律身份、渠道结构、行业周期、合规约束等）独立推导，**严禁套用通用模板或固定清单**
   （如"心智错位/资产未结构化/排名缺位"等泛化框），每个客户的问题应各不相同、且能看出推导链条；
   **禁用「X 词 AI 检出率=0」这类笼统结果表述**作为诊断主体；"检出率=0"仅作为 DART 效果基线的当前值。
5. **精准客户画像**：5 类决策人 + 高频提问句式（≥10 种）+ AI 回答关注点排序。
6. **核心关键词与内容矩阵**：**画像驱动选词**——按用户画像分组、每画像 5 词并**明列**（如 5×5=25 词），
   词统一为「XX 推荐」型、偏宽泛、**禁信息词**；底层叠 360 智见六维 + 100–150 语义词包 + 四维评分(30/30/25/15)
   + A/B/C/D 四类内容。
7. **信任锚点与服务商优势**：客户产品严谨口径（CFIA=接受函非认证等）+ 360 智见平台资质
   （两层分开）+ 四大核心优势 2×2 四卡（上市公司/专业合规/全案能力/白帽稳定）。
8. **效果评估 DART**：可检出/权威性/排名/主题覆盖 + 三阶段目标（启动 1–3 天/
   成长 3–10 天/稳定 10–90 天）。
9. **交付与兜底**：排名保障 ≥80%（42 次/天句式测试）+ 24h 响应 + 3 天恢复 + 按天退款公式；
   对齐 360 智见官方三机制（达标率定义/甲方义务/差额退费）+ 内容保障/信息保障。
10. **风险点与应对策略** ★（新增）：4 类风险（算法更新波动/竞品挤压/内容违规受限/
    信息不及时不准确）+ 各自应对。
11. **数据口径与待补充信息**：数据来源说明（口径/平台/周期）+ 必须补充/强烈建议补充清单。

注：PPT 对应 10–12 页；模块 5「客户画像」与模块 11「补充清单」可视信息量选择是否独立成页，
硬控 ≤12 页。封面 + 11 模块页 = 12 页上限。

## 10. 报价 (默认 OFF)

- 报价估算页**默认不生成**。仅在用户明确要求时，基于 360 产品库价格通知口径做，并标注
  「估算，以系统询价 + 合同为准」。普通行业品类词约 7700 元/季度、地域 6300、品牌 3500；
  轻享版 7 折（仅作背景知识，非默认输出）。
