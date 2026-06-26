# Experiment Results Report Template

Template for the markdown report generated in Step 10. All `{PLACEHOLDERS}` are
replaced at generation time.

## Timestamp Conventions

- **Header fields** (Start Time, End Time): full ISO 8601 with timezone
  (e.g., `2025-03-30T14:05:32+08:00`)
- **Timeline tables**: time-only in UTC (e.g., `05:05:32`), column header
  marked "Time (UTC)". No milliseconds.
- Timeline events are embedded in each service's section — no standalone
  timeline section.

## File Naming

```bash
TIMESTAMP=$(TZ=Asia/Shanghai date +%Y-%m-%d-%H-%M-%S)
SCENARIO_SLUG=$(echo "{SCENARIO_NAME}" | tr '[:upper:]' '[:lower:]' | tr ' :/' '-')
# File: ${EXPERIMENT_DIR}/${TIMESTAMP}-${SCENARIO_SLUG}-experiment-results.md
```

---

## Report Structure

```markdown
## FIS Experiment Results

**Experiment ID:** {EXPERIMENT_ID}
**Template ID:**   {TEMPLATE_ID}
**Stack:**         {STACK_NAME}
**Status:**        {FINAL_STATUS}
**Start Time:**    {START_TIME}
**End Time:**      {END_TIME}
**Duration:**      {ACTUAL_DURATION}

### Action Results

| Action | Action ID | Status | Start (UTC) | End (UTC) | Duration |
|---|---|---|---|---|---|
| {action_name} | {action_id} | {status} | {HH:MM:SS} | {HH:MM:SS} | {duration} |

### Stop Condition Alarms

| Alarm | Final Status |
|---|---|
| {alarm_name} | {OK/ALARM} |

### Per-Service Impact Analysis

For EACH service listed in the README's "Affected Resources" table, create a sub-section below.
Also include indirectly affected services (e.g., services impacted by network
disruption even without a dedicated FIS action).

#### {Service Name} ({resource_identifier})

| Time (UTC) | Event | Observation |
|---|---|---|
| {HH:MM:SS} | {event} | {what was observed at this point} |
| {HH:MM:SS} | {event} | {observed result / status change} |
| ... | ... | ... |

**Key Findings:**
- {finding_1 — what happened and why}
- {finding_2 — recovery behavior}

(Repeat for each service)

### Application Log Analysis

Embed the analysis output from app-service-log-analysis Step 7 here.
Use the report structure defined in app-service-log-analysis SKILL.md:
Summary table, per-application error timeline, key error patterns,
log samples, insights, cross-service correlation, and recommendations.

If application log collection was skipped (kubectl not available), include a note:
```
Application log collection was skipped (kubectl not available).
Only managed service logs were analyzed.
```

### Recovery Status Summary

| Resource | Recovery Status | Notes |
|---|---|---|
| {service} | {Recovered / Partially Recovered / Recovering} | {details} |

### Issues Requiring Attention

#### 1. {Issue title}
- **Problem:** {description}
- **Recommendation:** {action to take, with CLI command if applicable}

### Cleanup

{cleanup instructions with CLI commands — reference the stack name for CFN cleanup}

### Appendix: Log File Locations

**Raw log directory:** `{LOG_DIR}`

| Application | Log File |
|---|---|
| {namespace/deployment} | `{LOG_DIR}/{service}/{deployment}.log` |
```
