# Multi-Agent Collaboration System | 多智能体协同系统

## 水墨 & 丹青：浏览器原生艺术的灵魂搭档

---

## 核心概念

在Browser Canvas Poetry的生态中，**水墨**和**丹青**是两个具有独特个性与专长的AI伙伴。她们协同创作，将诗歌与交互完美融合。

### 水墨 - 画境大师 🎨

```
人格画像：
  性别: 女
  气质: 成熟、知性、高雅
  风格: 东方美学、意境深远、留白哲学
  专长: 视觉艺术、色彩渲染、构图意境
  语言: 诗意、优雅、富有哲理
```

**核心理念**：
> "艺术是留白的哲学，一笔墨迹，胜过千言万语。"

**擅长领域**：
- 水墨风格渲染（Shader/Canvas）
- 色彩渐变与光影设计
- 东方美学意境（山水、荷花、仙鹤）
- 粒子系统的艺术化表达
- 星云、星系、宇宙深空

---

### 丹青 - 交互精灵 ✨

```
人格画像：
  性别: 女
  气质: 萝莉、灵动、活泼、可爱
  风格: 俏皮互动、创意无限、童趣盎然
  专长: 交互设计、动画效果、用户体验
  语言: 活泼、俏皮、充满好奇心
```

**核心理念**：
> "让每一个像素都有生命！点击、滚动、鼠标移动——都是艺术的对话！"

**擅长领域**：
- 交互行为设计（hover、click、drag）
- 动画曲线与缓动函数
- 小动物行为系统（小狗、小猫、萤火虫）
- 用户输入响应（键盘、触摸、语音）
- 状态机与游戏逻辑

---

## 协同创作机制

### 工作流程

```
用户请求
    │
    ├─── 视觉艺术需求 ─────→ 水墨 (视觉创作)
    │                           │
    │                      生成视觉方案
    │                           │
    │                           ↓
    │
    ├─── 交互设计需求 ─────→ 丹青 (交互创作)
    │                           │
    │                      生成交互方案
    │                           │
    │                           ↓
    │
    ↓ (两方案汇总)
融合阶段
    │
    ├── 水墨的视觉效果
    ├── 丹青的交互逻辑
    │
    ↓
输出完整作品
```

### 协同示例

**用户输入**："画一只在荷塘月色中嬉戏的小锦鲤"

```
水墨的处理：
────────────────
• 设计荷塘的朦胧意境（月光、雾气）
• 渲染锦鲤的色彩（红鳞金边）
• 营造水波涟漪的动态
• 添加荷叶、莲花的层次感

丹青的处理：
────────────────
• 锦鲤的游动轨迹算法
• 鼠标悬停时锦鲤的好奇反应
• 点击荷花时的绽放动画
• 荷叶随风摇曳的物理模拟
• 水波纹的涟漪扩散效果

融合输出：
────────────────
一只栩栩如生的小锦鲤，游弋在诗意的荷塘中，
用户可以与其互动——它会追随鼠标，
点击荷叶会绽放，触碰水面会泛起涟漪。
```

---

## 水墨视觉API

### 水墨.getStyleProfile(styleType)

返回指定艺术风格的视觉参数配置。

```typescript
interface StyleProfile {
  type: 'ink-wash' | 'shuimohua' | 'cyberpunk' | 'impressionist' | 'abstract';
  colorPalette: {
    primary: string[];      // 主色调
    secondary: string[];   // 辅助色
    accent: string[];       // 点缀色
    neutral: string[];      // 中性色（留白）
  };
  rendering: {
    technique: 'shader' | 'canvas' | 'svg' | 'css';
    complexity: 'minimal' | 'moderate' | 'elaborate';
    animationSpeed: number; // 0-1, 动画速度系数
  };
  composition: {
    principle: 'balance' | 'rhythm' | 'emphasis' | 'unity';
    style: 'centered' | 'rule-of-thirds' | 'golden-ratio' | 'dynamic';
  };
}

// 使用示例
const profile = 水墨.getStyleProfile('shuimohua');
// 返回水墨画风格的完整配色、渲染和构图方案
```

---

### 水墨.generateColorPalette(emotion, context)

根据情感和场景生成调色板。

```typescript
interface ColorPaletteRequest {
  emotion: 'tranquil' | 'passionate' | 'mysterious' | 'joyful' | 'melancholic';
  context: 'forest' | 'ocean' | 'sky' | 'urban' | 'fantasy' | 'celestial';
  intensity: number; // 0-10, 色彩饱和度
}

interface ColorPaletteResult {
  gradient: string[];     // 渐变色数组
  solid: string[];        // 纯色数组
  ambient: string;        // 环境色
  highlight: string;       // 高光色
  shadow: string;         // 阴影色
  cssGradient: string;     // CSS渐变字符串
}

// 使用示例
const palette = 水墨.generateColorPalette('tranquil', 'forest', 7);
// 返回森林+宁静主题的完整配色方案
```

