# IMAGE PROMPT ENGINEERING

> Techniques for constructing effective AI image prompts across all models — apply when creating image prompts for any AI image generation model.

---

## CORE PRINCIPLES

Master these five principles for consistent prompt quality:

### 1. Clarity Over Cleverness

**Principle:** AI models interpret literally. Clear, explicit descriptions outperform clever or poetic language.

**Good Practice:**
- ✅ "A red sports car on a mountain road at sunset"
- ✅ "Isometric view of a voxel art castle, blocky geometry"
- ✅ "Close-up portrait, soft studio lighting, shallow depth of field"

**Bad Practice:**
- ❌ "A speedy beauty conquering peaks" (too vague)
- ❌ "Dreamy architectural wonder" (unclear style)
- ❌ "Artsy photo" (no specific guidance)

**Why It Works:** Models process concrete nouns, adjectives, and spatial relationships better than abstract concepts or metaphors.

### 2. Layered Construction

**Principle:** Build prompts in layers from general to specific. Each layer adds refinement without contradicting previous layers.

Start with your main subject, progressively add defining details, set the visual arrangement, then apply style and aesthetic choices. This left-to-right progression ensures AI models weight your most important elements (subject and details) higher than modifiers (style, lighting, technical specs).

**Why This Matters:** AI models process prompts with left-to-right weighting bias. Information at the beginning receives more attention than information at the end. By placing subject and defining details first, you ensure they dominate the output.

**The Layered Approach:**

```
Start → SUBJECT (what) → ACTION (doing what - if applicable)
     → KEY DETAILS (defining characteristics)
     → ENVIRONMENT (setting/context - if applicable)
     → COMPOSITION (how arranged/framed)
     → STYLE (aesthetic) → LIGHTING (light sources)
     → COLOR (palette) → TECHNICAL (quality) → End
```

**Example Construction:**

```
Layer 1: A wizard
Layer 2: reading from ancient tome
Layer 3: elderly with long white beard, purple robes
Layer 4: in ancient library with bookshelves and floating candles
Layer 5: medium shot, rule of thirds composition
Layer 6: in fantasy art style
Layer 7: warm candlelight with soft shadows
Layer 8: rich purples and golds
Layer 9: high detail, 16:9 aspect ratio
```

**Final Prompt:** "A wizard reading from ancient tome, elderly with long white beard and purple robes, in ancient library with bookshelves and floating candles, medium shot with rule of thirds composition, in fantasy art style, warm candlelight with soft shadows, rich purples and golds, high detail, 16:9 aspect ratio"

> 📖 **See UNIVERSAL PROMPT STRUCTURE section below for the complete optimized formula and detailed component breakdown.**

### 3. Specificity Wins

**Principle:** Specific descriptors produce more predictable results than generic terms. Replace vague adjectives with precise details.

**Vague → Specific Transformations:**

| Vague | Specific |
|-------|----------|
| "beautiful lighting" | "golden hour sunlight, soft shadows, warm glow" |
| "cool colors" | "deep blues, teals, and purple accents" |
| "modern style" | "minimalist design, clean lines, monochromatic palette" |
| "nice composition" | "rule of thirds, leading lines, foreground interest" |
| "artistic" | "impressionist brushstrokes, visible texture, painterly" |

**Specificity Hierarchy:**

```
Generic → Category → Specific → Precise

"car" → "sports car" → "red Ferrari" → "1967 Ferrari 275 GTB/4"
"building" → "castle" → "medieval castle" → "Gothic castle with pointed arches and flying buttresses"
"lighting" → "natural light" → "sunset lighting" → "golden hour backlighting at 30° angle"
```

### 4. Sensory Details

**Principle:** Engage multiple senses through visual proxies. Describe texture, atmosphere, temperature, and mood visually.

**Sensory Categories:**

**Texture:**
- "smooth glass surface, reflective"
- "rough stone walls, weathered and cracked"
- "soft fabric folds, flowing silk"

**Atmosphere:**
- "misty morning atmosphere, diffused light"
- "clear crisp air, sharp details"
- "hazy dreamlike quality, soft focus"

**Temperature (Visual):**
- "warm golden tones, sunset glow"
- "cool blue palette, ice and snow"
- "neutral grays, overcast ambiance"

**Mood (Lighting + Color):**
- "energetic: vibrant colors, high contrast, dynamic lighting"
- "serene: soft pastels, gentle gradients, even lighting"
- "mysterious: deep shadows, chiaroscuro, limited light sources"

### 5. Style File Priority

**Principle:** This file provides universal methodology and structure. When a style file is specified, follow its vocabulary and keyword recommendations. Only create vocabulary freely when no style file exists.

**Hierarchy:**
- **Universal Guidelines (This File)** - Methodology, structure, layering approach, composition techniques
- **Style-Specific Files** - Vocabulary, keywords, aesthetic choices, some technical parameters
- **Fallback** - Create vocabulary independently only when no style file is available

**In Practice:**
- ✅ Use style file's specified keywords for subject, details, lighting, color
- ✅ Apply this file's structure and layering methodology
- ✅ Combine style vocabulary with universal composition techniques
- ❌ Don't override style file's vocabulary choices
- ❌ Don't add generic keywords when style file provides specific ones

