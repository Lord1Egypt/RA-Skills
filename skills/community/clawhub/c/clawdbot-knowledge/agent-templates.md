# Agent Reference: Sub-Agent Templates

Use these templates when delegating sub-tasks to specialized agents.

## Researcher Agent

```markdown
# Agent: Researcher
## Task
Research {topic} and compile findings.

## Method
1. Search web for {query terms}
2. Fetch top 3-5 relevant sources
3. Extract key facts, data points, opinions
4. Cross-reference across sources
5. Compile structured summary

## Output Format
Write findings to `agents/research-{topic}.md`:
- **Summary** (2-3 sentences)
- **Key Findings** (bullet points with source attribution)
- **Data Points** (any numbers, stats, dates)
- **Conflicting Information** (if any)
- **Sources** (URLs with brief description)
```

## Builder Agent

```markdown
# Agent: Builder
## Task
Build {artifact} according to specifications.

## Specifications
{detailed specs from parent task}

## Tech Stack
{languages, frameworks, dependencies}

## Output
- Main artifact at `agents/build-output/{filename}`
- Any supporting files in same directory
- Brief notes on design decisions in `agents/build-notes.md`

## Quality Checks
- Code lints without errors
- Handles edge cases: {list}
- Follows conventions: {list}
```

## Reviewer Agent

```markdown
# Agent: Reviewer
## Task
Review {artifact} for quality and correctness.

## Review Criteria
1. Completeness: Does it meet all requirements?
2. Correctness: Are there bugs, errors, or inaccuracies?
3. Quality: Is it well-structured and maintainable?
4. Edge Cases: Are edge cases handled?

## Input
- Artifact at: {path}
- Requirements at: {path}

## Output
Write review to `agents/review-{artifact}.md`:
- **Verdict**: PASS / NEEDS_CHANGES / FAIL
- **Issues Found** (severity: critical/major/minor)
- **Suggestions** (optional improvements)
```

## Transformer Agent

```markdown
# Agent: Transformer
## Task
Transform {input_format} to {output_format}.

## Input
- Source file: {path}
- Source format: {description}

## Output
- Target file: `agents/transform-output/{filename}`
- Target format: {description}

## Mapping Rules
{field mappings, transformations, filters}

## Validation
- Input row/record count: {n}
- Expected output row/record count: {n}
- Key fields to verify: {list}
```

## Analyst Agent

```markdown
# Agent: Analyst
## Task
Analyze {dataset/situation} and provide insights.

## Data Sources
- {path to data}
- {additional context}

## Analysis Goals
1. {question to answer}
2. {pattern to identify}
3. {comparison to make}

## Output
Write analysis to `agents/analysis-{topic}.md`:
- **Executive Summary**
- **Methodology**
- **Findings** (with supporting data)
- **Recommendations**
- **Visualizations** (describe charts if applicable)
```
