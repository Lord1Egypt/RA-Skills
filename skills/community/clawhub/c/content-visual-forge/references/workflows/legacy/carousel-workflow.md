# 系列知识卡完整流程

本文件描述系列知识卡（knowledge-carousel）的完整生成流程。

---

## 适用场景

- 系列知识卡（6-12 页）
- 方法论图解
- 科普内容卡片
- 教程步骤卡
- 概念解释卡片

---

## 完整流程

### 阶段 0：Input Type Router

**参考：** [00-input-router.md](00-input-router.md)

识别输入源：
- PDF 方法论章节
- 网页文章
- 笔记/长文
- 教程/步骤说明
- 概念解释文本

**输出：**
```md
输入源类型：PDF / 网页 / 文本
可读取程度：完整 / 部分
适配器：text-adapter / pdf-adapter / webpage-adapter
下一步：Source Lock
```

---

### 阶段 1：Source Lock

**参考：** [01-source-lock.md](01-source-lock.md)

**必须回答：**
1. 当前内容源真正讲的主题是什么？
2. 核心主线是什么？
3. 有哪些章节结构？
4. 适合拆成几页？
5. 每页大致讲什么？
6. 哪些内容不能出现？

**输出：** Source Lock Report

**示例：**
```md
## Source Lock Report

### 内容源
类型：PDF 方法论文章
主题：时间管理四象限法
主线：重要性 vs 紧急性的任务分类方法

### 核心结构
1. 问题背景：为什么需要任务分类
2. 四象限定义：重要紧急、重要不紧急、不重要紧急、不重要不紧急
3. 每个象限的特点
4. 实践方法：如何判断任务属于哪个象限
5. 常见误区
6. 行动建议

### 建议分页
6-8 页

### 禁止偏离项
- 不得生成与时间管理四象限法无关的内容
- 不得虚构原文没有的案例
- 不得套用历史示例
```

---

### 阶段 2：Output Mode Router

**参考：** [02-output-mode-router.md](02-output-mode-router.md)

**确认输出模式：** `knowledge-carousel`

**判定依据：**
- 有明显章节结构 ✓
- 适合拆成 6–12 页 ✓
- 每页能承载一个核心点 ✓
- 目标是解释、总结、图解、科普、方法论传播 ✓

**输出：**
```md
输出模式：knowledge-carousel
选择原因：内容有清晰章节结构，适合拆页图解
预期卡片数量：8 页
使用模板：8-page-knowledge-carousel
风格建议：书卷感、编辑感、信息层级清晰
```

---

### 阶段 3：Execution Mode Router

**参考：** [03-execution-mode-router.md](03-execution-mode-router.md)

**判定执行路径：**

#### `direct_image_preview` - 直接生图预览
**适用场景：**
- 快速出样验证内容结构
- 不追求商用级别精度

---

#### `engineering_rendering` - 工程化渲染
**适用场景：** ⭐ 推荐
- 批量生成
- 商用发布
- 中文字段必须精确
- 需要风格一致性

**特点：** HTML/CSS 模板渲染，保证文字准确、风格统一

---

#### `prompt_package` - 仅输出提示词包
**适用场景：**
- 无图像生成能力
- 需要交给第三方工具

---

### 阶段 4：Content Analysis

**参考：** [04-content-analysis.md](04-content-analysis.md)

**提炼内容骨架：**
- 逻辑结构（递进/并列/对比/因果）
- 核心概念
- 关键步骤
- 可视化机会点（图表/流程/对比/示例）

**输出：**
```md
## 内容骨架

逻辑结构：递进（问题 → 方法 → 实践）
核心概念：四象限、重要性、紧急性
关键步骤：判断任务属性 → 分配象限 → 制定策略
可视化机会点：
  - 四象限坐标图
  - 任务分类示例
  - 误区对比
```

---

### 阶段 5：Carousel Script

**参考：** [05-carousel-script.md](05-carousel-script.md)

**使用模板：** `assets/templates/8-page-knowledge-carousel.md`

**输出分页脚本：**

