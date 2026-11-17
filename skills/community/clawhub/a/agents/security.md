# Security — Injection, Permissions, And Blast Radius

An agent turns a text vulnerability into an action vulnerability. The model does not need to be "jailbroken" for damage: it only needs to be persuaded by content it read through a tool while holding a credential and an outbound channel.

**Before widening any tool tier or adding an external integration**, read the last red-team report in `~/Clawic/data/agents/artifacts/` (via `## Boxes`) and the agent's `specs/<agent>.md` tool table. Widening a tier that a previous red-team pass closed is the most common way a fixed hole reopens.

**Contents:** [The trifecta](#the-lethal-trifecta) · [Injection](#prompt-injection-through-tools) · [Defenses](#defenses-that-hold) · [Permissions](#permissions-and-blast-radius) · [Sandboxing](#sandboxing-and-egress) · [Secrets](#secrets) · [Data](#data-handling-and-retention) · [Multi-agent](#multi-agent-and-borrowed-tools) · [Red-team](#red-teaming)

## The Lethal Trifecta

Simon Willison's framing, and the most useful security model for agents: serious exfiltration requires all three of

1. **Access to private data** — the user's files, records, or another tenant's rows,
2. **Exposure to untrusted content** — a fetched page, an email, a document, a database row someone else can write,
3. **An outbound channel** — email, HTTP, a message, a URL the agent can cause to be requested.

Remove any one and the class collapses. That is the design question for every agent: which of the three can this loop do without? An agent that reads private data and untrusted content but has no way to send anything out is dramatically safer than one with a "helpful" webhook tool.

## Prompt Injection Through Tools

| Vector | How it arrives | What it achieves |
|---|---|---|
| Indirect injection | Instructions inside a fetched page, email body, PDF, issue comment, calendar invite | The agent follows them as if the user wrote them |
| Poisoned data | A record the attacker can write, read later by the agent | Same, with better timing and no network trace |
| Tool-result injection | A third-party API's error string or field content | Trusted by default because it "came from our tool" |
| Sub-agent output | A worker's summary carrying instructions it read | Crosses the boundary the parent believed was internal |
| Multi-turn conditioning | Small nudges across a long conversation | Constraints erode without any single obvious attack |
| Exfiltration via arguments | Data encoded into a URL, filename, or search query | Leaves through a tool that looks read-only |

There is no known prompt wording that reliably prevents this. Treat instruction-following from tool content as a property to be **contained**, not eliminated.

## Defenses That Hold

- **Enforce in code at the tool layer, never in the prompt** (SKILL.md Rule 6). The invariant: content that entered the context through a tool cannot cause a write, external, or irreversible action in the same task without a human. Implement it as a taint flag on the run, checked by the executor (`implementation.md`).
- **Delimit and label** untrusted content — `<untrusted source="web">…</untrusted>` — and state in the prompt that it is data. This raises the bar; it does not close the hole.
- **Two-agent separation** where the value justifies it: a quarantined reader with no credentials and no outbound tools returns structured extracted fields; the privileged agent never sees the raw content.
- **Allowlist egress** by destination and shape: recipients from a fixed list, URLs from a fixed set of hosts, no free-form outbound. This is what actually stops exfiltration via arguments.
- **Human approval on the tiers that matter** (`human-in-the-loop.md`), showing the rendered arguments — approval on a tool name alone approves nothing.
- **Cap and log** everything: caps bound the damage of a successful attack, logs make it discoverable (`production.md`).

## Permissions And Blast Radius

- Grant the agent's own identity, not a person's. Scoped to the exact resources it needs, revocable independently, and auditable as itself.
- Per-tenant isolation at the storage layer, not by a filter the agent supplies. A missing filter is the cross-tenant leak that ends a product (`memory-design.md`).
- Read and write credentials are different credentials. Same for staging and production.
- Rate-limit per agent identity, per user, and per tool. An abused read tool is a cost incident and a scraping incident at once.
- Time-box elevated access: an approval grants one action, not a session. "Approve for the next hour" is how one approved refund becomes forty.

## Sandboxing And Egress

- Code execution and file access run in an isolated environment with no ambient credentials, a network allowlist, and a filesystem scoped to the task's workspace.
- Default-deny egress. An agent that can reach arbitrary hosts has an outbound channel whatever its tool list says — DNS lookups and image fetches are exfiltration channels.
- Rendered output is a channel too: a markdown image pointing at an attacker's host leaks whatever is in the URL when the client renders it. Sanitize outbound links and images, or disable rendering of remote assets.
- Cap resource use: execution time, memory, output size, and spend. Resource exhaustion is the cheapest attack there is.

## Secrets

- Credentials live server-side in the tool implementation. The agent passes a **reference** — an account id, a connection name — never a value.
- Nothing secret enters the context window: anything in the window can be echoed, logged into a trace, summarized into memory, or extracted by injected content.
- Traces and eval fixtures are copies of the context. Redact before storage, and set retention.
- Nothing under `~/Clawic/data/` ever holds a secret value, including in text the user pastes for safekeeping — strip the value and store `<kind>:<locator>` (`memory-template.md`).

## Data Handling And Retention

- Decide before launch what is stored: transcripts, tool arguments, tool results, memory records, traces. Each has a retention period and an owner.
- Redact personal data before the tool boundary when the `restrictions` preference area says so; redacting after it has been sent is theatre.
- Deletion must reach every copy: record, embedding, summary that quoted it, trace, eval fixture. Design this at the start — retrofitting deletion across five stores is a project.
- Never build an eval set out of raw customer transcripts without stripping personal data first; eval sets get shared, copied, and committed.

## Multi-Agent And Borrowed Tools

- A sub-agent's output is untrusted content to the parent. It was written by a model that read untrusted content (`multi-agent.md`).
- Tier ceilings are enforced at each child's own tool layer. A parent prompt instructing a child to behave is not a control.
- Third-party tool servers put text into your prompt on every turn and can change it without a deploy on your side: review descriptions, assign tiers yourself, namespace on import, and pin versions (`tools.md`).
- A tool that returns URLs the agent will fetch has chained itself into a fetch tool. Count that chain when assessing the trifecta.

## Red-Teaming

Run it as a cadence in `## Due`, not once before launch.

1. **Indirect injection**: instructions planted in every content source the agent reads — page, email, file, record, sub-agent output.
2. **Exfiltration**: get private data into a tool argument, a URL, a filename, a search query, a rendered image.
3. **Approval bypass**: reach an irreversible action through a chain of individually approved steps, or by changing arguments after approval.
4. **Tier escalation**: make a read tool produce a write, or persuade the agent that a tier does not apply.
5. **Persistence**: write instructions into memory that fire on a later session (`memory-design.md`).
6. **Resource exhaustion**: an input that maximizes turns, fan-out, or tool calls until the cap.
7. **Cross-tenant**: user A's data reachable from user B's session.

Every attempt becomes a case in `evals/<agent>.md` with the forbidden tool asserted, so the fix is permanent (`evaluation.md`). Report the bound honestly: zero failures in 50 attempts gives a 95% upper bound near 6% by the rule of three, not zero.

**After every red-team pass**, write `~/Clawic/data/agents/artifacts/red-team-<yyyy-mm>.md` — scope, attempts, findings, fixes, the bound — add its `## Boxes` line, add each attempt as an eval case, and record the run date in `## Due`, all in the same turn (`memory-template.md`). A finding that lives only in a chat is a finding that returns with the next tier widening.
