# Three.js Engine — Quality Gates

## Three-1: Dispose Trio (Prevent VRAM Leaks)

Three.js never auto-releases GPU resources. On scene switch, manually dispose everything:

```js
function disposeObject(obj) {
  if (obj.geometry) obj.geometry.dispose();
  if (obj.material) {
    const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
    mats.forEach(mat => {
      Object.values(mat).forEach(v => { if (v instanceof THREE.Texture) v.dispose(); });
      mat.dispose();
    });
  }
}

// Walk entire scene tree:
scene.traverse(child => disposeObject(child));
renderer.dispose();
```

## Three-2: GLB Compression Pipeline

Tested: 14MB → 800KB (94% reduction).

```bash
npx gltf-transform resample input.glb tmp1.glb
npx gltf-transform dedup tmp1.glb tmp2.glb
npx gltf-transform prune tmp2.glb tmp3.glb
npx gltf-transform quantize tmp3.glb tmp4.glb
npx gltf-transform draco tmp4.glb output.glb
```

**⚠️ Prune Pitfall:** On rigged models without animations, `prune` deletes Skin nodes (thinks bones are unused). Fix: use a GLB that already contains at least one animation (e.g., idle) as base model.

Frontend requires: DRACOLoader + decoder path from CDN.

## Three-3: Animation State Machine with Crossfade

Never `stop()` + `play()` directly — causes one-frame jump. Always crossfade:

```js
function playAnimation(name, fadeDuration = 0.3) {
  const next = mixer.clipAction(clips[name]);
  if (currentAction === next) return;
  next.reset().fadeIn(fadeDuration).play();
  if (currentAction) currentAction.fadeOut(fadeDuration);
  currentAction = next;
}
```

For missing animations (e.g., TRIPO quad `run` fails), use `timeScale` on walk clip:
```js
clips.run = clips.walk; // fallback
mixer.clipAction(clips.run).timeScale = 1.8;
```

## Three-4: Import Circular Dependencies

ES module `import` is static. A imports B + B imports A → deadlock in Three.js modular projects.

Workaround: expose shared functions via `window.functionName` or use an event bus / shared state module.

## Three.js Checklist

- [ ] All geometry/material/texture disposed on scene switch?
- [ ] GLB models Draco-compressed?
- [ ] Animation transitions use fadeIn/fadeOut?
- [ ] `prune` didn't delete Skin on rigged models?
- [ ] DRACOLoader decoder path configured?
- [ ] No circular imports between modules?
