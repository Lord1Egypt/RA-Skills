# Video Generation Scenarios & Model Configuration

**Purpose**: Scenario-to-model mapping for ambiguous cases.

**Usage**: Read this only when user intent doesn't clearly match a specific model choice in SKILL.md.

**Fallback Source of Truth**: Exact automatic fallback pairs are defined only in `fallback_models.json` and consumed by `scripts/run_task.py`. This file selects primary models and params; do not treat it as the authoritative fallback mapping.

---

## Part 1: Text-to-Video

### T2V-1: General Text-to-Video
**Use Case**: User provides only a text description to generate a video from scratch.

**Model**: `doubao-seedance-2-0-260128` → `text2video`
**Params**: `aspect_ratio` as requested, `resolution` per model max

---

## Part 2: Single-Image-to-Video

### I2V-1: Single Image Animation
**Use Case**: User provides a single image and wants to animate it or turn it into a video.

**Model**: `doubao-seedance-2-0-260128` → `single_image2video`
**Params**: `aspect_ratio="16:9"`, `resolution` per model max

---

## Part 3: Interpolation

### INT-1: First & Last Frame Interpolation
**Use Case**: User provides a starting image and an ending image, wanting a video that transitions between them.

**Model**: `doubao-seedance-2-0-260128` → `start_end_frame2video`  
**Params**: `aspect_ratio="16:9"`, `resolution` per model max

---

## Part 4: Multi-Image Reference

### MR-1: Multi-Image Reference Video
**Use Case**: User provides multiple images and wants to combine them into a video.

**Model**: `doubao-seedance-2-0-260128` → `multiple_image2video`  
**Params**: `image_urls` (>=2), `aspect_ratio="16:9"`, `resolution` per model max
