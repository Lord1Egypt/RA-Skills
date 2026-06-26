# Scattering Analysis - Troubleshooting

## ERROR-001: `gmx` not found

**Symptom**
```bash
[ERROR] ERROR-001: gmx not found for SAXS calculation
```

**Cause**
- GROMACS not installed or not in `PATH`

**Fix**
```bash
which gmx
gmx --version
export PATH="/path/to/gromacs/bin:$PATH"
```

If the system has no GROMACS scattering tool, use existing curve input instead:
```bash
bash scripts/analysis/scattering-analysis.sh \
  --curve calc_saxs.dat --exp exp_saxs.dat --mode compare
```

---

## ERROR-002: `gmx sans` / `gmx scattering` unavailable

**Symptom**
```bash
[ERROR] ERROR-002: gmx sans/scattering not available; provide --sans existing_curve.dat
```

**Cause**
- Current GROMACS build does not expose `gmx sans` or `gmx scattering`

**Fix**
1. Check available commands:
```bash
gmx help commands | grep -E 'sans|scattering|saxs'
```
2. If only SAXS is available, compute SAXS separately and provide SANS as external data.
3. For experiment-facing work, import reduced SANS data directly:
```bash
bash scripts/analysis/scattering-analysis.sh \
  --sans sans_reduced.dat --exp exp_sans.dat --mode all
```

---

## ERROR-003: missing simulated curve for comparison

**Symptom**
```bash
[ERROR] ERROR-003: missing simulated curve for comparison
```

**Cause**
- `--curve` not provided and no calculation step produced a curve

**Fix**
```bash
bash scripts/analysis/scattering-analysis.sh \
  --curve sim_curve.dat --exp exp_curve.dat --mode compare
```

Or run calculation mode first:
```bash
bash scripts/analysis/scattering-analysis.sh -s md.tpr -f md.xtc --exp exp_curve.dat --mode all
```

---

## ERROR-004: missing experimental curve for comparison

**Symptom**
```bash
[ERROR] ERROR-004: missing experimental curve for comparison
```

**Cause**
- `--exp` file not supplied in compare mode

**Fix**
Use an experiment file with at least two columns:
```text
q  I(q)  error(optional)
```

Example:
```bash
bash scripts/analysis/scattering-analysis.sh \
  --curve calc_saxs.xvg --exp beamline_processed.dat --mode compare
```

---

## ERROR-005: no curve available for interpretation

**Symptom**
```bash
[ERROR] ERROR-005: no curve available for interpretation
```

**Cause**
- Neither `--curve`, `--exp`, `--sans`, nor calculation output exists

**Fix**
Provide at least one curve file:
```bash
bash scripts/analysis/scattering-analysis.sh --curve calc_saxs.dat --mode interpret
```

---

## Python says `no numeric rows found`

**Cause**
- Input contains headers only, or delimiter/content is not numeric

**Fix**
Clean the curve first:
```bash
grep -v '^[@#]' raw_curve.xvg > clean_curve.dat
awk 'NF>=2 {print $1, $2, (NF>=3?$3:"nan")}' clean_curve.dat | head
```

Expected format:
```text
0.05  152.4  3.1
0.06  149.0  2.9
```

---

## Comparison fails with `insufficient q overlap`

**Cause**
- Simulation and experiment use different q domains or units

**Fix**
1. Confirm both are in `1/nm`.
2. Convert `1/A` to `1/nm` if needed:
```bash
awk '{print $1*10, $2, (NF>=3?$3:"nan")}' exp_in_A.dat > exp_in_nm.dat
```
3. Restrict both datasets to the common q-range.

Practical guidance:
- Compare only after masking beamstop / bad low-q points.
- Do not extrapolate far beyond the shared q window.

---

## Guinier interpretation looks unreasonable

**Symptoms**
- Very large `Rg`
- Poor `R^2`
- `qRg > 1.3`

**Cause**
- Aggregation at low q
- Wrong units
- Low-q window too wide
- Negative/near-zero intensities after subtraction

**Fix**
1. Inspect the lowest-q points for upturns.
2. Ensure q units are `1/nm`.
3. Trim the fit window to lower q.
4. Re-check buffer subtraction and concentration dependence.

Rule of thumb:
- Use Guinier only when `qRg < 1.3`.
- If low-q upturn exists, report it rather than forcing a fit.

---

## Kratky interpretation suggests disorder but sample should be folded

**Cause**
- Under-normalized curve
- Ensemble heterogeneity
- Flexible tails dominating the signal
- Hydration/solvent mismatch in simulation

**Fix**
- Inspect `q^2 I(q)` plot together with the raw curve.
- Compare multiple replicas or cluster-wise SAXS.
- For experiment comparison, state whether disagreement is low-q or high-q dominated.

---

## No figure is generated

**Cause**
- `python3` or `matplotlib` missing

**Fix**
Install plotting stack:
```bash
python3 -c "import matplotlib"
pip3 install matplotlib
```

The workflow still produces TSV/JSON/Markdown without plotting.

---

## Recommended experiment-facing workflow

```bash
# 1. Generate or import simulation curve
bash scripts/analysis/scattering-analysis.sh \
  -s md.tpr -f md.xtc --exp exp_saxs.dat --mode all

# 2. Inspect report
less scattering-analysis/SCATTERING_REPORT.md

# 3. Make publication-ready figures
automd-viz --type data --input scattering-analysis/export/ --style nature
```

## Data preparation checklist

- Same q unit on both datasets (`1/nm` preferred)
- Experimental columns are `q I error`
- Low-q aggregation / interparticle effects checked
- SAXS buffer subtraction documented
- SANS contrast factor and D2O/H2O fraction recorded
- Comparison restricted to shared q-range
