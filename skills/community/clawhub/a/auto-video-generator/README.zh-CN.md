# 🎬 自动视频生成器 (Auto Video Generator)

[![PyPI version](https://badge.fury.io/py/auto-video-generator.svg)](https://pypi.org/project/auto-video-generator/)
[![Python Version](https://img.shields.io/pypi/pyversions/auto-video-generator)](https://pypi.org/project/auto-video-generator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/auto-video-generator)](https://pepy.tech/project/auto-video-generator)

**从 HTML 页面生成专业演示视频，配备 AI 语音解说功能**

自动将您的 Web 应用转化为精美的产品演示、教程视频和演示剪辑——零人工干预！

---

## ✨ 功能特性

### 🎯 核心能力
- **多框架支持**: 自动检测 Vue、React、Angular + UI 库（Ant Design、Element UI、Vuetify...）
- **8+ 组件处理器**: 表格排序、表单填写、日期选择、树形导航...
- **AI 语音解说**: Edge TTS 支持 4 种语音（中英文），可调节语速和音量
- **生产级质量**: 熔断器、指数退避重试、结构化日志

### 🛠️ 使用模式

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| **CLI 命令行** | 命令行工具 | CI/CD 流水线、自动化脚本 |
| **Python API** | 编程接口 | 自定义集成、批量处理 |
| **Web UI 网页界面** | 浏览器操作 | 非技术人员、快速演示 |
| **VS Code 插件** | IDE 集成 | 开发者日常工作流 |

---

## 🚀 快速开始

### 安装

```bash
# 基础安装（CLI + API）
pip install auto-video-generator

# 包含 Web UI 支持
pip install "auto-video-generator[web]"

# 包含开发工具
pip install "auto-video-generator[dev]"

# 完整安装（包含所有功能）
pip install "auto-video-generator[all]"
```

### CLI 使用示例

```bash
# 从 URL 生成视频
avg generate https://example.com/dashboard

# 从本地文件生成
avg generate ./demo.html --fps 10 --quality high

# 使用自定义语音
avg generate ./page.vue --voice zh-CN-XiaoxiaoNeural --rate "+0%"

# 启动 Web UI
avg web --port 8080

# 初始化新项目
avg init my-demo-project

# 检测项目中的 UI 框架
avg detect ./src/
```

### Python API 示例

```python
import asyncio
from auto_video_generator import VideoGenerator

async def main():
    # 初始化生成器
    gen = VideoGenerator()

    # 从 URL 生成视频
    result = await gen.generate(
        source="https://example.com/demo",
        output="./output/demo.mp4",
        options={
            "fps": 4,
            "voice": "zh-CN-YunxiNeural",
            "quality": "high"
        }
    )

    print(f"✅ 视频生成完成！")
    print(f"   路径: {result.output_path}")
    print(f"   大小: {result.file_size_mb:.2f} MB")
    print(f"   时长: {result.duration_seconds:.1f} 秒")

# 运行异步函数
asyncio.run(main())
```

---

## 📖 文档

| 语言 | 文档链接 | 说明 |
|------|---------|------|
| 🇺🇸 English | [SKILL.md](./SKILL.md) | 英文完整版文档 |
| 🇨🇳 中文 | [SKILL.zh-CN.md](./SKILL.zh-CN.md) | 中文完整版文档 |

### 详细文档目录

#### 入门指南 (`docs/getting-started/`)
- [系统介绍](./docs/getting-started/introduction.md) - 架构设计与技术栈
- [快速上手](./docs/getting-started/quick-start.md) - 5 分钟入门教程
- [安装指南](./docs/getting-started/installation.md) - 环境配置与依赖
- [配置参考](./docs/getting-started/configuration.md) - YAML/JSON/环境变量

#### API 文档
- [VideoGenerator API](./docs/api/video-generator.md) - 完整编程接口参考

#### 教程与最佳实践
- [第一个视频](./docs/tutorials/01-first-video.md) - 手把手教程
- [性能优化](./docs/guides/performance-tuning.md) - 加速生成技巧
- [错误排查](./docs/troubleshooting/common-errors.md) - 常见问题解决

#### 特色功能
- [模板市场](./docs/template-gallery.md) - 预置模板使用指南
- [CI/CD 集成](./CI_CD_DOCUMENTATION.md) - GitHub Actions 工作流

---

## 🎨 模板系统

### 快速使用模板

```bash
# 查看所有可用模板
avg template list

# 预览模板效果
avg template preview finance-dashboard

# 从模板生成视频
avg generate --template landing-page-saas \
  --output saas-demo.mp4 \
  --company-name "我的产品"
```

### 内置模板库

#### 基础模板（通用场景）
| 模板 ID | 描述 | 预计时长 |
|---------|------|---------|
| `landing-page-saas` | 现代 SaaS 产品落地页 | ~25 秒 |
| `dashboard-analytics` | 数据分析仪表板 | ~30 秒 |

#### 行业模板（专业场景）
| 模板 ID | 行业分类 | 描述 |
|---------|---------|------|
| `finance-dashboard` | 金融/银行 | 金融仪表板，包含账户、交易记录、图表分析 |

---

## 🔧 支持的框架和UI库

### 自动检测框架

本工具会自动识别并适配以下技术栈：

| 框架 | UI 库 | 支持的组件数 |
|------|-------|------------|
| Vue.js | Ant Design Vue | 8+ |
| React | Ant Design | 8+ |
| Vue.js | Element UI | 8+ |
| Vue.js | Vuetify | 8+ |
| Vue.js | Naive UI | 8+ |
| Vue.js | Arco Design | 8+ |

### 支持的组件类型

✅ Table（表格）- 排序、筛选、分页  
✅ Form（表单）- 输入验证、提交  
✅ DatePicker（日期选择）- 日历选择器  
✅ Tree（树形控件）- 展开/折叠节点  
✅ Upload（文件上传）- 拖拽上传  
✅ Tabs（标签页）- 切换面板  
✅ Modal/Dialog（弹窗）- 对话框交互  
✅ Select（下拉选择）- 选项列表  

---

## 🌐 语音选项

### Edge TTS 神经网络语音（推荐）

#### 英语语音
- `en-US-JennyNeural` 👩 - 女性，专业口音（默认）
- `en-US-GuyNeural` 👨 - 男性，对话风格
- `en-GB-SoniaNeural` 👩 - 女性，英式口音

#### 中文语音
- `zh-CN-XiaoxiaoNeural` 👩 - 女性，亲切友好
- `zh-CN-YunxiNeural` 👨 - 男性，专业稳重
- `zh-CN-XiaoyiNeural` 👩 - 女性，年轻活力

**调整语速示例**:
```bash
avg generate ./page.html --voice zh-CN-XiaoxiaoNeural --rate "+20%"  # 加快
avg generate ./page.html --voice en-US-JennyNeural --rate "-10%"  # 减慢
```

---

## 🔄 CI/CD 集成示例

### GitHub Actions 自动化

```yaml
name: 生成演示视频

on:
  push:
    branches: [main]

jobs:
  generate-video:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: 配置 Python 环境
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: 安装 AVG
        run: pip install "auto-video-generator[all]"

      - name: 生成视频
        run: |
          avg generate ./dist/index.html \
            --output ./demo-video.mp4 \
            --fps 4 \
            --quality high

      - name: 上传视频产物
        uses: actions/upload-artifact@v3
        with:
          name: demo-video
          path: ./demo-video.mp4
```

---

## 📊 性能基准测试

| 页面复杂度 | FPS | 质量 | 平均耗时 | 文件大小 |
|-----------|-----|------|---------|----------|
| 简单（落地页） | 4 | medium | ~45秒 | ~15 MB |
| 中等（仪表板） | 4 | medium | ~90秒 | ~35 MB |
| 复杂（应用） | 4 | high | ~180秒 | ~80 MB |

**优化建议**:
- 降低帧率 (`--fps 2`) 可提升 50% 速度
- 使用 `--quality low` 减少文件大小
- 启用 `clip_sidebar` 裁剪录制区域

---

## ❓ 常见问题

### Q: 如何安装浏览器依赖？
```bash
playwright install chromium
```

### Q: FFmpeg 未找到怎么办？
```bash
# Windows
chocolatey install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### Q: 支持哪些 Python 版本？
Python 3.8, 3.9, 3.10, 3.11, 3.12

更多问题请查看：[常见错误排查指南](./docs/troubleshooting/common-errors.md)

---

## 🤝 参与贡献

我们欢迎各种形式的贡献！

### 开发环境搭建

```bash
# 克隆项目
git clone https://github.com/avg-team/auto-video-generator.git
cd auto-video-generator

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 代码格式化
black auto_video_generator/
isort auto_video_generator/
```

详细指南请参见：[contributing.md](./contributing.md)

---

## 📄 许可证

本项目基于 [MIT License](./LICENSE) 开源。

---

## 🙏 致谢

感谢以下开源项目的支持：

- [Playwright](https://playwright.dev/) - 浏览器自动化框架
- [Edge TTS](https://github.com/rany2/edge-tts) - 微软神经网络 TTS
- [FFmpeg](https://ffmpeg.org/) - 视频处理工具
- [Click](https://click.palletsprojects.com/) - Python CLI 框架
- [Flask](https://flask.palletsprojects.com/) - Web 应用框架

---

## 📞 联系方式

- **问题反馈**: [GitHub Issues](https://github.com/avg-team/auto-video-generator/issues)
- **功能建议**: [GitHub Discussions](https://github.com/avg-team/auto-video-generator/discussions)
- **文档网站**: https://auto-video-generator.readthedocs.io
- **邮箱**: team@avg.dev

---

<p align="center">
  <strong>Auto Video Generator</strong> - 让演示视频生成变得简单高效 🚀
</p>

<p align="center">
  <sub>版本 3.0.0 | 维护团队: AVG Team | 许可证: MIT</sub>
</p>
