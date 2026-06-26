# COMSOL Script Map

Use this map to choose the smallest reliable entry point. Most scripts are
diagnostic probes kept for troubleshooting; do not run them unless the main
workflow or the user specifically needs that level of inspection.

## Main User-Facing Entry Points

- `scripts/discover_comsol_environment.py`: locate COMSOL, Java, and likely mph setup.
- `scripts/check_comsol_products.py`: inspect available COMSOL products/modules.
- `scripts/install_mph.py`: install or verify the Python `mph` bridge.
- `scripts/run_optoelectronic_sim.py`: run a configured optoelectronic model.
- `scripts/run_optical_simulation.py`: run a configured optical model.
- `scripts/run_thermal_coupled_sim.py`: run a configured thermal-coupled model.
- `scripts/run_parameter_sweep.py`: run batch sweeps with checkpoint/resume behavior.
- `scripts/test_sweep_offline.py`: offline smoke test for sweep logic; does not require COMSOL.

## Post-Processing

- `scripts/extract_iv.py`: extract I-V style results.
- `scripts/extract_detector_metrics.py`: extract detector-oriented metrics.
- `scripts/extract_detector_metrics_v2.py`: newer detector metric extraction variant.

## Model Repair and Solver Recovery

- `scripts/diagnose_rerun.py`: inspect a failed run and rerun after adjustments.
- `scripts/fix_and_solve.py`: apply known fixes and solve.
- `scripts/fix_equilibrium.py`: focus on equilibrium initialization issues.
- `scripts/reconfigure_solve.py`: reconfigure solver settings before solving.
- `scripts/solver_fallback_config.py`: generate fallback solver settings.
- `scripts/solver_log_probe.py`: inspect solver logs.

## Environment and API Probes

Use only when debugging COMSOL/mph API differences:

- `probe_application_library_examples.py`
- `probe_all_features.py`
- `probe_boundary_indices.py`
- `probe_boundary_structure.py`
- `probe_box_selection.py`
- `probe_box_selection2.py`
- `probe_chi0_doping.py`
- `probe_chi_mobility.py`
- `probe_doping_name.py`
- `probe_doping_trap.py`
- `probe_expressions.py`
- `probe_fin_action.py`
- `probe_fin_props.py`
- `probe_fin_props2.py`
- `probe_geom_ops.py`
- `probe_material_physics.py`
- `probe_material_props.py`
- `probe_model_selection.py`
- `probe_parametric.py`
- `probe_ref_energy.py`
- `probe_selection_timing.py`
- `probe_selection_types.py`
- `probe_semi_props.py`
- `probe_semi_set.py`
- `probe_solution.py`
- `probe_solver.py`
- `probe_sweep_api.py`

## Legacy or Narrow Debug Scripts

Keep these for reproducibility and deep troubleshooting, but prefer the main
entry points first:

- `build_heterostructure.py`
- `compile_probe.py`
- `debug_semiconductor_variants.py`
- `deep_probe.py`
- `depvar_probe.py`
- `direct_diagnose.py`
- `init_probe.py`
- `last_attempt.py`
- `semi_config_probe.py`
- `simple_pn_test.py`
- `simple_solve.py`
- `single_point_test.py`
- `study_config_probe.py`
- `version_probe.py`
