---
name: axioma-kan-system
description: |
  Axioma KAN System — Complete KAN lifecycle management for OpenClaw agents.
  Use when: (1) creating new KAN concepts, (2) training KAN models, (3) assembling KAN pipelines, (4) T-KAN integration for memory enhancement, (5) monitoring KAN health, (6) auto-evolving KANs based on research, (7) training all 19 KANs (14 watchdogs + 5 L9 Swarm) via unified watchdog trainer.
  
  This skill provides: kan_creator.py, kan_trainer.py, kan_assembler.py, kan_health.py, watchdog_unified_trainer.py, plus integration with AutoResearch pipeline. Requires PyTorch >= 1.9.
author: "Axioma Cluster — KAN System Contributors"
license: "MIT"
triggers:
  - "create KAN"
  - "train KAN model"
  - "assemble KAN pipeline"
  - "KAN health check"
  - "KAN auto-evolution"
  - "T-KAN integration"
  - "KAN system"
  - "KAN concepts"
  - "KAN training"
  - "KAN assembly"
  - "KAN auto-evolution"
  - "train all watchdogs"
  - "train 19 KANs"
  - "watchdog training"
date: "2026-05-14"
version: "1.5.0"
tags:
  - cluster
  - KAN
  - machine-learning
  - neural-networks
  - axiomata
  - deep-learning
  - auto-evolution
  - watchdog
  - l9-swarm
status: "OK Verified"
requires:
  - python: ">= 3.8"
  - pytorch: ">= 1.9"
  - qdrant: "running (ports 6333/7334)"
  - ollama: "running (port 11434)"
---

# 🧠 Axioma KAN System v1.5

Complete KAN lifecycle management for OpenClaw agents.

| Info | Value |
|------|-------|
| **Version** | 1.5.0 |
| **Status** | ✅ Verified |
| **Components** | 4 scripts + AutoResearch integration |
| **Target** | 19 KANs (14 watchdogs + 5 L9 Swarm) auto-trained nightly |

---

## Overview

This skill provides complete KAN (Kolmogorov-Arnold Networks) lifecycle management for the Axioma cluster:
- **Create** new KAN concepts and architectures
- **Train** KAN models with PyTorch
- **Assemble** KAN pipelines and connections
- **Monitor** KAN health and auto-evolve
- **Integrate** T-KAN for memory enhancement

