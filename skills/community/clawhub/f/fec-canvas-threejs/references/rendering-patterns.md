# Canvas, Three.js and R3F mode

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

## Animation loop

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

## Three.js basic scenario

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
<Canvas camera={{ position: [0, 0, 5], fov: 75 }} role="img" aria-label="3D Product Preview">
  <ambientLight intensity={0.5} />
  <directionalLight position={[5, 5, 5]} />
  <mesh>
    <boxGeometry />
    <meshStandardMaterial color="hotpink" />
  </mesh>
  <OrbitControls />
</Canvas>
```

## Performance and cleanup

- Textures are compressed as much as possible and the size is limited. The normal upper limit is first evaluated at 2048px.
- Use `InstancedMesh` for repeated geometry.
- Pause animation loop when continuous redrawing is not required.
- Release geometry, material, texture, renderer, and controls when uninstalling.
- ResizeObserver updates camera aspect and renderer size.
