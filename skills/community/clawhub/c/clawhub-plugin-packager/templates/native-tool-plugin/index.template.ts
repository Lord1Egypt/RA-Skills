import { definePluginEntry } from "openclaw/plugin-sdk";

export default definePluginEntry(({ api, config }) => {
  api.registerTool({
    id: "{{TOOL_ID}}",
    description: "{{TOOL_DESCRIPTION}}",
    optional: {{OPTIONAL_FLAG}},
    inputSchema: {
      type: "object",
      properties: {
        input: { type: "string", description: "Primary text input." }
      },
      required: ["input"],
      additionalProperties: false
    },
    async run({ input }) {
      return {
        content: `{{DISPLAY_NAME}} received: ${input}`
      };
    }
  });

  return {
    name: "{{PLUGIN_ID}}"
  };
});
