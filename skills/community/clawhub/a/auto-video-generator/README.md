# 🎬 Auto Video Generator

[![PyPI version](https://badge.fury.io/py/auto-video-generator.svg)](https://pypi.org/project/auto-video-generator/)
[![Python Version](https://img.shields.io/pypi/pyversions/auto-video-generator)](https://pypi.org/project/auto-video-generator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/auto-video-generator)](https://pepy.tech/project/auto-video-generator)

**Professional demo video generation from HTML pages with AI voice narration.**

Generate stunning product demos, tutorial videos, and presentation clips automatically from your web application - with zero manual effort!

---

## ✨ Features

### 🎯 Core Capabilities
- **Multi-Framework Support**: Auto-detects Vue, React, Angular + UI libraries (Ant Design, Element UI, Vuetify...)
- **8+ Component Handlers**: Table sorting, Form filling, DatePicker selection, Tree navigation...
- **AI Voice Narration**: Edge TTS with 4 voices (Chinese/English), adjustable speed & volume
- **Production-Grade**: Circuit breaker, exponential backoff retry, structured logging

### 🛠️ Usage Modes
| Mode | Description | Best For |
|------|-------------|----------|
| **CLI** | Command-line tool | CI/CD pipelines, automation scripts |
| **Python API** | Programmatic usage | Custom integrations, batch processing |
| **Web UI** | Browser interface | Non-technical users, quick demos |
| **VS Code Plugin** | IDE integration | Developers, daily workflow |

---

## 🚀 Quick Start

### Installation

```bash
# Basic installation (CLI + API)
pip install auto-video-generator

# With Web UI support
pip install "auto-video-generator[web]"

# With development tools
pip install "auto-video-generator[dev]"

# Everything
pip install "auto-video-generator[all]"
```

### CLI Usage

```bash
# Generate video from URL
avg generate https://example.com/dashboard

# Generate from local file
avg generate ./demo.html --fps 10 --quality high

# With custom voice
avg generate ./page.vue --voice zh-CN-XiaoxiaoNeural --rate "+0%"

# Start Web UI
avg web --port 8080

# Initialize new project
avg init my-demo-project

# Detect UI framework in project
avg detect ./src/
```

### Python API

```python
import asyncio
from auto_video_generator import VideoGenerator

async def main():
    # Initialize generator
    gen = VideoGenerator()
    
    # Generate video from URL
    result = await gen.generate(
        source="https://example.com/demo",
        output="./output/demo.mp4",
        options={
            "fps": 4,
            "voice": "zh-CN-YunxiNeural",
            "quality": "high"
        }
    )
    
    print(f"✅ Video generated!")
    print(f"   Path: {result.output_path}")
    print(f"   Size: {result.file_size_mb:.2f} MB")
    print(f"   Duration: {result.duration_seconds:.1f}s")

# Run async function
asyncio.run(main())
```

### Quick Sync Wrapper

```python
from auto_video_generator import generate_video_sync

# One-liner for simple cases
result = generate_video_sync("https://example.com", fps=10)
print(result.output_path)
```

### Web UI

```bash
# Start web server
avg web

# Open browser to http://localhost:5000
# Upload file or enter URL → Configure → Generate → Download
```

---

## 📖 Documentation

### Configuration Options

```yaml
# config.yaml
browser:
  headless: true          # Don't show browser window
  viewport_width: 1440     # Recording resolution width
  viewport_height: 900     # Recording resolution height

video:
  fps: 4                  # Frames per second (1-30)
  format: mp4             # Output format
  quality: high           # low / medium / high
  output_dir: ./output    # Output directory

audio:
  engine: edge_tts        # TTS engine
  voice: zh-CN-YunxiNeural # Voice selection
  rate: "-5%"             # Speech rate (-50% ~ +50%)
  volume: "+0%"           # Volume adjustment

recording:
  interaction_mode: real  # real / static / hybrid
  clip_sidebar: true      # Remove sidebar from recording
  auto_scroll: true       # Auto-scroll long pages
```

### Supported Frameworks & Components

**Auto-Detected Frameworks:**
- ✅ Vue 2/3 + Ant Design Vue
- ✅ React + Ant Design
- ✅ Element UI / Element Plus
- ✅ Vuetify (Vue 3)
- ✅ Naive UI
- ✅ Arco Design

**Component Handlers:**
| Component | Supported Actions |
|-----------|-------------------|
| **Table** | Sort, Filter, Paginate, Select Rows |
| **Form** | Fill Inputs, Toggle Switches, Submit |
| **DatePicker** | Select Date, Range Pick |
| **Tree** | Expand/Collapse, Check Nodes |
| **Upload** | File Upload Simulation |
| **Tabs** | Switch Tabs, Get Active Tab |
| **Modal/Dialog** | Open, Close, Confirm |
| **Tooltip** | Show/Hide Tooltips |

### Voice Options

| Voice ID | Language | Gender | Description |
|----------|----------|--------|-------------|
| `zh-CN-YunxiNeural` | Chinese | Male | Deep, professional tone |
| `zh-CN-XiaoxiaoNeural` | Chinese | Female | Friendly, clear pronunciation |
| `en-US-GuyNeural` | English | Male | Natural American accent |
| `en-US-JennyNeural` | English | Female | Warm, engaging tone |

---

## 🔧 Advanced Usage

### Custom Adapter Registration

```python
from auto_video_generator import AdapterFactory, BaseAdapter

class MyCustomAdapter(BaseAdapter):
    framework_name = "MyFramework"
    
    def click_button(self, page, selector):
        # Custom implementation
        pass

# Register adapter
AdapterFactory.register('my-framework', MyCustomAdapter)

# Now use it
gen = VideoGenerator()
result = await gen.generate("./page.html")
```

### Error Handling

```python
from auto_video_generator import VideoGenerator, GenerationOptions
from auto_video_generator.error_handler import CircuitBreakerConfig

options = GenerationOptions(
    fps=10,
)

gen = VideoGenerator()

try:
    result = await gen.generate(
        "https://flaky-service.com/page",
        options=options
    )
except Exception as e:
    print(f"Generation failed: {e}")
    # Automatic retry already attempted 3 times
    # Circuit breaker opened after 5 failures
```

### Performance Monitoring

```python
from auto_video_generator.performance_monitor import monitor, TimerContext

with TimerContext("page_load") as timer:
    await page.goto(url)

print(f"Page load took: {timer.duration_ms:.2f}ms")

# View all metrics
monitor.print_dashboard()
metrics = monitor.export_metrics()
```

---

## 🏗️ Project Structure

```
auto-video-generator/
├── auto_video_generator/      # Main package
│   ├── __init__.py           # Package init & exports
│   ├── cli.py                # Command-line interface
│   ├── generator.py          # Core generator class
│   ├── config.py             # Configuration management
│   ├── environment.py        # Environment detection
│   ├── adapters.py           # Framework adapters
│   └── web.py                # Web UI module
│
├── web-ui/                    # Web application
│   ├── app.py               # Flask backend
│   ├── templates/           # HTML templates
│   └── static/              # CSS/JS assets
│
├── vscode-extension/         # VS Code plugin
│   ├── src/                 # TypeScript sources
│   └── package.json         # Extension manifest
│
├── component_handlers.py     # UI component handlers
├── framework_adapters.py     # Framework adapters
├── environment_detector.py   # Environment detection
├── error_handler.py          # Error handling system
├── performance_monitor.py    # Monitoring & logging
├── config_manager.py         # Configuration manager
│
├── pyproject.toml            # Package configuration
├── README.md                 # This file
├── LICENSE                   # MIT License
└── tests/                    # Test suite
```

---

## 🧪 Testing

```bash
# Install development dependencies
pip install "auto-video-generator[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=auto_video_generator --cov-report=html

# Run specific test file
pytest tests/test_generator.py -v
```

---

## 📊 Benchmarks

| Metric | Value |
|--------|-------|
| **Generation Speed** | ~45 seconds for typical dashboard demo |
| **Output Size** | 8-15 MB (at 1440x900, 4fps) |
| **Memory Usage** | ~200-400 MB during generation |
| **Supported Browsers** | Chromium (via Playwright) |
| **Max Page Complexity** | 100+ components detected |

---

## 🔄 Changelog

### v3.0.0 (2026-05-30)
- ✨ Complete rewrite with modular architecture
- ✨ 8 new component handlers (DatePicker, Tree, Upload, etc.)
- ✨ Production-grade error handling (circuit breaker, retry)
- ✨ Performance monitoring & structured logging
- ✨ VS Code extension with visual config panel
- ✨ Web UI for non-technical users
- ✨ pip package distribution
- 🐛 Bug fixes and performance improvements

### v2.0.0
- Initial public release
- Basic video generation from HTML pages
- Edge TTS integration
- Multi-framework detection

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [Edge TTS](https://github.com/rany2/edge-tts) - Text-to-speech
- [FFmpeg](https://ffmpeg.org/) - Video encoding
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [Click](https://click.palletsprojects.com/) - CLI framework

---

## 📞 Support

- 📝 [Documentation](https://auto-video-generator.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/avg-team/auto-video-generator/issues)
- 💬 [Discussions](https://github.com/avg-team/auto-video-generator/discussions)
- 📧 Email: team@avg.dev

---

<div align="center">

**Built with ❤️ by the AVG Team**

*Generate professional demo videos effortlessly!*

</div>
