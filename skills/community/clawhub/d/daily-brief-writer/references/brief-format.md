# Daily Brief Format

Use this reference when the user asks for a polished brief, multiple variants, or a specific audience.

## Section Rules

- Headline: One sentence. State the main business or project implication.
- Done today: Include shipped work, closed decisions, sent deliverables, resolved incidents, and completed reviews.
- In progress: Include ongoing work with current status and the nearest expected checkpoint.
- Blockers / risks: Include dependencies, unclear decisions, missed data, production risk, schedule risk, or ownership gaps.
- Next actions: Start each bullet with a verb. Include owner and date only when provided or safely inferable from the source.

## Compression Rules

- Merge updates that describe the same workstream.
- Drop process chatter unless it explains a decision or risk.
- Keep praise, frustration, and speculation out of the brief unless the user asks for tone preservation.
- Use "Needs confirmation" for important missing details instead of guessing.

## Example

Input:

```text
API pagination fix merged. QA found one edge case on empty results.
Design review moved to Thursday. Need backend estimate for export job.
```

Output:

```markdown
**Daily Brief**
Headline: The API pagination fix is merged, with one QA edge case still open.

Done today:
- Merged the API pagination fix.

In progress:
- QA is checking an empty-results edge case.
- Design review moved to Thursday.

Blockers / risks:
- Export job planning needs a backend estimate.

Next actions:
- Confirm the backend estimate for the export job.
```
