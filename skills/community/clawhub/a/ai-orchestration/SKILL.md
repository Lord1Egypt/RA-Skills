---
name: ai-orchestration
description: "Multi-agent AI orchestration, prompt engineering, and eval-driven development. Design, coordinate, and evaluate AI agent systems with structured communication and context management."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata:
  version: "2.0.0"
  author: "Tim van Maurik"
  category: "Dev Workflow"
  tags: [multi-agent, prompt-engineering, eval-driven, orchestration]
---

# AI Orchestration Skill — Multi-Agent Systems

Design, coordinate, and evaluate multi-agent AI systems. This skill covers agent architecture, prompt engineering patterns, eval-driven development, and context management for AI agents.

## When to Use This Skill

### Explicit Triggers
- "Design multi-agent system"
- "Orchestrate AI agents"
- "Write prompt for agent"
- "Build eval framework"
- "Coordinate parallel AI tasks"

### Implicit Detection
- Complex task requiring specialization
- Multiple independent subtasks
- Need for agent communication
- Evaluating AI output quality
- Managing context across agents

## Multi-Agent Architecture

### Agent Decomposition Pattern

Break complex tasks into specialized agents:

```
Orchestrator (main context)
├── Planner Agent     → Designs approach, identifies files
├── Implementer Agent → Writes code following plan
├── Reviewer Agent    → Reviews code for quality/security
├── Tester Agent      → Writes and runs tests
└── Documenter Agent  → Updates docs and README
```

**Principles:**
- Each agent has single responsibility
- Orchestrator manages high-level state
- Agents communicate via structured output
- Sub-agents receive focused, complete instructions

### Parallel vs Sequential

```
PARALLEL (independent tasks):
- Security review + Performance review + Type check
- Multiple file searches across different directories
- Independent repo enhancements

SEQUENTIAL (dependent tasks):
- Plan → Implement → Test → Review
- Read file → Edit file → Verify edit
- Clone repo → Create branch → Make changes → Push → Create PR
```

**Decision Guide:**
- Use parallel when tasks are independent
- Use sequential when output of one task is input to next
- Mix patterns for complex workflows

### Context Isolation Strategy

```
Main Context (orchestrator):
- Keeps high-level state and progress
- Delegates detailed work to sub-agents
- Aggregates results from sub-agents

Sub-Agent Context:
- Receives focused, complete instructions
- Has access to tools but limited context
- Returns structured summary to orchestrator
- Does not see other sub-agent outputs
```

**Benefits:**
- Each agent stays focused
- Context windows remain manageable
- Easier to debug individual agents
- Can parallelize independent agents

## Prompt Engineering Patterns

### Role-Task-Context-Format (RTCF)

```
ROLE: You are a senior security engineer with 10 years of experience
      in authentication systems and OAuth implementations.
TASK: Review this code for vulnerabilities following OWASP Top 10.
CONTEXT: This is an Express.js API handling user authentication with
      JWT tokens. The API is used by 10k+ daily users.
FORMAT: For each issue, provide:
  - severity: critical|high|medium|low
  - file:line
  - description
  - recommended fix
  - CVSS score if applicable

Start your review now:
```

### Chain of Thought (CoT)

```
Think step by step:
1. First, identify what the code does
2. Then, check for input validation
3. Next, trace data flow from input to output
4. Finally, identify any points where unsanitized data reaches sensitive operations

Apply this to the following code:
```

### Few-Shot Learning

```
Here are examples of good commit messages:

feat(dashboard): add threat severity chart
- Displays threat levels by category
- Interactive filtering by severity
- Links to detailed threat reports

fix(api): handle timeout in proxy server
- Added connection timeout (30s)
- Implemented retry logic (3 attempts)
- Added circuit breaker pattern

security: add CSP headers to express middleware
- Added Content-Security-Policy header
- Allowed same-origin scripts only
- Blocked inline script execution

Now write a commit message for these changes:
[git diff output]
```

### Structured Output

```
Return your security analysis as JSON:

{
  "summary": "Total: 5 issues (1 critical, 2 high, 2 medium)",
  "issues": [
    {
      "severity": "critical",
      "category": "injection",
      "file": "routes/auth.js",
      "line": 42,
      "description": "SQL injection vulnerability in login query",
      "fix": "Use parameterized queries",
      "cve_potential": true
    }
  ],
  "recommendations": [
    "Implement input validation middleware",
    "Add rate limiting to auth endpoints",
    "Use prepared statements for all queries"
  ]
}

Do not include any text outside the JSON.
```

