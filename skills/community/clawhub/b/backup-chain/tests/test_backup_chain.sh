#!/usr/bin/env bash
# backup-chain v1.2.2 functional test suite.
# Runs the protocol against synthetic workspaces: gates, fencing, drills,
# per-member restore, ledger adapters, refusals, witness layer (v1.1):
# decision traces, operator acks, custody events; curation layer (v1.2):
# per-member excludes, walk pruning, evict with custody hand-off, build
# stow, advisory detections, and the ack policy — disabling acks is a
# witnessed act, never a traceless one; staging discipline (v1.2.1):
# pre-planted symlink decoys at the old predictable staging names are
# ignored, and crash leftovers stay self-excluded; ledger line discipline
# and stow staging (v1.2.2): every str.splitlines() separator is refused by
# writers and inert to readers, and a stow destination's planted symlink is
# replaced, never followed; sink-inventory tripwire (v1.2.2): drift in what the
# tool can write or spawn fails the suite until it is classified, and the
# tripwire is itself tested by planting each kind of drift. No network.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BC="python3 $HERE/../scripts/backup_chain.py"
PASS=0; FAIL=0
WS_BASE="$(mktemp -d /tmp/backup-chain-test.XXXXXX)"
trap 'rm -rf "$WS_BASE"' EXIT

ok()   { PASS=$((PASS+1)); echo "  PASS: $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL: $1"; }
check() { # check <desc> <expected_rc> <actual_rc>
  if [ "$2" -eq "$3" ]; then ok "$1 (rc=$3)"; else bad "$1 (expected rc=$2, got rc=$3)"; fi
}
assert_has() { # assert_has <desc> <needle> <haystack>
  case "$3" in *"$2"*) ok "$1";; *) bad "$1 (missing: $2)";; esac
}
latest() { # latest <dir> <prefix>  → BARE filename of the matching tarball
  (cd "$1" 2>/dev/null && ls "${2}"*.tar.gz 2>/dev/null | sed 's|.*/||' | sort | tail -1)
}

echo "== T1 init + members + gated build (gen 1) =="
WS="$WS_BASE/ws"; mkdir -p "$WS"
cd "$WS" || exit 1
echo "alpha" > worklog.md
mkdir -p skills/sk1 download
echo "skill body" > skills/sk1/SKILL.md
echo "deliverable" > download/report.md
$BC init --name demo --output-dir download >/dev/null 2>&1; check "init" 0 $?
$BC init >/dev/null 2>&1; check "re-init refused without --force" 2 $?
$BC member add worklog.md --critical >/dev/null 2>&1; check "member add file" 0 $?
$BC member add skills/ >/dev/null 2>&1; check "member add dir" 0 $?
$BC member add download/ --critical >/dev/null 2>&1; check "member add output dir" 0 $?
OUT1="$($BC build --carries 'first blood' 2>&1)"; RC1=$?
check "build gen1" 0 $RC1
assert_has "drill gate passed" "restore drill: PASS" "$OUT1"
assert_has "roundtrip gate" "manifest roundtrip: OK" "$OUT1"
T1="$(latest "$WS" download/demo-g1)"
[ -n "$T1" ] && ok "tarball exists: $T1" || bad "tarball g1 missing"
[ -f "$WS/download/$T1.sha256" ] && ok "receipt exists" || bad "receipt missing"
[ ! -e "$WS/download/.download" ] && ok "no stray temp files" || bad "stray temp files"

echo "== T2 chain linkage (gen 2 parent == gen 1 sha) =="
OUT2="$($BC build --carries 'second' 2>&1)"; check "build gen2" 0 $?
T2="$(latest "$WS" download/demo-g2)"
PARENT="$(python3 -c "
import tarfile,json
with tarfile.open('$WS/download/$T2') as tf:
    print(json.load(tf.extractfile('backup-manifest.json'))['parent_sha256'])")"
G1SHA="$(cut -d' ' -f1 "$WS/download/$T1.sha256")"
if [ -n "$PARENT" ] && [ -n "$G1SHA" ] && [ "$PARENT" = "$G1SHA" ]; then
  ok "parent hash links to gen1"
else
  bad "parent mismatch: '$PARENT' vs '$G1SHA'"
fi

echo "== T3 verify: receipt MATCH, tamper detected =="
$BC verify "download/$T1" >/dev/null 2>&1; check "verify clean archive" 0 $?
cp "$WS/download/$T1" "$WS/download/tampered.tar.gz"
printf 'X' | dd of="$WS/download/tampered.tar.gz" bs=1 seek=200 conv=notrunc 2>/dev/null
$BC verify "$WS/download/tampered.tar.gz" >/dev/null 2>&1; check "verify tampered fails" 1 $?

echo "== T4 fencing: head restores, stale refuses =="
D="$($BC check "download/$T2" 2>&1)"; check "check head archive rc" 0 $?
assert_has "decision restore" '"decision": "restore"' "$D"
$BC build --carries 'third' >/dev/null 2>&1; check "build gen3" 0 $?
T3="$(latest "$WS" download/demo-g3)"
D="$($BC check "download/$T2" 2>/dev/null)"; RC=$?
check "stale check refused" 2 $RC
assert_has "stale handoff reason" "stale" "$D"

echo "== T5 per-member restore into empty target =="
TGT="$WS_BASE/target5"
R="$($BC restore "download/$T3" --target "$TGT" 2>&1)"; RC=$?
check "restore head" 0 $RC
assert_has "restored verified" "restored:" "$R"
CMP="$(python3 -c "
import hashlib
def s(p):
    h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()
a=s('$TGT/worklog.md'); b=s('$WS/worklog.md')
c=s('$TGT/skills/sk1/SKILL.md'); d=s('$WS/skills/sk1/SKILL.md')
print('MATCH' if a==b and c==d else 'DIFFER')")"
[ "$CMP" = "MATCH" ] && ok "restored bytes identical" || bad "restored bytes differ"
RECHK="$($BC recheck 3)"; assert_has "recheck ok" '"decision": "ok"' "$RECHK"

echo "== T6 stale restore refused =="
$BC restore "download/$T2" --target "$WS_BASE/target6" >/dev/null 2>&1; check "stale restore refused" 2 $?

echo "== T7 overwrite discipline =="
echo "mutated" > "$TGT/worklog.md"
$BC restore "download/$T3" --target "$TGT" >/dev/null 2>&1; check "conflict refused w/o --overwrite" 2 $?
$BC restore "download/$T3" --target "$TGT" --overwrite >/dev/null 2>&1; check "conflict replaced with --overwrite" 0 $?
GOT="$(cat "$TGT/worklog.md")"
[ "$GOT" = "alpha" ] && ok "file actually restored" || bad "file content wrong: $GOT"

echo "== T8 dry-run writes nothing =="
CNT_BEFORE="$(find "$TGT" -type f | wc -l)"
$BC restore "download/$T3" --target "$TGT" --overwrite --dry-run >/dev/null 2>&1; check "dry-run rc" 0 $?
CNT_AFTER="$(find "$TGT" -type f | wc -l)"
[ "$CNT_BEFORE" = "$CNT_AFTER" ] && ok "dry-run wrote nothing" || bad "dry-run changed files"

