"use strict";
/**
 * Baozi Claw - OpenClaw Skill
 *
 * Main entry point for the baozi-claw skill.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.tools = void 0;
const exampleTool = {
    name: "example-tool",
    description: "An example tool for baozi-claw.",
    execute: async (args) => {
        const input = args.input;
        return {
            success: true,
            data: `Processed: ${input}`,
        };
    },
};
exports.tools = [exampleTool];
exports.default = {
    metadata: {
        name: "baozi-claw",
        description: "An OpenClaw skill.",
        version: "0.1.0",
    },
    tools: exports.tools,
};
//# sourceMappingURL=index.js.map