## Eval-Driven Development (EDD)

### Define Evals Before Building

```python
# eval_suite.py
from typing import List
from dataclasses import dataclass

@dataclass
class EvalCase:
    input: str
    expected: str
    criteria: List[str]

@dataclass
class EvalResult:
    score: float
    passed: bool
    feedback: str

class PromptEval:
    def __init__(self, prompt_template: str):
        self.template = prompt_template
        self.test_cases: List[EvalCase] = []

    def add_case(self, input: str, expected: str, criteria: List[str]):
        """Add a test case for the prompt."""
        self.test_cases.append(EvalCase(input, expected, criteria))

    def run(self, model: str) -> dict:
        """Run all test cases and return results."""
        results = []
        for case in self.test_cases:
            # Format prompt with input
            formatted_prompt = self.template.format(input=case.input)

            # Call model
            output = call_model(model, formatted_prompt)

            # Evaluate output
            score = self._evaluate(output, case.expected, case.criteria)
            results.append({
                'input': case.input,
                'output': output,
                'expected': case.expected,
                'score': score
            })

        return {
            'prompt': self.template,
            'model': model,
            'results': results,
            'avg_score': sum(r['score'] for r in results) / len(results)
        }

    def _evaluate(self, output: str, expected: str, criteria: List[str]) -> float:
        """Score output against expected result and criteria."""
        score = 0.0

        # Correctness (40%)
        if expected.lower() in output.lower():
            score += 0.4

        # Completeness (30%)
        for criterion in criteria:
            if criterion.lower() in output.lower():
                score += 0.1

        # Format/Structure (30%)
        if self._is_well_formatted(output):
            score += 0.3

        return min(score, 1.0)

    def _is_well_formatted(self, output: str) -> bool:
        """Check if output follows expected structure."""
        # Implement format validation
        return len(output.split('\n')) >= 3


# Usage
eval_suite = PromptEval(
    "Summarize this article: {input}\n\nProvide 3 bullet points."
)

eval_suite.add_case(
    input="AI is transforming healthcare...",
    expected="AI in healthcare",
    criteria=["machine learning", "diagnosis", "treatment"]
)

eval_suite.add_case(
    input="Climate change impacts...",
    expected="Climate change",
    criteria=["rising temperatures", "extreme weather", "solutions"]
)

results = eval_suite.run("claude-sonnet-4")
print(f"Average score: {results['avg_score']:.2f}")
```

### Evaluation Criteria

| Criteria | Weight | How to Measure |
|----------|--------|---------------|
| Correctness | 40% | Output matches expected result |
| Completeness | 30% | All required elements present |
| Safety | 15% | No harmful/biased content |
| Format | 10% | Follows requested structure |
| Conciseness | 5% | Token count efficiency |

### A/B Testing Prompts

```python
from prompt_eval import PromptEval

# Prompt A: Direct instruction
prompt_a = "Summarize this article in 3 bullet points."

# Prompt B: Structured with examples
prompt_b = """Extract the 3 most important facts from this article.
Format as bullet points starting with action verbs.

Example:
✓ Implement feature X to solve Y
✓ Refactor module Z for better performance
✓ Add tests covering edge cases

Article: {input}
"""

# Run evals on both prompts
eval_a = PromptEval(prompt_a)
eval_b = PromptEval(prompt_b)

# Add same test cases
for case in test_cases:
    eval_a.add_case(case.input, case.expected, case.criteria)
    eval_b.add_case(case.input, case.expected, case.criteria)

# Compare results
results_a = eval_a.run("claude-sonnet-4")
results_b = eval_b.run("claude-sonnet-4")

print(f"Prompt A: {results_a['avg_score']:.2f}")
print(f"Prompt B: {results_b['avg_score']:.2f}")

# Choose better performing prompt
if results_b['avg_score'] > results_a['avg_score']:
    print("Prompt B wins! Use structured format with examples.")
```

## Use Cases

### Use Case 1: Code Review Multi-Agent System

**Scenario:** Automated security and quality review for pull requests

**Agent Architecture:**
```
Orchestrator
├── Security Reviewer → OWASP Top 10, common vulnerabilities
├── Performance Reviewer → Algorithm complexity, bottlenecks
├── Style Reviewer → Code style, linting
└── Integration Reviewer → API compatibility, breaking changes
```

