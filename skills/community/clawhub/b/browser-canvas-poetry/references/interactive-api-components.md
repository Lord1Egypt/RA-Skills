# Interactive API Components | 可导入的交互组件库

## 浏览器原生艺术的交互构件库

---

## 概述

本组件库提供**可import导入**的JavaScript/TypeScript模块，让Browser Canvas Poetry的交互艺术能力模块化、可复用。设计师和开发者可以直接引入这些组件，快速构建富有生命力的浏览器原生艺术作品。

### 设计理念

> "像搭积木一样创作艺术，每个组件都有生命，每个交互都有意义。"

### 核心特性

- **零依赖**：纯原生JavaScript/TypeScript，无外部库依赖
- **可组合**：组件之间可以自由组合，创造复杂效果
- **可定制**：每个组件都提供丰富的配置项
- **类型安全**：完整的TypeScript类型定义
- **轻量级**：每个组件<5KB gzip压缩

---

## 组件索引

| 组件 | 功能 | 复杂度 | 适用场景 |
|------|------|--------|----------|
| `ParticleSystem` | 粒子发射与运动 | ⭐⭐ | 星空、烟雾、雪花、萤火虫 |
| `PhysicsEngine` | 物理模拟（重力、碰撞、流体） | ⭐⭐⭐ | 粒子交互、刚体模拟、布料模拟 |
| `CreatureEngine` | 生物行为系统 | ⭐⭐⭐ | 小猫、小狗、蝴蝶、鸟儿 |
| `WaveGenerator` | 波形与波动效果 | ⭐⭐ | 水波、声音可视化、动态背景 |
| `GradientRenderer` | 渐变与色彩渲染 | ⭐ | 背景、过渡、氛围 |
| `EffectComposer` | 后期特效合成 | ⭐⭐ | 模糊、发光、色差 |
| `InteractionHandler` | 交互事件处理 | ⭐ | 点击、悬停、拖拽、触摸 |
| `AnimationTween` | 补间动画引擎 | ⭐ | 过渡、缓动、循环 |
| `AudioReactive` | 音频反应系统 | ⭐⭐⭐ | 音乐可视化、声波动画 |
| `ParticleTrail` | 粒子拖尾效果 | ⭐⭐ | 流星、笔触、轨迹 |

---

## ParticleSystem | 粒子系统

### 基本用法

```javascript
import { ParticleSystem } from 'browser-canvas-poetry/components';

const particles = new ParticleSystem({
  canvas: document.getElementById('canvas'),
  count: 200,
  emitRate: 5,           // 每秒发射粒子数
  lifetime: 3000,        // 粒子存活时间（毫秒）
  size: { min: 2, max: 8 },
  color: '#ffd700',
  velocity: { x: 0, y: -1 },
  spread: 0.5            // 扩散角度
});

particles.start();
```

### 配置参数

```typescript
interface ParticleSystemConfig {
  canvas: HTMLCanvasElement;           // 画布元素
  count: number;                         // 最大粒子数
  emitRate: number;                      // 发射速率（个/秒）
  lifetime: number;                      // 存活时间（毫秒）

  // 外观
  size: number | { min: number; max: number };
  color: string | string[];             // 单色或渐变色数组
  opacity: number;                      // 透明度 0-1
  shape: 'circle' | 'star' | 'heart' | 'custom';

  // 运动
  velocity: { x: number; y: number } | ((particle) => { x: number; y: number });
  spread: number;                        // 扩散角度（弧度）
  gravity: { x: number; y: number };
  friction: number;                     // 摩擦力 0-1
  turbulence: number;                   // 湍流强度

  // 行为
  trail: boolean;                       // 是否带拖尾
  blendMode: 'normal' | 'additive' | 'screen';
  onDeath?: (particle) => void;         // 死亡回调
}
```

### 预设模板

```javascript
// 萤火虫效果
import { ParticleSystem, Presets } from 'browser-canvas-poetry/components';
const fireflies = new ParticleSystem(Presets.fireflies);

// 雪花飘落
const snow = new ParticleSystem(Presets.snow);

// 星系旋转
const galaxy = new ParticleSystem(Presets.galaxy);

// 墨迹晕染
const ink = new ParticleSystem(Presets.inkDiffusion);
```

### 内置预设

