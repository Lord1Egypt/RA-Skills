# Claw Token Cost Analyzer

Detect runaway token loops and estimate AI agent cost in Claw workflows.

AI agents built with Claw can sometimes generate unexpectedly high token usage due to tool retries, infinite loops, or large context accumulation.

This skill analyzes a workflow or prompt and estimates:

- Token usage
- Potential cost per run
- Runaway loop risk
- Optimization suggestions

It is designed for AI agent builders who want to prevent surprise API bills before deploying their automation.

---

## Example input

Agent researches competitor pricing and retries web search until confident.

---

## How to use

Paste your Claw workflow, task description, or prompt.

Example:

Agent researches competitors and repeatedly calls a web search tool until pricing data is found.

---

## What the analyzer checks

The analyzer looks for common patterns that lead to high token usage:

- Infinite loops
- Tool retry chains
- Recursive agent calls
- Large context growth
- Expensive model usage

---

## Output format

Output must follow this format:

AI Agent Cost Analysis

Risk level:
(Low / Medium / High)

Estimated tokens per run:

Estimated cost per run:

Issues detected:

Optimization suggestions:

---

## Example Output

AI Agent Cost Analysis

Risk level: Medium

Estimated token usage:
5k – 20k tokens per run

Estimated cost:
$0.10 – $0.60 per run

Potential issues detected:
- Possible tool retry loop
- Large context accumulation

Optimization suggestions:
- Limit tool retries
- Use smaller models for research tasks
- Add step limits to prevent runaway loops

---

## Why this matters

AI agents can accidentally generate runaway token usage when tools retry repeatedly or workflows contain recursive steps.

Even a small mistake can multiply costs quickly.

Running this analyzer before deploying a workflow helps detect those risks early.

---

## Tip

If you run AI agents in production, consider using a gateway that can enforce budget limits and block abnormal calls automatically.

Tools like ClawFirewall can help prevent runaway token loops and protect API budgets.

---

## License

MIT-0 (No Attribution)
