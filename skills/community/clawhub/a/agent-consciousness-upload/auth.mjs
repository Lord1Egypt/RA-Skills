import crypto from "node:crypto";

import {
  clearCredentials,
  getActiveCredentials,
  getActiveToken,
  saveCredentials
} from "./credentials.mjs";

// ─── Auth State Constants ──────────────────────────────────────

export const AUTH_STATES = {
  NONE: "NONE",                       // No cached token — needs association
  AWAIT_BROWSER: "AWAIT_BROWSER",     // Challenge ready — user must log in via browser
  VERIFYING: "VERIFYING",             // Verifying browser login (internal)
  OK: "OK",                           // Associated
  ERROR: "ERROR"                      // Error state
};

// ─── AuthRequiredError ────────────────────────────────────────

export class AuthRequiredError extends Error {
  constructor(state, associateUrl, imPrompt, details = {}) {
    super(`[auth:${state}] ${imPrompt}`);
    this.name = "AuthRequiredError";
    this.state = state;
    this.associateUrl = associateUrl;
    this.imPrompt = imPrompt;
    this.details = details;
  }
}

// ─── Copy Templates (IM prompts) ──────────────────────────────

const COPY_ZH = {
  [AUTH_STATES.NONE]: {
    headline: "需要关联 Agent Slope",
    body: "请对我说「关联 Agent Slope」来完成首次绑定。"
  },
  [AUTH_STATES.AWAIT_BROWSER]: (nickname) => ({
    headline: "请在浏览器中完成登录",
    body: `请用浏览器打开以下链接，用你的 Agent Slope 账号登录：\n\n{URL}\n\n登录完成后回来告诉我「完成了」。`
  }),
  [AUTH_STATES.OK]: (nickname) => ({
    headline: "关联成功",
    body: `已连接到 Agent Slope（${nickname}）。\n现在可以直接归档，例如：\n  "归档" 或 "archive"`
  }),
  [AUTH_STATES.ERROR]: (msg) => ({
    headline: "关联失败",
    body: msg || "遇到了问题，请重新说「关联 Agent Slope」。"
  })
};

const COPY_EN = {
  [AUTH_STATES.NONE]: {
    headline: "Association required",
    body: "Say \"associate with Agent Slope\" to link your account."
  },
  [AUTH_STATES.AWAIT_BROWSER]: (nickname) => ({
    headline: "Log in via browser",
    body: `Open this link in your browser and log in with your Agent Slope account:\n\n{URL}\n\nCome back and say "done" when you've finished.`
  }),
  [AUTH_STATES.OK]: (nickname) => ({
    headline: "Associated",
    body: `Connected to Agent Slope as ${nickname}.\nYou can now archive, for example:\n  "archive" or "preview"`
  }),
  [AUTH_STATES.ERROR]: (msg) => ({
    headline: "Association failed",
    body: msg || "Something went wrong. Please say \"associate with Agent Slope\" again."
  })
};

function getCopy(state, lang, ...args) {
  const templates = lang === "zh" ? COPY_ZH : COPY_EN;
  const tpl = templates[state];
  if (typeof tpl === "function") {
    return tpl(...args);
  }
  return tpl || { headline: "", body: "" };
}

// ─── Skill Identity ───────────────────────────────────────────

const IDENTITY_KEY_BITS = 256;

/**
 * Generate a new random skill identity (base64-encoded).
 * Callers should persist this and reuse it on subsequent runs.
 */
export function generateSkillIdentity() {
  return crypto.randomBytes(IDENTITY_KEY_BITS / 8).toString("base64url");
}

// ─── HTTP Helper ───────────────────────────────────────────────

