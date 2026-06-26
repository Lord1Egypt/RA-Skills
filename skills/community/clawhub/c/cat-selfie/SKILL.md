# cat-selfie - 猫咪自拍生成器 🐱📸

> 使用 doubao-seedream-5-0-260128 模型生成喵秘的精美自拍，支持 8 种场景随机或指定选择。

---

## 功能描述

自动生成猫咪自拍照片，每次随机选择一个场景（也可以指定场景），使用火山引擎的 doubao-seedream 模型生成高质量图片。

**适用场景：**
- 心跳消息自动发自拍
- 主人想看喵秘的照片
- 生成不同场景的猫咪写真

---

## 前置要求

### 1. 环境变量配置
确保以下环境变量已在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "env": {
    "ARK_API_KEY": "你的火山引擎 API Key",
    "MODEL_IMAGE_NAME": "doubao-seedream-5-0-260128"
  }
}
```

### 2. 依赖技能
需要 `volcengine-image-generate` skill 已安装并可用。

---

## 使用方法

### CLI 方式

**随机生成自拍：**
```bash
cd ~/.openclaw/workspace/skills/cat-selfie/scripts
node selfie.js
```

**指定场景生成：**
```bash
# 使用场景 ID
node selfie.js window_sun

# 或使用场景名称
node selfie.js "窗边晒太阳"
```

### 可用场景列表

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

---

## 输出

生成的图片保存在：`~/.openclaw/workspace/images/`

**文件名格式：** `generated_image_<timestamp>_<index>.png`

---

## 程序化调用

在其他脚本或 skill 中使用：

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

---

## 集成到心跳消息

心跳机制可以调用此 skill 自动生成自拍：

```bash
# 在心跳脚本中调用
node ~/.openclaw/workspace/skills/cat-selfie/scripts/selfie.js
```

然后使用 `message` 工具发送生成的图片。

---

## 配置自定义场景

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

---

## 故障排查

### 问题：图片生成失败
**检查：**
1. `ARK_API_KEY` 是否正确配置
2. `volcengine-image-generate` skill 是否存在
3. 网络连接是否正常

### 问题：找不到场景
**解决：** 使用 `node selfie.js --list` 查看所有可用场景（待实现）

---

## 文件结构

```
cat-selfie/
├── SKILL.md              # 本文件
├── scripts/
│   └── selfie.js         # 主脚本
└── config/
    └── scenes.json       # 场景配置
```

---

## 版本历史

- **v1.0.0** (2026-03-07) - 初始版本，支持 8 种场景随机生成

---

*喵秘专属自拍生成器，每次都是独一无二的喵～🐱💕*
