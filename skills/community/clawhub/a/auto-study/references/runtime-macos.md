# runtime-macos

## Use this file when

- the host is macOS

## Prerequisites

- Google Chrome installed on macOS
- `agent-browser` installed and available in `PATH`

## Default profile root

- `~/Library/Application Support/AutoStudy/browser`

## Core policy

- the task should drive a local macOS Chrome instance
- the usual Chrome app path is `/Applications/Google Chrome.app`
- when using a dedicated persistent profile, keep site profiles under `~/Library/Application Support/AutoStudy/browser`
- if `agent-browser` is already running and you need a different `--profile` or launch option, close existing sessions first and start again