echo "== T9 ledger registration survives local loss =="
$BC build --carries 'registered' --register >/dev/null 2>&1; check "registered build" 0 $?
assert_has "ledger carries gen4" "gen=4" "$(cat "$WS/.vault/ledger.log")"
mkdir -p "$WS_BASE/stash" && mv "$WS"/download/demo-g*.tar.gz* "$WS_BASE/stash/" 2>/dev/null
NG="$($BC next-gen | head -1)"
case "$NG" in 5\ *|5$'\t'*) ok "next-gen from ledger after total local loss ($NG)";; *) bad "next-gen from ledger after total local loss (got: $NG)";; esac
mv "$WS_BASE/stash"/* "$WS/download/" 2>/dev/null
T4="$(latest "$WS" download/demo-g4)"
V="$($BC verify "$WS/download/$T4" 2>&1)"
assert_has "ledger authenticity MATCH" "ledger:  MATCH" "$V"

echo "== T10 missing critical member refuses build =="
mv "$WS/worklog.md" "$WS_BASE/worklog.md.bak"
$BC build >/dev/null 2>&1; check "build with missing critical member" 1 $?
mv "$WS_BASE/worklog.md.bak" "$WS/worklog.md"

echo "== T11 drill catches corrupted member (crafted manifest) =="
python3 - "$WS_BASE/bad.tar.gz" <<'PYEOF'
import tarfile, json, io, sys
manifest = {"kind":"backup-chain workspace snapshot","protocol":"backup-chain/1",
            "chain_name":"fake","generation":99,"built_at":"2026-01-01T00:00:00Z",
            "parent_sha256":None,"member_count":1,
            "members":{"f.txt":"0"*64}}
with tarfile.open(sys.argv[1], "w:gz") as tf:
    mb = json.dumps(manifest).encode()
    ti = tarfile.TarInfo("backup-manifest.json"); ti.size = len(mb)
    tf.addfile(ti, io.BytesIO(mb))
    data = b"hello"
    ti = tarfile.TarInfo("f.txt"); ti.size = 5
    tf.addfile(ti, io.BytesIO(data))
PYEOF
$BC drill "$WS_BASE/bad.tar.gz" >/dev/null 2>&1; check "drill fails on corrupt member" 1 $?
$BC restore "$WS_BASE/bad.tar.gz" --target "$WS_BASE/t11" >/dev/null 2>&1; check "restore fails on corrupt member" 1 $?

echo "== T12 unreachable command ledger =="
WS2="$WS_BASE/ws2"; mkdir -p "$WS2"; cd "$WS2" || exit 1
echo "data" > f.txt
$BC init --name ws2 --ledger command --read-cmd "false" --append-cmd "false" >/dev/null 2>&1
$BC member add f.txt --critical >/dev/null 2>&1
$BC build --register --allow-cmd-ledger >/dev/null 2>&1; check "build with dead ledger (register fails loudly)" 1 $?
$BC build >/dev/null 2>&1; check "second build proceeds without register" 0 $?
TG2="$(latest "$WS2" download/ws2-g2)"
D="$($BC check "download/$TG2" 2>/dev/null)"
assert_has "fencing SKIPPED (marked, not silent)" '"decision": "skip"' "$D"
assert_has "skip is local-assertable" "local head" "$D"

echo "== T13 restore without config (wiped vault) =="
TGT13="$WS_BASE/target13"
mkdir -p "$TGT13"
mv "$WS2/.vault" "$WS_BASE/vault2.bak"
R="$($BC restore "download/$TG2" --target "$TGT13" 2>&1)"; RC=$?
check "restore with no vault (marked skip)" 0 $RC
assert_has "skip banner shown" "FENCING SKIPPED" "$R"
[ "$(cat "$TGT13/f.txt")" = "data" ] && ok "bytes restored" || bad "restore content wrong"
mv "$WS_BASE/vault2.bak" "$WS2/.vault"

echo "== T14 status =="
cd "$WS" || exit 1
S="$($BC status 2>&1)"; check "status rc" 0 $?
assert_has "status shows local head" "local head:" "$S"
assert_has "status shows ledger head" "head=4" "$S"

echo "== T15 in-root symlinked file nested in a directory member (dereferenced) =="
WS15="$WS_BASE/ws15"; mkdir -p "$WS15/skills" "$WS15/docs"
cd "$WS15" || exit 1
echo "wl" > worklog.md
echo "real content" > "$WS15/docs/target15.txt"
ln -s "../docs/target15.txt" skills/linked.txt
$BC init --name sym >/dev/null 2>&1
$BC member add worklog.md --critical >/dev/null 2>&1
$BC member add skills/ >/dev/null 2>&1
OUT15="$($BC build --carries 'nested in-root symlink' 2>&1)"; RC15=$?
check "build with nested in-root symlinked file" 0 $RC15
assert_has "drill covers the symlinked member" "skills/linked.txt" "$OUT15"
T15="$(latest "$WS15" download/sym-g1)"
RESTORED="$(python3 -c "
import tarfile
with tarfile.open('$WS15/download/$T15') as tf:
    print(tf.extractfile('skills/linked.txt').read().decode().strip())")"
[ "$RESTORED" = "real content" ] && ok "in-root symlinked file archived with real content" \
  || bad "symlinked file content wrong: '$RESTORED'"

echo "== T20 out-of-root nested symlink is refused at the boundary, not archived =="
echo "secret-ish external bytes" > "$WS_BASE/outside20.txt"
ln -s "$WS_BASE/outside20.txt" skills/cache.txt
OUT20="$($BC build --carries 'boundary test' 2>&1)"; RC20=$?
check "build with out-of-root nested symlink still succeeds" 0 $RC20
assert_has "out-of-root link skipped with warning" "skipping symlink escaping project root" "$OUT20"
T20="$(latest "$WS15" download/sym-g2)"
INARCHIVE="$(python3 -c "
import tarfile, json
with tarfile.open('$WS15/download/$T20') as tf:
    m = json.load(tf.extractfile('backup-manifest.json'))
    print('YES' if 'skills/cache.txt' in m['members'] else 'NO')")"
[ "$INARCHIVE" = "NO" ] && ok "out-of-root link NOT in manifest (no external bytes)" || bad "out-of-root link reached the archive"
assert_has "drill still passes with boundary skip" "restore drill: PASS" "$OUT20"
rm -f skills/cache.txt

echo "== T16 broken symlink nested in a directory member (skipped, not a crash) =="
rm -f skills/linked.txt
ln -s "$WS_BASE/does-not-exist-15.txt" skills/broken.txt
OUT16="$($BC build --carries 'nested broken symlink' 2>&1)"; RC16=$?
check "build with nested broken symlink does not crash" 0 $RC16
assert_has "broken symlink skipped with a warning" "skipping broken symlink" "$OUT16"
rm -f skills/broken.txt

echo "== T17 'member add'/'member remove' with no path argument; bad recheck input =="
$BC member add >/dev/null 2>&1; check "member add w/o path is refused, not a crash" 2 $?
$BC member remove >/dev/null 2>&1; check "member remove w/o path is refused, not a crash" 2 $?
$BC recheck not-a-number >/dev/null 2>&1; check "recheck non-integer is refused, not a traceback" 2 $?

echo "== T18 restore --dry-run previews conflicts without requiring --overwrite =="
TGT18="$WS_BASE/target18"; mkdir -p "$TGT18"
echo "different" > "$TGT18/worklog.md"
# sym-g3 = the T16 broken-symlink build (sym-g2 was consumed by T20's boundary test)
T16="$(latest "$WS15" download/sym-g3)"
OUT18="$($BC restore "download/$T16" --target "$TGT18" --dry-run 2>&1)"; RC18=$?
check "dry-run with conflicts succeeds (no --overwrite needed to preview)" 0 $RC18
assert_has "dry-run reports the conflict" "would need --overwrite" "$OUT18"
[ ! -e "$TGT18/skills" ] && ok "dry-run still wrote nothing" || bad "dry-run wrote files"

echo "== T19 non-regular files (FIFO) in a member dir are skipped, not hung on =="
mkdir -p "$WS15/pipes"
mkfifo "$WS15/pipes/pipe.fifo"
$BC member add pipes/ >/dev/null 2>&1
OUT19="$(timeout 60 $BC build --carries 'fifo guard' 2>&1)"; RC19=$?
if [ "$RC19" = "124" ]; then
  bad "build HUNG on FIFO (timeout killed it) — guard regressed"
else
  check "build with FIFO does not hang/crash" 0 $RC19
fi
assert_has "FIFO skipped with warning" "skipping non-regular file" "$OUT19"
assert_has "drill still passes after FIFO skip" "restore drill: PASS" "$OUT19"
$BC member remove pipes/ >/dev/null 2>&1

echo "== T21 restore refuses symlinked dir component beneath --target (audit T09) =="
WS21="$WS_BASE/ws21"; mkdir -p "$WS21/docs"
cd "$WS21" || exit 1
echo "note bytes" > docs/note.txt
$BC init --name sub >/dev/null 2>&1
$BC member add docs/ >/dev/null 2>&1
$BC build --carries 'restore boundary setup' >/dev/null 2>&1; check "ws21 setup build" 0 $?
T21A="$(latest "$WS21" download/sub-g1)"
mkdir -p "$WS_BASE/outside21"
TGT21="$WS_BASE/target21"; mkdir -p "$TGT21"
ln -s "$WS_BASE/outside21" "$TGT21/docs"
D21="$($BC restore "download/$T21A" --target "$TGT21" --dry-run 2>&1)"; RC21D=$?
check "dry-run previews the symlink-component refusal" 0 $RC21D
assert_has "dry-run names the offending component" "WOULD REFUSE" "$D21"
[ ! -e "$WS_BASE/outside21/note.txt" ] && ok "dry-run wrote nothing outside target" || bad "dry-run wrote through the symlink"
$BC restore "download/$T21A" --target "$TGT21" >/dev/null 2>&1; check "real restore refused on symlinked component" 2 $?
R21="$($BC restore "download/$T21A" --target "$TGT21" 2>&1)"
assert_has "refusal explains the fix" "remove or replace the symlink" "$R21"
[ ! -e "$WS_BASE/outside21/note.txt" ] && ok "refused restore wrote nothing outside target" || bad "restore escaped via symlinked dir"
rm -f "$TGT21/docs"

echo "== T22 final-component symlink: conflict, then --overwrite replaces the link itself =="
echo "outside22 bytes" > "$WS_BASE/outside22.txt"
TGT22="$WS_BASE/target22"; mkdir -p "$TGT22/docs"
ln -s "$WS_BASE/outside22.txt" "$TGT22/docs/note.txt"
$BC restore "download/$T21A" --target "$TGT22" >/dev/null 2>&1; check "symlink at final component is a conflict (refused w/o --overwrite)" 2 $?
[ -f "$WS_BASE/outside22.txt" ] && [ "$(cat "$WS_BASE/outside22.txt")" = "outside22 bytes" ] && ok "refused overwrite left link target untouched" || bad "link target was modified"
$BC restore "download/$T21A" --target "$TGT22" --overwrite >/dev/null 2>&1; check "--overwrite replaces the link itself" 0 $?
if [ ! -L "$TGT22/docs/note.txt" ] && [ "$(cat "$TGT22/docs/note.txt")" = "note bytes" ]; then
  ok "link replaced by real verified file"
else
  bad "final component wrong after overwrite (still a link or wrong content)"
fi
[ "$(cat "$WS_BASE/outside22.txt")" = "outside22 bytes" ] && ok "os.replace did not follow the link (external file intact)" || bad "external file clobbered"

echo "== T23 command-adapter execution is loud AND opted-in (1.0.3 warn + 1.0.4 flag) =="
WS3="$WS_BASE/ws3"; mkdir -p "$WS3"; cd "$WS3" || exit 1
echo "data" > f.txt
$BC init --name ws3 --ledger command \
  --read-cmd "cat $WS_BASE/ws3-ledger.ext" \
  --append-cmd "tee -a $WS_BASE/ws3-ledger.ext" >/dev/null 2>&1
$BC member add f.txt >/dev/null 2>&1
S3ERR="$($BC status --allow-cmd-ledger 2>&1 >/dev/null)"
assert_has "read execution warns at runtime" "WARN" "$S3ERR"
assert_has "warning names the executed command key" "read_cmd" "$S3ERR"
assert_has "warning points at the config file" ".vault/config.json" "$S3ERR"
B3ERR="$($BC build --register --allow-cmd-ledger 2>&1 >/dev/null)"; check "build --register with command adapter still works" 0 $?
assert_has "append execution warns at runtime" "append_cmd" "$B3ERR"
[ -s "$WS_BASE/ws3-ledger.ext" ] && ok "append_cmd still received the ledger entry" || bad "append_cmd never got the entry"
S3="$($BC status --allow-cmd-ledger 2>/dev/null)"
assert_has "ledger still parses through the warned read path" "head=1" "$S3"
J3TG="$(latest "$WS3" download/ws3-g1)"
J3="$($BC check "download/$J3TG" --allow-cmd-ledger 2>/dev/null)"
assert_has "check JSON on stdout stays warning-free" '"decision"' "$J3"

echo "== T24 command adapter refuses without explicit opt-in (1.0.4 audit T09, round 3) =="
WS4="$WS_BASE/ws4"; mkdir -p "$WS4"; cd "$WS4" || exit 1
echo "data" > f.txt
CANARY4="$WS_BASE/ws4-canary.txt"
$BC init --name ws4 --ledger command \
  --read-cmd "/bin/echo \"injected; touch $CANARY4\"" \
  --append-cmd "tee -a $WS_BASE/ws4-ledger.ext" >/dev/null 2>&1
$BC member add f.txt >/dev/null 2>&1
S4="$($BC status 2>&1)"; check "status proceeds without opt-in (refusal is marked, not fatal)" 0 $?
assert_has "read path refuses with opt-in guidance" "allow-cmd-ledger" "$S4"
[ -f "$CANARY4" ] && bad "read_cmd executed WITHOUT opt-in" || ok "read_cmd not executed without opt-in"
[ -f "$WS_BASE/ws4-ledger.ext" ] && bad "append side effect without opt-in" || ok "no ledger side effects without opt-in"
B4="$($BC build --register 2>&1)"; check "build --register without opt-in fails loudly" 1 $?
assert_has "register refusal names the opt-in flag" "allow-cmd-ledger" "$B4"
[ -f "$CANARY4" ] && bad "canary created during refused build" || ok "still no execution without opt-in"
S4B="$($BC status --allow-cmd-ledger 2>/dev/null)"
assert_has "opted-in read executes and parses" "command-adapter ledger" "$S4B"
[ -f "$CANARY4" ] && bad "shell metacharacter ';' was interpreted" || ok "argv execution leaves shell metacharacters inert"
$BC build --register --allow-cmd-ledger >/dev/null 2>&1; check "opted-in register appends through tee" 0 $?
[ -s "$WS_BASE/ws4-ledger.ext" ] && ok "append_cmd executed with opt-in" || bad "append_cmd never ran with opt-in"
$BC init --force --name ws4 --ledger command \
  --read-cmd 'cat "unclosed' --append-cmd "tee -a $WS_BASE/ws4-ledger.ext" >/dev/null 2>&1
S4C="$($BC status --allow-cmd-ledger 2>&1)"
assert_has "unparseable command line is a clean refusal (shlex)" "shlex" "$S4C"
rm -f "$CANARY4"

echo "== T25 config trust boundary: root pin + path containment (1.0.5 audit T09, round 4) =="
WS5="$WS_BASE/ws5"; mkdir -p "$WS5"; cd "$WS5" || exit 1
echo "secret" > f.txt
$BC init --name ws5 >/dev/null 2>&1
$BC member add f.txt >/dev/null 2>&1
cfgset() { # cfgset <key> <json-value> [subkey] — hand-edit the workspace config
  python3 - "$WS5" "$@" <<'PYEOF'
import json, sys
ws, key, val = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
p = ws + "/.vault/config.json"
cfg = json.load(open(p))
if len(sys.argv) > 4:
    cfg[key][sys.argv[4]] = val
else:
    cfg[key] = val
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
}
# 1) planted foreign root — the exfiltration primitive, now refused
cfgset root "\"$WS_BASE\""
S25="$($BC status 2>&1)"; check "planted foreign root refuses status" 1 $?
assert_has "root refusal names the trust boundary" "may not redirect the backup boundary" "$S25"
B25="$($BC build 2>&1)"; check "build under planted foreign root refuses" 1 $?
[ -z "$(ls "$WS5/download" 2>/dev/null)" ] && ok "no archive written under refused root" || bad "archive appeared despite root refusal"
cfgset root "\"$WS5\""
S25B="$($BC status 2>/dev/null)"; check "restored root accepted again" 0 $?
# 2) symlinked path to the SAME workspace must not false-positive the pin
WS5LINK="$WS_BASE/ws5-link"; ln -s "$WS5" "$WS5LINK"
$BC --root "$WS5LINK" status >/dev/null 2>&1; check "symlink path to same workspace passes root pin" 0 $?
# 3) config members re-validated at load ('..' member = collection escape)
echo "outside" > "$WS_BASE/outside25.txt"
cfgset members '[{"path": "../outside25.txt"}]'
B25B="$($BC build 2>&1)"; check "config member with '..' refused at load" 1 $?
assert_has "member refusal names re-validation" "config member rejected" "$B25B"
cfgset members '[{"path": "f.txt"}]'
# 4) chain_name is a filename component — traversal refused
cfgset chain_name '"../../evil25"'
S25C="$($BC status 2>&1)"; check "chain_name traversal refused" 1 $?
assert_has "chain_name refusal is specific" "path separators" "$S25C"
cfgset chain_name '"ws5"'
# 5) output_dir stays inside the workspace
cfgset output_dir "\"$WS_BASE/evil25-out\""
B25C="$($BC build 2>&1)"; check "absolute output_dir refused" 1 $?
assert_has "output refusal points at --output" "--output" "$B25C"
cfgset output_dir '"../evil25-out"'
B25D="$($BC build 2>&1)"; check "traversing output_dir refused" 1 $?
# 6) symlinked output dir: lexical path is inside, resolved path is not
cfgset output_dir '"download"'
rm -rf "$WS5/download"; mkdir "$WS_BASE/evil25-dl"; ln -s "$WS_BASE/evil25-dl" "$WS5/download"
B25E="$($BC build 2>&1)"; check "symlinked output dir refused at build" 1 $?
assert_has "symlink refusal names the resolved escape" "resolves outside" "$B25E"
[ -z "$(ls "$WS_BASE/evil25-dl" 2>/dev/null)" ] && ok "nothing written through the symlink" || bad "archive landed outside via symlink"
rm "$WS5/download"; mkdir "$WS5/download"
# 7) --output stays the operator's per-invocation escape hatch
$BC build --output "$WS_BASE/evil25-out/cli25.tar.gz" >/dev/null 2>&1; check "--output to external path still works (operator voice)" 0 $?
[ -f "$WS_BASE/evil25-out/cli25.tar.gz" ] && ok "archive landed at operator-chosen path" || bad "--output archive missing"
# 8) absolute ledger file path in config: exits 0 but is GATED since 1.0.6
#    (round-4 note: the old cfgset here set a bogus "ledger" subkey and never
#    exercised an external path at all — fixed by pointing at "file")
cfgset ledger "\"$WS_BASE/ws5-ledger-ext.log\"" file
S25L="$($BC status 2>&1)"; check "absolute external ledger config: status exits marked, rc=0" 0 $?
assert_has "status marks the external ledger unreachable" "ledger unreachable" "$S25L"
# 9) init-time validation: same rules for the operator's own arguments
WS5B="$WS_BASE/ws5b"; mkdir -p "$WS5B"; cd "$WS5B" || exit 1
echo x > f.txt
$BC init --name "My Chain" >/dev/null 2>&1; check "init accepts space-bearing chain name" 0 $?
$BC init --force --name "../evil25" >/dev/null 2>&1; check "init refuses separator-bearing --name" 2 $?
assert_has "refused init left the good config intact" "My Chain" "$($BC status 2>/dev/null)"
rm -f "$WS_BASE/outside25.txt"

echo "== T26 external ledger gate (audit round 5): config proposes, operator disposes =="
WS6="$WS_BASE/ws6"; EXT6="$WS_BASE/ext26"; mkdir -p "$WS6" "$EXT6"; cd "$WS6" || exit 1
cfgset6() { # cfgset6 <key> <json-value> [subkey] — cfgset twin bound to $WS6
  python3 - "$WS6" "$@" <<'PYEOF'
import json, sys
ws, key, val = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
p = ws + "/.vault/config.json"
cfg = json.load(open(p))
if len(sys.argv) > 4:
    cfg[key][sys.argv[4]] = val
else:
    cfg[key] = val
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
}
echo data26 > d26.txt
$BC init --name demo26 >/dev/null 2>&1; check "init (in-root ledger default)" 0 $?
$BC member add d26.txt >/dev/null 2>&1; check "member add" 0 $?
$BC build --carries 'control' --register >/dev/null 2>&1
check "control: register to in-root ledger unchanged" 0 $?
# 1) planted absolute external ledger.file — the T09 round-5 primitive
cfgset6 ledger "\"$EXT6/evil26.log\"" file
S26A="$($BC status 2>&1)"; check "status with planted external ledger exits marked, rc=0" 0 $?
assert_has "status marks the gated ledger unreachable" "ledger unreachable" "$S26A"
assert_has "status note names the opt-in flag" "--allow-external-ledger" "$S26A"
R26A="$($BC build --carries x --register 2>&1)"; check "register without flag refused" 1 $?
assert_has "register refusal names --allow-external-ledger" "--allow-external-ledger" "$R26A"
[ ! -e "$EXT6/evil26.log" ] && ok "refused register wrote nothing outside" || bad "append escaped without consent"
R26B="$($BC build --carries x --register --allow-external-ledger 2>&1)"
check "register with flag succeeds (operator voice)" 0 $?
assert_has "opted-in external append warns on stderr" "proceeding under --allow-external-ledger" "$R26B"
grep -q "gen=" "$EXT6/evil26.log" 2>/dev/null && ok "external ledger received the line" || bad "external ledger empty after opted-in register"
S26B="$($BC status --allow-external-ledger 2>&1)"
assert_has "status with flag reads the external ledger" "file ledger at $EXT6/evil26.log" "$S26B"
# 2) traversing relative path lands outside — same gate
cfgset6 ledger "\"../ext26/evil26b.log\"" file
$BC build --carries x --register >/dev/null 2>&1; check "traversing relative ledger.file refused" 1 $?
[ ! -e "$EXT6/evil26b.log" ] && ok "traversing append wrote nothing" || bad "traversal escaped"
# 3) symlink escape: lexical path in-root, resolved target outside
rm -f "$WS6/.vault/ledger.log"   # drop the real ledger from the control build
python3 - "$WS6" "$EXT6" <<'PYEOF'
import os, sys
ws, ext = sys.argv[1], sys.argv[2]
tgt = ext + "/evil26c.log"; open(tgt, "a").close()
os.symlink(tgt, ws + "/.vault/ledger.log")
PYEOF
cfgset6 ledger "\".vault/ledger.log\"" file
$BC build --carries x --register >/dev/null 2>&1
check "symlinked in-root ledger.file refused (resolves outside)" 1 $?
[ "$(wc -l < "$EXT6/evil26c.log")" -eq 0 ] && ok "nothing written through planted symlink" || bad "symlink escape appended"
$BC build --carries x --register --allow-external-ledger >/dev/null 2>&1
check "same symlink append with flag succeeds" 0 $?
[ "$(wc -l < "$EXT6/evil26c.log")" -eq 1 ] && ok "opted-in symlink append landed in target" || bad "flagged symlink append missing"
rm -f "$WS6/.vault/ledger.log"
# 4) in-root symlink to in-root target: unaffected, no flag needed
rm -f "$WS6/.vault/ledger.log"
python3 - "$WS6" <<'PYEOF'
import os, sys
ws = sys.argv[1]
open(ws + "/plain26.log", "w").close()
# absolute target: a symlink INSIDE .vault/ would resolve relative names
# against .vault/, not the workspace root
os.symlink(ws + "/plain26.log", ws + "/.vault/ledger.log")
PYEOF
cfgset6 ledger "\".vault/ledger.log\"" file
S26C="$($BC status 2>&1)"; check "in-root symlinked ledger needs no flag" 0 $?
assert_has "in-root symlink status reachable" "file ledger at" "$S26C"
rm -f "$WS6/.vault/ledger.log" "$WS6/plain26.log"
# 5) malformed ledger shapes refused at load (T09 round 5, shape validation)
cfgset6 ledger "{\"adapter\": \"file\"}"
$BC status >/dev/null 2>&1; check "ledger.file absent falls back to in-root default" 0 $?
cfgset6 ledger "{\"adapter\": \"file\", \"file\": \"\"}"
$BC status >/dev/null 2>&1; check "empty ledger.file refused at load" 1 $?
cfgset6 ledger "\"not-an-object\""
$BC status >/dev/null 2>&1; check "non-object ledger refused at load" 1 $?
cfgset6 ledger "{\"file\": \"ok.log\", \"adapter\": \"command\", \"read_cmd\": \"false\", \"append_cmd\": \"false\"}"
L26="$($BC status 2>&1)"
assert_has "external-ledger flag does NOT unlock the command adapter" "--allow-cmd-ledger" "$L26"
# 6) the documented wipe-safety workflow end to end (operator voice, both ends)
WS6B="$WS_BASE/ws6b"; mkdir -p "$WS6B"; cd "$WS6B" || exit 1
echo x > f26b.txt
I26="$($BC init --ledger-file "$EXT6/wipesafe26.log" 2>&1)"
check "init --ledger-file external accepted (operator voice)" 0 $?
assert_has "init warns about the per-invocation flag" "--allow-external-ledger" "$I26"
$BC member add f26b.txt >/dev/null 2>&1
$BC build --carries ws >/dev/null 2>&1
check "unflagged build without --register still works" 0 $?
$BC build --carries ws --register >/dev/null 2>&1; check "wipe-safety register needs the flag" 1 $?
$BC build --carries ws --register --allow-external-ledger >/dev/null 2>&1
check "wipe-safety register completes with flag" 0 $?
grep -q "gen=" "$EXT6/wipesafe26.log" 2>/dev/null && ok "wipe-safe external ledger holds the entry" || bad "wipe-safe ledger missing entry"

echo
echo "== T27 witness layer (v1.1): decision traces, acks, events =="
cd "$WS" || exit 1
# legacy archive (built before v1.1, no trace): verify reports absence, no crash
V27LEG="$($BC verify "download/$T1" 2>&1)"
assert_has "legacy manifest reports no trace" "trace:   none recorded (pre-v1.1 generation)" "$V27LEG"
# 1) cot builds, registers, digests into the ledger line
LONG141="$(printf 'a%.0s' $(seq 1 141))"
$BC build --carries cot --cot-trigger quarterly --cot-belief x >/dev/null 2>&1
check "bad cot trigger refused" 2 $?
$BC build --carries cot --cot-belief "orphan belief" >/dev/null 2>&1
check "cot without trigger refused" 2 $?
$BC build --carries cot --cot-trigger manual --cot-belief "$LONG141" >/dev/null 2>&1
check "cot over per-field cap refused (not truncated)" 2 $?
GEN27="$( ($BC next-gen | head -1) | awk '{print $1}')"
LAST27=$((GEN27 - 1))
OUT27="$($BC build --carries cot-test --cot-trigger schedule \
  --cot-belief "tests green, tree clean" \
  --cot-risk "db/ excluded by design" \
  --cot-falsifier "members list matches status output" --register 2>&1)"
check "cot build registers" 0 $?
assert_has "ledger entry carries cot digest" "cot=t=schedule|b=tests_green," "$OUT27"
T27A="$(latest "$WS" "download/demo-g$GEN27")"
MCOT="$(python3 -c "
import tarfile,json
with tarfile.open('$WS/download/$T27A') as tf:
    m=json.load(tf.extractfile('backup-manifest.json'))
print(m['cot']['t'], '|', m['cot']['b'])")"
[ "$MCOT" = "schedule | tests green, tree clean" ] && ok "manifest carries decision trace" || bad "manifest trace wrong: $MCOT"
V27A="$($BC verify "download/$T27A" 2>&1)"
assert_has "verify prints trace" "trace:   t=schedule|b=tests green, tree clean" "$V27A"
assert_has "verify trace ledger digest MATCH" "trace:   ledger digest MATCH" "$V27A"
# 2) tampered ledger digest: MISMATCH is an alarm, not a gate (rc stays 0)
sed -i 's/cot=t=schedule[^ ]*/cot=t=anomaly-TAMPERED/' "$WS/.vault/ledger.log"
V27B="$($BC verify "download/$T27A" 2>&1)"; RC=$?
check "tampered digest does not gate verify" 0 $RC
assert_has "tampered digest alarms" "trace:   ledger digest MISMATCH" "$V27B"
# 3) ack: happy path, unknown gen, note cap, adapter none
$BC ack "$LAST27" "looked at the drill receipt" >/dev/null 2>&1; check "ack known gen" 0 $?
grep -q "op=ack gen=$LAST27 ts=" "$WS/.vault/ledger.log" && ok "ack line in ledger" || bad "ack line missing"
$BC ack 99999 "nothing there" >/dev/null 2>&1; check "ack unknown gen refused" 2 $?
LONGNOTE="$(printf 'n%.0s' $(seq 1 121))"
$BC ack "$LAST27" "$LONGNOTE" >/dev/null 2>&1; check "ack note over cap refused" 2 $?
S27="$($BC status 2>&1)"
assert_has "status shows ack summary" "acks:     1 operator acknowledgment(s) on record" "$S27"
V27C="$($BC verify "download/$T27A" 2>&1)"
assert_has "verify prints ack trail (none yet for this gen)" "witness:  no operator ack on record for this generation" "$V27C"
$BC ack "$GEN27" "seen" >/dev/null 2>&1
V27D="$($BC verify "download/$T27A" 2>&1)"
assert_has "verify prints op=ack witness" "witness:  op=ack ts=" "$V27D"
# 4) restore prints the witness narrative + records the event
TGT27="$WS_BASE/target27"
R27="$($BC restore "download/$T27A" --target "$TGT27" 2>&1)"; check "cot restore" 0 $?
assert_has "restore narrative shows trace" "trace:    built as: t=schedule b=tests green, tree clean" "$R27"
assert_has "restore narrative shows falsifier" "trace:    falsifier: members list matches status output" "$R27"
assert_has "restore records event" "event:    restore recorded in ledger" "$R27"
grep -q "event=restore gen=$GEN27 ts=" "$WS/.vault/ledger.log" && ok "event=restore line in ledger" || bad "event=restore missing"
# 5) standalone drill records its event; acks/events never move next-gen
NG27_BEFORE="$($BC next-gen | head -1)"
$BC drill "download/$T27A" >/dev/null 2>&1; check "standalone drill" 0 $?
grep -q "event=drill gen=$GEN27 ts=" "$WS/.vault/ledger.log" && ok "event=drill line in ledger" || bad "event=drill missing"
NG27_AFTER="$($BC next-gen | head -1)"
[ "$NG27_BEFORE" = "$NG27_AFTER" ] && ok "acks/events do not move next-gen ($NG27_AFTER)" || bad "next-gen moved: '$NG27_BEFORE' -> '$NG27_AFTER'"
# 6) ack with adapter 'none' refused — a witness needs a place to live
WS27B="$WS_BASE/ws27b"; mkdir -p "$WS27B"; cd "$WS27B" || exit 1
echo x > f27.txt
$BC init --ledger none >/dev/null 2>&1
$BC member add f27.txt >/dev/null 2>&1
$BC build >/dev/null 2>&1
$BC ack 1 >/dev/null 2>&1; check "ack with adapter none refused" 2 $?

