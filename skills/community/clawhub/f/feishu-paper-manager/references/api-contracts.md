# API Contracts

Use this reference when implementing the Feishu bot to OpenClaw handoff and the downstream result contract.

## Recommended boundary

Keep Feishu-specific event handling outside OpenClaw. Pass OpenClaw a normalized ingestion payload.

Recommended split:

- Feishu bot owns webhook verification, message parsing, attachment download, and chat replies.
- OpenClaw owns paper normalization, metadata extraction, deduplication, summary generation, tagging, doc/table writes, and taxonomy review.

## Ingestion payload

Recommended request shape from Feishu bot to OpenClaw:

```json
{
  "event_id": "evt_01H...",
  "message_id": "om_xxx",
  "message_link": "https://...",
  "chat_id": "oc_xxx",
  "sender": {
    "user_id": "ou_xxx",
    "name": "Alice"
  },
  "sent_at": "2026-03-16T09:30:00+08:00",
  "candidate_index": 0,
  "source": {
    "source_type": "pdf",
    "raw_url": "https://...",
    "pdf_download_url": "https://...",
    "filename": "paper.pdf",
    "mime_type": "application/pdf"
  },
  "context": {
    "text_excerpt": "please save this paper",
    "channel_name": "paper-share",
    "tenant_id": "cli_xxx"
  },
  "options": {
    "force_reclassify": false,
    "skip_taxonomy_review": false
  }
}
```

## OpenClaw result payload

Recommended response shape from OpenClaw back to the Feishu bot:

```json
{
  "status": "created",
  "paper_id": "paper_2026_000123",
  "title": "Example Paper",
  "doc_link": "https://...",
  "table_record_id": "rec_xxx",
  "source_link": "https://...",
  "summary_one_line": "Uses retrieval-augmented planning to improve long-horizon agent decisions.",
  "tags": {
    "topic": ["agent", "retrieval"],
    "method": ["rag", "planning"],
    "task": ["planning"],
    "domain": ["general"],
    "stage": ["reading", "important"]
  },
  "taxonomy": {
    "version": "v2",
    "review_triggered": false
  },
  "dedup": {
    "is_duplicate": false,
    "canonical_paper_id": null
  },
  "errors": []
}
```

Allowed `status` values:

- `created`
- `updated`
- `duplicate`
- `failed`

## Idempotency contract

Use at least two idempotency keys:

- `event_id + candidate_index` for webhook retry protection
- canonical paper fingerprint for record deduplication

Recommended canonical fingerprint inputs:

- DOI if present
- otherwise external paper ID
- otherwise normalized title plus first author plus year

The Feishu bot should be able to safely resend the same payload. OpenClaw must return the same canonical result without creating extra files or rows.

## Feishu API-facing components

When the user asks for implementation details, suggest these abstract interfaces:

```ts
interface FeishuMessageSource {
  verifyEvent(headers: Record<string, string>, body: string): Promise<void>;
  parseCandidates(event: unknown): Promise<PaperCandidate[]>;
  reply(messageId: string, response: BotReply): Promise<void>;
}

interface FeishuDriveStore {
  ensureFolder(path: string[]): Promise<{ folderToken: string }>;
  uploadPdf(input: UploadPdfInput): Promise<{ docLink: string; fileToken: string }>;
  createLinkDoc(input: CreateLinkDocInput): Promise<{ docLink: string; docToken: string }>;
}

interface FeishuTableStore {
  findByFingerprint(input: FindPaperInput): Promise<TableRow | null>;
  createRow(input: CreatePaperRowInput): Promise<TableRow>;
  updateRow(rowId: string, patch: UpdatePaperRowInput): Promise<TableRow>;
  countCanonicalRows(): Promise<number>;
}
```

The concrete SDK does not matter. Preserve this boundary so OpenClaw logic stays testable without Feishu webhook fixtures.

## Taxonomy review contract

OpenClaw should expose a separate review action, even if the first version calls it inline:

```json
{
  "action": "review_taxonomy",
  "trigger_count": 100,
  "current_version": "v2"
}
```

Recommended result:

```json
{
  "status": "completed",
  "old_version": "v2",
  "new_version": "v3",
  "trigger_count": 100,
  "updated_rows": 100,
  "changes": [
    {
      "type": "merge",
      "before": ["instruction-tuning"],
      "after": ["finetuning"],
      "reason": "synonym consolidation"
    }
  ]
}
```

This keeps taxonomy migration explicit and separately retryable.
