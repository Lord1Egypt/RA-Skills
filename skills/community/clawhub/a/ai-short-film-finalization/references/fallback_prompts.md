# Fallback Prompts for Problematic Shots

## 03 — Student / Civilian Era
`Cinematic medium shot, 1930s Shanghai street, young Chinese woman student named Li Lin with round face and short black hair, wearing simple blue cotton student jacket with white collar and dark skirt, no cap, no hat, no headwear, no badge, no military uniform, holding books, walking among other Chinese students in simple civilian clothes, old Chinese shop signs and art deco buildings in background, overcast daylight, documentary realism, 16:9, historical atmosphere, no military uniforms, no caps, no hats, no badges, no Japanese uniforms, no peaked caps`

## 06 — Cavalry / Battle (Single Rider to Avoid Timeout)
`Cinematic medium-wide shot, 1937 northern China dusty mountain valley in Yanbei, young Chinese woman commander Li Lin with round face and short black hair on a black horse galloping toward camera, wearing grey cotton Chinese Communist Eighth Route Army uniform with simple open collar, flat-topped cloth cap with two front buttons, and red scarf flying behind her, holding a modern rifle, determined heroic expression, dust and golden sunlight, film grain, historical drama, 16:9, no other soldiers, no ancient armor, no spears, no Japanese uniforms, no Japanese-style caps with ear flaps, no peaked caps, no cap badges, no samurai helmets`

## 07 — Villagers / Mass Scene
`Warm cinematic medium shot, 1930s northern Chinese village courtyard under a big old tree, young Chinese woman soldier Li Lin with round face and short black hair, wearing grey cotton Chinese Communist Eighth Route Army uniform with simple open collar and flat-topped cloth cap with two plain front buttons, no cap badge, no star, no insignia, no collar tabs, red scarf around neck, sitting with elderly villagers and children in simple plain cotton clothes, no caps, no hats, no headwear on villagers, sharing steamed buns, soft golden late afternoon light, 16:9, emotional heartwarming atmosphere, no Japanese uniforms, no peaked caps, no samurai helmets, no cap badges, no military caps on villagers`

## 12 — Memorial Hall (Fallback to Static Image + Zoom if Video Times Out)
When the memorial hall shot times out, create a static memorial image from `standard-portrait-v2.jpg`:
- Convert portrait to black and white
- Add vignette and dark border
- Add title text "李林烈士 永垂不朽" and dates "1915 - 1940"
- Add symbolic candles and wreaths
- Generate a slow zoom video with ffmpeg zoompan
