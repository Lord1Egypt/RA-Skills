# 基础卡片生成工作流（Base Card Workflow）

> **定位：** 本文件是**所有领域卡片的共享执行流程**。
> 
> 各领域通过 `domain-configs/` 配置差异化内容，而不是复制整个流程。

---

## 适用说明

本工作流适用于所有卡片生成场景：
- 语言学习卡（language-card）
- 封面卡（cover-card）
- 知识轮播卡（carousel）
- 社交媒体卡（social-card）

**使用方式：**
1. 阅读本文件理解完整流程
2. 查看对应的域配置文件获取领域特定规则
3. 域配置定义的扩展点会覆盖本文件的默认行为

---

## 完整执行流程（阶段 0-9）

### 阶段 0：Input Type Router

**目标：** 快速识别输入源类型

**参考：** [00-input-router.md](00-input-router.md)

**通用识别规则：**
- PDF/网页/文章 → 内容源
- 截图/图片 → 视觉源
- 单字/词表 → 结构化数据源
- 视频/音频转写稿 → 转写源

**输出：**
```md
输入源类型：[识别结果]
可读取程度：完整 / 部分
短路提示：[如果能直接确定输出模式，提前标注]
下一步：Source Lock
```

**扩展点 #1：领域特定路由**
查看域配置文件的 `input_routing_rules` 章节。

---

### 阶段 1：Source Lock

**目标：** 锁定内容边界，防止生成过程偏离

**参考：** [01-source-lock.md](01-source-lock.md)

**硬规则：No Source Lock, No Generation**

**必须明确：**
1. 源类型
2. 目标内容
3. 主题/核心观点
4. 禁止偏离的约束
5. 页数/卡片数量

**快速 Source Lock（某些场景可用）：**
```md
源类型：[类型]
目标内容：[具体内容]
主题：[主题]
禁止偏离：[约束]
页数：[数量]
```

**完整 Source Lock：**
- 提取核心观点
- 识别内容结构
- 确定信息密度要求
- 记录来源可靠性

**扩展点 #2：领域特定 Source Lock 要求**
查看域配置文件的 `source_lock_requirements` 章节。

---

### 阶段 2：Output Mode Router

**目标：** 根据内容和用户意图选择输出模式

**参考：** [02-output-mode-router.md](02-output-mode-router.md)

**通用路由逻辑：**
1. 识别用户意图（封面/知识卡/学习卡/社交图）
2. 检查内容适配性
3. 选择输出模式

**输出：**
```md
输出模式：[模式名称]
选择原因：[简短说明]
预期数量：[卡片/页面数]
使用模板：[模板族名称]
风格建议：[风格方向]
```

**扩展点 #3：领域特定输出模式**
查看域配置文件的 `output_modes` 章节。

---

### 阶段 3：Execution Mode Router

**目标：** 选择执行路径

**参考：** [03-execution-mode-router.md](03-execution-mode-router.md)

**三种执行模式：**

#### `direct_image_preview` - 直接生图预览
**适用：** 单张快速预览、验证风格
**劣势：** 中文准确性不稳定、不适合批量

#### `engineering_rendering` - 工程化渲染 ⭐ 推荐
**适用：** 批量生成、商用、中文必须精确
**优势：** 文字准确、风格一致、批量高效
**硬规则：** 商用、大批量、付费课程必须用此模式

#### `prompt_package` - 仅输出提示词包
**适用：** 无图像生成能力、交给第三方工具

**输出：**
```md
执行模式：[模式]
选择原因：[判定依据]
```

**扩展点 #4：领域特定执行模式偏好**
查看域配置文件的 `execution_mode_preferences` 章节。

---

### 阶段 4：Content Analysis

**目标：** 提取结构化内容字段

**参考：** [04-content-analysis.md](04-content-analysis.md)

**通用分析维度：**
1. 主要内容提取
2. 关键信息识别
3. 结构化字段填充
4. 视觉元素规划

**基础卡片必填字段：**
- `title` - 标题
- `content` - 主要内容
- `visual_hint` - 视觉提示
- `style` - 风格定义
- `color_scheme` - 色彩方案

**扩展点 #5：领域特定字段**
查看域配置文件的 `content_fields` 章节，每个领域有自己的必填/选填字段。

---

### 阶段 5：Visual Direction（可选增强）

**目标：** 为复杂场景提供视觉导演

**参考：** [05-visual-direction.md](05-visual-direction.md)

**三种导演模式：**
- `click_first` - 点击优先（引导交互）
- `save_first` - 保存优先（便于收藏）
- `brand_first` - 品牌优先（强化记忆）

**适用场景：** 主要用于社交媒体多页组图

**扩展点 #6：领域特定视觉导演**
查看域配置文件的 `visual_direction_rules` 章节。

---

### 阶段 6：Prompt / Render Package

**目标：** 准备生成所需的数据包

**参考：** [10-prompt-and-render-package.md](10-prompt-and-render-package.md)

#### 如果是 `engineering_rendering`

