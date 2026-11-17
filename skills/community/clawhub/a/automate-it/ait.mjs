#!/usr/bin/env node
// ait — Automate It CLI for AI agents.
//
// Zero-dependency ESM script (Node 18+ or Bun). Speaks the Model Context
// Protocol (StreamableHTTP, stateless) to Automate It's public MCP server,
// authenticating with an API key (ak_*). Every command goes through MCP —
// there is no REST path.
//
// The command surface is a closed set: every tool the workspace MCP server
// exposes has exactly one named command here, and there is no generic
// passthrough. Adding a tool to the server means adding its command here —
// that's deliberate, so the skill's capabilities can be read off its docs.
// Scopes and workspace role still bound what runs, enforced server-side, and
// tools that destroy data additionally require an explicit --yes.
//
// Tool output is printed verbatim on stdout; errors go to stderr as
// {"error": "..."} with exit code 1.

import { pathToFileURL } from "node:url";
import { realpathSync } from "node:fs";

const DEFAULT_API_URL = "https://api.automate.it.com";
const REQUEST_TIMEOUT_MS = 120_000;
const PUBLISH_MODES = ["immediate", "scheduled", "manual"];

export const USAGE = `ait — Automate It CLI for AI agents

Environment:
  AUTOMATE_IT_API_KEY    (required) API key (ak_*), created in Profile → API keys
  AUTOMATE_IT_API_URL    API base URL (default: ${DEFAULT_API_URL}). Must be
                         https:// — plain http:// is only allowed for
                         localhost, 127.0.0.1, or [::1] (local dev).
  AUTOMATE_IT_WORKSPACE  Default workspace id (else pass --workspace, else
                         auto-resolved when the key has exactly one workspace)

Destructive commands (task delete, task delete-content, task clear-content,
automation delete, folders delete, skills delete) permanently remove data and
refuse to run without --yes. Only pass it when the operator asked for that
deletion by name.

Discovery:
  ait workspaces                       List workspaces the key can access,
                                       each with its memory entries
  ait whoami                           Show the user this key acts as
  ait integrations                     Platforms connected for publishing

Tasks (the review-gate loop):
  ait task create --title <t>          Create a task
      [--instructions <text>] [--output-types x,linkedin,...]
      [--publish-mode manual|immediate|scheduled] [--publish-at <ISO date>]
      Omitted --publish-mode falls back to the workspace's default publish
      mode; scheduled without --publish-at auto-schedules at approval.
      [--no-review] [--claim] [--skills <names or ids>] [--assign <userId|me>]
      --claim creates the task already claimed (status "working") so the
      built-in worker never picks it up — use it when YOU will generate the
      content, then: task add-content → task complete.
      --skills accepts skill names or ids (see \`ait skills list\`).
      --assign gives the task to a workspace member; the built-in worker
      skips assigned tasks and the assignee works them.
  ait task submit --title <t> --body <text>
      [--type <contentType>] [--media '<json array>'] [same flags as create]
      [--link-url <url>] [--link-action learn_more|book|order|buy|sign_up]
      [--topic <topic>]
      One-shot: creates the task WITH finished content — it skips todo/working
      and lands directly in the human review queue.
  ait task list [--status <s>] [--mine] [--limit <n>] [--offset <n>]
      --mine filters to tasks assigned to you (find your agent's work with
      --mine --status todo).
                                       Statuses: todo working review approved
                                       publishing published deleted failed
  ait task get <taskId>                Full task detail, incl. reviewer comments
                                       and the memory entries to apply
  ait task update <taskId>             Patch task fields (admin keys)
      [--title <t>] [--instructions <text>] [--output-types x,linkedin,...]
      [--publish-mode manual|immediate|scheduled] [--publish-at <ISO date>]
      [--clear-publish-at] [--review] [--no-review]
                                       Only provided flags are changed.
                                       --review turns the gate back on;
                                       --clear-publish-at drops a scheduled time
                                       (the task does not need to be approved).
  ait task links <taskId>              Published post URLs for a task
  ait task claim-next                  Atomically claim the oldest todo task;
                                       returns it with its memory entries
  ait task claim <taskId>              Claim a specific todo task
  ait task add-content <taskId>        Add generated content to a claimed task
      [--body <text>] [--type <contentType>] [--title <t>]
      [--media '<json array>'] [--sort-order <n>]
      [--link-url <url>] [--link-action learn_more|book|order|buy|sign_up]
      --link-url is where the post sends readers; Google Business Profile
      publishes it as the post's button, which --link-action names (default
      learn_more = "Learn more"). Set it to the page the post is about — the
      blog article it summarizes, a product, booking, or signup page.
      [--topic <topic>]                Threads only: the post's one topic.
                                       Threads has no hashtags — set the
                                       topic here (no #, 1-50 chars, no . or
                                       &), never as a #tag in the body.
                                       First post of a thread only.
      --media items are [{"type":"image|video|audio|document","fileId":"<id>"}]
      — get a fileId from "ait upload-url"; URLs are not accepted.
      --items '<json array>'           Several posts in ONE call: each entry
                                       has the single-post fields (body, type
                                       as contentType, title, media, sortOrder,
                                       outputType, linkUrl, linkAction,
                                       topicTag). A
                                       thread is one call with
                                       sortOrder 0, 1, 2...; all-or-nothing —
                                       a bad item means nothing is added and
                                       the error names it by index. Items that
                                       omit sortOrder are numbered by position
                                       within their contentType. Not combined
                                       with the single-post flags.
      For --type youtube, an image in --media alongside the video becomes the
      video's custom thumbnail (match the video's shape: 16:9, or 9:16 for a
      Short). Any image format works; it is converted if YouTube won't take it.
  ait task update-content <taskId> <contentItemId>
      [--body <text>] [--title <t>] [--media '<json array>']
      [--link-url <url>] [--link-action learn_more|book|order|buy|sign_up]
      [--clear-link] [--topic <topic>] [--clear-topic]
                                       Rewrite a content item in place.
                                       Omit --media to leave attachments;
                                       --media '[]' clears them. --clear-link
                                       removes the item's link and button;
                                       --clear-topic removes a Threads topic.
  ait task delete-content <taskId> <contentItemId> --yes
  ait task clear-content <taskId> --yes
                                       Remove every content item from a task
  ait task complete <taskId>           Finish work (status → review/approved)
  ait task comment <taskId> --comment <text> [--file-ids <csv>]
                                       Leave a note for the human reviewer.
                                       --file-ids attaches workspace files
                                       (ids must belong to this workspace).
  ait task next-review                 Next task waiting for human review
  ait task approve <taskId>            Approve (reviewer/admin keys)
      [--tiktok '<json>']              Required for TikTok tasks: the operator's Post to
                                       TikTok visibility and interaction choices. Ask for
                                       them; never pick a privacy level yourself.
  ait task reject <taskId> [--comment <text>]
  ait task unapprove <taskId> [--comment <text>]
                                       Undo an approval: back to review, work
                                       kept. Use reject to have it redone.
  ait task publish <taskId> [--platforms a,b]
  ait task schedule <taskId> --at <ISO date> | --auto | --clear
                                       Schedule an approved task to publish
                                       later; --auto picks the next open slot
                                       per the workspace's scheduling rules;
                                       --clear returns it to manual
  ait task delete <taskId> --yes

Skills (workspace voice, formatting rules, bundled reference files):
  ait skills list                      id, name, description for each skill
  ait skills get <skillId>             Full instructions, memory entries,
                                       bundled file ids
  ait skills create --name <n>         [--description <text>]
      [--instructions <text>] [--file-ids <csv>] [--folder-ids <csv>]
                                       Instructions capped at 24,000 characters;
                                       name must be unique in the workspace
  ait skills update <skillId>          [--name <n>] [--description <text>]
      [--instructions <text>] [--file-ids <csv>] [--folder-ids <csv>]
                                       Only provided fields are changed
  ait skills delete <skillId> --yes    Fails if an automation or active task
                                       still references the skill

Automations:
  ait automation create --name <n>     [--instructions <text>]
      [--output-types x,...] [--schedule <json>] [--no-review]
  ait automation list
  ait automation get <automationId>    Full detail, including memory entries
  ait automation update <automationId> [--name <n>] [--instructions <text>]
      [--output-types x,...] [--schedule <json>]
  ait automation delete <automationId> --yes
                                       Also deletes its unfinished tasks (to
                                       do, in progress, in review); approved
                                       and published tasks are kept
  ait automation run <automationId>    Trigger now; returns the spawned task
  ait automation pause <automationId>  Stops new tasks from being created;
                                       existing tasks still publish, Run Now
                                       still works
  ait automation resume <automationId> Resumes at the next slot; missed runs
                                       are not backfilled

Files:
  ait upload-url --filename <f> --mime-type <m>
                                       Presigned upload URL for media
  ait files list [--search <s>] [--mime-type <m>] [--limit <n>]
  ait files download-url <fileId> [--expires-in <seconds>]
                                       Presigned URL — download it yourself
  ait files move <fileId> [--folder <folderId>]
                                       Move into a folder; omit --folder for
                                       the workspace root
  ait files copy <fileId> [--folder <folderId>]
                                       Duplicate the file (new file + object)

Folders:
  ait folders list [--parent <folderId>] [--root]
                                       --root lists top-level folders only
  ait folders create --name <n> [--parent <folderId>]
  ait folders rename <folderId> --name <n>
  ait folders delete <folderId> --yes  Also deletes every file and nested
                                       folder inside it

Composing posts:
  ait limits [--platform <p>]          Text limits for every platform, or one.
       [--text <draft>]                With --text, returns the draft's length
                                       under that platform's counting rule and
                                       whether it fits. Platforms count
                                       differently: X counts a URL as 23 and
                                       emoji as 2, Threads counts emoji as
                                       UTF-8 bytes, Bluesky counts graphemes.
  ait shorten <url> [--title <t>]      Shorten a link for a post

All workspace commands accept --workspace <id>.

Output: tool results may include a human-readable status line before the
JSON. Pass --json to print only the JSON value, pipable to jq.`;

