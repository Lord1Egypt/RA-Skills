# Changelog

## [5.3.3] - 2026-06-01

### Security (SkillSpector audit remediation — batch 2)
- **`eval` removed** from `scripts/analysis/property-extended.sh` — `safe_run()` now uses explicit command arguments instead of string eval, preventing potential command injection
- **Conditional report generation** in `scripts/analysis/property-extended.sh` — sections now marked ⚠️ when analysis failed, preventing users from trusting non-existent output files
- **MARTINI download gated** in `scripts/advanced/coarse-grained.sh` — `check_martini_forcefield()` now requires `AUTOMD_CG_ALLOW_DOWNLOAD=1`; HTTP → HTTPS for all download URLs
- **aMD report integrity** in `scripts/advanced/accelerated-md.sh` — report now conditionally excludes aMD reweighting formulas when metadynamics fallback was used; metadynamics-specific analysis sections provided instead
- **INSTALLATION.md warnings** — security advisories added before all `sudo`, `/etc/`, and system-level operations; `insane.py` download uses HTTPS; `~/.gromacs_env.sh` warns against adding to `.bashrc`
- **ligand-topology.md warnings** — `apt-get`, `/etc/ld.so.conf.d/`, and `ldconfig` commands now commented out with security advisories and conda alternatives
- **qmmm-errors.md warnings** — `/etc/hosts` modification now includes security context and container-only guidance; `SYS_PTRACE` capability risk documented
- **membrane-errors.md warnings** — `sudo mv insane.py` replaced with user-path `~/.local/bin/` install; HTTPS download

## [5.3.2] - 2026-06-01

### Security (ClawHub audit remediation)
- **Command injection fixed** in `scripts/utils/utils.sh` (extract) and `scripts/utils/preprocess.sh` — replaced unsafe `$CMD` string concatenation with bash arrays (`"${cmd_arr[@]}"`)
- **aMD silent fallback removed** in `scripts/advanced/accelerated-md.sh` — PLUMED absence is now fatal by default; metadynamics fallback requires explicit `AUTOMD_AMD_ALLOW_FALLBACK=1`; fallback report now includes a prominent warning banner
- **Auto-install gated** in `scripts/advanced/ligand.sh`, `membrane.sh`, `freeenergy.sh`, `coarse-grained.sh` — `auto_install_dependencies()` now respects `AUTOMD_AUTO_INSTALL` (default: 0/off), shows missing tools and install instructions instead of silently modifying the host
- **Troubleshoot logging disabled by default** in `references/guides/troubleshoot-escalation.md` — requires `AUTOMD_TROUBLESHOOT_LOG=1`; log directory moved from `~/.gromacs_troubleshoot_log/` to `./automd-troubleshoot-log/` for user visibility

## [5.3.1] - 2026-05-29

### Added
- ORCA OpenMPI parallel troubleshooting (ERROR-011)
- QM/MM error references (`references/troubleshoot/qmmm-errors.md`)

## [5.3.0] - 2026-05-28

### Added
- AI experiment log/plan rules: mandatory `EXPT_LOG.md` and `PLAN.md` before any computation
- GPU references: cross-forcefield system building, GPU installation, GPU MD execution, ligand topology
  - `references/gpu/cross-forcefield-system.md`
  - `references/gpu/gpu-installation.md`
  - `references/gpu/gpu-md-execution.md`
  - `references/gpu/ligand-topology.md`
- Troubleshooting: setup errors (`references/troubleshoot/setup-errors.md`)
- SKILLS_INDEX expanded with GPU and troubleshooting entries

### Changed
- Enhanced AI assistant rules with mandatory experiment documentation
- Updated GPU-related guidance throughout workflows

## [5.2.0] - 2026-05-25

### Changed
- Based on GROMACS 2025.4 - 2026.1
- Runtime dependency updates

## [5.0.1] - 2026-05-22

### Added
- ISPETase (PDB: 8H5K) complete example workflow under `examples/ispetase/`
  - Setup → Equilibration → Production → Analysis (real trajectory)
  - PCA eigenvalues, 2D projection, clustering results
  - Self-contained README with reproduce commands
