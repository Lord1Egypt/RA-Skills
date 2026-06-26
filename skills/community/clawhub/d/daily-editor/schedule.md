# Scheduling

Use this reference when the user wants `私人编辑部` to run on a schedule instead of as a one-off edition.

## What to confirm

Before setting up or describing a timed workflow, confirm:

- cadence: daily, weekdays, weekly, or custom
- exact delivery time
- timezone
- output destination: local PDF file, folder, inbox-like handoff, or preview directory
- whether the run should stop at draft or continue to final delivery
- whether preview is required before final delivery

## Default recommendation

For local recurring runs:

1. generate a dated single-file A4 portrait PDF artifact
2. save it to a stable output directory
3. use a system scheduler to run the generation step
4. preview only if the user asked for a human-in-the-loop flow

## macOS recommendation

Prefer `launchd` for long-term local scheduling on macOS.

Use `cron` only when:

- the user explicitly prefers it
- the task is simple
- there is no need for richer launchd behavior

## Scheduling patterns

### Daily morning push

- cadence: daily
- time: 08:00
- purpose: morning scan before work

### Workday brief

- cadence: weekdays
- time: 09:00
- purpose: avoid weekend noise

### Weekly issue

- cadence: weekly
- time: Sunday 20:00
- purpose: summary + next week watchlist

## Output naming

Prefer predictable file naming:

- `private-editorial-YYYY-MM-DD.pdf`
- `issue-YYYY-MM-DD.pdf`
- `topic-name-YYYY-MM-DD.pdf`

Keep the directory stable so previews and downstream automation are easy.

## Preview-aware scheduling

If preview is required:

1. generate a draft PDF file
2. if needed, preview the print-first render source before final export
3. finalize after review
4. save or distribute the final version

If preview is not required:

1. generate directly to final output
2. save with dated filename
3. log enough metadata to trace each issue

## Minimal scheduling handoff

If actual automation is not being set up in the current environment, return:

- the generation command or workflow
- the output path
- the schedule specification
- a short note on the recommended scheduler

## Example schedule specs

### Example 1

```text
每天早上 8 点生成私人编辑部，输出到 ~/Documents/private-editorial/
```

Interpretation:

- cadence: daily
- time: 08:00
- timezone: local timezone unless specified otherwise
- output: local folder
- format: PDF

### Example 2

```text
每个工作日 9 点推送 AI + 科技版，先生成 pdf，必要时让我预览。
```

Interpretation:

- cadence: weekdays
- time: 09:00
- sections: AI, technology
- output: PDF
- workflow: draft first, preview if needed
