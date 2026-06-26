---
name: avatar-generator
description: Professional avatar generator for social media and profiles. Use when user needs to create high-quality avatars for WeChat, QQ, Xiaohongshu, Twitter, Discord. Supports multiple styles: letter, geometric, gradient, abstract. Auto-export multi-platform sizes. 头像生成、头像制作、社交头像。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "👤", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install pillow"
---

# Avatar Generator

Professional avatar generator with 6 styles, multi-platform export, and customizable options.

## Features

- 🎨 **6 Avatar Styles**: Letter, Geometric, Gradient, Abstract, Pattern, Badge
- 📱 **Multi-Platform**: Auto-export for 9+ platforms
- 🎯 **Customizable**: Colors, shapes, sizes, fonts
- ⚡ **Fast Generation**: Local Pillow rendering
- 🌍 **Multi-Language**: Chinese and English support

## Supported Platforms

| Platform | Size | Shape | Priority |
|----------|------|-------|----------|
| WeChat | 640×640 | Square | ⭐⭐⭐⭐⭐ |
| QQ | 100×100 | Square | ⭐⭐⭐⭐⭐ |
| Xiaohongshu | 400×400 | Round | ⭐⭐⭐⭐ |
| Weibo | 200×200 | Round | ⭐⭐⭐⭐ |
| Twitter/X | 400×400 | Round | ⭐⭐⭐⭐ |
| Discord | 128×128 | Round | ⭐⭐⭐ |
| Reddit | 256×256 | Round | ⭐⭐⭐ |
| Facebook | 170×170 | Round | ⭐⭐⭐ |
| LinkedIn | 400×400 | Square | ⭐⭐⭐ |

## Avatar Styles

### 1. Letter Avatar (Initial Letter)
- Single letter or initials
- Clean background
- Professional look
- Best for: Business, professional

### 2. Geometric Avatar
- Abstract shapes
- Modern design
- Eye-catching
- Best for: Tech, creative

### 3. Gradient Avatar
- Smooth color transitions
- Trendy look
- Customizable
- Best for: Social media

### 4. Abstract Avatar
- Artistic patterns
- Unique design
- Stand out
- Best for: Creative, personal

### 5. Pattern Avatar
- Repeating elements
- Structured design
- Brand identity
- Best for: Teams, companies

### 6. Badge Avatar
- Circular frame
- Official look
- Identity badge
- Best for: Certification, ID

## Trigger Conditions

- "Generate avatar" / "生成头像"
- "Create WeChat avatar" / "做微信头像"
- "Make social media avatar" / "生成社交头像"
- "avatar-generator"

---

## Python Code