echo "== T28 symlinked SUBDIRECTORY escaping project root (dirnames, not filenames) =="
# collect_members already refused an out-of-root symlinked FILE nested in a
# directory member (T05/T15). A symlinked DIRECTORY nested the same way goes
# through a different loop (os.walk's dirnames, not filenames) and was never
# checked: os.walk(followlinks=False) already keeps it from being descended
# into (no file content leaks either way), but its bare name still landed in
# the archive as an empty directory placeholder — contradicting "skipped …
# never part of what you selected." This closes that gap.
WS28="$WS_BASE/ws28"; mkdir -p "$WS28/docs" "$WS_BASE/secret28"
cd "$WS28" || exit 1
echo wl > worklog.md
echo "topsecret" > "$WS_BASE/secret28/creds.txt"
ln -s "$WS_BASE/secret28" docs/cache
echo "readme" > docs/readme.txt
$BC init --name dirsym >/dev/null 2>&1
$BC member add worklog.md --critical >/dev/null 2>&1
$BC member add docs/ >/dev/null 2>&1
OUT28="$($BC build --carries 'dir symlink escape' 2>&1)"; check "build with out-of-root dir symlink" 0 $?
assert_has "escaping directory symlink warned and skipped" \
  "skipping symlinked directory escaping project root: docs/cache" "$OUT28"
