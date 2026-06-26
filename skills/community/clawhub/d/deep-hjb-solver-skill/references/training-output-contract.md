# Training Output Contract

## `trainer.train()` return value

Returns `self.history` — a `dict[str, list[float | int]]` with the same keys and ordering as the training history CSV. Values are Python lists, one entry per completed stage.

## CSV files

Written by `trainer.save_history_csv()` when `config.saveOutput = True`.

### `{config.save_dir}/{config.saveName}_training_history.csv`

One row per training stage. Stage count = `config.sampling_stages`, unless early stopping triggers.

| Column | Type | Description |
|--------|------|-------------|
| `stage` | int | Stage index 0, 1, …, N−1 |
| `loss_total` | float | `L1 + L3` (control loss L2 is excluded) |
| `loss_L1` | float | PDE / HJB interior residual loss |
| `loss_L2` | float | Control / FOC residual loss |
| `loss_L3` | float | Terminal condition loss |
| `maxdiff_V` | float | `max|diff_V|` — max abs HJB residual over the validation batch |
| `maxdiff_terminal` | float | `max|diff_terminal|` — max abs terminal residual |
| `V_at_origin` | float | Value network output at `t=0, x=0` (or `x=[1,0]` for 2D) |
| `<control_name>` | float | Control network output at the eval point — one column per name in `config.control_names` |

**Optional columns** (present when listed in `config.metrics_config` and populated via `config.extra_info_mapping`):

| Typical column | Source |
|---------------|--------|
| `max_foc_residual` | returned in `extra_info` from `compute_control_loss` |
| `max_control_bound` | returned in `extra_info` |
| `max_penalty` | returned in `extra_info` |

Any key in `extra_info_mapping` that maps from `compute_control_loss` → metric name will appear as a column if also listed in `config.metrics_config`.

### `{config.save_dir}/{config.saveName}_training_summary.csv`

One row per tracked metric. Columns: `metric, final_value, min_value, max_value, mean_value`.

Covers `loss_total`, `loss_L1`, `loss_L2`, `loss_L3`, plus all entries in `config.metrics_config`.

## `problem.extract_metrics()` interface

Called by `DGMTrainer` after every validation eval step.

```python
def extract_metrics(self, validation_results, t_eval, X_eval, model, control):
    ...
    return dict[str, float]
```

Input `validation_results` tuple (in order):
```
(L1_val, L3_val, diff_V_val, diff_terminal_val, L2_val, extra_info)
```
- `extra_info`: `dict[str, tf.Tensor]` — returned by `compute_control_loss`

**Default implementation** (no override needed for standard metrics):
1. Computes `maxdiff_V = max|diff_V_val|` and `maxdiff_terminal = max|diff_terminal_val|`
2. Evaluates `V_at_origin = model(t_eval, X_eval)[0, 0]`
3. Evaluates each control at `(t_eval, X_eval)` and records under `control_names`
4. Applies `config.extra_info_mapping`: for each `{extra_key: metric_name}`, pulls `extra_info[extra_key]` as `max|·|`
5. Computes `config.custom_metrics` from arithmetic combinations of already-computed metrics

**Override only** when you need metrics that cannot be expressed through `extra_info_mapping` or `custom_metrics`.

## Plotting requirements

- Never assume fixed control column names. Detect them dynamically: any column that is not in the core set (`stage, loss_total, loss_L1, loss_L2, loss_L3, maxdiff_V, maxdiff_terminal, V_at_origin`) is a dynamic column.
- Handle absent optional columns gracefully (check `col in df.columns` before plotting).
- Minimum required plots: loss curves (`loss_total`, `L1`, `L2`, `L3`), `maxdiff_V`, `V_at_origin`.
- Recommended output files: `training_history.png`, `residuals.png`.
