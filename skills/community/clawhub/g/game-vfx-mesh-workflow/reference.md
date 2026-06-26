# game02 VFX Reference

## Environment Constraints (Do Not Re-enable)

These caused black wedges, occlusion, or style break in game02:

- Procedural sky as main background
- SDFGI / SSIL / volumetric fog
- Scene blocking walls around player
- Realistic PBR + strong directional light for ink-unlit style

Use solid paper background (`ink_paper_env.tres`), unlit shaders, minimal post-FX.

---

## 降维打击方案 (Original Workflow)

Independent AI 3D dev path when DCC mastery is unrealistic:

1. **白嫖 3D 基础网格** — VFX Mesh Pack with ready UV (rings, cones, hemispheres, arcs).
2. **AI 生成核心材质** — Stable Diffusion / Leonardo: seamless high-contrast noise (magma, energy, ink wash).
3. **引擎组装**:
   - Import mesh
   - Material: AI texture + **UV Animation** (Y scroll ~2 cycles/s)
   - Code: self-rotate (e.g. 360°/s), scale up, fade out

Result: rich detail from texture, motion from code — not from offline rendered FX.

**Adaptation for 2.5D ink game**: replace cone tornado with ground ring + vertical billboards; replace sci-fi emissive with ink grade + jade palette.

---

## Aesthetic Reference Notes

### 游戏特效定义

Dynamic visuals beyond character/scene: skills, hits, environment, mood — makes actions feel powerful.

### 631 口诀

六做主色定基调，三做辅色拉层次，一做点缀提高光。

### 流体/魔法配色扩展

`主色（冷色大面积）+ 对比焦点色（邻近色小面积）+ 色散高光（彩虹微面积）+ 点缀色（冷暖对比极小面积）`

game02 heal mapping:

- 主色 60%: jade green twirl/circle/smoke
- 辅色 30%: blue-purple magic mist
- 点缀 10%: gold star/spark additive
- 墨痕: black scratch/slash/trace (contrast, not counted in 631 area)

### 水泡技能参考 (translated to heal)

- Core fluid volume → twirl billboard body
- Bubble black edge → ink stroke shader dark rim
- Gold star trails → spark billboards rising
- Fan/spread shape → ground ring expand via `expand_progress` + mesh scale

---

## Shader Uniform Cheat Sheet

### heal_vfx_layer.gdshader

- `tone_dark / tone_mid / tone_bright / tone_accent` — 4-stop grade
- `scroll_speed`, `effect_time` — UV animation
- `expand_enabled`, `expand_progress` — ground ring expand from center
- `intensity` — tween fade (0–4)
- `texture_gain` — boost mask contrast

### heal_vfx_ink.gdshader

- `ink_black`, `ink_edge` — near-black with subtle green edge
- Same scroll/expand as layer

### heal_vfx_add.gdshader

- `glow_color`, `core_color` — warm gold / white core
- `blend_add` only

---

## Iteration History (What Changed)

1. Procedural spheres/leaves → rejected (no assets, flat)
2. Kenney GPUParticles → rejected (billboard/orientation, neon)
3. Cylinder + noise shader → rejected (2.5D sees geometry not texture)
4. Mesh + scroll + Kenney + billboards + 631 + ink → **current**

When user says "only geometry no texture": check mesh type (cylinder caps), mask multiplication, fresnel kill, and ink_blend crushing detail.

---

## Optional Upgrade Path

Replace Kenney placeholders with AI seamless textures per skill:

1. Generate 512² seamless mask PNG
2. Place in `assets/textures/vfx/<skill>_energy.png`
3. Swap `preload` in effect script — keep shader/code unchanged

Effekseer / flipbook sequences: use for hero skills later; higher integration cost in Godot.
