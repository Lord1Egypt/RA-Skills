# cp2k_task_map.md

This file defines default parameter-selection rules for common CP2K tasks, primarily for QUICKSTEP/DFT workflows. It is designed for natural-language routing in a CP2K input-generation skill.

## 1. General principles

- Default engine: `&FORCE_EVAL METHOD QS` with Quickstep DFT.
- Default basis/pseudopotential family for routine pseudopotential DFT: MOLOPT Gaussian basis + GTH pseudopotential.
- Default pseudopotential flavor: choose `GTH-PBE[-qN]` when the XC functional is PBE-family GGA.
- Default GPW settings for routine DFT:
  - `&QS METHOD GPW`
  - `&MGRID CUTOFF 500`
  - `&MGRID REL_CUTOFF 60`
- Default SCF strategy:
  - finite-gap, nonmetal, isolated molecules / semiconductors: OT-based SCF
  - metals or systems with k-points / smearing needs: diagonalization-based SCF
- Default print verbosity: `PRINT_LEVEL LOW` or `MEDIUM`.

## 2. Task routing by user intent

### 2.1 Single-point energy

**When to use**
- User asks for total energy, electronic energy, frontier orbitals, charge density, DOS precursor, adsorption energy component, or a “single-point” calculation.

**Core choice**
- `RUN_TYPE ENERGY`
- Add `FORCE_EVAL / DFT / SCF`
- Add `SUBSYS` with structure and `KIND` blocks

**Defaults**
- Molecule / cluster:
  - `PERIODIC NONE`
  - cubic vacuum box, at least 8–12 Å padding around structure
  - OT SCF
- Periodic solid:
  - periodic cell from structure source
  - gamma-point for large supercells
  - Monkhorst-Pack mesh for primitive/small cells
  - diagonalization SCF if metallic or if smearing is needed

### 2.2 Energy + forces

**When to use**
- User asks for forces, pre-relaxation check, or downstream vibrational / optimization workflow.

**Core choice**
- `RUN_TYPE ENERGY_FORCE`

**Defaults**
- Same as single-point energy, but ensure force evaluation is enabled through run type.

### 2.3 Geometry optimization (fixed cell)

**When to use**
- Molecules, adsorbates in fixed supercells, slabs with frozen lattice, clusters, isolated defects where the cell should not change.

**Core choice**
- `RUN_TYPE GEO_OPT`
- Add `&MOTION / &GEO_OPT`

**Defaults**
- Optimizer:
  - small/medium systems: `BFGS`
  - larger systems or when memory is a concern: `LBFGS`
- Suggested convergence targets:
  - `MAX_FORCE 4.5E-4` to `1.0E-3` Ha/Bohr depending on requested accuracy
  - `MAX_DR 3.0E-3`
  - `RMS_DR 1.5E-3`
- Keep cell fixed.

### 2.4 Cell optimization

**When to use**
- Bulk crystals when the user wants lattice constants, relaxed cell parameters, or pressure-free equilibrium structure.

**Core choice**
- `RUN_TYPE CELL_OPT`
- Add `&MOTION / &CELL_OPT`

**Defaults**
- `CELL_OPT / TYPE DIRECT_CELL_OPT` unless the workflow explicitly requests alternating geometry optimization.
- Use periodic boundary conditions.
- Use k-points for primitive cells.
- Do not use for isolated molecules in vacuum.

### 2.5 Molecular dynamics

**When to use**
- User asks for MD, finite-temperature equilibration, NVT/NVE/NPT trajectory, diffusion, thermal fluctuation.

**Core choice**
- `RUN_TYPE MD`
- Add `&MOTION / &MD`

**Defaults**
- Ensemble:
  - unspecified condensed phase equilibration: `NVT`
  - microcanonical dynamics: `NVE`
  - variable-cell bulk dynamics: `NPT_F`
- Timestep heuristic:
  - systems containing H and no mass repartitioning: 0.5–1.0 fs
  - heavy-atom systems: up to ~1.0–2.0 fs if justified
- SCF:
  - reuse wavefunction guess from previous step
  - OT for insulating gamma-point systems
  - diagonalization + smearing for metals

### 2.6 Vibrational analysis

**When to use**
- User asks for normal modes, IR precursor workflow, frequencies, zero-point energy.

**Core choice**
- `RUN_TYPE VIBRATIONAL_ANALYSIS`
- Add `&VIBRATIONAL_ANALYSIS`

**Defaults**
- Require a previously optimized stationary structure.
- Tighten SCF and geometry thresholds versus ordinary relaxation.
- Recommended `EPS_SCF ~ 1E-8`.

### 2.7 Band structure / DOS for periodic systems

**When to use**
- User asks for electronic band structure, DOS, projected DOS, band gap of a solid.

**Core choice**
- SCF on a converged k-point mesh first.
- Then add `&FORCE_EVAL / &PROPERTIES / &BANDSTRUCTURE` or DOS-related print/properties blocks.

**Defaults**
- Use `KPOINTS` with Monkhorst-Pack mesh for SCF.
- For 2D systems, set nonperiodic direction mesh to 1.
- Metals require smearing and diagonalization.
- Semiconductors may use diagonalization or OT depending on whether k-points / smearing are needed.

### 2.8 Surface adsorption / interface binding energy

**When to use**
- User asks for adsorption energy, binding energy, molecule-on-surface interaction.

**Core choice**
- Usually three calculations:
  1. relaxed combined system
  2. isolated slab
  3. isolated adsorbate
- Use consistent XC, basis, cutoff, cell convention, and k-point strategy across all three.

