---
name: china-id-photo
description: 生成中国标准证件照。Use when the user needs to create an ID photo, passport photo, visa photo, or any standard photo with specific size and background color. Supports 1-inch, 2-inch, passport, and custom sizes with white/blue/red backgrounds. Outputs JPEG or PNG. Uses OpenCV for face detection.
version: 1.2.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📷", "requires": {"bins": ["python3"]}, "primaryEnv": ""}}
---

# 中国证件照生成 China ID Photo

将个人照片转换为符合中国标准的证件照，支持多种尺寸和背景颜色。

## 功能特点

- 🎨 支持白/蓝/红三种标准背景色
- 📐 支持1寸、2寸、护照等标准尺寸
- 🖼️ 输出JPEG（默认）或PNG格式
- 🔒 完全本地处理，不上传任何服务器

## 触发时机

- "帮我做一张证件照"
- "把这张照片转成1寸证件照"
- "我需要蓝色背景的2寸照片"
- "生成护照照片，白色背景"
- "这张照片转成证件照，要红色背景"
- "帮我制作身份证照片"

---

## Step 0：环境检查与依赖安装

```bash
# 检查 python3
if ! command -v python3 &> /dev/null; then
  echo "❌ 需要 python3"
  echo "  macOS:  brew install python3"
  echo "  Ubuntu: sudo apt install python3"
  echo "  Windows: 从 python.org 下载安装"
  exit 1
fi

# 检查并安装依赖
echo "📦 检查依赖..."
pip install rembg pillow opencv-python-headless -q 2>/dev/null || {
  echo "❌ 依赖安装失败，请手动执行："
  echo "  pip install rembg pillow opencv-python-headless"
  exit 1
}

echo "✅ 环境检查通过"
```

---

## Step 1：识别用户需求

```
用户提供照片路径 → 识别参数：

尺寸（用户指定或默认1寸）：
  "1寸" / "一寸" / "小一寸"     → 295×413 像素
  "2寸" / "二寸"                → 413×579 像素
  "小二寸" / "护照" / "passport" → 390×567 像素
  "大一寸" / "签证" / "visa"     → 390×567 像素
  "身份证" / "id card"          → 358×441 像素
  未指定                        → 默认1寸（295×413）

背景色（用户指定或默认白色）：
  "白色" / "白底" / "white"     → #FFFFFF
  "蓝色" / "蓝底" / "blue"      → #438EDB（标准证件照蓝）
  "红色" / "红底" / "red"       → #FF0000
  未指定                        → 默认白色

输出格式：
  "PNG" / "png" / "透明"        → PNG格式
  未指定                        → 默认JPEG格式
```

---

## Step 2：生成证件照

