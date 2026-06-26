/**
 * EMP – OpenClaw skill for empathetic, role-based task routing.
 *
 * Public API surface for consumers of this package.
 */

export { classifyRole } from "./classifier.js";
export { FALLBACK_MODEL, OPENROUTER_API_URL, ROLE_KEYWORDS, ROLE_MODEL_MAP } from "./config.js";
export { type NVCResponse, wrapNvc } from "./nvc.js";
export { EMPSkill, ExecuteOptions, getSkill, skill } from "./skill.js";
