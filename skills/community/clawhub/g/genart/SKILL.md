---
name: genart
description: Generate algorithmic visual art — flow fields, fractals, cellular automata, circle packing, wave patterns. SVG + PNG output.
metadata:
  openclaw:
    emoji: "🎨"
---

# GenArt Skill

Procedural visual art generator using Python. Produces SVG vector art and PNG raster output from algorithmic patterns and mathematical structures.

## Algorithms

### Flow Fields
Perlin noise-based vector fields that guide particle motion, creating organic flowing patterns and fluid-like aesthetics.

### Fractals
Recursive geometric structures: Mandelbrot sets, Julia sets, L-systems, and self-similar branching patterns with configurable depth and parameters.

### Cellular Automata
Conway's Game of Life and variants, generating complex patterns from simple local rules. Produces static snapshots or animated sequences.

### Circle Packing
Algorithm-driven placement of circles in constrained spaces, creating organic compositions with visual balance.

### Wave Patterns
Sinusoidal and superposed wave interference, creating ripple effects, moiré patterns, and harmonic visualizations.

## Usage

```bash
genart.py --algorithm flow_field --output art.svg [--params "noise=0.5,scale=10"]
genart.py --algorithm fractal --output mandelbrot.png --width 1024 --height 1024
genart.py --algorithm cellular_automata --output ca.svg --iterations 100
genart.py --algorithm circle_pack --output circles.svg --target-count 200
genart.py --algorithm waves --output waves.png --frequency 5 --amplitude 100
```

Outputs SVG for scalable vector art or PNG for raster. All fully deterministic and scriptable.

## Features

- **Deterministic:** Seed-based generation for reproducible art
- **Scalable:** SVG output scales infinitely without quality loss
- **Raster export:** PNG rendering for web and print
- **Configurable:** Every algorithm exposes tunable parameters
- **Fast:** Optimized Python with optional NumPy acceleration
