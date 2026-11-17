#!/usr/bin/env bash
# Test suite for android-arm64-devkit-skill.
#
#   ./tests/run-tests.sh
#
# The adb-related tests run against a COPY of scripts/ in a temp dir, so the
# real (gitignored) config.sh is never read and never written.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STUB="$REPO/tests/stubs"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
COPY="$TMP/repo"; mkdir -p "$COPY"; cp -r "$REPO/scripts" "$COPY/"

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf '  ok   %s\n' "$1"; }
ko()  { FAIL=$((FAIL+1)); printf '  FAIL %s\n' "$1"; [ -n "${2:-}" ] && printf '       %s\n' "$2"; }
has() { [ "${1#*"$2"}" != "$1" ]; }

echo "== setup-aapt2-arm64.sh =="

out="$(bash "$REPO/scripts/setup-aapt2-arm64.sh" --bogus 2>&1)"; rc=$?
[ "$rc" = 2 ] && ok "unknown option exits 2" || ko "unknown option exits 2" "exit=$rc"

out="$(bash "$REPO/scripts/setup-aapt2-arm64.sh" 2>&1)"; rc=$?
[ "$rc" = 0 ] && ok "check mode exits 0" || ko "check mode exits 0" "exit=$rc"
has "$out" "ARM aarch64" && ok "reports the native aarch64 toolchain" || ko "reports the native aarch64 toolchain"

proj="$TMP/proj"; mkdir -p "$proj"; printf 'org.gradle.jvmargs=-Xmx1g\n' > "$proj/gradle.properties"
bash "$REPO/scripts/setup-aapt2-arm64.sh" --write-gradle-property "$proj" >/dev/null 2>&1
bash "$REPO/scripts/setup-aapt2-arm64.sh" --write-gradle-property "$proj" >/dev/null 2>&1
n="$(grep -c '^android.aapt2FromMavenOverride=' "$proj/gradle.properties")"
[ "$n" = 1 ] && ok "writes the gradle property exactly once (idempotent)" || ko "writes the gradle property exactly once (idempotent)" "count=$n"
grep -q '^org.gradle.jvmargs=' "$proj/gradle.properties" \
  && ok "preserves existing gradle.properties content" || ko "preserves existing gradle.properties content"

echo "== scripts/lib/adb.sh =="

[ -f "$REPO/scripts/lib/adb.sh" ] && ok "lib exists" || ko "lib exists" "missing scripts/lib/adb.sh"

if [ -f "$REPO/scripts/lib/adb.sh" ]; then
  out="$(PATH="$STUB:$PATH" STUB_ARGV=1 bash -c ". '$REPO/scripts/lib/adb.sh'; ADB_REMOTE_HOST=; adb_call -s dev:1 install -r /tmp/a.apk" 2>&1)"
  if has "$out" "ARG[-s]" && has "$out" "ARG[dev:1]" && has "$out" "ARG[-r]"; then
    ok "local: arguments reach adb as separate argv entries"
  else
    ko "local: arguments reach adb as separate argv entries" "$(printf '%s' "$out" | tr '\n' ' ')"
  fi

  out="$(PATH="$STUB:$PATH" ADB_REMOTE_HOST=testhost ADB_REMOTE_BIN=adb.exe bash -c ". '$REPO/scripts/lib/adb.sh'; adb_call -s dev:1 install -r /tmp/a.apk" 2>&1)"
  if has "$out" "adb.exe" && has "$out" "-s" && has "$out" "dev:1"; then
    ok "remote: command carries the binary and all arguments"
  else
    ko "remote: command carries the binary and all arguments" "$out"
  fi
fi

echo "== adb-connect.sh =="

out="$(cd "$COPY" && PATH="$STUB:$PATH" ADB_HOST=dev bash scripts/adb-connect.sh 2>&1)"; rc=$?
[ "$rc" != 0 ] && has "$out" "No wireless port found" \
  && ok "refuses to guess when no wireless port is discoverable" \
  || ko "refuses to guess when no wireless port is discoverable" "exit=$rc out=$(printf '%s' "$out" | tr '\n' ' ')"

