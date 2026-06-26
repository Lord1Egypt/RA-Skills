import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

export default definePluginEntry({
  id: "resilience-guard",
  name: "Resilience Guard",
  description: "Opens the external OpenClaw Gateway Resilience Guard dashboard.",
  register(api) {
    if (api.registrationMode !== "full") return;
    const dashboardUrl = String(api.pluginConfig?.dashboardUrl || "http://127.0.0.1:18790/");

    api.registerHttpRoute({
      path: "/resilience-guard",
      auth: "gateway",
      match: "exact",
      replaceExisting: true,
      async handler(_req, res) {
        res.statusCode = 302;
        res.setHeader("Location", dashboardUrl);
        res.end(`Redirecting to ${escapeHtml(dashboardUrl)}`);
        return true;
      },
    });

    api.registerHttpRoute({
      path: "/resilience-guard/info",
      auth: "gateway",
      match: "exact",
      replaceExisting: true,
      async handler(_req, res) {
        const body = JSON.stringify({
          ok: true,
          dashboardUrl,
          note: "The external dashboard is served by the watchdog service, so it can stay available when Gateway is down.",
        });
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/json; charset=utf-8");
        res.end(body);
        return true;
      },
    });
  },
});
