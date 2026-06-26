---
name: autoresearch
description: |
  Autonomous AI research skill for running automated neural network experiments. This skill should be used when the user wants to set up autonomous AI research experiments, run automated neural network training, conduct autonomous machine learning research, or let AI agents experiment with model architectures and hyperparameters. Based on Andrej Karpathy's autoresearch project, this skill enables AI agents to autonomously modify training code, run experiments, evaluate results, and iteratively improve models. Use when: (1) Setting up autonomous research experiments, (2) Running automated neural network training, (3) Conducting AI-driven research optimization, (4) Experimenting with model architectures and hyperparameters, (5) Implementing autonomous research loops, or (6) When the user mentions "autonomous research", "AI experiments", "automated training", "neural network optimization", or "autoresearch".
---

# Autoresearch Skill

This skill enables autonomous AI research experiments based on Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) project. It allows AI agents to autonomously modify neural network training code, run experiments, evaluate results, and iteratively improve models.

## Core Concept

The idea: give an AI agent a small but real LLM training setup and let it experiment autonomously. The agent modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats. You can leave it running overnight and wake up to a log of experiments and (hopefully) a better model.

## Key Files

The project has three core files:

1. **`prepare.py`** — Fixed constants, one-time data prep (downloads training data, trains a BPE tokenizer), and runtime utilities (dataloader, evaluation). **Not modified**.
2. **`train.py`** — The single file the agent edits. Contains the full GPT model, optimizer (Muon + AdamW), and training loop. Everything is fair game: architecture, hyperparameters, optimizer, batch size, etc. **This file is edited and iterated on by the agent**.
3. **`program.md`** — Baseline instructions for the agent. **This file is edited and iterated on by the human**.

## Requirements

- Single NVIDIA GPU (tested on H100)
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

## Quick Start Workflow

### Phase 1: Initial Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/karpathy/autoresearch.git
   cd autoresearch
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Prepare data** (one-time setup):
   ```bash
   uv run prepare.py
   ```

### Phase 2: Experiment Setup

1. **Agree on a run tag** (e.g., based on date like `mar20`)
2. **Create a new branch**:
   ```bash
   git checkout -b autoresearch/<tag>
   ```
3. **Initialize results file**:
   ```bash
   echo -e "commit\tval_bpb\tmemory_gb\tstatus\tdescription" > results.tsv
   ```

### Phase 3: Autonomous Experimentation Loop

The agent follows this loop indefinitely:

```
LOOP FOREVER:
  1. Look at current git state
  2. Modify train.py with experimental idea
  3. git commit
  4. Run experiment: uv run train.py > run.log 2>&1
  5. Extract results: grep "^val_bpb:\|^peak_vram_mb:" run.log
  6. If crash → analyze logs and fix or mark as crash
  7. Record results in results.tsv
  8. If improved → keep commit
  9. If not improved → git reset
```

## Key Metrics

- **val_bpb** (validation bits per byte) — Lower is better, vocab-size-independent
- **Training time** — Fixed 5-minute budget per experiment
- **Peak VRAM** — Memory usage in GB
- **Status** — `keep`, `discard`, or `crash`

## Constraints

### What the agent CAN do:
- Modify `train.py` (architecture, optimizer, hyperparameters, training loop, etc.)
- Experiment with different model configurations
- Run training experiments autonomously

### What the agent CANNOT do:
- Modify `prepare.py` (read-only)
- Install new packages or add dependencies
- Modify the evaluation harness

## Quality Criteria

1. **Simplicity**: Simpler solutions are preferred over complex ones
2. **Performance**: Lower val_bpb is better
3. **Memory**: VRAM usage should be reasonable
4. **Stability**: Code must run without crashing

## Output Format

Each experiment produces a summary:
```
---
val_bpb:          0.997900
training_seconds: 300.1
total_seconds:    325.9
peak_vram_mb:     45060.2
mfu_percent:      39.80
total_tokens_M:   499.6
num_steps:        953
num_params_M:     50.3
depth:            8
```

## Results Logging

Results are logged to `results.tsv` (tab-separated):
```
commit	val_bpb	memory_gb	status	description
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	increase LR to 0.04
c3d4e5f	1.005000	44.0	discard	switch to GeLU activation
d4e5f6g	0.000000	0.0	crash	double model width (OOM)
```

## Autonomous Operation

**CRITICAL**: Once the experiment loop begins, the agent operates autonomously:
- Do NOT pause to ask the human if you should continue
- Do NOT ask "should I keep going?" or "is this a good stopping point?"
- Continue working indefinitely until manually stopped
- If out of ideas, think harder: read papers, re-analyze code, try radical changes

## Use Cases

1. **Overnight experiments**: Leave running while sleeping, wake up to results
2. **Architecture search**: Automatically explore model architectures
3. **Hyperparameter optimization**: Find optimal training parameters
4. **Research automation**: Reduce manual experimentation effort

## Troubleshooting

### Common Issues:
1. **GPU not available**: Check CUDA installation and GPU drivers
2. **uv not installed**: Install uv package manager
3. **Data not prepared**: Run `uv run prepare.py`
4. **Out of memory**: Reduce model size or batch size

### Error Handling:
- Crashes are logged as `crash` status
- Analyze logs with `tail -n 50 run.log`
- Fix simple issues and retry, skip fundamentally broken ideas

## Best Practices

1. **Start with baseline**: Always run unmodified code first
2. **Incremental changes**: Make small, focused modifications
3. **Document experiments**: Clear descriptions in results.tsv
4. **Monitor progress**: Regularly check results and trends
5. **Balance exploration/exploitation**: Mix radical ideas with incremental improvements

## Integration with Agent Teams

This skill can be combined with the `agent-teams-playbook` skill for:
- Multi-agent research coordination
- Parallel experimentation
- Specialized roles (architect, optimizer, evaluator)
- Distributed research workflows

## References

- Original repository: https://github.com/karpathy/autoresearch
- Nanochat implementation: https://github.com/karpathy/nanochat
- Project announcement: https://x.com/karpathy/status/2029701092347630069
- "Dummy's Guide": https://x.com/hooeem/status/2030720614752039185