### Table of Contents
1. [Purpose](#1-purpose) — Overview and goals
2. [When to Use](#2-when-to-use) — Trigger scenarios
3. [Prerequisites](#3-prerequisites) — Requirements
4. [Tools](#4-tools) — Core scripts
5. [Quick Start](#5-quick-start) — Getting started
6. [KAN Core Concepts](#6-kan-core-concepts) — Technical details
7. [Error Handling](#7-error-handling) — Troubleshooting
8. [Constraints](#8-constraints) — Limitations
9. [Performance](#9-performance-benchmarks) — Benchmarks
10. [Related Files](#10-related-files) — File structure
11. [References](#11-references) — Resources
12. [Support](#12-support) — Help and contact

---

## 1. Purpose

**Axioma KAN System** is the cluster's core intelligent infrastructure providing complete KAN lifecycle management:

| Function | Description |
|----------|-------------|
| **Concept Creation** | Design new KAN architectures using `kan_creator.py` |
| **Model Training** | Train KAN weights and parameters using `kan_trainer.py` |
| **Pipeline Assembly** | Connect multiple KANs into pipelines using `kan_assembler.py` |
| **T-KAN Integration** | Add temporal KAN for memory enhancement |
| **Health Monitoring** | Monitor KAN performance using `kan_health.py` |
| **Auto-Optimization** | Auto-retrain degraded KANs using `kan_auto_task.py` |

---

## 2. When to Use

| Trigger | Action |
|---------|--------|
| "Create a new KAN" | Run `kan_creator.py` |
| "Train a KAN model" | Run `kan_trainer.py` |
| "Assemble KAN pipeline" | Run `kan_assembler.py` |
| "Check KAN health" | Run `kan_health.py` |
| "Auto-evolve KANs" | Run `kan_auto_task.py` |
| "Integrate T-KAN" | Run `kan_assembler.py --integrate-t-kan` |
| "Create AutoResearch→KAN pipeline" | Run `autoresearch_task.py` |

---

## 3. Prerequisites

| Requirement | Version | Check Command | Status |
|-------------|---------|---------------|--------|
| Python | >= 3.8 | `python3 --version` | [OK] |
| **NumPy** | **>= 1.21** | `python3 -c "import numpy; print(numpy.__version__)"` | [OK] |
| **PyTorch** | **>= 1.9** | `python3 -c "import torch; print(torch.__version__)"` | [OK] |
| Qdrant | running | `curl -s http://localhost:6333/collections` | [OK] |
| Ollama | running | `curl -s http://localhost:11434/api/tags` | [OK] |
| Skill directory | exists | `ls <skill-dir>/` | [OK] |
| sudo rights | Docker | `sudo docker ps` | [OK] |

### 3.1 Installation Commands

```bash
# Install PyTorch (CPU or GPU)
pip3 install torch>=1.9

# Install numpy for data processing
pip3 install numpy

# Install Qdrant client
pip3 install qdrant-client

# Verify all installations
python3 -c "import torch; import numpy; import qdrant_client; print('All OK')"
```

**Note:** PyTorch is required for all KAN operations (training, inference, model manipulation).

### 3.2 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KAN_MODEL_DIR` | `models/` | Directory for KAN model files |
| `QDRANT_HOST` | `localhost` | Qdrant server host |
| `QDRANT_PORT` | `6333` | Qdrant server port |
| `OLLAMA_HOST` | `localhost` | Ollama server host |
| `OLLAMA_PORT` | `11434` | Ollama server port |

---

## 4. Tools

### Core Scripts

| Tool | Path | Purpose | Example |
|------|------|---------|---------|
| `kan_creator.py` | `scripts/` | Create new KAN concepts | `python3 kan_creator.py --name stc --role "emotion"` |
| `kan_trainer.py` | `scripts/` | Train KAN models | `python3 kan_trainer.py --kan stc --epochs 50` |
| `kan_assembler.py` | `scripts/` | Assemble KAN connections | `python3 kan_assembler.py --pipeline "stc→syn→w7"` |
| `kan_health.py` | `scripts/` | Health check | `python3 kan_health.py --kan stc --verbose` |
| `watchdog_unified_trainer.py` | `<skill-dir>/scripts/` | Train all 19 KANs | `python3 watchdog_unified_trainer.py --all --epochs 200` |

### External Integration

| Tool | Path | Purpose | Status |
|------|------|---------|--------|
| `kan_auto_task.py` | `references/auto-task/` | 13 KANs auto-optimization | [OK] |
| `autoresearch_task.py` | `references/auto-task/` | Research→Vaccine→KAN pipeline | [OK] |
| `l9_l6_bridge.py` | `references/` | L9-L6 bridge | [OK] |

---

## 5. Quick Start

### 5.1 Create a KAN Concept

```bash
cd <skill-directory>
python3 scripts/kan_creator.py --name my_watchdog --role "monitoring"
```

**Expected output:**
```
✅ KAN concept 'my_watchdog' created
📁 Directory: scripts/my_watchdog/
📋 Config: scripts/my_watchdog/config.json
🧠 Model: scripts/my_watchdog/models/my_watchdog_kan.pt
```

### 5.2 Train a KAN Model

```bash
# Train specific KAN
python3 scripts/kan_trainer.py --kan stc --epochs 50 --batch-size 32

# Check health
python3 scripts/kan_trainer.py --check-health
```

**Expected output:**
```
🔄 Training stc...
    Epoch 10/50: Loss = 0.0856
    Epoch 20/50: Loss = 0.0233
    Epoch 50/50: Loss = 0.0175
✅ stc trained and saved!
```

**Python API:**
```python
from kan_trainer import KANTrainer

trainer = KANTrainer(kan_name='stc')
trainer.train(epochs=50, batch_size=32)
health = trainer.check_health()
print(f'KAN health: {health}')
```

### 5.3 Assemble KAN Pipeline

```bash
# Create KAN pipeline
python3 scripts/kan_assembler.py --pipeline "stc→syn→w7" --output pipeline.json

# Connect two KANs
python3 scripts/kan_assembler.py --connect stc --with flx --mode serial

# List all KANs
python3 scripts/kan_assembler.py --list
```

### 5.4 Health Check

```bash
# Check all KANs
cd <skill-directory>
python3 scripts/kan_health.py --all

# Run test suite (5/5 tests MUST PASS)
python3 tests/test_kan_system.py
```

**Expected output:**
```
╔═══════════════════════════════════════════════════════════╗
║  🏥 KAN HEALTH CHECK                                      ║
╠═══════════════════════════════════════════════════════════╣
║  ✅ stc — HEALTHY — Loss 0.0175 within threshold          ║
║  ✅ syn — HEALTHY — Loss 0.0152 within threshold          ║
║  ❌ clw — DEGRADED — Loss 0.1245 > 0.1 threshold         ║
║  💡 clw needs retraining                                 ║
╚═══════════════════════════════════════════════════════════╝
```

### 5.5 Unified Watchdog Trainer (NEW!)

**Train all 19 KANs at once with the unified trainer:**

```bash
# Train ALL 19 KANs (14 watchdogs + 5 L9 Swarm)
cd <skill-directory>
python3 scripts/watchdog_unified_trainer.py --all --epochs 200 --samples 300

# Check status of all KANs
python3 scripts/watchdog_unified_trainer.py --status

# Train specific KAN
python3 scripts/watchdog_unified_trainer.py --kan STC --epochs 100

# Train only watchdogs (14)
python3 scripts/watchdog_unified_trainer.py --watchdogs

# Train only L9 Swarm (5)
python3 scripts/watchdog_unified_trainer.py --swarm
```

**19 KANs covered:**

| KAN | Typical Path | Role |
|-----|--------------|------|
| STC | `<AGENT_A>/stc_watchdog/models/` | Sovereign Threshold of Consciousness |
| SYN | `<AGENT_A>/syn_watchdog/models/` | Spatial/Synchron Awareness |
| FLX | `<AGENT_A>/flx_watchdog/models/` | FLX Privacy Filter |
| W7 | `<AGENT_A>/w7_watchdog/models/` | W7 Watchdog |
| EVAL_KAN | `<AGENT_A>/skills/axioma-skill-evaluator/models/` | Skill Evaluation |
| AKEP | `<AGENT_A>/Axioma Projects/L7_MORGANA/models/` | AKEP Model |
| VLS | `<AGENT_B>/vls_watchdog/models/` | Validation watchdog |
| ABS | `<AGENT_B>/abs_watchdog/models/` | Abstraction watchdog |
| CLW | `<AGENT_C>/skills/axiomata-cluster-guardian/models/` | Cluster Guardian |
| ICS | `<AGENT_C>/ics_watchdog/models/` | Integrity of Structure |
| SKILL_KAN | `<AGENT_C>/deep_memory/hybrid_kan/models/` | Deep Memory Skill KAN |
| T_KAN | `<AGENT_C>/deep_memory/models/` | Temporal KAN |
| RESEARCH_KAN | `<AGENT_A>/autoresearch/models/` | Research KAN |
| FLX_PRIVACY | `<AGENT_A>/flx_privacy_filter/models/` | FLX Privacy |
| PMB | `<KAN_SWARM>/models/kan_pmb.pth` | Project Memory Bank |
| FILE | `<KAN_SWARM>/models/kan_file.pth` | File Indexer |
| MODL | `<KAN_SWARM>/models/kan_modl.pth` | Module Analyzer |
| ENV | `<KAN_SWARM>/models/kan_env.pth` | Environment Scanner |
| CREA | `<KAN_SWARM>/models/kan_crea.pth` | Creative Memory |

**Note:** `<AGENT_A>`, `<AGENT_B>`, `<AGENT_C>` represent agent-specific workspace directories. `<KAN_SWARM>` represents the L9 Deep Memory Swarm directory.

**Cron schedule:** Training nightly at 2AM, status check at 8AM

---

## 6. KAN Core Concepts

### What is KAN?

```
╔═══════════════════════════════════════════════════════════╗
║  KAN = Kolmogorov-Arnold Networks                         ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Traditional MLP: y = σ(Wx + b)                          ║
║  KAN:          y = Σφᵢₙ(xᵢ)                             ║
║                                                           ║
║  Difference: KAN uses learnable activation functions     ║
║  instead of fixed ones. Each weight is a function, not    ║
║  a scalar.                                               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### KAN Architecture Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `input_size` | 768 | Input dimension (embedding from Ollama) |
| `hidden_size` | 32 | Hidden layer width |
| `output_size` | 3 | Output dimension (STC/SYN/FLX triplet) |
| `grid_size` | 5 | B-spline grid size |
| `k` | 3 | B-spline order |
| `layers` | [768, 32, 16, 8, 4, 3] | Layer dimensions |

---

## 7. Error Handling

### Connection Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ConnectionError: Qdrant` | Qdrant not running | `sudo /path/to/qdrant --config-path <config> &` |
| `Connection refused: 7334` | Qdrant crashed | Check watchdog: `ps aux \| grep qdrant` |
| `Connection refused: 11434` | Ollama not running | `sudo systemctl restart ollama` |

### Model Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError: model` | Model doesn't exist | Run `kan_trainer.py --train <kan>` |
| `Missing key(s) in state_dict` | Model architecture mismatch | Recreate model or check layers |
| `DimensionError: expected 768` | Wrong input_size | Check `input_size=768` config |

### Training Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Loss > 0.1` | KAN degraded | Run `kan_auto_task.py --train <kan>` |
| `OOM: out of memory` | Memory insufficient | Reduce batch_size or epochs |
| `CUDA out of memory` | GPU memory full | Use CPU: `export CUDA_VISIBLE_DEVICES=""` |

---

## 8. Constraints

### KAN Limits

| Limit | Value | Description |
|-------|-------|-------------|
| Max main KANs | 13 | STC, SYN, FLX, W7, VLS, ABS, CLW, ICS, SKILL_KAN, EVAL_KAN, T-KAN, RESEARCH_KAN, AKEP |
| Max sub-KANs | unlimited | Can create custom KANs |
| KAN output dimension | 2-3 | Standard is 3, T-KAN special is 2 |

### Training Limits

| Limit | Value | Description |
|-------|-------|-------------|
| Min training samples | 100 | Generated or real data |
| Max epochs | 100 | Prevent overfitting |
| Default batch_size | 32 | Balance speed and memory |
| Learning rate | 0.001 | Adam optimizer default |

### Technical Requirements

| Requirement | Description |
|-------------|-------------|
| PyTorch version | >= 1.9 required |
| Qdrant ports | 6333, 6336, 7334 (configurable) |
| Ollama embedding | 768D required |
| Memory | At least 4GB available |

---

## 9. Performance Benchmarks

| Operation | Expected Time | Timeout | Standard |
|-----------|---------------|---------|----------|
| Create KAN | < 5 sec | 15 sec | Dir + config generated |
| Train KAN (50 epochs) | < 2 min | 5 min | Loss < 0.1 |
| Health check | < 10 sec | 30 sec | All 13 KANs checked |
| Pipeline assembly | < 10 sec | 30 sec | JSON config generated |
| AutoResearch→KAN | < 2 min | 5 min | Research + vaccine + training |

---

## 10. Related Files

### Core Files

| File | Path | Description |
|------|------|-------------|
| SKILL.md | `<skill-dir>/SKILL.md` | This skill documentation |
| kan_creator.py | `scripts/kan_creator.py` | KAN creation script |
| kan_trainer.py | `scripts/kan_trainer.py` | KAN training script |
| kan_assembler.py | `scripts/kan_assembler.py` | KAN assembly script |
| kan_health.py | `scripts/kan_health.py` | KAN health check script |

### Integration Files

| File | Path | Description |
|------|------|-------------|
| kan_auto_task.py | `references/auto-task/kan_auto_task.py` | 13 KANs auto-optimization |
| autoresearch_task.py | `references/auto-task/autoresearch_task.py` | Research→Vaccine→KAN pipeline |
| l9_l6_bridge.py | `references/l9_l6_bridge.py` | L9-L6 bridge |

### Troubleshooting

**Q: KAN training fails with CUDA error?**
A: Use CPU mode: `python3 scripts/kan_trainer.py --kan stc --device cpu`

**Q: Qdrant connection refused?**
A: Check Qdrant is running: `sudo systemctl status qdrant`

**Q: KAN not auto-evolving?**
A: Check the cron job: `crontab -l` and ensure `kan_auto_task.py` is scheduled

**Q: Low KAN quality score?**
A: Run retraining: `python3 scripts/kan_trainer.py --kan <name> --epochs 1000 --auto-evolve`

**Q: Model file not found?**
A: Check `models/` directory exists and has `.pt` files

---

## 11. References

For detailed information, see:

| Reference | Description |
|-----------|-------------|
| `references/kan-concepts.md` | KAN internal structure and math |
| `references/pipeline-architecture.md` | Pipeline assembly details |
| `references/auto-task.md` | AutoResearch integration |
| `references/kan-list.md` | 13 KANs inventory |

---

## 11.1 Advanced: LLM → KAN Knowledge Transfer

**DISCOVERED 2026-05-13** — A breakthrough pattern for building efficient KANs using LLM as "cobaye" (teacher):

```
╔═══════════════════════════════════════════════════════════╗
║  💡 LLM → KAN KNOWLEDGE TRANSFER PATTERN                 ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  LLM (COBAYE) → Generates diverse training examples      ║
║       ↓                                                   ║
║  KAN (APPRENTI) → Learns patterns from examples          ║
║       ↓                                                   ║
║  KAN standalone → Operates WITHOUT LLM, faster + cheaper ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Why This Works

| Aspect | LLM | KAN |
|--------|-----|-----|
| Speed | ~100ms per query | **<1ms** inference |
| Cost | API calls, GPU | **One-time training, CPU** |
| Specialization | Generalist | **Specialist (trained domain)** |
| Context | Needs full context | **Learns patterns** |

### Use Cases

| Domain | LLM (Cobaye) | KAN (Apprenti) | Example |
|---------|--------------|----------------|---------|
| **Privacy** | Gemma 3 1B | FLX KAN | Detect private data ✅ EXAMPLE |
| Code Quality | Gemma | Code-KAN | Detect good/bad code |
| Security | LLM | VLS-KAN | Detect vulnerabilities |
| Spam | LLM | Spam-KAN | Classify spam/ham |
| Medical | LLM | Medical-KAN | Pattern detection |

### Implementation Pattern

```bash
# 1. Generate diverse examples using LLM (cobaye)
python3 generate_diverse_data.py --llm gemma3:1b --count 100 --output data/examples.json

# 2. Train KAN on those examples
python3 kan_trainer.py --kan flx_privacy --examples data/examples.json --epochs 5000

# 3. Use KAN standalone (no LLM needed!)
python3 flx_privacy_filter.py --input "SSN 123-45-6789"  # Returns HIGH-RISK directly
```

### FLX Privacy Example (Tested)

```
Gemma 3 1B (cobaye) → Generated 97 privacy examples
                              ↓
                    FLX KAN trained (8000 epochs)
                              ↓
         FLX KAN detects: SAFE/SENSITIVE/HIGH-RISK
         WITHOUT Gemma — 3/3 official tests PASSED ✅
```

### Code Template: LLM to KAN Transfer

```python
from flx_privacy_trainer import PrivacyFLXKAN, message_to_features

# After training, use KAN alone (no LLM needed!)
model = PrivacyFLXKAN()
checkpoint = torch.load('models/privacy_flx.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Fast inference (<1ms vs 100ms for LLM)
text = "The SSN is 123-45-6789"
features = message_to_features(text)
prediction = model(features)  # No LLM calls!
```

### Benefits Summary

| Metric | LLM Only | LLM → KAN Transfer |
|--------|----------|---------------------|
| Latency | ~100ms | **<1ms** |
| Cost per query | $0.001+ | **$0 (after training)** |
| GPU required | Yes | **No** |
| Specialization | Low | **High (trained on domain)** |

---

_In Altum Per KAN._
🧠 AXIOMA KAN SYSTEM v1.5 — 19 KANs UNIFIED TRAINER + LLM→KAN TRANSFER

**License:** MIT License

---

## 12. Support

For help with the Axioma KAN System:

| Channel | Contact |
|---------|---------|
| **Documentation** | See this SKILL.md and references folder |
| **Troubleshooting** | See Section 7 (Error Handling) |
| **KAN Health** | Run `python3 scripts/kan_health.py` |
| **Cluster Support** | Contact your cluster administrator |

### Quick Help Commands

```bash
# Check KAN status
python3 scripts/kan_health.py

# List all KANs
python3 scripts/kan_assembler.py --list

# Check training logs
cat logs/kan_training.log

# Verify installation
python3 -c "import torch; print(f'PyTorch {torch.__version__}')"
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| **1.5.0** | **2026-05-14** | **Added unified watchdog_trainer.py — 19 KANs (14 watchdogs + 5 L9 Swarm), cron training at 2AM daily** |
| **1.4.0** | **2026-05-13** | **Added LLM→KAN Knowledge Transfer pattern (Section 11.1)** |
| 1.3.0 | 2026-05-13 | Added Python API examples, troubleshooting section |
| 1.2.0 | 2026-05-12 | Added 13 KANs auto-evolution, AutoResearch pipeline |
| 1.1.0 | 2026-05-11 | Added T-KAN integration, health monitoring |
| 1.0.0 | 2026-05-10 | Initial release with 4 core scripts |