# Remotion 组件模板

## 基础 Composition

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
        durationInFrames={150}  // 5秒 @ 30fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: 'Hello World',
          subtitle: 'Generated with Remotion',
        }}
      />
    </>
  );
};
```

## 基础视频组件

```tsx
// src/MyVideo.tsx
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface MyVideoProps {
  title: string;
  subtitle: string;
}

export const MyVideo: React.FC<MyVideoProps> = ({ title, subtitle }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 标题弹簧动画
  const titleScale = spring({
    fps,
    frame,
    config: { damping: 100, stiffness: 200, mass: 0.5 },
  });

  // 标题淡入
  const titleOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // 副标题滑入
  const subtitleY = interpolate(frame, [40, 60], [50, 0], {
    extrapolateRight: 'clamp',
  });
  const subtitleOpacity = interpolate(frame, [40, 55], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // 背景渐变动画
  const bgProgress = interpolate(frame, [0, 150], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(135deg, 
          hsl(${220 + bgProgress * 40}, 70%, 30%) 0%, 
          hsl(${280 + bgProgress * 40}, 70%, 50%) 100%)`,
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      {/* 主标题 */}
      <div
        style={{
          fontSize: 100,
          fontWeight: 'bold',
          color: 'white',
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
          transform: `scale(${titleScale})`,
          opacity: titleOpacity,
        }}
      >
        {title}
      </div>

      {/* 副标题 */}
      <div
        style={{
          fontSize: 40,
          color: 'rgba(255,255,255,0.9)',
          marginTop: 20,
          transform: `translateY(${subtitleY}px)`,
          opacity: subtitleOpacity,
        }}
      >
        {subtitle}
      </div>
    </AbsoluteFill>
  );
};
```

## 入口文件

```tsx
// src/index.ts
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';

registerRoot(RemotionRoot);
```

## 常用动画模式

### 弹簧动画 (Spring)

```tsx
const scale = spring({
  fps,
  frame,
  config: {
    damping: 100,    // 阻尼 (越大越平稳)
    stiffness: 200,  // 刚度 (越大越快)
    mass: 0.5,       // 质量 (越大越慢)
  },
});
```

### 线性插值 (Interpolate)

```tsx
const value = interpolate(frame, [startFrame, endFrame], [startValue, endValue], {
  extrapolateLeft: 'clamp',   // 左侧超出时钳制
  extrapolateRight: 'clamp',  // 右侧超出时钳制
});
```

### 序列动画 (Sequence)

```tsx
import { Sequence } from 'remotion';

<Sequence from={0} durationInFrames={60}>
  <Scene1 />
</Sequence>
<Sequence from={60} durationInFrames={60}>
  <Scene2 />
</Sequence>
```

## 常见问题

### 1. 端口被占用

清理残留进程:
```bash
pkill -f chrome-headless
```

### 2. IPv6 问题

确保 loopback 地址存在:
```bash
ip -6 addr show lo | grep ::1 || ip -6 addr add ::1/128 dev lo
```

### 3. 浏览器权限

```bash
chmod +x node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell
```
