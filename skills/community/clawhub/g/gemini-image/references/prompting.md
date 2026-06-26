# Gemini Image Prompting Guide

**Core principle:** Describe the scene, don't just list keywords. Narrative paragraphs beat disconnected words.

---

## 1. Photorealistic Scenes

Use photography terms: camera angles, lens types, lighting, fine details.

**Template:**
```
A photorealistic [shot type] of [subject], [action or expression], set in [environment]. 
The scene is illuminated by [lighting description], creating a [mood] atmosphere. 
Captured with a [camera/lens details], emphasizing [key textures and details]. 
The image should be in a [aspect ratio] format.
```

**Example:**
```
A photorealistic close-up portrait of an elderly Japanese ceramicist, focused intently 
on shaping clay on a traditional wheel, set in a rustic, sunlit workshop. The scene is 
illuminated by soft, diffused natural light from a large window, creating a warm, 
contemplative atmosphere. Captured with a 85mm f/1.4 lens, emphasizing the deep lines 
on his hands and the smooth, wet texture of the clay.
```

---

## 2. Stylized Illustrations & Stickers

Be explicit about style and request transparent background for assets.

**Template:**
```
A [style] sticker of a [subject], featuring [key characteristics] and a [color palette]. 
The design should have [line style] and [shading style]. The background must be transparent.
```

**Example:**
```
A kawaii-style sticker of a happy red panda holding a bamboo shoot, featuring oversized 
sparkling eyes and rosy cheeks with a pastel pink and green color palette. The design 
should have thick black outlines and soft cel-shading. The background must be transparent.
```

---

## 3. Accurate Text in Images

Gemini excels at rendering text. Be clear about text content, font style, and design. Use **Gemini 3 Pro Image** for best results.

**Template:**
```
Create a [image type] for [brand/concept] with the text "[text to render]" in a [font style]. 
The design should be [style description], with a [color scheme].
```

**Example:**
```
Create a modern, minimalist logo for a coffee shop called 'The Daily Grind' with the text 
"The Daily Grind" in a clean, sans-serif font with a subtle coffee bean replacing the 'o'. 
The design should be flat and geometric, with a warm brown and cream color scheme.
```

---

## 4. Product Mockups & Commercial Photography

Clean, professional product shots for ecommerce, advertising, or branding.

**Template:**
```
A high-resolution, studio-lit product photograph of a [product description] on a 
[background surface/description]. The lighting is a [lighting setup] to [lighting purpose]. 
The camera angle is a [angle type] to showcase [specific feature]. Ultra-realistic, 
with sharp focus on [key detail]. [Aspect ratio].
```

**Example:**
```
A high-resolution, studio-lit product photograph of a minimalist ceramic coffee mug 
with a matte terracotta finish on a raw concrete slab. The lighting is a three-point 
softbox setup to create soft shadows and highlight the mug's curves. The camera angle 
is a 45-degree hero shot to showcase the handle and interior. Ultra-realistic, with 
sharp focus on the subtle glaze texture. 4:5 aspect ratio.
```

---

## 5. Minimalist & Negative Space Design

Great for backgrounds, presentations, or marketing materials with text overlay.

**Template:**
```
A minimalist composition featuring a single [subject] positioned in the [position] of the frame. 
The background is a vast, empty [color] canvas, creating significant negative space. 
Soft, subtle lighting. [Aspect ratio].
```

**Example:**
```
A minimalist composition featuring a single, delicate red maple leaf positioned in the 
bottom-right of the frame. The background is a vast, empty off-white canvas, creating 
significant negative space for text. Soft, subtle lighting. 16:9 aspect ratio.
```

---

## 6. Sequential Art (Comics / Storyboards)

Character consistency + scene description for visual storytelling. Best with **Gemini 3 Pro Image**.

**Template:**
```
Make a 3 panel comic in a [style]. Put the character in a [type of scene].
```

**Example:**
```
Make a 3 panel comic in a noir detective style. Panel 1: A detective in a trench coat 
enters a dimly lit bar. Panel 2: Close-up of his weathered face as he orders whiskey. 
Panel 3: He notices a mysterious woman at the end of the bar watching him.
```

