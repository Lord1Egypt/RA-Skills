# AgentBrowse Operating Guide

This reference expands the main skill with the operating rules that matter
most during a live browser task.

## Start From The Current State

- If the right browser and page are already open, attach to them instead of
  restarting the session.
- If you already know the destination, use `agentbrowse navigate <url>`
  instead of clicking through intermediate pages.
- Use plain `observe` for general page inventory. Add a goal only when you
  want the result focused around a specific question.

## AI-Assisted Features

- Core browser commands (`launch`, `attach`, `navigate`, `act`,
  `browser-status`, `screenshot`, `close`) need no API key.
- `observe` with a natural-language goal, and any `extract`, call an LLM
  through the gateway. Configure API access with `agentbrowse init <apiKey>`
  before using them.
- If AI-assisted `observe` or `extract` still fails after `init`, run
  `agentbrowse doctor` to inspect the local config.

## Recovery

- After redirects, reloads, or dynamic updates, run a fresh `observe` before
  deciding on the next action.
- If a target ref becomes stale, discard it and observe again instead of
  forcing the old action.
- If the browser disconnects or becomes unresponsive, check
  `agentbrowse browser-status`, then reconnect with `launch` or `attach`.
- After reconnecting, treat all previous refs as stale until a new observe
  pass returns them again.

## Protected Steps

- AgentBrowse can take you up to a protected login, identity, or payment step.
- When the next step needs approved protected values or a dedicated protected
  step flow,
  switch to the companion protected-flow tool instead of improvising it in
  browser commands.
