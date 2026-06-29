# Agnes Image Generator Skill for OpenClaw

这个技能让你能直接在对话中使用 Agnes Image 2.1 Flash 生成图片。

## 配置

1. **设置 API Key 环境变量**（推荐）：

在你的 shell 配置文件中添加（如 `~/.bashrc` 或 `~/.zshrc`）：
```bash
export AGNES_API_KEY="your-agnes-api-key-here"
```

然后重新登录或运行 `source ~/.bashrc`。

2. **或者**将 API Key 硬编码到脚本（不推荐）：
   编辑 `scripts/generate.js`，将 `AGNES_API_KEY` 常量改为你的 key。

## 使用方法

### 直接调用脚本

```bash
# 文生图
node scripts/generate.js --prompt "一只可爱的小狗在公园里玩耍" --size 1024x1024

# 图生图（使用图片URL）
node scripts/generate.js --prompt "把这张图变成赛博朋克风格" --image "https://example.com/input.jpg" --size 1024x1024

# 图生图（使用Data URI）
node scripts/generate.js --prompt "保留构图，把颜色变成橙色" --image "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." --size 1024x768
```

### 在 OpenClaw 对话中

直接对我说：
- "生成一张小狗在公园里玩耍的图片"
- "画一个未来城市的海报，1024x768"
- "基于这张图片（URL）... 生成..."

我会自动调用这个技能并返回图片链接。

## 输出

成功时返回 JSON：
```json
{
  "success": true,
  "url": "https://storage.googleapis.com/agnes-aigc/xxx.png"
}
```

失败时返回：
```json
{
  "success": false,
  "error": "错误信息"
}
```

## 注意事项

- 图片成本：$0.003/张（Agnes 定价）
- 支持尺寸：如 1024x1024, 1024x768, 1536x1024 等
- 图生图会尽量保留原图构图
- 确保 API Key 有充足的余额

## 技术细节

- 端点：`https://apihub.agnes-ai.com/v1/images/generations`
- 模型：`agnes-image-2.1-flash`
- 输出格式：URL（存储在云端，可公开访问）
