"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildPatchSuggestion = buildPatchSuggestion;
function buildPatchSuggestion(args) {
    return {
        path: args.path,
        kind: args.kind,
        summary: args.summary,
        before: args.before,
        after: args.after
    };
}
//# sourceMappingURL=PatchSuggestion.js.map