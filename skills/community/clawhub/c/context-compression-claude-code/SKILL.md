---
name: context-compression
description: Use this skill whenever the conversation context is getting long, when a user asks to "compress", "summarize", or "clean up" the conversation, or when you detect the context window is filling up. Also triggers automatically via PreCompact hook if configured. Compresses conversation history using a tiered strategy — preserving what matters, summarizing what's useful, dropping what's noise — then writes a structured memory file so nothing important is truly lost. Use this even for partial compression of recent exchanges.
---

> **Origin**: This skill was extracted from Claude Code's internal implementation and rules. Claude Code openly exposes its safety mechanisms (hooks, system prompts, skill definitions) in the `~/.claude/` directory. The tiered compression strategy, layer classification system, and memory file structure were reverse-engineered from Claude Code's PreCompact/PostCompact hooks and session memory handling, then adapted for OpenClaw's multi-channel environment.

# Context Compression

## Why Tiered Compression Is Needed

A one-size-fits-all approach to dropping context either leaves the agent without memory or burns through context too quickly. The core principle of tiered strategy is: **different information has different lifecycles**. A user's statement "I prefer concise responses" is worth remembering forever; but a resolved error message from three days ago has no value today.

---

## Before Compression: Identify the Scenario

Before starting compression, determine which conversation scenario you're in, as retention strategies differ:

| Scenario | Characteristics | Compression Tendency |
|----------|------------------|----------------------|
| **Task-oriented** | Clear goal, step-driven | Keep goal and incomplete steps, compress process details |
| **Chat-oriented** | Open topics, no clear task | Keep only user preference signals, discard aggressively |
| **Research-oriented** | Gathering information, continuous accumulation | Keep conclusions and sources, compress procedural discussions |
| **Group-chat** | Multiple people, high noise | Discard aggressively, keep only directly relevant content |

---

## Three-Layer Compression Strategy

### Layer 1: Must Preserve (Keep Original)

These contents remain in original or near-original form after compression:

- User's **explicitly stated** goals, requirements, deadlines
- **Incomplete tasks** (in-progress, interrupted)
- **Confirmed important decisions** ("We decided to go with Plan B")
- User-expressed **explicit preferences** ("I don't like X", "Always use Y format going forward")
- **Key credentials or config** (accounts, paths, special settings)

### Layer 2: Compress to Summary (Extract and Keep)

Keep conclusions, discard process:

- Completed tasks → One-sentence conclusion ("Completed X, result was Y")
- Long explanations → Core point in 1-2 sentences
- Tool call outputs → Keep only final results, discard intermediate steps
- Repeated topics → Merge into one record

### Layer 3: Discard Directly

- Small talk, thanks, acknowledgment messages ("ok", "thanks", "got it")
- Rejected or obsolete proposals
- Multiple attempts at the same question (keep only the final effective one)
- Pure transitional content ("let me think", "hold on")
- Resolved error messages that won't be needed again

---

## Compression Execution Steps

**Step 1: Scan All Conversation**
Identify all Layer 1 content, make a checklist — this cannot be discarded.

**Step 2: Process Layer 2**
For each conversation segment, judge: Is there a conclusion worth keeping? If yes, distill into one sentence.

**Step 3: Generate Compressed Summary**
In chronological order, combine Layer 1 content + Layer 2 extractions into a compact context summary, typically no more than 600 characters.

**Step 4: Update Memory File**
Write high-persistence-value information (user preferences, long-term goals, important decisions) to the memory file. See `memory-template.md` for format.

**Step 5: Inform the User**
Briefly explain what was compressed and what key information was preserved, so the user knows the context has been updated.

---

## OpenClaw Multi-Channel Supplementary Rules

OpenClaw runs across multiple messaging platforms, pay extra attention:

**Group chat scenarios**: Other members' messages default to Layer 3 (discard) unless the user explicitly responds to or quotes that message.

**Cross-day conversations**: Judge by topic unit, not time unit. An unfinished task from yesterday belongs to Layer 1; a completed topic from yesterday drops one level today.

**Channel switching**: If the user asks similar questions on different channels (WhatsApp vs Telegram), it indicates genuine concern — promote priority to Layer 1.

---

## Optional: Auto-Trigger (Hook Configuration)

If you use Claude Code or an agent that supports PreCompact hooks, you can configure auto-trigger. See `setup-hook.md` for details.

Without hook configuration, you can trigger manually: just tell the agent "compress my context" or "context is getting long, clean it up".