T28="$(latest "$WS28" download/dirsym-g1)"
NAMES28="$(python3 -c "
import tarfile
with tarfile.open('$WS28/download/$T28') as tf:
    print(' '.join(tf.getnames()))")"
case " $NAMES28 " in
  *" docs/cache "*) bad "escaping dir symlink still left a trace in the archive" ;;
  *) ok "escaping dir symlink left no trace in the archive (not even empty)" ;;
esac
case " $NAMES28 " in
  *" docs/readme.txt "*) ok "sibling real file in the same directory still archived" ;;
  *) bad "sibling real file missing — over-broad exclusion" ;;
esac
# in-root dir symlink: unaffected, still preserved as an empty placeholder
mkdir -p docs/real_sub
ln -s real_sub docs/alias
OUT28B="$($BC build --carries 'in-root dir symlink' 2>&1)"; check "build with in-root dir symlink" 0 $?
T28B="$(latest "$WS28" download/dirsym-g2)"
NAMES28B="$(python3 -c "
import tarfile
with tarfile.open('$WS28/download/$T28B') as tf:
    print(' '.join(tf.getnames()))")"
case " $NAMES28B " in
  *" docs/alias "*) ok "in-root dir symlink still preserved (no regression)" ;;
  *) bad "in-root dir symlink lost its placeholder" ;;
esac

# ---- cfgsetN: config hand-edit helpers bound to a workspace root ----
cfgsetWS() { # cfgsetWS <ws> <key> <json-value> [subkey]
  python3 - "$1" "${@:2}" <<'PYEOF'
import json, sys
ws, key, val = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
p = ws + "/.vault/config.json"
cfg = json.load(open(p))
if len(sys.argv) > 4:
    cfg[key][sys.argv[4]] = val
else:
    cfg[key] = val
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
}

echo
echo "== T29 per-member excludes (v1.2, opt-in) and walk pruning =="
WS29="$WS_BASE/ws29"; mkdir -p "$WS29/code/sub" "$WS29/code/logs"; cd "$WS29" || exit 1
echo wl > worklog.md
echo "keep me" > code/app.txt
echo "noise" > code/debug.log
echo "noise2" > code/sub/inner.log
echo "deep" > code/sub/data.txt
$BC init --name ex29 >/dev/null 2>&1; check "ws29 init" 0 $?
$BC member add worklog.md --critical >/dev/null 2>&1
$BC member add code/ --exclude "*.log" >/dev/null 2>&1; check "member add --exclude" 0 $?
M29="$($BC member list 2>&1)"
assert_has "member list shows the pattern" "*.log" "$M29"
OUT29="$($BC build --carries 'member excludes' 2>&1)"; check "build with member exclude" 0 $?
assert_has "drill passes with excludes" "restore drill: PASS" "$OUT29"
T29A="$(latest "$WS29" download/ex29-g1)"
NAMES29="$(python3 -c "import tarfile; print(' '.join(tarfile.open('$WS29/download/$T29A').getnames()))")"
case " $NAMES29 " in
  *" code/debug.log "*|*" code/sub/inner.log "*) bad "member-excluded log still archived" ;;
  *) ok "member --exclude kept the logs out" ;;
esac
case " $NAMES29 " in
  *" code/app.txt "*) ok "non-matching sibling still archived" ;;
  *) bad "over-broad member exclude" ;;
esac
case " $NAMES29 " in
  *" code/sub/data.txt "*) ok "non-excluded file in unpruned subtree archived" ;;
  *) bad "unpruned subtree lost a file" ;;
esac
# single directory pattern prunes the whole subtree (the old two-pattern gotcha)
$BC member remove code/ >/dev/null 2>&1
$BC member add code/ --exclude sub >/dev/null 2>&1
$BC build --carries 'dir prune' >/dev/null 2>&1; check "build with dir-pattern exclude" 0 $?
T29B="$(latest "$WS29" download/ex29-g2)"
NAMES29B="$(python3 -c "import tarfile; print(' '.join(tarfile.open('$WS29/download/$T29B').getnames()))")"
case " $NAMES29B " in
  *" code/sub/data.txt "*|*" code/sub/inner.log "*) bad "excluded subtree still walked" ;;
  *) ok "one dir pattern pruned the whole subtree" ;;
esac
# hand-edited bad shapes refused at load (config is code)
cfgsetWS "$WS29" members '[{"path": "code/", "exclude": "not-a-list"}]'
B29C="$($BC build 2>&1)"; check "member exclude of wrong shape refused at load" 1 $?
assert_has "member-exclude refusal names the fix" "non-empty pattern strings" "$B29C"
cfgsetWS "$WS29" members '[{"path": "code/", "exclude": ["sub"]}, {"path": "worklog.md", "critical": true}]'
cfgsetWS "$WS29" exclude '"*.log"'
B29D="$($BC build 2>&1)"; check "global exclude of wrong shape refused at load" 1 $?
assert_has "global-exclude refusal names the key" "config exclude" "$B29D"
cfgsetWS "$WS29" exclude '[]'

