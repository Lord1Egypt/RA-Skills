# Cryptomatte Format Reference

## Overview

Cryptomatte is an open standard for storing ID-based matte information in EXR files. It embeds object, material, or asset identifiers directly into render passes, enabling automatic matte extraction in compositing without manual rotoscoping.

## How It Works

### Hash-Based IDs

Each object/material name is hashed to a 32-bit integer using **MurmurHash3_32**. This hash is then stored in the EXR as a **float32** by reinterpreting the uint32 bits as IEEE 754 float (not casting — the numerical value is meaningless as a float).

To decode:
```python
# Read as float32 from EXR
id_float = read_channel('crypto_material00.R')  # shape (H, W), dtype float32

# Reinterpret bits as uint32 (NOT a cast)
id_uint32 = id_float.view(np.uint32)
```

### Channel Layout

Cryptomatte data is stored in ranked pairs across multiple channel groups:

```
crypto_material00.R  = ID of rank-0 (most dominant) material at each pixel
crypto_material00.G  = coverage/weight of rank-0 material [0.0 - 1.0]
crypto_material00.B  = ID of rank-1 material
crypto_material00.A  = coverage of rank-1 material

crypto_material01.R  = ID of rank-2 material
crypto_material01.G  = coverage of rank-2
crypto_material01.B  = ID of rank-3 material
crypto_material01.A  = coverage of rank-3

crypto_material02.R  = ID of rank-4 material
crypto_material02.G  = coverage of rank-4
...
```

Each level (`00`, `01`, `02`) stores two ID/coverage pairs. Most files have 3 levels (6 ranks), which is enough for typical scenes.

The **rank-0 pair** (`00.R` and `00.G`) is usually sufficient for flat-color ID visualizations — it gives the dominant material at each pixel.

### Preview Channel

Some renderers also write a preview/visualization channel:
```
crypto_material.R, .G, .B
```
This is a pre-computed RGB visualization (low-quality hash-derived colors). The extraction script ignores this and builds its own palette.

## Channel Naming by Renderer

Different renderers use different naming conventions:

| Renderer | Material | Object | Asset |
|----------|----------|--------|-------|
| Arnold (standard) | `crypto_material00` | `crypto_object00` | `crypto_asset00` |
| Arnold (short) | `crypto_mat00` | `crypto_obj00` | — |
| V-Ray | `crypto_material00` | `crypto_object00` | `crypto_asset00` |
| Redshift | `crypto_material00` | `crypto_object00` | `crypto_asset00` |

The extraction script auto-detects both standard and shortened naming.

## Crypto Types

### crypto_material
Segments by **material/shader assignment**. Objects sharing the same material get the same ID. Most useful for:
- Material identification in renders
- Training segmentation models on material boundaries

### crypto_object
Segments by **scene object/shape**. Each mesh/geometry gets a unique ID regardless of material. Useful for:
- Object-level masks for compositing
- Instance segmentation

### crypto_asset
Segments by **asset/group** in the scene hierarchy. Multiple objects that belong to the same asset (e.g., all parts of a car) share one ID. Useful for:
- High-level asset selection
- Grouping related objects

## EXR Metadata

Cryptomatte stores metadata in the EXR header under keys like:

```
cryptomatte/{hex_id}/name:       crypto_material
cryptomatte/{hex_id}/hash:       MurmurHash3_32
cryptomatte/{hex_id}/conversion: uint32_to_float32
cryptomatte/{hex_id}/manifest:   {"MaterialName":"hex_hash", ...}
```

The **manifest** is a JSON dict mapping human-readable names to their hex-encoded uint32 hashes. This allows looking up what each hash ID actually represents.

Example:
```json
{
  "car_paint_red_mtl": "5fb1af9a",
  "glass_windshield_mtl": "583231f2",
  "tire_rubber_mtl": "a3c1e7b2"
}
```

The hex hash can be converted: `int("5fb1af9a", 16)` → uint32 → reinterpret as float32.

## Background Detection

Pixels with zero coverage (`00.G == 0.0`) have no material data — these are truly empty (outside the rendered object, alpha=0 regions).

The **background material** (sky, environment, ground plane) typically has coverage but is the most common ID at the image edges. The extraction script samples edges and corners:

```python
edge_samples = concat([
    ids[0, :],              # top row
    ids[-1, :],             # bottom row
    ids[:, 0],              # left column
    ids[:, -1],             # right column
    ids[0:10, 0:10],        # corners (10x10 blocks)
    ids[0:10, -10:],
    ids[-10:, 0:10],
    ids[-10:, -10:],
])
bg_id = most_common(edge_samples)
```

This background ID is assigned a neutral color (gray) to avoid wasting a bold palette slot on the largest-area but least-interesting region.
