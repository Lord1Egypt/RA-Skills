---
name: fusion-bench
description: Use FusionBench to run model fusion experiments. Covers running benchmarks, adding new merging algorithms, evaluating fused models, and managing model pools. Use when the user wants to merge models, run fusion experiments, evaluate fusion methods, or work with the FusionBench framework.
---

# FusionBench Skill

FusionBench is a comprehensive benchmark/toolkit for deep model fusion (model merging). 

**Paper:** arXiv:2406.03280  
**PyPI:** `pip install fusion-bench`  
**Repo:** https://code.tanganke.com/tanganke/fusion_bench  
**Docs:** https://tanganke.github.io/fusion_bench/

## Quick Start

```bash
# Install
pip install fusion-bench

# Run a simple experiment (CLIP ViT-B/32, task arithmetic on 8 tasks)
fusion_bench method=task_arithmetic modelpool=clip-vit-base-patch32 taskpool=clip-vit-base-patch32_8tasks

# Run with different merging method
fusion_bench method=ties_merging modelpool=clip-vit-base-patch32 taskpool=clip-vit-base-patch32_8tasks
```

## Architecture Overview

```
fusion_bench/
├── method/           # Merging algorithms (30+)
├── modelpool/        # Model loading & management
├── config/           # Hydra YAML configs
├── tasks/            # Task evaluation
├── utils/            # Helpers (state_dict ops, lazy loading, etc.)
└── scripts/          # CLI & web UI
```

### Key Components

1. **ModelPool**: Loads and manages pre-trained/fine-tuned models
   - `AutoModelPool`: Auto-selects based on config
   - `CLIPVisionModelPool`: For CLIP ViT models
   - `CausalLMPool`: For Llama, GPT-2, etc.

2. **Method**: The merging algorithm
   - Inherits from `BaseModelFusionAlgorithm`
   - Implements `run(modelpool)` → merged model

3. **TaskPool**: Evaluation tasks
   - CLIP: 8-38 classification tasks
   - LLM: ARC, HellaSwag, MMLU, etc.

## Supported Merging Methods

### Basic
| Method | Config Name | Description |
|--------|-------------|-------------|
| Simple Average | `simple_average` | Uniform weight averaging |
| Weighted Average | `weighted_average` | Learnable task weights |
| Task Arithmetic | `task_arithmetic` | task_vector = fine-tuned - base |
| Slerp | `slerp` | Spherical interpolation |

### Sparse/Pruning
| Method | Config Name | Description |
|--------|-------------|-------------|
| TIES | `ties_merging` | Trim, Elect, Sign + merge |
| DARE | `dare` | Drop And REscale |
| Magnitude Pruning | `magnitude_pruning` | Prune by magnitude |

### Advanced
| Method | Config Name | Description |
|--------|-------------|-------------|
| AdaMerging | `adamerging` | Learn layer-wise coefficients |
| Fisher Merging | `fisher_merging` | Fisher-weighted merging |
| RegMean | `regmean` | Regression mean (closed-form) |
| RegMean++ | `regmean_plusplus` | Enhanced RegMean with cross-layer deps |

### MoE-Based
| Method | Config Name | Description |
|--------|-------------|-------------|
| WE-MoE | `we_moe` | Weight Ensembling MoE |
| PWE-MoE | `pwe_moe` | Pareto-optimal WE-MoE |
| RankOne-MoE | `rankone_moe` | Rank-1 expert decomposition |
| Sparse-WE-MoE | `sparse_we_moe` | Sparse weight ensembling |

### Continual Merging
| Method | Config Name | Description |
|--------|-------------|-------------|
| OPCM | `opcm` | Orthogonal Projection Continual Merging |
| DOP | `dop` | Dual Orthogonal Projection |
| Gossip | `gossip` | Gossip-based continual merging |

### Specialized
| Method | Config Name | Description |
|--------|-------------|-------------|
| ISO-C/CTS | `isotropic_merging` | Isotropic merging in common/task subspace |
| AdaSVD | `ada_svd` | SVD-based adaptive merging |
| WUDI | `wudi` | Wasserstein distance merging |
| ExPO | `expo` | Exponential task vectors |

## Running Experiments

### 1. Basic Merging (CLI)

```bash
# Task Arithmetic on CLIP ViT-B/32
fusion_bench \
  method=task_arithmetic \
  modelpool=clip-vit-base-patch32 \
  taskpool=clip-vit-base-patch32_8tasks

# TIES merging with custom scaling
fusion_bench \
  method=ties_merging \
  method.scaling_coefficient=0.3 \
  modelpool=clip-vit-base-patch32 \
  taskpool=clip-vit-base-patch32_8tasks
```

### 2. LLM Merging

```bash
# Merge Llama models
fusion_bench \
  method=task_arithmetic \
  modelpool=llama2-7b \
  taskpool=llama2-7b_tasks

# With DARE
fusion_bench \
  method=dare \
  method.type=task_arithmetic \
  modelpool=llama2-7b
```

### 3. Using Fabric (Distributed/Mixed Precision)

```bash
fusion_bench \
  fabric=deepspeed_stage_2 \
  method=adamerging \
  modelpool=clip-vit-base-patch32
```

