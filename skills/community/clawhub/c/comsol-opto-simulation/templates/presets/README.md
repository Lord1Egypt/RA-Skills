# Preset Simulation Templates

This directory contains topic-neutral JSON templates for common simulation patterns. They are intentionally not ready-to-run quantitative examples.

Before running any template, replace every `<CONFIGURE_...>` placeholder with values from the installing user's own project configuration, measured data, or cited literature.

| Template | Simulation Type | Use Case |
| --- | --- | --- |
| `standard_optical.json` | Optical | Baseline optical absorption or field simulation |
| `low_light.json` | Optical | User-defined low-intensity condition |
| `concentrated.json` | Optical | User-defined high-intensity or high-flux condition |
| `thin_active_layer.json` | Optoelectronic | Thinner user-selected layer test |
| `thick_active_layer.json` | Optoelectronic | Thicker user-selected layer test |
| `high_doping.json` | Optoelectronic | Carrier density, defect density, or conductivity-related parameter test |
| `low_temperature.json` | Optoelectronic | User-defined low-temperature condition |
| `high_temperature.json` | Optoelectronic | User-defined high-temperature condition |
| `thermal_standard.json` | Thermal coupled | Thermal or multiphysics coupling template |

## Usage

```bash
python scripts/run_optical_simulation.py --config templates/presets/standard_optical.json
python scripts/run_optoelectronic_sim.py --config templates/presets/thin_active_layer.json
python scripts/run_thermal_coupled_sim.py --config templates/presets/thermal_standard.json
python scripts/run_parameter_sweep.py --config templates/config_sweep.json
```

The commands above are examples of script entry points. They should be executed only after the placeholders have been replaced with valid values.

## Configuration Checklist

- Define the user's material, sample, device, or system structure.
- Replace layer names, roles, thicknesses, optical constants, transport parameters, and boundary conditions.
- State which values are measured, literature-sourced, or assumed.
- Define validation criteria before trusting numerical results.
- Keep unconfigured templates separate from configured project files.
