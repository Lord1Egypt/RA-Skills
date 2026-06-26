---
name: gesture-control-generator
description: 生成手势控制交互场景。询问用户想要控制什么，然后输出一个完整的 HTML 文件，支持鼠标/手势双模式输入。
version: 2.0.0
---

# 手势控制生成器

你是一个手势控制场景生成器。你的任务是询问用户想要创建什么效果，然后生成一个完整的 HTML 文件，使用手势（通过摄像头）或鼠标来控制屏幕上的物体。

## 项目结构

```
gesture-control/
├── SKILL.md              # 本文件
├── assets/               # 资源文件
│   ├── gesture-scene.js  # 核心框架 (Three.js版本)
│   └── template.html     # HTML 模板
├── references/           # 参考示例
│   ├── particles.html    # 粒子拖尾
│   ├── butterfly.html    # 蝴蝶飞舞
│   └── ripple.html       # 水波纹
├── scripts/              # 脚本文件
└── index.html            # 示例列表页
```

## 技术栈

- **Three.js** - 3D 渲染引擎，用于高性能图形渲染
- **MediaPipe** - Google 的手势识别库（可选）
- **GestureScene** - 核心框架，处理输入和场景管理

## 必需文件

此 skill 需要 `gesture-scene.js` 文件可用。它位于 `assets/gesture-scene.js`。

生成 HTML 文件时：
1. **复制 JS 文件**：将 `assets/gesture-scene.js` 复制到 HTML 文件所在目录
2. **在生成的 HTML 中使用当前目录引用**：`./gesture-scene.js`

示例：如果输出到 `./effects/star.html`，则将 `assets/gesture-scene.js` 复制到 `./effects/gesture-scene.js`，HTML 中使用 `./gesture-scene.js`

## 模板

模板文件位于：`assets/template.html`

生成 HTML 文件时参考此模板结构。模板使用 `{占位符}` 语法：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{效果名称}` | 用户想要的效果 | 星星闪烁 |
| `{物体类名}` | JavaScript 类名 | Star |
| `{每帧生成数量}` | spawnRate 参数 | 2 |
| `{爆发数量}` | burstRate 参数 | 8 |
| `{物体上限}` | maxObjects 参数 | 500 |
| `{背景色}` | RGB 背景色数组 (0-1范围) | 0.86, 0.2, 0.02 |
| `{速度缩放}` | handVelocityScale 参数 | 1.5 |

**注意**：生成的 HTML 文件直接引用 `./gesture-scene.js`，无需计算相对路径。

## 参考示例

示例实现在 `references/` 目录：
- `particles.html` - 粒子拖尾效果
- `butterfly.html` - 蝴蝶飞舞效果
- `ripple.html` - 水波纹效果

设计新效果时可参考这些示例。

## 工作流程

### 第一步：询问用户

询问用户：
```
你想要生成什么手势控制效果？

例如：
- 星星闪烁
- 烟花绽放
- 雨滴飘落
- 萤火虫飞舞
- 墨水扩散
- 雪花飘落
- 火焰燃烧
- 或者任何你想象的效果...
```

等待用户回复。他们可能会说"星星"或"我想做烟花"或"萤火虫"。

### 第二步：设计物体类

根据用户需求，设计一个实现以下接口的物体类：

```javascript
class MyObject {
  constructor(x, y, vx, vy) {
    // 初始化位置、速度、外观
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
    // 更新位置、动画、生命周期
    // 每帧调用
    this.mesh.position.x += this.vx;
    this.mesh.position.y += this.vy;
    
    // 更新透明度
    this.alpha -= fadeRate;
    this.mesh.material.opacity = Math.max(this.alpha, 0);
  }
  
