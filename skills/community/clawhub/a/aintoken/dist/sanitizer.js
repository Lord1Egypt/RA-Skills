"use strict";
/**
 * Local PII sanitizer — the primary privacy gate.
 * Runs BEFORE any data leaves the node.
 * Strips all identifiable information from action traces
 * and replaces them with Lobster argument placeholders.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.sanitizeTrace = sanitizeTrace;
exports.sanitizeActionArgs = sanitizeActionArgs;
const PII_RULES = [
    {
        name: "email",
        pattern: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
        argType: "string",
    },
    {
        name: "phone",
        pattern: /\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/g,
        argType: "string",
    },
    {
        name: "card",
        pattern: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g,
        argType: "string",
    },
    {
        name: "ssn",
        pattern: /\b\d{3}-\d{2}-\d{4}\b/g,
        argType: "string",
    },
    {
        name: "password",
        pattern: /(?:password|passwd|pwd)\s*[:=]\s*\S+/gi,
        argType: "string",
    },
    {
        name: "api_key",
        pattern: /(?:api[_-]?key|token|secret)\s*[:=]\s*[A-Za-z0-9_\-]{16,}/gi,
        argType: "string",
    },
    {
        name: "ip_address",
        pattern: /\b(?:\d{1,3}\.){3}\d{1,3}\b/g,
        argType: "string",
    },
];
// Common user-input field names that likely contain personal data
const SENSITIVE_FIELD_NAMES = new Set([
    "username",
    "user_name",
    "first_name",
    "last_name",
    "full_name",
    "name",
    "email",
    "phone",
    "address",
    "street",
    "city",
    "zip",
    "zipcode",
    "postal_code",
    "ssn",
    "social_security",
    "credit_card",
    "card_number",
    "cvv",
    "expiry",
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "dob",
    "date_of_birth",
    "birthday",
]);
function sanitizeTrace(raw) {
    let result = raw;
    const extractedArgs = new Map();
    let argCounter = 0;
    // Pass 1: Regex-based PII detection
    for (const rule of PII_RULES) {
        const matches = result.match(rule.pattern);
        if (matches) {
            for (const match of new Set(matches)) {
                const argName = `${rule.name}_${argCounter++}`;
                const placeholder = `$LOBSTER_ARG_${argName.toUpperCase()}`;
                extractedArgs.set(argName, {
                    type: rule.argType,
                    placeholder,
                    originalPattern: rule.name,
                });
                result = result.replaceAll(match, placeholder);
            }
        }
        rule.pattern.lastIndex = 0;
    }
    return { sanitized: result, extractedArgs };
}
function sanitizeActionArgs(args) {
    const allExtracted = new Map();
    const sanitized = {};
    for (const [key, value] of Object.entries(args)) {
        const lowerKey = key.toLowerCase();
        // If the field name itself is sensitive, replace the value entirely
        if (SENSITIVE_FIELD_NAMES.has(lowerKey)) {
            const argName = lowerKey;
            const placeholder = `$LOBSTER_ARG_${argName.toUpperCase()}`;
            allExtracted.set(argName, {
                type: typeof value === "number" ? "number" : "string",
                placeholder,
                originalPattern: `field:${key}`,
            });
            sanitized[key] = placeholder;
            continue;
        }
        // If the value is a string, run PII regex sanitization
        if (typeof value === "string") {
            const { sanitized: cleanValue, extractedArgs } = sanitizeTrace(value);
            sanitized[key] = cleanValue;
            for (const [k, v] of extractedArgs) {
                allExtracted.set(k, v);
            }
        }
        else {
            sanitized[key] = value;
        }
    }
    return { sanitized, extractedArgs: allExtracted };
}