- Example READMEs for freeenergy, umbrella, membrane, and ligand workflows
- `accelerated-md` entry in SKILLS_INDEX.yaml

### Fixed
- `bc` dependency replaced with `awk` in setup.sh, equilibration.sh
- `base_dir` hardcoded path → `${SKILL_ROOT:-.}` in SKILLS_INDEX.yaml
- SKILL.md Quick Start: clarified troubleshoot path resolution
- Aligned `protein.sh` references between SKILLS_INDEX and METHOD_SELECTION_INDEX
- Removed stale `SKILLS_INDEX.yaml.backup` (v2.0)

### Removed
- 69 development artifacts (dev reports, test reports, publish logs) from git tracking
- 3 orphan/unreferenced scripts: `analysis/pca.sh`, `workflow/workflow.sh`, `analysis/protein.sh`
- `method-selector-SKILL.md` (orphan, content covered by main SKILL.md)

### Changed
- `.gitignore` and `.skillignore` updated to exclude development artifacts
- Root directory cleaned: 85+ files → 5 core files

## [5.0.0] - 2026-04-11

### Added
- Decision layer: method-selector with METHOD_SELECTION_INDEX.yaml
- Core workflow: setup, equilibration, production, preprocessing, utilities
- Enhanced sampling: umbrella, free energy, replica exchange, metadynamics, steered MD, enhanced sampling, accelerated MD
- Special systems: membrane, ligand, coarse-grained, electric field, non-equilibrium, QM/MM
- Validation: trajectory, binding, property, membrane, scattering, free-energy, protein-focused analyses
- Visualization: publication-ready plotting (Nature/Science/Cell styles)
- Token-optimized troubleshooting references for every workflow
- Quick reference parameters embedded in each script

## [5.1.0] - 2026-05-22 (Unified Workflow + Python Analysis Engine)

### Added
- `automd-master.sh`: Unified master controller — single command for end-to-end MD
  - Auto-detects system state (pdb/topology/prepared)
  - Automatic checkpoint resume
  - Integrated basic analysis (RMSD/RMSF/Rg/PCA/clustering)
- `scripts/basic/smart-production.sh`: Enhanced production with checkpoint resume + real-time monitoring
- `scripts/analysis/analysis-extended.sh`: Bash wrapper for Python analysis modules
- `scripts/analysis/py/msd.py`: Python MSD analysis (MDAnalysis — bypasses GROMACS 2026 selection bug)
- `scripts/analysis/py/distance.py`: Residue pair distance tracking
- `scripts/analysis/py/chi.py`: Chi1/Chi2 side-chain dihedral angle analysis
- All 3 Python modules verified on ISPETase trajectory

### Fixed
- GROMACS 2026 conda-forge selection bug workaround (msd, distance, chi)
- analysis-extended.sh: absolute path resolution before cd into output dir

## [5.1.1] - 2026-05-22 (Native GROMACS Analysis)

### Added
- `scripts/analysis/native-analysis.sh`: Pure GROMACS 2026 native analysis
  - `gmx msd -sel`: MSD + diffusion (fixed from v5.0.1 Python workaround)
  - `gmx pairdist -ref/-sel`: Residue COM distance tracking
  - `gmx chi`: Full chi angle analysis with per-residue-type histograms
- All native commands verified on ISPETase trajectory

### Fixed
- GROMACS 2026 conda-forge selection bug diagnosis: was incorrect syntax, not a build bug
- Correct syntax for GROMACS 2026:
  - `gmx msd -sel 'atomname CA'` ✅
  - `gmx pairdist -ref 'res_cog of resnr N' -sel 'res_cog of resnr M'` ✅
  - `gmx chi` (auto-detects protein, no input needed) ✅
- `gmx nmeig` still requires special hessian setup → Python fallback retained

### Deprecated
- Python py/msd.py, py/distance.py, py/chi.py: retained as fallbacks only
- Preferred path: `native-analysis.sh` (faster, richer output)
