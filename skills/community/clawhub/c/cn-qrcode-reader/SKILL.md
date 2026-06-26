slug: cn-qrcode-reader
name: 二维码识别器
version: "1.0.0"
author: 千策

# 二维码识别器


识别图片中的二维码和条形码，支持摄像头和文件输入。

## 功能

- 识别图片中的二维码
- 识别条形码（EAN-13, Code-128等）
- 支持URL、文本、联系方式等多种格式

## 使用方法

```bash
# 识别图片文件
python3 cn_qrcode_reader.py qrcode.png
python3 cn_qrcode_reader.py barcode.jpg

# 识别多个文件
python3 cn_qrcode_reader.py *.png

# 显示详细信息
python3 cn_qrcode_reader.py qrcode.png --verbose
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `image` | 图片路径（支持glob） | 必填 |
| `--verbose` | 显示详细信息 | False |
| `--save` | 保存结果到文件 | False |

## 依赖

- Python 3.x
- Pillow (pip install Pillow)
- pyzbar (pip install pyzbar)
  - macOS: `brew install zbar`
  - Ubuntu: `sudo apt-get install libzbar0`

## 示例

```bash
# 识别单个二维码
python3 cn_qrcode_reader.py test.png

# 批量识别
python3 cn_qrcode_reader.py "*.png"
```

## 注意事项

- 需要安装zbar库
- 支持PNG、JPG、BMP等常见图片格式
- 条形码识别依赖pyzbar库

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
