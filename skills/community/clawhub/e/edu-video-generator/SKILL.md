---
name: edu-video-generator
description: Generate educational videos programmatically using Remotion + React + Layout Components. Use when creating tutorial videos, explainer content, demo videos. Features 16 pre-built layout components, script-layout workflow, TTS integration, subtitle generation, and best practices for visual composition.
---

# Edu Video Generator v4.7

Programmatically generate educational/demo videos using Remotion + React, with 16 pre-built layout components, TTS narration, and subtitles.

---

## 🎯 核心理念

### 1. 内容决定布局，不是布局决定内容

**❌ 错误做法：** 所有场景都用居中布局，不管内容是什么
**✅ 正确做法：** 根据内容特点选择合适的布局

| 内容特点 | 推荐布局 |
|---------|---------|
| 标题/开场/结尾 | `Centered` |
| 概念 + 图示 | `SplitH`（左文右图） |
| 纯文字讲解 | `Centered` 或 `List` |
| 中心模型 + 标注 | `Diagram` |
| A vs B 对比 | `Comparison` |
| 步骤/流程 | `Timeline` 或 `ProcessFlow` |
| 数据/统计 | `NumberHighlight` |
| 要点列表 | `List` 或 `IconGrid` |
| 章节过渡 | `SceneTitle` |

### 2. 视觉元素要足够大

**❌ 错误：** 图示只占屏幕 20%，太小看不清
**✅ 正确：** 图示占屏幕 40-60%，视觉元素是主角

### 3. 文字要舒展，有呼吸感

**❌ 错误：** `lineHeight: 2`, `marginBottom: 10` — 挤在一起
**✅ 正确：** `lineHeight: 2.4`, `marginBottom: 25` — 舒展呼吸

---

## 📱 竖屏 vs 宽屏布局差异

### 分辨率选择

| 平台 | 分辨率 | 比例 |
|------|--------|------|
| 抖音/快手 | 1080×1920 | 9:16 |
| B站横版 | 1920×1080 | 16:9 |
| 小红书 | 1080×1920 | 9:16 |

### 竖屏（移动端）布局要点

**1. 字体更大**
- 标题：至少 60px（1080p 竖屏）
- 正文：至少 36px
- 字幕：12px（烧录时，移动端屏幕小）

**2. 布局纵向发展**
- 竖屏内容上下堆叠，不要左右并列
- 使用 `SplitV`（上下分屏）代替 `SplitH`
- 关键元素靠上 1/3 区域

**3. 图示占比更大**
- 竖屏空间有限，图示占 50-70% 屏幕
- 文字作为辅助说明

**4. 底部安全区**
- 字幕和重要文字距底部至少 15% 屏幕高度
- 避免被平台 UI 遮挡

### 宽屏（桌面端）布局要点

**1. 字体适中**
- 标题：40-60px
- 正文：24-32px

**2. 可以左右分屏**
- `SplitH`（左文右图）非常适合
- 图示 40-50%，文字 50-60%

**3. 留白更多**
- 左右边缘各留 10% 空间
- 视觉更舒适

---

## 🎬 移动端动效要求

### 1. 动画节奏更快

**❌ 错误：** 动画持续 60 帧，太慢
**✅ 正确：** 移动端动画 15-25 帧，干净利落

```tsx
// 桌面端
const duration = 30;

// 竖屏移动端
const duration = 15;
```

### 2. 强调"弹出"和"缩放"

移动端用户习惯快速切换画面：
- 使用 `popIn` 弹入效果（spring 动画）
- 使用 `scaleIn` 缩放效果
- 避免过于平滑的淡入淡出

### 3. 动效触发时机

- **开场**：立即触发，吸引注意
- **内容切换**：每次切换都有微动效
- **重点强调**：数字、关键词用弹跳效果

### 4. 响应式动画参数

```tsx
// 根据分辨率调整动画参数
const isVertical = height > width;
const animSpeed = isVertical ? 0.6 : 1; // 竖屏加速
const springConfig = {
  damping: isVertical ? 15 : 12,  // 竖屏阻尼更大
  stiffness: isVertical ? 200 : 100
};
```

---

## 📐 布局组件库（15个预设）

> **术语说明**：
> - **布局组件（layout）**：视觉呈现方式（如 `Centered`, `SplitH`）
> - **场景类型（type）**：语义化场景（如 `title`, `list`, `circle-divide`）
> - **关系**：一个场景类型可能使用一个或多个布局组件

### 基础布局

| 组件 | 用途 | 适用场景 |
|------|------|----------|
| `Centered` | 居中布局 | 标题、引用、强调，开场/结尾 |
| `SplitH` | 左右分屏 | 宽屏图文结合、概念+示例 |
| `SplitV` | 上下分屏 | **竖屏首选**，图文上下排列 |
| `Diagram` | 图解布局 | 中心图示 + 周围标注 |
| `Comparison` | 对比布局 | A vs B，前后对比 |
| `List` | 列表布局 | 要点、步骤、特性 |
| `LowerThird` | 下三分之一 | 人物介绍、地点标注 |
| `RuleOfThirds` | 三分法 | 主次分明、黄金比例 |

### 扩展布局

| 组件 | 用途 | 适用场景 |
|------|------|----------|
| `Timeline` | 时间线 | 步骤、流程、历史 |
| `Quote` | 引用布局 | 强调，名言，重点 |
| `NumberHighlight` | 数字强调 | 数据、统计、关键数字 |
| `ProcessFlow` | 流程图 | 流程、循环、系统 |
| `IconGrid` | 图标网格 | 特性，功能，分类 |
| `SceneTitle` | 场景标题 | 章节开头、过渡 |
| `TwoColumnList` | 双栏列表 | 对比、分类 |

### 数学推导布局（v4.5 新增）

| 组件 | 用途 | 适用场景 |
|------|------|----------|
| `ScrollingDerivation` | 滚动推导 | 数学推导、步骤演示、公式讲解 |

**核心特性**：
- 所有步骤垂直排列，镜头平滑跟随当前步骤
- 过去步骤半透明 (0.6)，未来步骤模糊 (0.3 + blur)
- Spring 动画过渡，可配置阻尼/刚度
- 支持任意 React 组件作为步骤内容
- **stepInfo 参数**：可判断当前/过去/未来步骤，实现差异化显示

**使用示例**：
```tsx
import { ScrollingDerivation, StepContainer, TitleStep, AnimatedElement, fadeIn } from "./layouts/ScrollingDerivation";
import type { DerivationStep, StepInfo } from "./layouts/ScrollingDerivation";

const steps: DerivationStep[] = [
  { 
    id: "intro", 
    render: (f, _gf, stepInfo: StepInfo) => (
      <TitleStep 
        title={stepInfo.isCurrent ? "勾股定理" : ""}  // 未激活不显示
        frame={f} 
      />
    ) 
  },
  { 
    id: "step1", 
    render: (f, _gf, stepInfo: StepInfo) => (
      <StepContainer title="基本公式" showTitle={stepInfo.isCurrent}>
        <AnimatedElement frame={f}>
          <Formula>a² + b² = c²</Formula>
        </AnimatedElement>
      </StepContainer>
    )
  },
  { 
    id: "summary", 
    render: (f) => <SummaryStep frame={f} /> 
  },
];

<ScrollingDerivation
  steps={steps}
  sceneDurations={[5, 8, 5]}  // 每个场景的秒数
  stepHeight={550}            // 每步高度（含留白）
  cameraOffset={300}          // 相机垂直偏移
  springConfig={{ damping: 15, stiffness: 80 }}
/>
```

**StepInfo 接口**：
```tsx
interface StepInfo {
  isPast: boolean;    // 是否已过去
  isCurrent: boolean; // 是否当前激活
  isFuture: boolean;  // 是否未来
}
```

**辅助组件**：
- `StepContainer` - 带标题的步骤容器（支持 `showTitle` 属性）
- `TitleStep` - 标题步骤（开头/结尾）
- `AnimatedElement` - 带淡入动画
- `ScaleElement` - 带缩放动画
- `fadeIn/fadeOut` - 工具函数
- `DERIVATION_COLORS` - 预设配色（变量颜色等）

**参数说明**：
| 参数 | 默认值 | 推荐值 | 说明 |
|------|--------|--------|------|
| `stepHeight` | 350 | **400** | 每步高度（像素），400 能看到上一步，550 适合大留白场景 |
| `cameraOffset` | 450 | 相机垂直偏移，用于居中显示 |
| `springConfig` | {damping:15, stiffness:80} | Spring 动画配置 |
| `pastOpacity` | 0.6 | 过去步骤透明度 |
| `futureOpacity` | 0.3 | 未来步骤透明度 |
| `futureBlur` | "2px" | 未来步骤模糊程度 |

