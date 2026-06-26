#!/bin/bash
set -e

# Find project root by locating go.mod (prefer current directory)
PROJECT_ROOT="$PWD"
while [ "$PROJECT_ROOT" != "/" ] && [ ! -f "$PROJECT_ROOT/go.mod" ]; do
    PROJECT_ROOT="$(dirname "$PROJECT_ROOT")"
done

if [ ! -f "$PROJECT_ROOT/go.mod" ]; then
    echo "Error: Cannot find project root (go.mod). Please run this script from the cloudinary_mcp project directory."
    exit 1
fi

CLI_BIN="$PROJECT_ROOT/cloudinary-cli"
ENV_FILE="$PROJECT_ROOT/cmd/cli/.env"

if [ ! -f "$CLI_BIN" ]; then
    echo "CLI not found. Running installer..."
    bash "$PROJECT_ROOT/.agents/skills/cloudinary-cli/scripts/install.sh"
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found."
    echo "Please create it with the following variables:"
    echo "  CLOUDINARY_CLOUD=your_cloud_name"
    echo "  CLOUDINARY_KEY=your_api_key"
    echo "  CLOUDINARY_SECRET=your_api_secret"
    echo "  CLOUDINARY_DIRECTORY=uploads        # optional"
    echo "  CLOUDINARY_COMPRESS=true            # optional"
    exit 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)

MISSING=""
[ -z "$CLOUDINARY_CLOUD" ] && MISSING="$MISSING CLOUDINARY_CLOUD"
[ -z "$CLOUDINARY_KEY" ] && MISSING="$MISSING CLOUDINARY_KEY"
[ -z "$CLOUDINARY_SECRET" ] && MISSING="$MISSING CLOUDINARY_SECRET"

if [ -n "$MISSING" ]; then
    echo "Error: Missing required env variables:$MISSING"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file1> [file2] ..."
    exit 1
fi

cd "$PROJECT_ROOT/cmd/cli"
"$CLI_BIN" "$@"
