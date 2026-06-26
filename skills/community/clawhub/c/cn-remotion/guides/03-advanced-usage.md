# 高级用法

## AWS Lambda 渲染

Lambda 渲染通过并发多个 Lambda 函数大幅缩短渲染时间：

```bash
# 安装 Lambda 包
npm install @remotion/lambda

# 配置 AWS 凭证
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1

# 部署 Lambda 函数和 S3 存储桶
npx remotion lambda sites create --site-name=my-video
npx remotion lambda functions deploy

# 渲染（并发 Lambda 处理）
npx remotion lambda render my-video MyComposition
```

```typescript
// 代码方式调用 Lambda 渲染
import { renderMediaOnLambda, getRenderProgress } from '@remotion/lambda/client'

const { renderId, bucketName } = await renderMediaOnLambda({
  region: 'us-east-1',
  functionName: 'remotion-render-4-0-0-mem2048mb-disk2048mb-120sec',
  serveUrl: 'https://your-s3-site.s3.amazonaws.com',
  composition: 'MyComposition',
  inputProps: { name: 'Alice', score: 95 },
  codec: 'h264',
})

// 轮询进度
const progress = await getRenderProgress({ renderId, bucketName, region: 'us-east-1' })
console.log(`渲染进度: ${progress.overallProgress * 100}%`)
```

---

## 批量个性化视频生成

用数据批量生成个性化视频（例如 GitHub Unwrapped 风格）：

```typescript
// scripts/batch-render.ts
import { renderMedia, selectComposition } from '@remotion/renderer'

const users = [
  { name: 'Alice', score: 95, year: 2024 },
  { name: 'Bob', score: 87, year: 2024 },
  { name: 'Carol', score: 92, year: 2024 },
]

for (const user of users) {
  const composition = await selectComposition({
    serveUrl: 'http://localhost:3000',
    id: 'PersonalVideo',
    inputProps: user,
  })

  await renderMedia({
    composition,
    serveUrl: 'http://localhost:3000',
    codec: 'h264',
    outputLocation: `out/${user.name.toLowerCase()}.mp4`,
    inputProps: user,
  })

  console.log(`✅ 渲染完成：${user.name}`)
}
```

```bash
# 先启动 Studio（作为 Bundle 服务器）
npx remotion studio &
# 然后运行批量脚本
npx ts-node scripts/batch-render.ts
```

---

## 字幕生成

```typescript
// 安装依赖
// npm install @remotion/captions @remotion/media-utils

import { useCurrentFrame, useVideoConfig } from 'remotion'
import { Caption, createTikTokStyleCaptions } from '@remotion/captions'

// 创建字幕数据（通常来自 Whisper/AssemblyAI 等 STT 服务）
const captions: Caption[] = [
  { text: 'Hello World', startMs: 0, endMs: 1500, confidence: 0.99 },
  { text: 'This is Remotion', startMs: 1500, endMs: 3000, confidence: 0.98 },
]

// TikTok 风格逐词字幕
const { pages } = createTikTokStyleCaptions({
  captions,
  combineTokensWithinMilliseconds: 1200,
})

export const SubtitleVideo: React.FC = () => {
  const frame = useCurrentFrame()
  const { fps } = useVideoConfig()
  const currentTimeMs = (frame / fps) * 1000

  const currentPage = pages.find(
    (p) => p.startMs <= currentTimeMs && p.endMs > currentTimeMs
  )

  return (
    <AbsoluteFill>
      <Video src={staticFile('speech.mp4')} />
      {currentPage && (
        <div style={{
          position: 'absolute', bottom: 100, left: 0, right: 0,
          textAlign: 'center', fontSize: 48, color: 'white',
          textShadow: '2px 2px 4px black',
        }}>
          {currentPage.text}
        </div>
      )}
    </AbsoluteFill>
  )
}
```

---

## 使用 Google Fonts

```typescript
import { loadFont } from '@remotion/google-fonts/Roboto'

const { fontFamily } = loadFont()

export const VideoWithFont: React.FC = () => {
  return (
    <AbsoluteFill>
      <h1 style={{ fontFamily, fontSize: 80 }}>Custom Font</h1>
    </AbsoluteFill>
  )
}
```

---

## 嵌入 GIF

```typescript
import { Gif } from '@remotion/gif'
import { AbsoluteFill, staticFile } from 'remotion'

export const GifExample: React.FC = () => {
  return (
    <AbsoluteFill>
      <Gif
        src={staticFile('animation.gif')}
        width={400}
        height={300}
        fit="fill"
        playbackRate={1}
      />
    </AbsoluteFill>
  )
}
```

---

## 调用外部 API 获取数据

```typescript
import { delayRender, continueRender, staticFile } from 'remotion'

export const ApiDataVideo: React.FC = () => {
  const [data, setData] = useState(null)
  const [handle] = useState(() => delayRender())  // 告诉 Remotion 等待数据

  useEffect(() => {
    fetch('https://api.example.com/data')
      .then(r => r.json())
      .then(d => {
        setData(d)
        continueRender(handle)  // 数据就绪，继续渲染
      })
  }, [handle])

  if (!data) return null

  return (
    <AbsoluteFill>
      <h1>{data.title}</h1>
    </AbsoluteFill>
  )
}
```

---

## 渲染质量配置

```bash
# 高质量 H.264（推荐）
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --codec h264 \
  --crf 18

# H.265（更小文件）
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --codec h265

# ProRes（无损，剪辑用）
npx remotion render src/index.ts MyVideo out/video.mov \
  --codec prores

# 并发渲染（加快速度）
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --concurrency=4
```

---

## 完成确认检查清单

- [ ] Lambda 部署成功（`npx remotion lambda sites create` 无报错）
- [ ] 批量渲染脚本正常运行（可选）
- [ ] 字幕组件在预览中同步显示（可选）
- [ ] 高质量 MP4 渲染无伪影

---

## 相关链接

- [故障排查](../troubleshooting.md)
- [完整文档](https://remotion.dev/docs)
- [Lambda 指南](https://remotion.dev/docs/lambda)
- [字幕文档](https://remotion.dev/docs/captions)
