# research-harness

> A cognitive discipline framework for AI-native scientific experimentation.
>
> [中文版](README_zh.md)

## What Problem Does It Solve?

Running LLM-based experiments is easy. Running them *reproducibly*, *traceably*, and *without overclaiming* is not. Agents conducting research routinely:
- Scale experiments before validating the minimum loop
- Report "p < 0.05" as conclusive evidence
- Treat surprising results as method failures before checking the pipeline
- Delete failed runs to make progress look cleaner
- Change baselines or rubrics silently

This skill provides **guardrails, not recipes** — a set of cognitive disciplines enforced by repo structure and validation rules, independent of any specific domain.

## What Makes It Better?

- **Thinking, not scripting** — Teaches agents *how to reason* about experiments, not just which commands to run
- **Domain-agnostic** — Works for NLP, vision, bio, social science, or any field using LLM-based evaluation
- **Provenance by design** — Every run traceable to a git commit, model version, and prompt version
- **Anti-overclaiming** — Evidence status grading, protected surfaces, and pipeline-first diagnosis prevent the most common agent research failures
- **Agent-safe handoffs** — Alignment docs replace chat history for cross-agent continuity

## How to Use

Load this skill when setting up a new research experiment. The skill provides:

1. **Five cognitive disciplines** — guardrails for agent reasoning during experiments
2. **Five governance rules** — human-agent boundaries and evidence status grading
3. **Phase workflow (0→4)** — a scaffold template and validation framework to build upon
4. **Reference knowledge** — detailed methodology in `references/` for each discipline

The skill does not include automation scripts. It teaches the agent *how to think*, not which commands to run.

## Origin

Distilled from real-world PhD research execution — running controlled experiments with LLM agents, building dual-track scoring systems, and learning (the hard way) that most "method failures" are actually pipeline failures.

## License

MIT
