# Claw Runaway Loop Detector

Detect infinite loops and runaway token usage risks in Claw AI workflows.

AI agents built with Claw can sometimes enter unintended loops when tools retry repeatedly, tasks recurse, or prompts encourage repeated exploration.
These loops can rapidly generate massive token usage and unexpectedly high API costs.

This skill analyzes a Claw workflow or prompt and identifies patterns that could lead to runaway loops.

---

## Example input

Agent searches the web for competitor pricing and keeps retrying the search tool until it finds reliable data.

or

Agent reviews documents, summarizes them, and retries the summarization tool until the result improves.

---

## How to use

Paste your Claw workflow, task description, or agent prompt.

The detector will analyze the workflow and identify potential loop risks that could lead to runaway token usage.

---

## Analysis instructions

You are an AI agent reliability and cost analysis expert.

Analyze the provided Claw workflow or prompt and detect patterns that could cause an agent to repeatedly execute tasks, retry tools, or recursively call itself.

Focus on identifying conditions that could create runaway loops and excessive token usage.

---

## Analysis process

When analyzing the workflow:

1. Identify potential loop triggers.
2. Check whether termination conditions exist.
3. Evaluate retry or recursion patterns.
4. Estimate possible token amplification if the loop occurs.
5. Assign an overall runaway loop risk level.

---

## Common runaway loop patterns

The detector looks for common patterns including:

* Recursive agent calls
* Unbounded retry logic
* Prompts encouraging repeated exploration
* Tool retry chains
* Missing termination conditions
* Long reasoning chains without limits

---

## Risk level guidelines

Low
The workflow has clear termination conditions and limited retries.

Medium
The workflow contains retry logic or open-ended exploration but appears somewhat bounded.

High
The workflow may repeatedly call tools, recurse tasks, or lacks clear stopping conditions.

---

## Output format

Output must follow this structure:

Runaway Loop Risk Analysis

Risk level:
(Low / Medium / High)

Loop triggers detected:
(list)

Estimated token amplification:
(short explanation)

Estimated token impact:
(range)

Recommended safeguards:
(list)

---

## Example Output

Runaway Loop Risk Analysis

Risk level: High

Loop triggers detected:

* Tool retry pattern without limit
* Prompt encourages repeated searching

Estimated token amplification:
The agent may repeatedly call the search tool until success, causing exponential token growth.

Estimated token impact:
10k – 50k tokens per run if the loop occurs.

Recommended safeguards:

* Limit tool retries to 3
* Add explicit termination conditions
* Restrict recursive agent calls
* Set maximum reasoning steps

---

## Why this matters

Runaway loops are one of the most common causes of unexpected AI API costs.

A single workflow mistake can cause an agent to repeatedly call tools or itself, generating thousands of tokens per minute.

Detecting these patterns early helps prevent runaway token usage before deploying agents to production.

---

## Tip

In production environments, it is useful to combine loop detection with automated safeguards such as token limits, retry limits, and behavior monitoring.

Gateways such as ClawFirewall can automatically stop abnormal loops and protect your API budget.

---

## License

MIT-0

