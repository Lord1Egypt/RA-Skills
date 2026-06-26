# Eval Guide: Writing Effective Eval Criteria

How to write eval criteria that actually improve your skill's output. This guide covers the hybrid rule+LLM eval system used by brainforge-autoresearch (previously `openclaw-autoresearch`).

## The Golden Rule

**Binary yes/no only. No scales.**

Every eval must produce a pass or fail. Not "7/10", not "mostly good", not "needs improvement". Pass or fail.

Why: Scales are subjective (your 7 is my 5), hard to optimize against, and create noise. Binary forces you to define exactly what "good" means.

Bad: "Rate the tone from 1-5"
Good: "Does the output use a professional tone without slang or emojis?"

## Rule-Based Evals

Rule-based evals cost zero tokens, run instantly, and are 100% consistent. Use them whenever possible.

### `regex`

Pattern matching against the output text.

```json
{
  "type": "rule",
  "name": "has_date_format",
  "rule": "regex",
  "pattern": "\\d{4}-\\d{2}-\\d{2}",
  "description": "Output contains a date in YYYY-MM-DD format"
}
```

```json
{
  "type": "rule",
  "name": "has_markdown_headers",
  "rule": "regex",
  "pattern": "^#{1,3} .+",
  "description": "Output uses markdown headers"
}
```

Useful for: format validation, structure checks, required patterns.

### `banned_phrases`

Exact phrases that must not appear in the output.

```json
{
  "type": "rule",
  "name": "no_filler",
  "rule": "banned_phrases",
  "phrases": ["as an AI", "I cannot", "I'm sorry but", "it depends", "各方面", "总的来说"],
  "description": "No AI disclaimers or vague filler phrases"
}
```

Useful for: removing AI-speak, enforcing brand voice, blocking lazy language.

### `word_count`

Min and/or max word limits. For Chinese text, counts characters.

```json
{
  "type": "rule",
  "name": "length_check",
  "rule": "word_count",
  "min": 100,
  "max": 500,
  "description": "Output is between 100-500 words"
}
```

Useful for: preventing one-line answers, keeping outputs concise, matching format requirements.

### `contains`

Required keywords or phrases that must appear.

```json
{
  "type": "rule",
  "name": "has_source",
  "rule": "contains",
  "values": ["Source:", "Reference:", "来源:"],
  "match": "any",
  "description": "Output cites at least one source"
}
```

`match` can be `"any"` (at least one) or `"all"` (every value must appear).

```json
{
  "type": "rule",
  "name": "has_all_sections",
  "rule": "contains",
  "values": ["## Summary", "## Action Items", "## Risks"],
  "match": "all",
  "description": "Output has all required sections"
}
```

Useful for: enforcing structure, required sections, key terminology.

### `not_contains`

Phrases or patterns that must NOT appear.

```json
{
  "type": "rule",
  "name": "no_placeholder",
  "rule": "not_contains",
  "values": ["TODO", "TBD", "FIXME", "[insert", "[placeholder"],
  "description": "No placeholder text left in output"
}
```

Useful for: catching incomplete outputs, blocking specific content.

## LLM-Based Evals

LLM evals handle semantic judgments that rules cannot express. They cost tokens and have slight variance, so use them only when necessary.

### When to Use LLM Evals

Use LLM when you need to judge:
- Accuracy against source material (hallucination detection)
- Logical coherence or reasoning quality
- Whether advice is actionable vs. generic
- Tone, style, or audience-appropriateness
- Semantic completeness (did it cover all key points?)

Do NOT use LLM for things rules can handle:
- Word count, format checks, required sections (use rules)
- Presence of specific keywords (use contains)
- Forbidden phrases (use banned_phrases)

### Writing Good LLM Eval Questions

```json
{
  "type": "llm",
  "name": "no_hallucination",
  "question": "Compare the output against the provided input data. Does every claim in the output have a corresponding fact in the input? Ignore formatting and phrasing differences.",
  "pass_description": "Every factual claim maps to input data. No invented statistics, dates, or details.",
  "fail_description": "Contains at least one claim not supported by the input data."
}
```

Key principles:
1. **Be specific about what to check.** Not "is this good?" but "does every claim have a source?"
2. **Tell the LLM what to compare against.** "Compare against the input data" or "based on the search results provided."
3. **Define pass and fail concretely.** The LLM judge needs clear criteria, not vibes.
4. **One judgment per eval.** Don't ask "is it accurate AND well-structured?" -- split into two evals.

