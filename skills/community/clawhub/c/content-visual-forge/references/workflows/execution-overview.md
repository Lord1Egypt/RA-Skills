# 固定执行流程概览

本文件串联所有工作流阶段，提供完整的执行路径视图。

---

## 核心流程图

```
用户输入
  ↓
[阶段 0] Input Type Router ············ 00-input-router.md
  ↓
[阶段 1] Source Lock ··················· 01-source-lock.md
  ↓
[阶段 2] Output Mode Router ············ 02-output-mode-router.md
  ↓
[阶段 3] Execution Mode Router ········· 03-execution-mode-router.md
  ↓
[阶段 4] Content Analysis ·············· 04-content-analysis.md
  ↓
[可选增强] 4A-4G 路由阶段 ··············· 见下方
  ↓
[阶段 5] Card Script / Cover Concept ··· 05-09
  ↓
[阶段 6] Prompt / Render Package ······· 10-prompt-and-render-package.md
  ↓
[阶段 7] Batch Generation / Rendering ··· （执行生成）
  ↓
[阶段 8] Quality Gate ·················· （质量检查）
  ↓
[阶段 9] Retry / Production Upgrade ····· （重试或升级）
```

---

## 阶段详解

### 阶段 0：Input Type Router
**文件：** [00-input-router.md](00-input-router.md)

**目标：** 识别输入源类型（PDF / 网页 / 文本 / 视频 / 音频 / 图片 / PPT / 多源混合 / 单字词表）

**输出：**
- 输入源类型
- 可读取程度
- 需要的适配器
- 下一步：Source Lock

---

### 阶段 1：Source Lock
**文件：** [01-source-lock.md](01-source-lock.md)

**目标：** 锁定当前内容源，防止内容跑偏、历史样例串台

**必须回答：**
1. 当前内容源是什么？
2. 它真正讲的主题是什么？
3. 核心主线是什么？
4. 哪些是事实？哪些是推断？
5. 哪些内容不能出现？
6. 适合拆成几页？

**输出：** Source Lock Report（使用 `assets/templates/source-lock-report.md`）

**闸门规则：** 没完成 Source Lock 不允许生成图片

---

### 阶段 2：Output Mode Router
**文件：** [02-output-mode-router.md](02-output-mode-router.md)

**目标：** 判断本次任务属于哪一种输出模式

**可选模式：**
- `knowledge-carousel` - 系列知识卡
- `wechat-inline-image` - 公众号文内配图
- `social-card` - 小红书/社交平台组图
- `cover-card` - 公众号封面
- `character-card` - 单字学习卡
- `vocabulary-card` / `grammar-card` / `phrase-card` - 词汇/语法/短语卡

**输出：**
- 输出模式
- 选择原因
- 预期卡片数量
- 使用模板
- 风格建议

---

### 阶段 3：Execution Mode Router
**文件：** [03-execution-mode-router.md](03-execution-mode-router.md)

**目标：** 判断执行路径

**可选执行模式：**
- `preview_image` - 快速预览图
- `production_cover` - 正式封面
- `background_then_layout` - 先背景后排版
- `direct_image_preview` - 直接生图预览
- `prompt_package` - 仅输出提示词包
- `engineering_rendering` - 模板渲染/程序排版

**判定逻辑：**
- cover-card：正式发布 → `production_cover` 或 `background_then_layout`
- social-card：批量/商用/精确截图 → `engineering_rendering`
- knowledge-carousel：批量/稳定/商用 → `engineering_rendering`
- 快速验证 → `direct_image_preview`

---

### 阶段 4：Content Analysis
**文件：** [04-content-analysis.md](04-content-analysis.md)

**目标：** 提炼内容骨架、传播角度和可视化机会点

**输出：**
- 内容结构分析
- 核心主题提炼
- 可视化机会点
- 传播角度建议

---

### 可选增强路由阶段（4A-4G）

根据需求动态启用：

#### 4A：Content Compression Ladder
**触发条件：** 社交卡/长文拆页内容压缩

**目标：** 把长文压缩成适合社交平台的短内容

#### 4B：Style Atlas Routing
**触发条件：** 用户要求特定画家/流派/图鉴风格

**目标：** 路由到风格图谱，选择视觉参考

#### 4C：Visual Direction Routing
**触发条件：** 小红书/社交组图（默认启用）

**文件：** `references/config/visual-direction-system.md`

**目标：** 视觉导演编排（click_first / save_first / brand_first）

#### 4D：Design Enhancement Routing
**触发条件：** 用户要求美化/设计探索

**目标：** 设计增强建议