| 预设名 | 描述 | 视觉效果 |
|--------|------|----------|
| `fireflies` | 萤火虫 | 温暖黄绿光点，轻微漂浮，随机闪烁 |
| `snow` | 雪花 | 白色圆点，缓缓飘落，有层次感 |
| `rain` | 细雨 | 细长线条，快速下落，有风感 |
| `galaxy` | 星系 | 密集星点，缓慢旋转，中心发光 |
| `sparkle` | 闪粉 | 小光点，随机闪烁，色彩斑斓 |
| `inkDiffusion` | 墨迹晕染 | 黑色扩散，随机飘散，有渗透感 |
| `confetti` | 彩带 | 五彩碎片，重力下落，有旋转 |
| `clouds` | 云朵 | 白色团状，缓慢漂浮，有叠层 |

### 方法

```typescript
// 粒子系统方法
particles.emit(count?: number);         // 发射指定数量粒子
particles.pause();                       // 暂停
particles.resume();                      // 恢复
particles.clear();                       // 清除所有粒子
particles.setVelocity(vector);           // 设置速度
particles.setColor(color);               // 设置颜色
particles.setPosition(x, y);             // 设置发射位置
particles.on(event, callback);           // 监听事件
particles.destroy();                     // 销毁系统
```

### 事件

```typescript
particles.on('emit', (particle) => {});        // 发射时
particles.on('death', (particle) => {});       // 死亡时
particles.on('update', (particles) => {});     // 每帧更新
particles.on('click', (particle, event) => {}); // 点击粒子
```

---

## PhysicsEngine | 物理引擎

### 基本用法

```javascript
import { PhysicsEngine } from 'browser-canvas-poetry/components';

const physics = new PhysicsEngine({
  gravity: { x: 0, y: 0.5 },
  wind: { x: 0.1, y: 0, variance: 0.02 },
  boundaries: 'wrap'           // 'infinite' | 'bounded' | 'wrap'
});

physics.addParticle({ x: 100, y: 100, vx: 2, vy: -1, mass: 1 });
physics.addAttractor({ x: 300, y: 300, strength: 50, radius: 200 });

physics.on('collision', (p1, p2) => {
  // 处理碰撞
});

physics.start();
```

### 配置参数

```typescript
interface PhysicsConfig {
  // 力场
  gravity: { x: number; y: number };
  wind?: { x: number; y: number; variance: number };

  // 边界
  boundaries: 'infinite' | 'bounded' | 'wrap';
  bounds?: { x: number; y: number; width: number; height: number };

  // 碰撞
  collisions: boolean;
  collisionElasticity: number;       // 弹性系数

  // 性能
  subSteps: number;                  // 子步骤数（精度）
  spatialHashCellSize: number;      // 空间哈希网格大小
}
```

### 物理对象

```typescript
// 添加粒子
physics.addParticle({
  x: number; y: number;
  vx: number; vy: number;
  mass: number;
  radius: number;
  charge?: number;                   // 电荷（用于电力）
  friction?: number;
  restitution?: number;              // 弹性
  customData?: object;               // 自定义数据
});

// 添加吸引器（引力场）
physics.addAttractor({
  x: number; y: number;
  strength: number;                  // 引力强度
  radius: number;                    // 影响范围
  falloff: 'linear' | 'inverse-square';
});

// 添加障碍物
physics.addObstacle({
  type: 'circle' | 'rect' | 'line';
  position: { x: number; y: number };
  size: object;
  static: boolean;                   // 是否静态
});

// 添加流体
physics.addFluid({
  density: number;                  // 密度
  viscosity: number;                // 粘度
  region: { x: number; y: number; width: number; height: number };
});
```

### 内置物理场景

```javascript
import { PhysicsEngine, PhysicsScenes } from 'browser-canvas-poetry/components';

// 粒子碰撞
const collisionScene = new PhysicsEngine(PhysicsScenes.collision);

// 布料悬挂
const clothScene = new PhysicsEngine(PhysicsScenes.cloth);

// 流体模拟
const fluidScene = new PhysicsEngine(PhysicsScenes.fluid);

// 万有引力
const gravityScene = new PhysicsEngine(PhysicsScenes.gravity);
```

---

## CreatureEngine | 生物引擎

### 基本用法

```javascript
import { CreatureEngine } from 'browser-canvas-poetry/components';

const ecosystem = new CreatureEngine({
  canvas: document.getElementById('canvas'),
  creatures: [
    { type: 'cat', count: 2, personality: 'curious' },
    { type: 'butterfly', count: 5, behavior: 'wander' },
    { type: 'firefly', count: 10, behavior: 'swarm' }
  ]
});

ecosystem.start();
```

### 生物类型

