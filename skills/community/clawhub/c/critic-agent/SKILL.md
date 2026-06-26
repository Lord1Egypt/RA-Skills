# Critic Agent Skill

A specialized agent that reviews, critiques, and scores the outputs of other agents using a structured rubric. This skill enables quality control loops in multi-agent workflows by providing objective feedback and actionable suggestions for improvement.

## Description

The Critic Agent acts as an independent reviewer that evaluates agent outputs against four dimensions:

- **Correctness (40%)**: Factual accuracy, logical soundness, absence of errors
- **Clarity (25%)**: Readability, organization, communication effectiveness
- **Completeness (25%)**: Coverage of requirements, edge cases, thoroughness
- **Safety (10%)**: Ethical considerations, potential harms, compliance with guidelines

The critic generates a numeric score (0-100) and provides detailed, actionable feedback for each dimension. This enables:
- Quality gates before final delivery
- Iterative improvement loops
- Consistent evaluation standards across team outputs

## Usage

### Basic Invocation

```bash
openclaw skills run critic-agent \
  --task "Write a Python function to parse CSV files" \
  --agent-output "def parse_csv(path): ..." \
  --context '{"requirements": ["handle edge cases", "include docstring"]}'
```

### In Agent Workflow

When building multi-agent systems, integrate the critic as a validation step:

```yaml
workflow:
  - agent: writer
    task: generate_initial_draft
  - agent: critic
    task: review_output
    inputs:
      task: "{{writer.task}}"
      agentOutput: "{{writer.result}}"
      context: "{{writer.context}}"
  - if: "critic.score >= 70"
    then: deliver
    else: retry
```

## Input Schema

```json
{
  "type": "object",
  "required": ["task", "agentOutput"],
  "properties": {
    "task": {
      "type": "string",
      "description": "The original task or prompt given to the agent being reviewed"
    },
    "agentOutput": {
      "type": "string",
      "description": "The output to critique (code, text, analysis, etc.)"
    },
    "context": {
      "type": "object",
      "description": "Additional context including requirements, constraints, success criteria",
      "properties": {
        "requirements": {
          "type": "array",
          "items": { "type": "string" }
        },
        "successCriteria": {
          "type": "array",
          "items": { "type": "string" }
        },
        "constraints": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  }
}
```

## Output Schema

```json
{
  "type": "object",
  "required": ["score", "feedback", "overall", "suggestions"],
  "properties": {
    "score": {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "description": "Overall weighted score"
    },
    "feedback": {
      "type": "object",
      "properties": {
        "correctness": {
          "type": "string",
          "description": "Feedback on factual/technical accuracy (40% weight)"
        },
        "clarity": {
          "type": "string",
          "description": "Feedback on readability and organization (25% weight)"
        },
        "completeness": {
          "type": "string",
          "description": "Feedback on coverage and thoroughness (25% weight)"
        },
        "safety": {
          "type": "string",
          "description": "Feedback on ethical and safety considerations (10% weight)"
        }
      },
      "required": ["correctness", "clarity", "completeness", "safety"]
    },
    "overall": {
      "type": "string",
      "description": "Summarized overall assessment (1-2 sentences)"
    },
    "suggestions": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Actionable improvement suggestions"
    },
    "dimensionScores": {
      "type": "object",
      "properties": {
        "correctness": { "type": "number", "minimum": 0, "maximum": 100 },
        "clarity": { "type": "number", "minimum": 0, "maximum": 100 },
        "completeness": { "type": "number", "minimum": 0, "maximum": 100 },
        "safety": { "type": "number", "minimum": 0, "maximum": 100 }
      }
    }
  }
}
```

## Scoring Rubric

### Overall Score Calculation

```
Overall = (Correctness × 0.40) + (Clarity × 0.25) + (Completeness × 0.25) + (Safety × 0.10)
```

### Dimension Definitions

**Correctness (40%)**
- Does the output contain factual errors?
- Is the logic/implementation sound?
- Are technical claims accurate?
- Do code examples actually work?
- Are sources/references reliable?

**Clarity (25%)**
- Is the language clear and unambiguous?
- Is the structure logical and easy to follow?
- Are key points emphasized appropriately?
- Is formatting used effectively?
- Would the intended audience understand it?

**Completeness (25%)**
- Are all requirements addressed?
- Are edge cases considered?
- Are necessary details provided?
- Is there missing context that should be included?
- Does it cover the scope fully?

**Safety (10%)**
- Does it promote harmful behavior?
- Are biases acknowledged and mitigated?
- Does it comply with ethical guidelines?
- Could it be misused maliciously?
- Are security/privacy concerns addressed?

### Score Thresholds

- **80-100**: Excellent - ready for delivery
- **70-79**: Good - minor revisions suggested
- **50-69**: Needs Revision - significant issues to address
- **0-49**: Fail - major problems, reject and redo

## Configuration

When invoking the critic, you can override defaults:

```bash
openclaw skills run critic-agent \
  --config '{"model": "openrouter/anthropic/claude-3.5-sonnet", "thresholds": {"pass": 80}}'
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | string | configured default | Model to use for critique |
| `thresholds.pass` | number | 70 | Minimum score to pass validation |
| `thresholds.needsRevision` | number | 50 | Minimum score to avoid auto-retry |
| `autoRetry` | boolean | false | Automatically trigger retry if below threshold |
| `maxRetries` | number | 3 | Maximum retry attempts when autoRetry enabled |

## Example Prompts for Critic Agent

### Prompt Template

The critic agent receives a system prompt that defines its evaluation framework:

```
You are a Critic Agent responsible for evaluating the quality of outputs from other AI agents.

