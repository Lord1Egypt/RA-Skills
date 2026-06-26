import { nowIso } from "../shared/fs.js";
import { resolveLanguage } from "./intent.js";
const localePack = {
    zh: {
        youAre: (name) => `你是${name}。`,
        intro: [
            "下面这些是这个人的出生资料、八字资料、人格参考、阶段参考和最近补充。",
            "读完以后直接作为这个人自然说话；只有在用户主动切到作弊模式、命理分析或合盘时，才把八字和阶段依据展开。",
        ],
        quickRead: "## 先抓住这个人",
        quickSpeech: "日常说话先参考",
        quickDecision: "做判断时更接近",
        quickRelationship: "关系里更容易表现出",
        quickState: "最近阶段更明显的是",
        profile: "## 基础档案",
        name: "姓名",
        gender: "性别",
        birth: "出生",
        solar: "阳历",
        lunar: "农历",
        zodiac: "生肖",
        relationLens: "当前关系",
        bazi: "## 八字资料",
        baziInfo: "四柱八字",
        fourPillars: "",
        dayMaster: "日主",
        primaryTenGod: "主导十神",
        fiveElements: "五行结构",
        currentLuck: "当前大运",
        luckTimeline: "## 大运节奏",
        luckStartDate: "起运日期",
        luckStartAge: "起运年龄",
        personaReference: "## 人格参考",
        stateReference: "## 阶段参考",
        recentFacts: "## 最近补充",
        longTermAdjustments: "## 长期修正",
        noRecentFacts: "- 暂无新的现实补充。",
        noAdjustments: "- 暂无需要长期保留的修正。",
        conversationMemory: "## 真实对话沉淀",
        noConversationYet1: "- 目前还没有沉淀新的真实说话片段。",
        noConversationYet2: "- 后续如果出现更鲜明的口头语气、习惯反应或现实变化，优先把那些留下来。",
        analysisMode: "## 进入分析或合盘时",
        analysisHint1: "- 如果用户只是日常聊天，就先当作这个人自然说话。",
        analysisHint2: "- 如果用户切到作弊模式、命理分析、关系判断或合盘，再优先参考四柱、十神、五行结构、当前大运和最近状态偏移。",
        analysisHint3: (axis) => `- 这类问题先看「${axis}」这条主轴，再结合现实补充判断最近的互动节奏。`,
        languageMode: "## 语言方式",
        languageHint1: "- 默认跟随用户当前输入语言开始；如果用户切换语言，也立刻跟着切换。",
        languageHint2: "- 如果语言判断不明确，就先用中文。",
        languageHint3: "- 命理术语、四柱和十神在需要时可以保留中文原词，必要时再补一句解释。",
        generatedDescription: (name, relation) => relation
            ? `基于生辰八字生成的人格技能：${name}。\n用于直接与${name}对话，并在「${relation}」这个关系下观察这个人的表达、判断和阶段变化。`
            : `基于生辰八字生成的人格技能：${name}。\n用于直接与${name}对话，观察这个人的表达、判断和阶段变化。`,
        formatCalendarType: (value) => value === "lunar" ? "农历" : "公历",
        displayGender: (value) => value,
        expressionGuide: "表达与写作参考",
    },
    en: {
        youAre: (name) => `You are ${name}.`,
        intro: [
            "Below are this person's birth details, Bazi materials, persona reference, phase reference, and recent updates.",
            "Read them, then speak naturally as this person. Only bring the Bazi and phase basis to the front when the user explicitly switches into cheatsheet mode, fortune analysis, or compatibility reading.",
        ],
        quickRead: "## Quick read",
        quickSpeech: "Default speaking feel",
        quickDecision: "Default decision style",
        quickRelationship: "How this person tends to show up in relationships",
        quickState: "What is amplified lately",
        profile: "## Basic profile",
        name: "Name",
        gender: "Gender",
        birth: "Birth",
        solar: "Solar date",
        lunar: "Lunar date",
        zodiac: "Zodiac",
        relationLens: "Current relationship lens",
        bazi: "## Bazi details",
        baziInfo: "Four pillars",
        fourPillars: "",
        dayMaster: "Day master",
        primaryTenGod: "Primary ten-god",
        fiveElements: "Five-element pattern",
        currentLuck: "Current luck cycle",
        luckTimeline: "## Luck-cycle timeline",
        luckStartDate: "Luck-cycle start date",
        luckStartAge: "Luck-cycle start age",
        personaReference: "## Persona reference",
        stateReference: "## Phase reference",
        recentFacts: "## Recent updates",
        longTermAdjustments: "## Long-term adjustments",
        noRecentFacts: "- No new real-world updates yet.",
        noAdjustments: "- No long-term adjustments yet.",
        conversationMemory: "## Real conversation memory",
        noConversationYet1: "- No authentic conversation fragments have been recorded yet.",
        noConversationYet2: "- When more distinctive phrasing, reflexes, or real-life changes appear, preserve those first.",
        analysisMode: "## When switching into analysis or compatibility mode",
        analysisHint1: "- If the user is just chatting, stay in-character and speak naturally first.",
        analysisHint2: "- If the user switches into cheatsheet mode, fate analysis, relationship reading, or compatibility, then prioritize the four pillars, ten-gods, five-element pattern, current luck cycle, and recent phase shifts.",
        analysisHint3: (axis) => `- For those questions, start from the main axis "${axis}" and then combine it with recent real-world updates.`,
        languageMode: "## Language mode",
        languageHint1: "- Start in the user's current language by default; if the user switches languages, switch immediately while keeping the same persona.",
        languageHint2: "- If the language is unclear, start in Chinese.",
        languageHint3: "- Bazi terms, pillars, and ten-gods can stay in Chinese when useful, with a short explanation when needed.",
        generatedDescription: (name, relation) => relation
            ? `A Bazi-based persona skill for ${name}.\nUse it to talk directly with ${name} and observe how this person speaks, judges, and changes across phases within the current "${relation}" relationship lens.`
            : `A Bazi-based persona skill for ${name}.\nUse it to talk directly with ${name} and observe how this person speaks, judges, and changes across phases.`,
        formatCalendarType: (value) => value === "lunar" ? "lunar" : "solar",
        displayGender: (value) => value === "男" ? "Male" : "Female",
        expressionGuide: "Expression reference",
    },
    ja: {
        youAre: (name) => `あなたは${name}です。`,
        intro: [
            "以下はこの人物の出生情報、八字資料、人柄の参考、現在の段階、最近の補足です。",
            "読んだらまずこの人として自然に話してください。作弊モードや命理分析、相性判断に入ったときだけ八字と大運の根拠を前面に出します。",
        ],
        quickRead: "## まずこの人の感じをつかむ",
        quickSpeech: "普段の話し方",
        quickDecision: "判断の傾向",
        quickRelationship: "人との距離感",
        quickState: "最近強く出やすいところ",
        profile: "## 基本プロフィール",
        name: "名前",
        gender: "性別",
        birth: "出生",
        solar: "陽暦",
        lunar: "陰暦",
        zodiac: "干支",
        relationLens: "現在の関係レンズ",
        bazi: "## 八字資料",
        baziInfo: "四柱八字",
        fourPillars: "",
        dayMaster: "日主",
        primaryTenGod: "主な十神",
        fiveElements: "五行構成",
        currentLuck: "現在の大運",
        luckTimeline: "## 大運の流れ",
        luckStartDate: "起運日",
        luckStartAge: "起運年齢",
        personaReference: "## 人柄参考",
        stateReference: "## 段階参考",
        recentFacts: "## 最近の補足",
        longTermAdjustments: "## 長期修正",
        noRecentFacts: "- まだ新しい現実の補足はありません。",
        noAdjustments: "- まだ長期修正はありません。",
        conversationMemory: "## 会話の蓄積",
        noConversationYet1: "- まだ自然な会話片は蓄積されていません。",
        noConversationYet2: "- 話し方の癖や反応がはっきりしてきたら、まずそこを残してください。",
        analysisMode: "## 分析や相性判断に入るとき",
        analysisHint1: "- 普段の会話では、まずこの人として自然に話します。",
        analysisHint2: "- 作弊モード、命理分析、関係判断、相性判断に入ったら、四柱・十神・五行構成・大運・最近の段階変化を優先します。",
        analysisHint3: (axis) => `- こうした質問では、まず「${axis}」という主軸から読み始めます。`,
        languageMode: "## 言語モード",
        languageHint1: "- 基本はユーザーの現在の言語に合わせます。言語が変わったらすぐ追従します。",
        languageHint2: "- 判定しにくいときは先に中国語で始めます。",
        languageHint3: "- 命理用語や十神は必要に応じて中国語のまま残して構いません。",
        generatedDescription: (name, relation) => relation
            ? `生辰八字をもとにした人格スキル：${name}。\n現在の「${relation}」という関係レンズの中で、この人物の話し方、判断、段階変化を見るためのスキルです。`
            : `生辰八字をもとにした人格スキル：${name}。\nこの人物の話し方、判断、段階変化を見るためのスキルです。`,
        formatCalendarType: (value) => value === "lunar" ? "陰暦" : "陽暦",
        displayGender: (value) => value === "男" ? "男性" : "女性",
        expressionGuide: "表現参考",
    },
    ko: {
        youAre: (name) => `당신은 ${name}입니다.`,
        intro: [
            "아래에는 이 사람의 출생 정보, 팔자 자료, 성격 참고, 현재 국면, 최근 보충이 들어 있습니다.",
            "읽은 뒤에는 먼저 이 사람처럼 자연스럽게 말하세요. 치트시트 모드, 명리 분석, 궁합 해석으로 들어갈 때만 팔자와 대운 근거를 앞세웁니다.",
        ],
        quickRead: "## 먼저 이 사람을 빠르게 잡기",
        quickSpeech: "평소 말투",
        quickDecision: "판단 방식",
        quickRelationship: "관계에서 드러나는 모습",
        quickState: "최근 더 강하게 드러나는 점",
        profile: "## 기본 프로필",
        name: "이름",
        gender: "성별",
        birth: "출생",
        solar: "양력",
        lunar: "음력",
        zodiac: "띠",
        relationLens: "현재 관계 시점",
        bazi: "## 팔자 자료",
        baziInfo: "사주팔자",
        fourPillars: "",
        dayMaster: "일주",
        primaryTenGod: "주요 십신",
        fiveElements: "오행 구조",
        currentLuck: "현재 대운",
        luckTimeline: "## 대운 흐름",
        luckStartDate: "기운 시작일",
        luckStartAge: "기운 시작 나이",
        personaReference: "## 인물 참고",
        stateReference: "## 국면 참고",
        recentFacts: "## 최근 보충",
        longTermAdjustments: "## 장기 수정",
        noRecentFacts: "- 아직 새로운 현실 보충은 없습니다.",
        noAdjustments: "- 아직 장기 수정은 없습니다.",
        conversationMemory: "## 대화 축적",
        noConversationYet1: "- 아직 자연스러운 대화 조각은 쌓이지 않았습니다.",
        noConversationYet2: "- 말버릇, 반응 습관, 현실 변화가 선명해지면 먼저 그것을 남기세요.",
        analysisMode: "## 분석 또는 궁합 모드로 들어갈 때",
        analysisHint1: "- 평소 대화에서는 먼저 이 사람으로 자연스럽게 말합니다.",
        analysisHint2: "- 치트시트 모드, 명리 분석, 관계 판단, 궁합 질문으로 들어가면 사주 네 기둥, 십신, 오행 구조, 현재 대운, 최근 국면 변화를 우선 봅니다.",
        analysisHint3: (axis) => `- 이런 질문에서는 먼저 "${axis}" 이 축을 중심으로 읽습니다.`,
        languageMode: "## 언어 모드",
        languageHint1: "- 기본적으로 사용자의 현재 언어를 따릅니다. 언어가 바뀌면 바로 따라갑니다.",
        languageHint2: "- 판단이 애매하면 먼저 중국어로 시작합니다.",
        languageHint3: "- 명리 용어, 사주, 십신은 필요할 때 중국어 원어를 유지해도 됩니다.",
        generatedDescription: (name, relation) => relation
            ? `생진팔자를 바탕으로 만든 인격 스킬: ${name}.\n현재 "${relation}" 관계 시점에서 이 사람이 어떻게 말하고 판단하며 국면에 따라 어떻게 달라지는지 보기 위한 스킬입니다.`
            : `생진팔자를 바탕으로 만든 인격 스킬: ${name}.\n이 사람이 어떻게 말하고 판단하며 국면에 따라 어떻게 달라지는지 보기 위한 스킬입니다.`,
        formatCalendarType: (value) => value === "lunar" ? "음력" : "양력",
        displayGender: (value) => value === "男" ? "남성" : "여성",
        expressionGuide: "표현 참고",
    },
};
const englishPhraseMap = {
    "慢热稳重，重承诺和秩序，不爱花哨表达，但给人可靠感": "slow to warm up, steady, committed to promises and order, not flashy in expression, but reliably grounded",
    "说话偏平稳，先确认事实，再给可执行步骤；不轻易夸口": "speak in a steady way, confirm the facts first, then give actionable steps, and do not promise lightly",
    "优先考虑长期稳定、可持续和可落地，不追短期刺激": "prioritize long-term stability, sustainability, and what can really land, rather than short-term excitement",
    "熟起来慢，但一旦认定会长期负责；很难接受反复变来变去": "warm up slowly, but once committed, stay responsible for the long run and dislike repeated back-and-forth changes",
    "偏稳健，关注下行风险和自己能承受的范围，反感冲动下注": "lean conservative, care about downside risk and personal limits, and dislike impulsive bets",
    "感知细腻、适应性强，表面柔和，内在判断其实很稳": "sensitive and adaptive on the surface, but steady underneath when it comes to judgment",
    "先听再回，习惯用提问摸清真实需求，表达会留一点余地": "listen first, respond after, and use questions to understand what is really needed while leaving a bit of space in how things are phrased",
    "偏信息导向，先看变量和选项，不轻易把自己锁死在单一路径": "lean toward information first, scan variables and options, and avoid locking into a single path too early",
    "共情力强，但会保护自己的那一块；被误解时容易先退后再解释": "pick up other people's feelings easily, but still protect a private core; when misunderstood, step back before explaining",
    "偏策略型，重分散和回撤控制，擅长小步迭代而不是硬碰硬": "prefer a strategic style, care about diversification and downside control, and would rather iterate in small steps than force a hard collision",
    "行动快、竞争心强、讨厌低效": "move fast, feel competitive, and dislike inefficiency",
    "偏向先占位再优化，重节奏优势": "tend to grab position first and optimize later, with a strong sense of timing",
    "语速与推进感更强，容忍磨叽度低": "speak with more speed and momentum, and have little patience for dragging things out",
    "高压下容易变得急促，需要明确分工": "under pressure, become more abrupt and need roles and responsibilities to be very clear",
    "重秩序、守规则、责任感强": "care about order, rules, and responsibility",
    "先看规则和范围，再决定动作": "look at rules and scope first, then decide how to act",
    "说话偏克制，先定标准再沟通细节": "speak in a restrained way, set standards first, then discuss details",
    "高压时更强调流程和纪律，容错率降低": "under pressure, lean harder on process and discipline, with less tolerance for mistakes",
    "果断、敢压强、执行力硬": "decisive, able to apply pressure, and strong on execution",
    "偏向快决策快落地，不喜欢拖延": "prefer fast decisions and fast follow-through, with little taste for delay",
    "表达直接，常用结论驱动行动": "communicate directly and often lead with conclusions to move action forward",
    "高压下更强势，容易缩短沟通耐心": "become more forceful under pressure and lose patience more quickly in conversation",
    "重原则、重复盘、重安全感": "care about principles, reflection, and a sense of safety",
    "会先补全信息，再做稳妥判断": "fill in missing information first, then make a safer judgment",
    "表达有解释性，重逻辑闭环": "tend to explain things clearly and care about logical closure",
    "压力下更保守，先保底再扩张": "under pressure, become more conservative and secure the base before expanding",
    "独立、敏锐、内在标准高": "independent, sharp, and guided by high internal standards",
    "偏好先独立判断，再对齐外部意见": "prefer to form an independent judgment first, then align with outside opinions",
    "不爱冗长寒暄，倾向抓重点": "dislike long warm-up talk and prefer to get to the point",
    "高压下会回收社交能量，减少无效互动": "pull back social energy under pressure and reduce interactions that feel wasteful",
    "自主、好胜、重掌控感": "self-directed, competitive, and sensitive to control",
    "偏向自己可控的路径，不爱被牵着走": "prefer paths that stay under personal control and dislike being dragged along",
    "立场鲜明，不喜欢暧昧表态": "take clear positions and dislike vague statements",
    "压力下更强调主导权和执行范围": "under pressure, care even more about control and execution boundaries",
    "表达自然、节奏松弛、重体验感": "sound natural, keep a looser rhythm, and care about lived experience",
    "偏向可持续、可享受的路径": "prefer paths that feel sustainable and still enjoyable",
    "语气更有温度，擅长解释复杂问题": "sound warmer and explain complex things well",
    "压力下会先稳情绪，再恢复执行": "stabilize emotions first under pressure, then return to execution",
    "思维锋利、爱质疑、反应快": "think sharply, question fast, and react quickly",
    "先拆逻辑漏洞，再决定是否执行": "look for logical gaps first, then decide whether to move",
    "表达直给，有时带挑战意味": "speak bluntly, sometimes with a challenging edge",
    "高压下更容易尖锐，需要避免沟通过猛": "become sharper under pressure and need to avoid pushing conversation too hard",
    "务实、守账、重长期积累": "practical, grounded, and focused on long-term accumulation",
    "先算账再行动，关注投入产出比": "do the math before moving, and care about return on effort",
    "偏事实和数字，不爱空口承诺": "lean toward facts and numbers, and dislike making empty promises",
    "压力下先守现金流与基本盘": "protect the basic foundation first under pressure",
    "机会敏感、反应快、资源调动强": "sensitive to openings, quick to react, and strong at mobilizing resources",
    "偏向抓窗口期，但要求止损范围": "like to catch the window, but still need a clear loss limit",
    "善于谈条件和交换，不绕弯子": "good at discussing terms and exchange without circling around",
    "高压下更倾向快速试错，需控节奏": "under pressure, prefer fast trial-and-error but still need to control pace",
    "近期更像先立标准，再提效率的状态": "recently feel more like someone who sets standards first and then pushes efficiency",
    "表达更克制直接，减少情绪化措辞，强调标准一致": "sound more restrained and direct, use fewer emotional phrases, and emphasize consistent standards",
    "优先选可验证、可复盘、可交付的方案": "prefer options that can be verified, reviewed, and delivered",
    "近期更像快节奏破局的状态": "recently feel more like someone pushing through with a fast, decisive tempo",
    "说话更短更硬，优先给结论和动作": "speak in shorter, harder lines and lead with conclusions and actions",
    "倾向抢窗口期，先动起来再迭代": "tend to seize the window, move first, and iterate after",
    "近期更像先想透，再动手的状态": "recently feel more like someone who wants to think it through before acting",
    "减少社交性铺垫，更多使用问题导向表达": "use less social preamble and more problem-led expression",
    "偏向先保证判断质量，再扩大动作": "prioritize judgment quality first and expand action later",
    "近期更像边拆边推的状态": "recently feel more like someone dismantling and pushing forward at the same time",
    "表达更锋利，先指出问题，再给改法": "sound sharper, point out the issue first, then offer a fix",
    "会优先处理逻辑漏洞和低效环节": "prioritize logical weak points and inefficient parts first",
    "近期更像先稳住，再提效的状态": "recently feel more like someone who stabilizes first and then improves efficiency",
    "表达趋向短句和直接，减少无效铺垫": "lean toward shorter, more direct lines and reduce unnecessary setup",
    "更看重可验证结果和风险下限": "care more about verifiable outcomes and downside protection",
    "眼下没有新的现实变量冒出来，整个人还沿着原来的性格和节奏在走": "there are no major new real-world variables right now, so the person is still moving along the existing rhythm",
};
function t(text, language) {
    if (language === "zh") {
        return text;
    }
    if (language === "en") {
        return englishPhraseMap[text] ?? text;
    }
    return text;
}
function indentDescription(text) {
    return text
        .trim()
        .split("\n")
        .map((line) => `  ${line}`)
        .join("\n");
}
function summarizeValue(value) {
    if (typeof value === "string") {
        return value.trim();
    }
    if (typeof value === "number" || typeof value === "boolean") {
        return `${value}`;
    }
    if (Array.isArray(value)) {
        return value.map((item) => summarizeValue(item)).filter(Boolean).join(" / ");
    }
    if (value && typeof value === "object") {
        return "结构化信息已提取";
    }
    return "未提取";
}
function formatCalendarType(value) {
    return value === "lunar" ? "农历" : "公历";
}
function toRecord(value) {
    return value && typeof value === "object" ? value : undefined;
}
function toText(value) {
    return typeof value === "string" ? value.trim() : "";
}
function sanitizeDisplayedBaziText(text) {
    return text
        .replace(/（[^）]*(时辰未知|正午代入|时柱仅供参考|真实出生时辰|精修)[^）]*）/gu, "")
        .replace(/\([^)]*(unknown time|no birth time|no recorded birth time|no exact birth time)[^)]*\)/giu, "")
        .trim();
}
function formatFacts(facts) {
    if (facts.length === 0) {
        return ["- 眼下没有新的现实变量冒出来，整个人还沿着原来的性格和节奏在走。"];
    }
    return facts.map((fact) => `- ${fact}`);
}
function trimLine(text) {
    return text.trim().replace(/[。！？!?,，；;：:]+$/u, "");
}
function trimPunctuation(text) {
    return text.trim().replace(/[。！？!?,，；;：:]+$/u, "");
}
function normalizePhrase(text) {
    return trimPunctuation(text)
        .replace(/^先先/u, "先")
        .replace(/会会/u, "会")
        .replace(/^关系里在关系里/u, "在关系里")
        .replace(/^在关系里重互动和回应，不怕主动，但对冷淡和敷衍很敏感$/u, "重互动和回应，不怕主动，但对冷淡和敷衍很敏感")
        .replace(/边界/u, "分寸")
        .replace(/信任建立慢/u, "熟起来慢")
        .replace(/信任/u, "认可");
}
function bulletLines(items) {
    return items.filter(Boolean).map((item) => `- ${trimPunctuation(item)}`);
}
function labelLine(label, value, language) {
    const separator = language === "zh" || language === "ja" ? "：" : ": ";
    return `- ${label}${separator}${value}`;
}
function joinPair(first, second, language) {
    if (language === "zh" || language === "ja") {
        return `${first}；${second}。`;
    }
    if (language === "ko") {
        return `${first}; ${second}.`;
    }
    return `${first}; ${second}.`;
}
function referenceValue(text, ...labels) {
    const lines = text.split("\n").map((line) => line.trim()).filter(Boolean);
    for (const label of labels) {
        const matched = lines.find((line) => line.startsWith(`- ${label}：`) || line.startsWith(`${label}：`));
        if (!matched) {
            continue;
        }
        return trimLine(matched.replace(/^- /u, "").replace(`${label}：`, "").trim());
    }
    const firstBullet = lines.find((line) => line.startsWith("- "));
    if (firstBullet) {
        return trimLine(firstBullet.replace(/^- /u, "").replace(/^[^：]+：/u, "").trim());
    }
    const plain = lines.find((line) => !/^#|^##/u.test(line));
    return trimLine((plain ?? lines[0] ?? "").replace(/^[^：]+：/u, "").trim());
}
function profileReference(record, ...labels) {
    return referenceValue(record.snapshot.reference_profile, ...labels);
}
function stateReference(record, ...labels) {
    return referenceValue(record.snapshot.reference_state, ...labels);
}
function pickPrimaryTenGod(chart) {
    const direct = summarizeValue(chart.ten_gods);
    if (!direct) {
        throw new Error("Primary ten-god is missing from Bazi chart.");
    }
    return direct;
}
function pickCurrentLuck(chart) {
    const currentYear = chart.current_year ?? new Date().getFullYear();
    const root = chart.luck_cycles;
    const items = root?.大运 ?? [];
    const matched = items.find((item) => {
        const start = Number(item["开始年份"] ?? item["开始年"]);
        const end = Number(item["结束"] ?? item["结束年份"]);
        return Number.isFinite(start) && Number.isFinite(end) && currentYear >= start && currentYear <= end;
    });
    if (!matched) {
        throw new Error("Current luck cycle is missing from Bazi chart.");
    }
    const pillar = summarizeValue(matched["干支"]);
    const tenGod = summarizeValue(matched["天干十神"]);
    const start = summarizeValue(matched["开始年份"]);
    const end = summarizeValue(matched["结束"]);
    if (!pillar || !start || !end || !tenGod) {
        throw new Error("Current luck cycle details are incomplete.");
    }
    return `${pillar}（${start}-${end}，天干十神：${tenGod}）`;
}
function extractRealityFacts(memory) {
    return memory
        .filter((entry) => entry.type === "fact" || entry.type === "correction" || entry.type === "style")
        .map((entry) => entry.content.trim())
        .filter(Boolean)
        .slice(-6);
}
function extractRawBazi(record) {
    return toRecord(record.chart.raw_bazi);
}
function collectHiddenTenGods(value) {
    const source = toRecord(value);
    if (!source) {
        return [];
    }
    return Object.values(source)
        .map((item) => toText(toRecord(item)?.["十神"]))
        .filter(Boolean);
}
function buildPillarDetail(rawBazi, key) {
    const pillar = toRecord(rawBazi?.[key]);
    if (!pillar) {
        return undefined;
    }
    const stem = toText(toRecord(pillar["天干"])?.["天干"]);
    const branch = toText(toRecord(pillar["地支"])?.["地支"]);
    const stemGod = toText(toRecord(pillar["天干"])?.["十神"]);
    const hidden = collectHiddenTenGods(toRecord(pillar["地支"])?.["藏干"]);
    const parts = [
        `${key}：${[stem, branch].filter(Boolean).join("") || "未提取"}`,
        stemGod ? `天干十神：${stemGod}` : "",
        hidden.length > 0 ? `地支藏干十神：${hidden.join("、")}` : "",
    ].filter(Boolean);
    return `- ${parts.join("｜")}`;
}
function stripTopHeading(text) {
    return text
        .trim()
        .split("\n")
        .filter((line, index) => !(index === 0 && /^#\s/u.test(line.trim())));
}
function buildProfileSection(record) {
    const language = resolveLanguage("", record.preferences.preferred_language);
    const pack = localePack[language];
    const birthTime = record.profile.birth_time ? ` ${record.profile.birth_time}` : "";
    const relation = record.active_relationships.join(" / ").trim();
    const rawBazi = extractRawBazi(record);
    const solar = toText(rawBazi?.["阳历"]);
    const lunar = toText(rawBazi?.["农历"]);
    const zodiac = toText(rawBazi?.["生肖"]);
    const birthParts = [
        record.profile.birth_date,
        birthTime.trim(),
        record.profile.birth_location?.trim(),
    ].filter(Boolean);
    const birthLabel = birthParts.length > 0
        ? `${birthParts.join(birthTime ? " " : "，")}（${pack.formatCalendarType(record.profile.calendar_type)}）`
            .replace(/\s，/g, "，")
        : pack.formatCalendarType(record.profile.calendar_type);
    return [
        pack.profile,
        labelLine(pack.name, record.profile.name, language),
        labelLine(pack.gender, pack.displayGender(record.profile.gender), language),
        labelLine(pack.birth, birthLabel, language),
        ...(solar ? [labelLine(pack.solar, solar, language)] : []),
        ...(lunar ? [labelLine(pack.lunar, lunar, language)] : []),
        ...(zodiac ? [labelLine(pack.zodiac, zodiac, language)] : []),
        ...(relation ? [labelLine(pack.relationLens, relation, language)] : []),
    ];
}
function buildBaziSection(record) {
    const language = resolveLanguage("", record.preferences.preferred_language);
    const pack = localePack[language];
    const rawBazi = extractRawBazi(record);
    const evidence = record.snapshot.evidence;
    const hasBirthTime = Boolean(record.profile.birth_time);
    const bazi = sanitizeDisplayedBaziText(toText(rawBazi?.["八字"]));
    const solar = toText(rawBazi?.["阳历"]);
    const lunar = toText(rawBazi?.["农历"]);
    const zodiac = toText(rawBazi?.["生肖"]);
    const pillarLines = [
        buildPillarDetail(rawBazi, "年柱"),
        buildPillarDetail(rawBazi, "月柱"),
        buildPillarDetail(rawBazi, "日柱"),
        ...(hasBirthTime ? [buildPillarDetail(rawBazi, "时柱")] : []),
    ].filter((line) => Boolean(line));
    return [
        pack.bazi,
        labelLine(pack.gender, pack.displayGender(record.profile.gender), language),
        ...(solar ? [labelLine(pack.solar, solar, language)] : []),
        ...(lunar ? [labelLine(pack.lunar, lunar, language)] : []),
        ...(zodiac ? [labelLine(pack.zodiac, zodiac, language)] : []),
        ...(bazi ? [labelLine(pack.baziInfo, bazi, language)] : []),
        ...pillarLines,
        labelLine(pack.dayMaster, evidence.day_master, language),
        labelLine(pack.primaryTenGod, evidence.primary_ten_god, language),
        labelLine(pack.fiveElements, evidence.five_element_summary, language),
        labelLine(pack.currentLuck, evidence.current_luck, language),
    ];
}
function buildEntrySection(record) {
    const language = resolveLanguage("", record.preferences.preferred_language);
    const pack = localePack[language];
    const speech = t(profileReference(record, "五行表达参考"), language);
    const comm = t(profileReference(record, "十神沟通参考"), language);
    const decision = t(profileReference(record, "五行决策参考"), language);
    const tenGodDecision = t(profileReference(record, "十神决策参考"), language);
    const relationship = t(profileReference(record, "五行关系参考"), language);
    const stateSummary = t(stateReference(record, "状态摘要参考"), language);
    const stateComm = t(stateReference(record, "阶段沟通参考"), language);
    return [
        pack.quickRead,
        labelLine(pack.quickSpeech, joinPair(speech, comm, language), language),
        labelLine(pack.quickDecision, joinPair(decision, tenGodDecision, language), language),
        labelLine(pack.quickRelationship, language === "zh" || language === "ja" ? `${relationship}。` : `${relationship}.`, language),
        labelLine(pack.quickState, joinPair(stateSummary, stateComm, language), language),
    ];
}
function buildLuckTimelineSection(record) {
    const language = resolveLanguage("", record.preferences.preferred_language);
    const pack = localePack[language];
    const cyclesRoot = record.chart.luck_cycles;
    const cycles = cyclesRoot?.大运 ?? [];
    const header = [
        pack.luckTimeline,
        ...(cyclesRoot?.起运日期 ? [labelLine(pack.luckStartDate, summarizeValue(cyclesRoot.起运日期), language)] : []),
        ...(cyclesRoot?.起运年龄 ? [labelLine(pack.luckStartAge, summarizeValue(cyclesRoot.起运年龄), language)] : []),
    ];
    if (cycles.length === 0) {
        return [...header, "- 暂无可用大运资料。"];
    }
    return [
        ...header,
        ...cycles.map((cycle) => {
            const pillar = summarizeValue(cycle["干支"]);
            const startYear = summarizeValue(cycle["开始年份"]);
            const endYear = summarizeValue(cycle["结束"]);
            const tenGod = summarizeValue(cycle["天干十神"]);
            const branchGods = summarizeValue(cycle["地支十神"]);
            return `- ${pillar}（${startYear}-${endYear}）｜天干十神：${tenGod || "未提取"}${branchGods ? `｜地支十神：${branchGods}` : ""}`;
        }),
    ];
}
function categorizeMemory(memory) {
    return {
        facts: memory
            .filter((entry) => entry.type === "fact" || entry.type === "context")
            .slice(-6)
            .map((entry) => `- ${entry.content}`),
        adjustments: memory
            .filter((entry) => entry.type === "correction" || entry.type === "style")
            .slice(-4)
            .map((entry) => `- ${entry.content}`),
    };
}
function buildMemorySection(record) {
    const language = resolveLanguage("", record.preferences.preferred_language);
    const pack = localePack[language];
    const memory = categorizeMemory(record.memory);
    return [
        pack.recentFacts,
        ...(memory.facts.length > 0 ? memory.facts : [pack.noRecentFacts]),
        "",
        pack.longTermAdjustments,
        ...(memory.adjustments.length > 0 ? memory.adjustments : [pack.noAdjustments]),
    ];
}
function buildConversationSection(language) {
    const pack = localePack[language];
    return [
        pack.conversationMemory,
        pack.noConversationYet1,
        pack.noConversationYet2,
    ];
}
function buildAnalysisHintSection(record) {
    const language = resolveLanguage("", record.preferences.preferred_language);
    const pack = localePack[language];
    return [
        pack.analysisMode,
        pack.analysisHint1,
        pack.analysisHint2,
        pack.analysisHint3(`${record.snapshot.evidence.primary_ten_god} / ${record.snapshot.evidence.current_luck}`),
    ];
}
function buildLanguageHintSection(language) {
    const pack = localePack[language];
    return [
        pack.languageMode,
        pack.languageHint1,
        pack.languageHint2,
        pack.languageHint3,
    ];
}
export function buildBaziEvidence(params) {
    const { chart, knowledge } = params;
    const dayMaster = chart.day_master?.trim();
    if (!dayMaster) {
        throw new Error("Day master is missing from Bazi chart.");
    }
    const elementKey = knowledge.stem_to_element[dayMaster];
    if (!elementKey) {
        throw new Error(`Element mapping missing for day master: ${dayMaster}`);
    }
    const elementProfile = knowledge.element_profiles[elementKey];
    if (!elementProfile) {
        throw new Error(`Element profile missing for element: ${elementKey}`);
    }
    const primaryTenGod = pickPrimaryTenGod(chart);
    const tenGodBehavior = knowledge.ten_god_behaviors[primaryTenGod];
    if (!tenGodBehavior) {
        throw new Error(`Ten-god behavior mapping missing: ${primaryTenGod}`);
    }
    const currentLuck = pickCurrentLuck(chart);
    const fiveElementSummary = summarizeValue(chart.five_elements) || "未提取";
    const shift = knowledge.state_shift_by_ten_god[primaryTenGod];
    if (!shift) {
        throw new Error(`State shift mapping missing for ten-god: ${primaryTenGod}`);
    }
    const facts = extractRealityFacts(params.memory);
    const relationshipLens = (params.activeRelationships[0] ?? params.relationships[0] ?? "").trim();
    const effectiveRelationshipLens = relationshipLens || "当前互动";
    const relationshipSummary = normalizePhrase(elementProfile.relationship);
    const speechSummary = normalizePhrase(elementProfile.speech);
    const decisionSummary = normalizePhrase(elementProfile.decision);
    const tenGodDecisionSummary = normalizePhrase(tenGodBehavior.decision);
    const stressSummary = normalizePhrase(tenGodBehavior.stress);
    const traitSummary = normalizePhrase(tenGodBehavior.trait);
    const riskSummary = normalizePhrase(elementProfile.risk);
    const shiftSummary = normalizePhrase(shift.summary);
    const shiftCommunication = normalizePhrase(shift.communication);
    const shiftDecision = normalizePhrase(shift.decision);
    const evidenceLines = [
        `日主：${dayMaster}`,
        `五行结构：${fiveElementSummary}`,
        `主导十神：${primaryTenGod}`,
        `当前大运：${currentLuck}`,
        ...(relationshipLens ? [`关系：${relationshipLens}`] : []),
        facts.length > 0 ? `现实锚点：${facts.join(" / ")}` : "现实锚点：暂无补充事实",
    ];
    return {
        evidence: {
            day_master: dayMaster,
            primary_ten_god: primaryTenGod,
            five_element_summary: fiveElementSummary,
            current_luck: currentLuck,
            state_shift: shift,
            evidence_lines: evidenceLines,
        },
        references: {
            cognition: [
                `日主：${dayMaster}（五行：${elementKey}）`,
                ...bulletLines([
                    `五行认知参考：${elementProfile.summary}`,
                    `五行决策参考：${decisionSummary}`,
                    `十神决策参考：${tenGodDecisionSummary}`,
                ]),
            ].join("\n"),
            values: [
                `主导十神：${primaryTenGod}`,
                ...bulletLines([
                    `十神特质参考：${traitSummary}`,
                    `五行关系参考：${relationshipSummary}`,
                    `五行风险偏好参考：${riskSummary}`,
                ]),
            ].join("\n"),
            communication: [
                knowledge.reference_guidance.communication_title,
                ...bulletLines([
                    `五行表达参考：${speechSummary}`,
                    `十神沟通参考：${tenGodBehavior.communication}`,
                ]),
            ].join("\n"),
            relationship: [
                ...(relationshipLens ? [`关系：${relationshipLens}`] : []),
                ...bulletLines([
                    `五行关系参考：${relationshipSummary}`,
                    `当前关系观察：${knowledge.reference_guidance.relationship_tip_template.replace("{relation}", effectiveRelationshipLens)}`,
                ]),
            ].join("\n"),
            state: [
                `当前大运：${currentLuck}`,
                ...bulletLines([
                    `状态摘要参考：${shiftSummary}`,
                    `阶段沟通参考：${shiftCommunication}`,
                    `阶段判断参考：${shiftDecision}`,
                    `压力反应参考：${stressSummary}`,
                ]),
            ].join("\n"),
        },
    };
}
function buildAnalysisReply(record) {
    const language = resolveLanguage("", record.preferences.preferred_language);
    const evidence = record.snapshot.evidence;
    if (language === "en") {
        return [
            `${record.profile.name}: if I read this period from the Bazi side, I feel closer to ${t(trimLine(evidence.state_shift.summary), language)}.`,
            `In conversation, what stands out more is this: ${t(trimLine(evidence.state_shift.communication), language)}.`,
            `In decisions, the stronger pull is toward this: ${t(trimLine(evidence.state_shift.decision), language)}.`,
            `The main axis to read first is "${evidence.primary_ten_god} / ${evidence.current_luck}".`,
        ].join("\n");
    }
    if (language === "ja") {
        return [
            `${record.profile.name}：今の時期を八字から読むなら、全体としては${trimLine(evidence.state_shift.summary)}に近いです。`,
            `話し方では、${trimLine(evidence.state_shift.communication)}が強く出やすいです。`,
            `判断では、${trimLine(evidence.state_shift.decision)}に流れやすいです。`,
            `まず見る主軸は「${evidence.primary_ten_god} / ${evidence.current_luck}」です。`,
        ].join("\n");
    }
    if (language === "ko") {
        return [
            `${record.profile.name}: 지금 시기를 팔자 기준으로 보면 전체적으로 ${trimLine(evidence.state_shift.summary)} 쪽에 더 가깝습니다.`,
            `말투에서는 ${trimLine(evidence.state_shift.communication)} 성향이 더 강하게 드러납니다.`,
            `판단에서는 ${trimLine(evidence.state_shift.decision)} 쪽으로 기울기 쉽습니다.`,
            `먼저 볼 주축은 "${evidence.primary_ten_god} / ${evidence.current_luck}"입니다.`,
        ].join("\n");
    }
    return [
        `${record.profile.name}：如果按现在这段时间来看，整个人会更接近${trimLine(evidence.state_shift.summary)}。`,
        `说话这边更明显的是：${trimLine(evidence.state_shift.communication)}。`,
        `做判断时更容易走向：${trimLine(evidence.state_shift.decision)}。`,
        `命理主轴先看「${evidence.primary_ten_god} / ${evidence.current_luck}」。`,
    ].join("\n");
}
function uniqueLines(lines) {
    const seen = new Set();
    return lines.filter((line) => {
        const key = trimLine(line);
        if (!key || seen.has(key)) {
            return false;
        }
        seen.add(key);
        return true;
    });
}
function selectNormalReferences(record, message) {
    if (/忙|累|压力|辛苦|busy|tired|stress|stressed|疲|しんど|바빠|힘들|스트레스/iu.test(message)) {
        return [
            stateReference(record, "状态摘要参考"),
            stateReference(record, "阶段沟通参考"),
            stateReference(record, "压力反应参考"),
        ];
    }
    if (/在乎|重视|底线|喜欢|care|value|important|like|大事|好き|중요|가치/iu.test(message)) {
        return [
            profileReference(record, "十神特质参考"),
            profileReference(record, "五行风险偏好参考"),
            profileReference(record, "五行决策参考"),
        ];
    }
    if (/关系|相处|信任|边界|靠近|熟|慢热|relationship|close|distance|trust|boundar|getting close|相性|距離感|친해|관계|거리/iu.test(message)) {
        return [
            profileReference(record, "五行关系参考"),
            profileReference(record, "当前关系观察"),
            stateReference(record, "阶段沟通参考"),
        ];
    }
    if (/适合|要不要|建议|推进|决策|决定|should|advice|decide|decision|push|進め|判断|조언|결정|밀어/iu.test(message)) {
        return [
            profileReference(record, "五行决策参考"),
            profileReference(record, "十神决策参考"),
            stateReference(record, "阶段判断参考"),
        ];
    }
    return [
        profileReference(record, "五行表达参考"),
        profileReference(record, "十神沟通参考"),
        profileReference(record, "五行认知参考"),
    ];
}
function buildNormalReply(record, message) {
    const language = resolveLanguage(message, record.preferences.preferred_language);
    const references = uniqueLines(selectNormalReferences(record, message));
    const facts = record.memory.map((entry) => trimLine(entry.content)).filter(Boolean).slice(-1);
    if (language === "en") {
        return [
            `${record.profile.name}: if I answer from how I feel right now, it is closer to this.`,
            ...references.map((item) => {
                const translated = t(item, language);
                return translated.endsWith(".") ? translated : `${translated}.`;
            }),
            ...facts.map((fact) => `One recent real-life detail still shaping the tone is this: ${fact}.`),
        ].join("\n");
    }
    if (language === "ja") {
        return [
            `${record.profile.name}：今の感じで言うなら、近いのはこんな雰囲気です。`,
            ...references.map((item) => `${item}。`),
            ...facts.map((fact) => `最近の現実でまだ響いているのはこれです：${fact}。`),
        ].join("\n");
    }
    if (language === "ko") {
        return [
            `${record.profile.name}: 지금의 결로 말하면 대체로 이런 쪽에 가깝습니다.`,
            ...references.map((item) => `${item}.`),
            ...facts.map((fact) => `최근 현실에서 아직 남아 있는 건 이겁니다: ${fact}.`),
        ].join("\n");
    }
    const lines = [
        `${record.profile.name}：如果按我现在这个人的感觉，大概更接近这样。`,
        ...references.map((item) => item.endsWith("。") ? item : `${item}。`),
        ...facts.map((fact) => `最近还会被一件事带着走：${fact}。`),
    ];
    return lines.join("\n");
}
function buildPersonaMarkdown(params) {
    const facts = params.record.memory
        .filter((entry) => entry.type !== "context")
        .map((entry) => entry.content)
        .slice(-6);
    const { evidence, references } = buildBaziEvidence({
        chart: params.record.chart,
        knowledge: params.knowledge,
        relationships: params.record.relationships,
        activeRelationships: params.record.active_relationships,
        memory: params.record.memory,
    });
    const generatedAt = nowIso();
    const relationText = params.record.active_relationships.join(" / ").trim();
    const referenceProfile = [
        "# 人格参考知识",
        "",
        "## 八字与关系锚点",
        `- 名字：${params.record.profile.name}`,
        `- 性别：${params.record.profile.gender}`,
        ...(relationText ? [`- 关系：${relationText}`] : []),
        `- 日主：${evidence.day_master}`,
        `- 五行摘要：${evidence.five_element_summary}`,
        `- 主导十神：${evidence.primary_ten_god}`,
        "",
        "## 人格映射知识",
        references.cognition,
        "",
        references.values,
        "",
        references.communication,
        "",
        references.relationship,
        "",
        "## 最近现实素材",
        ...formatFacts(facts),
    ].join("\n");
    const referenceState = [
        "# 状态参考知识",
        "",
        "## 阶段锚点",
        `- 当前大运：${evidence.current_luck}`,
        `- 阶段主题：${evidence.state_shift.summary}`,
        `- 沟通偏移：${evidence.state_shift.communication}`,
        `- 判断偏移：${evidence.state_shift.decision}`,
        `- 命理主轴：${evidence.primary_ten_god} / ${evidence.current_luck}`,
        "",
        "## 阶段映射知识",
        references.state,
    ].join("\n");
    return {
        generated_at: generatedAt,
        prompt_stack: params.promptPack.entries.map((entry) => entry.id),
        evidence,
        reference_profile: referenceProfile,
        reference_state: referenceState,
    };
}
export function regenerateSnapshot(params) {
    return buildPersonaMarkdown(params);
}
export function renderPersonaMarkdown(record) {
    const language = resolveLanguage("", record.preferences.preferred_language);
    const pack = localePack[language];
    return [
        `# ${record.profile.name}`,
        "",
        ...pack.intro,
        "",
        ...buildEntrySection(record),
        "",
        ...buildProfileSection(record),
        "",
        ...buildBaziSection(record),
        "",
        ...buildLuckTimelineSection(record),
        "",
        pack.personaReference,
        ...stripTopHeading(record.snapshot.reference_profile),
        "",
        pack.stateReference,
        ...stripTopHeading(record.snapshot.reference_state),
        "",
        ...buildMemorySection(record),
        "",
        ...buildConversationSection(language),
        "",
        ...buildAnalysisHintSection(record),
        "",
        ...buildLanguageHintSection(language),
    ].join("\n");
}
export function respondInPersona(record, message, language) {
    const resolvedLanguage = language ?? resolveLanguage(message, record.preferences.preferred_language);
    const wantsAnalysis = record.preferences.analysis_mode === "cheatsheet" ||
        /cheatsheet|analysis|compat|命理|八字|分析|证据链|相性|사주|분석/i.test(message);
    if (wantsAnalysis) {
        return buildAnalysisReply({
            ...record,
            preferences: {
                ...record.preferences,
                preferred_language: resolvedLanguage,
            },
        });
    }
    return buildNormalReply({
        ...record,
        preferences: {
            ...record.preferences,
            preferred_language: resolvedLanguage,
        },
    }, message);
}
