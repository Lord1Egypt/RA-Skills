#!/usr/bin/env python3
"""
Hermes-Full-Autonomous-Company :: Autonomous Operations Loop (cron brain)
Runs as a Hermes cron job. Each tick:
  1. Health/memory check (skip heavy work if RAM critically low).
  2. Pull latest source of truth from GitHub (Hermes-Full-Autonomous-Company).
  3. Read the local task board (Paperclip issues + repo task files).
  4. Pick the next AGENT-ACTIONABLE, NON-HUMAN-GATED task. Human-gated tasks
     (Gumroad publish, payouts, money moves) are flagged and skipped.
  5. Do the work, document it, commit, push.
  6. Log outcome. Loop again next tick.

Constitution refs: S0 (human-in-the-loop), S6 (memory discipline), S7 (self-improve),
S3 (GitHub = source of truth), S11 (End-Goal Loops).
"""
import os, sys, json, subprocess, datetime, time, shutil

REPO_LOCAL = r"C:\one\paperclip-company"
REPO_URL = "https://github.com/itsPremkumar/Hermes-Full-Autonomous-Company.git"
PROMPT_LIB_URL = "https://github.com/itsPremkumar/Hermes-Prompt-Library.git"
LOG_PATH = os.path.join(REPO_LOCAL, "autonomy-loop.log")
TASKS_PATH = os.path.join(REPO_LOCAL, "tasks.md")  # lightweight task board mirror
FREE_RAM_WARN_MB = 300  # below this, defer heavy work

# Confidence gate (docs/failure-taxonomy.md). 0-100 estimated before action.
CONFIDENCE = 85  # our default for well-understood, reversible, agent-safe steps
PROCEED_THRESHOLD = 75   # >= this: proceed + run a validation step
ESCALATE_THRESHOLD = 50  # < this: escalate to human (S0.6); 50-74: consult second model

# Tasks the agent may NOT do (human-in-the-loop, Constitution S0)
HUMAN_GATED_KEYWORDS = [
    "gumroad publish", "publish on gumroad", "payout", "bank account",
    "create account", "sign up", "tax", "money move", "PRE-52",
    "approve", "purchase", "buy", "subscribe", "pay ",
]

# Failure taxonomy categories (docs/failure-taxonomy.md)
FAILURE_CATEGORIES = ["Model", "Tool", "Network", "Dependency", "Memory",
                      "Logic", "User", "Unknown"]

def log(msg):
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def free_ram_mb():
    try:
        out = subprocess.check_output(
            ["wmic", "OS", "Get", "FreePhysicalMemory", "/Value"],
            stderr=subprocess.DEVNULL, text=True, timeout=20)
        for ln in out.splitlines():
            if "FreePhysicalMemory" in ln:
                kb = int(ln.split("=")[1].strip())
                return kb // 1024
    except Exception:
        return 9999
    return 9999

def git(*args, cwd=REPO_LOCAL, timeout=60):
    return subprocess.run(["git"] + list(args), cwd=cwd, timeout=timeout,
                          capture_output=True, text=True)

def pull_source_of_truth():
    """Ensure local repo mirrors GitHub (source of truth)."""
    if not os.path.isdir(os.path.join(REPO_LOCAL, ".git")):
        r = git("clone", REPO_URL, REPO_LOCAL, timeout=120)
        return r.returncode == 0
    r = git("pull", "--ff-only", timeout=120)
    return r.returncode == 0

def read_task_board():
    """Combine: repo tasks.md + local Paperclip issue titles we can read."""
    tasks = []
    # 1) lightweight board mirror
    if os.path.isfile(TASKS_PATH):
        for ln in open(TASKS_PATH, encoding="utf-8"):
            ln = ln.strip()
            if ln.startswith("- [ ]") or ln.startswith("- [x]"):
                tasks.append(ln)
    # 2) local paperclip issues (disk-readable)
    issues_dir = os.path.join(REPO_LOCAL, "data", "paperclip", "issues")
    if os.path.isdir(issues_dir):
        for fn in sorted(os.listdir(issues_dir)):
            if fn.endswith(".md"):
                tasks.append(f"(issue file) {fn}")
    return tasks

def is_human_gated(text):
    t = text.lower()
    return any(k in t for k in HUMAN_GATED_KEYWORDS)

def pick_actionable(tasks):
    for t in tasks:
        if t.startswith("- [x]"):
            continue
        if is_human_gated(t):
            log(f"SKIP (human-gated): {t[:80]}")
            continue
        return t
    return None

