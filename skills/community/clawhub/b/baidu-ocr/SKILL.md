---
name: baidu-ocr
description: 百度 OCR 文字识别。支持中英文混合、公式、表格识别，准确率 95%+。使用百度 AI 开放平台 API。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["python3"], "env": ["BAIDU_API_KEY", "BAIDU_SECRET_KEY"] },
        "primaryEnv": "BAIDU_API_KEY",
      },
  }
---

# 百度 OCR

使用百度 AI 开放平台进行高精度文字识别。

## 特点

- ✅ 中英文混合识别
- ✅ 准确率 95%+
- ✅ 支持公式识别
- ✅ 支持表格识别
- ✅ 每天 500 次免费额度

## 快速开始

```bash
python3 {baseDir}/baidu_ocr.py /path/to/image.jpg
```

## 使用方法

```bash
python3 {baseDir}/baidu_ocr.py <图片路径> [输出格式]
```

**参数**:
- `<图片路径>`: 本地图片文件（jpg, png, bmp 等）
- `[输出格式]`: 可选，`text`（默认）或 `json`

## 示例

```bash
# 基础识别
python3 {baseDir}/baidu_ocr.py image.jpg

# JSON 格式输出
python3 {baseDir}/baidu_ocr.py image.jpg json

# 批量处理
for file in *.jpg; do
    python3 {baseDir}/baidu_ocr.py "$file"
done
```

## API 配置

在 `~/.openclaw-env` 中配置：

```bash
export BAIDU_API_KEY="your_api_key"
export BAIDU_SECRET_KEY="your_secret_key"
```

或者在 `~/.openclaw/openclaw.json` 中配置：

```json5
{
  skills: {
    "baidu-ocr": {
      apiKey: "YOUR_API_KEY",
      secretKey: "YOUR_SECRET_KEY"
    }
  }
}
```

## 支持的图片格式

- JPG/JPEG
- PNG
- BMP
- WEBP
- GIF

## 识别类型

| 类型 | 说明 | API |
|------|------|-----|
| 通用文字 | 中英文混合识别 | `general_basic` |
| 高精度 | 含位置信息 | `general` |
| 表格 | 表格结构识别 | `table` |
| 公式 | 数学公式识别 | `formula` |

## 免费额度

- **通用文字识别**: 每天 500 次
- **高精度版**: 每天 50 次
- **表格识别**: 每月 500 次
- **公式识别**: 每月 500 次

## 错误处理

| 错误码 | 说明 | 解决方法 |
|--------|------|----------|
| 110 | Access Token 无效 | 重新获取 Token |
| 111 | Access Token 过期 | 重新获取 Token |
| 216100 | 认证失败 | 检查 API Key |
| 216101 | 授权失败 | 检查 Secret Key |

## 相关文档

- [百度 OCR 官方文档](https://ai.baidu.com/ai-doc/OCR/Ek3h7xypm)
- [API 调用说明](https://ai.baidu.com/ai-doc/REFERENCE/Wk3h7x8bv)

---

*版本：1.0.0 | 更新时间：2026-03-07*
