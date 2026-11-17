# ct-samplesize Operation SOP

> Agent: `ct-samplesize`
> Version: v4.0.1
> See `SKILL.md` for the canonical definition.

## 1. Purpose

- Covers sample-size & power calculation for clinical-trial practitioners.
- Supports 49+ test types via natural-language prompts; computes power / sample
  size / effect size for t-test, ROC (AUC), Poisson, RCT, SSR, and more.

## 2. Environment

- **coze R service (default / production):** the skill sends trial-design params to
  `CTSS_COZE_ENDPOINT` and gets results + optional figures back. No local R needed.
  For a no-network demo, set `CTSS_COZE_MOCK=1`. **v5: no local compute fallback** —
  coze unreachable → error + config guidance.
- **Python 3.8+**: stdlib only, drives the CLI / orchestration (no third-party compute
  deps; the v5 local pure-Python fallback was removed).
- **R 4.x (dev / optional, NOT in published skill):** only the local-R backend
  (`adapters/local-r/`, `CTSS_BACKEND=local-r`) needs R. Detected by `find_rscript` (which
  locates `Rscript`); search order: `PATH` → `C:\Tools\R-4.5.1\bin\x64\Rscript.exe`
  → `C:\Program Files\R\R-4.5.1\bin\x64\Rscript.exe` → `/usr/local/bin/Rscript`,
  `/usr/bin/Rscript`. If none found, emit `error.rscript_not_found`.
- **R packages (coze-side):** `stats`, `pwr`, `rpact`, plus base R — all run
  server-side on coze; nothing to install locally in the published skill.
- Inline R engines: `.R` logic lives in `adapters/local-r/local_r_backend.py` (`I18N_R`,
  `ADAPTIVE_SIM_R`); synced to coze. The CLI shows the coze request envelope in
  SAFE PREVIEW and computes via coze.
- Install helpers (dev only, removed from published CLI in v5.0.2): R packages run server-side on coze; the legacy `--install-all-packages` / `--run-install` flags exist only in the dev backend (`adapters/local-r/`, not shipped) — use the printed `install.packages()` snippet instead.

## 3. Agent invocation

### 3.1 Agent entry

The agent reads `SKILL.md` and runs the CLI with `--test`. Default is a
**SAFE PREVIEW (dry-run)**; on coze the compute is fired by the natural-language trigger, **not** by `--yes` (the legacy `--yes` flag applies only to the optional local-R dev backend).

### 3.2 CLI shape

```bash
python scripts/samplesize_power.py --test <test type> [params] [--dry-run | --yes | --show-code]
```

- `--dry-run` (default) prints the coze request envelope (or R source for the
  local-R dev backend) without sending/executing.
- `--yes` sends the request to coze and computes (accepted but not required for
  coze, which is a stateless compute service); for the optional local-R dev
  backend it is required to run R locally.
- `--show-code` prints the coze request JSON (and the R source on request).

## 4. Security model

- **dry-run by default**: the coze request envelope (or R source for the local-R
  dev backend) is shown but nothing is sent/executed.
- allowlist: every user string that could reach server-side R is validated against
  a strict allowlist — prevents injection / RCE.
- The published skill never runs R or a shell locally; the optional local-R dev
  backend runs `subprocess.run([rscript, '--vanilla', tmp])` with no shell, behind
  `--yes`.

## 5. Common flags

|Flag|Used for|Default|
|------|------|
|`--test`|`ttest_ind`, `roc`, `poisson`, `cluster`, `adaptive_simulate`, `gsd_*`|—|
|`--alpha`|significance level|0.05|
|`--power`|target power (alternative to `--nobs`)|—|
|`--nobs`|sample size (alternative to `--power`)|—|
|`--effect`|effect size|—|
|`--sd`|standard deviation (t-tests)|—|
|`--side`|`one` or `two`|`two`|
|`--p1` / `--p2`|proportions (two-sample)|—|
|`--sim_design` `--effect_size` `--sim_n` `--interim_looks` `--spending_function` `--n_simulations` `--sim_seed` `--sim_output` `--visualize`|adaptive-simulator controls|—|

## 6. Examples

### 6.1 t-test power → n

```bash
python scripts/samplesize_power.py --test ttest_ind --side one --sd 0.8 --effect 0.5 --power 0.9 --yes
```

Output: `n per group: 45` (Cohen's d = 0.625).

### 6.2 ROC n → power

```bash
python scripts/samplesize_power.py --test roc --auc0 0.6 --auc1 0.8 --nobs 200 --alpha 0.05 --yes
```

Output: `Achieved power: 0.9931`.

### 6.3 Adaptive simulation

```bash
python scripts/samplesize_power.py --test adaptive_simulate \
  --sim_design group_sequential --effect_size 0.3 --sim_n 100 \
  --interim_looks 2 --spending_function obrien_fleming --alpha 0.025 \
  --n_simulations 2000 --sim_seed 42 --yes
```

Reports empirical power, type I error, expected N, efficacy Z bounds, and
early-stop rates. Use `--sim_output results.json` and `--visualize` for artifacts.

## 7. Notes

1. In the published skill, R math runs server-side on coze; `CTSS_FORCE_R=1`
   prefers coze-R (else local-R dev backend), `CTSS_RETURN_R_CODE=1` returns the
   full R source + result.
2. The optional local-R dev backend labels results `label.cohens_d` / `n per group`
   under `--yes`.
3. `--visualize` / `--plot_effects` / `--n_seq` render charts (PNG from coze,
   SVG/HTML figures written to `CTSS_OUTPUT_DIR`).
4. `--sim_output` writes a JSON result file.
5. `--show-code` shows the coze request JSON (and the embedded R source on request).

## 8. Troubleshooting

|Symptom|Cause|Fix|
|------|------|------|
|R `unexpected symbol in "_qt"`|old code used `._qt`|use `._qt`; fixed in v3.7.1+ (local-R dev backend)|
|ROC `NameError: name 'ss_roc' is not defined`|Python path issue|fixed in v3.7.1+ (R path)|
|`error.rscript_not_found`|Rscript missing (local-R dev backend)|install R or set `RSCRIPT_PATH` / `find_rscript`|
|`pwr` / `rpact` missing|package not installed (local-R dev backend)|run `install.packages("rpact")` etc. (legacy `--install-all-packages` removed in v5.0.2)|
|coze endpoint not configured|`CTSS_COZE_ENDPOINT` unset|set `CTSS_COZE_ENDPOINT` (real) or `CTSS_COZE_MOCK=1` (demo)|
|coze unreachable (no local fallback in v5)|test requires coze|configure coze (`CTSS_COZE_ENDPOINT` / `CTSS_COZE_MOCK=1`); dev-only alternative: `adapters/local-r/` + `CTSS_BACKEND=local-r`|
|locale shows zh|OS language is zh/CN|expected; output follows OS locale|

## 9. Maintenance

- In the published skill, R logic lives server-side on coze (synced from
  `adapters/local-r/local_r_backend.py` + `adapters/local-r/r_templates/`), not in standalone `.R` files.
- The optional local-R dev backend runs the code under `--yes` after a SAFE PREVIEW;
  the v3.7.1 fix renamed `._qt` to `._qt` consistently (historical).
