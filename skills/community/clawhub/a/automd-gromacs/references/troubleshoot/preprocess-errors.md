# preprocess errors

## ERROR: MDP not found

**Cause:** File path wrong or typo

**Fix:**
```bash
ls *.mdp  # list available
preprocess -f em.mdp -c conf.gro
```

## ERROR: No topology found

**Cause:** Auto-detect failed, no topol.top

**Fix:**
```bash
# Specify explicitly
preprocess -f em.mdp -c conf.gro -p system.top

# Or create symlink
ln -s ../topol.top .
```

## ERROR: Atom count mismatch

**Cause:** Coordinate & topology don't match

**Fix:**
```bash
# Check both
gmx check -f conf.gro
grep "^\[ molecules \]" -A 10 topol.top

# Regenerate topology or use correct coordinate
```

## WARNING: continuation=yes but no checkpoint

**Cause:** MDP has continuation but -t missing

**Fix:**
```bash
# Add checkpoint
preprocess -f npt.mdp -c nvt.gro -t nvt.cpt -o npt.tpr

# Or change MDP
sed -i 's/continuation.*=.*yes/continuation = no/' npt.mdp
```

## WARNING: POSRES defined but no restraint

**Cause:** MDP defines POSRES but -r missing

**Fix:**
```bash
# Add restraint reference
preprocess -f nvt.mdp -c em.gro -r em.gro -o nvt.tpr

# Or remove POSRES from MDP
sed -i '/define.*POSRES/d' nvt.mdp
```

## grompp failed with warnings

**Cause:** Topology issues, parameter conflicts

**Fix:**
```bash
# Check grompp.log
tail -50 grompp.log

# Increase tolerance if safe
preprocess -f em.mdp -c conf.gro --maxwarn 2

# Common issues:
# - Missing [ atomtypes ]
# - Duplicate [ molecules ]
# - Invalid MDP parameters
```

## Quick bypass validation

**Use case:** Trusted inputs, skip checks

```bash
preprocess -f em.mdp -c conf.gro --quick
```

---

**Reference:** GROMACS Manual Ch. 7 (grompp)
