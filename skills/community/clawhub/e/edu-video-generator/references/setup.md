# 项目初始化指南

## 方式一：使用 create-video 脚手架

```bash
npx create-video@latest my-video --template=blank
```

**交互式选项**:
- 选择模板 (推荐 Blank)
- 是否初始化 Git (可选)
- 是否添加 TailwindCSS (可选)
- 是否添加 Agent Skills (可选)

## 方式二：手动初始化

### 1. 创建项目目录

```bash
mkdir my-video && cd my-video
```

### 2. 初始化 npm

```bash
npm init -y
```

### 3. 修改 package.json

```json
{
  "name": "my-video",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "remotion studio src/index.ts",
    "render": "node render.mjs",
    "build": "node render.mjs"
  },
  "dependencies": {
    "@remotion/bundler": "^4.0.0",
    "@remotion/cli": "^4.0.0",
    "@remotion/player": "^4.0.0",
    "@remotion/renderer": "^4.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "remotion": "^4.0.0",
    "typescript": "^5.0.0"
  }
}
```

### 4. 安装依赖

```bash
npm install
```

### 5. 创建目录结构

```bash
mkdir -p src out
```

### 6. 创建 TypeScript 配置

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  },
  "include": ["src/**/*"]
}
```

### 7. 创建 Remotion 配置 (可选)

```typescript
// remotion.config.ts
import { Config } from '@remotion/cli/config';

// 可选：指定 Chrome 路径
// Config.setBrowserExecutable('/path/to/chrome');

// 可选：设置默认端口
// Config.setPort(3000);
```

### 8. 创建组件文件

```tsx
// src/Root.tsx
import { Composition } from 'remotion';
import { MyVideo } from './MyVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyVideo"
        component={MyVideo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: 'Hello World',
        }}
      />
    </>
  );
};
```

```tsx
// src/MyVideo.tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

interface MyVideoProps {
  title: string;
}

export const MyVideo: React.FC<MyVideoProps> = ({ title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ fps, frame, config: { damping: 100, stiffness: 200 } });
  const opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      <div
        style={{
          fontSize: 100,
          fontWeight: 'bold',
          color: 'white',
          transform: `scale(${scale})`,
          opacity,
        }}
      >
        {title}
      </div>
    </AbsoluteFill>
  );
};
```

```tsx
// src/index.ts
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';

registerRoot(RemotionRoot);
```

### 9. 创建渲染脚本

```javascript
// render.mjs
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function render() {
  console.log('Bundling...');
  const bundled = await bundle({
    entryPoint: path.join(__dirname, 'src/index.ts'),
    outDir: path.join(__dirname, 'out/bundle'),
  });

  console.log('Getting composition...');
  const composition = await selectComposition({
    serveUrl: bundled,
    id: 'MyVideo',
    preferIpv4: true,
  });

  console.log('Rendering...');
  await renderMedia({
    composition,
    serveUrl: bundled,
    codec: 'h264',
    outputLocation: path.join(__dirname, 'out/video.mp4'),
    preferIpv4: true,
  });

  console.log('Done! Output: out/video.mp4');
}

render().catch(console.error);
```

## 开发流程

### 1. 预览 (开发模式)

```bash
npm start
# 或
npx remotion studio src/index.ts
```

浏览器打开 `http://localhost:3000` 查看实时预览

### 2. 渲染 (生产模式)

```bash
npm run render
# 或
node render.mjs
```

### 3. 自定义渲染参数

```tsx
await renderMedia({
  composition,
  serveUrl: bundled,
  codec: 'h264',
  outputLocation: './out/video.mp4',
  
  // 质量设置
  crf: 18,              // 质量 (0-51, 越低质量越好)
  preset: 'medium',     // 编码预设
  
  // 性能设置
  concurrency: 4,       // 并发渲染帧数
  frameRange: [0, 60],  // 只渲染部分帧
  
  // 浏览器设置
  preferIpv4: true,
  browserExecutable: '/path/to/chrome',
  
  // 日志
  onProgress: ({ renderedFrames, encodedFrames }) => {
    console.log(`Rendered: ${renderedFrames}, Encoded: ${encodedFrames}`);
  },
});
```

## 常用依赖版本

```json
{
  "remotion": "^4.0.434",
  "@remotion/cli": "^4.0.434",
  "@remotion/bundler": "^4.0.434",
  "@remotion/renderer": "^4.0.434",
  "@remotion/player": "^4.0.434",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "typescript": "^5.9.0"
}
```
