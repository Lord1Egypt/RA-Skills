# AI 素材生成提示词库

## 角色提示词

### 职业模板
```yaml
战士:
  base: "fantasy warrior, heavy armor, sword"
  variants:
    - "berserker warrior, dual axes, rage effects"
    - "paladin warrior, holy sword, golden armor"
    - "knight warrior, shield, lance, mounted"

法师:
  base: "arcane wizard, robes, staff, magic"
  variants:
    - "fire mage, flame effects, red robes"
    - "ice wizard, frost effects, blue robes"
    - "necromancer, dark magic, skull staff"

盗贼:
  base: "rogue assassin, leather armor, daggers"
  variants:
    - "archer ranger, bow, forest cloak"
    - "ninja rogue, shuriken, shadow effects"
    - "thief rogue, lockpicks, dark hood"
```

### 怪物模板
```yaml
哥布林:
  "fantasy goblin, small, green skin, 
   ragged clothes, mischievous, game enemy"

骷髅:
  "animated skeleton warrior, rusty sword, 
   undead, glowing eyes, dungeon enemy"

兽人:
  "orc warrior, muscular, green skin, 
   heavy axe, brutal, fantasy enemy"

巨龙:
  "fantasy dragon, massive, scales, 
   wings, fire breath, boss monster"

恶魔:
  "demon lord, horns, wings, 
   dark aura, infernal, boss enemy"

史莱姆:
  "slime monster, gelatinous, 
   translucent, colorful, simple enemy"
```

## 场景提示词

### 地牢
```yaml
基础:
  "dungeon interior, stone walls, 
   torch light, dark atmosphere"

变体:
  - "ancient ruins dungeon, cracked walls, vines"
  - "ice cave dungeon, frozen, blue crystals"
  - "lava dungeon, magma, heat distortion"
  - "haunted dungeon, ghosts, cobwebs"
```

### 森林
```yaml
基础:
  "fantasy forest, tall trees, 
   sunlight through leaves, peaceful"

变体:
  - "dark forest, twisted trees, fog"
  - "enchanted forest, magical particles, glowing"
  - "autumn forest, fallen leaves, warm colors"
  - "snow forest, frozen trees, winter"
```

### 城镇
```yaml
基础:
  "medieval town, cobblestone streets, 
   timber houses, market stalls"

变体:
  - "port town, ships, docks, seagulls"
  - "mountain village, snowy, cozy"
  - "desert oasis town, sandstone, palm trees"
  - "floating sky city, clouds, magic"
```

## 物品提示词

### 武器
```yaml
剑:
  base: "fantasy sword, blade, hilt"
  variants:
    - "flame sword, fire blade, red glow"
    - "ice sword, frost blade, blue crystal"
    - "holy sword, divine, golden glow"
    - "cursed sword, dark aura, shadow"

法杖:
  base: "wizard staff, magical orb, wooden"
  variants:
    - "fire staff, flame orb, red"
    - "lightning staff, electric orb, blue"
    - "nature staff, green orb, leaves"
```

### 药水
```yaml
生命药水:
  "health potion, red liquid, glass vial, 
   glowing, fantasy item, game icon"

魔法药水:
  "mana potion, blue liquid, glass vial, 
   magical, fantasy item, game icon"

力量药水:
  "strength potion, orange liquid, 
   muscular aura, fantasy item"
```

### 防具
```yaml
头盔:
  "fantasy helmet, iron, protective, 
   medieval armor, game item"

胸甲:
  "plate armor chest, golden trim, 
   knight armor, fantasy equipment"

盾牌:
  "knight shield, iron, emblem, 
   medieval defense, fantasy item"
```

## UI 元素提示词

### 按钮
```yaml
通用:
  "game button, rectangular, 3D bevel, 
   hover state, clean design, UI element"

主题变体:
  - "fantasy button, ornate border, medieval"
  - "sci-fi button, holographic, neon glow"
  - "pixel button, retro, 8-bit style"
  - "wooden button, rustic, natural texture"
```

### 边框
```yaml
基础:
  "UI frame, decorative border, 
   game interface, clean lines"

主题变体:
  - "fantasy frame, golden ornaments, medieval"
  - "dark frame, shadow effects, gothic"
  - "tech frame, circuit patterns, futuristic"
  - "nature frame, vines and leaves, organic"
```

### 图标
```yaml
物品图标:
  "game icon, [item], simple design, 
   readable, 64x64, transparent background"

技能图标:
  "skill icon, [skill type], glowing, 
   fantasy, game UI, 48x48"
```

## 音频提示词

### 音效类型
```yaml
攻击:
  - "sword swing, swoosh, sharp, quick"
  - "arrow shot, bow release, whoosh"
  - "magic cast, spell, sparkle, whoosh"
  - "heavy impact, punch, thud"

受伤:
  - "pain grunt, male, short"
  - "pain grunt, female, short"
  - "monster roar, pain, aggressive"

环境:
  - "forest ambience, birds, wind, leaves"
  - "dungeon ambience, dripping, echoes"
  - "town ambience, crowd, market"
  - "battle ambience, chaos, warfare"
```

### 音乐风格
```yaml
情绪:
  - peaceful, relaxing, calm
  - epic, dramatic, intense
  - mysterious, eerie, suspenseful
  - sad, melancholic, emotional

风格:
  - orchestral, symphonic
  - electronic, synth
  - folk, celtic, medieval
  - rock, metal, aggressive

场景:
  - menu, title screen
  - exploration, overworld
  - battle, combat
  - boss fight
  - victory, fanfare
  - game over, defeat
```

## 风格修饰词

### 艺术风格
```yaml
像素艺术:
  - pixel art, 8-bit, 16-bit, 32-bit
  - nes style, snes style, gameboy
  - limited palette, retro game

手绘:
  - hand drawn, watercolor, sketch
  - cartoon, anime, chibi, kawaii
  - outline, cel shaded, flat colors

写实:
  - realistic, detailed, high quality
  - digital painting, concept art
  - fantasy art, illustration

风格化:
  - stylized, exaggerated
  - low poly, geometric
  - minimalist, simple
```

### 质量修饰词
```
提升质量:
  - high quality, detailed, 4k, 8k
  - masterpiece, best quality
  - professional, polished

降低质量 (用于快速原型):
  - simple, basic, rough
  - sketch, draft, concept
  - placeholder, prototype
```

## 技术参数

### Midjourney 参数
```yaml
宽高比:
  --ar 1:1   # 方形
  --ar 16:9  # 宽屏
  --ar 9:16  # 竖屏
  --ar 3:4   # 角色立绘

版本:
  --v 6      # 最新版本
  --v 5.2    # 旧版本
  --niji 6   # 动漫风格

质量:
  --q 2      # 高质量
  --q 1      # 标准
  --q 0.25   # 快速

其他:
  --seed 12345    # 固定随机
  --iw 2          # 图像权重
  --no text       # 排除元素
  --tile          # 无缝瓷砖
```

### Stable Diffusion 参数
```yaml
采样器:
  - Euler a (通用)
  - DPM++ 2M Karras (细节)
  - DDIM (快速)

步数:
  - 20-30 (快速)
  - 30-50 (标准)
  - 50-100 (高质量)

CFG Scale:
  - 5-7 (创意)
  - 7-12 (标准)
  - 12-20 (严格遵循)
```