**Prompt for Security Reviewer:**
```
ROLE: Senior security engineer specializing in OWASP Top 10.
TASK: Review this code for security vulnerabilities.
CONTEXT: This is a pull request for an authentication service.
      Handle 10k+ daily requests. Uses JWT tokens.
FORMAT: JSON with vulnerability details.

{
  "vulnerabilities": [
    {
      "severity": "critical|high|medium|low",
      "category": "injection|broken_auth|xss|csrf|misconfig",
      "file": "path/to/file.js",
      "line": 42,
      "description": "Detailed description",
      "fix": "Recommended fix",
      "cve_potential": true|false
    }
  ]
}

Code to review:
[diff]
```

**Orchestrator Logic:**
```python
def review_pr(pr_id):
    # Get PR diff
    diff = get_pr_diff(pr_id)

    # Run parallel reviews
    security_review = run_agent("security-reviewer", diff)
    performance_review = run_agent("performance-reviewer", diff)
    style_review = run_agent("style-reviewer", diff)
    integration_review = run_agent("integration-reviewer", diff)

    # Aggregate results
    all_reviews = [
        security_review,
        performance_review,
        style_review,
        integration_review
    ]

    # Post comment on PR
    post_review_comment(pr_id, all_reviews)

    # Block merge if critical issues found
    if has_critical_issues(all_reviews):
        block_merge(pr_id)
```

### Use Case 2: Feature Implementation Workflow

**Scenario:** Implement OAuth authentication for WordPress plugin

**Agent Workflow (Sequential):**

**Step 1: Planner Agent**
```
Prompt:
"Plan the implementation of OAuth authentication for WordPress.
Requirements:
- Support Google and GitHub OAuth
- JWT token management
- Session handling
- Secure token storage

Output JSON plan with:
- Implementation steps
- Required files
- Dependencies
- Security considerations"
```

**Output:**
```json
{
  "steps": [
    "Create OAuth service class",
    "Implement Google OAuth flow",
    "Implement GitHub OAuth flow",
    "Add JWT token generation",
    "Create session manager",
    "Update user model",
    "Add authentication middleware"
  ],
  "files": [
    "includes/oauth.php",
    "includes/jwt.php",
    "includes/session.php",
    "models/user.php"
  ],
  "dependencies": ["firebase/php-jwt", "league/oauth2-google"],
  "security_considerations": [
    "Store tokens encrypted",
    "Implement token refresh",
    "Add CSRF protection",
    "Rate limiting"
  ]
}
```

**Step 2: Implementer Agent**
```
Prompt:
"Implement OAuth authentication following this plan:
[planner output]

Write production-ready code with:
- Clear comments
- Error handling
- Security best practices
- WordPress coding standards"
```

**Step 3: Tester Agent**
```
Prompt:
"Write comprehensive tests for OAuth implementation.
Test cases should cover:
- Successful authentication
- Failed authentication
- Token refresh
- Session expiry
- Edge cases

Use PHPUnit with WordPress test suite."
```

**Step 4: Reviewer Agent**
```
Prompt:
"Review OAuth implementation for:
- Security vulnerabilities
- Code quality
- WordPress standards
- Test coverage

Provide feedback and recommendations."
```

### Use Case 3: Parallel Content Generation

**Scenario:** Generate documentation, tests, and examples for new API

**Agent Workflow (Parallel):**

```
Orchestrator
├── Doc Generator → API documentation
├── Test Generator → Unit tests
└── Example Generator → Usage examples
```

**All agents run simultaneously:**

**Doc Generator:**
```
Prompt:
"Generate API documentation for:
[API spec]

Format as Markdown with:
- Overview
- Endpoint descriptions
- Request/response schemas
- Code examples
- Error codes"
```

**Test Generator:**
```
Prompt:
"Write unit tests for this API:
[API spec]

Use pytest with:
- Happy path tests
- Error case tests
- Edge case tests
- Mocking for external dependencies"
```

**Example Generator:**
```
Prompt:
"Create usage examples for this API:
[API spec]

Include:
- Python examples
- JavaScript examples
- cURL examples
- Real-world use cases"
```

**Orchestrator aggregates:**
```python
def generate_api_artifacts(api_spec):
    # Run agents in parallel
    docs = run_agent("doc-generator", api_spec)
    tests = run_agent("test-generator", api_spec)
    examples = run_agent("example-generator", api_spec)

    # Combine artifacts
    return {
        "documentation": docs,
        "tests": tests,
        "examples": examples
    }
```

## Agent Communication Patterns