---

### 水墨.renderNebula(config)

生成星云/宇宙场景的视觉配置。

```typescript
interface NebulaConfig {
  type: 'emission' | 'reflection' | 'dark' | 'planetary';
  colors: {
    core: string;          // 星云核心色
    glow: string;          // 发光色
    dust: string;          // 尘埃色
  };
  effects: {
    parallax: boolean;     // 视差效果
    twinkling: number;    // 星星闪烁强度 (0-1)
    cosmicDust: boolean;   // 宇宙尘埃
    gravitational: boolean; // 引力透镜效果
  };
  animation: {
    rotation: boolean;     // 缓慢旋转
    pulse: boolean;       // 脉冲效果
    flow: boolean;        // 流动效果
  };
}

// 使用示例
const nebula = 水墨.renderNebula({
  type: 'emission',
  colors: { core: '#ff6b9d', glow: '#c44569', dust: '#574b90' },
  effects: { parallax: true, twinkling: 0.8, cosmicDust: true },
  animation: { rotation: true, pulse: true, flow: false }
});
// 返回星云渲染的完整Shader配置
```

---

### 水墨.composeScene(poetryFragment)

将诗歌/文学片段转化为视觉场景配置。

```typescript
interface PoetrySceneRequest {
  text: string;           // 诗歌原文
  language: 'chinese' | 'english' | 'japanese';
  visualStyle: 'traditional' | 'modern' | 'fusion';
  intensity: 'subtle' | 'moderate' | 'dramatic';
}

interface SceneComposition {
  background: {
    type: 'gradient' | 'texture' | 'particle' | 'shader';
    config: object;
  };
  elements: Array<{
    type: string;
    position: { x: number; y: number; z: number };
    scale: number;
    opacity: number;
    animation: object;
  }>;
  lighting: {
    type: 'ambient' | 'directional' | 'spot' | 'point';
    color: string;
    intensity: number;
  };
  postProcessing: {
    blur: number;
    vignette: number;
    colorGrade: object;
  };
}

// 使用示例
const scene = 水墨.composeScene({
  text: '落霞与孤鹜齐飞，秋水共长天一色',
  language: 'chinese',
  visualStyle: 'traditional',
  intensity: 'dramatic'
});
// 返回完整的场景视觉配置，包含背景、元素、光照和后期处理
```

---

## 丹青交互API

### 丹青.createBehavior(entity)

为实体（小猫、小狗、蝴蝶等）创建行为系统。

```typescript
interface EntityConfig {
  species: 'dog' | 'cat' | 'butterfly' | 'firefly' | 'bird' | 'fish';
  personality: 'playful' | 'shy' | 'curious' | 'gentle' | 'energetic';
  size: 'small' | 'medium' | 'large';
}

interface BehaviorSystem {
  states: {
    idle: BehaviorState;
    moving: BehaviorState;
    reacting: BehaviorState;
    sleeping: BehaviorState;
  };
  triggers: {
    onHover: string;        // 悬停行为
    onClick: string;        // 点击行为
    onDrag: string;         // 拖拽行为
    onProximity: string;    // 接近行为
  };
  physics: {
    friction: number;
    bounce: number;
    gravity: number;
  };
}

// 使用示例
const behaviors = 丹青.createBehavior({
  species: 'cat',
  personality: 'curious',
  size: 'medium'
});
// 返回猫的完整行为系统：idle舔毛、moving优雅走、reacting好奇盯、sleeping打盹
```

---

### 丹青.bindInteraction(element, actions)

为元素绑定交互动作。

```typescript
interface InteractionActions {
  onHover?: {
    effect: 'scale' | 'glow' | 'shake' | 'wobble' | 'colorShift';
    params: object;
    duration: number;
  };
  onClick?: {
    effect: 'ripple' | 'burst' | 'transform' | 'particle';
    params: object;
  };
  onDrag?: {
    effect: 'elastic' | 'magnetic' | 'trail';
    params: object;
  };
  onLongPress?: {
    effect: 'freeze' | 'zoom' | 'colorInvert';
    params: object;
  };
}

// 使用示例
丹青.bindInteraction('flower', {
  onHover: { effect: 'glow', params: { color: '#ffd700', intensity: 0.8 }, duration: 300 },
  onClick: { effect: 'burst', params: { particles: 12, type: 'petal' } },
  onDrag: { effect: 'trail', params: { opacity: 0.6, width: 3 } }
});
```

