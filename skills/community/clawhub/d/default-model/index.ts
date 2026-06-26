import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

/**
 * default_model plugin
 *
 * /default_model           → show current default model from config
 * /default_model <model>   → set default model persistently (agents.defaults.model.primary)
 *
 * On Telegram, also registers an interactive handler for defmdl_* callbacks
 * so users can pick a model with inline buttons.
 */

function getProviders(cfg) {
  const entries = cfg?.models?.providers;
  if (!entries || typeof entries !== "object") return [];
  return Object.keys(entries);
}

function getModelsForProvider(cfg, provider) {
  const provCfg = cfg?.models?.providers?.[provider];
  if (!provCfg) return [];
  const models = provCfg.models;
  if (!Array.isArray(models)) return [];
  return models
    .map((m) => (typeof m === "string" ? m : m?.id))
    .filter(Boolean);
}

function resolveDefaultModel(cfg) {
  const model = cfg?.agents?.defaults?.model;
  if (typeof model === "string") return model;
  if (model && typeof model === "object" && model.primary) return String(model.primary);
  return null;
}

function buildByProvider(cfg) {
  const map = new Map();
  for (const prov of getProviders(cfg)) {
    const models = getModelsForProvider(cfg, prov);
    if (models.length > 0) map.set(prov, models);
  }
  return map;
}

