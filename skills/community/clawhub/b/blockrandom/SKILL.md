---
name: blockrandom
description: Generate seeded permuted-block randomization lists for small clinical trials — stratified, reproducible byte-for-byte from a recorded seed, with a full allocation list, a sealed enrolment list, an audit log and a ready-to-paste methods paragraph. A seed is required and is never invented by the tool. Use when asked to create a randomization or allocation list, set up permuted-block randomization with strata, or regenerate a trial allocation schedule from its seed. Not for eGFR calculation (use egfr-batch), lab-unit conversion (use labunits), growth z-scores (use growthz), or de-identification checks (use safeharbor-check).
license: MIT
compatibility: Requires Python 3.10+, standard library only, no dependencies. Installing needs network access to GitHub; the tool itself runs fully offline.
---

# blockrandom

## What this tool does

blockrandom generates permuted-block randomization lists for small clinical trials: from stated
arms, allocation ratio, block sizes, strata and a seed, it writes the full allocation list, a sealed
enrolment list, per-stratum files, an audit log and a methods paragraph. Balance is exact at every
completed block's end, and the same seed and parameters regenerate the lists byte-for-byte. Without
a seed it refuses: an unseeded list cannot be reproduced (ICH E9 requires a reproducible schedule).

## Install

```bash
pip install git+https://github.com/RakTikoo/blockrandom
```

This provides the `blockrandom` command; verify an install with `blockrandom check` (block balance
and byte-for-byte regeneration, PASS/FAIL).

## Run

```bash
blockrandom generate --trial-name "Example trial" --arms Treatment,Control --ratio 1:1 --blocks 4,6,8 --n-per-stratum 40 --strata "site=North,South" --seed-file seed.txt --out-dir trial-lists
```

- `--arms` (at least two, all different), `--ratio` (one whole number per arm; `2:1` and three-arm
  ratios work), `--blocks` and `--n-per-stratum` are required and never guessed. Every block size
  must be a multiple of the ratio sum; give at least two sizes for a real trial.
- `--strata` takes `name=level,level` chunks separated by semicolons (omit for one unstratified
  list); each stratum gets its own sequence of `--n-per-stratum` allocations.
- Exactly one of `--seed TEXT` or `--seed-file FILE` is required. The seed itself is never written
  anywhere; only its SHA-256 hash is recorded. Use a long, random seed.

## Reading the results

Exit code `0` means the lists were generated. The summary restates the design and the seed's
SHA-256. Outputs: `allocation.csv` (full list with block details), `sealed.csv` (enrolment copy: no
block structure, no seed material), `per_stratum/`, `audit.log` (every parameter, output hashes,
Python version) and `methods.txt`. A final block truncated to reach a stratum's length does not hold
the ratio exactly — flagged `block_complete=false`, named in the audit log and mentioned in the
methods paragraph, never hidden.

Exit code `2` means the tool refused and wrote nothing — no seed (or both seed sources), a ratio
that does not match the arms, a block size that cannot hold the ratio, duplicate arms, malformed
strata — one clean explanation, never a traceback.

## Limits

- **Research / educational tool. Not a medical device.** blockrandom only generates allocation
  lists, a standard trial-design artefact. It gives no diagnosis, staging, or dose or treatment
  advice, and does not decide whether randomization, a ratio, or stratification is appropriate for
  any trial. Verify any list before clinical use, and have the design reviewed under your trial's
  protocol and governance.
- A list is not a trial design: caps on strata, allocations and block sizes exist, but the tool
  will generate a badly designed list exactly as specified. Too many strata for the sample size is a
  common, uncaught design error.
- Allocation concealment is a process, not a file format: the sealed list removes the block
  structure, but concealment also depends on who holds which file and how enrolment is run. Keep the
  full list and audit log away from anyone enrolling participants.
- Permuted blocks are predictable at a block's end if the block size is known or guessed; random
  block sizes reduce this, they do not eliminate it, and a single block size leaves it fully in
  place (the methods paragraph says so).
- The seed's hash protects the seed only if the seed is long and random: a short or guessable seed
  can be brute-forced from the hash, and the whole list predicted. Treat the audit log as
  confidential for a real trial.
- Reproducibility rests on CPython's guarantee for `random.Random.random()`; the audit log records
  the exact Python version used — archive it with the list and re-verify before relying on a
  reproduction under a different interpreter.
- No blinding, no enrolment, no participant data: it takes no participant input and produces no
  medical output. Correctness is property-based (balance, reproducibility, sealed contents); there
  is no published reference list to diff against.
