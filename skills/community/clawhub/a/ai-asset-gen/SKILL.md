---
name: ai-asset-gen
description: AI-powered game asset generation guide covering 2D sprites, tilemaps, UI elements, audio, music, and 3D models. Use when generating game assets with AI tools, optimizing prompts for game art, creating consistent art styles, or integrating AI assets into game engines. Includes prompt templates and tool recommendations.
---

# AI 游戏素材生成指南

## 概览

AI 工具可以加速游戏开发，但需要正确的提示词和后期处理。

### 推荐工具矩阵

| 素材类型 | 推荐工具 | 最佳用例 |
|---------|---------|---------|
| 2D 角色 | Midjourney, Stable Diffusion | 角色立绘、怪物设计 |
| 像素画 | PixelLab, Aseprite + AI | 像素角色、物品图标 |
| UI 元素 | DALL-E 3, Midjourney | 按钮、图标、边框 |
| 瓷砖地图 | TileGen, 自定义 SD | 地板、墙壁纹理 |
| 背景图 | Midjourney, Stable Diffusion | 场景背景、天空盒 |
| 音效 | ElevenLabs, Suno | 环境音、UI 音效 |
| 音乐 | Suno, Udio | 背景音乐、战斗曲 |
| 3D 模型 | Meshy, Luma AI | 简单道具、建筑 |

## 2D 角色生成

### Midjourney 提示词模板
```
游戏角色生成公式:
[角色类型] + [风格] + [动作/姿势] + [视角] + [背景] + [技术参数]

示例:
"a fantasy warrior character, pixel art style, idle stance, 
front view, transparent background, game sprite sheet, 
16-bit retro game style, detailed armor --ar 1:1 --v 6"
```

### 风格关键词
```yaml
像素艺术:
  - pixel art, 16-bit, 8-bit, retro game style
  - nes style, snes style, gameboy style
  - limited color palette

手绘风格:
  - hand drawn, watercolor, sketch style
  - cartoon, anime, chibi
  - outline, cel shaded

写实风格:
  - realistic, detailed, high quality
  - fantasy art, digital painting
  - concept art, illustration
```

### 角色类型提示词
```yaml
战士:
  "fantasy warrior, heavy armor, sword and shield, 
   battle-worn, heroic pose, game character design"

法师:
  "arcane wizard, flowing robes, glowing staff, 
   magical effects, mystical aura, fantasy rpg"

盗贼:
  "rogue assassin, dark leather armor, daggers, 
   hooded cloak, stealthy pose, shadow effects"

怪物:
  "fantasy monster, [monster type], fearsome, 
   dark dungeon style, creature design, game enemy"
```

### 一致性技巧
```
方法1: 使用相同的 seed
"fantasy warrior --seed 12345 --v 6"

方法2: 使用图像作为参考
"fantasy warrior --iw 2 --ref [image_url]"

方法3: 创建角色设定表
"character sheet of fantasy warrior, 
 multiple poses, expressions, turn around"
```

## 瓷砖地图生成

### 地板瓷砖
```
提示词模板:
"[theme] floor tile, seamless texture, top-down view, 
 game asset, 32x32 pixels, tileable pattern"

示例:
"dungeon stone floor tile, seamless texture, 
 top-down view, game asset, 32x32, cobblestone pattern"

"grass field tile, rpg maker style, top-down, 
 seamless, game texture, 16-bit pixel art"
```

### 墙壁瓷砖
```
"dungeon wall tile, side view, game asset, 
 stone brick texture, 32x32, tileable"

"castle interior wall, medieval style, 
 top-down rpg, seamless pattern"
```

### 主题关键词
```yaml
地牢: dungeon, dark, stone, torch, moss, cobweb
森林: forest, grass, dirt path, leaves, roots
沙漠: desert, sand, dunes, cactus, ruins
雪地: snow, ice, frozen, winter, blizzard
城堡: castle, stone, elegant, flags, banners
```

## UI 元素生成

### 按钮设计
```
提示词模板:
"[style] game button, [shape], [state], 
 UI element, game interface, clean design"

示例:
"fantasy rpg button, rectangular, golden border, 
 normal state, game UI, medieval style, clean design"

"sci-fi game button, rounded corners, neon glow, 
 hover state, futuristic interface, holographic"
```

### 图标设计
```
"game icon, [item name], simple design, 
 readable, 64x64 pixels, transparent background"

示例:
"game icon, health potion, red vial, 
 simple design, 64x64, pixel art, transparent bg"

"game icon, gold coin, shiny, rpg style, 
 32x32, clean edges, transparent background"
```

### UI 边框
```
"fantasy UI frame, ornate border, 
 game interface, gold decorations, medieval"

"sci-fi HUD frame, holographic border, 
 futuristic, glowing edges, game UI"
```

## 音频生成