export default definePluginEntry({
  id: "default-model",
  name: "Default Model",
  description: "Set the default model persistently via /default_model command",

  register(api) {
    // ─── /default_model command ───────────────────────────────────
    api.registerCommand({
      name: "default_model",
      description: "Show or set the default model (persists to config file).",
      acceptsArgs: true,
      requireAuth: true,
      handler: async (ctx) => {
        const arg = (ctx.args ?? "").trim();

        // ── No args: show current default + provider picker on Telegram ──
        if (!arg) {
          const current = resolveDefaultModel(ctx.config) ?? "not set";
          const byProvider = buildByProvider(ctx.config);
          const providers = [...byProvider.keys()];

          // Telegram → interactive picker
          if (ctx.channel === "telegram" && providers.length > 0) {
            const rows = [];
            for (let i = 0; i < providers.length; i += 2) {
              const row = [];
              for (const prov of providers.slice(i, i + 2)) {
                const count = byProvider.get(prov)?.length ?? 0;
                row.push({
                  text: `${prov} (${count})`,
                  callback_data: `defmdl:list_${prov}_1`,
                });
              }
              rows.push(row);
            }

            return {
              text: [
                `📋 **Default model (config):** \`${current}\``,
                "",
                "Select a provider to choose default model:",
              ].join("\n"),
              channelData: {
                telegram: { buttons: rows },
              },
            };
          }

          // Other channels → text instructions
          return {
            text: [
              `📋 **Default model (config):** \`${current}\``,
              "",
              "Usage: `/default_model <model-id>`",
              "Example: `/default_model openrouter/stepfun/step-3.5-flash:free`",
              "",
              "This sets the default model in the config file.",
              "Changes persist across restarts.",
            ].join("\n"),
          };
        }

        // ── With args: set default model ──────────────────────────
        const cfg = api.runtime.config.loadConfig();
        const byProvider = buildByProvider(cfg);
        const current = resolveDefaultModel(cfg) ?? "not set";

        // Try to resolve the model: accept provider/model or plain model name
        let normalizedModel = null;

        if (arg.includes("/")) {
          // Full provider/model format
          const slashIdx = arg.indexOf("/");
          const provider = arg.slice(0, slashIdx);
          const modelId = arg.slice(slashIdx + 1);
          const models = byProvider.get(provider);
          if (models && models.includes(modelId)) {
            normalizedModel = `${provider}/${modelId}`;
          } else {
            // Allow it anyway — the model might exist but not be in the catalog
            normalizedModel = arg;
          }
        } else {
          // Plain model name — search across providers
          for (const [prov, models] of byProvider) {
            if (models.includes(arg)) {
              normalizedModel = `${prov}/${arg}`;
              break;
            }
          }
          if (!normalizedModel) {
            // Try matching as a known alias from config
            const aliases = cfg?.agents?.defaults?.models;
            if (aliases && typeof aliases === "object") {
              for (const [fullId, entry] of Object.entries(aliases)) {
                if (entry && typeof entry === "object" && entry.alias === arg) {
                  normalizedModel = fullId;
                  break;
                }
              }
            }
          }
          if (!normalizedModel) {
            return {
              text: [
                `⚠️ Unknown model: \`${arg}\``,
                "",
                "Use format: `provider/model` or a known model alias.",
                "",
                "Available providers:",
                ...getProviders(cfg).map((p) => `  • ${p}`),
              ].join("\n"),
            };
          }
        }

        // Update config
        const configBase = JSON.parse(JSON.stringify(cfg));
        const agentsSection = (configBase.agents ??= {});
        const defaultsSection = (agentsSection.defaults ??= {});
        const modelSection = defaultsSection.model;

        if (modelSection && typeof modelSection === "object" && !Array.isArray(modelSection)) {
          modelSection.primary = normalizedModel;
        } else {
          defaultsSection.model = { primary: normalizedModel };
        }

        try {
          await api.runtime.config.writeConfigFile(configBase);
        } catch (err) {
          return {
            text: `⚠️ Failed to write config: ${String(err)}`,
          };
        }

        return {
          text: [
            `✅ **Default model updated!**`,
            "",
            `**Before:** \`${current}\``,
            `**After:** \`${normalizedModel}\``,
            "",
            "• Config file updated (persists across restarts)",
            "• New sessions will use this model by default",
            "• Current session model unchanged (use `/model` to change)",
          ].join("\n"),
        };
      },
    });

    // ─── Telegram interactive handler for defmdl_* callbacks ──────
    api.registerInteractiveHandler({
      channel: "telegram",
      namespace: "defmdl",
      handler: async (ctx) => {
        const payload = ctx.callback.payload; // e.g. "list_openrouter_1" or "sel_openrouter/gpt-4"

        const cfg = api.runtime.config.loadConfig();
        const byProvider = buildByProvider(cfg);

        // ── List models for a provider: list_{provider}_{page} ──
        const listMatch = payload.match(/^list_(.+)_(\d+)$/);
        if (listMatch) {
          const provider = listMatch[1];
          const page = parseInt(listMatch[2], 10);
          const models = byProvider.get(provider) ?? [];

          if (models.length === 0) {
            await ctx.respond.editMessage({
              text: `No models found for ${provider}.`,
              buttons: [],
            });
            return { handled: true };
          }

          const sorted = [...models].sort();
          const pageSize = 8;
          const totalPages = Math.max(1, Math.ceil(sorted.length / pageSize));
          const safePage = Math.max(1, Math.min(page, totalPages));
          const start = (safePage - 1) * pageSize;
          const pageModels = sorted.slice(start, start + pageSize);

          const rows = [];
          for (const model of pageModels) {
            const cb = `defmdl:sel_${provider}/${model}`;
            if (Buffer.byteLength(cb, "utf-8") <= 64) {
              rows.push([{ text: model, callback_data: cb }]);
            }
          }

          // Pagination
          if (totalPages > 1) {
            const pagRow = [];
            if (safePage > 1) {
              pagRow.push({
                text: "◀ Prev",
                callback_data: `defmdl:list_${provider}_${safePage - 1}`,
              });
            }
            if (safePage < totalPages) {
              pagRow.push({
                text: "Next ▶",
                callback_data: `defmdl:list_${provider}_${safePage + 1}`,
              });
            }
            rows.push(pagRow);
          }

          await ctx.respond.editMessage({
            text: `Select default model for ${provider} (${models.length} models, page ${safePage}/${totalPages}):`,
            buttons: rows,
          });
          return { handled: true };
        }

        // ── Select model: sel_{provider}/{model} ──────────────
        const selMatch = payload.match(/^sel_(.+)$/);
        if (selMatch) {
          if (!ctx.auth.isAuthorizedSender) {
            await ctx.respond.reply({
              text: "❌ Not authorized to change default model.",
            });
            return { handled: true };
          }

          const rawModel = selMatch[1];
          const slashIdx = rawModel.indexOf("/");
          if (slashIdx < 0) {
            await ctx.respond.editMessage({
              text: "❌ Invalid model selection.",
              buttons: [],
            });
            return { handled: true };
          }

          const provider = rawModel.slice(0, slashIdx);
          const modelId = rawModel.slice(slashIdx + 1);

          // Validate model is still available
          const models = byProvider.get(provider);
          if (!models || !models.includes(modelId)) {
            await ctx.respond.editMessage({
              text: "❌ Model no longer available. Provider or model list may have changed.",
              buttons: [],
            });
            return { handled: true };
          }

          const normalizedModel = `${provider}/${modelId}`;
          const current = resolveDefaultModel(cfg) ?? "not set";

          // Update config
          const configBase = JSON.parse(JSON.stringify(cfg));
          const agentsSection = (configBase.agents ??= {});
          const defaultsSection = (agentsSection.defaults ??= {});
          const modelSection = defaultsSection.model;

          if (modelSection && typeof modelSection === "object" && !Array.isArray(modelSection)) {
            modelSection.primary = normalizedModel;
          } else {
            defaultsSection.model = { primary: normalizedModel };
          }

          try {
            await api.runtime.config.writeConfigFile(configBase);
            await ctx.respond.editMessage({
              text: [
                `✅ **Default model updated!**`,
                "",
                `**Before:** \`${current}\``,
                `**After:** \`${normalizedModel}\``,
                "",
                "• Config file updated (persists across restarts)",
                "• New sessions will use this model",
              ].join("\n"),
              buttons: [],
            });
          } catch (err) {
            await ctx.respond.editMessage({
              text: `⚠️ Failed to write config: ${String(err)}`,
              buttons: [],
            });
          }
          return { handled: true };
        }

        return { handled: false };
      },
    });
  },
});
