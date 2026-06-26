# Color Space Reference

## ACEScg (AP1) to Linear sRGB

The combined 3x3 matrix converting from ACEScg AP1 primaries to linear sRGB (Rec.709 primaries, D65 white point):

```
[ 1.70505  -0.62179  -0.08326]
[-0.13026   1.14080  -0.01055]
[-0.02400  -0.12897   1.15297]
```

Usage (numpy):
```python
ACESCG_TO_LINEAR_SRGB = np.array([
    [ 1.70505, -0.62179, -0.08326],
    [-0.13026,  1.14080, -0.01055],
    [-0.02400, -0.12897,  1.15297],
], dtype=np.float32)

# rgb_aces is (H, W, 3) in ACEScg
flat = rgb_aces.reshape(-1, 3)
linear_srgb = (flat @ ACESCG_TO_LINEAR_SRGB.T).reshape(H, W, 3)
linear_srgb = np.clip(linear_srgb, 0, 1)
```

This matrix is the product of:
1. ACEScg AP1 → CIE XYZ (D60)
2. Bradford chromatic adaptation D60 → D65
3. CIE XYZ → linear sRGB (Rec.709)

## sRGB OETF (Gamma Encoding)

The sRGB transfer function converts linear light to gamma-encoded sRGB. It is **piecewise**, not a simple 2.2 gamma:

```
if L <= 0.0031308:
    V = L * 12.92
else:
    V = 1.055 * L^(1/2.4) - 0.055
```

Where L is the linear value and V is the encoded value, both in [0, 1].

```python
def srgb_oetf(x):
    return np.where(
        x <= 0.0031308,
        x * 12.92,
        1.055 * np.power(np.maximum(x, 0), 1.0 / 2.4) - 0.055,
    )
```

**Do not use** `pow(x, 1/2.2)` — it's a common approximation but produces visible color shifts, especially in darks and saturated regions.

## Common VFX Pipelines

### ACEScg Render → PNG
1. Read float32 EXR channels (R, G, B)
2. Apply ACEScg→linear sRGB matrix
3. Clamp to [0, 1]
4. Apply sRGB OETF
5. Quantize to uint8

### Linear sRGB Render → PNG
1. Read float32 EXR channels
2. Clamp to [0, 1]
3. Apply sRGB OETF
4. Quantize to uint8

### Already sRGB → PNG
1. Read float32 EXR channels
2. Clamp to [0, 1]
3. Quantize to uint8

## OCIO vs Manual Matrix

**OpenColorIO (OCIO)** is the industry standard for color management. However:
- Requires a compiled C++ library with Python bindings
- Can segfault with certain builds (observed with PyOpenColorIO on Windows/WinPython)
- Needs an OCIO config file (aces_1.2, studio, etc.)

The **manual 3x3 matrix approach** used in `exr_extract.py`:
- No extra dependencies beyond numpy
- Exact same math for the ACEScg→sRGB conversion
- Portable and debuggable
- Sufficient for per-pixel linear transforms

Use OCIO when you need: LUT-based transforms, CDL grades, view transforms (ACES Output Transforms), or when working within a full color pipeline (Nuke, Houdini, etc.).

## Tone Mapping Note

The matrix approach does **not** include tone mapping. Values above 1.0 after the color space transform are simply clamped. For HDR content with bright highlights, consider:
- Reinhard: `rgb / (1 + rgb)` — simple but desaturates
- ACES Output Transform (RRT + ODT) — industry standard, requires OCIO
- Filmic curves — Blender, AGX, etc.

For most VFX beauty renders intended for review/comp, the linear clamp is acceptable since renders are typically exposed correctly.

For HDR content or camera-originated EXRs, use the **oiiotool** skill which provides proper ACES display transforms via OCIO:
```bash
oiiotool input.exr --ociodisplay "sRGB - Display" "ACES 1.0 - SDR Video" -d uint8 -o output.png
```