### 音效 (ElevenLabs / Suno)
```yaml
攻击音效:
  "sword slash sound effect, sharp, quick, 
   fantasy game, 1 second"

魔法音效:
  "magical spell cast, whoosh, sparkle, 
   fantasy rpg, ethereal, 2 seconds"

环境音:
  "dungeon ambience, dripping water, 
   distant echoes, creepy, loopable"

UI 音效:
  "button click sound, satisfying, 
   game menu, short, clean"
```

### 背景音乐 (Suno / Udio)
```yaml
探索音乐:
  "peaceful exploration music, fantasy village, 
   acoustic guitar, flute, relaxing, loopable, 2 minutes"

战斗音乐:
  "epic battle music, fast tempo, 
   orchestral, intense, fantasy combat, loopable"

Boss 战:
  "intense boss battle theme, dramatic, 
   choir, heavy drums, dark fantasy, epic"

标题画面:
  "main menu theme, memorable melody, 
   orchestral, fantasy adventure, grand"
```

### 音乐提示词技巧
```
结构: [情绪] + [风格] + [乐器] + [速度] + [长度]

示例:
"melancholic fantasy music, celtic style, 
 harp and violin, slow tempo, 3 minutes, loopable"

"energetic combat music, metal style, 
 electric guitar, fast tempo, 2 minutes"
```

## 3D 模型生成

### Meshy.ai 提示词
```
"low poly fantasy sword, game ready, 
 simple geometry, stylized"

"medieval treasure chest, game prop, 
 stylized, optimized mesh"
```

### 模型优化
```yaml
多边形数:
  移动端: < 10,000 tris
  PC 独立游戏: < 50,000 tris
  AAA: > 100,000 tris

纹理分辨率:
  移动端: 512x512 - 1024x1024
  PC: 1024x1024 - 4096x4096
```

## 后期处理工作流

### 精灵图处理
```bash
# 1. 移除背景 (rembg)
rembg i input.png output.png

# 2. 调整尺寸 (ImageMagick)
convert sprite.png -resize 32x32 sprite_32.png

# 3. 批量处理
for f in *.png; do
  rembg i "$f" "cleaned_$f"
  convert "cleaned_$f" -resize 64x64 "final_$f"
done
```

### 瓷砖无缝化
```python
# Python: 使瓷砖无缝
from PIL import Image
import numpy as np

def make_tileable(img_path, output_path):
    img = Image.open(img_path)
    arr = np.array(img)
    
    # 边缘渐变混合
    width = arr.shape[1]
    for x in range(width):
        blend = x / width
        arr[:, x] = arr[:, x] * blend + arr[:, (x + width//2) % width] * (1 - blend)
    
    result = Image.fromarray(arr)
    result.save(output_path)
```

### 调色板统一
```python
# 统一所有精灵的颜色调色板
from PIL import Image
import glob

def normalize_palette(directory, reference_img):
    ref = Image.open(reference_img)
    ref_palette = ref.getpalette()
    
    for img_path in glob.glob(f"{directory}/*.png"):
        img = Image.open(img_path).convert('P', palette=Image.ADAPTIVE)
        img.putpalette(ref_palette)
        img.save(img_path)
```

## Godot 集成

### 导入设置
```yaml
精灵图:
  - Filter: Nearest (像素艺术) / Linear (高清)
  - Repeat: Disabled
  - Mipmaps: Disabled (2D)

瓷砖集:
  - 创建 TileSet 资源
  - 设置 Tile Size: 32x32 或 64x64
  - 配置碰撞形状

音频:
  - BGM: Stream, Loop: On
  - SFX: Stream, Loop: Off
```

### 自动化脚本
```csharp
// Godot C#: 批量导入精灵
public void ImportSprites(string path)
{
    var dir = DirAccess.Open(path);
    if (dir == null) return;
    
    dir.ListDirBegin();
    string fileName = dir.GetNext();
    
    while (fileName != "")
    {
        if (fileName.EndsWith(".png"))
        {
            var texture = GD.Load<Texture2D>($"{path}/{fileName}");
            // 处理纹理...
        }
        fileName = dir.GetNext();
    }
}
```

## 提示词库

### 完整示例
```
角色立绘:
"fantasy female elf ranger character, green cloak, 
 bow and arrow, forest background, anime style, 
 game character design, detailed, full body, 
 transparent background --ar 3:4 --v 6"

怪物设计:
"fantasy dragon boss, fierce, scales, wings, 
 dark cave environment, concept art, 
 game enemy design, multiple views --ar 16:9 --v 6"

道具图标:
"health potion icon, red glowing vial, 
 fantasy rpg item, game UI, 64x64 pixels, 
 transparent background, clean design --ar 1:1"

背景场景:
"mystical forest background, ancient trees, 
 magical particles, fantasy rpg, 
 game background art, detailed --ar 16:9 --v 6"
```

## 参考资源

- **提示词库**: [references/prompt-library.md](references/prompt-library.md)
- **工具对比**: [references/tool-comparison.md](references/tool-comparison.md)
- **工作流模板**: [references/workflows.md](references/workflows.md)
