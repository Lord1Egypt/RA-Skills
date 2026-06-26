#!/bin/bash
# DataGuard DLP — Emergency Override (wrapper)
# Delegates to override.sh for backwards compatibility
exec "$(cd "$(dirname "$0")" && pwd)/override.sh" "$@"