echo
echo "== T30 evict: custody-preserving member removal (v1.2) =="
cd "$WS29" || exit 1
mkdir -p side30 && echo "side data" > side30/s.txt
$BC member add side30/ >/dev/null 2>&1
E30="$($BC evict side30/ 2>&1)"; check "evict without stow destination refused" 2 $?
assert_has "refusal points at the stow options" "--stow-to" "$E30"
E30B="$($BC evict not-a-member --stow-to "$WS_BASE/stow30" 2>&1)"; check "evict of non-member refused" 2 $?
assert_has "non-member refusal names member remove" "member remove" "$E30B"
E30C="$($BC evict side30/ --stow-to "$WS_BASE/stow30" --note 'dead weight' 2>&1)"
check "evict with --stow-to succeeds" 0 $?
assert_has "evict reports custody" "evicted with custody" "$E30C"
assert_has "evict records the witness" "evict recorded in ledger" "$E30C"
PKG30="$(ls "$WS29"/download/ex29-evict-g*.tar.gz 2>/dev/null | head -1)"
[ -n "$PKG30" ] && ok "eviction package exists" || bad "no eviction package"
[ -f "$WS_BASE/stow30/$(basename "$PKG30")" ] && ok "package copied to --stow-to" || bad "stow copy missing"
[ -f "$WS_BASE/stow30/$(basename "$PKG30").sha256" ] && ok "receipt copied to --stow-to" || bad "stow receipt missing"
STOWSHA="$(sha256sum "$PKG30" | cut -d' ' -f1)"
DSTSHA="$(sha256sum "$WS_BASE/stow30/$(basename "$PKG30")" | cut -d' ' -f1)"
[ "$STOWSHA" = "$DSTSHA" ] && ok "stow roundtrip hash MATCH" || bad "stow copy differs from package"
grep -q "event=evict gen=" "$WS29/.vault/ledger.log" && ok "event=evict line in ledger" || bad "evict witness missing"
grep -q "path=side30" "$WS29/.vault/ledger.log" && ok "witness names the evicted path" || bad "witness path missing"
grep -q "note=dead weight" "$WS29/.vault/ledger.log" && ok "witness carries the note" || bad "witness note missing"
ML30="$($BC member list 2>&1)"; case "$ML30" in *side30*) bad "member still tracked after evict" ;; *) ok "member untracked after evict" ;; esac
EVSHA="$(python3 -c "import tarfile,json
tf = tarfile.open('$PKG30')
m = json.load(tf.extractfile('evict-manifest.json'))
print(m['evicted_path'], m['member_count'], m['note'])")"
case "$EVSHA" in "side30 1 dead weight") ok "evict-manifest carries path/count/note" ;; *) bad "evict-manifest wrong: $EVSHA" ;; esac
# custody failure keeps the member (the whole point)
mkdir -p side30b && echo x > side30b/y.txt
$BC member add side30b/ >/dev/null 2>&1
# A destination BENEATH A REGULAR FILE fails for every uid. (chmod 555 does not
# stop root, so under root - agent sandboxes, Docker CI - this assertion used to
# fail on the one custody refusal that matters most.)
RO30="$WS_BASE/stow30-notadir"; echo x > "$RO30"
E30D="$($BC evict side30b/ --stow-to "$RO30/sub" 2>&1)"; check "evict with failing stow refuses removal (rc=1)" 1 $?
assert_has "custody failure explains the recovery" "member NOT evicted" "$E30D"
ML30B="$($BC member list 2>&1)"; case "$ML30B" in *side30b*) ok "member kept when custody fails" ;; *) bad "member dropped despite failed custody" ;; esac
[ -f "$PKG30" ] && ok "package survives the failed custody attempt" || bad "package lost on failed custody"
rm -f "$RO30"
# evict --stow-cmd happy path (bytes on stdin)
mkdir -p side30c && echo stream > side30c/z.txt
$BC member add side30c/ >/dev/null 2>&1
E30E="$($BC evict side30c/ --stow-cmd "tee -a $WS_BASE/evict30-stream.bin" 2>&1)"
check "evict --stow-cmd succeeds" 0 $?
[ -s "$WS_BASE/evict30-stream.bin" ] && ok "stow-cmd received package bytes on stdin" || bad "stow-cmd got nothing"

echo
echo "== T31 build --stow-to / --stow-cmd (v1.2, opt-in custody hand-off) =="
cd "$WS29" || exit 1
B31="$($BC build --carries 'stow build' --stow-to "$WS_BASE/stow31" 2>&1)"; check "build --stow-to" 0 $?
assert_has "stow MATCH line" "stow:     MATCH" "$B31"
grep -q "event=stow gen=" "$WS29/.vault/ledger.log" && ok "event=stow line in ledger" || bad "stow witness missing"
LAST31="$(ls -t "$WS_BASE/stow31"/ex29-g*.tar.gz 2>/dev/null | head -1)"
[ -n "$LAST31" ] && ok "archive copy landed in stow dir" || bad "no archive in stow dir"
B31B="$($BC build --carries 'stow cmd fail' --stow-cmd false 2>&1)"; check "failing stow-cmd does not fail the build" 0 $?
assert_has "failing stow-cmd warns loudly" "stow command failed" "$B31B"
rm -f "$WS_BASE/stow31-stream.bin"
B31C="$($BC build --carries 'stow cmd ok' --stow-cmd "tee -a $WS_BASE/stow31-stream.bin" >/dev/null 2>&1)"
check "passing stow-cmd" 0 $?
[ -s "$WS_BASE/stow31-stream.bin" ] && ok "stow-cmd received archive bytes on stdin" || bad "stow-cmd got nothing"
B31D="$($BC build --carries 'plain build' 2>&1)"
case "$B31D" in *"stow:"*) bad "unstowed build printed stow lines" ;; *) ok "default build stays silent about stow (option, not default)" ;; esac

echo
echo "== T32 detections (v1.2): advisory failsafes, never gates =="
cd "$WS29" || exit 1
dd if=/dev/zero of=code/big.bin bs=1024 count=600 2>/dev/null
cp code/app.txt code/app-copy.txt
cfgsetWS "$WS29" detect '{"growth_pct": 1, "growth_mb": 0, "archive_mb": 0}'
B32="$($BC build --carries 'detect tripwire' 2>&1)"; check "build with detections armed" 0 $?
assert_has "top-heavy detect fires" "DETECT   largest members:" "$B32"
assert_has "duplicates detect fires" "DETECT   duplicates:" "$B32"
assert_has "archive-bound detect fires" "exceeds the 0 MB archive bound" "$B32"
cfgsetWS "$WS29" detect '{"enabled": false}'
B32B="$($BC build --carries 'silent' 2>&1)"; check "build with detections disabled" 0 $?
case "$B32B" in *"DETECT "*) bad "detect lines present despite enabled:false" ;; *) ok "enabled:false silences detections" ;; esac
dd if=/dev/urandom of=code/rand.bin bs=1024 count=200 2>/dev/null
cfgsetWS "$WS29" detect '{"growth_pct": 1, "growth_mb": 0.0001, "archive_mb": 10000}'
B32C="$($BC build --carries 'growth vs parent' 2>&1)"; check "build for growth tripwire" 0 $?
assert_has "parent-growth detect fires" "vs parent" "$B32C"
cfgsetWS "$WS29" detect '{"growth_pct": 50, "growth_mb": 4, "archive_mb": 32}'
cfgsetWS "$WS29" detect '"bogus"'
B32D="$($BC build 2>&1)"; check "detect of wrong shape refused at load" 1 $?
assert_has "detect refusal names the object" "not an object" "$B32D"
cfgsetWS "$WS29" detect '{"growth_pct": 50, "growth_mb": 4, "archive_mb": 32}'
S32="$($BC status 2>&1)"
assert_has "status shows member sizes" "sizes:    " "$S32"
assert_has "status shows archive totals" "archives: " "$S32"
assert_has "status shows custody ops" "ops:      " "$S32"
assert_has "status shows the evict op" "event=evict" "$S32"
B32E="$($BC build --carries 'detect never gates' 2>&1)"; check "detect-heavy chain still builds clean (rc=0)" 0 $?

echo
echo "== T33 ack policy (v1.2): disabling acks is witnessed, never traceless =="
cd "$WS29" || exit 1
S33="$($BC ack-policy 2>&1)"; check "ack-policy show (default)" 0 $?
assert_has "default policy says enabled" "acks:     enabled (default)" "$S33"
A33="$($BC ack 1 'pre-policy look' 2>&1)"; check "ack works while policy enabled" 0 $?
NG33A="$($BC next-gen | cut -d' ' -f1)"
P33="$($BC ack-policy off --note 'chat-only deployment, human cannot run a shell' 2>&1)"
check "ack-policy off" 0 $?
assert_has "off prints the witness line" "event=ack-off gen=" "$P33"
grep -q "^event=ack-off gen=" "$WS29/.vault/ledger.log" && ok "event=ack-off line in ledger" || bad "ack-off witness missing"
grep -q "note=chat-only deployment" "$WS29/.vault/ledger.log" && ok "policy line carries the why" || bad "policy note missing"
python3 -c "import json; cfg=json.load(open('$WS29/.vault/config.json')); assert cfg.get('ack_policy',{}).get('mode')=='off'" && ok "config records the policy state" || bad "config policy state missing"
$BC ack-policy off >/dev/null 2>&1; check "second off refused (decision already recorded)" 2 $?
A33B="$($BC ack 1 2>&1)"; check "ack refuses while disabled" 2 $?
assert_has "refusal names the recorded decision" "disabled by recorded decision" "$A33B"
assert_has "refusal names the re-enable path" "ack-policy on" "$A33B"
S33B="$($BC status 2>&1)"
assert_has "status shows the policy" "ack policy: DISABLED by recorded decision" "$S33B"
T33V="$(latest "$WS29" download/ex29)"
V33="$($BC verify "$WS29/download/$T33V" 2>&1)"
assert_has "verify attributes absence to the policy" "absence is policy, not neglect" "$V33"
assert_has "verify still passes under the policy (witness, not gate)" "verify: OK" "$V33"
NG33B="$($BC next-gen | cut -d' ' -f1)"
[ "$NG33A" = "$NG33B" ] && ok "policy lines never advance next-gen (parser discipline)" || bad "policy line polluted next-gen: $NG33A -> $NG33B"
P33B="$($BC ack-policy on --note 'local-operator deployment' 2>&1)"; check "ack-policy on" 0 $?
assert_has "on prints the witness line" "event=ack-on gen=" "$P33B"
grep -q "^event=ack-on gen=" "$WS29/.vault/ledger.log" && ok "event=ack-on line in ledger" || bad "ack-on witness missing"
python3 -c "import json; cfg=json.load(open('$WS29/.vault/config.json')); assert 'ack_policy' not in cfg" && ok "config policy state cleared on re-enable" || bad "config policy state not cleared"
A33C="$($BC ack 1 'post-policy look' 2>&1)"; check "ack works again after on" 0 $?
$BC ack-policy on >/dev/null 2>&1; check "on without off refused" 2 $?
cfgsetWS "$WS29" ack_policy '{"mode": "enabled"}'
$BC status >/dev/null 2>&1; check "corrupt ack_policy refused at load" 1 $?
cfgsetWS "$WS29" ack_policy '{"mode": "off", "ts": "2026-01-01T00:00:00Z", "gen": 2, "note": "restored"}'
S33C="$($BC status 2>&1)"
assert_has "hand-set off policy still recognized" "ack policy: DISABLED" "$S33C"
python3 -c "import json; cfg=json.load(open('$WS29/.vault/config.json')); cfg.pop('ack_policy',None); json.dump(cfg,open('$WS29/.vault/config.json','w'))"