## Adding a New Method

### Step 1: Create method file

```python
# fusion_bench/method/my_method.py
from fusion_bench.method.base_algorithm import BaseModelFusionAlgorithm
from fusion_bench.modelpool import BaseModelPool
import torch

class MyMergingAlgorithm(BaseModelFusionAlgorithm):
    """
    My custom merging algorithm.
    """
    def __init__(self, scaling_coefficient: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.scaling_coefficient = scaling_coefficient
    
    @torch.no_grad()
    def run(self, modelpool: BaseModelPool):
        # 1. Load base model
        base_model = modelpool.load_model("_base_")
        base_sd = base_model.state_dict()
        
        # 2. Compute merged task vectors
        merged_tv = {}
        for model_name in modelpool.model_names:
            if model_name == "_base_":
                continue
            model = modelpool.load_model(model_name)
            tv = {k: v - base_sd[k] for k, v in model.state_dict().items()}
            # Your merging logic here
            for k in tv:
                if k not in merged_tv:
                    merged_tv[k] = tv[k] * self.scaling_coefficient
                else:
                    merged_tv[k] += tv[k] * self.scaling_coefficient
        
        # 3. Apply merged task vector
        for k in base_sd:
            base_sd[k] += merged_tv.get(k, 0)
        
        base_model.load_state_dict(base_sd)
        return base_model
```

### Step 2: Register in `__init__.py`

```python
# fusion_bench/method/__init__.py
_import_structure = {
    ...
    "my_method": ["MyMergingAlgorithm"],
}
```

### Step 3: Create config

```yaml
# config/method/my_method.yaml
_target_: fusion_bench.method.my_method.MyMergingAlgorithm
scaling_coefficient: 1.0
```

### Step 4: Run

```bash
fusion_bench method=my_method modelpool=clip-vit-base-patch32
```

## Model Pool Configuration

### CLIP Models

```yaml
# config/modelpool/clip-vit-base-patch32.yaml
_target_: fusion_bench.modelpool.CLIPVisionModelPool
model_names:
  - _base_
  - Cars
  - DTD
  - EuroSAT
  - GTSRB
  - MNIST
  - RESISC45
  - SUN397
  - SVHN
model_dir: ${oc.env:HOME}/.cache/fusion_bench/models
```

### LLM Models

```yaml
# config/modelpool/llama2-7b.yaml
_target_: fusion_bench.modelpool.CausalLMPool
model_names:
  - _base_
  - arc
  - hellaswag
  - mmlu
model_dir: ${oc.env:HOME}/.cache/fusion_bench/llama_models
```

## Utilities

### State Dict Arithmetic

```python
from fusion_bench.utils.state_dict_arithmetic import StateDict

# Convenient operations on state dicts
sd1 = StateDict(model1.state_dict())
sd2 = StateDict(model2.state_dict())

merged = sd1 + sd2           # Add
diff = sd1 - sd2             # Subtract
scaled = sd1 * 0.5           # Scale
tv_merged = sd1 + 0.3 * sd2  # Linear combination
```

### Lazy State Dict

```python
from fusion_bench.utils.lazy_state_dict import LazyStateDict

# Load large models without OOM
lazy_sd = LazyStateDict.from_file("model.safetensors")
# Only loads tensors when accessed
```

## Common Workflows

### 1. Evaluate a single merged model

```python
from fusion_bench import AutoModelPool
from fusion_bench.method import SimpleAverageAlgorithm

pool = AutoModelPool.from_config("config/modelpool/clip-vit-base-patch32.yaml")
method = SimpleAverageAlgorithm()
merged_model = method.run(pool)

# Evaluate on tasks
for task_name in pool.model_names:
    if task_name == "_base_":
        continue
    acc = evaluate(merged_model, task_name)
    print(f"{task_name}: {acc:.2%}")
```

### 2. Hyperparameter search

```bash
# Sweep scaling coefficient
for coeff in 0.2 0.4 0.6 0.8 1.0; do
  fusion_bench \
    method=task_arithmetic \
    method.scaling_coefficient=$coeff \
    modelpool=clip-vit-base-patch32
done
```

### 3. Compare multiple methods

```bash
for method in simple_average task_arithmetic ties_merging dare; do
  echo "=== $method ==="
  fusion_bench \
    method=$method \
    modelpool=clip-vit-base-patch32 \
    taskpool=clip-vit-base-patch32_8tasks
done
```

## Tips

1. **Memory**: Use `fabric=deepspeed_stage_2` for large models
2. **Caching**: Models are cached in `~/.cache/fusion_bench/`
3. **Reproducibility**: Set `seed=42` in config
4. **Debugging**: Use `hydra.verbose=true` for detailed logs
5. **Web UI**: Run `fusion_bench_webui` for interactive exploration

## Related Papers

1. **FusionBench** (arXiv:2406.03280) - The benchmark paper
2. **SMILE** (arXiv:2408.10174) - Sparse MoE from pre-trained models
3. **WE-MoE** - Weight Ensembling MoE for multi-task merging
4. **OPCM/DOP** - Continual model merging methods
5. **RegMean++** (arXiv:2508.03121) - Enhanced RegMean
