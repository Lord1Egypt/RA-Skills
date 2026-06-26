---
name: illustrated-ppt-generator
description: 图文并茂PPT生成技能。使用MiniMax API生成匹配图片，将图片嵌入PPT实现图文并茂效果。支持商用、教学、演讲等多场景，自动保持图文对应关系。
version: 1.0.0
author: TJMtaotao
tags: [PPT, 图文并茂, 课程课件, 商业演示, MiniMax, AI生成]
---

# 图文并茂PPT生成技能

## 功能概述

将文字内容与AI生成的配图自动结合，生成图文并茂的专业PPT。适用于：
- 课程课件制作（教育场景）
- 商业演示PPT（商务场景）
- 技术分享演讲（技术场景）
- 产品介绍展示（营销场景）

## 核心特性

- **图文匹配**：根据文字内容生成对应的配图描述
- **多场景适配**：教育/商务/技术/创意等多种风格
- **批量生成**：一次生成多张配图，自动嵌入PPT
- **蓝色科技风**：默认蓝色科技风格，统一视觉

## 前置要求

### 1. 安装依赖

```bash
pip install python-pptx requests Pillow
```

### 2. 配置API Key

```bash
export MINIMAX_API_KEY="your-api-key"
```

获取地址：https://platform.minimaxi.com/

## 使用方法

### 命令行方式

```bash
# 基本用法
python3 scripts/generate_illustrated_ppt.py "课程主题" --slides 10

# 指定输出路径
python3 scripts/generate_illustrated_ppt.py "深度学习" --output /path/to/output.pptx

# 指定场景风格
python3 scripts/generate_illustrated_ppt.py "产品介绍" --scene business

# 批量生成
python3 scripts/generate_illustrated_ppt.py "课程名称" --batch
```

### Python API

```python
from illustrated_ppt import IllustratedPPTGenerator

# 初始化
generator = IllustratedPPTGenerator(api_key="your-key")

# 生成PPT
slides_content = [
    {"title": "封面", "type": "cover", "content": "课程标题"},
    {"title": "目录", "type": "toc", "chapters": ["第1章", "第2章"]},
    {"title": "内容页", "type": "content", "bullets": ["要点1", "要点2"]},
]

result = generator.generate(
    topic="课程主题",
    slides=slides_content,
    scene="education",  # education/business/tech/creative
    style="blue_tech"   # blue_tech/clean/minimal
)

print(f"PPT已生成: {result['output_path']}")
```

## 场景类型

| 场景 | 风格 | 适用场景 |
|------|------|----------|
| education | 蓝色科技风 | 课程课件、培训教程 |
| business | 专业商务风 | 商业演示、汇报汇报 |
| tech | 技术简约风 | 技术分享、架构说明 |
| creative | 创意活力风 | 产品介绍、营销推广 |

## 输出格式

生成的PPT包含：
- 封面页（标题+副标题+机构信息）
- 目录页（章节导航）
- 内容页（左文右图布局）
- 代码页（如需代码演示）
- 总结页（要点回顾）
- 结束页（AI标识）

## 图文对应原则

1. **标题匹配**：每页配图与页面标题主题一致
2. **内容呼应**：图片内容反映页面要点
3. **风格统一**：全篇保持一致的视觉风格
4. **布局合理**：图片与文字比例适当

## 示例

### 深度学习课程PPT

```python
slides = [
    {"title": "深度学习基础课程", "type": "cover"},
    {"title": "目录", "type": "toc", "chapters": ["神经网络", "CNN", "RNN", "Transformer"]},
    {"title": "神经网络基础", "type": "content", "bullets": ["神经元模型", "激活函数", "损失函数"]},
    {"title": "卷积神经网络 CNN", "type": "content", "bullets": ["卷积层", "池化层", "经典架构"]},
]
generator.generate(topic="深度学习", slides=slides, scene="education")
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| API Key无效 | 检查MINIMAX_API_KEY环境变量 |
| 图片生成失败 | 检查网络连接和API额度 |
| PPT生成慢 | 减少slides数量或分批生成 |