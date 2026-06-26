import { definePluginEntry } from "openclaw/plugin-sdk";

export default definePluginEntry(({ api, config }) => {
  api.registerChannel({
    id: "{{CHANNEL_ID}}",
    description: "{{CHANNEL_DESCRIPTION}}"
  });

  return {
    name: "{{PLUGIN_ID}}"
  };
});
