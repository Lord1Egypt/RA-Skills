# Design Principles for Consulting Slides

## Grid System

12カラムグリッドを基本とする。

```html
<div class="grid grid-cols-12 gap-6">
  <div class="col-span-5">Left content</div>
  <div class="col-span-7">Right content</div>
</div>
```

## Typography Hierarchy

3レベルの階層で情報を整理:

1. **Eyebrow** (text-sm, uppercase, text-slate-400)
   - カテゴリ、セクション名
   
2. **Title** (text-3xl, font-black)
   - メインメッセージ、キーポイント
   
3. **Body** (text-lg, text-slate-600)
   - 補足説明、詳細

```html
<div class="text-sm font-medium text-slate-400 tracking-wider uppercase mb-2">
  Section Label
</div>
<h1 class="text-3xl font-black text-slate-900 mb-4">
  Main Message
</h1>
<p class="text-lg text-slate-600">
  Supporting details...
</p>
```

## Color Palette

### Primary: Navy
```css
--navy-900: #0f172a;  /* Headers, emphasis */
--navy-800: #1e293b;  /* Secondary headers */
--navy-700: #334155;  /* Tertiary elements */
```

### Accent Colors
```css
--accent-red: #dc2626;    /* Alerts, critical */
--accent-orange: #ea580c; /* Warnings, high priority */
--accent-amber: #d97706;  /* Caution, medium */
--accent-green: #059669;  /* Success, positive */
--accent-gold: #ca8a04;   /* Premium, highlight */
```

### Usage Rules
- Navy for primary UI and headers
- Single accent color per slide for focus
- Reserve red/orange for critical information
- Green for positive outcomes and success states

## White Space

余白は意図的に設計する:

```html
<!-- Standard padding -->
<div class="px-16 py-12">

<!-- Card spacing -->
<div class="p-5 space-y-4">

<!-- Section gaps -->
<div class="mb-8">
```

## Data Visualization

### Large Numbers
```html
<div class="text-5xl font-black text-red-600">67%</div>
```

### Progress Bars
```html
<div class="h-3 bg-slate-100 rounded-full overflow-hidden">
  <div class="h-full bg-red-500 rounded-full" style="width: 67%"></div>
</div>
```

### Stats with Context
```html
<div class="flex items-baseline gap-6">
  <div class="w-24 text-right">
    <span class="text-5xl font-black text-red-600">67</span>
    <span class="text-2xl font-bold text-red-600">%</span>
  </div>
  <div class="flex-1">
    <div class="text-xl font-bold text-slate-900 mb-1">Description</div>
    <!-- Progress bar -->
  </div>
</div>
```

## 2x2 Matrix Rules

### Must Have Meaningful Axes

Bad: 4 items arranged in a grid
Good: 2 dimensions that create insight

```
        検証なし    検証済み
        ─────────────────────
機能あり │ Untested │ NotMet/Pass
        ├──────────┼──────────
機能なし │ Missing  │ N/A
```

### Implementation
```html
<div class="grid grid-cols-2 gap-4">
  <!-- Include axis labels -->
  <div class="text-center text-sm font-bold text-slate-500 mb-4 col-span-2">
    横軸ラベル →
  </div>
  <!-- Matrix cells -->
</div>
```

## Card Design

```html
<div class="bg-white border-2 border-{color}-200 rounded-xl p-5 relative">
  <!-- Badge -->
  <div class="absolute -top-3 -left-3 w-6 h-6 bg-{color}-500 rounded-full 
              flex items-center justify-center text-white text-xs font-bold">
    !
  </div>
  <!-- Content -->
  <div class="flex items-center gap-2 mb-3">
    <span class="text-xs font-bold text-white bg-{color}-500 px-2 py-0.5 rounded">
      LABEL
    </span>
    <span class="text-xl font-black text-{color}-700">Title</span>
  </div>
</div>
```

## Step Flow Design

```html
<div class="flex items-stretch gap-3">
  <!-- Step with connector -->
  <div class="flex-1 relative">
    <div class="bg-navy-900 text-white rounded-xl p-5 h-full flex flex-col">
      <div class="text-xs font-bold text-slate-400 mb-1">01</div>
      <div class="text-lg font-bold mb-2">Step Title</div>
      <div class="text-sm text-slate-300 mt-auto">Detail</div>
    </div>
    <!-- Connector circle -->
    <div class="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1/2 z-10 
                w-6 h-6 bg-white border-2 border-navy-700 rounded-full 
                flex items-center justify-center text-navy-700 text-xs">
      →
    </div>
  </div>
</div>
```

## Insight/Conclusion Box

```html
<div class="bg-navy-900 text-white px-5 py-4 rounded-lg">
  <div class="text-xs font-medium text-slate-400 mb-1">示唆</div>
  <div class="font-medium">Key insight message here</div>
</div>
```

## Responsive Notes

These slides are fixed at 1200x675px for consistent screenshot output.
Do not use responsive breakpoints.
