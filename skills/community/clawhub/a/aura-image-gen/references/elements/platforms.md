# Platform Specifications

多平台图片生成规格详解。

## Aspect Ratios & Dimensions

| Platform | Ratio | Pixels | Use Case |
|----------|-------|--------|----------|
| `xiaohongshu` | 3:4 | 1080×1440 | 小红书笔记首选 |
| `xiaohongshu-square` | 1:1 | 1080×1080 | 小红书备选 |
| `pinterest` | 2:3 | 1000×1500 | Pinterest 标准 Pin |
| `pinterest-long` | 1:3 | 1000×3000 | Pinterest 长图（慎用） |
| `instagram-square` | 1:1 | 1080×1080 | IG Feed 标准 |
| `instagram-portrait` | 4:5 | 1080×1350 | IG Feed 竖版（最大高度） |
| `instagram-story` | 9:16 | 1080×1920 | Story / Reels |
| `youtube-thumbnail` | 16:9 | 1280×720 | YouTube 封面 |
| `twitter-card` | 1.91:1 | 1200×628 | Twitter 卡片 |
| `facebook-post` | 1.91:1 | 1200×628 | Facebook 帖子 |

## Safe Zones

### Xiaohongshu (3:4)

```
┌─────────────────────────────┐
│                   [❤️💬⭐]   │  ← 右上角：点赞评论收藏
│                             │
│     ✓ 安全内容区域           │
│                             │
│  [标题栏覆盖区 - 底部 10%]    │  ← 避开关键信息
└─────────────────────────────┘
```

**要点**：
- 右上角 15% 区域：避开重要文字
- 底部 10% 区域：标题栏覆盖
- 左侧 5%：可能被裁剪（不同设备）

### Pinterest (2:3)

```
┌─────────────────────────┐
│  [标题前 40 字符显示区]    │  ← SEO 最重要区域
│                         │
│   ✓ 安全内容区域         │
│                         │
│   [保存按钮 - 右下角]     │
└─────────────────────────┘
```

**要点**：
- 顶部 20%：标题预览区，放核心关键词
- 右下角：保存按钮覆盖
- 文字清晰可读（移动端优先）

### Instagram Square (1:1)

```
┌─────────────────────┐
│ [❤️💬]              │  ← 左上角互动图标
│                     │
│   ✓ 安全内容区域     │
│                     │
│ [文字说明 - 下方]    │
└─────────────────────┘
```

**要点**：
- 中心聚焦构图最佳
- 四角可能被圆形头像/图标遮挡

### Instagram Story (9:16)

```
┌─────────────────┐
│ [进度条 - 顶部]  │
│                 │
│  ✓ 安全内容区域  │
│                 │
│ [输入框 - 底部]  │
└─────────────────┘
```

**要点**：
- 顶部 10%：进度条 + 用户头像
- 底部 15%：评论输入框
- 左右各 5%：边缘可能被裁剪

### YouTube Thumbnail (16:9)

```
┌────────────────────────────┐
│                            │
│    ✓ 安全内容区域           │
│    (大字 + 高对比)          │
│                            │
└────────────────────────────┘
```

**要点**：
- 小图预览场景：文字≥48pt 等效
- 高对比度：深色背景 + 亮色文字
- 人脸表情：夸张情绪更吸引点击

## Platform-Specific Tips

### Xiaohongshu
- 封面决定点击率：3 秒法则
- 系列图保持风格一致
- 避免过度 AI 感（完美对称、塑料质感）

### Pinterest
- SEO 优先：标题前 40 字符包含关键词
- 长尾词策略：具体场景 + 人群
- 垂直领域一致性：同一账号保持视觉风格

### Instagram
- Feed 美学：与前后帖子协调
- Story 互动：留白给贴纸/投票
- Reels 封面：动态预览效果

### YouTube
- 缩略图测试：缩小到 10% 看是否清晰
- 人脸 > 物体：表情吸引点击
- 数字/列表：「7 个技巧」> 「技巧」

## Color Profiles

| Platform | Color Space | Notes |
|----------|-------------|-------|
| Xiaohongshu | sRGB | 移动端优化，避免过饱和 |
| Pinterest | sRGB | 明亮鲜艳更吸引 |
| Instagram | sRGB | 滤镜文化，可后期 |
| YouTube | sRGB | 高对比度优先 |

## Export Settings

```yaml
format: PNG | JPEG
quality: 90-95%
color_profile: sRGB IEC61966-2.1
dpi: 72 (screen)
metadata: strip (reduce file size)
```

**File size limits**:
- Xiaohongshu: ≤10MB per image
- Pinterest: ≤20MB per pin
- Instagram: ≤30MB per photo
- YouTube: ≤2MB recommended (faster load)
