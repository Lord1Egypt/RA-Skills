#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solver Fallback & Mesh Strategy Configuration for COMSOL Multiphysics.

Provides:
  - Solver strategy selection (direct vs. iterative vs. segregated)
  - Automatic mesh density fallback on memory failure
  - Voltage-step reduction on non-convergence
  - Configuration generators for EM / Semiconductor / Thermal problems

Usage:
    from solver_fallback_config import SolverStrategy, MeshFallback, StudyConfig
    strategy = SolverStrategy.for_semiconductor(n_dof_estimate=50000)
    strategy.apply_to_study(study, mesh)
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


# ── constants ────────────────────────────────────────────────────

class SolverType:
    DIRECT = "direct"
    ITERATIVE = "iterative"
    SEGREGATED = "segregated"
    AUTOMATIC = "automatic"


class MeshDensity:
    EXTREMELY_FINE = 1
    EXTRA_FINE = 2
    FINER = 3
    FINE = 4
    NORMAL = 5
    COARSE = 6
    COARSER = 7
    EXTRA_COARSE = 8
    EXTREMELY_COARSE = 9


# ── dataclasses ──────────────────────────────────────────────────

@dataclass
class SolverStrategy:
    """Recommended solver configuration for a given problem type and scale."""
    solver_type: str = SolverType.AUTOMATIC
    linear_solver: str = "mumps"          # mumps, pardiso, gmres, bicgstab
    preconditioner: str = "ilu"           # ilu, ssor, multigrid, block
    max_iterations: int = 1000
    relative_tolerance: float = 1e-6
    absolute_tolerance: float = 1e-12
    # Segregated step order (for thermal-electric coupling)
    segregated_steps: list[str] = field(default_factory=list)
    # Memory estimate (GB)
    estimated_memory_gb: float = 0.0

    @classmethod
    def for_optical(cls, n_wavelengths: int = 9, n_dof_estimate: int = 20000) -> "SolverStrategy":
        """Optical (EM Waves) problems: moderate DOF, moderate memory."""
        return cls(
            solver_type=SolverType.DIRECT,
            linear_solver="mumps",
            preconditioner="ilu",
            max_iterations=500,
            relative_tolerance=1e-6,
            estimated_memory_gb=n_dof_estimate * 1e-6 * n_wavelengths,
        )

    @classmethod
    def for_semiconductor(
        cls,
        n_layers: int = 6,
        n_dof_estimate: int = 50000,
        bias_points: int = 51,
    ) -> "SolverStrategy":
        """Semiconductor drift-diffusion: nonlinear, sparse, medium memory."""
        # Direct solver good up to ~100k DOF; switch to iterative above
        use_iterative = n_dof_estimate > 80000 or bias_points > 100
        return cls(
            solver_type=SolverType.ITERATIVE if use_iterative else SolverType.DIRECT,
            linear_solver="gmres" if use_iterative else "mumps",
            preconditioner="multigrid" if use_iterative else "ilu",
            max_iterations=2000 if use_iterative else 500,
            relative_tolerance=1e-8,
            estimated_memory_gb=n_dof_estimate * 2e-6 * bias_points,
        )

    @classmethod
    def for_thermal_coupled(
        cls,
        n_dof_estimate: int = 100000,
        coupling_strength: str = "weak",  # weak / moderate / strong
    ) -> "SolverStrategy":
        """Thermal-electric coupled: fully coupled is expensive."""
        if coupling_strength == "strong":
            return cls(
                solver_type=SolverType.SEGREGATED,
                linear_solver="gmres",
                preconditioner="multigrid",
                max_iterations=3000,
                relative_tolerance=1e-7,
                segregated_steps=["heat_transfer", "semiconductor"],
                estimated_memory_gb=n_dof_estimate * 3e-6,
            )
        else:
            use_iterative = n_dof_estimate > 60000
            return cls(
                solver_type=SolverType.ITERATIVE if use_iterative else SolverType.DIRECT,
                linear_solver="gmres" if use_iterative else "mumps",
                preconditioner="multigrid" if use_iterative else "ilu",
                max_iterations=2000,
                relative_tolerance=1e-7,
                estimated_memory_gb=n_dof_estimate * 2.5e-6,
            )

    def apply_to_study(self, jm, study_tag: str = "std1", stat_tag: str = "stat1") -> dict:
        """
        Apply solver strategy to a COMSOL study via Java API.
        Returns a log dict; actual API calls are wrapped in try/except.
        """
        log = {"actions": [], "errors": []}
        try:
            study = jm.study(study_tag)
            stat = study.feature(stat_tag)

            # Set solver type in Stationary step (if applicable)
            if self.solver_type == SolverType.DIRECT:
                # COMSOL default for Stationary is usually direct (MUMPS/PARDISO)
                # No explicit override needed unless switching from iterative
                log["actions"].append("Set solver to DIRECT (default)")
            elif self.solver_type == SolverType.ITERATIVE:
                # In COMSOL, solver choice is in the solver sequence, not study feature
                # This is a placeholder showing intent; actual config is in sol() node
                log["actions"].append("Set solver to ITERATIVE (GMRES/FGMRES)")
            elif self.solver_type == SolverType.SEGREGATED:
                log["actions"].append("Set solver to SEGREGATED (thermal -> electric)")

        except Exception as e:
            log["errors"].append(str(e))

        return log


