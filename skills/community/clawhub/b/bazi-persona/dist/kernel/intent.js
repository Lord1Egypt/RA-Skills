import { parseCliArgs } from "../shared/fs.js";
export function normalizeLanguage(value) {
    const text = value?.trim().toLowerCase();
    if (!text) {
        return undefined;
    }
    if (text === "zh" || text === "cn" || text === "zh-cn" || text === "zh-hans") {
        return "zh";
    }
    if (text === "en" || text === "en-us" || text === "en-gb") {
        return "en";
    }
    if (text === "ja" || text === "jp" || text === "ja-jp") {
        return "ja";
    }
    if (text === "ko" || text === "kr" || text === "ko-kr") {
        return "ko";
    }
    return undefined;
}
export function detectLanguage(input) {
    const text = input.trim();
    if (!text) {
        return undefined;
    }
    if (/[가-힣]/u.test(text)) {
        return "ko";
    }
    if (/[ぁ-ゟ゠-ヿ]/u.test(text)) {
        return "ja";
    }
    if (/[一-龥]/u.test(text)) {
        return "zh";
    }
    if (/[A-Za-z]/u.test(text)) {
        return "en";
    }
    return undefined;
}
export function resolveLanguage(input, preferred = "auto") {
    return detectLanguage(input) ?? (preferred === "auto" ? "zh" : preferred);
}
export function parseArgsWithPositionalInput(argv) {
    let cliTokens = argv.slice(2);
    if (cliTokens.length === 1) {
        const single = cliTokens[0].trim();
        if (single.startsWith("/bazi-persona") || single.startsWith("bazi-persona")) {
            const parts = single.match(/"[^"]*"|'[^']*'|[^\s]+/g) ?? [single];
            cliTokens = parts.map((part) => (part.startsWith("\"") && part.endsWith("\"")) || (part.startsWith("'") && part.endsWith("'"))
                ? part.slice(1, -1)
                : part);
        }
    }
    const normalizedArgv = [argv[0] ?? "node", argv[1] ?? "script", ...cliTokens];
    const parsed = parseCliArgs(normalizedArgv);
    if (parsed.input || parsed.message || parsed.query) {
        return parsed;
    }
    const consumed = new Set();
    for (let i = 0; i < cliTokens.length; i += 1) {
        const token = cliTokens[i];
        if (!token.startsWith("--")) {
            continue;
        }
        consumed.add(i);
        const next = cliTokens[i + 1];
        if (next && !next.startsWith("--")) {
            consumed.add(i + 1);
            i += 1;
        }
    }
    const positional = cliTokens.filter((_, index) => !consumed.has(index));
    if (positional.length > 0) {
        parsed.input = positional.join(" ").trim();
    }
    return parsed;
}
export function routeIntent(input) {
    const text = input.trim();
    const lower = text.toLowerCase();
    const analysis_mode = /cheatsheet|analysis|compat|打开作弊模式|開啟作弊模式|turn on cheat mode|enable cheat mode|上帝视角|命理|证据链|八字看|相性|사주|분석/i.test(text)
        ? "cheatsheet"
        : "normal";
    const temporalStateQuery = /(昨天|今天|明天|后天|yesterday|today|tomorrow|昨日|今日|明日|어제|오늘|내일)/i.test(text)
        && /(不一样|不太一样|变化|变了|差别|区别|感觉|状态|different|changed|change|difference|調子|変化|違う|달라|변화|상태)/i.test(text);
    if (!text || /help|帮助|怎么用|usage|使い方|도움말/.test(lower)) {
        return { action: "help", payload: text, analysis_mode };
    }
    if (/黄历|万年历|节气|calendar|almanac|暦|달력/.test(text)) {
        return { action: "calendar", payload: text, analysis_mode };
    }
    if (/我有哪些|有哪些人格|list|查看人格|inspect all|personas|一覧|목록/i.test(text)) {
        return { action: "inspect", payload: text, analysis_mode };
    }
    if ((/(状态|流年|流月|运势|current state|fortune|運勢|상태)/i.test(text) || temporalStateQuery) && !/(创建|更新|补充|create|update|生成|作成|생성)/i.test(text)) {
        return { action: "flow", payload: text, analysis_mode };
    }
    if (/更新|补充|纠正|修正|记住|update|remember|correct|fix|修正して|업데이트|기억/.test(text)) {
        return { action: "update", payload: text, analysis_mode };
    }
    if (/创建|生成|新建|create|generate|build|作成|生成して|만들|생성/i.test(lower)) {
        return { action: "create", payload: text, analysis_mode };
    }
    if (/查看|看看|inspect|是谁|设定|profile|show|誰|설정|프로필/i.test(lower)) {
        return { action: "inspect", payload: text, analysis_mode };
    }
    return { action: "respond", payload: text, analysis_mode };
}
function extractDateLikeToken(text) {
    const full = text.match(/(\d{4})[年년\-/.](\d{1,2})[月월\-/.](\d{1,2})(?:[日号일])?/u);
    if (full) {
        return `${full[1]}-${full[2].padStart(2, "0")}-${full[3].padStart(2, "0")}`;
    }
    const iso = text.match(/(\d{4})-(\d{1,2})-(\d{1,2})/u);
    if (!iso) {
        return undefined;
    }
    return `${iso[1]}-${iso[2].padStart(2, "0")}-${iso[3].padStart(2, "0")}`;
}
function extractTime(text) {
    const hm = text.match(/((上午|下午|晚上|凌晨|am|pm|AM|PM|morning|evening|night|오전|오후)?\s*\d{1,2}(?::|：|点|시)\d{1,2})/u);
    if (hm) {
        return hm[1].replace(/\s+/g, "");
    }
    const half = text.match(/((上午|下午|晚上|凌晨|오전|오후)?\s*\d{1,2}(点半|시반))/u);
    return half?.[1]?.replace(/\s+/g, "");
}
function extractName(text) {
    const cleaned = text.replace(/^.*?[：:]/u, "").trim();
    const beforeComma = cleaned.split(/[，,]/u)[0]?.trim();
    if (!beforeComma || /创建|人格|八字|帮我|please|create|persona|bazi/iu.test(beforeComma)) {
        return undefined;
    }
    return beforeComma;
}
function extractLocation(text) {
    const pieces = text.split(/[，,]/u).map((part) => part.trim()).filter(Boolean);
    return pieces.find((piece) => !/\d{4}|男|女|male|female|创建|生成|更新|create|generate|build|persona|bazi|同事|朋友|伴侣|家人|客户|friend|partner|family|coworker|最近/u.test(piece))?.replace(/人$/u, "");
}
function extractRelation(text) {
    const hints = ["同事", "朋友", "伴侣", "家人", "客户", "老板", "同学", "前任", "coworker", "friend", "partner", "family", "同僚", "友達", "恋人", "家族", "동료", "친구", "연인", "가족"];
    return hints.find((hint) => text.toLowerCase().includes(hint.toLowerCase()));
}
function extractGender(text) {
    if (/\bmale\b|男|男性|남/u.test(text)) {
        return "男";
    }
    if (/\bfemale\b|女|女性|여/u.test(text)) {
        return "女";
    }
    return undefined;
}
export function hydrateCreateArgs(args, input) {
    const next = { ...args };
    next.name = next.name ?? extractName(input) ?? "";
    next.gender = next.gender ?? extractGender(input) ?? "";
    next["birth-date"] = next["birth-date"] ?? extractDateLikeToken(input) ?? "";
    next["birth-time"] = next["birth-time"] ?? extractTime(input) ?? "";
    next["birth-location"] = next["birth-location"] ?? extractLocation(input) ?? "";
    next.relation = next.relation ?? extractRelation(input) ?? "";
    return next;
}
export function resolvePersonaRef(input, personas) {
    const lower = input.toLowerCase();
    return personas.find((persona) => lower.includes(persona.slug.toLowerCase()) || lower.includes(persona.name.toLowerCase()));
}
export function extractUpdateFact(input) {
    const [, payload = ""] = input.split(/[：:]/u, 2);
    return (payload || input).trim();
}
