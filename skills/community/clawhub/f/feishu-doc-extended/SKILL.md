---
name: feishu-doc-extended
description: 飞书文档扩展工具，提供图片下载和 OCR 识别功能。需要配合内置 feishu 插件使用。
homepage: https://open.feishu.cn
metadata:
  {
    "openclaw": {
      "emoji": "📄",
      "requires": {
        "bins": ["tesseract"],
        "plugins": ["feishu"]
      },
      "install": [
        {
          "id": "brew-tesseract",
          "kind": "brew",
          "formula": "tesseract",
          "bins": ["tesseract"],
          "label": "Install tesseract OCR"
        },
        {
          "id": "brew-tesseract-lang",
          "kind": "brew",
          "formula": "tesseract-lang",
          "label": "Install tesseract language data"
        }
      ]
    }
  }
---

# feishu-doc-extended

飞书文档扩展工具，提供图片下载和 OCR 识别功能。

## 功能

| 功能 | 说明 |
|------|------|
| **get_image** | 获取飞书文档中图片的下载 URL |
| **image_ocr** | 下载图片并进行 OCR 文字识别（需要 tesseract） |

## 依赖

- tesseract + 中文语言包（用于 OCR）
- 飞书开放平台应用权限
- OpenClaw 内置 feishu 插件

## 安装

```bash
# 安装 tesseract
brew install tesseract

# 安装中文语言包
brew install tesseract-lang
```

## 修改内置插件

本技能需要修改 OpenClaw 内置的 feishu 插件：

### 1. 修改 doc-schema.ts

文件路径: `/usr/local/lib/node_modules/openclaw/extensions/feishu/src/doc-schema.ts`

在 `FeishuDocSchema` 的 Union 类型末尾添加：

```typescript
// Image download
Type.Object({
  action: Type.Literal("get_image"),
  image_token: Type.String({ description: "Image token (from block image.token)" }),
}),
```

### 2. 修改 docx.ts

文件路径: `/usr/local/lib/node_modules/openclaw/extensions/feishu/src/docx.ts`

1. 在文件末尾（`uploadFileBlock` 函数后）添加：

```typescript
async function getImage(client: Lark.Client, imageToken: string) {
  const domain = client.domain ?? "https://open.feishu.cn";
  const token = await client.tokenManager.getTenantAccessToken();

  const res = await client.httpInstance.get<{ code?: number; data?: { image_url?: string } }>(
    `${domain}/open-apis/image/v4/get`,
    {
      params: { image_token: imageToken },
      headers: { Authorization: `Bearer ${token}` },
    },
  );

  if (res.data?.code !== 0 && res.data?.code !== undefined) {
    throw new Error(`Failed to get image: ${res.data}`);
  }

  return {
    image_url: res.data?.data?.image_url,
    image_token: imageToken,
  };
}
```

2. 在 switch 语句中添加 case：

```typescript
case "get_image":
  return json(await getImage(client, p.image_token));
```

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

## 使用方法

### 1. 获取文档中的图片 token

使用 `feishu_doc` 工具的 `list_blocks` 获取文档中的图片 block：

```json
{
  "action": "list_blocks",
  "doc_token": "文档Token"
}
```

从返回结果中获取图片的 token（在 `block.image.token` 中）。

### 2. 获取图片下载 URL

```json
{
  "action": "get_image",
  "image_token": "图片Token"
}
```

返回：
```json
{
  "image_url": "https://xxx...",
  "image_token": "图片Token"
}
```

### 3. OCR 识别

获取图片 URL 后，可以用浏览器打开并截图，然后用 tesseract 识别：

```bash
tesseract /path/to/screenshot.jpg - -l chi_sim
```

## 工作流程

```
1. feishu_doc list_blocks → 获取图片 block 和 token
2. feishu_doc get_image → 获取图片下载 URL
3. 浏览器访问 URL → 截图
4. tesseract OCR → 识别文字
```

## 注意事项

- `get_image` 返回的 URL 是飞书临时 URL，有时效性
- 如果 URL 过期，需要重新调用 `get_image`
- OCR 识别效果取决于图片清晰度

## 更新日志

- 2026-03-12: 初始版本，添加 get_image 功能
