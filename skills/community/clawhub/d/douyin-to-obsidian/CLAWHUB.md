# ClawHub 上传资料 - douyin-to-obsidian

## 📦 上传信息

| 字段 | 值 |
|------|-----|
| **Slug** | `douyin-to-obsidian` |
| **Display Name** | `Douyin to Obsidian` |
| **Version** | `1.0.0` |
| **Tags** | `douyin, obsidian, transcript, whisper, video, chinese, youtube` |

## 📝 描述

抖音视频文案自动提取工具，一键将抖音视频转为结构化 Obsidian 笔记。支持绕过风控、本地 Whisper 语音识别、长视频分段处理。

### 核心功能

- ✅ 智能识别抖音短链/分享口令
- ✅ 自动绕过抖音滑动验证码
- ✅ 本地 Whisper 语音识别（零 API 成本）
- ✅ 自动生成结构化 Markdown 笔记
- ✅ 长视频自动分段处理
- ✅ FFmpeg 自动下载（无需手动配置）

## 📋 Changelog

```markdown
## v1.0.0 - 初始发布

### 新增
- 🎉 抖音短视频文案完整提取
- 🎉 支持抖音短链和分享口令智能识别
- 🎉 自动绕过抖音滑动验证码
- 🎉 本地 Whisper 语音识别（中文优化）
- 🎉 自动生成结构化 Obsidian 笔记
- 🎉 长视频自动分段处理
- 🎉 FFmpeg 自动下载和管理

### 技术特性
- 使用 Playwright 进行浏览器自动化
- 精选模态链接绕过风控
- FFmpeg 自动下载（首次运行）
- 异步架构支持并发处理
- 临时文件自动清理

### 系统要求
- Python 3.8+
- 首次运行约 200MB（Whisper 模型 + FFmpeg）
- Windows（macOS/Linux 需手动安装 FFmpeg）
```

## 📁 文件结构

```
douyin-to-obsidian/
├── SKILL.md                 # 技能描述（必需）
├── README.md                # 详细文档
├── scripts/
│   ├── run_extract.py       # 主入口脚本
│   ├── extractor.py         # 核心提取引擎
│   └── requirements.txt     # Python 依赖
└── reference/
    └── architecture.md      # 架构文档
```

**总大小**: ~30KB（不包含 FFmpeg，运行时自动下载）

## ✅ 验证清单

- [x] Python 依赖可正常安装
- [x] Playwright 可正常运行
- [x] FFmpeg 自动下载功能已实现
- [x] 输出路径可配置
- [x] 错误处理和日志已添加
- [x] 无二进制文件（符合 ClawHub 规定）
- [x] 总大小 < 50MB

## 🚀 使用方法

```bash
# 安装依赖
pip install -r scripts/requirements.txt
playwright install chromium

# 运行提取
python scripts/run_extract.py "https://v.douyin.com/xxxxx/"
```

## 📄 License

MIT-0

## 💡 注意事项

1. **首次运行**: 会自动下载 FFmpeg（约 100MB）和 Whisper 模型（约 150MB）
2. **网络要求**: 需要能访问抖音和 Gyan.dev（FFmpeg 下载源）
3. **保存路径**: 默认为 `E:\icloud\iCloudDrive\iCloud~md~obsidian\myobsidian`，可在 `run_extract.py` 中修改
