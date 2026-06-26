# Shader 与 WebGL 模式

## 技术选型参考

| 目标               | 推荐起点           | 注意事项                       |
| ------------------ | ------------------ | ------------------------------ |
| 数学几何 3D 形态   | SDF + 光线步进     | 步数上限、法线质量、软阴影开销 |
| 有机运动效果       | 噪声 + 域扭曲      | 过度绘制、重复噪声调用         |
| 粒子效果           | 实例化或着色器粒子 | 移动端粒子数量上限、混合开销   |
| 泛光/故障/色彩调整 | 后处理通道         | 额外帧缓冲区显存               |
| 持续模拟           | 乒乓帧缓冲区       | 纹理格式支持                   |
| 白屏调试           | 编译/链接日志      | 函数顺序、被优化掉的 uniform   |

## WebGL2 适配清单

- 片元着色器以 `#version 300 es` 开头。
- 添加 `precision highp float;` 和 `out vec4 fragColor;`。
- 用 `in`/`out` 替代旧版 `varying`。
- 用 `texture()` 替代 `texture2D()`。
- 将 ShaderToy 风格的 `mainImage` 包装为标准 `main`。
- 使用 `gl_FragCoord.xy` 获取片元坐标。
- 辅助函数必须在被调用前声明。
- 预计算常量，不要在宏定义中放函数调用。

## 运行时骨架

```ts
const gl = canvas.getContext("webgl2");
if (!gl) throw new Error("WebGL2 is unavailable");

function compile(type: number, source: string) {
  const shader = gl.createShader(type);
  if (!shader) throw new Error("Cannot create shader");
  gl.shaderSource(shader, source.trim());
  gl.compileShader(shader);

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    throw new Error(gl.getShaderInfoLog(shader) ?? "Shader compile failed");
  }

  return shader;
}
```

## 性能预算

- 光线步进步数：从 64 起步，仅在出现伪影且证明必要时再提升。
- 体积采样：桌面端每条射线 16-24 次，移动端酌情降低。
- FBM 倍频：从 4 开始；避免在光线循环内嵌套 FBM。
- DPR：桌面端上限 2，移动端重度场景上限 1.5。
- 纹理尺寸：使用压缩或缩放资源；不要假设 4K 纹理是安全的。

## 调试视图

- 法线：输出归一化后的法线，映射到 0-1 范围。
- 步数：输出当前步数除以最大步数。
- 距离/深度：以灰度输出命中距离。
- UV：映射后输出 `vec3(uv, 0.0)`。
- 材质 ID：将 ID 映射到少量固定调色板。

## 视觉验证

- 桌面端和移动端尺寸下 Canvas 不为空白。
- 缩放时更新绘制缓冲区、视口、相机纵横比和 uniform。
- 低功耗模式下仍能响应，或有静态降级方案。
- 控制台无着色器编译/链接错误。
- 卸载或场景隐藏时停止动画。