**Example:**
- Style file specifies: "blocky geometry, cubic forms, isometric view"
- This file teaches: Layer structure (SUBJECT → DETAILS → COMPOSITION → STYLE)
- Correct output: "voxel art castle, blocky geometry with cubic forms, isometric view, rule of thirds" (style vocabulary + universal structure)
- Incorrect: "geometric castle, modern polygonal design" (ignoring style vocabulary)

---

## UNIVERSAL PROMPT STRUCTURE

Apply this structure for all models, then adapt syntax for specific platforms.

### The Optimized Formula

```
[SUBJECT], [ACTION], [KEY DETAILS], [ENVIRONMENT], [COMPOSITION], in [STYLE], [LIGHTING], [COLOR], [TECHNICAL]
```

**Why This Order:**
- **Subject First** - Establishes what the image is about (highest left-to-right weight)
- **Action Next** - What subject is doing (if applicable)
- **Key Details** - Defines subject characteristics before modifiers
- **Environment** - Setting/context where subject exists (if applicable)
- **Composition** - Camera work and framing decisions
- **Style** - Aesthetic applied to fully-defined scene
- **Lighting** - Light sources create atmosphere
- **Color** - Palette specifications work with lighting
- **Technical Last** - Quality and rendering specifications (lowest weight)

**Component Priority:**

**MANDATORY (always include):**
- **SUBJECT** - Core entity or scene being depicted
- **COMPOSITION** - Camera angle, framing, layout
- **STYLE** - Visual aesthetic and artistic approach
- **LIGHTING** - Light sources, quality, direction

**CONDITIONAL (use when applicable):**
- **ACTION** - Only if subject has action/activity
- **ENVIRONMENT** - Only when subject is entity in important setting

**IMPORTANT (recommended for most prompts):**
- **KEY DETAILS** - Characteristics that define the subject
- **COLOR** - Color palette when specific colors matter

**OPTIONAL (use selectively):**
- **TECHNICAL** - Quality parameters (at minimum: aspect ratio recommended)

### Breaking Down Each Component

#### 1. SUBJECT (Mandatory)

**What:** Core entity or scene being depicted - the "what" of your image

**Format:** Concise noun phrase identifying main focus (keep to 1-5 words)

**Types:**
- **Single Entity:** character, creature, object, building
- **Scene/Location:** landscape, cityscape, interior, environment

**Examples:**
- Single entity: "A dragon", "A wizard", "A sports car", "A Gothic cathedral"
- Scene: "A fantasy landscape", "A cyberpunk cityscape", "A throne room"

**Rules:**
- ✅ Keep short and focused - this gets highest left-to-right weighting
- ✅ Use concrete nouns, avoid vague terms
- ❌ Don't add descriptors here (save for KEY DETAILS)
- ❌ Don't describe location here (use ENVIRONMENT)

---

#### 2. ACTION (Conditional - only if subject has action)

**What:** What the subject is doing - verb phrase describing activity or state

**Format:** Verb phrase or participial phrase

**When to use:**
- ✅ Subject performing action: "breathing fire", "reading book", "flying through clouds"
- ✅ Subject in specific pose: "standing heroically", "crouching in shadows"
- ❌ Skip for static subjects: landscapes, architecture, still objects
- ❌ Skip for neutral portraits without specific action

**Examples:**
- "breathing fire"
- "reading from ancient tome"
- "racing through city streets"
- "typing on holographic keyboard"
- "floating in cosmic void"
- "wielding flaming sword"

**Detail levels:**
- Simple: "flying"
- Detailed: "soaring through storm clouds trailing fire"

