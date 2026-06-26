---
name: deep-hjb-solver
description: "Create or refactor code for solving HJB equations with this repository's TensorFlow DGM framework. Use when users ask to generate new HJB training code, add a new problem (config/problem/loss/train script), adapt sampling/training hyperparameters, or create plotting/analysis code from trainer CSV outputs."
---

# Deep HJB Solver

**Before writing any loss or config code**, read `references/repo-conventions.md` — it contains the exact constructor signatures and return-type contracts that must be followed.  
**Before writing any CSV or plotting code**, read `references/training-output-contract.md`.

Never modify `DGMTrainer`, `DGMNet`, or any file under `src/trainers/` or `src/models/` unless explicitly asked.

---

## Output layout

Every new HJB problem is created as a **self-contained folder** named after the problem slug. Nothing is written outside it.

```
<slug>/
├── src/
│   ├── __init__.py
│   ├── configs/
│   │   ├── __init__.py
│   │   ├── common_config.py          ← copied from assets
│   │   └── <slug>_config.py          ← generated
│   ├── models/
│   │   ├── __init__.py
│   │   └── dgm_net.py                ← copied from assets
│   ├── problems/
│   │   ├── __init__.py
│   │   ├── base_problem.py           ← copied from assets
│   │   └── <slug>_problem.py         ← generated
│   ├── losses/
│   │   ├── __init__.py
│   │   └── <slug>_loss.py            ← generated
│   ├── samplers/
│   │   ├── __init__.py
│   │   ├── base_sampler.py           ← copied from assets
│   │   ├── uniform_sampler.py        ← copied from assets
│   │   └── uniform_sampler_2d.py     ← copied from assets
│   ├── trainers/
│   │   ├── __init__.py
│   │   └── dgm_trainer.py            ← copied from assets
│   └── utils/
│       ├── __init__.py
│       └── visualization.py          ← copied from assets
├── examples/
│   └── <slug>_train.py               ← generated
├── plot_training_csv.py              ← copied from assets
└── requirements.txt                  ← copied from assets
```

---

## Workflow

Use the following steps in order. In every template below, replace:
- `<slug>` → snake_case problem name, e.g. `linear_control`
- `<Prefix>` → CamelCase version, e.g. `LinearControl`
- `<dim>` → spatial dimension (`1` or `2`)
- `<N>` → number of control variables
- `<controls>` → Python list literal of control names, e.g. `['Z', 'W']`

### Step 1 — Copy the DGM framework into `<slug>/src/`

**This step is mandatory and must be executed immediately without asking the user for permission or confirmation.** Do not say "should I copy the assets?" — just do it.

Run the following shell commands to copy the bundled framework. Replace `<slug>` with the actual problem slug and `<SKILL_DIR>` with the absolute path to this skill folder (the directory containing this SKILL.md):

```bash
mkdir -p <slug>/src
cp -r <SKILL_DIR>/assets/src/. <slug>/src/
cp <SKILL_DIR>/assets/plot_training_csv.py <slug>/plot_training_csv.py
cp <SKILL_DIR>/assets/requirements.txt <slug>/requirements.txt
```

**Do not proceed to Step 2 until the copy commands have completed successfully.**

### Step 2 — Create `<slug>/src/configs/<slug>_config.py`

**1D domain** (`<dim>` = 1):

```python
"""Configuration for <Prefix>."""

from dataclasses import dataclass, field
from .common_config import CommonConfig


@dataclass
class <Prefix>Config(CommonConfig):

    dimension: int = 1
    T: float = 1.0
    t_low: float = 0.0
    X_low: float = 0.0
    X_high: float = 1.0

    num_controls: int = <N>
    control_names: list = field(default_factory=lambda: <controls>)
    metrics_config: list = field(default_factory=lambda: ['maxdiff_V', 'maxdiff_terminal'])
    extra_info_mapping: dict = field(default_factory=dict)
    early_stop_metric: str = 'maxdiff_V'
    early_stop_threshold: float = 1e-4
    problem_params_keys: list = field(default_factory=list)

    saveName: str = '<slug>'
```

**2D domain** (`<dim>` = 2) — replace the bounds lines with:

```python
    dimension: int = 2
    X_low: list = field(default_factory=lambda: [0.0, 0.0])
    X_high: list = field(default_factory=lambda: [1.0, 1.0])
```

### Step 3 — Create `<slug>/src/problems/<slug>_problem.py`

```python
"""Problem definition for <Prefix>."""

from .base_problem import BaseProblem


def terminal_utility_<slug>(x):
    """TODO: implement terminal payoff g(x). x shape: (batch, dim)."""
    return -x[:, :1]


class <Prefix>Problem(BaseProblem):

    def get_terminal_condition(self, x):
        return terminal_utility_<slug>(x)
```

### Step 4 — Create `<slug>/src/losses/<slug>_loss.py`

