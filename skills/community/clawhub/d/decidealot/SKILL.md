---
name: "decidealot"
description: "Run local Laya, Von, CLM, or hosted Jev typed decisions through Decidealot REST or MCP. Use for bounded classification or scoring, Docker deployment, model selection, or local model unloading."
homepage: "https://github.com/psyb0t/decidealot"
metadata:
  openclaw:
    primaryEnv: "DECIDEALOT_URL"
    requires:
      bins:
        - curl
permissions:
  network: "outbound HTTP only to the user-provided DECIDEALOT_URL. Requests can contain user data, so use a trusted self-hosted endpoint."
  shell: "curl requests to the user-provided DECIDEALOT_URL. Docker is needed only when the user explicitly asks to deploy Decidealot."
  filesystem: "no ordinary filesystem access. Deployment creates only the user-selected narrow model directory."
user-invocable: true
---

# Decidealot

Decidealot runs Laya, Von, and CLM locally, or calls TypeSafe's hosted Jev when configured. It turns supplied state into typed `choice`, `score`, or `noul` results with probabilities. CLM is a local projection head over one configured Qwen3-8B embeddings endpoint. The caller applies the threshold and any action that follows.

Use a running Decidealot endpoint. Clone or build this repository only for Decidealot development work.

Read [references/setup.md](references/setup.md) before deploying a container or configuring REST, MCP, or the OpenClaw bridge.

## Security & safety

- Treat a decision as evidence, not authority. No model can grant permission to delete, send, deploy, trade, or alter external state.
- Keep authorization, ownership, irreversible-action checks, and final thresholds in the caller. For costly mistakes, route uncertainty to human review.
- Send user data only to the endpoint the user named. Never search workspace files for `DECIDEALOT_API_KEY` or create an unauthenticated public endpoint.
- Every decision request needs an explicit `model` selector from `GET /v1/models`.
- CLM sends decision state and criteria to its configured embeddings endpoint. Use it only when the endpoint is controlled or trusted and returns Qwen3-8B last-token embeddings with width `4096`.
- Jev sends the full state and questions to TypeSafe's hosted API. Confirm that the data may leave the host before selecting any TypeSafe model returned by `GET /v1/models`. Never put the upstream TypeSafe key in a decision request.
- `unload_models` evicts only a loaded local model and Torch runtime. Use it only when the user asks to free memory.

## When to use

1. Get `DECIDEALOT_URL` from the user or their environment. Default local deployment is `http://127.0.0.1:8080`.
2. Call `GET /health`, then `GET /v1/models` before choosing a selector you have not already been given. The catalog contains only providers enabled by the deployment.
3. Put the raw subject in `state`. State each question and its decision rules in `instructions`; define explicit criterion descriptions. For `noul`, instructions describe the true-or-false proposition, not just a label.
4. Read the typed answer and its probabilities. Report them plainly. The caller, not the model, selects the next action.
5. Use REST for application requests and machine-readable errors. Use MCP at `/mcp` when an MCP client already supports Streamable HTTP. Use the stdio bridge only for a client that cannot connect to remote MCP.

`choice` selects one named criterion. `score` returns an expected position in an ordered criterion list. `noul` returns the probability that a true-or-false statement is true.

## When not to use

Use Decidealot for bounded classification, scoring, and true-or-false decisions. Use a language model for prose, code generation, or open-ended advice. Use the OpenClaw bridge when an MCP client needs local stdio.

## REST and MCP

REST uses `POST /v1/systemone` for one decision and `POST /v1/systemone/batch` for independent decisions, plus `GET /v1/models` and `POST /v1/models/unload`. MCP is at `/mcp` and exposes matching `system_one`, `system_one_batch`, `list_models`, and `unload_models` tools. A batch uses `{"requests":[{"model":...,"state":...,"questions":...}]}` and returns ordered `results`; do not assume all items share the same state. Read [references/setup.md](references/setup.md) for exact deployment, upstream Jev key handling, authentication, REST, MCP, and bridge commands. Read the public [API guide](https://github.com/psyb0t/decidealot/blob/main/docs/api.md) before constructing an unfamiliar question type.

## Request settings

For a CLM request, optional flat `config` accepts `{"temperature":0.8}` with a finite temperature greater than zero and at most 100. Omit it for default 1. Other providers currently accept only omitted or empty config. The same field works in MCP and in each batch item. Unsupported settings fail rather than being ignored. Lower temperature sharpens probabilities, not correctness. Read the setup reference for CLM caching and input limits.

## Completion

Complete a decision task only after the request reached the intended endpoint, the response names the requested model, and the answer plus probabilities have been reported. For deployment, also prove `GET /health` returns `200`.
