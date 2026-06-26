# 手势控制生成器

生成手势控制交互场景的 Claude Code 技能。询问用户想要控制什么，然后输出一个完整的 HTML 文件，支持鼠标/手势双模式输入。

## 功能特点

- 🎯 **鼠标/手势双模式** - 自动切换，摄像头不可用时降级到纯鼠标控制
- 🎨 **丰富的视觉效果** - 粒子、蝴蝶、水波纹等多种预设效果
- 📱 **响应式设计** - 支持桌面和移动设备
- ⚡ **高性能** - Three.js 渲染引擎，支持数万个物体
- 🔧 **易于扩展** - 简单的类接口，轻松创建自定义效果

## 项目结构

```
gesture-control-generator/
├── SKILL.md              # 技能定义文件
├── assets/               # 资源文件
│   ├── gesture-scene.js  # 核心框架 (Three.js版本)
│   └── template.html     # HTML 模板
├── references/           # 参考示例
│   ├── particles.html    # 粒子拖尾
│   ├── butterfly.html    # 蝴蝶飞舞
│   └── ripple.html       # 水波纹
├── scripts/              # 脚本文件
├── tests/                # 测试报告
└── index.html            # 示例列表页
```

## 技术栈

- **Three.js** - 3D 渲染引擎，用于高性能图形渲染
- **MediaPipe** - Google 的手势识别库（可选）
- **GestureScene** - 核心框架，处理输入和场景管理

## 快速开始

### 1. 安装技能

将此目录软链接到 Claude Code 技能目录：

```bash
# Claude Code
ln -s /path/to/gesture-control-generator ~/.claude/skills/gesture-control-generator

# OpenCode
ln -s /path/to/gesture-control-generator ~/.opencode/skills/gesture-control-generator
```

### 2. 使用技能

在 Claude Code 中，直接描述你想要的手势控制效果：

```
我想做一个星星闪烁的手势控制效果
```

或者：

```
生成一个烟花绽放的手势控制场景
```

### 3. 打开效果

生成的 HTML 文件可以直接在浏览器中打开，支持：
- 鼠标移动控制物体生成
- 鼠标按下触发爆发效果
- 点击右上角按钮开启摄像头手势控制

## 示例效果

打开 `index.html` 查看所有示例，或直接访问：

| 效果 | 文件 | 描述 |
|------|------|------|
| ✨ 粒子拖尾 | `references/particles.html` | 经典粒子效果，彩色拖尾 |
| 🦋 蝴蝶飞舞 | `references/butterfly.html` | 翅膀扇动，随机飞舞 |
| 💧 水波纹 | `references/ripple.html` | 涟漪扩散，多层叠加 |

## 创建自定义效果

### 物体类接口

每个物体类需要实现以下方法：

```javascript
class MyObject {
  constructor(x, y, vx, vy) {
    // x, y: 生成位置（来自手指/鼠标）
    // vx, vy: 初始速度（来自移动方向）
    
    // 创建 Three.js 几何体和材质
    const geometry = new THREE.SphereGeometry(size, 16, 16);
    const material = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(hue, saturation, lightness),
      transparent: true,
      opacity: 1.0,
    });
    
    // 创建网格
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.position.set(x, y, 0);
  }
  
  update() {
    // 更新位置、状态（每帧调用）
    this.mesh.position.x += this.vx;
    this.mesh.position.y += this.vy;
    
    // 更新透明度
    this.alpha -= fadeRate;
    this.mesh.material.opacity = Math.max(this.alpha, 0);
  }
  
  isDead() {
    // 返回 true 表示物体应该被移除
    return this.alpha <= 0;
  }
}
```

### 场景配置

```javascript
const scene = new GestureScene({
  title: '我的效果 · 手势控制',
  create: (x, y, vx, vy) => new MyObject(x, y, vx, vy),
  spawnRate: 2,      // 每帧生成数量 (1-5)
  burstRate: 8,      // 爆发数量 (3-15)
  maxObjects: 500,   // 物体上限 (100-5000)
  background: [0.86, 0.2, 0.02],  // 背景色 [r, g, b] (0-1范围)
  handVelocityScale: 1.5,        // 手势速度缩放
});
```

### 配置指南

| 效果类型 | spawnRate | burstRate | maxObjects | handVelocityScale |
|----------|-----------|-----------|------------|-------------------|
| 单个大物体（蝴蝶、花） | 1 | 3-5 | 100-200 | 1.0-1.5 |
| 中等密度（萤火虫、雪花） | 2-3 | 5-8 | 300-500 | 1.2-1.8 |
| 高密度（粒子、雨滴） | 3-5 | 10-15 | 1000-4000 | 1.5-2.0 |
| 波纹类（水波纹、声波） | 1 | 2-3 | 50-100 | 0.8-1.2 |

**手势模式参数：** `handSpawnRate`(默认2) 控制手势每帧生成数，`handBurstSpeed`(默认15) 控制爆发触发阈值。

## 常见效果示例

### 星星闪烁

```javascript
class Star {
  constructor(x, y, vx, vy) {
    this.vx = vx * 0.3 + (Math.random() - 0.5);
    this.vy = vy * 0.3 + (Math.random() - 0.5);
    this.size = 3 + Math.random() * 5;
    this.hue = 40 + Math.random() * 20; // 金黄色
    this.alpha = 1.0;
    this.fade = 0.005 + Math.random() * 0.01;
    
    // 创建星形几何体
    const shape = new THREE.Shape();
    // ... 定义星形顶点
    const geometry = new THREE.ShapeGeometry(shape);
    const material = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(this.hue / 360, 0.8, 0.8),
      transparent: true,
      opacity: this.alpha,
    });
    
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.position.set(x, y, 0);
  }
  // ... update(), isDead()
}
```

### 烟花绽放

```javascript
class Firework {
  constructor(x, y, vx, vy) {
    this.phase = 'rise'; // 上升阶段
    this.vy = -(3 + Math.random() * 3); // 向上
    this.explosionParticles = [];
    
    // 创建头部
    const geometry = new THREE.SphereGeometry(2.5, 8, 8);
    const material = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(Math.random(), 0.8, 1),
      transparent: true,
      opacity: 1.0,
    });
    
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.position.set(x, y, 0);
  }
  // 上升 → 爆炸 → 粒子扩散
}
```

## 降级模式

当摄像头不可用或用户拒绝授权时，GestureScene 自动降级到纯鼠标模式：

- 显示"鼠标控制中（摄像头不可用）"
- 鼠标移动生成物体，按住鼠标触发爆发
- 所有视觉效果正常工作，仅缺少手势控制

## 性能调优

| 设备类型 | maxObjects | spawnRate | burstRate |
|----------|------------|-----------|-----------|
| 高端 PC | 3000-5000 | 3-5 | 10-15 |
| 中端笔记本 | 1000-2000 | 2-3 | 8-10 |
| 低端设备 | 300-800 | 1-2 | 5-8 |
| 移动浏览器 | 200-500 | 1-2 | 3-5 |

## 许可证

MIT License