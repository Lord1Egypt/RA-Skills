# COMSOL Skill Input Schema

All schemas are topic-neutral templates. Replace every `<CONFIGURE_...>` value with the user's own project values before running scripts.

## Shared Device Stack

```json
{
  "name": "<CONFIGURE_DEVICE_OR_SAMPLE_NAME>",
  "dimension": "<CONFIGURE_DIMENSION_1D_2D_OR_3D>",
  "device_width_nm": "<CONFIGURE_WIDTH_NM_IF_RELEVANT>",
  "layers": [
    {
      "name": "<CONFIGURE_LAYER_1_NAME>",
      "role": "<CONFIGURE_LAYER_1_ROLE>",
      "material": "<CONFIGURE_LAYER_1_MATERIAL>",
      "thickness_nm": "<CONFIGURE_LAYER_1_THICKNESS_NM>",
      "n": "<CONFIGURE_LAYER_1_REFRACTIVE_INDEX>",
      "k": "<CONFIGURE_LAYER_1_EXTINCTION_COEFFICIENT>",
      "Nd": "<CONFIGURE_LAYER_1_DONOR_DENSITY_CM3_IF_RELEVANT>",
      "Na": "<CONFIGURE_LAYER_1_ACCEPTOR_DENSITY_CM3_IF_RELEVANT>",
      "mu_n": "<CONFIGURE_LAYER_1_ELECTRON_MOBILITY_IF_RELEVANT>",
      "mu_p": "<CONFIGURE_LAYER_1_HOLE_MOBILITY_IF_RELEVANT>",
      "tau_n": "<CONFIGURE_LAYER_1_ELECTRON_LIFETIME_IF_RELEVANT>",
      "tau_p": "<CONFIGURE_LAYER_1_HOLE_LIFETIME_IF_RELEVANT>",
      "bandgap_eV": "<CONFIGURE_LAYER_1_BANDGAP_IF_RELEVANT>",
      "electron_affinity_eV": "<CONFIGURE_LAYER_1_ELECTRON_AFFINITY_IF_RELEVANT>"
    }
  ]
}
```

## Optical Config

```json
{
  "simulation_type": "optical",
  "device_stack": "<CONFIGURE_DEVICE_STACK_OBJECT>",
  "wavelengths_nm": "<CONFIGURE_WAVELENGTH_LIST_NM>",
  "incident_intensity": "<CONFIGURE_INTENSITY_WITH_UNIT>",
  "polarization": "<CONFIGURE_POLARIZATION>",
  "output_dir": "output/optical_configured_project"
}
```

## Optoelectronic Config

```json
{
  "simulation_type": "optoelectronic",
  "device_stack": "<CONFIGURE_DEVICE_STACK_OBJECT>",
  "optical_generation": {
    "source": "<CONFIGURE_FROM_OPTICAL_SIM_OR_ANALYTIC_OR_UNIFORM>",
    "file": "<CONFIGURE_OPTICAL_RESULT_FILE_IF_USED>",
    "wavelength_nm": "<CONFIGURE_WAVELENGTH_NM>",
    "intensity": "<CONFIGURE_INTENSITY_WITH_UNIT>"
  },
  "bias_range": {
    "start_V": "<CONFIGURE_START_V>",
    "stop_V": "<CONFIGURE_STOP_V>",
    "points": "<CONFIGURE_POINT_COUNT>"
  },
  "temperature_K": "<CONFIGURE_TEMPERATURE_K>",
  "output_dir": "output/optoelectronic_configured_project"
}
```

## Thermal Config

```json
{
  "simulation_type": "thermal_coupled",
  "device_stack": "<CONFIGURE_DEVICE_STACK_OBJECT>",
  "thermal_properties": "<CONFIGURE_THERMAL_PROPERTY_TABLE>",
  "thermal_boundaries": "<CONFIGURE_BOUNDARY_CONDITIONS>",
  "heat_sources": "<CONFIGURE_HEAT_SOURCES>",
  "temperature_coefficients": "<CONFIGURE_TEMPERATURE_DEPENDENT_MODELS>",
  "output_dir": "output/thermal_configured_project"
}
```

## Metric Extraction Config

```json
{
  "extraction_type": "<CONFIGURE_EXTRACTION_TYPE>",
  "model_path": "<CONFIGURE_MODEL_OR_DATA_PATH>",
  "measurement_conditions": "<CONFIGURE_MEASUREMENT_CONDITIONS>",
  "output_dir": "output/metrics_configured_project"
}
```

## Rule

If a placeholder remains, ask the user for the missing value instead of substituting a topic-specific default.
