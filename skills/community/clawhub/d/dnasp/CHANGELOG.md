# Changelog

All notable changes to the `dnasp` skill package are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

Answers the ClawBio maintainer review of the DnaSP pull request; ported from the ClawBio tree.

### Added
- `SKILL.md`: a "Known Differences from DnaSP 6.12.03" section with the four unresolved VCF
  single-site Pi and R2 values and the differences of setting, and a "Version History" section
  listing every result-changing definition since 0.5.0.
- `tests/fixtures/inputs/README.md` and `tests/fixtures/validation5/README.md`: provenance of every
  test input and of the DnaSP captures and transcriptions; the three DnaSP 6.12.03 sliding-window
  output files cited by the window tests.

### Changed
- `tests/test_historical_concordance.py` renamed `tests/test_historical_comparisons.py`. Besides
  pinning the recorded Python values, it now checks each current value against DnaSP's printed
  figure at DnaSP's precision, with the seven rows that differ from DnaSP listed with their reason.
- Comments explain the two intentional `pass` branches flagged by CodeQL; an unused variable in
  `test_cli_genetic_code_flag` is replaced by an assertion.

### Fixed
- VCF runs split by CHROM: a CHROM named `result.json` or `reproducibility` no longer takes the
  root envelope's path or receives the root reproducibility bundle; it gets its own `chrom_`
  directory.

## [0.6.1] - 2026-10-03

Answers the ClawBio maintainer's review of the 0.6.0 pull request.

### Changed

- Coalescent P-values are reported only where the simulated null varies, per statistic
  and per conditioning: R2 is constant with two sequences, Fu's Fs is constant with two
  sequences given S but not given theta, and Tajima's D has no variance below four
  sequences. A constant null is reported with no P-value and a note naming the
  statistic, instead of the P of 1 such a test would always give.
- The observed value and a replicate sum R2's terms in the same order, so a genuine tie
  is bitwise equal and counts in both tails.
- SKILL.md, the report and the reference say that the null has no recombination and name
  recombination as a cause of a low Fu's Fs P-value.
- A run warns before a very large simulation starts, and the report says a seed replays
  only on the same Python.
- The module header says the statistics were implemented from the primary literature and
  checked against the DnaSP 6 source, of which the package contains none.

## [0.6.0] - 2026-09-17

### Added

- Coalescent-simulation P-values for Tajima's D (two-tailed), Ramos-Onsins and
  Rozas R2 and Fu's Fs (lower tail) over the whole region: `--n-sim`,
  `--sim-given S|theta` and `--sim-seed`. The null is the Kingman coalescent with
  constant size, infinite sites and no recombination, conditioned by default on the
  observed number of segregating sites. Opt-in: without `--n-sim` no simulation
  runs and no statistic changes. Two sequences give R2 and Fu's Fs P-values; only
  Tajima's D needs three. Each P-value is (b + 1)/(N + 1) for b of N valid
  replicates at least as extreme, so none is zero (Phipson and Smyth 2010); the
  counts b are stored, from which DnaSP's proportion b/N follows.

### Changed

- The report no longer turns Tajima's D or R2 into a significance claim from a
  fixed threshold; they are described as not assessed unless `--n-sim` supplies a
  P-value. No statistic changes.
- The version history moved from SKILL.md to `docs/version_history.md`.

## [0.5.3] - 2026-09-16

### Fixed

- Every input in the skill metadata now names the command-line flag it maps to
  (`cli_flag`). Without it an agent reading only the registered metadata had to
  guess, and two independent models turned `window_size` into the non-existent
  `--window-size`. Guarded by `tests/test_skill_contract.py`.

### Unchanged

- Numerical behaviour is identical to 0.5.2, the version compared with
  DnaSP 6.12.03. No statistic changes.

## [0.5.2] - 2026-09-15

Round-5 DnaSP 6.12.03 validation fixes; version bumped so that the three skill trees (ClawBio,
the canonical DnaSP mirror and this package) no longer share 0.5.1 with different algorithms.

### Changed (validation round 5, DnaSP 6.12.03, 2026-09-15; ported from the ClawBio tree)
- Sliding windows now follow DnaSP's placement (`CODIGO2.vb`, `CONTROLE.vb`): the next start
  advances by the step and is capped at the alignment length, the window end is capped there too,
  the first window reaching the end terminates the loop (so the final truncated window is kept),
  and each window carries DnaSP's `Midpoint` (the ceil(net/2)-th gap-free column, or the window
  start when the window has none) in `results.tsv`, `summary.json`, the report and the figure. VCF
  window plots label their axis as retained variant index, not bp.
- Mismatch distribution: observed variance of k is the unbiased variance over sequence pairs and
  the C.V. carries Sokal & Rohlf's (1 + 1/4n) correction, as in `PairwiseDiff.vb`
  (rp49 40.7780 / 0.3987; DmelOSRegion 7298.4971 / 1.3168).
