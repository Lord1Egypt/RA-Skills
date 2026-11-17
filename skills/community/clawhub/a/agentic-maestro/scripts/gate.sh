#!/bin/bash
# Machine-wide gate lock: at most $GATE_SLOTS (default 2) heavy check commands at once across all
# lanes. Usage: gate.sh <command...>.
#   GATE_SLOTS    number of slots (positive integer, base 10; '08' is 8; default 2)
#   GATE_LOCK_DIR lock directory (default ${TMPDIR:-/tmp}/agentic-maestro-gate-$(id -u), created
#                 0700 and verified: real directory, owned by us, no group/other access)
#   GATE_MAX_WAIT max seconds to wait for a slot (positive integer, default 3600; on timeout exit 75)
#
# The lock is a KERNEL lock on one file per slot ($GATE_LOCK_DIR/slot.<n>), so a stale lock cannot
# exist: when the holder dies the operating system releases it. Acquisition is non-blocking with
# flock(1) when it exists (Linux util-linux); otherwise scripts/gate_lock.py (python3 -I) acquires
# the slot itself with fcntl.flock(LOCK_EX|LOCK_NB). Each round tries every slot and then sleeps 2 s.
# The command runs as a child in its own process group (its own session) while the lock stays held;
# INT/TERM/HUP are forwarded to that group, the lock is kept until the child exits, and the child's
# exit code is propagated (128+signal if it was killed by a signal). There is NO unlocked fallback:
# exit 69 if there is no lock mechanism or the lock directory cannot be created or written, or if
# the lock directory or a slot file is not safe (symlink, foreign owner, group/other access).
SLOTS=${GATE_SLOTS:-2}
LOCK_DIR=${GATE_LOCK_DIR:-${TMPDIR:-/tmp}/agentic-maestro-gate-$(id -u)}
MAX_WAIT=${GATE_MAX_WAIT:-3600}

case "$SLOTS" in
  '' | *[!0-9]*)
    echo "gate.sh: GATE_SLOTS must be a positive integer (got '$SLOTS')" >&2
    exit 64
    ;;