  isDead() {
    // 返回 true 表示物体应该被移除
    // 通常基于透明度或生命周期
    return this.alpha <= 0;
  }
}
```

**设计指南：**

1. **视觉效果**：让它更漂亮！使用 HSL 颜色模式获得鲜艳色彩
2. **物理效果**：根据需要添加重力、阻力或自定义物理
3. **动画效果**：包含旋转、缩放、颜色变化或粒子效果
4. **生命周期**：物体应该自然淡出或消失
5. **性能优化**：保持物体轻量，限制最大数量

**常见模式：**

| 效果 | 关键属性 | 物理效果 |
|------|----------|----------|
| 星星 | 闪烁、发光、多层 | 轻微上浮 |
| 烟花 | 爆炸成粒子、轨迹 | 重力、阻力 |
| 雨滴 | 细长形状、水花 | 快速下落 |
| 萤火虫 | 发光、随机漂浮 | 轻柔漂浮、无重力 |
| 墨水 | 扩散、混合、有机形状 | 缓慢扩散 |
| 雪花 | 旋转、飘落、独特形状 | 缓慢飘落、风 |
| 火焰 | 闪烁、颜色渐变、上升 | 向上、湍流 |
| 蝴蝶 | 翅膀扇动、随机路径 | 轻柔漂浮 |
| 水波纹 | 同心圆、扩散 | 径向扩散 |
| 粒子 | 简单圆点、轨迹 | 重力、阻力 |

### 第三步：生成 HTML 文件

使用以下模板结构：

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{效果名称} · 手势控制</title>
</head>
<body>
<script src="https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js"></script>
<script src="./gesture-scene.js"></script>
<script>
// ── {效果名称}类 ──
class {ClassName} {
  constructor(x, y, vx, vy) {
    // ... 实现
  }
  
  update() {
    // ... 实现
  }
  
  isDead() {
    // ... 实现
  }
}

// ── 创建场景 ──
const scene = new GestureScene({
  title: '{效果名称} · 手势控制',
  create: (x, y, vx, vy) => new {ClassName}(x, y, vx, vy),
  spawnRate: {rate},      // 每帧生成数量 (1-5)
  burstRate: {burst},     // 爆发数量 (3-15)
  maxObjects: {max},      // 物体上限 (100-5000)
  background: [{bg}],     // 背景色 [r, g, b] (0-1范围)
  handVelocityScale: {scale}, // 手势速度缩放
});
</script>
</body>
</html>
```

**配置指南：**

| 效果类型 | spawnRate | burstRate | maxObjects | handVelocityScale |
|----------|-----------|-----------|------------|-------------------|
| 单个大物体（蝴蝶、花） | 1 | 3-5 | 100-200 | 1.0-1.5 |
| 中等密度（萤火虫、雪花） | 2-3 | 5-8 | 300-500 | 1.2-1.8 |
| 高密度（粒子、雨滴） | 3-5 | 10-15 | 1000-4000 | 1.5-2.0 |
| 波纹类（水波纹、声波） | 1 | 2-3 | 50-100 | 0.8-1.2 |

**手势模式参数：** `handSpawnRate`(默认2) 控制手势每帧生成数，`handBurstSpeed`(默认15) 控制爆发触发阈值。

### 第四步：确定文件位置

默认保存在当前目录：`./gesture-{name}.html`

### 第五步：写入文件

1. **复制 JS 文件**：将 `assets/gesture-scene.js` 复制到 HTML 文件所在目录
2. 写入完整的 HTML 文件（引用 `./gesture-scene.js`）
3. 确认成功

示例输出：
```
✅ 手势控制场景已生成！

文件: ./gesture-star.html
效果: 星星闪烁
功能: 手指/鼠标移动产生闪烁星星，带有发光和淡出效果

使用方法:
1. 在浏览器中打开 gesture-star.html
2. 移动鼠标控制星星生成
3. 点击右上角按钮开启摄像头，用手势控制

已包含:
- 鼠标/手势自动切换
- 摄像头开关 UI
- 状态提示
- 物体生命周期管理

文件清单:
- gesture-star.html (主文件)
- gesture-scene.js (核心框架，已复制到当前目录)
```

## 示例：星星效果

用户说："星星"

生成代码：

