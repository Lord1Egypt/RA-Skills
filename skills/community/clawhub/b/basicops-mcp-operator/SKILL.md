---
name: basicops-mcp-operator
description: Operate BasicOps through an available BasicOps MCP server. Use when the user wants to read from or update BasicOps tasks, projects, notes, messages, assignments, statuses, subtasks, reviews, or related work in an MCP-capable environment. Trigger on requests like "update this BasicOps task", "assign this in BasicOps", "summarize this BasicOps thread", "request review", "create subtasks", or "mark this complete". Prefer safe context gathering before writes, ask one concise clarifying question when the target is ambiguous, and summarize completed changes briefly.
---

# BasicOps MCP Operator

Use BasicOps safely through an existing BasicOps MCP connection.

This skill is the work half of the BasicOps MCP pair. It handles everyday task, project, note, message, and review operations once setup is complete.

## Best for

- day-to-day BasicOps work through MCP
- safe task and project updates from natural language
- agents that need concise reads, careful writes, and clean follow-up

## Pairs with

- `basicops-mcp-setup` when the BasicOps MCP connection is missing, unauthorized, or not yet verified

## Overview

Use this skill to turn a general agent into a careful BasicOps operator through MCP.

Assume the preferred path is an available BasicOps MCP server, not raw REST calls. Reuse the MCP tool surface that already exists in the environment. Focus on safe writes, clear scope, concise follow-up, and good judgment.

If no usable BasicOps MCP server or BasicOps tool surface is available, read `references/setup.md`, explain the missing prerequisite briefly, and stop instead of inventing an API fallback.

## Example requests

- "Assign this BasicOps task to Amanda."
- "Mark this complete in BasicOps."
- "Summarize this BasicOps thread."
- "Create subtasks for this rollout task."
- "Request review from Kai on this task."

## Read these references only when needed

- Read `references/setup.md` when you need to confirm whether BasicOps MCP is available, authenticated, or correctly named.
- Read `references/workflow-patterns.md` when the request needs broader context, multiple objects, or a decision about how much to inspect before acting.
- Read `references/write-safety.md` before non-trivial writes or when there is any ambiguity about assignment, status, subtasks, reviews, replies, or destructive actions.
- Read `references/common-requests.md` when mapping casual user wording to likely BasicOps operations.

## Quick operating workflow

1. Detect the available BasicOps MCP tool surface.
2. Identify the current target object and current surface.
3. Gather only the context needed to act safely.
4. Perform the write only when the target and requested change are clear.
5. Post or return a short completion summary that says exactly what changed.

## Core operating rules

- Prefer MCP over direct HTTP.
- Prefer reads before writes unless the request is trivial and unambiguous.
- Confirm the active workspace, current user context, and target object before non-trivial writes, especially in shared, demo, or multi-user workspaces.
- Stay on the current task, project, note, or thread unless the user explicitly asks to inspect related work.
- Prefer replying in the current thread or surface instead of creating fresh top-level chatter.
- Ask exactly one concise clarifying question when the target, assignee, or requested mutation is unclear.
- Avoid destructive actions unless the user explicitly requests them.
- Do not bluff missing context, missing objects, or missing permissions.
- After any write, summarize exactly what changed in plain language.

## Scope rules

Use the smallest safe scope first.

- For simple task mutations like assign, rename, mark complete, or change priority, do minimal lookup and act.
- For summaries, related-work discovery, description rewriting, blocked-task analysis, or checklist generation, read the relevant local context first.
- For cross-project or broad updates, confirm intent unless the user was already explicit.

## Completion style

Keep outputs short and practical.

- Good: "Assigned the task to Amanda and set status to In Progress."
- Good: "Created 5 subtasks under the parent task and posted a short checklist summary."
- Good: "I found 3 related tasks in the same project."
- Avoid long audit logs unless the user asked for detail.

## Natural-language intent handling

Map casual phrasing to valid BasicOps operations when reasonable.

Examples:
- "start this" -> likely set status to `In Progress`
- "mark this complete" -> likely set status to `Complete`
- "make this high priority" -> likely set priority to `High`
- "put together subtasks" -> likely create a modest checklist or subtask set

If more than one reasonable interpretation exists, ask one short question.

## v1 boundaries

This skill is for operating BasicOps well through MCP.

Do not turn it into:
- a raw API client skill
- a webhook-runtime framework
- a giant automation system
- a schema-guessing engine for every custom workspace variation

Keep the promise tight: safe reads, safe writes, concise results, and good workflow judgment.
