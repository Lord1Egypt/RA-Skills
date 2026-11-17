# Adaptive-Trial Monte-Carlo Simulator

Module: `--test adaptive_simulate` in the main CLI. **In the published skill, the
authoritative engine is an inlined pure base-R function library** `ADAPTIVE_SIM_R`,
maintained in `adapters/local-r/local_r_backend.py` (no extra R packages), running **server-side
on coze**. The CLI shows the coze request envelope in SAFE PREVIEW and computes via
coze (no local R/shell). **Dev / offline:** the equivalent local-R path writes the
inlined engine to a temp `.R` file, `source()`s it and calls `run_adaptive_sim()`
(SAFE PREVIEW, `--yes` to run). A legacy pure-Python module
`adapters/local-r/legacy/adaptive_simulator.py` is retained for offline dev/testing.
Ported from the ClawHub skill `adaptive-trial-simulator` (aipoch-ai) and
re-implemented to fit ct-samplesize.

> **No standalone `.R` file is shipped in the published skill.** The R engine lives
> inline in `adapters/local-r/local_r_backend.py` as `ADAPTIVE_SIM_R` (excluded from the publish
> package; synced to coze). To drive the engine from R yourself, run the CLI with
> `--show-code` (or `-y`) and copy the printed R code into R.

## Run the R engine via CLI

This is the normal path (no manual `source()` needed):

```bash
# default = SAFE PREVIEW (shows the generated R code that sources the inlined engine)
python scripts/samplesize_power.py --test adaptive_simulate --sim_design group_sequential   --effect_size 0.3 --sim_n 200 --interim_looks 3 --spending_function obrien_fleming   --alpha 0.025 --n_simulations 20000 --sim_seed 42

# add -y / --yes to execute and compute power / type I error
python scripts/samplesize_power.py --test adaptive_simulate --sim_design group_sequential   --effect_size 0.3 --sim_n 200 --interim_looks 3 --spending_function obrien_fleming   --alpha 0.025 --n_simulations 20000 --sim_seed 42 -y
```

## Drive the engine directly from R

There is no standalone `.R` file to `source()`. To run the engine from R,
replicate what the CLI does: run `python scripts/samplesize_power.py --test
adaptive_simulate ... --show-code`, copy the printed R code (it contains the full
`ADAPTIVE_SIM_R` definition plus the `run_adaptive_sim(...)` call) into R, and run
it. The pasted code is self-contained — base R only, no extra packages.

## When to use

Use this **simulation** engine when you want to *validate* an adaptive or
group-sequential design by Monte-Carlo (empirical power, empirical type I error,
expected sample size, early-stop probabilities) rather than solve a closed-form
sample size. For **analytic** group-sequential / adaptive sample size (rpact /
gsDesign), use `--test group_sequential` or `--test adaptive` instead — they are
complementary.

> **coze is the primary compute path** in the published skill: the CLI shows the
> coze request envelope (SAFE PREVIEW) and computes via coze (server-side R, base R
> only, no extra packages). The optional local-R dev backend (`adapters/local-r/`) behaves
> like v3.x — R code is generated and shown, re-run with `--yes` to execute locally.
> If neither coze nor a local R install is available, the legacy pure-Python engine
> (`adapters/local-r/legacy/adaptive_simulator.py`) still gives a result offline.

## Capabilities (6)

|#|Capability|How|
|---|---|---|
|1|Design Simulation|Monte-Carlo of the chosen design under H1 & H0|
|2|Sample-Size Re-estimation|promising-zone + Cui-Hung-Wang weighted statistic|
|3|Early Stopping|efficacy + non-binding futility boundaries|
|4|Type I Error Control|alpha-spending calibration, verified under H0|
|5|Multi-Arm|drop-the-loser interim selection (Dunnett/Bonferroni)|
|6|Power Optimization|grid search for min per-arm N reaching target power|

## Designs & spending

- `--sim_design`: `group_sequential` | `adaptive_reestimate` | `drop_the_loser`
- `--spending_function`: `obrien_fleming` (conservative early) | `pocock`
  (aggressive early) | `power_family` (shape via `--rho`, e.g. 3)

Boundaries are computed by an exact Armitage-McPherson-Rowe recursion on the
Brownian (B-value) scale, reproducing gsDesign-style OBF/Pocock boundaries.

## Key flags