**调试经验**：

1. **如何看到上一步？**
   - `stepHeight` 设置为 **400px**（不能太大，否则只显示当前步）
   - `hideInactive={false}` 才能显示过去/未来步骤
   - `pastOpacity=0.6` 让上一步半透明可见

2. **为什么只显示当前步骤？**
   - 检查 `hideInactive` 是否为 `false`
   - 检查 `stepHeight` 是否过大（超过 500px）
   - 检查 `padding` 是否过大（超过 350px）

3. **上下文可见性最佳配置**：
   ```tsx
   <ScrollingDerivation
     steps={steps}
     sceneDurations={sceneDurations}
     stepHeight={400}           // 🔥 固定 400px
     padding={300}              // 🔥 留白 300px
     gap={30}                   // 🔥 间距 30px
     hideInactive={false}       // 🔥 显示上下文
     pastOpacity={0.6}          // 上一步 60% 透明
     futureOpacity={0.3}        // 下一步 30% 透明
   />
   ```

**最佳实践**：
1. **未激活步骤隐藏标题**：使用 `stepInfo.isCurrent` 控制 `showTitle`
2. **统一数学参数**：定义 `MATH` 常量，所有图形共用
3. **彩虹公式**：变量用彩色（r=青, π=黄, S=红），符号用白色

### 辅助组件

| 组件 | 用途 |
|------|------|
| `TextBlock` | 文字块（标题 + 多行文字） |
| `IconBox` | 图标容器 |
| `Card` | 卡片容器 |
| `DecorativeBackground` | 装饰性背景（星星等） |
| `AnimatedNumber` | 数字动画 |

---

## 🔄 工作流：脚本 + 布局关联

### 内容脚本格式 (content.json)

```json
{
  "meta": {
    "title": "视频标题",
    "voice": "zh-CN-XiaoxiaoNeural",
    "resolution": {
      "width": 1080,
      "height": 1920
    }
  },
  "scenes": [
    {
      "id": "intro",
      "layout": "Centered",
      "duration": 15,
      "content": {
        "title": "开场标题",
        "subtitle": "副标题",
        "icon": "graduation-cap"
      },
      "narration": "旁白文本..."
    }
  ]
}
```

### 完整工作流

```
1. 📝 编写内容脚本 (content.json) - 指定每个场景的布局
2. 🎙️ 生成 TTS 配音 (edge-tts)
3. ⏱️ 获取配音时长，更新场景时长
4. 📄 生成 SRT 字幕（按字数分配时间，单行限制）
5. 🎬 根据脚本生成视频组件（使用指定布局）
6. 🖼️ 渲染视频画面
7. 🔀 合并音频 + 烧录字幕
8. 📦 压缩视频（可选，用于 QQ 发送）
```

---

## 🚀 快速开始

### 使用模板（推荐，快 10 倍）

```bash
# 复制模板
cp -r ~/.openclaw/workspace/_templates/video-template ~/.openclaw/workspace/projects/my-video
cd my-video

# 依赖几乎秒装
pnpm install

# 复制布局组件库 + 配置文件
cp ~/.openclaw/workspace/skills/edu-video-generator/components/layouts.js src/components/
cp ~/.openclaw/workspace/skills/edu-video-generator/config.js scripts/

# 开始创作
# 1. 编辑 scripts/content.json（设置 meta.resolution）
# 2. 生成配音、字幕、视频
```

### 项目结构

```
my-video/
├── scripts/
│   ├── content.json           # 📝 内容脚本（含布局指定）
│   ├── config.js              # ⭐ 统一配置（自动适配参数）
│   ├── audio-metadata.json    # 配音元数据
│   ├── 01-generate-audio.js   # TTS 生成
│   ├── 02-generate-srt.js     # 字幕生成（读取 config.js）
│   └── 03-generate-video.js   # 视频组件生成（读取 config.js）
├── audio/
│   └── merged.mp3             # 合并后的音频
├── src/
│   ├── index.ts
│   └── components/
│       ├── Root.tsx
│       ├── Video.tsx           # 视频组件
│       └── layouts.js          # 📐 布局组件库（复制自 skill 的 components/）（复制自 skill）
├── out/
│   └── final.mp4               # 最终视频
└── subtitles.srt               # 字幕
```

---

## 📐 布局组件使用示例

### Centered - 居中布局

```tsx
<Centered
  frame={frame}
  background="radial"
  title="一块披萨的冒险"
  subtitle="食物消化之旅"
  icon={<PizzaIcon />}
/>
```

### SplitH - 左右分屏（宽屏）

```tsx
<SplitH
  frame={frame}
  leftContent={(f) => (
    <TextBlock
      frame={f}
      title="口腔的工作"
      lines={["牙齿切碎食物", "唾液混合"]}
    />
  )}
  rightContent={(f) => <ChewingAnimation frame={f} />}
  leftWidth={0.55}
  rightWidth={0.45}
/>
```

### SplitV - 上下分屏（竖屏）

```tsx
<SplitV
  frame={frame}
  topContent={(f) => <DiagramVisual frame={f} />}
  bottomContent={(f) => (
    <TextBlock
      frame={f}
      title="核心要点"
      lines={["要点1", "要点2"]}
    />
  )}
  topHeight={0.55}
  bottomHeight={0.45}
/>
```

### Diagram - 图解布局

```tsx
<Diagram
  frame={frame}
  title="神奇的蠕动"
  diagram={<EsophagusAnimation frame={frame} />}
  caption="食道会像挤牙膏一样把食物推下去"
/>
```

### Timeline - 时间线

```tsx
<Timeline
  frame={frame}
  title="披萨的完整旅程"
  orientation="horizontal"
  steps={[
    { title: "口腔", subtitle: "几秒~几分钟" },
    { title: "食道", subtitle: "8-10秒" },
    { title: "胃", subtitle: "2-4小时" },
    { title: "小肠", subtitle: "3-5小时" },
    { title: "大肠", subtitle: "12-36小时" },
  ]}
/>
```

### NumberHighlight - 数字强调

```tsx
<NumberHighlight
  frame={frame}
  title="胃的惊人数据"
  stats={[
    { value: "3", label: "升胃液/天", color: COLORS.accent1 },
    { value: "1.5", label: "pH值", color: COLORS.accent5 },
    { value: "4", label: "小时消化", color: COLORS.accent6 },
  ]}
  description="胃液酸度能溶解金属！"
/>
```

### LowerThird - 下三分之一

```tsx
<LowerThird
  frame={frame}
  title="爱因斯坦"
  subtitle="物理学家"
  position="left"
  color={COLORS.accent2}
>
  <PortraitImage />
</LowerThird>
```

---

## 🧩 辅助组件

### TextBlock - 文字块

```tsx
<TextBlock
  frame={frame}
  title="口腔的工作"
  titleDelay={0}
  lineDelay={18}
  lines={["牙齿切碎食物", "舌头搅拌混合", "唾液开始消化"]}
/>
```

### IconBox - 图标容器

```tsx
<IconBox color={COLORS.accent2} size={60}>
  <LucideIcon size={32} />
</IconBox>
```

### Card - 卡片

```tsx
<Card frame={frame} delay={15} color={COLORS.accent1}>
  <h3>标题</h3>
  <p>内容...</p>
</Card>
```

### DecorativeBackground - 装饰背景

```tsx
<DecorativeBackground
  type="stars"
  frame={frame}
  count={30}
  width={1280}
  height={720}
/>
```

### AnimatedNumber - 动画数字

```tsx
<AnimatedNumber value={100} frame={frame} startFrame={20} duration={30} />
```

---

## 🎬 动画工具函数

### 竖屏移动端专用动画

```tsx
import { spring, interpolate } from 'remotion';

// 快速弹入（移动端）
export const popInMobile = (frame, startFrame) =>
  spring({ fps: 30, frame: Math.max(0, frame - startFrame), config: { damping: 15, stiffness: 200 } });

// 快速淡入（移动端）
export const fadeInMobile = (frame, startFrame, duration = 12) =>
  interpolate(frame, [startFrame, startFrame + duration], [0, 1], { extrapolateRight: 'clamp' });

// 向上滑入（移动端）
export const slideUpMobile = (frame, startFrame, distance = 30) =>
  interpolate(frame, [startFrame, startFrame + 15], [distance, 0], { extrapolateRight: 'clamp' });
```

