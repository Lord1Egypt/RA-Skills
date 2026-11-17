# 封面生成完整流程（Cover Card Workflow）

> **本文件是精简版工作流。**  
> 完整的执行流程请参考：[base-card-workflow.md](base-card-workflow.md)

---

## 快速导航

- **完整执行流程：** [base-card-workflow.md](base-card-workflow.md)
- **领域特定规则：** [domain-configs/cover-card-config.md](domain-configs/cover-card-config.md)
- **完整版（已归档）：** [legacy/cover-workflow.md](legacy/cover-workflow.md)

---

## 领域定位

> **覆盖范围：** 公众号封面、头图、首图、海报封面
> 
> **核心特点：** 无文字背景 + 后期文字叠加

---

## 适用场景

支持 2 种封面模式：
- **draft_cover** - 草稿封面（带文字预览）
- **production_cover** - 正式封面（无文字背景 + 排版规范）⭐ 推荐

---

## 执行流程

### 使用方式

1. **阅读基础流程：** [base-card-workflow.md](base-card-workflow.md) - 阶段 0-9 完整执行流程
2. **查看领域配置：** [domain-configs/cover-card-config.md](domain-configs/cover-card-config.md) - 封面生成特定规则
3. **应用扩展点：** 在基础流程的 9 个扩展点处，应用 cover-card 的特定规则

---

## 领域特定要点

### 封面概念方法论

**必须生成三要素：**
1. **内容意图** - 从文章提取核心观点
2. **风格路由** - 匹配受众和主题
3. **视觉概念** - 具体画面描述

### 硬规则（扩展点 #9）
1. **Production Must Be Text-Free** - 正式封面必须无文字
2. **Safe Area Required** - 必须标注文字安全区域
3. **Mobile-First** - 构图和色彩适配移动端

### 画幅规范
- 公众号封面：**2.35:1** (900×383)
- 正方形封面：**1:1** (1080×1080)

---

## 内容字段速查

详细字段见：[domain-configs/cover-card-config.md](domain-configs/cover-card-config.md) 扩展点 #5

**Production Cover 必填字段：**
- content_intent（内容意图）
- visual_concept（视觉概念）
- style_direction（风格方向）
- color_palette（色彩方案）
- composition（构图说明）
- text_safe_area（文字安全区域）

---

## 视觉风格方向

- **专业商务：** 深色背景、几何构图
- **科技创新：** 渐变色、未来感
- **人文情感：** 温暖色调、人物特写
- **知识传播：** 简洁、图标化

---

## 生成示例

**场景：** 生成《时间管理的艺术》公众号封面

1. Source Lock：文章主题（四象限法）、核心观点
2. 路由到 `production_cover` 模式
3. 生成封面概念：
   - 内容意图：传授时间管理方法
   - 风格路由：专业知识类
   - 视觉概念：四象限图示 + 时钟元素
4. 输出：无文字背景图（2.35:1）+ 排版规范
5. 工程层叠加标题和作者信息

**输出：**
- 背景图：清晰的四象限视觉
- 文字安全区：上方居中区域
- 建议字体：思源黑体 Bold
- 建议字号：标题 48px，副标题 28px

---

## 架构说明

本文件采用精简版架构：
- 通用流程 → [base-card-workflow.md](base-card-workflow.md)
- 领域配置 → [domain-configs/cover-card-config.md](domain-configs/cover-card-config.md)
- 完整归档 → [legacy/cover-workflow.md](legacy/cover-workflow.md)

---

**版本：** 2.0.0（精简版）  
**基于：** base-card-workflow.md v1.0.0  
**配置文件：** cover-card-config.md v1.0.0  
**最后更新：** 2026-06-17