```python
from PIL import Image, ImageDraw, ImageFont
import os
import colorsys
import random

class AvatarGenerator:
    def __init__(self):
        self.platforms = {
            'wechat': {'size': (640, 640), 'shape': 'square'},
            'qq': {'size': (100, 100), 'shape': 'square'},
            'xiaohongshu': {'size': (400, 400), 'shape': 'round'},
            'weibo': {'size': (200, 200), 'shape': 'round'},
            'twitter': {'size': (400, 400), 'shape': 'round'},
            'discord': {'size': (128, 128), 'shape': 'round'},
            'reddit': {'size': (256, 256), 'shape': 'round'},
            'facebook': {'size': (170, 170), 'shape': 'round'},
            'linkedin': {'size': (400, 400), 'shape': 'square'},
        }
    
    def _load_font(self, size):
        """Load font with fallback"""
        paths = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except:
                    continue
        return ImageFont.load_default()
    
    def create_letter_avatar(self, letter, bg_color, text_color, size=(400, 400)):
        """Style 1: Letter avatar"""
        img = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(img)
        
        font = self._load_font(size[0] // 2)
        
        bbox = draw.textbbox((0, 0), letter, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = (size[0] - w) // 2, (size[1] - h) // 2
        
        draw.text((x, y), letter, font=font, fill=text_color)
        return img
    
    def create_geometric_avatar(self, colors, size=(400, 400)):
        """Style 2: Geometric avatar"""
        img = Image.new('RGB', size, colors[0])
        draw = ImageDraw.Draw(img)
        
        # Add geometric shapes
        center = size[0] // 2
        draw.ellipse([(50, 50), (size[0]-50, size[1]-50)], fill=colors[1])
        draw.regular_polygon((center, center, size[0]//3), 6, fill=colors[2])
        
        return img
    
    def create_gradient_avatar(self, color1, color2, size=(400, 400)):
        """Style 3: Gradient avatar"""
        import numpy as np
        
        img = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        for y in range(size[1]):
            ratio = y / size[1]
            r = int(color1[0] * (1-ratio) + color2[0] * ratio)
            g = int(color1[1] * (1-ratio) + color2[1] * ratio)
            b = int(color1[2] * (1-ratio) + color2[2] * ratio)
            img[y, :] = [r, g, b]
        
        return Image.fromarray(img)
    
    def create_abstract_avatar(self, seed, colors, size=(400, 400)):
        """Style 4: Abstract avatar"""
        random.seed(seed)
        img = Image.new('RGB', size, colors[0])
        draw = ImageDraw.Draw(img)
        
        for _ in range(10):
            x, y = random.randint(0, size[0]), random.randint(0, size[1])
            r = random.randint(20, 100)
            color = random.choice(colors[1:])
            draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=color)
        
        return img
    
    def create_pattern_avatar(self, pattern_type, colors, size=(400, 400)):
        """Style 5: Pattern avatar"""
        img = Image.new('RGB', size, colors[0])
        draw = ImageDraw.Draw(img)
        
        cell_size = 40
        for x in range(0, size[0], cell_size):
            for y in range(0, size[1], cell_size):
                if (x // cell_size + y // cell_size) % 2 == 0:
                    draw.rectangle([(x, y), (x+cell_size, y+cell_size)], fill=colors[1])
        
        return img
    
    def create_badge_avatar(self, text, bg_color, border_color, size=(400, 400)):
        """Style 6: Badge avatar"""
        img = Image.new('RGB', size, (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw circular badge
        margin = 20
        draw.ellipse([(margin, margin), (size[0]-margin, size[1]-margin)], 
                     fill=bg_color, outline=border_color, width=5)
        
        # Add text
        font = self._load_font(size[0] // 4)
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = (size[0] - w) // 2, (size[1] - h) // 2
        draw.text((x, y), text, font=font, fill='white')
        
        return img
    
    def make_round(self, img):
        """Make image circular"""
        size = img.size
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse([(0, 0), size], fill=255)
        
        result = Image.new('RGBA', size, (0, 0, 0, 0))
        result.paste(img, mask=mask)
        return result
    
    def export_multi_platform(self, img, output_dir, platforms=None):
        """Export for multiple platforms"""
        os.makedirs(output_dir, exist_ok=True)
        
        if platforms is None:
            platforms = list(self.platforms.keys())
        
        exported = []
        for platform in platforms:
            if platform in self.platforms:
                config = self.platforms[platform]
                resized = img.resize(config['size'], Image.LANCZOS)
                
                if config['shape'] == 'round':
                    resized = self.make_round(resized)
                
                path = os.path.join(output_dir, f'avatar_{platform}.png')
                resized.save(path)
                exported.append(path)
        
        return exported

# Example usage
gen = AvatarGenerator()

# Letter avatar
avatar1 = gen.create_letter_avatar('Z', (30, 60, 114), (255, 255, 255))

# Gradient avatar
avatar2 = gen.create_gradient_avatar((67, 142, 219), (30, 60, 114))

# Export to all platforms
gen.export_multi_platform(avatar1, 'output/')
```

---

## Usage Examples

```
User: "Generate a WeChat avatar with blue background and white Z"
Agent: Create 640×640 letter avatar

User: "Make a gradient avatar for Xiaohongshu"
Agent: Create 400×400 round gradient avatar

User: "Create social media avatars"
Agent: Generate avatars for all platforms
```

---

## Notes

- All avatars generated locally with Pillow
- No external API required
- Cross-platform compatible
- Supports Chinese and English text