|Flag|Meaning|Default|
|---|---|---|
|`--sim_design`|design type|group_sequential|
|`--effect_size`|Cohen's d (single-arm designs)|0.3|
|`--effect_sizes`|per-arm d list for drop_the_loser, e.g. `0.2,0.35,0.5`|—|
|`--sim_n`|per-arm sample size|100|
|`--interim_looks`|looks incl. final|2|
|`--spending_function`|alpha spending|obrien_fleming|
|`--rho`|power_family shape|3.0|
|`--futility` / `--beta`|add non-binding futility|off / 0.2|
|`--reestimate_method`|SSR method|promising_zone|
|`--interim_fraction` `--target_cp` `--max_inflation`|SSR controls|0.5 / 0.9 / 2.0|
|`--n_arms` `--selection_fraction` `--correction`|multi-arm controls|3 / 0.5 / dunnett|
|`--optimize` `--n_min` `--n_max` `--power`|power search|off / 10 / 1000 / 0.9|
|`--n_simulations`|MC replications|10000|
|`--alpha`|one-sided alpha (from common flag)|0.05|
|`--visualize` `--sim_output` `--sim_seed`|PNG / JSON / seed|off / — / —|

> Note: `--alpha` is the shared common flag (default 0.05). For a one-sided
> 0.025 design pass `--alpha 0.025`.

## Examples

```bash
# Default = SAFE PREVIEW (shows the generated R code). Append -y / --yes to
# execute the R code and compute the result. If R is absent, the Python
# fallback runs automatically (also without --yes).

# 1) Group-sequential, 3 looks, OBF spending, one-sided 0.025  (preview)
python samplesize_power.py --test adaptive_simulate --sim_design group_sequential \
  --effect_size 0.3 --sim_n 200 --interim_looks 3 --spending_function obrien_fleming \
  --alpha 0.025 --n_simulations 20000 --sim_seed 42

# 1b) same, but execute (-y) -> runs the R code and prints power / type I error
python samplesize_power.py --test adaptive_simulate --sim_design group_sequential \
  --effect_size 0.3 --sim_n 200 --interim_looks 3 --spending_function obrien_fleming \
  --alpha 0.025 --n_simulations 20000 --sim_seed 42 -y

# 2) With non-binding futility (Pocock spending)
python samplesize_power.py --test adaptive_simulate --sim_design group_sequential \
  --effect_size 0.3 --sim_n 200 --interim_looks 3 --spending_function pocock \
  --futility --beta 0.2 --alpha 0.025 -y

# 3) Sample-size re-estimation (promising zone, CHW statistic)
python samplesize_power.py --test adaptive_simulate --sim_design adaptive_reestimate \
  --effect_size 0.3 --sim_n 200 --interim_fraction 0.5 --target_cp 0.9 \
  --max_inflation 2.0 --alpha 0.025 -y

# 4) Multi-arm drop-the-loser (3 arms) with Dunnett-style adjustment
python samplesize_power.py --test adaptive_simulate --sim_design drop_the_loser \
  --effect_sizes "0.2,0.35,0.5" --sim_n 150 --selection_fraction 0.5 \
  --correction dunnett --alpha 0.025 -y

# 5) Power optimization: min per-arm N reaching 90% power, + PNG
python samplesize_power.py --test adaptive_simulate --optimize \
  --effect_size 0.3 --power 0.9 --interim_looks 2 --alpha 0.025 \
  --n_min 150 --n_max 400 --visualize -y

# Standalone Python fallback (only needed when R is unavailable):
python adaptive_simulator.py --design group_sequential --effect-size 0.3 \
  --sample-size 200 --interim-looks 3 --spending-function obrien_fleming --alpha 0.025
```

## Output

**R engine (primary):** a human-readable report (power, type I error, expected /
max sample size, early-stop rates, Z boundaries, etc.) plus an optional JSON file
when `--sim_output <path>` is given.

**Python fallback (no R):** the same quantities as a JSON block with (design-dependent)
`power`, `type_i_error`, `expected_sample_size` (total & per-arm), `max_sample_size`,
`early_stop_rate {efficacy, futility}` (GS), `prob_sample_size_increase` (SSR),
`power_correct_selection` / `prob_correct_selection` (multi-arm), and a `design_config`
echoing all inputs plus the computed Z boundaries.

## Validation

At α=0.025 the empirical type I error is calibrated to ≈0.025 across all
designs (checked with 20k-40k replications): GS 3-look OBF → power 0.846 / T1E
0.0251; SSR promising-zone → power 0.890 / T1E 0.0251 / 28% inflation prob;
drop-the-loser 3-arm → power_any 0.959 / correct-selection 0.693 / T1E 0.0235.

## Statistical notes

- Effect size is Cohen's d; final non-centrality is `d*sqrt(n/2)` per two-arm Z.
- SSR uses the Cui-Hung-Wang (1999) weighted statistic `Zw = w1*Z1 + w2*Z2`
  with pre-planned weights, preserving type I under data-dependent re-estimation.
- Futility is non-binding beta-spending under H1 (efficacy boundaries computed
  independently).