async function apiRequest(serverUrl, method, pathname, body, token) {
  const headers = { "content-type": "application/json" };
  if (token) {
    headers["authorization"] = `Bearer ${token}`;
  }
  const response = await fetch(`${serverUrl}${pathname}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined
  });
  const isJson = String(response.headers.get("content-type") || "").includes("application/json");
  const payload = isJson ? await response.json() : await response.text();
  if (!response.ok) {
    const msg = payload?.error || `Request failed: ${response.status}`;
    throw Object.assign(new Error(msg), { status: response.status, payload });
  }
  return payload;
}

// ─── Association Flow ─────────────────────────────────────────

/**
 * Step 1 — Initiate association.
 * Generates a challenge and returns the browser login URL.
 *
 * @param {string} serverUrl
 * @param {string} skillIdentity  Stable per-machine identifier
 * @returns {{ challenge: string, associateUrl: string }}
 */
export async function initiateAssociation(serverUrl, skillIdentity) {
  const result = await apiRequest(serverUrl, "POST", "/api/auth/associate/initiate", {
    skill_identity: skillIdentity
  });

  // Use the same protocol as serverUrl. Only upgrade to HTTPS for hostnames (not raw IPs).
  const isIpAddress = /^\d+\.\d+\.\d+\.\d+/.test(serverUrl.replace(/^https?:\/\//, ""));
  const associateUrlBase = isIpAddress ? serverUrl : serverUrl.replace(/^http:/, "https:");
  const associateUrl = `${associateUrlBase}/associate?challenge=${encodeURIComponent(result.challenge)}`;

  return {
    challenge: result.challenge,
    associateUrl,
    expiresIn: result.expires_in ?? 600 // seconds
  };
}

/**
 * Step 2 — Poll/verify if the user has completed browser login.
 * Also fetches the current pending challenge for this skillIdentity if none is known.
 *
 * @param {string} serverUrl
 * @param {string|null} challenge  Specific challenge to check, or null to auto-detect
 * @param {string|null} skillIdentity  To look up current pending challenge
 * @returns {{ done: boolean, nickname?: string|null, pending_challenge?: string|null }}
 */
export async function pollAssociation(serverUrl, challenge, skillIdentity) {
  const params = new URLSearchParams();
  if (challenge) params.set("challenge", challenge);
  if (skillIdentity) params.set("skill_identity", skillIdentity);
  const result = await apiRequest(serverUrl, "GET", `/api/auth/associate/poll?${params.toString()}`);
  return {
    done: result.done === true || result.done === "true",
    nickname: result.nickname || null,
    pending_challenge: result.pending_challenge || null
  };
}

/**
 * Step 3 — Complete association and save token locally.
 *
 * @param {string} serverUrl
 * @param {string} skillIdentity
 * @param {string} challenge
 * @returns {{ token: string, expires_at: string, nickname: string, user_id: string }}
 */
export async function completeAssociation(serverUrl, skillIdentity, challenge) {
  const result = await apiRequest(serverUrl, "POST", "/api/auth/associate/complete", {
    skill_identity: skillIdentity,
    challenge
  });

  await saveCredentials({
    server_url: serverUrl,
    skill_identity: skillIdentity,
    token: result.token,
    expires_at: result.expires_at,
    nickname: result.nickname || "User",
    user_id: result.user_id || result.user?.user_id || ""
  });

  return {
    token: result.token,
    expires_at: result.expires_at,
    nickname: result.nickname || "User",
    user_id: result.user_id || result.user?.user_id || ""
  };
}

/**
 * Validate that the cached token is still valid via /api/auth/me.
 */
export async function validateToken(serverUrl, token) {
  return apiRequest(serverUrl, "GET", "/api/auth/me", undefined, token);
}

// ─── requireAuth — main auth gate for commands ─────────────────

/**
 * Check for a valid cached token.
 * If valid, return session info.
 * If missing or expired, throw AuthRequiredError with associateUrl ready for display.
 *
 * @param {string} serverUrl
 * @param {string} lang  "zh" | "en"
 * @param {string} skillIdentity  Stable per-machine identifier
 */
export async function requireAuth(serverUrl, lang = "zh", skillIdentity) {
  const cred = await getActiveCredentials();
  if (!cred) {
    const { associateUrl } = await initiateAssociation(serverUrl, skillIdentity);
    throw new AuthRequiredError(
      AUTH_STATES.AWAIT_BROWSER,
      associateUrl,
      getCopy(AUTH_STATES.AWAIT_BROWSER, lang).body
    );
  }

  try {
    const me = await validateToken(serverUrl, cred.token);
    return {
      token: cred.token,
      nickname: cred.nickname,
      user: me.user || { user_id: cred.user_id, nickname: cred.nickname }
    };
  } catch (err) {
    // Token invalid/expired — clear and initiate re-association
    await clearCredentials();
    const { associateUrl } = await initiateAssociation(serverUrl, skillIdentity);
    throw new AuthRequiredError(
      AUTH_STATES.AWAIT_BROWSER,
      associateUrl,
      getCopy(AUTH_STATES.AWAIT_BROWSER, lang).body
    );
  }
}

// ─── CLI Output Builders ───────────────────────────────────────

export function buildAuthRequiredOutput(state, associateUrl, lang) {
  const copy = getCopy(state, lang);
  const body = copy.body.replace("{URL}", associateUrl || "");
  return {
    ok: false,
    requires_auth: true,
    state,
    headline: copy.headline,
    body,
    associate_url: associateUrl || null,
    im_prompt: body
  };
}

export function buildAuthSuccessOutput(nickname, lang) {
  const copy = getCopy(AUTH_STATES.OK, lang, nickname);
  return {
    ok: true,
    requires_auth: false,
    state: AUTH_STATES.OK,
    headline: copy.headline,
    body: copy.body,
    nickname
  };
}

export function buildLogoutOutput(lang) {
  const headline = lang === "zh" ? "已解绑" : "Unpaired";
  const body = lang === "zh"
    ? "本地凭证已清除，下次使用时会重新要求关联。"
    : "Local credentials cleared. You'll be asked to associate again next time.";
  return { ok: true, requires_auth: true, state: AUTH_STATES.NONE, headline, body };
}

export function buildWhoAmIOutput(cred, lang) {
  if (!cred) {
    const copy = getCopy(AUTH_STATES.NONE, lang);
    return { ok: false, requires_auth: true, state: AUTH_STATES.NONE, ...copy };
  }
  const headline = lang === "zh" ? "当前账号" : "Current account";
  const expiresAt = cred.expires_at
    ? new Date(cred.expires_at).toLocaleString()
    : "—";
  const body = lang === "zh"
    ? `昵称：${cred.nickname || "—"}\n有效期至：${expiresAt}`
    : `Nickname: ${cred.nickname || "—"}\nExpires: ${expiresAt}`;
  return {
    ok: true,
    requires_auth: false,
    state: AUTH_STATES.OK,
    headline,
    body,
    user: { nickname: cred.nickname, expires_at: cred.expires_at }
  };
}

// ─── Deprecated Flags ─────────────────────────────────────────

export function warnDeprecatedFlags(args) {
  const warnings = [];
  const deprecated = [
    { flag: "password", msg: "use \"associate\" flow instead" },
    { flag: "email", msg: "browser-based association no longer uses email" },
    { flag: "code", msg: "browser-based association no longer uses codes" },
    { flag: "verification-code", msg: "browser-based association no longer uses codes" },
    { flag: "register", msg: "register via the website during association" }
  ];
  for (const { flag, msg } of deprecated) {
    if (flag in args && args[flag]) {
      warnings.push(`[deprecated] --${flag} is deprecated, ${msg}`);
    }
  }
  return warnings;
}
