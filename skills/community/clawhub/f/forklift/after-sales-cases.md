<!--
Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran"
Licensed under the MIT License - See the complete license at LICENSE.md
-->
# Forklift Repair Case Ledger (Self-Evolving)

> This file is maintained by the `after-sales-service.md` module and is **automatically appended after each real repair Q&A**.
> It is the only knowledge file in this skill that grows over time, and it accepts **only cases that actually occurred**.
>
> 🚫 **Red line:** Never invent cases to fill the ledger. An empty ledger is better than a padded one.
> An empty ledger does not indicate incompetence; a contaminated ledger is harmful because false experience can mislead future users.
>
> Maintainer: Yang Pengfei / Forklift Veteran · Ledger format v1.0

---

## 1. How to Use This Ledger

| Situation | Action |
|------|------|
| A new fault Q&A comes in | **Search this ledger first** (same model + same symptom, then same symptom across models) |
| A similar case is found | Prefer its troubleshooting path; state its confidence rating and hit count |
| No similar case is found | Diagnose from mechanisms in `fault-diagnosis.md`, then **add a new entry** after answering |
| The user follows up with "fixed/not fixed" | **Update the case's follow-up result and confidence**, then increment the hit count |
| An old case is found to be wrong | **Add a new entry** marked `revised-from AS-xxxx`; do not overwrite the original |

---

## 2. Confidence Legend

| Label | Meaning | Recommendation strength next time |
|------|------|--------------|
| ⭐⭐⭐ **Verified** | The user confirmed the repair worked and the result matches the prescribed fix | Recommend first |
| ⭐⭐ **Uncertain** | Feedback is vague or the issue was only partly resolved | List as a candidate and recheck |
| ⭐ **Awaiting follow-up** | Diagnosis was given, but no feedback has been received | Use only as a lead |
| ❌ **Disproved** | The suggested action failed or another cause was found | Deprioritize and note that it previously failed |
| 🚫 **High risk** | Involves a safety red line | Show a prominent warning and refer to the manufacturer |

> Decay rule: After 12 months without another hit, lower the rating by one level. A successful revalidation raises it by one level (see §4.2 of the module).

---

## 3. Required Ledger Fields

```
Case ID          AS-YYYYMMDD-NN
Date recorded    YYYY-MM-DD
Source           User Q&A / user follow-up / author compilation
Vehicle          Brand + model + power type
Symptom          One-sentence description (prefer the user's own words)
Intake details   Vehicle age / operating conditions / intermittent or constant / prior repairs
Checks           Recommended or performed checks
Diagnosis        Mechanism-based assessment (may reference a section in fault-diagnosis.md)
Prescription     Owner checks / workshop tools / refer to manufacturer
Follow-up        Resolved / partly resolved / unresolved / awaiting follow-up / disproved
Confidence       ⭐⭐⭐ / ⭐⭐ / ⭐ / ❌ / 🚫
Hit count        Number (starts at 1)
Notes            Hazards / applicability limits / special cautions
```

---

## 4. Case Ledger

> The ledger starts below. **There are currently no real cases**; the first entry will be added after the first real repair Q&A.
> A **format example** follows the table. It is explicitly marked as an example, is not a real case, and must not be cited as experience.

| Case ID | Date recorded | Source | Vehicle | Symptom | Diagnosis | Prescription | Follow-up | Confidence | Hits |
|--------|----------|------|------|------|------|------|----------|--------|------|
| _(pending)_ | | | | | | | | | |

<!-- Append new cases below the table using the format shown here: -->

---

## 5. Format Example (⚠️ Example Only; Not a Real Case; Never Cite as Experience)

> The entry below **only demonstrates the format**. The vehicle and conclusion are fictional placeholders and are marked `EXAMPLE`.
> When citing this ledger, the agent **must skip every row marked `EXAMPLE`**.

| Case ID | Date recorded | Source | Vehicle | Symptom | Diagnosis | Prescription | Follow-up | Confidence | Hits |
|--------|----------|------|------|------|------|------|----------|--------|------|
| AS-20260930-01 [EXAMPLE] | 2026-09-30 | User Q&A | Fictional brand, 3-ton lithium counterbalance truck | Does not move when shifted while cold; operates normally when warm | Possible oxidized contactor contacts | Owner check: measure contactor coil voltage; workshop check: measure contact voltage drop with a multimeter | Awaiting follow-up | ⭐ | 1 |

**Expanded record (fields that do not fit in the table)**

```
[EXAMPLE] AS-20260930-01
Intake details: Purchased in 2024 / cold-storage use / always occurs when cold / no prior repair
Checks: Contactor coil voltage is a normal 24 V; main contact voltage drop is 1.2 V (high)
Prescription: Clean or replace the contactor; replace the complete unit if contacts are burned
Notes: High humidity in cold storage can frequently oxidize contactors; check this component first on the same model
```

---

## 6. Statistics (May Be Refreshed Periodically by the Agent)

- Total cases: **0**
- Verified (⭐⭐⭐): **0** · Uncertain (⭐⭐): **0** · Awaiting follow-up (⭐): **0** · Disproved (❌): **0** · High risk (🚫): **0**
- Models covered: **0**
- Last updated: **—** (filled automatically after the first entry)

