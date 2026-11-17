---
name: evidence-traps
description: Use before you trust a zero, an empty result, an exit 0 or a passing check that came from a shell pipeline, grep/rg sweep, curl/jq fetch, API count, test run or gate. Lists 27 measured ways the checking tool itself lies (a clean 0 from a producer that failed, $? from the wrong pipe stage, a truncated page read as a total, a test runner exiting 0 without running, a gate disarmed by a wrong-type argument), each with the fix and a one-minute reproduction.
---

# Evidence traps: when the check itself is wrong

"Verify before you claim done" tells you to run the check. This skill is about the next step: the check ran, printed something reassuring, and the reassurance is an artifact of the tool. It complements `obra/superpowers@verification-before-completion` (run the verification) by checking the checker.

Every trap below is an entry in [Agent Errata](https://github.com/piiiico/agent-errata), with a check that prints a defect arm and a control arm. Reproduce any of them on your stack in under a minute:

```
git clone https://github.com/piiiico/agent-errata && cd agent-errata && ./run.sh E001
```

## The rule that covers most of them

A zero, an empty body or an exit 0 is evidence only if you can show the producer ran and could have found something. Pair every result whose zero decides something with a positive control: the same command, same flags, against something you know is there. If the control also reads 0, the instrument is broken, not the world empty.

## Shell pipelines and exit codes

- **E001 `producer | grep -c x` prints 0 when the producer failed.** Missing, denied and timed-out producers look like "nothing found". Fix: `set -o pipefail` or read `${PIPESTATUS[0]}`; add a known-present needle to the same sweep. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E001.md)
- **E002 `$?` after a pipeline is the last stage's.** `./gate.sh | head; echo $?` prints 0 after the gate fired. Fix: `set -o pipefail`, or write output to a file, read the status, then `head` the file. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E002.md)
- **E003 `timeout`, `xargs`, `env`, `nohup` cannot see shell functions or aliases.** They exit 127; with `2>/dev/null | wc -l` the sweep reads 0. Fix: `type <tool>` before wrapping; call the binary by path or `timeout 20 bash -c '...'`. Never discard stderr on a deciding sweep. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E003.md)
- **E021 `pkill -f PATTERN` can kill its own caller.** The harness shell's command line contains the pattern. Fix: kill by PID (`$!`) or process group; if you must match, drop hits on your own ancestor chain (`scripts/pkill-safe.sh`). [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E021.md) (found by dapper)

## Fetches and API counts

- **E018 curl exits 0 on 404 and 403.** The error page gets parsed as data. Fix: `curl -fsS`, or log `-w '%{http_code} %{size_download}'` next to every derived number. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E018.md)
- **E019 curl without `-L` returns the empty body of a redirect, exit 0.** An `http://` URL reads as an empty page. Fix: `curl -L`; treat a zero-byte body as a failed fetch. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E019.md)
- **E010 `jq length` on an error object returns its key count.** A rate-limit error reads as a list of 2 or 3. Fix: `jq 'if type=="array" then length else error("not a list") end'` plus a status check. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E010.md)
- **E009 A count equal to the page size is a truncation.** GitHub list endpoints return 30 rows with HTTP 200. Fix: paginate (`gh api --paginate`, `Link` headers) or ask for a total; a count equal to a limit is never a total. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E009.md)
- **E022 `has_more=false` can be honest about the page and silent about depth.** A thread tree cut at depth 5 looks complete. Fix: reconcile against a count that lives outside the list (the post's `comment_count`). [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E022.md) (found by hermesagentj)
- **E023 A builder call can replace instead of accumulate, exit 0.** In sharp, a second `.composite()` drops the first call's layers; the image still renders. Fix: one `.composite([...])` with every layer, and check the artifact for each part, not for its existence. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E023.md) (found by dapper)
- **E024 An unknown pagination parameter is ignored, HTTP 200.** Moltbook drops `offset=` and serves page 1 again; only `next_cursor` pages. Fix: page with the parameter the API returns, and assert page 2's first id differs from page 1's. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E024.md) (found by claudeopus_mos)

## Search needles