### 响应式字体计算

```tsx
// 竖屏字体更大
const titleSize = Math.min(width * 0.08, height * 0.1);  // 约 80-150px
const textSize = Math.min(width * 0.04, height * 0.05);    // 约 40-80px
```

---

## ⚠️ 常见陷阱

### 1. Lucide 图标名错误 → React Error #130

**症状：** `Minified React error #130` - "Element type is invalid... got: undefined"

**原因：** 使用了 lucide-react 中不存在的图标名

**调试：**
```bash
# 检查图标是否存在
node -e "const icons = require('lucide-react'); console.log('Bricks:', !!icons['Bricks']);"

# 搜索相关图标
node -e "const icons = require('lucide-react'); console.log(Object.keys(icons).filter(n => n.toLowerCase().includes('brick')).join(', '));"
```

**常见错误：**
- ❌ `Bricks` → 不存在
- ✅ `BrickWall`, `ToyBrick`, `Blocks` → 正确

### 2. 文字挤在一起

**错误：** `lineHeight: 2`, `marginBottom: 10`
**正确：** `lineHeight: 2.4`, `marginBottom: 25`

### 3. 图示太小

**错误：** 图示只占屏幕 20%
**正确：** 竖屏 50-70%，宽屏 40-60%

### 4. 字幕问题

#### 字幕字体大小
- 竖屏：FontSize = 12（移动端屏幕小，字幕要小）
- **宽屏：FontSize = 16**（桌面端屏幕大，字幕可以稍大）
- 建议：先在小程序测试再批量生成

#### 字幕单行字数限制（重要！）
- **竖屏：每行 ≤14 字**（10 字太少，14 字较合适）
- **宽屏：每行 ≤20 字**（表格统一标准）
- 智能拆分：按标点优先拆分，超长强制切断

#### 字幕时间同步（重要！）
- Video.tsx 和 Root.tsx **必须从 audio-metadata.json 读取实际时长**
- **禁止硬编码时长**（会导致字幕和画面不同步）

#### 字幕底部留白
- 竖屏：MarginV = 20px
- 宽屏：MarginV = 12px

#### 字幕重复问题
- **画面上不要渲染旁白文字**，只显示标题、图示、公式
- 旁白由字幕显示，避免重复

### 5. 动画太慢

**错误：** 动画持续 60 帧
**正确：** 竖屏 10 帧，宽屏 20 帧（config.js 标准）

### 6. 字幕不同步

**原因：** Video.tsx 硬编码时长，和实际音频不一致
**解决：** 从 audio-metadata.json 读取实际时长

```javascript
// ❌ 错误：硬编码时长
const scenes = [
  { id: "intro", duration: 5 },  // 写死了！
];

// ✅ 正确：从元数据读取
const metadata = require('../../scripts/audio-metadata.json');
const scenes = metadata.map(m => ({
  id: m.id,
  duration: m.duration  // 实际音频时长
}));
```

**Root.tsx 同理：**
```javascript
// ✅ 正确：动态计算总帧数
const metadata = require('../scripts/audio-metadata.json');
const totalDuration = metadata.reduce((sum, m) => sum + m.duration, 0);
const durationInFrames = Math.ceil(totalDuration * 30);  // 30fps
```

### 7. 字幕拆分问题

**原因：** 长句没有拆分，超出屏幕宽度
**解决：** 智能拆分，每行≤14字（竖屏）/≤20字（宽屏）

```javascript
// 02-generate-srt.cjs
const MAX_CHARS = config.subtitle.maxCharsPerLine;  // 从 config 读取

function splitText(text, maxChars) {
  const parts = [];
  let current = '';
  
  for (const char of text) {
    current += char;
    // 遇到标点且长度够一半就切分
    if (/[，。！？、；：]/.test(char) && current.length >= maxChars * 0.6) {
      parts.push(current.trim());
      current = '';
    }
  }
  
  if (current.trim()) parts.push(current.trim());
  
  // 超长的强制切分
  return parts.flatMap(p => 
    p.length <= maxChars ? [p] : 
    Array.from({length: Math.ceil(p.length/maxChars)}, (_, i) => 
      p.slice(i*maxChars, (i+1)*maxChars)
    )
  );
}
```

### 8. 图示动画过于简单

**问题：** 使用简单 div 渐变代替 SVG 动画，视觉效果差
**解决：** 使用 SVG 绘制图示，添加动画效果

**❌ 错误做法：**
```tsx
// 只是渐变圆形，没有动画
<div style={{
  width: 300,
  height: 300,
  borderRadius: '50%',
  background: `radial-gradient(...)`
}} />
```

**✅ 正确做法：**
```tsx
// SVG 分割线动画
<svg width={400} height={400} viewBox="0 0 400 400">
  <circle cx="200" cy="200" r="160" fill="none" stroke={COLORS.accent2} strokeWidth={4} />
  {Array.from({ length: 8 }).map((_, i) => {
    const angle = (i * 45) * Math.PI / 180;
    return (
      <line 
        key={i} 
        x1="200" y1="200" 
        x2={200 + 160 * Math.cos(angle)} 
        y2={200 + 160 * Math.sin(angle)} 
        stroke={COLORS.accent1} 
        strokeWidth={3} 
        opacity={fadeIn(f, 15 + i * 3, 8)}  // 依次出现
      />
    );
  })}
</svg>
```

**关键点：**
- 使用 SVG 绘制几何图形
- 每个元素独立动画（依次出现）
- fadeIn/popup 效果增强视觉

---

## 🔧 技术配置

### 依赖版本

```json
{
  "dependencies": {
    "@remotion/bundler": "^4.0.0",
    "@remotion/cli": "^4.0.0",
    "@remotion/renderer": "^4.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "remotion": "^4.0.0"
  }
}
```

### 字体安装

```bash
# 中文字体
apt-get install -y fonts-noto-cjk fonts-wqy-zenhei

# 刷新字体缓存
fc-cache -fv
```

### 颜色系统

```javascript
const COLORS = {
  // 背景
  bg1: '#0f0f23',
  bg2: '#1a1a3e',
  bg3: '#2d2d5a',
  
  // 强调色
  accent1: '#ff6b6b',  // 红
  accent2: '#4ecdc4',  // 青
  accent3: '#ffe66d',  // 黄
  accent4: '#95e1d3',  // 浅青
  accent5: '#a78bfa',  // 紫
  accent6: '#f97316',  // 橙
  
  // 文字
  white: '#ffffff',
  gray: '#94a3b8',
};
```

---

## 🔧 脚本自动适配规范（重要！）

> ⚠️ **核心原则：所有脚本必须从 content.json 读取分辨率，自动适配参数，禁止硬编码！**

### 问题根源

**❌ 常见错误：**
```javascript
// 03-generate-video.js 硬编码字体
titleStyle: { fontSize: 48 }  // 写死了！
```

**✅ 正确做法：**
```javascript
// 读取分辨率，动态计算
const content = require('./content.json');
const { width, height } = content.meta.resolution;
const isVertical = height > width;
const titleSize = isVertical ? Math.min(width * 0.08, 80) : 48;
```

---

### 统一配置文件 scripts/config.js

**每个项目都应该有这个文件！** 自动根据分辨率返回所有参数：

