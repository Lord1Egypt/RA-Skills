#!/bin/bash
# Test the default project, then let Checkly present and confirm its deploy plan.
# Usage: test-and-deploy.sh (no arguments).
# Exit 3 means approval is required for a nonempty plan; no changes can exit 0.
# After approval, run the returned confirmCommand verbatim with Checkly directly.
# For custom --config or authorized CI flags, test and deploy the same config
# directly; deploy-only argument forwarding could test one project and deploy another.

set -e

if [ "$#" -ne 0 ]; then
  echo "This helper takes no arguments. Run Checkly directly for custom configs or an approved confirmCommand." >&2
  exit 2
fi

echo "Testing checks in the Checkly runtime..." >&2
if npx checkly test; then
  echo "Checks passed. Reviewing the deployment plan..." >&2
else
  status=$?
  echo "Checks did not pass; nothing was deployed." >&2
  exit "$status"
fi

# Preserve upstream stdout and status, including confirmation_required / exit 3.
# The CLI owns confirmation so the user approves the actual plan.
npx checkly deploy
