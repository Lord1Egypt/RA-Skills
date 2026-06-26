# Curiosity Loop — Intrinsic Curiosity-Driven Continuous Learning

A self-improvement framework for AI agents that transforms knowledge gaps and failed outcomes into structured learning cycles.

## Overview

The Curiosity Loop treats failures not as errors but as **curiosity signals** — prompts for active exploration, skill updates, and curriculum building. This creates a continuous self-improvement loop that makes the agent progressively better at its domain.

### Inspired by Developmental AI

Built on research from [Flowers Lab, INRIA](https://www.robots.org/flowers-lab/) and the work of Cédric Colas:

- **Automatic Curriculum Learning (ACL)** — structured progression, not random learning
- **Autotelic Activity** — intrinsic motivation to learn for its own sake
- **Zone of Proximal Development (ZPD)** — learning "just beyond" current capability
- **Map-Elites / Behavioral Diversity** — maximize repertoire diversity, not single optimization
- **Semantic Interference** — biases reveal representation limits

## Installation

```bash
# Install from this repo
hermes skills tap add https://github.com/USER/REPO

# Or install directly
hermes skills install https://raw.githubusercontent.com/USER/REPO/main/SKILL.md
```

## Usage

The Curiosity Loop activates automatically when the agent detects:

1. **Result delta** — a response does not produce the expected effect
2. **Iterative loop** — user repeats the same correction 2+ times
3. **Incomplete knowledge** — missing information for a correct answer
4. **Sub-optimal approach** — recognizing a better approach exists
5. **Knowledge scan** — discovering new concepts via periodic scanning

The 6-step loop: **Action → Delta → Curiosity → Research → Integration → Curriculum**

## Structure

```
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── references/
│   └── flowers-lab-concepts.md # Academic reference documentation
└── scripts/
    └── scan_sources.py         # Periodic knowledge scanner
```

## Periodic Scanning

Configure knowledge sources in `~/.hermes/deltas.json`:

```json
{
  "scan_sources": [
    {
      "name": "Flowers INRIA",
      "type": "youtube_channel",
      "url": "https://www.youtube.com/channel/UCrBNVs3u3mwlRsm2v3EKuXA",
      "last_scanned": "2026-05-22"
    }
  ]
}
```

Run the scanner:
```bash
python3 ~/.hermes/skills/research/curiosity-loop/scripts/scan_sources.py
```

## License

MIT License — feel free to use, adapt, and contribute.

## References

- Portolas et al., "Automatic Curriculum Learning for Deep RL: a Short Survey"
- Cédric Colas, "Automatic Curriculum Learning for Developmental Machine Learners" (PhD Thesis, INRIA, 2022)
- Mouret & Clune, "Illuminating Search Spaces" (Map-Elites, 2015)
