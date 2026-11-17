# Aesthetic Analysis Framework (风格分析框架)

> A rigorous methodology for synthesizing raw visual references into structured aesthetic rules, dimensional models, and reusable prompt seeds.

---

## 1. Reference Clustering Methodology

### 1.1 Clustering Principles
Group harvested references into 3–5 distinct design directions:
1. **Feature Tagging**: Tag each reference across color, typography, graphic language, material, and emotional vibe.
2. **Overlap Clustering**: Group items sharing strong dimensional overlap into candidate clusters.
3. **Consolidation**: Merge small clusters (<3 items) into adjacent directions; split overly broad buckets. Ensure every direction has ≥3 verified real-world examples.
4. **Distinct Naming**: Give each direction an evocative, recognizable style moniker (e.g., "Kinetic Neo-Brutalism", "Ethereal Frosted Minimal").

### 1.2 Differentiation Standards
- Distinct directions must visibly diverge across **at least 2 visual dimensions** (e.g., typography + graphic language, not just minor color tweaks).
- Every direction must be expressible in a single coherent thesis sentence ("What is this aesthetic?").
- Avoid redundant single-axis variations (e.g., purely "Dark Mode vs Light Mode" of the same layout).

---

## 2. Seven Dimensions of Aesthetic Deconstruction

Analyze each clustered design direction across the following 7 dimensions:

### 2.1 Color (色彩)
| Sub-Dimension | Analysis Scope |
|---|---|
| **Dominant Tone** | Primary hue family, temperature bias (e.g., warm ochre, ice cobalt) |
| **Supporting Hues** | Secondary structural accents and their roles (balance, transition) |
| **Harmony Logic** | Complementary, analogous, monochromatic, triadic, split-complementary |
| **Saturation & Value** | High chroma vs desaturated wash, high-key lightness vs moody shadows |
| **Psychological Mood** | Emotional signaling (warmth, austerity, clinical trust, rebellion) |

### 2.2 Typography (排版与版式)
| Sub-Dimension | Analysis Scope |
|---|---|
| **Typeface Style** | Serif, Sans-Serif, Geometric Mono, High-contrast Display, Handcrafted |
| **Hierarchy Scale** | Headline-to-body scale ratio, weight contrast, tracking/kerning density |
| **Negative Space** | Tight compact grouping vs expansive breathing room, asymmetry |
| **Alignment** | Flush-left, centered classical, justified editorial, experimental free-flow |
| **Typographic Rhythm** | Information chunking, visual entry points, and eye travel paths |

### 2.3 Graphic Language (图形语言)
| Sub-Dimension | Analysis Scope |
|---|---|
| **Form Vocabulary** | Strict geometric, organic curvilinear, hand-drawn vector, 3D clay/chrome |
| **Iconography** | Monoline outline, solid glyph, duotone, glassmorphic, skeuomorphic |
| **Illustration Tone** | Flat vector, risograph grain, watercolor wash, collage, technical line art |
| **Visual Density** | Sparse minimalism, balanced grid, maximalist collage |

### 2.4 Texture & Lighting (材质与光影)
| Sub-Dimension | Analysis Scope |
|---|---|
| **Substrate Texture** | Rough watercolor paper, brushed aluminum, matte velvet, film grain |
| **Gradient Dynamics** | Smooth mesh gradients, stepped duotone, chromatic aberration |
| **Shadow Treatment** | Hard architectural drop shadows, diffuse ambient occlusion, zero shadow |
| **Luminance & Glow** | Neon emission, cinematic rim light, volumetric fog, backlighting |
| **Surface Finish** | Frosted glass (glassmorphism), liquid chrome, ceramic matte |

### 2.5 Composition & Grid (构图与布局)
| Sub-Dimension | Analysis Scope |
|---|---|
| **Layout Matrix** | Modular Swiss grid, golden section, central symmetry, dynamic diagonal |
| **Visual Gravity** | Off-center focal point, corner tension, dispersed multi-focal |
| **Figure-Ground Ratio** | Positive subject vs negative space area percentage |
| **Boundary Breaking** | Bleed-off edges, overlapping frames, broken margins |

### 2.6 Emotional Tone (情绪调性)
| Sub-Dimension | Analysis Scope |
|---|---|
| **Aesthetic Keywords** | 3–5 tone descriptors (e.g., Austere, Poetic, Kinetic, Heritage) |
| **Perceived Message** | Immediate cognitive impact on the viewer |
| **Best-Fit Scenarios** | Optimal industries, mediums, or user demographics |

### 2.7 Signature Techniques (核心手法)
Identify 3–5 actionable, concrete execution techniques that define the aesthetic. Examples:
- "Treat oversized typography as the primary graphic hero."
- "Superimpose translucent geometric shapes over high-grain monochrome photography."
- "Use extreme margin padding (≥20% canvas width) to project understated luxury."

---

## 3. Prompt Derivation Guidelines

### 3.1 Structural Prompt Formula
```
[Subject/Hero], [Style/Aesthetic Movement], [Color Palette & Tone], [Texture & Lighting], [Composition & Viewpoint], [Atmospheric Emotion], --ar [W:H] --style raw
```

### 3.2 Parameter Bracketing
Always bracket customizable parameters with `[placeholder]` tags (e.g., `[Product Name]`, `[Key Subject]`), accompanied by adjustment notes (e.g., "Increase contrast for higher drama, decrease saturation for editorial calm").
