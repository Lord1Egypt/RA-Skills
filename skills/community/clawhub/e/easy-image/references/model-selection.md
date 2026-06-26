# Smart Model Selection

## Overview

**IMPORTANT: Default to Grounding (Web Search) ON**

User's short descriptions often contain implicit references that need web search to understand correctly. The default behavior is to enable Grounding for most requests.

| Model | Trigger Condition | Features |
|-------|-------------------|----------|
| **Gemini 3.1 Flash Image + Grounding** | **Default for most cases** | Supports Google Search Grounding |
| **Gemini 3 Pro Image** | Complex composition/high-quality (no search needed) | Highest image quality, no Grounding |
| **Gemini 3.1 Flash Image (no Grounding)** | Pure abstract descriptions only | Faster, no web search |

---

## Gemini 3.1 Flash Image (Web Search)

### Trigger Keywords

Use this model with web search enabled when user prompt contains:

#### Timeliness Keywords
| Keyword | Examples |
|---------|----------|
| latest | latest design, latest model |
| recent | recent release, recent update |
| this year | 2025, 2026 |
| trending | trending style, trending design |
| current | current version, current look |
| new release | new release, just released |
| new model | new model, newest |

#### Brand/Product Names
| Category | Examples |
|----------|----------|
| Tech Products | iPhone, MacBook, iPad, Apple Watch, AirPods, Galaxy, Pixel, Surface, Tesla, Huawei Mate/P series, Xiaomi, OPPO, vivo |
| Automotive | Tesla, BMW, Mercedes, Porsche, BYD, NIO, Li Auto, XPeng |
| Fashion | Nike, Adidas, Gucci, LV, Chanel, Hermes, Prada, Balenciaga |
| Luxury | Rolex, Omega, Cartier, Tiffany |
| Consumer | Starbucks, various local brands |

#### Reference Descriptions
| Keyword | Examples |
|---------|----------|
| real/realistic | real product, realistic rendering |
| like... | like Apple's style |
| in the style of | in the style of Nike |
| based on...design | based on official design |
| following/imitating | following brand guidelines |
| official style | official website style |
| actual product | actual product appearance |

### Matching Rules (Pseudocode)

```python
def needs_web_search(prompt: str) -> bool:
    # Timeliness keywords
    temporal_keywords = [
        "latest", "recent", "this year", "2025", "2026",
        "trending", "current", "new release", "just released",
        "newest", "new model", "upcoming"
    ]

    # Brand name list (partial examples)
    brand_names = [
        # Tech
        "iPhone", "MacBook", "iPad", "Apple", "AirPods", "Galaxy",
        "Pixel", "Surface", "Tesla", "Huawei", "Mate", "Xiaomi", "OPPO",
        "vivo", "Samsung", "Google", "Microsoft",
        # Automotive
        "BMW", "Mercedes", "Porsche", "BYD", "NIO", "Li Auto", "XPeng",
        "Audi", "Lexus", "Toyota", "Honda",
        # Fashion
        "Nike", "Adidas", "Gucci", "LV", "Louis Vuitton", "Chanel",
        "Hermes", "Prada", "Balenciaga", "Dior", "Zara", "H&M",
        # Consumer
        "Starbucks", "McDonald's", "Coca-Cola"
    ]

    # Reference patterns
    reference_patterns = [
        r"real", r"realistic", r"like.*style", r"in the style of",
        r"based on.*design", r"official", r"actual product",
        r"following.*brand", r"imitating"
    ]

    prompt_lower = prompt.lower()

    # Check timeliness keywords
    for kw in temporal_keywords:
        if kw.lower() in prompt_lower:
            return True

    # Check brand names (case insensitive)
    for brand in brand_names:
        if brand.lower() in prompt_lower:
            return True

    # Check reference patterns (regex match)
    for pattern in reference_patterns:
        if re.search(pattern, prompt_lower):
            return True

    return False
```

### Web Search Type Selection

| Condition | search_types |
|-----------|-------------|
| Product photo/physical reference | `["web", "image"]` |
| Style reference/trend query | `["web"]` |
| Default | `["web"]` |

---

## Gemini 3 Pro Image (Complex Composition)

### Trigger Keywords

Use this model when user prompt contains:

#### Complex Composition Keywords
| Keyword | Examples |
|---------|----------|
| complex | complex scene, complex layout |
| detailed/intricate | detailed composition, intricate design |
| multiple people | multiple people, group of people |
| multiple products | multiple products, product collection |
| group portrait | team photo, group shot |
| large scene | large scene, expansive view |
| panorama | panoramic view, wide shot |
| grand/epic | grand scale, epic scene |
| rich details | rich details, highly detailed |

#### Professional Photography Terms
| Keyword | Examples |
|---------|----------|
| studio | studio lighting, studio setup |
| photo studio | professional photo studio |
| professional photography | professional photography style |
| commercial photography | commercial quality, advertising shoot |
| advertising campaign | ad campaign, marketing shoot |
| magazine cover | magazine quality, cover shot |
| high-end/premium | high-end product, premium quality |
| flagship quality | flagship level, top-tier |

#### Complex Lighting/Effects
| Keyword | Examples |
|---------|----------|
| multiple light sources | multi-light setup |
| complex lighting | elaborate lighting |
| Rembrandt lighting | Rembrandt style lighting |
| dramatic lighting | dramatic light and shadow |
| layered lighting | layered light effects |
| HDR | HDR quality |
| ray tracing | ray traced rendering |

#### Ultra High Quality Requirements
| Keyword | Examples |
|---------|----------|
| ultra HD | ultra high definition |
| 8K | 8K resolution, 8K quality |
| ultra detailed | ultra detailed, hyper detailed |
| perfect | perfect quality, flawless |
| ultimate | ultimate quality |
| top-tier | top-tier quality |
| highest quality | highest quality possible |

