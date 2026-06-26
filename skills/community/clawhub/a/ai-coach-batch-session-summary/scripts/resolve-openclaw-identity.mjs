/**
 * 从 OpenClaw 入站 body 解析 hardware 查询用的 userId / orgId。
 *
 * model 组装规则（与 tfd-api AiService 一致）：
 * - 有组织：openclaw:{userId}{orgId}
 * - 个人：  openclaw:{userId}person
 *
 * userId 取 body.user；orgId 优先 body.orgId，否则从 model 后缀解析。
 */

export const OPENCLAW_MODEL_PREFIX = "openclaw:";
export const OPENCLAW_MODEL_PERSON_SUFFIX = "person";

export function modelEndsWithPerson(model) {
  const m = String(model ?? "").trim();
  if (!m) {
    return false;
  }
  return m.toLowerCase().endsWith(OPENCLAW_MODEL_PERSON_SUFFIX.toLowerCase());
}

/**
 * 从 model 去掉 openclaw:{user} 前缀后的后缀作为 orgId。
 * @param {string} model
 * @param {string} user OpenClaw user / hardware userId
 */
export function parseOrgIdFromModel(model, user) {
  const m = String(model ?? "").trim();
  const u = String(user ?? "").trim();
  if (!m || !u || !m.startsWith(OPENCLAW_MODEL_PREFIX)) {
    return null;
  }
  if (modelEndsWithPerson(m)) {
    return null;
  }
  const prefix = OPENCLAW_MODEL_PREFIX + u;
  if (!m.startsWith(prefix)) {
    return null;
  }
  const suffix = m.slice(prefix.length).trim();
  if (!suffix || modelEndsWithPerson(suffix)) {
    return null;
  }
  return suffix;
}

/**
 * @param {object|null} body OpenClaw / 网关 stdin JSON
 * @returns {{
 *   userId: string|null,
 *   orgId: string|null,
 *   personal: boolean,
 *   orgSource: string|null,
 *   model: string|null
 * }}
 */
export function resolveOpenClawIdentity(body) {
  const userId = String(body?.user ?? body?.userId ?? "").trim() || null;
  const model = body?.model != null ? String(body.model).trim() : null;

  if (body?.orgId != null && String(body.orgId).trim() !== "") {
    return {
      userId,
      orgId: String(body.orgId).trim(),
      personal: false,
      orgSource: "body.orgId",
      model,
    };
  }

  if (body?.orgId != null && String(body.orgId).trim() === "") {
    return {
      userId,
      orgId: null,
      personal: true,
      orgSource: "body.orgId_empty",
      model,
    };
  }

  if (modelEndsWithPerson(model)) {
    return {
      userId,
      orgId: null,
      personal: true,
      orgSource: "model.person",
      model,
    };
  }

  const fromModel = userId ? parseOrgIdFromModel(model, userId) : null;
  if (fromModel) {
    return {
      userId,
      orgId: fromModel,
      personal: false,
      orgSource: "model.suffix",
      model,
    };
  }

  return {
    userId,
    orgId: null,
    personal: true,
    orgSource: model ? "model.unresolved" : "missing",
    model,
  };
}
