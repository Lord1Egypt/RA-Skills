# benchmarking

Benchmark models and agents based on **operator leverage**, not just pretty answers.

This skill helps you design, run, and score benchmarks that reflect real production work:
- tool/runtime choice
- hidden constraints
- failure recovery
- proof-oriented completion
- routing decisions for real tasks

## Why this exists
Most model benchmarks are too soft.

They reward:
- formatting
- shallow JSON compliance
- prompt parroting
- polished nonsense

This skill is for building harder evaluations that answer the useful question:

> Which model can operate inside a real environment without making expensive mistakes?

## What a good benchmark tests
- judgment under ambiguity
- hidden constraints
- correct tool/runtime selection
- recovery from provider/harness failure
- proof before claiming success
- business usefulness, not just style

## Benchmark modes

### Design mode
Create a benchmark or full suite.

Typical outputs:
- `README.md`
- `tasks.json`
- `answer-key.json`
- `rubric.md`
- `judge-notes.md`

### Execution mode
Run models through an existing benchmark.

Typical outputs:
- `results-raw.json`
- `results-scored.json`
- `README.md`
- optional infographic or league-table PNG

### Expansion mode
Make existing benchmarks harder or add new tracks.

## Principles
1. Use real work, not toy prompts.
2. Hide important constraints in context, not all in the prompt.
3. Weight judgment above syntax.
4. Include tasks where the correct answer is **not to act immediately**.
5. Separate model failure from harness/provider failure.
6. Save raw results before making pretty charts.
7. Better a verified no-PNG pack than a beautiful lie.

## Recommended benchmark tracks
A strong benchmark suite usually includes some combination of:
- Slack / message triage
- tool routing under constraints
- failure recovery / self-heal
- config safety / docs-first behavior
- delegation + proof of completion

## Failure taxonomy
Use explicit failure classes:
- **MF** — model failure
- **HF** — harness failure
- **PF** — provider failure
- **CF** — context failure
- **PB** — policy block
- **SF** — schema/format failure
- **DF** — delegation failure

## Output standard
Put each benchmark in a folder like:

`output/benchmarks/YYYY-MM-DD-<benchmark-name>/`

Include machine-readable files and human-readable summaries together.

## Success criterion
The benchmark should change model-routing decisions.

If it does not affect which model or agent you would trust for real work, the benchmark is too easy.

## Credits
Built by the [Enterprise Crew](https://github.com/henrino3) for [OpenClaw](https://github.com/openclaw/openclaw).
