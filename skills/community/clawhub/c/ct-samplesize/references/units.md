# Atomic Task Units — ct-samplesize

> Registry of ct-samplesize capability atomic units, for agent / `ct-pipeline` chaining reference (BASE.md §6). Each unit carries 5 fields: **Input · Output · Depends-on · AI autonomy · Compose interface**.
>
> This skill belongs to ② Design (Tier A, local · no retrieval). Units are chained by the agent / user; no hardcoded dispatch to other skills.

## U1 — Forward Sample Size (target power → n)

- **Input**: `--test <type>` (required) + effect-size / rate / HR params + `--power` (target, default) + optional `--side` / `--sd` / design flags.
- **Output**: Required sample size `n` (per-arm or total), with reproducible R code shown in SAFE PREVIEW.
- **Depends on**: none (entry unit).
- **AI autonomy**: 🟨 semi-auto (confirm params; coze compute fires on the natural-language trigger — no `--yes` needed; legacy `--yes` is local-R dev only).
- **Compose interface**: → U2 (reverse check) / U3 (curve) / U6 (report).

## U2 — Reverse Power (fixed n → achieved power)

- **Input**: `--test <type>` + effect params + `--nobs N` (switches to reverse mode; mutually exclusive with `--power`).
- **Output**: Achieved power for the given `n`; native reverse (`pwr.*`, `PowerTOST`, `rpact`) where available, otherwise analytic inverse via non-centrality.
- **Depends on**: none (entry unit); often paired with U1.
- **AI autonomy**: 🟨 semi-auto.
- **Compose interface**: → U1 (forward) / U6 (report).

## U3 — Curve Mode (Power / Sample-size curves)

- **Input**: `--test <type>` + `--n_seq` (sample-size sequence) or `--power_seq` (power sequence) + optional `--plot_effects` (overlay) + `--out` (PNG path).
- **Output**: PNG curve (base R graphics, no ggplot2) + data table; 22 supported test types.
- **Depends on**: U1 (reuses the same validated formulas).
- **AI autonomy**: 🟨 semi-auto.
- **Compose interface**: → U6 (report).

## U4 — Adaptive Monte-Carlo Simulator

- **Input**: `--test adaptive_simulate` + design (`group_sequential` / `adaptive_reestimate` / `drop_the_loser`) + spending function + optional `--futility` / `--optimize` / `--visualize` + `--n_sim`.
- **Output**: Empirical power, type-I error, expected sample size, early-stop probabilities. Primary engine = inlined pure-base-R `ADAPTIVE_SIM_R` (no extra packages), running **server-side on coze** in the published skill. Dev/offline legacy: `adapters/local-r/legacy/adaptive_simulator.py` (pure Python, not shipped).
- **Depends on**: none (entry unit). Published skill requires coze (no local fallback).
- **AI autonomy**: 🟨 semi-auto.
- **Compose interface**: → U6 (report) / feeds design validation.

## U5 — R Package Management (coze-side, v5)

- **Input**: none — all R packages run **server-side on coze** (image pre-installed). The published skill never installs R locally; the legacy `--install-all-packages` / `--run-install` flags were **removed in v5.0.2**.
- **Output**: coze R engine serves all 65 test types; no local install step.
- **Depends on**: none.
- **AI autonomy**: ⬜ none (no local install capability in the published skill; dev backend `adapters/local-r/` uses printed `install.packages()` snippets instead).
- **Compose interface**: prerequisite handled by coze deployment (r_packages.txt).

## U6 — Report Generation

- **Input**: Any computed result (U1–U4) + optional `--out` path.
- **Output**: Curve PNG + data table + on-request reproducible R code block (SAFE PREVIEW).
- **Depends on**: U1 / U2 / U3 / U4.
- **AI autonomy**: ⬛ auto (formatting only; no new computation).
- **Compose interface**: terminal unit → user / downstream document (e.g. `ct-protocol` skeleton, CSR).