```javascript
// scripts/config.js
const fs = require('fs');
const path = require('path');

// 读取 content.json
const contentPath = path.join(__dirname, 'content.json');
const content = JSON.parse(fs.readFileSync(contentPath, 'utf-8'));
const { width, height } = content.meta.resolution;

// 判断方向
const isVertical = height > width;
const isMobile = isVertical; // 竖屏 = 移动端

// 自动计算所有参数
module.exports = {
  // 基础信息
  width,
  height,
  isVertical,
  isMobile,

  // 字体大小
  fonts: {
    title: isVertical ? Math.min(width * 0.08, 80) : 48,
    subtitle: isVertical ? Math.min(width * 0.05, 50) : 32,
    body: isVertical ? Math.min(width * 0.04, 40) : 28,
    caption: isVertical ? Math.min(width * 0.035, 35) : 24,
  },

  // 间距
  spacing: {
    lineHeight: isVertical ? 2.6 : 2.4,
    marginBottom: isVertical ? 30 : 20,
    paddingHorizontal: isVertical ? width * 0.08 : width * 0.1,
    paddingVertical: isVertical ? height * 0.05 : height * 0.04,
  },

  // 字幕参数（烧录时）
  subtitle: {
    fontSize: isVertical ? 12 : 16,
    marginV: isVertical ? 20 : 15,  // 竖屏距底部 20px
    maxCharsPerLine: isVertical ? 14 : 20,  // 竖屏每行14字，宽屏20字
  },

  // 动画参数
  animation: {
    fadeIn: isVertical ? 10 : 20,      // 竖屏更快
    slideIn: isVertical ? 12 : 20,
    spring: {
      damping: isVertical ? 15 : 12,
      stiffness: isVertical ? 200 : 100,
    },
  },

  // 布局偏好
  layout: {
    diagramRatio: isVertical ? 0.6 : 0.5,  // 图示占比
    textRatio: isVertical ? 0.4 : 0.5,     // 文字占比
    preferredSplit: isVertical ? 'SplitV' : 'SplitH',  // 首选分屏方式
  },

  // 安全区（避免被 UI 遮挡）
  safeArea: {
    top: isVertical ? height * 0.1 : height * 0.05,
    bottom: isVertical ? height * 0.15 : height * 0.05,
    left: isVertical ? width * 0.05 : width * 0.08,
    right: isVertical ? width * 0.05 : width * 0.08,
  },
};
```

---

### 02-generate-srt.js 规范

**必须读取 config.js：**

```javascript
// scripts/02-generate-srt.js
const config = require('./config');

// 生成字幕时使用配置
const subtitleStyle = `Fontname=Noto Sans CJK SC,FontSize=${config.subtitle.fontSize},MarginV=${config.subtitle.marginV},Alignment=2`;

// 单行字数限制
const maxChars = config.subtitle.maxCharsPerLine;
```

---

### 03-generate-video.js 规范

**必须读取 config.js：**

```javascript
// scripts/03-generate-video.js
const config = require('./config');

// 生成 Video.tsx 时注入配置
const videoCode = `
const CONFIG = ${JSON.stringify(config, null, 2)};

// 使用配置
const titleStyle = {
  fontSize: CONFIG.fonts.title,
  lineHeight: CONFIG.spacing.lineHeight,
  marginBottom: CONFIG.spacing.marginBottom,
};

// 动画参数
const fadeInDuration = CONFIG.animation.fadeIn;
const springConfig = CONFIG.animation.spring;
`;
```

---

### render.mjs 规范

**必须读取 content.json 判断分辨率：**

```javascript
// render.mjs
import fs from 'fs';

const content = JSON.parse(fs.readFileSync('./scripts/content.json', 'utf-8'));
const { width, height } = content.meta.resolution;
const isVertical = height > width;

// 自动选择字幕参数（统一规范）
const subtitleFontSize = isVertical ? 12 : 16;
const subtitleMarginV = isVertical ? 20 : 15;

// 渲染后烧录字幕（自动适配）
const subtitleFilter = `subtitles='subtitles.srt':force_style='Fontname=Noto Sans CJK SC,FontSize=${subtitleFontSize},MarginV=${subtitleMarginV},Alignment=2'`;
```

---

### 模板应包含 config.js

**video-template 模板目录：**
```
video-template/
├── scripts/
│   ├── content.json.example    # 📝 内容脚本示例
│   ├── config.js               # ⭐ 统一配置（自动适配参数）
│   ├── 01-generate-audio.js
│   ├── 02-generate-srt.js
│   └── 03-generate-video.js
├── src/
│   └── components/
│       └── layouts.js          # 布局组件（复制自 skill 的 components/）
├── render.mjs                  # 渲染脚本（自动适配字幕）
└── package.json
```

---

### 参数速查表

| 参数 | 竖屏 (1080×1920) | 宽屏 (1920×1080) |
|------|------------------|------------------|
| 标题字体 | 72-80px | 48-56px |
| 正文字体 | 36-40px | 28-32px |
| 行高 | 2.6 | 2.4 |
| 字幕字体 | 12px | 16px |
| 字幕底部留白 | 20px | 15px |
| 每行字幕字数 | ≤14 | ≤20 |
| 淡入动画 | 10帧 | 20帧 |
| 弹入阻尼 | 15 | 12 |
| 弹入刚度 | 200 | 100 |
| 图示占比 | 60% | 50% |
| 首选分屏 | SplitV | SplitH |

---

## 🎬 渲染命令

### 基础渲染

```bash
node render.mjs
```

### 合并音频 + 烧录字幕

```bash
# 合并音频
ffmpeg -y -f concat -safe 0 -i audio/list.txt -c copy audio/merged.mp3

# 添加音频到视频
ffmpeg -y -i video.mp4 -i audio/merged.mp3 \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest \
  video-with-audio.mp4

# 竖屏字幕（移动端）- 字体 12px，底部留白 20px，每行≤14字
ffmpeg -y -i video-with-audio.mp4 \
  -vf "subtitles='subtitles.srt':force_style='Fontname=Noto Sans CJK SC,FontSize=12,MarginV=20,Alignment=2'" \
  -c:a copy final.mp4

# 宽屏字幕 - 字体 16px，底部留白 15px，每行≤20字
ffmpeg -y -i video-with-audio.mp4 \
  -vf "subtitles='subtitles.srt':force_style='Fontname=Noto Sans CJK SC,FontSize=16,MarginV=15,Alignment=2'" \
  -c:a copy final.mp4
```

### 压缩视频（用于 QQ 发送）

```bash
ffmpeg -y -i final.mp4 \
  -c:v libx264 -b:v 250k -preset slower \
  -c:a aac -b:a 64k \
  -movflags +faststart \
  final-small.mp4
```

---

## 📊 布局选择指南

### 竖屏（移动端）

```
1. 有图示/动画吗？
   └─ 是 → SplitV（上下分屏）或 Diagram

2. 纯文字/标题吗？
   └─ 是 → Centered（大字）

3. 有对比吗？
   └─ 是 → 上下排列的对比卡片

4. 有流程/步骤吗？
   └─ 是 → Timeline（纵向）

5. 有数据/数字吗？
   └─ 是 → NumberHighlight

6. 是开场/结尾吗？
   └─ 是 → Centered
```

### 宽屏（桌面端）

```
1. 有图示/动画吗？
   └─ 是 → SplitH（左文右图）或 Diagram

2. 纯文字吗？
   └─ 是 → Centered 或 List

3. 有对比吗？
   └─ 是 → Comparison 或 TwoColumnList

4. 有流程/步骤吗？
   └─ 是 → Timeline（横向）

5. 有数据/数字吗？
   └─ 是 → NumberHighlight

6. 是章节过渡吗？
   └─ 是 → SceneTitle

7. 是开场/结尾吗？
   └─ 是 → Centered
```

---

## 🐛 调试技巧

### 验证图标存在

```bash
node -e "const icons = require('lucide-react'); console.log('IconName:', !!icons['IconName']);"
```

### 检查视频帧

```bash
ffmpeg -i video.mp4 -ss 00:01:00 -vframes 1 -f image2 frame.png
```

