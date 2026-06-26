import { definePluginEntry } from "openclaw/plugin-sdk";

export default definePluginEntry(({ api, config }) => {
  api.registerProvider({
    id: "{{PROVIDER_ID}}",
    description: "{{PROVIDER_DESCRIPTION}}"
  });

  return {
    name: "{{PLUGIN_ID}}"
  };
});
