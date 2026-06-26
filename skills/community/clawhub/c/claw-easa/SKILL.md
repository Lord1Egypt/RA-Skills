---
name: claw-easa
description: Query EASA Easy Access Rules locally with exact reference lookup, full-text search, and semantic search. Use when answering EASA regulatory questions, retrieving article/reference wording, checking applicability, or finding AMC, GM, and FAQ material from the local claw-easa index.
---

Use the local `claw-easa` CLI from this repository.

Preferred commands:
- `claw-easa lookup <REF>` for exact references such as `ORO.FTL.110`
- `claw-easa refs "<query>"` for reference-oriented search
- `claw-easa snippets "<query>"` for cited text excerpts
- `claw-easa hybrid "<query>"` for mixed lexical + semantic retrieval
- `claw-easa ask "<question>"` for routed natural-language queries
- `claw-easa status` to verify corpus/index availability

Source-scoped search — use `--slug <source>` to restrict results to a specific
source document. This is important when a broad query returns too many results
from different sources, or when you know which source is most relevant:
- `claw-easa refs "crew fatigue" --slug occurrence-reporting`
- `claw-easa snippets "crew fatigue" --slug occurrence-reporting`
- `claw-easa hybrid "fatigue reporting" --slug occurrence-reporting`
Use `claw-easa sources-list` to see available slugs.
- `claw-easa sources-list` to list ingested EARs and FAQ domains (supports `--type ear|faq`)
- `claw-easa ear-discover` to list Easy Access Rules available on the EASA website
- `claw-easa ear-list` to list built-in known source aliases
- `claw-easa ingest fetch <slug>` to download a source (use `--url` to bypass catalog)
- `claw-easa ingest parse <slug>` to parse a fetched source into the database
- `claw-easa ingest diagnose <slug>` to verify parser coverage against the source XML
- `claw-easa ingest faq-all` to ingest all EASA FAQs (crawls every sub-domain)
- `claw-easa ingest faq <domain>` to ingest FAQs for a specific domain
- `claw-easa ingest faq-discover` to list available FAQ domains on the EASA website

Answering rules:
- Prefer exact lookup when the user gives a regulation reference.
- Quote the retrieved text or excerpt before paraphrasing.
- Distinguish regulation text from AMC/GM/FAQ material.
- If retrieval is empty or ambiguous, say so explicitly instead of inferring.
- When the question targets a specific regulation domain (e.g. occurrence
  reporting, aircrew, air operations), use `--slug` to scope the search.
  This dramatically improves recall for items buried in long annexes.

Read these files only when needed:
- `references/usage.md` for repository-aware usage and installation notes
- `references/runtime-setup.md` when the local `claw-easa` CLI may not be installed yet
- `references/easa-answering.md` for answer format and evidence rules

Local install notes:
- The skill package lives under `skill/claw-easa/` in the repository.
- For OpenClaw local installation, copy this folder into `~/.openclaw/workspace/skills/claw-easa/`.
- Avoid symlinks that resolve outside the OpenClaw workspace.