esac
SLOTS=$((10#$SLOTS))
if [ "$SLOTS" -lt 1 ]; then
  echo "gate.sh: GATE_SLOTS must be a positive integer (got '$SLOTS')" >&2
  exit 64
fi

case "$MAX_WAIT" in
  '' | *[!0-9]*)
    echo "gate.sh: GATE_MAX_WAIT must be a positive integer (got '$MAX_WAIT')" >&2
    exit 64
    ;;
esac
MAX_WAIT=$((10#$MAX_WAIT))
if [ "$MAX_WAIT" -lt 1 ]; then
  echo "gate.sh: GATE_MAX_WAIT must be a positive integer (got '$MAX_WAIT')" >&2
  exit 64
fi

if [ "$#" -lt 1 ]; then
  echo "gate.sh: no command given; usage: gate.sh <command...>" >&2
  exit 64
fi

if command -v flock >/dev/null; then
  MECH=flock
elif command -v python3 >/dev/null; then
  MECH=python3
else
  echo "gate.sh: neither 'flock' nor 'python3' is available; refusing to run unlocked" >&2
  exit 69
fi

if ! mkdir -p -m 700 "$LOCK_DIR"; then
  echo "gate.sh: cannot create lock directory '$LOCK_DIR'; refusing to run unlocked" >&2
  exit 69
fi

# The lock directory sits in a shared temp location, so it must not be redirectable: a symlink
# would let another user point the gate at their own directory, and group/other access would let
# them read or replace slot files. Verify instead of repairing (chmod would hide a bad directory).
dir_problem=
if [ -L "$LOCK_DIR" ] || [ ! -d "$LOCK_DIR" ]; then
  dir_problem="it is not a real directory"
elif [ ! -O "$LOCK_DIR" ]; then
  dir_problem="it is not owned by the current user"
else
  # GNU stat first, then BSD stat; both print the permission bits as octal digits.
  dir_mode=$(stat -c %a "$LOCK_DIR" 2>/dev/null || stat -f %Lp "$LOCK_DIR" 2>/dev/null)
  case "$dir_mode" in
    '' | *[!0-7]*) dir_problem="its mode cannot be determined" ;;
    *)
      if [ "${dir_mode#"${dir_mode%??}"}" != 00 ]; then
        dir_problem="its mode $dir_mode allows group or other access"
      fi
      ;;
  esac
fi
if [ -n "$dir_problem" ]; then
  echo "gate.sh: lock directory '$LOCK_DIR' is not safe: $dir_problem (need a real directory owned by you with mode 0700); refusing to run unlocked" >&2
  exit 69
fi

probe="$LOCK_DIR/.probe.$$"
# The probe is the only step allowed to silence stderr.
if ! ( : >"$probe" ) 2>/dev/null; then
  echo "gate.sh: lock directory '$LOCK_DIR' is not writable; refusing to run unlocked" >&2
  exit 69
fi
rm -f "$probe"

if [ "$MECH" = python3 ]; then
  # gate_lock.py: acquires a slot, then runs the command as its child in a new session, forwards
  # INT/TERM/HUP to the child's process group, keeps the lock fd until the child exits, and exits
  # with the child's status (128+signal when killed). MAX_WAIT expiry exits 75.
  exec python3 -I "$(cd "$(dirname "$0")" && pwd)/gate_lock.py" "$LOCK_DIR" "$SLOTS" "$MAX_WAIT" "$@"
fi

LOCK_FD=

# try_slot <n>: 0 acquired, 1 busy, 2 error (SLOT_PROBLEM says why). On success sets LOCK_FD.
try_slot() {
  slot="$LOCK_DIR/slot.$1"
  LOCK_FD=
  SLOT_PROBLEM=
  # A symlink at a slot path would redirect the lock, and the append below, to a file we do not own;
  # anything but a regular file (a FIFO) could block the append instead of failing.
  if [ -L "$slot" ]; then
    SLOT_PROBLEM="slot.$1 is a symlink"
    return 2
  fi
  if [ -e "$slot" ] && [ ! -f "$slot" ]; then
    SLOT_PROBLEM="slot.$1 is not a regular file"
    return 2
  fi
  # Writable-file test before opening on fd 9; the wrapper's stderr stays untouched afterwards.
  if ! ( : >>"$slot" ) 2>/dev/null; then
    SLOT_PROBLEM="slot.$1 is not writable"
    return 2
  fi
  # Append (never truncate): an existing slot file must keep its contents.
  exec 9>>"$slot" || { SLOT_PROBLEM="slot.$1 cannot be opened"; return 2; }
  if flock -n 9; then
    LOCK_FD=9
    return 0
  fi
  exec 9>&-
  return 1
}

# Every slot is checked up front, not only the one this run happens to take: a slot file this run
# never reaches could still be handed to a later round, and a symlink means the directory is not
# ours to trust. try_slot re-checks before opening, so this is for the slots we skip.
s=1
while [ "$s" -le "$SLOTS" ]; do
  slot="$LOCK_DIR/slot.$s"
  if [ -L "$slot" ]; then
    echo "gate.sh: slot $s under '$LOCK_DIR' is a symlink; refusing to run unlocked" >&2
    exit 69
  fi
  if [ -e "$slot" ] && [ ! -f "$slot" ]; then
    echo "gate.sh: slot $s under '$LOCK_DIR' is not a regular file; refusing to run unlocked" >&2
    exit 69
  fi
  s=$((s + 1))
done

acquired=0
deadline=$(( $(date +%s) + MAX_WAIT ))
while [ "$acquired" = 0 ]; do
  s=1
  while [ "$s" -le "$SLOTS" ]; do
    try_slot "$s"; r=$?
    if [ "$r" = 0 ]; then acquired=1; break; fi
    if [ "$r" = 2 ]; then
      echo "gate.sh: cannot use slot $s under '$LOCK_DIR' ($SLOT_PROBLEM); refusing to run unlocked" >&2
      exit 69
    fi
    s=$((s + 1))
  done
  [ "$acquired" = 1 ] && break
  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "gate.sh: timed out after ${MAX_WAIT}s waiting for a gate slot (GATE_SLOTS=$SLOTS, lock=$LOCK_DIR)" >&2
    exit 75
  fi
  sleep 2
done

release() {
  if [ -n "$LOCK_FD" ]; then
    exec 9>&-
    LOCK_FD=
  fi
}
trap 'release' EXIT

forward() { kill -"$1" -- -"$child" 2>/dev/null || kill -"$1" "$child" 2>/dev/null; }
trap 'forward TERM' TERM
trap 'forward INT' INT
trap 'forward HUP' HUP

# Run the command as a child in its own process group; the lock stays held until it exits.
set -m
nice -n 5 "$@" 9>&- &
child=$!
set +m

wait "$child"; rc=$?
while kill -0 "$child" 2>/dev/null; do
  wait "$child"; rc=$?
done
release
trap - EXIT
exit $rc
