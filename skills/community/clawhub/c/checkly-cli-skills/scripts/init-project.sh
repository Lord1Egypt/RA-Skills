#!/bin/bash
# Initialize a new Checkly monitoring project

set -e

PROJECT_NAME="${1:-my-monitoring-project}"

echo "🚀 Creating Checkly monitoring project: $PROJECT_NAME" >&2

# Create project
npm create checkly@latest "$PROJECT_NAME" -- --yes

cd "$PROJECT_NAME"

echo "✅ Project created successfully!" >&2
echo "" >&2
echo "Next steps:" >&2
echo "  cd $PROJECT_NAME" >&2
echo "  npx checkly login" >&2
echo "  npx checkly test" >&2
echo "  npx checkly deploy" >&2
