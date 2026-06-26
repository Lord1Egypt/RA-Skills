#!/bin/bash
# gbrain CLI wrapper
# Usage: gbrain.sh <command> [args...]
cd ~/gbrain && bun run src/cli.ts "$@"
