import { buildChart, normalizeDateInput, normalizeTimeInput } from "../tools/bazi/calc.js";
import { parseDateTimeInput, queryChineseCalendar } from "../tools/calendar/query.js";
import { nowIso } from "../shared/fs.js";
import { createPersonaRecord, deletePersona, getPersonaFilePaths, listPersonas, loadHistoryEntries, loadPersona, resolvePersonaBaseDir, savePersona, searchPersonas, } from "./persona-store.js";
import { regenerateSnapshot } from "./persona-engine.js";
function normalizeGender(value) {
    if (value === "male" || value === "男") {
        return { runtime: "male" };
    }
    return { runtime: "female" };
}
function normalizeMemoryEntry(entry) {
    const content = typeof entry.content === "string" ? entry.content.trim() : "";
    if (!content) {
        return undefined;
    }
    const type = entry.type === "correction" || entry.type === "style" || entry.type === "context"
        ? entry.type
        : "fact";
    return {
        memory_id: entry.memory_id?.trim() || undefined,
        type,
        key: entry.key?.trim() || undefined,
        content,
        source: entry.source?.trim() || "user",
        time_anchor: entry.time_anchor?.trim() || undefined,
        importance: typeof entry.importance === "number" ? entry.importance : undefined,
        confidence: typeof entry.confidence === "number" ? entry.confidence : undefined,
        created_at: entry.created_at ?? nowIso(),
        updated_at: entry.updated_at,
    };
}
function normalizeMemoryList(entries) {
    return entries
        .map((entry) => normalizeMemoryEntry(entry))
        .filter((entry) => Boolean(entry));
}
function refreshRecord(record, context) {
    const snapshot = regenerateSnapshot({
        record: {
            schema_version: "4.0.0",
            slug: record.slug,
            profile: record.profile,
            relationships: record.relationships,
            active_relationships: record.active_relationships,
            preferences: record.preferences,
            chart: record.chart,
            memory: record.memory,
        },
        promptPack: context.promptPack,
        knowledge: context.knowledge,
    });
    return {
        ...record,
        snapshot,
        updated_at: snapshot.generated_at,
    };
}
function buildTransientRecordFromChart(input) {
    if (!input.chart) {
        throw new Error("bazi_flow_tool needs either chart or persona_slug.");
    }
    const now = nowIso();
    return {
        schema_version: "4.0.0",
        slug: "temporary-persona",
        profile: {
            name: "临时对象",
            gender: "女",
            birth_date: input.chart.birth_input.date,
            birth_time: input.chart.birth_input.provided_time,
            birth_location: input.chart.birth_input.location || undefined,
            calendar_type: input.chart.birth_input.calendar_type,
        },
        relationships: [],
        active_relationships: [],
        preferences: {
            preferred_language: input.lang ?? "zh",
            analysis_mode: "cheatsheet",
        },
        chart: input.chart,
        memory: [],
        snapshot: {
            generated_at: now,
            prompt_stack: [],
            evidence: {
                day_master: "",
                primary_ten_god: "",
                five_element_summary: "",
                current_luck: "",
                state_shift: {
                    summary: "",
                    communication: "",
                    decision: "",
                },
                evidence_lines: [],
            },
            reference_profile: "",
            reference_state: "",
        },
        created_at: now,
        updated_at: now,
    };
}
function normalizeConversationCandidate(raw, sourceType) {
    if (typeof raw === "string") {
        const content = raw.trim();
        if (!content) {
            return undefined;
        }
        return {
            id: `import-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            session_id: `import-${Date.now()}`,
            role: "user",
            content,
            mode: "chat",
            source_type: sourceType,
            created_at: nowIso(),
        };
    }
    if (!raw || typeof raw !== "object") {
        return undefined;
    }
    const source = raw;
    const content = typeof source.content === "string" ? source.content.trim() : "";
    if (!content) {
        return undefined;
    }
    return {
        id: typeof source.id === "string" ? source.id : `import-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        session_id: typeof source.session_id === "string" ? source.session_id : `import-${Date.now()}`,
        role: source.role === "assistant" ? "assistant" : "user",
        content,
        mode: "chat",
        source_type: sourceType,
        created_at: typeof source.created_at === "string" ? source.created_at : nowIso(),
    };
}
export async function bazi_chart_tool(input) {
    if (!input.name?.trim() || !input.birth_date?.trim() || !input.gender) {
        throw new Error("bazi_chart_tool requires name, gender, and birth_date.");
    }
    const gender = normalizeGender(input.gender);
    const chart = await buildChart({
        name: input.name.trim(),
        gender: gender.runtime,
        date: normalizeDateInput(input.birth_date),
        time: input.birth_time ? normalizeTimeInput(input.birth_time) : undefined,
        location: input.birth_location ?? "",
        calendarType: input.calendar_type ?? "solar",
        sect: input.sect ?? 2,
        sourceCommand: "/bazi-persona create",
    });
    return { chart };
}
export async function calendar_tool(input) {
    const at = parseDateTimeInput(input.at);
    const calendar = await queryChineseCalendar({
        year: at.year,
        month: at.month,
        day: at.day,
    });
    return {
        at: at.display,
        calendar,
    };
}
export async function bazi_flow_tool(input, context) {
    const record = input.persona_slug
        ? loadPersona(input.persona_slug, input.base_dir)
        : buildTransientRecordFromChart(input);
    const refreshed = refreshRecord({
        ...record,
        preferences: {
            ...record.preferences,
            preferred_language: input.lang ?? record.preferences.preferred_language,
            analysis_mode: "cheatsheet",
        },
    }, context);
    const at = parseDateTimeInput(input.at);
    const calendar = input.include_calendar === false
        ? undefined
        : await queryChineseCalendar({
            year: at.year,
            month: at.month,
            day: at.day,
        });
    return {
        persona_slug: input.persona_slug,
        at: at.display,
        flow: refreshed.snapshot.evidence,
        calendar,
    };
}
export async function chat_import_tool(input) {
    const sourceType = input.source_type;
    const maxCandidates = typeof input.max_candidates === "number" && input.max_candidates > 0
        ? input.max_candidates
        : 50;
    const rawItems = Array.isArray(input.payload)
        ? input.payload
        : typeof input.payload === "string"
            ? input.payload.split("\n").map((line) => line.trim()).filter(Boolean)
            : [input.payload];
    const candidates = rawItems
        .map((item) => normalizeConversationCandidate(item, sourceType === "ocr_text" ? "text" : sourceType))
        .filter((item) => Boolean(item))
        .slice(0, maxCandidates);
    const memories = candidates.map((entry) => ({
        memory_id: entry.id,
        type: "fact",
        content: entry.content,
        source: `chat_import:${sourceType}`,
        confidence: sourceType === "json" ? 0.8 : 0.65,
        created_at: entry.created_at,
    }));
    return {
        source_type: sourceType,
        timezone: input.timezone ?? "Asia/Shanghai",
        candidates,
        memories,
    };
}
export async function persona_data_tool(input, context) {
    const baseDir = resolvePersonaBaseDir(input.base_dir);
    const action = input.action;
    if (action === "list") {
        return {
            action,
            items: listPersonas(baseDir),
            base_dir: baseDir,
        };
    }
    if (action === "search") {
        return {
            action,
            items: searchPersonas(input.search_query ?? "", baseDir),
            base_dir: baseDir,
        };
    }
    if (action === "create") {
        const payload = input.create_payload;
        if (!payload?.profile?.name || !payload.profile.gender || !payload.profile.birth_date || !payload.chart) {
            throw new Error("persona_data_tool create requires create_payload.profile(name/gender/birth_date) and chart.");
        }
        const gender = payload.profile.gender === "男" ? "男" : "女";
        const birthDate = normalizeDateInput(payload.profile.birth_date);
        const birthTime = payload.profile.birth_time ? normalizeTimeInput(payload.profile.birth_time) : undefined;
        const initialFacts = Array.isArray(payload.initial_facts)
            ? payload.initial_facts.map((item) => item.trim()).filter(Boolean)
            : [];
        const memory = normalizeMemoryList([
            ...(payload.memory ?? []),
            ...initialFacts.map((content) => ({
                type: "fact",
                content,
                source: "initial_facts",
            })),
        ]);
        const record = createPersonaRecord({
            name: payload.profile.name,
            gender,
            birth_date: birthDate,
            birth_time: birthTime,
            birth_location: payload.profile.birth_location?.trim() || undefined,
            calendar_type: payload.profile.calendar_type ?? "solar",
            relation: payload.relationship,
            chart: payload.chart,
            memory,
            promptPack: context.promptPack,
            knowledge: context.knowledge,
            slug: payload.slug,
        });
        const saved = savePersona(payload.snapshot
            ? {
                ...record,
                snapshot: payload.snapshot,
                updated_at: nowIso(),
            }
            : record, baseDir);
        return {
            action,
            persona_slug: saved.slug,
            profile: saved.profile,
            files: getPersonaFilePaths(saved.slug, baseDir),
        };
    }
    if (action === "query") {
        if (!input.persona_slug?.trim()) {
            throw new Error("persona_data_tool query requires persona_slug.");
        }
        const record = loadPersona(input.persona_slug.trim(), baseDir);
        return {
            action,
            persona_slug: record.slug,
            profile: record.profile,
            relationships: record.active_relationships,
            snapshot: record.snapshot,
            files: getPersonaFilePaths(record.slug, baseDir),
            persona_markdown: record.persona_markdown ?? "",
            chart: record.chart,
            memory: record.memory,
            history_count: loadHistoryEntries(record.slug, baseDir).length,
        };
    }
    if (action === "patch") {
        if (!input.persona_slug?.trim() || !input.patch_payload) {
            throw new Error("persona_data_tool patch requires persona_slug and patch_payload.");
        }
        const record = loadPersona(input.persona_slug.trim(), baseDir);
        const patch = input.patch_payload;
        const profilePatch = patch.profile_patch ?? {};
        const mergedProfile = {
            ...record.profile,
            ...profilePatch,
            birth_date: profilePatch.birth_date ? normalizeDateInput(profilePatch.birth_date) : record.profile.birth_date,
            birth_time: profilePatch.birth_time ? normalizeTimeInput(profilePatch.birth_time) : record.profile.birth_time,
        };
        const memoryAppend = normalizeMemoryList(patch.memory_append ?? []);
        const nextRecord = {
            ...record,
            profile: mergedProfile,
            active_relationships: patch.relationship?.trim()
                ? [patch.relationship.trim()]
                : record.active_relationships,
            memory: [...record.memory, ...memoryAppend],
            preferences: {
                ...record.preferences,
                analysis_mode: patch.analysis_mode ?? record.preferences.analysis_mode,
            },
            updated_at: nowIso(),
        };
        const refreshed = refreshRecord(nextRecord, context);
        const withSnapshot = patch.snapshot_replace
            ? {
                ...refreshed,
                snapshot: {
                    ...refreshed.snapshot,
                    ...patch.snapshot_replace,
                    evidence: {
                        ...refreshed.snapshot.evidence,
                        ...(patch.snapshot_replace.evidence ?? {}),
                        state_shift: {
                            ...refreshed.snapshot.evidence.state_shift,
                            ...(patch.snapshot_replace.evidence?.state_shift ?? {}),
                        },
                    },
                },
                updated_at: nowIso(),
            }
            : refreshed;
        const saved = savePersona(withSnapshot, baseDir);
        return {
            action,
            persona_slug: saved.slug,
            profile: saved.profile,
            memory_count: saved.memory.length,
            updated_at: saved.updated_at,
            files: getPersonaFilePaths(saved.slug, baseDir),
        };
    }
    if (action === "delete") {
        if (!input.persona_slug?.trim()) {
            throw new Error("persona_data_tool delete requires persona_slug.");
        }
        const deleted = deletePersona(input.persona_slug.trim(), baseDir);
        return {
            action,
            persona_slug: input.persona_slug.trim(),
            deleted,
        };
    }
    throw new Error(`Unsupported persona_data_tool action: ${action}`);
}
function upsertByIdentity(existing, incoming) {
    let created = 0;
    let updated = 0;
    const next = [...existing];
    for (const item of incoming) {
        const index = next.findIndex((current) => ((item.memory_id && current.memory_id && item.memory_id === current.memory_id) ||
            (item.key && current.key && item.key === current.key)));
        if (index >= 0) {
            next[index] = {
                ...next[index],
                ...item,
                created_at: next[index].created_at,
                updated_at: nowIso(),
            };
            updated += 1;
            continue;
        }
        next.push(item);
        created += 1;
    }
    return { next, created, updated };
}
export async function memory_tool(input, context) {
    const baseDir = resolvePersonaBaseDir(input.base_dir);
    const record = loadPersona(input.persona_slug, baseDir);
    const action = input.action;
    if (action === "query") {
        const query = input.query?.trim().toLowerCase();
        const items = query
            ? record.memory.filter((entry) => entry.content.toLowerCase().includes(query) ||
                (entry.key?.toLowerCase().includes(query) ?? false))
            : record.memory;
        return {
            action,
            persona_slug: record.slug,
            count: items.length,
            items,
        };
    }
    if (action === "delete") {
        const filters = normalizeMemoryList(input.memories ?? []);
        const before = record.memory.length;
        const nextMemory = record.memory.filter((entry) => {
            if (filters.length === 0) {
                return true;
            }
            return !filters.some((filter) => (filter.memory_id && entry.memory_id === filter.memory_id) ||
                (filter.key && entry.key === filter.key) ||
                (filter.content && entry.content === filter.content));
        });
        const refreshed = refreshRecord({
            ...record,
            memory: nextMemory,
            updated_at: nowIso(),
        }, context);
        savePersona(refreshed, baseDir);
        return {
            action,
            persona_slug: record.slug,
            count: refreshed.memory.length,
            deleted: before - refreshed.memory.length,
        };
    }
    const incoming = normalizeMemoryList(input.memories ?? []);
    if (incoming.length === 0) {
        throw new Error(`memory_tool ${action} requires non-empty memories.`);
    }
    let nextMemory = record.memory;
    let created = 0;
    let updated = 0;
    if (action === "upsert") {
        const result = upsertByIdentity(record.memory, incoming);
        nextMemory = result.next;
        created = result.created;
        updated = result.updated;
    }
    else if (action === "merge") {
        const policy = input.merge_policy ?? "append";
        if (policy === "append") {
            nextMemory = [...record.memory, ...incoming];
            created = incoming.length;
        }
        else if (policy === "replace_same_key") {
            const result = upsertByIdentity(record.memory, incoming);
            nextMemory = result.next;
            created = result.created;
            updated = result.updated;
        }
        else {
            const existing = [...record.memory];
            for (const item of incoming) {
                if (!item.key) {
                    existing.push(item);
                    created += 1;
                    continue;
                }
                const index = existing.findIndex((entry) => entry.key === item.key);
                if (index < 0) {
                    existing.push(item);
                    created += 1;
                    continue;
                }
                const current = existing[index];
                const currentConfidence = typeof current.confidence === "number" ? current.confidence : 0;
                const nextConfidence = typeof item.confidence === "number" ? item.confidence : 0;
                if (nextConfidence >= currentConfidence) {
                    existing[index] = {
                        ...current,
                        ...item,
                        created_at: current.created_at,
                        updated_at: nowIso(),
                    };
                    updated += 1;
                }
            }
            nextMemory = existing;
        }
    }
    else {
        throw new Error(`Unsupported memory_tool action: ${action}`);
    }
    const refreshed = refreshRecord({
        ...record,
        memory: nextMemory,
        updated_at: nowIso(),
    }, context);
    savePersona(refreshed, baseDir);
    return {
        action,
        persona_slug: record.slug,
        count: refreshed.memory.length,
        created,
        updated,
    };
}