```bash
# 设置参数（根据用户需求调整）
INPUT_IMAGE="/path/to/user/photo.jpg"
SIZE="1"           # 尺寸：1/2/passport/id_card
BG_COLOR="white"   # 背景色：white/blue/red
OUTPUT_FORMAT="jpg" # 输出格式：jpg/png

# 创建输出目录
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/id_photo_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# 执行Python脚本处理图片
python3 - "$INPUT_IMAGE" "$OUTPUT_DIR" "$SIZE" "$BG_COLOR" "$OUTPUT_FORMAT" << 'PYEOF'
import sys
import os
from rembg import remove
from PIL import Image, ImageFilter
import cv2
import numpy as np

# 从命令行参数获取配置
input_path = sys.argv[1]
output_dir = sys.argv[2]
size_type = sys.argv[3]
bg_color_name = sys.argv[4]
output_format = sys.argv[5]

# 标准尺寸映射（像素，300DPI）
SIZES = {
    '1': (295, 413),        # 1寸
    '2': (413, 579),        # 2寸
    'passport': (390, 567), # 护照/小二寸
    'id_card': (358, 441),  # 身份证
}

# 背景色映射（RGB）- 中国证件照标准色值
BG_COLORS = {
    'white': (255, 255, 255),   # 白色：身份证、护照、签证
    'blue': (67, 142, 219),     # 蓝色：毕业证、工作证
    'red': (255, 0, 0),         # 红色：结婚证、党员证
}

def detect_face(img_array):
    """使用OpenCV检测人脸，返回包含头发的头部边界框"""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    if len(faces) > 0:
        # 返回最大的人脸
        areas = [w * h for (x, y, w, h) in faces]
        max_idx = areas.index(max(areas))
        fx, fy, fw, fh = faces[max_idx]
        
        # 扩展边界框以包含头发
        # 向上扩展约40%（头发区域）
        # 向下扩展约10%（下巴下方）
        # 向左右各扩展约10%
        expand_top = int(fh * 0.4)
        expand_bottom = int(fh * 0.1)
        expand_side = int(fw * 0.1)
        
        # 计算扩展后的边界框（确保不超出图片边界）
        img_h, img_w = gray.shape
        new_x = max(0, fx - expand_side)
        new_y = max(0, fy - expand_top)
        new_w = min(fw + expand_side * 2, img_w - new_x)
        new_h = min(fh + expand_top + expand_bottom, img_h - new_y)
        
        return (new_x, new_y, new_w, new_h)
    
    return None

def refine_mask(mask, radius=2):
    """优化抠图边缘，去除锯齿"""
    # 转换为numpy数组
    mask_np = np.array(mask)
    
    # 轻微模糊边缘
    mask_np = cv2.GaussianBlur(mask_np, (radius*2+1, radius*2+1), 0)
    
    # 二值化
    _, mask_np = cv2.threshold(mask_np, 128, 255, cv2.THRESH_BINARY)
    
    return Image.fromarray(mask_np)

def crop_face_centered(img, target_size, face_bbox=None):
    """根据头部位置进行智能裁剪，确保头顶留白符合证件照标准
    
    标准要求：
    - 头顶到照片上边沿：约10%照片高度
    - 头部高度：约65%照片高度
    - 头部水平居中
    """
    target_w, target_h = target_size
    target_ratio = target_w / target_h
    img_w, img_h = img.size
    
    if face_bbox is not None:
        fx, fy, fw, fh = face_bbox
        
        # 计算头部中心（水平位置）
        head_cx = fx + fw // 2
        
        # 根据中国证件照标准计算裁剪区域
        # 头部高度应占照片高度的65%
        # 头顶留白占照片高度的10%
        
        # 假设face_bbox已经是扩展后的头部区域
        # 头部高度 fh 对应照片高度的 65%
        target_area_h = int(fh / 0.65)
        target_area_w = int(target_area_h * target_ratio)
        
        # 确保不超出图片
        target_area_w = min(target_area_w, img_w)
        target_area_h = min(target_area_h, img_h)
        
        # 水平居中
        crop_x = head_cx - target_area_w // 2
        
        # 垂直位置：头顶留10%空白
        # face_bbox的y坐标是头顶位置
        # 头顶到裁剪区域顶部的距离 = 照片高度 * 10%
        head_top_offset = int(target_area_h * 0.10)
        crop_y = fy - head_top_offset
        
        # 边界调整
        crop_x = max(0, min(crop_x, img_w - target_area_w))
        crop_y = max(0, min(crop_y, img_h - target_area_h))
        
        img = img.crop((crop_x, crop_y, crop_x + target_area_w, crop_y + target_area_h))
    else:
        # 没有检测到人脸，使用改进的居中裁剪
        img_ratio = img_w / img_h
        if img_ratio > target_ratio:
            new_w = int(img_h * target_ratio)
            left = (img_w - new_w) // 2
            img = img.crop((left, 0, left + new_w, img_h))
        else:
            new_h = int(img_w / target_ratio)
            top = int((img_h - new_h) * 0.15)  # 上方留15%空白
            img = img.crop((0, top, img_w, top + new_h))
    
    # 缩放到目标尺寸（使用高质量缩放）
    return img.resize(target_size, Image.LANCZOS)

def process_image(input_path, output_dir, size_type, bg_color_name, output_format):
    print(f"📸 正在处理图片...")
    
    if not os.path.exists(input_path):
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)
    
    # 读取原图
    input_img = Image.open(input_path).convert('RGB')
    orig_size = input_img.size
    print(f"   原图尺寸: {orig_size}")
    
    # 检测人脸位置（在抠图前检测）
    print("👤 检测人脸...")
    img_array = np.array(input_img)
    face_bbox = detect_face(img_array)
    
    if face_bbox is not None:
        fx, fy, fw, fh = face_bbox
        print(f"   检测到人脸: 位置({fx},{fy}) 大小({fw}x{fh})")
    else:
        print("   ⚠️ 未检测到人脸，将使用智能居中裁剪")
    
    # 抠图（移除背景）
    print("✂️ 正在抠图（可能需要几秒）...")
    output_img = remove(input_img)
    
    # 获取目标尺寸
    if size_type in SIZES:
        target_size = SIZES[size_type]
        size_name = {'1': '1寸', '2': '2寸', 'passport': '护照', 'id_card': '身份证'}[size_type]
    else:
        target_size = (295, 413)
        size_name = '1寸（默认）'
    
    print(f"📐 目标尺寸: {size_name} {target_size[0]}x{target_size[1]} 像素")
    
    # 获取背景色
    bg_color = BG_COLORS.get(bg_color_name, BG_COLORS['white'])
    print(f"🎨 背景色: {bg_color_name} RGB{bg_color}")
    
    # 提取并优化alpha通道（抠图边缘）
    if output_img.mode != 'RGBA':
        print("❌ 抠图失败，未生成透明通道")
        sys.exit(1)
    
    r, g, b, a = output_img.split()
    print("🔧 优化抠图边缘...")
    a_refined = refine_mask(a, radius=2)
    
    # 创建纯色背景
    bg = Image.new('RGB', output_img.size, bg_color)
    
    # 将抠图结果粘贴到背景上（使用优化后的mask）
    person_rgb = Image.merge('RGB', (r, g, b))
    bg.paste(person_rgb, mask=a_refined)
    
    # 智能裁剪（根据人脸位置）
    print("✂️ 裁剪到目标尺寸...")
    result = crop_face_centered(bg, target_size, face_bbox)
    
    # 验证输出尺寸
    if result.size != target_size:
        print(f"⚠️ 尺寸调整: {result.size} → {target_size}")
        result = result.resize(target_size, Image.LANCZOS)
    
    # 保存
    output_ext = 'png' if output_format == 'png' else 'jpg'
    output_path = os.path.join(output_dir, f'id_photo_{size_type}_{bg_color_name}.{output_ext}')
    
    if output_ext == 'png':
        result.save(output_path, 'PNG')
    else:
        result.save(output_path, 'JPEG', quality=95, subsampling=0)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ 证件照已生成: {output_path}")
    print(f"   最终尺寸: {result.size[0]}x{result.size[1]} 像素")
    print(f"   文件大小: {file_size / 1024:.1f} KB")
    
    return output_path

try:
    result = process_image(input_path, output_dir, size_type, bg_color_name, output_format)
    print("\n🎉 处理完成！")
except Exception as e:
    print(f"\n❌ 处理失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF
```

