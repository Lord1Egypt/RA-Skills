slug: cn-image-watermark
name: 图片水印工具
version: "1.0.0"
author: 千策

# 图片水印工具

为图片添加文字或图片水印，防止搬运。

## 核心功能
- **文字水印**：叠加文字（半透明、位置可调）
- **图片水印**：叠加Logo/小图标
- **批量处理**：对整个文件夹批量加水印
- **位置控制**：九宫格位置（9个锚点）
- **透明度**：0-100可调

## 使用场景
- 知识付费内容防搬运（水印"，禁止转载"）
- 社交媒体图片品牌标识
- 封面图添加版权信息
- 批量处理产品图片

## 输出格式
```json
{
  "input": "photo.jpg",
  "output": "photo_watermarked.jpg",
  "type": "text",
  "position": "右下",
  "status": "ok"
}
```

## 使用方式
```bash
# 文字水印
python ~/.qclaw/skills/cn-image-watermark/watermark.py text "photo.jpg" "©养虾记" --position bottom-right

# Logo水印
python ~/.qclaw/skills/cn-image-watermark/watermark.py image "photo.jpg" "logo.png" --position bottom-right --opacity 60

# 批量处理
python ~/.qclaw/skills/cn-image-watermark/watermark.py batch "./photos" "output" "©养虾记"
```

## 依赖
- Python3
- Pillow（PIL）：`pip3 install Pillow`

## 标签
cn, watermark, image, photo, protection

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
