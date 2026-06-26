"use strict";
/**
 * ClawWall Plugin — OpenClaw DLP Bridge
 *
 * Hooks into `before_tool_call` to scan outbound content via the
 * ClawWall Python service. Enforces BLOCK/REDACT decisions.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.beforeToolCall = beforeToolCall;
const DEFAULT_CONFIG = {
    serviceUrl: "http://127.0.0.1:8642",
    blockOnError: false,
    timeoutMs: 5000,
};
function extractContent(args) {
    const parts = [];
    for (const [key, value] of Object.entries(args)) {
        if (typeof value === "string") {
            parts.push(value);
        }
        else if (value !== null && value !== undefined) {
            parts.push(JSON.stringify(value));
        }
    }
    return parts.join("\n");
}
function inferDestination(toolName, args) {
    // Try common arg names for URLs/hosts
    for (const key of ["url", "endpoint", "host", "destination", "to"]) {
        const val = args[key];
        if (typeof val === "string") {
            try {
                return new URL(val).hostname;
            }
            catch {
                return val;
            }
        }
    }
    return undefined;
}
async function scanContent(content, config, context) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), config.timeoutMs);
    try {
        const resp = await fetch(`${config.serviceUrl}/api/v1/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                content,
                destination: context.destination ?? inferDestination(context.toolName, context.args),
                agent_id: context.agentId,
                tool_name: context.toolName,
            }),
            signal: controller.signal,
        });
        if (!resp.ok) {
            throw new Error(`ClawWall returned ${resp.status}`);
        }
        return (await resp.json());
    }
    finally {
        clearTimeout(timeout);
    }
}
async function promptUser(scan) {
    // Fall back to auto-deny if stdin is not a TTY
    if (!process.stdin.isTTY) {
        return false;
    }
    const readline = await Promise.resolve().then(() => __importStar(require("readline")));
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stderr,
    });
    console.error(`\n[ClawWall] ${scan.findings_count} finding(s) detected:`);
    for (const f of scan.findings) {
        console.error(`  - ${f.finding_type} (${f.severity})${f.redacted_snippet ? ": " + f.redacted_snippet : ""}`);
    }
    if (scan.suggested_action) {
        console.error(`  Suggested action: ${scan.suggested_action}`);
    }
    return new Promise((resolve) => {
        rl.question("[ClawWall] Allow this tool call? [y/N] ", (answer) => {
            rl.close();
            resolve(answer.trim().toLowerCase() === "y");
        });
    });
}
/**
 * Main hook export — called by OpenClaw before each tool call.
 */
async function beforeToolCall(context, pluginConfig) {
    const config = { ...DEFAULT_CONFIG, ...pluginConfig };
    const content = extractContent(context.args);
    if (!content.trim()) {
        return { allow: true };
    }
    let scan;
    try {
        scan = await scanContent(content, config, context);
    }
    catch (err) {
        // Service unreachable — fail-open or fail-closed based on config
        if (config.blockOnError) {
            return {
                allow: false,
                reason: `ClawWall service unreachable and blockOnError=true: ${err}`,
            };
        }
        return { allow: true };
    }
    switch (scan.action) {
        case "ALLOW":
            return { allow: true };
        case "BLOCK":
            return {
                allow: false,
                reason: `ClawWall BLOCKED: ${scan.findings_count} finding(s) detected — ${scan.findings.map((f) => f.finding_type).join(", ")}`,
            };
        case "REDACT":
            if (scan.content !== null) {
                // Replace all string args with the redacted content
                // This is a simplified approach — a production version would
                // map redaction offsets back to individual args
                const modifiedArgs = { ...context.args };
                for (const key of Object.keys(modifiedArgs)) {
                    if (typeof modifiedArgs[key] === "string") {
                        modifiedArgs[key] = scan.content;
                        break; // Only replace the first string arg for now
                    }
                }
                return { allow: true, modifiedArgs };
            }
            return { allow: true };
        case "PROMPT": {
            const approved = await promptUser(scan);
            if (!approved) {
                return {
                    allow: false,
                    reason: `ClawWall BLOCKED (user denied): ${scan.findings_count} finding(s) — ${scan.findings.map((f) => f.finding_type).join(", ")}`,
                };
            }
            // User approved — apply redaction if suggested action was REDACT
            if (scan.suggested_action === "REDACT" && scan.content !== null) {
                const modifiedArgs = { ...context.args };
                for (const key of Object.keys(modifiedArgs)) {
                    if (typeof modifiedArgs[key] === "string") {
                        modifiedArgs[key] = scan.content;
                        break;
                    }
                }
                return { allow: true, modifiedArgs };
            }
            return { allow: true };
        }
        default:
            return { allow: true };
    }
}
