# Canvas Workspace Skill

画布工作区操作能力。支持 AI 生图、编辑图、将图片推送到画布。

## 功能

- **文生图**：使用 Qwen 或 Gemini 模型生成图片
- **编辑图**：基于标记或自由编辑现有图片
- **推送图片**：将任意图片 URL 推送到画布
- **画布状态**：查看当前画布上的图片列表

## 快速开始

```bash
# 启动画布工作区
npx deepminer-claw-canvas@latest

# 文生图
npx deepminer-claw-canvas gen --prompt "一张极简海报"

# 编辑图
npx deepminer-claw-canvas edit --prompt "变成卡通风格" --raw-image "image.png"

# 推送图片
npx deepminer-claw-canvas push --url "https://example.com/image.png"
```

## 环境变量

| 变量 | 用途 |
|------|------|
| `QWEN_TEXT_IMAGE_API_KEY` | Qwen 文生图 API Key |
| `QWEN_EDIT_IMAGE_API_KEY` | Qwen 编辑图 API Key |
| `GEMINI_TEXT_IMAGE_API_KEY` | Gemini 文生图 API Key |

详见 [SKILL.md](./SKILL.md) 中的完整文档。

## 许可

MIT
