# Agent Types — Recipes By What The Agent Is For

Each type has a characteristic tool set, memory shape, escalation profile, and a failure that shows up first. Start from the closest one, then apply the general rules.

**Before designing a new agent**, read `## Agents` in `~/Clawic/data/agents/memory.md` — an agent for a neighbouring purpose may already exist, and adding a tool to it usually beats a second agent (SKILL.md Rule 1).

**Contents:** [Support](#customer-support) · [Coding](#coding) · [Research](#research) · [Ops](#ops-and-infrastructure) · [Data](#data-and-reporting) · [Inbox and scheduling](#inbox-and-scheduling) · [Outbound](#outbound-and-sales) · [Content](#content) · [Voice](#voice) · [Browser](#browser-and-computer-use) · [Internal knowledge](#internal-knowledge) · [Sizing the first version](#sizing-the-first-version)

## Customer Support

- **Tools**: order/account lookup (read) · policy search (read) · create ticket or return (write, idempotency-keyed on the order) · message the customer (external).
- **Memory**: working plus the last few interactions; the system of record is the ticket system, never the agent's store (`memory-design.md`).
- **Escalation**: anger, legal or safety content, any refund, two failed attempts on the same goal, VIP segment.
- **Autonomy**: `approve-writes` until the reversal rate is measured and low.
- **First failure**: the agent apologizes and promises something it cannot do. Fix by making the promise vocabulary a hard constraint and asserting the forbidden phrases in the eval set.
- **The number to watch**: reversal rate on escalations, not deflection rate — deflection improves by ignoring people.

## Coding

- **Tools**: read file · search repository · write file · run tests · run a command in a sandbox (`security.md`).
- **Memory**: the repository is the memory. Persist only conventions and past decisions; everything else is re-read.
- **Loop**: verified-done is available and cheap — the tests are the checker. Use them as the stop condition (`architecture.md`).
- **Escalation**: touching credentials, infrastructure, migrations, or anything outside the declared scope.
- **First failure**: confident edits that were never executed. Require the test run as evidence, and treat "it should work" as an unfinished task.
- **Cost shape**: file contents dominate the transcript; read sections, not whole files (`context.md`).

## Research

- **Tools**: search · fetch · read section of a document · write notes.
- **Structure**: the one place fan-out genuinely pays — parallel read-only subagents, each returning a bounded summary with its sources, merged by the orchestrator (`multi-agent.md`).
- **Memory**: notes file as the artifact; the transcript must not become the notes.
- **Escalation**: rarely needed — this is the safest agent type because it is read-only, provided fetched content cannot reach a write tool (the trifecta, `security.md`).
- **First failure**: confident synthesis with no traceable source. Require a source id per claim and assert it in the eval set.
- **Cost shape**: fan-out multiplies tokens by `k`; set `k` deliberately and cap it.

## Ops And Infrastructure

- **Tools**: query metrics and logs (read) · describe resources (read) · restart or scale (write) · deploy or delete (irreversible).
- **Autonomy**: read freely; every irreversible action behind approval with a rendered diff, always, whatever the hour.
- **Memory**: the runbook and past incidents are the value (`memory-template.md` artifacts). The infrastructure itself is the source of truth for state.
- **Escalation**: anything customer-visible, anything it has not seen before, anything outside the named blast radius.
- **First failure**: acting on a stale read. Re-read immediately before the write, in the same turn.
- **Cost shape**: log volume. Truncate at the tool boundary or one query eats the window (`tools.md`).

## Data And Reporting

- **Tools**: schema introspection (read) · run a read-only query (read) · write a file or chart (write).
- **Guardrail**: a read-only connection, enforced by the credential, not by the prompt. This is the single control that matters.
- **Verified done**: the query runs and returns rows of the expected shape — use it.
- **First failure**: a plausible query answering a subtly different question. Require the agent to state the question the query answers, in its own words, next to the result.
- **Escalation**: anything writing to a warehouse, and any query whose cost estimate exceeds the budget.

## Inbox And Scheduling

- **Tools**: list and read messages (read) · calendar read · draft (write) · send (external) · create event (write).
- **The defining risk**: every message is untrusted content, and the agent holds both private data and an outbound channel — the full trifecta. Either drafts only, or a strict recipient allowlist (`security.md`).
- **Memory**: per-correspondent context and preferences; the mail system stays the record.
- **First failure**: an auto-reply to a mailing list or an automated sender. Detect list headers and no-reply patterns before any send.
- **Escalation**: unknown sender asking for something, anything financial, anything the user has not replied to in a similar case before.

## Outbound And Sales

- **Tools**: CRM read · enrichment (read) · draft (write) · send (external) · log activity (write).
- **Autonomy**: drafts by default. Sending on behalf of a person is `external` tier and carries reputational blast radius that is invisible in metrics until it is not.
- **Hard constraints**: volume caps per day and per recipient, an unsubscribe path, and no claims outside an approved list. These are code, not prompt.
- **Memory**: contact and account context belongs in the CRM; the shared `contacts.md` holds only people the *user* deals with directly (`memory-template.md`).
- **First failure**: personalization from a hallucinated fact. Every personalized clause cites the field it came from, or it does not ship.

## Content

- **Tools**: research (read) · read the style guide (read) · draft (write) · publish (external or irreversible).
- **Split by mechanical versus judgment**: reformatting, resizing, scheduling, transcription and metadata drafting can be automated; hooks, opinions and anything in the author's voice stay human. The middle band — outlines, variants, summaries — is agent-drafts, human-picks.
- **Memory**: the voice guide is a long text read whole, so it is an artifact, not a memory row (`memory-design.md`).
- **First failure**: fluent output that violates the style guide in ways nobody wrote down. Turn each correction into a banned-phrase or must-contain eval case.

## Voice

- **The constraint is latency**, not quality: every turn is a person waiting. Budget the whole turn end to end and cut the tool set to what fits.
- Prefer a single-turn shape with tools resolved once; a multi-turn deliberation is audible as silence (`architecture.md`).
- Barge-in, partial transcripts and disfluency mean the input is noisier than text — assume the transcription is wrong sometimes and confirm anything irreversible by repeating it back.
- **Escalation** must be instant and warm: a transfer path with the handoff packet delivered to the human before they speak.
- **First failure**: long, correct answers that nobody can follow by ear. Constrain output length hard, in the prompt and in the eval.

## Browser And Computer Use

- **Highest blast radius per action** of any type: the agent operates a real session with real credentials and every page is untrusted content.
- Isolate the session: dedicated profile, no saved passwords, no access to other tabs or the host filesystem, network allowlist (`security.md`).
- Every irreversible click behind approval with a screenshot. Assume the page can lie about what a button does.
- **First failure**: brittleness — a changed selector or layout ends the run. Prefer an API where one exists; use the browser only where none does.
- **Cost shape**: page content and screenshots dominate. Extract, do not paste; cap result size hard (`tools.md`).

## Internal Knowledge

- **Tools**: retrieval over internal documents (read) · fetch the source document (read).
- Retrieval quality is the whole product — that is `rag`, not this skill. What belongs here: permissions per document at retrieval time, freshness of the index, and citation of the source.
- **The defining risk**: answering from a document the asker is not allowed to read. Filter by the *asker's* permissions inside the retrieval call, never after.
- **First failure**: a confident answer from a superseded document. Show the document date next to every citation and prefer recency on conflict.

## Sizing The First Version

Whatever the type, the first version has: one agent, the smallest tool set that completes the happy path, `approve-writes`, all three caps set, an eval set built from ten real inputs, and a trace with the end reason. Everything else — more tools, more autonomy, a second agent — is added against a measured gap.

**When an agent of any type is defined**, write its row in `## Agents` of `~/Clawic/data/agents/memory.md` and its full definition in `~/Clawic/data/agents/specs/<agent>.md` — purpose, user, modality, tools with tiers and idempotency, memory policy, escalation triggers, caps, model bundle — with its `## Boxes` line, in the same turn (`memory-template.md`).