| 类型 | 默认行为 | 可配置属性 |
|------|----------|------------|
| `cat` | 闲逛、舔毛、打盹 | 毛色、性格、步伐 |
| `dog` | 摇尾、嗅闻、追逐 | 品种、大小、兴奋度 |
| `butterfly` | 飞舞、停歇、翅膀扇动 | 颜色、飞行轨迹 |
| `bird` | 飞翔、停歇、鸣叫 | 翅膀频率、高度偏好 |
| `fish` | 游动、吐泡、群体 | 鳞色、速度、群居性 |
| `firefly` | 发光、聚集、闪烁 | 亮度、闪烁频率 |
| `rabbit` | 跳跃、警觉、躲藏 | 毛色、耳朵长度 |
| `turtle` | 缓慢爬行、缩壳 | 壳纹、速度 |
| `frog` | 跳跃、鸣叫 | 颜色、大小 |
| `dragonfly` | 快速飞行、悬停 | 翅膀颜色、速度 |

### 配置参数

```typescript
interface CreatureConfig {
  type: CreatureType;
  position: { x: number; y: number };
  scale: number;                     // 相对大小
  personality: 'playful' | 'shy' | 'aggressive' | 'calm' | 'curious';
  color: string;                     // 主体颜色
  speed: number;                     // 移动速度
  energy: number;                   // 精力值 0-100

  // 行为
  behavior: 'wander' | 'follow' | 'flee' | 'hunt' | 'swarm' | 'idle';
  followTarget?: 'mouse' | 'creature' | 'path';

  // 动画
  animate: boolean;
  animationSpeed: number;

  // 状态
  mood: 'happy' | 'neutral' | 'sad' | 'scared' | 'excited';

  // 交互
  interactive: boolean;
  clickAction?: string;              // 点击行为
  hoverReaction?: string;           // 悬停反应
}
```

### 生物状态机

```typescript
// 每个生物都有状态机
creature.states.define('idle', {
  duration: [2000, 5000],           // 持续时间范围
  transitions: ['walk', 'sleep'],
  onEnter: () => { /* 开始发呆 */ },
  onUpdate: (dt) => { /* 发呆中 */ },
  onExit: () => { /* 结束发呆 */ }
});

creature.states.define('walk', {
  transitions: ['idle', 'run', 'react'],
  onEnter: () => { /* 开始走路 */ },
  onUpdate: (dt) => {
    // 移动逻辑
    creature.moveTo(targetPosition);
  }
});

creature.states.define('sleep', {
  duration: [5000, 15000],
  transitions: ['idle'],
  onEnter: () => {
    creature.playAnimation('sleep');
    creature.opacity = 0.7;
  }
});

creature.states.define('react', {
  transitions: ['idle', 'flee'],
  onEnter: (trigger) => {
    // 触发反应
    if (trigger === 'hover') {
      creature.playAnimation('look');
    } else if (trigger === 'click') {
      creature.playAnimation('jump');
    }
  }
});

// 状态切换
creature.states.setState('walk');
creature.states.getState();          // 当前状态
```

### 生物行为系统

```typescript
// 漫游行为
creature.behaviors.add('wander', {
  speed: 1,
  changeDirectionInterval: [2000, 4000],
  boundaryBehavior: 'bounce'
});

// 追随行为
creature.behaviors.add('follow', {
  target: 'mouse',
  distance: 50,                     // 保持距离
  smoothing: 0.1,                   // 平滑度
  leadDistance: 20                  // 提前量
});

// 躲避行为
creature.behaviors.add('flee', {
  triggerDistance: 100,
  speed: 3,
  safeDistance: 200
});

// 群聚行为（Boids算法）
creature.behaviors.add('flock', {
  separation: 30,
  alignment: 50,
  cohesion: 50,
  neighborhood: 100
});
```

### 预设生态系统

```javascript
import { CreatureEngine, EcosystemPresets } from 'browser-canvas-poetry/components';

// 森林生态系统
const forest = new CreatureEngine(EcosystemPresets.forest);
// 包含：兔子、松鼠、蝴蝶、鸟儿、萤火虫

// 海洋生态系统
const ocean = new CreatureEngine(EcosystemPresets.ocean);
// 包含：鱼群、海龟、水母、珊瑚

// 花园生态系统
const garden = new CreatureEngine(EcosystemPresets.garden);
// 包含：蜜蜂、蝴蝶、蜥蜴、青蛙、小鸟

// 夜晚生态系统
const night = new CreatureEngine(EcosystemPresets.night);
// 包含：萤火虫、猫头鹰、蝙蝠、星星
```

