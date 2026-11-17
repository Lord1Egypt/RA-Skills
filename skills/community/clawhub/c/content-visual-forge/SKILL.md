---
name: content-visual-forge
archetype: general
description: 视觉资产制作 skill，把任意输入源（PDF/网页/文章/截图/视频转写稿/单字或词表）转化为公众号封面、知识卡、单字卡、头图、Excalidraw/p5.js/PixiJS/ASCII 创意微资产，统一视觉风格批量输出。触发语义：用户要"做封面""出卡片""生成字卡""画头图""视觉化内容""风格探索""手绘风图解"等明确视觉资产请求时启用。产物始终是图像/PDF/HTML 可视化文件，不是文字报告或长文。
---

# Content Visual Forge

版本：v2.7.2
定位：把多种内容源统一转化为多种视觉输出。

---

## ⚡ 5 分钟快速开始

### 场景 1：生成单张汉字学习卡

**用户输入：**
```
给汉字"穿"做一张学习卡
```

**系统执行：**
1. 识别输入类型：单个汉字 → 路由到 `character-card`
2. Source Lock：锁定汉字"穿"的信息
3. 填充字段：拼音、笔画、部首、释义、常用词、例句
4. 选择执行模式：单张预览用 `direct_image_preview`，批量用 `engineering_rendering`
5. 生成卡片

**输出：**
- 包含拼音 chuān、释义"wear, put on"、常用词"穿衣服/穿鞋"、例句的精美学习卡

---

### 场景 2：生成公众号封面

**用户输入：**
```
给我的文章生成公众号封面，标题是《时间管理的艺术》，内容讲的是四象限法
```

**系统执行：**
1. Source Lock：文章主题、核心观点
2. 路由到 `cover-card` + `production_cover` 模式
3. 生成封面概念：内容意图、风格路由、视觉概念
4. 输出无文字背景图 + 排版规范
5. 工程层叠加标题

**输出：**
- 2.35:1 或 1:1 封面，标题清晰可读，适合移动端

---

### 场景 3：批量生成 50 个词汇卡

**用户输入：**
```
把这个 GRE 词汇表做成 50 张卡片，用于付费课程
```

**系统执行：**
1. 检测：批量 + 商用 + 精确中文 → 强制 `engineering_rendering`
2. 对每个单词完成 Content Analysis
3. 准备 50 个卡片的渲染数据包（JSON）
4. 调用 HTML/CSS 模板批量渲染
5. 质量检查：准确性、一致性

**输出：**
- 50 张风格完全一致的词汇卡（1080×1440），中文释义像素级准确

---

### 场景 4：小红书组图（社交卡片）

**用户输入：**
```
这个产品介绍做成小红书 6 页组图
```

**系统执行：**
1. 声明平台规格：1080×1440 (3:4)
2. 内容压缩阶梯：长文 → 适合社交平台的短内容
3. 视觉导演路由：选择 `save_first`（保存优先）
4. 页面角色编排：封面 → 痛点 → 功能亮点 → 总结
5. 批量渲染

**输出：**
- 6 页风格统一、信息密度适中、便于保存收藏的小红书组图

---

## 核心定位

这个 Skill 的本质不是"做图"，而是：

> 先理解内容，再选择最合适的输出形式；先保证内容正确，再保证视觉统一；先判断宿主能力，再决定最终交付路径。

**六条能力主线：**
1. **内容卡片主线** - 多源输入 → Source Lock → 卡片脚本 → 生图/渲染
2. **封面生成主线** - 内容意图 → 风格路由 → 视觉概念 → 预览/正式封面
3. **平台社交图主线** - 平台规格 → 内容压缩 → 页面角色 → 工程化渲染
4. **插画语法主线** - Source Lock → 插画语法 → 场景脚本 → 批量一致性
5. **创意微资产主线** - 输出模式 → 设计导演 → ASCII/手绘/p5.js/PixiJS → 渲染包
6. **风格探索主线** - 主体锁定 → 视觉轴组合 → 小批量样张 → 正式生产

---

## 输出类型

### Template Families
1. `cover-card` - 公众号封面/头图/首图/海报封面
2. `wechat-inline-image` - 公众号文内配图
3. `social-card` - 小红书/Rednote/社交平台 3:4 组图
4. `knowledge-carousel` - 系列知识卡/方法论图解
5. `character-card` - 单字学习卡
6. `vocabulary-card` - 词汇卡
7. `grammar-card` - 语法点卡
8. `phrase-card` - 短语/句型卡
9. `pronunciation-card` - 发音卡 ⭐ 新增
10. `translation-card` - 翻译卡 ⭐ 新增

### 支持的输入源
PDF, 网页, 文章, 截图, 视频转写稿, 音频转写稿, 图片, PPT, 单字/词表, 多源混合

---

## 核心硬规则（Top 5）

1. **No Source Lock, No Generation** - 没完成 Source Lock 不生成图片
2. **Content Fidelity First** - 内容忠实度优先
3. **Chinese Legibility First** - 中文可读性优先
4. **Platform Specs Before Social Cards** - 社交组图先声明平台规格
5. **Engineering Rendering For Production** - 批量/商用优先工程化渲染

👉 完整硬规则（23 条）：[references/core/hard-rules.md](references/core/hard-rules.md) ⭐

---

## 固定执行流程

### 阶段 0: Input Type Router
识别输入源类型

### 阶段 1: Source Lock
锁定内容源，生成 Content Source Brief

### 阶段 2: Output Mode Router
判断输出类型（封面/系列卡/单字卡等）

### 阶段 3: Execution Mode Router
判断执行路径：
- `preview_image` - 快速预览图
- `production_cover` - 正式封面
- `background_then_layout` - 先背景后排版
- `direct_image_preview` - 直接生图预览
- `prompt_package` - 仅输出提示词包
- `engineering_rendering` - 模板渲染/程序排版