- Codon usage exports a named per-sequence ENC (`codon.per_sequence_enc`, outgroup excluded,
  undefined as null) alongside the weighted summary ENC.
- Every run writes `summary.json` (module summaries; LD pair grids stay in `ld_pairs.tsv`) and
  `result.json` (the structured envelope ClawBio's runner reads, written by `_repro_writers.py`
  with the same keys as the shared ClawBio writer); both declared in `SKILL.md`. Multi-CHROM VCF
  runs add a root envelope summarising the per-CHROM runs; file and CHROM names are sanitised
  before they appear in chat lines. Console output tolerates non-UTF-8 terminals (Windows cp1252) and
  result files are written as UTF-8.
- LD: at tied allele frequencies the first sequence's allele is the reference, as in DnaSP's
  `calculo_mas_freq1`, so the sign of D matches DnaSP's grids (|D|, |D'| and r^2 unchanged).
- Tests: `test_validation5_regressions.py` (round-5 capture regressions, including the
  Segregating-sites setting of Fu and Li's tests, the LD sign rule and the result.json envelope) and `test_windows_encoding.py`; fixtures for
  the round-5 inputs and the transcribed per-sequence ENC tables.

### Fixed
- The filename sanitisation test no longer creates a file name that Windows rejects (tab,
  asterisk, angle brackets); the adversarial string is checked directly on `_display_label`.

## [0.5.1] - unreleased

Not yet published to ClawHub or Hermes: awaiting a validated DnaSP release.

### Source
- Packaged from the development copy of skill version 0.5.1, whose validation against DnaSP 6 is
  in progress. No statistic, parser or report formula was changed by the packaging.

### Changed for packaging
- Reproducibility writers: `_repro_writers.py`, written for this package, provides
  `write_commands_sh`, `write_environment_yml` and `write_checksums`. `dnasp.py` loads it by file
  path under a private module name (`_load_repro_writers`), so an unrelated module named
  `reproducibility`, whether already imported or earlier on `sys.path`, can never supply the
  writers, and nothing is added to `sys.path` or `sys.modules`. Checksum labels always use forward
  slashes.
- Reports name the tool as DnaSP-Python in the header, the Methods section and the disclaimer.
- `LICENSE.txt` ships inside `skills/dnasp/` as well as at the repository root, so every installed
  copy carries it.
- `SKILL.md`: top-level `version` and `compatibility`, a `metadata.hermes` block, the OpenClaw
  emoji and homepage, commands written relative to the skill directory, and an Integration section
  for calling `dnasp.py` directly. Dependencies list matplotlib only: the skill never imports
  numpy, pandas or OpenTelemetry.
- `environment.yml` and the new `requirements.txt` match those dependencies.

### Added
- `tests/test_standalone_packaging.py`: writer loading under a conflicting `sys.modules` entry and
  a conflicting earlier `sys.path` entry, bundle formats (checksums verify, LF endings, executable
  `commands.sh` that replays, `environment.yml` contents), the licence inside the skill directory,
  report wording, and imports limited to the standard library, matplotlib and the skill's own
  modules.
- `.github/workflows/tests.yml` (repository root): the test suite, a `--demo` run, checksum
  verification and a bash replay of `commands.sh` on Ubuntu and Windows with Python 3.10 and
  3.13, plus an Ubuntu job without matplotlib. The Windows jobs run in Python's UTF-8 mode
  (`PYTHONUTF8=1`); see Known issues.
- `.github/workflows/publish-clawhub.yml` and `.github/scripts/` (repository root): publish to
  ClawHub at exactly the version recorded in the skill, instead of ClawHub's automatic numbering
  (1.0.0 for a new skill, then the next patch). The workflow checks that the four version fields
  agree, requires a dated `CHANGELOG.md` entry for a real publish, refuses a version that is not
  greater than ClawHub's latest, and succeeds only when ClawHub lists the version as published and
  lets it be downloaded, waiting up to ten minutes for security checks. A re-run never uploads identical content again and reports
  whether the version became public or was blocked. Covered by `.github/scripts/test_clawhub_scripts.py`,
  which runs in CI.

### Known issues
- Windows without UTF-8 mode: when stdout is redirected (as when an agent captures it), Python uses
  the ANSI code page and the console summary's non-ASCII symbols raise `UnicodeEncodeError`, so
  the run exits 1. `results.tsv` and `ld_pairs.tsv` are also written without an explicit encoding,
  and several tests read reports with the platform default. Workaround: `PYTHONUTF8=1`. A fix is
  ready and arrives with the next refresh.

### Removed
- A test of an external command-line dispatcher that is not part of this package.
