#!/usr/bin/env bash
set -euo pipefail
cd /home/moltuser/clawd
mcporter call gemini.gemini_chat prompt="Ответь ровно: smoke-ok" model="gemini-3.0-flash"
