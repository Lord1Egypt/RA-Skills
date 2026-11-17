# Issue and Improvement Log

## Shared Index, Distinct Schemas

Maintain one compact status table for defects and improvements. Each row contains identifier, content label, status, severity, and summary. Detailed entries must have a one-to-one relationship with the index.

Defect fields:

```yaml
type: defect
content_tag: Defect
status: open
severity: medium
found_by:
discovered_at:
fixed_at:
release_note_ready: no
affected_area:
superseded_by:
```

Improvement fields:

```yaml
type: improvement
content_tag: Improvement
status: proposed
severity: medium
proposed_by:
started_at:
completed_at:
release_note_ready: no
affected_area:
superseded_by:
```

Repositories may localize labels and status values, but the type-to-label mapping must remain deterministic.

## Active Log and Archives

Keep the active log bounded to unresolved work, recent completions, and current release candidates. Move older completed records into period-based archives. Preserve identifiers and full record bodies; never copy one identifier into both active and archived files.

Ordinary tasks search the active log first. Archives are opened only by explicit identifier, keyword, release trace, or historical decision need. Validators should check uniqueness and record integrity across both locations without requiring an agent to read every archive.

## Historical Integrity

- Append records; do not erase completed history.
- Correct inaccurate facts explicitly.
- Use `superseded_by` when later behavior replaces an earlier implementation or rule.
- If a timestamp is unknown, write a historical-reconstruction marker instead of inventing a minute.
- If evidence was not retained, say so and identify the present source of truth.
- A completed record must include an end time and verification evidence.
- Small wording, spacing, color, or decorative adjustments may be grouped into one stage record instead of creating one entry per edit.

## Release Candidates

Treat `release_note_ready` as a filter, not a publication event. Any ready record must include concise user-facing release copy. Private paths, secrets, and raw investigation notes must never appear in it.

## Templates

Keep separate templates for defects and improvements at the end of the log. Include every schema key, even when an end-time field is initially empty.
