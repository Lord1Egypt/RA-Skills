# Debugging Non-Deterministic Agent Behavior in Reinforcement Learning Environments

## Overview

This skill provides a comprehensive toolkit for debugging reinforcement learning (RL) agents that exhibit non-deterministic behavior — one of the most challenging aspects of RL development. Non-determinism arises from environment stochasticity, policy randomness, seed mismanagement, and subtle numerical issues, making bugs notoriously hard to reproduce and diagnose.

## Core Modules

### 1. Stochasticity Control

Strategies for controlling and isolating sources of randomness in RL pipelines:

- **Seed Management**: Set and track seeds across all random sources (Python random, NumPy, PyTorch/TF, environment RNG, custom samplers).
- **Entropy Scheduling**: Monitor and clamp policy entropy to detect exploration collapse or excessive randomness.
- **Action Distribution Inspection**: Log full action distributions (not just sampled actions) to verify the policy is learning correctly.
- **Environment Stochasticity Toggle**: Identify which environment transitions are stochastic vs. deterministic, and temporarily freeze stochastic dimensions for debugging.

### 2. Reproducibility Tools

Utilities for making RL experiments reproducible:

- **ReproWrapper**: Wraps any env+agent pair to capture full episode trajectories (observations, actions, rewards, dones, seeds, RNG states).
- **Episode Replay**: Replays a recorded episode step-by-step for comparison against expected behavior.
- **State Snapshot**: Saves/restores complete training state (model weights, optimizer state, RNG state, env state).
- **Diff Replay**: Compares two episode trajectories and highlights divergences with step-level granularity.
- **Seed Cascade**: Generates deterministic seed sequences for parallel workers to avoid seed collisions.

### 3. Behavior Analysis

Techniques for understanding what the agent is actually doing:

- **Trajectory Clustering**: Groups similar trajectories to identify behavioral modes (e.g., "agent always fails at corner cases").
- **Action Frequency Heatmap**: Visualizes action distributions over state space regions.
- **Policy Consistency Check**: Detects if the same state produces different action distributions across episodes (a sign of state encoding bugs or hidden state leakage).
- **Temporal Correlation Detector**: Finds unintended correlations between consecutive actions that indicate the agent isn't respecting Markov assumptions.
- **Behavioral Mode Detection**: Identifies distinct behavioral regimes the agent switches between (e.g., cautious vs. reckless).

### 4. Reward Debugging

Methods for diagnosing reward-related issues:

- **Reward Decomposition**: Breaks multi-component rewards into individual signals to identify which component drives behavior.
- **Reward Shaping Validator**: Checks if shaped rewards accidentally create local optima or reward cycling.
- **Sparse Reward Tracer**: For sparse-reward environments, logs the full trajectory leading up to reward events for analysis.
- **Reward Scale Analyzer**: Detects reward scale mismatches between components that cause gradient domination.
- **Episode Return Sanity Check**: Verifies that discounted returns are computed correctly and that reward normalization isn't destroying the signal.
- **Reward Hacking Detector**: Flags when the agent achieves high reward through unintended behavior (exploiting bugs in reward computation).

## Usage Patterns

### Quick Reproducibility Check
```
1. Set global seed via seedAll()
2. Run episode with EpisodeRecorder
3. Replay and compare
```

### Diagnose Erratic Behavior
```
1. Run 50 episodes with fixed seeds
2. Cluster trajectories
3. Inspect divergent clusters
4. Use policyConsistencyCheck on divergent states
```

### Reward Signal Investigation
```
1. Decompose reward into components
2. Run rewardScaleAnalyzer
3. Check for hacking via rewardHackingDetector
4. Validate return computation
```

## Anti-Patterns to Watch For

- **Seed per episode but not per step**: Environment internal RNG can diverge even with episode-level seeding.
- **Caching state without RNG**: Replay buffers that store (s, a, r, s') without the RNG state cannot reproduce the exact transition.
- **Floating point mode differences**: GPU non-determinism from reduced-precision ops. Use `torch.backends.cudnn.deterministic = True` during debug.
- **Hidden environment state**: Some environments (e.g., Atari with frame-skipping) have internal state not exposed in the observation.
- **Reward normalization drift**: Running mean/std normalization changes the effective reward over training, making early episodes non-reproducible.

## Integration Tips

- Works with Gym/Gymnasium, PettingZoo, and custom env wrappers.
- Compatible with PyTorch, TensorFlow, and JAX-based agents.
- Output formats: JSON trajectories, CSV logs, and structured debug reports.