echo
echo "== T33b ack policy refuses without a ledger (un-witnessable = unmakeable) =="
WS33="$WS_BASE/ws33"; mkdir -p "$WS33"; cd "$WS33" || exit 1
echo a > a.txt
$BC init --name n33 --ledger none >/dev/null 2>&1
$BC member add a.txt >/dev/null 2>&1
$BC ack-policy off >/dev/null 2>&1; check "ack-policy off refused with adapter none" 2 $?
python3 -c "import json; cfg=json.load(open('$WS33/.vault/config.json')); assert 'ack_policy' not in cfg" && ok "config unchanged after refusal" || bad "config mutated despite refusal"
$BC ack-policy 2>&1 | grep -q "enabled (default)" && ok "policy unchanged after refusal" || bad "show disagrees after refusal"

echo
echo "== T34 staging: pre-planted symlink decoys at the OLD predictable names are ignored (T09 r6) =="
WS34="$WS_BASE/ws34"; mkdir -p "$WS34/out"; cd "$WS34" || exit 1
mkdir -p canary .vault
echo canary-original > canary/canary.txt
ln -s "$PWD/canary/canary.txt" .vault/.config.json.tmp
ln -s "$PWD/canary/canary.txt" .vault/.backup-chain-dir.tmp
ln -s "$PWD/canary/canary.txt" .vault/.last_build.json.tmp
$BC init --name t34 --output-dir out >/dev/null 2>&1; check "init succeeds with decoys planted" 0 $?
grep -q canary-original canary/canary.txt && ok "decoy target untouched by config/marker writes" || bad "decoy target overwritten"
[ -L .vault/.config.json.tmp ] && [ -L .vault/.backup-chain-dir.tmp ] && [ -L .vault/.last_build.json.tmp ] && ok "planted vault decoys intact (never consumed as staging)" || bad "vault decoy consumed or replaced"
echo x > f1.txt; $BC member add f1.txt >/dev/null 2>&1
ln -s "$PWD/canary/canary.txt" out/t34-g1.tar.gz.part
ln -s "$PWD/canary/canary.txt" out/.t34-g1.tar.gz.sha256.tmp
B34="$($BC build 2>&1)"; check "build succeeds with .part and receipt decoys planted" 0 $?
grep -q canary-original canary/canary.txt && ok "decoy target untouched by archive and receipt writes" || bad "archive/receipt write followed decoy"
[ -L out/t34-g1.tar.gz.part ] && [ -L out/.t34-g1.tar.gz.sha256.tmp ] && ok "planted out-dir decoys intact (never consumed as staging)" || bad "out decoy consumed or replaced"
LEFT34="$(find "$WS34/out" "$WS34/.vault" \( -name '*.tmp' -o -name '*.part' \) -type l | wc -l)"
[ "$LEFT34" -eq 5 ] && ok "no NEW staging leftovers (only the 5 planted decoys)" || bad "$LEFT34 staging-link leftovers (expected 5 planted)"
T34A="$(latest "$WS34" out/t34)"
T34V="$($BC verify "out/$T34A" 2>&1)"; assert_has "verify OK after decoy build" "verify: OK" "$T34V"

echo
echo "== T35 staging: restore ignores a pre-planted .restore-part decoy (T09 r6) =="
WS35="$WS_BASE/ws35"; mkdir -p "$WS35/out" "$WS35/target" "$WS35/atticted"; cd "$WS35" || exit 1
echo "restore me" > r1.txt
$BC init --name t35 --output-dir out >/dev/null 2>&1
$BC member add r1.txt >/dev/null 2>&1
$BC build >/dev/null 2>&1; check "build for restore test" 0 $?
echo do-not-touch > "$WS35/atticted/keep.txt"
ln -s "$WS35/atticted/keep.txt" "$WS35/target/r1.txt.restore-part"
R35="$($BC restore "out/t35-g1.tar.gz" --target "$WS35/target" 2>&1)"; check "restore with decoy planted" 0 $?
grep -q do-not-touch "$WS35/atticted/keep.txt" && ok "restore decoy target untouched" || bad "restore wrote through planted symlink"
grep -q "restore me" "$WS35/target/r1.txt" && ok "member restored correctly past decoy (real file, not the link)" || bad "member not restored"
[ ! -L "$WS35/target/r1.txt" ] && ok "restored member is a real file" || bad "restored member is a symlink"
[ -L "$WS35/target/r1.txt.restore-part" ] && ok "planted decoy itself left alone (never our staging)" || bad "planted decoy removed or replaced"
LEFT35="$(find "$WS35/target" -name '*.restore-part' | wc -l)"
[ "$LEFT35" -eq 1 ] && ok "no NEW staging leftovers in target (only the planted decoy)" || bad "$LEFT35 .restore-part leftovers (expected 1 planted)"

echo
echo "== T36 staging: crash leftovers of the new naming stay self-excluded =="
WS36="$WS_BASE/ws36"; mkdir -p "$WS36/out"; cd "$WS36" || exit 1
echo a > a.txt
$BC init --name t36 --output-dir out >/dev/null 2>&1
$BC member add a.txt >/dev/null 2>&1
$BC member add out/ >/dev/null 2>&1
$BC build >/dev/null 2>&1; check "g1 build" 0 $?
printf 'not-an-archive' > "out/.t36-g1.tar.gz.build-JUNK4821.part"
printf 'not-an-archive' > "out/t36-g1.tar.gz.legacy.part"
$BC build >/dev/null 2>&1; check "g2 build with crash leftovers present" 0 $?
if tar -tzf out/t36-g2.tar.gz | grep -q "JUNK4821"; then bad "new-naming crash leftover collected into archive"; else ok "new-naming crash leftover self-excluded"; fi
if tar -tzf out/t36-g2.tar.gz | grep -q "legacy.part"; then bad "legacy-naming crash leftover collected into archive"; else ok "legacy-naming crash leftover self-excluded"; fi
T36V="$($BC verify "out/t36-g2.tar.gz" 2>&1)"; assert_has "verify OK with leftovers excluded" "verify: OK" "$T36V"

echo
echo "== T37 ledger single-line discipline: every str.splitlines() separator, writer AND reader =="
# 1.2.1 rejected only \n \r \x00 in notes, while its reader split with
# str.splitlines(): a note holding U+2028 / VT / NEL / FS was written as ONE
# physical line and read back as TWO, the second a forged build entry
# (next-gen jumped to 1000; a full forged "gen=N sha256=<64 hex>" fits in the cap).
export BCPATH="$HERE/../scripts/backup_chain.py"
WS37="$WS_BASE/ws37"; mkdir -p "$WS37"; cd "$WS37" || exit 1
echo a > a.txt
$BC init --name t37 --ledger file >/dev/null 2>&1
$BC member add a.txt >/dev/null 2>&1
$BC build --carries one --register >/dev/null 2>&1; check "g1 build + register" 0 $?
R37="$(python3 - <<'PYEOF'
import os, subprocess
bc = ["python3", os.environ["BCPATH"]]
forged = "gen=1 sha256=" + "0" * 64
rcs = []
for sep in ["\n", "\r", "\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"]:
    rcs.append(subprocess.run(bc + ["ack", "1", "x" + sep + forged], capture_output=True).returncode)
print("RCS", " ".join(map(str, rcs)))
PYEOF
)"
assert_has "all 10 line-separator variants refused by ack (rc=2 each)" "RCS 2 2 2 2 2 2 2 2 2 2" "$R37"
NG37="$($BC next-gen 2>&1)"; assert_has "next-gen unmoved by the refused acks" "2  # from ledger" "$NG37"
[ "$(wc -l < .vault/ledger.log)" -eq 1 ] && ok "refused acks wrote nothing" || bad "ledger gained lines from refused acks"
$BC ack 1 "an ordinary note" >/dev/null 2>&1; check "ordinary ack still works" 0 $?
printf 'op=ack gen=1 ts=2026-01-01T00:00:00Z note=x\xe2\x80\xa8gen=999 sha256=%064d\n' 0 >> .vault/ledger.log
NG37B="$($BC next-gen 2>&1)"; assert_has "a line poisoned by an older version is inert to the reader" "2  # from ledger" "$NG37B"
assert_has "...and the inertness is loud, not silent (LEDGER-ANOMALY alarm)" "LEDGER-ANOMALY" "$NG37B"
$BC status 2>&1 | grep -q "LEDGER-ANOMALY" && ok "status raises the same alarm" || bad "status silent about a poisoned ledger"
C37="$(python3 - <<'PYEOF'
import importlib.util, os
spec = importlib.util.spec_from_file_location("bc", os.environ["BCPATH"])
bc = importlib.util.module_from_spec(spec); spec.loader.exec_module(bc)
cfg = bc.load_config(os.getcwd())
try:
    bc.ledger_append(cfg, "event=x gen=1 ts=t note=a\u2028gen=7")
    print("ALLOWED")
except bc.GateError:
    print("BLOCKED")
PYEOF
)"
assert_has "ledger_append chokepoint refuses a splitting line from a caller that forgot to validate" "BLOCKED" "$C37"

echo
echo "== T38 stow destination: planted symlink replaced, never followed; no partial copies =="
WS38="$WS_BASE/ws38"; mkdir -p "$WS38/st" "$WS38/outside"; cd "$WS38" || exit 1
echo a > a.txt
$BC init --name t38 --ledger file >/dev/null 2>&1
$BC member add a.txt >/dev/null 2>&1
echo "PRECIOUS" > "$WS38/outside/victim.txt"
ln -s "$WS38/outside/victim.txt" "$WS38/st/t38-g1.tar.gz"
B38="$($BC build --carries x --stow-to "$WS38/st" 2>&1)"; check "build with a decoy at the stow archive name" 0 $?
[ "$(cat "$WS38/outside/victim.txt")" = "PRECIOUS" ] && ok "decoy target never written" || bad "stow followed the planted symlink"
{ [ -f "$WS38/st/t38-g1.tar.gz" ] && [ ! -L "$WS38/st/t38-g1.tar.gz" ]; } && ok "decoy replaced by a regular file" || bad "final stow name is not a regular file"
STSHA="$(sha256sum "$WS38/st/t38-g1.tar.gz" | cut -d' ' -f1)"; DLSHA="$(sha256sum "$WS38/download/t38-g1.tar.gz" | cut -d' ' -f1)"
[ "$STSHA" = "$DLSHA" ] && ok "stow copy is byte-identical to the archive" || bad "stow copy differs from the archive"
assert_has "MATCH is claimed after a real roundtrip" "stow:     MATCH" "$B38"
[ -z "$(ls -A "$WS38/st" | grep -v -e '^t38-g1.tar.gz')" ] && ok "no staging leftovers in the stow dir" || bad "leftover files in the stow dir"
P38="$(python3 - <<'PYEOF'
import importlib.util, os, resource, tempfile, hashlib, shutil
spec = importlib.util.spec_from_file_location("bc", os.environ["BCPATH"])
bc = importlib.util.module_from_spec(spec); spec.loader.exec_module(bc)
d = tempfile.mkdtemp(); src = os.path.join(d, "arch-g1.tar.gz"); dest = os.path.join(d, "stow")
open(src, "wb").write(os.urandom(3 << 20))
dig = hashlib.sha256(open(src, "rb").read()).hexdigest()
soft, hard = resource.getrlimit(resource.RLIMIT_FSIZE)
resource.setrlimit(resource.RLIMIT_FSIZE, (1 << 20, hard))   # writes past 1 MiB fail (EFBIG), root included
try:
    why = bc.stow_to_dir(src, dig, dest)