out="$(cd "$COPY" && PATH="$STUB:$PATH" ADB_HOST=dev \
      STUB_DEVICES_L="dev:41271   device product:STUB model:STUB transport_id:1" \
      STUB_DEVICES="dev:41271	device" bash scripts/adb-connect.sh 2>&1)"; rc=$?
has "$out" "dev:41271" && ok "discovers the port from an existing wireless transport" \
  || ko "discovers the port from an existing wireless transport" "$(printf '%s' "$out" | tr '\n' ' ')"
[ "$rc" = 0 ] && ok "connects successfully with a good port" || ko "connects successfully with a good port" "exit=$rc"

# A Windows-hosted adb server answers with CRLF; the state parser must survive it.
out="$(cd "$COPY" && PATH="$STUB:$PATH" ADB_HOST=dev STUB_CRLF=1 \
      STUB_DEVICES_L="dev:41271   device product:STUB model:STUB transport_id:1" \
      STUB_DEVICES="dev:41271 device" bash scripts/adb-connect.sh 2>&1)"; rc=$?
[ "$rc" = 0 ] && has "$out" "is ready" \
  && ok "tolerates CRLF line endings from a Windows adb server" \
  || ko "tolerates CRLF line endings from a Windows adb server" "exit=$rc out=$(printf '%s' "$out" | tr -d '\r' | tr '\n' ' ')"

echo "== SKILL.md =="

SKILL="$REPO/SKILL.md"
[ -f "$SKILL" ] && ok "SKILL.md exists at repo root" || ko "SKILL.md exists at repo root" "missing SKILL.md"

if [ -f "$SKILL" ]; then
  grep -q '^name: *android-arm64-devkit' "$SKILL" \
    && ok "frontmatter declares the skill name" || ko "frontmatter declares the skill name"

  desc="$(sed -n 's/^description: *//p' "$SKILL" | head -1)"
  [ -n "$desc" ] && [ "${#desc}" -lt 200 ] \
    && ok "description present and under 200 chars (${#desc})" \
    || ko "description present and under 200 chars" "len=${#desc}"

  # Files that only exist at runtime (gitignored, e.g. config.sh copied from
  # config.example.sh) are expected to be absent in a fresh clone.
  miss=""
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    git -C "$REPO" check-ignore -q "$p" && continue
    [ -e "$REPO/$p" ] || miss="$miss $p"
  done < <(grep -oE '\{baseDir\}/[A-Za-z0-9._/-]+' "$SKILL" | sed 's#{baseDir}/##' | sort -u)
  [ -z "$miss" ] && ok "every {baseDir} reference resolves" || ko "every {baseDir} reference resolves" "missing:$miss"

  grep -qiE '^#+ .*host' "$SKILL" && grep -qi 'aarch64' "$SKILL" \
    && grep -qi 'x86-64' "$SKILL" && grep -qi 'windows' "$SKILL" \
    && ok "has a host-branch section (ARM64 vs x86-64 vs Windows)" \
    || ko "has a host-branch section (ARM64 vs x86-64 vs Windows)"
  grep -q 'config.example.sh' "$SKILL" \
    && ok "routes personal values through config.example.sh" || ko "routes personal values through config.example.sh"

  grep -qiE '^#+ .*gotcha' "$SKILL" \
    && ok "has an ARM64 host-gotchas section" || ko "has an ARM64 host-gotchas section"
  grep -qF 'case $-' "$SKILL" \
    && ok "documents the non-interactive shell rc-guard trap" || ko "documents the non-interactive shell rc-guard trap"
  grep -q 'compileSdk' "$SKILL" \
    && ok "documents the compileSdk cap with the distro aapt2" || ko "documents the compileSdk cap with the distro aapt2"

  grep -q 'new-project.sh' "$SKILL" \
    && ok "documents the scaffold script" || ko "documents the scaffold script"
  grep -qiE '^#+ .*create' "$SKILL" \
    && ok "has a create-an-app section" || ko "has a create-an-app section"
fi

echo "== new-project.sh =="

