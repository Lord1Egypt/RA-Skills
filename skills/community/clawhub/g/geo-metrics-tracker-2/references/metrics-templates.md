# GEO Metrics Tracker – Reference Templates

This file provides reusable **metric catalog, schema, alert rule, and dashboard layout templates**
for the `geo-metrics-tracker` skill so you don’t have to design them from scratch each time.

Keep this file **short, skimmable, and easy to adapt**. The goal is to provide **structures and
examples** that can be quickly customized to the user’s context.

---

## 1. GEO metrics catalog template (AIGVR / SoM / citations / coverage)

Use this as a starting point when filling in the `## Metrics Catalog` section.

```markdown
| Metric           | Description                                   | Formula / Approximation                          | Dimensions                         | Cadence |
|------------------|-----------------------------------------------|--------------------------------------------------|------------------------------------|---------|
| AIGVR            | AI-generated visibility rate                  | brand-answers / total sampled answers            | platform, intent, locale           | weekly  |
| SoM              | Share of Model vs. competitors                | brand answers / all brand+competitor answers     | platform, intent, competitor       | weekly  |
| Citation Volume  | Count of AI citations of our brand/resources  | number of links/mentions in sampled outputs      | platform, page, intent             | daily   |
| Intent Coverage  | # of intents where we appear at all           | count of intents with ≥1 brand citation          | platform, intent cluster           | monthly |
| Response Latency | Time for models to reflect key site changes   | days between change shipped and answer updated   | platform, change_type (content/schema) | ad hoc  |
```

In real projects:

- Adjust `Cadence` to match the team’s real review rhythm (daily / weekly / monthly).
- If the team already has internal KPI names, you can add an extra `Internal Name` column to map.

---

## 2. Metric storage schema template

Use this as a base when describing the **warehouse/table schema** in
`## Tracking Schema & Storage`. The example below assumes a single daily-grain metrics table.

```markdown
| Column            | Type        | Description                                                         |
|-------------------|------------|---------------------------------------------------------------------|
| date              | DATE       | Statistics date (UTC or business timezone; document this clearly). |
| platform          | STRING     | AI platform (chatgpt / perplexity / gemini / claude / sge, etc.).  |
| intent_id         | STRING     | Intent or query-cluster ID.                                        |
| intent_name       | STRING     | Human-readable name of the intent.                                 |
| locale            | STRING     | Locale / region (e.g. en-US, zh-CN).                               |
| brand             | STRING     | Brand name.                                                         |
| competitor        | STRING     | Competitor name (or NULL / 'none' if not applicable).              |
| aigvr             | FLOAT      | AIGVR value for this slice on this date.                           |
| som               | FLOAT      | SoM value for this slice on this date.                             |
| citation_volume   | INT        | Count of citations in sampled answers.                             |
| coverage_flag     | BOOLEAN    | Whether the brand appeared at least once for this intent.          |
| sample_size       | INT        | Number of sampled answers for this slice/date.                     |
| data_source       | STRING     | Origin of data (manual_sample / report_export / api / logs, etc.). |
| updated_at        | TIMESTAMP  | Last update timestamp for this row.                                |
```

You can also split tables **by platform** or **by grain**, but keep the same design principles:
columns should be clear, well-documented, and easy for downstream BI tools to use without guesswork.

---

## 3. Alert rules & anomaly detection templates

Use these patterns in the `## Alerts & Anomaly Rules` section. You can mix **table-style summaries**
with **pseudo‑YAML** for implementation notes.

### 3.1 Table-style overview

```markdown
| Metric          | Condition example                                        | Severity  | Channel            | Notes                                                        |
|-----------------|----------------------------------------------------------|-----------|--------------------|--------------------------------------------------------------|
| AIGVR           | current_3d_avg < 0.7 * previous_14d_avg                 | critical  | Slack #geo-alerts  | Sustained AIGVR drop on core intents; treat as major event. |
| SoM             | drop > 15% vs previous_28d_avg for key competitor       | warning   | Email GEO owner    | Share-of-model loss vs a key competitor; investigate.       |
| CitationVolume  | change > +100% vs previous_7d_avg                       | info      | Slack #geo-notifs  | Strong positive spike, possible opportunity.                 |
| Coverage        | coverage_flag flips 1→0 for any Tier-1 intent          | critical  | PagerDuty / Oncall | Potential structural issue (model “forgetting” content).    |
```

### 3.2 YAML snippet template

```yaml
alert: low_aigvr_core_intents
metric: aigvr
scope:
  platform: "ChatGPT"
  intent_cluster: "core-product"
condition: "current_3d_avg < 0.7 * previous_14d_avg"
severity: critical
channel: "Slack #geo-alerts"
runbook: "geo-metrics-tracker/runbooks/low_aigvr_core_intents.md"
```

In real-world scenarios:

- `scope` can include more granular fields such as `locale`, `brand`, and `competitor`.

- `runbook` points to internal team documentation or a "Incident Playbook" snippet generated by this skill.

---

## 4. Dashboard layout templates

For `## Dashboards & Views`, a typical three-tier view is provided: top-level, operations, and experimentation.

### 4.1 Executive view structure

```markdown
### Executive GEO Health Dashboard
- Top KPIs (cards)
  - AIGVR (overall, last 30d vs previous 30d)
  - SoM (top 10 intents, last 30d)
  - Citation Volume (total & by platform)
  - Coverage (# of active intents)
- Trend charts
  - AIGVR (90d) by platform
  - SoM (90d) vs main competitor
- Highlights
  - Biggest positive movers (intents with strongest uplift)
  - Biggest negative movers
```

### 4.2 Operations view structure

```markdown
### GEO Ops Dashboard
- Table: Intents x Platform with AIGVR / SoM / Citation Volume (sortable, filterable)
- Chart: AIGVR by intent cluster (last 30d)
- Chart: Citation volume vs content release timeline (campaign overlays)
- Table: Alerts fired in last 14d with status & owner
```

### 4.3 Experiment / campaign view structure

```markdown
### GEO Experiment View
- Selector: Experiment / Campaign
- Pre vs Post comparison:
  - AIGVR
  - SoM
  - Citation Volume
- Timeline:
  - Key releases (content / schema / llms.txt changes)
  - Metric curves overlaid
```

---

## 5. Sampling workflow pseudo-code template

When users need to collect AI answers in a "semi-automatic" or "scripted" manner, the following pseudocode/structure can be used as an example.

```python
def sample_answers(platform: str, intents: list[str]) -> list[dict]:
    \"\"\"Pseudo-code: The results are either obtained by calling the platform interface or by manually copying and pasting, and then structured into a unified format.\"\"\"
    results = []
    for intent in intents:
        # This can be an API call or data read from a manual table.
        answers = fetch_answers_from_platform(platform, intent)
        for ans in answers:
            results.append(
                {
                    "platform": platform,
                    "intent_id": intent.id,
                    "intent_name": intent.name,
                    "raw_answer": ans.text,
                    "has_brand": detect_brand(ans.text),
                    "has_competitor": detect_competitor(ans.text),
                    "links": extract_links(ans.text),
                }
            )
    return results
```


