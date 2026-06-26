# Canvas、Three.js 与 R3F 模式

## Canvas 2D

```ts
const canvas = document.getElementById("chart") as HTMLCanvasElement;
const ctx = canvas.getContext("2d");
if (!ctx) throw new Error("Canvas 2D is unavailable");

ctx.fillStyle = "#3b82f6";
ctx.fillRect(10, 10, 50, 50);
ctx.beginPath();
ctx.arc(100, 100, 30, 0, Math.PI * 2);
ctx.fill();
```

## 动画循环

```ts
let animationId = 0;

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  updateParticles();
  drawParticles(ctx);
  animationId = requestAnimationFrame(animate);
}

animate();
return () => cancelAnimationFrame(animationId);
```

## Three.js 基础场景

```ts
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);
```

## React Three Fiber

```tsx
<Canvas camera={{ position: [0, 0, 5], fov: 75 }} role="img" aria-label="3D 产品预览">
  <ambientLight intensity={0.5} />
  <directionalLight position={[5, 5, 5]} />
  <mesh>
    <boxGeometry />
    <meshStandardMaterial color="hotpink" />
  </mesh>
  <OrbitControls />
</Canvas>
```

## 性能与清理

- 纹理尽量压缩并限制尺寸，常规上限先按 2048px 评估。
- 重复几何体用 `InstancedMesh`。
- 不需要持续重绘时暂停 animation loop。
- 卸载时释放 geometry、material、texture、renderer、controls。
- ResizeObserver 更新相机 aspect 和 renderer size。
