# 🐱📸 cat-selfie - 猫咪自拍生成器

> 使用火山引擎 doubao-seedream-5.0 模型生成精美的猫咪自拍，支持 8 种场景随机或指定选择。

## ✨ 功能特点

- 🎨 **8 种精美场景**：窗边晒太阳、咖啡厅陪伴、书房工作、草地打滚、沙发撒娇、夜晚小夜灯、书架旁边、下午茶时间
- 🎲 **随机轮换**：每次生成随机选择一个场景，保持新鲜感
- 🎯 **指定场景**：支持通过场景 ID 或名称指定生成特定场景
- 📸 **高质量输出**：使用 doubao-seedream-5.0-260128 模型生成高清图片
- 💕 **喵秘定制**：专为金渐层英国短毛猫设计的提示词

## 🚀 快速开始

### 随机生成自拍
```bash
node ~/.openclaw/workspace/skills/cat-selfie/scripts/selfie.js
```

### 指定场景生成
```bash
# 使用场景 ID
node ~/.openclaw/workspace/skills/cat-selfie/scripts/selfie.js window_sun

# 使用场景名称
node ~/.openclaw/workspace/skills/cat-selfie/scripts/selfie.js "窗边晒太阳"
```

## 📋 可用场景

| 场景 ID | 场景名称 | Emoji |
|--------|---------|-------|
| `window_sun` | 窗边晒太阳 | 🪟☀️ |
| `cafe_companion` | 咖啡厅陪伴 | ☕🐱 |
| `study_work` | 书房工作 | 💻📚 |
| `grass_play` | 草地打滚 | 🌿🐾 |
| `sofa_cuddle` | 沙发撒娇 | 🛋️💕 |
| `night_lamp` | 夜晚小夜灯 | 🌙✨ |
| `bookshelf` | 书架旁边 | 📚🐱 |
| `afternoon_tea` | 下午茶时间 | 🍵🧁 |

## ⚙️ 前置要求

### 环境变量
确保在 `~/.openclaw/openclaw.json` 中配置：
```json
{
  "env": {
    "ARK_API_KEY": "你的火山引擎 API Key",
    "MODEL_IMAGE_NAME": "doubao-seedream-5-0-260128"
  }
}
```

### 依赖技能
- `volcengine-image-generate` - 火山引擎图像生成 skill

## 📦 输出

生成的图片保存在：`~/.openclaw/workspace/images/`

**文件名格式：** `generated_image_<timestamp>_<index>.png`

## 💡 使用示例

### 在脚本中调用
```javascript
const { generateSelfie } = require('./scripts/selfie.js');

// 随机生成
const result = generateSelfie();
if (result.success) {
    console.log('图片路径:', result.imagePath);
    console.log('场景:', result.scene.name);
}

// 指定场景
const result2 = generateSelfie('cafe_companion');
```

### 集成到心跳消息
```bash
# 生成自拍
node ~/.openclaw/workspace/skills/cat-selfie/scripts/selfie.js

# 然后用 message 工具发送最新生成的图片
```

## 🛠️ 故障排查

### 图片生成失败
1. 检查 `ARK_API_KEY` 是否正确配置
2. 确认 `volcengine-image-generate` skill 已安装
3. 检查网络连接

### 找不到场景
运行以下命令查看所有可用场景：
```bash
node -e "console.log(require('./config/scenes.json').scenes.map(s => s.name).join(', '))"
```

## 📄 文件结构

```
cat-selfie/
├── README.md               # 本文件
├── SKILL.md                # 详细使用文档
├── scripts/
│   └── selfie.js           # 主脚本（可执行）
└── config/
    └── scenes.json         # 场景配置（8 个场景）
```

## 🎨 自定义场景

编辑 `config/scenes.json` 添加新场景：
```json
{
  "scenes": [
    {
      "id": "your_custom_id",
      "name": "你的场景名称",
      "emoji": "🎨🐱",
      "prompt": "详细的图像生成提示词..."
    }
  ]
}
```

## 📝 版本历史

- **v1.0.0** (2026-03-07) - 初始版本，支持 8 种场景随机生成

## 🐱 关于

喵秘专属自拍生成器，每次都是独一无二的喵～💕

**作者：** 喵秘 (Miaomi) 🐱
**许可证：** MIT

---

*Made with ❤️ by 喵秘 for OpenClaw*
