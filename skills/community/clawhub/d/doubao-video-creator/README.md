# 豆包视频创作助手 - Doubao Video Creator

🎬 使用火山引擎豆包（Doubao Seedance）AI 模型，将想法转化为专业视频

## ✨ 核心特性

- **🎯 专业提示词生成** - 结构化模板 + 镜头语言词库
- **📋 严格确认流程** - 提示词确认 + 逐个场景确认
- **⚙️ 项目化管理** - 完整配置 + 状态追踪 + 日志记录
- **📚 完整文档体系** - 15 个专业文档覆盖全流程

## 🚀 快速开始

### 1. 安装技能

```bash
# 方法 1: 使用 OpenClaw
/plugin install https://github.com/YOUR_USERNAME/doubao-video-creator

# 方法 2: 克隆到本地
git clone https://github.com/YOUR_USERNAME/doubao-video-creator.git
cp -r doubao-video-creator ~/.openclaw/workspace/skills/
```

### 2. 首次配置

首次使用会引导配置：
- 火山引擎豆包 API Key
- 文生视频模型选择（2.0/1.5/1.0）
- 图生视频模型选择

### 3. 开始创作

```
用户：用豆包帮我生成一个产品宣传视频

助手：好的！我是豆包视频创作助手 🎬

为了生成更符合您需求的视频，请告诉我：
1. 视频主题：是什么产品/服务？
2. 目标受众：给谁看的？
3. 视频风格：科技感？温馨？专业？
4. 参考资料：有产品图片、文档或链接吗？
```

## 📋 核心功能

### 1. 专业提示词生成器 ⭐

使用结构化模板生成专业提示词：

```
【整体描述】风格 + 时长 + 比例 + 氛围

【分镜描述】
0-5 秒：[景别][运镜] 镜头，[画面内容]，[主体动作]，[光影效果]，[质量词]

【声音说明】配乐/音效
【参考素材】@图片 1 作为...
```

### 2. 镜头语言词库

- **景别**：远景、全景、中景、近景、特写
- **运镜**：推、拉、摇、移、跟、环绕、升降、希区柯克变焦
- **转场**：硬切、渐变、匹配剪辑、特效转场
- **质量词**：高清写实、电影级画质、4K 细节

### 3. 严格确认流程

```
需求收集 → 技术参数 → 脚本规划 → 关键元素 → 生成方式 
→ 提示词生成 → 提示词确认 ⚠️ → 分场景生成 ✅ → 视频合成
```

### 4. 技术参数自动计算

```
场景数量 = 总时长 ÷ 5（固定）

30 秒 → 6 个场景
60 秒 → 12 个场景
```

## 📁 文件结构

```
doubao-video-creator/
├── prompt_generator.py      ⭐ 专业提示词生成器
├── config_manager.py        配置管理
├── scene_confirmation.py    场景确认
├── doubao_video_creator.py  视频生成
├── video_project.py         项目管理
├── element_generator.py     元素生成
├── prompt_optimizer.py      提示词优化
├── SKILL.md                 ⭐ 主技能文档
├── README.md                使用说明
├── BEST_PRACTICES.md        最佳实践
├── CINEMATOGRAPHY_LIBRARY.md ⭐ 镜头语言词库
├── QUICK_REFERENCE.md       快速参考
├── TECH_SPECS_GUIDE.md      技术参数
├── SEEDANCE_ANALYSIS.md     技能分析
└── project_template.json    配置模板
```

## 🎯 使用示例

### 产品宣传视频

```
用户：用豆包帮我生成一个智能手表宣传视频

助手：好的！请告诉我：
1. 视频主题：智能手表的哪些功能想重点展示？
2. 目标受众：消费者/经销商/内部？
3. 视频风格：科技感？运动感？商务感？
4. 参考资料：有产品图片或文档吗？

用户：科技感，面向消费者，重点展示心率和运动追踪功能

助手：好的！技术参数推荐：
- 总时长：30 秒（6 个场景）
- 比例：9:16 竖屏（适合抖音）
- 画质：720p 高清

开始生成脚本...
```

