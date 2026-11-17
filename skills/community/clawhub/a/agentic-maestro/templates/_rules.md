Working rules (binding; identical for every executor, so keep this block first and unchanged):
- Logging: never pipe a command into `tail`. Write its output to a UNIQUE log inside your working directory, never a shared `/tmp` path, and keep the exit code: `LOG=.agent-logs/<step>.log; mkdir -p .agent-logs; cmd > "$LOG" 2>&1; rc=$?; tail -30 "$LOG"; echo "exit=$rc"`. Keep the full log; the exit code decides, never the tail.
- Reading: grep first, then read files in ranges. You may read the files in your map and their imports, callers, types and tests; no open-ended exploration. The brief already quotes the conventions and the pattern you need.
- Testing: run targeted tests after a group of related edits, not after each edit. Run the gate commands once at the end, exactly as given, one at a time (they may be wrapped by a lock script; never strip or replace the wrapper).
- Looping: if the same error repeats 3 times, or one command waits more than 10 minutes, stop and report instead of retrying.
- Scope: stay inside your working directory and touch only the files in your map; a change needed anywhere else is a blocked question.
- Tests are evidence: never weaken, skip, exempt or delete an existing test; if one must change, say why in the report.
- Safety: never read secrets, env or credential files; never make paid or subscription calls; never run commands marked user-only.
- Decisions: anything the brief does not decide is a blocked question, never a guess. Finish everything the question does not block, then report it.
