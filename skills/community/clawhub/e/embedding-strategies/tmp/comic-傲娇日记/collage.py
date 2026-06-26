from PIL import Image, ImageDraw
import os

# 9 格漫画不规则布局
panel_files = [
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel1.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel2.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel3.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel4.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel5.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel6.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel7.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel8.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel9.png",
]

# 加载所有图片
panels = []
for f in panel_files:
    if os.path.exists(f):
        img = Image.open(f)
        panels.append(img.resize((768, 768)))
        print(f"Loaded panel: {f}")
    else:
        print(f"Warning: File not found {f}")

if len(panels) < 9:
    print(f"Error: Only found {len(panels)} panels, need 9")
    exit(1)

# 创建画布（3 列×4 行）
canvas_width = 768 * 3
canvas_height = 768 * 4
canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
draw = ImageDraw.Draw(canvas)

# 布局配置 (x, y, width_multiplier, height_multiplier)
layout = [
    (0, 0, 1, 1),      # 1
    (1, 0, 1, 1),      # 2
    (2, 0, 1, 1),      # 3
    (0, 1, 1, 1),      # 4
    (1, 1, 2, 1),      # 5 (跨两列)
    (0, 2, 1, 1),      # 6
    (1, 2, 1, 1),      # 7
    (2, 2, 1, 1),      # 8
    (0, 3, 3, 1),      # 9 (跨三列)
]

# 粘贴图片
for i, (x, y, w_mult, h_mult) in enumerate(layout):
    if i < len(panels):
        x_pos = x * 768
        y_pos = y * 768
        w = 768 * w_mult
        h = 768 * h_mult
        panel = panels[i].resize((w, h))
        canvas.paste(panel, (x_pos, y_pos))
        # 画黑色边框
        draw.rectangle([x_pos, y_pos, x_pos+w, y_pos+h], outline='black', width=3)
        print(f"Pasted panel {i+1}: ({x_pos}, {y_pos}) size {w}x{h}")

# 保存
output_path = "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/final-comic.png"
canvas.save(output_path, 'PNG')
print(f"Comic collage completed: {output_path}")
print(f"MEDIA: {output_path}")
