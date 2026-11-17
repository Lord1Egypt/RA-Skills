# 封面生成完整流程

本文件描述公众号封面、头图、首图的完整生成流程。

---

## 适用场景

- 公众号封面 / 头图
- 公众号 `21:9 + 1:1` 封面对
- 海报封面
- 文章首图

---

## 完整流程

### 阶段 0：Input Type Router

**参考：** [00-input-router.md](00-input-router.md)

识别输入源：
- 文章正文
- 文章标题 + 摘要
- 内容主题 + 关键词
- 参考图 + 文字描述

**输出：**
```md
输入源类型：文章正文 / 文章标题 / 主题关键词
可读取程度：完整 / 部分
下一步：Source Lock
```

---

### 阶段 1：Source Lock

**参考：** [01-source-lock.md](01-source-lock.md)

**必须回答：**
1. 文章真正讲的主题是什么？
2. 核心主线是什么？
3. 目标读者是谁？
4. 传播角度是什么？（科普/故事/观点/方法论/情绪共鸣）
5. 封面需要传达什么？

**输出：** Content Source Brief

**禁止偏离项：**
- 不得生成与文章无关的封面主题
- 不得套用历史示例
- 不得把参考图内容当作当前文章主题

---

### 阶段 2：Output Mode Router

**参考：** [02-output-mode-router.md](02-output-mode-router.md)

**确认输出模式：** `cover-card`

**输出：**
```md
输出模式：cover-card
使用模板：references/template-families/cover-card/
风格建议：（根据文章类型和目标读者）
```

---

### 阶段 3：Execution Mode Router

**参考：** [03-execution-mode-router.md](03-execution-mode-router.md)

**判定执行路径：**

#### `preview_image` - 快速预览图
**适用场景：**
- 只要快速看效果
- 验证封面主题方向
- 不追求正式发布质量

**特点：** 图像模型直接生成带标题的封面

---

#### `production_cover` - 正式封面
**适用场景：**
- 需要正式公众号封面
- 标题可读性要求高
- 准备发布使用

**特点：** 无文字背景图 + 后期标题排版

**优先级：** 正式封面首选此模式

---

#### `background_then_layout` - 先背景后排版
**适用场景：**
- 需要明显画面感、背景主视觉或插画主体
- 需要灵活调整标题位置
- 需要保证中文标题清晰

**特点：** 
1. 先生成无文字背景图（插画主体/场景/主视觉）
2. 再用工程层叠加标题、副标题、装饰元素

**流程：**
```
背景图提示词生成 → 生成背景图 → 排版规范输出 → 工程层叠字
```

---

#### `direct_image_preview` - 直接生图预览
**适用场景：**
- 快速验证视觉方向
- 不需要精确排版

---

#### `prompt_package` - 仅输出提示词包
**适用场景：**
- 无图像生成能力
- 需要交给第三方工具生成

---

#### `engineering_rendering` - 工程化渲染
**适用场景：**
- 仅需文字叠层、版式或安全区
- 批量生成封面
- 需要精确控制标题位置和字号

---

### 阶段 4：Content Analysis

**参考：** [04-content-analysis.md](04-content-analysis.md)

**提炼内容骨架：**
- 文章核心观点
- 情绪基调（理性/感性/幽默/严肃）
- 视觉关键词（场景/人物/物件/抽象概念）
- 传播角度（悬念/痛点/好奇/共鸣）

**输出：**
```md
核心主题：
情绪基调：
视觉关键词：
传播角度：
```

---

### 阶段 4B：Style Atlas Routing（可选）

**触发条件：** 用户要求特定画家/流派/图鉴风格

**文件：** `references/config/style-atlas.md`

**输出：** 风格参考、视觉参考

---

### 阶段 4E：Illustration Grammar Routing（可选）

**触发条件：** 需要插画感封面背景

**文件：** [04E-illustration-grammar-routing.md](04E-illustration-grammar-routing.md)

**输出：** 插画语法配置
- scene role（场景角色）
- subject focus（主体焦点）
- composition axis（构图轴）
- camera distance（镜头距离）
- texture level（质感层次）
- text load（文字负载）

---

### 阶段 4G：Style Exploration Lab（可选）

**触发条件：** 用户要求风格探索

**文件：** `references/config/style-exploration-lab.md`

**输出：** 稀有视觉风格探索方案

---

### 阶段 8：Cover Concept

**参考：** [08-cover-concept.md](08-cover-concept.md)

**使用模板：** `assets/templates/cover-card/cover-concept-template.md`