```python
"""Loss functions for <Prefix>."""

import tensorflow as tf


class <Prefix>Loss:

    def __init__(self, problem):
        self.problem = problem

    def compute_value_loss(self, model, control, t_interior, X_interior, t_terminal, X_terminal):
        # TODO: replace with real HJB PDE residual.
        # IMPORTANT: if you need more than one gradient from the same tape (e.g.
        # both V_t and V_x), you MUST use persistent=True and delete the tape
        # afterward. A non-persistent tape raises RuntimeError on the second call.
        with tf.GradientTape(persistent=True, watch_accessed_variables=False) as gt:
            gt.watch(t_interior)
            gt.watch(X_interior)
            V = model(t_interior, X_interior)
        V_t = gt.gradient(V, t_interior)   # ∂V/∂t
        V_x = gt.gradient(V, X_interior)   # ∂V/∂x  (use if needed by the HJB)
        del gt  # release persistent tape immediately after use

        ctrl = control(t_interior, X_interior)  # u from control network — substitute into HJB
        residual = V_t  # TODO: replace with actual HJB residual, e.g. V_t + ctrl * V_x + ...
        L1 = tf.reduce_mean(tf.square(residual))

        target_terminal = self.problem.get_terminal_condition(X_terminal)
        fitted_terminal = model(t_terminal, X_terminal)
        diff_terminal = fitted_terminal - target_terminal
        L3 = tf.reduce_mean(tf.square(diff_terminal))

        # diff_V can be either:
        #   (a) a plain tensor — the HJB residual (e.g. diff_V = residual), OR
        #   (b) a dict of debug tensors that MUST contain a 'residual' key
        #       (e.g. {'residual': residual, 'V': V, 'V_t': V_t, 'V_x': V_x})
        # base_problem.extract_metrics handles both forms automatically.
        # MUST return exactly this 4-tuple — DGMTrainer unpacks it directly.
        diff_V = residual          # option (a): simplest form
        # diff_V = {'residual': residual, 'V': V, 'V_t': V_t, 'V_x': V_x}  # option (b)
        return L1, L3, diff_V, diff_terminal

    def compute_control_loss(self, model, control, t_interior, X_interior, t_terminal, X_terminal):
        # TODO: implement FOC / control objective.
        # Always use persistent=True here: you need at least V_x, and some problems
        # also need V_xx (second-order), which requires a nested tape inside this one.
        # persistent=True lets you reuse the outer tape multiple times safely.
        with tf.GradientTape(persistent=True, watch_accessed_variables=False) as gt:
            gt.watch(X_interior)
            V = model(t_interior, X_interior)
        V_x = gt.gradient(V, X_interior)          # ∂V/∂x
        del gt
        ctrl = control(t_interior, X_interior)    # u from control network
        # TODO: compute L2 from the inf{...} terms of the HJB using ctrl and V_x.
        # See "How to translate an HJB equation into loss functions" below for the rule.
        # Example (LQ, inf_u { u*V_x + ½u² }): L2 = tf.reduce_mean(ctrl * V_x + 0.5 * tf.square(ctrl))
        L2 = tf.reduce_mean(ctrl)      # placeholder — replace with real Hamiltonian terms
        # MUST return exactly this 2-tuple — DGMTrainer unpacks it directly
        return L2, {'V_x': V_x, 'ctrl': ctrl}
```

### Step 5 — Register new classes in `<slug>/src/configs/__init__.py`, `<slug>/src/problems/__init__.py`, `<slug>/src/losses/__init__.py`

Append one import line to each file:

```python
# src/configs/__init__.py
from .<slug>_config import <Prefix>Config

# src/problems/__init__.py
from .<slug>_problem import <Prefix>Problem

# src/losses/__init__.py
from .<slug>_loss import <Prefix>Loss
```

### Step 6 — Create `<slug>/examples/<slug>_train.py`

All imports are relative to `<slug>/` (the script is run from inside that folder).

```python
"""Training script for <slug>."""

import os
import sys
import tensorflow as tf

# Ensure the problem folder is on the path when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.configs.<slug>_config import <Prefix>Config
from src.problems.<slug>_problem import <Prefix>Problem
from src.losses.<slug>_loss import <Prefix>Loss
from src.models import DGMNet
from src.samplers import UniformSampler, UniformSampler2D
from src.trainers import DGMTrainer
from plot_training_csv import plot_training_history


def main():
    config = <Prefix>Config()
    config.save_dir = './results'
    os.makedirs(config.save_dir, exist_ok=True)

    problem = <Prefix>Problem(config)
    # UniformSampler: scalar 1D bounds only.
    # UniformSampler2D: supports any dimension >= 2 (array bounds).
    sampler = UniformSampler(config, problem) if config.dimension == 1 else UniformSampler2D(config, problem)

    model = DGMNet(
        layer_width=config.nodes_per_layer,
        n_layers=config.num_layers,
        input_dim=config.dimension,
        output_dim=1,
        control_output=False,
        activation=config.activation,
    )
    control = DGMNet(
        layer_width=config.nodes_per_layer,
        n_layers=config.num_layers,
        input_dim=config.dimension,
        output_dim=config.num_controls,
        control_output=True,
        activation=config.activation,
    )

    loss_fn = <Prefix>Loss(problem)
    lr_schedule = config.get_optimizer_config()

    trainer = DGMTrainer(
        model=model,
        control=control,
        loss_fn=loss_fn,
        sampler=sampler,
        optimizer_value=tf.keras.optimizers.Adam(lr_schedule),
        optimizer_control=tf.keras.optimizers.Adam(lr_schedule),
        config=config,
        problem=problem,
    )

    history = trainer.train()
    if config.saveOutput:
        trainer.save_models(config.save_dir)

    csv_path = f"{config.save_dir}/{config.saveName}_training_history.csv"
    if os.path.exists(csv_path):
        plot_training_history(csv_path, config.save_dir)

    print('final maxdiff_V:', history['maxdiff_V'][-1])


if __name__ == '__main__':
    main()
```

