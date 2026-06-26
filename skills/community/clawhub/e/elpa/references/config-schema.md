# ELPA Config Schema

## Training Config (`elpa_orchestrator.py`)

Top-level fields:

- `dataset` (string): training CSV path.
- `val_dataset` (string, optional): validation CSV path.
- `test_dataset` (string, optional): test CSV path.
- `horizon` (int, optional): forecast horizon.
- `period` (int, optional): cycle period.
- `seed` (int, optional): random seed.
- `context` (object, optional): extra placeholder values for command templates.
- `models` (array, required): list of real sub-model training jobs.

Model fields:

- `name` (string, required): unique model key.
- `group` (string, required): `online` or `offline`.
- `enabled` (bool, optional, default true): whether this model is active.
- `train_cmd` (string, required): shell command template for real training.
- `env` (object, optional): extra environment variables for this model.

Supported placeholders in `train_cmd`:

- `{dataset}`, `{train_dataset}`
- `{val_dataset}`, `{test_dataset}`
- `{run_dir}`, `{model_dir}`, `{model_name}`
- `{horizon}`, `{period}`, `{seed}`
- any scalar top-level field (for example `{project_root}`)
- any scalar in `context` (for example `{python_bin}`)

## Integration Config (`elpa_integrator.py`)

Top-level fields:

- `beta` (float, optional): EWMA factor.
- `dirty_interval` (int, optional): ELPA dirty interval.
- `amplitude_window` (int, optional): ELPA amplitude calibration window.
- `mutant_epsilon` (float or null, optional): mutant threshold.
- `models` (array, required): model validation error inputs.

Per-model fields:

- `name` (string, required)
- `group` (`online` or `offline`, required)
- one of:
  - `ewma_score` (float)
  - `error_values` (float array)
  - `error_csv` (CSV path)

`error_csv` accepted formats:

- Column `abs_error`
- or columns `y_true` and `pred` (script computes abs error)
