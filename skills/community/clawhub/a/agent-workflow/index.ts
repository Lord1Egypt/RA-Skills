// index.ts
// Plugin entry point. Registers the agent_workflow tool with OpenClaw.

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";
import { fileURLToPath } from "node:url";
import { WorkflowEngine } from "./src/workflow-engine.js";
import { StateStore } from "./src/state-store.js";
import { SkillLoader } from "./src/skill-loader.js";
import path from "node:path";
import os from "node:os";

export default definePluginEntry({
  id: "agent-workflow",
  name: "Agent Workflow",
  description: "Structured workflow engine with persistent state, branching, and multi-project support.",

  register(api) {
    // Resolve storage directory
    const storageDir: string =
      (api.pluginConfig?.storageDir as string | undefined) ??
      path.join(os.homedir(), ".openclaw", "workspace");

    const maxForks: number =
      (api.pluginConfig?.maxForks as number | undefined) ?? 3;

    // Plugin root: prefer api.rootDir (always reliable), fall back to fileURLToPath
    // which correctly handles Windows paths (unlike raw import.meta.url.pathname)
    const pluginRoot = api.rootDir ?? path.dirname(fileURLToPath(import.meta.url));

    const store = new StateStore(storageDir);
    const skillLoader = new SkillLoader(pluginRoot);
    const engine = new WorkflowEngine(store, skillLoader, maxForks);

    // ── Register the agent_workflow tool ──────────────────────────────────────

    api.registerTool(() => ({
      name: "agent_workflow",
      label: "Agent Workflow",
      description: [
        "Navigate and manage structured workflows with persistent state.",
        "Supports brainstorm → plan → execute → verify → deliver with branching,",
        "parallel context-plugins, and multi-project concurrency.",
        "",
        "Actions:",
        "  start        — Begin a new workflow (auto-extracts projectName from context)",
        "  status       — View current state (omit workflowId to see all active)",
        "  next         — Advance to the next step (specify branch at branch points)",
        "  goto         — Jump to any node (soft guard warns about skipped steps)",
        "  complete     — Mark current node done, stay in place until next() is called",
        "  fork         — Activate a context-plugin without leaving the main flow",
        "  join         — Complete a fork and return to main flow",
        "  getSkill     — Load full SKILL.md content for a node (call after next/goto)",
        "  list         — List workflows (filter by status)",
        "  abandon      — Abandon a workflow",
      ].join("\n"),

      parameters: Type.Object({
        action: Type.Union([
          Type.Literal("start"),
          Type.Literal("status"),
          Type.Literal("next"),
          Type.Literal("goto"),
          Type.Literal("complete"),
          Type.Literal("fork"),
          Type.Literal("join"),
          Type.Literal("getSkill"),
          Type.Literal("list"),
          Type.Literal("abandon"),
        ]),

        // start
        projectName: Type.Optional(Type.String({
          description: "Project name. Extract from the user's conversation context and pass explicitly. Falls back to 'Untitled Project' if omitted.",
        })),

        // most state actions
        workflowId: Type.Optional(Type.String({
          description: "Target workflow ID. Required for next/goto/complete/fork/join/abandon.",
        })),

        // next
        branch: Type.Optional(Type.String({
          description: "Branch id to follow at a branch point (e.g. 'subagent' or 'sequential').",
        })),

        // goto / getSkill / fork
        step: Type.Optional(Type.String({
          description: [
            "Purpose depends on action:",
            "  goto: target node id to jump to",
            "  getSkill: node name whose SKILL.md to load",
            "  fork: context-plugin name to activate (one of: dispatching-parallel-agents, requesting-review, receiving-review)",
          ].join(" "),
        })),

        // join
        forkId: Type.Optional(Type.String({
          description: "Fork ID returned by fork(), required for join().",
        })),

        // complete / join
        note: Type.Optional(Type.String({
          description: "Optional note or summary to attach to the completed step.",
        })),

        // complete
        output: Type.Optional(Type.Any({
          description: "Optional structured output from the completed step.",
        })),

        // list
        status: Type.Optional(Type.String({
          description: "Filter workflows by status: active | paused | completed | abandoned.",
        })),
      }),

      async execute(_id, params) {
        let result: unknown;

        try {
          switch (params.action) {

            case "start": {
              const name = params.projectName ?? "Untitled Project";
              result = engine.start(name);
              break;
            }

            case "status": {
              result = engine.status(params.workflowId);
              break;
            }

            case "next": {
              if (!params.workflowId) {
                result = { ok: false, message: "workflowId is required for next()." };
                break;
              }
              result = engine.next(params.workflowId, params.branch);
              break;
            }

            case "goto": {
              if (!params.workflowId || !params.step) {
                result = { ok: false, message: "workflowId and step are required for goto()." };
                break;
              }
              result = engine.goto(params.workflowId, params.step);
              break;
            }

            case "complete": {
              if (!params.workflowId) {
                result = { ok: false, message: "workflowId is required for complete()." };
                break;
              }
              result = engine.complete(params.workflowId, params.note, params.output);
              break;
            }

            case "fork": {
              if (!params.workflowId || !params.step) {
                result = { ok: false, message: "workflowId and step (plugin name) are required for fork()." };
                break;
              }
              result = engine.fork(params.workflowId, params.step);
              break;
            }

            case "join": {
              if (!params.workflowId || !params.forkId) {
                result = { ok: false, message: "workflowId and forkId are required for join()." };
                break;
              }
              result = engine.join(params.workflowId, params.forkId, params.note);
              break;
            }

            case "getSkill": {
              if (!params.step) {
                result = { ok: false, message: "step (node name) is required for getSkill()." };
                break;
              }
              result = engine.getSkill(params.step);
              break;
            }

            case "list": {
              result = engine.list(params.status);
              break;
            }

            case "abandon": {
              if (!params.workflowId) {
                result = { ok: false, message: "workflowId is required for abandon()." };
                break;
              }
              result = engine.abandon(params.workflowId);
              break;
            }

            default:
              result = { ok: false, message: `Unknown action: ${String(params.action)}` };
          }
        } catch (err: unknown) {
          const msg = err instanceof Error ? err.message : String(err);
          api.logger.error(`[agent-workflow] Unexpected error in execute(): ${err instanceof Error ? err.message : String(err)}`);
          result = { ok: false, error: { code: "UNKNOWN", message: msg }, message: msg };
        }

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
          details: {},
        };
      },
    }));

    api.logger.info("agent-workflow plugin registered. Storage: " + storageDir);
  },
});
