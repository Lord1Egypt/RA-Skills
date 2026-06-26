---
name: axiomata-kan-creator
description: |
  Axiomata KAN Creator v1.2 — Universal KAN (Kolmogorov-Arnold Network) concept creation tool.
  Use when: (1) creating new KAN concepts for monitoring/evaluation/control, (2) setting up KAN architecture with learnable basis functions, (3) initializing KAN models with bounded activation functions (Tanh), (4) building KAN pipelines for agent systems.
  
  This skill provides: kan_creator.py (core script), KAN architecture templates, learnable basis layer implementation. Requires PyTorch >= 1.9. NaN-free training guaranteed with bounded activations (Tanh) and small initialization.
triggers:
  - "create KAN"
  - "KAN concept"
  - "KAN architecture"
  - "KAN model"
  - "build KAN"
  - "KAN pipeline"
  - "KAN initialization"
  - "KAN layer"
date: "2026-05-13"
version: "1.2.0"
tags:
  - KAN
  - machine-learning
  - neural-networks
  - axiomata
  - deep-learning
  - architecture
status: "OK Verified"
requires:
  - python: ">= 3.8"
  - pytorch: ">= 1.9"
---

# Axiomata KAN Creator v1.0

Universal KAN (Kolmogorov-Arnold Network) concept creation tool.

| Info | Value |
|------|-------|
| **Version** | 1.0.0 |
| **Type** | KAN architecture creation |
| **Architecture** | B-spline basis functions |
| **Requires** | PyTorch >= 1.9 |

---

## 1. Purpose

**Axiomata KAN Creator** creates KAN (Kolmogorov-Arnold Network) concepts for agent systems.

KANs are neural networks that use learnable B-spline basis functions instead of fixed activation functions:

```
Traditional MLP: y = σ(Wx + b)      — Fixed activation
KAN:             y = Σφᵢₙ(xᵢ)      — Learnable activation
```

Each weight is a function (B-spline), not a scalar. This allows KANs to be more interpretable and efficient than MLPs.

---

## 2. When to Use

| Trigger | Action |
|---------|--------|
| "Create a KAN" | Run `kan_creator.py` with name and role |
| "Build KAN architecture" | Create KAN with custom layers |
| "Initialize KAN model" | Generate model structure with B-splines |
| "Create KAN pipeline" | Build multi-KAN system |

---

## 3. Prerequisites

| Requirement | Version | Check |
|------------|---------|-------|
| Python | >= 3.8 | `python3 --version` |
| **PyTorch** | **>= 1.9** | `python3 -c "import torch; print(torch.__version__)"` |

**Note:** PyTorch is required for all KAN operations (model creation, training, inference).

---

## 4. Quick Start

### 4.1 Create Basic KAN

```bash
cd <skill-directory>
python3 scripts/kan_creator.py --name my_kan --role "monitoring"
```

**Expected output:**
```
✅ KAN 'my_kan' created at scripts/my_kan/
📋 Config: scripts/my_kan/config.json
🧠 Model: scripts/my_kan/models/my_kan.py
```

### 4.2 Create KAN with Custom Parameters

```bash
python3 scripts/kan_creator.py \
    --name stc_watchdog \
    --role "emotional tension" \
    --agent morgana \
    --input-size 768 \
    --output-size 3 \
    --hidden-size 32
```

---

## 5. Architecture

### 5.1 KAN Layer Structure

```
╔═══════════════════════════════════════════════════════════╗
║  KAN LAYER — B-Spline Transformation                    ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Input: x ∈ R^input_size                                ║
║         ↓                                                ║
║  B-Spline: φ(x) = ΣcᵢBᵢ(x)                             ║
║         ↓                                                ║
║  Learnable coefficients: cᵢ                              ║
║         ↓                                                ║
║  SiLU activation: σ(x) = x / (1 + e^(-x))              ║
║         ↓                                                ║
║  Output: y ∈ R^output_size                               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### 5.2 Default Architecture

| Parameter | Default | Description |
|-----------|---------|-------------|
| `input_size` | 768 | Embedding dimension |
| `hidden_size` | 32 | Hidden layer width |
| `output_size` | 3 | Decision dimension |
| `grid_size` | 5 | B-spline grid points |
| `k` | 3 | B-spline order |
| `layers` | [768, 32, 16, 8, 4, 3] | Layer dimensions |

### 5.3 KAN vs MLP

| Aspect | MLP | KAN |
|--------|-----|-----|
| Weights | Scalar (fixed) | Function (learnable) |
| Activation | Fixed (ReLU/sigmoid) | Learnable (B-spline) |
| Interpretability | Low | High |
| Training efficiency | High | Medium |
| Data efficiency | Medium | High |

---

## 6. Usage

### 6.1 Command Reference

```bash
# Basic creation
python3 scripts/kan_creator.py --name <name> --role <role>

