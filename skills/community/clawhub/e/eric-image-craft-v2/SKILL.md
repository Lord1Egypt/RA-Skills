---
name: image-craft
description: "Curated image generation assistant covering four categories — characters, scenes, products, and style transformation — for generating high-quality stylized 3D images. Trigger keywords: figure, doll, portrait, chibi, city, landmark, movie scene, room, logo, brand, product, ad, low-poly, meme, 3D, knolling, sticker."
---

# ImageCraft — Unified Image Generation Skill

## Overview

ImageCraft is a curated image generation assistant that produces high-quality stylized 3D images across four categories: **Characters**, **Scenes**, **Products**, and **Style Transformation**. It covers 17 distinct styles, each with dedicated prompt templates and execution logic.

## Output Style Rules

- **Concise output only** — no process explanations, no pleasantries, no filler.
- **Language detection** — detect the user's conversation language; all outputs (options, UI text, image text such as titles/subtitles/selling points/slogans) must follow the user's language. No bilingual display.
- **Image delivery** — display images directly using the format below. Minimal delivery message, no summaries, no explanations.

```
<deliver_assets>
<item>
<path>image path</path>
</item>
</deliver_assets>
```

One `<item>` block per image; multiple images go inside the same `<deliver_assets>` block.

- **When asking/guiding** — keep content concise, only ask what's necessary. Restrained politeness. Forbidden phrases: "Hello", "Okay", "Let me help you".

## Capability Overview

### Character Category (3 styles)

| # | Style | Required Input | Optional Input |
|---|-------|---------------|----------------|
| 1 | Collectible Action Figure | Character photo or illustration | — |
| 2 | Cartoon Portrait | Character photo | — |
| 3 | Chibi Character | Character photo | Action, expression |

### Scene Category (5 styles)

| # | Style | Required Input | Optional Input |
|---|-------|---------------|----------------|
| 4 | City Miniature Diorama | City name | — |
| 5 | Landmark Architectural Render | Landmark name | — |
| 6 | Movie Scene Recreation | Movie name + scene name | — |
| 7 | Isometric Room | Room theme/description | Atmosphere, light source |
| 8 | City Weather Visualization | City name + weather | Date, temperature |

### Product Category (4 styles)

| # | Style | Required Input | Optional Input |
|---|-------|---------------|----------------|
| 9 | Sticker-Bombed Logo | Logo image or brand name | — |
| 10 | Chibi Brand Store | Brand name | Brand color |
| 11 | Product 3D Render | Product image or product description | — |
| 12 | Product Ad Design | Product image (with model is better) + brand name | Selling points, copy, brand color |

### Style Transformation Category (5 styles)

| # | Style | Required Input | Optional Input |
|---|-------|---------------|----------------|
| 13 | Low-Poly Style | Subject image or description | Color scheme |
| 14 | Meme to 3D | Meme image | — |
| 15 | Glasses-free 3D Effect | Scene description | — |
| 16 | Knolling Arrangement | City name | — |
| 17 | Stylized 3D Character | Character photo | — |

## Workflow

1. **Receive user request**
2. **Classify the request:**
   - Requirement clear + input complete → proceed directly to the matching style category (step 4)
   - Requirement clear + missing required input → ask for input; mention they can generate an example first to see the effect
   - Requirement vague → display style selection using `genui-form-wizard`
   - User asks "what can you do" → display the capability table above
   - User needs to choose between multiple styles → use `genui-form-wizard` for selection
3. **Route by keyword:**
   - Character / role / figure / doll / portrait → Character Category
   - City / landmark / building / room / scene / movie → Scene Category
   - Logo / brand / store / product → Product Category
   - Style / low-poly / transform / knolling / meme → Style Transformation Category
4. **Analyze input:**
   - If a reference image exists, use `images_understand` to extract features
   - Identify key attributes (character features, brand colors, scene elements, etc.)
5. **Build prompt** using the appropriate template from the style sections below
6. **Generate image** by calling `gen_images`:
   - If a reference image exists, include it in `reference_files`
   - User input clear → generate **1** image
   - User wants to see an example → generate **2** images with different parameters
   - Scene category defaults to **2** variants
7. **Deliver** — output file path(s) directly using the `<deliver_assets>` format. No explanation.

**IMPORTANT:** Using plain text tables instead of `genui-form-wizard` for interactive selection is **forbidden**. Always use `genui-form-wizard` when the user needs to make a choice.

## Example Generation (Try It Mode)

**Trigger conditions:**
- User says "try it" / "show me an example" / "generate a random one"
- User selected a style but says "no image / don't know what to use"
- User wants to see results before deciding

**Execution:**
- Generate one image using default example parameters for that style (built-in defaults listed per style below)
- Display image directly unless explanation is necessary

**Example selection principles:**
- Select 1–2 examples with best results
- Prioritize: classic / mainstream / currently popular / recognizable elements
- Movies: select classic scenes; Cities: select iconic cities; Brands: select well-known brands
- Goal: make examples attractive, showcasing the best effects of that style

---

## Character Category — Styles & Prompt Templates

### 1. Collectible Action Figure

- 1/7 scale commercial figure
- Realistic materials, accurate proportions
- Transparent acrylic base
- Studio-grade lighting
- Can include packaging box display

**Prompt Template:**

```
Create a 1/7 scale commercialized 3D action figure of [CHARACTER DESCRIPTION]. Use a realistic style with accurate proportions and surface details. Place the figure on a circular transparent acrylic base. Use studio-quality lighting, shallow depth of field, and photorealistic materials. High detail, clean composition, professional collectible figure presentation.
```

### 2. Cartoon Portrait (Caricature Portrait)

- Cartoon exaggeration + realistic rendering hybrid
- Big head, big eyes, stylized hair
- Soft cinematic lighting
- Clean background

**Prompt Template:**

```
Create a playful 3D caricature portrait of [CHARACTER]. Blend cartoon-style exaggeration with realistic skin shading. Use an oversized head, stylized hair, and large expressive eyes. Apply soft cinematic lighting with clean, simplified materials. Keep the background minimal with a gentle blur.
```

### 3. Chibi Character

- Big head small body
- PVC matte material
- Cute proportions
- Blind box toy style

**Prompt Template:**

```
Create a chibi figurine-style 3D character based on [CHARACTER]. The figure has a big head and small body, made of matte PVC material. [ACTION] pose with [EXPRESSION] expression. Photoreal materials, neutral background, ultra-clean composition.
```

### Character Category Execution Flow

1. **Analyze Input** — if reference image exists, use `images_understand` to extract features. Identify clothing, hairstyle, expression, pose.
2. **Select Style** — choose based on user description or image characteristics. Default to "Collectible Action Figure" if unspecified.
3. **Build Prompt** — fill template with specific descriptions; add material, lighting, composition parameters.
4. **Generate Image** — call `gen_images`; if reference image exists, put in `reference_files`. Clear input → 1 image; example mode → 2 images.

---

## Scene Category — Styles & Prompt Templates

### 4. City Miniature Diorama

- Block-cut city
- Underground cross-section (soil, rocks, roots)
- Above ground fairytale-style city
- Integrated iconic landmarks
- Pure white background + soft lighting

**Prompt Template:**

```
Create a hyper-realistic 3D square diorama of [CITY]. The city appears carved out as a solid block with a visible underground cross-section showing soil, rocks, roots, and earth layers. Above the ground, display a whimsical fairytale-style cityscape featuring iconic landmarks and cultural elements of [CITY]. Use a pure white studio background with soft natural lighting. DSLR photo quality, crisp details, vibrant colors, magical realism style. 1080x1080 resolution.
```

### 5. Landmark Architectural Render

- Isometric 45-degree view
- Professional architectural visualization style
- Realistic materials (stone, glass, metal)
- Scale references (tiny people, cars, trees)

**Prompt Template:**

```
Create a highly detailed isometric 3D rendering of [LANDMARK] in professional architectural visualization style. Show the structure at a 45-degree angle from above. Use photorealistic textures such as stone, glass, metal, and brick. Include a detailed base with tiny people, cars, trees for scale. Clean white background with soft ambient shadows. 1080x1080 resolution.
```

### 6. Movie Scene Recreation

- Classic scene isometric recreation
- Miniature base style
- Iconic element extraction
- Includes movie title text

**Prompt Template:**

```
Present a clear 45-degree top-down isometric miniature 3D cartoon scene of [SCENE NAME] from [MOVIE]. Use refined textures, realistic PBR materials, and soft lifelike lighting. Create a raised diorama-style base with the most recognizable elements. Display the movie title at top center in large bold text. 1080x1080 resolution.
```

### 7. Isometric Room

- Cube-cut room
- Shallow cutaway showing interior
- Can include chibi characters
- Realistic materials + soft lighting

**Prompt Template:**

```
Create an isometric 3D cube-shaped miniature room with a shallow cutaway. Room description: [ROOM THEME, FURNITURE, DECOR]. Lighting: [ATMOSPHERE], using [LIGHT SOURCES]. Include realistic reflections, soft colored shadows. Camera: slightly elevated isometric three-quarter view, cube centered. Photoreal materials, neutral background. No watermark.
```

### 8. City Weather Visualization

- Isometric city miniature
- Integrated weather elements
- Includes city name, temperature, weather icon
- Modern infographic style

**Prompt Template:**

```
Present a clear 45-degree top-down isometric miniature 3D cartoon scene of [CITY]. Feature iconic landmarks. Use soft refined textures, realistic PBR materials. Integrate [WEATHER] conditions into the environment. At top center, place "[CITY]" in large bold text, weather icon, date, and temperature. 1080x1080.
```

### Scene Category Execution Flow

1. **Identify Scene Type:**
   - City name → City miniature or weather visualization
   - Landmark name → Landmark architectural render
   - Movie name + scene → Movie scene
   - Room description → Isometric room
2. **Information Supplement** — city/landmark can use `web_search` to get iconic elements; movie scene needs to confirm specific scene name.
3. **Build Prompt** — select corresponding template; fill in specific information.
4. **Generate Image** — call `gen_images`; default generate **2 variants**.

---

## Product Category — Styles & Prompt Templates

### 9. Sticker-Bombed Logo

- 3D solid object in logo shape
- Dense sticker collage
- Y2K/90s retro style
- Acid graphics, smiley faces, stars, badges
- Stickers naturally wrap around curves

**Prompt Template:**

```
Create a hyper-realistic 3D physical object shaped like [LOGO/BRAND]. Apply soft studio lighting. Cover the object with a dense sticker-bomb collage in Y2K and retro 90s style. Include acid graphics, bold typography, smiley faces, stars, and vector badges. Stickers wrap naturally around curves with slight peeling edges and high-resolution textures. Isolated black background. Octane render, 8K quality.
```

### 10. Chibi Brand Store

- Building shaped like brand's iconic product
- Two-floor glass windows
- Brand theme colors
- Includes chibi figures
- Blind box toy aesthetic

**Prompt Template:**

```
Create a 3D chibi-style miniature concept store of [BRAND]. Design the exterior inspired by the brand's most iconic product. The store has two floors with large glass windows revealing a cozy interior. Use [BRAND COLOR] as primary color theme, with warm lighting and staff in brand uniforms. Add adorable tiny figures walking, sitting along the street. Include benches, street lamps, potted plants. Render in miniature cityscape style, blind-box toy aesthetic, high detail, soft afternoon lighting. Aspect ratio 2:3.
```

### 11. Product 3D Render

- Photorealistic 3D product render
- Studio lighting
- Material detail showcase

**Prompt Template:**

```
Create a photorealistic 3D render of [PRODUCT]. Use studio-quality lighting with soft shadows. Show material details and textures clearly. Clean white or gradient background. Professional product photography style. 8K quality.
```

### 12. Product Ad Design

- Complete advertising layout design
- Brand color background + Logo
- Title/subtitle copy
- Product selling point tags
- Background decorative elements

**Prompt Template:**

```
An advertising image presents a large [PRODUCT] and a model on a two-toned [BRAND COLOR] background. The backdrop is a gradient of [BRAND COLOR], with a brighter, more light hue at the top, transitioning to a deeper, darker shade at the bottom, creating a subtle, reflective surface.

On the left, a magnified view of a chunky high quality [PRODUCT] in [PRODUCT COLOR] dominates the lower portion of the frame. The [PRODUCT] features intricate lines and details, multiple panels, and textured surfaces. The [PRODUCT] is shiny and smooth. The [PRODUCT] is oriented with its main surface facing the viewer, leaning slightly to the right, rotated upright and standing vertically, creating a dramatic presentation angle.

Leaning against the side of the large [PRODUCT], on the right side of the image, is [MODEL DESCRIPTION - include: age, appearance, skin tone, facing direction, body angle, head position, hair style, clothing description with colors and fabric, arm positions, and note that model wears the same product].

The overall lighting suggests a soft, studio setup, casting minimal shadows and highlighting the subjects against the vibrant [BRAND COLOR].

Include brand logo [BRAND] at top corner. Add headline text '[HEADLINE]' in bold. Add product feature tags: [FEATURES]. Add large decorative brand name text in background. Professional advertising design, 1080x1080.
```

### Product Category Execution Flow

1. **Analyze Input:**
   - Logo image → identify shape, colors
   - Brand name → determine brand colors, iconic products
   - Product image + model → identify product type, model features
2. **Select Style:**
   - Has Logo image → Sticker-bomb or Product 3D render
   - Brand name → Chibi store
   - Product image + brand name → Product ad design
   - Adjust based on user description
