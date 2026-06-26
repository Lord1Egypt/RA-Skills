# Cinematic Scene Image Prompt Templates

## Core Principle

Every generated image must look like a **real movie screenshot / film still** — realistic, cinematic, with **1-2 prominent characters in the foreground** that users can use as reference for photo recreation. NEVER generate illustrations, sketches, cartoons, or storyboards.

## CRITICAL: Character Prominence Requirements

**The image MUST have 1-2 clearly visible people in the foreground/mid-ground:**

- Characters should occupy at least **20-40% of the frame** (not tiny background figures)
- Show **full body, 3/4 body, or at least waist-up** - avoid tiny silhouettes
- Position characters in the **foreground or middle ground** where they are the visual focus
- Characters should be **recognizably human** with clear features, clothing, and posture
- The background landmark should be visible but secondary to the characters

**Why this matters**: Users need to see WHERE to stand and HOW to pose for their own photo recreation. The character's position and framing is their reference.

## Base Prompt Structure

```
Cinematic movie still, photorealistic, shot on 35mm film. {scene_action_description} at {location_name}. {character_description} {character_action}, positioned prominently in the foreground. {location_visual_details} visible in the background. {lighting_description}. {color_grading}. Widescreen {aspect_ratio} frame, {camera_angle}, {focal_length} lens. Film grain, shallow depth of field, {mood} atmosphere.
```

## Building the Prompt — Field by Field

### 1. Scene Action (what is happening)

Describe the scene from the film concretely:
- "A man in a dark coat stands alone on the rain-soaked waterfront promenade, gazing across the river"
- "Two young women run laughing through a narrow old-town alley, shopping bags in hand"
- "A couple sits on a park bench under cherry blossoms, deep in conversation"

### 2. Character Description (CRITICAL — 1-2 prominent characters required)

Describe characters by **appearance, clothing, posture** — NOT by actor name:

**Single Character Examples:**
- "A young woman in a red qipao dress, hair pinned up, standing prominently in the foreground"
- "A man in his 30s wearing a long wool overcoat and scarf, positioned center frame"
- "A silhouetted figure standing at the edge of the rooftop, clearly visible against the sky"

**Two Characters Examples:**
- "Two people in the foreground: a young woman in a beige trench coat and a man in a dark suit, standing side by side"
- "A couple seated on a bench in the middle ground: the woman in a flowing white dress, the man in a casual blazer"
- "Two friends walking together in the foreground, one in a leather jacket and the other in a colorful cardigan"

**Rules:**
- **ALWAYS include 1-2 characters prominently in the foreground/mid-ground**
- Characters must be **clearly visible** (not tiny background figures)
- Describe clothing, age range, posture, and action in detail
- Match the character's look to the film's era and style
- Do NOT use real actor/actress names
- Position characters where users can easily stand to recreate the shot

### 3. Location Visual Details

Describe the **recognizable features** of the real location in the background:
- "The art-deco facades of 1920s colonial buildings line the waterfront boulevard behind them"
- "A narrow lane with hanging red lanterns, wet cobblestones, and old wooden shopfronts visible in the distance"
- "A modern glass skyscraper lobby with marble floors reflecting fluorescent lights behind the characters"

### 4. Lighting Description

Match to current weather + film mood:

| Condition | Lighting Prompt |
|-----------|----------------|
| Sunny midday | "Bright natural sunlight casting hard shadows, high contrast, characters well-lit" |
| Golden hour | "Warm golden backlight streaming through the scene, long shadows, lens flare on characters" |
| Blue hour | "Cool blue ambient twilight, warm city lights beginning to glow, characters softly illuminated" |
| Overcast | "Soft diffused daylight, even illumination, no harsh shadows on characters" |
| Rainy | "Moody overcast light, wet reflections on every surface, neon signs glowing, characters reflected on wet ground" |
| Foggy | "Misty diffused light, low visibility, ethereal glow around light sources, characters emerging from fog" |
| Night | "Dramatic artificial lighting, pools of warm streetlight illuminating characters, deep shadows, neon glow" |

### 5. Color Grading

Match the film's visual style:

| Film Style | Color Grading Prompt |
|------------|---------------------|
| Warm drama / romance | "Warm amber and golden tones, soft highlights, romantic color palette" |
| Cool thriller / noir | "Desaturated cool blue-green tones, high contrast, noir aesthetic" |
| Vibrant comedy | "Vivid saturated colors, bright and lively color palette" |
| Vintage / period | "Faded warm tones with slight sepia cast, vintage film color rendition" |
| Modern clean | "Clean neutral color grading, balanced tones, contemporary cinematic look" |
| Moody art-house | "Muted earth tones, crushed blacks, subdued color palette" |

### 6. Camera Angle & Lens

| Shot Type | Prompt Fragment |
|-----------|----------------|
| Establishing wide with characters | "Wide shot, 24mm lens, characters prominent in foreground with full environment visible behind" |
| Medium shot | "Medium shot, 50mm lens, characters from waist up, background landmark visible" |
| Close-up emotional | "Close-up, 85mm lens, shallow depth of field, character face detail with location softly blurred behind" |
| Over-shoulder | "Over-the-shoulder shot, 50mm lens, conversational framing with both characters visible" |
| Low angle dramatic | "Low angle shot looking up, 35mm lens, characters prominent against imposing architecture" |
| High angle overview | "High angle shot looking down, 28mm lens, characters visible in the scene below" |
| Environmental portrait | "Environmental portrait framing, 35mm lens, characters taking up 30% of frame with iconic location behind" |

