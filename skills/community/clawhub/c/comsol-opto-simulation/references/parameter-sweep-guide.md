# Parameter Sweep Guide

Use this guide to design user-configured sweeps without inheriting any source-workspace topic assumptions.

## Sweep Definition

A sweep requires:

- base config path
- JSON path to each parameter
- sweep mode: `lin`, `log`, or `list`
- units and physical meaning
- output metrics
- validation criteria

Example template:

```json
{
  "simulation_type": "parameter_sweep",
  "base_config_path": "<CONFIGURE_BASE_CONFIG_JSON>",
  "sweep_parameters": [
    {
      "name": "device_stack.layers[<CONFIGURE_LAYER_INDEX>].<CONFIGURE_PARAMETER>",
      "description": "<CONFIGURE_PARAMETER_DESCRIPTION>",
      "mode": "lin",
      "start": "<CONFIGURE_START_VALUE>",
      "stop": "<CONFIGURE_STOP_VALUE>",
      "points": "<CONFIGURE_POINT_COUNT>"
    }
  ],
  "output_dir": "output/sweep_configured_project",
  "extract_metrics": "<CONFIGURE_TRUE_FALSE>",
  "generate_summary_plots": "<CONFIGURE_TRUE_FALSE>"
}
```

## Planning Checklist

- Sweep one physical factor first before fitting multiple uncertain parameters.
- Keep the baseline case unchanged and recorded.
- Choose ranges from measured data, literature, or an explicit user assumption.
- Avoid silently using placeholder values as numerical inputs.
- For failed cases, keep solver logs and record whether the failure is numerical or physically meaningful.

## Reporting

Report:

- configured parameter and units
- range and sampling mode
- fixed assumptions
- successful and failed cases
- best case by the user's validation metric
- sensitivity or uncertainty interpretation
