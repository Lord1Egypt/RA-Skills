# Repository Conventions

## Framework location

The DGM framework is bundled in this skill at `assets/src/`. When used in an existing repo, `src/` lives at the repo root. All path references below assume `src/` is at the repo root (copied from `assets/src/` if starting fresh).

## Directory structure

| Path | Purpose |
|------|---------|
| `src/configs/` | Problem config dataclasses (inherit `CommonConfig`) |
| `src/problems/` | Problem definitions (inherit `BaseProblem`) |
| `src/losses/` | HJB residual losses (plain classes, not base class) |
| `src/models/dgm_net.py` | `DGMNet` — do NOT modify |
| `src/trainers/dgm_trainer.py` | Training loop — do NOT modify |
| `src/samplers/` | `UniformSampler` (1D scalar bounds), `UniformSampler2D` (multi-dimensional, dimension ≥ 2) |
| `examples/` | Runnable training scripts |
| `plot_training_csv.py` | Generic CSV plotting utility |

## Naming convention

- Module slug: `example_<n>` (snake_case)
- Class prefix: CamelCase from slug — `example_4` → `Example4`
- File triplet: `example_4_config.py` / `example_4_problem.py` / `example_4_loss.py`

## DGMNet constructor

```python
DGMNet(
    layer_width=config.nodes_per_layer,  # int: hidden layer width
    n_layers=config.num_layers,          # int: number of hidden layers
    input_dim=config.dimension,          # int: spatial dims only (no time)
    output_dim=1,                        # 1 for value; num_controls for control
    control_output=False,                # True for control network
    activation=config.activation,        # str: 'swish' default
)
```

Call: `model(t, x)` where `t: (batch, 1)`, `x: (batch, input_dim)` → returns `(batch, output_dim)`.  
All inputs/outputs must be `tf.float32`.

## DGMTrainer constructor

```python
DGMTrainer(
    model=model,                          # value DGMNet
    control=control,                      # control DGMNet
    loss_fn=loss_fn,                      # loss class instance
    sampler=sampler,                      # UniformSampler / UniformSampler2D
    optimizer_value=tf.keras.optimizers.Adam(lr_schedule),
    optimizer_control=tf.keras.optimizers.Adam(lr_schedule),
    config=config,
    problem=problem,
)
```

`trainer.train()` → returns `self.history` dict (same keys as CSV; see training-output-contract.md).  
`trainer.save_models(save_dir)` → saves `model_value.weights.h5` and `model_control.weights.h5`.

## Loss class — required return signatures

### `compute_value_loss`
```python
def compute_value_loss(self, model, control, t_interior, X_interior, t_terminal, X_terminal):
    ...
    return L1, L3, diff_V, diff_terminal   # all tf.Tensor
```
- `L1`: scalar — PDE / HJB interior residual loss  
- `L3`: scalar — terminal condition loss  
- `diff_V`: `(batch,)` or `(batch, 1)` — per-sample HJB residuals (for `maxdiff_V`)  
- `diff_terminal`: `(batch,)` or `(batch, 1)` — per-sample terminal residuals

### `compute_control_loss`
```python
def compute_control_loss(self, model, control, t_interior, X_interior, t_terminal, X_terminal):
    ...
    return L2, extra_info   # L2: tf.Tensor scalar; extra_info: dict[str, tf.Tensor]
```
- `extra_info` maps string keys to tensors; these are pulled into metrics via `config.extra_info_mapping`.  
- Return `{}` if no extra metrics needed.

**DGMTrainer unpacks these returns directly. Wrong shapes or missing values cause silent failures.**

## CommonConfig key fields

| Field | Default | Purpose |
|-------|---------|---------|
| `dimension` | 1 | Spatial dimension |
| `T` | 1.0 | Terminal time |
| `X_low`, `X_high` | 0.0, 1.0 | Domain bounds (scalar for 1D; list for 2D) |
| `num_layers` | 3 | DGMNet hidden layers |
| `nodes_per_layer` | 32 | Layer width |
| `activation` | `'swish'` | Hidden layer activation |
| `sampling_stages` | 5000 | Total training iterations |
| `steps_per_sample` | 10 | SGD steps per sampled batch |
| `initial_learning_rate` | 0.001 | LR schedule start value |
| `end_learning_rate` | 0.00001 | LR schedule end value |
| `nSim_interior` | 2000 | Interior sample size per stage |
| `nSim_terminal` | 1 | Terminal sample size per stage |
| `num_controls` | 1 | Number of control variables |
| `control_names` | `None` → `['u0']` | Column names for control outputs |
| `metrics_config` | `None` → `['maxdiff_V','maxdiff_terminal']` | Metrics to track and log |
| `extra_info_mapping` | `{}` | `extra_info` key → metric name mapping |
| `early_stop_metric` | `'maxdiff_V'` | Which metric triggers early stop |
| `early_stop_threshold` | `1e-4` | Convergence threshold |
| `saveName` | (set in subclass) | Prefix for output CSV and weight files |
| `save_dir` | `'./results'` | Output directory |
| `saveOutput` | `True` | Whether to write CSV and weights |

`config.get_optimizer_config()` → returns a `PolynomialDecay` lr schedule ready to pass to `Adam`.

## BaseProblem interface

Subclasses **must** implement:
```python
def get_terminal_condition(self, x):
    """x: (batch, dimension) tf.Tensor → (batch, 1) tf.Tensor"""
```

`extract_metrics()` has a default implementation that handles `maxdiff_V`, `maxdiff_terminal`, `V_at_origin`, per-control values, and any keys in `extra_info_mapping`. Override only when you need custom metric computation not expressible through `extra_info_mapping`.

## Registering new modules in `__init__.py`

After creating `example_n_config.py`, `example_n_problem.py`, `example_n_loss.py`:

```python
# src/configs/__init__.py
from .example_n_config import ExampleNConfig

# src/problems/__init__.py
from .example_n_problem import ExampleNProblem

# src/losses/__init__.py
from .example_n_loss import ExampleNLoss
```

## Safe-change boundary

- Never modify `DGMTrainer` train loop, `eval_step`, or `save_history_csv`.
- Never change `DGMNet` constructor or `call` signature.
- Never change existing loss method return shapes.
- Keep all tensors as `tf.float32`.
