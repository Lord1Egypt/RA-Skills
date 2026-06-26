# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Go CLI (`caesar`) for the [Caesar](https://www.caesar.org/) research API. It wraps the `https://api.caesar.xyz` REST API to let users run research jobs, chat with results, brainstorm, and manage collections from the terminal.

## Build & Run

```bash
go build -o caesar .       # build the binary
go run . [command]          # run without building
go build ./...              # verify all packages compile
go vet ./...                # static analysis
```

There are no tests yet. When adding tests, use standard `go test ./...` and place test files alongside the code they test (`*_test.go`).

## Authentication

The API key is read from the `CAESAR_API_KEY` environment variable. Never hardcode keys or store them in files tracked by git. The `.gitignore` excludes `.env`.

## Architecture

```
main.go                       → entry point, calls cmd.Execute()
cmd/                          → cobra command definitions (one file per command group)
  root.go                     → root command, wires subcommands
  research.go                 → research create/get/events/watch + polling logic
  chat.go                     → chat send/history on research jobs
  brainstorm.go               → brainstorm session creation
  collections.go              → collection management
internal/
  client/
    client.go                 → HTTP client: auth, request/response, all API methods
    types.go                  → request/response structs for the Caesar API
  config/
    config.go                 → base URL constant and env var reading
  output/
    output.go                 → JSON printing and error helpers
```

**Key patterns:**
- Each `cmd/*.go` file registers its commands in an `init()` function via `rootCmd.AddCommand()`
- All API calls go through `internal/client.Client`, which handles auth headers and error checking in a single `do()` method
- The `client.Client` is created per-command via `client.New()` (reads the API key from env at that point)
- Output is always JSON via `output.JSON()` unless there's a human-friendly format (like brainstorm questions or chat responses)

## Caesar API Overview

Base URL: `https://api.caesar.xyz` — Bearer token auth via `Authorization: Bearer <token>`

**Research lifecycle:** `POST /research` → returns job ID with status `queued` → poll `GET /research/{id}` → status progresses through `searching`, `summarizing`, `analyzing`, `researching` → `completed` or `failed`. The completed response includes `content` (synthesized answer with `[n]` citations) and a `results` array mapping citation indices to source URLs.

**Key endpoints:**
- `POST /research` — create research job (many optional params: model, reasoning_loops, auto, exclude_social, etc.)
- `GET /research/{id}` — poll job status and get results
- `GET /research/{id}/events` — get reasoning step log
- `GET /research/{id}/results/{resultId}/content?format=raw|markdown` — fetch source content
- `POST /research/brainstorm` — get clarifying questions before research
- `POST /research/{id}/chat` — follow-up questions (response via polling or SSE at `/chat/{messageId}/stream`)
- `GET /research/{id}/chat` — chat history
- `POST /research/collections` — create file collections

**Models available:** `gpt-5.2`, `gemini-3-pro`, `gemini-3-flash`, `claude-opus-4.5`

## Adding New Commands

1. Create a new file in `cmd/` (e.g., `cmd/newfeature.go`)
2. Define the cobra command and register it in `init()` via `rootCmd.AddCommand()` or as a subcommand
3. Add any new API methods to `internal/client/client.go` and types to `internal/client/types.go`
4. Use `output.JSON()` for structured output, `output.Error()` for fatal errors