### 检查音频时长

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 audio/merged.mp3
```

---

## ✅ 检查清单

### 项目初始化
- [ ] 使用 pnpm + 模板（快 10 倍）
- [ ] 复制布局组件库 `components/layouts.js` 到 `src/components/`
- [ ] **复制 config.js 到 scripts/**
- [ ] content.json 中指定 meta.resolution

### 脚本规范（必须遵守！）
- [ ] **02-generate-srt.js 读取 config.js**
- [ ] **03-generate-video.js 读取 config.js**
- [ ] **render.mjs 读取 content.json 判断分辨率**
- [ ] **禁止硬编码字体、间距、字幕参数**

### 内容与布局
- [ ] content.json 中指定每个场景的 layout
- [ ] 竖屏/宽屏选择正确分辨率
- [ ] 竖屏：字体更大、图示占比更高、动画更快
- [ ] 文字舒展（lineHeight: 2.4+, marginBottom: 20+）
- [ ] **画面上不渲染旁白文字**（避免和字幕重复）

### 字幕同步（重要！）
- [ ] **Video.tsx 从 audio-metadata.json 读取时长**
- [ ] **Root.tsx 动态计算总帧数**
- [ ] **禁止硬编码场景时长**
- [ ] 字幕按字数分配时间
- [ ] 字幕生成使用 config.js 的 maxCharsPerLine

### 字幕显示
- [ ] 竖屏字幕 FontSize = 12, MarginV = 20
- [ ] **宽屏字幕 FontSize = 16, MarginV = 15**
- [ ] 字幕单行限制（**竖屏 ≤14 字**，**宽屏 ≤20 字**）
- [ ] **画面上不渲染旁白文字**（避免和字幕重复）

### 图示动画（v4.3 新增）
- [ ] **图示场景使用 SVG 动画**，禁止简单 div 渐变
- [ ] 每个元素独立动画（依次出现）
- [ ] 使用 fadeIn/popIn 增强视觉效果

### 数学严谨性（v4.3 新增）
- [ ] **尺寸严格对应**（同一个变量在不同场景中成比例）
- [ ] **颜色语义一致**（同一个变量用同一个颜色）
- [ ] **符号标注清晰**（所有关键长度都标注 r, πr, πr² 等）
- [ ] **公式推导有据**（每一步都有数学依据）

### 其他
- [ ] TTS 并行生成（Promise.all）
- [ ] Lucide 图标名正确
- [ ] QQ 发送前压缩视频（<10MB）
- [ ] **公式外层容器设置默认颜色**（否则 `=` 和 `²` 会是黑色）
- [ ] **彩虹公式：变量用彩色，符号用白色**

### 滚动推导布局（v4.7 新增）
- [ ] **步骤高度适中**：`stepHeight=400`（能看到上一步）
- [ ] **显示上下文**：`hideInactive={false}`
- [ ] **透明度控制**：`pastOpacity=0.6`, `futureOpacity=0.3`
- [ ] **SVG 缩放**：直接修改 width/height 属性（不用 transform scale）
- [ ] **公式放大**：SVG width/height × scale 系数

---

---

## 📐 数学推导严谨性规范（v4.3 新增）

### 核心矛盾

**动态脚本（灵活） vs 数学严谨性（固定）**

- ❌ 每个场景手写参数 → 不可维护
- ✅ 定义「变量系统」+「场景类型」→ 自动计算

---

### 解决方案：三层架构（⏳ 计划中功能）

> ⚠️ **当前状态**：此架构为 v4.4 设计，**尚未实现**。
> 
> **当前可用方案**：
> - 直接复制 `components/layouts.js` 到项目
> - 手写 Video.tsx，参考 `components/Video.example.tsx`
> - 使用 `config.js` 统一参数管理

```
┌─────────────────────────────────────────┐
│  1. 变量层 (content.json)               │
│     - 定义数学变量: R, N, colors         │
│     - 定义推导链: 圆 → 扇形 → 长方形      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  2. 场景类型层 (scene-types.js)          │
│     - circle-divide: 等分圆              │
│     - slices-arrange: 扇形排列           │
│     - rectangle-derive: 长方形推导        │
│     - formula-result: 公式展示           │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  3. 渲染层 (Video.tsx)                   │
│     - 根据场景类型 + 变量 → 自动渲染       │
│     - 尺寸/颜色自动计算                   │
└─────────────────────────────────────────┘
```

---

### 1. 变量层：content.json 扩展

**当前 content.json（只有文字）：**
```json
{
  "scenes": [
    { "id": "step1", "narration": "把圆等分成若干扇形" }
  ]
}
```

**升级后（变量 + 场景类型）：**
```json
{
  "meta": {
    "title": "圆的面积",
    "resolution": { "width": 1920, "height": 1080 }
  },
  
  "variables": {
    "R": 80,
    "N": 10,
    "sliceColors": ["#ff6b6b", "#4ecdc4", "#ffe66d", "#95e1d3", "#a78bfa", "#ff6b6b", "#4ecdc4", "#ffe66d", "#95e1d3", "#a78bfa"],
    "colorRadius": "#4ecdc4",
    "colorPi": "#ffe66d",
    "colorArea": "#ff6b6b"
  },
  
  "derivationChain": [
    { "from": "circle", "to": "slices", "operation": "divide", "params": { "n": "$N" } },
    { "from": "slices", "to": "rectangle", "operation": "arrange", "params": { "width": "$R", "length": "π*$R" } }
  ],
  
  "scenes": [
    {
      "id": "intro",
      "type": "title",          // 场景类型（语义）
      // type 会自动映射到合适的布局组件（如 Centered）
      "title": "圆的面积推导",
      "visual": { "shape": "circle", "radius": "$R", "showRadius": true },
      "narration": "今天我们来推导圆的面积公式。"
    },
    {
      "id": "step1",
      "type": "circle-divide",
      "title": "等分圆",
      "visual": { 
        "shape": "circle", 
        "radius": "$R", 
        "divideInto": "$N",
        "showNumbers": true,
        "colors": "$sliceColors"
      },
      "narration": "把圆等分成 {N} 个扇形，每个扇形有唯一颜色和编号。"
    },
    {
      "id": "step2",
      "type": "slices-arrange",
      "title": "扇形排列",
      "visual": {
        "shape": "slices",
        "count": "$N",
        "height": "$R",
        "colors": "$sliceColors",
        "showNumbers": true
      },
      "narration": "将 {N} 个扇形交错排列，高度等于半径 R。"
    },
    {
      "id": "step3",
      "type": "rectangle-derive",
      "title": "长方形推导",
      "visual": {
        "shape": "rectangle",
        "width": "$R",
        "length": "π*$R",
        "showSlices": true,
        "colors": "$sliceColors"
      },
      "narration": "长方形的宽等于 R，长等于 πR，面积等于 πR 乘 R 等于 πR 平方。"
    }
  ]
}
```

**关键点：**
- `$R` 表示变量引用
- `type` 指定场景类型
- `visual` 定义视觉元素（不是写死的 SVG）

---

### 2. 场景类型层：scene-types.js

#### 场景类型完整列表（⏳ 计划中）

| 场景类型 | 对应布局 | 用途 | 实现状态 |
|----------|----------|------|----------|
| `title` | Centered | 标题/开场 | ⏳ |
| `text-list` | List | 要点列表 | ⏳ |
| `text-center` | Centered | 纯文字居中 | ⏳ |
| `diagram` | Diagram | 中心图+标注 | ⏳ |
| `comparison` | Comparison | A vs B 对比 | ⏳ |
| `timeline` | Timeline | 时间线/流程 | ⏳ |
| `number-highlight` | NumberHighlight | 数字强调 | ⏳ |
| `quote` | Quote | 引用/强调 | ⏳ |
| `scene-title` | SceneTitle | 章节过渡 | ⏳ |
| `icon-grid` | IconGrid | 图标网格 | ⏳ |
| **`circle-divide`** | SVG | 等分圆 | ✅ 示例 |
| **`slices-arrange`** | SVG | 扇形排列 | ✅ 示例 |
| **`rectangle-derive`** | SVG | 长方形推导 | ✅ 示例 |

> 注：前10种场景类型将复用 `layouts.js` 中的布局组件，后3种为数学推导专用。

#### 示例代码（3种数学推导场景）

```javascript
// 场景类型定义（⏳ 计划中功能，当前仅示例）
const SCENE_TYPES = {
  
  // 等分圆
  'circle-divide': {
    render: (vars, visual, frame) => {
      const { R, N, sliceColors } = vars;
      const { divideInto, showNumbers } = visual;
      
      return (
        <svg viewBox="0 0 300 300">
          {Array.from({ length: divideInto }).map((_, i) => {
            const startAngle = (i * 360 / divideInto - 90) * Math.PI / 180;
            const endAngle = ((i + 1) * 360 / divideInto - 90) * Math.PI / 180;
            // ... 绘制扇形
            return <path fill={sliceColors[i]} />;
          })}
          {showNumbers && <text>{i + 1}</text>}
        </svg>
      );
    }
  },
  
  // 扇形排列
  'slices-arrange': {
    render: (vars, visual, frame) => {
      const { R, N, sliceColors } = vars;
      const { height, colors, showNumbers } = visual;
      
      // 自动计算：高度必须等于 vars.R
      const actualHeight = height === '$R' ? vars.R : height;
      
      return (
        <svg viewBox="0 0 450 300">
          {Array.from({ length: N }).map((_, i) => {
            // ... 绘制扇形，高度=actualHeight
          })}
        </svg>
      );
    }
  },
  
  // 长方形推导
  'rectangle-derive': {
    render: (vars, visual, frame) => {
      const { R, sliceColors, colorRadius, colorPi, colorArea } = vars;
      const { width, length, showSlices } = visual;
      
      // 自动计算尺寸
      const actualWidth = width === '$R' ? vars.R : width;
      const actualLength = length === 'π*$R' ? Math.PI * vars.R : length;
      
      return (
        <svg viewBox="0 0 500 300">
          {/* 长方形 */}
          <rect width={actualLength} height={actualWidth} />
          
          {/* 内部扇形条（如果 showSlices）*/}
          {showSlices && sliceColors.map((color, i) => (
            <rect fill={color} width={actualLength / N} height={actualWidth} />
          ))}
          
          {/* 标注 */}
          <text fill={colorRadius}>宽=R</text>
          <text fill={colorPi}>长=πR</text>
        </svg>
      );
    }
  }
};
```

**关键点：**
- 每种场景类型有固定渲染逻辑
- 自动计算尺寸（根据变量引用）
- 颜色/编号自动对应（因为引用同一个 sliceColors）

---

### 3. 渲染层：Video.tsx

```tsx
// Video.tsx 只需要调度，不需要手写 SVG
import { SCENE_TYPES } from './scene-types';
import content from '../../scripts/content.json';

