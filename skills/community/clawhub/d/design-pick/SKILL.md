---
name: design-pick
description: "Generates multi-themed food collages (Viral Cakes, Street Food, Smoothie Bowls, Coffee Art, Fusion Tacos). Use when user asks for a collage of specific food categories, layouts with circle-masked images, or when they want to 'pick' items from a curated list."
---

# Design Pick

This skill generates high-quality food collages based on predefined themes.

## Usage

Use the `generate_collage.py` script to generate collages. 

```bash
python3 /root/.openclaw/workspace/skills/design-pick/scripts/generate_collage.py
```

## Features

- **Collage Layout**: Generates a 3x3 grid of circular-masked images.
- **Dynamic Titles**: Automatically handles "PICK 2..." or "PICK 3..." titles based on the theme.
- **Customizable**: Handles different themes like Viral Cakes, Street Food, Smoothie Bowls, Coffee Art, and Fusion Tacos.

## Themes

- Viral_Cakes
- Street_Food
- Smoothie_Bowls
- Coffee_Art
- Fusion_Tacos
