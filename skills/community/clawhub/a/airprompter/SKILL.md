---
name: airprompter
description: Use when the user wants to save a prompt, template or workflow to reuse, find or run one they saved, or share one with their team ("share this prompt with my team"); to create a workflow, build a reusable process, or turn this into a skill; or to edit, import or export AirPrompter workflows, skills, and prompts, or diagnose its connection. Not for repository maintenance, a file, script or skill the user wants kept local, another product the user names, or one-off writing with no reuse.
---

# AirPrompter

## Author a workflow or skill

In AirPrompter context, "create a workflow," "create a skill," "make a workflow,"
"make a skill," "turn this into a skill or workflow," and "build a reusable
process" mean author a workflow; a supplied prompt or template is `create_prompt`,
no plan. Load tools by exact name. For new designs,
show a useful preview before asking. Resolve the account before using its data
or saving. Use `plan_draft` with `target: workflow`. Confirm before `save_workflow`.
Do not run future actions during authoring.

A saved AirPrompter skill is a workflow. Use the AirPrompter MCP tools on the
account the user chooses. Local skill authoring stays local unless the user
asks to save it in AirPrompter. For an explicitly local skill, use the host's
local skill flow and skip AirPrompter tools.

### Design, preview, and save

1. For a new workflow or skill on the selected account, call `plan_draft`
   first. Unless the user already asked to use AirPrompter, first say that the
   request goes to their AirPrompter account to plan it, and continue only if
   they agree; if not, sketch the preview locally. Send `target: workflow` and
   put only the user's request in `instruction`, never secrets or unrelated
   conversation.
   If the host defers tools, search for the exact name `plan_draft`. Describe
   and call the returned tool using its full name and arguments. For Hermes
   Tool Search, pass `calls: [{name, arguments}]` to `tool_call`.
2. Use the plan and the user's brief to show a proposed name, destination,
   steps, and data inputs. Ask one question only if the answer changes the
   design. Ask whether to save the preview to that library and end the turn.
   Call `save_workflow` only after a later user reply approves the preview.
3. After confirmation, write the agreed step prompts and save in that turn.
   Use `generate_draft` with the plan and the user's answers if you need
   drafting guidance. Call `save_workflow` once with the approved name and
   prompts. Send `creationRouting: { mode: "host_planned" }`. Report the tool
   result.

Use `create_prompt` for a standalone prompt.
For edits, use `get_workflow` or `get_prompt` to resolve the item, show the
proposed change, and use `update_workflow` or `update_prompt` after confirmation.

## Run fast path

1. Use `find_workflows` to resolve an ambiguous name. Ask which saved item to use
   if the result is ambiguous. Show which account and workflow will run.
2. Use `execute_workflow` with the selected workflow and `fallbackPolicy` set to
   `fail_only`, or `execute_prompt` for a saved prompt. AirPrompter receives the
   run inputs and step results needed to continue. Tell the user before sharing
   data they have not already authorized for this workflow.
3. Follow the returned step and call the continuation tool the server specifies.
   Stop on completion, cancellation, or failure. Ask before consequential
   actions or before sending information to another service. If the host cannot
   complete a step, report what is needed. Do not produce a substitute result.

## Find, import, export, and diagnose

Use `find_workflows` or `get_prompt` for saved items. Use `preview_skill_import`
to show what the user-selected material would add to AirPrompter, then call
`import_skill` after confirmation. Use `export_workflow_skill` for a requested
export. Use `diagnose_connection` to check a configured AirPrompter connection.
If AirPrompter is unavailable, tell the user how to reconnect in the host.
