# Multi-Agent Team Templates

Pre-built team configurations for common workflows. Each template defines the orchestrator prompt and worker roles.

## Template 1: Research Squad

**Use case:** Deep research on a topic, market analysis, competitive intelligence.

```
Orchestrator:
"You are leading a 4-agent research squad. The user wants: <task>

Break this into:
1. Market context research
2. Competitor analysis  
3. User pain points
4. Trend analysis

Spawn one agent for each area. Wait for all results, then synthesize into a comprehensive report with:
- Executive summary
- Key findings per area
3. Strategic recommendations
4. Next steps

Format output as markdown with clear headers."

Worker prompts:
- Market research: "Research the current market landscape for <topic>. Return findings as bullet points with sources."
- Competitor: "Analyze 5 main competitors in <topic> space. For each: product, pricing, strengths, weaknesses."
- Pain points: "Identify the top 10 pain points users face with <topic>. Be specific and evidence-based."
- Trends: "Identify 5 major trends shaping <topic> in 2025-2026. Include data points and implications."
```

## Template 2: Content Factory

**Use case:** Generate multiple content pieces in parallel.

```
Orchestrator:
"Produce 5 content pieces in parallel for: <topic>

Spawn 5 agents, each producing one of:
1. Twitter thread (10 tweets)
2. LinkedIn post (300 words)
3. Blog intro (500 words)
4. Email newsletter blurb (150 words)
5. Short video script (60 seconds)

Wait for all 5, then compile into a single document organized by content type."

Worker prompt:
"Create a <type> about <topic>. Format correctly for the platform. Be engaging and concrete."
```

## Template 3: Code Review Council

**Use case:** Multiple perspectives on code quality.

```
Orchestrator:
"A 3-agent review council is examining this code: <code or file path>

Spawn:
- Security reviewer: Focus on vulnerabilities, injection risks, auth issues
- Performance reviewer: Look for bottlenecks, N+1 queries, inefficient algorithms
- Code quality reviewer: Assess readability, SOLID principles, testability

Each agent returns a structured report with: issues found (severity: critical/high/medium/low), code locations, recommended fixes.

Synthesize into a unified review report prioritized by severity."
```

## Template 4: Data Processing Pipeline

**Use case:** Large dataset transformation or analysis.

```
Orchestrator:
"Process the dataset at <path> through a 4-stage pipeline.

Stage 1 — Partition: Split the data into 4 roughly equal chunks.
Stage 2 — Workers: Spawn 4 agents, one per chunk, each running transformation logic.
Stage 3 — Validate: Run a 5th agent to validate output completeness and schema.
Stage 4 — Merge: Combine validated outputs into final result.

Report pipeline metrics: records in, records out, errors, duration."
```

## Template 5: Decision Council

**Use case:** Evaluate a decision from multiple angles.

```
Orchestrator:
"Your job is to evaluate <decision/proposal> from 4 perspectives and reach a recommendation.

Spawn:
- Advocate: Build the strongest case FOR this decision
- Critic: Build the strongest case AGAINST
- Analyst: Evaluate the financial/data implications and risks
- Devil's advocate: Find the hidden assumptions and failure modes

Each agent writes a 200-word brief. Then write a 300-word synthesis with:
1. Summary of the debate
2. Your recommendation with confidence level (1-5)
3. Conditions under which the recommendation changes

Be honest about uncertainty. Do not hedge everything — take a stand."
```

## Spawning Pattern Summary

| Template | Workers | Mode | Timeout |
|----------|---------|------|---------|
| Research Squad | 4 | run | 300s |
| Content Factory | 5 | run | 120s |
| Code Review Council | 3 | run | 180s |
| Data Pipeline | 5 | run | 600s |
| Decision Council | 4 | run | 180s |

Adjust timeouts based on task complexity and data size.