**Rules:**
- Place immediately after SUBJECT
- Can be single word or descriptive phrase
- Skip entirely if not applicable (don't force it)

#### STYLE
**What:** Visual aesthetic and artistic approach
**Categories:**
- Art Style: "voxel art", "photorealistic", "watercolor painting"
- Time Period: "1980s retro", "futuristic", "medieval"
- Reference: "Studio Ghibli style", "Blade Runner aesthetic"

**Examples:**
- "in voxel art style, blocky cubic geometry"
- "photorealistic 3D render"
- "hand-drawn anime style, cel-shaded"

#### COMPOSITION
**What:** Camera work, framing, spatial arrangement
**Key Elements:**
- **Camera Angle:** "isometric view", "bird's eye view", "low angle looking up"
- **Framing:** "close-up", "medium shot", "wide establishing shot"
- **Layout:** "centered composition", "rule of thirds", "symmetrical"
- **Negative Space:** "top third reserved for text", "minimal negative space"

**Examples:**
- "isometric view, wide shot, centered composition"
- "close-up portrait, shallow depth of field, subject filling frame"
- "aerial view looking down, symmetrical layout"

---

#### 3. KEY DETAILS (Important - subject characteristics)

**What:** Defining characteristics of the SUBJECT before style modifies it

**Scope depends on subject type:**

**When SUBJECT = Single Entity (character, object, building):**
- Physical attributes: size, shape, color, texture, material
- Defining features: ornate, weathered, glowing, mechanical, ancient
- Subject qualities: elderly, muscular, transparent, sleek

**When SUBJECT = Scene (landscape, cityscape, interior):**
- Key elements within the scene
- Defining features that make scene distinctive
- Objects/structures that characterize the environment

**Format:** Comma-separated concrete descriptors

**Examples:**

*Single Entity - Portrait:*
- "elderly man with long white beard, deep-set eyes, weathered face"
- "young woman with flowing red hair, bright green eyes, freckles"

*Single Entity - Creature:*
- "red scales, massive wingspan, sharp horns, glowing amber eyes"
- "translucent form, flowing ethereal wisps, soft blue glow"

*Single Entity - Object:*
- "sleek aerodynamic design, matte black finish, glowing blue accents"
- "ornate golden frame, intricate engravings, jeweled details"

*Single Entity - Architecture:*
- "pointed arches, flying buttresses, tall spire, stained glass windows"
- "glass facade, steel framework, geometric patterns, minimalist design"

*Scene - Landscape:*
- "floating islands, cascading waterfalls, glowing crystals, cherry blossom trees"
- "rugged mountains, pine forests, winding river, snow-capped peaks"

*Scene - Cityscape:*
- "towering skyscrapers, neon signs, rain-slicked streets, holographic billboards"
- "medieval streets, cobblestone paths, timber buildings, market stalls"

**Rules:**
- ✅ Describe observable characteristics (what you can see)
- ✅ Focus on defining attributes, not emotions
- ❌ Don't describe WHERE subject is (use ENVIRONMENT)
- ❌ Don't describe HOW it's styled (use STYLE)

**Note:** These define WHAT the subject IS, before other components modify it.

---

#### 4. ENVIRONMENT (Optional - setting/context)

**What:** Location, setting, or context where subject exists - includes environmental details

**Format:** Prepositional phrase with location and details

**When to use:**
- ✅ SUBJECT is single entity (character, object, building) AND environment is important to image
- ❌ SUBJECT is scene/location (landscape, interior) - redundant, scene IS environment
- ❌ Isolated shots (close-up portraits, product shots with no context)

**Detail levels:**

*Simple environment (location only):*
- "in ancient library"
- "on battlefield"
- "underwater"
- "in futuristic laboratory"

*Detailed environment (location + features):*
- "in ancient magical library with towering bookshelves, floating candles, and leather-bound tomes"
- "on war-torn battlefield with smoke, debris, and distant fires"
- "in underwater coral reef with colorful fish and swaying seaweed"
- "in futuristic laboratory with holographic displays, gleaming equipment, and neon accent lighting"

**Examples by subject type:**

*Character in environment:*
- "in throne room with marble columns and red velvet"
- "on spaceship bridge with glowing control panels"
- "in mystical forest with ancient trees and glowing mushrooms"

*Object in environment:*
- "on marble pedestal in museum gallery"
- "floating in cosmic void with distant nebulae"
- "on workshop table surrounded by tools"

*Building in environment:*
- "on cliff edge overlooking ocean"
- "in dense jungle clearing"
- "surrounded by futuristic cityscape"

**Rules:**
- ✅ Use prepositions: "in", "on", "at", "within", "surrounded by"
- ✅ Can include environmental details directly in this component
- ✅ Describe setting features that matter to composition/atmosphere
- ❌ Skip if subject IS the environment (landscapes as subject)
- ❌ Don't repeat details from KEY DETAILS (avoid redundancy)

---

#### 5. COMPOSITION (Mandatory)

**What:** Camera work, framing, spatial arrangement - HOW the scene is captured/arranged

**Categories:**

**Camera Angle:**
- "eye-level", "low angle looking up", "high angle looking down"
- "bird's eye view", "worm's eye view", "isometric view"
- "three-quarter view", "profile view", "over-the-shoulder"

**Framing/Shot Type:**
- "extreme close-up", "close-up", "medium shot", "american shot"
- "full shot", "wide shot", "establishing shot"

**Spatial Layout:**
- "centered composition", "rule of thirds", "golden ratio placement"
- "symmetrical", "asymmetrical", "diagonal composition"
- "leading lines", "triangular composition", "frame within frame"

**Depth/Focus:**
- "shallow depth of field", "deep depth of field"
- "foreground/midground/background layers"

**Negative Space:**
- "minimal negative space, subject fills frame"
- "generous negative space, subject isolated"
- "negative space on left for text overlay"
- "negative space at top, subject in lower third"
- "negative space around subject for breathing room"

**Examples:**
- "medium shot, eye-level, rule of thirds with subject on left"
- "wide shot, bird's eye view, centered symmetrical composition"
- "close-up, shallow depth of field, subject in focus with blurred background"
- "wide shot with generous negative space at top for title text"

---

#### 6. STYLE (Mandatory)

**What:** Visual aesthetic and artistic approach - HOW it should look artistically

**Categories:**

**Art Medium/Technique:**
- "photorealistic", "3D render", "digital art", "digital painting"
- "voxel art", "pixel art", "low poly"
- "oil painting", "watercolor painting", "acrylic painting"
- "pencil sketch", "ink drawing", "charcoal drawing"
- "anime", "manga", "comic book style"

**Artistic Movement/Era:**
- "impressionist", "surrealist", "abstract", "cubist"
- "art nouveau", "art deco", "baroque", "renaissance"
- "minimalist", "maximalist"
- "retro 1980s", "vintage", "futuristic", "cyberpunk", "steampunk"

**Specific References:**
- "Studio Ghibli style", "Disney animation style"
- "Blade Runner aesthetic", "Art Nouveau"
- "in the style of [artist name]"

**Technical Qualities:**
- "highly detailed", "minimalist", "abstract"
- "cel-shaded", "flat colors", "gradients"
- "textured", "smooth", "painterly"

**Examples:**
- "in voxel art style, blocky and geometric with soft gradients"
- "photorealistic 3D render with cinematic lighting"
- "watercolor painting style with soft edges and color bleeding"
- "1980s retro aesthetic with neon colors and grid patterns"

---

#### 7. LIGHTING (Mandatory)

**What:** Light sources, quality, direction, time - creates atmosphere

**Categories:**

**Light Source:**
- "natural sunlight", "studio lighting", "softbox"
- "candlelight", "firelight", "lamplight"
- "neon lights", "LED lights", "string lights"
- "moonlight", "starlight"
- "bioluminescence", "magical glow"

**Light Quality:**
- "soft diffused", "harsh direct", "gentle"
- "dramatic", "moody", "bright", "dim"
- "high contrast", "low contrast"
- "even lighting", "dramatic shadows"

**Light Direction:**
- "front lighting", "side lighting", "backlighting"
- "top-down lighting", "bottom lighting", "rim lighting"
- "three-point lighting"

**Time of Day/Atmosphere:**
- "golden hour", "blue hour", "midday sun"
- "dawn", "dusk", "noon", "midnight"
- "overcast", "clear sky"
- "foggy", "misty", "hazy"

**Examples:**
- "golden hour sunlight, warm and soft, side lighting from left creating gentle shadows"
- "studio lighting, three-point setup, soft diffused light, professional photography"
- "dramatic spotlight from above, surrounded by darkness, theatrical"
- "neon lights in pink and cyan, reflective wet surfaces, cyberpunk nighttime"

**Key Principle:** Describe the lighting conditions naturally. Include physical atmosphere (mist, fog) as it affects light behavior. Focus on observable light qualities rather than emotional descriptors.

---

#### 8. COLOR (Important - palette specification)

**What:** Color palette, color relationships, saturation level

**Categories:**

**Color Palette Approach:**
- "vibrant color palette", "muted color palette"
- "monochromatic", "complementary colors", "analogous colors"
- "warm tones", "cool tones", "earth tones"
- "pastel colors", "neon colors", "jewel tones"
- "black and white", "grayscale", "sepia tone"

**Specific Colors:**
- Primary: "red", "blue", "yellow"
- Secondary: "green", "orange", "purple"
- Neutral: "white", "black", "gray", "beige", "brown"
- Descriptive: "navy blue", "forest green", "sky blue", "crimson red"
- "gold", "silver", "bronze", "copper"

**Color Relationships:**
- "dominant [color] with [color] accents"
- "[color] and [color] color scheme"
- "primarily [color] transitioning to [color]"

**Saturation/Contrast:**
- "high saturation", "low saturation", "desaturated"
- "high contrast", "low contrast"
- "bold and vivid", "soft and muted"

**Examples:**
- "vibrant color palette, cyan and magenta with yellow highlights"
- "muted earth tones, browns and greens with rust accents"
- "monochromatic blue, from deep navy to pale sky blue"
- "high contrast black and white with pops of red"

---

#### 9. TECHNICAL (Optional - quality parameters)

**What:** Quality specifications, rendering details, aspect ratio - model-dependent

**⚠️ MODEL COMPATIBILITY:**

**Categories for Midjourney / Stable Diffusion:**

**Quality Keywords:**
- "8k", "4k", "ultra HD", "high resolution"
- "highly detailed", "intricate details", "sharp focus"
- "professional photography", "award winning"

**Rendering/Engine:**
- "octane render", "unreal engine", "unity engine"
- "ray tracing", "global illumination", "volumetric lighting"
- "photorealistic", "hyperrealistic"

**DALL·E 3 / Gemini:**
- Use natural descriptive language instead of technical keywords
- ❌ "octane render, 8k, ray tracing"
- ✅ "photorealistic quality with accurate lighting and fine details"

**Aspect Ratio (all models):**
- "1:1" (square), "16:9" (landscape), "9:16" (portrait)
- "4:3" (standard), "3:4" (portrait), "21:9" (cinematic)

**Examples:**

*Midjourney/Stable Diffusion:*
- "8k, octane render, volumetric lighting, photorealistic, 16:9"
- "highly detailed, unreal engine 5, ray tracing, cinematic lighting"

*DALL·E 3/Gemini:*
- "photorealistic quality with natural lighting, widescreen format"
- "highly detailed illustration with fine textures and sharp focus"


---

## COMPOSITION TECHNIQUES

Master these techniques for visual impact and control.

> **📖 Reference:** This section expands on the COMPOSITION component from UNIVERSAL PROMPT STRUCTURE above. Use these techniques when defining camera angles, framing, and spatial layouts in your prompts.

### Spatial Layout Techniques

#### Rule of Thirds
**When:** Balanced, dynamic composition without centered symmetry
**Pattern:** "rule of thirds composition, [subject] positioned at [intersection]"
**Example:** "rule of thirds composition, lighthouse at right intersection, ocean filling lower two-thirds"

#### Centered Composition
**When:** Formal, symmetrical, stable subjects; logos, icons, portraits
**Pattern:** "centered composition, [subject] in middle of frame, symmetrical"
**Example:** "centered composition, crystal throne in middle of frame, symmetrical architecture"

#### Leading Lines
**When:** Guide viewer's eye to subject, create depth and perspective
**Pattern:** "leading lines from [element] converging on [subject]"
**Example:** "leading lines from railroad tracks converging on distant mountains"

#### Framing Within Frame
**When:** Add depth, focus attention, create layered composition
**Pattern:** "[framing element] framing [subject]"
**Example:** "ornate archway framing distant garden view, natural vignette"

#### Negative Space
**When:** Reserve space for text/logo, create breathing room, minimalist aesthetic
**Pattern:** "[area] with negative space for [purpose]"
**Example:** "top third with clean negative space for text overlay, subject in lower two-thirds"

#### Golden Ratio
**When:** Sophisticated, natural composition; fine art, cinematic work
**Pattern:** "golden ratio composition, [subject] at focal point"
**Example:** "golden ratio composition, spiral leading from foreground trees to distant castle"

#### Diagonal Composition
**When:** Dynamic energy, movement, action scenes
**Pattern:** "diagonal composition, [elements] along diagonal axis"
**Example:** "diagonal composition, mountain ridge cutting bottom-left to top-right"

#### Triangular Composition
**When:** Stable groups, classical balance, architectural shots
**Pattern:** "triangular composition, [elements] forming [shape] triangle"
**Example:** "triangular composition, three characters forming pyramid with leader at apex"

#### Depth Layers (Foreground/Midground/Background)
**When:** Create dimensional depth in landscapes and environments
**Pattern:** "[foreground] in foreground, [subject] in midground, [background] in background"
**Example:** "fence posts in foreground, red barn in midground, misty mountains in background"

#### Visual Weight and Balance
**When:** Distribute elements for asymmetric balance or formal symmetry
**Pattern:** "[heavier element] on [side] balanced by [lighter element] on [opposite]"
**Example:** "small bright red barn on left balanced by larger muted forest on right"
**Note:** Weight factors: size, color saturation, contrast, detail density, position

#### S-Curve Composition
**When:** Natural flow, winding paths, graceful movement
**Pattern:** "S-curve composition, [elements] flowing from [start] through [middle] to [end]"
**Example:** "S-curve composition, winding river from bottom-left through center to top-right"

#### Radial Composition
**When:** Dramatic central focus, architectural domes, sunbursts, explosions
**Pattern:** "radial composition, [elements] radiating from/converging to [center]"
**Example:** "radial composition, stone pillars radiating from circular plaza center"

#### Overlapping Elements
**When:** Create depth through layering, mountain ranges, forests
**Pattern:** "[near] overlapping [middle] overlapping [far], layered depth"
**Example:** "overlapping mountain ranges from dark foreground to lighter distant peaks"

#### Silhouette Composition
**When:** Dramatic mood, emphasis on shape/form, sunrise/sunset scenes
**Pattern:** "silhouette composition, [subject] as dark shape against [bright background]"
**Example:** "silhouette composition, warrior with raised sword against orange sunset sky"

### Camera Perspective Guide

#### Eye-Level
**When:** Neutral, realistic, relatable perspective
**Pattern:** "eye-level perspective"
**Example:** "eye-level perspective, portrait looking at camera"

#### Low Angle (Looking Up)
**When:** Heroic, powerful, imposing mood
**Pattern:** "low angle looking up at [subject]" | "worm's eye view from ground level" (extreme)
**Example:** "low angle looking up at towering skyscraper, dramatic perspective"

#### High Angle (Looking Down)
**When:** Vulnerable subject, overview, map-like view
**Pattern:** "high angle looking down at [subject]" | "bird's eye view" (extreme)
**Example:** "high angle looking down at busy marketplace, aerial perspective"

#### Three-Quarter View (3/4)
**When:** Character art, product shots showing depth and dimension
**Pattern:** "three-quarter view" or "3/4 angle"
**Example:** "three-quarter view of character showing both face and profile"

#### Profile View
**When:** Character design, silhouettes, clean side view
**Pattern:** "profile view" or "side view"
**Example:** "profile view of warrior, clean silhouette against sunset"

#### Over-the-Shoulder (OTS)
**When:** Conversations, immersive portraits, POV-adjacent
**Pattern:** "over-the-shoulder view from behind [subject]"
**Example:** "over-the-shoulder from behind pianist, hands on keys, audience visible"

#### Point of View (POV)
**When:** Immersive first-person perspective, viewer as subject
**Pattern:** "point of view" | "first-person perspective" | "POV shot"
**Example:** "point of view looking down at hands holding ancient map, compass beside it"

#### Isometric View
**When:** Game art, technical diagrams, architectural clarity
**Pattern:** "isometric view" (avoid specifying angles)
**Example:** "isometric view of fantasy village, parallel lines, no vanishing point"
**Note:** Term "isometric" sufficient for AI—don't specify degrees

#### Dutch Angle (Tilted)
**When:** Tension, unease, dynamic action, instability
**Pattern:** "dutch angle, diagonal horizon" | "heavily tilted dutch angle" (extreme)
**Example:** "moderate dutch angle, diagonal horizon creating tension"
**Note:** Use descriptive terms (slight/moderate/heavy), not numerical degrees

#### Lens Characteristics

**Principle:** Lens choice fundamentally changes spatial relationships, depth, and perspective—not just zoom level

#### Wide-Angle Lens (24mm-35mm)
**When:** Epic landscapes, architectural interiors, environmental context, dramatic scale
**Effect:** Exaggerated depth, expansive field of view, foreground appears much larger than background
**Pattern:** "wide-angle lens perspective, [subject with context], expansive depth"
**Example:** "wide-angle lens perspective, hiker on cliff edge with vast mountain vista, expansive depth showing scale"
**Note:** Distorts faces when too close—avoid for tight portraits

#### Normal Lens (40mm-60mm)
**When:** Natural-looking portraits, street photography, neutral perspective
**Effect:** Matches human vision, minimal distortion, realistic spatial relationships
**Pattern:** "natural perspective, [subject], balanced spatial relationships"
**Example:** "natural perspective, market vendor at stall with balanced composition"
**Note:** Versatile default—"invisible" lens that doesn't impose stylistic look

#### Telephoto Lens (85mm-200mm+)
**When:** Portrait photography, wildlife, subject isolation, stacked landscapes
**Effect:** Compressed depth, background appears closer to subject, shallow depth of field
**Pattern:** "telephoto lens compression, [subject], compressed depth, blurred background"
**Example:** "telephoto lens compression, portrait with city lights blurred behind, shallow depth isolating subject"
**Note:** Flattering for portraits (85-135mm range); creates natural bokeh

#### Macro Lens (Close-Focus)
**When:** Product details, nature close-ups, abstract textures, microscopic detail
**Effect:** Extreme magnification, razor-thin focus plane, background completely defocused
**Pattern:** "macro lens, extreme close-up of [detail], shallow focus, [background] blurred"
**Example:** "macro lens, extreme close-up of dewdrop on petal, background garden completely blurred"

#### Lens + Angle Combinations
**Powerful pairings:**
- Wide-angle + Low angle = Heroic, imposing scale
- Telephoto + Eye-level = Intimate portrait isolation
- Wide-angle + High angle = Vulnerable subject in vast environment
- Macro + Any angle = Detail emphasis (magnification dominates)

### Framing Options

#### Extreme Close-Up (ECU)
**Coverage:** Specific detail (eyes, hands, object detail)
**Pattern:** "extreme close-up of [detail]"

#### Close-Up (CU)
**Coverage:** Face or single object filling frame
**Pattern:** "close-up of [subject], shallow depth of field"

#### Medium Shot (MS)
**Coverage:** Waist up (person) or object with context
**Pattern:** "medium shot of [subject], [context]"

#### American Shot / Cowboy Shot
**Coverage:** Mid-thigh up
**When:** Action scenes, standing characters with environment
**Pattern:** "american shot" or "cowboy shot, mid-thigh up"

#### Full Shot (FS)
**Coverage:** Head to toe, subject fills frame
**Pattern:** "full shot, head to toe, [subject] filling frame"

#### Wide Shot (WS)
**Coverage:** Full subject with significant environment
**Pattern:** "wide shot showing [subject and environment]"

#### Establishing Shot (ES)
**Coverage:** Full scene setting location and context
**Pattern:** "establishing shot of [location], panoramic view"

#### Two-Shot
**When:** Conversations, relationships, interactions
**Pattern:** "two-shot of [subject 1] and [subject 2], [interaction]"
**Example:** "two-shot of detective and suspect across table, tense"

#### Group Shot
**When:** Team photos, crowd scenes, ensemble casts
**Pattern:** "group shot of [number] [subjects], [arrangement]"
**Example:** "group shot of five adventurers, triangular formation with leader at front"

---

### Subject Placement & Framing Conventions

**Principle:** Professional framing rules create natural viewing experiences; breaking them intentionally creates tension

#### Headroom
**What:** Space between subject's head and top frame edge

**Proper Headroom (Standard):**
**When:** Natural, comfortable framing
**Pattern:** "proper headroom, [subject] with comfortable space above head"
**Example:** "portrait with proper headroom, subject naturally framed"

**Minimal Headroom (Tight):**
**When:** Intimacy, intensity, dramatic close-ups
**Pattern:** "tight framing with minimal headroom, [subject] filling frame"
**Example:** "dramatic close-up with minimal headroom, intense framing"

**Excessive Headroom:**
**When:** Vulnerability, isolation, subject appears small
**Pattern:** "excessive headroom, [subject] positioned low in frame with large space above"
**Example:** "excessive headroom, lone figure under vast empty sky, isolation mood"

#### Looking Room (Nose Room)
**What:** Space in front of subject's face in direction they're looking/facing

**Proper Looking Room:**
**When:** Natural, comfortable composition
**Pattern:** "looking room, [subject] facing [direction] with space ahead"
**Example:** "portrait with looking room, woman facing right positioned on left third"
**Note:** Subject facing left = position on right third; facing right = position on left third

**Minimal Looking Room:**
**When:** Tension, claustrophobia, trapped feeling
**Pattern:** "minimal looking room, [subject] facing frame edge, creating tension"
**Example:** "minimal looking room, man staring toward frame edge, claustrophobic"

**Space Behind Subject:**
**When:** Vulnerability, being-watched feeling, thriller/horror mood
**Pattern:** "space behind subject, [subject] facing camera with empty area behind"
**Example:** "large space behind subject, character looking back over shoulder, vulnerable mood"

#### Walking Room (Lead Room)
**What:** Space in front of moving subject in direction of movement

**Proper Walking Room:**
**When:** Show forward motion and momentum
**Pattern:** "walking room, [subject] moving [direction] with space ahead"
**Example:** "walking room, cyclist moving left to right with open road ahead"
**Note:** Moving left to right = position left, space right; moving right to left = position right, space left

**Minimal Walking Room:**
**When:** Subject arriving, blocked, or stopping
**Pattern:** "minimal walking room, [subject] approaching frame edge, arrival mood"
**Example:** "minimal walking room, character approaching doorway at frame edge"

**Expansive Walking Room:**
**When:** Epic journey, vast scale, adventure mood
**Pattern:** "expansive walking room, [subject] moving into vast landscape, journey composition"
**Example:** "expansive walking room, traveler walking into desert horizon, vast space ahead"

#### Combining Conventions
**Examples:**
- Portrait: "proper headroom and looking room, subject on left third facing right"
- Action: "walking room, athlete sprinting left to right with space ahead showing momentum"
- Tension: "minimal headroom and minimal looking room, character facing frame edge, claustrophobic"
- Epic: "excessive headroom and expansive walking room, small figure in vast landscape, epic scale"

### Depth of Field (DOF)

#### Shallow DOF (f/1.4 - f/2.8)
**When:** Isolate subject, portraits, product photography, single subject emphasis
**Pattern:** "shallow depth of field, [subject] in sharp focus, blurred background, bokeh"
**Example:** "portrait with shallow depth of field, face sharp, background softly blurred with bokeh"

#### Deep DOF (f/8 - f/16)
**When:** Landscapes, architecture, group shots, environmental detail throughout
**Pattern:** "deep depth of field, sharp focus throughout, foreground to background"
**Example:** "mountain landscape with deep depth of field, sharp from foreground rocks to distant peaks"

#### Selective Focus
**When:** Direct attention to specific element, food photography, narrative focus
**Pattern:** "focus on [primary element], [secondary elements] out of focus"
**Example:** "focus on chess piece in foreground, chessboard blurring into background"

**Note:** AI models respond well to both f-stop terminology (f/1.4, f/16) and descriptive terms (shallow/deep)

### Aspect Ratio Guidance

#### 1:1 (Square)
**Best for:** Instagram feed, profile images, logos, icons, minimalist designs
**Strategy:** Centered subjects, symmetrical compositions, balanced negative space
**Pattern:** "1:1 aspect ratio, centered composition"
**Example:** "product shot in 1:1 aspect ratio, centered with symmetrical negative space"

#### 16:9 (Landscape / Widescreen)
**Best for:** YouTube thumbnails, blog headers, landscapes, cinematic scenes
**Strategy:** Horizontal elements (horizons, roads), rule of thirds, wide establishing shots
**Pattern:** "16:9 aspect ratio, wide [composition]"
**Example:** "mountain landscape in 16:9, wide panoramic with horizon on lower third"

#### 9:16 (Portrait / Vertical)
**Best for:** Instagram Stories, TikTok, mobile wallpapers, fashion, tall architecture
**Strategy:** Vertical elements (buildings, waterfalls), top-to-bottom flow, vertical leading lines
**Pattern:** "9:16 aspect ratio, vertical [composition]"
**Example:** "skyscraper in 9:16, vertical composition emphasizing height, low angle"

#### 4:3 (Classic / Standard)
**Best for:** Traditional photography, presentations, classic portraits
**Strategy:** Flexible for portraits and landscapes, slight horizontal bias
**Pattern:** "4:3 aspect ratio, [composition]"
**Example:** "portrait in 4:3, classic composition with subject slightly off-center"

#### 3:4 (Portrait Classic)
**Best for:** Traditional portraits, book covers, poster designs
**Strategy:** Vertical emphasis less extreme than 9:16, room for environmental context
**Pattern:** "3:4 aspect ratio, vertical portrait composition"
**Example:** "character portrait in 3:4, medium shot with environmental context"

#### 21:9 (Cinematic / Ultra-Wide)
**Best for:** Cinematic artwork, epic landscapes, dramatic scenes
**Strategy:** Ultra-wide panoramas, multiple subjects across frame, epic scale
**Pattern:** "21:9 aspect ratio, ultra-wide cinematic [composition]"
**Example:** "epic battle scene in 21:9, ultra-wide cinematic with armies across horizon"

#### Quick Selection Guide
**By Subject:** Tall (buildings, portraits) → 9:16/3:4 | Wide (landscapes, groups) → 16:9/21:9 | Balanced (products, logos) → 1:1/4:3
**By Platform:** Instagram feed → 1:1 | Instagram Stories → 9:16 | YouTube → 16:9 | Mobile wallpaper → 9:16

---

## MODEL OPTIMIZATION TECHNIQUES

Adapt universal prompt structure for specific AI models. Three categories: **Natural Language** (DALL·E, Gemini), **Keyword-Rich** (Midjourney, SD), **Hybrid** (Grok/Flux).

**Universal Structure:** `[SUBJECT], [ACTION], [KEY DETAILS], [ENVIRONMENT], [COMPOSITION], in [STYLE], [LIGHTING], [COLOR], [TECHNICAL]`

---

### DALL·E 3 / ChatGPT Image

**Syntax:** Natural sentences (1-2 sentences) | **Best for:** Photorealism, text-in-image, beginners

**Parameters:**
- `Size:` 1024x1024 | 1792x1024 | 1024x1792
- `Quality:` standard | hd
- `Style:` natural (realistic) | vivid (artistic)

**Vocabulary:** Natural descriptive language, avoid technical keywords (no "8k, octane render")

**Example:**
```
A serene mountain landscape with a winding road through pine forests,
wide panoramic composition in impressionist style, golden hour lighting, warm color palette

Settings: Size 1792x1024 | Quality hd | Style natural
```

---

### Gemini Image (Imagen 3)

**Syntax:** Natural sentences (1-3 sentences) | **Best for:** Photorealism, flexible ratios

**Parameters:**
- `Aspect Ratio:` 1:1 | 3:4 | 4:3 | 9:16 | 16:9
- `Safety Filter:` BLOCK_ONLY_HIGH (recommended)

**Vocabulary:** Clear descriptive language, natural quality terms

**Example:**
```
A futuristic cityscape at night with neon-lit skyscrapers reflecting in rain-slicked streets,
wide establishing shot in cyberpunk aesthetic, dramatic lighting, vibrant blues and purples, high detail

Settings: Aspect Ratio 16:9 | Safety BLOCK_ONLY_HIGH
```

---

### Grok/Flux

**Syntax:** Hybrid (natural language + keywords) | **Best for:** Fantasy/sci-fi, advanced control

**Parameters:**
- `Aspect Ratio:` 1:1 | 16:9 | 9:16 | 4:3 | 3:4 | 21:9
- `Guidance:` 3.0-15.0 (7.5 default) - Lower=creative, Higher=literal
- `Steps:` 20-50 (28 default, 25-35 recommended)

**Vocabulary:** Natural base + technical keywords (8k, high detail, photorealistic)

**Example:**
```
A cyberpunk street market at night with holographic signs and neon lights, rain-slicked pavement,
wide shot, photorealistic 3D render, dramatic neon lighting, vibrant cyan and magenta,
high detail, 8k quality

Settings: Aspect Ratio 16:9 | Guidance 7.5 | Steps 28
```

---

### Midjourney

**Syntax:** Comma-separated keywords + inline params | **Best for:** Artistic/stylized imagery, composition

**Parameters:**
- `--ar [ratio]` - 16:9 | 1:1 | 21:9 (custom ratios supported)
- `--q [0.25|0.5|1|2]` - Quality (2=highest)
- `--s [0-1000]` - Stylization (100 default, higher=more artistic)
- `--style [raw|expressive]` - raw for photorealism
- `element::weight` - Keyword emphasis (dragon::2, castle::1)

**Vocabulary:** Keywords only, descriptive adjectives, technical quality terms

**Example:**
```
ancient temple, overgrown with vines, jungle setting, wide cinematic shot,
fantasy art style, golden hour lighting, atmospheric mist, highly detailed
--ar 16:9 --q 2 --style raw
```

**With Weights:**
```
majestic dragon::3, ancient castle::1, mountain landscape::1, sunset::2,
fantasy art, epic scale, dramatic lighting --ar 21:9 --q 2
```

---

### Stable Diffusion XL

**Syntax:** Comma-separated keywords | **Best for:** Full control, customization, privacy

**Parameters:**
- `Steps:` 25-35 (quality/speed balance)
- `CFG Scale:` 7-9 (lower=creative, higher=literal)
- `Sampler:` DPM++ 2M Karras (recommended)
- `Size:` 1024x1024 base (multiples of 64)

**Vocabulary:** Keywords, quality descriptors (highly detailed, sharp focus, professional)

**Example:**
```
epic fantasy landscape, floating islands, waterfalls, magical atmosphere,
wide panoramic view, digital art, dramatic lighting, vibrant colors,
highly detailed, 4k quality

Settings: Steps 30 | CFG 7.5 | Sampler DPM++ 2M Karras | Size 1024x1024
```

---

### Quick Reference

| Model | Format | Key Params | Use Case |
|-------|--------|------------|----------|
| **DALL·E 3** | Natural sentences | Size, Quality, Style | Photorealism, text rendering |
| **Gemini** | Natural sentences | Aspect ratio, Safety | Photorealism, flexible ratios |
| **Grok/Flux** | Hybrid | Aspect ratio, Guidance, Steps | Fantasy/sci-fi, advanced control |
| **Midjourney** | Keywords | --ar, --q, --s, ::weights | Artistic work, composition |
| **SD XL** | Keywords | Steps, CFG, Sampler | Full control, customization |

**Adaptation Strategy:**
- **Natural Language:** Expand structure into flowing sentences
- **Keywords:** Compress structure to comma-separated terms + params
- **Hybrid:** Keep structure, add technical keywords