export class CliError extends Error {}

const BOOLEAN_FLAGS = new Set(["no-review", "review", "claim", "mine", "clear", "clear-publish-at", "auto", "help", "yes", "root", "json", "clear-link", "clear-topic"]);

// MCP tools that permanently remove data, keyed to what they destroy. Keyed by
// tool rather than by command so the gate lives next to the thing that does
// the damage — a second command routing to one of these inherits it.
const DESTRUCTIVE_TOOLS = new Map([
  ["delete_task", "delete the task and everything attached to it"],
  ["delete_content_item", "delete the content item"],
  ["clear_task_content", "remove every content item from the task"],
  ["delete_automation", "delete the automation and its unfinished tasks (to do, in progress, in review); approved and published tasks are kept"],
  ["delete_folder", "delete the folder and every file and folder inside it"],
  ["delete_skill", "delete the skill"],
]);

/** Destructive tools need an explicit --yes; nothing else is affected. */
function requireConfirmation(flags, toolName) {
  const effect = DESTRUCTIVE_TOOLS.get(toolName);
  if (!effect || flags.yes === true) return;
  throw new CliError(
    `Refusing to run without --yes: this would ${effect}. It cannot be undone — confirm with the operator, then re-run with --yes.`
  );
}

export function parseArgs(argv) {
  const positional = [];
  const flags = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith("--")) {
      positional.push(arg);
      continue;
    }
    let key = arg.slice(2);
    let value;
    const eq = key.indexOf("=");
    if (eq !== -1) {
      value = key.slice(eq + 1);
      key = key.slice(0, eq);
      if (BOOLEAN_FLAGS.has(key)) value = value !== "false";
    } else if (BOOLEAN_FLAGS.has(key)) {
      value = true;
    } else {
      value = argv[++i];
      if (value === undefined) throw new CliError(`Missing value for --${key}`);
    }
    flags[key] = value;
  }
  return { positional, flags };
}

