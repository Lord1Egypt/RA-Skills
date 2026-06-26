---
name: brainforge-autoresearch
description: >-
  Use when user wants to optimize, improve, benchmark, or evaluate a skill's prompt.
  Triggers on "optimize skill", "improve skill prompt", "benchmark skill", "eval skill",
  "run autoresearch", "tune prompt", "prompt optimization", "skill evaluation",
  "A/B test prompt", "find best prompt", "auto-improve skill".
  Runs automated prompt experiments using the Karpathy autoresearch pattern.
version: 0.2.5
metadata:
  author: zning1994
  openclaw:
    requires:
      anyEnv:
        - MINIMAX_API_KEY
        - OPENAI_API_KEY
        - ANTHROPIC_API_KEY
      anyBins:
        - python3
        - python
    primaryEnv: OPENAI_API_KEY
    optionalEnv:
      - OPENAI_BASE_URL
      - OPENAI_API_BASE
    homepage: https://github.com/zning1994/brainforge-autoresearch
    os:
      - macos
      - linux
---

# brainforge-autoresearch

> Previously published as `autoresearch` / `openclaw-autoresearch`. Renamed for the brainforge marketplace rollout — functionality unchanged.

Autonomous prompt optimization for AI agent skills. Runs controlled experiments to find better prompt variants using the [Karpathy autoresearch pattern](https://github.com/karpathy/autoresearch): generate hypothesis, mutate prompt, evaluate, repeat.

## When to use

- 用户说"优化一下这个 skill" / User says "optimize this skill's prompt"
- 用户要对比不同 prompt 版本的效果 / User wants to benchmark prompt variants
- 用户说"run autoresearch on X" / "eval skill X" / "improve skill X"
- 用户对 skill 输出质量不满，想系统性改进 / User is unhappy with skill output quality and wants systematic improvement

**Do not use:**
- 一次性的小改动（直接改 prompt 即可） / One-off prompt tweaks — just edit the prompt directly
- 调试某个特定失败 case / Debugging a specific failure — investigate the root cause instead
- Skill 脚本本身有 bug（代码逻辑问题不是 prompt 问题） / Skill script has a bug — fix the code, not the prompt

## Requirements

- Python 3.10+
- `autoresearch.py` script in the skill directory
- LLM API access (MiniMax, OpenAI, or Anthropic)
- Target skill must have a prompt file (SKILL.md, SYSTEM.md, or similar)

## Procedure

Always follow these steps in order: (1) Create eval.json, (2) Run autoresearch command, (3) Review results and apply best prompt.

### Step 1: Gather context

Before running, you need:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--target` | Path to the skill directory or prompt file to optimize | `../workspace/skills/brain-search/SKILL.md` |
| `--evals` | Path to eval definition JSON file | `eval.json` |
| `--provider` | LLM provider for running experiments | `minimax` (default), `openai`, `anthropic` |
| `--runs` | Number of runs per experiment (statistical significance) | `5` (default) |
| `--max-experiments` | Maximum experiments before stopping | `30` (default) |
| `--dashboard` | Open live results dashboard in browser | flag, no value |

### Step 2: Create eval.json

Define test inputs and evaluation criteria. Each eval is a binary pass/fail check.

```json
{
  "test_inputs": [
    "search for latest AI agent frameworks",
    "find news about LLM inference optimization",
    "搜一下 transformer 架构的最新进展"
  ],
  "evals": [
    {
      "name": "has_sources",
      "type": "rule",
      "rule": "regex",
      "pattern": "(https?://|Source:|来源:)"
    },
    {
      "name": "no_hallucinated_urls",
      "type": "rule",
      "rule": "banned_phrases",
      "phrases": ["example.com", "placeholder.url"]
    },
    {
      "name": "sufficient_detail",
      "type": "rule",
      "rule": "word_count",
      "min": 50,
      "max": 500
    },
    {
      "name": "contains_summary",
      "type": "rule",
      "rule": "contains",
      "values": ["summary", "key findings", "结论"]
    },
    {
      "name": "no_apology_prefix",
      "type": "rule",
      "rule": "not_contains",
      "values": ["I apologize", "I'm sorry, but"]
    },
    {
      "name": "actionable_output",
      "type": "llm",
      "question": "Does the response provide actionable information the user can immediately use (links, specific facts, concrete next steps)?",
      "pass_description": "The response contains specific actionable items like URLs, concrete facts, or clear next steps",
      "fail_description": "The response is vague, generic, or lacks specific actionable information"
    }
  ]
}
```

**Rule types:**

| Rule | Parameters | Description |
|------|-----------|-------------|
| `regex` | `pattern` | Pass if regex matches output |
| `banned_phrases` | `phrases` (list) | Pass if NONE of the phrases appear |
| `word_count` | `min`, `max` (optional) | Pass if word count is within range |
| `contains` | `values` (list), optional `match`: `"any"` (default) or `"all"` | Pass if any/all values appear in output (case-insensitive) |
| `not_contains` | `values` (list) | Pass if NONE of the values appear in output (case-insensitive) |

**LLM eval type:**

| Field | Description |
|-------|-------------|
| `type` | Must be `"llm"` |
| `name` | Unique name for this eval |
| `question` | What to ask the judge LLM about the output |
| `pass_description` | Description of what a passing output looks like |
| `fail_description` | Description of what a failing output looks like |

See `eval-guide.md` for detailed guidance on writing effective evals.

### Step 3: Run autoresearch

```bash
python autoresearch.py \
  --target ../workspace/skills/brain-search/SKILL.md \
  --evals eval.json \
  --provider minimax \
  --runs 5 \
  --max-experiments 30 \
  --dashboard
```

### Step 4: Review results and apply changes

The script writes results to `results.tsv` in the working directory. Each row is one experiment:

```
experiment_id  parent_id  mutation_description  avg_score  pass_rate  evals_detail  prompt_diff
```

Find the best performing variant:
```bash
cat results.tsv | sort -k4 -nr | head -5
```

Apply the winning prompt to your skill by copying the optimized prompt text to replace the original.

## Example: optimizing brain-search

```
User: brain-search 的搜索结果经常缺少来源链接，帮我优化一下

完整流程:

1. 创建 eval.json:
   {
     "test_inputs": [
       "search for latest news on OpenAI",
       "搜一下最新的 AI 芯片进展",
       "find recent papers on RAG optimization",
       "what happened with Anthropic this week",
       "查查 GPU 价格趋势"
     ],
     "evals": [
       {
         "name": "has_urls",
         "type": "rule",
         "rule": "regex",
         "pattern": "https?://[^\\s]+"
       },
       {
         "name": "min_2_sources",
         "type": "rule",
         "rule": "regex",
         "pattern": "https?://[^\\s]+.*https?://[^\\s]+"
       },
       {
         "name": "structured_output",
         "type": "llm",
         "question": "Is the output well-structured with clear sections?",
         "pass_description": "Output uses clear structure like bullets or headers",
         "fail_description": "Output is a wall of text without clear structure"
       }
     ]
   }

2. 运行命令:
   python autoresearch.py \
     --target ../workspace/skills/brain-search/SKILL.md \
     --evals eval.json \
     --runs 5 \
     --max-experiments 20

3. 查看并应用结果:
   - 检查 results.tsv 找最高分变体
   - 查看 mutation_description 了解关键改动
   - 将最佳 prompt 应用到原始 SKILL.md
```

## Failure handling

| Issue | Action |
|-------|--------|
| LLM API rate limit | Script auto-retries with backoff; if persistent, reduce `--runs` |
| Target file not found | Check path, must be readable prompt/skill file |
| All experiments score 0 | Evals may be too strict — review eval definitions, loosen criteria |
| Script crashes mid-run | Results already written to `results.tsv` are preserved; re-run continues |

## Gotchas

- 每次实验会调用 LLM 多次（runs x test_inputs x llm_evals），注意 API 用量 / Each experiment makes multiple LLM calls — watch API usage
- LLM eval 本身有噪声，`--runs` 设高一点（5+）才有统计意义 / LLM evals are noisy, use 5+ runs for statistical significance
- Rule evals 比 LLM evals 更稳定、更便宜，优先用 rule / Rule evals are more stable and cheaper — prefer them
- Baseline 分数太低（< 20%）说明 eval 定义可能有问题，先修 eval / If baseline score is very low, fix evals first
- 优化 prompt 不能解决架构问题（比如搜索 API 本身返回差结果） / Prompt optimization cannot fix architectural issues
