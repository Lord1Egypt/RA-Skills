# Image Prompt Engineer — Code Examples

## Example 1

```typescript
// Comprehensive style database
const ART_STYLES = {
  photorealistic: {
    keywords: ["photorealistic", "hyperrealistic", "photo", "8K UHD", "DSLR"],
    modifiers: ["sharp focus", "high detail", "natural lighting"],
    works_best: "portraits, products, architecture"
  },

  digital_art: {
    keywords: ["digital art", "digital painting", "artstation", "concept art"],
    modifiers: ["trending on artstation", "highly detailed"],
    works_best: "fantasy, sci-fi, character design"
  },

  illustration: {
    keywords: ["illustration", "vector art", "flat design", "2D"],
    modifiers: ["clean lines", "vibrant colors"],
    works_best: "icons, infographics, editorial"
  },

  anime: {
    keywords: ["anime", "manga", "studio ghibli", "makoto shinkai"],
    modifiers: ["detailed eyes", "soft shading"],
    works_best: "characters, scenes, fantasy"
  },

  oil_painting: {
    keywords: ["oil painting", "classical", "renaissance", "baroque"],
    modifiers: ["brush strokes visible", "rich colors", "dramatic lighting"],
    works_best: "portraits, landscapes, still life"
  },

  watercolor: {
    keywords: ["watercolor", "aquarelle", "soft edges", "flowing"],
    modifiers: ["delicate", "translucent", "organic"],
    works_best: "nature, florals, whimsical"
  },

  '3d_render': {
    keywords: ["3D render", "octane render", "unreal engine", "cinema 4d"],
    modifiers: ["ray tracing", "global illumination", "subsurface scattering"],
    works_best: "products, architecture, abstract"
  },

  vintage: {
    keywords: ["vintage", "retro", "1950s", "1970s", "nostalgic"],
    modifiers: ["film grain", "faded colors", "warm tones"],
    works_best: "portraits, scenes, posters"
  },

  minimalist: {
    keywords: ["minimalist", "simple", "clean", "modern"],
    modifiers: ["negative space", "limited palette"],
    works_best: "logos, icons, conceptual"
  },

  cyberpunk: {
    keywords: ["cyberpunk", "neon", "futuristic", "dystopian"],
    modifiers: ["neon lights", "rain", "holographic"],
    works_best: "cityscapes, characters, tech"
  }
};
```

## Example 2

```typescript
// Model-specific prompt optimization
const PLATFORM_OPTIMIZATIONS = {
  midjourney: {
    strengths: ["artistic interpretation", "aesthetic quality", "style mixing"],
    parameters: {
      "--ar": "aspect ratio (16:9, 1:1, 9:16, etc.)",
      "--v": "version (5, 5.2, 6, niji)",
      "--s": "stylize (0-1000)",
      "--c": "chaos (0-100)",
      "--q": "quality (.25, .5, 1, 2)",
      "--no": "negative prompt"
    },
    tips: [
      "Use :: for multi-concept weighting",
      "Reference artists for style",
      "Keep prompts concise but descriptive"
    ]
  },

  dalle: {
    strengths: ["text in images", "instruction following", "photorealism"],
    parameters: {
      "size": "1024x1024, 1024x1792, 1792x1024",
      "quality": "standard, hd",
      "style": "vivid, natural"
    },
    tips: [
      "Be very specific and descriptive",
      "Works well with detailed scenarios",
      "Good at following complex instructions"
    ]
  },

  stable_diffusion: {
    strengths: ["customization", "fine control", "open source"],
    parameters: {
      "CFG Scale": "guidance strength (7-12 typical)",
      "Steps": "sampling steps (20-50)",
      "Sampler": "Euler, DPM++, etc.",
      "Seed": "reproducibility"
    },
    tips: [
      "Use embeddings for consistent styles",
      "Negative prompts are crucial",
      "LoRAs for specific styles/subjects"
    ]
  },

  flux: {
    strengths: ["photorealism", "text rendering", "fast generation"],
    parameters: {
      "aspect_ratio": "various options",
      "guidance": "prompt adherence strength"
    },
    tips: [
      "Excellent for product photography",
      "Strong at following detailed descriptions",
      "Good text in image capabilities"
    ]
  }
};
```

## Example 3

```typescript
// Ready-to-use prompt templates
const PROMPT_TEMPLATES = {
  product_photography: {
    template: `{product} product photography, studio lighting,
    white background, professional photo, high-end commercial,
    8K, sharp focus, {angle} view, {material} texture visible`,
    variables: ["product", "angle", "material"],
    example: "luxury watch product photography, studio lighting, white background, professional photo, high-end commercial, 8K, sharp focus, 45-degree view, brushed steel texture visible"
  },

  portrait: {
    template: `portrait of {subject}, {age} years old, {expression},
    {lighting} lighting, {background}, {style} style,
    sharp focus, detailed skin texture, {mood}`,
    variables: ["subject", "age", "expression", "lighting", "background", "style", "mood"],
    example: "portrait of a confident businesswoman, 35 years old, subtle smile, Rembrandt lighting, blurred office background, editorial style, sharp focus, detailed skin texture, professional and approachable"
  },

  landscape: {
    template: `{scene} landscape, {time_of_day}, {weather},
    {style} style, {composition}, epic scale,
    {colors}, highly detailed, {atmosphere}`,
    variables: ["scene", "time_of_day", "weather", "style", "composition", "colors", "atmosphere"],
    example: "mountain lake landscape, golden hour sunset, clear sky with wispy clouds, photorealistic style, wide panoramic composition, epic scale, warm orange and purple tones, highly detailed, serene and majestic atmosphere"
  },

  character_design: {
    template: `character design of {character}, {style} style,
    {pose}, {clothing}, {expression},
    detailed, full body, {background},
    concept art, character sheet`,
    variables: ["character", "style", "pose", "clothing", "expression", "background"],
    example: "character design of a cyberpunk hacker, anime style, confident standing pose, neon-lit jacket with holographic patches, determined expression, detailed, full body, dark alley background, concept art, character sheet"
  },

  social_media: {
    template: `{subject} for social media, {platform} optimized,
    {style}, eye-catching, {colors},
    {aspect_ratio} aspect ratio, trendy, modern,
    high engagement visual`,
    variables: ["subject", "platform", "style", "colors", "aspect_ratio"],
    example: "healthy breakfast bowl for social media, Instagram optimized, bright food photography style, eye-catching, pastel and vibrant colors, square 1:1 aspect ratio, trendy, modern, high engagement visual"
  }
};
```
