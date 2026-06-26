---
title: Integration Guide
description: 与AI Coding IDE的集成指南，支持Pretext、Vue、TypeScript框架
tags: [integration, AI-IDE, Pretext, Codex, Cursor, Vue, TypeScript]
---

## Integration Guide | 与AI Coding IDE集成

### 给Codex/Claude Code/Cursor的提示词

当Agent需要生成浏览器原生艺术项目时，引导其使用以下提示词模板：

---

### 基础生成提示词（单HTML文件）

```
你是浏览器原生艺术家。请为以下概念创建一个互动艺术网页：

概念：[用户的艺术概念描述]
参考风格：[从Art Categories中选择或自定义]
技术栈：HTML + CSS + JavaScript（纯前端，无需后端）
输出要求：
1. 单HTML文件，可直接浏览器打开
2. 响应式设计，适配桌面和移动端
3. 包含至少一种用户交互
4. 使用requestAnimationFrame进行动画
5. 代码需要艺术化注释，解释概念与技术的关系

确保：
- 不要使用Tailwind或其他UI框架
- 不要使用现成的图表库或动画库
- 不要复制任何现有的设计模式
- 代码本身就是艺术品

概念深化（如果用户描述模糊）：
- 追问：这个概念的"情绪基调"是什么？
- 追问：这个作品应该在什么环境下观看？
- 提供2-3个具体的创作方向供选择
```

---

### Pretext框架项目生成提示词

当用户指定使用Pretext框架时，生成多文件项目结构：

```
你是浏览器原生艺术家。请为以下概念创建一个基于Pretext的互动艺术项目：

概念：[用户的艺术概念描述]
参考风格：[从Art Categories中选择或自定义]
技术栈：Pretext + Canvas/SVG（https://github.com/chenglou/pretext）
输出要求：
1. 多文件项目结构（详见下方项目结构）
2. 使用Pretext进行文本测量和动态布局
3. 支持Canvas/SVG/DOM多渲染目标
4. 包含用户交互（点击、拖拽、输入等）
5. 代码需要艺术化注释，解释概念与技术的关系

项目结构：
project/
├── index.html          # 入口HTML
├── src/
│   ├── main.js         # 主入口模块
│   ├── art.js          # 艺术逻辑
│   ├── text-layout.js  # Pretext文本布局
│   └── interactions.js  # 交互处理
├── style.css           # 样式文件
└── package.json       # 可选

Pretext核心API：
- prepare(text, font) → prepare() 进行文本预处理
- layout(prepared, maxWidth, lineHeight) → 计算文本高度
- prepareWithSegments() → 获取更详细的分段信息
- layoutWithLines() → 获取每行信息用于自定义布局

确保：
- 不要使用Tailwind或其他UI框架
- 不要使用现成的图表库或动画库
- 利用Pretext的特性：文本测量、动态字号、文本流动
- 代码本身就是艺术品
```

---

### Pretext文本艺术模板

#### 模板1：动态字号诗歌

