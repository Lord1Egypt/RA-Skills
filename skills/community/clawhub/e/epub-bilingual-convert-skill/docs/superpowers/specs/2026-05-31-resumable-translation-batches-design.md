# Resumable Translation Batches Design

## Goal

Make large EPUB translation tasks efficient, interruptible, resumable, and mechanically verifiable without requiring external translation APIs by default.

## Problem

Large books can contain hundreds of paragraphs and exceed a single response or context window. The current workflow says to fill `extraction.json`, but it does not define how to split work, resume after interruption, reject malformed partial output, or prove that every paragraph was translated exactly once.

The workflow must preserve the existing skill contract:

- Extraction does not translate.
- Translation only fills target-language fields.
- Assembly does not invent translations.
- External APIs or CLI agents are not used unless the user explicitly approves them.

## Recommended Approach

Use a batch manifest and per-batch source/translation files.

The extracted `extraction.json` remains the final source of truth for assembly. Translation work is staged through deterministic batch files:

```text
output/
  extraction.json
  translation_manifest.json
  translation_batches/
    batch_0001.source.json
    batch_0001.translated.json
    batch_0002.source.json
  translation_checkpoints/
    extraction.after_batch_0001.json
```

Each batch is small enough for the current agent/session to translate directly. A batch is merged into `extraction.json` only after validation passes.

## Batch Shape

Each source batch contains immutable paragraph identity and a source hash:

```json
{
  "batch_id": "batch_0001",
  "target_language": "Simplified Chinese",
  "kind": "paragraphs",
  "items": [
    {
      "article_num": 1,
      "paragraph_index": 0,
      "source_hash": "sha256...",
      "source_text": "..."
    }
  ]
}
```

Each translated batch must mirror the same identities:

```json
{
  "batch_id": "batch_0001",
  "translations": [
    {
      "article_num": 1,
      "paragraph_index": 0,
      "source_hash": "sha256...",
      "translated_text": "..."
    }
  ]
}
```

Metadata translation for title, section, and summary may use `kind: "metadata"` batches. Paragraph batches and metadata batches are validated separately because their schemas differ.

## Manifest

`translation_manifest.json` records deterministic batch state:

```json
{
  "schema_version": 1,
  "extraction_path": "extraction.json",
  "target_language": "Simplified Chinese",
  "batching": {
    "max_items": 16,
    "max_source_chars": 8000
  },
  "batches": [
    {
      "batch_id": "batch_0001",
      "kind": "paragraphs",
      "source_file": "translation_batches/batch_0001.source.json",
      "translated_file": "translation_batches/batch_0001.translated.json",
      "status": "pending",
      "item_count": 16,
      "source_hash": "sha256..."
    }
  ]
}
```

Allowed statuses:

- `pending`: source batch exists and has not been applied.
- `done`: translated batch passed validation and was merged.
- `failed`: validation failed; the error is recorded and the batch can be retried.

Recovery always starts from the first `failed` or `pending` batch. `done` batches are not retranslated unless the user explicitly resets them.

## Components

Add focused scripts under `scripts/`:

- `translation_plan.py`: creates `translation_manifest.json` and `.source.json` batch files from `extraction.json`.
- `translation_status.py`: reports completed, failed, pending, and next batch.
- `apply_translation_batch.py`: validates one translated batch and merges it into `extraction.json`.
- `validate_translation.py`: validates the whole translated extraction before assembly.

The scripts should use only Python standard library modules.

## Data Flow

1. Run `scripts/extract.py` to create `extraction.json`.
2. Run `scripts/translation_plan.py extraction.json`.
3. Translate the next source batch with the current agent/session.
4. Save the translated batch beside its source batch.
5. Run `scripts/apply_translation_batch.py extraction.json batch_0001.translated.json`.
6. Repeat from the next pending/failed batch.
7. Run `scripts/validate_translation.py extraction.json`.
8. Run `scripts/assemble.py extraction.json`.

## Validation Rules

Batch apply must reject:

- `batch_id` mismatch.
- Unknown `article_num` or `paragraph_index`.
- Duplicate translated item identity.
- Missing translated item.
- Extra translated item.
- Empty `translated_text`.
- `source_hash` mismatch.
- Any translated batch that changes source fields.

Whole-extraction validation must reject:

- Missing `title_dest_language`.
- Missing `summary_dest_language`.
- `translated_paragraphs` that are not a list.
- Paragraph count mismatch.
- Empty paragraph translations.
- Any article whose required target-language fields are incomplete.

## Checkpoints

After each successful batch apply, write:

```text
translation_checkpoints/extraction.after_<batch_id>.json
```

This gives an audit trail and a manual recovery point if a later operation corrupts the working extraction.

## Testing Requirements

Use small JSON fixtures, not real copyrighted books.

Required tests:

- `translation_plan.py` creates stable batch IDs from the same fixture.
- Large fixtures split by both `max_items` and `max_source_chars`.
- Resume behavior skips `done` batches and reports the next `pending` batch.
- Applying a valid batch fills the expected `translated_paragraphs` slots.
- Applying a batch with a `source_hash` mismatch fails.
- Applying a batch with a missing, duplicate, or extra translation fails.
- Applying a batch with empty translation text fails.
- Whole validation fails when any title, summary, or paragraph translation is missing.
- Whole validation passes on a fully translated fixture.

## Skill Behavior

The skill should instruct agents to use this resumable batch workflow for large books by default. The workflow improves efficiency without treating installed API keys or external CLIs as implicit permission to use third-party services.

If the user explicitly approves an external translation provider, the provider may fill translated batch files, but the same validation and apply scripts still gate all writes into `extraction.json`.