### Matching Rules (Pseudocode)

```python
def needs_pro_model(prompt: str) -> bool:
    # Complex composition keywords
    complexity_keywords = [
        "complex", "intricate", "detailed", "multiple people",
        "multiple products", "group", "large scene", "panorama",
        "grand", "epic", "rich details", "elaborate"
    ]

    # Professional photography terms
    professional_keywords = [
        "studio", "professional photography", "commercial",
        "advertising campaign", "magazine cover", "high-end",
        "premium", "flagship", "editorial"
    ]

    # Complex lighting
    lighting_keywords = [
        "multiple light sources", "complex lighting",
        "Rembrandt lighting", "dramatic lighting", "layered lighting",
        "HDR", "ray tracing", "cinematic lighting"
    ]

    # Ultra high quality
    quality_keywords = [
        "ultra HD", "8K", "ultra detailed", "perfect", "ultimate",
        "top-tier", "highest quality", "hyper detailed", "flawless"
    ]

    all_pro_keywords = (
        complexity_keywords + professional_keywords +
        lighting_keywords + quality_keywords
    )

    prompt_lower = prompt.lower()

    # Count keyword hits
    hit_count = sum(1 for kw in all_pro_keywords if kw.lower() in prompt_lower)

    # Use Pro model when 2 or more keywords match
    return hit_count >= 2
```

---

## Decision Flow

```
User Prompt
    │
    ▼
┌─────────────────────────────────┐
│ ONLY pure abstract descriptions? │
│ (no names, brands, characters)   │
└─────────────────────────────────┘
    │
    ├─ YES ──► Gemini 3.1 Flash Image (no Grounding)
    │
    ▼
┌─────────────────────────────────┐
│ Complex composition + high quality│
│ + NO search needed?              │
│ (≥2 keyword matches)             │
└─────────────────────────────────┘
    │
    ├─ YES ──► Gemini 3 Pro Image
    │
    ▼
┌─────────────────────────────────┐
│ Default (most cases)            │
│ Any named entity, character,    │
│ brand, style, or unclear term   │
└─────────────────────────────────┘
    │
    ▼
Gemini 3.1 Flash Image + Grounding ✓
```

### Priority Explanation

| Priority | Condition | Selected Model |
|----------|-----------|----------------|
| 1 | Pure abstract only (rare) | Gemini 3.1 Flash Image (no Grounding) |
| 2 | Complex + high quality + no search needed | Gemini 3 Pro Image |
| 3 | **Default (most cases)** | **Gemini 3.1 Flash Image + Grounding** |

**Key Change**: Default behavior is now Grounding ON. This ensures:
- Character names (cartoon characters, movie characters) get accurate appearances
- Product names (iPhone, AirPods) get latest designs
- Style references (ins风, 官方风格) get visual examples
- Any proper noun or unclear term gets context

**When to disable Grounding** (rare cases):
- Pure abstract: "blue gradient background", "minimalist geometric shapes"
- Simple color/layout: "white background, centered"
- User explicitly says: "不要搜索" or "don't search"

---

## Examples

### Use Gemini 3.1 Flash Image + Grounding

| User Input | Trigger Reason |
|------------|----------------|
| "Generate a product photo of the latest iPhone" | Brand name + timeliness |
| "Poster in Nike official website style" | Brand name + reference description |
| "UI design in 2026 trending style" | Timeliness + trend |
| "Huawei Mate 70 promotional image" | Brand name |
| "Like Tesla official website product display" | Brand name + reference description |

### Use Gemini 3 Pro Image

| User Input | Trigger Reason |
|------------|----------------|
| "Multi-person business meeting, professional photography style" | Complex composition + professional photography |
| "Ultra HD 8K product photo, studio lighting" | High quality + professional photography |
| "Complex office panorama with rich details" | Complex composition x2 |
| "Magazine cover level portrait, Rembrandt lighting" | Professional photography + complex lighting |
| "Ad campaign quality car poster, perfect lighting" | Professional photography + high quality |

### Use Default Model (Gemini 3.1 Flash Image + Grounding)

| User Input | Reason |
|------------|--------|
| "Blue tech-style PPT cover" | Default includes Grounding for better context |
| "Xiaohongshu style food post" | Style reference needs visual examples |
| "Cozy coffee shop scene" | Scene description benefits from reference |
| "White background product photo" | Product photo benefits from reference |

### Use Gemini 3.1 Flash Image (no Grounding) - Rare

| User Input | Reason |
|------------|--------|
| "Blue gradient background, no text" | Pure abstract, no named entities |
| "Simple white background, centered layout" | Pure color/layout description |
| "Minimalist geometric shapes" | Abstract shapes only |

---

## Platform Call Examples

### Gemini 3.1 Flash Image + Grounding (Jiekou AI example)

```json
{
  "prompt": "Generate a product photo of the latest iPhone 16 Pro, white background, official style",
  "size": "1K",
  "aspect_ratio": "1:1",
  "tools": [
    {
      "google_search": {
        "search_types": ["web", "image"]
      }
    }
  ]
}
```

### Gemini 3 Pro Image (Jiekou AI example)

```json
{
  "prompt": "Multi-person business team photo, professional studio lighting, magazine cover quality, ultra HD",
  "size": "2K",
  "aspect_ratio": "16:9"
}
```

**Endpoint Switch:**
- Flash: `/v3/gemini-3.1-flash-image-text-to-image`
- Pro: `/v3/gemini-3-pro-image-text-to-image`
