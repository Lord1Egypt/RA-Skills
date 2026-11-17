# 社交媒体卡片完整流程（Social Card Workflow）

> **本文件是精简版工作流。**  
> 完整的执行流程请参考：[base-card-workflow.md](base-card-workflow.md)

---

## 快速导航

- **完整执行流程：** [base-card-workflow.md](base-card-workflow.md)
- **领域特定规则：** [domain-configs/social-card-config.md](domain-configs/social-card-config.md)
- **完整版（已归档）：** [legacy/social-card-workflow.md](legacy/social-card-workflow.md)

---

## 领域定位

> **覆盖范围：** 小红书组图、Rednote、Instagram Carousel
> 
> **核心特点：** 平台适配、内容压缩、视觉导演优先

---

## 适用场景

单一模式：**social-card**

**目标平台：**
- 小红书：1080×1440 (3:4)
- Instagram：1080×1350 (4:5) 或 1080×1080 (1:1)
- Rednote：1080×1440 (3:4)

---

## 执行流程

### 使用方式

1. **阅读基础流程：** [base-card-workflow.md](base-card-workflow.md) - 阶段 0-9 完整执行流程
2. **查看领域配置：** [domain-configs/social-card-config.md](domain-configs/social-card-config.md) - 社交卡特定规则
3. **应用扩展点：** 在基础流程的 9 个扩展点处，应用 social-card 的特定规则

---

## 核心特性：视觉导演系统 ⭐

### 三种导演模式（扩展点 #6）

#### `save_first` - 保存优先 ⭐ 推荐
**适用：** 种草、产品展示、知识科普

**策略：**
- 第 1 页：精美封面，吸引保存
- 后续页：实用内容，值得收藏
- 最后页：行动召唤

**视觉特点：**
- 高颜值封面
- 信息密度中等
- 色彩和谐统一

---

#### `click_first` - 点击优先
**适用：** 引流、活动推广

**策略：**
- 第 1 页：悬念/疑问，引导滑动
- 中间页：逐步揭晓答案
- 最后页：外链/联系方式

**视觉特点：**
- 封面留悬念
- 渐进式信息披露

---

#### `brand_first` - 品牌优先
**适用：** 品牌宣传、企业号

**策略：**
- 每页都有品牌元素
- 统一视觉识别
- 强化品牌记忆

**视觉特点：**
- Logo 一致露出
- 品牌色贯穿
- 视觉符号强化

---

## 领域特定要点

### 硬规则（扩展点 #9）
1. **Platform Spec Declaration** - 必须声明目标平台和画幅
2. **Visual Director Required** - 必须选择视觉导演模式
3. **Mobile-First Legibility** - 文字大小适合移动端

### 内容压缩阶梯
```
长文（2000+ 字）
↓ 提取核心观点
中文（500-800 字）
↓ 分页编排
社交卡片内容（每页 80-120 字）
```

### 信息密度
- ✅ 每页 80-120 字
- ✅ 留白充足（安全区 80px）
- ✅ 文字大小：标题 36-48px，正文 24-28px

---

## 内容字段速查

详细字段见：[domain-configs/social-card-config.md](domain-configs/social-card-config.md) 扩展点 #5

**页面编排必填字段：**
- total_pages（总页数，建议 6-9 页）
- visual_director_mode（视觉导演模式）
- platform（目标平台）
- dimensions（画幅）
- pages[]（页面数组）
  - page_number（页码）
  - role（页面角色：封面/痛点/功能/总结）
  - content（内容）

---

## 视觉风格

### 小红书风格
- **清新种草：** 粉色系、圆角、贴纸元素
- **干货教程：** 简洁、列表式、色块分隔
- **探店打卡：** 实景图、文字标注

### Instagram 风格
- **高级质感：** 深色背景、大留白
- **生活方式：** 自然光、柔和色调
- **创意设计：** 几何图形、撞色

---

## 生成示例

**场景：** 生成产品介绍小红书 6 页组图

1. Source Lock：产品功能、目标用户、平台规格（小红书 3:4）
2. 选择视觉导演：`save_first`（种草场景）
3. 内容压缩：产品介绍 → 6 页核心卖点
4. 页面角色编排：
   - 第 1 页：封面（精美产品图）
   - 第 2 页：痛点（用户困扰）
   - 第 3-5 页：功能亮点（每页 1 个核心功能）
   - 第 6 页：总结 + 行动召唤
5. 批量 `engineering_rendering` 生成
6. 质量检查：第 1 页吸引力 + 全组图风格一致

**输出：** 6 张小红书组图（1080×1440）

---

## 架构说明

本文件采用精简版架构：
- 通用流程 → [base-card-workflow.md](base-card-workflow.md)
- 领域配置 → [domain-configs/social-card-config.md](domain-configs/social-card-config.md)
- 完整归档 → [legacy/social-card-workflow.md](legacy/social-card-workflow.md)

---

**版本：** 2.0.0（精简版）  
**基于：** base-card-workflow.md v1.0.0  
**配置文件：** social-card-config.md v1.0.0  
**最后更新：** 2026-06-17
