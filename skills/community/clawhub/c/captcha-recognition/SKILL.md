---
name: captcha-recognition
version: 1.0.0
description: Recognizes CAPTCHA images using ddddocr library. Invoke when user needs to recognize/decode CAPTCHA images or mentions captcha verification.
author: Moxin1044
triggers:
    - "OCR"
    - "captcha recognition"
    - "captcha verification"
    - "captcha decode"
---

# CAPTCHA Recognition Skill

基于 [ddddocr](https://github.com/sml2h3/ddddocr) 的验证码识别技能，提供简单易用的验证码识别功能。

## When to Use This Skill

当用户有以下请求时，应该激活此技能：

- **识别验证码图片**：
  - "帮我识别这个验证码"
  - "这个验证码是什么"
  - "帮我破解这个验证码图片"
  - "识别这张图片中的验证码"

- **网络验证码识别**：
  - "识别这个 URL 的验证码：http://example.com/captcha.png"
  - "帮我识别网页上的验证码图片"
  - 用户提供了 HTTP/HTTPS 链接的验证码图片

- **OCR 相关请求**：
  - "OCR 识别这个图片"
  - "提取图片中的文字"
  - "图片文字识别"

- **验证码验证场景**：
  - 用户发送了验证码图片并询问内容
  - 需要自动识别网页/应用中的验证码

## 依赖安装

```bash
pip install ddddocr opencv-python numpy Pillow requests
```

## 支持的图片输入格式

本技能支持多种验证码图片输入方式：

| 格式 | 示例 | 说明 |
|------|------|------|
| 本地文件路径 | `captcha.jpg` | 本地存储的验证码图片 |
| HTTP/HTTPS URL | `http://example.com/captcha.png` | 网络上的验证码图片 |
| Blob URL | `blob:https://example.com/...` | 浏览器 Blob URL（需特殊处理） |
| 字节数据 | `bytes` | 图片的二进制数据 |
| PIL Image | `PIL.Image.Image` | PIL Image 对象 |

### 关于 Blob URL

Blob URL（如 `blob:https://example.com/xxx`）是浏览器内部创建的临时 URL，无法从服务器端直接访问。如果用户提供 Blob URL，需要：

1. 在浏览器中右键保存图片到本地
2. 或者使用浏览器开发者工具获取实际的图片 URL
3. 或者将图片下载后提供本地路径

## 命令行使用

```bash
python scripts/captcha.py <image_path_or_url> [--preprocess]
```

参数说明:

- `image_path_or_url`: 验证码图片路径或网络 URL（必需）
- `--preprocess`: 可选，启用图像预处理（灰度化、二值化）

示例:

```bash
# 本地文件
python scripts/captcha.py captcha.jpg
python scripts/captcha.py captcha.jpg --preprocess

# 网络 URL
python scripts/captcha.py http://example.com/captcha.png
python scripts/captcha.py https://example.com/captcha.jpg --preprocess
```

## Python API 使用

（注意：如果想要更快速和节省Token，你应该优先使用命令行的方式！）

### 快速开始

```python
from scripts.captcha import recognize_captcha

# 方法1: 从文件路径识别（最常用）
result = recognize_captcha("path/to/captcha.jpg")
print(f"验证码内容: {result}")

# 方法2: 从网络 URL 识别
result = recognize_captcha("http://example.com/captcha.png")
print(f"验证码内容: {result}")

result = recognize_captcha("https://example.com/captcha.jpg")
print(f"验证码内容: {result}")

# 方法3: 从字节数据识别
with open("captcha.jpg", "rb") as f:
    image_bytes = f.read()
result = recognize_captcha(image_bytes)

# 方法4: 从 PIL Image 对象识别
from PIL import Image
pil_image = Image.open("captcha.jpg")
result = recognize_captcha(pil_image)
```

### 启用图像预处理

对于质量较差或有干扰线的验证码，可以启用预处理：

```python
# preprocess=True 会进行灰度化和二值化处理
result = recognize_captcha("captcha.jpg", preprocess=True)
```

## API Reference

### `recognize_captcha(image, preprocess=False, show_ad=False, timeout=10)`

主要识别函数，支持多种输入格式。

**参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | `str` / `bytes` / `PIL.Image.Image` | 是 | 验证码图片，可以是文件路径、网络 URL、字节数据或 PIL Image 对象 |
| `preprocess` | `bool` | 否 | 是否启用图像预处理（灰度化、二值化），默认 `False` |
| `show_ad` | `bool` | 否 | 是否显示 ddddocr 广告，默认 `False` |
| `timeout` | `int` | 否 | 网络 URL 请求超时时间（秒），默认 `10` |

**返回值：**

- `str`: 识别出的验证码文本

**异常：**

- `FileNotFoundError`: 图片文件不存在
- `ValueError`: 不支持的 URL 格式（如 Blob URL）
- `RuntimeError`: 网络请求失败或图像处理失败
- `TypeError`: 不支持的图片类型
- `ImportError`: 缺少必要的依赖库

### `CaptchaRecognizer` 类

如需更细粒度的控制，可以直接使用类：

```python
from scripts.captcha import CaptchaRecognizer

recognizer = CaptchaRecognizer(show_ad=False)

# 从文件识别
result = recognizer.recognize_from_file("captcha.jpg", preprocess=False)

# 从网络 URL 识别
result = recognizer.recognize_from_url("http://example.com/captcha.png", preprocess=False)

# 从字节识别
with open("captcha.jpg", "rb") as f:
    result = recognizer.recognize_from_bytes(f.read())

# 从 PIL Image 识别
from PIL import Image
img = Image.open("captcha.jpg")
result = recognizer.recognize_from_pil(img)
```

## 最佳实践

1. **优先使用文件路径**：如果图片已保存为文件，直接传递路径字符串最简单
2. **网络 URL 识别**：支持 HTTP/HTTPS URL，会自动下载并识别验证码
3. **预处理建议**：对于背景复杂、有干扰线或颜色较多的验证码，尝试 `preprocess=True`
4. **错误处理**：建议捕获 `FileNotFoundError`、`ValueError` 和 `TypeError` 提供友好的错误提示
5. **性能优化**：`recognize_captcha()` 使用单例模式，重复调用不会重复加载 OCR 模型
6. **超时设置**：对于网络 URL，可以通过 `timeout` 参数调整请求超时时间

## 完整示例

```python
from scripts.captcha import recognize_captcha

def solve_captcha(image_source):
    """识别验证码并处理可能的错误"""
    try:
        # 先尝试不预处理
        result = recognize_captcha(image_source)
        
        # 如果结果为空或不合理，尝试预处理
        if not result or len(result) < 2:
            result = recognize_captcha(image_source, preprocess=True)
        
        return result
        
    except FileNotFoundError:
        return "错误：找不到图片文件"
    except ValueError as e:
        return f"错误：{e}"
    except ImportError as e:
        return f"错误：缺少依赖库 - {e}"
    except Exception as e:
        return f"错误：识别失败 - {e}"

# 使用本地文件
result = solve_captcha("captcha.jpg")
print(f"识别结果: {result}")

# 使用网络 URL
result = solve_captcha("http://example.com/captcha.png")
print(f"识别结果: {result}")
```
