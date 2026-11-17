// Browser page.fetch facade. Open API transport stays unimplemented for testcase.

import { BASE, parseLooseJson } from "./pure.mjs";

export function createTransport(kind, session) {
  const name = kind || "browser";
  if (name === "browser") {
    if (!session || typeof session.fetch !== "function") {
      throw new Error("browser transport requires a page session");
    }
    return {
      kind: "browser",
      implemented: true,
      async request(url, opts) {
        return session.fetch(url, opts);
      },
    };
  }
  if (name === "open" || name === "open-api") {
    return {
      kind: "open",
      implemented: false,
      phase: 2,
      async request() {
        const error = new Error(
          "Open API transport is not implemented in Phase 1. Test plans and test cases, including Phase 2a writes, use the browser session on https://www.teambition.com (testcase/api and /api/testcases/{id}/archive), not a teambition_cli or MCP token.",
        );
        error.code = "TRANSPORT_NOT_IMPLEMENTED";
        throw error;
      },
    };
  }
  throw new Error(`Unknown transport: ${name}`);
}

export function createPageSession({ task, page, base = BASE, pageName = "p1" } = {}) {
  if (!task || !page) throw new Error("createPageSession requires task and page");
  let finished = false;
  return {
    spaceId: task.spaceId,
    async ensureSite() {
      let current = "";
      try {
        current = await page.url();
      } catch {
        current = "";
      }
      if (!current || !String(current).includes("teambition.com")) {
        await page.goto(base);
        if (typeof page.waitForLoadState === "function") await page.waitForLoadState();
      }
    },
    async fetch(url, opts = {}) {
      const timeout = opts.timeout ?? 30_000;
      const method = opts.method ? String(opts.method).toUpperCase() : "";
      const init = { timeout };
      if (method && method !== "GET") {
        init.method = method;
        init.credentials = "include";
        if (opts.body !== undefined && opts.body !== null) {
          init.headers = {
            "content-type": "application/json",
            ...(opts.headers || {}),
          };
          init.body = typeof opts.body === "string" ? opts.body : JSON.stringify(opts.body);
        }
      }
      const response = await page.fetch(url, init);
      const raw = response ? response.body : undefined;
      const body = typeof raw === "string" || raw == null ? parseLooseJson(raw) : raw;
      return { status: response ? response.status : 0, body };
    },
    async finish(options = {}) {
      if (finished) return;
      finished = true;
      await task.finish({ keep: options.keep ? [pageName] : [] });
    },
    async cleanup() {
      finished = true;
      await task.finish({ keep: [] });
    },
    async handOff() {
      if (typeof task.handOff === "function") await task.handOff();
    },
  };
}