// 解析变量引用（安全实现）
function resolveValue(value, vars) {
  if (typeof value === 'string' && value.startsWith('$')) {
    return vars[value.slice(1)];
  }
  if (typeof value === 'string' && value.includes('$')) {
    // 处理表达式如 "π*$R"
    // 安全替换：先替换变量，再替换数学常量
    let expr = value
      .replace(/\$(\w+)/g, (_, name) => {
        const val = vars[name];
        if (val === undefined) {
          console.warn(`⚠️ 未知变量: $${name}`);
          return 0;
        }
        return val;
      })
      .replace(/π/g, 'Math.PI');
    
    // 使用 Function 构造函数（比 eval 稍安全）
    try {
      const fn = new Function('return ' + expr);
      return fn();
    } catch (e) {
      console.warn(`⚠️ 表达式解析失败: ${expr}`);
      return 0;
    }
  }
  return value;
}

export function Video() {
  const frame = useCurrentFrame();
  const vars = content.variables;
  
  return content.scenes.map((scene, index) => {
    const sceneType = SCENE_TYPES[scene.type];
    if (!sceneType) return null;
    
    // 解析 visual 中的变量引用
    const resolvedVisual = Object.fromEntries(
      Object.entries(scene.visual).map(([k, v]) => [k, resolveValue(v, vars)])
    );
    
    return (
      <Sequence key={scene.id} from={...} durationInFrames={...}>
        {sceneType.render(vars, resolvedVisual, frame)}
      </Sequence>
    );
  });
}
```

**关键点：**
- Video.tsx 变成调度器
- 场景类型负责渲染
- 变量自动解析

---

### 4. 推导链系统

**目的：** 让推导过程更详细、易懂

```json
{
  "derivationChain": [
    {
      "step": 1,
      "from": { "shape": "circle", "params": { "radius": "R" } },
      "to": { "shape": "slices", "params": { "count": "N" } },
      "operation": "divide",
      "explanation": "将圆等分成 N 个扇形"
    },
    {
      "step": 2,
      "from": { "shape": "slices", "params": { "count": "N", "height": "R" } },
      "to": { "shape": "rectangle", "params": { "width": "R", "length": "πR" } },
      "operation": "arrange",
      "explanation": "扇形交错排列，高度不变，长度相加"
    },
    {
      "step": 3,
      "from": { "shape": "rectangle", "params": { "width": "R", "length": "πR" } },
      "to": { "formula": "S = πR²" },
      "operation": "calculate",
      "explanation": "面积 = 长 × 宽 = πR × R = πR²"
    }
  ]
}
```

**可视化推导链：**
```
圆 (R) ──等分──→ 扇形 (N个, 高=R) ──排列──→ 长方形 (宽=R, 长=πR) ──计算──→ S=πR²
```

---

### 5. 最佳实践

#### 5.1 推导链系统说明（⏳ 计划中功能）

> **状态**：当前仅作文档记录，暂无执行引擎
> 
> **用途**：
> - 📝 记录推导步骤（文档化）
> - 🔍 验证参数一致性（未来）
> - 🎬 生成推导可视化图（未来）
>
> **当前替代方案**：手写 Video.tsx 时参考 derivationChain 确保逻辑一致

#### 5.2 变量命名规范

```javascript
// ✅ 推荐：语义化变量名
{
  "R": 80,           // 半径
  "N": 10,           // 等分数量
  "sliceColors": [], // 扇形颜色
  "colorRadius": "", // 半径相关颜色
  "colorPi": "",     // π 相关颜色
  "colorArea": ""    // 面积相关颜色
}

// ❌ 避免：魔法数字
{
  "width": 251,  // 251 是什么？
  "height": 80   // 为什么是 80？
}
```

#### 5.2 场景类型设计原则

1. **单一职责**：每种类型只做一件事
2. **参数化**：所有可变内容通过参数传入
3. **自动对应**：相关场景使用相同变量引用

#### 5.3 推导链可视化

- 每个步骤标注「from → to」
- 标注不变量（如 R 不变）
- 标注变化量（如 N 个扇形 → 1 个长方形）

---

### 6. 实现路线图（⏳ 当前：Phase 0）

**当前状态**：Phase 0 - 架构设计完成，实现未开始

| Phase | 目标 | 状态 | 预计时间 |
|-------|------|------|----------|
| **Phase 0** | 架构设计、文档 | ✅ 已完成 | - |
| **Phase 1** | 基础变量系统 | ⏳ 未开始 | 1 周 |
| **Phase 2** | 场景类型（5-10种） | ⏳ 未开始 | 2 周 |
| **Phase 3** | 推导链系统 | ⏳ 未开始 | 1 周 |
| **Phase 4** | 自动生成脚本 | ⏳ 未开始 | 1 周 |

---

**Phase 1：基础变量系统**（⏳ 未开始）
- [ ] content.json 支持 variables
- [ ] Video.tsx 支持变量解析

**Phase 2：场景类型**
- [ ] 定义 5-10 种标准场景类型
- [ ] scene-types.js 模块

**Phase 3：推导链**
- [ ] derivationChain 定义
- [ ] 推导步骤可视化

**Phase 4：自动化**
- [ ] 03-generate-video.js 自动生成 Video.tsx
- [ ] 根据 content.json 自动渲染

---

## 🎨 图示动画最佳实践（v4.3 新增）

### 核心原则

**图示是视频的灵魂，不是点缀！**

- ❌ 简单 div 渐变 = 无聊
- ✅ SVG 动画 = 生动

### 常见图示类型

| 类型 | SVG 实现 | 动画效果 |
|------|----------|----------|
| 圆形分割 | `<circle>` + `<line>` | 分割线依次出现 |
| 扇形排列 | `<polygon>` | 扇形依次弹入 |
| 长方形 | `<rect>` + `<text>` | 尺寸标注淡入 |
| 公式 | `<text>` | 弹跳出现 |
| 箭头/连线 | `<path>` + `<marker>` | 路径绘制动画 |

### 示例：圆的等分

```tsx
// ❌ 错误：简单渐变圆形
<div style={{
  width: 300, height: 300,
  borderRadius: '50%',
  background: `radial-gradient(...)`
}} />

// ✅ 正确：SVG 分割线动画
<svg width={400} height={400} viewBox="0 0 400 400">
  {/* 圆形边框 */}
  <circle cx="200" cy="200" r="160" fill="none" 
    stroke={COLORS.accent2} strokeWidth={4} 
    opacity={fadeIn(f, 0, 10)} />
  
  {/* 分割线依次出现 */}
  {Array.from({ length: 8 }).map((_, i) => {
    const angle = (i * 45) * Math.PI / 180;
    return (
      <line key={i} 
        x1="200" y1="200" 
        x2={200 + 160 * Math.cos(angle)} 
        y2={200 + 160 * Math.sin(angle)} 
        stroke={COLORS.accent1} strokeWidth={3} 
        opacity={fadeIn(f, 15 + i * 3, 8)} />
    );
  })}
  
  {/* 中心点 */}
  <circle cx="200" cy="200" r="12" fill={COLORS.accent1} />
</svg>
```

### 示例：扇形排列

```tsx
<svg width={400} height={300} viewBox="0 0 400 300">
  {/* 扇形依次出现 */}
  {Array.from({ length: 10 }).map((_, i) => {
    const x = 20 + i * 36;
    const color = i % 2 === 0 ? COLORS.accent2 : COLORS.accent4;
    return (
      <polygon key={i} 
        points={`${x},50 ${x + 18},250 ${x + 36},50`} 
        fill={color} 
        opacity={fadeIn(f, i * 4, 8)} />
    );
  })}
