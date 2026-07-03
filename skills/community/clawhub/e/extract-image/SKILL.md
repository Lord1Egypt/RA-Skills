---
name: 图像提取转换服务
description: MCP服务器提供从本地文件、URL提取图像并转换为base64格式的功能，适用于LLM分析。
version: 1.0.0
---

# 图像提取转换服务

MCP服务器提供从本地文件、URL提取图像并转换为base64格式的功能，适用于LLM分析。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Extract and analyze images from local file paths. Supports visual content understanding, OCR text extraction, and object recognition for screenshots, photos, diagrams, and documents. | `scripts.tools.extract_image_from_file` |
| Extract and analyze images from web URLs. Perfect for analyzing web screenshots, online photos, diagrams, or any image accessible via HTTP/HTTPS for visual content analysis and text extraction. | `scripts.tools.extract_image_from_url` |
| Extract and analyze images from base64-encoded data. Ideal for processing screenshots from clipboard, dynamically generated images, or images embedded in applications without requiring file system access. | `scripts.tools.extract_image_from_base64` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.extract_image_from_file
工具描述：Extract and analyze images from local file paths. Supports visual content understanding, OCR text extraction, and object recognition for screenshots, photos, diagrams, and documents.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|file_path|string|true| |Path to the image file to analyze (supports screenshots, photos, diagrams, and documents in PNG, JPG, GIF, WebP formats)|
|resize|boolean|false|true|For backward compatibility only. Images are always automatically resized to optimal dimensions (max 512x512) for LLM analysis|
|max_width|number|false|512.0|For backward compatibility only. Default maximum width is now 512px|
|max_height|number|false|512.0|For backward compatibility only. Default maximum height is now 512px|

---

## scripts.tools.extract_image_from_url
工具描述：Extract and analyze images from web URLs. Perfect for analyzing web screenshots, online photos, diagrams, or any image accessible via HTTP/HTTPS for visual content analysis and text extraction.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|url|string|true| |URL of the image to analyze for visual content, text extraction, or object recognition (supports web screenshots, photos, diagrams)|
|resize|boolean|false|true|For backward compatibility only. Images are always automatically resized to optimal dimensions (max 512x512) for LLM analysis|
|max_width|number|false|512.0|For backward compatibility only. Default maximum width is now 512px|
|max_height|number|false|512.0|For backward compatibility only. Default maximum height is now 512px|

---

## scripts.tools.extract_image_from_base64
工具描述：Extract and analyze images from base64-encoded data. Ideal for processing screenshots from clipboard, dynamically generated images, or images embedded in applications without requiring file system access.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|base64|string|true| |Base64-encoded image data to analyze (useful for screenshots, images from clipboard, or dynamically generated visuals)|
|mime_type|string|false|"image/png"|MIME type of the image (e.g., image/png, image/jpeg)|
|resize|boolean|false|true|For backward compatibility only. Images are always automatically resized to optimal dimensions (max 512x512) for LLM analysis|
|max_width|number|false|512.0|For backward compatibility only. Default maximum width is now 512px|
|max_height|number|false|512.0|For backward compatibility only. Default maximum height is now 512px|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据