---

## WaveGenerator | 波形生成器

### 基本用法

```javascript
import { WaveGenerator } from 'browser-canvas-poetry/components';

const wave = new WaveGenerator({
  canvas: document.getElementById('canvas'),
  type: 'sine',                      // 波形类型
  frequency: 0.02,
  amplitude: 50,
  phase: 0,
  speed: 2,
  layers: 3                          // 波层数量
});

wave.start();
```

### 波形类型

| 类型 | 描述 | 视觉效果 |
|------|------|----------|
| `sine` | 正弦波 | 平滑起伏，优雅波浪 |
| `cosine` | 余弦波 | 类似正弦，相位偏移90° |
| `square` | 方波 | 硬朗边缘，机械感 |
| `sawtooth` | 锯齿波 | 急升缓降，扫描感 |
| `triangle` | 三角波 | 线性升降，规则感 |
| `noise` | 噪声波 | 随机波动，自然感 |
| `perlin` | Perlin噪声 | 平滑随机，烟雾感 |
| `simplex` | Simplex噪声 | 3D平滑噪声，更自然 |

### 配置参数

```typescript
interface WaveConfig {
  canvas: HTMLCanvasElement;

  // 波形
  type: WaveType;
  frequency: number;                 // 频率
  amplitude: number;                // 振幅
  phase: number;                   // 相位
  speed: number;                   // 速度

  // 外观
  color: string | string[];
  strokeWidth: number;
  fill: boolean;
  gradient: boolean;

  // 多层
  layers: number;                   // 波层数
  layerOffset: number;             // 层间偏移

  // 效果
  glow: boolean;
  glowIntensity: number;
  shadow: boolean;

  // 交互
  mouseInteraction: boolean;        // 鼠标交互
  audioReactive: boolean;          // 音频反应
}
```

### 使用示例：水面效果

```javascript
import { WaveGenerator } from 'browser-canvas-poetry/components';

const water = new WaveGenerator({
  canvas: document.getElementById('canvas'),
  type: 'perlin',
  frequency: 0.008,
  amplitude: 15,
  speed: 0.5,
  layers: 4,
  color: ['#1e3c72', '#2a5298', '#60a3bc', '#85c1e9'],
  fill: true,
  gradient: true,
  mouseInteraction: true
});

water.on('mouseenter', () => {
  water.setAmplitude(30);           // 鼠标进入时波浪加大
});

water.on('mouseleave', () => {
  water.setAmplitude(15);           // 鼠标离开时恢复平静
});
```

---

## GradientRenderer | 渐变渲染器

### 基本用法

```javascript
import { GradientRenderer } from 'browser-canvas-poetry/components';

const gradient = new GradientRenderer({
  canvas: document.getElementById('canvas'),
  type: 'linear',                   // 'linear' | 'radial' | 'conic'
  colors: [
    { color: '#ff6b6b', position: 0 },
    { color: '#feca57', position: 0.5 },
    { color: '#48dbfb', position: 1 }
  ],
  angle: 45,                        // 线性渐变角度
  animation: {
    type: 'rotate',                  // 'rotate' | 'shift' | 'pulse'
    duration: 5000,
    loop: true
  }
});

gradient.start();
```

### 配置参数

```typescript
interface GradientConfig {
  canvas: HTMLCanvasElement;

  type: 'linear' | 'radial' | 'conic' | 'mesh';

  // 颜色
  colors: Array<{
    color: string;
    position: number;               // 0-1
    opacity?: number;
  }>;

  // 几何
  angle: number;                   // 线性渐变角度
  center: { x: number; y: number }; // 径向渐变中心
  radius: number;                   // 径向渐变半径

  // 动画
  animation: {
    type: 'rotate' | 'shift' | 'pulse' | 'flow' | 'none';
    duration: number;
    loop: boolean;
    easing?: string;
  };

  // 滤镜
  blur: number;
  noise: number;                    // 添加噪点
  vignette: number;
}
```

### 使用示例：极光效果

```javascript
import { GradientRenderer } from 'browser-canvas-poetry/components';

const aurora = new GradientRenderer({
  canvas: document.getElementById('canvas'),
  type: 'linear',
  colors: [
    { color: '#00ff87', position: 0, opacity: 0.3 },
    { color: '#60efff', position: 0.4, opacity: 0.5 },
    { color: '#ff6b9d', position: 0.7, opacity: 0.4 },
    { color: '#c44569', position: 1, opacity: 0.2 }
  ],
  angle: 0,
  animation: {
    type: 'flow',
    duration: 8000,
    loop: true
  },
  blur: 20,
  noise: 0.1
});

aurora.start();
```

