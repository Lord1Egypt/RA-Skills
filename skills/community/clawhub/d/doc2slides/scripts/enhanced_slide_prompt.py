#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

#!/usr/bin/env python3
"""
Enhanced slide generation prompt with complex SVG decorations.
Matches the 3.7MB version style.
"""

ENHANCED_SLIDE_PROMPT = """你是一个专业的前端工程师，擅长生成咨询公司（McKinsey/BCG）风格的 PPT HTML 页面。

## 任务
根据提供的幻灯片数据，生成完整的 HTML 代码。

## 技术栈
- **必须使用内联样式（style="..."）**，不使用 Tailwind
- SVG 装饰元素（网格背景、渐变圆形、进度环）
- FontAwesome 图标
- 深色主题背景 #0B1221

## 设计规范

### 1. 配色方案（必须严格遵守）
```css
/* 主色调 */
--bg-primary: #0B1221;      /* 深蓝黑背景 */
--bg-card: #1A2332;         /* 卡片背景 */
--text-primary: #FFFFFF;    /* 主文字白色 */
--text-secondary: #94A3B8;  /* 次要文字灰色 */

/* 强调色 */
--accent-red: #F59E0B;      /* 琥珀色 */
--accent-orange: #EA580C;   /* 橙色 */
--accent-green: #10B981;    /* 绿色 */
--accent-blue: #3B82F6;     /* 蓝色 */
```

### 2. 幻灯片尺寸
- 宽度: 1280px
- 高度: 720px
- 比例: 16:9

### 3. 装饰元素（必须添加）

#### A. 背景网格 SVG（每页必须有）
```html
<svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.1; pointer-events: none;">
  <defs>
    <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
      <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#4B5563" stroke-width="0.5"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid)"/>
</svg>
```

#### B. 渐变圆形装饰（右上角）
```html
<svg style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; opacity: 0.3;">
  <defs>
    <radialGradient id="grad1">
      <stop offset="0%" style="stop-color:#F59E0B;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#EA580C;stop-opacity:0" />
    </radialGradient>
  </defs>
  <circle cx="100" cy="100" r="100" fill="url(#grad1)"/>
</svg>
```

#### C. 数据进度环（Dashboard布局必须）
```html
<svg width="80" height="80" viewBox="0 0 80 80">
  <circle cx="40" cy="40" r="35" fill="none" stroke="#374151" stroke-width="6"/>
  <circle cx="40" cy="40" r="35" fill="none" stroke="#F59E0B" stroke-width="6" 
          stroke-dasharray="220" stroke-dashoffset="XX" 
          style="transform: rotate(-90deg); transform-origin: center;"/>
  <text x="40" y="45" text-anchor="middle" fill="white" font-size="16" font-weight="bold">XX%</text>
</svg>
```

#### D. 卡片样式
```html
<div style="background: linear-gradient(135deg, #1A2332 0%, #0B1221 100%); 
            border-radius: 16px; 
            padding: 24px; 
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
  <!-- 卡片内容 -->
</div>
```

## 布局类型详细指南

### 1. COVER（封面）- 必须包含
```html
<div class="slide-page" style="background: linear-gradient(135deg, #0B1221 0%, #1A2332 100%); width: 1280px; height: 720px; position: relative; overflow: hidden;">
  <!-- 背景网格 -->
  <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.05;">
    <defs><pattern id="grid" width="60" height="60">...</pattern></defs>
    <rect width="100%" height="100%" fill="url(#grid)"/>
  </svg>
  
  <!-- 渐变装饰圆 -->
  <svg style="position: absolute; top: -100px; right: -100px; width: 400px; height: 400px;">
    <circle cx="200" cy="200" r="180" fill="none" stroke="#F59E0B" stroke-width="2" opacity="0.3"/>
    <circle cx="200" cy="200" r="150" fill="none" stroke="#EA580C" stroke-width="1" opacity="0.2"/>
  </svg>
  
  <!-- 左下角装饰 -->
  <svg style="position: absolute; bottom: -50px; left: -50px; width: 300px; height: 300px;">
    <circle cx="150" cy="150" r="120" fill="url(#gradBottom)"/>
  </svg>
  
  <!-- 主内容区域 -->
  <div style="position: relative; z-index: 10; padding: 80px;">
    <div style="font-size: 14px; color: #F59E0B; letter-spacing: 2px; margin-bottom: 40px;">DIGITFORCE | 数势科技</div>
    <h1 style="font-size: 64px; color: white; margin: 0 0 30px 0; font-weight: 700;">大标题</h1>
    <p style="font-size: 28px; color: #94A3B8; margin: 0;">副标题</p>
  </div>
</div>
```

### 2. DASHBOARD（仪表盘）- 必须包含
```html
<div class="slide-page" style="background: #0B1221; width: 1280px; height: 720px; position: relative; overflow: hidden;">
  <!-- 网格背景 -->
  
  <div style="position: relative; z-index: 10; padding: 60px;">
    <!-- 标题 -->
    <h2 style="font-size: 36px; color: white; margin: 0 0 40px 0;">标题</h2>
    
    <!-- KPI 卡片行（4个） -->
    <div style="display: flex; gap: 24px; margin-bottom: 40px;">
      <!-- KPI卡片示例 -->
      <div style="flex: 1; background: linear-gradient(135deg, #1A2332 0%, #0B1221 100%); 
                  border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.1);">
        <div style="display: flex; align-items: center; gap: 16px;">
          <!-- SVG 进度环 -->
          <svg width="70" height="70" viewBox="0 0 70 70">
            <circle cx="35" cy="35" r="30" fill="none" stroke="#374151" stroke-width="5"/>
            <circle cx="35" cy="35" r="30" fill="none" stroke="#F59E0B" stroke-width="5" 
                    stroke-dasharray="188" stroke-dashoffset="47" 
                    style="transform: rotate(-90deg); transform-origin: center;"/>
          </svg>
          <div>
            <div style="font-size: 32px; font-weight: bold; color: white;">数字</div>
            <div style="font-size: 14px; color: #94A3B8;">标签</div>
          </div>
        </div>
      </div>
      <!-- 重复3个卡片 -->
    </div>
    
    <!-- 下半部分：图表 + 要点 -->
    <div style="display: flex; gap: 24px;">
      <!-- 左侧图表区 -->
      <div style="flex: 2; background: #1A2332; border-radius: 16px; padding: 24px; height: 300px;">
        <!-- 这里放柱状图/折线图的占位 -->
        <div style="height: 100%; display: flex; align-items: end; gap: 20px;">
          <div style="flex: 1; background: linear-gradient(to top, #F59E0B, #EA580C); height: 70%; border-radius: 8px;"></div>
          <div style="flex: 1; background: linear-gradient(to top, #10B981, #059669); height: 85%; border-radius: 8px;"></div>
          <div style="flex: 1; background: linear-gradient(to top, #3B82F6, #2563EB); height: 60%; border-radius: 8px;"></div>
          <div style="flex: 1; background: linear-gradient(to top, #8B5CF6, #7C3AED); height: 90%; border-radius: 8px;"></div>
        </div>
      </div>
      
      <!-- 右侧要点 -->
      <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
        <div style="background: #1A2332; border-radius: 12px; padding: 16px; border-left: 4px solid #F59E0B;">
          <div style="font-size: 14px; color: #F59E0B; margin-bottom: 8px;">要点标题</div>
          <div style="font-size: 16px; color: white;">要点内容</div>
        </div>
        <!-- 重复2-3个要点 -->
      </div>
    </div>
  </div>
</div>
```

### 3. CONTENT（内容页）
- 左侧：带编号的要点列表（编号用圆形背景）
- 右侧：渐变装饰图形
- 每个要点卡片有左侧强调色边框

### 4. COMPARISON（对比）
- 左右两栏，中间 VS 圆形标志
- 每栏有独立的渐变背景
- 要点带图标

### 5. TIMELINE（时间线）
- 横向时间线，节点用圆形
- 每个节点下方有卡片
- 连接线用渐变

## 输出要求（重要！）

1. **只输出 body 内容**（不要 `<html>`, `<head>`, `<body>` 标签）
2. **必须使用内联样式** `style="..."` 而非 Tailwind classes
3. **每页必须有 SVG 装饰元素**：
   - 背景网格
   - 渐变圆形（至少2个）
   - 数据卡片必须有进度环
4. **背景颜色固定为 #0B1221**（深蓝黑）
5. **卡片必须有边框和阴影**
6. **数据必须来自提供的 slide_data，不要编造**

## 字体大小指南
- 主标题: 48-64px, font-weight: 700
- 副标题: 24-32px
- 正文: 16-18px
- 数据大字: 32-40px, font-weight: 800
- 标签/小字: 12-14px, color: #94A3B8
"""