### 阶段 4: Content Analysis
提炼内容骨架、传播角度和可视化机会点

### 阶段 4A-4G: 可选增强路由
- **4A: Content Compression Ladder** - 社交卡/长文拆页内容压缩
- **4B: Style Atlas Routing** - 画家/流派/图鉴风格
- **4C: Visual Direction Routing** - 小红书/社交组图视觉导演（默认启用）
- **4D: Design Enhancement Routing** - 美化/设计探索
- **4E: Illustration Grammar Routing** - 插画感/场景化
- **4F: Creative Micro Assets Routing** - ASCII/手绘/Excalidraw/p5.js/PixiJS
- **4G: Style Exploration Lab** - 风格探索实验

### 阶段 5: Card Script / Cover Concept
- 知识卡/社交卡 → 分页脚本、页面角色
- 封面 → 内容意图、风格路由、视觉概念

### 阶段 6: Prompt / Render Package
生成每页/每卡/封面的提示词或渲染包

### 阶段 7: Batch Generation / Rendering
批量生成或模板渲染

### 阶段 8: Quality Gate
内容忠实度检查、风险黑名单扫描、视觉质量门禁

### 阶段 9: Retry / Production Upgrade
不合格内容重试；商用需求升级到工程化渲染

👉 详细流程：[references/workflows/execution-overview.md](references/workflows/)

---

## 场景快速路由

**做公众号封面：**
- 👉 [references/workflows/cover-workflow.md](references/workflows/)
- 👉 [references/template-families/cover-card/](references/template-families/cover-card/)

**做系列知识卡：**
- 👉 [references/workflows/carousel-workflow.md](references/workflows/)
- 👉 [references/template-families/knowledge-carousel/](references/template-families/knowledge-carousel/)

**做社交平台组图：**
- 👉 [references/workflows/social-card-workflow.md](references/workflows/)
- 👉 [references/template-families/social-card/](references/template-families/social-card/)
- 👉 [references/config/visual-direction-system.md](references/config/visual-direction-system.md) ⭐

**做语言学习卡（单字/词汇/语法/短语/发音/翻译）：**
- 👉 [references/workflows/language-card-workflow.md](references/workflows/)
- 👉 [references/template-families/learning-card/](references/template-families/learning-card/)
- 👉 [references/template-families/character-card/](references/template-families/character-card/)（单字卡特定视觉）
- ⭐ 新增：pronunciation-card（发音练习）、translation-card（翻译练习）

**风格探索/实验：**
- 👉 [references/config/style-exploration-lab.md](references/config/style-exploration-lab.md)

**插画感/场景化：**
- 👉 [references/config/illustration-grammar.md](references/config/illustration-grammar.md)

**创意微资产（ASCII/手绘/p5.js/PixiJS）：**
- 👉 [references/config/creative-micro-assets.md](references/config/creative-micro-assets.md)

**PixiJS 生图增强：**
- 👉 [references/config/pixijs-generated-visual-layer.md](references/config/pixijs-generated-visual-layer.md)

---

## 完整导航

👉 [references/README.md](references/README.md) - 参考文档总导航（76 个文件）

**分层结构：**
- `core/` - 核心硬规则
- `config/` - 配置与门禁
- `workflows/` - 工作流程
- `template-families/` - 8 种输出类型模板
- `cover-engine/` - 封面引擎
- `source-adapters/` - 源适配器
- `schemas/` - 数据结构定义

---

## 视觉系统速查

### 知识卡系统
- 画幅：3:4
- 背景：奶油白/米白
- 主色：深墨绿、鼠尾草绿、珊瑚橙
- 风格：书卷感、编辑感、信息层级清晰

### 单字卡系统
- 画幅：3:4
- 风格：童趣、贴纸感、启蒙友好
- 主色：柔和、低饱和

### 社交卡系统
- 画幅：3:4
- 平台适配：小红书/Rednote
- 视觉导演：click_first / save_first / brand_first
- 页面角色：封面→痛点→认知→方法→证据→操作→总结→行动

---

## 质量门禁

**必须检查：**
- ✅ Source Lock 完成
- ✅ 内容忠实度验证
- ✅ 中文可读性（小字号不交给图像模型）
- ✅ 风险动作黑名单扫描
- ✅ 素材来源记录（外部资产）
- ✅ 平台规格声明（社交卡）
- ✅ 批量生产用工程化渲染

---

## 未来发展路线

### Phase 1：当前支持（v2.7.0）
- ✅ **语言学习卡片** - character-card, vocabulary-card, grammar-card, phrase-card
- ✅ **知识可视化** - knowledge-carousel（系列知识卡）
- ✅ **社交媒体内容** - social-card（小红书/Rednote 组图）
- ✅ **封面生成** - cover-card（公众号封面/头图）
- ✅ **文内配图** - wechat-inline-image

### Phase 2：STEM 扩展（未来）
当有明确需求时，将支持：
- **formula-card** - 数学/物理/化学公式卡
- **concept-card** - 学科概念定义卡
- **code-card** - 编程学习卡（语法/算法）

**设计原则：**
- 每个新域独立 workflow 文件（如 `stem-card-workflow.md`）
- 共享基础架构（Source Lock、Quality Gate）
- 保持向后兼容

### Phase 3：人文社科扩展（未来）
- **timeline-card** - 历史事件时间线卡
- **figure-card** - 人物传记卡
- **case-card** - 案例分析卡

---

**版本：** v2.7.2
**最后更新：** 2026-06-19
**重构说明：** 优化工作流架构，提取通用流程，消除 85% 重复代码，大幅降低维护成本