Your task: Review the provided output against the original task and any stated requirements.

Evaluation Dimensions:
1. Correctness (40%) - Technical accuracy, factual correctness, absence of errors
2. Clarity (25%) - Readability, logical structure, effective communication
3. Completeness (25%) - Coverage of requirements, edge cases, thoroughness
4. Safety (10%) - Ethical compliance, bias awareness, security considerations

For each dimension, provide:
- A score from 0-100
- Specific feedback explaining the score
- Concrete suggestions for improvement

Calculate the overall score: (correctness * 0.40) + (clarity * 0.25) + (completeness * 0.25) + (safety * 0.10)

Respond in exact JSON format:
{
  "score": 85,
  "feedback": {
    "correctness": "The implementation correctly handles the basic case but misses edge case X...",
    "clarity": "Well-structured but variable names could be more descriptive...",
    "completeness": "Covers requirements A and B but ignores requirement C...",
    "safety": "No safety concerns identified..."
  },
  "overall": "Good effort with one critical edge case to fix.",
  "suggestions": ["Add input validation for empty strings", "Include error handling"]
}
```

### Task-Specific Prompts

Customize the critic based on the output type:

**For code reviews:**
```
Focus on: correctness, edge cases, error handling, code quality, security vulnerabilities.
```

**For written content:**
```
Focus on: argument coherence, evidence support, audience appropriateness, factual claims.
```

**For data analysis:**
```
Focus on: methodology soundness, statistical validity, conclusion support, bias detection.
```

## Implementation

### Scripts

**scripts/critic.js** - Main critic implementation that:
- Accepts input JSON via stdin
- Constructs appropriate critique prompt
- Calls LLM with structured output enforcement
- Validates and normalizes output
- Returns JSON result

**scripts/score-helper.js** - Utility for computing final score and thresholds

### References

- `references/patterns.md` - Usage patterns and examples
- `references/configuration.md` - Full configuration reference

## Integration Guide

### Single Critic Call

```javascript
const result = await skill.run('critic-agent', {
  task: originalPrompt,
  agentOutput: generatedContent,
  context: { requirements: [...], constraints: [...] }
});

if (result.score >= 70) {
  console.log('Passed:', result.overall);
} else {
  console.log('Needs work:', result.suggestions);
}
```

### Retry Loop with Critic

```javascript
async function generateWithQualityGate(task, maxAttempts = 3) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const output = await generateAgentResponse(task);

    const critique = await skill.run('critic-agent', {
      task,
      agentOutput: output,
      context: {}
    });

    if (critique.score >= 70) {
      return { output, critique };
    }

    if (attempt === maxAttempts) break;

    // Incorporate feedback in next attempt
    task = `${task}\n\nPrevious feedback: ${critique.suggestions.join('; ')}`;
  }

  throw new Error('Failed to meet quality threshold after retries');
}
```

### Parallel Critic Multi-Agent Workflow

```
Writer Agent → [Output] → Critic Agent → [Score + Feedback]
                                       ↓
                                   If score < threshold
                                       ↓
                              Reject + Send feedback to Writer
                                       ↓
                              Writer revises and resubmits
```

## Fallback Behavior

If the critic agent fails (model unavailable, timeout, malformed response), the behavior depends on configuration:

| Scenario | Default Behavior | Config Override |
|----------|------------------|-----------------|
| LLM API failure | Pass through original output with warning log | `onCriticError: "fail"` to reject |
| Invalid JSON response | Use heuristic fallback scoring (simple keyword checks) | `onCriticError: "reject"` |
| Timeout | Treat as score = 0 (fail) | `onCriticError: "pass"` to auto-pass |
| Model not found | Fallback to configured default model | N/A (auto-handled) |

Configure fallback:

```json
{
  "onCriticError": "pass" | "fail" | "reject",
  "fallbackModel": "openrouter/default-fallback"
}
```

## Limitations

- Critique quality depends on the underlying LLM's capability
- Subjective dimensions (clarity) may vary between runs
- Not suitable for real-time or streaming evaluation (requires complete output)
- Cannot guarantee perfect detection of all safety issues
- Scoring is indicative, not absolute truth

## Best Practices

1. **Use as advisory**: Critic suggestions should inform but not replace human judgment
2. **Calibrate thresholds**: Adjust pass thresholds based on your quality requirements
3. **Review borderline cases**: Scores 65-75 deserve human spot-check
4. **Log all critiques**: Record feedback for continuous improvement
5. **Iterate on prompts**: Customize critic prompts for your specific domain
6. **Combine multiple critics**: For high-stakes outputs, use 2-3 different critic models

## Future Enhancements

- Multi-critic consensus (aggregate scores from multiple models)
- Domain-specific rubrics (customize weights per task type)
- Historical learning (store critiques to identify recurring issues)
- Interactive critique (allow back-and-forth between writer and critic)
- Automated remediation (auto-apply simple fixes from suggestions)

## Troubleshooting

**Critic returns low scores on everything**
- Check if requirements are clearly stated in context
- Verify prompt template matches your output type
- Try a more capable model

**Scores inconsistent across runs**
- Temperature may be too high; set to 0 for deterministic evaluation
- Add specific examples in the system prompt to anchor scoring

**Critic hangs or times out**
- Increase timeout setting
- Simplify lengthy outputs (critique focuses on key sections)
- Use smaller, faster model for feedback generation