### 生成的提示词示例

```
【整体描述】
现代科技感风格，5 秒，9:16，简约商务氛围

【分镜描述】
0-5 秒：特写镜头从下往上缓缓推近，智能手表表盘，
        光线扫过屏幕展示质感，自然光从侧面射入照明，
        高清写实，电影级画质，4K 细节

【参考素材】
@图片 1 作为产品外观参考
```

## 📊 推荐配置

| 用途 | 总时长 | 场景数 | 比例 | 画质 |
|------|--------|--------|------|------|
| 抖音/快手 | 30 秒 | 6 个 | 9:16 竖屏 | 720p |
| YouTube/B 站 | 60 秒 | 12 个 | 16:9 横屏 | 1080p |
| 朋友圈 | 15 秒 | 3 个 | 9:16 竖屏 | 720p |

## 📚 文档说明

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 完整技能说明 |
| [README.md](README.md) | 使用说明 |
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | **最佳实践指南** ⭐ |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | **快速参考卡片** ⭐ |
| [CINEMATOGRAPHY_LIBRARY.md](CINEMATOGRAPHY_LIBRARY.md) | **镜头语言词库** ⭐ |
| [TECH_SPECS_GUIDE.md](TECH_SPECS_GUIDE.md) | 技术参数确认 |
| [REQUIREMENTS_BEST_PRACTICE.md](REQUIREMENTS_BEST_PRACTICE.md) | 需求收集指南 |

## ⚙️ 配置要求

### 必需
- OpenClaw 运行环境
- 火山引擎豆包 API Key

### 可选
- 通义万相 API Key（生成参考图）

## 💡 最佳实践

### 1. 提供参考资料
- 📄 产品文档
- 🔗 官网/参考视频
- 🖼️ 产品图片（**强烈建议！**）

### 2. 确认技术参数
- 根据发布平台选择比例
- 30 秒最适合（6 个场景）

### 3. 仔细确认提示词
- 提示词确认后才会生成
- 可以要求修改优化

### 4. 逐个场景确认
- 每个场景都确认质量
- 不满意可以重新生成

## 🔧 开发

### 模块说明

| 模块 | 说明 |
|------|------|
| prompt_generator.py | 专业提示词生成器 |
| config_manager.py | 配置和项目管理 |
| scene_confirmation.py | 场景确认流程 |
| doubao_video_creator.py | 视频生成核心 |

### 测试

```bash
cd doubao-video-creator
python3 prompt_generator.py  # 测试提示词生成
python3 config_manager.py    # 测试配置管理
```

## 📈 版本历史

### v2.1 (2026-04-01)
- ✨ 新增专业提示词生成器
- ✨ 整合镜头语言词库
- ✨ 优化提示词结构
- ✨ 新增快速参考卡片
- 📝 完善文档体系（15 个文档）

### v2.0 (2026-03-31)
- ✨ 首次使用配置流程
- ✨ 分场景生成方式选择
- ✨ 完整项目记录
- ✨ 严格确认流程

### v1.1 (2026-03-31)
- ✨ 关键元素生成和确认

## 🎯 核心优势

**doubao-video-creator =**
- seedance-storyboard 的专业性（提示词 + 镜头语言）✅
- 严格的流程管理（配置 + 确认）✅
- 完整的文档体系（15 个专业文档）✅
- 实测数据支撑（5 秒最佳时长）✅

## 📞 支持

- **技能作者**: 卡妹 🌸
- **更新日期**: 2026-04-01
- **版本**: v2.1
- **许可**: MIT

## 🙏 致谢

灵感来源于 [seedance-storyboard](https://github.com/elementsix/claude-seedance-plugin) 技能，借鉴了其专业的提示词结构和镜头语言词库。

---

**享受 AI 视频创作的乐趣！** 🎬✨
