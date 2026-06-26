---
name: agentbrowse
description: Browser automation workflows through the agentbrowse CLI for
  launch, attach, observe, act, extract, navigation, and screenshots.
homepage: https://github.com/MercuryoAI/agentbrowse
metadata: {"openclaw":{"homepage":"https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/openclaw/marketplace/README.md","requires":{"bins":["agentbrowse"]},"install":[{"id":"npm","kind":"node","package":"@mercuryo-ai/agentbrowse-cli","bins":["agentbrowse"],"label":"Install AgentBrowse CLI (npm)"}]}}
---

AgentBrowse is the browser layer for agent tasks that happen on a real
website.

Use this skill when the agent needs to:

- launch a browser or attach to an existing one;
- inspect the current page and decide from visible state;
- click, type, select, and otherwise act on returned target refs;
- navigate directly to a known URL;
- extract structured data from the page;
- capture screenshots or recover a stuck browser session.

AgentBrowse works well on its own for browser automation. It can also be
paired with MagicPay later when a broader flow reaches an approved login,
identity, or payment step.

Open source:

- Browser library and docs: `https://github.com/MercuryoAI/agentbrowse`
- CLI package: `@mercuryo-ai/agentbrowse-cli`

## Setup

- `agentbrowse` must be available on `PATH`. If it is missing or outdated, run
  `npm i -g @mercuryo-ai/agentbrowse-cli@latest`, then verify with
  `agentbrowse --version`.
- `agentbrowse launch` needs an environment that can start a browser.
  `agentbrowse attach <cdp-url>` needs a reachable CDP endpoint.
- Core browser commands such as `launch`, `attach`, `navigate`, `act`,
  `browser-status`, `screenshot`, and `close` do not need any API key.
- AI-assisted features — `observe` with a natural-language goal and
  `extract` — call an LLM through the gateway. Configure API access with
  `agentbrowse init <apiKey>` before using them. Pass a non-default API
  URL during init if needed.
- `agentbrowse doctor` inspects the local config. Use it after `init`
  when AI-assisted `observe` or `extract` still fails.

## Core Loop

1. Start or connect to a browser with `agentbrowse launch [url]` or
   `agentbrowse attach <cdp-url>`.
2. Read the page with `agentbrowse observe`.
3. Act on the returned refs with `agentbrowse act <targetRef> <action> [value]`.
4. Re-run `agentbrowse observe` after navigation or meaningful UI changes.
5. Use `agentbrowse navigate <url>` when the destination is already known.
6. Use `agentbrowse extract '<schema-json>' [scopeRef]` when you need
   structured output instead of another page action.
7. Use `agentbrowse screenshot` or `agentbrowse browser-status` only for
   evidence and debugging.
8. Finish with `agentbrowse close` when the browser session is no longer
   needed.

## When To Bring In Another Tool

Bring in a companion protected-flow tool when the site reaches:

- a login step that needs approved protected values;
- an identity form with protected personal data;
- a payment step with protected card details or approval flow.

At that point AgentBrowse can stay the browsing layer around the protected
step, but it should not invent its own secret-handling flow.

## Ask-User Boundary

Ask the user only when:

- the correct next step is still ambiguous after re-observing the page;
- the environment cannot launch or attach to a browser;
- the task crosses into a protected approval or payment boundary.

## Operating Rules

- Trust the visible page state, not assumptions about what should have
  happened.
- Re-observe after meaningful page changes instead of reusing stale refs.
- Keep browser work and protected-step handling separated.
- `close` is only teardown or recovery. Never treat `close` as a success
  signal — task success comes from the visible page state before `close`.

## More Detail

Open an extra reference only when it helps:

- [Operating guide](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/references/workflow.md) for resume and recovery.
- [Command guide](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/references/commands.md) for every CLI command.
- [Failure recovery](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/references/statuses.md) for common runtime states.
- [Boundaries and escalation](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/references/guardrails.md) for safety rules.

If a term (`session`, `ref`, `targetRef`, `scopeRef`, `fillRef`, `pageRef`)
is unfamiliar, check the
[AgentBrowse API reference glossary](../../agentbrowse/docs/api-reference.md#ref-glossary).
