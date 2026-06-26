#!/usr/bin/env python3
"""
DeepSpeed Training Monitor
Monitor training progress, plot metrics, and analyze checkpoints.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np


class TrainingMonitor:
    """Monitor and analyze DeepSpeed training progress."""
    
    def __init__(self, log_dir: str):
        """
        Initialize training monitor.
        
        Args:
            log_dir: Directory containing training logs and checkpoints
        """
        self.log_dir = Path(log_dir)
        self.metrics_history: List[Dict[str, Any]] = []
        
    def load_metrics(self) -> Dict[str, Any]:
        """Load training metrics from logs."""
        
        metrics = {}
        
        # Load trainer_state.json if available
        trainer_state_path = self.log_dir / "trainer_state.json"
        if trainer_state_path.exists():
            with open(trainer_state_path, "r") as f:
                trainer_state = json.load(f)
                metrics.update(trainer_state.get("log_history", []))
        
        # Load train_results.json if available
        train_results_path = self.log_dir / "train_results.json"
        if train_results_path.exists():
            with open(train_results_path, "r") as f:
                train_results = json.load(f)
                metrics["final"] = train_results
        
        # Load eval_results.json if available
        eval_results_path = self.log_dir / "eval_results.json"
        if eval_results_path.exists():
            with open(eval_results_path, "r") as f:
                eval_results = json.load(f)
                metrics["evaluation"] = eval_results
        
        return metrics
    
    def get_checkpoints(self) -> List[str]:
        """Get list of checkpoint directories."""
        
        checkpoints = []
        for item in self.log_dir.iterdir():
            if item.is_dir() and item.name.startswith("checkpoint-"):
                checkpoints.append(str(item))
        
        checkpoints.sort(key=lambda x: int(Path(x).name.split("-")[1]))
        return checkpoints
    
    def get_latest_checkpoint(self) -> Optional[str]:
        """Get the latest checkpoint directory."""
        
        checkpoints = self.get_checkpoints()
        return checkpoints[-1] if checkpoints else None
    
    def get_best_checkpoint(self, metric: str = "eval_loss") -> Optional[str]:
        """
        Get checkpoint with best metric value.
        
        Args:
            metric: Metric name to optimize (default: eval_loss, lower is better)
        """
        
        best_checkpoint = None
        best_value = float("inf")
        
        for ckpt_dir in self.get_checkpoints():
            trainer_state_path = Path(ckpt_dir) / "trainer_state.json"
            if trainer_state_path.exists():
                with open(trainer_state_path, "r") as f:
                    state = json.load(f)
                    for log in state.get("log_history", []):
                        if metric in log:
                            if log[metric] < best_value:
                                best_value = log[metric]
                                best_checkpoint = ckpt_dir
        
        return best_checkpoint
    
    def plot_loss(self, output_path: Optional[str] = None):
        """
        Plot training loss over time.
        
        Args:
            output_path: Path to save plot (optional)
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Matplotlib not installed. Install with: pip install matplotlib")
            return
        
        metrics = self.load_metrics()
        
        if isinstance(metrics, dict) and "log_history" not in metrics:
            print("No training metrics found")
            return
        
        if isinstance(metrics, dict) and "log_history" in metrics:
            logs = metrics["log_history"]
        else:
            logs = metrics
        
        # Extract loss values
        steps = []
        train_losses = []
        eval_losses = []
        
        for log in logs:
            if "step" in log:
                steps.append(log["step"])
                if "loss" in log:
                    train_losses.append(log["loss"])
                else:
                    train_losses.append(None)
                
                if "eval_loss" in log:
                    eval_losses.append(log["eval_loss"])
                else:
                    eval_losses.append(None)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if steps:
            # Plot training loss
            train_loss_values = [loss if loss is not None else np.nan for loss in train_losses]
            ax.plot(steps, train_loss_values, label="Train Loss", alpha=0.7)
            
            # Plot evaluation loss
            eval_loss_values = [loss if loss is not None else np.nan for loss in eval_losses]
            ax.plot(steps, eval_loss_values, "o-", label="Eval Loss", markersize=6)
        
        ax.set_xlabel("Step")
        ax.set_ylabel("Loss")
        ax.set_title("Training Progress")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            print(f"Plot saved to: {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def print_summary(self):
        """Print training summary."""
        
        metrics = self.load_metrics()
        checkpoints = self.get_checkpoints()
        
        print("=" * 60)
        print("Training Summary")
        print("=" * 60)
        print(f"Log Directory: {self.log_dir}")
        print(f"Number of Checkpoints: {len(checkpoints)}")
        
        if checkpoints:
            print(f"Latest Checkpoint: {checkpoints[-1]}")
            best_ckpt = self.get_best_checkpoint()
            if best_ckpt:
                print(f"Best Checkpoint (eval_loss): {best_ckpt}")
        
        print("\nFinal Metrics:")
        if isinstance(metrics, dict) and "final" in metrics:
            for key, value in metrics["final"].items():
                print(f"  {key}: {value}")
        
        print("\nEvaluation Metrics:")
        if isinstance(metrics, dict) and "evaluation" in metrics:
            for key, value in metrics["evaluation"].items():
                print(f"  {key}: {value}")
        
        print("=" * 60)
    
    def get_training_time(self) -> Optional[float]:
        """Get total training time in seconds."""
        
        trainer_state_path = self.log_dir / "trainer_state.json"
        if not trainer_state_path.exists():
            return None
        
        with open(trainer_state_path, "r") as f:
            state = json.load(f)
        
        logs = state.get("log_history", [])
        if not logs:
            return None
        
        # Find last log with epoch information
        for log in reversed(logs):
            if "train_runtime" in log:
                return log["train_runtime"]
        
        return None
    
    def estimate_remaining_time(self, current_step: int, total_steps: int) -> Optional[float]:
        """
        Estimate remaining training time.
        
        Args:
            current_step: Current training step
            total_steps: Total training steps
            
        Returns:
            Estimated remaining time in seconds
        """
        
        trainer_state_path = self.log_dir / "trainer_state.json"
        if not trainer_state_path.exists():
            return None
        
        with open(trainer_state_path, "r") as f:
            state = json.load(f)
        
        logs = state.get("log_history", [])
        
        # Find training start time
        start_time = None
        for log in logs:
            if "train_runtime" in log:
                start_time = log.get("epoch_end_time", None)
                break
        
        if not start_time:
            return None
        
        # Estimate based on current progress
        elapsed_time = self.get_training_time()
        if elapsed_time is None:
            return None
        
        progress = current_step / total_steps
        if progress > 0:
            remaining_time = elapsed_time / progress - elapsed_time
            return remaining_time
        
        return None


def main():
    parser = argparse.ArgumentParser(description="DeepSpeed Training Monitor")
    
    parser.add_argument("--log-dir", type=str, required=True,
                        help="Directory containing training logs")
    parser.add_argument("--plot", action="store_true",
                        help="Generate loss plot")
    parser.add_argument("--plot-output", type=str, default=None,
                        help="Path to save plot")
    parser.add_argument("--checkpoints", action="store_true",
                        help="List all checkpoints")
    parser.add_argument("--best-checkpoint", action="store_true",
                        help="Get best checkpoint")
    parser.add_argument("--metric", type=str, default="eval_loss",
                        help="Metric for best checkpoint selection")
    parser.add_argument("--summary", action="store_true",
                        help="Print training summary")
    
    args = parser.parse_args()
    
    monitor = TrainingMonitor(args.log_dir)
    
    if args.summary:
        monitor.print_summary()
    
    if args.checkpoints:
        checkpoints = monitor.get_checkpoints()
        print(f"\nCheckpoints ({len(checkpoints)}):")
        for ckpt in checkpoints:
            print(f"  - {ckpt}")
    
    if args.best_checkpoint:
        best = monitor.get_best_checkpoint(args.metric)
        if best:
            print(f"\nBest checkpoint ({args.metric}): {best}")
        else:
            print(f"\nNo checkpoint found with metric: {args.metric}")
    
    if args.plot:
        monitor.plot_loss(args.plot_output)
    
    if not any([args.plot, args.checkpoints, args.best_checkpoint, args.summary]):
        # Default: print summary
        monitor.print_summary()


if __name__ == "__main__":
    main()