```md
## 8 页知识卡脚本

### 第 1 页：封面页
**页面角色：** 封面
**核心内容：** 主题标题 + 一句话概括
**视觉元素：** 主题配图
**文字内容：**
  - 标题：时间管理四象限法
  - 副标题：重要性 vs 紧急性的任务分类

---

### 第 2 页：问题背景
**页面角色：** 痛点/背景
**核心内容：** 为什么需要任务分类
**视觉元素：** 任务堆积场景
**文字内容：**
  - 小标题：为什么总觉得忙但没成果？
  - 正文：3-4 行痛点描述

---

### 第 3 页：方法概览
**页面角色：** 概念介绍
**核心内容：** 四象限定义
**视觉元素：** 四象限坐标图
**文字内容：**
  - 小标题：四象限法
  - 象限名称：重要紧急、重要不紧急、不重要紧急、不重要不紧急

---

### 第 4 页：象限 1 详解
**页面角色：** 方法细节
**核心内容：** 重要且紧急
**视觉元素：** 象限 1 示意
**文字内容：**
  - 象限名称
  - 特点描述
  - 任务示例（2-3 个）

---

### 第 5 页：象限 2 详解
**页面角色：** 方法细节
**核心内容：** 重要但不紧急
**视觉元素：** 象限 2 示意
**文字内容：**
  - 象限名称
  - 特点描述
  - 任务示例（2-3 个）

---

### 第 6 页：实践方法
**页面角色：** 操作指南
**核心内容：** 如何判断任务属于哪个象限
**视觉元素：** 判断流程图
**文字内容：**
  - 小标题：如何判断
  - 步骤 1-3

---

### 第 7 页：常见误区
**页面角色：** 避坑
**核心内容：** 常见错误做法
**视觉元素：** 错误示例对比
**文字内容：**
  - 小标题：避开这些坑
  - 误区 1-3（简短描述）

---

### 第 8 页：行动建议
**页面角色：** 行动号召
**核心内容：** 立即可执行的建议
**视觉元素：** 行动清单
**文字内容：**
  - 小标题：现在开始
  - 行动建议 1-3
```

---

### 阶段 6：Prompt / Render Package

**参考：** [10-prompt-and-render-package.md](10-prompt-and-render-package.md)

#### 如果是 `engineering_rendering`（推荐）

**输出渲染数据包：**
```json
{
  "carousel_title": "时间管理四象限法",
  "carousel_subtitle": "重要性 vs 紧急性的任务分类",
  "style": {
    "background": "#F5F5DC",
    "primary_color": "#2C5F2D",
    "secondary_color": "#D2691E",
    "accent_color": "#FF6347",
    "font_family": "思源黑体"
  },
  "pages": [
    {
      "page_number": 1,
      "page_role": "cover",
      "title": "时间管理四象限法",
      "subtitle": "重要性 vs 紧急性的任务分类",
      "visual_hint": "四象限图标"
    },
    {
      "page_number": 2,
      "page_role": "background",
      "title": "为什么总觉得忙但没成果？",
      "body": "每天疲于应付紧急任务\n但重要的长期目标总是被搁置\n时间管理的关键不是做得更快\n而是做对的事",
      "visual_hint": "任务堆积场景"
    }
    // ... 其他页面
  ]
}
```

**使用模板：** `assets/render-engine/html-templates/knowledge-carousel.html`

---

#### 如果是 `direct_image_preview`

**输出每页提示词：**
```md
## 第 1 页提示词

画幅：3:4 (1080×1440)
背景：奶油白 (#F5F5DC)
主标题：时间管理四象限法
副标题：重要性 vs 紧急性的任务分类
视觉元素：简洁四象限图标，深墨绿色
风格：书卷感、编辑感、信息层级清晰
文字位置：中心偏上
装饰：极简几何线条

---

## 第 2 页提示词

画幅：3:4 (1080×1440)
背景：奶油白
小标题：为什么总觉得忙但没成果？
正文：
  每天疲于应付紧急任务
  但重要的长期目标总是被搁置
  时间管理的关键不是做得更快
  而是做对的事
视觉元素：任务堆积抽象插图
右上角：页码胶囊 2/8
```

