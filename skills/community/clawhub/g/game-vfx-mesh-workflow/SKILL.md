---
name: game-vfx-mesh-workflow
description: >-
  Builds game VFX with mesh shell + scrolling texture + engine animation (dead
  model, live texture, engine math). Covers 2.5D billboard rules, 631 color,
  point-line-surface layering, ink-wash grading, and Godot ShaderMaterial/Tween
  patterns. Use when implementing skills, magic, heal, or combat VFX in Godot,
  choosing VFX tech route, or when the user mentions 降维打击, Mesh+贴图, UV scroll,
  Kenney, AI texture, 631配色, 点线面, or水墨特效.
---

# Game VFX: Mesh + Texture + Engine Math

## Core Philosophy

> **3D 软件造壳，AI/贴图画皮，引擎赋魂。**

```
VFX ≈ 简单 Mesh（塑料外壳）× 滚动贴图（活涂装）× 引擎数学（缩放/旋转/淡出/错开）
```

Do **not** render finished FX in DCC or rely on TyFlow/Houdini for indie iteration.
Do **not** replace textures with pure procedural `noise2d()` unless prototyping.

### Standard Pipeline

| Step | Input | Output |
|------|--------|--------|
| 1. Mesh | CC0 VFX pack **or** Godot primitives (Plane/Cylinder/Torus) | UV-ready shell |
| 2. Texture | AI seamless noise **or** CC0 sprite sheet (Kenney placeholder) | Alpha/mask + detail |
| 3. Shader | `sampler2D` + UV scroll + style grade | Visible texture shape |
| 4. Code | Tween scale / rotation / intensity / stagger | Timed performance |
| 5. Anchor | Node under Player at feet (y≈0) or chest | Correct bind point |

### AI Texture Prompt Hints

Generate **seamless**, **high-contrast** masks suitable for UV scroll:

- `seamless jade ink wash noise, high contrast alpha, tileable, 512x512, no background`
- `seamless magic energy noise, soft core bright edges dark, tileable`
- Avoid illustrative single-frame art; need **tileable mask/energy** maps.

Drop into `assets/textures/vfx/` and assign to `albedo_texture` in shader.

---

## Composition: 点 · 线 · 面

| Element | Role | Mesh | Texture examples |
|---------|------|------|------------------|
| **面** | Base area, 60% main color | Horizontal plane, large billboard | circle, smoke, magic |
| **线** | Direction, trail, ink stroke | Thin billboard, ground trace plane | slash, trace, scratch |
| **点** | Accent sparkle, scatter | Small billboards | star, spark |

Layer with **staggered delays** (0.05–0.18s). Never spawn everything at t=0.

---

## Color: 631 Rule + Contrast

| Share | Role | Usage |
|-------|------|--------|
| **60%** | Main attribute color | Pool, rings, body aura |
| **30%** | Secondary (adjacent hue) | Mist, inner glow, edge wash |
| **10%** | Accent (warm/high sat) | Gold stars, white core flash |

**Ink black (墨痕)** is not part of 631 area — use as **contrast edge** (like bubble black rims): small coverage, high opacity.

Extended formula (fluid/magic):

`主色冷色大面积 + 辅色邻近/弱对比 + 微面积色散高光 + 极小面积点缀色`

For **ink-wash projects**: main = jade/teal; secondary = blue-purple mist; accent = warm gold; ink = near-black.

---

## 2.5D / Fixed Camera Rules (Critical)

Orthographic oblique camera (e.g. offset `(20, 22.5, 20)`) breaks many free-3D assumptions.

| Do | Don't |
|----|-------|
| **Horizontal** `PlaneMesh` for ground FX | Vertical ring only visible as line |
| **Billboard** planes for body FX (`look_at` camera) | Cylinder/Torus body (shows caps, hides UV) |
| Texture **discard** on low alpha (`if mask < 0.025: discard`) | Uniform green fog without texture shape |
| Texture drives mask; shader tints | Procedural ring `mask *= ring` covering texture |
| `blend_mix` + ink grade for main layers | Full-scene neon `blend_add` |
| `blend_add` only for accent/core layer | |
| Anchor ground at `y ≈ -0.93` (feet), slightly above ground plane | Same Y as ground (z-fight) |