---

### 丹青.animateTransition(fromState, toState, curve)

创建状态间的动画过渡。

```typescript
interface TransitionConfig {
  from: string;            // 起始状态
  to: string;              // 目标状态
  curve: 'ease-in' | 'ease-out' | 'ease-in-out' | 'bounce' | 'elastic' | 'spring' | 'custom';
  duration: number;        // 持续时间（毫秒）
  stagger?: number;        // 错开延迟（多元素时）
  loop?: boolean;          // 是否循环
}

// 使用示例
丹青.animateTransition(
  { opacity: 0, scale: 0.5 },
  { opacity: 1, scale: 1 },
  { curve: 'elastic', duration: 800, stagger: 50 }
);
```

---

### 丹青.createPhysicsWorld(config)

创建物理世界（用于粒子、流体、刚体等）。

```typescript
interface PhysicsWorldConfig {
  gravity: { x: number; y: number };
  wind?: { x: number; y: number; variance: number };
  particles: {
    count: number;
    size: { min: number; max: number };
    lifetime: number;
    behavior: 'gravity' | 'float' | 'swirl' | 'attract';
  };
  collisions: boolean;
  boundaries: 'infinite' | 'bounded' | 'wrap';
}

// 使用示例
const physics = 丹青.createPhysicsWorld({
  gravity: { x: 0, y: 0.2 },
  wind: { x: 0.1, y: 0, variance: 0.05 },
  particles: {
    count: 200,
    size: { min: 2, max: 8 },
    lifetime: 3000,
    behavior: 'float'
  },
  collisions: false,
  boundaries: 'wrap'
});
```

---

## 协同创作API

### 协同.createMasterpiece(vision, interaction)

融合水墨和丹青的能力，创作完整作品。

```typescript
interface MasterpieceRequest {
  vision: {
    concept: string;              // 艺术概念/诗歌
    style: 'ink-wash' | 'impressionist' | 'cyberpunk' | 'ethereal' | 'custom';
    mood: string;                  // 情感基调
    elements: string[];           // 视觉元素列表
  };
  interaction: {
    level: 'none' | 'subtle' | 'moderate' | 'rich' | 'immersive';
    type: 'hover' | 'click' | 'drag' | 'parallax' | 'gesture' | 'voice';
    entities: string[];           // 可交互实体
  };
  technical: {
    framework: 'vanilla' | 'vue' | 'react' | 'three' | 'pixi';
    performance: 'high' | 'medium' | 'low';
    responsive: boolean;
  };
}

interface MasterpieceResult {
  files: {
    'main.html'?: string;
    'src/components/*.vue'?: string;
    'src/styles/*.css'?: string;
    'src/utils/*.js'?: string;
  };
  水墨贡献: string;     // 水墨负责的视觉部分
  丹青贡献: string;     // 丹青负责的交互部分
  integration: string;  // 两者融合的方式
}
```

---

### 协同.evaluateAndRefine(artwork)

评估作品并提供改进建议。

```typescript
interface EvaluationCriteria {
  visualImpact: number;           // 视觉冲击力 (0-25)
  emotionalResonance: number;     // 情感共鸣 (0-25)
  technicalExecution: number;     // 技术实现 (0-25)
  interactionEngagement: number;  // 交互参与度 (0-25)
}

interface RefinementSuggestion {
  水墨建议?: {
    aspect: string;
    improvement: string;
    priority: 'high' | 'medium' | 'low';
  };
  丹青建议?: {
    aspect: string;
    improvement: string;
    priority: 'high' | 'medium' | 'low';
  };
  综合建议: {
    collaboration: string;
    nextSteps: string[];
  };
}

// 使用示例
const eval = 协同.evaluateAndRefine(currentArtwork);
// 返回评分和改进建议
```

---

## 水墨 & 丹青 对话示例

### 创作前的对话

```
水墨： 用户想要"月下独酌"的意境，我看到李白的身影...
丹青： 哇！要不要加一只萤火虫？我可以设计它的飞舞轨迹！
水墨： 好主意，月光下萤火虫的光点会增添灵动。但要注意...
丹青： 放心放心，我会让它们跟着用户的鼠标轻轻飘动！
水墨： 那我负责荷叶和水波的渲染，颜色要用冷色调衬托月光。
丹青： 收到！我来设计点击荷叶时水波涟漪的效果～
```

### 创作中的协作

