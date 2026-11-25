#!/bin/bash
# Validate Checkly project configuration and preserve the CLI's exit status.

set -e

echo "Validating Checkly project configuration..." >&2
npx checkly validate --verify-runtime-dependencies
echo "Configuration is valid." >&2
