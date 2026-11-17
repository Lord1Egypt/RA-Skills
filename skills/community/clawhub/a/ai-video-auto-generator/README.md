# ai-video-auto-generator

AI 短视频全自动流水线 — 从想法到成片，一键出视频。

```bash
python skills/project-generate/scripts/pipeline.py --mode auto
```

## Quick Start

### 🔥 快速尝鲜（30 秒出预览，无需 API Key）

```bash
# 在 skill 根目录执行
python skills/project-generate/scripts/pipeline.py --project ./sample --mode demo
```

自动装依赖 → ffmpeg 本地合成预览视频 → 看到效果 → 引导下一步。

### 💬 AI Agent 一键出片（推荐）

加载本 skill 后，直接向 AI Agent 描述需求：

```
"帮我做一个古代将军在现代城市醒来的短视频，紧张氛围，约30秒"
```

Agent 会自动完成：
1. 分析需求 → 生成完整 `script.json`（含角色卡/场景卡/镜头列表）
2. 运行 `optimize` 命令（OptimizerV2）做 12 维叙事自动修复
3. 调用 `--mode auto` 全自动流水线
4. 完成后通知你

> 支持多种输入：文本描述、URL、本地文件(.txt/.md/.docx)、飞书文档链接。直接发给 Agent 即可。

### 安装

skill 安装后会自动检测环境，缺失的依赖（opencv, edge-tts, PIL 等）会自动安装：

```bash
python skills/project-generate/scripts/pipeline.py --project . --mode setup
```

### 方式 1：从模板创建新项目

```bash
# 查看可用模板（在 skill 根目录执行）
python scripts/create_project.py --list-types

# 创建项目
python scripts/create_project.py --project ./my_video --template short_drama

# 一键出片
cd my_video
python skills/project-generate/scripts/pipeline.py --mode auto
```

### 方式 2：导入现有 `script.json`

```bash
# 在已有项目目录下
python skills/project-generate/scripts/pipeline.py --mode auto
```

### 方式 3：从飞书文档导入

```bash
# 在 skill 根目录执行，把飞书需求文档 URL 写入 script.json
python scripts/create_project.py --project . --feishu-doc-url <feishu_doc_url>
cd my_video
python skills/project-generate/scripts/pipeline.py --mode auto
```

## 流水线概览

```
script.json
  ↓ 叙事 12 维自动修复（ID/时长/钩子/运镜/情绪/收尾...）
  ↓ 角色资产生成 + 6 维质量验证
  ↓ 场景资产生成 + 无人检测 + 风格检测
  ↓ 首帧图生成 + 50 分制验证 + L1/L2/L3 降敏修复
  ↓ 视频提交 → 轮询 → 下载 → 55 分制验证（含运镜+情绪）
  ↓ 拼接（hyperframes / ffmpeg）
  ↓ TTS 配音 + BGM + 环境音 + 音效 + ffmpeg 多轨混音
  ↓ SRT 字幕
  → final.mp4
```

## 命令速查

```bash
# 🎮 快速尝鲜（30 秒，无需 API Key）
python skills/project-generate/scripts/pipeline.py --mode demo

# 环境检测 + 自动安装
python skills/project-generate/scripts/pipeline.py --mode setup

# 💬 告诉 AI Agent 你的需求（推荐）
#    在 WorkBuddy 中加载本 skill 后，直接描述需求即可
#    示例: "帮我做一个古代将军在现代城市醒来的短视频"

# 全自动流水线（已有 script.json 时）
python skills/project-generate/scripts/pipeline.py --mode auto

# 预检（只验证不生成）
python skills/project-generate/scripts/pipeline.py --mode validate

# 仅轮询（已有 task 的项目续跑）
python skills/project-generate/scripts/pipeline.py --mode poll --detached

# 项目状态（默认 JSON 输出，--text 人类可读）
python skills/project-generate/scripts/project_generate.py --project . status

# 单独拼接（HF 无字幕渲染 → ffmpeg 烧录字幕 → 叠加音频/BGM → final.mp4）
python skills/project-generate/scripts/project_generate.py --project . stitch --tracker local
```

## Provider 切换

默认使用 Agnes AI。修改 `script.json` 中的 `script.provider` 即可切换：

```json
{
  "script": {
    "provider": "xiaoyunqiao",
    "video_provider": "xiaoyunqiao"
  }
}
```

自定义 Provider：实现 `BaseProvider` 后通过 `register_provider()` 注册。

## 已知限制

| 限制 | 说明 |
|------|------|
| 需 API Key | 默认使用 Agnes AI，需配置 `~/.agnes-api-key`（免费无限额度）。也可切换其他 Provider。 |
| Windows 优先 | 路径处理、asyncio 事件循环针对 Windows 设计。macOS / Linux 未完整测试。 |
| OpenCV 依赖 | 视觉验证需要 `opencv-python-headless`（~50MB），`--mode setup` 会自动安装。 |
| 无实时进度条 | `auto` 模式 detach 后日志写入文件，无终端进度条。用 `tail -f auto.log` 查看。 |

## 验证体系

| 资产类型 | 检查内容 | 分值 |
|---------|---------|------|
| 角色图 | 文件+模糊+人物数量+背景+全身照+风格 | 55 分 |
| 场景图 | 人脸检测+风格检测 | pass/fail |
| 首帧图 | 文件+尺寸+模糊+人物数量+色彩 | 50 分 |
| 视频 | 时长+比例+帧质量+运镜+情绪 | 55 分 |
| 脚本 | 12 维叙事结构 | P0/P1/P2 |

## 文档

- [流水线排错指南](references/troubleshooting.md)
- [环境搭建指南](references/setup-guide.md)
- [Provider 配置参考](references/provider-config.md)
- [script.json 生成检查清单](references/script-json-checklist.md)

## License

MIT