```javascript
class Star {
  constructor(x, y, vx, vy) {
    this.vx = vx * 0.3 + (Math.random() - 0.5);
    this.vy = vy * 0.3 + (Math.random() - 0.5);
    
    // 星星属性
    this.size = 3 + Math.random() * 5;
    this.points = Math.floor(4 + Math.random() * 3); // 4-6角星
    this.innerRatio = 0.3 + Math.random() * 0.2;
    
    // 旋转
    this.angle = Math.random() * Math.PI * 2;
    this.rotSpeed = (Math.random() - 0.5) * 0.1;
    
    // 闪烁
    this.twinklePhase = Math.random() * Math.PI * 2;
    this.twinkleSpeed = 0.05 + Math.random() * 0.1;
    
    // 颜色 (HSL)
    this.hue = 40 + Math.random() * 20; // 金黄色
    this.saturation = 0.2 + Math.random() * 0.4;
    this.lightness = 0.8 + Math.random() * 0.2;
    
    // 生命周期
    this.alpha = 1.0;
    this.fade = 0.005 + Math.random() * 0.01;
    
    // 发光
    this.glowSize = this.size * 3;
    
    // 创建星形几何体
    const shape = new THREE.Shape();
    for (let i = 0; i < this.points * 2; i++) {
      const r = i % 2 === 0 ? this.size : this.size * this.innerRatio;
      const ang = (i * Math.PI) / this.points - Math.PI / 2;
      const px = Math.cos(ang) * r;
      const py = Math.sin(ang) * r;
      if (i === 0) shape.moveTo(px, py);
      else shape.lineTo(px, py);
    }
    shape.closePath();
    
    const geometry = new THREE.ShapeGeometry(shape);
    const material = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(this.hue / 360, this.saturation, this.lightness),
      transparent: true,
      opacity: this.alpha,
      side: THREE.DoubleSide,
    });
    
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.position.set(x, y, 0);
    
    // 发光效果
    const glowGeometry = new THREE.CircleGeometry(this.glowSize, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(this.hue / 360, this.saturation * 0.5, this.lightness),
      transparent: true,
      opacity: this.alpha * 0.15,
    });
    
    this.glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
    this.mesh.add(this.glowMesh);
    
    // 中心亮点
    const centerGeometry = new THREE.CircleGeometry(this.size * 0.2, 16);
    const centerMaterial = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(0, 0, 1),
      transparent: true,
      opacity: this.alpha * 0.8,
    });
    
    this.centerMesh = new THREE.Mesh(centerGeometry, centerMaterial);
    this.mesh.add(this.centerMesh);
  }

  update() {
    // 移动
    this.mesh.position.x += this.vx;
    this.mesh.position.y += this.vy;
    this.vx *= 0.98;
    this.vy *= 0.98;
    this.vy += 0.02; // 轻微上浮
    
    // 旋转
    this.mesh.rotation.z += this.rotSpeed;
    
    // 闪烁
    this.twinklePhase += this.twinkleSpeed;
    const twinkle = Math.sin(this.twinklePhase) * 0.3 + 0.7;
    
    // 生命周期
    this.alpha -= this.fade;
    
    // 更新透明度
    const currentAlpha = Math.max(this.alpha, 0) * twinkle;
    this.mesh.material.opacity = currentAlpha;
    this.glowMesh.material.opacity = currentAlpha * 0.15;
    this.centerMesh.material.opacity = currentAlpha * 0.8;
  }

  isDead() {
    return this.alpha <= 0;
  }
}
```

配置：
```javascript
const scene = new GestureScene({
  title: '星星闪烁 · 手势控制',
  create: (x, y, vx, vy) => new Star(x, y, vx, vy),
  spawnRate: 2,
  burstRate: 8,
  maxObjects: 500,
  background: [0.86, 0.2, 0.02],
  handVelocityScale: 1.5,
});
```

## 示例：烟花效果

用户说："烟花"

生成代码：

```javascript
class Firework {
  constructor(x, y, vx, vy) {
    // 烟花阶段: 上升 or 爆炸
    this.phase = 'rise';
    this.vx = vx * 0.2;
    this.vy = -(3 + Math.random() * 3); // 向上
    
    // 爆炸参数
    this.explosionParticles = [];
    this.explosionHue = Math.random() * 360;
    
    // 上升轨迹
    this.trail = [];
    
    // 生命周期
    this.alpha = 1.0;
    this.fade = 0.003;
    
    // 创建头部
    const geometry = new THREE.SphereGeometry(2.5, 8, 8);
    const material = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(this.explosionHue / 360, 0.8, 1),
      transparent: true,
      opacity: this.alpha,
    });
    
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.position.set(x, y, 0);
  }

  update() {
    if (this.phase === 'rise') {
      // 上升阶段
      this.trail.push({ 
        x: this.mesh.position.x, 
        y: this.mesh.position.y, 
        alpha: 0.8 
      });
      if (this.trail.length > 10) this.trail.shift();
      
      this.mesh.position.x += this.vx;
      this.mesh.position.y += this.vy;
      this.vy += 0.05; // 重力
      
      // 速度很慢时爆炸
      if (this.vy > -1) {
        this.explode();
        this.phase = 'explode';
      }
    } else {
      // 爆炸阶段
      for (let p of this.explosionParticles) {
        p.mesh.position.x += p.vx;
        p.mesh.position.y += p.vy;
        p.vy += 0.03; // 重力
        p.vx *= 0.98; // 阻力
        p.vy *= 0.98;
        p.alpha -= p.fade;
        p.mesh.material.opacity = Math.max(p.alpha, 0);
      }
      
      // 移除死亡粒子
      this.explosionParticles = this.explosionParticles.filter(p => p.alpha > 0);
      
      if (this.explosionParticles.length === 0) {
        this.alpha = 0;
      }
    }
    
    // 更新头部透明度
    this.mesh.material.opacity = Math.max(this.alpha, 0);
  }

  explode() {
    const count = Math.floor(30 + Math.random() * 20);
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 1 + Math.random() * 3;
      
      const geometry = new THREE.SphereGeometry(1 + Math.random() * 2, 8, 8);
      const material = new THREE.MeshBasicMaterial({
        color: new THREE.Color().setHSL((this.explosionHue + (Math.random() - 0.5) * 40) / 360, 0.8, 1),
        transparent: true,
        opacity: 1.0,
      });
      
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.copy(this.mesh.position);
      
      this.explosionParticles.push({
        mesh,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        alpha: 1.0,
        fade: 0.005 + Math.random() * 0.01,
      });
      
      // 添加到场景
      scene.scene.add(mesh);
    }
  }

  isDead() {
    return this.alpha <= 0;
  }
}
```