Billboard facing (Godot 4):

```gdscript
node.look_at(camera.global_position, Vector3.UP)
node.rotate_object_local(Vector3.RIGHT, -PI * 0.5)
node.rotate_object_local(Vector3.FORWARD, yaw_offset)
```

---

## Godot Implementation Pattern

### Shader Split (3 materials max)

| Shader | Render | Purpose |
|--------|--------|---------|
| `heal_vfx_layer.gdshader` | `blend_mix` | Main layers: 4-tone grade, UV scroll, optional expand |
| `heal_vfx_ink.gdshader` | `blend_mix` | Black ink strokes/splashes |
| `heal_vfx_add.gdshader` | `blend_add` | Gold/white accent only |

Key uniforms: `albedo_texture`, `scroll_speed`, `effect_time`, `intensity`, `expand_progress`, `tone_dark/mid/bright/accent`.

### Script Structure (`heal_mesh_effect.gd` reference)

```
HealEffect (Node3D, y=1.0 on Player)
├── Ground: pool + rings (horizontal planes)
├── Body: twirl billboards ×2 crossed yaw
├── Mist: secondary billboard (30%)
├── Ink: splashes, strokes, traces, rising flecks
└── Accent: core add + star billboards (10%)
```

API: `trigger_heal()` with cooldown; `_process` updates `effect_time` + billboard facing.

### Tween Rules

```gdscript
# CORRECT — lambda passes float to intensity
_tween.tween_method(func(v): mat.set_shader_parameter("intensity", v), 0.0, 2.0, 0.3)

# WRONG — bind appends args; float hits wrong parameter
_tween.tween_method(_set_intensity.bind(mat), 0.0, 2.0, 0.3)  # breaks in GDScript 4
```

Return type for `tween_method`: `MethodTweener`, not `Tween`.

Typed arrays for texture pick:

```gdscript
const SPARK_TEX: Array[Texture2D] = [TEX_A, TEX_B, TEX_C]
var tex: Texture2D = SPARK_TEX[i % 3]
```

---

## New Skill Checklist

Before shipping a VFX, verify:

- [ ] Texture visible in isolation (not hidden by procedural mask / fresnel kill)
- [ ] Body elements face camera in 2.5D
- [ ] 631 color balance readable on project background
- [ ] Ink/contrast layer present if style is ink-wash
- [ ] Staggered layer timing
- [ ] `preload()` textures; sync `effect_time` on all materials
- [ ] No dependency on sky/SDFGI/volumetric fog for this project style
- [ ] Headless load / in-game Q test passes

---

## Anti-Patterns (Learned in game02)

| Failed approach | Why |
|-----------------|-----|
| GPUParticles + Kenney without billboard | Side-on quads invisible in 2.5D |
| Cylinder aura | Top cap reads as geometry, not texture |
| Pure noise shaders | No craft; flat green fog |
| Procedural ring × texture | Texture shape lost |
| Stacking 10+ layers same hue | Monotone, no 631 |
| `Tween.bind()` for multi-arg setters | Runtime type errors |

---

## Reference Implementation (game02)

| Asset | Path |
|-------|------|
| Effect script | `scripts/heal_mesh_effect.gd` |
| Layer shader | `shaders/heal_vfx_layer.gdshader` |
| Ink shader | `shaders/heal_vfx_ink.gdshader` |
| Add shader | `shaders/heal_vfx_add.gdshader` |
| Textures (placeholder) | `addons/kenney_particle_pack/` |
| Scene hook | `Player/HealEffect` in `scenes/main_3d.tscn` |

Kenney mapping for heal: `smoke_06` pool, `circle_05` ring, `twirl_02` body, `light_03` halo, `magic_02` mist, `magic_04` core, `star/spark` accent, `scratch/scorch/slash/trace` ink.

For extended pitfalls and environment constraints, see [reference.md](reference.md).