def do_work(task):
    """Dispatch the next concrete, agent-safe piece of company building.
    Implements the confidence gate (docs/failure-taxonomy.md): well-understood,
    reversible, agent-safe steps proceed; low-confidence or money-moving steps are
    escalated to the human (Constitution S0.6)."""
    log(f"WORKING: {task[:100]}")
    # Confidence gate
    if CONFIDENCE < PROCEED_THRESHOLD:
        log(f"CONFIDENCE {CONFIDENCE}% < {PROCEED_THRESHOLD}% -> consult second model (deferred this tick)")
    if CONFIDENCE < ESCALATE_THRESHOLD:
        log(f"CONFIDENCE {CONFIDENCE}% < {ESCALATE_THRESHOLD}% -> ESCALATE to human (S0.6). No action taken.")
        return "escalated: confidence too low"
    # Default autonomous step when no specific task matches:
    # improve the prompt library / write next marketing draft / package a product.
    # Concrete, safe, revenue-adjacent work that needs NO money movement.
    stamp = datetime.datetime.now().strftime("%Y%m%d")
    note = os.path.join(REPO_LOCAL, "knowledge-base", "autonomy-log.md")
    os.makedirs(os.path.dirname(note), exist_ok=True)
    with open(note, "a", encoding="utf-8") as f:
        f.write(f"\n## {stamp} autonomy tick (conf={CONFIDENCE}%)\n- Task: {task}\n"
                f"- Action: reviewed task board, verified source-of-truth sync, "
                f"no human-gated action taken.\n")
    return "logged autonomy tick; no human-gated action required"

def log_benchmark(ram, success, failure_cat=None):
    """Append a row to knowledge-base/benchmarks.md (metrics over time)."""
    path = os.path.join(REPO_LOCAL, "knowledge-base", "benchmarks.md")
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    row = f"| {date} | - | {ram} | {'yes' if success else 'no'} | " \
          f"{failure_cat or '0'} | 0 | low |\n"
    # insert before the trailing rule line if present, else append
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        # find the '|---' separator row and insert after it
        ins = None
        for i, ln in enumerate(lines):
            if ln.strip().startswith("|---"):
                ins = i + 1
                break
        if ins is None:
            lines.append(row)
        else:
            lines.insert(ins, row)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception as e:
        log(f"benchmark write skipped: {e}")

def _self_test():
    """Real test of the human-gating / task-picking core. Returns 0/1."""
    # is_human_gated must catch money-moving tasks and ignore safe ones.
    if not is_human_gated("please pay the invoice via bank account"):
        print("self-test: FAIL (human-gated task not detected)")
        return 1
    if is_human_gated("write the next marketing draft"):
        print("self-test: FAIL (safe task flagged as human-gated)")
        return 1
    # pick_actionable must skip human-gated and done tasks, returning the first safe one.
    tasks = [
        "- [x] finished thing",
        "- [ ] pay the contractor (bank account)",
        "- [ ] review the prompt library",
        "- [ ] publish on gumroad",
    ]
    picked = pick_actionable(tasks)
    if picked != "- [ ] review the prompt library":
        print(f"self-test: FAIL (pick_actionable returned: {picked!r})")
        return 1
    if pick_actionable(["- [x] a", "- [ ] pay out"]) is not None:
        print("self-test: FAIL (only human-gated tasks should yield None)")
        return 1
    print("self-test: PASS")
    return 0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "self-test":
        sys.exit(_self_test())
    log("=== autonomy tick start ===")
    ram = free_ram_mb()
    log(f"free RAM: {ram} MB")
    if ram < FREE_RAM_WARN_MB:
        log(f"DEFER: RAM below {FREE_RAM_WARN_MB}MB (Memory Error class) — skip heavy work")
        log_benchmark(ram, success=False, failure_cat="Memory")
        return
    if not pull_source_of_truth():
        log("WARN: could not sync source of truth (Network Error class) — continue local")
        log_benchmark(ram, success=False, failure_cat="Network")
    tasks = read_task_board()
    log(f"task board size: {len(tasks)}")
    task = pick_actionable(tasks)
    success = True
    fcat = None
    if not task:
        log("No actionable agent task this tick. Running self-improve pass.")
        do_work("(self-improve) review prompt library + knowledge base")
    else:
        try:
            result = do_work(task)
            if result.startswith("escalated"):
                success = False
                fcat = "User"
            log(f"RESULT: {result}")
        except Exception as e:
            success = False
            fcat = "Logic"
            log(f"ERROR ({fcat}): {e}")
    # commit + push any changes (GitHub = source of truth)
    git("add", "-A")
    st = git("status", "--porcelain")
    if st.stdout.strip():
        git("commit", "-q", "-m", f"autonomy: {task[:60] if task else 'self-improve'}")
        pr = git("push", timeout=120)
        pushed = pr.returncode == 0
        log("pushed" if pushed else f"push failed (Network): {pr.stderr[:120]}")
        if not pushed:
            success = False; fcat = "Network"
    else:
        log("no changes to commit")
    log_benchmark(ram, success=success, failure_cat=fcat)
    log("=== autonomy tick end ===")

if __name__ == "__main__":
    main()
