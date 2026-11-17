# Cover Card 领域配置

> **本文件定义封面卡的差异化内容。**
> 
> 完整流程请参考：[base-card-workflow.md](../base-card-workflow.md)

---

## 领域定位

**覆盖范围：** 公众号封面、头图、首图、海报封面

**核心特点：** 无文字背景 + 后期文字叠加，适配 2.35:1 或 1:1 画幅

---

## 扩展点 #1：输入路由规则

```md
- 文章/PDF → 提取主题 → cover-card
- 明确封面需求 → cover-card
```

---

## 扩展点 #2：Source Lock 要求

**必须明确：**
- 文章主题/核心观点
- 目标受众
- 风格偏好（如有）

---

## 扩展点 #3：输出模式

支持 2 种封面模式：
- `draft_cover` - 草稿封面（带文字预览）
- `production_cover` - 正式封面（无文字背景 + 排版规范）

**推荐：** 正式场景使用 `production_cover`

---

## 扩展点 #4：执行模式偏好

- 草稿预览：`direct_image_preview` 可用
- 正式发布：建议 `engineering_rendering` 保证质量

---

## 扩展点 #5：内容字段

### 封面概念方法论

**必须生成：**
```md
1. 内容意图（从文章提取）
2. 风格路由（匹配受众和主题）
3. 视觉概念（具体画面描述）
```

### Production Cover 特有字段
```json
{
  "cover_type": "production",
  "content_intent": "文章核心观点",
  "visual_concept": "画面描述",
  "style_direction": "风格方向",
  "color_palette": ["#主色", "#辅色"],
  "composition": "构图说明",
  "text_safe_area": "文字安全区域说明"
}
```

---

## 扩展点 #6：视觉导演规则

不适用（cover-card 不使用视觉导演系统）

---

## 扩展点 #7：渲染包结构

### Production Cover 输出规范
```json
{
  "background_image": "无文字背景图 URL",
  "dimensions": "2.35:1 或 1:1",
  "typography_guide": {
    "title_position": "建议位置",
    "font_recommendation": "字体建议",
    "color_contrast": "对比度要求"
  }
}
```

---

## 扩展点 #8：质量标准

### 封面特有标准
- [ ] 画面主体清晰不混乱
- [ ] 预留足够文字安全区
- [ ] 色彩饱和度适合移动端
- [ ] 构图符合 2.35:1 或 1:1 画幅

---

## 扩展点 #9：领域硬规则

### Cover Card 特定硬规则
1. **Production Must Be Text-Free** - 正式封面必须无文字，文字由工程层叠加
2. **Safe Area Required** - 必须明确标注文字安全区域
3. **Mobile-First** - 构图和色彩必须适配移动端阅读

---

## 视觉系统

### 风格方向
- 专业商务：深色背景、几何构图
- 科技创新：渐变色、未来感
- 人文情感：温暖色调、人物特写
- 知识传播：简洁、图标化

### 画幅规范
- 公众号封面：2.35:1 (900×383)
- 正方形封面：1:1 (1080×1080)

---

**配置版本：** 1.0.0  
**对应 base-card-workflow 版本：** 1.0.0