**输出：**
```md
## 封面概念

### 内容意图
- 文章主题：
- 传播角度：
- 目标读者：

### 风格路由
- 视觉风格：
- 情绪基调：
- 参考方向：

### 视觉概念
- 主视觉：（场景/人物/物件/抽象概念）
- 构图方式：（中心/三分/对角/留白）
- 色彩方案：（暖/冷/对比/和谐）
- 标题位置：（上/中/下/左/右）
- 装饰元素：（几何/线条/色块/纹理）

### 执行路径
- 执行模式：production_cover / background_then_layout
- 背景图提示词：（如果需要生成背景）
- 排版规范：（标题字号/位置/颜色/对齐方式）
```

---

### 阶段 6：Prompt / Render Package

**参考：** [10-prompt-and-render-package.md](10-prompt-and-render-package.md)

#### 如果是 `background_then_layout`

**输出背景图提示词：**
```md
## 背景图提示词

主体：
场景：
构图：
色彩：
风格：
禁止元素：任何文字、标题、字母
```

**输出排版规范：**
```md
## 排版规范

画幅：2.35:1 (1200×510) 或 1:1 (1080×1080)
标题位置：上部居中 / 左上 / 右下
标题字号：48-72pt
标题颜色：白色/黑色/品牌色
标题背景：透明/半透明色块/无
副标题：（如果需要）
安全区：距离边缘 60px
```

---

#### 如果是 `engineering_rendering`

**输出渲染数据包：**
```json
{
  "title": "封面标题",
  "subtitle": "副标题（可选）",
  "background_color": "#F5F5DC",
  "title_color": "#2C3E50",
  "title_position": "center-top",
  "title_size": "64px",
  "decoration": "geometric-lines"
}
```

**使用模板：** `assets/render-engine/html-templates/cover-card.html`

---

### 阶段 7：Batch Generation / Rendering

#### 执行路径 A：生成背景图 + 后期排版
```
1. 使用背景图提示词生成无文字背景
2. 检查背景图质量
3. 按排版规范叠加标题
4. 输出最终封面
```

#### 执行路径 B：工程化渲染
```
1. 准备渲染数据
2. 调用 HTML/CSS 模板
3. 渲染输出 PNG/JPEG
```

#### 执行路径 C：直接生图
```
1. 使用完整提示词（含标题）生成封面
2. 输出预览图
```

---

### 阶段 8：Quality Gate

**质量检查清单：**

#### 内容忠实度
- [ ] 封面主题与文章一致
- [ ] 没有虚构文章没有的内容
- [ ] 没有套用历史示例

#### 中文可读性
- [ ] 标题清晰可读（移动端可读）
- [ ] 字号符合平台规范（≥48pt）
- [ ] 颜色对比度足够
- [ ] 没有小字号中文交给图像模型

#### 平台规范
- [ ] 画幅符合公众号规范（2.35:1 或 1:1）
- [ ] 安全区内没有被裁切的关键内容
- [ ] 文件格式符合要求（JPEG/PNG）

#### 风险扫描
- [ ] 没有触发风险动作黑名单
- [ ] 外部素材已记录来源
- [ ] 没有版权风险

---

### 阶段 9：Retry / Production Upgrade

#### 不合格情况处理

**标题不可读 →** 升级到 `background_then_layout` 或 `engineering_rendering`

**背景图不满意 →** 调整提示词重新生成

**风格不符 →** 调整 Style Atlas 或 Illustration Grammar

**需要批量生成 →** 升级到 `engineering_rendering`

---

#### 预览升级到正式版

**流程：**
```
1. 用户确认预览方向满意
2. 升级执行模式：preview_image → production_cover
3. 生成无文字背景图
4. 输出排版规范
5. 工程层叠字
6. 输出正式封面
```

---

## 核心规则

### 硬规则
1. **No Source Lock, No Generation** - 没完成 Source Lock 不生成封面
2. **Content Fidelity First** - 封面主题必须与文章一致
3. **Chinese Legibility First** - 标题可读性优先
4. **Production Cover Defaults to Background + Typography Overlay** - 正式封面默认采用"无文字背景图 + 后期标题排版"

### 推荐实践
- 正式发布优先 `production_cover` 或 `background_then_layout`
- 快速验证用 `preview_image`
- 批量生成用 `engineering_rendering`
- 背景图提示词必须明确"禁止任何文字"

---

## 参考资源

### 模板族
- [template-families/cover-card/](../template-families/cover-card/)

### 配置文件
- [config/risk-action-blacklist.md](../config/risk-action-blacklist.md)
- [config/asset-source-policy.md](../config/asset-source-policy.md)
- [config/style-exploration-lab.md](../config/style-exploration-lab.md)

### 核心引擎
- [cover-engine/](../cover-engine/)

---

**版本：** 1.0.0  
**最后更新：** 2026-06-16  
**维护：** Content Visual Forge
