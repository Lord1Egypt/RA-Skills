# Image Generation Scenarios & Model Configuration

**Purpose**: Scenario-to-model mapping for ambiguous cases.

**Usage**: Read this only when user intent doesn't clearly match a specific model choice in SKILL.md.

**Fallback Source of Truth**: Exact automatic fallback pairs are defined only in `fallback_models.json` and consumed by `scripts/run_task.py`. This file selects primary models and params; do not treat it as the authoritative fallback mapping.

---

## Part 1: Text-to-Image Generation

### T2I-0: General Default
**Use Case**: Generic or unclear text-to-image requests that do not match other scenarios.

**Model**: `gpt-image-2` → `text2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### T2I-1: General Commercial & Social Media
**Use Case**: Product photos, social media posts, marketing materials, e-commerce images, general commercial photography.

**Model**: `gemini-3.1-flash-image-preview` → `text2image`  
**Params**: `aspect_ratio="1:1"` (adjust per platform), `resolution="2k"`

---

### T2I-2: Premium Commercial & Cinematic
**Use Case**: Premium brand visuals, cinematic aspect ratios (21:9), high-end commercial content requiring finer details and higher dynamic range.

**Model**: `gemini-3.1-flash-image-preview` → `text2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### T2I-3: Artistic & Creative Advertising
**Use Case**: High-concept art, creative advertising campaigns, cinematic storyboards, mood boards, atmospheric photography with emphasis on lighting and texture.

**Model**: `gpt-image-2` → `text2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### T2I-4: Photorealistic Humans & Portraits
**Use Case**: Character design, virtual photography, portrait generation, realistic human figures with consistent facial features and anatomically correct proportions.

**Model**: `gpt-image-2` → `text2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### T2I-5: PPT/UI/Interior Visuals
**Use Case**: Presentation graphics, UI mockups, interior design renders, architectural visualization, game concept art, technical diagrams.

**Model**: `gpt-image-2` → `text2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### T2I-6: Fast Iteration & Prototyping
**Use Case**: Rapid concept exploration, thumbnail generation, real-time preview, high-volume generation for iteration-heavy workflows.

**Model**: `gpt-image-2` → `text2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="1k"`

---

### T2I-7: Budget-Conscious Generation
**Use Case**: Cost-effective drafts, internal documentation, low-budget projects, internal-use-only visuals.

**Model**: `gpt-image-2` → `text2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="1k"`

---

### T2I-8: Complex Prompts & 4K Requirements
**Use Case**: Very detailed/nuanced prompts requiring complex logic interpretation, strict layout accuracy, or 4K resolution output.

**Model**: `gemini-3.1-flash-image-preview` → `text2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="4k"`

---

## Part 2: Image-to-Image Editing

### I2I-0: General Editing
**Use Case**: Generic or unclear image editing requests that do not match other scenarios.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### I2I-1: Style Transfer & Artistic Transformation
**Use Case**: Converting photos to paintings, sketches, cartoons, watercolor, oil painting, anime style, or other artistic transformations.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### I2I-2: Multi-Reference Fusion
**Use Case**: Generating images that combine styles, compositions, or elements from 2-5 reference images.

**Model**: `gemini-3.1-flash-image-preview` → `image2image`  
**Params**: `image_urls` (2-5 URLs), `aspect_ratio="1:1"`, `resolution="2k"`  
**Note**: Check model's `max_reference_images` before proceeding

---

### I2I-3: Object & Element Removal
**Use Case**: Removing people, objects, text, watermarks, or other unwanted elements from images with seamless inpainting.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`

---

### I2I-4: Outpainting & Canvas Extension
**Use Case**: Extending image borders, expanding canvas, generating surrounding context to make images wider/taller while maintaining spatial coherence.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### I2I-5: Background Replacement
**Use Case**: Changing background scene/setting while preserving the main subject intact.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`  
**Note**: Consider using `background_remove` first for clean subject isolation

---

### I2I-6: Photo Enhancement & Restoration
**Use Case**: Sharpening blurry photos, fixing old/damaged images, color correction, improving overall image quality without changing size.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`  
**Note**: For resolution upscaling specifically, use `image_upscale` instead

---

### I2I-7: Portrait Modification
**Use Case**: Applying makeup, changing hair color/style, modifying facial expressions or poses, age progression/regression, virtual clothing try-on.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

### I2I-8: PPT/UI/Product Editing
**Use Case**: Editing presentation graphics, product photos, UI mockups, interior design visuals, or other specialized commercial content.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`

---

### I2I-9: Inpainting (Marked Region)
**Use Case**: Editing content within a specific user-marked, circled, or masked area of an image.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`  
**Note**: Requires user-provided mask or clear markup indication

---

### I2I-10: High-End Artistic Transformation
**Use Case**: Premium creative work requiring top-tier artistic quality, professional art conversion, gallery-quality transformations.

**Model**: `gpt-image-2` → `image2image`  
**Params**: `aspect_ratio="1:1"`, `resolution="2k"`

---

## Part 3: Utility Operations

### UTIL-1: Image Upscaling
**Use Case**: Increasing image resolution and pixel density without blur or quality loss.

**Tool**: `image_upscale`  
**Params**: `upscale_ratio=2` or `4` (only supported values)  
**Fallback**: If tool fails → Use `image2image` with higher `resolution`, or `gemini-3-pro-image-preview` with `resolution="4k"` for regeneration

---

### UTIL-2: Background Removal
**Use Case**: Isolating subject with transparent or solid color background, removing all background elements.

**Tool**: `background_remove`  
**Fallback**: If tool fails → Use I2I-5 (Background Replacement) with solid color background in prompt

---

## Special Considerations

**Multi-Reference**: Always verify model's `max_reference_images` capability in `image_models.md` spec before using 2+ images in `image_urls`.

**Aspect Ratio**: Default to `"1:1"` for all image operations.
