---
name: fooocus-image-gen
description: Local AI image generation using Fooocus (Stable Diffusion XL). Use when users want to generate images locally without relying on cloud APIs. Supports text-to-image, image variations, upscaling, inpainting, outpainting, face swap, and style transfer. Triggers on phrases like "generate image with Fooocus", "local image generation", "SDXL generation", "inpaint this image", "upscale image locally", or any image generation request when Fooocus is mentioned or preferred over cloud services.
homepage: https://github.com/lllyasviel/Fooocus
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python"],"packages":["torch","gradio","websockets","requests","Pillow"]},"primaryEnv":"FOOOCUS_PATH"}}
license: MIT
---

> **Skill Version**: 2.0 | **Last Updated**: 2026-03-08
> 
> 本 Skill 持续从 Fooocus GitHub 社区学习更新，整合了官方文档、社区讨论和实战经验。

# Fooocus Image Generation Skill

Generate AI images locally using Fooocus - an offline, open-source image generation tool based on Stable Diffusion XL.

## Overview

This skill integrates with [Fooocus](https://github.com/lllyasviel/Fooocus), a powerful local image generation software that runs on your machine. It provides a user-friendly interface to Fooocus's Gradio API, hiding complexity while exposing all powerful features.

### Key Features

- **Text-to-Image**: Generate images from text prompts
- **Image-to-Image**: Create variations, upscale, or transform existing images
- **Inpainting/Outpainting**: Edit specific regions or extend images
- **Style Control**: Apply presets and custom styles
- **Batch Generation**: Generate multiple images at once
- **Face Swap**: Replace faces in images
- **IP-Adapter**: Use reference images for style transfer
- **Real-time Progress**: WebSocket-based live progress updates

### System Requirements

- **OS**: Windows 10/11, Linux, or macOS
- **GPU**: NVIDIA GPU with 4GB+ VRAM (minimum)
- **RAM**: 8GB+ recommended
- **Storage**: 10GB+ free space for models
- **Python**: 3.10 or higher
- **Network**: Local only (no internet required after setup)

---

## 🚀 Quick Start

### Step 1: Environment Check

First, verify your system is ready:

```bash
python "${SKILL_ROOT}/scripts/check_env.py"
```

This will check:
- ✅ Python version (3.10+)
- ✅ CUDA availability and GPU memory
- ✅ Fooocus installation status
- ✅ Required dependencies

### Step 2: Install Fooocus (if needed)

If Fooocus is not installed:

```bash
# Automatic installation
python "${SKILL_ROOT}/scripts/install_fooocus.py" --path ~/Fooocus

# With model pre-download (slower but ready immediately)
python "${SKILL_ROOT}/scripts/install_fooocus.py" --path ~/Fooocus --download-models
```

### Step 3: Start Fooocus Service

**Option A: Manual Start (Recommended for first time)**

```bash
cd ~/Fooocus
python entry_with_update.py
```

Wait for the message:
```
Running on local URL: http://127.0.0.1:7865
```

**Option B: Auto-start via check_env script**

```bash
python "${SKILL_ROOT}/scripts/check_env.py" --start
```

**Option C: Start with specific preset**

```bash
cd ~/Fooocus
python entry_with_update.py --preset anime
```

### Step 4: Verify Service is Running

```bash
# Check if Fooocus is responding
curl http://localhost:7865

# Or use the check script
python "${SKILL_ROOT}/scripts/check_env.py"
```

---

## 🗺️ 决策流程图：如何选择正确的配置

```
用户请求类型判断
│
├─► 文生图（从无到有生成）
│   ├─► 纯2D动漫风格？
│   │   └─► 使用 run_anime.bat
│   │       └─► 勾选 SAI Anime + MRE Anime
│   │           取消所有 Fooocus 系列
│   │
│   ├─► 照片写实风格？
│   │   └─► 使用 run.bat 或 run_realistic.bat
│   │       └─► 勾选 Fooocus Photograph + Photo 系列
│   │           取消所有 Anime/Manga 系列
│   │
│   ├─► 写实增强风格？
│   │   └─► 使用 run.bat
│   │       └─► 勾选 Fooocus V2 + Masterpiece + Enhance + Sharp
│   │           取消所有 Anime/Photographic 系列
│   │
│   └─► 其他艺术风格？
│       └─► 使用 run.bat
│           └─► 勾选对应 Artstyle 或 Mk 系列
│
├─► 图生图（基于参考图）
│   ├─► 风格迁移？
│   │   └─► Input Image → Image Prompt
│   │       └─► 上传参考图 + 填写新内容 Prompt
│   │
│   ├─► 放大图片？
│   │   └─► Input Image → Upscale or Variation
│   │       └─► 选择 Upscale (2x) 或 (1.5x)
│   │
│   ├─► 局部修改？（Inpaint）
│   │   └─► 提醒用户：需要手动上传和涂抹！
│   │       └─► Input Image → Inpaint or Outpaint
│   │           └─► Method: Modify Content
│   │               Inpaint Additional Prompt: [填写要生成的内容]
│   │               ⚠️ 首次使用需下载模型
│   │
│   └─► 扩展画面？（Outpaint）
│       └─► Input Image → Inpaint or Outpaint
│           └─► 选择扩图方向 (Left/Right/Top/Bottom)
│
└─► 其他功能
    ├─► 反推 Prompt？
    │   └─► Input Image → Describe
    │
    └─► 图像增强？
        └─► Input Image → Enhance
```

**默认设置检查清单（所有任务）**:
```
□ Performance: Quality（除非用户要求速度）
□ Aspect Ratio: 根据用途选择（默认 896×1152）
□ Image Number: 2-4（根据需求）
```

---

## 🖥️ Fooocus Web UI 面板使用手册 (重点)

Fooocus Web UI 位于 `http://localhost:7865`，面板结构如下：

### ⚠️ 重要提醒：重启后必须重新配置

**Fooocus 不会自动保存上次的配置！**

**每次重启 Fooocus 或刷新页面后，必须重新设置**：
1. **Preset** (如果使用 run_anime.bat 则自动为 anime)
2. **Styles** - 最关键！必须重新勾选/取消
3. **Performance** - 默认为 Speed，但 **Quality 是更好的默认选择**（除非用户明确要求速度）
4. **Aspect Ratio** - 根据图片用途选择合适的分辨率（见下方分辨率选择指南）
5. **Image Number** - 默认为 2
6. **Negative Prompt** - 必须重新输入
7. **Input Image** - 必须重新勾选并上传

**快速恢复配置检查清单**:
```
□ 是否使用了正确的启动方式？(run_anime.bat / run.bat / run_realistic.bat)
□ Styles 是否正确？(SAI Anime + MRE Anime / Fooocus 系列)
□ Negative Prompt 是否包含 3d, realistic, photorealistic？(纯2D动漫时)
□ Input Image 是否已勾选并上传？(图生图时)
□ Image Prompt 模式是否已选择？(风格迁移时)
```

**建议**: 在生成前截图确认配置，避免遗漏！

---

### 📐 分辨率选择指南 (Aspect Ratio)

根据图片用途选择合适的分辨率：

| 用途 | 推荐分辨率 | 比例 | 说明 |
|------|-----------|------|------|
| **头像/肖像** | 896×1152 | 7:9 | 竖版，适合人物肖像 |
| **手机壁纸** | 1152×2048 | 9:16 | 竖版全面屏 |
| **桌面壁纸** | 1920×1088 | 16:9 | 横版标准 |
| **社交媒体** | 1024×1024 | 1:1 | 方形，Instagram 等 |
| **网页横幅** | 1536×640 | 12:5 | 宽屏横幅 |
| **打印海报** | 2048×2048 | 1:1 | 高分辨率方形 |
| **风景插画** | 1280×768 | 5:3 | 横版风景 |
| **漫画/条漫** | 768×2048 | 3:8 | 超长竖版 |

**默认推荐**: 896×1152 (7:9) - 适合大多数人物生成场景

---

### ⚡ 性能设置指南 (Performance)

**默认选择**: **Quality**（除非用户明确要求速度）

| 模式 | 采样步数 | 速度 | 质量 | 适用场景 |
|------|---------|------|------|----------|
| **Quality** | 30步 | 较慢 | 最高 | **默认推荐**，最佳效果 |
| **Speed** | 20步 | 中等 | 高 | 快速预览 |
| **Extreme Speed** | 10步 | 快 | 中等 | 草图阶段 |
| **Lightning** | 5步 | 很快 | 较低 | 快速测试 |
| **Hyper-SD** | 4步 | 最快 | 低 | 仅用于参考 |

**选择建议**:
- **最终成品**: 使用 Quality
- **快速迭代**: 使用 Speed 或 Extreme Speed
- **草图探索**: 使用 Lightning
- **批量生成**: 先用 Speed 筛选，再用 Quality 生成最终版

---

### 1. 主生成区域 (左侧)

#### Prompt 输入框
- **位置**: 页面左侧顶部
- **功能**: 输入生成图像的文本描述
- **最佳实践**: 使用英文 Stable Diffusion 语法

#### 功能开关

| 开关 | 功能 |
|------|------|
| **Input Image** | 启用图像输入功能（图生图、放大、局部重绘等） |
| **Enhance** | 启用图像增强功能 |
| **Advanced** | 显示高级设置面板 |

---

### 2. Input Image 功能详解

当勾选 **Input Image** 后，显示以下子功能：

#### 2.1 Upscale or Variation
- **功能**: 放大或生成变体
- **选项**: Disabled, Vary (Subtle), Vary (Strong), Upscale (1.5x/2x/Fast 2x)

#### 2.2 Image Prompt (图像提示/风格迁移)
- **功能**: 使用参考图像作为风格提示
- **特点**: 支持最多4张参考图像
- **引擎**: Fooocus Image Mixture Engine

#### 2.3 Inpaint or Outpaint (局部重绘或扩图)
- **Inpaint**: 重绘特定区域
  - ⚠️ 首次使用需下载模型
  - Prompt 填写在 **Inpaint Additional Prompt** 中
  - 选择 **Modify Content** 方法更换/添加元素
- **Outpaint**: 向外扩展图像
- **选项**: Enable Advanced Masking, Method, Outpaint Direction

#### 2.4 Describe / Enhance / Metadata
- **Describe**: 自动生成图像描述（反推 Prompt）
  - 上传图片，自动生成描述图片内容的文本
  - 用于学习优秀图片的 Prompt 写法
  - 可基于生成的描述进行修改再生成
- **Enhance**: 图像质量增强
- **Metadata**: 查看生成参数

---

### 3. Describe (图像描述/Prompt 反推)

**核心概念**: 分析图像内容并生成对应的文本描述（Prompt）

**使用场景**:
- 看到喜欢的图片，想知道它的 Prompt 怎么写
- 想复现某种风格但不知道关键词
- 学习优秀的 Prompt 构造技巧

**使用方法**:
1. 勾选 **Input Image**
2. 切换到 **Describe** 标签
3. 上传图片
4. 点击 Generate
5. 查看生成的描述文本

**技巧**:
- 可以基于生成的描述进行修改，再用于生成
- 对比原图和生成图，学习关键词的效果
- 结合 Image Prompt 使用，实现风格迁移

---

## 🎨 高级功能详解与技巧

### 1. Upscale or Variation (图像放大与变体)

#### 1.1 放大功能 (Upscale)

**适用场景**:
- 将低分辨率图像放大到更高分辨率
- 改善图像细节和质量

**选项对比**:

| 选项 | 放大倍数 | 速度 | 质量 | 适用场景 |
|------|----------|------|------|----------|
| **Upscale (1.5x)** | 1.5倍 | 中等 | 高 | 轻微放大，保持细节 |
| **Upscale (2x)** | 2倍 | 较慢 | 最高 | 大幅放大，最佳质量 |
| **Upscale (Fast 2x)** | 2倍 | 快 | 中等 | 快速预览，质量稍降 |

**使用技巧**:
1. **workflow**: 先生成小图测试 → 满意后使用 Upscale (2x)
2. **多次放大**: 可以多次使用 1.5x 逐步放大，比一次 2x 更稳定
3. **显存管理**: 2x 放大需要更多显存，低显存用户建议用 Fast 2x
4. **结合 Variation**: 可以先 Vary (Subtle) 再 Upscale，获得变化后的高清图

#### 1.2 变体功能 (Variation)

**适用场景**:
- 基于现有图像生成相似但不同的版本
- 探索同一构图的不同可能性

**选项对比**:

| 选项 | 变化程度 | 使用场景 |
|------|----------|----------|
| **Vary (Subtle)** | 轻微变化 (10-20%) | 微调细节，保持主体 |
| **Vary (Strong)** | 强烈变化 (30-50%) | 大幅改变，探索新可能 |

**使用技巧**:
1. **种子锁定**: 使用 Vary 时保持 seed 可以控制变化范围
2. **迭代优化**: Subtle → 不满意 → Strong → 选择最佳 → Upscale
3. **批量生成**: 配合 Image Number 生成多个变体选择
4. **风格迁移**: 在变体时切换 Styles，可以获得不同风格的同一构图

**实战案例 - 角色设计优化**:
```
步骤1: 生成基础角色图
步骤2: 使用 Vary (Subtle) 生成4个微调版本
步骤3: 选择最满意的，使用 Vary (Strong) 探索姿态变化
步骤4: 选定最终版本，Upscale (2x) 获得高清图
```

---

### 2. Image Prompt (图像提示/风格迁移)

#### 2.1 基础用法

**核心概念**: 使用参考图像引导生成结果的风格、构图或内容

**特点**:
- 支持最多 **4张参考图** 同时输入
- 与文本 prompt 混合使用效果更佳
- 使用 Fooocus Image Mixture Engine，比标准 IP-Adapter 效果更好

#### 2.2 使用模式

**模式1: 纯图像提示 (无文本)**
- 完全基于参考图生成
- 适合：风格迁移、图像变体

**模式2: 图像 + 文本混合**
- 参考图提供风格/构图
- 文本 prompt 提供内容描述
- 适合：角色设计、场景创作

**模式3: 多图像混合**
- 2-4张参考图同时输入
- Fooocus 会自动融合各图特点
- 适合：混合多种风格、创建独特效果

#### 2.3 高级控制 (Advanced)

勾选 **Advanced** 后可用：

**PyraCanny (金字塔Canny边缘控制)**:
- 基于多分辨率边缘检测
- 更好地捕捉图像结构
- 首次使用下载约 350MB
- 适合：保持原图结构的同时改变风格

**CPDS (对比保留去色结构)**:
- 快速结构提取
- 无需预处理
- 首次使用下载约 350MB
- 适合：快速获取图像结构

#### 2.4 实用技巧

**技巧1: 风格迁移**
```
参考图: 梵高的星空
文本: a modern cityscape
结果: 梵高风格的现代城市
```

**技巧2: 角色一致性**
```
参考图: 角色草图或参考照片
文本: character in different poses, walking in the park
结果: 同一角色在不同场景
```

**技巧3: 多风格融合**
```
参考图1: 赛博朋克城市
参考图2: 水墨画风格
文本: a futuristic warrior
结果: 水墨风格的赛博朋克战士
```

**技巧4: 构图参考**
```
参考图: 电影截图或摄影作品
文本: my original character in this composition
结果: 保持参考图构图，替换内容
```

#### 2.5 常见问题

**问题1: 图像提示效果不明显**
- 解决: 增加参考图权重，或减少文本 prompt 的详细程度

**问题2: 多图像混合后质量下降**
- 解决: 减少参考图数量，或选择风格相近的图像

**问题3: 文本被图像完全覆盖**
- 解决: 使用更详细的文本描述，或降低图像影响

---

### 3. Inpaint or Outpaint (局部重绘与扩图)

#### 3.1 Inpaint (局部重绘)

**核心概念**: 重绘图像的特定区域，保持其他部分不变

**⚠️ 重要提示 1**: Inpaint 功能首次使用需要下载专用模型，请确保网络连接稳定！

**⚠️ 重要提示 2**: **图片上传和涂抹需要用户手动操作**，浏览器自动化无法完成！

**使用步骤**:

**步骤 1-2: 用户手动操作（必须）**
1. **上传图像**: 点击 "拖放图片至此处" 区域，选择本地图片文件
2. **涂抹蒙版**: 使用鼠标在图片上涂抹要重绘的区域（白色区域 = 要重绘的区域）
   - 涂抹技巧：可以稍微扩大涂抹范围，确保完全覆盖需要重绘的部分
   - 验证：确认能看到白色的涂抹蒙版区域

**步骤 3-6: 助手自动化配置**
3. **选择 Method**: "Modify Content (add objects, change background, etc.)"
4. **在 Inpaint Additional Prompt 中输入描述**（不是主 Prompt！）
5. 点击 Generate
6. **首次使用会下载模型**，请耐心等待

**选项说明**:

| 选项 | 功能 | 推荐使用场景 |
|------|------|-------------|
| **Enable Advanced Masking Features** | 启用高级蒙版功能 | 需要精确控制蒙版时 |
| **Method** | 选择重绘算法 | 根据需求选择 |
| **Inpaint or Outpaint (default)** | 默认算法 | 一般修复 |
| **Improve Detail** | 改善细节 | 面部/手部细节增强 |
| **Modify Content** | 修改内容 | 更换/添加元素 |

**Prompt 填写位置（重要！）**:
- ❌ **不要在主 Prompt 区域填写**（页面顶部的文本框）
- ✅ **必须在 Inpaint Additional Prompt 中填写**（Inpaint 面板内的文本框）
- ❌ **不需要填写 Negative Prompt**（Inpaint 会自动处理）

**正确配置示例**:
```
主 Prompt: [留空]
Negative Prompt: [留空]
Method: Modify Content (add objects, change background, etc.)
Inpaint Additional Prompt: human face, normal human head, blonde hair, natural skin tone, detailed face
```

**实用技巧**:

**技巧1: 修复瑕疵**
```
场景: 生成的图像手部有问题
操作: 涂抹手部区域，prompt: "perfect hand, detailed fingers"
```

**技巧2: 更换元素**
```
场景: 把角色的衣服换成红色
操作: 涂抹衣服区域，prompt: "red dress, elegant fabric"
```

**技巧3: 添加元素**
```
场景: 在场景中添加一只猫
操作: 涂抹要添加猫的区域，prompt: "a cute cat sitting here"
```

**技巧4: 面部修复**
```
场景: 角色面部细节不够
操作: 涂抹面部，prompt: "detailed face, beautiful eyes, sharp features"
```

#### 3.2 Outpaint (扩图)

**核心概念**: 向外扩展图像，生成原图之外的内容

**使用步骤**:
1. 上传图像
2. 选择扩图方向 (Left/Right/Top/Bottom)
3. 输入描述扩展内容的 prompt
4. 点击 Generate

**方向选择**:

| 方向 | 用途 |
|------|------|
| **Left** | 向左扩展 |
| **Right** | 向右扩展 |
| **Top** | 向上扩展 |
| **Bottom** | 向下扩展 |
| **组合** | 可同时选择多个方向 |

**实用技巧**:

**技巧1: 改变画幅比例**
```
场景: 把竖图变成横图
操作: 选择 Left + Right，生成两侧内容
```

**技巧2: 全景图制作**
```
场景: 制作宽屏风景
操作: 多次使用 Outpaint (Left/Right)，逐步扩展
```

**技巧3: 添加背景**
```
场景: 角色只有半身，想添加全身和背景
操作: 选择 Bottom，prompt: "full body, standing on grass, blue sky"
```

**技巧4: 构图调整**
```
场景: 主体太居中，想调整构图
操作: 向一侧扩展，创造留白空间
```

#### 3.3 Inpaint vs Outpaint 对比

| 功能 | 修改范围 | 使用场景 | 蒙版要求 |
|------|----------|----------|----------|
| **Inpaint** | 图像内部区域 | 修复、替换、添加元素 | 需要涂抹蒙版 |
| **Outpaint** | 图像外部区域 | 扩展画幅、添加背景 | 选择方向即可 |

#### 3.4 高级组合技巧

**组合1: Outpaint + Inpaint**
```
步骤1: Outpaint 扩展画面
步骤2: Inpaint 修复扩展区域的瑕疵
步骤3: Upscale 获得高清最终图
```

**组合2: Inpaint + Image Prompt**
```
步骤1: 上传基础图像
步骤2: 使用 Image Prompt 提供风格参考
步骤3: Inpaint 重绘特定区域，融合新风格
```

**组合3: Outpaint + Variation**
```
步骤1: Outpaint 扩展画面
步骤2: 对结果使用 Vary (Subtle) 微调
步骤3: 选择最佳版本
```

---

### 4. Enhance (图像增强)

#### 4.1 功能说明

**核心概念**: 自动提升图像质量和细节

**适用场景**:
- 提升低质量图像
- 增强细节和清晰度
- 改善色彩和对比度

#### 4.2 使用方式

**方式1: 独立 Enhance 功能**
- Input Image → Enhance 标签
- 直接上传图像增强

**方式2: 结合生成**
- 在生成设置中调整参数
- Sharpness、Guidance Scale 等

#### 4.3 参数调优

| 参数 | 默认值 | 作用 | 建议 |
|------|--------|------|------|
| **Sharpness** | 2 | 锐度 | 动漫1.5-2，写实2.5-3 |
| **Guidance Scale** | 6 | 引导强度 | 越高越艺术化 |

#### 4.4 实战技巧

**技巧1: 老照片修复**
```
输入: 模糊的老照片
操作: Enhance 功能 + 适当提高 Sharpness
结果: 清晰化的修复照片
```

**技巧2: 细节增强**
```
输入: 细节不足的生成图
操作: 使用 Inpaint 涂抹细节区域 + Enhance
结果: 细节丰富的图像
```

**技巧3: 批量增强**
```
场景: 多张图像需要统一增强
操作: 使用相同参数依次处理，保持风格一致
```

---

### 5. Describe (图像描述)

#### 5.1 功能说明

**核心概念**: 自动生成图像的文本描述 (反推 prompt)

**适用场景**:
- 学习优秀图像的 prompt 写法
- 复现喜欢的图像风格
- 批量处理图像获取描述

#### 5.2 使用技巧

**技巧1: 学习 Prompt**
```
操作: 上传喜欢的图像，获取 Describe 结果
学习: 分析生成的 prompt 结构和关键词
应用: 修改后用于自己的生成
```

**技巧2: 批量处理**
```
场景: 整理大量图像
操作: 使用 Describe 获取每张图的描述
用途: 建立图像库、标签管理
```

---

### 6. Metadata (元数据)

#### 6.1 功能说明

**核心概念**: 查看图像的生成参数

**包含信息**:
- Prompt (正面提示词)
- Negative Prompt (负面提示词)
- Seed (随机种子)
- Styles (使用的风格)
- Performance (性能模式)
- 其他生成参数

#### 6.2 使用场景

**场景1: 复现结果**
```
操作: 查看 Metadata 获取完整参数
应用: 使用相同参数重新生成
```

**场景2: 参数学习**
```
操作: 分析优秀图像的完整参数
学习: 了解哪些参数组合效果好
```

**场景3: 版本管理**
```
操作: 保存 Metadata 用于记录
用途: 追踪不同版本的生成参数
```

---

### 7. 综合实战 workflow

#### workflow 1: 从草图到成品
```
步骤1: 手绘草图或简单线稿
步骤2: Image Prompt (草图) + 文本描述
步骤3: 生成基础图像
步骤4: Inpaint 修复细节问题
步骤5: Vary (Subtle) 微调优化
步骤6: Upscale (2x) 获得高清成品
```

#### workflow 2: 风格迁移创作
```
步骤1: 准备参考图 (目标风格)
步骤2: Image Prompt (参考图) + 新内容描述
步骤3: 生成风格化图像
步骤4: Outpaint 扩展构图
步骤5: Inpaint 调整细节
步骤6: Enhance 最终优化
```

#### workflow 3: 角色一致性系列
```
步骤1: 生成基础角色图
步骤2: 使用相同 Seed + Vary (Subtle) 生成表情变化
步骤3: Image Prompt (基础图) + 不同场景描述
步骤4: Inpaint 调整服装细节
步骤5: Upscale 所有图像统一高清
```

#### workflow 4: 全景场景制作
```
步骤1: 生成核心场景
步骤2: Outpaint (Left) 扩展左侧
步骤3: Outpaint (Right) 扩展右侧
步骤4: 使用 Vary (Subtle) 统一风格
步骤5: Inpaint 修复接缝处
步骤6: Upscale 获得超宽全景图
```

---

### 3. 右侧面板 - 四个标签页

#### 3.1 Settings (设置)

| 设置项 | 说明 |
|--------|------|
| **Preset** | 预设: `initial`, `anime`, `default`, `lcm`, `lightning`, `playground_v2.5`, `pony_v6`, `realistic`, `sai` |
| **Performance** | 性能: `Quality`, `Speed`, `Extreme Speed`, `Lightning`, `Hyper-SD` |
| **Aspect Ratios** | 宽高比选择 |
| **Image Number** | 生成数量: 1-32张 |
| **Output Format** | 输出格式: `png`, `jpeg`, `webp` |
| **Negative Prompt** | 负面提示词 |
| **Random** | 随机种子 |
| **History Log** | 历史记录 |

#### 3.2 Styles (风格) - ⚠️ 关键

**⚠️ 重要经验：Style 是多选框，混合不同风格会产生意外效果！**

| 风格类型 | 说明 | 适用场景 |
|----------|------|----------|
| **SAI Anime** | 纯2D动漫风格 | 日式动漫 |
| **MRE Anime** | 另一种动漫风格 | 搭配 SAI Anime |
| **MRE Manga** | 漫画风格 | 黑白漫画 |
| **Fooocus V2** | 默认增强 | ⚠️ 增加写实感 |
| **Fooocus Semi Realistic** | 半写实 | ⚠️ 3D/写实混合 |
| **Fooocus Masterpiece** | 杰作增强 | ⚠️ 增加写实感 |
| **Fooocus Enhance** | 图像增强 | ⚠️ 增加写实感 |
| **Fooocus Sharp** | 锐化 | ⚠️ 增加写实感 |

**🎯 风格选择黄金法则：**

1. **纯2D动漫** (关键经验 2026-03-08):
   - ✅ `SAI Anime`, `MRE Anime`
   - ❌ **必须取消所有 Fooocus 系列** (V2, Semi Realistic, Masterpiece, Enhance, Sharp)
   - ⚠️ **即使使用 `anime` preset，如果勾选了 Fooocus 风格，仍然会产生3D效果！**
   - 💡 **启动方式**: 必须使用 `run_anime.bat`，不能用 `run.bat`

2. **写实/照片**:
   - ✅ `Fooocus V2`, `Fooocus Enhance`, `Fooocus Sharp`
   - ❌ 取消所有 Anime 风格

3. **⚠️ 绝对不要混用** 写实组和动漫组！会产生3D/2D混合的怪异效果

**风格冲突示例** (错误配置):
```
❌ Fooocus V2 + SAI Anime → 3D/2D混合
❌ Fooocus Semi Realistic + MRE Anime → 写实/动漫混合
```

**正确配置示例** (纯2D动漫):
```
✅ 仅 SAI Anime + MRE Anime → 纯正2D动漫
```

📖 **完整风格手册**: 查看 [STYLES.md](./STYLES.md) 获取所有 200+ 风格的详细说明和分类

#### 3.3 Models (模型)

| 设置项 | 说明 |
|--------|------|
| **Base Model** | 基础模型 (SDXL only) |
| **Refiner** | 精炼模型 (可选) |
| **LoRA 1-5** | LoRA 模型 (可勾选启用) |
| **Weight** | LoRA 权重 0-2 |
| **🔄 Refresh** | 刷新模型列表 |

#### 3.4 Advanced (高级)

| 参数 | 默认值 | 说明 |
|------|--------|------|
| **Guidance Scale** | 6 | 引导比例，越高越艺术化 |
| **Image Sharpness** | 2 | 图像锐度 |
| **Developer Debug Mode** | - | 调试模式 |

---

### 4. 图像预览区域

- **位置**: 页面顶部中央
- **操作**: 点击缩略图切换、Download下载、清除清空

---

## 🧪 实战经验与踩坑记录

### 使用规则：持续学习与更新

**重要原则**：每次使用 Fooocus 后，如果获得新的经验或用户反馈指出问题，必须更新此 SKILL.md 文档。

**判断是否需要记录的标准**：
1. 用户明确指出某个配置导致意外结果
2. 发现新的踩坑点或解决方案
3. 成功解决一个之前未记录的问题
4. 用户反馈某个 workflow 特别有效

**更新格式**：
```markdown
### [日期] - [简短标题]

**问题/经验**: [描述]

**解决方案/结论**: [具体做法]

**参考案例**: [如果有具体例子]
```

---

### 2026-03-08 - 纯2D动漫风格生成完整经验

**问题**: 使用 `run_anime.bat` 启动并勾选 SAI Anime，但生成的图像仍然有3D/写实混合效果

**根本原因**: 
- 虽然使用了 `anime` preset，但 Styles 中仍然勾选了 `Fooocus V2` 等写实增强风格
- **Fooocus V2/Semi Realistic/Masterpiece/Enhance/Sharp 会强制增加写实/3D效果**，与动漫风格冲突

**解决方案** (必须同时满足):
1. ✅ 使用 `run_anime.bat` 启动 (`--preset anime`)
2. ✅ **仅勾选 `SAI Anime` + `MRE Anime`**
3. ✅ **取消所有 Fooocus 系列风格** (V2, Semi Realistic, Masterpiece, Enhance, Sharp)
4. ✅ Negative Prompt 必须包含: `3d, realistic, photorealistic`
5. ✅ Prompt 中加入动漫关键词: `kawaii, moe, big eyes, cel shaded, japanese anime style`

**验证案例 - 僵尸女孩动漫化**:
```
启动: run_anime.bat
Styles: ✅ SAI Anime, ✅ MRE Anime, ❌ 所有 Fooocus 系列
Prompt: masterpiece, best quality, 1girl, zombie girl, undead, white hair, torn dress, horror character, anime style, detailed face, looking at viewer, dark atmosphere, anime aesthetic, 2d illustration, vibrant colors, high detail, kawaii, moe, big eyes, cel shaded, japanese anime style
Negative: 3d, realistic, photorealistic, lowres, bad anatomy...
结果: 纯正2D动漫风格，无3D混合
```

**风格分组法则**:
| 组别 | 风格 | 效果 | 兼容性 |
|------|------|------|--------|
| 纯2D动漫组 | SAI Anime, MRE Anime, MRE Manga | 纯正2D | ✅ 内部可混用 |
| 写实增强组 | Fooocus V2, Semi Realistic, Masterpiece, Enhance, Sharp | 3D/写实 | ❌ 不要与动漫组混用 |
| 照片写实组 | Fooocus Photograph, SAI Photographic, Photo 系列 | 照片级 | ✅ 内部可混用 |
| 艺术风格组 | Artstyle 系列, Mk 系列 | 艺术化 | ✅ 可与其他组少量混用 |
| 游戏风格组 | Game 系列 | 游戏化 | ✅ 内部可混用 |

**重要教训**: 
- `run_anime.bat` 只是设置了基础配置，**Styles 的选择完全独立于 preset**
- 即使 preset 是 anime，如果勾选了 Fooocus Semi Realistic，仍然会产生3D效果
- **Styles 是多选框，混合不同组别会产生不可预期的结果**

---

### 🎨 通用风格配置推理（基于纯2D动漫经验）

**核心原则**: 不同风格组别之间不要混用，同一组别内部可以混用

#### 1. 纯2D动漫风格（已验证）
```
启动: run_anime.bat
Styles: ✅ SAI Anime + MRE Anime
排除: ❌ 所有 Fooocus 系列
Prompt: 加入 kawaii, moe, big eyes, cel shaded
Negative: 排除 3d, realistic, photorealistic
```

#### 2. 照片写实风格（推理）
```
启动: run.bat 或 run_realistic.bat
Styles: ✅ Fooocus Photograph + SAI Photographic + Photo 系列
排除: ❌ 所有 Anime/Manga 系列
Prompt: 加入 photorealistic, detailed, 8k, professional photography
Negative: 排除 anime, cartoon, illustration, painting
```

#### 3. 写实增强风格（推理）
```
启动: run.bat
Styles: ✅ Fooocus V2 + Fooocus Masterpiece + Fooocus Enhance + Fooocus Sharp
排除: ❌ 所有 Anime/Manga/Photographic 系列
Prompt: 加入 masterpiece, best quality, highly detailed, professional
Negative: 排除 low quality, blurry, amateur
```

#### 4. 艺术绘画风格（推理）
```
启动: run.bat
Styles: ✅ Artstyle 系列（如 Artstyle Oil Painting, Artstyle Watercolor）
可选: ✅ Mk 系列（如 Mk Van Gogh, Mk Singer Sargent）
排除: ❌ Fooocus V2, Photographic（会冲突）
Prompt: 加入 artistic, painting style, brush strokes, canvas texture
Negative: 排除 photorealistic, 3d render, digital art
```

#### 5. 游戏风格（推理）
```
启动: run.bat
Styles: ✅ Game 系列（如 Game Zelda, Game Cyberpunk Game）
排除: ❌ Photographic, Artstyle（会冲突）
Prompt: 加入 game art, stylized, vibrant colors, game screenshot
Negative: 排除 photorealistic, blurry, low poly（除非需要）
```

#### 6. 科幻/未来风格（推理）
```
启动: run.bat
Styles: ✅ Futuristic 系列（如 Futuristic Cyberpunk, Futuristic Sci Fi）
可选: ✅ MRE Dark Cyberpunk
排除: ❌ Artstyle Renaissance, Photo Film Noir（会冲突）
Prompt: 加入 cyberpunk, neon lights, futuristic, sci-fi, high tech
Negative: 排除 medieval, vintage, old fashioned
```

**通用配置检查清单**:
- [ ] 是否使用了正确的启动方式？（anime/realistic/default）
- [ ] Styles 是否来自同一组别？
- [ ] 是否排除了冲突组别的 Styles？
- [ ] Prompt 是否包含该风格的关键词？
- [ ] Negative Prompt 是否排除了相反风格的关键词？

---

### 2026-03-08 - 浏览器自动化限制：文件上传和涂抹操作

**问题**: 使用浏览器自动化无法完成 Inpaint 的图片上传和涂抹操作

**根本原因**:
- **浏览器安全限制**: 无法通过 JavaScript 自动选择本地文件（系统文件选择器需要用户手动交互）
- **Gradio 文件上传机制**: `browser(action="upload")` 返回成功但图片未正确显示在 Inpaint 区域
- **Canvas 涂抹限制**: 无法通过自动化脚本在图像编辑器上进行涂抹操作

**解决方案**:
1. **用户手动上传**（推荐）：
   - 用户点击 "拖放图片至此处" 区域
   - 在系统文件选择器中选择目标图片
   - 验证图片是否正确显示在 Inpaint 区域

2. **用户手动涂抹**（必须）：
   - 用户使用鼠标在图片上涂抹要重绘的区域
   - 涂抹区域会显示为白色蒙版
   - 确保涂抹范围覆盖需要重绘的全部区域

3. **助手负责其他配置**（自动化）：
   - 选择 Method: Modify Content
   - 填写 Inpaint Additional Prompt
   - 配置 Styles、Performance 等参数
   - 点击 Generate 开始生成

**工作流程**:
```
用户操作：                      助手操作：
├─ 启动 Fooocus                 ├─ 等待用户完成上传和涂抹
├─ 上传图片到 Inpaint 区域      ├─ 配置 Method
├─ 涂抹重绘区域（白色蒙版）     ├─ 填写 Inpaint Additional Prompt
└─ 通知助手继续                 ├─ 配置其他参数
                                └─ 点击 Generate
```

**验证清单**:
- [ ] 图片是否正确显示在 Inpaint 区域？（不是 "拖放图片至此处"）
- [ ] 是否能看到涂抹的白色蒙版区域？
- [ ] Method 是否已选择 Modify Content？
- [ ] Inpaint Additional Prompt 是否已填写？

---

### 2026-03-08 - Inpaint 功能首次使用需要下载模型

**问题**: 点击 Generate 后页面回到初始状态，没有生成结果，命令窗口显示 "请按任意键继续..."

**根本原因**: 
- **Inpaint 功能需要额外下载专用模型**（inpainter 模型）
- 首次使用 Inpaint 时，Fooocus 会自动下载所需模型文件
- 如果网络不稳定或被墙，下载会失败，导致功能无法使用

**解决方案**:
1. **手动下载模型**（推荐）：
   - 从可靠来源下载 Inpaint 模型文件
   - 放置到 Fooocus 的 models 目录
   - 具体路径：`Fooocus/models/inpaint/`

2. **网络修复后重试**：
   - 确保网络连接稳定
   - 可能需要科学上网
   - 重新启动 Fooocus 并再次尝试

3. **验证模型是否下载成功**：
   - 检查 `Fooocus/models/` 目录是否有新的 inpaint 相关文件
   - 查看命令窗口输出，确认 "Downloading inpainter..." 变为 "Loading inpainter..."

**重要提示**:
- Inpaint 模型通常较大（几百 MB 到几 GB）
- 下载时间取决于网络速度
- 下载完成后，后续使用 Inpaint 功能就不需要再次下载了

**首次使用 Inpaint 的完整流程**:
```
1. 配置 Inpaint 参数（图片、涂抹区域、Method、Inpaint Additional Prompt）
2. 点击 Generate
3. Fooocus 自动检测并下载所需模型（首次）
4. 等待下载完成
5. 开始生成
```

---

### RTX 5060 兼容性修复

**问题**: RTX 5060 (sm_120) 与 PyTorch 2.1.0+cu121 不兼容

**症状**:
```
NVIDIA GeForce RTX 5060 with CUDA capability sm_120 is not compatible
```

**解决方案**:
```bash
# 1. 升级 PyTorch 到 nightly CUDA 12.8
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128

# 2. 降级 numpy (解决依赖冲突)
pip install numpy==1.26.4
```

### Preset vs Styles 关系理解

**重要区别**:
- **Preset (预设)**: 大方向配置，决定基础模型和默认参数
- **Styles (风格)**: 微调细节，可以叠加多个

**Preset 选择建议**:
| 目标 | Preset | 说明 |
|------|--------|------|
| 纯动漫 | `anime` | 使用动漫优化配置 |
| 写实照片 | `realistic` | 使用写实优化配置 |
| 快速测试 | `lightning` | 最快生成速度 |
| 通用 | `default` | 平衡配置 |

**关键经验**: 
- 即使选择 `anime` preset，如果勾选了 `Fooocus Semi Realistic` style，仍然会产生3D效果！
- Preset 和 Styles 是独立的，需要同时正确配置

### 风格选择踩坑

**错误配置** (产生3D/写实混合):
- ✅ Fooocus V2 + Fooocus Enhance + Fooocus Sharp + SAI Anime

**正确配置** (纯2D动漫):
- ❌ 取消所有 Fooocus 系列
- ✅ 只留 SAI Anime + MRE Anime

**风格分组理解**:

**写实增强组** (会产生3D/写实效果):
- Fooocus V2
- Fooocus Semi Realistic ⚠️ 最容易导致3D化
- Fooocus Masterpiece
- Fooocus Enhance
- Fooocus Sharp
- Fooocus Photograph

**纯2D动漫组**:
- SAI Anime
- MRE Anime
- MRE Manga
- Misc Manga

**艺术风格组**:
- SAI Digital Art
- SAI Fantasy Art
- Artstyle 系列
- 各种艺术流派风格

### Prompt 语言选择

**❌ 中文描述** (效果差):
```
楚轩，无效恐怖，半身像，动漫风格
```

**✅ 英文 SD 语法** (效果好):
```
masterpiece, best quality, 1boy, solo, half body, black hair, short hair, glasses, calm expression, school uniform, looking at viewer, detailed face, anime style, chuunibyou demo koi ga shitai style, kyoto animation style
```

### Prompt 权重语法

Fooocus 支持 A1111 的权重语法：

```
I am (happy:1.5) today
```

- 值 > 1: 增强该词的影响
- 值 < 1: 减弱该词的影响
- 值 = 1: 默认影响

**示例**:
```
a (beautiful:1.3) girl with (long:0.8) hair
```

### Embedding 使用

Fooocus 支持 embedding 文件：
```
(embedding:file_name:1.1)
```

### Fooocus 自动优化

Fooocus 内置离线 GPT-2 prompt 处理引擎：
- 自动优化 prompt，无需复杂的 prompt engineering
- 短 prompt (如 "house in garden") 也能获得好结果
- 长 prompt (1000+ 词) 同样能处理好
- 采样改进确保结果始终美观

**建议**: 保持 prompt 简洁自然，Fooocus 会自动优化

### 负面提示词模板

```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, mutation, deformed, extra limbs, extra arms, extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed, mutated hands, 3d, realistic, photorealistic
```

### 批量生成建议

- 复杂 prompt 生成 4 张而非 2 张
- 更多选择 = 更高概率获得满意结果

### API vs 浏览器自动化

**API 尝试失败**:
- Gradio API 需要 153 个参数
- Gradio Client bug: `AttributeError: 'dict' object has no attribute 'replace'`

**浏览器自动化成功**:
- 使用 Playwright 控制浏览器
- 直接操作 UI 元素
- 更可靠

### 启动方式选择

**Windows 推荐方式**:
- 使用 `run_anime.bat` 或 `run.bat` 启动
- 会自动激活 embedded Python 环境
- 避免与系统 Python 冲突

**启动参数经验**:
- `--preset anime` 自动选择动漫配置
- `--always-low-vram` 低显存模式
- `--disable-update-check` 加快启动速度

### 模型下载经验

**首次启动**:
- 会自动下载约 6-10GB 的模型文件
- 下载速度取决于网络
- 可以手动下载放到 `models/checkpoints/` 目录

**模型位置**:
- 基础模型: `Fooocus/models/checkpoints/`
- LoRA 模型: `Fooocus/models/loras/`
- VAE 模型: `Fooocus/models/vae/`
- ControlNet 模型: `Fooocus/models/controlnet/`

**Image Prompt 首次使用**:
- 会自动下载 2.5GB 的文件
- 包括 IP-Adapter 和相关组件

**PyraCanny/CPDS 首次使用**:
- 各需下载约 350MB 的控制模型

### 推荐模型来源

**Civitai** (https://civitai.com):
- 最大的 SD 模型社区
- 支持 SDXL 模型
- 可以直接搜索 "SDXL" 筛选

**Hugging Face**:
- 官方模型仓库
- Fooocus 默认模型来源

**手动下载放置**:
1. 下载 `.safetensors` 文件
2. 放到对应目录
3. 点击 "🔄 Refresh All Files" 刷新

### 生成参数调优经验

**Guidance Scale (引导比例)**:
- 默认值 6 适合大多数情况
- 值越高风格越明显，但可能过饱和
- 动漫风格建议 6-7

**Image Sharpness (锐度)**:
- 默认值 2
- 动漫风格可以适当降低到 1.5
- 写实风格可以提高到 2.5-3

**Performance 模式选择**:

| 模式 | Steps | 适用场景 |
|------|-------|----------|
| `Quality` | 30-60 | 最终输出，追求最佳质量 |
| `Speed` | 30 | 日常生成，平衡速度和质量 |
| `Extreme Speed` | 15-20 | 快速预览 |
| `Lightning` | 4-8 | 最快生成，质量略有下降 |
| `Hyper-SD` | 4-8 | 类似 Lightning |

**选择建议**:
- 迭代调试: `Lightning` 或 `Extreme Speed`
- 日常生成: `Speed`
- 最终输出: `Quality`

### 质量 vs 速度权衡

**快速测试流程**:
1. 使用 `Lightning` preset 快速生成草图
2. 找到满意的 seed 和构图
3. 切换到 `Quality` 模式生成最终版本

**批量生成策略**:
- 先用低质量模式生成多张
- 选择满意的再高质量重绘

### 网络问题处理

**h11 HTTP 协议错误**:
- 症状: `h11._util.LocalProtocolError: can't handle event type Response`
- 原因: 通常与 VPN 或代理有关
- 解决: 关闭 VPN 或更换网络环境

**WARNING: Invalid HTTP request received**:
- 症状: 控制台输出 `WARNING: Invalid HTTP request received`
- 原因: 网络环境问题，可能是代理/VPN/防火墙干扰
- **解决步骤**:
  1. **重新启动 Fooocus** (首选方案)
  2. 如果仍有问题，**关闭 VPN** 再试
  3. 如果关闭 VPN 不行，**开启 VPN** 再试
  4. **切换网络环境** (如从 WiFi 切换到有线，或更换网络)
  5. 检查系统代理设置，尝试关闭系统代理

**下载超时**:
- 模型下载时可能超时
- 可以手动下载模型文件
- 或使用国内镜像源

### 浏览器自动化操作指南

**使用 Playwright 控制 Fooocus**:

```python
# 1. 打开 Fooocus
browser(action="open", url="http://localhost:7865")

# 2. 获取页面快照
browser(action="snapshot", targetId="xxx")

# 3. 点击元素
browser(action="act", request={"kind": "click", "ref": "e24"})

# 4. 输入文本
browser(action="act", request={"kind": "type", "ref": "e22", "text": "prompt"})
```

**常用元素参考**:
- Generate 按钮: ref=e24
- Prompt 文本框: ref=e22
- Settings 标签: ref=e1074
- Styles 标签: ref=e1083
- Models 标签: ref=e1218
- Advanced 标签: ref=e1219

### 多图像生成功能

**图像预览区**:
- 生成完成后显示缩略图按钮
- 点击缩略图切换查看不同图像
- Download 按钮下载当前显示的图像
- 清除按钮清空图像

**批量生成策略**:
- Settings → Image Number 设置数量
- 建议复杂 prompt 生成 4 张
- 简单 prompt 2 张即可

### 风格搜索功能

**Styles 面板**:
- 顶部有搜索框: "🔎 Type here to search styles"
- 支持实时过滤
- 200+ 风格可用

**常用风格组合**:
- 京都动画风格: `SAI Anime` + `MRE Anime`
- 复古照片: `SAI Analog Film`
- 赛博朋克: `SAI Neonpunk` + `Futuristic Cyberpunk Cityscape`
- 油画: `Artstyle Impressionist`

### 负面提示词进阶

**基础负面** (必用):
```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry
```

**针对动漫** (额外添加):
```
3d, realistic, photorealistic, bad proportions
```

**针对写实** (额外添加):
```
cartoon, anime, illustration, painting, drawing
```

### 显存管理技巧

**低显存模式** (< 8GB):
- 启动时添加 `--always-low-vram`
- 降低分辨率到 768x768
- 使用 `Lightning` 或 `Hyper-SD` 模式

**高显存优化** (> 12GB):
- 可以使用 `--always-high-vram`
- 支持更高分辨率
- 可以同时加载更多 LoRA

### 常见错误及解决

**错误: `No CUDA GPUs are available`**
- 原因: CUDA 不可用或驱动问题
- 解决: 检查 NVIDIA 驱动，或尝试 CPU 模式

**错误: `CUDA out of memory`**
- 原因: 显存不足
- 解决: 降低分辨率，使用低显存模式，关闭其他程序

**错误: `Model not found`**
- 原因: 模型文件缺失
- 解决: 等待自动下载，或手动下载放置到正确目录

**错误: `Connection refused`**
- 原因: Fooocus 服务未启动
- 解决: 启动 Fooocus 服务，检查端口

**错误: `missing {'cond_stage_model.clip_g.transformer.text_model.embeddings.position_ids'}`**
- 原因: 模型加载时的警告，通常不影响使用
- 解决: 可以忽略，或更新模型文件

**错误: `Connection Errored out` / `1006`**
- 原因: Inpaint/Outpaint 时连接错误
- 解决: 检查模型文件完整性，重新启动 Fooocus

**警告: `WARNING: Invalid HTTP request received`**
- 原因: 网络环境问题，代理/VPN/防火墙干扰
- 解决: 
  1. 重新启动 Fooocus
  2. 关闭/开启 VPN 尝试
  3. 切换网络环境
  4. 检查系统代理设置

---

## 📚 社区经验总结 (来自 GitHub Discussions)

### 从 Midjourney 迁移到 Fooocus

Fooocus 设计目标是对标 Midjourney 的易用性：

| Midjourney | Fooocus |
|------------|---------|
| V1/V2/V3/V4 (变体) | Input Image → Upscale or Variation → Vary (Subtle/Strong) |
| U1/U2/U3/U4 (放大) | Input Image → Upscale or Variation → Upscale (1.5x/2x) |
| Inpaint/Pan | Input Image → Inpaint or Outpaint |
| Image Prompt | Input Image → Image Prompt |
| `--style` | Advanced → Style |
| `--stylize` | Advanced → Guidance |
| `--niji` | `run_anime.bat` 或 `--preset anime` |
| `--quality` | Advanced → Quality |
| `--ar` | Advanced → Aspect Ratios |
| `--no` | Advanced → Negative Prompt |
| Multi Prompts (::) | 多行 prompt |
| Prompt Weights | `(happy:1.5)` 格式 |

### Sharpness (锐度) 参数详解

**官方说明**: Sharpness 是 Fooocus 开发的解决 SDXL 过度平滑问题的方案。

**特点**:
- 不同于 CFG scale，不会影响图像全局结构
- 容易控制，不会过度处理
- 可以解决 90% 的 SDXL 过度平滑问题

**推荐值**:
- 默认值 2: 适合大多数情况
- 值 10: 增加细节和纹理
- 值 20: 更强的锐化效果

### Image Prompt (图像提示) 最佳实践

**Fooocus Image Prompt vs 标准 IP-Adapter**:

| 特性 | Midjourney | 标准 IP-Adapter (A1111/ComfyUI) | Fooocus |
|------|------------|----------------------------------|---------|
| 与文本 prompt 配合 | ✅ 混合良好 | ❌ 容易忽略文本 | ✅ 混合良好 |
| 多图像输入 | ✅ 质量不下降 | ❌ 质量下降 | ✅ 质量不下降 |
| 失败时表现 | 高质量但不相关 | 低质量过度处理 | 高质量但不相关 |
| 结果多样性 | ✅ 保持多样性 | ❌ 变化小 | ✅ 保持多样性 |

**高级功能**:
- **PyraCanny**: 金字塔 Canny 边缘控制，捕获更多细节
- **CPDS**: 快速结构提取，无需预处理

### 官方预设启动器说明

**2.1.60+ 版本提供 3 个启动器**:
- `run.bat` - 默认启动器
- `run_anime.bat` - 动漫优化配置
- `run_realistic.bat` - 写实优化配置

**如果没有多个启动器**:
- 运行 `run.bat` 会自动更新并创建所有启动器

### 开发者调试模式

**启用方式**: Advanced → Developer Debug Mode

**功能**:
- 可以混合 upscale/vary/inpaint 等高级功能
- 可以调整 denoising strength
- 可以查看 debug preprocessor 结果

**重要提醒**: 
> 如果你通过调整大量高级参数获得了满意结果，应该尝试复制 prompt，重启 Fooocus，不做任何修改直接生成。你会发现结果甚至更好，那些调整都是不必要的。（唯一例外可能是更换基础模型）

---

## 📖 完整实战案例

### 案例: 生成《中二病也要谈恋爱》风格的楚轩半身像

**目标**: 生成动漫角色楚轩的半身像，京都动画风格

**步骤 1: 启动 Fooocus**
```bash
cd D:\AI\Fooocus\Fooocus_win64_2-5-0\Fooocus_win64_2-5-0
run_anime.bat
```

**步骤 2: 配置 Settings**
- Preset: `anime`
- Performance: `Speed`
- Aspect Ratios: `896×1152 | 7:9`
- Image Number: `4`
- Output Format: `png`

**步骤 3: 配置 Styles** ⚠️ 关键
- ✅ SAI Anime
- ✅ MRE Anime
- ❌ Fooocus V2 (取消)
- ❌ Fooocus Semi Realistic (取消)
- ❌ Fooocus Masterpiece (取消)
- ❌ Fooocus Enhance (取消)
- ❌ Fooocus Sharp (取消)

**步骤 4: 输入 Prompt**
```
masterpiece, best quality, 1boy, solo, half body, black hair, short hair, glasses, calm expression, school uniform, looking at viewer, detailed face, anime style, chuunibyou demo koi ga shitai style, kyoto animation style, soft lighting, vibrant colors, high detail
```

**步骤 5: 输入 Negative Prompt**
```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, mutation, deformed, extra limbs, extra arms, extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed, mutated hands, 3d, realistic, photorealistic
```

**步骤 6: 生成并选择**
- 点击 Generate
- 等待生成完成
- 从4张中选择最符合预期的一张

**结果评估**:
- ✅ 纯2D动漫风格
- ✅ 京都动画特征明显
- ✅ 没有3D/写实混合效果
- ✅ 角色特征符合描述

---

## 📚 Fooocus 界面百科大全

### 界面层级结构

```
Fooocus Web UI (http://localhost:7865/)
├── 主生成区域 (左侧)
│   ├── Prompt 输入框
│   ├── Generate 按钮
│   └── 功能开关 (Input Image / Enhance / Advanced)
├── Input Image 子功能 (当 Input Image 勾选时显示)
│   ├── Upscale or Variation
│   ├── Image Prompt
│   ├── Inpaint or Outpaint
│   ├── Describe
│   ├── Enhance
│   └── Metadata
├── 右侧面板 (Settings / Styles / Models / Advanced)
│   ├── Settings 标签
│   ├── Styles 标签
│   ├── Models 标签
│   └── Advanced 标签
└── 底部状态栏
```

---

### 一、主生成区域详解

#### 1.1 Prompt 输入框
| 属性 | 说明 |
|------|------|
| **位置** | 页面左侧顶部 |
| **功能** | 输入生成图像的文本描述 |
| **语法** | 英文 Stable Diffusion 语法 |
| **最佳实践** | 使用逗号分隔关键词，越靠前的权重越高 |
| **示例** | `masterpiece, best quality, 1girl, anime style, detailed face` |

**Prompt 权重语法**:
- `(word)` - 权重 1.1 倍
- `((word))` - 权重 1.21 倍
- `(word:1.5)` - 权重 1.5 倍
- `[word]` - 权重 0.9 倍

#### 1.2 Generate 按钮
| 属性 | 说明 |
|------|------|
| **功能** | 开始生成图像 |
| **状态显示** | 生成中显示进度条和当前步骤 |
| **中断** | 点击 Stop 可中断生成 |
| **跳过** | 点击 Skip 跳过当前采样步骤 |

#### 1.3 功能开关

| 开关 | 功能 | 子功能 |
|------|------|--------|
| **Input Image** | 启用图像输入功能 | Upscale/Variation, Image Prompt, Inpaint, Describe, Enhance, Metadata |
| **Enhance** | 启用图像增强 | 独立功能，直接增强上传的图像 |
| **Advanced** | 显示高级设置 | Sharpness, Guidance Scale, Seed 等 |

---

### 二、Input Image 子功能详解

#### 2.1 Upscale or Variation

**功能层级**:
```
Upscale or Variation
├── Disabled (禁用)
├── Vary (Subtle) - 轻微变体
├── Vary (Strong) - 强烈变体
├── Upscale (1.5x) - 1.5倍放大
├── Upscale (2x) - 2倍放大
└── Upscale (Fast 2x) - 快速2倍放大
```

| 选项 | 功能 | 参数 | 适用场景 |
|------|------|------|----------|
| **Vary (Subtle)** | 轻微变化 | 变化 10-20% | 微调细节，保持主体 |
| **Vary (Strong)** | 强烈变化 | 变化 30-50% | 大幅改变，探索新可能 |
| **Upscale (1.5x)** | 1.5倍放大 | 中等速度 | 轻微放大，保持细节 |
| **Upscale (2x)** | 2倍放大 | 较慢，质量最高 | 大幅放大，最佳质量 |
| **Upscale (Fast 2x)** | 快速2倍放大 | 快，质量中等 | 快速预览，低显存 |

#### 2.2 Image Prompt (图像提示)

**功能层级**:
```
Image Prompt
├── 图像上传区域 (4个槽位)
├── Advanced (高级选项)
│   ├── PyraCanny (金字塔边缘控制)
│   └── CPDS (快速结构提取)
└── 图像权重控制
```

| 参数 | 功能 | 默认值 | 范围 |
|------|------|--------|------|
| **图像权重** | 控制参考图影响程度 | 1.0 | 0.0 - 2.0 |
| **停止步数** | 控制参考图影响时长 | 0.5 | 0.0 - 1.0 |

#### 2.3 Inpaint or Outpaint

**功能层级**:
```
Inpaint or Outpaint
├── 图像编辑区域 (Canvas)
├── Enable Advanced Masking Features (高级蒙版)
├── Method (方法选择)
│   ├── Inpaint or Outpaint (default)
│   ├── Improve Detail (face, hand, eyes, etc.)
│   └── Modify Content (add objects, change background, etc.)
├── Inpaint Additional Prompt (局部重绘提示词)
├── Outpaint Direction (扩图方向)
│   ├── Left / Right / Top / Bottom
└── Additional Prompt Quick List (快速提示词)
```

| 选项 | 功能 | 适用场景 |
|------|------|----------|
| **Inpaint or Outpaint (default)** | 默认算法 | 一般修复和扩图 |
| **Improve Detail** | 改善细节 | 面部/手部/眼睛细节增强 |
| **Modify Content** | 修改内容 | 更换/添加元素，改变背景 |

**Inpaint Additional Prompt**:
- 位置：Inpaint 面板内的文本框
- 功能：描述要在涂抹区域生成的内容
- 注意：不是主 Prompt！

#### 2.4 Describe (图像描述)

**功能层级**:
```
Describe
├── 图像上传区域
└── 生成按钮
```

| 属性 | 说明 |
|------|------|
| **输入** | 上传图像 |
| **输出** | 自动生成描述图像内容的文本 |
| **用途** | 反推 Prompt，学习优秀图像的描述方式 |

#### 2.5 Enhance (图像增强)

**功能层级**:
```
Enhance
├── 图像上传区域
└── 增强参数
```

| 参数 | 功能 | 默认值 | 建议值 |
|------|------|--------|--------|
| **Sharpness** | 锐度 | 2.0 | 动漫 1.5-2，写实 2.5-3 |

#### 2.6 Metadata (元数据)

**功能层级**:
```
Metadata
├── 图像上传区域
└── 显示生成参数
```

| 显示内容 | 说明 |
|----------|------|
| **Prompt** | 生成时使用的正向提示词 |
| **Negative Prompt** | 生成时使用的负向提示词 |
| **Seed** | 随机种子值 |
| **Model** | 使用的基础模型 |
| **Styles** | 应用的样式 |

---

### 三、右侧面板详解

#### 3.1 Settings 标签

**功能层级**:
```
Settings
├── Preset (预设)
├── Performance (性能)
├── Aspect Ratios (分辨率)
├── Image Number (生成数量)
├── Output Format (输出格式)
└── Negative Prompt (负向提示词)
```

| 选项 | 可选值 | 默认值 | 说明 |
|------|--------|--------|------|
| **Preset** | initial/anime/default/realistic/... | initial | 预设配置组合 |
| **Performance** | Quality/Speed/Extreme Speed/Lightning/Hyper-SD | Speed | 生成速度和质量 |
| **Aspect Ratios** | 多种分辨率 | 896×1152 | 输出图像尺寸 |
| **Image Number** | 1-32 | 2 | 一次生成数量 |
| **Output Format** | png/jpeg/webp | png | 输出文件格式 |
| **Negative Prompt** | 文本 | 空 | 排除的内容描述 |

**Performance 详细对比**:

| 模式 | 采样步数 | 速度 | 质量 | VRAM需求 |
|------|---------|------|------|----------|
| **Quality** | 30 | 慢 | 最高 | 高 |
| **Speed** | 20 | 中等 | 高 | 中 |
| **Extreme Speed** | 10 | 快 | 中等 | 低 |
| **Lightning** | 5 | 很快 | 较低 | 低 |
| **Hyper-SD** | 4 | 最快 | 低 | 最低 |

#### 3.2 Styles 标签

**功能层级**:
```
Styles
├── Search Styles (搜索框)
└── Selected Styles (已选样式列表)
    ├── Fooocus 官方系列
    ├── SAI 系列
    ├── MRE 系列
    ├── Ads 系列
    ├── Artstyle 系列
    ├── Futuristic 系列
    ├── Game 系列
    ├── Misc 系列
    ├── Papercraft 系列
    ├── Photo 系列
    └── Mk 系列
```

**样式分组**:

| 组别 | 包含样式 | 效果 | 兼容性 |
|------|---------|------|--------|
| **纯2D动漫组** | SAI Anime, MRE Anime, MRE Manga | 纯正2D | ✅ 内部可混用 |
| **写实增强组** | Fooocus V2, Semi Realistic, Masterpiece, Enhance, Sharp | 3D/写实 | ❌ 不与动漫组混用 |
| **照片写实组** | Fooocus Photograph, SAI Photographic, Photo 系列 | 照片级 | ✅ 内部可混用 |
| **艺术风格组** | Artstyle 系列, Mk 系列 | 艺术化 | ✅ 可少量混用 |
| **游戏风格组** | Game 系列 | 游戏化 | ✅ 内部可混用 |
| **科幻未来组** | Futuristic 系列 | 科幻感 | ✅ 内部可混用 |

#### 3.3 Models 标签

**功能层级**:
```
Models
├── Base Model (基础模型)
├── Refiner (精炼模型)
└── LoRAs (微调模型 x5)
```

| 选项 | 功能 | 说明 |
|------|------|------|
| **Base Model** | 主要生成模型 | 决定图像基础风格 |
| **Refiner** | 后期精炼模型 | 改善细节和质量 |
| **Refiner Switch** | 切换步数 | 何时切换到精炼模型 |
| **LoRA 1-5** | 微调模型 | 添加特定风格或角色 |

**常用基础模型**:

| 模型 | 风格 | 用途 |
|------|------|------|
| **juggernautXL** | 写实 | 照片级人像 |
| **animaPencilXL** | 动漫 | 2D动漫风格 |
| **realisticVision** | 写实 | 艺术写实 |
| **dreamshaperXL** | 通用 | 平衡质量和多样性 |

#### 3.4 Advanced 标签

**功能层级**:
```
Advanced
├── Guidance Scale (引导强度)
├── Sharpness (锐度)
├── ADM Scoring (ADM评分)
├── Seed (随机种子)
├── Sampler (采样器)
├── Scheduler (调度器)
└── Developer Debug Mode (开发者调试模式)
```

| 参数 | 功能 | 默认值 | 建议值 |
|------|------|--------|--------|
| **Guidance Scale** | 文本引导强度 | 6.0 | 4-8，越高越艺术化 |
| **Sharpness** | 图像锐度 | 2.0 | 动漫1.5-2，写实2.5-3 |
| **ADM Scaler Positive** | 正向ADM评分 | 1.5 | 一般保持默认 |
| **ADM Scaler Negative** | 负向ADM评分 | 0.8 | 一般保持默认 |
| **Seed** | 随机种子 | -1(随机) | 固定值可复现结果 |
| **Sampler** | 采样算法 | dpmpp_2m_sde_gpu | 一般保持默认 |
| **Scheduler** | 调度算法 | karras | 一般保持默认 |

---

### 四、启动器说明

#### 4.1 官方启动器

| 启动器 | 功能 | 适用场景 |
|--------|------|----------|
| **run.bat** | 默认启动 | 通用场景 |
| **run_anime.bat** | 动漫优化 | 生成2D动漫风格 |
| **run_realistic.bat** | 写实优化 | 生成照片级写实风格 |

#### 4.2 启动参数

```bash
# 基本启动
python entry_with_update.py

# 使用预设
python entry_with_update.py --preset anime

# 指定端口
python entry_with_update.py --port 7865

# 监听所有IP
python entry_with_update.py --listen 0.0.0.0
```

---

### 五、文件输出结构

```
Fooocus/outputs/
├── 2026-03-08/
│   ├── 2026-03-08_12-34-56_1234.png  # 生成的图像
│   ├── 2026-03-08_12-35-10_5678.png
│   └── log.html                       # 生成日志
├── 2026-03-07/
│   └── ...
└── ...
```

---

### 六、模型文件结构

```
Fooocus/models/
├── checkpoints/          # 基础模型 (.safetensors)
├── loras/               # LoRA 模型
├── inpaint/             # Inpaint 专用模型
├── upscale_models/      # 放大模型
├── controlnet/          # ControlNet 模型
└── ...
```

---

## 🎯 快速参考卡片

### 生成纯2D动漫 (完整配置)
```
启动: run_anime.bat (必须使用，不能用 run.bat)
Preset: anime
Performance: Quality (默认，除非用户要求速度)
Aspect Ratio: 896×1152 (7:9，适合人物)
Styles: 
  ✅ SAI Anime
  ✅ MRE Anime
  ❌ Fooocus V2 (必须取消)
  ❌ Fooocus Semi Realistic (必须取消)
  ❌ Fooocus Masterpiece (必须取消)
  ❌ Fooocus Enhance (必须取消)
  ❌ Fooocus Sharp (必须取消)
Prompt: 加入 kawaii, moe, big eyes, cel shaded, japanese anime style
Negative: 必须包含 3d, realistic, photorealistic
```

**生成前检查清单**:
- [ ] **启动方式**: 是否使用 run_anime.bat？
- [ ] **Performance**: 是否为 Quality？
- [ ] **Styles**: 是否只勾选了 SAI Anime + MRE Anime？
- [ ] **Styles**: 是否取消了所有 Fooocus 系列？
- [ ] **Prompt**: 是否包含 anime style, kawaii, moe, big eyes, cel shaded？
- [ ] **Negative**: 是否包含 3d, realistic, photorealistic？
- [ ] **验证**: 截图确认 Styles 面板状态

**常见错误**:
- ❌ 使用 run.bat + SAI Anime = 风格不够浓
- ❌ run_anime.bat + Fooocus V2 = 3D/2D混合
- ❌ 忘记排除 3d, realistic = 出现写实效果

### Describe 图像描述/Prompt 反推
```
用途: 分析图片内容并生成 Prompt
使用场景:
  - 看到喜欢的图片想知道 Prompt 怎么写
  - 想复现某种风格
  - 学习优秀的 Prompt 构造

步骤:
  1. Input Image: ✅ 勾选
  2. 切换到 Describe 标签
  3. 上传图片
  4. 点击 Generate
  5. 查看生成的描述文本

技巧:
  - 可基于生成的描述修改后再生成
  - 结合 Image Prompt 实现风格迁移
```

**生成前检查清单**:
- [ ] Input Image 是否已勾选？
- [ ] 是否切换到了 Describe 标签？
- [ ] 图片是否已成功上传？

**常见错误**:
- ❌ 在 Prompt 区域填写内容 → Describe 不需要 Prompt

### Upscale 超分辨率放大
```
用途: 将低分辨率图像放大到更高分辨率
使用场景:
  - 小图放大用于打印
  - 提升生成图像的细节和质量

步骤:
  1. Input Image: ✅ 勾选
  2. Upscale or Variation: ✅ 选择
  3. 选择放大倍数:
     - Upscale (1.5x): 轻微放大，保持细节
     - Upscale (2x): 大幅放大，最佳质量（推荐）
     - Upscale (Fast 2x): 快速放大，质量稍降
  4. 点击 Generate

workflow 建议:
  先生成小图测试 → 满意后使用 Upscale (2x)
  可多次使用 1.5x 逐步放大，比一次 2x 更稳定
```

**生成前检查清单**:
- [ ] Input Image 是否已勾选？
- [ ] Upscale or Variation 是否已选择？
- [ ] 放大倍数是否为 Upscale (2x)（推荐）？
- [ ] 原图是否已成功上传？

**常见错误**:
- ❌ 选择 Vary (Subtle/Strong) → 这是生成变体，不是放大
- ❌ 使用 2x 放大低质量原图 → 先确保原图质量足够

### Inpaint 局部重绘 (完整配置)
```
启动: 任意 (run.bat / run_anime.bat 均可)
Input Image: ✅ 勾选
Inpaint or Outpaint: ✅ 选择

步骤 1-2: 用户手动操作（浏览器自动化无法完成）
  1. 上传图片: 点击 "拖放图片至此处"，选择本地文件
  2. 涂抹区域: 用鼠标涂抹要重绘的区域（显示白色蒙版）
     ⚠️ 验证: 确认图片已显示，白色蒙版可见

步骤 3-7: 助手自动化配置
  3. Method: Modify Content (add objects, change background, etc.)
  4. Inpaint Additional Prompt: [填写要生成的内容]
     例如: human face, normal human head, blonde hair, detailed face
  5. 主 Prompt: [留空]
  6. Negative Prompt: [留空]
  7. 点击 Generate

注意: ⚠️ 首次使用需下载模型，请确保网络稳定！
```

**生成前检查清单（分角色）**:

**用户必须完成**:
- [ ] 图片是否正确显示在 Inpaint 区域？（不是 "拖放图片至此处"）
- [ ] 是否能看到涂抹的白色蒙版区域？

**助手必须完成**:
- [ ] Method 是否选择 Modify Content？
- [ ] Prompt 是否填写在 Inpaint Additional Prompt 中？
- [ ] 主 Prompt 是否留空？
- [ ] Negative Prompt 是否留空？
- [ ] 是否提醒用户首次使用需下载模型？
- [ ] 是否截图确认配置？

**常见错误**:
- ❌ Prompt 填在主 Prompt 区域 → 必须填在 Inpaint Additional Prompt
- ❌ 选择 Improve Detail → 这是改善细节，不是修改内容
- ❌ 忘记提醒用户手动上传/涂抹 → 浏览器自动化无法完成
- ❌ 首次使用未等待模型下载 → 页面会回到初始状态
- ❌ 主 Prompt 或 Negative Prompt 未清空 → 可能干扰生成

**故障排查**:
```
页面回到初始状态？
└─► 模型下载失败 → 检查网络，手动下载到 models/inpaint/

生成无效果？
└─► 检查 Prompt 是否在 Inpaint Additional Prompt 中

效果不符合预期？
└─► 检查 Method 是否为 Modify Content
└─► 检查涂抹区域是否覆盖目标区域
```

### 生成写实照片
```
Preset: realistic
Styles: Fooocus V2 + Fooocus Enhance + Fooocus Sharp
Negative: + cartoon, anime, illustration
```

### 快速测试
```
Preset: lightning
Performance: Extreme Speed
Steps: 4-8
```

### 高质量输出
```
Preset: anime/realistic
Performance: Quality
Styles: 根据需要选择
Image Number: 4
```

---

## 📊 Parameter Reference

### Core Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--prompt` | string | required | Main text prompt |
| `--negative-prompt` | string | "" | Things to avoid |
| `--output` | path | required | Output file path |
| `--preset` | string | "default" | Style preset |

### Quality Parameters

| Parameter | Type | Default | Range |
|-----------|------|---------|-------|
| `--quality` | int | 1 | 1-3 |
| `--steps` | int | 30 | 1-150 |
| `--guidance-scale` | float | 7.0 | 1.0-30.0 |
| `--sharpness` | float | 2.0 | 0.0-30.0 |

### Image Parameters

| Parameter | Type | Default |
|-----------|------|---------|
| `--aspect-ratio` | string | "1:1" |
| `--width` | int | 1024 |
| `--height` | int | 1024 |
| `--seed` | int | random |

---

## 🎭 Available Presets

| Preset | Description | Best For |
|--------|-------------|----------|
| `default` | Balanced | General |
| `anime` | Anime style | Anime, manga |
| `realistic` | Photorealistic | Photos |
| `lcm` | Latent Consistency | Fast generation |
| `lightning` | SDXL Lightning | Very fast |
| `playground_v2.5` | Playground v2.5 | Artistic |
| `pony_v6` | Pony Diffusion | Versatile |
| `sai` | Stable AI | Professional |

---

## 📐 Aspect Ratios

| Ratio | Dimensions | Best For |
|-------|------------|----------|
| `1:1` | 1024×1024 | Square |
| `4:3` | 1024×768 | Classic photos |
| `3:4` | 768×1024 | Portrait |
| `16:9` | 1024×576 | Widescreen |
| `9:16` | 576×1024 | Mobile |
| `21:9` | 1024×448 | Cinematic |

---

## 🔧 Troubleshooting

### Fooocus Not Running

**Solution**:
```bash
cd ~/Fooocus && python entry_with_update.py
# Wait for "Running on local URL: http://127.0.0.1:7865"
```

### Out of Memory

**Solutions**:
1. Reduce image size: `--width 768 --height 768`
2. Use lighter preset: `--preset lcm`
3. Enable low VRAM mode: `python entry_with_update.py --always-low-vram`

### Slow Generation

**Solutions**:
1. Use `--preset lightning` for fastest generation
2. Reduce steps: `--steps 20`
3. Check GPU: `nvidia-smi`

---

## 💡 Tips for Best Results

1. **Be Specific**: Detailed prompts yield better results
2. **Use Styles**: Leverage presets for consistent aesthetics
3. **Iterate**: Start with lower quality for faster iteration
4. **Negative Prompts**: Use to avoid common issues
5. **Batch Generate**: Create 4 variations to choose from
6. **Style Isolation**: Don't mix realistic and anime styles
7. **English Prompts**: Use SD-optimized English syntax

---

## 🚨 常见错误速查表

### 生成前自检清单
```
□ Styles 是否来自同一组别？（不要混用动漫组和写实组）
□ Performance 是否为 Quality？（除非用户要求速度）
□ Prompt 是否使用了英文 SD 语法？
□ Negative Prompt 是否排除了相反风格的关键词？
□ Inpaint 的 Prompt 是否在 Additional Prompt 中？
□ 是否提醒用户手动上传/涂抹？（Inpaint时）
```

### 错误现象与解决方案

| 错误现象 | 可能原因 | 解决方案 |
|---------|---------|---------|
| **3D/2D混合效果** | 混用了不同风格组（如 Fooocus V2 + SAI Anime） | 取消 Fooocus 系列，只保留 SAI/MRE Anime |
| **写实风格不够真实** | 使用了 anime preset 或勾选了动漫风格 | 使用 run_realistic.bat，勾选 Photographic 系列 |
| **动漫风格不够2D** | 使用了 run.bat 或勾选了 Fooocus V2 | 使用 run_anime.bat，仅勾选 SAI/MRE Anime |
| **Inpaint无效果** | Prompt填在主Prompt区域 | 填在 **Inpaint Additional Prompt** 中 |
| **Inpaint页面回到初始状态** | 首次使用需下载模型，网络失败 | 检查网络，手动下载模型到 models/inpaint/ |
| **生成速度极慢** | 使用了 Quality + 高分辨率 | 改用 Speed 模式或降低分辨率 |
| **Outpaint方向错误** | 选择了错误的方向 | 根据需求选择 Left/Right/Top/Bottom |
| **Image Prompt效果不明显** | 权重太低或参考图质量差 | 增加权重到 1.2-1.5，使用清晰的参考图 |
| **无法上传图片** | 浏览器自动化限制 | 提醒用户手动上传 |
| **无法涂抹蒙版** | 浏览器自动化限制 | 提醒用户手动涂抹 |
| **页面显示 Connection errored** | Fooocus服务未运行或崩溃 | 检查进程状态，重新启动 Fooocus |
| **模型下载失败** | 网络问题 | 关闭VPN/开启VPN，或手动下载模型 |

### 风格配置快速修复

**问题：风格不符合预期**

1. **检查启动方式**:
   - 动漫 → `run_anime.bat`
   - 写实 → `run.bat` 或 `run_realistic.bat`

2. **检查 Styles**:
   - 纯2D动漫：✅ SAI Anime, MRE Anime | ❌ 所有 Fooocus 系列
   - 照片写实：✅ Fooocus Photograph, Photo 系列 | ❌ 所有 Anime 系列
   - 写实增强：✅ Fooocus V2, Masterpiece, Enhance | ❌ Anime/Photographic

3. **检查 Prompt**:
   - 是否包含风格关键词？（如 anime style, photorealistic）
   - Negative Prompt 是否排除了相反风格？

### Inpaint 专项排查

**问题：Inpaint 不工作或效果差**

```
步骤1: 检查图片是否已上传
   └─► 是否显示 "拖放图片至此处"？→ 重新上传

步骤2: 检查蒙版是否已涂抹
   └─► 是否能看到白色蒙版区域？→ 重新涂抹

步骤3: 检查 Method
   └─► 是否选择了 Modify Content？→ 修改内容必须选这个

步骤4: 检查 Prompt 位置
   └─► 是否填在 Inpaint Additional Prompt？→ 不是主 Prompt！

步骤5: 检查模型是否已下载
   └─► 首次使用需下载 ~500MB 模型 → 检查网络，等待下载

步骤6: 检查生成状态
   └─► 页面是否回到初始状态？→ 下载失败，需手动修复
```

---

## 📚 Resources

### 官方资源
- [Fooocus GitHub](https://github.com/lllyasviel/Fooocus)
- [Fooocus Wiki](https://github.com/lllyasviel/Fooocus/wiki)
- [Fooocus Discussions](https://github.com/lllyasviel/Fooocus/discussions)

### 重要 Discussion 链接
- [#117 - Fooocus Advanced](https://github.com/lllyasviel/Fooocus/discussions/117) - 高级参数详解
- [#390 - Variation/Upscale](https://github.com/lllyasviel/Fooocus/discussions/390) - 变体和放大功能
- [#414 - Inpaint/Outpaint](https://github.com/lllyasviel/Fooocus/discussions/414) - 局部重绘和扩图
- [#557 - Image Prompts](https://github.com/lllyasviel/Fooocus/discussions/557) - 图像提示功能
- [#679 - Anime/Realistic Support](https://github.com/lllyasviel/Fooocus/discussions/679) - 动漫和写实预设

### 社区资源
- [Civitai](https://civitai.com) - SDXL 模型社区
- [SDXL Prompt Guide](https://stable-diffusion-art.com/sdxl-prompt/)
- [Hugging Face Fooocus Models](https://huggingface.co/lllyasviel)

---

## 🔬 社区进阶经验汇总 (2026-03-08 更新)

> **来源**: Fooocus GitHub Discussions & Issues
> 
> **核心资源**: [All 276 Styles Google Table](https://docs.google.com/spreadsheets/d/10UXU59fBA5wZrcEEvgv1MTf1MSNTCB5PT4fNxsAst8E) - 社区维护的完整风格对比表

### 一、风格选择深度解析

#### 1.1 风格交互原理

**核心发现：风格是乘法效应，不是加法**

来自社区大量测试的重要结论：
- 选择多个风格时，它们的效果会**相乘**，而不是简单叠加
- 冲突风格（如写实+动漫）会产生"塑料感"或"3D渲染感"artifacts
- 同类风格混用会**增强**该方向的特征，但过多会过饱和

**风格交互示例**:
```
SAI Anime (1.0) × MRE Anime (1.0) = 纯正2D动漫 (1.0)
SAI Anime (1.0) × Fooocus V2 (1.0) = 3D/2D混合 (0.6) ❌
Fooocus V2 (1.0) × Fooocus Enhance (1.0) = 写实增强 (1.2) ✅
```

#### 1.2 社区验证的最佳风格组合

| 目标风格 | 推荐组合 | 权重建议 | 效果评分 |
|---------|---------|---------|---------|
| **纯2D日式动漫** | SAI Anime + MRE Anime | 1:1 | ⭐⭐⭐⭐⭐ |
| **赛博朋克动漫** | SAI Anime + Futuristic Cyberpunk | 2:1 | ⭐⭐⭐⭐⭐ |
| **复古动漫** | SAI Anime + SAI Analog Film | 2:1 | ⭐⭐⭐⭐ |
| **照片级写实** | Fooocus Photograph + Photo 系列 | 1:1 | ⭐⭐⭐⭐⭐ |
| **艺术油画** | Artstyle Oil Painting + Mk 艺术家 | 1:1 | ⭐⭐⭐⭐ |
| **游戏概念** | Game 系列 + SAI Digital Art | 1:1 | ⭐⭐⭐⭐ |
| **科幻场景** | Futuristic Sci Fi + SAI Digital Art | 1:1 | ⭐⭐⭐⭐ |

#### 1.3 风格权重间接控制技巧

虽然 Fooocus 不直接支持风格权重，但可以通过以下方式控制：

**方法1: Prompt 强化**
```
# 增强动漫特征
masterpiece, best quality, anime style, anime style, anime style, 1girl...
# 重复关键词可间接提升该方向权重
```

**方法2: Negative Prompt 排除**
```
# 纯2D动漫时排除写实特征
3d, realistic, photorealistic, render, cgi, blender, 3d model

# 照片级写实时排除动漫特征  
anime, cartoon, illustration, manga, cel shaded, 2d
```

**方法3: Image Prompt 多图参考**
- 上传 2-4 张同风格参考图
- 每张图权重设为 0.8-1.2
- 效果比单图更强

---

### 二、CFG (Guidance Scale) 最佳实践

**来自社区测试的重要发现**:

| 模型 | 推荐 CFG | 效果描述 |
|-----|---------|---------|
| **juggernautXL** | 7.0 | 更真实、更详细的图像 |
| **juggernautXL** | 4.0 | 更快生成，但可能不够真实 |
| **DreamShaperXL** | 2.0 | 配合 Turbo 模型使用 |
| **SSD-1B** | 4.0 | 快速生成，质量适中 |

**CFG 选择建议**:
```
CFG 2-4:  宽松遵循提示，更多创意自由度
CFG 5-7:  平衡模式，推荐用于大多数场景
CFG 8-12: 严格遵循提示，可能过饱和
```

---

### 三、Prompt 工程最佳实践

#### 3.1 Prompt 结构模板

**通用结构** (社区推荐):
```
[质量前缀], [主体描述], [细节特征], [场景环境], [风格修饰], [视角构图], [光照效果]
```

**示例分解**:
```
masterpiece, best quality,              # 质量前缀
1girl, solo,                            # 主体描述
long silver hair, blue eyes, white dress, # 细节特征
standing in a flower field,             # 场景环境
anime style, detailed face,             # 风格修饰
looking at viewer, upper body,          # 视角构图
soft lighting, golden hour              # 光照效果
```

#### 2.2 质量前缀对比测试

社区测试不同质量前缀的效果：

| 前缀组合 | 效果评分 | 适用场景 |
|---------|---------|---------|
| `masterpiece, best quality` | ⭐⭐⭐⭐⭐ | 通用，推荐 |
| `masterpiece, best quality, ultra-detailed` | ⭐⭐⭐⭐⭐ | 高细节需求 |
| `masterpiece, best quality, official art` | ⭐⭐⭐⭐ | 官方插画风格 |
| `masterpiece, best quality, cinematic lighting` | ⭐⭐⭐⭐ | 电影感 |
| `best quality` (单独) | ⭐⭐⭐ | 简洁但效果稍弱 |
| `high quality` | ⭐⭐⭐ | 不如 best quality |

#### 2.3 视角和构图关键词

**视角关键词效果排序** (社区测试):
```
# 从强到弱
extreme close-up > close-up > portrait > upper body > full body > wide shot > aerial view
```

**构图关键词**:
```
dutch angle          # 荷兰角，倾斜构图
from above/below     # 俯视/仰视
from side            # 侧面
from behind          # 背面
profile              # 侧面轮廓
symmetrical          # 对称构图
rule of thirds       # 三分法
dynamic angle        # 动态角度
```

#### 2.4 光照效果关键词

**常用光照效果**:
```
soft lighting        # 柔和光照 (通用)
cinematic lighting   # 电影光照 (戏剧性)
rim lighting         # 轮廓光 (突出主体)
backlighting         # 逆光 (氛围感)
volumetric lighting  # 体积光 (光束效果)
golden hour          # 黄金时刻 (暖色调)
blue hour            # 蓝调时刻 (冷色调)
neon lights          # 霓虹灯 (赛博朋克)
sunlight             # 阳光 (自然)
studio lighting      # 摄影棚光 (专业)
```

---

### 四、性能优化与显存管理

#### 4.1 显存使用优化策略

**根据显存大小的配置建议**:

| 显存 | 推荐分辨率 | Performance | 并发数 | 特殊参数 |
|-----|-----------|-------------|--------|---------|
| 4-6GB | 768×768 | Lightning | 1 | `--always-low-vram` |
| 8GB | 896×1152 | Speed | 1 | `--always-low-vram` |
| 12GB | 1024×1024 | Quality | 1-2 | 无需特殊参数 |
| 16GB+ | 1024×1024+ | Quality | 2-4 | `--always-high-vram` |

#### 4.2 生成速度优化

**快速迭代 workflow**:
```
步骤1: Lightning 模式 (4步) 快速筛选构图
步骤2: Speed 模式 (20步) 验证细节
步骤3: Quality 模式 (30步) 最终输出
```

**社区验证的快速模型配置** (来自 Discussion #2082):

| 配置 | 生成时间 | 质量 | 适用场景 |
|-----|---------|------|---------|
| **DreamShaperXL_Turbo_v2** + CFG:2 + 8步 | 15-20秒 (1024×1024) | ⭐⭐⭐⭐ | 快速迭代 |
| **SSD-1B** + CFG:4 + 20步 | 10-15秒 (1024×1024) | ⭐⭐⭐ | 草图生成 |
| **DreamShaperXL_Turbo_v2** + CFG:2 + 8步 | 35-40秒 (1920×1080) | ⭐⭐⭐⭐ | 高清快速 |

**Turbo 模型使用技巧**:
```
模型: DreamShaperXL_Turbo_v2
CFG: 2.0 (必须低CFG)
Steps: 8
Sampler: dpmpp_sde_gpu
Scheduler: karras
```

**SSD-1B 模型优势**:
- 比 Speed 性能模式更快
- 模型体积小，加载快
- 适合快速预览和草图

**批量生成策略**:
- 先用 Speed 模式生成 4 张选最佳
- 用 Vary (Subtle) 在最佳基础上微调
- 最终用 Quality 模式输出

#### 4.3 模型加载优化

**减少模型切换时间**:
- 保持基础模型一致，使用 LoRA 切换风格
- 预加载常用模型到显存
- 使用 `--always-high-vram` 保持模型常驻

---

### 五、高级功能深度解析

#### 4.1 Image Prompt 进阶技巧

**多图混合策略**:
```
参考图1 (权重 1.0): 风格参考 (如梵高星空)
参考图2 (权重 0.8): 构图参考 (如电影截图)
参考图3 (权重 0.6): 色彩参考 (如配色方案)
文本 Prompt: 描述主体内容
```

**Image Prompt + 文本权重平衡**:
- 图像权重 0.8-1.2: 风格主导，文本辅助
- 图像权重 0.4-0.6: 文本主导，图像参考
- 图像权重 0.2 以下: 图像影响微弱

#### 4.2 Inpaint 高级技巧

**精细控制蒙版**:
```
技巧1: 涂抹时稍微超出目标区域边缘
技巧2: 复杂区域分多次 Inpaint
技巧3: 使用 Improve Detail 修复面部/手部
技巧4: 使用 Modify Content 更换服装/背景
```

**Inpaint 工作流程优化**:
```
步骤1: 生成基础图像
步骤2: 使用 Describe 反推 Prompt
步骤3: Inpaint 修复问题区域
步骤4: Vary (Subtle) 统一风格
步骤5: Upscale 最终输出
```

#### 4.3 Outpaint 创意应用

**全景图制作**:
```
步骤1: 生成核心场景 (896×512)
步骤2: Outpaint Left 扩展左侧
步骤3: Outpaint Right 扩展右侧
步骤4: 重复直到达到目标宽度
步骤5: 使用 Vary (Subtle) 统一接缝
```

**构图调整**:
```
场景: 主体太居中
操作: Outpaint 一侧创造留白
效果: 改善构图，增加艺术感
```

---

### 六、常见错误深度排查

#### 6.1 生成质量不佳的系统排查

**排查清单**:
```
□ 是否使用了正确的 Preset？
□ Styles 是否冲突？（写实+动漫）
□ Prompt 是否足够详细？
□ Negative Prompt 是否排除了干扰项？
□ Performance 是否为 Quality？
□ 分辨率是否合适？
□ Seed 是否固定？（固定seed便于对比）
```

#### 6.2 特定问题解决方案

**问题: CUDA kernel errors might be asynchronously reported**
```
症状: RuntimeError: CUDA error: the launch timed out and was terminated
原因: 显卡驱动或 CUDA 版本兼容性问题
解决:
1. 升级 Nvidia 驱动到最新版本 (推荐 53X 版本，不是 3XX 或 4XX)
2. 使用官方版本，避免修改版或 fork
3. 如果仍有问题，使用 CUDA 11 + Xformers:
   - 备份并删除 python_embeded 文件夹
   - 从 release 页面下载 "previous_old_xformers_env.7z"
   - 解压到 Fooocus 目录
   - 重新运行
```

**问题: RTX 50 系列显卡不支持 (sm_120)**
```
症状: NVIDIA GeForce RTX 5060 with CUDA capability sm_120 is not compatible
原因: PyTorch 2.1.0 不支持 sm_120 架构
解决:
1. 升级 PyTorch 到 nightly CUDA 12.8:
   pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
2. 降级 numpy 解决依赖冲突:
   pip install numpy==1.26.4
```

**问题: 人物面部崩坏**
```
原因: 分辨率过低或面部占比太小
解决:
1. 使用 896×1152 或更高分辨率
2. 使用 close-up 或 portrait 视角
3. 添加 detailed face 到 Prompt
4. 使用 Inpaint → Improve Detail 修复面部
```

**问题: 手部畸形**
```
原因: AI 对手部理解不足
解决:
1. 避免显示手部的构图 (from behind, hands in pockets)
2. 使用 Inpaint → Improve Detail 修复
3. 添加 perfect hands, detailed fingers 到 Prompt
4. 使用负面提示: bad hands, mutated hands
```

**问题: 图像过曝/过暗**
```
原因: 光照描述不当
解决:
1. 使用 soft lighting 替代强烈光照
2. 添加 balanced lighting 到 Prompt
3. 调整 Sharpness 参数 (降低锐度)
```

**问题: Colab 连接超时**
```
症状: Google Colab 断开连接
原因: 长时间无交互或网络问题
解决:
1. 使用 Colab 保持活动脚本
2. 定期检查连接状态
3. 考虑使用本地运行时
```

---

### 七、模型选择指南

#### 6.1 基础模型推荐

| 模型 | 风格 | 显存需求 | 推荐场景 |
|-----|------|---------|---------|
| **juggernautXL** | 写实 | 8GB+ | 照片级人像 |
| **animaPencilXL** | 动漫 | 6GB+ | 2D动漫风格 |
| **realisticVision** | 写实艺术 | 8GB+ | 艺术写实 |
| **dreamshaperXL** | 通用 | 8GB+ | 平衡质量和多样性 |
| **ponyDiffusion** | 通用 | 8GB+ | 高质量动漫和写实 |

#### 7.2 LoRA 使用技巧

**LoRA 叠加原则**:
- 最多同时加载 5 个 LoRA
- 总权重建议不超过 2.0
- 风格 LoRA 权重 0.6-1.0
- 角色 LoRA 权重 0.8-1.2

**热门 LoRA 类型**:
```
角色 LoRA: 特定动漫/游戏角色
风格 LoRA: 特定艺术家风格
服装 LoRA: 特定服装类型
姿势 LoRA: 特定姿势/动作
概念 LoRA: 特定主题 (赛博朋克、蒸汽朋克等)
```

---

### 八、workflow 模板库

#### 7.1 角色设计 workflow

```
步骤1: 基础生成
  - 使用 anime/realistic preset
  - 生成 4 张不同 seed 的草图
  - 选择最佳构图

步骤2: 风格细化
  - 固定 seed
  - 调整 Styles 组合
  - 微调 Prompt 细节

步骤3: 多角度生成
  - Image Prompt (基础图) + 不同角度描述
  - front view, side view, back view

步骤4: 表情变化
  - 相同 seed + Vary (Subtle)
  - happy, sad, angry, surprised

步骤5: 最终输出
  - Upscale (2x) 所有选定图像
  - 统一后期处理
```

#### 7.2 场景设计 workflow

```
步骤1: 构图探索
  - Lightning 模式快速生成 8 张
  - 选择最佳构图

步骤2: 细节深化
  - Speed 模式验证
  - 添加环境细节到 Prompt

步骤3: 风格统一
  - 固定 seed
  - 调整光照和氛围

步骤4: 扩展画面
  - Outpaint 扩展构图
  - 添加前景/背景元素

步骤5: 最终渲染
  - Quality 模式输出
  - Upscale 到目标分辨率
```

#### 7.3 风格迁移 workflow

```
步骤1: 准备参考
  - 收集 3-5 张目标风格参考图
  - 确保参考图质量高

步骤2: 基础生成
  - Image Prompt (参考图) + 新内容描述
  - 调整图像权重 0.8-1.2

步骤3: 风格微调
  - 调整 Styles 组合
  - 添加风格关键词到 Prompt

步骤4: 内容优化
  - Inpaint 修复不匹配区域
  - Vary (Subtle) 统一风格

步骤5: 最终输出
  - Quality 模式生成
  - 对比参考图验证风格一致性
```

---

## 🎯 实战场景指南

### 场景1：用户无法操作电脑时的灵活方案

**适用情况**：
- 用户无法手动上传图片或涂抹蒙版
- 需要快速生成概念图或角色设计
- 远程协助场景

**推荐方案：纯文本生成 + 精心设计的 Prompt**

**步骤1：图像分析**
```
1. 识别角色/主体特征（外貌、服装、姿态）
2. 确定目标风格（写实、动漫、油画等）
3. 分析需要保留和排除的元素
```

**步骤2：Prompt 设计**
```
# 正向 Prompt 结构
[角色身份], [外貌特征], [服装], [场景], [风格关键词], [质量前缀]

# 示例：科学家角色
William Birkin, human scientist, middle-aged man with blonde hair, 
wearing white lab coat, professional portrait, realistic, detailed face, 
soft lighting, scientific laboratory background, masterpiece, best quality
```

**步骤3：Negative Prompt 设计**
```
# 排除不需要的元素
monster, mutation, creature, beast, deformed, mutated, 
zombie, horror, scary, ugly, distorted, 3d, cartoon, anime
```

**步骤4：参数配置**
| 参数 | 推荐值 | 理由 |
|-----|-------|------|
| Preset | realistic/anime | 根据目标风格选择 |
| Performance | Speed | 快速生成多个选项 |
| Image Number | 4 | 提供选择空间 |
| Styles | 对应风格组合 | 增强目标风格效果 |

**实战案例：威廉·柏金人类形态还原**

*背景*：用户提供了 G 病毒变异形态的威廉·柏金图片，要求还原成人类科学家形态，但无法操作电脑。

*解决方案*：
1. **分析原图**：识别出角色身份、金发、白大褂等特征
2. **设计 Prompt**：强调 "human scientist"、"white lab coat"、"realistic"
3. **Negative Prompt**：排除 "monster"、"mutation"、"G-virus" 等变异特征
4. **生成结果**：成功生成符合要求的科学家形象

*关键经验*：
- 详细的 Prompt 可以弥补无法使用 Inpaint 的局限
- Negative Prompt 对排除不需要的元素至关重要
- 生成多张图片可以选择最接近需求的

---

### 场景2：角色设计 workflow

**目标**：为游戏/创作设计一致的角色形象

**步骤1：基础形象生成**
```
Prompt: [角色名称], [基础外貌], [服装], [风格], masterpiece, best quality
参数：Speed 模式，生成 4 张
```

**步骤2：选择最佳基础图**
- 选择构图和特征最符合的图像
- 记录使用的 Seed

**步骤3：多角度生成**
```
Prompt: [角色名称], [相同特征], front view, portrait
Prompt: [角色名称], [相同特征], side view, profile
Prompt: [角色名称], [相同特征], back view
固定 Seed + Vary (Subtle) 保持一致性
```

**步骤4：表情变化**
```
Prompt: [角色名称], [相同特征], happy expression
Prompt: [角色名称], [相同特征], serious expression
Prompt: [角色名称], [相同特征], angry expression
```

**步骤5：最终输出**
- Quality 模式生成高清版本
- Upscale 到目标分辨率

---

### 场景3：风格迁移 workflow

**目标**：将现有图像转换为特定艺术风格

**方案A：使用 Image Prompt（需要用户操作）**
```
1. 上传原图到 Image Prompt
2. 设置权重 0.8-1.2
3. 添加目标风格描述到 Prompt
4. 选择对应 Styles
5. 生成并微调
```

**方案B：纯文本重新生成（无需用户操作）**
```
1. 分析原图内容
2. 描述内容 + 目标风格
3. 使用详细 Prompt 生成
4. 多次迭代优化
```

**案例：写实照片转动漫风格**
```
Prompt: [原图内容描述], anime style, 2d illustration, 
cel shaded, vibrant colors, big eyes, kawaii, moe

Styles: SAI Anime + MRE Anime
Preset: anime (使用 run_anime.bat)
```

---

## 📝 Prompt 模板库

### 人物角色模板

**科学家/研究员**：
```
[姓名], human scientist, [年龄] years old, [发色] hair, 
wearing white lab coat, professional portrait, 
[实验室/办公室] background, realistic, detailed face, 
soft lighting, masterpiece, best quality
```

**动漫角色**：
```
[姓名], 1[性别], [发色] hair, [瞳色] eyes, 
[服装描述], [表情], anime style, detailed face, 
looking at viewer, [场景], masterpiece, best quality, 
kawaii, moe, cel shaded
```

**写实肖像**：
```
[姓名], professional portrait, [年龄] years old, 
[发色] hair, [瞳色] eyes, [服装], 
[场景], realistic, detailed face, 
soft lighting, masterpiece, best quality, 
photographic, high detail
```

### 场景模板

**科幻实验室**：
```
futuristic laboratory, high-tech equipment, 
blue lighting, clean white walls, 
scientific instruments, holographic displays, 
sci-fi atmosphere, detailed, masterpiece
```

**赛博朋克城市**：
```
cyberpunk cityscape, neon lights, rain, 
night scene, futuristic buildings, 
flying vehicles, vibrant colors, 
cinematic lighting, detailed, masterpiece
```

**奇幻森林**：
```
enchanted forest, magical atmosphere, 
glowing plants, ancient trees, 
mystical fog, fantasy art style, 
detailed, masterpiece, best quality
```

---

### 九、社区资源与持续学习

#### 9.1 推荐学习资源

**官方资源**:
- [Fooocus GitHub](https://github.com/lllyasviel/Fooocus) - 官方仓库
- [Fooocus Wiki](https://github.com/lllyasviel/Fooocus/wiki) - 官方文档
- [Fooocus Discussions](https://github.com/lllyasviel/Fooocus/discussions) - 社区讨论
- [Troubleshoot Guide](https://github.com/lllyasviel/Fooocus/blob/main/troubleshoot.md) - 官方故障排查

**重要 Discussion 主题**:
- #117 - 高级参数详解
- #390 - 变体和放大功能
- #414 - 局部重绘和扩图
- #557 - 图像提示功能
- #679 - 动漫和写实预设
- #2082 - [All 276 Styles Google Table](https://docs.google.com/spreadsheets/d/10UXU59fBA5wZrcEEvgv1MTf1MSNTCB5PT4fNxsAst8E) ⭐ 风格完整对比
- #3281 - Fooocus 2.5.0 Enhance 功能

**社区资源**:
- [Civitai](https://civitai.com) - SDXL 模型和 LoRA
- [Hugging Face](https://huggingface.co/lllyasviel) - 官方模型
- [SDXL Prompt Guide](https://stable-diffusion-art.com/sdxl-prompt/) - Prompt 指南
- [FoooXus Extender](https://github.com/toutjavascript/FoooXus-Fooocus-Extender) - 社区扩展工具

#### 9.2 持续更新机制

**本 Skill 的更新原则**:
1. 每次使用后记录新发现
2. 定期整理社区新经验
3. 验证后更新到 SKILL.md
4. 保持与 Fooocus 版本同步

**贡献方式**:
- 测试新的风格组合
- 分享成功的 workflow
- 报告问题和解决方案
- 完善故障排查指南

---

## License

Fooocus is released under the GPL-3.0 license. This skill is provided as-is for integration purposes.

---

> **文档维护**: 本 Skill 持续从 Fooocus 社区学习更新
> 
> **最后更新**: 2026-03-08
> 
> **版本**: 2.0 - 新增社区进阶经验、workflow 模板库、深度排查指南