#### 4E：Illustration Grammar Routing
**文件：** [04E-illustration-grammar-routing.md](04E-illustration-grammar-routing.md)

**触发条件：** 插画感/场景化需求

**目标：** 应用插画语法（scene role / subject focus / composition axis / camera distance / texture level / text load）

#### 4F：Creative Micro Assets Routing
**文件：** `references/config/creative-micro-assets.md`

**触发条件：** ASCII/手绘/Excalidraw/p5.js/PixiJS 需求，或工程化渲染画质不足但需要保留精确文字

**目标：** 创意微资产生成；必要时进入 `pixijs_generated_visual_layer` 做 AI 无文字主体 + PixiJS canvas 叠层 + 工程文字排版 + 静态截图导出

#### 4G：Style Exploration Lab
**文件：** `references/config/style-exploration-lab.md`

**触发条件：** 风格探索实验

**目标：** 稀有视觉风格探索，视觉轴组合

---

### 阶段 5：Card Script / Cover Concept

根据 Output Mode 分支：

#### 知识卡/社交卡
**文件：** [05-carousel-script.md](05-carousel-script.md)

**输出：** 分页脚本、页面角色

#### 文内配图
**文件：** [06-wechat-inline-image-routing.md](06-wechat-inline-image-routing.md)

**输出：** 配图方案、插画语法

#### 单字卡/词汇卡
**文件：** [07-card-data-fill.md](07-card-data-fill.md)

**输出：** 结构化字段填充

#### 封面
**文件：** [08-cover-concept.md](08-cover-concept.md)

**输出：** 内容意图、风格路由、视觉概念

---

### 阶段 6：Prompt / Render Package
**文件：** [10-prompt-and-render-package.md](10-prompt-and-render-package.md)

**目标：** 生成每页/每卡/封面的提示词或渲染包

**输出格式：**
- 图像提示词（用于 AI 生成）
- 渲染数据包（用于工程化模板）
- 排版规范（用于后期叠字）

---

### 阶段 7：Batch Generation / Rendering
**执行方式：**
- `direct_image_preview` / `preview_image` → 直接调用图像生成
- `engineering_rendering` → 调用 HTML/CSS 模板渲染引擎
- `prompt_package` → 输出提示词包，由用户自行生成

---

### 阶段 8：Quality Gate
**检查项：**
- ✅ Source Lock 完成
- ✅ 内容忠实度验证
- ✅ 中文可读性（小字号不交给图像模型）
- ✅ 风险动作黑名单扫描（`references/config/risk-action-blacklist.md`）
- ✅ 素材来源记录（外部资产，`references/config/asset-source-policy.md`）
- ✅ 平台规格声明（社交卡）
- ✅ 批量生产用工程化渲染

---

### 阶段 9：Retry / Production Upgrade
**触发条件：**
- 内容忠实度不合格 → 重试
- 中文可读性差 → 升级到 `background_then_layout` 或 `engineering_rendering`
- 风险动作触发 → 人工审核
- 预览满意，需要正式版 → 升级到 `production_cover` 或 `engineering_rendering`

---

## 场景快速路由

根据场景选择入口：

### 做公众号封面
**路径：** 阶段 0-1-2-3 → 阶段 8（封面概念）→ 阶段 6-7-8-9

**详细文档：** [cover-workflow.md](cover-workflow.md)

### 做系列知识卡
**路径：** 阶段 0-1-2-3-4 → 阶段 5（分页脚本）→ 阶段 6-7-8-9

**详细文档：** [carousel-workflow.md](carousel-workflow.md)

### 做社交平台组图
**路径：** 阶段 0-1-2-3 → 4A（内容压缩）→ 4C（视觉导演）→ 阶段 5-6-7-8-9

**详细文档：** [social-card-workflow.md](social-card-workflow.md)

### 做语言学习卡（单字/词汇/语法/短语）
**路径：** 阶段 0-1-2-3 → 阶段 7（字段填充）→ 阶段 6-7-8-9

**详细文档：** [language-card-workflow.md](language-card-workflow.md)

---

## 核心规则（非协商）

完整规则见 [references/core/hard-rules.md](../core/hard-rules.md)

**Top 5：**
1. **No Source Lock, No Generation** - 没完成 Source Lock 不生成图片
2. **Content Fidelity First** - 内容忠实度优先
3. **Chinese Legibility First** - 中文可读性优先
4. **Platform Specs Before Social Cards** - 社交组图先声明平台规格
5. **Engineering Rendering For Production** - 批量/商用优先工程化渲染

---

**版本：** 1.0.0  
**最后更新：** 2026-06-16  
**维护：** Content Visual Forge
