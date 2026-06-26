# Phase 2 Design Document

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Douyin Video Analyzer                     │
├─────────────────────────────────────────────────────────────┤
│  Phase 1 (Foundation)          Phase 2 (Analysis)           │
│  ┌──────────────────┐          ┌──────────────────┐         │
│  │ URL Resolver     │          │ Video Downloader │         │
│  │ Web Scraper      │          │ Frame Extractor  │         │
│  │ Data Formatter   │◄────────►│ AI Visual Analyzer│        │
│  └──────────────────┘          └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Module Design

### 1. Video Downloader Module
**File**: `lib/video-downloader.js`

**Interface**:
```javascript
async function downloadVideo(videoUrl, outputDir)
// Returns: { success: boolean, filePath: string, error?: string }
```

**Implementation**:
- Use `yt-dlp` to download videos
- Save to `temp/downloads/{videoId}/`
- Support retry logic
- Handle download errors gracefully

### 2. Frame Extractor Module
**File**: `lib/frame-extractor.js`

**Interface**:
```javascript
async function extractKeyframes(videoPath, outputDir, options)
// options: { interval: number (seconds), maxFrames: number }
// Returns: { frames: string[], duration: number }
```

**Implementation**:
- Use `ffmpeg` to extract frames
- Frame interval: 1 frame per second (configurable)
- Max frames: 30 (to limit API costs)
- Save to `temp/frames/{videoId}/`

### 3. AI Visual Analyzer Module
**File**: `lib/ai-analyzer.js`

**Interface**:
```javascript
async function analyzeFrames(framePaths, zhipuApiKey, modelName = 'glm-4.6v-flash')
// modelName: 'glm-4.6v-flash' | 'glm-4.6v-flashx' | 'glm-4.6v'
// Returns: {
//   visualStyle: string,
//   textPatterns: string[],
//   colorScheme: string,
//   transitions: number,
//   hooks: string[]
// }
```

**Implementation**:
- Use Zhipu AI direct API (open.bigmodel.cn)
- Default model: `glm-4.6v-flash`
- Batch process frames (max 5 per request for vision models)
- Structured output with JSON schema
- Cache results to avoid redundant API calls

### 4. Enhanced Report Generator
**File**: `lib/utils.js` (extend existing)

**New Function**:
```javascript
function generateFullReport(phase1Data, phase2Data)
// Returns: Markdown string with complete analysis
```

## Data Flow

```
User Input (URL)
      ↓
[URL Resolver] → Resolved URL + Video ID
      ↓
┌─────────────────────────────────────┐
│ Parallel Execution                  │
│ ┌──────────────┐ ┌──────────────┐  │
│ │ Web Scraper  │ │ Video        │  │
│ │ (Phase 1)    │ │ Downloader   │  │
│ └──────────────┘ └──────────────┘  │
└─────────────────────────────────────┘
      ↓                    ↓
Basic Data          Video File
      ↓                    ↓
                      [Frame Extractor]
                              ↓
                      Frame Images
                              ↓
                      [AI Visual Analyzer]
                              ↓
                      Visual Insights
      ↓                    ↓
[Report Generator] ←── Combined Data
      ↓
Complete Markdown Report
```

## API Integration

### Zhipu GLM-4.6V Vision API

**Endpoint**: `https://open.bigmodel.cn/api/paas/v4/chat/completions`

**Models**:
- `glm-4.6v-flash` (Default) - Fast, cost-effective
- `glm-4.6v-flashx` - Enhanced quality
- `glm-4.6v` - Full capability

**Request Format**:
```json
{
  "model": "glm-4.6v-flash",
  "messages": [{
    "role": "user",
    "content": [
      { "type": "text", "text": "Analyze these video frames..." },
      { "type": "image_url", "image_url": { "url": "data:image/png;base64,..." } }
    ]
  }]
}
```

**Expected Output Structure**:
```json
{
  "visualStyle": "大字报风格",
  "textOverlays": true,
  "textFrequency": "high",
  "colorScheme": "暖橙色系",
  "sceneTransitions": 5,
  "hooks": [
    "开场使用疑问句吸引注意",
    "大字强调关键信息"
  ]
}
```

## Error Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| Download failed | Retry 3 times, then fallback to Phase 1 only |
| Frame extraction failed | Continue with available frames |
| API rate limit | Exponential backoff, max 5 retries |
| API key invalid | Clear error message, suggest checking .env |

## File Structure

```
douyin-video-analyzer/
├── lib/
│   ├── url-resolver.js        # ✅ Existing
│   ├── scraper.js             # ✅ Existing
│   ├── utils.js               # 📝 Extend
│   ├── video-downloader.js    # 🆕 New
│   ├── frame-extractor.js     # 🆕 New
│   └── ai-analyzer.js         # 🆕 New
├── scripts/
│   └── analyze.js             # 📝 Update
└── temp/                      # 🆕 Gitignored
    ├── downloads/
    └── frames/
```