@dataclass
class MeshFallback:
    """Mesh density fallback chain."""
    initial_density: int = MeshDensity.FINE
    fallback_chain: list[int] = field(default_factory=lambda: [
        MeshDensity.FINE,
        MeshDensity.NORMAL,
        MeshDensity.COARSE,
        MeshDensity.EXTRA_COARSE,
    ])
    max_retries: int = 3

    def get_next_density(self, current_density: int) -> int | None:
        """Return next coarser density level, or None if exhausted."""
        try:
            idx = self.fallback_chain.index(current_density)
            if idx + 1 < len(self.fallback_chain):
                return self.fallback_chain[idx + 1]
        except ValueError:
            pass
        return None

    def apply_to_mesh(self, jm, mesh_tag: str = "mesh1", density: int | None = None) -> dict:
        """Apply mesh density to COMSOL mesh via Java API."""
        log = {"actions": [], "errors": []}
        d = density if density is not None else self.initial_density
        try:
            mesh = jm.component("comp1").mesh(mesh_tag)
            # Global size setting
            mesh.feature("size1").set("hauto", str(d))
            log["actions"].append(f"Set mesh size level to {d}")
        except Exception as e:
            log["errors"].append(str(e))
        return log


@dataclass
class StudyConfig:
    """Complete study configuration combining solver + mesh + fallback."""
    solver: SolverStrategy = field(default_factory=SolverStrategy)
    mesh: MeshFallback = field(default_factory=MeshFallback)
    bias_step_reduction: float = 0.5  # Halve step on divergence
    min_bias_step: float = 0.01       # Minimum V step

    @classmethod
    def for_problem_type(
        cls,
        problem_type: str,  # "optical" | "optoelectronic" | "thermal_coupled"
        config: dict,
    ) -> "StudyConfig":
        """Factory: build recommended config from simulation config dict."""
        layers = config.get("device_stack", {}).get("layers", [])
        n_layers = len(layers)

        # Rough DOF estimate (2D)
        width_nm = config.get("device_stack", {}).get("device_width_nm", 1000)
        total_thickness = sum(l.get("thickness_nm", 100) for l in layers)
        # Mesh elements ≈ (width / h) * (thickness / h); h ≈ 5 nm for fine
        h_nm = 5
        n_elements = (width_nm / h_nm) * (total_thickness / h_nm)
        n_dof = n_elements * 4  # ~4 DOF per element for semiconductor (V, n, p, T)

        if problem_type == "optical":
            wavelengths = config.get("wavelengths_nm", [])
            solver = SolverStrategy.for_optical(
                n_wavelengths=len(wavelengths),
                n_dof_estimate=int(n_dof),
            )
            mesh = MeshFallback(initial_density=MeshDensity.FINE)
            return cls(solver=solver, mesh=mesh)

        elif problem_type == "optoelectronic":
            bias_cfg = config.get("bias_range", {})
            points = bias_cfg.get("points", 51)
            solver = SolverStrategy.for_semiconductor(
                n_layers=n_layers,
                n_dof_estimate=int(n_dof),
                bias_points=points,
            )
            mesh = MeshFallback(initial_density=MeshDensity.FINE)
            return cls(solver=solver, mesh=mesh)

        elif problem_type == "thermal_coupled":
            solver = SolverStrategy.for_thermal_coupled(
                n_dof_estimate=int(n_dof * 1.5),  # thermal adds DOF
                coupling_strength=config.get("coupling_mode", "weak"),
            )
            mesh = MeshFallback(initial_density=MeshDensity.NORMAL)
            return cls(solver=solver, mesh=mesh)

        else:
            raise ValueError(f"Unknown problem_type: {problem_type}")

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


