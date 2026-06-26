import type { PluginConfig } from "./config.js";

const USER_AGENT = "sigai-openclaw-plugin/0.1.0";
const MAX_RETRIES = 2;
const RETRY_CODES = new Set([429, 500, 502, 503, 504]);

export class BrandApiClient {
  private baseUrl: string;
  private apiKey?: string;
  private timeoutMs: number;

  constructor(config: PluginConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, "");
    this.apiKey = config.apiKey;
    this.timeoutMs = config.timeoutMs;
  }

  private async request(path: string, options?: { method?: string; body?: unknown }): Promise<unknown> {
    const url = `${this.baseUrl}/api/public/brands${path}`;
    const headers: Record<string, string> = {
      "User-Agent": USER_AGENT,
      "Accept": "application/json",
    };
    if (this.apiKey) {
      headers["Authorization"] = `Bearer ${this.apiKey}`;
    }
    if (options?.body) {
      headers["Content-Type"] = "application/json";
    }

    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
      if (attempt > 0) {
        await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, attempt - 1)));
      }

      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), this.timeoutMs);

      try {
        const res = await fetch(url, {
          method: options?.method || "GET",
          headers,
          body: options?.body ? JSON.stringify(options.body) : undefined,
          signal: controller.signal,
        });

        clearTimeout(timer);

        if (res.ok) {
          return await res.json();
        }

        if (res.status === 404) {
          throw new Error("brand not found");
        }

        if (RETRY_CODES.has(res.status) && attempt < MAX_RETRIES) {
          lastError = new Error(`HTTP ${res.status}`);
          continue;
        }

        if (res.status === 429) {
          throw new Error("rate limited");
        }

        throw new Error(`HTTP ${res.status}`);
      } catch (err) {
        clearTimeout(timer);
        if (err instanceof Error && err.name === "AbortError") {
          lastError = new Error("backend unavailable");
          if (attempt < MAX_RETRIES) continue;
        }
        throw err;
      }
    }

    throw lastError || new Error("backend unavailable");
  }

  async searchBrands(query: string, vertical?: string, limit?: number) {
    const params = new URLSearchParams({ q: query });
    if (vertical) params.set("vertical", vertical);
    if (limit) params.set("limit", String(limit));
    return this.request(`/search?${params}`);
  }

  async getBrand(slug: string) {
    return this.request(`/brand/${encodeURIComponent(slug)}`);
  }

  async getBrandBrief(slug: string) {
    return this.request(`/brand/${encodeURIComponent(slug)}/brief`);
  }

  async getBrandGraph(slug: string) {
    return this.request(`/brand/${encodeURIComponent(slug)}/graph`);
  }

  async getBrandDigest(slugs: string[], include?: string[]) {
    return this.request("/digest", {
      method: "POST",
      body: { slugs, ...(include ? { include } : {}) },
    });
  }

  async compareBrands(slugs: string[]) {
    const params = new URLSearchParams();
    slugs.forEach((s) => params.append("slugs", s));
    return this.request(`/compare?${params}`);
  }

  async findAlternatives(slug: string, limit?: number) {
    const params = limit ? `?limit=${limit}` : "";
    return this.request(`/brand/${encodeURIComponent(slug)}/alternatives${params}`);
  }

  async getLandscape(verticalSlug: string, limit?: number) {
    const params = limit ? `?limit=${limit}` : "";
    return this.request(`/vertical/${encodeURIComponent(verticalSlug)}${params}`);
  }

  async findByCapability(capability: string, domain?: string, limit?: number) {
    const params = new URLSearchParams({ q: capability });
    if (domain) params.set("domain", domain);
    if (limit) params.set("limit", String(limit));
    return this.request(`/capabilities/search?${params}`);
  }
}
