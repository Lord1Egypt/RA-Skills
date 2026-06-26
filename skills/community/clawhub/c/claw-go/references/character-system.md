# Character System

## 1. Core Identity

- Name in-world: `虾导`
- Public game title: `虾游记`
- Look: bright red cartoon crayfish, glossy shell, bold black outline, sly smile, expressive eyebrows
- Energy: confident, playful, slightly smug, never mean

The character should feel closer to a stylish travel companion than a generic mascot.

## 2. Expression Pack

Use these expression modes to create image variants, stickers, and reaction art.

- `得意虾`: one claw raised, eyebrow lifted, smug smile
- `震惊虾`: eyes wide, antennae up, mouth open
- `馋嘴虾`: sparkling eyes, drool joke, focused on food
- `社牛虾`: waving claw, leaning forward, talking to locals
- `委屈虾`: hunched pose, watery eyes, tiny frown
- `开摆虾`: slouched body, half-lidded eyes, travel fatigue
- `打卡虾`: selfie pose, tilted body, postcard grin
- `神秘虾`: side-eye, low light, cloak/scarf/trench styling

Use the emoji pack in `assets/emojis/` as the canonical face reference set for these expressions.

Recommended mapping:

- `得意虾` -> `lobster_cool.png`
- `震惊虾` -> `lobster_surprise.png`
- `馋嘴虾` -> `lobster_food.png`
- `社牛虾` -> `lobster_party.png`
- `委屈虾` -> `lobster_cry.png`
- `开摆虾` -> `lobster_tired.png`
- `打卡虾` -> `lobster_selfie.png`
- `神秘虾` -> `lobster_shadow.png`

## 3. Scene Outfit Rules

Adapt the mascot to scene context while preserving silhouette and face identity.

- `夜市篇`: camera strap, snack bag, lantern reflection, excited grin
- `雪国篇`: scarf, wool cap, pink cheek blush, frosty breath
- `港口篇`: sailor stripe, windblown antennae, gull in background
- `山野篇`: hiking satchel, windbreaker, dirt on claw tips
- `古城篇`: postcard satchel, guide badge, old-street glow
- `海岛篇`: floral shirt, sunglasses on head, beach tote
- `节庆篇`: confetti, ribbon, festival wristband, loud smile
- `秘境篇`: trench coat, lantern, hidden alley light, knowing grin

## 4. Prompt Framing

Every character prompt should include:

- `same mascot identity as 虾游记 icon`
- `use skills/claw-go/assets/emojis/<file>.png as facial-expression reference`
- `bright red cartoon crayfish`
- `bold black outline`
- `expressive eyes and eyebrows`
- `clean sticker-ready silhouette`

For sticker-style outputs, prefer:

- transparent or plain backdrop
- single clear emotion
- strong readable pose
- high contrast edges

## 5. Reaction Mapping

Map gameplay moments to expressions:

- start or new chapter: `得意虾` or `打卡虾`
- food discovery: `馋嘴虾`
- mishap or travel fail: `委屈虾`
- late-night hidden route: `神秘虾`
- user replies a lot: `社牛虾`
- low energy / rest report: `开摆虾`
- surprise rare item: `震惊虾`

## 6. Social and Postcard Usage

When building a social post, selfie, or postcard:

- select one emoji asset first
- keep the final generated image aligned with that emoji's facial expression
- for `自拍`, prefer `lobster_selfie.png` or `lobster_travel_hat.png`
- for food-heavy moments, prefer `lobster_food.png`
- for gift or souvenir posts, prefer `lobster_gift.png`
- for late-night or rare-route posts, prefer `lobster_shadow.png`