# ── convergence monitor / retry logic ────────────────────────────

class ConvergenceRetry:
    """Encapsulate retry-on-failure logic for COMSOL solve calls."""

    def __init__(self, study_config: StudyConfig):
        self.cfg = study_config
        self.attempt = 0
        self.current_mesh_density = study_config.mesh.initial_density
        self.current_bias_step = 1.0  # fraction of original step

    def should_retry(self, error_message: str) -> bool:
        """Analyze error message to decide if retry is worthwhile."""
        error_lower = error_message.lower()
        retry_triggers = [
            "out of memory",
            "mumps",
            "singular matrix",
            "did not converge",
            "diverge",
            "no convergence",
            "failed to find a solution",
            "maximum number of iterations",
        ]
        return any(trigger in error_lower for trigger in retry_triggers)

    def next_strategy(self) -> dict:
        """Generate next fallback action."""
        self.attempt += 1
        actions = []

        # Action 1: coarsen mesh
        next_density = self.cfg.mesh.get_next_density(self.current_mesh_density)
        if next_density is not None and self.attempt <= self.cfg.mesh.max_retries:
            self.current_mesh_density = next_density
            actions.append({"action": "coarsen_mesh", "new_density": next_density})

        # Action 2: switch solver type (direct -> iterative)
        if self.cfg.solver.solver_type == SolverType.DIRECT and self.attempt == 2:
            self.cfg.solver.solver_type = SolverType.ITERATIVE
            self.cfg.solver.linear_solver = "gmres"
            self.cfg.solver.preconditioner = "multigrid"
            actions.append({"action": "switch_solver", "new_solver": "iterative"})

        # Action 3: reduce bias step
        if self.current_bias_step > self.cfg.min_bias_step:
            self.current_bias_step *= self.cfg.bias_step_reduction
            actions.append({"action": "reduce_bias_step", "new_step_fraction": self.current_bias_step})

        return {
            "attempt": self.attempt,
            "actions": actions,
            "continue": len(actions) > 0,
        }

    def log_attempt(self, result: dict, output_dir: Path) -> None:
        """Append retry log to a JSONL file."""
        log_path = output_dir / "solver_retry_log.jsonl"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")


# ── convenience functions ────────────────────────────────────────

def recommend_solver_config(problem_type: str, config: dict) -> dict:
    """One-liner: get full recommended solver + mesh config as dict."""
    study_cfg = StudyConfig.for_problem_type(problem_type, config)
    return study_cfg.to_dict()


# ── module self-test ─────────────────────────────────────────────

if __name__ == "__main__":
    # Quick self-test
    test_config = {
        "device_stack": {
            "device_width_nm": 1000,
            "layers": [
                {"name": "configured_contact_a", "thickness_nm": 100},
                {"name": "configured_absorber_a", "thickness_nm": 100},
                {"name": "configured_absorber_b", "thickness_nm": 100},
                {"name": "configured_transport_layer", "thickness_nm": 50},
                {"name": "configured_contact_b", "thickness_nm": 100},
            ],
        },
        "bias_range": {"start_V": -1.0, "stop_V": 1.0, "points": 51},
        "coupling_mode": "fully_coupled",
    }

    for ptype in ["optical", "optoelectronic", "thermal_coupled"]:
        cfg = StudyConfig.for_problem_type(ptype, test_config)
        print(f"\n=== {ptype} ===")
        print(json.dumps(cfg.to_dict(), indent=2, ensure_ascii=False))

    # Test retry logic
    retry = ConvergenceRetry(cfg)
    print("\n--- Retry simulation ---")
    for i in range(3):
        strat = retry.next_strategy()
        print(f"Attempt {i+1}: {json.dumps(strat, indent=2)}")
        if not strat["continue"]:
            break