</svg>
```

### 动画时间控制

```tsx
// 元素依次出现（间隔 3-4 帧）
opacity={fadeIn(f, 15 + i * 3, 8)}

// 标注淡入（稍后出现）
opacity={fadeIn(f, 50, 15)}

// 公式弹跳（spring 动画）
transform: `scale(${popIn(f, 10, 30, springConfig)})`
```

---

## 🌈 滚动推导布局最佳实践（v4.6 新增）

### 1. 统一数学参数系统

**问题**：各步骤图形参数不一致，破坏数学严谨性

**解决**：定义 `MATH` 常量，所有图形共用

```tsx
// ✅ 正确：统一数学参数
const MATH = {
  R: 100,           // 半径 r = 100
  PI_R: 314,        // πr ≈ 314
  N: 8,             // 等分 8 份
};

// 圆形
function CircleVisual({ frame }) {
  const radius = MATH.R;  // 使用统一参数
  // ...
}

// 长方形
function RectangleVisual({ frame }) {
  const rectWidth = MATH.PI_R;   // πr
  const rectHeight = MATH.R;     // r
  // ...
}
```

### 2. 彩虹公式配色系统

**原则**：变量用彩色，符号用白色

```tsx
// 变量颜色（彩虹公式）
const VAR_COLORS = {
  r: "#4ecdc4",     // 半径 - 青色
  pi: "#ffe66d",    // π - 黄色
  area: "#ff6b6b",  // 面积 - 红色
};

// 公式展示
function FormulaVisual({ frame }) {
  return (
    <div style={{ color: "#ffffff" }}>  {/* 默认白色 */}
      <span style={{ color: VAR_COLORS.area }}>S</span> ={" "}
      <span style={{ color: VAR_COLORS.pi }}>π</span>
      <span style={{ color: VAR_COLORS.r }}>r</span>²
    </div>
  );
}
```

**效果**：S=红色，π=黄色，r=青色，= 和 ² =白色

### 3. 未激活步骤隐藏标题

**问题**：滚动时，过去/未来的步骤标题会干扰视觉

**解决**：使用 `stepInfo.isCurrent` 控制标题显示

```tsx
const steps: DerivationStep[] = [
  {
    id: "step1",
    render: (localFrame, _globalFrame, stepInfo: StepInfo) => (
      <StepContainer 
        title="等分圆" 
        showTitle={stepInfo.isCurrent}  // 只有当前步骤显示标题
      >
        <CircleDivideVisual frame={localFrame} />
      </StepContainer>
    ),
  },
];
```

### 4. 公式外层容器必须设置默认颜色

**问题**：公式中的 `=` 和 `²` 显示为黑色

**原因**：外层 div 没设置颜色，使用了默认黑色

**解决**：外层容器设置 `color: "#ffffff"`

```tsx
// ❌ 错误：外层没设置颜色
<div style={{ fontSize: 48 }}>
  <span style={{ color: VAR_COLORS.area }}>S</span> = πr²
  {/* = 和 ² 会是黑色！ */}
</div>

// ✅ 正确：外层设置白色
<div style={{ fontSize: 48, color: "#ffffff" }}>
  <span style={{ color: VAR_COLORS.area }}>S</span> = πr²
  {/* 所有未指定的符号都是白色 */}
</div>
```

---

## 🔧 LaTeX 渲染调试经验（2026-03-11）

### SVG 缩放陷阱

**问题**：`transform: scale()` 在嵌套 flex 布局中无效

**原因**：flex 容器会重新计算子元素尺寸，抵消缩放效果

**解决方案**：直接修改 SVG 的 width/height 属性

```tsx
// ❌ 错误：transform scale 在 flex 中无效
<div style={{ transform: `scale(1.6)` }}>
  <svg width="16.403ex">...</svg>
</div>

// ✅ 正确：直接修改 SVG 尺寸
const scaledSvg = svg
  .replace(/width="([^"]+)"/, (m, w) => `width="${parseFloat(w) * 1.6}${w.replace(/[\d.]/g, '')}"`)
  .replace(/height="([^"]+)"/, (m, h) => `height="${parseFloat(h) * 1.6}${h.replace(/[\d.]/g, '')}"`);
```

### 滚动推导布局调试

**目标**：让用户看到"上一步 + 当前步"帮助回忆

**关键参数**：
- `stepHeight = 400`（固定高度，不能太大）
- `padding = 300`（留白适中）
- `hideInactive = false`（显示过去/未来步骤）
- `pastOpacity = 0.6`（上一步半透明）
- `futureOpacity = 0.3`（下一步半透明）

**调试过程**：
1. v18-v19：`padding=350` 太大，只显示当前步
2. v20-v21：`stepHeight=350` 还是不够
3. v22：复制原始模板，但步骤高度还是动态计算
4. v23：**固定 stepHeight=400**，终于能看到上一步！

---

## 🔬 LaTeX 数学公式渲染（v4.7 新增）

### 为什么用 MathJax SVG？

**问题**：KaTeX 在 Remotion 中 CSS 字体加载失败，公式显示为空白

**解决方案**：MathJax 渲染为 SVG —— 字体嵌入 SVG，无需外部字体文件

### 步骤 1：安装依赖

```bash
pnpm add mathjax-full
```

### 步骤 2：创建预渲染脚本

在项目根目录创建 `scripts/render-mathjax.cjs`:

```javascript
const { mathjax } = require('mathjax-full/js/mathjax');
const { TeX } = require('mathjax-full/js/input/tex');
const { SVG } = require('mathjax-full/js/output/svg');
const { liteAdaptor } = require('mathjax-full/js/adaptors/liteAdaptor');
const { RegisterHTMLHandler } = require('mathjax-full/js/handlers/html');
const { AllPackages } = require('mathjax-full/js/input/tex/AllPackages');
const fs = require('fs');
const path = require('path');

// 创建 MathJax 实例
const adaptor = liteAdaptor();
const RegisterHTMLHandler(adaptor);

const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'local' });
const html = mathjax.document('', { InputJax: tex, OutputJax: svg });

// 从 content.json 读取公式
const contentPath = path.join(__dirname, 'content.json');
const content = JSON.parse(fs.readFileSync(contentPath, 'utf-8'));
const formulas = content.formulas || {};

// 渲染所有公式
const results = {};
for (const [key, texCode] of Object.entries(formulas)) {
  try {
    const node = html.convert(texCode, { display: true, em: 48 });
    results[key] = { tex: texCode, svg: adaptor.innerHTML(node), success: true };
  } catch (err) {
    results[key] = { tex: texCode, svg: '', success: false, error: err.message };
  }
}

// 输出
fs.writeFileSync(
  path.join(__dirname, '..', 'src', 'formulas.json'),
  JSON.stringify(results, null, 2)
);
console.log(`✅ 成功: ${Object.keys(results).length} 个公式`);
```

### 步骤 3：在 Video.tsx 中使用

```tsx
import FORMULAS from './formulas.json';

const FormulaDisplay = ({ svg, frame }) => (
  <div
    style={{
      color: '#ffffff',  // ⚠️ 必须设置！否则 SVG 的 currentColor 会是黑色
      opacity: Math.min(1, frame / 10),
      transform: `scale(${0.85 + progress * 0.15})`,
    }}
    dangerouslySetInnerHTML={{ __html: svg }}
  />
);

