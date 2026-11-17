# AI Short Drama Workload Estimation

Use this reference to produce a defensible workload estimate. Always state assumptions and distinguish creative labor, generation operations, and wall-clock queue time.

## Inputs

- `episodes`: number of finished episodes.
- `duration`: target seconds per episode.
- `avg_shot`: average accepted shot length in seconds.
- `variants`: generated takes per accepted shot, including alternates.
- `rework`: extra ratio for prompt/reference failures.
- `characters`: unique principal characters requiring continuity.
- `scenes`: unique recurring scenes.
- `complexity`: `low`, `medium`, or `high`.
- `parallel`: concurrent paid generation tasks.
- `avg_generation_minutes`: average queue+render time per generation task.

## Base formulas

- `shots_per_episode = ceil(duration / avg_shot)`
- `total_shots = episodes × shots_per_episode`
- `raw_generations = ceil(total_shots × variants × (1 + rework))`
- `keyframes = ceil(total_shots × 1.2)`
- `generation_wall_hours = raw_generations × avg_generation_minutes / parallel / 60`

Default assumptions:

- `rework = 0.15`
- `variants = 2.5` for a consistency-sensitive cartoon
- `avg_shot = 8` seconds
- `parallel = 4`
- `avg_generation_minutes = 8` for 15–30 second tasks
- complexity multiplier: low `0.80`, medium `1.00`, high `1.35`

## Person-hour model

Use these as planning baselines, then replace with observed production data.

- prompt and shot design: `total_shots × 0.12 × complexity`
- character/scene consistency review: `total_shots × 0.06 × complexity`
- generation operations and take selection: `raw_generations × 0.05 × complexity`
- visual QC and regeneration decisions: `total_shots × 0.08 × complexity`
- asset preparation: `8 + 2 × characters + 0.4 × scenes`
- editing and finishing: `episodes × duration/60 × 2.2 × complexity`
- voice/TTS direction and cleanup: `episodes × duration/60 × 1.2 × complexity`
- subtitles: `episodes × 0.5`
- lip-sync: `total_shots × 0.35 × 0.12 × complexity`
- production management: `12%` of the above
- QA/release buffer: `10%` of the above

## Delivery estimate

- `person_days = total_person_hours / 8`
- `wall_days ≈ person_days / team_size × 1.15 + generation_wall_hours / 24`
- storage: `raw_generations × 0.04 GB + keyframes × 0.002 GB + total_shots × 0.02 GB + 5 GB project overhead`
- For a first pilot, use 3 episodes or 3 trailers and add a separate approval gate before scaling.

## Reference baseline

For 60 episodes × 120 seconds × 15 shots per episode:

- accepted shots: `900`
- raw generations at 2.5 variants and 15% rework: about `2,588`
- generation wall time at 4 parallel tasks × 8 minutes: about `86 hours`
- this is not a one-week solo workload; schedule and budget must reflect batch generation and QC.

## Reporting format

Always report:

1. accepted shots;
2. raw generations;
3. keyframes;
4. person-hours by role;
5. person-days;
6. estimated wall-clock days;
7. storage;
8. assumptions and excluded costs;
9. paid-generation gate.

Do not present a single total without its assumptions. If the user supplies actual per-shot retry rates, use them instead of defaults.
