#!/bin/sh
# Launch the HiDataLinker MCP proxy. It talks to the running desktop app.
set -eu

if [ -n "${HIDATALINKER_MCP:-}" ] && [ -x "${HIDATALINKER_MCP}" ]; then
	exec "${HIDATALINKER_MCP}"
fi

script_dir=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/../../.." && pwd)

for candidate in \
	"$repo_root/src-tauri/target/debug/agent-mcp" \
	"$repo_root/src-tauri/target/release/agent-mcp" \
	"${HOME:-}/.hidatalinker/bin/agent-mcp" \
	"$repo_root/src-tauri/target/debug/agent-mcp.exe" \
	"$repo_root/src-tauri/target/release/agent-mcp.exe" \
	"${HOME:-}/.hidatalinker/bin/agent-mcp.exe"
do
	if [ -x "$candidate" ]; then
		exec "$candidate"
	fi
done

for candidate in \
	"$repo_root/src-tauri/target/debug/app" \
	"$repo_root/src-tauri/target/release/app"
do
	if [ -x "$candidate" ]; then
		exec "$candidate" --agent-mcp
	fi
done

echo "HiDataLinker agent-mcp was not found. Build it with: cargo build --bin agent-mcp --manifest-path src-tauri/Cargo.toml" >&2
exit 1
