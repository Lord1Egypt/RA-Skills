# Video 速查（v1.3 新增）

**用途**：嵌入视频。支持 YouTube / Bilibili（自动转 iframe 嵌入）和直接的视频文件 URL（用原生 `<video>` 标签）。

## 语法

    <Video src="https://www.youtube.com/watch?v=dQw4w9WgXcQ" caption="演示视频" />

    <Video src="https://www.bilibili.com/video/BV1xx411c7mD" caption="B 站演示" />

    <Video src="./videos/demo.mp4" poster="./images/cover.png" caption="本地文件" />

## Props

| 名称 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `src` | `string` | — | **必填**。YouTube/Bilibili URL 或 直接的视频文件 URL |
| `poster` | `string` | — | 本地视频的封面图 URL（iframe 视频无效） |
| `caption` | `string` | — | 底部图注 |
| `autoplay` | `boolean` | `false` | 自动播放（自动隐含 muted） |
| `loop` | `boolean` | `false` | 循环播放 |
| `muted` | `boolean` | `false` | 静音 |
| `controls` | `boolean` | `true` | 显示播放控件 |

## URL 识别规则

- `youtube.com/watch?v=XXXX` / `youtu.be/XXXX` / `youtube.com/embed/XXXX` → 提取 11 位 videoId，转成 `https://www.youtube.com/embed/{videoId}`
- `bilibili.com/video/BVxxxxxx` → 提取 BV 号，转成 `https://player.bilibili.com/player.html?bvid={bv}&high_quality=1&autoplay=0`
- 其他 URL → 走原生 `<video>` 标签

## 样式

v1.3 起对齐首页卡片风格：
- 16:9 容器（`padding-bottom: 56.25%`）
- 20px 圆角
- 1px `#E8E5E0` 边框
- 深色背景 `#131314`（对齐首页 `--color-bg-dark`）
- 细阴影 `--shadow-sm`

## 注意

- **autoplay 必须配合 muted**——浏览器策略要求自动播放的视频静音。skill 的 renderer 会自动为 autoplay 加上 muted。
- **iframe 不支持 poster**——YouTube/Bilibili 自带封面
- **YouTube 在国内需要代理访问**——选 Bilibili 或本地 mp4 更稳
- 本地视频路径需要先通过 `image-localize.mjs` 本地化（v1.3 的 image-localize 暂不处理视频，需要手工拷贝到 `posts/<slug>/videos/`）

## 何时不用

- 只是一张动图 → 普通 `![alt](./images/x.gif)`
- 需要精细的视频编辑 / 章节 / 字幕 → 不在本组件能力范围