---

## EffectComposer | 特效合成器

### 基本用法

```javascript
import { EffectComposer } from 'browser-canvas-poetry/components';

const effects = new EffectComposer({
  source: canvasElement,
  effects: ['bloom', 'chromaticAberration', 'vignette']
});

effects.setIntensity('bloom', 0.8);
effects.setIntensity('chromaticAberration', 0.3);
effects.render();
```

### 内置特效

| 特效 | 参数 | 描述 |
|------|------|------|
| `bloom` | intensity, threshold, radius | 发光效果 |
| `blur` | radius, type | 模糊效果 |
| `chromaticAberration` | intensity, angle | 色差效果 |
| `vignette` | intensity, smoothness | 暗角效果 |
| `noise` | amount, monochrome | 噪点效果 |
| `colorGrade` | brightness, contrast, saturation, hue | 色彩调整 |
| `filmGrain` | intensity, animated | 胶片颗粒 |
| `scanlines` | frequency, intensity | 扫描线 |
| `glitch` | intensity, probability | 故障效果 |
| `pixelate` | size | 像素化 |
| `posterize` | levels | 海报化 |
| `sharpen` | intensity | 锐化 |

### 配置参数

```typescript
interface EffectConfig {
  // 通用
  intensity: number;                // 效果强度 0-1

  // bloom
  threshold?: number;               // 发光阈值
  radius?: number;                  // 发光半径

  // blur
  radius?: number;
  type?: 'gaussian' | 'box' | 'motion';
  direction?: { x: number; y: number }; // 运动模糊方向

  // chromaticAberration
  angle?: number;                   // 色差角度
  offset?: { x: number; y: number }; // 偏移量

  // colorGrade
  brightness?: number;
  contrast?: number;
  saturation?: number;
  hue?: number;
  levels?: { shadows: number; midtones: number; highlights: number };
}
```

---

## InteractionHandler | 交互处理器

### 基本用法

```javascript
import { InteractionHandler } from 'browser-canvas-poetry/components';

const interaction = new InteractionHandler({
  element: document.getElementById('canvas'),
  mouse: true,
  touch: true,
  keyboard: true,
  gesture: true
});

// 点击
interaction.on('click', (position, event) => {
  createRipple(position.x, position.y);
});

// 悬停
interaction.on('hover', (position) => {
  updateCursor(position);
});

// 拖拽
interaction.on('drag', (from, to, velocity) => {
  createTrail(from, to);
});

// 长按
interaction.on('longpress', (position, duration) => {
  triggerSpecialEffect(position);
});

// 双指缩放
interaction.on('pinch', (scale, center) => {
  zoomScene(scale, center);
});

// 自定义手势
interaction.on('swipe', (direction, velocity) => {
  if (direction === 'up') {
    showContent();
  }
});
```

### 配置参数

```typescript
interface InteractionConfig {
  element: HTMLElement;

  // 输入类型
  mouse: boolean;
  touch: boolean;
  keyboard: boolean;
  pointer: boolean;                 // 统一指针（未来）

  // 手势
  gesture: boolean;                // 是否启用手势识别
  gestureSensitivity: number;       // 灵敏度

  // 触摸
  touchAction: 'none' | 'pan' | 'zoom';
  preventDefault: boolean;

  // 性能
  throttle: number;                // 节流时间（毫秒）
  debounce: number;                 // 防抖时间（毫秒）
}
```

### 手势识别

```typescript
// 内置手势
interaction.gestures.enable('swipe');
interaction.gestures.enable('pinch');
interaction.gestures.enable('rotate');
interaction.gestures.enable('tap');
interaction.gestures.enable('doubletap');
interaction.gestures.enable('longpress');
interaction.gestures.enable('drag');

// 自定义手势
interaction.gestures.define('circle', {
  detector: (points) => {
    // 自定义圆形检测算法
    return isCircularMotion(points);
  },
  onRecognize: () => { /* 识别成功 */ }
});
```

---

## AnimationTween | 补间动画引擎

### 基本用法

