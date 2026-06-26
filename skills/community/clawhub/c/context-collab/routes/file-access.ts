/**
 * Context Plugin — HTTP Route for Viral Propagation
 *
 * When another agent fetches a Context URL:
 * - Has plugin → proxies to server with X-Context-Plugin header → gets content
 * - No plugin → server returns installation guidance markdown
 *
 * This route is registered on the OpenClaw gateway so that
 * agents with the plugin can transparently access shared files.
 */

import type { IncomingMessage, ServerResponse } from "node:http";

const CTX_BASE = "http://localhost:3100";

/**
 * Handle /ctx/:spaceId/* requests through the OpenClaw gateway.
 * Adds X-Context-Plugin header so the server knows this agent has the plugin.
 */
export async function handleContextFileRoute(req: IncomingMessage, res: ServerResponse): Promise<boolean> {
  const url = req.url || "";

  // Only handle /ctx/ paths
  if (!url.startsWith("/ctx/")) return false;

  try {
    // Proxy to context server with plugin header
    const proxyRes = await fetch(`${CTX_BASE}${url}`, {
      headers: { "X-Context-Plugin": "true" },
      signal: AbortSignal.timeout(8000),
    });

    const contentType = proxyRes.headers.get("content-type") || "text/plain";
    const body = await proxyRes.text();

    res.writeHead(proxyRes.status, { "Content-Type": contentType });
    res.end(body);
    return true;
  } catch (err: any) {
    res.writeHead(502, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Context server unavailable: " + err.message }));
    return true;
  }
}