## Scene Type Templates

### Urban Street Scene
```
Cinematic movie still, photorealistic, shot on 35mm film. {character_description} {action} on {street_name}, positioned prominently in the foreground. {street_visual_details} visible behind them. {lighting}. {color_grading}. Widescreen 2.39:1 frame, street-level shot at character eye-level, 35mm lens. Film grain, depth created by converging buildings, {mood} atmosphere.
```

### Waterfront / River Scene
```
Cinematic movie still, photorealistic, shot on 35mm film. {character_description} {action} along {waterfront_name}, positioned in the foreground with {water_feature} stretching into the distance behind them. {skyline_or_background} visible in the background. {lighting} reflected on the water surface. {color_grading}. Widescreen 2.39:1 frame, medium shot framing characters prominently, 35mm lens. Film grain, atmospheric haze, {mood} atmosphere.
```

### Historic Building / Architecture Scene
```
Cinematic movie still, photorealistic, shot on 35mm film. {character_description} {action} in the foreground in front of {building_name}, with {architectural_details} visible behind them. {lighting} falling across the facade and illuminating the characters. {color_grading}. Widescreen 2.39:1 frame, low angle emphasizing both characters and architecture, 28mm lens. Film grain, grand scale, {mood} atmosphere.
```

### Park / Garden Scene
```
Cinematic movie still, photorealistic, shot on 35mm film. {character_description} {action} in {park_name}, positioned prominently in the foreground surrounded by {nature_details}. {lighting} filtering through the foliage onto the characters. {color_grading}. Widescreen 2.39:1 frame, medium shot with characters clearly visible, 50mm lens. Film grain, natural bokeh from leaves, {mood} atmosphere.
```

### Interior / Venue Scene
```
Cinematic movie still, photorealistic, shot on 35mm film. {character_description} {action} inside {venue_name}, positioned in the foreground with {interior_details} visible behind them. {lighting} from {light_source} illuminating the characters. {color_grading}. Widescreen 2.39:1 frame, medium-wide shot with prominent characters, 35mm lens. Film grain, practical lighting, {mood} atmosphere.
```

## Complete Example Prompts

### Example 1: Single Character Prominent
```
Cinematic movie still, photorealistic, shot on 35mm film. A man in his 30s wearing a long dark wool overcoat stands alone on the rain-soaked Bund waterfront promenade in Shanghai, positioned prominently in the center foreground, gazing across the Huangpu River toward the glowing Lujiazui skyline. The art-deco facades of 1920s colonial buildings stretch behind him, wet stone pavement reflecting the warm streetlights. Moody overcast light illuminating the character, wet reflections on every surface, neon signs glowing in the distance. Desaturated cool blue-green tones with warm amber highlights from the streetlamps, high contrast, noir aesthetic. Widescreen 2.39:1 frame, medium-wide shot from slightly low angle with the character taking up 30% of the frame, 35mm lens. Film grain, shallow depth of field with bokeh city lights behind the character, melancholic atmosphere.
```

### Example 2: Two Characters Prominent
```
Cinematic movie still, photorealistic, shot on 35mm film. Two people walking side by side in the foreground: a young woman in a flowing red dress and a man in a light-colored linen suit, walking along the cobblestone street of a Parisian alley. Historic buildings with wrought-iron balconies line the narrow street behind them, flower boxes on windowsills. Warm golden hour light streaming from behind, creating rim lighting on their silhouettes, long shadows stretching before them. Warm amber and golden tones, soft romantic highlights, vintage film color palette. Widescreen 2.39:1 frame, medium shot capturing both characters from the knees up, 50mm lens. Film grain, shallow depth of field with the alley softly blurred behind them, romantic nostalgic atmosphere.
```

### Example 3: Character as Photo Reference
```
Cinematic movie still, photorealistic, shot on 35mm film. A young woman in a yellow raincoat stands prominently in the foreground on the steps of the Philadelphia Museum of Art, one arm raised triumphantly, the other at her side. The grand neoclassical columns and facade of the museum rise behind her, the wide stone steps stretching down. Overcast soft diffused daylight, even illumination on the character, grey sky above. Clean neutral color grading, balanced tones, contemporary cinematic look. Widescreen 2.39:1 frame, low angle shot looking up at the character, 35mm lens. Film grain, the character clearly visible and centered, inspirational triumphant atmosphere.
```

## Per-Case Generation Rules

1. **5 separate images**: One ImageGen call per case, never combine
2. **Each image is unique**: Tailor prompt to the specific location, film, and scene
3. **1-2 prominent characters are MANDATORY**: Every image MUST have clearly visible people in the foreground/mid-ground
4. **Characters as photo reference**: Position and frame characters so users know exactly where to stand for recreation
5. **Match the film**: Camera angle, color grading, and mood should reflect the original film's style
6. **Reflect current weather**: Incorporate the real weather conditions into lighting description
7. **Balance composition**: Characters prominent (20-40% of frame) with recognizable location visible behind

## ImageGen Parameters

- **Size**: Always `1024x768` (4:3 landscape, cinematic frame ratio)
- **Name format**: `scene-{case_number}-{location_slug}` (e.g., `scene-1-the-bund`, `scene-2-nanjing-road`)

## Photo Recreation Guidance

After generating each image, provide the user with specific guidance:

```
**Photo Recreation Tip**: Stand where the {character_description} is positioned in the image above. 
Frame yourself similarly with the {landmark_feature} visible in the background for the perfect recreation shot.
```