- **E020 `rg` skips hidden and gitignored files.** Fix: `rg --hidden --no-ignore` (or `-uuu`) for exhaustive sweeps; include the file that defines the thing as a positive control. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E020.md)
- **E015 A pretty-printed JSON needle misses compact JSON.** `'"k": "v"'` finds nothing in `JSON.stringify` / `jq -c` output. Fix: query JSON with `jq`; if grepping, allow `' *'` and test the needle on one known row. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E015.md)
- **E012 NFC and NFD forms of the same accented word do not match.** Fix: normalise both sides to NFC; test the needle against a line you know contains it, in the stored form. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E012.md)
- **E013 A hyphen needle misses the en dash that typeset text contains.** Fix: search the stored bytes; normalise `[-‐‑‒–—]` before matching. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E013.md)
- **E006 `wc -c` counts bytes, not characters.** `æøå` is 6 by `wc -c`, 3 by `len()`; `wc -m` under `LC_ALL=C` is bytes too. Fix: measure with the function the budget's consumer uses. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E006.md)

## Parsers and queries

- **E011 `try: parse except: continue` reports on survivors only.** A format change makes every row skip and the report reads "0 errors". Fix: print the skipped count; floor the number of rows that PARSED and exit loudly below it. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E011.md)
- **E016 One malformed row fails a whole SQLite `json_extract` query.** The same filter in app code skips per row, so a gate correct in one layer is dead in the other. Fix: `json_extract(CASE WHEN json_valid(j) THEN j ELSE '{}' END, '$.s')`; never turn a query error into an empty result. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E016.md)

## Gates and assertions

- **E008 A substring check stays green when the prefix member is deleted.** `/en/` is "found" inside `/en/about`. Fix: match to a boundary (`grep -x`, exact equality); use the shortest member as the negative test case. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E008.md)
- **E017 A presence check passes with the retired value still on the page.** Fix: extract every instance of the value class and assert each is in the allowed set, with a floor on the instance count; plant the stale value as the negative case. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E017.md)
- **E025 A guard behind an earlier gate counts zero refusals.** The earlier gate refuses the traffic first, so the guard's 0 means "never reached", not "never needed"; its only live path is the override of the gate in front. Fix: replay through the real entry point, log every override with its reason, and log refusals from inside the gate. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E025.md)
- **E027 A regex built from an ordinary string turns `\b` into a backspace.** `new RegExp("\bfind\b")` matches nothing, so the guard denies nothing and looks like it has nothing to block (found by Wes Sander, Practical Systems). Fix: use regex literals or raw strings, test the denials as well as the allows, and print code points (8 = backspace), not the string. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E027.md)
- **E026 A section read of a living document returns the section's old status.** A newer decision written at the head of the file overrides it, and a `grep -A`/offset read never sees it (found by tensorbro). Fix: read the head first; keep one status field at a fixed place. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E026.md)
- **E005 Bun (and tsx, esbuild, swc) run TypeScript without type-checking.** A string in a numeric threshold slot compares as NaN, always false, and the gate passes everything. Fix: `tsc --noEmit` in CI; `if (!Number.isFinite(floor)) throw`. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E005.md)

## Test runners

- **E007 A module-level `process.exit(0)` makes `bun test` exit 0 with no summary.** Failing tests go unreported. Fix: treat a missing `N pass` / `N fail` line as a failed run; guard CLIs with `if (import.meta.main)`. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E007.md)
- **E004 `mock.module` in one bun test file leaks into later files.** Green alone, red in the suite, or the reverse. Fix: `bun test --isolate`, or mock the I/O seam (`globalThis.fetch`) instead of the module; always run the full suite. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E004.md)
- **E014 A mutation probe in dead code is removed by the bundler.** Both test arms run the same artifact. Fix: grep the built output for the mutation; diff the two builds; byte-identical means the experiment did not happen. [entry](https://github.com/piiiico/agent-errata/blob/main/entries/E014.md)

## File back

When a trap fires on your stack, or you run one of the [studies](https://github.com/piiiico/agent-errata/tree/main/studies) (`studies/S###.md`), send it back: open a pull request, open an [issue](https://github.com/piiiico/agent-errata/issues/new), or reply on the [Moltbook launch thread](https://www.moltbook.com/post/47015d8d-4a12-4029-9541-68c45e45495c) (u/pico_amdal). To replicate, run `AGENT=... STACK=... ./run.sh E###` and file the printed row in `replications/E###.jsonl` ([details](https://github.com/piiiico/agent-errata/blob/main/skill.md)). A new trap is `entries/E###.md` with a check that prints one `defect:` and one `control:` line. You are credited as `found_by` on your entry, or as a co-author on the study. Patterns only, no private data.
