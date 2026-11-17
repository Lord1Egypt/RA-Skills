# Carousel (Knowledge Card) 领域配置

> **本文件定义系列知识卡的差异化内容。**
> 
> 完整流程请参考：[base-card-workflow.md](../base-card-workflow.md)

---

## 领域定位

**覆盖范围：** 系列知识卡、方法论图解、科普内容卡

**核心特点：** 多页连贯叙事，适合公众号轮播

---

## 扩展点 #1：输入路由规则

```md
- 长文/PDF → 知识点提取 → carousel
- 方法论内容 → 分页脚本 → carousel
```

---

## 扩展点 #2：Source Lock 要求

**必须明确：**
- 核心观点/方法论
- 目标页数（建议 6-10 页）
- 叙事结构（问题→方法→步骤→总结）

---

## 扩展点 #3：输出模式

单一模式：`knowledge-carousel`

**页面角色编排：**
1. 封面页：吸引注意
2. 问题页：建立共鸣
3. 方法页：核心内容
4. 步骤页：可执行指南
5. 总结页：强化记忆

---

## 扩展点 #4：执行模式偏好

- 单页预览：`direct_image_preview` 可用
- 完整系列：必须 `engineering_rendering` 保证一致性

---

## 扩展点 #5：内容字段

### 分页脚本
```json
{
  "total_pages": 8,
  "narrative_structure": "问题驱动型",
  "pages": [
    {
      "page_number": 1,
      "role": "封面",
      "title": "核心标题",
      "content": "简短引言",
      "visual_hint": "主视觉元素"
    },
    {
      "page_number": 2,
      "role": "问题",
      "pain_point": "用户痛点",
      "content": "问题描述"
    }
    // ... 其他页面
  ]
}
```

---

## 扩展点 #6：视觉导演规则

不适用（carousel 使用页面角色系统，不使用视觉导演）

---

## 扩展点 #7：渲染包结构

```json
{
  "template": "knowledge-carousel",
  "batch_info": {
    "total_pages": 数量,
    "style_anchor": "书卷感/编辑感",
    "consistency_rules": {
      "background": "浅色/纸质感",
      "typography": "衬线字体",
      "layout": "居中对齐"
    }
  },
  "pages": [...]
}
```

---

## 扩展点 #8：质量标准

### Carousel 特有标准
- [ ] 页面间叙事连贯
- [ ] 信息密度适中（每页 1-3 个核心点）
- [ ] 视觉风格贯穿全系列
- [ ] 最后一页有行动召唤

---

## 扩展点 #9：领域硬规则

### Carousel 特定硬规则
1. **Narrative Continuity** - 页面间必须有叙事连续性
2. **Information Density Control** - 每页信息量不超过 3 个核心点
3. **Visual Consistency Across Pages** - 全系列视觉风格必须统一

---

## 视觉系统

### 风格方向
- 书卷感：米黄背景、衬线字体、装饰元素
- 现代简约：白色背景、无衬线字体、几何形状
- 插画风格：手绘元素、温暖色调

### 页面规范
- 画幅：3:4 (1080×1440) 或方形 (1080×1080)
- 边距：上下左右各留 80px 安全区

---

**配置版本：** 1.0.0  
**对应 base-card-workflow 版本：** 1.0.0
