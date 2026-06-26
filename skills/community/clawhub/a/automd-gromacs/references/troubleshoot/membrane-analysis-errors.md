# membrane-analysis errors

## ERROR: File not found

**Cause:** `-s` / `-f` / `-n` path is wrong.

**Fix:**
```bash
ls md.tpr md.xtc index.ndx
membrane-analysis -s md.tpr -f md.xtc -n index.ndx
```

---

## Order parameter missing or empty

**Cause:** `gmx order` needs a valid lipid tail group; default `sn1/sn2` may not exist.

**Fix:**
```bash
# Check groups first
printf "q\n" | gmx make_ndx -f md.tpr

# Use actual tail groups from your index
membrane-analysis -s md.tpr -f md.xtc --type order --tail-g1 C1A --tail-g2 C1B -n lipids.ndx
```

**Notes:**
- `gmx order` is most robust when each group is a chemically consistent tail definition.
- For mixed membranes, prepare per-lipid tail groups if you want interpretable comparisons.

---

## Thickness estimate looks too small or too large

**Cause:** Trajectory is not centered / PBC-clean, or density peaks are not symmetric.

**Fix:**
```bash
# Use the built-in centered workflow
membrane-analysis -s md.tpr -f md.xtc --type thickness --center

# Or preprocess manually
printf "Membrane\nMembrane\n" | gmx trjconv -s md.tpr -f md.xtc -o centered.xtc -pbc mol -center
membrane-analysis -s md.tpr -f centered.xtc --type thickness
```

**Best practice:**
- For publication values, use headgroup-specific atoms (for example phosphate groups per leaflet), not total lipid density only.

---

## Density profile is noisy

**Cause:** Too few frames, bins too fine, or membrane is still drifting.

**Fix:**
```bash
# Increase averaging and reduce noise
membrane-analysis -s md.tpr -f md.xtc --type density --center --bins 100 --skip 5

# Analyze only equilibrated window
membrane-analysis -s md.tpr -f md.xtc --type density -b 50000 -e 200000 --center
```

**Rule of thumb:**
- Analyze the final 50-80% of the production trajectory.
- Smaller `--bins` gives smoother profiles.

---

## `gmx densmap` fails

**Cause:** Old GROMACS build, unsupported options, or selection/group issue.

**Fix:**
```bash
# Check command availability
gmx help densmap

# Use a simpler target group
membrane-analysis -s md.tpr -f md.xtc --type densmap --lipid Membrane --grid 80 --center
```

**If still failing:**
- Keep density + composition outputs and skip densmap for this environment.
- Upgrade to a newer GROMACS build if membrane map generation is essential.

---

## `gmx sorient` or `gmx densorder` fails

**Cause:** Group definition is incompatible, axis choice is wrong, or the tool is not available in the current build.

**Fix:**
```bash
# Standard bilayer: XY plane, Z normal
membrane-analysis -s md.tpr -f md.xtc --type orientation --axis z --center

# Check group names
printf "q\n" | gmx make_ndx -f md.tpr
```

**Interpretation note:**
- Use `sorient` mainly for solvent orientation near the interface.
- Use `densorder` for orientational ordering combined with spatial density.

---

## Cholesterol / component distribution looks wrong

**Cause:** Residue name mismatch (`CHOL`, `CLR`, `ERG`, etc.) or the target is not present in the index/topology.

**Fix:**
```bash
# Search residue naming in topology/coordinate files
grep -n "CHOL\|CLR\|ERG\|POPC\|POPE" topol.top md.gro

# Run with the actual residue name
membrane-analysis -s md.tpr -f md.xtc --type composition --component CLR --center
```

**Tip:**
- Always confirm the residue naming used by CHARMM-GUI / Martini / custom topologies.

---

## Protein density appears away from membrane center

**Cause:** Peripheral protein, tilted protein, or membrane center drift.

**Fix:**
```bash
membrane-analysis -s md.tpr -f md.xtc --type density --protein Protein --center
```

**Interpretation:**
- A transmembrane protein should usually contribute near the membrane center along the bilayer normal.
- Off-center protein density may reflect true peripheral binding, not necessarily an error.

---

## Mixed membrane order comparison is hard to interpret

**Cause:** Different lipid species are pooled into one membrane group.

**Fix:**
```bash
# Build separate tail groups per lipid species
# Then run order analysis on each species-specific index
membrane-analysis -s md.tpr -f md.xtc --type order --tail-g1 POPC_sn1 --tail-g2 POPC_sn2 -n species.ndx
```

**Recommendation:**
- Compare order parameter, densmap, and composition together for mixed systems.

---

## Script runs but report is mostly "skipped"

**Cause:** `gmx` is unavailable in the current shell, or a mock/test environment was used.

**Fix:**
```bash
which gmx
gmx --version
```

If needed:
```bash
module load gromacs
# or
conda activate gromacs
```

---

## Normal workflow for membrane trajectories

```bash
# 1. Use equilibrated / production trajectory
membrane-analysis -s md.tpr -f md.xtc --center

# 2. Focus on late trajectory window
membrane-analysis -s md.tpr -f md.xtc -b 50000 -e 200000 --center

# 3. Inspect cholesterol / specific lipid enrichment
membrane-analysis -s md.tpr -f md.xtc --type composition,densmap --component CHOL --center

# 4. Mixed interpretation
# thickness + density -> bilayer geometry
# order -> fluidity / condensation
# orientation -> interface polarization
# densmap + composition -> lateral heterogeneity / annular enrichment
```

---

## Manual facts worth remembering

- `gmx order`: larger `|S_CD|` means more ordered tails.
- Thickness is best estimated from leaflet headgroup density peaks.
- `gmx density` along the membrane normal is the quickest sanity check for bilayer stability.
- `gmx densmap` reveals lateral heterogeneity; it complements, not replaces, axial density.
- `gmx sorient` and `gmx densorder` are interface-focused tools; interpret them with the correct membrane normal.
- Semi-isotropic pressure coupling is the standard production setup for bilayers.

---

## When to trust the result

Trust more when:
- trajectory is PBC-clean and centered
- analysis window excludes early equilibration
- thickness, density, and order tell a consistent story
- target component naming is verified

Trust less when:
- leaflet peaks are broad / drifting
- order profiles are extremely noisy
- densmap hotspots change dramatically with small parameter tweaks
- the membrane is visibly undulated or not equilibrated