finally:
    resource.setrlimit(resource.RLIMIT_FSIZE, (soft, hard))
print("FAILED" if why else "UNEXPECTED_OK", "LEFT", len(os.listdir(dest)) if os.path.isdir(dest) else 0)
shutil.rmtree(d, ignore_errors=True)
PYEOF
)"
assert_has "a mid-copy I/O failure is reported as a failure" "FAILED" "$P38"
assert_has "...and leaves no partial file under any name in the custody dir" "LEFT 0" "$P38"

echo
echo "== T39 evict: hostile and oversized member names =="
WS39="$WS_BASE/ws39"; mkdir -p "$WS39/st"; cd "$WS39" || exit 1
echo a > a.txt
$BC init --name t39 --ledger file >/dev/null 2>&1
$BC member add a.txt >/dev/null 2>&1
$BC build --carries one --register >/dev/null 2>&1; check "g1 build + register" 0 $?
R39="$(python3 - <<'PYEOF'
import os, subprocess
bc = ["python3", os.environ["BCPATH"]]
def run(*a):
    r = subprocess.run(bc + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
forged = "gen=999 sha256=" + "0" * 64 + " built=2026-01-01T00:00:00Z file=f.tar.gz entries=1"
evil = "evil\n" + forged
open(evil, "w").write("x")
run("member", "add", evil)
rc1, o1 = run("evict", evil, "--stow-to", "st")
long = "L" * 200
os.makedirs(long); open(long + "/f", "w").write("x")
run("member", "add", long)
rc2, o2 = run("evict", long, "--stow-to", "st")
led = open(".vault/ledger.log").read().split("\n")
print("RC", rc1, rc2)
print("TRACEBACK", "Traceback" in o1 + o2)
print("EVLINES", sum(1 for l in led if l.startswith("event=evict")))
print("FORGED", any(l.startswith("gen=999") for l in led))
print("ESCAPED", any("%0A" in l for l in led if l.startswith("event=evict")))
print("CTRLNAMES", sum(1 for f in os.listdir("download") if any(ord(c) < 32 for c in f)))
PYEOF
)"
assert_has "hostile-named and 200-char members both evict (rc 0 0)" "RC 0 0" "$R39"
assert_has "no traceback from an oversized name" "TRACEBACK False" "$R39"
assert_has "each eviction witnessed by exactly one event line" "EVLINES 2" "$R39"
assert_has "no forged build entry reached the ledger" "FORGED False" "$R39"
assert_has "the hostile path is recorded escaped, not dropped" "ESCAPED True" "$R39"
assert_has "no control characters in output filenames" "CTRLNAMES 0" "$R39"
NG39="$($BC next-gen 2>&1)"; assert_has "next-gen unmoved by hostile names" "2  # from ledger" "$NG39"

echo
echo "== T40 sink-inventory tripwire: passes on the tree, and FAILS on each kind of planted drift =="
# A control that cannot fail is decoration (an earlier assertion in this very
# suite matched its own failure token and could never go red). So every class
# of drift the tripwire claims to see is planted, in a temp copy, and must trip it.
SC40="$HERE/../scripts/backup_chain.py"; RG40="$HERE/sink_registry.txt"
WS40="$WS_BASE/ws40"; mkdir -p "$WS40"; N40=0
python3 "$HERE/check_sinks.py" >/dev/null 2>&1; check "inventory matches the registry on this tree" 0 $?
mut() { # mut <label> <python appended to the script> <needle expected in the report>
  N40=$((N40+1)); local d="$WS40/m$N40"; mkdir -p "$d/scripts"; cp "$SC40" "$d/scripts/backup_chain.py"
  printf '\n%s\n' "$2" >> "$d/scripts/backup_chain.py"
  local out; out="$(python3 "$HERE/check_sinks.py" --script "$d/scripts/backup_chain.py" --registry "$RG40" 2>&1)"; local rc=$?
  check "$1: tripwire fails" 1 $rc; assert_has "$1: report names the cause" "$3" "$out"
}
regmut() { # regmut <label> <sed expression applied to the registry> <needle>
  N40=$((N40+1)); local r="$WS40/reg$N40.txt"; sed -e "$2" "$RG40" > "$r"
  local out; out="$(python3 "$HERE/check_sinks.py" --registry "$r" 2>&1)"; local rc=$?
  check "$1: tripwire fails" 1 $rc; assert_has "$1: report names the cause" "$3" "$out"
}
mut "planted shutil.copy2 (the 1.2.1 stow bug)" $'def _planted(a, b):\n    shutil.copy2(a, b)' "BANNED sink shutil.copy2"
mut "planted open(path, 'w')" $'def _planted(a):\n    open(a, "w").write("x")' "BANNED sink open(w)"
mut "planted new write sink (os.replace) in an unregistered function" $'def _planted(a, b):\n    os.replace(a, b)' "NEW sink os.replace"
mut "planted network import" 'import socket' "NEW import 'socket'"
mut "planted eval (hides sinks from the scan)" $'def _planted(x):\n    return eval(x)' "dynamic feature eval"
mut "planted getattr(os, ...) indirection" $'def _planted():\n    return getattr(os, "system")' "attribute indirection"
mut "planted importlib" 'import importlib' "importlib imported"
regmut "registry count disagrees with code" 's/^_stage_copy | os.replace | 1 /_stage_copy | os.replace | 2 /' "CHANGED count for _stage_copy | os.replace"
regmut "registry row for a sink that no longer exists" '$a\
ghost_function | os.replace | 1 | staged-write | a reason long enough to pass the length floor' "STALE registry row ghost_function"
regmut "registry reason left as TODO" 's/^\(set_fd_mode | os.fchmod | 1 | staged-meta | \).*/\1TODO/' "needs a real reason"
regmut "registering a banned kind" '$a\
ghost_function | shutil.copy2 | 1 | staged-write | a reason long enough to pass the length floor' "not registrable"
N40=$((N40+1)); d="$WS40/m$N40"; mkdir -p "$d/scripts"; cp "$SC40" "$d/scripts/backup_chain.py"; echo "print(1)" > "$d/scripts/second.py"
out="$(python3 "$HERE/check_sinks.py" --script "$d/scripts/backup_chain.py" --registry "$RG40" 2>&1)"; check "a second script outside the registry: tripwire fails" 1 $?
assert_has "a second script outside the registry: report names the cause" "scripts/ file set changed" "$out"

echo
echo "== T41 the drill is an honest read-back: writes nothing, claims nothing it does not do =="
# Through 1.2.1 the gate said members were verified "in .vault/drill" and the
# function rmtree'd that directory, but never wrote to it: the hash check ran on
# the decoded stream. The claim, and a recursive delete on a parameter, went.
WS41="$WS_BASE/ws41"; mkdir -p "$WS41"; cd "$WS41" || exit 1
echo a > a.txt
$BC init --name t41 --ledger file >/dev/null 2>&1
$BC member add a.txt >/dev/null 2>&1
B41="$($BC build --carries x 2>&1)"; check "build" 0 $?
assert_has "G8 line says nothing was written" "nothing written to disk" "$B41"
case "$B41" in *"verified in "*) bad "G8 still claims verification happened 'in' a directory" ;; *) ok "G8 no longer claims a staging directory" ;; esac
[ ! -e "$WS41/.vault/drill" ] && ok "no .vault/drill directory is created" || bad ".vault/drill still created"
D41="$($BC drill download/t41-g1.tar.gz 2>&1)"; check "standalone drill" 0 $?
mkdir -p "$WS41/precious" && echo keep > "$WS41/precious/file.txt"
K41="$(T41TB="$WS41/download/t41-g1.tar.gz" T41DIR="$WS41/precious" python3 - <<'PYEOF'
import importlib.util, os
spec = importlib.util.spec_from_file_location("bc", os.environ["BCPATH"])
bc = importlib.util.module_from_spec(spec); spec.loader.exec_module(bc)
bc.run_drill(os.environ["T41TB"], os.environ["T41DIR"])
print("INTACT" if os.path.exists(os.path.join(os.environ["T41DIR"], "file.txt")) else "DELETED")
PYEOF
)"
assert_has "run_drill never deletes a directory it is pointed at" "INTACT" "$K41"

echo "== T42 archive modes: 0600 default, --archive-mode verbatim, config form =="
# v1.3.0: archives, receipts and stow copies land owner-only by default; an
# explicit mode is applied verbatim (umask neither widens nor narrows it);
# config archive_mode is the persistent form (v1.3.1, audit T09: config may
# NARROW only — no group/other bits — widening is CLI-only); CLI wins over
# config; exec/setuid bits and non-octal values are refused before anything
# is written.
WS42="$WS_BASE/ws42"; mkdir -p "$WS42"; cd "$WS42" || exit 1
U42="$(umask)"; umask 022   # deterministic: the default-mode assertions below discriminate only under a permissive umask
echo a > a.txt
$BC init --name t42 --ledger file >/dev/null 2>&1
$BC member add a.txt >/dev/null 2>&1
$BC build --carries x >/dev/null 2>&1; check "build (default mode)" 0 $?
A42="$(stat -c %a download/t42-g1.tar.gz)"
[ "$A42" = "600" ] && ok "archive is 0600 by default" || bad "archive mode is $A42, expected 600"
R42="$(stat -c %a download/t42-g1.tar.gz.sha256)"
[ "$R42" = "600" ] && ok "receipt is 0600 by default" || bad "receipt mode is $R42, expected 600"
B42="$($BC build --carries y --archive-mode 644 2>&1)"; check "build --archive-mode 644" 0 $?
A42="$(stat -c %a download/t42-g2.tar.gz)"
[ "$A42" = "644" ] && ok "explicit 644 applied verbatim (umask 022 would also give 644, config proves the path)" || bad "archive mode is $A42, expected 644"
R42="$(stat -c %a download/t42-g2.tar.gz.sha256)"
[ "$R42" = "644" ] && ok "receipt follows archive mode" || bad "receipt mode is $R42, expected 644"
assert_has "G7 line prints the applied mode" "mode 0644" "$B42"
mkdir -p stow42
$BC build --carries z --archive-mode 640 --stow-to "$WS42/stow42" >/dev/null 2>&1
check "build with --stow-to" 0 $?
A42="$(stat -c %a stow42/t42-g3.tar.gz)"
[ "$A42" = "640" ] && ok "stow copy follows archive mode" || bad "stow copy mode is $A42, expected 640"
python3 - <<'PYEOF'
import json
p = ".vault/config.json"
cfg = json.load(open(p))
cfg["archive_mode"] = "400"
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
$BC build --carries w >/dev/null 2>&1; check "build with config archive_mode" 0 $?
A42="$(stat -c %a download/t42-g4.tar.gz)"
[ "$A42" = "400" ] && ok "config archive_mode honored (narrowing)" || bad "archive mode is $A42, expected 400"
$BC build --carries v --archive-mode 600 >/dev/null 2>&1
check "build with CLI override of config" 0 $?
A42="$(stat -c %a download/t42-g5.tar.gz)"
[ "$A42" = "600" ] && ok "CLI --archive-mode overrides config" || bad "archive mode is $A42, expected 600"
E42="$($BC build --carries q --archive-mode 755 2>&1)"; RC42=$?
[ $RC42 -eq 2 ] && ok "exec-bit mode refused (rc 2)" || bad "mode 755 gave rc $RC42, expected 2"
assert_has "refusal names the boundary" "outside 0..0666" "$E42"
E42="$($BC build --carries q --archive-mode xyz 2>&1)"; RC42=$?
[ $RC42 -eq 2 ] && ok "non-octal mode refused (rc 2)" || bad "mode xyz gave rc $RC42, expected 2"
assert_has "refusal names the bad value" "not an octal mode" "$E42"
[ ! -e download/t42-g6.tar.gz ] && ok "refused mode wrote nothing" || bad "refused build left an archive behind"
umask 077
$BC build --carries u --archive-mode 644 >/dev/null 2>&1; check "build 644 under umask 077" 0 $?
A42="$(stat -c %a download/t42-g6.tar.gz)"
[ "$A42" = "644" ] && ok "explicit mode applied verbatim — umask 077 did not narrow it" || bad "archive mode is $A42, expected 644 (verbatim); umask-ANDed semantics would give 600"
umask "$U42"
python3 - <<'PYEOF'
import json
p = ".vault/config.json"
cfg = json.load(open(p))
cfg.pop("archive_mode", None)
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
$BC evict a.txt --stow-to "$WS42/stow42e" >/dev/null 2>&1; check "evict (default mode, config key removed)" 0 $?
EV42="$(ls "$WS42/stow42e"/t42-evict-g*-a.txt.tar.gz 2>/dev/null | head -1)"
[ "$(stat -c %a "$EV42")" = "600" ] && ok "eviction package is 0600 by default" || bad "eviction package mode is $(stat -c %a "$EV42"), expected 600"
mkdir -p r42
$BC restore download/t42-g6.tar.gz --target "$WS42/r42" >/dev/null 2>&1
check "restore for the mode pin" 0 $?
A42="$(stat -c %a "$WS42/r42/a.txt")"
[ "$A42" = "600" ] && ok "restored member is owner-only (staging discipline, true since 1.1 — pinned here first)" || bad "restored member mode is $A42, expected 600"