**Defaults**
- Slab: periodic in slab plane; enough vacuum normal to surface.
- Usually `GEO_OPT` for combined system, optionally constrained bottom layers.
- Add dispersion correction unless user disables it.

### 2.9 Transition-state / saddle search

**When to use**
- User explicitly requests TS, saddle point, reaction barrier, NEB, CI-NEB, dimer-style workflows.

**Core choice**
- Not a default “simple” task.
- Requires explicit workflow selection and user confirmation if multiple reaction images/path guesses are possible.

**Defaults**
- If the request is vague, downgrade to reactant/product optimization plus ambiguity notice.

### 2.10 Core spectroscopy / XAS-like tasks

**When to use**
- User asks for XAS, core excitation, near-edge spectrum, core-level spectroscopy.

**Core choice**
- Prefer GAPW / all-electron treatment for excited atoms.
- `RUN_TYPE ENERGY`

**Defaults**
- Excited atom(s): all-electron basis + `POTENTIAL ALL`
- Other atoms may remain on MOLOPT + GTH pseudopotentials
- Hybrid functional and ADMM can be suggested for larger systems

## 3. Decision rules for periodicity and k-points

### 3.1 Molecules / clusters
- `PERIODIC NONE`
- No k-points
- Vacuum box required

### 3.2 3D bulk crystals
- `PERIODIC XYZ`
- Use k-points unless the structure is already a very large supercell

### 3.3 2D slabs / monolayers
- `PERIODIC XY` if the cell convention is explicit and supported by the template, otherwise keep full periodic cell with large vacuum and use `KPOINTS` mesh `kx ky 1`
- Add vacuum along nonperiodic direction

### 3.4 1D chains / wires
- periodic only along chain direction
- k-point mesh only along that direction

## 4. SCF defaults by electronic character

### 4.1 Insulators / finite-gap systems
- Prefer OT:
  - `&SCF`
  - `MAX_SCF 200`
  - `EPS_SCF 1.0E-6` (tighten if requested)
  - `&OT PRECONDITIONER FULL_ALL`
- No smearing by default.

### 4.2 Metals / small-gap systems / dense k-point meshes
- Prefer diagonalization:
  - `&SCF`
  - `MAX_SCF 200`
  - `EPS_SCF 1.0E-6`
  - `&DIAGONALIZATION`
  - `&MIXING` enabled
  - smearing enabled
- OT is not the default for metallic systems.

## 5. XC, dispersion, and accuracy defaults

### 5.1 XC functional
- Default: `PBE`
- If user says only “GGA”: map to `PBE`
- If user asks for hybrid and system size is moderate: suggest `PBE0` or `HSE06`
- If the user gives no XC and the task is routine structure relaxation / adsorption / screening: use `PBE`

### 5.2 Dispersion
- For molecular crystals, layered materials, physisorption, organic adsorption, interfaces: add D3(BJ)-type correction by default unless the user disables dispersion.
- For strongly covalent bulk screening where vdW is likely not load-bearing: dispersion may be omitted unless user requests it.

### 5.3 Grid accuracy
- Default production starting point:
  - `CUTOFF 500`
  - `REL_CUTOFF 60`
- “Fast screening” mode:
  - `CUTOFF 400`
  - `REL_CUTOFF 50`
- “Tight / publication” mode:
  - begin from `CUTOFF 600+`, with explicit convergence note

## 6. Output routing hints

- Energy task: print total energy and final coordinates.
- Geometry optimization: print trajectory + final structure.
- MD: print restart, trajectory, and thermodynamic summary.
- Band/DOS: print band structure / DOS section outputs.
- Vibrations: print frequencies and normal modes.
- Adsorption workflow: print each subsystem energy with consistent naming for post-processing.

## 7. What the skill should infer automatically

When the user does **not** specify parameters, the skill should infer, in this order:
1. system class: molecule / bulk / slab / wire / interface
2. task class: energy / energy_force / geo_opt / cell_opt / md / vibration / band / adsorption
3. periodicity
4. electronic character: insulating vs metallic guess
5. SCF algorithm
6. k-point need
7. whether dispersion is needed
8. accuracy tier: screening / standard / tight

## 8. Safe fallback presets

### Molecule standard preset
- `RUN_TYPE ENERGY` or `GEO_OPT`
- `PERIODIC NONE`
- box with 10 Å vacuum padding
- `PBE`
- `GPW`
- `DZVP-MOLOPT-SR-GTH`
- `GTH-PBE`
- `CUTOFF 500`, `REL_CUTOFF 60`
- OT SCF

### Bulk crystal standard preset
- `RUN_TYPE ENERGY` or `CELL_OPT`
- periodic cell from source
- `PBE`
- `GPW`
- `DZVP-MOLOPT-SR-GTH`
- `GTH-PBE`
- `CUTOFF 500`, `REL_CUTOFF 60`
- Monkhorst-Pack k-points
- diagonalization SCF if metallic, otherwise OT or diagonalization depending on template support

### Surface adsorption standard preset
- `RUN_TYPE GEO_OPT`
- slab supercell with vacuum
- bottom-layer constraints optional
- `PBE-D3(BJ)` style setup
- `DZVP-MOLOPT-SR-GTH`
- `GTH-PBE`
- `CUTOFF 500`, `REL_CUTOFF 60`
- `k_x k_y 1`

## 9. Non-goals for automatic routing

These tasks should not be silently auto-generated from a vague one-line prompt without warning:
- NEB / CI-NEB / transition-state search
- excited-state workflows beyond basic documented templates
- GW / RPA / MP2 / double hybrids
- QM/MM partitioning
- unusual pseudopotential families unless explicitly requested
