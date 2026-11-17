#!/usr/bin/env bash
# Tests for lib/function.sh + list.sh --by-function (v0.1.1). Sourced by tests/run.sh.

section "function categorization"

. "$REPO_ROOT/lib/function.sh"

fcat() { categorize "$1" "$2" "$3"; printf '%s' "$FUNC_CAT"; }

t_eq "claude is AI"        "AI / Agent 工具"    "$(fcat untracked claude "")"
t_eq "adb is mobile dev"   "移动开发"           "$(fcat untracked adb "")"
t_eq "docker is infra"     "容器 / 基础设施"     "$(fcat managed docker "Pack, ship and run any application")"
t_eq "lazygit is VCS"      "版本控制"           "$(fcat brew lazygit "A simple terminal UI for git commands")"
t_eq "libpng is a library" "库依赖"             "$(fcat brew libpng "Library for manipulating PNG images")"
t_eq "caddy is web"        "Web / 网络"         "$(fcat brew caddy "web server with automatic HTTPS")"
t_eq "ffmpeg is media"     "多媒体"             "$(fcat brew ffmpeg "Play, record, convert audio video")"
t_eq "node is a runtime"   "语言运行时"          "$(fcat npm node "")"
t_eq "gpg-agent is NOT AI" "其他独立工具"        "$(fcat brew gpg-agent "agent protocol helper")"
t_eq "system row buckets to system" "系统自带（SIP）" "$(fcat system sh "")"
t_eq "cow falls to fallback" "其他独立工具"       "$(fcat brew cowsay "Configurable talking cow")"

out=$(env PATH="$FAKE_PATH:$FIXTURES/prefix/systembin" BUTLER_OS_OVERRIDE=Darwin \
  BUTLER_LIST_PATH="$FAKE_BIN:$FIXTURES/prefix/systembin" BUTLER_PROBE_TIMEOUT=5 \
  BUTLER_SYSTEM_PREFIXES=":$FIXTURES/prefix/systembin:" \
  bash "$REPO_ROOT/bin/list.sh" --by-function 2>/dev/null)
t_contains "function view has AI group" "== AI / Agent 工具" "$out"
t_contains "claude listed with channel attr" "claude" "$out"
t_contains "function view has fallback group" "== 其他独立工具" "$out"
t_contains "function view has system group" "== 系统自带（SIP）" "$out"
t_contains "rows carry channel attribute" "npm" "$out"

out=$(env PATH="$FAKE_PATH" BUTLER_OS_OVERRIDE=Darwin \
  BUTLER_LIST_PATH="$FAKE_BIN" BUTLER_PROBE_TIMEOUT=5 \
  bash "$REPO_ROOT/bin/list.sh" 2>/dev/null)
t_contains "default channel view unchanged" "== brew (4)" "$out"