function csv(value) {
  if (!value) return [];
  return String(value)
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

/** --topic as the Threads topicTag field it sets, when given. */
function topicArgs(flags) {
  return flags.topic !== undefined ? { topicTag: flags.topic } : {};
}

/** --link-url / --link-action as the content fields they set, when given. */
function linkArgs(flags) {
  return {
    ...(flags["link-url"] !== undefined ? { linkUrl: flags["link-url"] } : {}),
    ...(flags["link-action"] !== undefined ? { linkAction: flags["link-action"] } : {}),
  };
}

function parseJsonFlag(value, flagName) {
  try {
    return JSON.parse(value);
  } catch {
    throw new CliError(`--${flagName} must be valid JSON`);
  }
}

// Tool results are text designed for agent consumption; some prefix JSON
// with a status line ("Successfully created task:\n{...}"). This pulls the
// first JSON value out of such text.
export function extractJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    // fall through to bracket scan
  }
  const candidates = ["{", "["]
    .map((ch) => text.indexOf(ch))
    .filter((i) => i !== -1);
  if (candidates.length === 0) return null;
  try {
    return JSON.parse(text.slice(Math.min(...candidates)));
  } catch {
    return null;
  }
}

export function formatOutput(result, jsonOnly) {
  let output = typeof result === "string" ? result : JSON.stringify(result, null, 2);
  if (jsonOnly) {
    const extracted = extractJson(output);
    if (extracted !== null) output = JSON.stringify(extracted, null, 2);
  }
  return output;
}

function parseRpcResponse(contentType, text) {
  if (contentType.includes("text/event-stream")) {
    for (const line of text.split("\n")) {
      if (!line.startsWith("data:")) continue;
      let message;
      try {
        message = JSON.parse(line.slice(5).trim());
      } catch {
        continue;
      }
      if (message.result !== undefined || message.error !== undefined) return message;
    }
    throw new CliError("No JSON-RPC response found in MCP event stream");
  }
  try {
    return JSON.parse(text);
  } catch {
    throw new CliError(`Unparseable MCP response: ${text.slice(0, 200)}`);
  }
}

const LOCAL_HOSTNAMES = new Set(["localhost", "127.0.0.1", "[::1]"]);