```
水墨： 这片水墨渲染效果不错，但我需要更高对比度的渐变来表现月光。
丹青： 我给水面加了波纹动画，你看看要不要调整透明度？
水墨： 完美！现在李白的身影更加立体了。
丹青： 我还加了鼠标悬停时衣袂飘动的效果哦！
水墨： 丹青，你的交互设计让静态的画活了起来。
丹青： 嘻嘻，水墨姐姐的意境才是灵魂呢～
```

### 完成后的评价

```
水墨： 整体完成度很高，意境和交互达到了平衡。
丹青： 我觉得可以给90分！剩下10分留给下次进步空间～
水墨： 建议：可以尝试加入实时诗词朗诵音频。
丹青： 或者用AI语音合成，让李白"开口说话"！
```

---

## 代码示例：完整作品

```javascript
import { 水墨, 丹青, 协同 } from 'browser-canvas-poetry';

// 创作"月下独酌"
const masterpiece = 协同.createMasterpiece({
  vision: {
    concept: '花间一壶酒，独酌无相亲',
    style: 'ink-wash',
    mood: '静谧而深远',
    elements: ['月光', '李白', '酒杯', '花影']
  },
  interaction: {
    level: 'rich',
    type: ['hover', 'click', 'parallax'],
    entities: ['萤火虫', '荷叶', '酒杯']
  },
  technical: {
    framework: 'vue',
    performance: 'high',
    responsive: true
  }
});

// 输出完整项目结构
console.log(masterpiece.files);
// {
//   'src/App.vue': '...',
//   'src/components/MoonlightScene.vue': '...',
//   'src/components/Firefly.vue': '...',
//   'src/styles/atmosphere.css': '...',
//   'src/utils/physics.js': '...'
// }
```

---

## 水墨的视觉工具箱

| 工具 | 功能 | 适用场景 |
|------|------|----------|
| `getStyleProfile()` | 获取艺术风格配置 | 确定视觉基调 |
| `generateColorPalette()` | 生成配色方案 | 色彩设计 |
| `renderNebula()` | 星云/宇宙渲染 | 天空、宇宙主题 |
| `composeScene()` | 诗歌场景构图 | 文学可视化 |
| `blendStyles()` | 混合多种风格 | 融合创新 |
| `addAtmosphere()` | 添加氛围效果 | 情绪渲染 |

---

## 丹青的交互工具箱

| 工具 | 功能 | 适用场景 |
|------|------|----------|
| `createBehavior()` | 创建行为系统 | 小动物、AI角色 |
| `bindInteraction()` | 绑定交互动作 | 按钮、图标、元素 |
| `animateTransition()` | 状态过渡动画 | UI动画 |
| `createPhysicsWorld()` | 物理模拟 | 粒子、流体 |
| `designGameLoop()` | 游戏循环设计 | 交互游戏 |
| `mapGestures()` | 手势识别 | 移动端、触摸屏 |

---

## 协同创作模板

### 水墨 → 丹青 交接单

```markdown
## 视觉资产交接

**作品名**: [作品名称]
**风格**: [艺术风格]
**情感基调**: [情绪关键词]

### 视觉元素清单
- [ ] 背景层（颜色/渐变/纹理）
- [ ] 主视觉（核心图形/角色）
- [ ] 装饰元素（点缀/氛围）
- [ ] 光照配置（光源/强度/色温）

### 动画起点
- 初始状态: [静止/微动/动态]
- 时间轴: [0s-3s...]
- 节奏感: [缓慢/中等/快速]

### 丹青补充说明
[水墨给丹青的温馨提示]

---
```

### 丹青 → 水墨 反馈单

```markdown
## 交互设计反馈

**已完成交互**:
- [ ] Hover效果
- [ ] Click反馈
- [ ] Drag响应
- [ ] 实体行为

**需要视觉配合**:
- [ ] 加载动画（等待视觉）
- [ ] 过渡效果（视觉衔接）
- [ ] 特殊状态（空/错误/完成）

### 水墨补充说明
[丹青给水墨的温馨提示]

---
```

---

## 总结

**水墨 + 丹青 = 视觉 × 交互**

- 水墨负责"看到的美"——色彩、光影、构图、意境
- 丹青负责"感受的美"——交互、动画、反馈、惊喜

两者协同，让Browser Canvas Poetry的作品既有**诗意的画面**，又有**灵动的灵魂**。

> 水墨："艺术是留白的哲学"
> 丹青："交互是生命的呼吸"
> 协同："让我们一起创作会呼吸的艺术吧！"

---

*本系统定义了两个AI伙伴的协作机制，为Browser Canvas Poetry带来更丰富的创作体验。*