---
name: doc-ocr
description: 文档 OCR 识别技能。扫描文件夹中的文档（PDF/图片），调用翔云 OCR API 识别文档信息。**重要：首次使用必须先配置翔云凭证，主动向用户索要 netocr_key 和 netocr_secret，或引导用户运行 --config 命令自行配置。**
---

# 文档 OCR 识别技能

批量识别文档。

## ⚠️ 首次使用必须配置凭证

**此技能需要翔云 OCR 服务，使用前必须先配置凭证！**

### 方式一：向用户提供凭证（推荐）

主动询问用户：
> "使用此技能需要翔云 netocr_key 和 netocr_secret，请提供这两个凭证。\
> 获取方式：翔云个人中心"

然后运行：
```bash
python scripts/recognize_doc.py --config
```

### 方式二：引导用户自行配置

告诉用户：
> "请先运行以下命令配置翔云凭证："
> ```bash
> python ~/.openclaw/skills/invoice-ocr/scripts/recognize_doc.py --config
> ```

## 特点

| 支持语言 | 代码 |
| :------- | :------- |
| 简体中文（印刷） | 0 |
| 简体中文（印刷+手写） | 3 |
| 繁体中文（印刷） | 1 |
| 繁体中文（印刷+手写） | 4 |
| 英文 | 2 |
| 阿拉伯 | 5 |
| 乌尔都 | 6 |
| 格鲁吉亚 | 7 |
| 西里尔文 | 8 |
| 法文 | 9 |
| 西班牙文 | 10 |
| 日文 | 11 |
| 韩文 | 12 |
| 葡萄牙文 | 13 |
| 越南 | 14 |
| 孟加拉 | 15 |

## 支持的文件格式

| 格式 | 扩展名 |
|------|--------|
| PDF | .pdf |
| OFD | .ofd |
| 图片 | .jpg, .jpeg, .png, .bmp , .tif, .tiff, .webp |


## 使用方法

### 识别文档

```bash
# 识别文件夹中的所有文档
python scripts/recognize_doc.py /path/to/doc

# 识别单文档
python scripts/recognize_doc.py /path/to/doc/123.png
```

### 配置管理

```bash
# 设置翔云凭证
python scripts/recognize_doc.py --config

# 查看当前配置
python scripts/recognize_doc.py --list-config
```

## 获取 netocr_key 和 netocr_secret

1. 登录[翔云](https://netocr.com)
2. 在个人中心获得

详细 API 说明见 [翔云 OCR API 参考](https://www.netocr.com/table.html)

## 工作流程

```
文档文件 → OCR识别 → 返回结果（输出原文不必翻译）
   ↓                    ↓
 PDF/图片             md结构
```

## 注意事项

1. 图片需清晰，建议长宽 > 500px
2. 单个文件不超过 10MB
3. 翔云 OCR 按次计费，注意费用控制
4. 配置文件保存在技能目录下的 config.json