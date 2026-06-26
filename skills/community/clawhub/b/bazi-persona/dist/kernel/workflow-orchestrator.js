import { nowIso } from "../shared/fs.js";
import { calendar_tool, bazi_chart_tool, bazi_flow_tool, chat_import_tool, memory_tool, persona_data_tool } from "./core-tools.js";
import { appendHistoryEntry, listPersonas, loadPersona, resolvePersonaBaseDir } from "./persona-store.js";
import { extractUpdateFact, hydrateCreateArgs, normalizeLanguage, resolveLanguage, resolvePersonaRef } from "./intent.js";
import { respondInPersona } from "./persona-engine.js";
function parseInitialFacts(args, input) {
    const collected = [args.memory, args.note, args["initial-facts"], extractUpdateFact(input)]
        .filter((item) => Boolean(item))
        .map((item) => item.trim())
        .filter(Boolean);
    return [...new Set(collected)];
}
function resolveConversationPersona(args, input, baseDir) {
    if (args["current-persona-slug"]?.trim()) {
        return args["current-persona-slug"].trim();
    }
    if (args.slug?.trim()) {
        return args.slug.trim();
    }
    const personas = listPersonas(baseDir);
    const matched = resolvePersonaRef(input, personas);
    if (matched) {
        return matched.slug;
    }
    if (personas.length === 1) {
        return personas[0].slug;
    }
    return undefined;
}
function preferredLanguageFromArgs(args, input) {
    return normalizeLanguage(args.lang) ?? resolveLanguage(input);
}
function conversationEntry(params) {
    return {
        id: `${params.mode}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        session_id: params.sessionId,
        role: params.role,
        content: params.content,
        mode: params.mode,
        source_type: params.source_type,
        created_at: nowIso(),
    };
}
function promptBody(context, id) {
    return context.promptPack.entries.find((entry) => entry.id === id)?.body.trim() ?? "";
}
function isCheatModeOpenSignal(input) {
    return /打开作弊模式|打開作弊模式|開啟作弊模式|turn on cheat mode|enable cheat mode|cheatsheet on|チートモード.*(オン|開)|치트 모드.*(켜|열)/iu.test(input);
}
function isCheatModeCloseSignal(input) {
    return /关闭作弊模式|關閉作弊模式|turn off cheat mode|disable cheat mode|cheatsheet off|チートモード.*(オフ|閉)|치트 모드.*(꺼|종료)/iu.test(input);
}
function isStartupInjectionRequest(input) {
    return /soul\.md|SOUL\.md|启动注入|啟動注入|启动设定|啟動設定|startup persona|inject persona|按.*persona.*启动/iu.test(input);
}
export async function workflow_create_persona(params) {
    const input = params.args.input ?? "";
    const args = hydrateCreateArgs(params.args, input);
    if (!args.name || !args.gender || !args["birth-date"]) {
        throw new Error("Create requires name, gender, and birth-date.");
    }
    const language = preferredLanguageFromArgs(args, input);
    const chartResult = await bazi_chart_tool({
        name: args.name,
        gender: args.gender,
        birth_date: args["birth-date"],
        birth_time: args["birth-time"],
        birth_location: args["birth-location"],
        calendar_type: args.calendar === "lunar" ? "lunar" : "solar",
    });
    const initialFacts = parseInitialFacts(args, input);
    const createResult = await persona_data_tool({
        action: "create",
        base_dir: args["base-dir"],
        create_payload: {
            slug: args.slug,
            profile: {
                name: args.name,
                gender: /男|male/i.test(args.gender) ? "男" : "女",
                birth_date: args["birth-date"],
                birth_time: args["birth-time"],
                birth_location: args["birth-location"],
                calendar_type: args.calendar === "lunar" ? "lunar" : "solar",
            },
            relationship: args.relation,
            initial_facts: initialFacts,
            chart: chartResult.chart,
        },
    }, params.context);
    if (initialFacts.length > 0) {
        await memory_tool({
            action: "upsert",
            base_dir: args["base-dir"],
            persona_slug: createResult.persona_slug,
            memories: initialFacts.map((fact) => ({
                type: "fact",
                content: fact,
                source: "workflow_create",
                created_at: nowIso(),
            })),
        }, params.context);
    }
    const sessionId = `create-${createResult.persona_slug}-${Date.now()}`;
    appendHistoryEntry(createResult.persona_slug, conversationEntry({
        role: "user",
        content: input,
        mode: "create",
        sessionId,
        source_type: "chat",
    }), args["base-dir"]);
    const output = language === "en"
        ? `Created persona: ${createResult.profile.name} (${createResult.persona_slug})\nYou can start chatting now.`
        : `已创建人格：${createResult.profile.name}（${createResult.persona_slug}）\n现在可以直接开始聊天。`;
    appendHistoryEntry(createResult.persona_slug, conversationEntry({
        role: "assistant",
        content: output,
        mode: "create",
        sessionId,
        source_type: "chat",
    }), args["base-dir"]);
    return output;
}
export async function workflow_update_persona(params) {
    const input = params.args.input ?? params.args.message ?? "";
    const baseDir = resolvePersonaBaseDir(params.args["base-dir"]);
    const targetSlug = resolveConversationPersona(params.args, input, baseDir);
    if (!targetSlug) {
        throw new Error("Update requires a target persona.");
    }
    const factText = params.args.memory ?? params.args.correction ?? extractUpdateFact(input);
    if (!factText.trim()) {
        throw new Error("Update requires at least one fact or correction.");
    }
    await memory_tool({
        action: "upsert",
        base_dir: params.args["base-dir"],
        persona_slug: targetSlug,
        memories: [{
                type: /纠正|更正|correct|fix|不是/.test(factText) ? "correction" : "fact",
                content: factText.trim(),
                source: "workflow_update",
                created_at: nowIso(),
            }],
    }, params.context);
    await persona_data_tool({
        action: "patch",
        base_dir: params.args["base-dir"],
        persona_slug: targetSlug,
        patch_payload: {
            relationship: params.args.relation,
        },
    }, params.context);
    const updated = loadPersona(targetSlug, params.args["base-dir"]);
    const output = `Updated persona: ${updated.profile.name} (${updated.slug})\n- Added memory: ${factText.trim()}`;
    const sessionId = `update-${updated.slug}-${Date.now()}`;
    appendHistoryEntry(updated.slug, conversationEntry({
        role: "user",
        content: input,
        mode: "update",
        sessionId,
        source_type: "chat",
    }), params.args["base-dir"]);
    appendHistoryEntry(updated.slug, conversationEntry({
        role: "assistant",
        content: output,
        mode: "update",
        sessionId,
        source_type: "chat",
    }), params.args["base-dir"]);
    return output;
}
export async function workflow_chat(params) {
    const input = params.args.input ?? params.args.message ?? "";
    const baseDir = resolvePersonaBaseDir(params.args["base-dir"]);
    const targetSlug = resolveConversationPersona(params.args, input, baseDir);
    if (!targetSlug) {
        throw new Error("Chat requires a target persona. Please specify persona name or slug.");
    }
    const cheatPrompt = promptBody(params.context, "cheat_mode");
    if (isStartupInjectionRequest(input)) {
        return workflow_persona_startup_injection({ args: { ...params.args, slug: targetSlug }, context: params.context });
    }
    if (isCheatModeOpenSignal(input)) {
        await persona_data_tool({
            action: "patch",
            base_dir: params.args["base-dir"],
            persona_slug: targetSlug,
            patch_payload: {
                analysis_mode: "cheatsheet",
            },
        }, params.context);
        return [
            "作弊模式已开启 ✓",
            "后续会在当前人格口吻下叠加命理分析视角。",
            cheatPrompt ? "已加载作弊模式提示词。" : "",
        ].filter(Boolean).join("\n");
    }
    if (isCheatModeCloseSignal(input)) {
        await persona_data_tool({
            action: "patch",
            base_dir: params.args["base-dir"],
            persona_slug: targetSlug,
            patch_payload: {
                analysis_mode: "normal",
            },
        }, params.context);
        return "作弊模式已关闭 ✓\n已回到普通聊天模式。";
    }
    const record = loadPersona(targetSlug, params.args["base-dir"]);
    const output = respondInPersona(record, input, preferredLanguageFromArgs(params.args, input));
    const mode = record.preferences.analysis_mode === "cheatsheet" ? "analysis" : "chat";
    const sessionId = `${mode}-${targetSlug}-${Date.now()}`;
    appendHistoryEntry(targetSlug, conversationEntry({
        role: "user",
        content: input,
        mode,
        sessionId,
        source_type: "chat",
    }), params.args["base-dir"]);
    appendHistoryEntry(targetSlug, conversationEntry({
        role: "assistant",
        content: output,
        mode,
        sessionId,
        source_type: "chat",
    }), params.args["base-dir"]);
    if (/记住|更新|补充|记一下|update|remember/i.test(input)) {
        await memory_tool({
            action: "upsert",
            base_dir: params.args["base-dir"],
            persona_slug: targetSlug,
            memories: [{
                    type: "fact",
                    content: input,
                    source: "chat",
                    created_at: nowIso(),
                }],
        }, params.context);
    }
    return output;
}
export async function workflow_query_flow(params) {
    const input = params.args.input ?? "";
    const baseDir = resolvePersonaBaseDir(params.args["base-dir"]);
    const targetSlug = params.args.slug?.trim() || resolveConversationPersona(params.args, input, baseDir);
    if (!targetSlug) {
        throw new Error("Flow query requires target persona.");
    }
    const result = await bazi_flow_tool({
        persona_slug: targetSlug,
        base_dir: params.args["base-dir"],
        at: params.args.at ?? input,
        include_calendar: true,
        lang: preferredLanguageFromArgs(params.args, input),
    }, params.context);
    return [
        `[Flow] ${targetSlug}`,
        `- 时间锚点: ${result.at}`,
        `- 当前大运: ${result.flow.current_luck}`,
        `- 阶段主题: ${result.flow.state_shift.summary}`,
        `- 沟通偏移: ${result.flow.state_shift.communication}`,
        `- 判断偏移: ${result.flow.state_shift.decision}`,
        ...(result.calendar?.干支日期 ? [`- 干支日期: ${result.calendar.干支日期}`] : []),
        ...(result.calendar?.节气 ? [`- 节气: ${result.calendar.节气.term}`] : []),
    ].join("\n");
}
export async function workflow_query_calendar(params) {
    const result = await calendar_tool({
        at: params.args.at ?? params.args.input,
    });
    if (!result.calendar) {
        return `Calendar unavailable for ${result.at}`;
    }
    return [
        `[Calendar] ${result.at}`,
        `- 农历: ${result.calendar.农历}`,
        `- 干支日期: ${result.calendar.干支日期}`,
        `- 节气: ${result.calendar.节气.term}`,
        `- 宜: ${result.calendar.宜}`,
        `- 忌: ${result.calendar.忌}`,
    ].join("\n");
}
export async function workflow_import_chat(params) {
    const targetSlug = params.args.slug?.trim() || params.args["persona-slug"]?.trim();
    if (!targetSlug) {
        throw new Error("Chat import requires persona slug.");
    }
    const sourceType = (params.args["source-type"] ?? "text");
    const payload = params.args.payload ?? params.args.input ?? "";
    const imported = await chat_import_tool({
        source_type: sourceType,
        payload,
        persona_slug: targetSlug,
        max_candidates: Number.parseInt(params.args["max-candidates"] ?? "50", 10),
    });
    await memory_tool({
        action: "merge",
        persona_slug: targetSlug,
        base_dir: params.args["base-dir"],
        memories: imported.memories,
        merge_policy: "append",
    }, params.context);
    await persona_data_tool({
        action: "patch",
        base_dir: params.args["base-dir"],
        persona_slug: targetSlug,
        patch_payload: {},
    }, params.context);
    for (const candidate of imported.candidates) {
        appendHistoryEntry(targetSlug, candidate, params.args["base-dir"]);
    }
    return `Imported ${imported.candidates.length} chat items, extracted ${imported.memories.length} memory candidates.`;
}
export async function workflow_persona_startup_injection(params) {
    const baseDir = resolvePersonaBaseDir(params.args["base-dir"]);
    const input = params.args.input ?? "";
    const targetSlug = params.args.slug?.trim() || resolveConversationPersona(params.args, input, baseDir);
    if (!targetSlug) {
        throw new Error("Startup injection requires target persona.");
    }
    const record = loadPersona(targetSlug, params.args["base-dir"]);
    const basePrompt = promptBody(params.context, "chat_base");
    return [
        `已准备 ${record.profile.name} 的启动注入内容（仅本 persona 生效）：`,
        "",
        "你现在进入指定 persona 的会话启动态。",
        "要求：",
        "1) 以 persona 的口吻、身份关系和表达节奏说话。",
        "2) 优先遵守基础聊天提示词里的边界、禁区和安全规则。",
        "3) 不要编造 persona 未提供的硬事实；不确定时先澄清。",
        "4) 普通模式下以自然对话为主，不主动展开命理术语。",
        "5) 仅在用户明确要求时再切换到作弊模式或其他专项提示词。",
        "",
        basePrompt ? "【基础聊天提示词已就绪】" : "【未找到基础聊天提示词，请检查 prompts/manifest.json】",
    ].join("\n");
}
