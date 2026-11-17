# Concept Cartographer

**Auto-generate prerequisite maps for learning any topic. Shows what to learn first, what depends on what, and the optimal learning path.**

## The Real-World Problem

Every self-learner hits the same wall: **"Where do I start?"**

You want to learn quantum computing. A quick search reveals you need linear algebra. But linear algebra requires calculus. And calculus needs... where does it end? Without a map, you either:
- **Give up** because the prerequisite chain seems infinite
- **Start at the wrong level** and bounce off material that's too advanced
- **Waste months** studying things in the wrong order, having to backtrack

This is called the **prerequisite problem** — it's the #1 barrier to self-directed learning. Universities solve it with curricula and advisors. Self-learners have... Google and guesswork.

## Who Needs This

- **Self-directed learners** pursuing any new skill or field
- **Career changers** entering tech, data science, finance — fields with steep prerequisite chains
- **Students** planning self-study alongside or ahead of formal education
- **Bootcamp graduates** who need to fill foundational gaps
- **Hobbyists** picking up complex skills (electronics, music theory, chess)
- **Mentors and teachers** helping others plan a learning journey

## How It Works

Concept Cartographer models knowledge as a **directed acyclic graph (DAG)** — a network where:
- **Nodes** are concepts/skills (e.g., "calculus", "neural networks")
- **Edges** point from prerequisites to dependents (calculus → gradient descent)

Using graph algorithms, it can:
1. **Topological sort** — find valid learning orders where prerequisites always come first
2. **Path finding** — compute the shortest sequence from your current knowledge to a target
3. **Critical path** — identify the longest dependency chain (your minimum time to competence)
4. **Gap analysis** — compare your knowledge against requirements and highlight missing pieces

## Quick Start

```bash
# Map prerequisites for a topic
python scripts/cartographer.py map "machine learning"

# Generate a personalized learning path
python scripts/cartographer.py path "machine learning" --known "python,statistics"

# Find your knowledge gaps
python scripts/cartographer.py audit "deep learning" --known "python,linear-algebra"
```

## Example Scenario

**Sarah**, a marketing analyst, wants to transition into machine learning. She knows Python and basic statistics. She runs:

```bash
python scripts/cartographer.py path "deep learning" --known "python,basic-statistics"
```

**Output:**
```
🎯 Target: Deep Learning
📊 Current knowledge: 2 concepts
⏱️  New concepts to learn: 7
🛤️  Critical path length: 5 steps

PATH:
  1. ☐ Linear Algebra — vectors, matrices, eigenvalues (essential for ML)
  2. ☐ Calculus — derivatives, gradients (needed for optimization)
  3. ☐ Probability Theory — distributions, Bayes' theorem
  4. ☐ Machine Learning Basics — supervised/unsupervised learning, evaluation
  5. ☐ Neural Networks — backpropagation, architectures
  6. ☐ Deep Learning — CNNs, RNNs, transformers
     └── 🎯 TARGET REACHED

Estimated time: 6–9 months at 10h/week
```

Sarah now has a clear, sequenced plan. She starts with linear algebra, knowing exactly why she needs it and what comes next.

## Why It Works

- **Reduces cognitive load**: You don't have to figure out the sequence — the algorithm does
- **Prevents false starts**: You never begin material you're not prepared for
- **Motivates through clarity**: Seeing the whole path makes the goal feel achievable
- **Respects your time**: Skips what you already know; focuses on gaps only

## Installation

```bash
git clone https://github.com/voronindenis5/concept-cartographer.git
cd concept-cartographer
# No external dependencies required — pure Python
```

## License

MIT — free for personal and educational use.