---

## 7. Grounding with Google Search

Generate images based on recent/real-time information (news, weather, sports).

**Example:**
```
Make a simple but stylish graphic of last night's Arsenal game in the Champion's League
```

---

## 8. iOS Wireframes & UI Mockups

Convert sketches to high-fidelity iOS UI. Use reference-first workflow with design system specs.

**Template:**
```
Convert this wireframe to high-fidelity iOS 18 UI. 
Device: [iPhone model] frame, [orientation].
Design system: [style specs].
Interpret sketch elements: scribbles→images, rectangles→buttons, lines→text.
```

**Example:**
```
Convert this wireframe sketch to a high-fidelity iOS 18 UI mockup.
Device: iPhone 16 Pro frame, portrait orientation.
Design system: iOS 18 native aesthetic, rounded corners (16px radius), soft drop shadows, 
SF Pro font, 8pt spacing grid, vibrant primary color (#007AFF).
Interpret the sketch: scribbles become placeholder images, rectangles become buttons, 
horizontal lines become text labels. Add a standard iOS status bar and home indicator.
```

**JSON-Structured Prompt (for complex layouts):**
```json
{
  "image_type": "UI mockup",
  "device": {"frame": "iPhone 16 Pro", "orientation": "portrait"},
  "design_system": {
    "style": "iOS 18 native",
    "corners": "rounded, 16px radius",
    "shadows": "soft drop shadows",
    "spacing": "8pt grid",
    "font": "SF Pro"
  },
  "layout": {
    "header": "Navigation bar with back button and title",
    "hero": "Large image card with rounded corners",
    "content": "List of items with icons and chevrons",
    "bottom_nav": "5 tab icons - Home, Search, Add, Activity, Profile"
  }
}
```

**Multi-Screen User Journeys:**
Request exactly N screens showing left-to-right flow:
```
Create a 4-screen iOS onboarding flow, arranged left to right:
1. Welcome screen with app logo and "Get Started" button
2. Feature highlight with illustration and "Next" button  
3. Permission request for notifications
4. Success screen with "Enter App" button
Consistent iOS 18 styling across all screens, iPhone 16 frames.
```

**Key Tips:**
- Specify device frame explicitly (iPhone 16, iPhone 16 Pro, etc.)
- Include design system details (corner radius, shadows, fonts)
- Tell model how to interpret sketch elements
- For multi-screen, generate separately or request specific grid layout
- Use `9:16` aspect ratio for portrait phone screens

---

# Editing Images

Provide images alongside text prompts for editing, composition, and style transfer.

---

## 1. Adding and Removing Elements

Provide an image and describe your change. Model matches original style, lighting, perspective.

**Template:**
```
Using the provided image of [subject], please [add/remove/modify] [element] to/from the scene. 
Ensure the change is [description of how the change should integrate].
```

**Example:**
```
Using the provided image of my cat, please add a small, knitted wizard hat perched 
on its head. Ensure the hat casts a subtle shadow and matches the soft lighting of 
the original photo.
```

---

## 2. Inpainting (Semantic Masking)

Conversationally define a "mask" to edit a specific part while leaving the rest untouched.

**Template:**
```
Using the provided image, change only the [specific element] to [new element/description]. 
Keep everything else in the image exactly the same, preserving the original style, 
lighting, and composition.
```

**Example:**
```
Using the provided image of a living room, change only the blue sofa to be a vintage, 
brown leather chesterfield sofa. Keep everything else exactly the same.
```

---

## 3. Style Transfer

Provide an image and recreate its content in a different artistic style.

**Template:**
```
Transform the provided photograph of [subject] into the artistic style of [artist/art style]. 
Preserve the original composition but render it with [description of stylistic elements].
```

**Example:**
```
Transform the provided photograph of a modern city street at night into the artistic 
style of a 1980s synthwave poster. Preserve the composition but render it with neon 
pink and cyan colors, chrome reflections, and a grid perspective.
```

