/**
 * Data models for claw-code-ts
 * Mirrored from Python src/models.py
 * Strict mode enabled.
 */
// ---------------------------------------------------------------------------
// Subsystem
// ---------------------------------------------------------------------------
export class Subsystem {
    constructor(args) {
        this.name = args.name;
        this.path = args.path;
        this.file_count = args.file_count;
        this.notes = args.notes;
    }
}
// ---------------------------------------------------------------------------
// PortingModule
// ---------------------------------------------------------------------------
export class PortingModule {
    constructor(args) {
        this.name = args.name;
        this.responsibility = args.responsibility;
        this.source_hint = args.source_hint;
        this.status = args.status ?? 'planned';
    }
}
// ---------------------------------------------------------------------------
// PermissionDenial
// ---------------------------------------------------------------------------
export class PermissionDenial {
    constructor(args) {
        this.tool_name = args.tool_name;
        this.reason = args.reason;
    }
}
// ---------------------------------------------------------------------------
// UsageSummary
// ---------------------------------------------------------------------------
export class UsageSummary {
    constructor(args) {
        this.input_tokens = args?.input_tokens ?? 0;
        this.output_tokens = args?.output_tokens ?? 0;
    }
    addTurn(prompt, output) {
        return new UsageSummary({
            input_tokens: this.input_tokens + prompt.split(/\s+/).filter(Boolean).length,
            output_tokens: this.output_tokens + output.split(/\s+/).filter(Boolean).length,
        });
    }
}
// ---------------------------------------------------------------------------
// PortingBacklog
// ---------------------------------------------------------------------------
export class PortingBacklog {
    constructor(args) {
        this.title = args?.title ?? '';
        this.modules = args?.modules ?? [];
    }
    summaryLines() {
        return this.modules.map((module) => `- ${module.name} [${module.status}] — ${module.responsibility} (from ${module.source_hint})`);
    }
}
