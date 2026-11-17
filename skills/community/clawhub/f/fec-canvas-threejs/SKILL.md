---
name: fec-canvas-threejs
description: Use when building or reviewing Canvas 2D, Three.js/WebGL, React Three Fiber, GLSL shaders, ShaderToy-to-WebGL adaptation, 2D/3D visualization, game rendering, animation loops, GPU resource cleanup, or rendering performance. Do not use for standard DOM UI, charts already covered by a chart library, or non-graphical performance work; Chinese triggers include Canvas, Three.js, WebGL, GLSL, Shader, 3D, data visualization, games.
---

# Canvas and Three.js

## Purpose

Enable high-performance 2D/3D graphics rendering in the browser.

## Procedure

1. First select the rendering layer: DOM for standard UI; Canvas 2D for simple 2D graphics/signatures/particles; Three.js/WebGL for 3D models, spatial interactions and complex particles; React Three Fiber for declarative 3D in React projects.
2. Define stable size, DPI adaptation, and resize behavior for the render container; Canvas does not automatically scale cleanly with CSS.
3. The animation loop uses `requestAnimationFrame`, which is paused when it is invisible or has no changes, and canceled when it is uninstalled.
4. Three.js must release geometry/material/texture/renderer and remove event listeners and observers.
5. Shader/WebGL tasks first identify whether it is an SDF, ray marching, noise, particle, post-processing, multipass or debugging issue, and then decide whether native WebGL2, Three.js ShaderMaterial or R3F is required.
6. Check the GLSL version, entry function, varying/in-out, texture API, uniform usage and function declaration order when adapting to WebGL2 to avoid white screen leaving only console errors.
7. Provide `aria-label`, alternative text or DOM summary for inaccessible graphic content; interactive graphics must have keyboard support.

## Core Patterns

```ts
const dpr = Math.min(window.devicePixelRatio || 1, 2);
canvas.width = width * dpr;
canvas.height = height * dpr;
canvas.style.width = `${width}px`;
canvas.style.height = `${height}px`;
ctx.scale(dpr, dpr);
```

```ts
let animationId = 0;
function animate() {
  animationId = requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

return () => {
  cancelAnimationFrame(animationId);
  geometry.dispose();
  material.dispose();
  renderer.dispose();
};
```

## Detailed reference

Load [references/rendering-patterns.md](references/rendering-patterns.md) when it comes to Canvas 2D drawing, animation loops, Three.js scene building, React Three Fiber, InstancedMesh, and performance cleanup.

Load [references/shader-webgl-patterns.md](references/shader-webgl-patterns.md) when it comes to shader routing, WebGL2 adaptation, GLSL debugging, multi-pass budgeting, and visual verification.

## Constraints

- Canvas/WebGL content is not visible to screen readers and alternative semantics must be provided.
- WebGL consumes GPU, and low-end devices need to limit the pixel ratio, number of faces and texture size.
- Three.js resources will not be released automatically, and missing `dispose()` will cause GPU memory leaks.
- Canvas responsive must synchronize CSS dimensions, drawing dimensions, and camera/viewport.
- Complex layout/path planning can be combined with the background thread workflow, but the rendering itself is still coordinated on the main thread/rendering thread.
- The Shader main loop, number of sampling layers, and number of multi-passes must be budgeted; on low-end devices, reduce the DPR, number of steps, number of particles, or disable heavy post-processing.
- Before delivery, you must confirm that the canvas is not empty, has the correct size, is not stretched after resize, and has no shader compile/link errors in the console.

## Expected Output

2D/3D scenes are crisp, responsive, cleanable, and close to 60fps on key devices; users can understand/operate with core content via alt text or keyboard paths.
