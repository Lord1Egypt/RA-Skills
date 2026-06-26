# FreeAds 随手拍广告 🎬

> **AI 高端广告视频生成器** - 一键将产品照片转化为 8 秒专业 TVC 级广告视频

[![Version](https://img.shields.io/badge/version-3.5.0-blue.svg)](https://github.com/lipeng10/freeads)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-CodeFlicker%20%7C%20OpenClaw%20%7C%20Claude--Code-purple.svg)]()

---

## ✨ 功能亮点

| 功能 | 说明 |
|------|------|
| 🎯 **智能产品识别** | 自动识别产品类型、材质、颜色、特征 |
| 🏠 **智能场景匹配** | 根据产品类别自动选择最佳展示环境（厨房电器→现代厨房，电子产品→科技空间等） |
| 🎬 **专业 3 镜头分镜** | REVEAL → SHOWCASE → HERO 结构化分镜设计 |
| 🎵 **BGM + 音效** | 自动配置背景音乐和同步音效 |
| 💬 **智能 Slogan** | AI 生成契合产品的品牌 Slogan |
| 📊 **完整输出报告** | 输出产品识别、场景设计、分镜脚本、提示词、视频 URL |

---

## 🎥 示例效果

**输入**：一张产品照片（如空气炸锅）

**输出**：
- 📦 **产品识别**: Digital Air Fryer - 白色哑光机身 + 黑色数字显示屏
- 🏠 **场景设计**: 现代简约厨房，大理石台面，晨光透过窗户
- 🎬 **3 镜头分镜**:
  - Shot 1 (0-3s): 产品在厨房环境中呈现
  - Shot 2 (3-6s): 环绕运镜展示细节
  - Shot 3 (6-8s): 最终美图 + Slogan
- 💬 **Slogan**: "Crisp Perfection"
- 🎥 **8 秒 TVC 视频**: [点击查看示例](https://atlas-media.oss-us-west-1.aliyuncs.com/videos/b0b0cd55-7853-414d-a2b9-aeaf7606789b.mp4)

---

## 🚀 快速开始

### 1. 获取 Atlas Cloud API Key

本 Skill 使用 [Atlas Cloud](https://www.atlascloud.ai?ref=LJNA3T) 提供的 AI 模型服务。

**注册链接**: 👉 [https://www.atlascloud.ai?ref=LJNA3T](https://www.atlascloud.ai?ref=LJNA3T)

> 🎁 **新用户福利**: 使用上述链接注册，首次充值可获得 **25% 奖励**（最高奖励 $100）！

注册后：
1. 登录 [Atlas Cloud Console](https://console.atlascloud.ai)
2. 进入 API Keys 页面
3. 创建新的 API Key
4. 复制保存 API Key

### 2. 配置环境变量

```bash
export ATLASCLOUD_API_KEY="your-api-key-here"
```

或添加到 `~/.zshrc` / `~/.bashrc` 永久保存。

### 3. 安装 Skill

```bash
clawhub install lipeng0820/freeads-snap-ad
```

### 4. 使用

在 CodeFlicker / OpenClaw / Claude-Code 中对 AI 说：

> "帮我用这张图片生成一个广告视频"
> 
> "随手拍广告：[粘贴图片 URL]"
> 
> "生成广告视频"

---

## 📋 使用的模型

| 功能 | 模型 | 提供商 |
|------|------|--------|
| 产品识别 + 分镜脚本 | `moonshotai/kimi-k2.5` | Moonshot AI |
| 视频生成 | `google/veo3.1/image-to-video` | Google DeepMind |

---

## 💰 费用估算

| 步骤 | 模型 | 费用估算 |
|------|------|----------|
| 分镜脚本 | Kimi K2.5 | ~$0.01 |
| 视频生成 | Veo 3.1 | ~$1.19 |
| **总计** | | **~$1.20/视频** |

---

## 📊 输出示例

执行后会生成完整的输出报告：

```markdown
## 1. 输入
- **原图**: https://example.com/product.jpg

## 2. 产品识别
{
  "type": "Kitchen Appliance",
  "name": "Digital Air Fryer",
  "material": "Matte white ABS plastic",
  "color": "Pure white with black digital interface",
  "features": ["Touch-sensitive digital display", "Ergonomic pull-handle"]
}

## 3. 场景设计
{
  "environment": "Modern minimalist kitchen",
  "setting_description": "Bright contemporary kitchen with marble countertop",
  "lighting": "Soft natural morning light",
  "mood": "Fresh, clean, inviting"
}

## 4. 分镜脚本（3 个镜头）
- Shot 1 (0-3s): REVEAL - 产品在厨房环境中呈现
- Shot 2 (3-6s): SHOWCASE - 60° 环绕运镜展示细节
- Shot 3 (6-8s): HERO - 最终美图 + Slogan 动画

## 5. Slogan
> Crisp Perfection

## 6. Veo 3.1 提示词
[完整提示词内容]

## 7. 输出视频
- **URL**: https://atlas-media.../video.mp4
```

---

## 🔄 版本历史

### v3.5.0 (2025-03-25) ⭐ 最新
- ✨ 优化分镜结构，严格限制最多 3 个镜头
- 🏠 根据产品类别智能选择场景环境
- 📊 输出结构化 JSON 分镜数据
- 📋 完整中间结果报告
- 🔄 分镜脚本模型改用 `moonshotai/kimi-k2.5`

### v3.4.0
- 优化 8 秒分镜时间结构

### v3.3.0
- 移除抠图步骤（避免产品被替换）
- 直接使用用户原图进行视频生成

### v3.2.0 及更早版本
- 初始版本，探索最佳工作流程

---

## ⚠️ 注意事项

1. **图片要求**: 建议使用清晰的产品图片，最好是白底或简洁背景
2. **视频时长**: 固定 8 秒，符合社交媒体短视频规范
3. **分辨率**: 1080p，16:9 比例
4. **API 额度**: 每次生成视频消耗约 $1.20，请确保 Atlas Cloud 账户余额充足

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **Atlas Cloud**: [https://www.atlascloud.ai?ref=LJNA3T](https://www.atlascloud.ai?ref=LJNA3T)（首次充值 25% 奖励，最高 $100）
- **ClawHub**: [https://clawhub.com/lipeng0820/freeads-snap-ad](https://clawhub.com/lipeng0820/freeads-snap-ad)

---

Made with ❤️ by lipeng0820