### Structured Handoff

```
Agent A (Planner) → returns JSON:
{
  "plan": ["step1", "step2", "step3"],
  "files_to_modify": ["file1.ts", "file2.ts"],
  "risks": ["dependency conflict", "breaking change"],
  "estimated_effort": "4 hours"
}

Agent B (Implementer) → receives plan, returns JSON:
{
  "changes": [
    {"file": "file1.ts", "diff": "..."}
  ],
  "tests_needed": [
    "test_scenario_1",
    "test_scenario_2"
  ],
  "questions": [
    "Should we maintain backward compatibility?"
  ]
}
```

### Error Recovery

```
If agent fails:
1. Check if it's a retryable error (rate limit, timeout)
   - If retryable: wait and retry with same context

2. If not retryable: adjust prompt and try different approach
   - Add more specific instructions
   - Provide examples
   - Simplify requirements

3. If persistent: escalate to user with context
   - What was attempted
   - What failed
   - What was tried to recover
```

## Context Window Management

### What to Include

```
ALWAYS include (top priority):
- The specific task/question
- Relevant code snippets (not entire files)
- Error messages if debugging
- Constraints and requirements

SOMETIMES include (medium priority):
- Related type definitions
- API documentation
- Test examples
- Similar working code

NEVER include (bottom priority):
- Entire node_modules or vendor dirs
- Binary files
- Irrelevant code from other features
- Duplicate information
```

### Progressive Context Loading

```
Step 1: Search for relevant files (Glob/Grep)
- Find files matching task keywords
- Filter by recency and relevance

Step 2: Read only relevant sections
- Use line numbers for targeted reads
- Read function/class definitions
- Skip tests/boilerplate if not needed

Step 3: Include surrounding context only if needed
- Read 10 lines before/after function
- Include imports and dependencies
- Skip unrelated code in same file

Step 4: Summarize large files instead of including verbatim
- Extract key functions/interfaces
- Summarize large blocks
- Note file structure
```

### Context Budget Allocation

```
Available: ~200K tokens
Reserve:   ~50K for output
Budget:    ~150K for input

Allocation:
- System prompt + instructions:  ~10K
- Task description:               ~2K
- Code context:                 ~100K (prioritized by relevance)
- Examples/few-shot:             ~10K
- Agent history (if applicable):   ~8K
- Buffer:                       ~20K
```

## Anti-Patterns

### God Agent
**Problem:** One agent doing everything
- Too many responsibilities
- Loses focus and quality
- Context window overload

**Solution:** Split into specialized agents

### Blind Delegation
**Problem:** Launching agents without clear success criteria
- Agents may produce wrong output
- No way to verify quality
- Wastes tokens and time

**Solution:** Define success criteria before delegation

### Context Overload
**Problem:** Stuffing entire codebase into prompt
- Hits token limits quickly
- Agent gets confused
- Slow and expensive

**Solution:** Progressive context loading, summarize first

### Eval-Free Development
**Problem:** Shipping prompts without measuring quality
- Don't know what works
- Can't improve prompts
- Risk of poor performance

**Solution:** Eval-driven development, measure everything

### Retry Loops
**Problem:** Retrying same failing approach without adjustment
- Infinite loops possible
- Wastes tokens
- No progress

**Solution:** Adjust approach after each failure

## Integration Points

- **skill-manager**: Manage agent configurations
- **verification-loop**: Validate agent outputs
- **continuous-learning-v2**: Learn from agent interactions
- **strategic-compact**: Manage context windows

## Best Practices

1. **Define success criteria before building agents**
2. **Start with one agent, split only when needed**
3. **Measure everything** (latency, cost, accuracy)
4. **Version your prompts** like you version code
5. **Use structured output** (JSON) for agent-to-agent communication
6. **Add guardrails** (output validation, content filtering)
7. **Log all interactions** for debugging and improvement

## Quick Reference

```bash
# Orchestrate multi-agent system
"Orchestrate security, performance, and style review in parallel"

# Write agent prompt
"Write prompt for security reviewer agent with RTCF pattern"

# Create eval suite
"Define eval criteria for code generation prompt"

# Manage context
"Load relevant context progressively for this task"
```

## Related Skills

- **skill-manager**: Agent orchestration and management
- **verification-loop**: Output validation
- **continuous-learning-v2**: Pattern extraction
- **strategic-compact**: Context management

---

**Remember**: Good orchestration starts with clear agent responsibilities, structured communication, and measurable success criteria.