### 设置环境变量并执行

```bash
export INPUT_IMAGE="/path/to/user/photo.jpg"
export OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/id_photo_$(date +%Y%m%d_%H%M%S)"
export SIZE="1"          # 1/2/passport/id_card
export BG_COLOR="white"  # white/blue/red
export OUTPUT_FORMAT="jpg"  # jpg/png

# 执行上面的python脚本
```

---

## Step 3：输出结果

证件照生成完成后：

```
✅ 证件照已生成！

📐 尺寸：1寸（295×413像素，2.5×3.5厘米）
🎨 背景：白色
📁 格式：JPEG
📍 位置：/path/to/id_photo_xxx/id_photo_1_white.jpg

可直接用于：
- 简历、报名表
- 各类证件申请
- 在线提交
```

---

## 常用尺寸速查

| 名称 | 像素 | 厘米 | 常用场景 |
|------|------|------|----------|
| 1寸 | 295×413 | 2.5×3.5 | 简历、报名表 |
| 2寸 | 413×579 | 3.5×5.0 | 毕业证、资格证 |
| 护照/小二寸 | 390×567 | 3.3×4.8 | 护照、签证 |
| 身份证 | 358×441 | 2.6×3.2 | 身份证办理 |

---

## 错误处理

```
文件不存在           → 提示用户确认照片路径
格式不支持           → 提示支持的格式：JPG, PNG, WEBP
依赖安装失败         → 提示手动安装：pip install rembg pillow
内存不足             → 建议压缩原图后再试
抠图效果不佳         → 建议使用背景简洁的正面照
```

---

## 注意事项

- 首次运行需下载rembg模型（约170MB），请保持网络连接
- 建议使用正面免冠照片，背景简洁效果更佳
- 原图分辨率建议 >= 500×500 像素
- 处理时间约2-10秒（取决于CPU性能）
- 所有处理完全在本地进行，不会上传任何数据
