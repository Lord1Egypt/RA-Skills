# Skills behavior evaluation

[简体中文](guide.md) | [English](guide.en.md)

This guide is for Skills maintainers. Normal chart generation does not require these materials. Run the commands below from the repository root.

## Cases and inputs

[cases.json](cases.json) provides `cases` covering defaults, single and exact target lists, display choices, selected-configuration precedence, `0/false`, station rests and cutoffs, distance and time-based water, and export formats. Each case has Chinese and English original prompts and `variants_zh` / `variants_en` paraphrases; all expressions for a case share the same expectations. `manual_review_cases` covers clarifications, conflicts, implicit Skill selection, and confirmation workflows. All cases use the synthetic [course.gpx](course.gpx) in the same directory.

## Procedure

1. Install and enable the version of `even-effort-pace-chart` under evaluation on the target platform, and confirm the loaded version. Open a separate agent session for each case, language, and expression so previous answers do not influence the result.
2. Extract a prompt: `--variant 1` is the original, and `2` onward are paraphrases in the selected language. The command shows only the prompt and optional `selected_config`, not the expected result:

   ```bash
   python3 skills/even-effort-pace-chart/evals/evaluate.py \
     --case single_target --prompt --language en --variant 2
   ```

3. Supply the prompt, route, and `selected_config` if present as an existing configuration; do not provide expected results. Retain the configuration the agent **actually wrote and used** and the execution trace, then run:

```bash
python3 skills/even-effort-pace-chart/evals/evaluate.py \
  --case single_target --config outputs/candidate.json
```

Use the same case ID and replace `--config` with the actual configuration path. The checker compares effective parameters, targets, station rests, and cutoffs against that case; an omitted `water_mode` means the default distance mode. Exit code `0` means the configuration matches, `1` means it does not, and `2` indicates a command or file error. Interactive cases have no final configuration expectation: extract their prompts and review them manually.

## Manual review and records

Review the trace for correct Skill loading, route inspection, unnecessary questions about defaults, the requested files actually being generated, and the effective parameters being read and checked. For the manual-weather case, also check that the description matches the user's confirmed conditions; the checker validates the source, confirmation, and a non-empty description, but not its meaning.

Extract each `manual_review_cases` expression using `--prompt`, run it in a separate session, and review it manually; do not pass it to the configuration checker:

- For customized water, check that the agent asks what the user wants before generating default amounts or delivering a blank chart. After the user requests a plan based on weather and personal needs, it should follow the time-based workflow.
- For missing personal details, check that the agent asks for the missing date, start time, drinking experience, carrying capacity, and station water availability instead of adopting default amounts. If the user does not know their personal rate, check that the agent asks about training records or sweat rate, explains the limitation, and avoids presenting personalized amounts before confirmation.
- In both scenarios, supply user-confirmed manual weather, personal rate, carrying capacity, and station water availability, then check that the agent generates with `water_mode: "time"` and the appropriate target. It should not ask again for information already provided.
- For the weather preview, verify the date, time zone, and reference target. If the forecast succeeds, check that the agent presents it and waits for the user's confirmation of the weather and personal rate, without generating files or inventing values first. After the evaluator confirms them, check that the agent reuses the complete forecast snapshot and generates the chart. If the forecast is unavailable, the agent should explain that and wait for user-confirmed manual conditions.
- For conflicting and missing targets, check that the agent asks for clarification rather than choosing or inventing a target.
- For implicit Skill selection, install and enable the Skill without naming it in the prompt. If the platform exposes invocation traces, check whether the Skill was selected; otherwise record selection as unverifiable.
- For confirmation before generation, check that the agent presents parameters without writing files before approval. Then request a single five-hour column and SVG only; after confirmation, check the actual configuration and files reflect that latest request.

For every run, record the platform, Skill and model versions, language, case ID, variant number, checker result, and manual review outcome. Record unverifiable or blocked cases separately. A pass rate can describe the runs actually performed, but must not count unexecuted cases as passes.

The checker runs offline without calling an agent. It does not verify execution traces or actual files. Unit tests establish that the checker accepts correct configurations and rejects incorrect ones, not that natural-language evaluations have passed.
