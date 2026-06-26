"""Plot training history exported by DGMTrainer CSV."""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def plot_training_history(csv_path, output_dir=None):
    """
    Plot training history from CSV file.
    
    Args:
        csv_path: Path to training history CSV
        output_dir: Directory to save plots (optional)
    """
    # Read CSV
    df = pd.read_csv(csv_path)
    
    if output_dir is None:
        output_dir = os.path.dirname(csv_path)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Plot 1: Loss curves and key states
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Total loss
    axes[0, 0].plot(df['stage'], df['loss_total'])
    axes[0, 0].set_xlabel('Stage')
    axes[0, 0].set_ylabel('Total Loss')
    axes[0, 0].set_title('Total Loss')
    axes[0, 0].set_yscale('log')
    axes[0, 0].grid(True)
    
    # L1, L2, L3
    axes[0, 1].plot(df['stage'], df['loss_L1'], label='L1 (HJB)')
    axes[0, 1].plot(df['stage'], df['loss_L2'].abs(), label='|L2| (FOC)')
    axes[0, 1].plot(df['stage'], df['loss_L3'], label='L3 (Terminal)')
    axes[0, 1].set_xlabel('Stage')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].set_title('Loss Components')
    axes[0, 1].legend()
    axes[0, 1].set_yscale('log')
    axes[0, 1].grid(True)
    
    # Value function at origin
    axes[1, 0].plot(df['stage'], df['V_at_origin'])
    axes[1, 0].set_xlabel('Stage')
    axes[1, 0].set_ylabel('V(0,0)')
    axes[1, 0].set_title('Value Function at Origin')
    axes[1, 0].grid(True)
    
    # Dynamic controls at origin (all non-core columns)
    core_cols = {
        'stage', 'loss_total', 'loss_L1', 'loss_L2', 'loss_L3',
        'maxdiff_V', 'maxdiff_terminal', 'max_foc_residual',
        'max_control_bound', 'max_penalty', 'V_at_origin'
    }
    control_cols = [col for col in df.columns if col not in core_cols]
    for col in control_cols:
        axes[1, 1].plot(df['stage'], df[col], label=f'{col}(origin)')
    axes[1, 1].set_xlabel('Stage')
    axes[1, 1].set_ylabel('Control Value')
    axes[1, 1].set_title('Control Variables at Origin')
    if control_cols:
        axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'training_history.png')
    plt.savefig(plot_path, dpi=150)
    print(f"Saved: {plot_path}")
    plt.close()
    
    # Plot 2: Residuals
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # HJB residual
    axes[0].plot(df['stage'], df['maxdiff_V'])
    axes[0].axhline(y=1e-2, color='r', linestyle='--', label='Threshold (1e-2)')
    axes[0].set_xlabel('Stage')
    axes[0].set_ylabel('Max |HJB residual|')
    axes[0].set_title('HJB Equation Residual')
    axes[0].set_yscale('log')
    axes[0].legend()
    axes[0].grid(True)
    
    # FOC residual (if available)
    if 'max_foc_residual' in df.columns:
        axes[1].plot(df['stage'], df['max_foc_residual'])
        axes[1].axhline(y=1e-3, color='r', linestyle='--', label='Threshold (1e-3)')
        axes[1].set_ylabel('Max |FOC residual|')
        axes[1].set_title('First-Order Condition Residual')
        axes[1].set_yscale('log')
        axes[1].legend()
    else:
        axes[1].text(0.5, 0.5, 'No max_foc_residual column', ha='center', va='center')
        axes[1].set_title('First-Order Condition Residual')
    axes[1].set_xlabel('Stage')
    axes[1].grid(True)
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'residuals.png')
    plt.savefig(plot_path, dpi=150)
    print(f"Saved: {plot_path}")
    plt.close()
    
    # Print final statistics
    print("\n" + "="*60)
    print("Training Statistics")
    print("="*60)
    print(f"Total stages: {len(df)}")
    print(f"\nFinal values (stage {df['stage'].iloc[-1]}):")
    print(f"  Total Loss: {df['loss_total'].iloc[-1]:.6e}")
    print(f"  L1 (HJB):   {df['loss_L1'].iloc[-1]:.6e}")
    print(f"  L2 (FOC):   {df['loss_L2'].iloc[-1]:.6e}")
    print(f"  L3 (Term):  {df['loss_L3'].iloc[-1]:.6e}")
    print(f"  Max HJB residual: {df['maxdiff_V'].iloc[-1]:.6e}")
    if 'max_foc_residual' in df.columns:
        print(f"  Max FOC residual: {df['max_foc_residual'].iloc[-1]:.6e}")
    print(f"  V(0,0):     {df['V_at_origin'].iloc[-1]:.6f}")
    for col in control_cols:
        print(f"  {col}(origin): {df[col].iloc[-1]:.6f}")
    print("="*60)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python plot_training_csv.py <path_to_training_history.csv>")
        print("\nExample:")
        print("  python plot_training_csv.py results/test/quick_test_training_history.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)
    
    plot_training_history(csv_path)