---

### 阶段 7：Batch Generation / Rendering

#### 执行路径 A：工程化渲染（推荐）
```
1. 准备渲染数据包（JSON）
2. 调用 HTML/CSS 模板
3. 批量渲染 8 页
4. 输出 PNG 文件
5. 检查风格一致性
```

**优势：**
- 中文文字准确
- 风格完全统一
- 批量生成高效
- 可微调模板复用

---

#### 执行路径 B：直接生图
```
1. 逐页生成图像
2. 检查内容忠实度
3. 检查风格一致性
4. 不合格页面重新生成
```

**劣势：**
- 中文准确性不稳定
- 风格一致性难保证
- 逐页生成效率低

---

### 阶段 8：Quality Gate

**质量检查清单：**

#### 内容忠实度
- [ ] 每页内容与 Source Lock 一致
- [ ] 没有虚构原文没有的内容
- [ ] 核心概念准确无误
- [ ] 页面顺序符合逻辑

#### 中文可读性
- [ ] 所有中文文字清晰可读
- [ ] 字号符合规范（标题≥48pt，正文≥28pt）
- [ ] 颜色对比度足够
- [ ] 没有错别字

#### 风格一致性
- [ ] 8 页背景色一致
- [ ] 主色调统一
- [ ] 字体字号一致
- [ ] 版式规范统一
- [ ] 视觉风格协调

#### 平台规范
- [ ] 画幅 3:4 (1080×1440)
- [ ] 安全区内没有被裁切的关键内容
- [ ] 页码清晰（右上角胶囊）

#### 风险扫描
- [ ] 没有触发风险动作黑名单
- [ ] 外部素材已记录来源

---

### 阶段 9：Retry / Production Upgrade

#### 不合格情况处理

**内容不忠实 →** 回到阶段 5，调整分页脚本

**中文不清晰 →** 升级到 `engineering_rendering`

**风格不一致 →** 升级到 `engineering_rendering`

**页面数量不合适 →** 调整为 6 页或 9 页，重新分页

---

#### 预览升级到正式版

**流程：**
```
1. 用户确认预览结构满意
2. 升级执行模式：direct_image_preview → engineering_rendering
3. 准备渲染数据包
4. 批量渲染
5. 质量检查
6. 输出正式版
```

---

## 核心规则

### 硬规则
1. **No Source Lock, No Generation** - 没完成 Source Lock 不生成卡片
2. **Content Fidelity First** - 内容忠实度优先
3. **Chinese Legibility First** - 中文可读性优先
4. **Engineering Rendering For Production** - 批量/商用优先工程化渲染

### 推荐实践
- 商用/批量生成必须用 `engineering_rendering`
- 快速验证用 `direct_image_preview`
- 页数建议 6-8 页，不超过 12 页
- 每页承载一个核心点
- 保持风格一致性

---

## 视觉系统

### 画幅
- 标准：3:4 (1080×1440)

### 背景
- 奶油白 (#F5F5DC)
- 米白 (#FAF9F6)

### 主色
- 深墨绿 (#2C5F2D)
- 鼠尾草绿 (#97A97C)
- 珊瑚橙 (#FF6347)

### 风格
- 书卷感
- 编辑感
- 信息层级清晰
- 留白充足

### 装饰
- 极简几何线条
- 页码胶囊（右上角）

---

## 参考资源

### 模板族
- [template-families/knowledge-carousel/](../template-families/knowledge-carousel/)

### 模板文件
- `assets/templates/8-page-knowledge-carousel.md`
- `assets/templates/6-page-explainer-carousel.md`
- `assets/templates/9-page-level-carousel.md`

### 渲染引擎
- `assets/render-engine/html-templates/knowledge-carousel.html`
- `assets/render-engine/css/knowledge-carousel.css`

### 配置文件
- [config/risk-action-blacklist.md](../config/risk-action-blacklist.md)
- [config/asset-source-policy.md](../config/asset-source-policy.md)

---

**版本：** 1.0.0  
**最后更新：** 2026-06-16  
**维护：** Content Visual Forge