**准备渲染数据包：**
```json
{
  "template": "[模板名]",
  "batch_info": {
    "total_cards": 数量,
    "style_anchor": "风格锚点",
    "consistency_rules": {
      "background_color": "#颜色",
      "font_family": "字体",
      "layout_template": "布局"
    }
  },
  "cards": [
    {
      "id": 1,
      ... 卡片字段 ...
    }
  ]
}
```

#### 如果是 `direct_image_preview`

**准备提示词：**
- 视觉主体描述
- 风格关键词
- 色彩方案
- 布局要求
- 文字内容

**扩展点 #7：领域特定渲染包结构**
查看域配置文件的 `render_package_schema` 章节。

---

### 阶段 7：Batch Generation / Rendering

**目标：** 执行生成

#### 执行路径 A：工程化渲染（推荐）
```
1. 准备批量渲染数据包（JSON）
2. 调用 HTML/CSS 模板
3. 批量渲染所有卡片
4. 质量检查
5. 输出 PNG 文件
```

**优势：**
- 文字显示准确
- 批量生成效率高
- 风格完全统一

#### 执行路径 B：直接生图
```
1. 逐张使用提示词生成卡片
2. 检查准确性
3. 不合格重新生成
```

**劣势：**
- 文字可能不准确
- 批量效率低
- 风格一致性难保证

---

### 阶段 8：Quality Gate

**目标：** 质量检查

**通用检查清单：**

#### 内容准确性（核心）
- [ ] 主要内容正确无误
- [ ] 关键信息完整
- [ ] 无事实性错误

#### 视觉效果
- [ ] 主要内容清晰可读
- [ ] 色彩搭配合理
- [ ] 整体风格协调

#### 批量一致性（批量生成时）
- [ ] 所有卡片风格统一
- [ ] 字体字号一致
- [ ] 版式规范一致

#### 平台规范
- [ ] 画幅符合要求
- [ ] 安全区内容无裁切

**扩展点 #8：领域特定质量标准**
查看域配置文件的 `quality_standards` 章节。

---

### 阶段 9：Retry / Production Upgrade

**目标：** 处理不合格情况

**常见问题和解决方案：**

| 问题 | 解决方案 |
|------|----------|
| 文字不准确 | 升级到 `engineering_rendering` |
| 风格不一致 | 设置 `style_anchor` |
| 内容过于复杂 | 回到阶段 4，简化内容 |
| 批量需求 | 升级到 `engineering_rendering` |
| 商用场景 | 强制 `engineering_rendering` |

---

## 核心硬规则

以下规则适用于所有领域，不可协商：

### 硬规则 1：No Source Lock, No Generation
没有完成 Source Lock 不得生成图片。即使是单张卡也必须完成快速 Source Lock。

### 硬规则 2：Content Fidelity First
内容忠实度优先。宁可视觉简单但内容准确，不可视觉华丽但内容错误。

### 硬规则 3：Chinese Legibility First
中文可读性优先。大量中文小字不交给图像模型，必须用工程化渲染。

### 硬规则 4：Engineering Rendering For Production
商用、大批量、付费课程材料必须用工程化渲染。

### 硬规则 5：Batch Style Consistency
批量生成必须设置 `style_anchor`，确保风格统一。

**扩展点 #9：领域特定硬规则**
查看域配置文件的 `domain_hard_rules` 章节。

---

## 扩展点总览

本工作流定义了 9 个扩展点，各领域可以通过域配置文件覆盖：

1. **input_routing_rules** - 领域特定输入路由
2. **source_lock_requirements** - Source Lock 要求
3. **output_modes** - 输出模式定义
4. **execution_mode_preferences** - 执行模式偏好
5. **content_fields** - 内容字段定义
6. **visual_direction_rules** - 视觉导演规则
7. **render_package_schema** - 渲染包结构
8. **quality_standards** - 质量标准
9. **domain_hard_rules** - 领域硬规则

---

## 使用示例

### 示例 1：生成语言学习卡

1. **阅读：** 本文件（base-card-workflow.md）
2. **查看：** `domain-configs/language-card-config.md`
3. **执行：** 按照本文件流程，在扩展点处应用 language-card 的特定规则

### 示例 2：生成公众号封面

1. **阅读：** 本文件（base-card-workflow.md）
2. **查看：** `domain-configs/cover-card-config.md`
3. **执行：** 按照本文件流程，在扩展点处应用 cover-card 的特定规则

---

## 架构优势

采用"基类 + 配置"架构的好处：

### 维护成本
- ✅ 通用流程只需维护 1 个文件（本文件）
- ✅ 修改通用逻辑自动影响所有域
- ✅ 避免 85% 内容重复

### 扩展成本
- ✅ 新增域只需添加 50 行配置文件
- ✅ 不需要复制 500 行完整流程

### 一致性
- ✅ 所有域共享相同的执行标准
- ✅ 质量门禁统一
- ✅ 硬规则一致应用

---

**版本：** 1.0.0  
**创建日期：** 2026-06-16  
**维护：** Content Visual Forge Team
