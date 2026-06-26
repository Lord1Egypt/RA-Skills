# 🎛️ The Style Mixer (Combinatorial Logic)

This engine ensures **infinite variety** by randomly combining stylistic factors.

## The Formula
`Result = Base Style + Material Twist + Lighting Modifier + Composition Rule`

## 1. Factor Pools

### A. Material Twists (The Texture)
*Select randomly based on Timestamp (Seconds % 8)*
1.  **Frosted Glass**: `Translucent, blur-20px, prism effect`
2.  **Liquid Metal**: `Chrome finish, fluid reflections, mercury-like`
3.  **Washi Paper**: `Fibrous texture, organic edges, soft ink bleed`
4.  **Vantablack**: `Absolute matte black, high contrast neon, void-like`
5.  **Bioplastic**: `Transparent organic material, cellular structure, glowing`
6.  **Sandstone**: `Rough texture, warm earth tones, ancient feel`
7.  **Holographic Foil**: `Iridescent, rainbow gradients, futuristic packaging`
8.  **Aerogel**: `Blue smoke, barely visible, floating`

### B. Lighting Modifiers (The Atmosphere)
*Select randomly based on Timestamp (Minutes % 7)*
1.  **Softbox**: `Studio lighting, even shadows, commercial look`
2.  **God Rays**: `Volumetric light, dust motes, dramatic entry`
3.  **Bioluminescence**: `Glowing from within, underwater vibe, cool tones`
4.  **Golden Hour**: `Warm sunlight, long shadows, emotional`
5.  **Neon Noir**: `Pink/Blue rim lights, dark background, cyberpunk`
6.  **Rembrandt**: `Strong contrast, triangular highlight, classical portrait`
7.  **Caustics**: `Water reflection patterns, dappled light, summer vibe`

### C. Composition Rules (The Eye-Flow)
*Select randomly*
1.  **Knolling**: `90-degree alignment, flat lay, organized chaos`
2.  **Golden Spiral**: `Focal point follows Fibonacci sequence`
3.  **Symmetry**: `Perfect mirror image, Wes Anderson style`
4.  **Extreme Macro**: `Close-up on details, shallow depth of field`
5.  **Isometric**: `30-degree angle, miniature world view`
6.  **Negative Space**: `Subject takes up 10%, 90% is empty void`

## 2. Harmony & Conflict Resolution (CRITICAL)

The engine MUST resolve physical contradictions.

*   **Conflict**: `Vantablack` (Absorbs light) + `Softbox` (Needs reflection).
    *   **Resolution**: Force Lighting to `Rim Light` or `Neon` to outline the shape.
*   **Conflict**: `Washi Paper` (2D/Flat) + `Caustics` (Needs depth/water).
    *   **Resolution**: Change `Caustics` to `Dappled Sunlight` (Shadows on paper).
*   **Conflict**: `Aerogel` (Invisible) + `High Key` (White background).
    *   **Resolution**: Force Background to `Dark/Black` to show the aerogel smoke.

## 3. Implementation in Prompt

When generating a prompt, **Roll the Dice** on these tables.
**MANDATORY**: Do not pick the first item. Use a randomization strategy (e.g., based on current time or random number generation) to pick an index.