### Bad vs Good Examples

Bad:
```json
{
  "question": "Is this a good summary?",
  "pass_description": "It's good",
  "fail_description": "It's bad"
}
```

Good:
```json
{
  "question": "Does the summary capture the 3 most important findings from the search results, without adding information not present in the results?",
  "pass_description": "All 3 key findings are mentioned. No information is fabricated beyond what the search results contain.",
  "fail_description": "Misses one or more key findings, or includes claims not supported by the search results."
}
```

## Examples by Skill Type

### Text/Copy Skills (newsletters, reports, summaries)

Typical eval mix:
- `banned_phrases`: remove filler ("总的来说", "as mentioned above", "综上所述")
- `word_count`: enforce length constraints
- `contains`: required sections or keywords
- LLM: accuracy check against source material
- LLM: actionability or specificity check

### Search Skills (web search, knowledge search)

Typical eval mix:
- `contains`: must cite URLs or sources
- `not_contains`: no hallucination markers ("[Source needed]", made-up URLs)
- LLM: does summary reflect actual search results
- LLM: is output well-structured with clear sections

### Code Generation Skills

Typical eval mix:
- `regex`: output contains code blocks (`` ```\w+ ``)
- `not_contains`: no placeholder code ("pass", "# TODO")
- `contains`: includes error handling patterns ("try", "except" or "catch")
- LLM: does the code solve the stated problem

### Translation Skills

Typical eval mix:
- `banned_phrases`: no untranslated source language fragments
- `word_count`: reasonable length ratio to source
- LLM: semantic equivalence to source text
- LLM: natural fluency in target language (no translationese)

### Data Extraction Skills

Typical eval mix:
- `regex`: output matches expected data format (JSON, CSV, etc.)
- `contains`: all required fields present
- LLM: extracted values are accurate against source
- LLM: edge cases handled (missing data, ambiguous values)

## Common Mistakes

### Too many evals (> 6)

More evals means more constraints. Past 6, the optimizer starts gaming individual evals at the expense of overall quality. The prompt becomes a checklist-satisfier instead of genuinely good.

**Fix**: Pick the 4-5 that matter most. If you can't decide, you don't understand what "good" means for this skill yet.

### Overlapping evals

If two evals test similar things, a failure on one is always a failure on the other. You're just adding noise.

Example of overlap:
- Eval A: "No filler language"
- Eval B: "Every sentence adds new information"

These catch the same problem. Pick one.

### Too vague

"Is the output helpful?" -- helpful to whom, for what? The LLM judge can't read your mind.

**Fix**: Replace with "Does the output provide at least 2 specific, actionable next steps the reader can take this week?"

### Too narrow

"Does the output mention React hooks?" -- this only works for one specific input. It will fail or be irrelevant for other test cases.

**Fix**: Evals should apply to ALL test inputs. If it's input-specific, it's not an eval -- it's a test assertion.

### Unmeasurable by LLM

"Will this output generate more revenue?" -- no LLM can judge this. Stick to things observable in the text.

**Fix**: Replace with proxies: "Does the output include a clear call-to-action?" or "Are the benefits described in concrete terms with numbers?"

## The 3-Question Test

Before adding any eval, ask:

1. **Can I explain pass/fail to a stranger in one sentence?**
   If not, the eval is too vague.

2. **Will this eval produce the same result on every test input?**
   If it only applies to some inputs, it's too narrow.

3. **Can a rule handle this instead?**
   If yes, use a rule. Save LLM evals for semantic judgments.

## Template

```json
{
  "evals": [
    {
      "type": "rule",
      "name": "short_snake_case_name",
      "rule": "contains|banned_phrases|word_count|regex|not_contains",
      "description": "One sentence: what this checks"
    },
    {
      "type": "llm",
      "name": "short_snake_case_name",
      "question": "Specific question for the LLM judge to answer about the output.",
      "pass_description": "Concrete description of what a passing output looks like.",
      "fail_description": "Concrete description of what a failing output looks like."
    }
  ],
  "test_inputs": [
    {
      "name": "descriptive_scenario_name",
      "input": "The actual input that will be sent to the skill."
    }
  ]
}
```

Start with 2-3 test inputs and 3-4 evals. Add more only after running a few optimization rounds and seeing where the gaps are.