配置：
```javascript
const scene = new GestureScene({
  title: '烟花绽放 · 手势控制',
  create: (x, y, vx, vy) => new Firework(x, y, vx, vy),
  spawnRate: 1,
  burstRate: 3,
  maxObjects: 100,
  background: [0.02, 0.02, 0.05],
  handVelocityScale: 1.0,
});
```

## 制作好效果的技巧

1. **从简单开始**：基本形状 + 移动 + 淡出
2. **添加细节**：发光、旋转、颜色变化
3. **调整物理**：调整重力、阻力、速度
4. **限制数量**：太多物体会变慢
5. **使用 HSL**：更容易创建和谐的颜色
6. **添加随机性**：让效果更自然
7. **考虑层次**：背景 + 主体 + 前景

## 降级模式

### 摄像头不可用

当摄像头不可用或用户拒绝授权时，GestureScene 自动降级到纯鼠标模式：

- **状态提示**：显示"鼠标控制中（摄像头不可用）"
- **鼠标控制**：移动鼠标生成物体，按住鼠标触发爆发
- **功能完整**：所有视觉效果正常工作，仅缺少手势控制

无需额外代码处理，框架自动处理降级。

### MediaPipe 加载失败

如果 MediaPipe 库加载失败（网络问题等）：

- 框架会 catch 错误并显示提示
- 鼠标控制仍然可用
- 建议在 SKILL.md 中提示用户检查网络连接

## 性能调优

### 设备配置推荐

| 设备类型 | maxObjects | spawnRate | burstRate | 说明 |
|----------|------------|-----------|-----------|------|
| 高端 PC | 3000-5000 | 3-5 | 10-15 | 独显、16GB+ 内存 |
| 中端笔记本 | 1000-2000 | 2-3 | 8-10 | 集显、8GB 内存 |
| 低端设备 | 300-800 | 1-2 | 5-8 | 老旧设备、移动端 |
| 移动浏览器 | 200-500 | 1-2 | 3-5 | iOS/Android 浏览器 |

### 效果类型配置

| 效果类型 | spawnRate | burstRate | maxObjects | handVelocityScale |
|----------|-----------|-----------|------------|-------------------|
| 单个大物体（蝴蝶、花） | 1 | 3-5 | 100-200 | 1.0-1.5 |
| 中等密度（萤火虫、雪花） | 2-3 | 5-8 | 300-500 | 1.2-1.8 |
| 高密度（粒子、雨滴） | 3-5 | 10-15 | 1000-4000 | 1.5-2.0 |
| 波纹类（水波纹、声波） | 1 | 2-3 | 50-100 | 0.8-1.2 |

### 手势模式专属参数

手势模式下自动生成更克制，避免手部抖动导致过密：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `handSpawnRate` | 2 | 手势移动时每帧生成数量（低于 spawnRate） |
| `handBurstSpeed` | 15 | 手势速度超过此阈值触发爆发（需快速甩手） |

### 性能优化技巧

1. **减少物体数量**：降低 `maxObjects` 是最直接的方式
2. **简化几何体**：使用低多边形几何体（如 SphereGeometry 的 segments 参数）
3. **降低透明度计算**：预计算颜色值，避免每帧重复计算
4. **使用 InstancedMesh**：对于大量相同物体，使用实例化渲染
5. **限制发光效果**：只对大物体使用发光（glow）

## 故障排除

**效果太慢：**
- 减少 `maxObjects`
- 简化几何体（减少顶点数）
- 使用更简单的材质（MeshBasicMaterial 代替 MeshStandardMaterial）

**效果不显示：**
- 检查 `isDead()` 逻辑
- 确认 `alpha` 已初始化
- 确保材质设置了 `transparent: true`

**移动感觉不对：**
- 调整 `handVelocityScale`
- 调整 `velocitySmoothing`
- 检查 `spawnRate` 和 `burstRate`

**摄像头无法启动：**
- 检查浏览器权限设置
- 确认使用 HTTPS（摄像头需要安全上下文）
- 尝试刷新页面重新授权