# Web Embedding Reference

Detailed reference for embedding `avatar-runtime` in browser applications.

## AvatarWidget options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `modelUrl` | string | `''` | Live2D model URL. Empty → vector renderer (no vendor scripts needed). |
| `vrmUrl` | string | — | VRM model URL (`.vrm`). Triggers VRM 3D renderer. |
| `control` | object | — | Initial control state `{ avatar: { face, body, emotion }, scene }`. |
| `stateUrl` | string | — | Runtime `/v1/status` URL for live control polling. |
| `pollMs` | number | `500` | Polling interval in ms. |
| `vendorBase` | string | `/demo/vendor-dist` | Directory for auto-loaded Live2D vendor scripts. Dev default only — set for production. |
| `width` | number | `360` | Canvas width in px. |
| `height` | number | `360` | Canvas height in px. |
| `widgetBase` | string | auto | Override `web/` script path when auto-detection fails. |

## AvatarWidget API

| Method | Description |
|--------|-------------|
| `ready()` | Promise — resolves when mounted. Always add `.catch()`. |
| `update(mediaState)` | Push mediaState. Buffered if called before `ready()`. |
| `destroy()` | Stop polling, unmount renderer. Irreversible. |
| `getState()` | Returns renderer internal state (debug). |

## npm / bundler usage

```js
const AvatarWidget = require('@acnlabs/avatar-runtime/widget');
const widget = new AvatarWidget(container, {
  modelUrl:   '/assets/live2d/slot/default.model.json',
  widgetBase: '/packages/avatar-runtime/web/',  // must be served statically
});
await widget.ready();
```

## Renderer Registry (advanced)

For programmatic control or custom renderer integration.

Load order matters — vector renderer has `canHandle: () => true` and must be last.

```html
<!-- custom renderer BEFORE index.js to take priority over vector fallback -->
<script src="/packages/avatar-runtime/web/renderer-registry.js"></script>
<script src="/your/custom-renderer.js"></script>
<script src="/packages/avatar-runtime/web/renderers/live2d-pixi-adapter.js"></script>
<script src="/packages/avatar-runtime/web/renderers/vrm-renderer.js"></script>
<script src="/packages/avatar-runtime/web/renderers/vector-renderer.js"></script>
<script src="/packages/avatar-runtime/web/index.js"></script>
```

```js
// use registry directly
var reg = window.OpenPersonaRendererRegistry;
reg.create(
  {
    avatarModel3Url: '/path/to/model.json',
    control: {
      avatar: { face: { mouth: { smile: 0.5 } } }
    },
    render: { rendererMode: 'pixi' }
  },
  container,
  { width: 360, height: 360 }
).then(function(instance) {
  instance.update({
    control: {
      avatar: {
        face: { pose: { yaw: 0.1 } }
      }
    }
  });
  // instance.unmount() when done
});
```

## Custom renderer skeleton

Renderers read from `mediaState.control` (v0.2+).

```js
window.OpenPersonaRendererRegistry.register({
  canHandle: function(mediaState) {
    return mediaState.render && mediaState.render.rendererMode === 'my-renderer';
  },
  createInstance: function() {
    return {
      mount:   function(container, opts) { return Promise.resolve(); },
      update:  function(mediaState) {
        var face    = mediaState.control && mediaState.control.avatar && mediaState.control.avatar.face;
        var emotion = mediaState.control && mediaState.control.avatar && mediaState.control.avatar.emotion;
        var scene   = mediaState.control && mediaState.control.scene;
        // apply face, emotion, scene...
      },
      unmount: function() { /* cleanup */ },
    };
  }
});
```

**Dead signal rule:** If your renderer does not support `body` or `scene` control, simply ignore those sub-domains. The runtime stores all control state regardless — renderers silently skip what they cannot handle.

See `web/IRenderer.js` for full interface JSDoc.

## mediaState shape (v0.2)

```js
{
  avatarModel3Url:   '/path/to/model.json',   // Live2D
  avatarModelVrmUrl: '/path/to/model.vrm',    // VRM 3D
  control: {
    avatar: {
      face: {
        pose:  { yaw: 0, pitch: 0, roll: 0 },
        eyes:  { blinkL: 1, blinkR: 1, gazeX: 0, gazeY: 0 },
        brows: { browInner: 0, browOuterL: 0, browOuterR: 0 },
        mouth: { jawOpen: 0, smile: 0, mouthPucker: 0 },
        source: 'agent'
      },
      body: {
        preset: 'idle',
        skeleton: { leftUpperArm: { x: 0, y: 0, z: -20 }, ... },
        source: 'agent'
      },
      emotion: {
        valence: 0, arousal: 0, label: 'neutral', intensity: 0.5,
        source: 'agent'
      }
    },
    scene: {
      camera: { position: { x: 0, y: 1.4, z: 1.8 }, fov: 30 },
      world: { ambientLight: 0.6, keyLight: { intensity: 1.0 } },
      source: 'agent'
    }
  },
  render: { rendererMode: 'pixi' }
}
```

## Package exports

```
@acnlabs/avatar-runtime          → src/runtime.js   (Node.js server)
@acnlabs/avatar-runtime/web      → web/index.js     (registry bootstrap)
@acnlabs/avatar-runtime/widget   → web/avatar-widget.js
```
