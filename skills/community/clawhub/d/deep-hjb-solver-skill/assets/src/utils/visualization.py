"""Visualization utilities."""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


def plot_control_surface(control_net, config, problem, control_idx=2, 
                         control_name='beta', filename='control.png'):
    """
    Plot control surface over (t, x) domain.
    
    Args:
        control_net: Control network
        config: Configuration object
        problem: Problem object
        control_idx: Index of control to plot (0=Z, 1=alpha, 2=beta)
        control_name: Name of control for labeling
        filename: Output filename
    """
    domain_bounds = problem.get_domain_bounds()
    
    X_plot = np.linspace(domain_bounds['X_low'], domain_bounds['X_high'], config.n_plot)
    t_plot = np.linspace(domain_bounds['t_low'], domain_bounds['t_high'], config.n_plot)
    
    t_mesh, X_mesh = np.meshgrid(t_plot, X_plot)
    
    t_flat = np.reshape(t_mesh, [config.n_plot**2, 1])
    X_flat = np.reshape(X_mesh, [config.n_plot**2, 1])
    
    t_flat = tf.convert_to_tensor(t_flat, dtype=tf.float32)
    X_flat = tf.convert_to_tensor(X_flat, dtype=tf.float32)
    
    # Get control values
    control_out = control_net(t_flat, X_flat)
    control_values = tf.expand_dims(control_out[:, control_idx], axis=-1)
    control_mesh = np.reshape(control_values, [config.n_plot, config.n_plot])
    
    # Plot
    plt.rcParams['axes.spines.right'] = True
    plt.rcParams['axes.spines.top'] = True
    
    c = np.min(control_mesh)
    d = np.max(control_mesh)
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=500)
    
    if d - c > 0:
        levels = np.arange(c, d, (d - c) / 20)
        CS = plt.contour(t_mesh, X_mesh, control_mesh, levels=levels)
        plt.clabel(CS, inline=True, fontsize=20)
    else:
        CS = plt.contour(t_mesh, X_mesh, control_mesh)
    
    plt.ylabel("x", fontsize=25, labelpad=10)
    plt.xlabel("t", fontsize=25, labelpad=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(f"Control {control_name}", fontsize=25)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    
    print(f"Control plot saved to {filename}")
    return control_mesh


def plot_control_sum(control_net, config, problem, filename='beta_plus_Z.png'):
    """
    Plot beta + Z surface.
    
    Args:
        control_net: Control network
        config: Configuration object
        problem: Problem object
        filename: Output filename
    """
    domain_bounds = problem.get_domain_bounds()
    
    X_plot = np.linspace(domain_bounds['X_low'], domain_bounds['X_high'], config.n_plot)
    t_plot = np.linspace(domain_bounds['t_low'], domain_bounds['t_high'], config.n_plot)
    
    t_mesh, X_mesh = np.meshgrid(t_plot, X_plot)
    
    t_flat = np.reshape(t_mesh, [config.n_plot**2, 1])
    X_flat = np.reshape(X_mesh, [config.n_plot**2, 1])
    
    t_flat = tf.convert_to_tensor(t_flat, dtype=tf.float32)
    X_flat = tf.convert_to_tensor(X_flat, dtype=tf.float32)
    
    # Get control values
    control_out = control_net(t_flat, X_flat)
    Z_values = control_out[:, 0]
    beta_values = control_out[:, 2]
    sum_values = Z_values + beta_values
    sum_mesh = np.reshape(sum_values, [config.n_plot, config.n_plot])
    
    # Plot
    plt.rcParams['axes.spines.right'] = True
    plt.rcParams['axes.spines.top'] = True
    
    c = np.min(sum_mesh)
    d = np.max(sum_mesh)
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=500)
    
    if d - c > 0:
        levels = np.arange(c, d, (d - c) / 50)
        CS = plt.contour(t_mesh, X_mesh, sum_mesh, levels=levels)
        plt.clabel(CS, inline=True, fontsize=20)
    else:
        CS = plt.contour(t_mesh, X_mesh, sum_mesh)
    
    plt.ylabel("x", fontsize=25, labelpad=10)
    plt.xlabel("t", fontsize=25, labelpad=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(r"$\beta + Z$", fontsize=25)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    
    print(f"Control sum plot saved to {filename}")
    return sum_mesh


def lolt(loss, threshold=1e-8, skip=5):
    """Filter loss values for plotting (threshold filter)."""
    res = []
    for i in range(len(loss)):
        if loss[i] < threshold or i % skip != 0:
            res.append(float("nan"))
        else:
            res.append(loss[i])
    return res


def lola(loss, threshold=1e-8, skip=5):
    """Filter loss values for plotting (below threshold)."""
    res = []
    for i in range(len(loss)):
        if loss[i] < threshold and i % skip == 0:
            res.append(threshold)
        else:
            res.append(float("nan"))
    return res


def plot_loss_history(history, filename='loss_function.png'):
    """
    Plot training loss history.
    
    Args:
        history: Training history dictionary
        filename: Output filename
    """
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=500)
    
    # Support both legacy and current trainer history key styles.
    l1 = history['loss_L1'] if 'loss_L1' in history else history.get('L1_list', [])
    maxdiff = history['maxdiff_V'] if 'maxdiff_V' in history else history.get('maxdiffV_list', [])
    penalty = history['max_penalty'] if 'max_penalty' in history else history.get('penalty_list', [])
    control_bound = history['max_control_bound'] if 'max_control_bound' in history else history.get('cb_list', [])

    n = len(l1)
    if n == 0:
        raise ValueError('History does not contain loss data for plotting.')

    x = np.arange(n)

    # Plot losses
    plt.plot(x, l1, label='$||L_{int}||_2$', color='blue')
    if len(maxdiff) == n:
        plt.plot(x, maxdiff, label='$||L_{int}||_{\\infty}$', color='blue', linestyle='dashed')

    if len(control_bound) == n:
        plt.plot(x, lolt(control_bound), '^', label='$||P(\\beta,Z)||_{1}$', color='green')
        plt.plot(x, lola(control_bound), '^', color='green', linewidth=5)

    if len(penalty) == n:
        plt.plot(x, lolt(penalty), 'x', color='green', label='$||P(\\beta,Z)||_{\\infty}$')
        plt.plot(x, lola(penalty), 'x', color='green', linestyle='dashed')
    
    plt.ylabel("Loss function", fontsize=25, labelpad=20)
    plt.xlabel("Training step n", fontsize=25, labelpad=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.yscale('log')
    plt.ylim([1e-8, 10])
    
    yticks = np.array([1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1])
    plt.yticks(yticks, fontsize=20)
    ax.set_yticklabels(['$10^{-7}$', '$10^{-6}$', '$10^{-5}$', '$10^{-4}$',
                       '$10^{-3}$', '$10^{-2}$', '$10^{-1}$', '$10^0$', '$10^1$'])
    
    plt.legend(fontsize="25", loc="upper right", framealpha=0.2)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    
    print(f"Loss history plot saved to {filename}")
