# 系列知识卡完整流程（Carousel Workflow）

> **本文件是精简版工作流。**  
> 完整的执行流程请参考：[base-card-workflow.md](base-card-workflow.md)

---

## 快速导航

- **完整执行流程：** [base-card-workflow.md](base-card-workflow.md)
- **领域特定规则：** [domain-configs/carousel-config.md](domain-configs/carousel-config.md)
- **完整版（已归档）：** [legacy/carousel-workflow.md](legacy/carousel-workflow.md)

---

## 领域定位

> **覆盖范围：** 系列知识卡、方法论图解、科普内容卡
> 
> **核心特点：** 多页连贯叙事，适合公众号轮播

---

## 适用场景

单一模式：**knowledge-carousel**

**典型内容：**
- 方法论讲解（如 PDCA、OKR）
- 知识点串讲
- 科普内容分解
- 教程步骤展示

---

## 执行流程

### 使用方式

1. **阅读基础流程：** [base-card-workflow.md](base-card-workflow.md) - 阶段 0-9 完整执行流程
2. **查看领域配置：** [domain-configs/carousel-config.md](domain-configs/carousel-config.md) - 系列卡特定规则
3. **应用扩展点：** 在基础流程的 9 个扩展点处，应用 carousel 的特定规则

---

## 领域特定要点

### 页面角色编排（扩展点 #5）

**标准 6-10 页结构：**
1. **封面页** - 吸引注意
2. **问题页** - 建立共鸣
3. **方法页** - 核心内容（2-3 页）
4. **步骤页** - 可执行指南（2-3 页）
5. **案例页** - 实例说明（可选）
6. **总结页** - 强化记忆 + 行动召唤

### 硬规则（扩展点 #9）
1. **Narrative Continuity** - 页面间必须有叙事连续性
2. **Information Density Control** - 每页不超过 3 个核心点
3. **Visual Consistency** - 全系列视觉风格统一

### 信息密度控制
- ✅ 每页 1-3 个核心点
- ✅ 单页文字量：100-150 字
- ❌ 避免信息过载

---

## 内容字段速查

详细字段见：[domain-configs/carousel-config.md](domain-configs/carousel-config.md) 扩展点 #5

**分页脚本必填字段：**
- total_pages（总页数）
- narrative_structure（叙事结构）
- pages[]（页面数组）
  - page_number（页码）
  - role（页面角色）
  - title（标题）
  - content（内容）
  - visual_hint（视觉提示）

---

## 视觉风格

### 书卷感风格
- 背景：米黄色、纸质感
- 字体：衬线字体（宋体）
- 装饰：书签、印章元素

### 现代简约风格
- 背景：白色、浅灰
- 字体：无衬线字体（思源黑体）
- 装饰：几何形状、色块分隔

### 插画风格
- 背景：温暖色调
- 元素：手绘插图、图标
- 风格：亲和、温馨

---

## 生成示例

**场景：** 生成《PDCA 循环法》8 页知识卡

1. Source Lock：方法论核心（Plan-Do-Check-Act）、目标 8 页
2. 路由到 `knowledge-carousel`
3. 分页脚本编排：
   - 第 1 页：封面 - "PDCA 循环法"
   - 第 2 页：问题 - "为什么执行总是偏离计划？"
   - 第 3 页：方法 - "PDCA 四步循环"
   - 第 4-7 页：步骤 - Plan/Do/Check/Act 详解
   - 第 8 页：总结 - 行动召唤
4. 选择风格：现代简约 + 书卷感
5. 批量 `engineering_rendering` 生成 8 页
6. 质量检查：叙事连贯性 + 视觉一致性

**输出：** 8 张风格统一的知识卡（1080×1440）

---

## 架构说明

本文件采用精简版架构：
- 通用流程 → [base-card-workflow.md](base-card-workflow.md)
- 领域配置 → [domain-configs/carousel-config.md](domain-configs/carousel-config.md)
- 完整归档 → [legacy/carousel-workflow.md](legacy/carousel-workflow.md)

---

**版本：** 2.0.0（精简版）  
**基于：** base-card-workflow.md v1.0.0  
**配置文件：** carousel-config.md v1.0.0  
**最后更新：** 2026-06-17