---

## 4. Advanced Composition: Combining Multiple Images

Provide multiple images to create a new composite scene. Perfect for product mockups or creative collages.

**Template:**
```
Create a new image by combining the elements from the provided images. 
Take the [element from image 1] and place it with/on the [element from image 2]. 
The final image should be a [description of the final scene].
```

**Example:**
```
Create a professional e-commerce fashion photo. Take the blue floral dress from image 1 
and show it being worn by the model from image 2. The final image should be a full-body 
shot in a clean white studio setting.
```

---

## 5. High-Fidelity Detail Preservation

Ensure critical details (face, logo) are preserved during edits by describing them explicitly.

**Template:**
```
Using the provided images, place [element from image 2] onto [element from image 1]. 
Ensure that the features of [element from image 1] remain completely unchanged. 
The added element should [description of how the element should integrate].
```

**Example:**
```
Using the provided images, place the sunglasses from image 2 onto the person's face 
in image 1. Ensure that the person's facial features remain completely unchanged. 
The sunglasses should sit naturally on the bridge of the nose with realistic reflections.
```

---

## 6. Bring Something to Life

Upload a rough sketch and refine it into a finished image.

**Template:**
```
Turn this rough [medium] sketch of a [subject] into a [style description] photo. 
Keep the [specific features] from the sketch but add [new details/materials].
```

**Example:**
```
Turn this rough pencil sketch of a sports car into a photorealistic studio photograph. 
Keep the aggressive body lines and proportions from the sketch but add glossy red paint, 
chrome details, and dramatic studio lighting.
```

---

## 7. Character Consistency: 360 View

Generate 360-degree views by iteratively prompting for different angles. Include previously generated images in subsequent prompts for consistency.

**Template:**
```
A studio portrait of [person] against [background], [looking forward/in profile looking right/etc.]
```

**Workflow:**
1. Generate initial view: "A studio portrait of a man with white glasses against a gray background, looking forward"
2. Include that image + prompt: "Same person, now in profile looking right"
3. Include both images + prompt: "Same person, three-quarter view looking left"

---

# Best Practices

**Be Hyper-Specific:**
Instead of "fantasy armor," describe it: "ornate elven plate armor, etched with silver leaf patterns, with a high collar and pauldrons shaped like falcon wings."

**Provide Context and Intent:**
Explain the purpose. "Create a logo for a high-end, minimalist skincare brand" beats "Create a logo."

**Iterate and Refine:**
Use conversation: "That's great, but can you make the lighting warmer?" or "Keep everything the same, but change the expression to more serious."

**Use Step-by-Step Instructions:**
For complex scenes: "First, create a background of a misty forest at dawn. Then, add a moss-covered stone altar in the foreground. Finally, place a glowing sword on top."

**Use Semantic Negative Prompts:**
Instead of "no cars," describe positively: "an empty, deserted street with no signs of traffic."

**Control the Camera:**
Use photographic terms: wide-angle shot, macro shot, low-angle perspective, 85mm portrait lens, three-point lighting.

**Generate Text First:**
For images with text, first generate the text content, then ask for an image containing it.

---

# Limitations

- **Languages:** Best in EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR, ru-RU, ua-UA, vi-VN, zh-CN
- **No audio/video inputs** for image generation
- **Image count may vary** from what you request
- **Input limits:**
  - `gemini-2.5-flash-image`: Up to 3 images
  - `gemini-3-pro-image-preview`: 5 images high-fidelity, up to 14 total
- **SynthID watermark** included in all generated images

---

# Quick Tips

- **Narrative > Keywords** — "A cat sleeping on a sunny windowsill" beats "cat, window, sun, sleeping"
- **Be specific** — Mention colors, materials, lighting, mood
- **Use photography terms** for realism — lens type, f-stop, lighting setup
- **Request transparent background** for stickers/icons
- **Specify aspect ratio** when composition matters
- **Use Gemini 3 Pro** for text rendering and complex scenes
- **For edits** — Describe what to preserve, not just what to change
