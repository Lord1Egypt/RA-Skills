---
name: ChatGPT
slug: chatgpt
version: 1.0.0
homepage: https://clawic.com/skills/chatgpt
description: Run ChatGPT with stronger prompts, Projects, GPTs, memory boundaries, and output QA for research, writing, analysis, and planning.
changelog: Initial release with surface routing, prompt packets, project workflows, QA checks, and troubleshooting for repeatable ChatGPT work.
metadata: {"clawdbot":{"emoji":"GPT","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/chatgpt/"]}}
---

## Setup

On first use, read `setup.md` and quietly align activation rules, privacy boundaries, and the user's normal ChatGPT workflow before suggesting a new system.

## When to Use

User wants better results from ChatGPT itself, not the OpenAI API. Agent handles prompt design, surface selection, project structure, custom GPT scoping, memory hygiene, and output verification for recurring work.

Use this for research, writing, planning, analysis, brainstorming, study support, and recurring assistant workflows inside ChatGPT. Do not use it for API integration, SDK coding, or model-provider benchmarking.

## Architecture

Memory lives in `~/chatgpt/`. If `~/chatgpt/` does not exist, run `setup.md`. See `memory-template.md` for structure and status fields.

```text
~/chatgpt/
|- memory.md          # Activation preference, constraints, and default workflow
|- workflows.md       # Reusable prompt packet patterns that worked well
|- projects.md        # Active ChatGPT projects, files, and decision logs
|- gpts.md            # Custom GPT roles, guardrails, and known limitations
`- qa.md              # Output failures, hallucination catches, and fixes
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory template and status model | `memory-template.md` |
| Choose between chat, Temporary Chat, Projects, GPTs, and instructions | `surfaces.md` |
| Build high-signal prompts and reusable packets | `prompt-packets.md` |
| Structure long-running work inside Projects | `project-playbook.md` |
| Review output before trusting or shipping it | `output-qa.md` |
| Diagnose drift, bland output, and memory contamination | `troubleshooting.md` |

## Core Rules

### 1. Route to the Right ChatGPT Surface First
- Choose the lightest surface that fits the job before rewriting the prompt.
- Use `surfaces.md` to distinguish standard chat, Temporary Chat, Projects, custom instructions, and GPTs.
- Bad routing creates false prompt problems: sensitive work in a remembered chat, long projects in throwaway chats, or one-off tasks buried inside durable instructions.

### 2. Build Prompt Packets, Not Wishful One-Liners
- Every serious request needs at least: goal, context, source material, deliverable, constraints, and review standard.
- Use `prompt-packets.md` to turn vague asks into packets ChatGPT can execute consistently.
- If the output shape matters, specify the shape before asking for the content.

### 3. Keep Durable Preferences Separate from Task Context
- Put stable preferences in custom instructions or memory notes only when they should affect future sessions.
- Put project-specific context in the active Project or current chat, not in global instructions.
- Use Temporary Chat for sensitive, one-off, or contamination-prone work that should not influence future conversations.

### 4. Force Evidence, Assumptions, and Unknowns into the Open
- For factual or consequential work, require ChatGPT to label what is confirmed, inferred, and missing.
- Ask for references to the files, notes, or user-provided facts it actually used.
- If the answer depends on outside facts and no evidence is present, treat it as a draft, not truth.

### 5. Split Complex Work into Passes
- Use multi-pass flows for anything larger than a quick answer: discover, outline, draft, critique, finalize.
- In Projects, keep a visible decision log so later turns do not silently undo earlier choices.
- Ask for one improvement target per pass instead of a broad "make it better."

### 6. QA the Result Before Reusing It
- Run `output-qa.md` on anything the user will send, publish, code from, or rely on.
- Check missing edge cases, unsupported claims, broken structure, and whether the output actually answered the brief.
- A polished answer that misses the goal is still a failed answer.

### 7. Recover Hard When Drift Appears
- If ChatGPT gets generic, repetitive, or contradictory, stop patching sentence by sentence.
- Restate the objective, paste the current source of truth, remove stale context, and switch surfaces when needed.
- Use `troubleshooting.md` to diagnose whether the problem is prompt quality, memory carryover, project sprawl, or wrong task framing.

## Common Traps

- Stuffing temporary requirements into custom instructions -> every later chat inherits the wrong behavior.
- Using the same chat for unrelated jobs -> old assumptions leak into new tasks.
- Asking for a final answer before defining audience, output format, and success criteria -> bland generic output.
- Trusting confident claims without asking what they are based on -> hallucinations survive review.
- Uploading files without telling ChatGPT which file is authoritative -> mixed or contradictory answers.
- Letting Projects accumulate stale drafts and renamed files -> the model anchors on obsolete context.
- Trying to fix a broken workflow with more adjectives -> structure beats style words.

## Security & Privacy

**Data that leaves your machine:**
- Anything the user chooses to type, paste, or upload into ChatGPT.
- Any instructions, files, or examples deliberately used in a ChatGPT workflow.

**Data that stays local:**
- Activation preferences, reusable workflows, project notes, GPT notes, and QA learnings under `~/chatgpt/`.

**This skill does NOT:**
- Automate browser sessions or upload files on its own.
- Store secrets unless the user explicitly wants a safe local note about a workflow boundary.
- Treat remembered preferences as facts when the current prompt says otherwise.
- Modify its own skill instructions.

## Trust

This skill is designed to improve work done inside ChatGPT. When the user runs those workflows, prompts and uploaded material may be sent to OpenAI through ChatGPT.
Only install and use this skill if that data flow is acceptable for the user's task.

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `assistant` - Build clearer working agreements and recurring collaboration patterns with an AI assistant.
- `brainstorm` - Expand idea generation when the user wants divergence before converging into a final prompt packet.
- `chat` - Improve conversational structure, turn-taking, and clarity in multi-turn interactions.
- `documentation` - Turn ChatGPT outputs into tighter docs, guides, and reusable written artifacts.
- `memory` - Design durable memory patterns when the user wants stable context beyond a single chat.

## Feedback

- If useful: `clawhub star chatgpt`
- Stay updated: `clawhub sync`