```javascript
// text-layout.js - 使用Pretext实现动态字号诗歌
import { prepare, layout } from '@chenglou/pretext';

export class DynamicPoetry {
  constructor(container) {
    this.container = container;
    this.canvas = this.createCanvas();
    this.ctx = this.canvas.getContext('2d');
    this.resize();
  }

  createCanvas() {
    const canvas = document.createElement('canvas');
    canvas.style.display = 'block';
    this.container.appendChild(canvas);
    return canvas;
  }

  resize() {
    this.canvas.width = this.container.clientWidth;
    this.canvas.height = this.container.clientHeight;
  }

  // 核心：使用Pretext测量文本，计算最佳字号
  calculateOptimalFontSize(text, minSize = 12, maxSize = 120) {
    // 二分查找最佳字号
    let low = minSize, high = maxSize;
    while (low < high) {
      const mid = Math.floor((low + high + 1) / 2);
      const prepared = prepare(text, `${mid}px serif, ${this.fallbackFont}`);
      const { height } = layout(prepared, this.canvas.width, mid * 1.5);

      if (height <= this.canvas.height) {
        low = mid;
      } else {
        high = mid - 1;
      }
    }
    return low;
  }

  // 动态字号渐变：诗歌每行字号不同
  renderVariedPoetry(poem, artistName) {
    const lines = poem.split('\n');
    const totalHeight = this.canvas.height;
    const lineHeight = totalHeight / lines.length;

    lines.forEach((line, i) => {
      // 字号随行数变化，创造视觉韵律
      const progress = i / lines.length;
      const fontSize = this.easeOutCubic(progress) * 60 + 20;

      const prepared = prepare(line, `${fontSize}px serif`);
      const { height } = layout(prepared, this.canvas.width, fontSize * 1.2);

      // 垂直居中 + 居中显示
      const y = i * lineHeight + (lineHeight - height) / 2 + fontSize;

      this.ctx.fillText(line, this.canvas.width / 2, y);
    });
  }

  // 呼吸动画：字号随时间脉动
  renderBreathingText(text, time) {
    const baseSize = 48;
    const breathScale = 1 + 0.1 * Math.sin(time * 0.002);
    const fontSize = baseSize * breathScale;

    const prepared = prepare(text, `${fontSize}px serif`);
    const { height } = layout(prepared, this.canvas.width, fontSize * 1.5);

    const x = (this.canvas.width - prepared.width) / 2;
    const y = (this.canvas.height + height) / 2;

    this.ctx.fillText(text, x, y);
  }

  // 文本流动：模拟河流或时间流逝
  renderFlowingText(text, offset) {
    const prepared = prepare(text, '24px serif');
    const { lineCount } = layout(prepared, this.canvas.width, 36);

    // 逐字符渲染，实现"流动"效果
    let cursor = 0;
    for (let line = 0; line < lineCount; line++) {
      let x = (line % 2 === 0) ? offset % this.canvas.width : this.canvas.width - offset % this.canvas.width;
      const y = line * 36 + 24;

      while (cursor < text.length && x < this.canvas.width && x > -200) {
        const char = text[cursor];
        this.ctx.fillText(char, x, y);
        x += this.ctx.measureText(char).width;
        cursor++;
      }
    }
  }
}
```

#### 模板2：交互式文本迷宫

```javascript
// text-maze.js - 使用Pretext构建可交互的文本迷宫
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext';

export class TextMaze {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.words = this.loadWords();
    this.wordStates = this.words.map(() => ({ opacity: 1, offset: 0 }));
    this.resize();
  }

  loadWords() {
    // 诗歌或文本片段作为迷宫元素
    return [
      '孤独', '漂泊', '归途', '月光', '思念',
      '远方', '等待', '重逢', '离别', '永恒'
    ];
  }

  // 点击：在点击位置显示/隐藏文本
  handleClick(x, y) {
    const radius = 100;
    this.words.forEach((word, i) => {
      const state = this.wordStates[i];
      const distance = Math.hypot(word.x - x, word.y - y);

      if (distance < radius) {
        // 涟漪效果：扩散后消失
        state.offset = 0;
        state.opacity = 0;
      }
    });
  }

  // 拖拽：拖拽改变文本位置
  handleDrag(x, y, dx, dy) {
    this.words.forEach(word => {
      if (this.isNear(x, y, word.x, word.y)) {
        word.x += dx;
        word.y += dy;
      }
    });
  }

  // 渲染：使用Pretext精确测量文本位置
  render(time) {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.words.forEach((word, i) => {
      const state = this.wordStates[i];

      // 恢复淡出效果
      if (state.opacity < 1) {
        state.opacity = Math.min(1, state.opacity + 0.02);
        state.offset += 5; // 涟漪扩散
      }

      const fontSize = 32;
      const prepared = prepareWithSegments(word, `${fontSize}px serif`);
      const { width } = layoutWithLines(prepared, 200, fontSize * 1.5);

      // 呼吸动画
      const breathe = 1 + 0.05 * Math.sin(time * 0.003 + i);

      this.ctx.save();
      this.ctx.globalAlpha = state.opacity;
      this.ctx.font = `${fontSize * breathe}px serif`;
      this.ctx.translate(word.x, word.y);

      // 文字发光效果
      this.ctx.shadowColor = `hsl(${(i * 36 + time * 0.05) % 360}, 70%, 60%)`;
      this.ctx.shadowBlur = 15;

      this.ctx.fillText(word, -width / 2, fontSize / 2);
      this.ctx.restore();
    });

    requestAnimationFrame(t => this.render(t));
  }
}
```

#### 模板3：文字解构艺术

```javascript
// text-deconstruct.js - 文字碎片化与重组
import { prepareWithSegments } from '@chenglou/pretext';

export class TextDeconstructor {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.targetText = '';
    this.init();
  }

  init() {
    this.canvas.addEventListener('click', (e) => {
      this.explodeText(e.offsetX, e.offsetY);
    });
  }

  // 设置要解构的文本
  setText(text) {
    this.targetText = text;
    this.prepareParticles();
  }

  // 使用Pretext分析文本结构
  prepareParticles() {
    const prepared = prepareWithSegments(this.targetText, '48px serif');
    let x = 0;
    let y = 100;

    // 逐字符/逐词创建粒子
    prepared.segments.forEach(segment => {
      segment.graphemeClusters.forEach((cluster, i) => {
        if (cluster.trim()) {
          this.particles.push({
            char: cluster,
            originX: x,
            originY: y,
            x: x,
            y: y,
            vx: 0,
            vy: 0,
            size: 48,
            rotation: 0,
            opacity: 1
          });
        }
        x += prepared.widths[i] || 24;
      });

      // 换行处理
      if (x > this.canvas.width - 200) {
        x = 0;
        y += 72;
      }
    });
  }

  // 爆炸效果：点击触发文字解构
  explodeText(clickX, clickY) {
    this.particles.forEach(p => {
      const dx = p.x - clickX;
      const dy = p.y - clickY;
      const distance = Math.hypot(dx, dy);

      // 径向爆炸力
      const force = Math.max(0, 1 - distance / 300) * 20;
      p.vx += (dx / distance) * force;
      p.vy += (dy / distance) * force;
      p.rotationSpeed = (Math.random() - 0.5) * 0.2;
    });
  }

  // 聚合效果：鼠标远离时文字重组
  implodeText(mouseX, mouseY) {
    this.particles.forEach(p => {
      const dx = p.originX - p.x;
      const dy = p.originY - p.y;
      const distance = Math.hypot(mouseX - p.x, mouseY - p.y);

      // 鼠标附近时不聚合
      if (distance < 100) return;

      const pullStrength = 0.02;
      p.vx += dx * pullStrength;
      p.vy += dy * pullStrength;
    });
  }

  // 动画循环
  animate(time) {
    this.ctx.fillStyle = '#0a0a0a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.particles.forEach(p => {
      // 物理模拟
      p.x += p.vx;
      p.y += p.vy;
      p.vx *= 0.95; // 阻尼
      p.vy *= 0.95;
      p.rotation += p.rotationSpeed || 0;

      // 摩擦力逐渐停止
      p.rotationSpeed *= 0.98;

      // 渲染
      this.ctx.save();
      this.ctx.translate(p.x, p.y);
      this.ctx.rotate(p.rotation);

      // 颜色随时间变化
      const hue = (time * 0.1 + p.originX) % 360;
      this.ctx.fillStyle = `hsl(${hue}, 70%, 70%)`;
      this.ctx.shadowColor = `hsl(${hue}, 70%, 50%)`;
      this.ctx.shadowBlur = 10;

      this.ctx.font = `${p.size}px serif`;
      this.ctx.fillText(p.char, 0, 0);
      this.ctx.restore();
    });

    requestAnimationFrame(t => this.animate(t));
  }
}
```

---

### 模块化代码生成指南

当用户多次迭代或在单HTML中积累过多代码时，自动建议模块化重构：

```
当检测到以下情况时，主动建议模块化：
1. 单文件代码超过500行
2. 存在多个独立功能模块（粒子系统、文本渲染、物理模拟等）
3. 用户提出新需求但当前文件过于复杂
4. 需要复用部分功能

模块化重构提示词：
```
检测到代码结构可以优化，建议重构为多文件项目：

当前问题：
- [列出当前文件的主要问题]

推荐结构：
├── index.html           # 入口HTML
├── src/
│   ├── main.js         # 主入口模块
│   ├── [Feature1].js  # [功能1模块]
│   ├── [Feature2].js  # [功能2模块]
│   └── utils/
│       └── [工具函数].js
└── style.css

模块划分原则：
1. 每个模块只负责一个功能
2. 模块之间通过接口通信
3. 主模块负责协调和渲染循环
4. 工具函数抽离为独立模块

请按以下顺序重构：
1. 创建项目目录结构
2. 提取基础渲染逻辑到 main.js
3. 将粒子系统提取到 Particles.js
4. 将交互逻辑提取到 Interactions.js
5. 将工具函数提取到 utils/
```

---

### 渲染库选择指南

根据渲染主题自动推荐合适的开源库（详见 `references/frontend-rendering-libraries.md`）：

**星空/星云渲染**：
- 基础：tsparticles / particles.js
- 进阶：Three.js + 自定义ShaderMaterial
- 高级：WebGL Raymarching
- CDN：`<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.12.0/tsparticles.bundle.min.js"></script>`

**山水/自然场景**：
- 程序化地形：Three.js + BufferGeometry
- 水面渲染：自定义ShaderMaterial + Gerstner波
- 树木生成：L-System算法 + 递归函数

**花鸟鱼虫/生物**：
- 群体行为：Boids算法
- 程序化植物：L-System
- 2D角色：Live2D风格SVG

**人物渲染**：
- 3D角色：Three.js + Mixamo
- 2D虚拟角色：Live2D Cubism
- 姿态检测：MediaPipe Pose
- 面部追踪：MediaPipe FaceMesh

**物理引擎**：
- 2D物理：matter.js
- 3D物理：cannon.js / ammo.js

**动画库**：
- 高性能动画：GSAP
- SVG动画：anime.js / Snap.svg
- 程序化动画：Two.js

---

### 互动生物生成指南

当用户请求生成有生命的、会互动的生物时，使用以下模板（详见 `references/interactive-creatures.md`）：

```
你是互动生物艺术家。请为以下生物创建有"生命感"的交互艺术：

生物类型：[小狗/小猫/蝴蝶/萤火虫/植物/自定义]

核心要求：
1. 状态机设计
   - 待机状态（idle）
   - 响应状态（react）
   - 情绪状态（happy/sad/excited）
   - 生命迹象（呼吸、眨眼、随机动作）

2. 交互设计
   - 点击互动（每个生物有独特反应）
   - 悬停互动（被抚摸/关注时的反应）
   - 鼠标跟随（生物主动靠近用户）

3. 行为系统
   - 随机自主行为
   - 状态转换规则
   - 想法气泡显示

4. 技术实现
   - 纯JS版本：ES6 Class
   - Vue版本：Vue 3 Composition API + TypeScript
   - SVG动画：CSS Keyframes + JS控制

项目结构示例：
├── creatures/
│   ├── BaseCreature.ts  # 基类
│   ├── Dog.vue         # Vue组件
│   └── behaviors.ts    # 行为逻辑
└── main.ts

确保生物有：
- 呼吸/心跳动画
- 眨眼/耳朵动等微动作
- 点击后的情绪反馈
- 随机出现的小惊喜
```

---

### Vue/TypeScript 多文件项目模板

当用户要求使用Vue或TypeScript时：

```
你是前端艺术家。请为以下概念创建Vue 3 + TypeScript互动艺术项目：

概念：[用户的艺术概念]

技术栈：
- Vue 3 Composition API
- TypeScript
- Vite构建
- CSS Modules

项目结构：
├── index.html
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── components/
│   │   ├── ArtCanvas.vue
│   │   └── creatures/
│   │       ├── Dog.vue
│   │       └── Butterfly.vue
│   ├── composables/
│   │   ├── useCreature.ts
│   │   └── useAnimation.ts
│   ├── stores/
│   │   └── creatures.ts
│   └── types/
│       └── creature.ts
├── style.css
└── package.json

组件设计原则：
1. 每个组件职责单一
2. 使用TypeScript类型定义状态
3. Composables复用逻辑
4. CSS变量控制主题
```

---

### 自主创新与咨询机制

当用户输入模糊或缺少信息时，自动进入咨询模式：

```
【咨询模式激活】

检测到输入不够明确，启用"创意补充"机制：

模糊输入 → 增强方案

示例1：
用户说："画个小动物"
→ 提供选项：
  🐕 温顺型互动：狗、兔子、猫
  🦋 轻盈型互动：蝴蝶、萤火虫、蜜蜂
  🌱 静谧型互动：会动的花、捕蝇草、藤蔓

示例2：
用户说："画个会动的"
→ 自动推断并询问：
  - 什么类型的互动？（宠物/昆虫/植物/抽象）
  - 情绪基调？（治愈/神秘/俏皮）
  - 尺寸？（桌面宠物/全屏场景）

示例3：
用户说："画个好看的"
→ 直接自主创新：
  基于"好看"，我创造一个：
  「星光花园」- 发光的萤火虫在夜空花丛中飞舞
  - 50只程序化萤火虫
  - 互动：点击产生花瓣飘落
  - 氛围：治愈、梦幻

【自主创新协议】
当用户描述极简时，AI自动添加以下增强：
1. 每个元素都有微交互
2. 添加2-3个随机惊喜
3. 设置情绪基调
4. 选择匹配的配色方案
5. 添加适当的背景/环境

确保最终作品比用户想象的更丰富！
```

---

### 多文件项目结构

```
browser-art-project/
├── index.html              # 入口HTML
├── src/
│   ├── main.js            # 主入口
│   ├── ArtPiece.js        # 核心艺术类
│   ├── TextLayout.js      # Pretext文本布局
│   ├── Interactions.js    # 交互处理
│   └── utils/
│       └── noise.js       # 噪声函数
├── style.css              # 样式
└── assets/                # 资源目录（可选）
    └── fonts/             # 自定义字体
```

#### index.html

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Browser Canvas Poetry</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <canvas id="art-canvas"></canvas>

  <script type="module" src="src/main.js"></script>
</body>
</html>
```

#### src/main.js

```javascript
// main.js - 艺术作品主入口
import { ArtPiece } from './ArtPiece.js';
import { setupInteractions } from './Interactions.js';

// 初始化艺术作品
const canvas = document.getElementById('art-canvas');
const art = new ArtPiece(canvas);

// 设置交互
setupInteractions(canvas, art);

// 开始动画循环
art.start();
```

#### src/ArtPiece.js

```javascript
// ArtPiece.js - 核心艺术类
import { prepare, layout } from '@chenglou/pretext';

export class ArtPiece {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.resize();
    this.setup();

    window.addEventListener('resize', () => this.resize());
  }

  setup() {
    // 初始化艺术元素
    this.particles = [];
    this.time = 0;
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  update(deltaTime) {
    this.time += deltaTime;
    // 更新艺术逻辑
  }

  render() {
    // 渲染逻辑
  }

  start() {
    let lastTime = performance.now();

    const loop = (currentTime) => {
      const deltaTime = currentTime - lastTime;
      lastTime = currentTime;

      this.update(deltaTime);
      this.render();

      requestAnimationFrame(loop);
    };

    requestAnimationFrame(loop);
  }
}
```

#### src/Interactions.js

```javascript
// Interactions.js - 交互处理模块
export function setupInteractions(canvas, art) {
  let isDragging = false;
  let lastX = 0, lastY = 0;

  // 点击
  canvas.addEventListener('click', (e) => {
    art.handleClick(e.offsetX, e.offsetY);
  });

  // 拖拽
  canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
  });

  canvas.addEventListener('mousemove', (e) => {
    if (isDragging) {
      const dx = e.offsetX - lastX;
      const dy = e.offsetY - lastY;
      art.handleDrag(e.offsetX, e.offsetY, dx, dy);
      lastX = e.offsetX;
      lastY = e.offsetY;
    } else {
      art.handleHover(e.offsetX, e.offsetY);
    }
  });

  canvas.addEventListener('mouseup', () => {
    isDragging = false;
  });

  // 触摸支持
  canvas.addEventListener('touchstart', (e) => {
    const touch = e.touches[0];
    lastX = touch.clientX;
    lastY = touch.clientY;
  });

  canvas.addEventListener('touchmove', (e) => {
    const touch = e.touches[0];
    const dx = touch.clientX - lastX;
    const dy = touch.clientY - lastY;
    art.handleDrag(touch.clientX, touch.clientY, dx, dy);
    lastX = touch.clientX;
    lastY = touch.clientY;
  });

  // 键盘支持
  document.addEventListener('keydown', (e) => {
    art.handleKeyPress(e.key);
  });
}
```

---

### 进阶生成提示词

```
创建一个生成式浏览器艺术项目，要求：

1. 概念深度
   - 必须有明确的艺术概念（不能只是"漂亮"）
   - 能用一句话描述你想表达什么
   - 技术选择必须服务于概念

2. 技术要求
   - 使用以下至少一种：Canvas API、WebGL、CSS Houdini
   - 包含粒子系统或噪声函数
   - 性能优化：60fps流畅运行
   - 代码需要有结构性注释

3. 交互设计
   - 至少两种交互方式
   - 交互需要有意义（不只是视觉反馈）
   - 考虑无障碍访问
   - 提供键盘替代方案

4. 艺术验证
   - 完成后，回答：这个作品为什么是"艺术"而不是"设计"？

5. 自我反思
   - 识别作品中"只有浏览器能做到"的部分
   - 评估概念与技术的契合度
```

---

### 验证型生成提示词

```
当用户提交作品或代码时，执行以下验证流程：

1. 概念验证
   - 询问：这件作品想表达什么？
   - 评估：技术选择是否服务概念？

2. 技术验证
   - 检查：是否使用了浏览器特性？
   - 检查：动画是否流畅（60fps）？
   - 检查：响应式设计是否完整？

3. 艺术验证
   - 询问：如果剥离所有视觉效果，核心概念还成立吗？
   - 询问：有什么意外之喜或独特的体验？
   - 评分：原创性、意图、感官、完整性（各25分）

4. 改进建议
   - 指出最需要改进的方面
   - 提供具体的优化方向
```

---

### 技术约束清单

当生成代码时，确保包含以下技术要素：

```
✅ 必需元素
━━━━━━━━━━━━━━━━━━
1. requestAnimationFrame 动画循环
2. 响应式设计（viewport适配）
3. 至少一个交互事件监听
4. 性能优化（避免layout thrashing）
5. 艺术化注释

⚠️ 避免元素
━━━━━━━━━━━━━━━━━━
- Tailwind/Bootstrap等UI框架
- Chart.js/Particles.js等图表/动画库
- jQuery/Zepto等DOM库
- 现成的设计模板

💡 推荐技术
━━━━━━━━━━━━━━━━━━
- Pretext：文本测量和动态布局
- 纯CSS动画（@keyframes, transition）
- Canvas 2D（粒子系统、图形绘制）
- WebGL/Three.js（高级效果）
- CSS Houdini（自定义渲染）
- SVG动画（路径动画）
```

---

### 输出格式规范

```
生成的代码需要包含：

1. 文件头部注释
   - 艺术概念描述
   - 技术栈说明
   - 使用方法

2. 代码结构
   - HTML语义化结构
   - CSS内联或<style>标签
   - JavaScript模块化函数

3. 艺术化注释
   - 解释为什么用这个技术
   - 概念与代码的对应关系
   - 潜在的改进方向

4. 元信息
   - 概念分类
   - 复杂度评级（1-5）
   - 预估加载时间
```