---
name: devtool-answer-monitor
description: >
  Use when the user wants to monitor how ChatGPT, Claude, Gemini, and other LLMs describe a developer tool, API, SDK, or open-source project. DevTool Answer Monitor is the companion skill for the devtool-answer-monitor repo and covers query pool design, four-metric monitoring, model-specific content placement, content checks, negative-answer repair, activation analysis, and T+7 or T+14 regression validation.
license: MIT
allowed-tools: Read
metadata:
  openclaw:
    emoji: "📈"
    author: "veeicwgy"
    homepage: "https://github.com/veeicwgy/devtool-answer-monitor"
    requires:
      env:
        - OPENAI_API_KEY
        - OPENAI_BASE_URL
      bins:
        - python3
        - bash
    primaryEnv: OPENAI_API_KEY
    env:
      - name: OPENAI_API_KEY
        description: "Optional provider API key for API collection mode only. Quickstart replay and manual paste mode do not need it."
        required: false
        sensitive: true
      - name: OPENAI_BASE_URL
        description: "Optional OpenAI-compatible gateway URL for multi-provider API collection mode."
        required: false
        sensitive: false
---

# Monitor What LLMs Say Before Users Choose Your Dev Tool

Use this skill as the **main visibility workflow router** for developer tools and open-source products.

**Brand:** DevTool Answer Monitor

**Companion repo:** [`devtool-answer-monitor`](https://github.com/veeicwgy/devtool-answer-monitor)

Use this when you want an agent to help you monitor how LLMs describe your product, build a reusable query pool, diagnose negative or outdated answers, and plan what to fix next.

## Safety First

- Treat this root skill as a **read-only workflow router**.
- Default to `quickstart replay` or `manual paste mode` when you only need examples or scoring help.
- Do not ask users to paste API keys into chat. If API collection mode is needed, tell them to configure local environment variables themselves and then hand off execution to `visibility-monitor`.
- Review local scripts such as `install.sh`, `quickstart.sh`, and the selected runner before executing shell commands.

## Start Here

Copy one of these prompts to begin:

- `Analyze how ChatGPT and Claude describe my API docs`
- `Build a developer-tool answer monitoring query pool for my SDK`
- `Find negative or outdated LLM claims about my project`

## 30-Second Result

**Typical input**

- product truth such as a README, docs, changelog, integrations, or positioning page
- answer evidence such as copied model answers, screenshots, or cited URLs
- scope such as target models, languages, regions, or a repeated query set

**What this skill returns**

- a reusable query pool
- raw evidence and a score draft plan
- a monitoring summary and report outline
- a repair backlog with T+7 or T+14 validation points

**Companion demo and sample outputs**

- Zero-install demo: [sample-run viewer](https://cdn.jsdelivr.net/gh/veeicwgy/devtool-answer-monitor@main/docs/index.html)
- Public benchmarks: [MinerU story](https://github.com/veeicwgy/devtool-answer-monitor/blob/main/benchmark/mineru-public-benchmark.md) and [Sciverse API story](https://github.com/veeicwgy/devtool-answer-monitor/blob/main/benchmark/sciverse-api-public-benchmark.md)
- Sample outputs: [leaderboard snapshot](https://github.com/veeicwgy/devtool-answer-monitor/blob/main/assets/leaderboard-sample.png) and [repair trend snapshot](https://github.com/veeicwgy/devtool-answer-monitor/blob/main/assets/repair-trend-sample.png)

## Trigger

Use this skill when the task is any of the following:

1. generate a visibility query matrix and Query Pool from product truth;
2. monitor how multiple LLMs mention, recommend, or misunderstand a product;
3. plan model-specific content placement based on datasource patterns;
4. check whether a draft page, FAQ, changelog, or case study is ready to influence model answers;
5. repair wrong, negative, outdated, or competitor-only answers;
6. verify whether a repair action improved metrics at T+7 or T+14;
7. help a user choose between quickstart replay, manual paste mode, and API collection mode.

## Beginner Routing

When the user is new to the repository, route them in this order.

| Situation | Next step |
|---|---|
| Needs environment check first | open `docs/getting-started.md` and review the environment check section |
| Wants environment-free first run | open `docs/index.html` or `docs/for-beginners.md` |
| Wants a short explanation first | open `docs/for-beginners.md` |
| Wants deeper onboarding | open `docs/getting-started.md` |
| Wants the English repository overview | open `README.md` |
| Wants the Chinese repository overview | open `README.zh-CN.md` |

## Visibility Strategy

Always keep the workflow in this order:

| Stage | Goal |
|---|---|
| Query design | turn product truth into scenario matrix, three-layer keywords, and Query Pool seeds |
| Monitoring | score mention, positive mention, capability accuracy, and ecosystem accuracy |
| Placement | map each target model to likely datasource channels and publication surfaces |
| Repair | classify bad answers into information error, negative evaluation, outdated information, or competitor insertion |
| Activation | analyze whether answers help a user install, integrate, or invoke the product |
| Regression | compare follow-up runs and check whether metrics improved after action |

## Mode Selection

Choose the execution mode before running monitoring.

| Mode | Use when | Typical inputs |
|---|---|---|
| Quickstart replay | user wants the fastest first run without API setup | sample model config + sample manual responses |
| Manual paste mode | user already has copied answers from chat tools | Query Pool + manual response JSON |
| API collection mode | user wants repeatable real monitoring | Query Pool + model config + locally configured provider env vars |

## Input Contract

Prepare as many of the following as possible before execution.

| Input | Examples |
|---|---|
| Product truth | README, docs, changelog, integrations, positioning |
| Answer evidence | raw answers, screenshots, copied responses, cited links |
| Monitoring scope | models, languages, regions, dates, repeated query set |
| Publishing targets | docs, blog, GitHub, Q&A, partner channels |

## Workflow Router

Choose the next sub-skill according to the user's immediate need.

| Situation | Next Skill |
|---|---|
| Need query design and scenario clustering | `visibility-query-matrix` |
| Need weekly monitoring, evidence logging, report output, or shell execution after explicit user approval | `visibility-monitor` |
| Need pre-publish content QA | `visibility-content-check` |
| Need to repair bad answers and define regression checks | `visibility-repair` |

## Required Reading Order

For a full program, read these repository documents in sequence:

1. `playbooks/visibility-workflow-architecture.md`
2. `playbooks/keyword-strategy.md`
3. `playbooks/monitoring-system.md`
4. `playbooks/model-datasources.md`
5. `playbooks/content-platform-map.md`
6. `playbooks/negative-fix-sop.md`

## Output Contract

Always preserve the following outputs.

| Output | Description |
|---|---|
| Query foundation | scenario matrix, keyword layers, Query Pool |
| Monitoring outputs | raw evidence, score draft, summary, report, leaderboard or overview |
| Action plan | content placement priorities and repair backlog |
| Regression record | T+7 and T+14 comparisons after key fixes |

## Positioning

DevTool Answer Monitor is the skill layer for the `devtool-answer-monitor` repo.

- Use the **repo** when you want runnable demos, scripts, and report artifacts.
- Use the **skill** when you want an agent-guided workflow for monitoring, repair, and regression planning.

## Handoff Rules

At the end of each run, preserve:

1. which product was optimized;
2. which models and languages were in scope;
3. which queries are reused in weekly tracking;
4. what the top three visibility weaknesses are;
5. what actions are already completed and what still needs validation.
