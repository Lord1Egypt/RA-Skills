# Qianfan and Baidu AI Cloud

Use this file for platform, model, or implementation questions related to Baidu AI Cloud and Qianfan.

## What This Surface Covers

- model and agent platform questions
- evaluation and workflow planning
- cloud-service selection around Baidu AI workloads
- account and rollout boundaries for Baidu-owned AI surfaces

## Planning Rules

1. Confirm whether the task is research, architecture planning, or account execution.
2. State the assumed region, docs language, and account owner.
3. Verify current capabilities against Baidu-owned documentation before naming a path.
4. Separate model selection, workflow orchestration, and cloud operations in the answer.

## Do Not Collapse These Layers

| Layer | What it decides |
|-------|-----------------|
| Platform | Which Baidu AI surface or product family is relevant |
| Model workflow | How the user wants prompting, agents, retrieval, or evaluation to work |
| Cloud operations | Accounts, permissions, deployment, logging, and cost boundaries |

## Guardrails

- Do not explain Qianfan only by analogy to another AI vendor.
- Do not recommend console changes without explicit user approval.
- Do not assume consumer Baidu surfaces and Qianfan share the same team or account.
- Do not turn vendor research into an execution plan without confirming ownership and risk.

## Output Contract

For non-trivial Qianfan work, end with:
- chosen path
- rejected alternatives
- assumed account owner
- hard blockers
- what must be verified live before execution