```javascript
import { AnimationTween } from 'browser-canvas-poetry/components';

// 基础动画
AnimationTween.to(element, {
  x: 100,
  y: 200,
  opacity: 1,
  scale: 1.2,
  rotation: 360,
  duration: 1000,
  easing: 'elastic.out(1, 0.5)'
});

// 序列动画
AnimationTween.sequence([
  { target: element1, to: { opacity: 0 }, duration: 300 },
  { target: element2, to: { scale: 1.5 }, duration: 500, delay: 200 },
  { target: element3, to: { rotation: 180 }, duration: 400 }
]);

// 交错动画
AnimationTween.stagger(elements, {
  to: { y: 0, opacity: 1 },
  duration: 600,
  stagger: 100,                     // 每个延迟
  easing: 'back.out(1.7)'
});
```

### 内置缓动函数

```typescript
// 线性
'ease.linear'

// 二次
'ease.in.quad' | 'ease.out.quad' | 'ease.in.out.quad'

// 三次
'ease.in.cubic' | 'ease.out.cubic' | 'ease.in.out.cubic'

// 弹性
'elastic.out(1, 0.5)' | 'elastic.in(1, 0.5)' | 'elastic.inOut(1, 0.5)'

// 弹跳
'bounce.out' | 'bounce.in' | 'bounce.inOut'

// 回弹
'back.out(1.7)' | 'back.in(1.7)' | 'back.inOut(1.7)'

// 正弦
'sine.in' | 'sine.out' | 'sine.inOut'

// 指数
'expo.out' | 'expo.in' | 'expo.inOut'

// 圆
'circ.out' | 'circ.in' | 'circ.inOut'

// 自定义
'easing: (t) => Math.sin(t * Math.PI)'
```

### 配置参数

```typescript
interface TweenConfig {
  to: object;                       // 目标属性
  duration: number;                 // 持续时间（毫秒）

  // 缓动
  easing: string | function;

  // 时间控制
  delay: number;                    // 延迟开始
  loop: number | boolean;           // 循环次数或永久

  // 方向
  yoyo: boolean;                    // 来回动画

  // 回调
  onStart?: () => void;
  onUpdate?: (progress) => void;
  onComplete?: () => void;
  onRepeat?: () => void;
}
```

### 时间线控制

```typescript
const timeline = AnimationTween.createTimeline();

// 添加关键帧
timeline.add(element, {
  0: { x: 0, y: 0 },
  500: { x: 100, y: 50, scale: 1.2 },
  1000: { x: 200, y: 0, rotation: 360 }
});

// 添加子时间线
const subTimeline = timeline.addSubtimeline(500, 1000);
subTimeline.add(subElement, {
  0: { opacity: 0 },
  500: { opacity: 1 }
});

// 控制
timeline.play();
timeline.pause();
timeline.seek(500);
timeline.reverse();
timeline.setTimeScale(2);           // 2倍速
```

---

## AudioReactive | 音频反应系统

### 基本用法

```javascript
import { AudioReactive } from 'browser-canvas-poetry/components';

const audio = new AudioReactive({
  source: 'microphone',              // 'microphone' | 'audioElement' | 'file'
  analyser: {
    fftSize: 256,
    smoothing: 0.8
  }
});

audio.on('beat', (intensity) => {
  pulseEffect(intensity);
});

audio.on('frequency', (data) => {
  updateVisualizer(data);
});

audio.on('waveform', (data) => {
  drawWaveform(data);
});

audio.start();
```

### 配置参数

```typescript
interface AudioReactiveConfig {
  source: 'microphone' | 'audio' | 'oscillator';

  // 分析器
  analyser: {
    fftSize: 256 | 512 | 1024 | 2048;
    smoothing: number;              // 0-1
  };

  // 频率带
  bands: {
    bass: { min: 20, max: 250 };
    mid: { min: 250, max: 4000 };
    treble: { min: 4000, max: 20000 };
  };

  // 触发器
  beatDetection: {
    enabled: boolean;
    sensitivity: number;            // 灵敏度
    threshold: number;              // 节拍阈值
  };
}
```

### 音频数据

```typescript
// 获取频率数据
audio.getFrequencyData();           // Uint8Array

// 获取频带能量
audio.getEnergy('bass');            // 0-255
audio.getEnergy('mid');
audio.getEnergy('treble');

// 获取波形数据
audio.getWaveform();               // Uint8Array

// 获取节拍事件
audio.on('beat', (timestamp, intensity) => {});

// 获取峰值
audio.on('peak', (frequency, intensity) => {});
```

---

## ParticleTrail | 粒子拖尾

### 基本用法

