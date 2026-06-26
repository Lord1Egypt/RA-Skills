# 豆包视频创作助手 v2.0

> 🎬 使用火山引擎豆包（Doubao Seedance）AI 模型，将想法转化为专业视频

## 🌟 v2.0 新特性

### 1. 首次使用配置 📋
- 引导式 API Key 配置
- 模型版本选择（2.0/1.5/1.0）
- 配置持久化保存

### 2. 分场景生成方式选择 🎯
- **文生视频**: 快速生成，适合简单场景
- **图生视频**: 精确控制，适合复杂场景
- 每个场景独立选择

### 3. 完整项目记录 📁
- 项目级配置管理
- 完整状态追踪
- 支持中断恢复
- 生成日志记录

## 📦 安装

```bash
# 技能已安装在
/root/.openclaw/workspace/skills/doubao-video-creator/
```

## 🚀 快速开始

### 1. 首次使用配置

```
用户：用豆包帮我生成一个产品宣传视频

助手：🔧 首次使用配置
检测到您是首次使用，需要配置：
1️⃣ 火山引擎豆包 API Key
2️⃣ 文生视频模型版本
3️⃣ 图生视频模型版本
```

### 2. 需求收集

提供以下信息：
- 视频主题/用途
- 目标受众
- 视频风格
- 参考资料（文档、图片、URL 等）

### 3. 脚本确认

AI 自动生成视频脚本，包含：
- 总时长（默认 12 秒）
- 场景数量（默认 3 个）
- 每个场景的描述、文案、风格

### 4. 关键元素生成

生成并确认：
- 人物形象参考图
- 场景背景参考图
- 关键物品参考图

### 5. 分场景制作

对每个场景：
1. 选择生成方式（文生视频/图生视频）
2. 确认原型图（仅图生视频）
3. 确认视频提示词
4. 生成视频
5. 确认视频质量

### 6. 视频合成

- 拼接所有场景
- 添加转场效果
- 添加背景音乐（可选）

## 📁 文件结构

```
doubao-video-creator/
├── SKILL.md                 # 技能说明文档
├── README.md                # 本文件
├── UPDATE_v2.0.md           # v2.0 更新说明
├── FLOWCHART_v2.md          # 完整工作流程图
├── project_template.json    # 项目配置模板
├── config_manager.py        # 配置管理模块
├── scene_confirmation.py    # 场景确认模块
├── doubao_video_creator.py  # 视频生成核心
├── element_generator.py     # 元素生成器
├── prompt_optimizer.py      # 提示词优化器
└── video_project.py         # 项目管理
```

## ⚙️ 配置说明

### 全局配置
位置：`~/.openclaw/workspace/doubao-config.json`

```json
{
  "default_api_key": "YOUR_API_KEY",
  "default_text_to_video_model": "doubao-seedance-2-0-pro",
  "default_image_to_video_model": "doubao-seedance-1-5-pro"
}
```

### 可用模型

| 模型 ID | 版本 | 推荐 | 说明 |
|--------|------|------|------|
| `doubao-seedance-2-0-pro` | 2.0 | ✅ | 最新版本，效果最佳 |
| `doubao-seedance-1-5-pro` | 1.5 | ✅ | 稳定版本，广泛使用 |
| `doubao-seedance-1-0-pro` | 1.0 | ❌ | 基础版本，兼容性好 |

## 📊 项目配置

每个项目生成独立的 `project.json`：

```json
{
  "project_id": "video_20260331_120000",
  "theme": "智能手表 X1 宣传视频",
  "api_config": {
    "api_key": "...",
    "text_to_video_model": "doubao-seedance-2-0-pro",
    "image_to_video_model": "doubao-seedance-1-5-pro"
  },
  "scenes": [
    {
      "id": 1,
      "generation_mode": "image_to_video",
      "prototype_images": ["/path/to/prototype.png"],
      "prompt": "...",
      "prompt_confirmed": true,
      "video_path": "/path/to/video.mp4",
      "video_status": "confirmed"
    }
  ],
  "generation_log": [...]
}
```

## 🎯 使用技巧

### 1. 文生视频 vs 图生视频

**选择文生视频**：
- 简单场景
- 抽象画面
- 快速测试
- 预算有限

**选择图生视频**：
- 复杂场景
- 需要精确控制
- 角色一致性要求高
- 重要场景

### 2. 提示词优化

好的提示词包含：
- 场景描述（主体、动作、环境）
- 镜头语言（推、拉、摇、移）
- 光影效果（自然光、逆光、侧光）
- 风格定位（写实、电影感、科技感）
- 质量词（高清、4K、电影级画质）

### 3. 成本控制

- 先用文生视频测试脚本
- 关键场景使用图生视频
- 确认提示词再生成
- 避免重复生成

## ⚠️ 注意事项

### 平台限制
- 视频时长：2-12 秒
- 推荐场景时长：4 秒
- 推荐场景数：3 个
- 总时长：12 秒

### 生成时间
- 图片生成：~30 秒/张
- 视频生成：~1-2 分钟/场景
- 完整流程：~10-15 分钟