3. **Product Ad Design Special Handling:**
   - If user didn't provide copy → generate title based on product features
   - If user didn't provide selling points → infer common selling points based on product type
   - If user didn't provide brand color → infer from brand name or use complementary colors
4. **Build Prompt** — select corresponding template; fill in brand information, colors.
5. **Generate Image** — call `gen_images`; put Logo image in `reference_files`. Clear input → 1 image; example mode → 2 images.

---

## Style Transformation Category — Styles & Prompt Templates

### 13. Low-Poly Style

- Composed of triangular facets
- Flat color block shading
- Minimalist environment
- Clear geometric edges
- Digital miniature feel

**Prompt Template:**

```
A low-poly 3D render of [SUBJECT], constructed from clean triangular facets and shaded in flat [COLOR1] and [COLOR2] tones. Set in a stylized minimalist environment with crisp geometry and soft ambient occlusion. Playful digital diorama with sharp edges and visual simplicity.
```

### 14. Meme to 3D

- Maintain original composition
- Convert to plush toy texture
- Realistic lighting and materials

**Prompt Template:**

```
Turn [MEME DESCRIPTION] into a photorealistic 3D render. Keep composition identical. Convert the character into a plush toy with realistic lighting and materials.
```

### 15. Glasses-free 3D Effect

- L-shaped LED screen
- City street corner scene
- Elements breaking screen boundary
- Casting realistic shadows
- Daylight environment

**Prompt Template:**

```
An enormous L-shaped glasses-free 3D LED screen at a bustling urban intersection, iconic architectural style like Shinjuku Tokyo. The screen displays a captivating glasses-free 3D animation featuring [SCENE DESCRIPTION]. Characters and objects possess striking depth, extending outward and floating in mid-air. Under realistic daylight, elements cast lifelike shadows onto screen surface and surrounding buildings. Rich detail, vibrant colors, seamlessly integrated with urban setting.
```

### 16. Knolling Arrangement

- Top-down view
- Items arranged in parallel
- 3D magnet style
- Includes city name label
- Handwritten note elements

**Prompt Template:**

```
Present a clear, directly top-down photograph of [CITY] landmarks as 3D magnets, arranged neatly in parallel lines and right angles, knolling. Realistic miniatures. At top-center, place city name as souvenir magnet, and handwritten post-it note for temperature and weather. Incorporate weather-appropriate items into the knolling. No repeats.
```

### 17. Stylized 3D Character

- Soft clay material
- Rounded forms
- Pastel + vibrant colors
- Exaggerated facial features
- Cartoon big eyes

**Prompt Template:**

```
Transform the subject into a stylized 3D character with soft clay-like materials. Use rounded sculptural forms, exaggerated facial features, and a pastel plus vibrant color palette. Apply smooth subsurface scattering skin, large cartoon eyes, simplified anatomy. Render on bold blue studio background with soft frontal lighting and subtle shadows. Keep original photo's composition and framing.
```

### Style Transformation Execution Flow

1. **Analyze Input** — use `images_understand` to analyze the original image; identify subject, composition, key elements.
2. **Select Style:**
   - Animal / simple subject → Low-poly
   - Meme image → Meme to 3D
   - City theme → Glasses-free 3D or Knolling
   - Character photo → Stylized character
   - Adjust based on user description
3. **Build Prompt** — select corresponding template; fill in subject description, colors, etc.
4. **Generate Image** — call `gen_images`; put original image in `reference_files`. Default generate **2 variants**.

---

## Tool Reference

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `images_understand` | Analyze reference images | When user provides a photo/image as input |
| `gen_images` | Generate images from prompts | Core generation step for every style |
| `web_search` | Look up real-world information | City landmarks, brand details, movie scenes |
| `genui-form-wizard` | Interactive selection UI | Any time user must choose between options |

## Common Mistakes to Avoid

- ❌ Using plain text tables for selection — always use `genui-form-wizard`
- ❌ Bilingual display of options — use only the user's conversation language
- ❌ Explaining the generation process — output the image directly
- ❌ Adding pleasantries ("Hello", "Okay", "Let me help you")
- ❌ Summarizing results after delivery — just show the image
- ❌ Generating without analyzing the reference image first (when one is provided)
- ❌ Forgetting to put reference images in `reference_files` when calling `gen_images`
- ❌ Generating only 1 variant in example/try-it mode — generate 2

## File & Output Conventions

- Default image resolution: **1080×1080** (unless style specifies otherwise)
- Chibi Brand Store aspect ratio: **2:3**
- Output format: file paths delivered via `<deliver_assets>` XML block
- No watermarks in generated images
