import type { Provider } from "../types";
import { LOGIN_URLS } from "../core/auth";
import { codexbarAvailable, codexbarPlugin, codexbarUsage, extractPluginSnapshot, extractUsageSnapshot } from "../core/codexbar";
import { errorSnapshot } from "../core/snapshot";

/** Factory: web-session providers served by the CodexBar menu-bar app.
 *  (claude / gemini / kimi / openrouter) */
export function codexbarProvider(id: string, label: string): Provider {
  return {
    id,
    label,
    loginUrl: LOGIN_URLS[id],

    async detect() {
      return codexbarAvailable()
        ? { configured: true, source: "codexbar" }
        : { configured: false, reason: "codexbar CLI not installed" };
    },

    async fetch() {
      if (!codexbarAvailable()) {
        return errorSnapshot(id, "codexbar CLI not installed — install CodexBar to read this provider", "codexbar", LOGIN_URLS[id]);
      }
      const items = codexbarUsage(id);
      const item = items[0];
      if (!item) {
        return errorSnapshot(id, `codexbar usage returned no data — run: codexbar usage --provider ${id}`, "codexbar", LOGIN_URLS[id]);
      }
      return extractUsageSnapshot(item);
    },
  };
}

/** apikey.fun relay wallet via the CodexBar JS plugin (`plugins fetch`). */
export const apikeyfunProvider: Provider = {
  id: "apikeyfun",
  label: "apikey.fun relay",
  loginUrl: LOGIN_URLS.apikeyfun,

  async detect() {
    return codexbarAvailable()
      ? { configured: true, source: "codexbar-plugin" }
      : { configured: false, reason: "codexbar CLI not installed" };
  },

  async fetch() {
    if (!codexbarAvailable()) {
      return errorSnapshot("apikeyfun", "codexbar CLI not installed", "codexbar-plugin", LOGIN_URLS.apikeyfun);
    }
    const data = codexbarPlugin("apikeyfun");
    if (!data) {
      return errorSnapshot(
        "apikeyfun",
        "plugin fetch failed — run: codexbar plugins fetch apikeyfun (approve once interactively)",
        "codexbar-plugin",
        LOGIN_URLS.apikeyfun,
      );
    }
    return extractPluginSnapshot(data, "apikeyfun");
  },
};
