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

cd "$PROJECT_ROOT"

if ! command -v go &> /dev/null; then
    echo "Error: Go is not installed. Please install Go first: https://go.dev/dl/"
    exit 1
fi

echo "Building cloudinary-cli..."
go build -o cloudinary-cli ./cmd/cli/
echo "Done: $PROJECT_ROOT/cloudinary-cli"
