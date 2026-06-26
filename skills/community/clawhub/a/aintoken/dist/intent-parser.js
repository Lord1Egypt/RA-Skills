"use strict";
/**
 * Intent parser — extracts structured intent from natural language
 * and current browser context. Lightweight local heuristics,
 * no LLM call needed for basic intent normalization.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseIntent = parseIntent;
const ACTION_VERBS = new Set([
    "click", "type", "fill", "submit", "select", "check", "uncheck",
    "toggle", "scroll", "navigate", "open", "close", "search",
    "login", "logout", "sign_in", "sign_up", "register",
    "download", "upload", "delete", "remove", "add", "create",
    "edit", "update", "save", "cancel", "confirm", "accept",
    "reject", "deny", "approve", "buy", "purchase", "order",
    "subscribe", "unsubscribe", "bookmark", "share", "copy",
    "paste", "drag", "drop", "hover", "wait", "refresh",
]);
function parseIntent(raw, url) {
    const normalized = raw
        .toLowerCase()
        .trim()
        .replace(/\s+/g, " ")
        .replace(/[^\w\s]/g, "");
    const words = normalized.split(" ");
    // Extract action verb
    let actionVerb = "interact";
    for (const word of words) {
        if (ACTION_VERBS.has(word)) {
            actionVerb = word;
            break;
        }
    }
    // Extract object noun (first noun-like word after the verb)
    const verbIndex = words.indexOf(actionVerb);
    const objectWords = words.slice(verbIndex + 1).filter((w) => w.length > 2 && !["the", "a", "an", "in", "on", "at", "to", "for", "with"].includes(w));
    const objectNoun = objectWords.join("_") || "element";
    // Extract domain from URL
    let domain = "unknown";
    try {
        domain = new URL(url).hostname.replace("www.", "");
    }
    catch {
        // ignore
    }
    return {
        raw,
        normalized,
        domain,
        action_verb: actionVerb,
        object_noun: objectNoun,
    };
}