### 成本估算
- 图片生成：¥0.05-0.10/张
- 视频生成：¥0.15-0.50/场景
- 完整视频（3 场景）：¥1-2 元

## 📝 对话示例

```
用户：用豆包帮我生成一个产品宣传视频

助手：好的！我是豆包视频创作助手 🎬

🔧 首次使用配置
检测到您是首次使用，需要配置 API 信息：
1️⃣ 火山引擎豆包 API Key
2️⃣ 文生视频模型（2.0/1.5/1.0）
3️⃣ 图生视频模型（2.0/1.5/1.0）

用户：API Key 是 65ae8f92-134c-4194-a3af-6e6cb74284e0，文生用 2.0，图生用 1.5

助手：✅ 配置已保存！

现在请告诉我：
1. 视频主题：是什么产品/服务？
2. 目标受众：给谁看的？
3. 视频风格：科技感？温馨？专业？
4. 参考资料：文档、图片、URL 等（可选）

用户：智能手表 X1，目标用户是都市白领，科技感风格

助手：📝 生成脚本...

【视频脚本】智能手表 X1 宣传
总时长：12 秒 | 场景数：3 个

场景 1（0-4 秒）：开场展示
- 画面：手表特写，镜头从下往上扫过
- 文案："创新科技，改变生活"
- 风格：现代科技感

场景 2（4-8 秒）：功能演示
- 画面：用户操作手表，显示心率和步数
- 文案："健康监测，一目了然"
- 风格：清晰直观

场景 3（8-12 秒）：品牌结尾
- 画面：产品图 + 品牌 Logo
- 文案："X1，你的智能伙伴"
- 风格：专业大气

这个脚本可以吗？需要调整吗？😊

用户：确认

助手：🎨 开始生成关键元素参考图...
（生成并确认人物、场景、物品参考图）

助手：🎬 场景 1 确认（0-4 秒）

请选择生成方式：
A) 文生视频 - 直接用文字提示词生成
B) 图生视频 - 先生成场景原型图

用户：B

助手：🎨 生成场景原型图...
<qqimg>scene1_prototype.png</qqimg>

确认用于视频生成吗？

用户：确认

助手：📝 提示词确认
【提示词】参考上传图片的场景...
确认开始生成视频吗？

用户：确认

助手：🎬 生成场景 1...
<qqvideo>scene1.mp4</qqvideo>

满意吗？需要调整吗？

用户：满意

助手：✅ 场景 1 已确认！准备生成场景 2...
（重复流程直到所有场景完成）

助手：🎉 所有场景完成！开始合成最终视频...
<qqvideo>final_video.mp4</qqvideo>

完成！这是您的智能手表 X1 宣传视频 🎊
```

## 🔧 开发

### 模块说明

- **config_manager.py**: 配置管理（API Key、模型选择、项目配置）
- **scene_confirmation.py**: 场景确认（生成方式、原型图、提示词、视频）
- **doubao_video_creator.py**: 视频生成核心（调用豆包 API）
- **element_generator.py**: 元素生成（人物、场景、物品参考图）
- **prompt_optimizer.py**: 提示词优化（基于参考图生成提示词）
- **video_project.py**: 项目管理（完整对话流程）

### 测试

```bash
cd /root/.openclaw/workspace/skills/doubao-video-creator/
python3 config_manager.py
python3 scene_confirmation.py
```

## 📚 相关文档

- [SKILL.md](SKILL.md) - 完整技能说明
- [UPDATE_v2.0.md](UPDATE_v2.0.md) - v2.0 更新说明
- [UPDATE_SUMMARY_v2.1.md](UPDATE_SUMMARY_v2.1.md) - **v2.1 调优总结** 📊
- [FLOWCHART_v2.md](FLOWCHART_v2.md) - 工作流程图
- [BEST_PRACTICES.md](BEST_PRACTICES.md) - **最佳实践指南** ⭐
- [REQUIREMENTS_BEST_PRACTICE.md](REQUIREMENTS_BEST_PRACTICE.md) - **需求收集指南** 📋
- [TECH_SPECS_GUIDE.md](TECH_SPECS_GUIDE.md) - **技术参数确认指南** ⚙️
- [SEEDANCE_DURATION_EXPLAINED.md](SEEDANCE_DURATION_EXPLAINED.md) - **时长说明** ⏱️
- [SEEDANCE_DURATION_REALITY.md](SEEDANCE_DURATION_REALITY.md) - **实测结论** 🔬
- [SEEDANCE_ANALYSIS.md](SEEDANCE_ANALYSIS.md) - **Seedance 技能分析** 📊
- [CINEMATOGRAPHY_LIBRARY.md](CINEMATOGRAPHY_LIBRARY.md) - **镜头语言词库** 🎬
- [project_template.json](project_template.json) - 项目配置模板

## 📞 支持

如有问题，请联系：
- 技能作者：卡妹 🌸
- 更新日期：2026-03-31
- 版本：v2.0

---

**享受 AI 视频创作的乐趣！** 🎬✨
