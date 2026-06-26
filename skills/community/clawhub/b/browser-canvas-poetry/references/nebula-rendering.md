---
title: Nebula Rendering Guide
description: 星云/星团渲染技术专项指南
tags: [nebula, rendering, WebGL, Three.js, shaders, particle-effects]
---

## 星云渲染专项技术指南

星云是浏览器原生艺术中最具挑战性的主题之一。本文档提供从基础到高级的完整技术方案。

---

## 一、技术选型对比

| 技术方案 | 难度 | 性能 | 效果质量 | 推荐场景 |
|---------|------|------|----------|---------|
| CSS多层渐变 | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | 背景装饰、简单星云 |
| Canvas粒子系统 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 中等复杂度星云 |
| **Three.js ShaderMaterial** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 高级星云、实时渲染 |
| WebGL Raymarching | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | 照片级星云 |
| 外接库(gsap/particles.js) | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 快速原型 |

---

## 二、推荐方案：Three.js + ShaderMaterial

### 基础星云模板

```javascript
// 引入Three.js
// <script type="importmap">
//   { "imports": { "three": "https://unpkg.com/three@0.160.0/build/three.module.js" }}
// </script>

import * as THREE from 'three';

class NebulaScene {
  constructor(container) {
    this.container = container;
    this.init();
    this.createNebula();
    this.animate();
  }

  init() {
    // 场景设置
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.container.appendChild(this.renderer.domElement);

    this.camera.position.z = 50;
  }

  createNebula() {
    // 自定义着色器材质
    const nebulaMaterial = new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        color1: { value: new THREE.Color(0x1a0a2e) },  // 深紫
        color2: { value: new THREE.Color(0xff6b9d) },  // 粉红
        color3: { value: new THREE.Color(0xc44dff) },  // 亮紫
      },
      vertexShader: `
        varying vec2 vUv;
        varying vec3 vPosition;
        void main() {
          vUv = uv;
          vPosition = position;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform float time;
        uniform vec3 color1;
        uniform vec3 color2;
        uniform vec3 color3;
        varying vec2 vUv;
        varying vec3 vPosition;

        // Simplex 3D Noise
        vec4 permute(vec4 x) { return mod(((x*34.0)+1.0)*x, 289.0); }
        vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

        float snoise(vec3 v) {
          const vec2 C = vec2(1.0/6.0, 1.0/3.0);
          const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
          vec3 i  = floor(v + dot(v, C.yyy));
          vec3 x0 = v - i + dot(i, C.xxx);
          vec3 g = step(x0.yzx, x0.xyz);
          vec3 l = 1.0 - g;
          vec3 i1 = min(g.xyz, l.zxy);
          vec3 i2 = max(g.xyz, l.zxy);
          vec3 x1 = x0 - i1 + C.xxx;
          vec3 x2 = x0 - i2 + C.yyy;
          vec3 x3 = x0 - D.yyy;
          i = mod(i, 289.0);
          vec4 p = permute(permute(permute(
            i.z + vec4(0.0, i1.z, i2.z, 1.0))
            + i.y + vec4(0.0, i1.y, i2.y, 1.0))
            + i.x + vec4(0.0, i1.x, i2.x, 1.0));
          float n_ = 1.0/7.0;
          vec3 ns = n_ * D.wyz - D.xzx;
          vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
          vec4 x_ = floor(j * ns.z);
          vec4 y_ = floor(j - 7.0 * x_);
          vec4 x = x_ *ns.x + ns.yyyy;
          vec4 y = y_ *ns.x + ns.yyyy;
          vec4 h = 1.0 - abs(x) - abs(y);
          vec4 b0 = vec4(x.xy, y.xy);
          vec4 b1 = vec4(x.zw, y.zw);
          vec4 s0 = floor(b0)*2.0 + 1.0;
          vec4 s1 = floor(b1)*2.0 + 1.0;
          vec4 sh = -step(h, vec4(0.0));
          vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy;
          vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww;
          vec3 p0 = vec3(a0.xy, h.x);
          vec3 p1 = vec3(a0.zw, h.y);
          vec3 p2 = vec3(a1.xy, h.z);
          vec3 p3 = vec3(a1.zw, h.w);
          vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
          p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
          vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
          m = m * m;
          return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
        }

        // FBM (Fractal Brownian Motion)
        float fbm(vec3 p) {
          float value = 0.0;
          float amplitude = 0.5;
          float frequency = 1.0;
          for (int i = 0; i < 6; i++) {
            value += amplitude * snoise(p * frequency);
            amplitude *= 0.5;
            frequency *= 2.0;
          }
          return value;
        }

        void main() {
          vec3 pos = vPosition * 0.05;

          // 基础噪声
          float n = fbm(pos + time * 0.1);

          // 多层噪声叠加
          float nebula = fbm(pos * 2.0 + n);
          nebula = smoothstep(-0.2, 0.8, nebula);

          // 颜色渐变
          vec3 color = mix(color1, color2, nebula);
          color = mix(color, color3, sin(nebula * 3.14159) * 0.5 + 0.5);

          // 边缘淡化
          float edge = length(vUv - 0.5) * 2.0;
          float alpha = nebula * smoothstep(1.5, 0.5, edge);

          // 添加发光效果
          color += color3 * pow(nebula, 3.0) * 0.5;

          gl_FragColor = vec4(color, alpha * 0.8);
        }
      `,
      transparent: true,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    // 创建几何体
    const geometry = new THREE.PlaneGeometry(100, 100, 64, 64);
    this.nebulaMesh = new THREE.Mesh(geometry, nebulaMaterial);
    this.scene.add(this.nebulaMesh);
  }

  animate() {
    const animate = () => {
      requestAnimationFrame(animate);

      // 更新时间uniform
      this.nebulaMesh.material.uniforms.time.value += 0.01;

      this.renderer.render(this.scene, this.camera);
    };
    animate();
  }
}

// 使用
const container = document.getElementById('canvas-container');
new NebulaScene(container);
```

---

## 三、WebGL Raymarching 高级方案

### 体积渲染星云

```javascript
// 纯WebGL实现（无需Three.js）
class RaymarchingNebula {
  constructor(canvas) {
    this.canvas = canvas;
    this.gl = canvas.getContext('webgl');
    this.init();
  }

  init() {
    const gl = this.gl;

    // 顶点着色器
    const vsSource = `
      attribute vec2 position;
      void main() {
        gl_Position = vec4(position, 0.0, 1.0);
      }
    `;

    // 片段着色器 - Raymarching核心
    const fsSource = `
      precision highp float;

      uniform vec2 resolution;
      uniform float time;

      // 随机函数
      float random(vec2 st) {
        return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
      }

      // 值噪声
      float noise(vec3 p) {
        vec3 i = floor(p);
        vec3 f = fract(p);
        f = f * f * (3.0 - 2.0 * f);

        float n = i.x + i.y * 57.0 + i.z * 113.0;

        float a = random(vec2(n, n));
        float b = random(vec2(n + 1.0, n + 1.0));
        float c = random(vec2(n + 57.0, n + 57.0));
        float d = random(vec2(n + 58.0, n + 58.0));
        float e = random(vec2(n + 113.0, n + 113.0));
        float f1 = random(vec2(n + 114.0, n + 114.0));
        float g = random(vec2(n + 170.0, n + 170.0));
        float h = random(vec2(n + 171.0, n + 171.0));

        return mix(
          mix(mix(a, b, f.x), mix(c, d, f.x), f.y),
          mix(mix(e, f1, f.x), mix(g, h, f.x), f.y),
          f.z
        );
      }

      // 分形布朗运动
      float fbm(vec3 p) {
        float value = 0.0;
        float amplitude = 0.5;
        for (int i = 0; i < 5; i++) {
          value += amplitude * noise(p);
          p *= 2.0;
          amplitude *= 0.5;
        }
        return value;
      }

      // 星云密度函数
      float nebulaDensity(vec3 p) {
        // 基础形状 - 椭球形
        vec3 center = vec3(0.0, 0.0, 2.0);
        float sphere = 1.0 - length((p - center) * vec3(1.0, 1.5, 1.0)) * 0.5;
        sphere = max(0.0, sphere);

        // 噪声扰动
        float n = fbm(p * 1.5 + time * 0.05);
        n = n * 0.5 + 0.5;

        return sphere * n;
      }

      // 颜色映射
      vec3 nebulaColor(float density, vec3 p) {
        vec3 color1 = vec3(0.1, 0.0, 0.3);   // 深紫
        vec3 color2 = vec3(0.8, 0.2, 0.5);   // 粉红
        vec3 color3 = vec3(0.3, 0.5, 1.0);   // 蓝色
        vec3 color4 = vec3(1.0, 0.8, 0.3);    // 金色（恒星）

        // 基于位置的颜色
        float t = p.y * 0.5 + 0.5;
        vec3 baseColor = mix(color1, color2, t);

        // 高密度区域添加亮色
        if (density > 0.7) {
          baseColor = mix(baseColor, color3, (density - 0.7) * 3.0);
        }

        return baseColor;
      }

      void main() {
        vec2 uv = (gl_FragCoord.xy - 0.5 * resolution) / resolution.y;

        // 相机设置
        vec3 ro = vec3(0.0, 0.0, -3.0);  // 相机位置
        vec3 rd = normalize(vec3(uv, 1.0));  // 射线方向

        // Raymarching
        vec3 color = vec3(0.0);
        float transmittance = 1.0;

        vec3 p = ro;
        for (int i = 0; i < 64; i++) {
          float density = nebulaDensity(p);

          if (density > 0.01) {
            vec3 col = nebulaColor(density, p);

            // 累积颜色
            float alpha = density * 0.1;
            color += col * alpha * transmittance;
            transmittance *= (1.0 - alpha);

            // 提前终止
            if (transmittance < 0.01) break;
          }

          // 步进
          p += rd * 0.1;
        }

        // 背景星空
        float stars = pow(random(uv * 1000.0), 20.0) * 2.0;
        color += vec3(stars);

        // 色调映射
        color = 1.0 - exp(-color * 1.5);

        gl_FragColor = vec4(color, 1.0);
      }
    `;

    // 编译着色器
    const vs = gl.createShader(gl.VERTEX_SHADER);
    gl.shaderSource(vs, vsSource);
    gl.compileShader(vs);

    const fs = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(fs, fsSource);
    gl.compileShader(fs);

    this.program = gl.createProgram();
    gl.attachShader(this.program, vs);
    gl.attachShader(this.program, fs);
    gl.linkProgram(this.program);

    // 创建全屏四边形
    const vertices = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

    const position = gl.getAttribLocation(this.program, 'position');
    gl.enableVertexAttribArray(position);
    gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

    // Uniforms
    this.resolutionLocation = gl.getUniformLocation(this.program, 'resolution');
    this.timeLocation = gl.getUniformLocation(this.program, 'time');

    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
  }

  render(time) {
    const gl = this.gl;
    gl.useProgram(this.program);
    gl.uniform2f(this.resolutionLocation, this.canvas.width, this.canvas.height);
    gl.uniform1f(this.timeLocation, time * 0.001);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
}
```

---

## 四、外接库方案

### 使用 tsparticles

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.12.0/tsparticles.bundle.min.js"></script>
</head>
<body>
  <div id="tsparticles"></div>
  <script>
    const nebulaConfig = {
      fullScreen: { enable: true },
      background: { color: "#0a0a1a" },
      particles: {
        number: { value: 200 },
        color: { value: ["#ff6b9d", "#c44dff", "#4d9fff"] },
        shape: { type: "circle" },
        opacity: {
          value: { min: 0.1, max: 0.8 },
          animation: { enable: true, speed: 0.5, minimumValue: 0.1 }
        },
        size: {
          value: { min: 1, max: 4 },
          animation: { enable: true, speed: 2, minimumValue: 0.5 }
        },
        move: {
          enable: true,
          speed: 0.5,
          direction: "none",
          random: true,
          straight: false,
          outModes: "out"
        },
        blur: { enable: true, value: 2 }
      },
      interactivity: {
        events: {
          onHover: { enable: true, mode: "bubble" }
        }
      },
      detectRetina: true
    };

    tsParticles.load("tsparticles", nebulaConfig);
  </script>
</body>
</html>
```

---

## 五、生成提示词模板

使用本skill时，可复制以下提示词：

```
创建一个星云艺术作品，主题：[你的星云描述]

技术要求：
- 使用 Three.js + 自定义ShaderMaterial
- 实现Simplex Noise + FBM噪声叠加
- 颜色方案：[深紫 #1a0a2e / 粉红 #ff6b9d / 亮紫 #c44dff]
- 添加Additive Blending发光效果
- 包含缓慢的呼吸动画

可选增强：
- 添加粒子状恒星点缀
- 实现鼠标悬停交互
- 添加景深模糊效果
```

---

## 六、效果优化技巧

### 1. 颜色选择
```javascript
// 星云经典配色
const nebulaPalettes = [
  { name: "创世之柱", colors: ["#0d0221", "#3d1a78", "#8b2fc9", "#ff6b9d"] },
  { name: "猎户座", colors: ["#0a0a2e", "#1a237e", "#5c6bc0", "#f8f8f8"] },
  { name: "玫瑰星云", colors: ["#1a0a1a", "#8b2252", "#e91e63", "#ffccbc"] },
  { name: "蓝巨星", colors: ["#0a1628", "#1565c0", "#42a5f5", "#b3e5fc"] },
];
```

### 2. 性能优化
- 使用低分辨率渲染 + 双线性插值
- 限制FBM迭代次数（4-6次足够）
- 使用 `requestAnimationFrame` 节流
- 移动端减少粒子数量50%

### 3. 常见问题

| 问题 | 解决方案 |
|-----|---------|
| 边缘锯齿 | 增加 PlaneGeometry 分段数 |
| 颜色断层 | 增加颜色节点，smoothstep过渡 |
| 性能卡顿 | 降低raymarching步数，使用LOD |
| 动画抖动 | 使用平滑噪声函数而非纯random |

---

## 七、参考资料

- [Three.js 官方示例](https://threejs.org/examples/?q=nebula)
- [The Book of Shaders - Noise](https://thebookofshaders.com/11/)
- [Inigo Quilez shaders](https://iquilezles.org/articles/distfunctions/)
- [TSParticles 官方文档](https://particles.js.org/)
