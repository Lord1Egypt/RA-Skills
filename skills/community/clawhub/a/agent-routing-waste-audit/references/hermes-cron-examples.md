# Hermes Cron List Examples

Two contrasting examples showing real vs. false positive candidates.

## False Positive — Script-only job at high frequency

```
5233cac535ea [active]
    Name:      hermes-health-watchdog
    Schedule:  */5 * * * *
    Repeat:    ∞
    Next run:  2026-05-30T12:15:00+08:00
    Deliver:   local
    Last run:  2026-05-30T12:11:07.249028+08:00  ok
```

**NOT a waste candidate.** `prompt_preview` from JSON is `bash /root/.hermes/scripts/health_watchdog.sh` — pure bash script, zero LLM tokens regardless of frequency. Do not flag.

**From JSON:**
```json
{
  "prompt_preview": "bash /root/.hermes/scripts/health_watchdog.sh",
  "skills": [],
  "model": null
}
```

## Real Candidate — Skill-chained job at high frequency

```
abc123def456 [active]
    Name:      seo-daily-synthesis
    Schedule:  */5 * * * *
    Repeat:    ∞
    Next run:  2026-05-30T12:15:00+08:00
    Deliver:   origin
    Skills:    investment-research-core
    Last run:  2026-05-30T12:10:59.123456+08:00  ok
```

**High-priority candidate.** 288 runs/day with a skill chain that invokes an LLM on every tick.

**From JSON:**
```json
{
  "prompt_preview": "You are an SEO data analysis assistant...",
  "skills": ["investment-research-core"],
  "model": "MiniMax-M2.7",
  "provider": "minimax"
}
```

## Low Risk — Daily job

```
760c41123c8f [active]
    Name:      vps-disk-daily-check
    Schedule:  0 9 * * *
    Repeat:    ∞
    Next run:  2026-05-31T09:00:00+08:00
    Deliver:   local
    Last run:  2026-05-30T09:01:00.169080+08:00  ok
```

~1 run/day. Not a priority regardless of what it does.

## One-shot disambiguation

```
33ae1c5e3d8a [active]
    Name:      InferClaw Tools 14天SEO报告
    Schedule:  once at 2026-06-13 09:00
    Repeat:    0/1
    Next run:  2026-06-13T09:00:00+08:00
    Deliver:   origin
    Skills:    web-research, lark-sheets
    Last run:  —  (not yet run)
```

**`Repeat: 0/1` = one-shot.** Zero recurrence risk. Do not flag.