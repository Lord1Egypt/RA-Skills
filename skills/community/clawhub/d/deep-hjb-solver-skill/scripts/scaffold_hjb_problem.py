"""Scaffold a new HJB problem module set for this repository.

Usage:
python .github/skills/deep-hjb-solver/scripts/scaffold_hjb_problem.py \
  --name example_4 --dimension 2 --num-controls 2 --control-names Z,W
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def bootstrap_framework(repo_root: Path) -> None:
    """Copy bundled DGM framework into repo_root if src/ is absent."""
    if (repo_root / "src").exists():
        return
    assets = Path(__file__).resolve().parent.parent / "assets"
    if not assets.exists():
        raise FileNotFoundError(
            f"Cannot find bundled assets at {assets}. "
            "Please copy assets/src/ manually to your repo root."
        )
    shutil.copytree(assets / "src", repo_root / "src")
    for name in ("plot_training_csv.py", "requirements.txt"):
        src_file = assets / name
        dst_file = repo_root / name
        if src_file.exists() and not dst_file.exists():
            shutil.copy2(src_file, dst_file)
    print("[bootstrap] Copied DGM framework to src/")
    print("[bootstrap] Run: pip install -r requirements.txt")


def snake_to_camel(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"File already exists: {path}")
    path.write_text(content, encoding="utf-8")


def build_config(module_slug: str, class_prefix: str, dimension: int, num_controls: int, control_names: list[str]) -> str:
    if dimension == 1:
        x_bounds = "    X_low: float = 0.0\n    X_high: float = 1.0"
    else:
        zeros = [0.0] * dimension
        ones = [1.0] * dimension
        x_bounds = (
            f"    X_low: list = field(default_factory=lambda: {zeros!r})\n"
            f"    X_high: list = field(default_factory=lambda: {ones!r})"
        )
    return f'''"""Configuration for {class_prefix}."""

from dataclasses import dataclass, field
from .common_config import CommonConfig


@dataclass
class {class_prefix}Config(CommonConfig):
    """Configuration for {class_prefix}."""

    dimension: int = {dimension}
    T: float = 1.0
    t_low: float = 0.0
{x_bounds}

    num_controls: int = {num_controls}
    control_names: list = field(default_factory=lambda: {control_names!r})
    metrics_config: list = field(default_factory=lambda: ['maxdiff_V', 'maxdiff_terminal'])
    extra_info_mapping: dict = field(default_factory=dict)
    early_stop_metric: str = 'maxdiff_V'
    early_stop_threshold: float = 1e-4
    problem_params_keys: list = field(default_factory=list)

    saveName: str = '{module_slug}'
'''


def build_problem(class_prefix: str) -> str:
    return f'''"""Problem definition for {class_prefix}."""

from .base_problem import BaseProblem


def terminal_utility_{class_prefix.lower()}(x):
    """TODO: define terminal utility g(x)."""
    return -x[:, :1]


class {class_prefix}Problem(BaseProblem):
    """Problem class for {class_prefix}."""

    def get_terminal_condition(self, x):
        return terminal_utility_{class_prefix.lower()}(x)
'''


def build_loss(class_prefix: str) -> str:
    return f'''"""Loss functions for {class_prefix}."""

import tensorflow as tf


class {class_prefix}Loss:
    """Loss functions for {class_prefix}."""

    def __init__(self, problem):
        self.problem = problem

    def compute_value_loss(self, model, control, t_interior, X_interior, t_terminal, X_terminal):
        # TODO: replace with real HJB residual
        with tf.GradientTape(watch_accessed_variables=False) as gt:
            gt.watch(t_interior)
            V = model(t_interior, X_interior)
        V_t = gt.gradient(V, t_interior)
        diff_V = V_t
        L1 = tf.reduce_mean(tf.square(diff_V))

        target_terminal = self.problem.get_terminal_condition(X_terminal)
        fitted_terminal = model(t_terminal, X_terminal)
        diff_terminal = fitted_terminal - target_terminal
        L3 = tf.reduce_mean(tf.square(diff_terminal))
        return L1, L3, diff_V, diff_terminal

    def compute_control_loss(self, model, control, t_interior, X_interior, t_terminal, X_terminal):
        # TODO: replace with real control objective and FOC residual
        ctrl = control(t_interior, X_interior)
        L2 = tf.reduce_mean(tf.square(ctrl))
        return L2, {{}}
'''


def build_example(module_slug: str, class_prefix: str) -> str:
    return f'''"""Training script for {module_slug}."""

import os
import tensorflow as tf

from src.configs.{module_slug}_config import {class_prefix}Config
from src.problems.{module_slug}_problem import {class_prefix}Problem
from src.losses.{module_slug}_loss import {class_prefix}Loss
from src.models import DGMNet
from src.samplers import UniformSampler, UniformSampler2D
from src.trainers import DGMTrainer
from plot_training_csv import plot_training_history


def main():
    config = {class_prefix}Config()
    config.save_dir = './results/{module_slug}'
    os.makedirs(config.save_dir, exist_ok=True)

    problem = {class_prefix}Problem(config)
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

    loss_fn = {class_prefix}Loss(problem)

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

    csv_path = f"{{config.save_dir}}/{{config.saveName}}_training_history.csv"
    if os.path.exists(csv_path):
        plot_training_history(csv_path, config.save_dir)

    print('final maxdiff_V:', history['maxdiff_V'][-1])


if __name__ == '__main__':
    main()
'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold HJB files for a new problem.")
    parser.add_argument("--name", required=True, help="Problem slug, e.g. example_4")
    parser.add_argument("--dimension", type=int, required=True, choices=[1, 2])
    parser.add_argument("--num-controls", type=int, required=True)
    parser.add_argument("--control-names", required=True, help="Comma-separated control names, e.g. Z,W")
    args = parser.parse_args()

    module_slug = args.name.strip().lower()
    class_prefix = snake_to_camel(module_slug)
    control_names = [c.strip() for c in args.control_names.split(",") if c.strip()]

    if len(control_names) != args.num_controls:
        raise ValueError("num-controls must match number of control-names")

    # Ensure DGM framework is present; copy from bundled assets if not.
    repo_root = Path.cwd()
    bootstrap_framework(repo_root)

    write_file(
        repo_root / "src" / "configs" / f"{module_slug}_config.py",
        build_config(module_slug, class_prefix, args.dimension, args.num_controls, control_names),
    )
    write_file(
        repo_root / "src" / "problems" / f"{module_slug}_problem.py",
        build_problem(class_prefix),
    )
    write_file(
        repo_root / "src" / "losses" / f"{module_slug}_loss.py",
        build_loss(class_prefix),
    )
    write_file(
        repo_root / "examples" / f"{module_slug}_train.py",
        build_example(module_slug, class_prefix),
    )

    print("Scaffold completed:")
    print(f"  src/configs/{module_slug}_config.py")
    print(f"  src/problems/{module_slug}_problem.py")
    print(f"  src/losses/{module_slug}_loss.py")
    print(f"  examples/{module_slug}_train.py")
    print()
    print("Next steps:")
    print(f"  1. Add 'from .{module_slug}_config import {class_prefix}Config' to src/configs/__init__.py")
    print(f"  2. Add 'from .{module_slug}_problem import {class_prefix}Problem' to src/problems/__init__.py")
    print(f"  3. Add 'from .{module_slug}_loss import {class_prefix}Loss' to src/losses/__init__.py")
    print("  4. Fill TODO blocks in the generated loss and problem files.")


if __name__ == "__main__":
    main()
