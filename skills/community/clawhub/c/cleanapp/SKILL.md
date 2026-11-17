---
name: cleanapp-report-problem
description: Prepare and submit an observed physical or digital problem to CleanApp, choose publication and notice permissions, or track recorded review decisions and actions. Use for a user's hazard, access barrier, waste, infrastructure, software bug, scam or service failure report. Excludes ordinary advice, emergency dispatch and autonomous bulk collection.
metadata: {"clawdbot":{"homepage":"https://www.cleanapp.io/agents","requires":{"bins":["python3"]}}}
---

# Report a problem to CleanApp

Start at **https://www.cleanapp.io/agents**; its linked `agents.txt` names the current endpoints. The public first-report paths need no account or API key. A listing or skill file supplies instructions; it does not grant network access or install an MCP connector.

Use only the observation the user wants to send. Preserve uncertainty and source context; do not invent a location, incident, independent verification or a promised fix. Include optional coordinates only when supplied or approved. Send the approved report text, not unrelated conversation or credentials.

## Connected MCP client

Connect **https://live.cleanapp.io/openai/mcp** using **Streamable HTTP**, authentication **none**. The `/openai/` path also serves generic MCP clients; the optional interactive widget is for supporting hosts.

1. Call `cleanapp_prepare_report` with the factual observation and explicit `handling`. New MCP previews default to `{publication:"automatic",notices:"automatic"}`: eligible publication and responsible-party notices after server privacy/eligibility checks. Offer `publication:"private"` and `notices:"none"` when requested. Display the exact report and both permission disclosures; preparing is not submission or approval. Set `requires_redaction:true` if the user requests privacy review or declares private information. Omitting it never certifies privacy clearance.
2. After the user approves that preview, its publication/notice permissions and sending it, call `cleanapp_submit_report` with the unchanged `draft_token` and `confirmed:true`. Permissions cannot be upgraded at submission or retry. Older sealed private drafts retain their original private handling.
3. Return the private receipt. Use `cleanapp_report_status` for its recorded outcome and next action while processing is pending. Unknown delivery is a reason to check the receipt before retrying the same draft.

## Client with outbound HTTPS POST

The included Python client discovers the current public endpoint. `description` alone is enough; title, source URL, agent name and coordinates are optional. No CleanApp API token is read or required.

For automatic handling, prepare JSON containing the user's real observation plus these explicitly approved permissions:

```json
{"description":"<the actual observed problem>","handling":{"publication":"automatic","notices":"automatic"}}
```

Show the exact content and permissions before sending. This HTTPS client's default omission of `handling` preserves private publication and no notices for older workflows. To request those explicitly, use `{"publication":"private","notices":"none"}`. Do not add a nested Wire `report`, `schema_version` or human-readable source ID to this public payload.

Preview the user's exact report offline:

```bash
python3 report.py --input approved-report.json --dry-run
```

Send only when authorized for that exact content and destination:

```bash
python3 report.py --input approved-report.json --submit --receipt-file private-receipt.json
python3 report.py --status --receipt-file private-receipt.json
```

The client generates a private random UUIDv4 `source_id` before sending and stores its checkpoint/receipt with mode 0600. Keep the receipt file private. If delivery is unknown, reuse the same input and file with `--retry --submit`; do not create another UUID for the same attempt. Changed input must be a separate report.

If the host only browses GET pages, or its execution tool has no outbound network, it cannot submit directly. Explain the missing capability and provide the canonical `/agents` link or the exact prepared request for an authorized network-enabled client. Never turn submission into a GET request or claim a report was sent without a receipt.

## Receipt meaning and advanced ingestion

Reports start in **private quarantine**. Analysis is the normal review: the private receipt's `outcome` records processing, decision/reason, publication, delivery evidence and next action. Return those specific states; check status again while `final` is false. A `cluster_candidate` is additional independent evidence for a related issue, retaining the reporter's observation and attribution. Exact request replay means the same submission was already received; it is a separate technical fact. Pending is not sent, and an evidence-backed send does not mean read or fixed. Final means this processing cycle ended, not issue resolution. Unsafe or ineligible actions can be held with a reason; neither publication nor notices are guaranteed. No reputation credit or payment is promised. Respect `429`/`Retry-After`; do not retry aggressively.

For request fields, status, retries and authenticated higher-volume Wire/CLI use, read [the API reference](references/API_REFERENCE.md). The advanced Wire path has separate API-key requirements; this public first-report skill does not provision those keys.
