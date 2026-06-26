"""Deep Galerkin Method Trainer."""

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tqdm import tqdm


class DGMTrainer:
    """Trainer for Deep Galerkin Method."""
    
    def __init__(self, model, control, loss_fn, sampler, 
                 optimizer_value, optimizer_control, config, problem):
        """
        Initialize DGM trainer.
        
        Args:
            model: Value function network
            control: Control network
            loss_fn: Loss function object
            sampler: Sampling strategy object
            optimizer_value: Optimizer for value network
            optimizer_control: Optimizer for control network
            config: Configuration object
            problem: Problem object (defines metrics and output format)
        """
        self.model = model
        self.control = control
        self.loss_fn = loss_fn
        self.sampler = sampler
        self.optimizer_value = optimizer_value
        self.optimizer_control = optimizer_control
        self.config = config
        self.problem = problem
        
        # Training history - get metric names from problem
        self.history = {
            'stage': [],
            'loss_total': [],
            'loss_L1': [],
            'loss_L2': [],
            'loss_L3': [],
        }
        
        # Add problem-specific metrics
        for metric_name in problem.get_metrics_config():
            self.history[metric_name] = []
        
        # Add V_at_origin
        self.history['V_at_origin'] = []
        
        # Add control columns
        for control_name in problem.get_control_names():
            self.history[control_name] = []
    
    @tf.function
    def train_step(self, t_interior, X_interior, t_terminal, X_terminal):
        """
        Perform single training step.
        
        Args:
            t_interior: Interior time points
            X_interior: Interior space points
            t_terminal: Terminal time points
            X_terminal: Terminal space points
            
        Returns:
            Tuple of loss values
        """
        t_interior = tf.convert_to_tensor(t_interior, dtype=tf.float32)
        X_interior = tf.convert_to_tensor(X_interior, dtype=tf.float32)
        t_terminal = tf.convert_to_tensor(t_terminal, dtype=tf.float32)
        X_terminal = tf.convert_to_tensor(X_terminal, dtype=tf.float32)
        
        # Update value function
        with tf.GradientTape() as tape1:
            L1, L3, diff_V, diff_terminal = self.loss_fn.compute_value_loss(
                self.model, self.control,
                t_interior, X_interior,
                t_terminal, X_terminal
            )
            total_loss = L1 + L3
        
        grads = tape1.gradient(total_loss, self.model.trainable_variables)
        self.optimizer_value.apply_gradients(
            zip(grads, self.model.trainable_variables)
        )
        
        # Update control
        with tf.GradientTape() as tape2:
            L2, extra_info = self.loss_fn.compute_control_loss(
                self.model, self.control,
                t_interior, X_interior,
                t_terminal, X_terminal
            )
        
        grads_control = tape2.gradient(L2, self.control.trainable_variables)
        self.optimizer_control.apply_gradients(
            zip(grads_control, self.control.trainable_variables)
        )
        
        return L1, L3, diff_V, diff_terminal, L2, total_loss
    
    @tf.function
    def eval_step(self, t_interior_val, X_interior_val, 
                  t_terminal_val, X_terminal_val):
        """
        Perform evaluation step.
        
        Args:
            t_interior_val: Validation interior time points
            X_interior_val: Validation interior space points
            t_terminal_val: Validation terminal time points
            X_terminal_val: Validation terminal space points
            
        Returns:
            Tuple of validation metrics
        """
        L1_val, L3_val, diff_V_val, diff_terminal_val = \
            self.loss_fn.compute_value_loss(
                self.model, self.control,
                t_interior_val, X_interior_val,
                t_terminal_val, X_terminal_val
            )
        
        L2_val, extra_info = \
            self.loss_fn.compute_control_loss(
                self.model, self.control,
                t_interior_val, X_interior_val,
                t_terminal_val, X_terminal_val
            )
        
        return (L1_val, L3_val, diff_V_val, diff_terminal_val,
                L2_val, extra_info)
    
    def train(self):
        """Main training loop."""
        t_eval = tf.constant([[0.0]], dtype=tf.float32)
        # Set X_eval based on problem dimension
        if self.config.dimension == 1:
            X_eval = tf.constant([[0.0]], dtype=tf.float32)
        else:  # 2D
            X_eval = tf.constant([[1.0, 0.0]], dtype=tf.float32)
        
        pbar = tqdm(range(self.config.sampling_stages), desc="Training")
        
        for i in pbar:
            # Sample training data
            t_interior, X_interior, t_terminal, X_terminal = \
                self.sampler.sample(
                    self.config.nSim_interior,
                    self.config.nSim_terminal
                )
            
            # Multiple SGD steps per sample
            for _ in range(self.config.steps_per_sample):
                L1, L3, diff_V, diff_terminal, L2, total_loss = \
                    self.train_step(
                        t_interior, X_interior,
                        t_terminal, X_terminal
                    )
            
            # Validation
            t_interior_val, X_interior_val, t_terminal_val, X_terminal_val = \
                self.sampler.sample(
                    self.config.nSim_interior,
                    self.config.nSim_terminal
                )
            
            t_interior_val = tf.convert_to_tensor(t_interior_val, dtype=tf.float32)
            X_interior_val = tf.convert_to_tensor(X_interior_val, dtype=tf.float32)
            t_terminal_val = tf.convert_to_tensor(t_terminal_val, dtype=tf.float32)
            X_terminal_val = tf.convert_to_tensor(X_terminal_val, dtype=tf.float32)
            
            validation_results = self.eval_step(
                t_interior_val, X_interior_val,
                t_terminal_val, X_terminal_val
            )
            
            # Extract problem-specific metrics
            metrics = self.problem.extract_metrics(
                validation_results, t_eval, X_eval, 
                self.model, self.control
            )
            
            # Record stage number
            self.history['stage'].append(i)
            
            # Record losses
            self.history['loss_total'].append(float(total_loss.numpy()))
            self.history['loss_L1'].append(float(L1.numpy()))
            self.history['loss_L2'].append(float(L2.numpy()))
            self.history['loss_L3'].append(float(L3.numpy()))
            
            # Record all metrics from problem
            for metric_name, metric_value in metrics.items():
                if metric_name in self.history:
                    self.history[metric_name].append(float(metric_value))
            
            # Update progress bar
            pbar.set_postfix({
                'maxdiff_V': f'{metrics["maxdiff_V"]:.4e}',
                'L1': f'{L1.numpy():.4e}',
                'L2': f'{L2.numpy():.4e}'
            })
            
            # Print detailed info periodically
            if i % 100 == 0:
                losses = {
                    'L1': L1.numpy(),
                    'L2': L2.numpy(),
                    'L3': L3.numpy()
                }
                
                # Use problem-specific formatting or default
                stage_info = self.problem.format_stage_info(i, metrics, losses)
                if stage_info:
                    print(stage_info)
                else:
                    # Default formatting
                    print(f"\nStage {i}:")
                    print(f"  L1={L1.numpy():.4e}, L2={L2.numpy():.4e}, L3={L3.numpy():.4e}")
                    for key, val in metrics.items():
                        print(f"  {key}={val:.4e}")
            
            # Early stopping check (defined by Problem)
            if self.problem.check_early_stopping(metrics, i):
                print(f"\nConverged at stage {i}!")
                break
        
        # Save training history to CSV
        if self.config.saveOutput:
            self.save_history_csv()
        
        return self.history
    
    def save_models(self, save_dir):
        """
        Save trained models.
        
        Args:
            save_dir: Directory to save models
        """
        os.makedirs(save_dir, exist_ok=True)
        self.model.save_weights(f'{save_dir}/model_value.weights.h5')
        self.control.save_weights(f'{save_dir}/model_control.weights.h5')
        print(f"Models saved to {save_dir}")
    
    def save_history_csv(self):
        """Save training history to CSV file."""
        save_dir = self.config.save_dir
        os.makedirs(save_dir, exist_ok=True)
        
        # Convert history dict to DataFrame
        df = pd.DataFrame(self.history)
        
        # Save to CSV
        csv_path = os.path.join(save_dir, f'{self.config.saveName}_training_history.csv')
        df.to_csv(csv_path, index=False)
        print(f"Training history saved to {csv_path}")
        
        # Also save a summary statistics file
        summary = {
            'metric': [],
            'final_value': [],
            'min_value': [],
            'max_value': [],
            'mean_value': []
        }
        
        # Summarize losses
        for key in ['loss_total', 'loss_L1', 'loss_L2', 'loss_L3']:
            if key in df.columns:
                summary['metric'].append(key)
                summary['final_value'].append(df[key].iloc[-1])
                summary['min_value'].append(df[key].min())
                summary['max_value'].append(df[key].max())
                summary['mean_value'].append(df[key].mean())
        
        # Summarize problem-specific metrics
        for metric_name in self.problem.get_metrics_config():
            if metric_name in df.columns:
                summary['metric'].append(metric_name)
                summary['final_value'].append(df[metric_name].iloc[-1])
                summary['min_value'].append(df[metric_name].min())
                summary['max_value'].append(df[metric_name].max())
                summary['mean_value'].append(df[metric_name].mean())
        
        summary_df = pd.DataFrame(summary)
        summary_path = os.path.join(save_dir, f'{self.config.saveName}_training_summary.csv')
        summary_df.to_csv(summary_path, index=False)
        print(f"Training summary saved to {summary_path}")
    
    def load_models(self, save_dir):
        """
        Load trained models.
        
        Args:
            save_dir: Directory to load models from
        """
        self.model.load_weights(f'{save_dir}/model_value.weights.h5')
        self.control.load_weights(f'{save_dir}/model_control.weights.h5')
        print(f"Models loaded from {save_dir}")