### Step 7 — Fill the real PDE

In `<slug>/src/losses/<slug>_loss.py`, replace the placeholder body of `compute_value_loss` with the actual HJB residual. The return signature **must not change**: `return L1, L3, diff_V, diff_terminal`.

In `<slug>/src/problems/<slug>_problem.py`, implement `terminal_utility_<slug>` with the correct payoff.

See **"How to translate an HJB equation into loss functions"** below for the exact decomposition rule.

---

## How to translate an HJB equation into loss functions

Given an HJB equation with an inf (or sup) operator, split it into two losses following this fixed rule.

### The rule

| Loss | What to put in it |
|------|-------------------|
| `compute_value_loss` → `L1` | Drop the inf/sup symbol; substitute the **control network** output for u; sum **all** remaining terms into a residual; squared mean. |
| `compute_control_loss` → `L2` | Keep **only the terms inside** inf{…}; evaluate them with the **control network**; take the mean directly (no square). For sup{…}, negate first. |

The intuition: `L1` trains the value network so the PDE residual → 0 (equation is satisfied). `L2` trains the control network to actually minimise (or maximise) the Hamiltonian — it IS a gradient-descent step on the inf objective, so no squaring.

---



## Running the training

```bash
cd <slug>
python examples/<slug>_train.py
```

Results are saved to `<slug>/results/`.

---

## Common pitfall: GradientTape reuse



### Rule

**Always use `persistent=True` in both `compute_value_loss` and `compute_control_loss`.** Even if you think you only need one gradient today, problems that include `V_xx` (second-order / diffusion terms) require a nested tape inside `compute_control_loss`, which only works when the outer tape is persistent. Using `persistent=True` consistently prevents hard-to-diagnose errors.

| Method | Minimum gradients | Must use `persistent=True`? |
|---|---|---|
| `compute_value_loss` | `V_t` + `V_x` (2 gradients) | Yes |
| `compute_control_loss` | `V_x` + possibly `V_xx` via nested tape | Yes |

### `compute_value_loss` — always `persistent=True`

```python
with tf.GradientTape(persistent=True, watch_accessed_variables=False) as gt:
    gt.watch(t_interior)
    gt.watch(X_interior)
    V = model(t_interior, X_interior)
V_t = gt.gradient(V, t_interior)
V_x = gt.gradient(V, X_interior)
del gt  # required — frees memory held by persistent tape
```

### `compute_control_loss` — always `persistent=True`

```python
with tf.GradientTape(persistent=True, watch_accessed_variables=False) as gt:
    gt.watch(X_interior)
    V = model(t_interior, X_interior)
V_x = gt.gradient(V, X_interior)
del gt  # always delete, even if only one gradient was taken
```

Omitting `persistent=True` when computing two or more gradients raises:
```
RuntimeError: A non-persistent GradientTape can only be used to compute one set of gradients
```

---

## Guardrails
- Never modify `DGMTrainer`, `DGMNet`, or sampler internals.
- Keep all tensors as `tf.float32`.
- Never hardcode CSV column names in plotting code — detect control columns dynamically.

---

## Environment setup (before running)

If the user wants to run the training script, make sure the Python environment is correctly configured first.

### 1. Install dependencies

```bash
cd <slug>
pip install -r requirements.txt
```

`requirements.txt` includes: `tensorflow`, `numpy`, `matplotlib`, `tqdm`, `pandas`.

### 2. Verify TensorFlow can see the GPU (optional but recommended)

```python
import tensorflow as tf
print(tf.__version__)                        # should be >= 2.10
print(tf.config.list_physical_devices('GPU'))  # empty list = CPU-only mode
```

If GPU is available but not listed, install the matching `tensorflow-gpu` or `cuda`/`cudnn` version.

### 3. Run from the correct directory

The training script uses relative imports rooted at `<slug>/`. **Always `cd` into the problem folder first:**

```bash
cd <slug>
python examples/<slug>_train.py
```

Running from the workspace root will cause `ModuleNotFoundError` for `src.*`.

### 4. Results location

Output is written to `<slug>/results/` (configurable via `CommonConfig.save_dir`).  
CSV training history: `<slug>/results/<saveName>_training_history.csv`  
Saved models: `<slug>/results/<saveName>_value_model/` and `<slug>/results/<saveName>_control_model/`

