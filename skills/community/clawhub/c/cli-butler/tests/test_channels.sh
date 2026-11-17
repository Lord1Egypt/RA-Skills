#!/usr/bin/env bash
# Tests for lib/channels.sh (Task 3). Sourced by tests/run.sh from repo root.

section "channel_available"
t_eq "brew via fake" "0" "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_available brew; echo $?')"
t_eq "cargo via fake" "0" "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_available cargo; echo $?')"
t_eq "unknown id rejected" "1" "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_available nonexistent; echo $?')"

section "channel_enumerate"
t_eq "brew merges formula+cask" "$(printf 'cowsay\t3.7.0\nfd\t9.0.0\nripgrep\t14.1.0\norbstack\t1.9.1')" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_enumerate brew')"
t_eq "npm skips header and self" "$(printf 'corepack\t0.29.0\ntypescript\t5.7.2')" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_enumerate npm')"
t_eq "pnpm scoped name intact" "$(printf '@nestjs/cli\t11.0.0\npnpm\t9.15.0')" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_enumerate pnpm')"
t_eq "pipx whitespace split" "$(printf 'black\t24.1.0\nhttpie\t3.2.2')" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_enumerate pipx')"
t_eq "uv plain lines" "$(printf 'duckdb\t1.0.0')" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_enumerate uv')"
t_eq "cargo strips v prefix" "$(printf 'fd-find\t9.0.0\nripgrep\t14.1.0')" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_enumerate cargo')"
t_eq "gem parenthesis split" "$(printf 'bundler\t2.4.10\nrake\t13.0.6')" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_enumerate gem')"
t_eq "apt via dpkg-query" "$(printf 'curl\t7.81.0-1\ngit\t2.34.1')" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_enumerate apt')"
t_fail "unknown id fails" bash -c '. lib/channels.sh; channel_enumerate nonexistent'

section "channel_desc"
t_eq "brew desc" "Configurable talking cow" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_desc brew cowsay')"
t_eq "npm reads local package.json" "TypeScript is a superset of JavaScript" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_desc npm typescript')"
t_eq "gem apostrophe preserved" "The best way to manage your application's dependencies" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_desc gem bundler')"
t_eq "apt dpkg summary" "command line tool for transferring data with URLs" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_desc apt curl')"
t_eq "uv has no channel desc source (whatis fallback lives in add_row)" "" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_desc uv duckdb')"
t_eq "unknown falls back empty" "" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_desc uv neverseen')"

section "resolve_owner"
t_eq "rule1 brew prefix" "brew|managed" \
  "$(bash -c '. lib/channels.sh; resolve_owner ripgrep /opt/homebrew/Cellar/ripgrep/14.1.0/bin/rg')"
t_eq "rule1 wins over other query (fd-find in cargo too)" "brew|managed" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; resolve_owner fd-find /opt/homebrew/Cellar/fd-find/9.0.0/bin/fd')"
t_eq "rule2 system on darwin" "system|system" \
  "$(BUTLER_OS_OVERRIDE=Darwin bash -c '. lib/channels.sh; resolve_owner docker /usr/bin/docker')"
t_eq "rule2.5 distro path query" "apt|managed" \
  "$(PATH="$FAKE_PATH" BUTLER_OS_OVERRIDE=Linux bash -c '. lib/channels.sh; resolve_owner curl /usr/bin/curl')"
t_eq "rule3 query contains name" "brew|managed" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; resolve_owner cowsay /nowhere/cowsay')"
JDIR="$(mktemp -d)"; mkdir -p "$JDIR"; printf 'loose-tool\tmanual\t1700000000\texample-src\tnote\n' > "$JDIR/journal.tsv"
t_eq "rule4 journal manual" "manual|manual" \
  "$(PATH="$FAKE_PATH" BUTLER_JOURNAL_DIR="$JDIR" bash -c '. lib/channels.sh; resolve_owner loose-tool /fixture/bin/loose-tool')"
rm -rf "$JDIR"
t_eq "rule5 untracked" "manual|untracked" \
  "$(PATH="$FAKE_PATH" BUTLER_JOURNAL_DIR="$(mktemp -d)" bash -c '. lib/channels.sh; resolve_owner loose-tool /fixture/bin/loose-tool')"

section "route builders"
t_eq "brew formula uninstall" "brew uninstall cowsay" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_uninstall_cmd brew cowsay')"
t_eq "brew cask uninstall flagged" "brew uninstall --cask orbstack" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_uninstall_cmd brew orbstack')"
t_eq "npm uninstall" "npm uninstall -g typescript" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_uninstall_cmd npm typescript')"
t_eq "pnpm scoped uninstall" "pnpm remove -g @nestjs/cli" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_uninstall_cmd pnpm @nestjs/cli')"
t_eq "cargo upgrade reinstall" "cargo install fd-find" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_upgrade_cmd cargo fd-find')"
t_eq "apt install route" "apt-get install -y curl" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_install_cmd apt curl')"
t_eq "brew cask upgrade" "brew upgrade --cask orbstack" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_upgrade_cmd brew orbstack')"

section "pipx empty-state"
t_eq "empty-state banner filtered from enumeration" "" \
  "$(PATH="$FAKE_PATH" BUTLER_FAKE_PIPX_LIST="$FIXTURES/data/pipx-empty.txt" bash -c '. lib/channels.sh; channel_enumerate pipx')"
t_eq "pipx no installs: shared bin dir not claimed" "$HOME/.local/pipx/venvs" \
  "$(PATH="$FAKE_PATH" BUTLER_FAKE_PIPX_LIST="$FIXTURES/data/pipx-empty.txt" bash -c '. lib/channels.sh; channel_enumerate pipx >/dev/null; channel_prefixes pipx')"
t_eq "pipx has installs: shared bin dir claimed" "$HOME/.local/pipx/venvs $HOME/.local/bin" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; ENUM_pipx=$(printf "black\\t24.1.0"); channel_prefixes pipx')"
t_eq "uv no tools: shared bin dir not claimed" "$FIXTURES/data/../prefix/uv-tools" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; channel_prefixes uv')"
t_eq "uv has tools: shared bin dir claimed" "$FIXTURES/data/../prefix/uv-tools $HOME/.local/bin" \
  "$(PATH="$FAKE_PATH" bash -c '. lib/channels.sh; ENUM_uv=$(printf "duckdb\\t1.0.0"); channel_prefixes uv')"
