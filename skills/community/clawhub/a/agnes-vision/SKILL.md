---
name: agnes-vision
description: 使用 agnes-2.0-flash 多模态模型分析图片（看图 / OCR / 描述 / 识别）。当用户想用 agnes 或 agnes-2.0-flash 处理图片、把图片理解任务交给更便宜的 flash 模型、或需要与 app 中 agnes 模型结果一致时使用。运行 skill 目录下的 agnes_vision.py，将图片 base64 编码后调用 Agnes 的 OpenAI 兼容接口返回文本。
allowed-tools: Bash(python .claude/skills/agnes-vision/agnes_vision.py *) Read
---

# Agnes Vision Skill

通过 Agnes 的 `agnes-2.0-flash` 多模态模型分析图片，把模型返回的文本拿来用。

## 何时使用

- 用户明确要求用 agnes / agnes-2.0-flash 处理图片
- 想用更便宜/更快的 flash 模型批量看图
- 需要与 app 中 agnes 模型保持一致的图片理解结果
- OCR、图片描述、物体识别等任务，且希望走 agnes 接口

> 注意：Claude Code 本身已能用 Read 工具直接看图。本 skill 仅在需要走 agnes 接口时使用，不要替代 Read 用于普通看图。

## 如何使用

在项目根目录运行 skill 脚本（工作目录默认就是项目根，用相对路径）：

```bash
python .claude/skills/agnes-vision/agnes_vision.py <图片路径> [<图片路径> ...] [-p "提示词"]
```

参数：
- `图片路径`：至少一张图片，支持多张
- `-p / --prompt`：给模型的提示词（默认“请详细描述这张图片的内容。”）
- `-m / --model`：模型名（默认 `agnes-2.0-flash`）
- `-k / --key`：API key（也可用环境变量或 config.json）
- `--max-tokens`：最大输出 token（默认不设）

脚本的 **stdout 就是模型的回答**，错误信息走 stderr。直接读 stdout 即可。

## API Key 配置

按优先级查找：
1. `--key` 参数
2. 环境变量 `AGNES_API_KEY`
3. skill 目录下 `config.json`：`{"api_key": "...", "model": "...", "endpoint": "..."}`

⚠️ 真实 key 不要写进 SKILL.md，不要提交到 git。推荐环境变量；用 config.json 的话已被 `.gitignore` 忽略。

## 工作流

1. 确认图片路径存在（必要时用 Glob/Read 找）
2. 根据任务构造合适的提示词（OCR 要“保持原文”、提取数据要“输出表格”等）
3. 运行脚本，读取 stdout 即模型回答
4. 把回答整合进给用户的回复；如需追问，带上图片再次调用

## 示例

```bash
# 描述一张图
python .claude/skills/agnes-vision/agnes_vision.py photo.jpg

# 自定义提示词：把图表数据提取成表格
python .claude/skills/agnes-vision/agnes_vision.py chart.png -p "把图表里的数据提取成 markdown 表格"

# 多张图对比
python .claude/skills/agnes-vision/agnes_vision.py a.png b.png -p "对比这两张图的差异"

# OCR
python .claude/skills/agnes-vision/agnes_vision.py receipt.jpg -p "识别图中所有文字，保持原文排版"
```

## 备注

- 脚本会把图片以 base64 data URL 形式发送到 `https://apihub.agnes-ai.com/v1/chat/completions`，属于把图片内容上传给第三方服务，敏感图片慎用。
- 脚本仅用 Python 标准库，无需 pip install。
- 首次运行若被沙箱拦截网络，需允许该次调用访问 `apihub.agnes-ai.com`。
