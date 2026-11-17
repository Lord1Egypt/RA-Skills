"""Slot lock for gate.sh on systems without flock(1) (macOS): python3 -I gate_lock.py <lock-dir> <slots> <max-wait> <command...>

Acquires one of <slots> kernel locks (fcntl.flock) in <lock-dir>, runs the command as a child in its
own session while holding it, forwards INT/TERM/HUP to the child's process group and exits with the
child's status (128+signal when killed). Exit 75 when no slot frees up within <max-wait> seconds; 69
when a slot file is unsafe (symlink, not a regular file) or cannot be opened.
"""
import errno, fcntl, os, signal, stat, subprocess, sys, time

lock_dir = sys.argv[1]
slots = int(sys.argv[2])
max_wait = int(sys.argv[3])
cmd = sys.argv[4:]


def fail(code, message):
    sys.stderr.write("gate.sh: " + message + "\n")
    sys.exit(code)


# Every slot is checked up front, not only the one this run happens to take: a symlink here means
# the lock directory has been tampered with, and opening it would write to a foreign file. A
# non-regular file matters too (a FIFO would block the open, a directory cannot be opened).
for n in range(1, slots + 1):
    path = os.path.join(lock_dir, "slot.%d" % n)
    try:
        st = os.lstat(path)
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            continue
        fail(69, "cannot inspect slot %d under %s: %s; refusing to run unlocked"
             % (n, lock_dir, exc.strerror))
    if stat.S_ISLNK(st.st_mode):
        fail(69, "slot %d under %s is a symlink; refusing to run unlocked" % (n, lock_dir))
    if not stat.S_ISREG(st.st_mode):
        fail(69, "slot %d under %s is not a regular file; refusing to run unlocked"
             % (n, lock_dir))

# Acquire a slot: non-blocking flock on each slot per round, 2 s between rounds.
lock_fd = None
deadline = time.monotonic() + max_wait
while lock_fd is None:
    for n in range(1, slots + 1):
        path = os.path.join(lock_dir, "slot.%d" % n)
        # O_NOFOLLOW: a symlinked slot would send the lock (and the append) to a file we do not own.
        try:
            fd = os.open(path,
                         os.O_CREAT | os.O_APPEND | os.O_WRONLY | os.O_NOFOLLOW,
                         0o600)
        except OSError as exc:
            if exc.errno == errno.ELOOP:
                fail(69, "slot %d under %s is a symlink; refusing to run unlocked"
                     % (n, lock_dir))
            fail(69, "cannot use slot %d under %s: %s; refusing to run unlocked"
                 % (n, lock_dir, exc.strerror))
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(fd)
            continue
        lock_fd = fd
        break
    if lock_fd is None:
        if time.monotonic() >= deadline:
            fail(75, "timed out after %ds waiting for a gate slot (GATE_SLOTS=%d, lock=%s)"
                 % (max_wait, slots, lock_dir))
        time.sleep(2)

child = None
pending = []


def forward(signum, frame):
    if child is None:
        pending.append(signum)
        return
    try:
        os.killpg(child.pid, signum)
    except OSError:
        pass


for forwarded in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(forwarded, forward)

try:
    os.nice(5)
except OSError:
    pass

try:
    child = subprocess.Popen(cmd, start_new_session=True)
except OSError as exc:
    fail(127, "%s: %s" % (cmd[0], exc.strerror or exc))

for signum in pending:
    try:
        os.killpg(child.pid, signum)
    except OSError:
        pass

rc = child.wait()
os.close(lock_fd)
if rc < 0:
    sys.exit(128 - rc)
sys.exit(rc)
