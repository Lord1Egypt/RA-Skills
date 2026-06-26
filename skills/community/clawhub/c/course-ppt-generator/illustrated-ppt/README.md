# 图文并茂PPT生成技能

## 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install python-pptx requests Pillow

# 配置API Key
export MINIMAX_API_KEY="your-api-key"
```

### 2. 基本使用

```bash
# 使用示例生成深度学习课程PPT
cd illustrated-ppt/templates
python examples.py dl
```

### 3. 自定义PPT

```python
from scripts.illustrated_ppt import IllustratedPPTGenerator

# 初始化
generator = IllustratedPPTGenerator(api_key="your-key")

# 定义内容
slides = [
    {"type": "cover", "title": "我的PPT", "content": "副标题"},
    {"type": "toc", "title": "目录", "chapters": ["第1章", "第2章"]},
    {"type": "content", "title": "内容页", "bullets": ["要点1", "要点2"]},
    {"type": "closing", "title": "谢谢观看", "content": "作者信息"},
]

# 生成
result = generator.generate(topic="我的PPT", slides=slides, scene="education")
```

## 场景类型

| 场景 | 说明 | 适用场景 |
|------|------|----------|
| education | 蓝色科技风 | 课程课件、培训教程 |
| business | 专业商务风 | 商业演示、汇报汇报 |
| tech | 技术简约风 | 技术分享、架构说明 |
| creative | 创意活力风 | 产品介绍、营销推广 |

## 幻灯片类型

| 类型 | 说明 | 必需字段 |
|------|------|----------|
| cover | 封面页 | title, content |
| toc | 目录页 | title, chapters[] |
| content | 内容页 | title, bullets[] |
| code | 代码页 | title, content |
| summary | 总结页 | title, bullets[] |
| homework | 作业页 | title, bullets[] |
| closing | 结束页 | title, content |

## 多场景适用示例

### 教育场景 - 课程课件

```python
slides = [
    {"type": "cover", "title": "Python程序设计", "content": "本科课程"},
    {"type": "toc", "title": "目录", "chapters": ["基础语法", "数据结构", "函数", "面向对象"]},
    {"type": "content", "title": "基础语法", "bullets": ["变量与类型", "运算符", "控制流程"]},
    {"type": "code", "title": "代码示例", "content": "print('Hello World')"},
    {"type": "summary", "title": "小结", "bullets": ["掌握基础语法", "理解数据类型"]},
]
```

### 商业场景 - 产品发布

```python
slides = [
    {"type": "cover", "title": "产品发布会", "content": "2026新品发布"},
    {"type": "toc", "title": "议程", "chapters": ["产品介绍", "核心优势", "市场分析"]},
    {"type": "content", "title": "产品介绍", "bullets": ["产品背景", "核心功能"]},
    {"type": "summary", "title": "核心要点", "bullets": ["技术创新", "市场领先"]},
]
```

### 技术场景 - 架构分享

```python
slides = [
    {"type": "cover", "title": "微服务架构", "content": "云原生技术分享"},
    {"type": "toc", "title": "大纲", "chapters": ["架构设计", "服务治理", "实战案例"]},
    {"type": "code", "title": "Dockerfile示例", "content": "FROM python:3.9..."},
    {"type": "content", "title": "服务治理", "bullets": ["负载均衡", "熔断机制", "限流策略"]},
]
```

## 图文对应原则

1. **标题匹配**：配图主题与页面标题一致
2. **内容呼应**：图片内容反映页面核心要点
3. **风格统一**：全篇保持一致的视觉风格
4. **布局合理**：图片与文字比例适当（通常各占50%）