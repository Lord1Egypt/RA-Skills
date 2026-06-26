# Three.js Engine Guide

Rules specific to **Three.js** WebGL/3D projects.

---

## T1: The Dispose Trio 🧹

**Problem:** Three.js NEVER auto-releases GPU resources. Scene switch without dispose = VRAM leak. Tab eventually crashes.

**Solution:** Manually dispose geometry + material + textures for every object:

```js
function disposeObject(obj) {
  if (obj.geometry) obj.geometry.dispose();
  if (obj.material) {
    const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
    mats.forEach(mat => {
      Object.values(mat).forEach(v => {
        if (v instanceof THREE.Texture) v.dispose();
      });
      mat.dispose();
    });
  }
}

// On scene switch:
scene.traverse(child => disposeObject(child));
renderer.dispose();
```

---

## T2: GLB Compression Pipeline 📦

**Tested result:** 14MB → 800KB (94% reduction)

```bash
npx gltf-transform resample input.glb tmp1.glb
npx gltf-transform dedup tmp1.glb tmp2.glb
npx gltf-transform prune tmp2.glb tmp3.glb
npx gltf-transform quantize tmp3.glb tmp4.glb
npx gltf-transform draco tmp4.glb output.glb
```

### ⚠️ The Prune Pitfall

On **rigged models without animations**, `prune` deletes Skin nodes because it thinks the bones are unused.

**Fix:** Always use a GLB that contains at least one animation (e.g., idle clip) as the base model before running the pipeline.

### Frontend Setup

```js
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
gltfLoader.setDRACOLoader(dracoLoader);
```

---

## T3: Animation Crossfade State Machine 🎬

**Problem:** Direct `stop()` + `play()` causes a visible one-frame jump.

**Solution:** Always use `fadeIn` / `fadeOut` for smooth transitions:

```js
function playAnimation(name, fadeDuration = 0.3) {
  const next = mixer.clipAction(clips[name]);
  if (currentAction === next) return;
  next.reset().fadeIn(fadeDuration).play();
  if (currentAction) currentAction.fadeOut(fadeDuration);
  currentAction = next;
}
```

**Workaround for missing animations:** Use `timeScale` on an existing clip:
```js
// If "run" animation doesn't exist, speed up "walk":
clips.run = clips.walk;
mixer.clipAction(clips.run).timeScale = 1.8;
```

---

## T4: Circular Import Deadlocks 🔄

**Problem:** ES module static imports — A imports B, B imports A → deadlock in Three.js modular projects.

**Solutions:**
1. Expose shared functions via `window.functionName`
2. Use an event bus or shared state module
3. Restructure to break the cycle (preferred)

---

## Three.js Pre-Deploy Checklist

- [ ] All geometry/material/texture disposed on scene switch?
- [ ] GLB models Draco-compressed?
- [ ] DRACOLoader decoder path configured?
- [ ] Animation transitions use fadeIn/fadeOut?
- [ ] `prune` didn't delete Skin on rigged models?
- [ ] No circular imports between modules?
- [ ] `renderer.dispose()` called on cleanup?