```javascript
import { ParticleTrail } from 'browser-canvas-poetry/components';

const trail = new ParticleTrail({
  canvas: document.getElementById('canvas'),
  follow: mouse,                    // 跟随目标（mouse/element/point）
  maxParticles: 50,
  lifetime: 1000,
  size: { start: 10, end: 1 },      // 从大到小
  color: {
    start: 'rgba(255, 215, 0, 1)',
    end: 'rgba(255, 215, 0, 0)'
  },
  blendMode: 'additive'
});

trail.start();
```

### 配置参数

```typescript
interface ParticleTrailConfig {
  canvas: HTMLCanvasElement;

  // 目标
  follow: 'mouse' | HTMLElement | { x: number; y: number };
  offset: { x: number; y: number }; // 偏移

  // 粒子
  maxParticles: number;
  lifetime: number;                // 存活时间（毫秒）

  // 外观
  size: number | { start: number; end: number };
  color: string | { start: string; end: string };
  shape: 'circle' | 'star' | 'spark';

  // 运动
  velocity: { x: number; y: number };
  turbulence: number;
  gravity: number;

  // 效果
  blendMode: 'normal' | 'additive' | 'screen';
  glow: boolean;

  // 事件
  onEmit?: (particle) => void;
  onDeath?: (particle) => void;
}
```

---

## 预设组合包

### 预设包索引

| 包名 | 包含组件 | 适用场景 |
|------|----------|----------|
| `starter` | ParticleSystem, InteractionHandler, AnimationTween | 入门级交互 |
| `ecosystem` | CreatureEngine, ParticleSystem, PhysicsEngine | 生物生态 |
| `audio-visualizer` | AudioReactive, WaveGenerator, ParticleSystem | 音乐可视化 |
| `water-world` | WaveGenerator, PhysicsEngine, GradientRenderer | 水面效果 |
| `nebula` | ParticleSystem, EffectComposer, GradientRenderer | 宇宙星云 |
| `particle-art` | ParticleTrail, ParticleSystem, EffectComposer | 粒子艺术 |
| `interactive-game` | PhysicsEngine, CreatureEngine, InteractionHandler | 交互游戏 |

### 使用示例

```javascript
import { EcosystemPreset } from 'browser-canvas-poetry/components';

// 一行代码创建生态系统
const ecosystem = EcosystemPreset.create('forest');

// 或自定义组合
import { ComponentBundle } from 'browser-canvas-poetry/components';

const myBundle = new ComponentBundle({
  particles: { count: 100, color: '#ffd700' },
  creatures: [{ type: 'cat', count: 2 }],
  physics: { gravity: { x: 0, y: 0.3 } }
});

myBundle.start();
```

---

## 完整示例：月下萤火虫

```javascript
import {
  ParticleSystem,
  GradientRenderer,
  EffectComposer,
  InteractionHandler,
  AnimationTween
} from 'browser-canvas-poetry/components';

// 1. 创建夜空背景
const nightSky = new GradientRenderer({
  canvas: document.getElementById('canvas'),
  type: 'radial',
  colors: [
    { color: '#0a0a1a', position: 0 },
    { color: '#1a1a3a', position: 0.5 },
    { color: '#2a2a5a', position: 1 }
  ],
  center: { x: 0.5, y: 0.2 },
  radius: 1.5
});

// 2. 创建月亮光晕
const moonGlow = new EffectComposer({
  source: document.getElementById('canvas'),
  effects: ['bloom']
});
moonGlow.setIntensity('bloom', 0.6);

// 3. 创建萤火虫粒子系统
const fireflies = new ParticleSystem({
  canvas: document.getElementById('canvas'),
  count: 30,
  emitRate: 0,                       // 初始发射
  lifetime: 8000,
  size: { min: 3, max: 8 },
  color: ['#ffd700', '#90ee90', '#87ceeb'],
  velocity: { x: 0, y: 0 },
  turbulence: 0.5,
  blendMode: 'additive',
  glow: true
});

// 初始化萤火虫位置
for (let i = 0; i < 30; i++) {
  fireflies.emit();
}

// 4. 交互：鼠标吸引萤火虫
const interaction = new InteractionHandler({
  element: document.getElementById('canvas'),
  mouse: true
});

interaction.on('move', (pos) => {
  fireflies.particles.forEach(p => {
    const dx = pos.x - p.x;
    const dy = pos.y - p.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < 150) {
      p.vx += dx * 0.0005;
      p.vy += dy * 0.0005;
    }
  });
});

// 5. 启动所有系统
nightSky.start();
fireflies.start();
moonGlow.render();

// 6. 添加点击效果：点击生成新的萤火虫
interaction.on('click', (pos) => {
  fireflies.setPosition(pos.x, pos.y);
  fireflies.emit(5);

  // 点击涟漪动画
  AnimationTween.to(clickRipple, {
    scale: 3,
    opacity: 0,
    duration: 800,
    easing: 'ease.out.cubic'
  });
});

// 7. 自动闪烁动画
setInterval(() => {
  const randomFirefly = fireflies.particles[Math.floor(Math.random() * 30)];
  if (randomFirefly) {
    AnimationTween.to(randomFirefly, {
      size: randomFirefly.size * 2,
      duration: 200,
      easing: 'ease.out.quad',
      onComplete: () => {
        AnimationTween.to(randomFirefly, {
          size: randomFirefly.size / 2,
          duration: 400
        });
      }
    });
  }
}, 500);
```

