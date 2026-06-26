# 设计原则 - 咨询风格幻灯片

## 核心理念

**McKinsey/BCG 咨询风格** - 专业、简洁、数据驱动

## 配色系统

### 主色调：Navy（专业感）
```css
--navy-900: #0f172a;  /* 标题、重点 */
--navy-800: #1e293b;  /* 次级标题 */
--navy-700: #334155;  /* 三级元素 */
```

### 强调色（语义化）
| 颜色 | 色值 | 用途 |
|------|------|------|
| 🔴 Red | #dc2626 | 警示、关键问题 |
| 🟠 Orange | #ea580c | 警告、高优先级 |
| 🟡 Amber | #d97706 | 注意、中优先级 |
| 🟢 Green | #059669 | 成功、正向结果 |
| 🟡 Gold | #ca8a04 | 高亮、优质 |

### 使用规则
- 每张幻灯片只用一种强调色
- Navy 用于所有标题和 UI 元素
- Red/Orange 仅用于需要关注的信息

## 排版层级

### 三级信息架构

```
┌─────────────────────────────┐
│ 1. Eyebrow (小标签)          │  text-sm, uppercase, slate-400
│ 2. Title (主标题)            │  text-3xl/4xl, font-black
│ 3. Body (正文)               │  text-lg, slate-600
└─────────────────────────────┘
```

### 字体规范
- **中文字体**: Noto Sans SC
- **字重**: 300 (轻), 400 (常规), 700 (粗), 900 (黑)
- **大数字**: text-5xl, font-black, tabular-nums

## 网格系统

### 12 列网格

```html
<div class="grid grid-cols-12 gap-6">
  <div class="col-span-5">左侧内容</div>
  <div class="col-span-7">右侧内容</div>
</div>
```

### 常用布局

| 布局 | 适用 |
|------|------|
| 5:7 | Problem（左文右数）|
| 6:6 | Compare（左右对比）|
| 12 | Solution（横向流程）|
| 2x2 | Matrix（四象限）|

## 数据可视化

### 大数字 + 进度条

```html
<div class="flex items-baseline gap-6">
  <div class="w-24 text-right">
    <span class="text-5xl font-black text-red-600">67</span>
    <span class="text-2xl font-bold text-red-600">%</span>
  </div>
  <div class="flex-1">
    <div class="text-xl font-bold mb-1">指标名称</div>
    <div class="h-3 bg-slate-100 rounded-full overflow-hidden">
      <div class="h-full bg-red-500 rounded-full" style="width: 67%"></div>
    </div>
  </div>
</div>
```

**原则**：
- 数字够大（text-5xl）
- 配进度条增强视觉
- 颜色表示语义（红=问题，绿=好）

## 留白原则

### 意图性留白

```html
<!-- 外边距 -->
<div class="px-16 py-12">

<!-- 卡片内边距 -->
<div class="p-5">

<!-- 元素间距 -->
<div class="space-y-6">
<div class="gap-6">
```

**规则**：
- 不堆砌内容
- 留白 = 高级感
- 每页一个焦点

## 模板选择指南

### Problem（数据驱动）
**适用场景**：
- 市场数据呈现
- 痛点分析
- 现状调查

**特征**：
- 左侧：文字说明
- 右侧：大数字 + 进度条

### Solution（解决方案）
**适用场景**：
- 方法论展示
- 实施步骤
- 行动计划

**特征**：
- 横向 5 步流程
- Navy→Green 渐变
- 底部 3 个效果卡片

### Matrix（战略矩阵）
**适用场景**：
- 优先级分析
- 策略选择
- 四象限定位

**特征**：
- 2x2 网格
- 轴标签有意义
- 优先级徽章

### Compare（对比分析）
**适用场景**：
- 优劣势对比
- Before/After
- Do/Don't

**特征**：
- 左右两栏
- ✓/✗ 图标
- 绿/红配色

### Process（流程图）
**适用场景**：
- 业务流程
- 决策树
- 工作流

**特征**：
- 纵向流程
- 决策点菱形
- 分支标注

## 输出规格

- **分辨率**: 1200 x 675 px
- **格式**: HTML → PNG
- **比例**: 16:9

## 禁忌

❌ 多种强调色混用
❌ 大段文字堆砌
❌ 无意义的图标装饰
❌ 复杂的渐变背景
❌ 花哨的动画效果

## 必须遵守

✅ 单页单焦点
✅ 大数字够醒目
✅ 留白充分
✅ 颜色语义化
✅ 标题简洁有力（≤10字）
