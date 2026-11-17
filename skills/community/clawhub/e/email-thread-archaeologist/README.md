# Email Thread Archaeologist

**The problem:** long email threads are archaeological sites — fourteen replies deep, quoted by four different clients (Gmail's `>`, Outlook's `From:/Sent:` header blocks, forward fences), with every sentence preserved in five copies at five depths. When someone asks "what did we actually decide, and did anyone answer the insurance question?" the answer is technically in there, but extracting it means twenty minutes of mental un-nesting. Worse: questions asked mid-thread and never answered are invisible unless you read every layer.

**What this does:** stdlib-only Python that excavates a thread (.eml or raw text paste) into structure:

- **Strata splitting** — every buried message detected via quote depth + client attribution headers, across Gmail/Outlook/Apple Mail dialects
- **Fuzzy dedup** — the fifth re-quoted copy of a sentence dies; the oldest occurrence survives (difflib ≥0.90)
- **Chronological timeline** — deepest (oldest) strata first, every fact once, attributed to its original author
- **Decision ledger** — agreement/decision/commitment markers ("agreed", "let's go with", "approved", "action item", "owner:") with who committed
- **Open questions** — questions that no later message answered (answer-starters + "agreed"/"yes" detection in the following window)

```bash
python3 scripts/thread_archaeologist.py dig thread.txt
# --- DECISION LEDGER ---
# ✔ [Oct 14, 2026 at 3:12 PM Dana Whitfield] Agreed — ... Let's go with Signature.
# --- OPEN QUESTIONS (never answered in-thread) ---
# ? [Dana Whitfield] One open item: who owns the punch-list documentation after install?
```

## Who needs this

Knowledge workers spend ~28% of the workweek in email; project decisions routinely live in threads nobody can reconstruct. Use cases: "what did we decide" before a meeting, catching silently-dropped questions, onboarding onto a running project, and answering "who committed to that?" without reading 40 messages.

## Honest limits

Attribution trusts the clients' quoting, which participants can edit — this is a reading aid, not certified evidence. Fully-HTML-quoted threads (no `>` characters) need plain-text export first. Locale support covers EN From-headers + RU/DE/FR variants.

## License

MIT
