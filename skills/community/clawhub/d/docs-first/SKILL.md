---
name: docs-first
description: Consult official documentation BEFORE answering any question that involves a specific third-party library, framework, package, SDK, CLI tool, API, or program. Use this whenever the user asks how to use, configure, install, or call something (e.g. "how do I do X in vLLM", "what's the flag for Y", "does library Z support W", version/compatibility questions, error messages from a tool, API signatures, config schemas). Trigger this EVEN WHEN you feel confident you know the answer — training knowledge goes stale for fast-moving software, and confidence is exactly the failure mode this skill exists to catch. Search the official site and the official repository first, then answer grounded in what you found, with links and the version you relied on. Skip only for purely conceptual questions ("what is a hash map") that name no specific tool.
---

# Docs-first

## Why this exists

Your training data has a cutoff. Libraries, frameworks, and tools change after it — APIs get renamed, flags get deprecated, defaults flip, new versions ship breaking changes. The dangerous case is not "I don't know" (you'll search anyway); it's "I'm confident I know" while the library moved on six months ago. A confident answer from stale memory is worse than no answer, because the user trusts it and burns time debugging a call signature that no longer exists.

So the rule is simple: **when a question is about a specific piece of software, go to its documentation before you answer — even if you think you already know.**

## When to trigger

Trigger when the request is about *using* a specific named tool, and the answer depends on facts that could have changed:

- API signatures, method/function names, arguments, return types
- Configuration: flags, env vars, config-file schema, defaults
- Installation, setup, version/compatibility constraints
- "How do I do X in Y" / "does Y support X" / "what changed in Y v…"
- Errors or stack traces coming from a specific tool
- Anything where you'd otherwise be reciting an API from memory

Software here means anything third-party: libraries, frameworks, packages, SDKs, CLI tools, runtimes, services, APIs, daemons, hardware SDKs.

## When NOT to trigger

- Purely conceptual questions naming no specific tool ("what is a B-tree", "explain backpressure")
- General programming-language syntax that is stable and not tied to a library
- The user explicitly says they don't want a search, or pastes the docs themselves
- Pure opinion/architecture discussion where no specific API fact is being asserted

When in doubt, lean toward searching. The cost of an unnecessary search is a few seconds; the cost of a confident wrong API is the user's afternoon.

## Procedure

1. **Identify the target and what fact you need.** Name the library/tool and the specific thing (a function, a flag, a version behavior). This shapes the query.
2. **Search official sources (in any language — whatever reaches the authoritative source), in this priority order:**
   - **Official site / hosted docs** first (e.g. `docs.<project>.<tld>`, the project's documentation portal). Use `web_search` with the project name + the specific term, then `web_fetch` the actual doc page — snippets are too thin to answer from.
   - **Official repository** next, and as the primary source when there's no separate docs site (common for infra/research projects). Look at the repo's `README`, `docs/` directory, and when needed the source itself or release notes / `CHANGELOG`. The repo is authoritative for projects whose docs lag behind the code.
   - Prefer the source that matches the version the user is on. If they didn't say, target the latest stable and say so.
3. **Read enough to actually ground the answer.** Fetch the relevant page(s). Don't answer off a search-result snippet. If the first source is thin or ambiguous, search again with different terms rather than filling the gap from memory.
4. **Answer, grounded.** Base the substantive claims (signatures, flags, defaults, behavior) on what you read, not on prior memory. If docs and your memory disagree, the docs win.
5. **If nothing official is found:** say so explicitly. Then you may answer from general knowledge, but flag it clearly as unverified against current docs and note what you'd want to check.

## Output requirements

**Answer in the user's language.** Search the docs in whatever language gets you to the authoritative source fastest — English, the user's language, or whatever the project publishes in; language is not a constraint on where you look. Then write the response in whatever language the user is using.

Every answer produced under this skill MUST end with a **single compact footer** that is just a short hyperlink — nothing else. The visible link text is at most a couple of words (e.g. the project + "docs"); the full URL lives behind the link. Render it small/muted so it stays out of the way. Do NOT print the raw URL, and do NOT include a version.

Format (Markdown link, short anchor, full URL hidden inside):

```
<direct answer, grounded in docs — in the user's language>

<sub>📄 [vLLM docs](https://docs.vllm.ai/en/stable/features/structured_outputs/)</sub>
```

Rules for the footer:
- Visible text = max ~2 words (e.g. `vLLM docs`, `Tauri sidecar`, `repo README`). The real page URL goes inside the link target, not on screen.
- The link must point to the **specific page** you relied on, not the project homepage.
- No version, no "Source:" label, no bullet list, no extra lines.
- Multiple sources → at most two short links separated by `·`, still on one line.
- Use `<sub>…</sub>` (or the smallest emphasis the renderer supports) so the footer reads as fine print.

If you searched and the docs confirmed what you already believed, that's fine — still drop the short link, so the user can verify. The point isn't to be uncertain; it's to be *checkable* without clutter.
