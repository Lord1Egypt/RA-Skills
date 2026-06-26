# 🐛 技术陷阱与排坑手册 (FableForge Troubleshooting Manual)

本手册整理了 FableForge 视频生成流水线在模式 A（纯图片）与模式 B（视频 B-roll）开发及渲染过程中已知的各种技术陷阱，提供针对性的根因分析与快速修复方案。

---

## 1. 模式 A（纯图片）陷阱

| 现象 | 根因 | 修复方案 |
|------|------|------|
| 图片裁切/偏移 | GSAP 矩阵覆盖了 `translate` 居中 | 改用 `object-fit: contain`，绝不用 `translate` 居中 |
| 正方形图片顶部被裁 | `object-fit: cover` 裁切了主体 | 强制 16:9 生图，或改用 `contain` + 毛玻璃背景填充 |
| 视频提前截断/少幕 | 字幕中含未转义的 `<` `>` 破坏 DOM 结构 | 改用 `textContent` 动态安全注入，不直接写 innerHTML |
| 画面色偏 | img 标签含 `filter: hue-rotate(...)` | 在 CSS/HTML 中删除或覆盖该 filter 属性 |

---

## 2. 模式 B（视频 + 文字叠加）陷阱

| 现象 | 根因 | 修复方案 |
|------|------|------|
| 视频背景全黑 | `.clip` 默认 `opacity: 0`，视频继承了该属性 | `.bg-video { opacity: 1; }` 物理覆盖，强制可见 |
| 渲染后视频冻结在第一帧 | `<video data-start>` 嵌套在 `<div data-start>` 内 | 扁平化，将 `<video>` 移出来作为 `#composition` 的扁平直接子元素 |
| `media_missing_id` 错误 | `<video>` 没有指定 `id` 属性 | 每个 `<video>` 标签必须加上唯一且语义清晰的 `id` |
| Pexels 下载 SSL 报错 | Cloudflare CDN 在传输末尾断开连接 | curl 增加 `--retry 5`，若文件通过 `ffprobe` 校验则视为下载成功 |
| 横屏视频裁切后比例变形 | 直接进行 scale 缩放，而非先 crop 裁切 | 使用 FFmpeg filter 先居中裁剪再缩放：`crop=ih*9/16:ih,scale=1080:1920` |

---

## 3. 通用底层陷阱

| 现象 | 根因 | 修复方案 |
|------|------|------|
| `inspect` 报 `totalDuration undefined` | 根容器 `#composition` 缺少 `data-duration` | 必须补上 `data-duration="{音频总长}"` 属性 |
| `inspect` 报错 / MP4 时长随机 | 动画 timeline 没有暂停，违反渲染合约 | 时间轴永远设置 `gsap.timeline({ paused: true })`，严禁在脚本中写入 `play()` |
| `FFmpeg not found` | 运行环境没有找到 ffmpeg 二进制文件 | 执行前通过脚本或手动 `export PATH=./bin:$PATH` 导入环境路径 |