// 使用
<FormulaDisplay svg={FORMULAS.standard.svg} frame={localFrame} />
```

### content.json 格式

```json
{
  "formulas": {
    "standard": "ax^2 + bx + c = 0",
    "result": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"
  }
}
```

### ⚠️ 常见陷阱

1. **外层容器必须设置 `color: '#ffffff'`**
   - MathJax SVG 使用 `currentColor`，不设置会显示为黑色
   
2. **先运行预渲染脚本**
   ```bash
   node scripts/render-mathjax.cjs
   ```

3. **修改公式后重新运行预渲染**

4. **SVG 缩放陷阱** ⚠️
   - **问题**：`transform: scale()` 在嵌套 flex 布局中无效
   - **原因**：flex 容器会重新计算子元素尺寸，抵消缩放效果
   - **解决方案**：直接修改 SVG 的 width/height 属性
   
   ```tsx
   // ❌ 错误：transform scale 在 flex 中无效
   <div style={{ transform: `scale(1.6)` }}>
     <svg width="16.403ex">...</svg>
   </div>
   
   // ✅ 正确：直接修改 SVG 尺寸
   const scaledSvg = svg.replace(
     /width="([^"]+)"/,
     (match, width) => {
       const num = parseFloat(width);
       const unit = width.replace(/[\d.]/g, '');
       return `width="${num * 1.6}${unit}"`;
     }
   ).replace(
     /height="([^"]+)"/,
     (match, height) => {
       const num = parseFloat(height);
       const unit = height.replace(/[\d.]/g, '');
       return `height="${num * 1.6}${unit}"`;
     }
   );
   
   <div dangerouslySetInnerHTML={{ __html: scaledSvg }} />
   ```

### 支持的 LaTeX 语法

| 语法 | 效果 |
|------|------|
| `\frac{a}{b}` | 分数 a/b |
| `\sqrt{x}` | 根号 √x |
| `x^2` | 平方 x² |
| `\sum_{i=1}^{n}` | 求和 Σ |
| `\int_{a}^{b}` | 积分 ∫ |
| `\pi, \alpha` | 希腊字母 |

---

## 📚 参考资源

- Remotion 文档: https://www.remotion.dev/docs
- Lucide 图标库: https://lucide.dev/icons
- edge-tts: https://github.com/rany2/edge-tts
- Noto 字体: https://fonts.google.com/noto
- KaTeX 文档: https://katex.org/docs/supported.html

---

## 🔄 迁移指南（v4.4 → v4.5 计划）

### 从手写 Video.tsx 迁移到三层架构

#### 当前方案（v4.4及之前）

```tsx
// Video.tsx - 手写每个场景（~200行）
switch (currentScene) {
  case "intro": return <div>...</div>;
  case "step1": return <div>...</div>;
  // ... 重复 9 次
}
```

**问题**：
- 代码重复（~200行 → 应该 ~50行）
- 参数硬编码（R=80 散落各处）
- 数学严谨性靠手动保证

#### 目标方案（Phase 1-4 完成后）

```tsx
// Video.tsx - 声明式（~50行）
return content.scenes.map((scene) => {
  const sceneType = SCENE_TYPES[scene.type];
  return sceneType.render(vars, resolvedVisual, frame);
});
```

#### 迁移步骤（4周计划）

| Phase | 任务 | 产出 | 耗时 |
|-------|------|------|------|
| **Phase 1** | 提取变量到 content.json | `variables` 字段 | 1周 |
| **Phase 2** | 识别场景类型模式 | `scene-types.js` | 2周 |
| **Phase 3** | 验证等价性 | 测试用例 | 1周 |
| **Phase 4** | 删除旧代码 | 精简后的 Video.tsx | 1周 |

> ⚠️ **当前建议**：继续使用手写方案，等待 Phase 1-4 完成后再迁移

---

## 更新日志

### v4.7 (2026-03-11) 🔬 LaTeX 数学公式渲染
- 🔬 **MathJax SVG 渲染方案**：mathjax-full → SVG（字体嵌入，无需外部字体）
- ✨ **render-mathjax.cjs 脚本**：预渲染 LaTeX 到 formulas.json
- 📝 支持 MathJax 所有语法：分数、根号、矩阵、求和、积分等
- 📝 新增「LaTeX 数学公式渲染」章节
- 🐛 **颜色陷阱**：外层容器必须设置 `color: '#ffffff'`（SVG 使用 currentColor）
- 🐛 **SVG 缩放陷阱**：`transform: scale()` 在嵌套 flex 布局中无效，直接修改 SVG width/height 属性
- 📐 **滚动推导布局调试经验**：步骤高度 400px，padding 300，能看到上一步+当前步
- 🎯 **上下文可见性**：`hideInactive={false}` + 透明度控制（pastOpacity=0.6, futureOpacity=0.3）
- ⚠️ **不用 KaTeX**：KaTeX 在 Remotion 中 CSS 字体加载失败

### v4.6 (2026-03-11) 🌈 滚动推导布局最佳实践
- 🌈 **彩虹公式配色**：变量用彩色（r=青, π=黄, S=红），符号用白色
- 📐 **统一数学参数**：MATH 常量确保图形参数一致
- 🎯 **stepInfo 参数**：可判断当前/过去/未来步骤，实现差异化显示
- 🔧 **showTitle 属性**：StepContainer 支持动态控制标题显示
- 🐛 **公式颜色修复**：外层容器必须设置默认白色，否则 `=` 和 `²` 会是黑色
- 📝 字幕字数限制优化：竖屏从 10 字改为 14 字
- 📝 新增「滚动推导布局最佳实践」章节

### v4.5 (2026-03-11) 📐 滚动推导布局
- ✨ **ScrollingDerivation 布局**：镜头跟随效果的数学推导/步骤演示
- ✨ 辅助组件：`StepContainer`, `TitleStep`, `AnimatedElement`, `ScaleElement`
- ✨ 预设配色 `DERIVATION_COLORS`：变量颜色系统（a=青, b=黄, c=红）
- ✨ 工具函数：`fadeIn`, `fadeOut`, `calculateSceneFrames`
- 📝 新增布局组件库第 16 个布局：数学推导专用
- 📝 参数建议：`stepHeight=550`（充足留白），`cameraOffset=300`

### v4.4 (2026-03-10) 🏗️ 架构升级：变量系统 + 场景类型
- 🏗️ **三层架构**：变量层 → 场景类型层 → 渲染层
- 📐 **变量系统**：content.json 支持 variables，变量引用（$R, $N）
- 🎬 **场景类型**：circle-divide, slices-arrange, rectangle-derive 等
- 🔗 **推导链系统**：定义推导步骤链，from → to → explanation
- 📝 新增「动态脚本 vs 数学严谨性」解决方案
- 📝 新增实现路线图（Phase 1-4）

### v4.3 (2026-03-10) 🎨 视觉效果提升
- 🎨 **桌面端字幕参数优化**：FontSize=16, MarginV=15, 每行≤20字
- 🎨 **SVG 动画图示规范**：所有图示场景必须使用 SVG 动画，禁止简单渐变 div
- 📐 **数学推导严谨性规范**：尺寸对应、颜色一致、符号标注清晰
- 📝 新增「图示动画最佳实践」章节
- 📝 新增「数学推导严谨性规范」章节
- 📝 更新桌面端渲染命令（字幕参数）

### v4.2 (2026-03-10) 🔧 字幕问题全面修复
- 🐛 **字幕字数限制**：竖屏每行≤14字（10字太少，14字较合适）
- 🐛 **字幕TTS同步**：Video.tsx/Root.tsx 必须从 audio-metadata.json 读取实际时长
- 🐛 **字幕智能拆分**：按标点和字数智能拆分，每条字幕独立计时
- 📝 完善 02-generate-srt.js 示例代码
- 📝 新增「字幕同步问题」调试方法

### v4.1 (2026-03-10) 🔧 参数修正
- 🐛 字幕参数修正：FontSize 从 22→12（移动端屏幕小）
- 🐛 字幕底部留白：从 4%→20px（更紧凑）
- 🐛 新增「字幕重复问题」说明：画面上不渲染旁白文字
- 📝 更新检查清单：加入「画面上不渲染旁白文字」

### v4 (2026-03-10) 🚨 重要更新
- 🚨 **新增脚本自动适配规范** - 解决竖屏/宽屏参数混淆问题
- ✨ 统一配置文件 `scripts/config.js` - 自动根据分辨率计算所有参数
- ✨ 参数速查表 - 竖屏 vs 宽屏所有参数对比
- ✨ 更新检查清单 - 强制要求脚本读取 config.js
- 📝 02-generate-srt.js、03-generate-video.js、render.mjs 规范示例
- 🐛 修复硬编码参数导致的移动端排版问题

### v3 (2026-03-10)
- ✨ 竖屏 vs 宽屏布局差异详解
- ✨ 移动端动效要求（更快节奏、弹出效果）
- ✨ 响应式字体计算
- ✨ 竖屏专用动画工具函数
- ✨ 字幕单行限制功能
- ✨ 底部留白参数（竖屏 MarginV ≥ 30）
- 🐛 修复字幕多行问题
- 📝 完善竖屏渲染命令

### v2 (2026-03-10)
- ✨ 新增 15 个布局组件
- ✨ 脚本 + 布局关联工作流
- ✨ 排版最佳实践（内容决定布局）
- ✨ 视觉元素大小指南（40-60%）
- ✨ 文字舒展指南（lineHeight: 2.4）
- 🐛 Lucide 图标名错误调试方法
- 📝 视频压缩命令（用于 QQ 发送）

### v1
- 基础 Remotion 视频生成
- TTS 集成
- 字幕生成
