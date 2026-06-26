#!/bin/zsh
# 内容工坊 NotebookLM wrapper - sets NODE_PATH so playwright resolves correctly
export NODE_PATH="/Users/dylanzheng/node_modules:$NODE_PATH"
exec npx --yes notebooklm "$@"