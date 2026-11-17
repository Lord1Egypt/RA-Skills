---
name: art-evaluation
description: 对上传的艺术作品进行评估，提供点评、改进建议、模拟优化图，并列出该类作品的代表艺术家及代表作品
agent_created: true
---

# Art Evaluation

## Overview
提供对多种艺术作品（素描、漫画、书法、速写、花鸟、山水、人物、油画）进行自动化评估和改进建议的能力。

## Capabilities
1. **评估**：接受上传的图像文件和作品类别，返回专业点评（构图、技法、色彩等）。
2. **改进建议**：基于点评提供具体的技术改进方案。
3. **模拟优化图**：调用图像生成模型（如 Ollama `qwen3.5:9b` + `nano-banana-pro`）生成改进后的示例图。
4. **代表艺术家&作品**：返回该类别的历史代表艺术家及其经典作品列表。

## Usage
1. 上传作品文件并指定类别（如 `素描`）。
2. 调用 `scripts/evaluate_art.py` 获取点评与建议。
3. 如需模拟图，调用 `scripts/improve_art.py`，返回生成的图像路径。
4. 参考 `references/representative_artists.md` 获取艺术家与作品信息。

## Resources

### scripts/
- `evaluate_art.py`：加载图像，使用视觉模型生成点评与建议（返回 JSON）。
- `improve_art.py`：基于点评调用图像生成模型生成优化示例图。

### references/
- `representative_artists.md`：各类别代表艺术家与作品。
- `evaluation_criteria.md`：评价指标说明（构图、笔法、色彩、表现力等）。

### assets/
- 示例艺术作品 `assets/example_sketch.png`（可供演示）。

## Implementation Notes
- 视觉模型可通过本地 Ollama 部署的 `qwen3.5:9b` 或外部图像生成服务实现。
- 生成的模拟图建议保存至项目 `art-evaluation/output/`，便于后续审阅。
- 如未安装所需模型，请参考相应技能（`ai-model-web`）进行部署。
