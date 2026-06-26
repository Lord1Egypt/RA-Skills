# 快速开始

## 适用场景

- 编写第一个 React 视频组件
- 使用核心动画 API（useCurrentFrame、interpolate、spring）
- 在 Remotion Studio 中预览和调试
- 本地渲染导出视频文件

---

## 项目结构

```
my-video/
├── src/
│   ├── index.ts         # 入口文件（registerRoot）
│   ├── Root.tsx         # Composition 注册
│   └── HelloWorld.tsx   # 视频组件
├── public/              # 静态资源
└── package.json
```

---

## 核心概念

### Composition（视频配置）

```typescript
// src/Root.tsx
import { Composition } from 'remotion'
import { MyVideo } from './MyVideo'

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyVideo"           // 渲染时引用的 ID
        component={MyVideo}
        durationInFrames={150} // 视频总帧数（30fps × 5秒 = 150帧）
        fps={30}               // 帧率
        width={1920}           // 宽度（像素）
        height={1080}          // 高度（像素）
      />
    </>
  )
}
```

---

## 基础视频组件

```typescript
// src/MyVideo.tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion'

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame()  // 当前帧号（从 0 开始）

  // 将帧号映射为透明度（0-30帧：从0渐变到1）
  const opacity = interpolate(frame, [0, 30], [0, 1])

  // 将帧号映射为移动距离
  const translateY = interpolate(frame, [0, 30], [50, 0])

  return (
    <AbsoluteFill style={{ backgroundColor: '#fff' }}>
      <div
        style={{
          opacity,
          transform: `translateY(${translateY}px)`,
          fontSize: 72,
          textAlign: 'center',
          marginTop: 400,
        }}
      >
        Hello, Remotion!
      </div>
    </AbsoluteFill>
  )
}
```

---

## 弹簧动画（spring）

```typescript
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion'

export const SpringExample: React.FC = () => {
  const frame = useCurrentFrame()
  const { fps } = useVideoConfig()

  // 弹簧动画：从 0 弹到 1，自然物理感
  const scale = spring({
    frame,
    fps,
    config: {
      damping: 200,   // 阻尼（越大越快停止）
      stiffness: 100, // 刚度
      mass: 1,        // 质量
    },
  })

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ transform: `scale(${scale})`, width: 200, height: 200, background: 'blue' }} />
    </AbsoluteFill>
  )
}
```

---

## 时序控制（Sequence）

```typescript
import { AbsoluteFill, Sequence } from 'remotion'

export const SequenceExample: React.FC = () => {
  return (
    <AbsoluteFill>
      {/* 第 0 帧开始，持续 60 帧 */}
      <Sequence from={0} durationInFrames={60}>
        <TitleCard />
      </Sequence>
      {/* 第 40 帧开始（与上一个有 20 帧重叠） */}
      <Sequence from={40} durationInFrames={80}>
        <ContentSection />
      </Sequence>
    </AbsoluteFill>
  )
}
```

---

## 动态 Props（数据驱动视频）

```typescript
// 定义 Props 类型
interface VideoProps {
  name: string
  score: number
}

export const PersonalVideo: React.FC<VideoProps> = ({ name, score }) => {
  const frame = useCurrentFrame()
  const displayScore = interpolate(frame, [0, 60], [0, score])

  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a2e' }}>
      <h1 style={{ color: 'white' }}>Hello, {name}!</h1>
      <p style={{ color: '#e94560' }}>Your score: {Math.round(displayScore)}</p>
    </AbsoluteFill>
  )
}

// 在 Root.tsx 中传入默认 Props（Studio 预览用）
<Composition
  id="PersonalVideo"
  component={PersonalVideo}
  defaultProps={{ name: 'World', score: 100 }}
  durationInFrames={90}
  fps={30}
  width={1280}
  height={720}
/>
```

---

## 使用图片和静态资源

```typescript
import { AbsoluteFill, Img, staticFile } from 'remotion'

export const WithImage: React.FC = () => {
  return (
    <AbsoluteFill>
      {/* 使用 public/ 目录中的文件 */}
      <Img src={staticFile('logo.png')} style={{ width: 300 }} />
    </AbsoluteFill>
  )
}
```

---

## Remotion Studio 预览

```bash
# 启动 Studio（热重载）
npx remotion studio

# 打开 http://localhost:3000
# - 左侧：Composition 列表
# - 中间：视频预览
# - 右侧：Props 编辑器
# - 底部：时间轴
```

---

## 本地渲染导出

```bash
# 渲染为 MP4
npx remotion render src/index.ts MyVideo out/video.mp4

# 渲染为 GIF
npx remotion render src/index.ts MyVideo out/video.gif

# 渲染为 WebM
npx remotion render src/index.ts MyVideo out/video.webm

# 只渲染特定帧范围
npx remotion render src/index.ts MyVideo out/video.mp4 --frames=0-60

# 渲染单帧（PNG）
npx remotion still src/index.ts MyVideo out/frame.png --frame=30

# 渲染时传入 Props
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --props='{"name":"Alice","score":95}'
```

---

## 完成确认检查清单

- [ ] 视频组件在 Studio 中正常预览（无错误）
- [ ] `useCurrentFrame()` 返回正确帧号（0 到 durationInFrames-1）
- [ ] `interpolate()` 动画效果正确
- [ ] `npx remotion render` 输出 MP4 文件且可以播放
- [ ] 动态 Props 在 Studio 中可编辑并实时预览

---

## 下一步

- [高级用法](03-advanced-usage.md) — Lambda 渲染、字幕生成、批量个性化视频