echo "== T43 archive-mode trust boundary: config may narrow, never widen (T09 round 7, v1.3.1) =="
# 1.3.0 let the persistent config key archive_mode widen artifacts up to 0666.
# ClawHub audit T09 (Warning/Medium, 2026-10-11) called it, correctly: a
# planted .vault/config.json is adversarial input like the rest of config,
# and "visible on the G7 line" is a warning, not consent — the same argument
# that closed 1.0.4's T09 on command execution. Since 1.3.1 the config key
# may only narrow (no group/other bits); widening is the operator's own
# per-invocation --archive-mode, echoed on the G7 line.
echo b43 > b.txt
$BC member add b.txt >/dev/null 2>&1
python3 - <<'PYEOF'
import json
p = ".vault/config.json"
cfg = json.load(open(p))
cfg["archive_mode"] = "666"
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
N43="$($BC next-gen 2>&1 | head -1)"
E43="$($BC build --carries t43 2>&1)"; RC43=$?
[ $RC43 -eq 2 ] && ok "world-readable config mode refused (rc 2)" || bad "config 666 gave rc $RC43, expected 2"
assert_has "refusal names the widening attempt" "grants group/other access" "$E43"
assert_has "refusal states the trust rule" "never widen them" "$E43"
assert_has "refusal names the operator remedy" "--archive-mode" "$E43"
[ ! -e download/t42-g7.tar.gz ] && ok "refused widening wrote nothing" || bad "refused build left an archive behind"
[ "$($BC next-gen 2>&1 | head -1)" = "$N43" ] && ok "refused build consumed no generation" || bad "refused build moved next-gen from [$N43]"
python3 - <<'PYEOF'
import json
p = ".vault/config.json"
cfg = json.load(open(p))
cfg["archive_mode"] = "640"
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
$BC build --carries t43b >/dev/null 2>&1; RC43=$?
[ $RC43 -eq 2 ] && ok "group-readable config mode refused" || bad "config 640 gave rc $RC43, expected 2"
python3 - <<'PYEOF'
import json
p = ".vault/config.json"
cfg = json.load(open(p))
cfg["archive_mode"] = "604"
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
$BC build --carries t43c >/dev/null 2>&1; RC43=$?
[ $RC43 -eq 2 ] && ok "other-readable config mode refused (1.3.0's T42 value)" || bad "config 604 gave rc $RC43, expected 2"
python3 - <<'PYEOF'
import json
p = ".vault/config.json"
cfg = json.load(open(p))
cfg["archive_mode"] = "400"
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
$BC build --carries t43d >/dev/null 2>&1; check "narrowing config mode accepted" 0 $?
A43="$(stat -c %a download/t42-g7.tar.gz)"
[ "$A43" = "400" ] && ok "config narrowing applied verbatim" || bad "archive mode is $A43, expected 400"
$BC build --carries t43e --archive-mode 644 >/dev/null 2>&1; check "CLI widen with hostile config present" 0 $?
A43="$(stat -c %a download/t42-g8.tar.gz)"
[ "$A43" = "644" ] && ok "CLI wins; config not consulted for widening" || bad "archive mode is $A43, expected 644"
python3 - <<'PYEOF'
import json
p = ".vault/config.json"
cfg = json.load(open(p))
cfg["archive_mode"] = "666"
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
E43="$($BC evict b.txt --stow-to "$WS42/stow43" 2>&1)"; RC43=$?
[ $RC43 -eq 2 ] && ok "evict refuses widening config (member stays tracked)" || bad "evict with config 666 gave rc $RC43, expected 2"
python3 - <<'PYEOF'
import json
p = ".vault/config.json"
cfg = json.load(open(p))
cfg.pop("archive_mode", None)
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
$BC evict b.txt --stow-to "$WS42/stow43" >/dev/null 2>&1; check "evict succeeds after config cleaned (member was never untracked)" 0 $?
EV43="$(ls "$WS42/stow43"/t42-evict-g*-b.txt.tar.gz 2>/dev/null | head -1)"
[ "$(stat -c %a "$EV43")" = "600" ] && ok "eviction package is 0600 by default (T43 rerun)" || bad "eviction package mode is $(stat -c %a "$EV43"), expected 600"

echo
echo "== T44 output-dir containment is shared: evict cannot diverge from build (T09 round 8, v1.3.2) =="
# 1.3.1's evict still wrote the eviction package through the pre-round-4
# pattern: outdir = output_abs(cfg); makedirs. A lexically-inside
# output_dir with a planted symlinked component carried the
# credential-bearing package AND its receipt outside the workspace
# (ClawHub audit T09 round 8, Warning, v1.3.1 re-scan; reproduced against
# shipped 1.3.1 bytes before the fix). Since 1.3.2 build and evict call
# ONE shared realpath containment, checked BEFORE makedirs: a refusal
# leaves nothing behind, not even a directory. --output (build) and
# --stow-to/--stow-cmd (evict) stay the per-invocation operator acts.
cfgset44() { # local config setter bound to WS44 (mirrors cfgset/$WS5)
  python3 - "$WS44" "$@" <<'PYEOF'
import json, sys
ws, key, val = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
p = ws + "/.vault/config.json"
cfg = json.load(open(p))
cfg[key] = val
json.dump(cfg, open(p, "w"), indent=2, sort_keys=True)
PYEOF
}
WS44="$WS_BASE/ws44"; mkdir -p "$WS44/st"; cd "$WS44" || exit 1
echo secret44 > secret.txt
$BC init >/dev/null 2>&1
# madd44: idempotent member re-add. On the CURRENT tree every evict below
# refuses and the member stays tracked, so this is a no-op; under mutation
# testing against an older tree an escaped evict UNTRACKS the member, and
# without the re-add every later case would fail as 'not a member' (rc 2)
# instead of showing its true mutation signal.
madd44() { $BC member add secret.txt --critical >/dev/null 2>&1 || true; }
madd44
$BC build --carries 't44 baseline' >/dev/null 2>&1; check "T44 baseline build" 0 $?
EVIL44="$WS_BASE/evil44-out"; mkdir -p "$EVIL44"
ln -s "$EVIL44" "$WS44/link-out"
cfgset44 output_dir '"link-out"'
E44="$($BC evict secret.txt --stow-to "$WS44/st" 2>&1)"; RC44=$?
[ $RC44 -eq 1 ] && ok "symlinked output_dir refused at evict (rc 1, same gate class as build)" || bad "evict with symlinked output_dir gave rc $RC44, expected 1"
assert_has "evict refusal names the resolved escape" "resolves outside" "$E44"
assert_has "evict refusal names the custody remedy" "--stow-to" "$E44"
[ -z "$(ls "$EVIL44" 2>/dev/null)" ] && ok "nothing written through the link (no package, no receipt, no staging)" || bad "eviction package landed outside via symlink: $(ls "$EVIL44" 2>/dev/null)"
$BC member list 2>/dev/null | grep -q secret.txt && ok "refused evict left the member tracked" || bad "member list lost secret.txt after refused evict"
# check-before-makedirs: a fresh subpath under a symlinked parent must not
# even create directories through the link.
madd44
EVIL44B="$WS_BASE/evil44-parent"; mkdir -p "$EVIL44B"
ln -s "$EVIL44B" "$WS44/link-parent"
cfgset44 output_dir '"link-parent/fresh/deep"'
E44="$($BC evict secret.txt --stow-to "$WS44/st" 2>&1)"; RC44=$?
[ $RC44 -eq 1 ] && ok "fresh subpath under symlinked parent refused" || bad "evict through fresh symlinked parent gave rc $RC44, expected 1"
[ ! -e "$EVIL44B/fresh" ] && ok "refusal created no directories through the link" || bad "makedirs ran through the symlink before the gate"
# one helper, two commands: build's refusal for the same hostile config
# carries the same containment prefix but its own remedy.
madd44
cfgset44 output_dir '"link-out"'
E44="$($BC build --carries t44-parity 2>&1)"; RC44=$?
[ $RC44 -eq 1 ] && ok "same hostile config refused at build (rc 1)" || bad "build with symlinked output_dir gave rc $RC44, expected 1"
assert_has "shared containment prefix across commands" "output_dir resolves outside the project root" "$E44"
assert_has "build refusal names its own remedy" "--output" "$E44"
# legitimate in-root output_dir: evict works exactly as before.
madd44
cfgset44 output_dir '"download"'
$BC evict secret.txt --stow-to "$WS44/st" >/dev/null 2>&1; check "in-root output_dir: evict succeeds as before" 0 $?
EV44="$(latest "$WS44/download" ws44-evict-g)"
[ -n "$EV44" ] && ok "eviction package still lands in output_dir: $EV44" || bad "eviction package missing from download/"
[ -z "$(ls "$EVIL44" 2>/dev/null)" ] && ok "external dir still untouched after the clean evict" || bad "clean evict wrote outside anyway"

echo
echo "RESULTS: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
exit 0
