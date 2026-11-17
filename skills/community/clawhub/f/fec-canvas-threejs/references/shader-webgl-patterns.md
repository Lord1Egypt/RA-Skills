# Shader and WebGL mode

## Technical selection reference

| Goals | Recommended starting points | Notes |
| ------------------ | ------------------ | ------------------------------ |
| Mathematical Geometry 3D Shape | SDF + Ray Stepping | Step Limit, Normal Quality, Soft Shadow Overhead |
| Organic motion effects | Noise + domain distortion | Overdraw, repeated noise calls |
| Particle effects | Instanced or shader particles | Mobile particle limit, blending overhead |
| Bloom/Glitch/Color Adjustments | Post-Processing Passes | Extra Frame Buffer Video Memory |
| Continuous Simulation | Ping Pong Frame Buffer | Texture Format Support |
| White screen debugging | Compilation/link log | Function order, optimized uniform |

## WebGL2 adaptation list

- Fragment shaders start with `#version 300 es`.
- Added `precision highp float;` and `out vec4 fragColor;`.
- Replace old `varying` with `in`/`out`.
- Use `texture()` instead of `texture2D()`.
- Wrap ShaderToy style `mainImage` into standard `main`.
- Use `gl_FragCoord.xy` to obtain fragment coordinates.
- Helper functions must be declared before being called.
- Precompute constants, don't put function calls in macro definitions.

## Runtime skeleton

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

## Performance budget

- Ray Steps: Start at 64 and only increase if artifacts appear and prove necessary.
- Volume sampling: 16-24 times per ray on desktop, lower as appropriate on mobile.
- FBM multiplier: starts from 4; avoid nesting FBMs inside ray loops.
- DPR: The upper limit is 2 on desktop and 1.5 in severe scenarios on mobile.
- Texture dimensions: Use compressed or scaled assets; don't assume 4K textures are safe.

## Debug view

- Normal: Outputs the normalized normal, mapped to the 0-1 range.
- Number of steps: Output the current number of steps divided by the maximum number of steps.
- Distance/Depth: Outputs hit distance in grayscale.
- UV: Output `vec3(uv, 0.0)` after mapping.
- Material IDs: Map IDs to a small number of fixed palettes.

## Visual verification

- Canvas is not blank in desktop and mobile sizes.
- Update draw buffer, viewport, camera aspect ratio and uniform when zooming.
- Still responsive in low power mode, or there may be a static degradation solution.
- No shader compilation/linking errors in the console.
- Stop animation when unloading or scene hidden.
