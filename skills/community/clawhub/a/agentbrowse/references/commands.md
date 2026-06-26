# AgentBrowse Command Guide

## Start A Session

### `agentbrowse launch [url] [options]`

Open a browser and optionally go straight to `url`.

### `agentbrowse attach <cdp-url> [--provider <name>]`

Attach to an existing browser over CDP.

### `agentbrowse navigate <url>`

Go directly to a known URL inside the current session.

## Read And Act On The Page

### `agentbrowse observe ["<goal>"]`

Read the current page and return targets, scopes, signals, and supported
forms. Add a goal when you want the result focused around a question.

### `agentbrowse act <targetRef> <action> [value]`

Interact with a target returned by `observe`.

### `agentbrowse extract '<schema-json>' [scopeRef]`

Return structured JSON from the whole page or a specific scope.

## Evidence And Recovery

### `agentbrowse screenshot [--path <file>]`

Capture the current page for debugging or evidence.

### `agentbrowse browser-status`

Inspect whether the current browser session is still reachable.

### `agentbrowse close`

Close the browser and clear the stored browser session.

## AI-Assisted Setup

### `agentbrowse init <apiKey> [--api-url <url>]`

Store the API key used by AI-assisted `observe` (with a natural-language
goal) and any `extract` in the local config file. Core browser commands do
not need this setup.

### `agentbrowse doctor`

Inspect the local config when AI-assisted `observe` or `extract` still
fails after `init`.

### `agentbrowse --version`

Print the installed CLI version.

If the command is missing or outdated, run
`npm i -g @mercuryo-ai/agentbrowse-cli@latest`, then rerun
`agentbrowse --version`.
