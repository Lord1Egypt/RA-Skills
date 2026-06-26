# Artifact Layout

Every report run must leave a folder with both the final report and the intermediate artifacts.

## Folder rule

Use one root folder per node and period:

`<period>_<node>/`

Inside it, use one subfolder per reporting cycle:

- `2026-01/`
- `2026-02/`
- `2026-Q1/`

## Required files per cycle

Each cycle folder should contain the fixed backbone files:

1. `00_intake.yaml`
2. `01_bp_anchor_map.yaml`
3. `02_source_inventory.md`
4. `03_evidence_ledger.md`
5. `04_cards/`
6. `05_ai_baseline_report.md`
7. `05_review_queue/`
8. `07_user_review_report.md`

But the cycle folder should not be treated as a fixed eight-item package forever.

The layout must support dynamic expansion when the template or revision flow requires it, for example:

- `02a_time_attribution_check.md`
- `04_cards/2.1_kr_01.md`
- `04_cards/2.1_kr_02.md`
- `04_cards/4.2_action_01.md`
- `05_review_queue/2.1_kr_02_yellow.md`
- `05_review_queue/4.2_action_01_black.md`
- `06_revision_log.md`
- `07_user_supplied_materials.md`

## File purpose

### `00_intake.yaml`

Stores:

- period
- node
- report cycle
- previous baseline path if any
- template and spec paths
- month attribution mode

Current default `month attribution mode` must be `report_time`.

### `01_bp_anchor_map.yaml`

Stores:

- goals
- key results
- measure standards
- owners and assignees

### `02_source_inventory.md`

Stores:

- raw-hit report count
- candidate report count after time attribution
- adopted report counts and breakdown
- all adopted evidence sources
- source priority
- whether each source is owner-authored or auxiliary

### `03_evidence_ledger.md`

Stores:

- month evidence lines
- time-attribution notes when needed
- source links
- confidence
- traffic-light support notes

### `04_cards/`

Stores:

- structure cards used for drafting
- chosen evidence
- traffic-light judgments
- open gaps

The minimum card unit should be:

- one key-result card
- or one key-action card

This is a required granularity target, not an optional refinement.

### `05_ai_baseline_report.md`

Stores the AI-generated baseline draft.

### `05_review_queue/`

Stores:

- one review card per `🟡 / 🔴 / ⚫` judgment block
- user-required answers
- rectification commitments
- carry-forward reminders

### `07_user_review_report.md`

Stores the user-reviewed monthly or quarterly report.

This is the formal review version, not just the AI baseline.

## Source linking rule

Do not create one local snapshot file per adopted report by default.

The final report and the intermediate markdown artifacts should point directly to the BP report itself, preferably with:

- `[工作汇报标题](reportId=<工作汇报id>&linkType=report)`

If the current API response does not expose `reportId`, keep the minimal source metadata inline:

- title
- author
- task mapping
- evidence priority
- `report_link_status: missing_report_id`

Attachment reading and direct online links should remain pending until upstream APIs expose stable fields for them.

## Minimum source metadata

Each adopted source entry should contain:

- source id, such as `R001`
- report title
- report id when available
- report link markdown when available
- report author
- linked BP task
- source priority: primary / secondary / auxiliary / summary_only
- report type
- concrete progress extraction
- attachment metadata if available

The file header should also contain:

- total raw-hit work-report count
- total candidate report count after time attribution, when different from raw-hit count
- total adopted work-report count
- adopted owner-authored report count
- adopted other-manual report count
- adopted AI report count
- a short source-coverage note
- a short batch-collapse note when notification-style reports were merged

Optional:

- a short note that explains why the source was adopted
- exported attachment files only when the upstream API exposes downloadable attachment links and the user wants local retention