NP="$REPO/scripts/new-project.sh"
[ -f "$NP" ] && ok "new-project.sh exists" || ko "new-project.sh exists" "missing scripts/new-project.sh"

if [ -f "$NP" ]; then
  bash "$NP" >/dev/null 2>&1; rc=$?
  [ "$rc" = 2 ] && ok "no args exits 2" || ko "no args exits 2" "exit=$rc"

  bash "$NP" "$TMP/bad1" "bad-pkg" >/dev/null 2>&1; rc=$?
  [ "$rc" = 2 ] && ok "rejects an invalid package id" || ko "rejects an invalid package id" "exit=$rc"

  bash "$NP" "$TMP/bad2" "com.1bad.app" >/dev/null 2>&1; rc=$?
  [ "$rc" = 2 ] && ok "rejects a segment starting with a digit" || ko "rejects a segment starting with a digit" "exit=$rc"

  bash "$NP" "$TMP/bad3" "single" >/dev/null 2>&1; rc=$?
  [ "$rc" = 2 ] && ok "rejects a single-segment package id" || ko "rejects a single-segment package id" "exit=$rc"

  proj2="$TMP/MyApp"
  bash "$NP" "$proj2" com.example.myapp "My App" >/dev/null 2>&1
  [ -f "$proj2/settings.gradle.kts" ] && [ -f "$proj2/app/build.gradle.kts" ] \
    && [ -f "$proj2/app/src/main/AndroidManifest.xml" ] \
    && [ -f "$proj2/app/src/main/java/com/example/myapp/MainActivity.kt" ] \
    && ok "scaffolds the project tree" || ko "scaffolds the project tree"

  grep -q 'namespace = "com.example.myapp"' "$proj2/app/build.gradle.kts" \
    && ok "sets namespace/applicationId from the package id" || ko "sets namespace/applicationId from the package id"
  grep -q '^package com.example.myapp' "$proj2/app/src/main/java/com/example/myapp/MainActivity.kt" \
    && ok "sets the Kotlin package" || ko "sets the Kotlin package"
  grep -q '^android.aapt2FromMavenOverride=' "$proj2/gradle.properties" \
    && ok "applies the aapt2 override via setup-aapt2-arm64.sh" || ko "applies the aapt2 override via setup-aapt2-arm64.sh"

  bash "$NP" "$proj2" com.example.myapp >/dev/null 2>&1; rc=$?
  [ "$rc" = 2 ] && ok "refuses to overwrite an existing path" || ko "refuses to overwrite an existing path" "exit=$rc"
fi

echo "== repository hygiene =="

miss=""
for f in config.sh .adb-device out/screen.png local.properties x.keystore app.apk; do
  git -C "$REPO" check-ignore -q "$f" 2>/dev/null || miss="$miss $f"
done
[ -z "$miss" ] && ok ".gitignore covers every sensitive/derived path" || ko ".gitignore covers every sensitive/derived path" "not ignored:$miss"

# personal-data guard: build the pattern from fragments so this file is not a hit
p1="jag""ones"; p2="one""plus"; p3="10""0.67.181"; p4="gio""va"; p5="Min""ipad"
PAT="$p1|$p2|$p3|$p4|$p5"
# scan only what could actually be committed: tracked + untracked-but-not-ignored
hits=""
while IFS= read -r f; do
  case "$f" in LICENSE|tests/*) continue ;; esac
  [ -f "$REPO/$f" ] || continue
  grep -qEi "$PAT" "$REPO/$f" && hits="$hits $f"
done < <(git -C "$REPO" ls-files --cached --others --exclude-standard)
[ -z "$hits" ] && ok "no personal data in tracked files (LICENSE excluded)" \
  || ko "no personal data in tracked files" "$(printf '%s' "$hits" | tr '\n' ' ')"

n="$(find "$REPO/tests" -type f | wc -l)"
[ "$n" -ge 3 ] && ok "test files are present ($n)" || ko "test files are present" "found $n"

echo
printf 'TOTAL: %s passed, %s failed\n' "$PASS" "$FAIL"
[ "$FAIL" = 0 ]