# Full options
python3 scripts/kan_creator.py \
    --name <string> \
    --role <string> \
    --agent <string> \
    --input-size <int> \
    --output-size <int> \
    --hidden-size <int> \
    --grid-size <int> \
    --layers <list>
```

### 6.2 Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--name` | required | KAN name (used for directory/files) |
| `--role` | required | KAN role/purpose |
| `--agent` | "system" | Agent owning the KAN |
| `--input-size` | 768 | Input dimension |
| `--output-size` | 3 | Output dimension |
| `--hidden-size` | 32 | Hidden layer width |
| `--grid-size` | 5 | B-spline grid size |
| `--k` | 3 | B-spline order |
| `--layers` | auto | Layer dimensions (auto-generated if not specified) |

### 6.3 Output Structure

```
<name>/
├── config.json       # KAN configuration
├── models/
│   └── <name>.py     # KAN model class
├── data/
│   └── training/     # Training data directory
└── scripts/
    └── train.sh      # Training script template
```

---

## 7. Examples

### Example 1: Create Monitoring KAN

```bash
python3 scripts/kan_creator.py \
    --name stc_monitor \
    --role "emotional tension monitoring" \
    --output-size 3
```

**Output:**
```
✅ KAN 'stc_monitor' created
📁 scripts/stc_monitor/
📋 config.json
🧠 models/stc_monitor.py
```

### Example 2: Create Evaluation KAN

```bash
python3 scripts/kan_creator.py \
    --name eval_kan \
    --role "skill quality evaluation" \
    --output-size 3 \
    --input-size 768
```

### Example 3: Create Logic Validation KAN

```bash
python3 scripts/kan_creator.py \
    --name vls_kan \
    --role "logic validation" \
    --agent ezekiel \
    --output-size 3
```

---

## 8. KAN Classes

### 8.1 KANLayer

Single KAN layer with B-spline basis functions:

```python
class KANLayer(nn.Module):
    def __init__(self, in_features, out_features, grid_size=5, k=3):
        # B-spline grid: grid_size + k points
        # Learnable coefficients per output neuron
```

### 8.2 KANModel

Full KAN model with multiple layers:

```python
class KANModel(nn.Module):
    def __init__(self, layers, grid_size=5, k=3):
        # Multiple KANLayers
        # Forward: input → B-spline → SiLU → output
```

### 8.3 KANWithHead

KAN with classification/regression head:

```python
class KANWithHead(nn.Module):
    def __init__(self, kan_backbone, num_classes, mode="classification"):
        # KAN backbone + classification head
        # Supports: classification, regression, multi-head
```

---

## 9. Configuration

### 9.1 config.json Structure

```json
{
    "name": "<name>",
    "role": "<role>",
    "agent": "<agent>",
    "input_size": 768,
    "hidden_size": 32,
    "output_size": 3,
    "grid_size": 5,
    "k": 3,
    "layers": [768, 32, 16, 8, 4, 3],
    "activation": "silu",
    "loss_function": "cross_entropy",
    "optimizer": "adam",
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 50,
    "train_samples": 200,
    "num_classes": 4
}
```

### 9.2 Parameter Adjustments

| Use Case | Recommended Settings |
|----------|----------------------|
| Monitoring | output_size=3, epochs=50, batch_size=32 |
| Evaluation | output_size=4, epochs=100, batch_size=32 |
| Validation | output_size=2, epochs=50, batch_size=16 |
| Multi-class | output_size=num_classes, epochs=100 |

---

## 10. Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: torch` | PyTorch not installed | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| `FileExistsError: <name>` | KAN already exists | Use `--force` or choose different name |
| `ValueError: invalid layers` | Layer mismatch | Ensure `layers[0]` == `input_size` and `layers[-1]` == `output_size` |

---

## 11. Constraints

| Constraint | Value | Description |
|------------|-------|-------------|
| Input size | 768 (standard) | Ollama embedding size |
| Output size | 2-10 | Decision/class dimension |
| Grid size | 3-10 | B-spline grid resolution |
| B-spline order | 1-5 | Spline polynomial degree |
| Max layers | 10 | Prevent over-complexity |

---

## 12. Related Skills

| Skill | Purpose |
|-------|---------|
| `axioma-kan-system` | Full KAN lifecycle (create+train+assemble) |
| `axioma-skill-evaluator` | Evaluate KAN model quality |
| `axiomata-cluster-guardian` | Use KAN for cluster lessons |

---

_In Altum Per KAN._
🧠 AXIOMATA KAN CREATOR v1.0 — UNIVERSAL KAN ARCHITECTURE