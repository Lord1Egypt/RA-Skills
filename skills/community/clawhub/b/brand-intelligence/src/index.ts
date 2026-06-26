/**
 * sig.ai Brand Intelligence Plugin for OpenClaw
 *
 * Exposes 9 agent tools for searching, comparing, and analyzing
 * 5,600+ companies across 30 verticals via the geo.sig.ai API.
 */
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";
import { BrandApiClient } from "./client.ts";
import type { PluginConfig } from "./config.ts";
import { DEFAULT_CONFIG } from "./config.ts";

function json(data: unknown) {
  return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
}

export default definePluginEntry({
  id: "sigai-brand-intelligence",
  name: "Brand Intelligence",
  description: "Search, compare, and analyze 5,600+ companies across 30 verticals via geo.sig.ai",

  register(api) {
    const pluginCfg = (api.pluginConfig ?? {}) as Partial<PluginConfig>;
    const config: PluginConfig = {
      baseUrl: pluginCfg.baseUrl ?? DEFAULT_CONFIG.baseUrl,
      apiKey: pluginCfg.apiKey ?? DEFAULT_CONFIG.apiKey,
      timeoutMs: pluginCfg.timeoutMs ?? DEFAULT_CONFIG.timeoutMs,
    };
    const client = new BrandApiClient(config);

    // 1. Search brands (read-only, no opt-in needed)
    api.registerTool({
      name: "sigai_search_brands",
      description:
        "Search 5,600+ brands by name, vertical, or keyword. Returns compact list with slug, brand, vertical, signal, rank, tier.",
      parameters: Type.Object({
        query: Type.String({ description: "Search term" }),
        vertical: Type.Optional(Type.String({ description: "Filter by vertical" })),
        limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 50, description: "Max results" })),
      }),
      async execute(_id, params) {
        const data = await client.searchBrands(params.query, params.vertical, params.limit);
        return json(data);
      },
    });

    // 2. Get brand detail
    api.registerTool({
      name: "sigai_get_brand",
      description:
        "Get full brand profile: company overview, signal, FAQs, tier, vertical, tags, AI visibility score.",
      parameters: Type.Object({
        slug: Type.String({ description: "Brand slug (e.g. 'cursor', 'salesforce')" }),
      }),
      async execute(_id, params) {
        const data = await client.getBrand(params.slug);
        return json(data);
      },
    });

    // 3. Get brand brief
    api.registerTool({
      name: "sigai_get_brand_brief",
      description:
        "Get a concise, citation-ready brand summary (~500 chars) with source URL, confidence, and last_updated.",
      parameters: Type.Object({
        slug: Type.String({ description: "Brand slug" }),
      }),
      async execute(_id, params) {
        const data = await client.getBrandBrief(params.slug);
        return json(data);
      },
    });

    // 4. Get brand graph
    api.registerTool({
      name: "sigai_get_brand_graph",
      description:
        "Get knowledge graph: entity type, parent/children, competitive edges, integrations, acquisitions, capabilities.",
      parameters: Type.Object({
        slug: Type.String({ description: "Brand slug" }),
      }),
      async execute(_id, params) {
        const data = await client.getBrandGraph(params.slug);
        return json(data);
      },
    });

    // 5. Get brand digest
    api.registerTool({
      name: "sigai_get_brand_digest",
      description:
        "Compact intelligence digest for multiple brands: signals, AI visibility, edges, capabilities. Perfect for watchlist summaries.",
      parameters: Type.Object({
        slugs: Type.Array(Type.String(), { description: "Brand slugs (up to 25)", maxItems: 25 }),
        include: Type.Optional(
          Type.Array(Type.String(), { description: "Fields: signals, visibility, edges, capabilities" }),
        ),
      }),
      async execute(_id, params) {
        const data = await client.getBrandDigest(params.slugs, params.include);
        return json(data);
      },
    });

    // 6. Compare brands
    api.registerTool({
      name: "sigai_compare_brands",
      description:
        "Compare 2-5 brands: AI visibility delta, capabilities overlap, shared integrations, direct relationships, bottom-line summary.",
      parameters: Type.Object({
        slugs: Type.Array(Type.String(), { description: "2-5 brand slugs", minItems: 2, maxItems: 5 }),
      }),
      async execute(_id, params) {
        const data = await client.compareBrands(params.slugs);
        return json(data);
      },
    });

    // 7. Find alternatives
    api.registerTool({
      name: "sigai_find_alternatives",
      description:
        "Find alternatives to a brand using knowledge graph, shared capabilities, and category matching. Each alternative includes WHY it's an alternative.",
      parameters: Type.Object({
        slug: Type.String({ description: "Brand slug" }),
        limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 20 })),
      }),
      async execute(_id, params) {
        const data = await client.findAlternatives(params.slug, params.limit);
        return json(data);
      },
    });

    // 8. Get landscape
    api.registerTool({
      name: "sigai_get_landscape",
      description:
        "Get competitive landscape for a vertical: leaders, challengers, emerging brands, tier breakdown, AI visibility summary.",
      parameters: Type.Object({
        vertical: Type.String({ description: "Vertical slug (e.g. 'cybersecurity', 'artificial-intelligence')" }),
        limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 100 })),
      }),
      async execute(_id, params) {
        const data = await client.getLandscape(params.vertical, params.limit);
        return json(data);
      },
    });

    // 9. Find by capability
    api.registerTool({
      name: "sigai_find_by_capability",
      description:
        "Find brands by capability (e.g. 'code-generation', 'payment-processing'). Optionally filter by domain/vertical.",
      parameters: Type.Object({
        capability: Type.String({ description: "Capability keyword" }),
        domain: Type.Optional(Type.String({ description: "Filter by vertical" })),
        limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 50 })),
      }),
      async execute(_id, params) {
        const data = await client.findByCapability(params.capability, params.domain, params.limit);
        return json(data);
      },
    });
  },
});
