# Source Schema

Use this lightweight schema to normalize source materials before drafting.

## Intake summary

```yaml
report_month:
bp_period:
node_id:
group_id:
template_path:
spec_path:
bp_source_paths: []
progress_source_paths: []
person_name:
role:
department:
```

## BP anchor map

```yaml
- section_key:
  section_title:
  period_id:
  group_id:
  goal_id:
  personal_bp_id:
  org_bp_ids: []
  bp_target:
  target_metrics: []
  milestone:
  goal_owners: []
  key_results:
    - result_id:
      result_name:
      measure_standard:
      report_cycle:
      owners: []
      action_assignees: []
      actions:
        - action_id:
          action_name:
          assignees: []
```

## Evidence ledger

```yaml
- evidence_id:
  date:
  bp_ids: []
  task_level: goal | key_result | action
  evidence_type: result | action | issue | risk | next_step
  summary:
  progress_facts: []
  completed_items: []
  in_flight_items: []
  blockers: []
  next_steps: []
  metric:
  report_title:
  report_type: manual | ai
  write_emp_name:
  author_priority: primary | secondary | auxiliary | summary_only
  author_matches_current_owner: true | false
  report_id:
  report_link_md:
report_link_status: ready | missing_report_id
attachments: []
attachment_fetch_status:
reply_count:
node_count:
reply_lines: []
node_lines: []
confidence: high | medium | low
```

## Source inventory summary

```yaml
raw_report_hit_count:
candidate_report_count:
adopted_report_count:
adopted_manual_report_count:
adopted_primary_report_count:
adopted_auxiliary_report_count:
adopted_ai_report_count:
coverage_note:
batch_collapse_note:
```

## Section card

```yaml
- section_key:
  heading:
  bp_ids: []
  target_statement:
  result_judgments:
    - result_id:
      result_name:
      measure_standard:
      current_evidence:
      judgment:
      traffic_light_reason:
      human_review_status:
      disagreement_reason_category:
      disagreement_reason_text:
      corrective_plan:
      corrective_due_date:
      next_cycle_actions: []
  selected_evidence: []
  primary_evidence: []
  auxiliary_evidence: []
  progress_points: []
  metrics: []
  section_level_summary:
  risks: []
  next_actions: []
  missing_fields: []
```

## Fine-grained cards

Minimum persisted card units:

- one KR card under `04_cards/kr_cards/`
- one action card under `04_cards/action_cards/`
- one review card per `🟡 / 🔴 / ⚫` block under `05_review_queue/`

## Drafting guidance

When the user has not provided machine-readable data, first convert the raw materials into the schemas above. The conversion step is the control mechanism.

Never treat unstructured BP text as if it were already ready for direct chapter writing.

The primary evidence object should be the original BP report itself:

- report main or title
- report id when exposed by the API
- markdown link in the form `[标题](reportId=<id>&linkType=report)` when available
- author
- report type
- linked task id
- reply list and reply count when exposed
- node-opinion list and node count when exposed
- attachment metadata or attachment links if available

Do not treat a hand-written markdown summary or a dumped local JSON file as the primary evidence object.
Do not stop at source attribution. Convert each source into concrete progress facts that can be used in sections 2-8.
Section 1 should surface both the raw hit count and the adopted source count explicitly so the user can judge whether the draft is under-sampled or over-collapsed.
When the same notification or confirmation content is mass-distributed to many organizations, keep the raw hit count, but collapse those rows into one adopted evidence entry.
