---
name: gan-evolution-engine
description: >
  Generative Adversarial Evolution for AI Agent Skills. Uses GAN-like process to evolve
  skill capabilities: Generator creates skill variants, Discriminator evaluates performance,
  iterative selection promotes high-fitness mutations. Integrates with evomap-publish for
  capsule submission.
tags: [evolution, gan, self-improvement, meta]
---

# 🧬 GAN Evolution Engine

**"进化即对抗：生成变异，判别优劣，迭代超越"**

The **GAN Evolution Engine** implements a generative adversarial approach to skill evolution. Instead of random mutations, it uses a learned Generator to propose skill modifications and a Discriminator to evaluate their fitness based on runtime metrics and user feedback.

## ✨ Features

- **🎲 Generator Network**: LLM-powered generation of skill variants (code, prompts, logic)
- **⚖️ Discriminator**: Performance-based fitness evaluation (accuracy, speed, user satisfaction)
- **🔁 Adversarial Loop**: Generator vs Discriminator co-evolution drives rapid improvement
- **📈 Population Management**: Maintains diverse pool of skill variants
- **🚀 Elite Selection**: Top-performing variants become candidates for promotion
- **📊 Integration**: Seamless integration with `evomap-publish` for capsule submission

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐
│   Generator     │     │  Discriminator   │
│  (LLM Agent)    │────▶│  (Perf Analyzer) │
└─────────────────┘     └──────────────────┘
         │                        │
         ▼                        ▼
   Skill Variants          Fitness Scores
         │                        │
         └────────┬───────────────┘
                  ▼
         Selection & Crossover
                  │
                  ▼
           Next Generation
```

---

## 📦 Usage

### Quick Start

```bash
# 1. Ensure evomap-publish is configured
mkdir -p ~/.evomap
echo "node_db2f95ffdba95eb6" > ~/.evomap/node_id
echo "d846e0f269030e8b3eb3ed60472b164b448f8360e578a6392ccc4740d096ba14" > ~/.evomap/node_secret

# 2. Run GAN evolution cycle
python3 scripts/gan_evolution.py --skill <target-skill> --generations 10 --population 20
```

### CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `--skill` | Target skill to evolve | required |
| `--generations` | Number of evolution cycles | 10 |
| `--population` | Population size per generation | 20 |
| `--elite-ratio` | Fraction of elite variants to keep | 0.2 |
| `--mutation-rate` | Probability of mutation | 0.1 |
| `--output` | Output directory for evolved skills | `evolved/` |
| `--promote` | Auto-promote top variants to production | false |
| `--publish` | Submit top capsule to EvoMap | false |

---

## 🔬 How It Works

### 1. Population Bootstrap
- Clone target skill as initial population (population=N)
- Apply random mutations to diversify initial pool

### 2. Generator Phase
For each generation:
- Prompt LLM with:
  - Parent skill code
  - Performance metrics (from Discriminator)
  - Mutation strategy (crossover, parameter tuning, prompt refinement)
- Generate `population` variant candidates

### 3. Evaluation Phase (Discriminator)
For each variant:
- Deploy in sandbox environment
- Run benchmark suite (accuracy, latency, resource usage)
- Collect user feedback if available
- Compute **fitness score** = weighted sum:
  ```
  fitness = 0.4 * accuracy + 0.3 * speed + 0.3 * feedback
  ```

### 4. Selection & Crossover
- Select top `elite_ratio * population` variants
- Perform crossover: combine code fragments from 2 parents
- Apply mutations to non-elite variants
- Form next generation population

### 5. Termination
After `generations` cycles:
- Select best variant (highest fitness)
- Optionally: promote to production (`--promote`)
- Optionally: create capsule and publish to EvoMap (`--publish`)

---

## 📊 Example Output

```
Generation 1/10
  Population: 20 variants
  Best fitness: 0.72 (variant-07)
  Avg fitness: 0.45
  Generator time: 2m 13s
  Discriminator time: 1m 42s

...

Evolution Complete! 🏆

🏆 Champion: variant-43 (fitness=0.89)
📈 Improvement: +22% over baseline
🚀 Promoted: skills/evolved/<skill>-v2/
📤 Capsule ID: sha256:abc123... (published)
```

---

## ⚙️ Implementation Details

### Files

```
gan-evolution-engine/
├── SKILL.md                 # This file
├── scripts/
│   ├── gan_evolution.py    # Main orchestrator
│   ├── generator.py        # LLM-based variant generation
│   ├── discriminator.py    # Performance evaluation
│   ├── population.py       # Population management
│   └── fitness.py          # Fitness computation
└── references/
    └── prompts/            # Generator prompt templates
```

### Key Functions

- `GANEvolutionEngine.__init__(skill_path, population, generations)`
- `Engine.bootstrap_population()`: Clone + mutate initial pool
- `Engine.run_generation()`: One full cycle
- `Generator.generate_variant(parent, strategy)`: Create new variant
- `Discriminator.evaluate(variant)`: Return fitness score 0-1
- `Population.select_elites()`: Top K variants
- `Population.crossover(parent1, parent2)`: Create child

---

## 🛡️ Safety & Risk

| Risk | Mitigation |
|------|------------|
| **Degenerate Skills** | Validation suite runs before evaluation; invalid variants discarded |
| **Infinite Loop** | Hard generation limit; timeout per variant (5min) |
| **Performance Regression** | Require fitness > baseline before promotion |
| **Code Injection** | Sandboxed execution; no network access for variants |
| **Resource Exhaustion** | Population size capped at 100; parallel evaluations limited |

---

## 🧪 Testing

Run unit tests:

```bash
python3 -m pytest tests/gan_evolution/ -v
```

---

## 📜 License
MIT

---

*"Evolution is not random mutation alone; it's the selective amplification of success."*