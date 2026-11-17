# Social Card 领域配置

> **本文件定义社交媒体卡片的差异化内容。**
> 
> 完整流程请参考：[base-card-workflow.md](../base-card-workflow.md)

---

## 领域定位

**覆盖范围：** 小红书组图、Rednote、Instagram Carousel

**核心特点：** 平台适配、内容压缩、视觉导演优先

---

## 扩展点 #1：输入路由规则

```md
- 产品介绍 → 内容压缩 → social-card
- 用户明确要求小红书/社交平台 → social-card
```

---

## 扩展点 #2：Source Lock 要求

**必须明确：**
- 目标平台（小红书/Instagram/Rednote）
- 目标页数（建议 6-9 页）
- 用户意图（种草/教程/展示）

**平台规格声明：**
- 小红书：1080×1440 (3:4)
- Instagram：1080×1350 (4:5) 或 1080×1080 (1:1)

---

## 扩展点 #3：输出模式

单一模式：`social-card`

**内容压缩阶梯：**
```
长文 → 核心观点提取 → 适合社交平台的短内容
```

---

## 扩展点 #4：执行模式偏好

- 单页预览：`direct_image_preview` 可用
- 完整组图：必须 `engineering_rendering` 保证风格一致

---

## 扩展点 #5：内容字段

### 页面角色编排
```json
{
  "total_pages": 6,
  "visual_director_mode": "save_first",
  "pages": [
    {
      "page_number": 1,
      "role": "封面",
      "hook": "吸引眼球的标题",
      "visual_priority": "high"
    },
    {
      "page_number": 2,
      "role": "痛点",
      "content": "用户痛点描述"
    },
    {
      "page_number": 3,
      "role": "功能亮点",
      "features": [...]
    }
    // ... 其他页面
  ]
}
```

---

## 扩展点 #6：视觉导演规则 ⭐ 核心

### 三种导演模式

#### `save_first` - 保存优先（推荐）
**适用：** 种草、产品展示、知识科普

**特点：**
- 第 1 页：精美封面，吸引保存
- 后续页：实用内容，值得收藏
- 最后页：行动召唤

#### `click_first` - 点击优先
**适用：** 引流、活动推广

**特点：**
- 第 1 页：悬念/疑问，引导滑动
- 中间页：逐步揭晓
- 最后页：外链/联系方式

#### `brand_first` - 品牌优先
**适用：** 品牌宣传、企业号

**特点：**
- 每页都有品牌元素
- 统一视觉识别
- 强化品牌记忆

---

## 扩展点 #7：渲染包结构

```json
{
  "template": "social-card",
  "platform": "xiaohongshu",
  "dimensions": "1080×1440",
  "visual_director": "save_first",
  "batch_info": {
    "total_pages": 6,
    "style_anchor": "清新种草风",
    "consistency_rules": {
      "color_palette": ["#FF6B9D", "#FFE5EC"],
      "font_family": "思源黑体",
      "border_radius": "20px"
    }
  },
  "pages": [...]
}
```

---

## 扩展点 #8：质量标准

### Social Card 特有标准
- [ ] 第 1 页吸引力强（封面质量）
- [ ] 信息密度适合快速浏览
- [ ] 文字大小适合手机屏幕
- [ ] 符合目标平台规格（3:4 / 4:5 / 1:1）
- [ ] 视觉风格统一（全组图）

---

## 扩展点 #9：领域硬规则

### Social Card 特定硬规则
1. **Platform Spec Declaration** - 必须明确声明目标平台和画幅
2. **Visual Director Required** - 必须选择视觉导演模式
3. **Mobile-First Legibility** - 文字大小必须适合移动端

---

## 视觉系统

### 小红书风格
- 清新种草：粉色系、圆角、贴纸元素
- 干货教程：简洁、列表式、色块分隔
- 探店打卡：实景图、文字标注

### Instagram 风格
- 高级质感：深色背景、大留白
- 生活方式：自然光、柔和色调
- 创意设计：几何图形、撞色

---

**配置版本：** 1.0.0  
**对应 base-card-workflow 版本：** 1.0.0
