# Auto Video Generator - VS Code Extension

[![VS Code](https://img.shields.io/badge/VS%20Code-Extension-blue.svg)](https://code.visualstudio.com/)
[![Version](https://img.shields.io/badge/version-3.0.0-green.svg)](https://github.com/your-org/auto-video-generator)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

## ✨ Features

### 🎬 One-Click Video Generation
- Generate demo videos from HTML/Vue/React files with a single click (Ctrl+Shift+V)
- Support for URL-based video generation
- PRD document to video conversion

### ⚙️ Visual Configuration Panel
- Intuitive sidebar panel for all settings
- Real-time configuration validation
- Export/import configuration templates
- Environment variable integration

### 🔍 Environment Detection
- Automatic framework detection (Vue, React, Angular, etc.)
- UI component library identification (Ant Design, Element UI, Vuetify...)
- Layout pattern analysis (sidebar, topnav, dashboard)
- Authentication method detection

### 📊 Performance Dashboard
- Real-time performance metrics visualization
- Operation timing statistics (P50/P95/P99)
- Resource usage monitoring (CPU, Memory, Disk)
- Framework usage distribution charts
- Historical operation logs

## 🚀 Quick Start

### Installation

1. **From VS Code Marketplace** (Recommended)
   ```
   Open VS Code → Extensions → Search "Auto Video Generator" → Install
   ```

2. **From Source**
   ```bash
   cd vscode-extension
   npm install
   npm run compile
   # Press F5 to launch Extension Development Host
   ```

### Basic Usage

#### 1. Generate Video from File
```
1. Open an HTML/Vue file in VS Code
2. Press Ctrl+Shift+V (or right-click → "Generate Demo Video")
3. Wait for generation to complete
4. Open the output folder to view your video!
```

#### 2. Configure Settings
```
1. Click the gear icon in the sidebar (⚙️ Configuration)
2. Adjust browser, video, audio, and recording settings
3. Click "Save Configuration"
4. Settings are automatically applied
```

#### 3. Detect Environment
```
1. Open any project folder in VS Code
2. Press Ctrl+Shift+G and select "Detect Environment"
3. View detailed detection report in output channel
4. Configuration is auto-adjusted based on detected framework
```

## 📖 Commands & Shortcuts

| Command | Shortcut | Description |
|---------|----------|-------------|
| `AVG: Generate Demo Video` | `Ctrl+Shift+V` | Generate video from active file |
| `AVG: Generate from URL` | - | Generate video from URL input |
| `AVG: Open Configuration Panel` | `Ctrl+Shift+G` | Show config sidebar |
| `AVG: Detect Environment` | - | Analyze current project |
| `AVG: Show Performance Dashboard` | - | Open metrics dashboard |
| `AVG: Export Config Template` | - | Save YAML/JSON template |

## ⚙️ Configuration Options

### Browser Settings
```jsonc
{
  "avg.browser.headless": false,
  // Run browser without UI (useful for CI/CD)

  "avg.video.fps": 4,
  // Video frame rate: 1, 2, 4, 10, 24, or 30 FPS

  "avg.audio.voice": "zh-CN-YunxiNeural",
  // TTS voice selection:
  // - zh-CN-YunxiNeural (Male Chinese)
  // - zh-CN-XiaoxiaoNeural (Female Chinese)
  // - en-US-GuyNeural (Male English)
  // - en-US-JennyNeural (Female English)

  "avg.outputDir": "./video_output"
  // Output directory for generated videos
}
```

### Advanced Configuration (via config.yaml)
```yaml
browser:
  viewport_width: 1440
  viewport_height: 900
  timeout_ms: 30000

video:
  format: mp4
  codec: libx264
  quality: high  # low, medium, high

audio:
  engine: edge_tts
  rate: "-5%"
  volume: "+0%"

recording:
  interaction_mode: real  # real, static, hybrid
  clip_sidebar: true
  auto_scroll: true

retry:
  max_attempts: 3
  base_delay_s: 0.5
  enable_circuit_breaker: true
```

## 🎯 Supported Frameworks & Components

### Frameworks (Auto-Detected)
- ✅ Vue + Ant Design Vue
- ✅ React + Ant Design
- ✅ Element UI / Element Plus
- ✅ Vuetify (Vue 3)
- ✅ Naive UI
- ✅ Arco Design

### Components (Intelligent Interaction)
| Component | Actions Supported |
|-----------|-------------------|
| **Table** | Sort, Filter, Paginate, Select Rows, Expand, Search |
| **Form** | Fill Inputs, Toggle Switches, Select Dropdowns, Submit |
| **DatePicker** | Select Date, Range Pick, Quick Options |
| **Tree** | Expand/Collapse Nodes, Check Items |
| **Upload** | Single/Multiple File Upload |
| **Tabs** | Switch Tabs, Close Tabs, Get Active Tab |
| **Modal/Dialog** | Open, Close, Confirm Actions |
| **Tooltip** | Show/Hide Tooltips |

## 📊 Performance Dashboard

Access via command: `AVG: Show Performance Dashboard`

### Metrics Tracked
- **Generation Statistics**: Total videos, success rate, avg time
- **Operation Timings**: Page load, screenshot, audio gen, encoding
- **Resource Usage**: CPU, memory, disk I/O
- **Framework Distribution**: Usage by framework type
- **Operation Log**: Recent operations with status

### Real-Time Updates
Dashboard auto-refreshes every 2 seconds when visible.

## 🔧 Development

### Project Structure
```
vscode-extension/
├── src/
│   ├── extension.ts              # Main entry point
│   ├── configPanel.ts            # Webview config panel
│   ├── videoGenerator.ts         # Video generation logic
│   ├── environmentDetector.ts    # Framework/component detection
│   └── performanceDashboard.ts   # Metrics visualization
├── package.json                  # Extension manifest
├── tsconfig.json                 # TypeScript config
└── README.md                     # This file
```

### Build & Debug
```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch mode (auto-recompile on changes)
npm run watch

# Launch debugger
# Press F5 in VS Code with this project open
# This opens Extension Development Host

# Package for distribution
npx vsce package
# Creates .vsix file for manual installation
```

### Testing
```bash
# Run tests
npm test

# Lint code
npm run lint
```

## 🌐 Integration

### CI/CD Pipeline Integration
```yaml
# GitHub Actions example
- name: Generate Demo Video
  uses: ./vscode-extension
  with:
    url: 'https://staging.example.com'
    voice: 'en-US-GuyNeural'
    fps: 10
    output: './demo-videos/build-${{ github.sha }}.mp4'

- name: Upload Artifact
  uses: actions/upload-artifact@v3
  with:
    name: demo-video
    path: ./demo-videos/*.mp4
```

### API Usage (Programmatic)
```typescript
import { VideoGeneratorManager } from 'vscode-extension/src/videoGenerator';

const generator = new VideoGeneratorManager(context);

// From file
const outputPath = await generator.generateFromFile('./demo.html');

// From URL
const outputPath = await generator.generateFromURL('https://example.com');

// From PRD
const outputPath = await generator.generateFromPRD('./requirements.prd');
```

## 🐛 Troubleshooting

### Common Issues

**Q: Video generation fails with "Browser not found"**
```
A: Ensure Playwright browsers are installed:
   npx playwright install chromium
```

**Q: Audio is not generated**
```
A: Check internet connection (Edge TTS requires network access)
   Or switch to local engine: set avg.audio.engine to "sapi"
```

**Q: Environment detection shows "Unknown"**
```
A: Make sure workspace folder contains package.json
   For vanilla JS projects, create config.yaml manually
```

**Q: Performance dashboard shows no data**
```
A: Generate at least one video first
   Data appears after first successful generation
```

### Getting Help
- 📝 [Documentation](https://github.com/your-org/auto-video-generator#readme)
- 🐛 [Issue Tracker](https://github.com/your-org/auto-video-generator/issues)
- 💬 [Discussions](https://github.com/your-org/auto-video-generator/discussions)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 👥 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

**Built with ❤️ by the AVG Team**

*Generate professional demo videos effortlessly with Auto Video Generator!*
