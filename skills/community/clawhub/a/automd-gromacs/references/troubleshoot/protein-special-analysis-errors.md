# protein-special-analysis errors

## ERROR: missing `-s` or `-f`

**Cause:** Required structure or trajectory file not provided.

**Fix:**
```bash
protein-special-analysis -s md.tpr -f md.xtc
```

---

## ERROR: `gmx` not found

**Cause:** GROMACS not loaded in current shell.

**Fix:**
```bash
source /usr/local/gromacs/bin/GMXRC
# or activate your conda env with gmx
```

---

## DSSP skipped

**Cause:** `dssp` / `mkdssp` missing.

**Fix:**
```bash
sudo apt-get install dssp
# verify
mkdssp --version
```

**Note:** Script still generates partial report without DSSP.

---

## `gmx do_dssp` failed

**Cause:** Non-protein system, broken topology, or DSSP conversion issue.

**Fix:**
```bash
# check groups
gmx make_ndx -f md.tpr

# try fitted / cleaned trajectory
echo "Backbone Backbone" | gmx trjconv -s md.tpr -f md.xtc -o fit.xtc -fit rot+trans
protein-special-analysis -s md.tpr -f fit.xtc --type dssp,report
```

**Interpretation:** If DSSP fails but RMSD/RMSF are normal, issue is often formatting rather than physics.

---

## `gmx rama` failed

**Cause:** Backbone atoms unavailable, non-protein system, or wrong group.

**Fix:**
```bash
protein-special-analysis -s md.tpr -f md.xtc --backbone-group Backbone
# if system is not protein-dominant, skip dihedral
protein-special-analysis -s md.tpr -f md.xtc --type dssp,helix,report
```

---

## `gmx chi` failed or output sparse

**Cause:** Side-chain chi only exists for specific residues; Gly/Ala-rich systems naturally have less signal.

**Fix:**
```bash
protein-special-analysis -s md.tpr -f md.xtc --protein-group Protein
```

**Interpretation:** Sparse chi data is not automatically an error.

---

## `gmx helix` failed

**Cause:** Selected region is not helical enough or residues are discontinuous.

**Fix:**
```bash
# focus on a known helix region
protein-special-analysis -s md.tpr -f md.xtc --helix-group Protein --helix-residues 10-35
```

**Practical rule:** Helix tools work best on one continuous helix or a clean helical subset.

---

## `gmx helixorient` failed

**Cause:** Helix axis cannot be defined robustly.

**Fix:**
```bash
# use a stable helix core, not termini
protein-special-analysis -s md.tpr -f md.xtc --helix-residues 14-31
```

**Interpretation:** Flexible termini often break orientation estimates before the helix truly unfolds.

---

## `gmx wheel` failed

**Cause:** Wheel analysis needs a clear helix-focused selection; whole-protein input is often too broad.

**Fix:**
```bash
protein-special-analysis -s md.tpr -f md.xtc --helix-residues 45-67
```

**Tip:** Use wheel mainly for amphipathic helices and membrane/interface helices.

---

## `gmx saltbr` failed

**Cause:** Wrong charged groups, no oppositely charged partners, or cutoff unsuitable.

**Fix:**
```bash
protein-special-analysis -s md.tpr -f md.xtc --salt-group1 Protein --salt-group2 Protein --salt-cutoff 0.40
```

**Auto-fix:** Script clamps cutoff into 0.35-0.45 nm when user input is unrealistic.

**Interpretation:** A low salt-bridge count is acceptable if the fold is hydrophobically stabilized.

---

## `gmx bundle` failed

**Cause:** Bundle analysis requires ordered helices and meaningful helix count.

**Fix:**
```bash
protein-special-analysis -s md.tpr -f md.xtc --bundle-nhelices 2
protein-special-analysis -s md.tpr -f md.xtc --bundle-group Protein --bundle-nhelices 4
```

**Rule of thumb:** If the system only has one helix, skip bundle.

---

## Key residue summary looks too generic

**Cause:** Script prioritizes robust signals (RMSF + reused DSSP/chi summaries) over fragile assumptions.

**Fix:**
```bash
# tighten time window around transition
protein-special-analysis -s md.tpr -f md.xtc -b 50000 -e 80000 --type dssp,dihedral,helix,keyres,report
```

**Interpretation:** Transition-focused windows usually produce sharper residue ranking than full-trajectory averages.

---

## Report generated but some sections say unavailable

**Cause:** Script degrades gracefully when one analysis module fails.

**Fix:**
```bash
# inspect module logs
find protein-special-analysis -name "*.log" -maxdepth 2
```

**Recommendation:** Keep the partial report; it often already shows which module is the bottleneck.

---

## Typical interpretation checklist

- **DSSP loss + Ramachandran outlier increase:** likely backbone rearrangement.
- **Helix tilt rise without DSSP collapse:** likely functional breathing, gating, or reorientation.
- **Salt bridge loss before RMSF increase:** electrostatic lock breaks first.
- **Bundle distance increase with one helix moving:** local helix disengagement, not global unfolding.
- **High RMSF but secondary structure retained:** mobile structured segment, often regulatory.

---

## Recommended integrated workflow

```bash
# 1. Basic stability baseline
bash scripts/basic/analysis.sh --input-tpr md.tpr --input-trj md.xtc --output analysis

# 2. Global advanced structure analysis
bash scripts/analysis/advanced-analysis.sh -s md.tpr -f md.xtc --type pca,cluster,fel

# 3. Protein-specific mechanistic analysis
bash scripts/analysis/protein-special-analysis.sh -s md.tpr -f md.xtc --type dssp,dihedral,helix,saltbridge,bundle,keyres,report
```

That combination is the intended handoff path for protein systems.
