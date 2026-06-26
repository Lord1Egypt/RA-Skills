# feishu-doc-extended

飞书文档扩展工具包，提供图片下载和 OCR 识别功能。

## 文件说明

```
feishu-doc-extended/
├── SKILL.md              # 技能定义文件
├── README.md             # 使用说明
├── src/
│   ├── doc-schema.ts     # 修改的 schema（新增 get_image）
│   └── docx.ts          # 修改的实现（新增 getImage 函数）
├── references/
│   └── CHANGELOG.md     # 更新日志
└── scripts/
    └── image-ocr.sh     # OCR 识别脚本（可选）
```

## 安装步骤

### 1. 安装依赖

```bash
# 安装 tesseract OCR
brew install tesseract
brew install tesseract-lang
```

### 2. 修改飞书插件

本技能需要修改 OpenClaw 内置的 feishu 插件：

**修改文件 1**: `/usr/local/lib/node_modules/openclaw/extensions/feishu/src/doc-schema.ts`

在 `FeishuDocSchema` 的 Union 类型末尾添加：

```typescript
// Image download
Type.Object({
  action: Type.Literal("get_image"),
  image_token: Type.String({ description: "Image token (from block image.token)" }),
}),
```

**修改文件 2**: `/usr/local/lib/node_modules/openclaw/extensions/feishu/src/docx.ts`

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

2. 在 `switch` 语句中添加 case：

```typescript
case "get_image":
  return json(await getImage(client, p.image_token));
```

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

## 使用示例

### 获取文档中的图片

```javascript
// 1. 列出文档中的 blocks
feishu_doc({
  action: "list_blocks",
  doc_token: "Cxvsw9nGpiy1hsky1Agc7agdnlc"
})

// 返回包含 image blocks，每个有 token
// 例如: block.image.token = "SJyGbgoTjomp0fxGI0Ccm4RInRf"

// 2. 获取图片下载 URL
feishu_doc({
  action: "get_image",
  image_token: "SJyGbgoTjomp0fxGI0Ccm4RInRf"
})

// 返回: { image_url: "https://xxx", image_token: "..." }
```

### OCR 识别

获取图片 URL 后，可以用浏览器打开并截图，然后用 tesseract 识别：

```bash
# 截图后识别
tesseract /path/to/screenshot.jpg - -l chi_sim
```

## 注意事项

1. **临时 URL**: `get_image` 返回的 URL 是飞书临时生成的，有时效性
2. **权限**: 需要飞书开放平台应用有 `drive:drive` 权限
3. **OCR 效果**: 取决于图片清晰度，建议使用高清图片

## 故障排除

### get_image 返回空 image_url

- 可能是 token 过期，尝试重新获取
- 检查飞书应用权限

### OCR 识别效果差

- 使用更高分辨率的图片
- 调整 tesseract 的预处理参数
- 考虑使用其他 OCR 服务

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT
