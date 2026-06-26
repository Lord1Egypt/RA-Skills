---
title: Interactive Creatures Guide
description: 互动生物行为系统完整指南 - 让小动物"活"起来
tags: [interactive, creatures, behavior, AI, pets, animals, Vue, TypeScript]
---

## 互动生物行为系统指南

让生成的生物拥有生命感、行为模式和情感反应。

---

## 一、行为系统架构

### 核心状态机

```typescript
// 基础生物状态
interface CreatureState {
  // 基础状态
  position: { x: number; y: number };
  velocity: { x: number; y: number };
  rotation: number;
  scale: number;

  // 行为状态
  currentAction: 'idle' | 'walk' | 'run' | 'sleep' | 'eat' | 'play' | 'react';
  mood: 'happy' | 'neutral' | 'sad' | 'excited' | 'scared';

  // 内部状态
  energy: number;      // 精力 0-100
  hunger: number;       // 饥饿度 0-100
  happiness: number;    // 快乐度 0-100
  attention: number;    // 注意力
}

// 状态转换规则
const stateTransitions = {
  idle: {
    on: {
      click: 'react',
      time: 3000, // 3秒后
      target: 'sleep',
      condition: (s) => s.energy < 30
    }
  },
  walk: {
    on: {
      click: 'react',
      time: 5000,
      target: 'idle',
      condition: () => true
    }
  },
  sleep: {
    on: {
      click: 'react',
      time: 10000,
      target: 'idle',
      condition: (s) => s.energy > 80
    }
  }
};
```

---

## 二、动物行为模板

### 2.1 小狗 🐕

```javascript
// creatures/Dog.js - 小狗行为系统
export class Dog {
  constructor(container) {
    this.container = container;
    this.state = {
      position: { x: 0, y: 0 },
      velocity: { x: 0, y: 0 },
      rotation: 0,
      action: 'idle',
      mood: 'happy',
      energy: 100,
      hunger: 0,
      tailWag: 0,
      earPerk: 0
    };

    this.behaviors = {
      // 待机行为
      idle: {
        duration: [2000, 5000],
        animations: ['breathe', 'lookAround', 'tailWag', 'earPerk'],
        next: ['walk', 'sit', 'sleep']
      },

      // 跟随主人
      follow: {
        target: null,
        speed: 2,
        distance: 50,
        animations: ['walk', 'run', 'happyJump']
      },

      // 对主人热情
      greet: {
        trigger: '主人靠近',
        animations: ['jump', 'spin', 'tailWagFast', 'lickFace'],
        duration: 2000
      },

      // 求投喂
      beg: {
        trigger: '饥饿 > 70',
        animations: ['sit', 'lookUp', 'pawLift'],
        sound: '呜呜叫'
      },

      // 睡觉
      sleep: {
        animations: ['breathe', 'snore', 'dream'],
        trigger: '精力 < 20'
      }
    };

    this.init();
  }

  init() {
    this.createDOM();
    this.bindEvents();
    this.startBehaviorLoop();
  }

  createDOM() {
    // 小狗SVG
    this.element = document.createElement('div');
    this.element.className = 'creature dog';
    this.element.innerHTML = `
      <svg viewBox="0 0 100 80" class="dog-svg">
        <!-- 身体 -->
        <ellipse class="body" cx="50" cy="50" rx="30" ry="20"/>
        <!-- 头部 -->
        <circle class="head" cx="75" cy="35" r="18"/>
        <!-- 耳朵 -->
        <ellipse class="ear ear-left" cx="62" cy="22" rx="8" ry="12"/>
        <ellipse class="ear ear-right" cx="88" cy="22" rx="8" ry="12"/>
        <!-- 眼睛 -->
        <circle class="eye eye-left" cx="70" cy="32" r="4"/>
        <circle class="eye eye-right" cx="82" cy="32" r="4"/>
        <circle class="pupil" cx="71" cy="33" r="2"/>
        <circle class="pupil" cx="83" cy="33" r="2"/>
        <!-- 鼻子 -->
        <ellipse class="nose" cx="90" cy="38" rx="4" ry="3"/>
        <!-- 腿 -->
        <rect class="leg leg-fl" x="25" y="60" width="8" height="18" rx="4"/>
        <rect class="leg leg-fr" x="40" y="60" width="8" height="18" rx="4"/>
        <rect class="leg leg-bl" x="55" y="60" width="8" height="18" rx="4"/>
        <rect class="leg leg-br" x="70" y="60" width="8" height="18" rx="4"/>
        <!-- 尾巴 -->
        <path class="tail" d="M 20 50 Q 5 40 10 30" fill="none" stroke-width="6" stroke-linecap="round"/>
      </svg>
    `;
    this.container.appendChild(this.element);
  }

  bindEvents() {
    // 点击互动
    this.element.addEventListener('click', () => this.onClick());
    this.element.addEventListener('mouseenter', () => this.onHover(true));
    this.element.addEventListener('mouseleave', () => this.onHover(false));

    // 跟随鼠标
    this.container.addEventListener('mousemove', (e) => this.onMouseMove(e));
  }

  onClick() {
    this.state.action = 'react';
    this.playAnimation('jump');

    // 根据状态给予不同反应
    if (this.state.hunger > 70) {
      this.showThought('想吃零食！');
      this.state.happiness += 10;
    } else if (this.state.energy < 30) {
      this.showThought('好困...');
    } else {
      this.showThought('汪汪！');
      this.playAnimation('spin');
    }
  }

  onHover(isHovering) {
    if (isHovering) {
      this.state.attention = 100;
      this.playAnimation('earPerk');
      this.showThought('想摸摸？');
    } else {
      this.state.attention = 0;
    }
  }

  onMouseMove(e) {
    // 简化的跟随逻辑
    const rect = this.container.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const targetX = mouseX - this.state.position.x;

    if (Math.abs(targetX) > 100) {
      this.state.action = 'walk';
      this.state.velocity.x = Math.sign(targetX) * 2;
      this.element.style.transform = `scaleX(${Math.sign(targetX)})`;
    }
  }

  playAnimation(name) {
    this.element.classList.add(`anim-${name}`);
    setTimeout(() => {
      this.element.classList.remove(`anim-${name}`);
    }, 500);
  }

  showThought(text) {
    let thought = this.element.querySelector('.thought');
    if (!thought) {
      thought = document.createElement('div');
      thought.className = 'thought';
      this.element.appendChild(thought);
    }
    thought.textContent = text;
    thought.style.opacity = 1;
    setTimeout(() => { thought.style.opacity = 0; }, 2000);
  }

  startBehaviorLoop() {
    // 行为循环
    setInterval(() => {
      this.updateNeeds();
      this.decideNextAction();
      this.updateDOM();
    }, 100);

    // 随机行为
    setInterval(() => {
      if (Math.random() < 0.3) {
        this.doRandomAction();
      }
    }, 3000);
  }

  updateNeeds() {
    this.state.energy = Math.max(0, this.state.energy - 0.1);
    this.state.hunger = Math.min(100, this.state.hunger + 0.05);
  }

  decideNextAction() {
    if (this.state.action !== 'idle' && this.state.action !== 'walk') return;

    if (this.state.energy < 20) {
      this.state.action = 'sleep';
    } else if (this.state.hunger > 70) {
      this.state.action = 'beg';
      this.showThought('肚子饿了...');
    } else if (this.state.attention > 50) {
      this.state.action = 'follow';
    }
  }

  doRandomAction() {
    const actions = ['breathe', 'lookAround', 'scratch', 'shake'];
    const action = actions[Math.floor(Math.random() * actions.length)];
    this.playAnimation(action);
  }

  updateDOM() {
    this.element.style.left = `${this.state.position.x}px`;
    this.element.style.top = `${this.state.position.y}px`;
  }
}
```

### 2.2 小猫 🐱

```javascript
// creatures/Cat.js - 小猫行为系统
export class Cat {
  constructor(container) {
    this.container = container;
    this.state = {
      position: { x: 0, y: 0 },
      purr: 0,
      isPurring: false,
      mood: 'neutral',
      // 猫特有
      isCatLoaf: false,
      isStretching: false,
      tailMood: 'calm' // 'calm' | 'angry' | 'curious'
    };

    this.behaviors = {
      // 猫的待机 - 更容易进入"猫饼"姿势
      idle: {
        animations: ['clean', 'lookAround', 'catLoaf', 'slowBlink'],
        duration: [5000, 15000]
      },

      // 玩耍
      play: {
        trigger: '点击',
        animations: ['pounce', 'chase', 'attack', 'roll']
      },

      // 被摸
      pet: {
        animations: ['purr', 'knead', 'slowBlink', 'lean'],
        duration: 5000
      },

      // 高冷无视
      ignore: {
        probability: 0.3,
        animations: ['lookAway', 'tailFlick', 'cleanSelf']
      }
    };

    this.init();
  }

  // 猫咪特有的"慢眨眼"动画
  doSlowBlink() {
    const eyes = this.element.querySelectorAll('.eye');
    eyes.forEach(eye => {
      eye.style.transform = 'scaleY(0.1)'; // 闭眼
      setTimeout(() => {
        eye.style.transform = 'scaleY(1)'; // 睁眼
      }, 300);
    });
  }

  // 揉面团动作（踩奶）
  doKnead() {
    this.playAnimation('knead');
    this.state.isPurring = true;
    this.showThought('咕噜咕噜~');
  }

  // 进入猫饼姿势
  becomeCatLoaf() {
    this.state.isCatLoaf = true;
    this.element.classList.add('cat-loaf');
    this.showThought('...?');
  }
}
```

### 2.3 蝴蝶 🦋

```javascript
// creatures/Butterfly.js - 蝴蝶飞舞系统
export class Butterfly {
  constructor(container) {
    this.container = container;
    this.state = {
      position: { x: 0, y: 0 },
      // 翅膀状态
      wingAngle: 0,
      wingSpeed: 0.3,
      wingColors: ['#ff6b9d', '#c44dff', '#4d9fff'],
      // 飞行状态
      path: [],
      pathIndex: 0,
      targetX: 0,
      targetY: 0
    };

    this.init();
  }

  createButterfly() {
    // 创建蝴蝶SVG
    this.element = document.createElement('div');
    this.element.className = 'butterfly';
    this.element.innerHTML = `
      <svg viewBox="0 0 100 60">
        <!-- 左翼 -->
        <path class="wing wing-left" d="M 50 30 Q 20 5 10 30 Q 20 55 50 30" fill="${this.state.wingColors[0]}"/>
        <path class="wing-detail wing-left" d="M 45 30 Q 30 20 25 30 Q 30 40 45 30" fill="${this.state.wingColors[1]}" opacity="0.7"/>
        <!-- 右翼 -->
        <path class="wing wing-right" d="M 50 30 Q 80 5 90 30 Q 80 55 50 30" fill="${this.state.wingColors[0]}"/>
        <path class="wing-detail wing-right" d="M 55 30 Q 70 20 75 30 Q 70 40 55 30" fill="${this.state.wingColors[1]}" opacity="0.7"/>
        <!-- 身体 -->
        <ellipse cx="50" cy="30" rx="3" ry="20" fill="#333"/>
        <!-- 触角 -->
        <path d="M 48 12 Q 40 5 35 8" fill="none" stroke="#333" stroke-width="1"/>
        <path d="M 52 12 Q 60 5 65 8" fill="none" stroke="#333" stroke-width="1"/>
      </svg>
    `;
    this.container.appendChild(this.element);

    // 开始飞舞动画
    this.startFlying();
    this.startWingFlap();
  }

  startWingFlap() {
    const animate = () => {
      this.state.wingAngle = Math.sin(Date.now() * 0.02) * 45;
      this.updateWingTransform();
      requestAnimationFrame(animate);
    };
    animate();
  }

  updateWingTransform() {
    const wings = this.element.querySelectorAll('.wing');
    wings.forEach((wing, i) => {
      const direction = i === 0 ? 1 : -1;
      wing.style.transform = `rotateX(${this.state.wingAngle * direction}deg)`;
    });
  }

  startFlying() {
    // 随机路径飞行
    setInterval(() => {
      this.generateNewTarget();
      this.flyToTarget();
    }, 2000);
  }

  generateNewTarget() {
    this.state.targetX = Math.random() * (this.container.clientWidth - 50);
    this.state.targetY = Math.random() * (this.container.clientHeight - 50);
  }

  flyToTarget() {
    const dx = this.state.targetX - this.state.position.x;
    const dy = this.state.targetY - this.state.position.y;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance > 5) {
      this.state.position.x += dx * 0.02;
      this.state.position.y += dy * 0.02;
      this.state.wingSpeed = 0.4; // 飞向目标时扇翅更快

      // 翻转方向
      this.element.style.transform = `translate(${this.state.position.x}px, ${this.state.position.y}px) scaleX(${dx > 0 ? 1 : -1})`;
    } else {
      this.state.wingSpeed = 0.2; // 到达后慢下来
    }
  }

  onClick() {
    // 被点击时飞舞到随机位置
    this.state.targetX = Math.random() * this.container.clientWidth;
    this.state.targetY = Math.random() * this.container.clientHeight;
    this.flyToTarget();
    this.showSparkle();
  }

  showSparkle() {
    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle';
    sparkle.style.left = `${this.state.position.x}px`;
    sparkle.style.top = `${this.state.position.y}px`;
    this.container.appendChild(sparkle);
    setTimeout(() => sparkle.remove(), 500);
  }
}
```

### 2.4 萤火虫 ✨

```javascript
// creatures/Firefly.js - 萤火虫系统
export class FireflySystem {
  constructor(container, count = 20) {
    this.container = container;
    this.fireflies = [];

    for (let i = 0; i < count; i++) {
      this.fireflies.push(new Firefly(container));
    }
  }

  // 批量管理
  update() {
    this.fireflies.forEach(f => f.update());
  }
}

class Firefly {
  constructor(container) {
    this.container = container;
    this.state = {
      x: Math.random() * container.clientWidth,
      y: Math.random() * container.clientHeight,
      brightness: Math.random(), // 0-1 发光强度
      blinkPhase: Math.random() * Math.PI * 2
    };

    this.element = document.createElement('div');
    this.element.className = 'firefly';
    this.container.appendChild(this.element);
  }

  update() {
    // 随机漂浮
    this.state.x += (Math.random() - 0.5) * 2;
    this.state.y += (Math.random() - 0.5) * 2 - 0.5; // 稍微向上飘

    // 闪烁
    this.state.blinkPhase += 0.05;
    this.state.brightness = (Math.sin(this.state.blinkPhase) + 1) / 2;

    // 边界处理
    if (this.state.x < 0) this.state.x = this.container.clientWidth;
    if (this.state.x > this.container.clientWidth) this.state.x = 0;
    if (this.state.y < 0) this.state.y = this.container.clientHeight;
    if (this.state.y > this.container.clientHeight) this.state.y = 0;

    this.render();
  }

  render() {
    const glow = 10 + this.state.brightness * 15;
    const opacity = 0.3 + this.state.brightness * 0.7;

    this.element.style.left = `${this.state.x}px`;
    this.element.style.top = `${this.state.y}px`;
    this.element.style.boxShadow = `0 0 ${glow}px ${glow/2}px #ffffa0`;
    this.element.style.opacity = opacity;
  }
}
```

---

## 三、Vue组件版本

### 小狗 Vue 组件

```vue
<!-- components/interactive/Dog.vue -->
<template>
  <div
    class="creature dog"
    :class="[state.action, state.mood]"
    :style="positionStyle"
    @click="onClick"
    @mouseenter="onHover(true)"
    @mouseleave="onHover(false)"
  >
    <svg viewBox="0 0 100 80" class="dog-svg">
      <ellipse class="body" cx="50" cy="50" rx="30" ry="20" />
      <circle class="head" cx="75" cy="35" r="18" />
      <ellipse class="ear ear-left" cx="62" cy="22" rx="8" ry="12" :style="earStyle" />
      <ellipse class="ear ear-right" cx="88" cy="22" rx="8" ry="12" :style="earStyle" />
      <circle class="eye" cx="70" cy="32" r="4" :class="{ blink: isBlinking }" />
      <circle class="eye" cx="82" cy="32" r="4" :class="{ blink: isBlinking }" />
      <ellipse class="nose" cx="90" cy="38" rx="4" ry="3" />
      <path class="tail" d="M 20 50 Q 5 40 10 30" fill="none" stroke-width="6" :style="tailStyle" />
    </svg>

    <!-- 想法气泡 -->
    <Transition name="fade">
      <div v-if="thought" class="thought-bubble">{{ thought }}</div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'

interface CreatureState {
  position: { x: number; y: number }
  velocity: { x: number; y: number }
  action: 'idle' | 'walk' | 'run' | 'sleep' | 'react'
  mood: 'happy' | 'neutral' | 'sad'
  energy: number
  hunger: number
  tailWag: number
  earPerk: number
}

const props = defineProps<{
  container: HTMLElement
}>()

const state = reactive<CreatureState>({
  position: { x: 100, y: 100 },
  velocity: { x: 0, y: 0 },
  action: 'idle',
  mood: 'happy',
  energy: 100,
  hunger: 20,
  tailWag: 0,
  earPerk: 0
})

const thought = ref('')
const isBlinking = ref(false)

const positionStyle = computed(() => ({
  transform: `translate(${state.position.x}px, ${state.position.y}px)`
}))

const tailStyle = computed(() => ({
  transform: `rotate(${Math.sin(state.tailWag) * 30}deg)`
}))

const earStyle = computed(() => ({
  transform: `translateY(${-state.earPerk * 5}px)`
}))

// 点击互动
const onClick = () => {
  state.action = 'react'
  state.tailWag += 10
  showThought(getRandomThought())
}

// 悬停
const onHover = (isHovering: boolean) => {
  state.earPerk = isHovering ? 1 : 0
  if (isHovering) {
    showThought('想摸摸~')
  }
}

const showThought = (text: string) => {
  thought.value = text
  setTimeout(() => { thought.value = '' }, 2000)
}

const getRandomThought = () => {
  const thoughts = ['汪!', '想玩!', '好开心~', '??', '饿了...', '汪汪!']
  return thoughts[Math.floor(Math.random() * thoughts.length)]
}

// 眨眼
const doBlink = () => {
  isBlinking.value = true
  setTimeout(() => { isBlinking.value = false }, 150)
}

// 尾巴摇摆
const updateTailWag = () => {
  state.tailWag += 0.1
}

// 主循环
let animationFrame: number
const gameLoop = () => {
  // 更新尾巴
  if (state.action !== 'sleep') {
    updateTailWag()
  }

  // 更新位置
  state.position.x += state.velocity.x
  state.position.y += state.velocity.y

  // 边界检测
  if (state.position.x < 0 || state.position.x > props.container.clientWidth - 100) {
    state.velocity.x *= -1
  }

  animationFrame = requestAnimationFrame(gameLoop)
}

onMounted(() => {
  gameLoop()
  // 随机眨眼
  setInterval(doBlink, 3000 + Math.random() * 2000)
})

onUnmounted(() => {
  cancelAnimationFrame(animationFrame)
})
</script>

<style scoped>
.creature {
  position: absolute;
  cursor: pointer;
  transition: transform 0.1s;
}

.dog {
  width: 100px;
  height: 80px;
}

.dog:hover .head {
  transform: translateY(-2px);
}

.dog .tail {
  transform-origin: 20px 50px;
  transition: transform 0.1s;
}

@keyframes blink {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(0.1); }
}

.blink {
  animation: blink 0.15s ease-in-out;
}

.thought-bubble {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.thought-bubble::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: white;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

---

## 四、植物行为系统 🌱

### 会动的植物

```javascript
// creatures/Plant.js - 植物交互系统
export class InteractivePlant {
  constructor(container) {
    this.container = container;
    this.state = {
      growth: 0,           // 生长阶段 0-100
      health: 100,          // 健康度
      isWilted: false,      // 是否枯萎
      swayAmount: 0,        // 摇摆幅度
      // 互动状态
      beingTouched: false,
      lastTouchTime: 0
    };

    this.createPlant();
    this.startBehavior();
  }

  createPlant() {
    this.element = document.createElement('div');
    this.element.className = 'interactive-plant';
    this.element.innerHTML = `
      <svg viewBox="0 0 100 150">
        <!-- 花盆 -->
        <path class="pot" d="M 30 130 L 35 100 L 65 100 L 70 130 Z" fill="#8B4513"/>
        <!-- 茎 -->
        <path class="stem" d="M 50 100 Q 45 70 50 40" fill="none" stroke="#228B22" stroke-width="4"/>
        <!-- 叶子 -->
        <g class="leaves">
          <ellipse class="leaf leaf-left" cx="35" cy="70" rx="15" ry="8" fill="#32CD32" transform="rotate(-30 35 70)"/>
          <ellipse class="leaf leaf-right" cx="65" cy="70" rx="15" ry="8" fill="#32CD32" transform="rotate(30 65 70)"/>
          <ellipse class="leaf leaf-top" cx="50" cy="40" rx="12" ry="20" fill="#FF69B4"/>
        </g>
      </svg>
    `;

    this.element.addEventListener('click', () => this.onClick());
    this.element.addEventListener('mouseenter', () => this.onHover(true));
    this.element.addEventListener('mouseleave', () => this.onHover(false));

    this.container.appendChild(this.element);
  }

  onClick() {
    // 点击会让植物开心
    this.state.health = Math.min(100, this.state.health + 10);
    this.state.isWilted = false;
    this.playAnimation('bounce');
    this.showMessage('谢谢你的关爱~');
  }

  onHover(isHovering) {
    this.state.beingTouched = isHovering;
    if (isHovering) {
      this.playAnimation('sway');
      this.showMessage('摸摸我...');
    }
  }

  startBehavior() {
    // 日常摇摆
    setInterval(() => {
      if (!this.state.beingTouched) {
        this.state.swayAmount = Math.sin(Date.now() * 0.001) * 5;
        this.updatePlantAppearance();
      }
    }, 50);

    // 逐渐枯萎/恢复
    setInterval(() => {
      if (this.state.beingTouched) {
        this.state.health = Math.min(100, this.state.health + 1);
      } else {
        this.state.health = Math.max(0, this.state.health - 0.1);
      }
      this.updatePlantAppearance();
    }, 1000);
  }

  updatePlantAppearance() {
    const stem = this.element.querySelector('.stem');
    const leaves = this.element.querySelector('.leaves');

    // 根据健康度调整颜色
    const hue = 80 + (this.state.health / 100) * 40; // 绿色到枯黄
    stem.style.stroke = `hsl(${hue}, 70%, 45%)`;
    leaves.style.opacity = this.state.health / 100;

    // 摇摆
    leaves.style.transform = `rotate(${this.state.swayAmount}deg)`;
    leaves.style.transformOrigin = '50px 100px';
  }
}
```

---

## 五、咨询与自主创新机制

### 当用户输入不明确时的处理

```
当用户输入模糊或缺少关键信息时，主动询问：

1. 识别模糊输入：
   - "画个小动物" → 需要确定物种
   - "画个会动的" → 需要确定什么类型的互动
   - "画个好看的" → 需要确定风格/情绪

2. 提供选择菜单：
   ```
   检测到：画个小动物

   请选择动物类型：
   🐕 温顺型：狗、兔子、猫
   🦅 活泼型：鸟、蝴蝶、松鼠
   🐙 神秘型：鱼、水母、章鱼
   🌱 植物型：会动的花、捕蝇草、藤蔓

   或者描述你想要的动物特征，我来帮你创造！
   ```

3. 自主创新机制：
   当用户提供极简描述时，AI主动添加特色：

   输入："画个星星"
   自动生成：
   - 🌟 眨眼闪烁的星星
   - ✨ 点击会爆发星尘
   - 🎵 背景有微妙的声音可视化
   - 💫 星星之间有引力交互

4. 增强型提示词生成：
   ```
   基于"星星"，我生成以下增强方案：

   核心元素：
   - 100颗程序化生成的星星
   - 每颗有独立闪烁节奏

   交互设计：
   - 鼠标靠近：星星发光增强
   - 点击星星：爆发粒子效果
   - 拖拽星星：创造流星轨迹

   情绪基调：
   - 宁静、梦幻、治愈

   技术选择：
   - Canvas粒子系统
   - GSAP动画
   - CSS混合模式发光
   ```
```

---

## 六、完整项目结构模板

```
interactive-creatures/
├── index.html
├── src/
│   ├── main.ts              # Vue应用入口
│   ├── creatures/
│   │   ├── BaseCreature.ts  # 生物基类
│   │   ├── Dog.vue          # 小狗组件
│   │   ├── Cat.vue          # 小猫组件
│   │   ├── Butterfly.vue    # 蝴蝶组件
│   │   ├── Plant.vue        # 植物组件
│   │   └── behaviors/       # 行为系统
│   │       ├── StateMachine.ts
│   │       ├── AI.ts
│   │       └── Animations.ts
│   ├── effects/
│   │   ├── Particles.ts
│   │   └── Glow.ts
│   └── stores/
│       └── creatures.ts    # Pinia状态管理
├── style.css
└── package.json
```

---

## 七、核心交互设计原则

1. **即时反馈**：每个交互都需要视觉/听觉反馈
2. **记忆感**：记住用户之前的互动
3. **生命迹象**：呼吸、眨眼、随机小动作
4. **情绪传染**：用户情绪影响生物状态
5. **惊喜元素**：随机出现的特殊行为
