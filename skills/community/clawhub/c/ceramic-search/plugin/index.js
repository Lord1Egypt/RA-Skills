import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
const S = (s) => s;
const PARAMS_SCHEMA = S({
  type: "object",
  properties: {
    query: {
      type: "string",
      description: "Natural language search query from the user or agent."
    },
    maxDescriptionLength: {
      type: "number",
      description: "Max characters per result description (1000\u20138000). Defaults to 3000.",
      minimum: 1e3,
      maximum: 8e3
    }
  },
  required: ["query"]
});
var index_default = definePluginEntry({
  id: "ceramic-search",
  name: "Ceramic Search",
  description: "Web search for AI agents.",
  register(api) {
    api.registerTool({
      name: "ceramic_search",
      label: "Ceramic Search",
      description: [
        "Search the web using Ceramic.",
        "Use for accurate current information — news, prices, recent events, documentation, general fact checking.",
        "Returns up to 10 ranked results with titles, URLs, and descriptions."
      ].join(" "),
      parameters: PARAMS_SCHEMA,
      async execute(_toolCallId, rawParams, signal) {
        const params = rawParams;
        const pluginConfig = api.pluginConfig;
        const apiKey = pluginConfig?.apiKey ?? process.env.CERAMIC_API_KEY ?? "";
        if (!apiKey) {
          return {
            content: [
              {
                type: "text",
                text: [
                  "Error: Ceramic API key is not configured.",
                  "Set it with:",
                  "  openclaw config set plugins.entries.ceramic-search.config.apiKey YOUR_KEY",
                  "or export CERAMIC_API_KEY=YOUR_KEY in the gateway environment."
                ].join("\n")
              }
            ],
            details: { status: "error", error: "missing_api_key" }
          };
        }
        let keywordQueries;
        let rewriteError;
        try {
          const llmResult = await api.runtime.llm.complete({
            purpose: "ceramic_search: query rewrite",
            systemPrompt: [
              "Rewrite the user's natural language query into 1\u20133 keyword-based search queries for Ceramic's lexical search engine.",
              "Ceramic matches exact keywords \u2014 it does not interpret natural language or synonyms automatically.",
              "",
              "Rules:",
              "- Queries must be 2-8 words.",
              "- Extract specific entities, topics, locations, and dates.",
              "- Replace conversational phrasing with concrete keywords.",
              "- Do not include uninformative words such as articles (the, a, an). Avoid prepositions (on, about, in, for, of, at, by, with) unless they are within established phrases or names (United States of America, Into the Wild).",
              "- Include relevant synonyms explicitly when terminology is ambiguous.",
              "- Keep word order meaningful (`house cat` and `cat house` return different results).",
              "",
              "Good keyword query examples:",
              '- "2026 Super Bowl halftime performer"',
              '- "climate change effects global warming impact"',
              '- "beginner investing strategies stocks bonds basics"',
              "",
              "Return ONLY a JSON array of strings with no markdown or explanation.",
              'Example: ["large language model news 2025", "LLM benchmarks latest research"]'
            ].join("\n"),
            messages: [{ role: "user", content: params.query }],
            maxTokens: 200,
            temperature: 0
          });
          const parsed = JSON.parse(llmResult.text.trim());
          if (Array.isArray(parsed) && parsed.length > 0 && parsed.every((q) => typeof q === "string")) {
            keywordQueries = parsed.slice(0, 3);
          } else {
            throw new Error("unexpected shape");
          }
        } catch (err) {
          keywordQueries = [params.query];
          rewriteError = err instanceof Error ? err.message : String(err);
        }
        const maxDescriptionLength = params.maxDescriptionLength ?? 3e3;
        const responses = await Promise.all(
          keywordQueries.map(async (kq) => {
            const res = await fetch("https://api.ceramic.ai/search", {
              method: "POST",
              headers: {
                Authorization: `Bearer ${apiKey}`,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({ query: kq, maxDescriptionLength }),
              signal: signal ?? void 0
            });
            if (!res.ok) {
              const body = await res.text().catch(() => "");
              throw new Error(
                `Ceramic API ${res.status} for query "${kq}": ${body}`
              );
            }
            return res.json();
          })
        );
        const seen = /* @__PURE__ */ new Set();
        const merged = [];
        for (const resp of responses) {
          for (const item of resp.result.results) {
            if (!seen.has(item.url)) {
              seen.add(item.url);
              merged.push(item);
            }
          }
        }
        if (merged.length === 0) {
          return {
            content: [
              {
                type: "text",
                text: `No results found for: ${params.query}`
              }
            ],
            details: {
              query: params.query,
              keywordQueries,
              results: [],
              totalResults: 0,
              ...rewriteError ? { rewriteError } : {}
            }
          };
        }
        const queryList = keywordQueries.map((q) => `"${q}"`).join(", ");
        const resultLines = merged.map((r, i) => `[${i + 1}] ${r.title}
${r.url}
${r.description}`).join("\n\n");
        const text = `Found ${merged.length} result${merged.length === 1 ? "" : "s"} for "${params.query}" (keyword queries: ${queryList}):

` + resultLines;
        return {
          content: [{ type: "text", text }],
          details: {
            query: params.query,
            keywordQueries,
            results: merged,
            totalResults: merged.length,
            ...rewriteError ? { rewriteError } : {}
          }
        };
      }
    });
  }
});
export {
  index_default as default
};