---

## 导入方式

### ES Module

```javascript
// 导入全部组件
import {
  ParticleSystem,
  PhysicsEngine,
  CreatureEngine,
  WaveGenerator,
  GradientRenderer,
  EffectComposer,
  InteractionHandler,
  AnimationTween,
  AudioReactive,
  ParticleTrail
} from 'browser-canvas-poetry/components';

// 导入单个组件
import { ParticleSystem } from 'browser-canvas-poetry/components/ParticleSystem';

// 导入预设
import { Presets } from 'browser-canvas-poetry/components/presets';
import { EcosystemPresets } from 'browser-canvas-poetry/components/ecosystem-presets';
```

### CDN

```html
<!-- 通过CDN引入 -->
<script src="https://unpkg.com/browser-canvas-poetry/components.min.js"></script>

<script>
  const { ParticleSystem, AnimationTween } = BCP;
</script>
```

### NPM

```bash
npm install browser-canvas-poetry
```

```javascript
import { ParticleSystem } from 'browser-canvas-poetry';
```

---

## 组件通信

### 事件总线

```javascript
import { EventBus } from 'browser-canvas-poetry/core';

// 创建全局事件总线
const bus = new EventBus();

// 组件A发布事件
particleSystem.on('collision', (p1, p2) => {
  bus.emit('physics:collision', { p1, p2 });
});

// 组件B订阅事件
bus.on('physics:collision', ({ p1, p2 }) => {
  visualEffect.trigger(p1.x, p1.y);
});
```

### 共享数据

```javascript
import { DataStore } from 'browser-canvas-poetry/core';

// 创建共享数据存储
const store = new DataStore({
  mouse: { x: 0, y: 0 },
  time: 0,
  audioLevel: 0
});

// 粒子系统读取mouse
const particles = new ParticleSystem({
  onUpdate: () => {
    const mouse = store.get('mouse');
    // 使用mouse数据
  }
});

// 交互处理器更新mouse
const interaction = new InteractionHandler({
  onMove: (pos) => {
    store.set('mouse', pos);
  }
});
```

---

## 性能优化

### 建议

1. **对象池**：重复创建/销毁粒子时使用对象池
2. **离屏渲染**：复杂效果使用离屏Canvas
3. **请求动画帧**：所有动画使用requestAnimationFrame
4. **节流**：高频事件（鼠标移动）进行节流
5. **降级**：低性能设备自动降级效果
6. **批量绘制**：同类元素批量绘制减少draw call

### 内置优化

```javascript
// 自动性能检测
import { PerformanceMonitor } from 'browser-canvas-poetry/components';

const monitor = new PerformanceMonitor();
monitor.on('low', () => {
  // 自动降级
  particles.setCount(50);
  effects.disable('bloom');
});
monitor.on('medium', () => {
  // 中等模式
  particles.setCount(100);
});
monitor.on('high', () => {
  // 完整模式
  particles.setCount(200);
  effects.enable('bloom');
});

monitor.start();
```

---

## 总结

本交互组件库提供了**10个核心模块**，可以自由组合创建丰富的浏览器原生艺术作品：

- **粒子系统** - 星空、烟雾、萤火虫
- **物理引擎** - 碰撞、流体、引力
- **生物引擎** - 小猫、小狗、蝴蝶
- **波形生成** - 水波、声音可视化
- **渐变渲染** - 极光、天空、水面
- **特效合成** - 发光、色差、暗角
- **交互处理** - 点击、拖拽、手势
- **补间动画** - 过渡、缓动、时间线
- **音频反应** - 音乐可视化
- **粒子拖尾** - 流星、笔触

> "像搭积木一样创作艺术，每个组件都有生命，每个交互都有意义。"

---

*本组件库是Browser Canvas Poetry的核心交互能力，可独立使用或与水墨丹青系统协同工作。*