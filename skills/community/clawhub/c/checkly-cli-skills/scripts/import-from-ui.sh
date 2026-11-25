#!/bin/bash
# Import existing checks from Checkly UI to code

set -e

echo "📥 Importing existing checks from Checkly..." >&2

# Check authentication
if ! npx checkly whoami &> /dev/null; then
  echo "❌ Not authenticated. Run 'npx checkly login' first." >&2
  exit 1
fi

# Import checks
npx checkly import plan

echo "" >&2
echo "✅ Import plan created; adoption is not complete." >&2
echo "" >&2
echo "Next steps:" >&2
echo "  1. Review imported files: git diff" >&2
echo "  2. Apply the reviewed plan: npx checkly import apply --plan-id <plan-id> --no-commit" >&2
echo "  3. Test the adopted project: npx checkly test" >&2
echo "  4. Make generated code durable in your deployment branch" >&2
echo "  5. Preview finalization: npx checkly import commit --plan-id <plan-id> --dry-run" >&2
echo "  6. Follow checkly-import's confirmation flow (exit 3 means approval required)" >&2
echo "Do not deploy generated code before applying its import plan." >&2
