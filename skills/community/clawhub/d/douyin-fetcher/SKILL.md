---
name: douyin-fetcher
description: 抖音视频获取模块。从抖音链接下载视频文件，支持短视频和 DASH 格式长视频。
---

# Douyin Fetcher - 视频下载

**
---

## 快速开始

```
输入抖音链接 → 获取视频ID → 浏览器提取视频 URL → 下载（可能需合并）
```

---

## Step 1: 解析链接

```bash
curl.exe -sL -o NUL -w "%{url_effective}" "https://v.douyin.com/xxx/"
# 输出: https://www.douyin.com/video/7612345678901234567
```

提取视频ID：`7612345678901234567`

---

## Step 2: 打开浏览器

```
browser(action='open', profile='openclaw', url='https://www.douyin.com/video/{视频ID}')
```

等待 10-15 秒让页面加载完成。

---

## Step 3: 提取视频 URL

### 3.1 调用方式

⚠️ **`act` 操作必须用 `request` 嵌套格式**，直接传 `fn` 会报错 `request required`：

```
browser(action='act', targetId='页面ID', request={"kind": "evaluate", "fn": "JS代码"})
```

❌ 错误写法：`browser(action='act', targetId='...', fn='JS代码')`
✅ 正确写法：`browser(action='act', targetId='...', request={"kind": "evaluate", "fn": "JS代码"})`

### 3.2 提取 JS 代码

```javascript
(() => {
    const entries = performance.getEntriesByType('resource');
    const videoEntries = entries.filter(e => {
        const name = e.name.toLowerCase();
        return name.includes('douyinvod') && 
               (name.includes('media-video') || name.includes('media-audio') || name.includes('video_mp4'));
    });
    return videoEntries.map(e => e.name);
})()
```

### 3.3 返回结果判断

**情况A：DASH 分离流（常见）**
```
[
  "https://v26-web.douyinvod.com/.../media-video-hvc1/...",
  "https://v26-web.douyinvod.com/.../media-audio-und-mp4a/..."
]
```
- 需要分别下载视频流和音频流，然后合并
- `media-video` → 视频流（无音频）
- `media-audio` → 音频流

**情况B：完整 MP4（部分视频）**
```
[
  "https://v26-web.douyinvod.com/.../?mime_type=video_mp4&..."
]
```
- 直接是完整视频，无需合并
- 下载后直接可用

---

## Step 4: 下载

### 情况A：分离流

```bash
# 下载视频流
curl.exe -L -H "Referer: https://www.douyin.com/" -o "/path/to/temp/douyin\video.mp4" "<视频流URL>"

# 下载音频流
curl.exe -L -H "Referer: https://www.douyin.com/" -o "/path/to/temp/douyin\audio.mp4" "<音频流URL>"
```

### 情况B：完整 MP4

```bash
curl.exe -L -H "Referer: https://www.douyin.com/" -o "/path/to/temp/douyin\video.mp4" "<完整URL>"
```

---

## Step 5: 合并（仅保存完整视频时需要）

⚠️ **教训**：DASH 分离流下载后已有独立的音频文件 `audio.mp4`，转录时直接传给 Whisper ASR 服务即可。合并只用于最终保存完整视频。

```bash
# 转录用：直接传给 Whisper ASR（无需处理）
curl.exe -X POST "http://localhost:PORT/asr" -F "audio_file=@/path/to/temp/douyin\audio.mp4"

# 保存用：需要完整视频时用 ffmpeg 合并
ffmpeg -i "/path/to/temp/douyin\video.mp4" -i "/path/to/temp/douyin\audio.mp4" -c:v copy -c:a aac "/path/to/temp/douyin\merged.mp4" -y
```

---

## 输出

| 文件 | 说明 |
|------|------|
| `/path/to/temp/douyin\video.mp4` | 视频流或完整视频 |
| `/path/to/temp/douyin\audio.mp4` | 音频流（仅情况A）|
| `/path/to/temp/douyin\merged.mp4` | 合并后的完整视频（仅情况A）|

---

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| JS 返回空数组 | 页面未加载完 | 等待 15-20 秒后重试，或先 snapshot 确认 |
| 下载 403 | URL 过期 | 重新获取视频 URL |
| 只有视频没有音频 | 忘记下载音频流 | 确保同时下载 media-audio |
| 找不到 DASH 流 | 该视频是完整 MP4 | 扩展搜索条件，找包含 `video_mp4` 的 URL |
| browser act 报错 "request required" | 格式错误 | 必须用 `request={"kind": "evaluate", "fn": "..."}` 嵌套格式 |

---

## 排查流程

提取 URL 失败时：

1. **确认页面已加载**
   ```
   browser(action='snapshot', targetId='页面ID')
   ```
   检查是否有视频播放器元素

2. **扩大搜索范围**
   ```javascript
   // 查看所有 douyinvod 相关资源
   entries.filter(e => e.name.includes('douyinvod')).map(e => e.name)
   ```

3. **检查视频时长**
   - 长视频（>2分钟）可能需要更长时间加载

---

## 前置条件

- curl 已安装
- ffmpeg 已安装（用于视频合并）
- 浏览器可用（openclaw profile）

---

## 已知限制

1. **视频 URL 有时效性** — 获取后立即下载，不要拖延
2. **需要浏览器** — openclaw profile 必须可用
3. **图文笔记** — 链接格式为 `/note/`，不适用此模块
4. **部分视频无分离流** — 直接是完整 MP4，无需合并

---

## 文件流转

### 临时目录

所有中间文件存放在 `/path/to/temp/douyin\`：

| 阶段 | 文件 | 保留 |
|------|------|------|
| 下载 | video.mp4, audio.mp4, merged.mp4 | ⚠️ 可选保留 merged.mp4 |
| 转录 | audio.wav | ❌ 转录后删除 |

### 最终位置

| 内容 | 位置 | 条件 |
|------|------|------|
| 转录稿 | `/path/to/knowledge\transcripts\{主题}-完整转录.md` | 必保存 |
| 视频 | `/path/to/videos\tutorials\{主题}.mp4` | 用户要求时保存 |

### 清理规则

转录完成后：
1. 删除 `audio.wav`（转录中间产物）
2. 保留或删除 `video.mp4/audio.mp4/merged.mp4`（根据用户需求）
3. 如保存视频 → 移动到 `/path/to/videos\` 后删除临时副本

### 浏览器处理

下载完成后关闭浏览器：
```
browser(action='stop')
```

释放资源，避免占用内存。

---

## 备用脚本

`scripts/` 目录下有历史脚本，当前流程不再使用，保留备用：

| 脚本 | 说明 | 状态 |
|------|------|------|
| `fetcher.py` | ~~TikHub API 下载脚本~~ | ❌ **已删除**（TikHub API 已废弃且包已卸载）|
| `browser_dom.py` | 浏览器 DOM 提取脚本 | ⚠️ 备用，需要 browser tool（沙盒环境不可用）|

---

## 相关模块

- **douyin-transcriber**：转录模块，用 Whisper 将视频转为文字
- **douyin-analyzer**：分析模块，提取要点生成总结
- **orchestrator**：编排模块，协调整个流程