import { createHash } from "node:crypto";
import { request } from "./http.js";

const noop = { info() {}, warn() {} };
const TAG = "[evermind-ai-everos]";

/** Generate a deterministic message ID scoped by idSeed.
 *  Same seed + role + content always produces the same ID.
 *  Different seeds (different turns/sessions) produce different IDs,
 *  so repeated short messages like "ok" won't collide across turns. */
function messageId(idSeed, role, content) {
  const hash = createHash("sha256").update(`${idSeed}:${role}:${content}`).digest("hex").slice(0, 24);
  return `em_${hash}`;
}

export async function searchMemories(cfg, params, log = noop) {
  const { memory_types, ...baseParams } = params;

  const episodicTypes = (memory_types ?? []).filter((t) => t === "episodic_memory" || t === "profile");
  const caseTypes = (memory_types ?? []).filter((t) => t === "agent_case" || t === "agent_skill");

  const searches = [];
  if (episodicTypes.length) searches.push({ label: "episodic+profile", types: episodicTypes });
  if (caseTypes.length) searches.push({ label: "case+skill", types: caseTypes });

  const results = await Promise.all(
    searches.map(async ({ label, types }) => {
      const p = { ...baseParams, memory_types: types };
      log.info(`${TAG} GET /api/v1/memories/search ${label}`, JSON.stringify(p));
      const r = await request(cfg, "GET", "/api/v1/memories/search", p);
      log.info(`${TAG} GET response ${label}`, JSON.stringify(r));
      return r;
    }),
  );

  // merge into a single response in order: episodic/profile first, then case/skill
  const merged = {
    status: "ok",
    result: {
      profiles: [],
      memories: [],
    },
  };
  for (const r of results) {
    if (r?.result?.profiles?.length) merged.result.profiles.push(...r.result.profiles);
    if (r?.result?.memories?.length) merged.result.memories.push(...r.result.memories);
  }
  return merged;
}

export async function saveMemories(cfg, { userId, groupId, messages = [], flush = false, idSeed = "" }, log = noop) {
  if (!messages.length) return;
  const stamp = Date.now();

  const payloads = messages.map((msg, i) => {
    const { role = "user", content = "" } = msg;
    const sender = role === "assistant" ? role : userId;
    const isLast = i === messages.length - 1;

    return {
      message_id: messageId(idSeed, role, content),
      create_time: new Date(stamp + i).toISOString(),
      role,
      sender,
      sender_name: sender,
      content,
      group_id: groupId,
      group_name: groupId,
      scene: "assistant",
      raw_data_type: "AgentConversation",
      ...(flush && isLast && { flush: true }),
    };
  });

  // Send sequentially to preserve message order on the backend
  for (const payload of payloads) {
    log.info(`${TAG} POST /api/v1/memories`, JSON.stringify(payload));
    const result = await request(cfg, "POST", "/api/v1/memories", payload);
    log.info(`${TAG} POST response`, JSON.stringify(result));
  }
}
