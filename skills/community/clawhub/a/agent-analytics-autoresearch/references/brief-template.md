# Growth Loop Brief

## Target

- Project:
- Surface:
- Public URL:
- Local source file or copy source:
- Primary metric:
- Proxy metric:
- Guardrail metrics:
- Recommended experiment name:
- Variant shape:

```text
variants: control,candidate_1,candidate_2
goal: <primary_event>
proxy: <proxy_event>
```

## Product Truth

Describe what the product is, who it serves, and what must remain true in every candidate.

Include:

- core promise
- target audience
- strongest differentiator
- language the product should own
- claims the product can support
- claims the product should not make

## Audience

Primary audience:

-

Pain:

-

Desired action:

-

## Current Control

Headline:

```text

```

Subheadline:

```text

```

Primary CTA:

```text

```

Supporting copy:

```text

```

## Analytics Commands Or Data

List commands, API calls, SQL queries, exports, or pasted data the agent should use before generating variants.

Agent Analytics CLI example:

```bash
# Run once if this machine or agent runtime is not logged in.
npx --yes @agent-analytics/cli@0.5.31 login

PROJECT_SLUG=<project_slug>
PRIMARY_EVENT=<primary_event>
PROXY_EVENT=<proxy_event>
RUN_DATE=$(date +%F)

mkdir -p "data/$RUN_DATE"

# Keep collecting the full snapshot even if one analytics command fails.
# Failed commands write their error output and exit code into the saved file.
run_snapshot_command() {
  output_file="$1"
  shift
  set +e
  "$@" > "$output_file" 2>&1
  command_status=$?
  set -e
  perl -i -pe 's/\e\[[0-9;]*m//g' "$output_file"
  if [ "$command_status" -ne 0 ]; then
    printf '\ncommand_exit_code: %s\n' "$command_status" >> "$output_file"
  fi
}

run_snapshot_command "data/$RUN_DATE/insights.txt" npx --yes @agent-analytics/cli@0.5.31 insights "$PROJECT_SLUG" --period 7d
run_snapshot_command "data/$RUN_DATE/pages.txt" npx --yes @agent-analytics/cli@0.5.31 pages "$PROJECT_SLUG" --since 7d
run_snapshot_command "data/$RUN_DATE/funnel.txt" npx --yes @agent-analytics/cli@0.5.31 funnel "$PROJECT_SLUG" --steps "page_view,$PROXY_EVENT,$PRIMARY_EVENT" --since 7d
run_snapshot_command "data/$RUN_DATE/${PROXY_EVENT}-events.txt" npx --yes @agent-analytics/cli@0.5.31 events "$PROJECT_SLUG" --event "$PROXY_EVENT" --days 7 --limit 50
run_snapshot_command "data/$RUN_DATE/${PRIMARY_EVENT}-events.txt" npx --yes @agent-analytics/cli@0.5.31 events "$PROJECT_SLUG" --event "$PRIMARY_EVENT" --days 7 --limit 50
run_snapshot_command "data/$RUN_DATE/experiments.txt" npx --yes @agent-analytics/cli@0.5.31 experiments list "$PROJECT_SLUG"
```

Generic placeholders:

```bash
<analytics-command> summary --project <project> --period 7d
<analytics-command> pages --project <project> --period 7d
<analytics-command> events --project <project> --event <proxy_event> --period 7d
<analytics-command> events --project <project> --event <primary_event> --period 7d
<analytics-command> funnel --project <project> --steps "page_view,<proxy_event>,<primary_event>"
<analytics-command> experiments --project <project> list
```

## Live Data Snapshot

Summary:

-

Primary event:

-

Proxy event:

-

Guardrails:

-

Data limitations:

-

## Drift Constraints

Candidates must not:

-

Candidates should:

-

## Judging Rubric

Rank candidates by:

- specificity to this product
- clarity for the target audience
- likely primary-event intent
- preservation of product truth
- low competitor-sayable language
- fit with available analytics data
