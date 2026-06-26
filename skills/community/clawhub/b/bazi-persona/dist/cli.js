#!/usr/bin/env node
import { deletePersona, getPersonaFilePaths, loadHistoryEntries, listPersonas, loadPersona, resolvePersonaBaseDir, } from "./kernel/persona-store.js";
import { normalizeLanguage, resolveLanguage, resolvePersonaRef, parseArgsWithPositionalInput } from "./kernel/intent.js";
import { readUtf8IfExists } from "./shared/fs.js";
export function inspectPersona(args) {
    const baseDir = resolvePersonaBaseDir(args["base-dir"]);
    const personas = listPersonas(baseDir);
    const input = args.input ?? args.slug ?? "";
    const ref = args.slug ? personas.find((persona) => persona.slug === args.slug) : resolvePersonaRef(input, personas);
    if (!ref) {
        if (personas.length === 0) {
            return `No stored personas in ${baseDir}.`;
        }
        return [
            `Stored personas in ${baseDir}:`,
            ...personas.map((persona) => `- ${persona.name} (${persona.slug}) updated ${persona.updated_at}`),
        ].join("\n");
    }
    const record = loadPersona(ref.slug, baseDir);
    const conversations = loadHistoryEntries(ref.slug, baseDir);
    const filePaths = getPersonaFilePaths(record.slug, baseDir);
    const personaMarkdown = readUtf8IfExists(filePaths.persona_md).trim();
    return [
        `${record.profile.name} (${record.slug})`,
        `- Persona: ${filePaths.persona_md}`,
        `- Bazi Data: ${filePaths.bazi_data_json}`,
        `- Memory: ${filePaths.memory_json}`,
        `- History: ${filePaths.history_json}`,
        `- Conversations: ${conversations.length}`,
        `- Updated: ${record.updated_at}`,
        `- Relation: ${record.active_relationships.join(" / ")}`,
        `- Memory count: ${record.memory.length}`,
        "",
        personaMarkdown || record.snapshot.reference_profile,
    ].join("\n");
}
export function deleteStoredPersona(args) {
    const baseDir = resolvePersonaBaseDir(args["base-dir"]);
    const personas = listPersonas(baseDir);
    const input = args.input ?? args.slug ?? "";
    const ref = args.slug ? personas.find((persona) => persona.slug === args.slug) : resolvePersonaRef(input, personas);
    if (!ref) {
        throw new Error("Delete needs a persona slug or a name that matches an existing stored persona.");
    }
    const deleted = deletePersona(ref.slug, baseDir);
    if (!deleted) {
        throw new Error(`Persona not found: ${ref.slug}`);
    }
    return `Deleted persona: ${ref.name} (${ref.slug})`;
}
const cliTextPack = {
    zh: {
        title: "八字人格 Bazi Persona",
        brand: "Created by Cantian AI / 参天AI",
        intro1: "基于生辰八字，生成一个会聊天、会判断、会变化的 AI 人格。",
        intro2: "不用手动写人设，而是从生日出发，直接开始对话、观察和分析。",
        canDo: "你可以用它做三件事：",
        canDoLines: [
            "- 创建一个可持续对话的人格",
            "- 在后续聊天里吸收现实变化，让人格继续演化",
            "- 切到作弊模式，从八字、大运、流年角度分析状态、趋势和关系互动",
        ],
        fastestStart: "怎么开始最快：",
        startLines: [
            '- 直接说：「帮我创建八字人格：舒晴，女，1999年8月12日，上海，同事」',
            "- 创建完成后，就可以直接和她聊天",
            '- 如果想从命理角度解读，再说：「打开作弊模式」',
        ],
        directExamples: [
            '- "帮我创建八字人格：舒晴，女，1999年8月12日，上海，同事"',
            '- "打开作弊模式"',
            '- "今天黄历怎么样"',
        ],
        cliPositioning: "CLI 的定位：",
        storageOnly: "- This CLI is storage-only: inspect / list / delete stored persona files.",
        nonCli: "- Persona generation, updates, dialogue, flow analysis, and calendar lookup belong to the agent tool layer, not the CLI.",
        noShell: "- Do not use Bash/Node/tsx CLI calls to create personas or chat. Use the skill directly in the agent conversation.",
        storedAt: "- Stored data lives in personas/<slug>/{persona.md,bazi_data.json,memory.json,history.json} inside the installed skill directory.",
        fileExamples: "文件查看示例：",
        chatExamples: "更常见的是直接在对话里这样用：",
        unsupported: (action) => `Unsupported CLI action: ${action}`,
        unsupportedIntro: "Bazi Persona 是一个基于生辰八字的人格产品，用来创建可聊天、可判断、可变化的 AI 人格。",
        unsupportedStart: "直接开始最简单：",
    },
    en: {
        title: "Bazi Persona",
        brand: "Created by Cantian AI",
        intro1: "Generate an AI persona that can chat, judge, and evolve from a Bazi birth chart.",
        intro2: "You do not need to handwrite a persona. Start from the birthday and move straight into dialogue, observation, and analysis.",
        canDo: "You can use it for three things:",
        canDoLines: [
            "- Create a persona you can keep talking to",
            "- Absorb new real-world changes over time so the persona keeps evolving",
            "- Switch into cheat mode to analyze state, timing, and relationships through Bazi, luck cycles, and yearly flow",
        ],
        fastestStart: "Fastest way to begin:",
        startLines: [
            '- Just say: "Create a bazi persona: Shu Qing, female, 1999-08-12, Shanghai, coworker"',
            "- Once it is created, you can start chatting with her directly",
            '- If you want a fate-analysis angle, say: "Turn on cheat mode"',
        ],
        directExamples: [
            '- "Create a bazi persona: Shu Qing, female, 1999-08-12, Shanghai, coworker"',
            '- "Turn on cheat mode"',
            '- "How is today\'s Chinese almanac?"',
        ],
        cliPositioning: "What the CLI is for:",
        storageOnly: "- This CLI is storage-only: inspect / list / delete stored persona files.",
        nonCli: "- Persona generation, updates, dialogue, flow analysis, and calendar lookup belong to the agent tool layer, not the CLI.",
        noShell: "- Do not use Bash/Node/tsx CLI calls to create personas or chat. Use the skill directly in the agent conversation.",
        storedAt: "- Stored data lives in personas/<slug>/{persona.md,bazi_data.json,memory.json,history.json} inside the installed skill directory.",
        fileExamples: "File-management examples:",
        chatExamples: "More commonly, use it directly in chat:",
        unsupported: (action) => `Unsupported CLI action: ${action}`,
        unsupportedIntro: "Bazi Persona is a Bazi-based persona product for creating AI personas that can chat, judge, and evolve.",
        unsupportedStart: "The fastest way to begin is:",
    },
    ja: {
        title: "八字人格 Bazi Persona",
        brand: "Created by Cantian AI / 参天AI",
        intro1: "生辰八字をもとに、会話し、判断し、変化していく AI 人格を生成します。",
        intro2: "人設を手で書く必要はありません。誕生日からそのまま会話、観察、分析に入れます。",
        canDo: "主にできることは3つです：",
        canDoLines: [
            "- 継続して会話できる人格を作る",
            "- 後から現実の変化を取り込み、人格を育てていく",
            "- 作弊モードに切り替えて、八字・大運・流年から状態や関係を読む",
        ],
        fastestStart: "いちばん早い始め方：",
        startLines: [
            '- まずこう言ってください：「八字人格を作って：舒晴、女性、1999年8月12日、上海、同僚」',
            "- 作成できたら、そのままこの人と会話を始められます",
            '- 命理の角度で見たいなら：「作弊モードをオンにして」と言ってください',
        ],
        directExamples: [
            '- "八字人格を作って：舒晴、女性、1999年8月12日、上海、同僚"',
            '- "作弊モードをオンにして"',
            '- "今日の黄暦はどう？"',
        ],
        cliPositioning: "CLI の役割：",
        storageOnly: "- This CLI is storage-only: inspect / list / delete stored persona files.",
        nonCli: "- Persona generation, updates, dialogue, flow analysis, and calendar lookup belong to the agent tool layer, not the CLI.",
        noShell: "- Do not use Bash/Node/tsx CLI calls to create personas or chat. Use the skill directly in the agent conversation.",
        storedAt: "- Stored data lives in personas/<slug>/{persona.md,bazi_data.json,memory.json,history.json} inside the installed skill directory.",
        fileExamples: "ファイル確認の例：",
        chatExamples: "ふだんは対話でこう使います：",
        unsupported: (action) => `Unsupported CLI action: ${action}`,
        unsupportedIntro: "Bazi Persona は、生辰八字をもとに会話し、判断し、変化していく AI 人格を作るためのプロダクトです。",
        unsupportedStart: "いちばん簡単なのは：",
    },
    ko: {
        title: "八字人格 Bazi Persona",
        brand: "Created by Cantian AI / 参天AI",
        intro1: "생년월일의 사주를 바탕으로 대화하고, 판단하고, 변화하는 AI 인격을 만듭니다.",
        intro2: "인물을 손으로 설계할 필요 없이, 생일부터 바로 대화, 관찰, 분석을 시작할 수 있습니다.",
        canDo: "주요 용도는 세 가지입니다:",
        canDoLines: [
            "- 계속 대화할 수 있는 인격 만들기",
            "- 현실의 변화가 생기면 나중에 반영해 인격을 계속 진화시키기",
            "- 치트 모드로 전환해 사주, 대운, 세운 기준으로 상태와 관계를 해석하기",
        ],
        fastestStart: "가장 빠른 시작 방법:",
        startLines: [
            '- 이렇게 말하면 됩니다: "사주 인격 만들어줘: 舒晴, 여자, 1999년 8월 12일, 상하이, 동료"',
            "- 생성이 끝나면 바로 그 사람과 대화를 시작할 수 있습니다",
            '- 명리 관점으로 보고 싶으면: "치트 모드 켜줘"',
        ],
        directExamples: [
            '- "사주 인격 만들어줘: 舒晴, 여자, 1999년 8월 12일, 상하이, 동료"',
            '- "치트 모드 켜줘"',
            '- "오늘 황력 어때?"',
        ],
        cliPositioning: "CLI 용도:",
        storageOnly: "- This CLI is storage-only: inspect / list / delete stored persona files.",
        nonCli: "- Persona generation, updates, dialogue, flow analysis, and calendar lookup belong to the agent tool layer, not the CLI.",
        noShell: "- Do not use Bash/Node/tsx CLI calls to create personas or chat. Use the skill directly in the agent conversation.",
        storedAt: "- Stored data lives in personas/<slug>/{persona.md,bazi_data.json,memory.json,history.json} inside the installed skill directory.",
        fileExamples: "파일 확인 예시:",
        chatExamples: "보통은 대화에서 이렇게 씁니다:",
        unsupported: (action) => `Unsupported CLI action: ${action}`,
        unsupportedIntro: "Bazi Persona는 사주를 바탕으로 대화하고, 판단하고, 변화하는 AI 인격을 만드는 제품입니다.",
        unsupportedStart: "가장 간단한 시작은:",
    },
};
function resolveCliLanguage(args, action) {
    const explicit = normalizeLanguage(args.lang);
    if (explicit) {
        return explicit;
    }
    const hintText = [args.input, args.message, args.query, action].filter(Boolean).join(" ").trim();
    return resolveLanguage(hintText);
}
export function renderCliHelp(language = "zh") {
    const pack = cliTextPack[language];
    return [
        pack.title,
        pack.brand,
        pack.intro1,
        pack.intro2,
        "",
        pack.canDo,
        ...pack.canDoLines,
        "",
        pack.fastestStart,
        ...pack.startLines,
        "",
        pack.cliPositioning,
        pack.storageOnly,
        pack.nonCli,
        pack.noShell,
        pack.storedAt,
        "",
        pack.fileExamples,
        "- npm run bazi -- --action inspect",
        "- npm run bazi -- --action inspect --slug shu-qing",
        "- npm run bazi -- --action delete --slug shu-qing",
        "",
        pack.chatExamples,
        ...pack.directExamples,
    ].join("\n");
}
function normalizeCliAction(action) {
    const normalized = (action ?? "help").trim().toLowerCase();
    if (normalized === "inspect" || normalized === "list") {
        return "inspect";
    }
    if (normalized === "delete" || normalized === "remove" || normalized === "rm") {
        return "delete";
    }
    if (!normalized || normalized === "help") {
        return "help";
    }
    return "unsupported";
}
function renderUnsupportedAction(action, language = "zh") {
    const pack = cliTextPack[language];
    return [
        pack.unsupported(action ?? "(empty)"),
        pack.unsupportedIntro,
        pack.storageOnly,
        pack.nonCli,
        pack.noShell,
        "",
        pack.unsupportedStart,
        ...pack.directExamples,
    ].join("\n");
}
export async function main(argv = process.argv) {
    const args = parseArgsWithPositionalInput(argv);
    const language = resolveCliLanguage(args, args.action);
    const action = normalizeCliAction(args.action);
    let output;
    switch (action) {
        case "inspect":
            output = inspectPersona(args);
            break;
        case "delete":
            output = deleteStoredPersona(args);
            break;
        case "unsupported":
            output = renderUnsupportedAction(args.action, language);
            break;
        default:
            output = renderCliHelp(language);
            break;
    }
    process.stdout.write(`${output}\n`);
}
if (import.meta.url === `file://${process.argv[1]}`) {
    main().catch((error) => {
        process.stderr.write(`${error.message}\n`);
        process.exitCode = 1;
    });
}