function baseUrl(ctx) {
  const raw = (ctx.env.AUTOMATE_IT_API_URL || DEFAULT_API_URL).replace(/\/+$/, "");
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new CliError(`AUTOMATE_IT_API_URL is not a valid URL: "${raw}"`);
  }
  const isLocalHttp = url.protocol === "http:" && LOCAL_HOSTNAMES.has(url.hostname);
  if (url.protocol !== "https:" && !isLocalHttp) {
    throw new CliError(
      `AUTOMATE_IT_API_URL must use https:// (plain http:// is only allowed for localhost, ` +
        `127.0.0.1, or [::1]) to avoid sending the API key to a plaintext endpoint: "${raw}"`
    );
  }
  return raw;
}

function apiKey(ctx) {
  const key = ctx.env.AUTOMATE_IT_API_KEY;
  if (!key) {
    throw new CliError(
      "AUTOMATE_IT_API_KEY is not set. Ask the operator to create an API key in Automate It (Profile → API keys) " +
        "and load it from their runtime's secret store or a mode-600 env file — not an interactive shell export."
    );
  }
  return key;
}

async function mcpRequest(ctx, method, params) {
  const url = `${baseUrl(ctx)}/mcp`;
  let res;
  try {
    res = await ctx.fetchFn(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey(ctx)}`,
        "Content-Type": "application/json",
        Accept: "application/json, text/event-stream",
      },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });
  } catch (err) {
    throw new CliError(`Request to ${url} failed: ${err?.message || err}`);
  }
  const text = await res.text();
  if (!res.ok) {
    const detail = extractJson(text)?.error ?? text.slice(0, 200) ?? res.statusText;
    throw new CliError(`MCP HTTP ${res.status}: ${typeof detail === "string" ? detail : JSON.stringify(detail)}`);
  }
  const message = parseRpcResponse(res.headers.get("content-type") || "", text);
  if (message.error) {
    throw new CliError(`MCP error ${message.error.code}: ${message.error.message}`);
  }
  return message.result;
}

async function callTool(ctx, name, args) {
  const result = await mcpRequest(ctx, "tools/call", { name, arguments: args });
  const text = (result?.content ?? [])
    .filter((c) => c.type === "text")
    .map((c) => c.text)
    .join("\n");
  if (result?.isError) throw new CliError(text || `Tool ${name} failed`);
  return text;
}

async function resolveWorkspace(ctx, flags) {
  if (flags.workspace) return flags.workspace;
  if (ctx.env.AUTOMATE_IT_WORKSPACE) return ctx.env.AUTOMATE_IT_WORKSPACE;
  const workspaces = extractJson(await callTool(ctx, "list_workspaces", {}));
  if (!Array.isArray(workspaces) || workspaces.length === 0) {
    throw new CliError("This API key has no workspaces.");
  }
  if (workspaces.length === 1) return workspaces[0].id;
  const options = workspaces.map((w) => `${w.id} (${w.name})`).join(", ");
  throw new CliError(
    `Multiple workspaces available — pass --workspace <id> or set AUTOMATE_IT_WORKSPACE. Options: ${options}`
  );
}

export function shapeLinks(task) {
  const results = Array.isArray(task?.publishResults) ? task.publishResults : [];
  return {
    taskId: task?.id ?? null,
    status: task?.status ?? null,
    links: results.map((r) => ({
      platform: r.platform ?? null,
      postUrl: r.postUrl ?? null,
      postId: r.postId ?? null,
    })),
  };
}

/** Fields shared by `task create` and `task submit`. */
function buildCreateTaskArgs(flags) {
  if (!flags.title) throw new CliError("--title is required for task create");
  const publishMode = flags["publish-mode"];
  if (publishMode && !PUBLISH_MODES.includes(publishMode)) {
    throw new CliError(`--publish-mode must be one of: ${PUBLISH_MODES.join(", ")}`);
  }
  return {
    title: flags.title,
    ...(flags.instructions ? { instructions: flags.instructions } : {}),
    outputTypes: csv(flags["output-types"]),
    ...(publishMode ? { publishMode } : {}),
    ...(flags["publish-at"] ? { publishAt: flags["publish-at"] } : {}),
    requiresReview: flags["no-review"] !== true,
  };
}

function requirePositional(rest, name, usage) {
  const value = rest[0];
  if (!value) throw new CliError(`Usage: ${usage} — missing <${name}>`);
  return value;
}

function requirePositionalAt(rest, index, name, usage) {
  const value = rest[index];
  if (!value) throw new CliError(`Usage: ${usage} — missing <${name}>`);
  return value;
}

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/**
 * Turn `--skills "brand-voice,<uuid>"` into skill ids. Agents know skills by
 * name, so anything that isn't already a uuid is looked up via list_skills.
 */
async function resolveSkillIds(ctx, workspaceId, value) {
  const entries = csv(value);
  if (entries.length === 0) return [];

  const needsLookup = entries.some((entry) => !UUID_RE.test(entry));
  if (!needsLookup) return entries;

  const text = await callTool(ctx, "list_skills", { workspaceId });
  const skills = extractJson(text);
  if (!Array.isArray(skills)) {
    throw new CliError(`No skills in this workspace to match ${entries.filter((e) => !UUID_RE.test(e)).join(", ")}`);
  }

  return entries.map((entry) => {
    if (UUID_RE.test(entry)) return entry;
    const match = skills.find((skill) => skill.name?.toLowerCase() === entry.toLowerCase());
    if (!match) {
      throw new CliError(`Unknown skill "${entry}". Available: ${skills.map((s) => s.name).join(", ") || "(none)"}`);
    }
    return match.id;
  });
}

export async function runCommand(argv, opts = {}) {
  const ctx = {
    fetchFn: opts.fetchFn || globalThis.fetch,
    env: opts.env || process.env,
  };
  const { positional, flags } = parseArgs(argv);
  const [resource, action, ...rest] = positional;

  if (!resource || resource === "help" || flags.help === true) {
    return USAGE;
  }

  const SINGLE_WORD_COMMANDS = new Set([
    "workspaces",
    "whoami",
    "upload-url",
    "integrations",
    "limits",
    "shorten",
  ]);
  const command = SINGLE_WORD_COMMANDS.has(resource)
    ? resource
    : [resource, action].filter(Boolean).join(" ");

  switch (command) {
    case "workspaces":
      return callTool(ctx, "list_workspaces", {});

    case "whoami":
      return callTool(ctx, "get_clerk_user_data", {});

    case "upload-url": {
      if (!flags.filename || !flags["mime-type"]) {
        throw new CliError("--filename and --mime-type are required for upload-url");
      }
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "get_upload_url", {
        workspaceId,
        filename: flags.filename,
        mimeType: flags["mime-type"],
      });
    }

    case "task create": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      const skillIds = await resolveSkillIds(ctx, workspaceId, flags.skills);
      return callTool(ctx, "create_task", {
        workspaceId,
        ...buildCreateTaskArgs(flags),
        ...(flags.claim === true ? { claim: true } : {}),
        ...(flags.assign ? { assignToUserId: flags.assign } : {}),
        ...(skillIds.length > 0 ? { skillIds } : {}),
      });
    }

    case "task submit": {
      if (!flags.body && !flags.media) {
        throw new CliError("task submit requires --body and/or --media (finished content)");
      }
      const workspaceId = await resolveWorkspace(ctx, flags);
      const skillIds = await resolveSkillIds(ctx, workspaceId, flags.skills);
      return callTool(ctx, "create_task", {
        workspaceId,
        ...buildCreateTaskArgs(flags),
        ...(flags.assign ? { assignToUserId: flags.assign } : {}),
        ...(skillIds.length > 0 ? { skillIds } : {}),
        content: [
          {
            ...(flags.body ? { body: flags.body } : {}),
            ...(flags.type ? { contentType: flags.type } : {}),
            ...(flags.media ? { media: parseJsonFlag(flags.media, "media") } : {}),
            ...linkArgs(flags),
            ...topicArgs(flags),
          },
        ],
      });
    }

    case "task list": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "list_tasks", {
        workspaceId,
        ...(flags.status ? { status: flags.status } : {}),
        ...(flags.mine === true ? { assignedTo: "me" } : {}),
        ...(flags.limit !== undefined ? { limit: Number(flags.limit) } : {}),
        ...(flags.offset !== undefined ? { offset: Number(flags.offset) } : {}),
      });
    }

    case "task update": {
      const taskId = requirePositional(rest, "taskId", "ait task update <taskId> [flags]");
      const workspaceId = await resolveWorkspace(ctx, flags);
      const publishMode = flags["publish-mode"];
      if (publishMode && !PUBLISH_MODES.includes(publishMode)) {
        throw new CliError(`--publish-mode must be one of: ${PUBLISH_MODES.join(", ")}`);
      }
      if (flags.review === true && flags["no-review"] === true) {
        throw new CliError("Use only one of --review, --no-review");
      }
      if (flags["publish-at"] && flags["clear-publish-at"] === true) {
        throw new CliError("Use only one of --publish-at, --clear-publish-at");
      }
      let requiresReview;
      if (flags.review === true) requiresReview = true;
      else if (flags["no-review"] === true) requiresReview = false;
      let publishAt;
      if (flags["clear-publish-at"] === true) publishAt = null;
      else if (flags["publish-at"]) publishAt = flags["publish-at"];
      return callTool(ctx, "update_task", {
        workspaceId,
        taskId,
        ...(flags.title ? { title: flags.title } : {}),
        ...(flags.instructions !== undefined ? { instructions: flags.instructions } : {}),
        ...(flags["output-types"] ? { outputTypes: csv(flags["output-types"]) } : {}),
        ...(publishMode ? { publishMode } : {}),
        ...(publishAt !== undefined ? { publishAt } : {}),
        ...(requiresReview !== undefined ? { requiresReview } : {}),
      });
    }

    case "task get":
    case "task links": {
      const taskId = requirePositional(rest, "taskId", `ait task ${action} <taskId>`);
      const workspaceId = await resolveWorkspace(ctx, flags);
      const text = await callTool(ctx, "get_task", { workspaceId, taskId });
      if (action === "get") return text;
      const task = extractJson(text);
      if (!task) throw new CliError(`Could not parse task detail from MCP response: ${text.slice(0, 200)}`);
      return shapeLinks(task);
    }

    case "task approve": {
      const taskId = requirePositional(rest, "taskId", "ait task approve <taskId> [--tiktok '<json>']");
      requireConfirmation(flags, "approve_task");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "approve_task", {
        workspaceId,
        taskId,
        ...(flags.tiktok ? { tiktok: parseJsonFlag(flags.tiktok, "tiktok") } : {}),
      });
    }

    case "task claim":
    case "task complete":
    case "task delete": {
      const toolByAction = {
        claim: "claim_task",
        complete: "complete_task",
        delete: "delete_task",
      };
      const taskId = requirePositional(rest, "taskId", `ait task ${action} <taskId>`);
      requireConfirmation(flags, toolByAction[action]);
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, toolByAction[action], { workspaceId, taskId });
    }

    case "task reject": {
      const taskId = requirePositional(rest, "taskId", "ait task reject <taskId> [--comment <text>]");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "reject_task", {
        workspaceId,
        taskId,
        ...(flags.comment ? { comment: flags.comment } : {}),
      });
    }

    case "task unapprove": {
      const taskId = requirePositional(rest, "taskId", "ait task unapprove <taskId> [--comment <text>]");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "unapprove_task", {
        workspaceId,
        taskId,
        ...(flags.comment ? { comment: flags.comment } : {}),
      });
    }

    case "task publish": {
      const taskId = requirePositional(rest, "taskId", "ait task publish <taskId> [--platforms a,b]");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "publish_task", {
        workspaceId,
        taskId,
        ...(flags.platforms ? { platforms: csv(flags.platforms) } : {}),
      });
    }

    case "task schedule": {
      const taskId = requirePositional(rest, "taskId", "ait task schedule <taskId> --at <ISO date> | --auto | --clear");
      const modes = [flags.at ? "--at" : null, flags.auto === true ? "--auto" : null, flags.clear === true ? "--clear" : null].filter(Boolean);
      if (modes.length > 1) {
        throw new CliError(`Use only one of --at, --auto, --clear (got ${modes.join(" and ")})`);
      }
      let publishAt = null;
      if (flags.auto === true) {
        publishAt = "auto";
      } else if (flags.clear !== true) {
        if (!flags.at) {
          throw new CliError("task schedule requires --at <ISO date>, --auto, or --clear");
        }
        const at = new Date(flags.at);
        if (isNaN(at.getTime())) throw new CliError(`--at is not a valid date: ${flags.at}`);
        publishAt = at.toISOString();
      }
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "schedule_task", { workspaceId, taskId, publishAt });
    }

    case "task add-content": {
      const taskId = requirePositional(rest, "taskId", "ait task add-content <taskId> --body <text> | --items '<json array>'");
      if (flags.items !== undefined) {
        // One call for every post; the server validates the batch together
        // and inserts it as one transaction.
        const singleFlags = ["body", "media", "type", "title", "sort-order", "link-url", "link-action", "topic"].filter((f) => flags[f] !== undefined);
        if (singleFlags.length > 0) {
          throw new CliError(
            `task add-content takes either --items or the single-post flags (${singleFlags.map((f) => `--${f}`).join(", ")}), not both`
          );
        }
        const items = parseJsonFlag(flags.items, "items");
        if (!Array.isArray(items) || items.length === 0) {
          throw new CliError("--items must be a non-empty JSON array of posts");
        }
        const workspaceId = await resolveWorkspace(ctx, flags);
        return callTool(ctx, "add_content_to_task", { workspaceId, taskId, items });
      }
      if (!flags.body && !flags.media) {
        throw new CliError("task add-content requires --body and/or --media (or --items for several posts)");
      }
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "add_content_to_task", {
        workspaceId,
        taskId,
        ...(flags.title ? { title: flags.title } : {}),
        ...(flags.body ? { body: flags.body } : {}),
        ...(flags.type ? { contentType: flags.type } : {}),
        ...(flags.media ? { media: parseJsonFlag(flags.media, "media") } : {}),
        ...(flags["sort-order"] !== undefined ? { sortOrder: Number(flags["sort-order"]) } : {}),
        ...linkArgs(flags),
        ...topicArgs(flags),
      });
    }

    case "task next-review": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "get_next_review_task", { workspaceId });
    }

    case "automation create": {
      if (!flags.name) throw new CliError("--name is required for automation create");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "create_automation", {
        workspaceId,
        name: flags.name,
        ...(flags.instructions ? { instructions: flags.instructions } : {}),
        outputTypes: csv(flags["output-types"]),
        ...(flags.schedule ? { schedule: parseJsonFlag(flags.schedule, "schedule") } : {}),
        requiresReview: flags["no-review"] !== true,
      });
    }

    case "automation list": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "list_automations", { workspaceId });
    }

    case "automation get":
    case "automation delete": {
      const automationId = requirePositional(rest, "automationId", `ait automation ${action} <automationId>`);
      const tool = action === "get" ? "get_automation" : "delete_automation";
      requireConfirmation(flags, tool);
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, tool, { workspaceId, automationId });
    }

    case "automation update": {
      const automationId = requirePositional(rest, "automationId", "ait automation update <automationId> [flags]");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "update_automation", {
        workspaceId,
        automationId,
        ...(flags.name ? { name: flags.name } : {}),
        ...(flags.instructions ? { instructions: flags.instructions } : {}),
        ...(flags["output-types"] ? { outputTypes: csv(flags["output-types"]) } : {}),
        ...(flags.schedule ? { schedule: parseJsonFlag(flags.schedule, "schedule") } : {}),
      });
    }

    case "automation run": {
      const automationId = requirePositional(rest, "automationId", "ait automation run <automationId>");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "run_automation", { workspaceId, automationId });
    }

    case "automation pause":
    case "automation resume": {
      const automationId = requirePositional(rest, "automationId", `ait automation ${action} <automationId>`);
      const tool = action === "pause" ? "pause_automation" : "resume_automation";
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, tool, { workspaceId, automationId });
    }

    case "task claim-next": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "claim_next_task", { workspaceId });
    }

    case "task comment": {
      const taskId = requirePositional(rest, "taskId", 'ait task comment <taskId> --comment "..." [--file-ids <csv>]');
      if (!flags.comment) throw new CliError("--comment is required for task comment");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "add_task_comment", {
        workspaceId,
        taskId,
        comment: flags.comment,
        ...(flags["file-ids"] ? { fileIds: csv(flags["file-ids"]) } : {}),
      });
    }

    case "task update-content": {
      const usage = "ait task update-content <taskId> <contentItemId>";
      const taskId = requirePositionalAt(rest, 0, "taskId", usage);
      const contentItemId = requirePositionalAt(rest, 1, "contentItemId", usage);
      const fieldFlags = ["link-url", "link-action", "clear-link", "topic", "clear-topic"].filter((f) => flags[f] !== undefined);
      if (flags.body === undefined && flags.title === undefined && flags.media === undefined && fieldFlags.length === 0) {
        throw new CliError(
          "at least one of --body, --title, --media, --link-url, --link-action, --clear-link, --topic, or --clear-topic is required for task update-content"
        );
      }
      if (flags["clear-topic"] === true && flags.topic !== undefined) {
        throw new CliError("--clear-topic removes the topic; don't combine it with --topic");
      }
      if (flags["clear-link"] === true && (flags["link-url"] !== undefined || flags["link-action"] !== undefined)) {
        throw new CliError("--clear-link removes the link; don't combine it with --link-url or --link-action");
      }
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "update_content_item", {
        workspaceId,
        taskId,
        contentItemId,
        ...(flags.body !== undefined ? { body: flags.body } : {}),
        ...(flags.title !== undefined ? { title: flags.title } : {}),
        ...(flags.media !== undefined ? { media: parseJsonFlag(flags.media, "media") } : {}),
        ...(flags["clear-link"] === true ? { linkUrl: null } : linkArgs(flags)),
        ...(flags["clear-topic"] === true ? { topicTag: null } : topicArgs(flags)),
      });
    }

    case "task delete-content": {
      const usage = "ait task delete-content <taskId> <contentItemId> --yes";
      const taskId = requirePositionalAt(rest, 0, "taskId", usage);
      const contentItemId = requirePositionalAt(rest, 1, "contentItemId", usage);
      requireConfirmation(flags, "delete_content_item");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "delete_content_item", { workspaceId, taskId, contentItemId });
    }

    case "task clear-content": {
      const taskId = requirePositional(rest, "taskId", "ait task clear-content <taskId> --yes");
      requireConfirmation(flags, "clear_task_content");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "clear_task_content", { workspaceId, taskId });
    }

    case "skills list": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "list_skills", { workspaceId });
    }

    case "skills get": {
      const skillId = requirePositional(rest, "skillId", "ait skills get <skillId>");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "get_skill", { workspaceId, skillId });
    }

    case "skills create": {
      if (!flags.name) throw new CliError("--name is required for skills create");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "create_skill", {
        workspaceId,
        name: flags.name,
        ...(flags.description !== undefined ? { description: flags.description } : {}),
        ...(flags.instructions !== undefined ? { instructions: flags.instructions } : {}),
        ...(flags["file-ids"] ? { fileIds: csv(flags["file-ids"]) } : {}),
        ...(flags["folder-ids"] ? { folderIds: csv(flags["folder-ids"]) } : {}),
      });
    }

    case "skills update": {
      const skillId = requirePositional(rest, "skillId", "ait skills update <skillId> [flags]");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "update_skill", {
        workspaceId,
        skillId,
        ...(flags.name !== undefined ? { name: flags.name } : {}),
        ...(flags.description !== undefined ? { description: flags.description } : {}),
        ...(flags.instructions !== undefined ? { instructions: flags.instructions } : {}),
        ...(flags["file-ids"] !== undefined ? { fileIds: csv(flags["file-ids"]) } : {}),
        ...(flags["folder-ids"] !== undefined ? { folderIds: csv(flags["folder-ids"]) } : {}),
      });
    }

    case "skills delete": {
      const skillId = requirePositional(rest, "skillId", "ait skills delete <skillId> --yes");
      requireConfirmation(flags, "delete_skill");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "delete_skill", { workspaceId, skillId });
    }

    case "files download-url": {
      const fileId = requirePositional(rest, "fileId", "ait files download-url <fileId>");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "get_download_url", {
        workspaceId,
        fileId,
        ...(flags["expires-in"] !== undefined ? { expiresIn: Number(flags["expires-in"]) } : {}),
      });
    }

    case "files list": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "list_workspace_files", {
        workspaceId,
        ...(flags.search ? { search: flags.search } : {}),
        ...(flags["mime-type"] ? { mimeType: flags["mime-type"] } : {}),
        ...(flags.limit !== undefined ? { limit: Number(flags.limit) } : {}),
      });
    }

    case "files move":
    case "files copy": {
      const usage = `ait files ${action} <fileId> [--folder <folderId>]`;
      const fileId = requirePositional(rest, "fileId", usage);
      const workspaceId = await resolveWorkspace(ctx, flags);
      // Omitting --folder targets the workspace root, matching the tools'
      // own default — for `move` that relocates the file, it isn't a no-op.
      return callTool(ctx, action === "move" ? "move_file" : "copy_file", {
        workspaceId,
        fileId,
        folderId: flags.folder ?? null,
      });
    }

    case "folders list": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "list_folders", {
        workspaceId,
        ...(flags.parent ? { parentId: flags.parent } : {}),
        ...(flags.root === true ? { root: true } : {}),
      });
    }

    case "folders create": {
      if (!flags.name) throw new CliError("--name is required for folders create");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "create_folder", {
        workspaceId,
        name: flags.name,
        ...(flags.parent ? { parentId: flags.parent } : {}),
      });
    }

    case "folders rename": {
      const folderId = requirePositional(rest, "folderId", "ait folders rename <folderId> --name <n>");
      if (!flags.name) throw new CliError("--name is required for folders rename");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "rename_folder", { workspaceId, folderId, name: flags.name });
    }

    case "folders delete": {
      const folderId = requirePositional(rest, "folderId", "ait folders delete <folderId> --yes");
      requireConfirmation(flags, "delete_folder");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "delete_folder", { workspaceId, folderId });
    }

    case "integrations": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "list_integrations", { workspaceId });
    }

    case "limits": {
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "get_platform_limit", {
        workspaceId,
        ...(flags.platform !== undefined ? { platform: flags.platform } : {}),
        ...(flags.text !== undefined ? { text: flags.text } : {}),
      });
    }

    case "shorten": {
      const url = requirePositional([action, ...rest].filter(Boolean), "url", "ait shorten <url> [--title <t>]");
      const workspaceId = await resolveWorkspace(ctx, flags);
      return callTool(ctx, "shorten_url", {
        workspaceId,
        url,
        ...(flags.title ? { title: flags.title } : {}),
      });
    }

    default:
      throw new CliError(`Unknown command "${command}". Run "ait help" for the full command list.`);
  }
}

const isMain = (() => {
  try {
    // realpath both sides: npm installs the bin as a symlink, so argv[1] is
    // the link while import.meta.url is the resolved file.
    return import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href;
  } catch {
    return false;
  }
})();

if (isMain) {
  const args = process.argv.slice(2);
  const jsonOnly = args.includes("--json");
  runCommand(args)
    .then((result) => {
      process.stdout.write(`${formatOutput(result, jsonOnly)}\n`);
    })
    .catch((err) => {
      process.stderr.write(`${JSON.stringify({ error: err?.message || String(err) })}\n`);
      process.exit(1);
    });
}
