# How To Use DualGap

DualGap (`dualgap`) is an agent skill for dual-domain research gap analysis. It turns two folders of research-paper PDFs into:

- per-paper critical notes
- independent note reviews
- direction-level syntheses
- cross-direction comparison
- research-gap analysis
- ranked improvement ideas
- validation/audit reports

It is designed for cases where you want to compare two research directions and find meaningful research gaps, not just summarize papers.

## 1. API Configuration Required

The workflow needs an OpenAI-compatible chat completion API before the agent can run the skill. New users should create a local `.env` file and pass its path in the DualGap prompt.

Example env file: `<workspace>\config\qwen.env`

```env
QWEN_API_KEY=your_api_key_here
QWEN_BASE_URL=https://your-openai-compatible-endpoint/v1
QWEN_MODEL=your_model_name
```

For Qwen-compatible deployments, it may look like:

```env
QWEN_API_KEY=your_api_key_here
QWEN_BASE_URL=https://your-openai-compatible-endpoint/v1
QWEN_MODEL=your_model_name
```

`Env prefix` tells the workflow which variable group to read. With `Env prefix: QWEN`, the workflow reads `QWEN_API_KEY`, `QWEN_BASE_URL`, and `QWEN_MODEL`.

Do not commit real API keys. Prefer a local env file outside generated notes and logs.

Alternative: use a JSON config file with:

```json
{
  "base_url": "https://api.example.com/v1",
  "api_key": "your_api_key_here",
  "model": "model-name"
}
```

Then pass the config path in your prompt or command as `--config <workspace>\config\llm_config.json`.

## 2. Use It By Talking To The Agent

Invoke the skill by name and include the API env file in the same request. Copy this template:

```text
Use $dualgap.

LLM API env file:
<ENV_FILE_PATH>

Env prefix:
QWEN

Direction A PDF directory:
<DIR_A>

Direction A name:
<NAME_A>

Direction B PDF directory:
<DIR_B>

Direction B name:
<NAME_B>

Output directory:
<OUT_DIR>

Agenda:
<AGENDA>
```

Concrete example:

```text
Use $dualgap.

LLM API env file:
<workspace>\config\qwen.env

Env prefix:
QWEN

Direction A PDF directory:
<workspace>\papers\agent_self_evolution

Direction A name:
Agent Self-Evolution

Direction B PDF directory:
<workspace>\papers\federated_learning

Direction B name:
Federated Learning

Output directory:
<workspace>\outputs\agent_self_evolution_vs_fl

Agenda:
Please run dual-domain research gap analysis. Prioritize agent self-evolution, skill memory, experience reuse, cross-client personalization, communication/server/token cost, scalability, and how federated learning mechanisms can transfer to self-evolving agents. Do not focus mainly on privacy, fairness, or poisoning attacks.
```

The agent should then:

1. Read the skill instructions in `SKILL.md`.
2. Check the API env file and the two PDF folders.
3. Run `scripts/run_literature_workflow.py`.
4. Generate notes, reviews, syntheses, research gaps, and ranked ideas.
5. Run `scripts/validate_outputs.py <out-dir>`.
6. Report the output paths and validation result.

Use the exact skill trigger `$dualgap`. If you type `$dual-gap` or `$DualGap`, the agent may not recognize the skill.

## 3. Manual Command-Line Usage

From this skill directory:

```powershell
cd <repo-root>\skills\dualgap
python -m pip install -r requirements.txt
```

Run the workflow:

```powershell
python scripts\run_literature_workflow.py `
  --dir-a <workspace>\papers\direction_a `
  --dir-b <workspace>\papers\direction_b `
  --name-a "Direction A Name" `
  --name-b "Direction B Name" `
  --out <workspace>\outputs\dualgap `
  --env-file <workspace>\config\qwen.env `
  --env-prefix QWEN `
  --agenda "Describe your research agenda, priorities, exclusions, and evaluation preferences." `
  --batch-size 10 `
  --max-chars 35000 `
  --max-tokens 5000 `
  --synthesis-tokens 4500 `
  --api-retries 6 `
  --api-timeout 240
```

Validate:

```powershell
python scripts\validate_outputs.py <workspace>\outputs\dualgap
```

Expected:

```text
Workflow outputs are valid.
```

## 4. Cheap Smoke Test

Use this before spending money on a large run:

```powershell
python scripts\run_literature_workflow.py `
  --dir-a <workspace>\papers\direction_a `
  --dir-b <workspace>\papers\direction_b `
  --name-a "Direction A Name" `
  --name-b "Direction B Name" `
  --out <workspace>\outputs\dualgap_smoke `
  --env-file <workspace>\config\qwen.env `
  --env-prefix QWEN `
  --limit-a 1 `
  --limit-b 1 `
  --batch-size 1 `
  --max-chars 30000 `
  --max-tokens 3000 `
  --synthesis-tokens 3500
```

Then:

```powershell
python scripts\validate_outputs.py <workspace>\outputs\dualgap_smoke
```

## 5. Output Files

The output directory contains:

```text
out/
  extracted_texts/
  notes/
    direction_a/*.md
    direction_b/*.md
  reviews/
  syntheses/
    direction_a_synthesis.md
    direction_b_synthesis.md
    cross_direction_analysis.md
    research_gaps.md
    improvement_ideas_ranked.md
  synthesis_reviews/
  raw/
  audit_report.md
  workflow_manifest.json
```

## 6. When To Rerun

Rerun with a larger `--max-tokens` value if notes are truncated. Rerun with smaller `--batch-size` or `--limit-a` / `--limit-b` if testing a new API key or reducing cost.

## 7. Validate The Skill Itself

Run:

```powershell
python scripts\self_validate_skill.py
```

Expected:

```json
{
  "passed": true
}
```

For a real historical validation example, see:

```text
skills-main/validation/paper-research-gap-realrun/manual_validation_case.md
skills-main/validation/paper-research-gap-realrun/outputs/full_20x19
```
