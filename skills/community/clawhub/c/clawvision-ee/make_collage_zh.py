from PIL import Image, ImageDraw, ImageFont
import sys

presets = ['minimal','editorial','retro','luxury','playful']
base_dir = sys.argv[1] if len(sys.argv) > 1 else 'v107_zh_test'
images = []
for p in presets:
    path = f'{base_dir}/{p}/clawvision-迷你课程计划_tab1.png'
    images.append(Image.open(path))

w = images[0].width
h = images[0].height
collage = Image.new('RGB', (w * 5, h + 40), (255, 255, 255))
draw = ImageDraw.Draw(collage)
font = ImageFont.load_default()

x = 0
for i, img in enumerate(images):
    collage.paste(img, (x, 0))
    draw.text((x + 10, h + 10), presets[i], fill=(0, 0, 0), font=font)
    x += w

out = f'{base_dir}/clawvision_zh_presets_preview.png'
collage.save(out)
print(out)
