# Cloud Product Analysis / 云产品文档对比工具

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-4.6.0-green.svg)](_meta.json)

**English** | [中文](#中文文档)

---

## What is this?

A documentation aggregation tool that automatically scrapes official cloud provider documentation (Alibaba Cloud, Huawei Cloud, AWS, Tencent Cloud) and generates structured comparison reports to assist with technical evaluation and learning.

## When to use

- **Technical evaluation**: Compare product features before cloud migration or multi-cloud deployment
- **Learning**: Understand cloud computing products across providers
- **Research**: Quickly access official documentation for competitive analysis
- **Architecture design**: Evaluate product capabilities for solution design

## Prerequisites

- Python 3.10+
- pip (Python package manager)

## Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Chromium browser for Playwright
playwright install chromium
```

## Quick Start

```bash
# Compare ECS products (Alibaba Cloud + Huawei Cloud by default)
python scripts/cloud_doc_scraper.py --product ecs

# Three-way comparison (Alibaba + Huawei + AWS)
python scripts/cloud_doc_scraper.py --product oss --providers aliyun,huawei,aws

# Include Tencent Cloud
python scripts/cloud_doc_scraper.py --product rds --providers aliyun,huawei,aws,tencent

# Save to file
python scripts/cloud_doc_scraper.py --product redis --output redis_comparison.md

# List all supported products
python scripts/cloud_doc_scraper.py --list
```

**Supported products**: ecs, oss, rds, redis, ack, fc, slb, maxcompute, pai, bailian, cdn, nas, flink, elasticsearch, dws

**Supported providers**: `aliyun`, `huawei`, `aws`, `tencent`

## Output Format

The generated markdown file contains:
- Quick comparison table (overview of key metrics)
- Original documentation content (for AI-assisted deep analysis)
- Update logs (recent feature releases)

View [sample output](https://github.com/example/sample_output.md) (example link)

## How it works

1. Dependency check (prompts for installation if missing)
2. Parse documentation navigation menu
3. Prioritize core pages (product overview > specs > pricing > scenarios)
4. Concurrent fetching with retry logic
5. Output denoised markdown suitable for AI analysis

**Fallback mechanisms**:
- HTTP fallback when JavaScript rendering fails
- Pre-configured deep links when menu parsing fails
- Domain fallback (.cn → .com for Huawei Cloud)

## Register as Claude Code Skill

To use this tool directly from Claude Code CLI:

```bash
# Copy or symlink this directory to ~/.claude/skills/
cp -r cloud-product-analysis ~/.claude/skills/

# Or create a symlink
ln -s $(pwd) ~/.claude/skills/cloud-product-analysis
```

Then in Claude Code:
```
User: Compare ECS products between Alibaba Cloud and AWS
Claude: [automatically invokes cloud-product-analysis skill]
```

## Contributing

Contributions welcome! Areas for improvement:
- Add more cloud providers (GCP, Azure)
- Add more product categories
- Improve content extraction accuracy
- Add integration tests

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

# 中文文档

## 这是什么？

云产品技术文档聚合工具，自动抓取阿里云、华为云、AWS、腾讯云官方文档，生成结构化对比资料，辅助技术选型和学习。

## 适用场景

- **技术选型**：云迁移或多云部署前对比产品特性
- **学习提升**：快速了解云计算产品知识
- **竞品研究**：对比不同云厂商的产品能力
- **架构设计**：评估产品能力以设计解决方案

## 前置要求

- Python 3.10+
- pip（Python 包管理器）

## 安装步骤

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 安装 Playwright 浏览器
playwright install chromium
```

## 快速开始

```bash
# 对比 ECS 产品（默认阿里云+华为云）
python scripts/cloud_doc_scraper.py --product ecs

# 三方对比（阿里云+华为云+AWS）
python scripts/cloud_doc_scraper.py --product oss --providers aliyun,huawei,aws

# 包含腾讯云
python scripts/cloud_doc_scraper.py --product rds --providers aliyun,huawei,aws,tencent

# 保存到文件
python scripts/cloud_doc_scraper.py --product redis --output redis_对比.md

# 查看所有支持的产品
python scripts/cloud_doc_scraper.py --list
```

**支持的产品**：ecs（云服务器）、oss（对象存储）、rds（关系数据库）、redis（缓存）、ack（容器服务）、fc（函数计算）、slb（负载均衡）、maxcompute（大数据）、pai（AI 平台）、bailian（大模型平台）、cdn、nas（文件存储）、flink（实时计算）、elasticsearch（搜索）、dws（数据仓库）

**支持的厂商**：`aliyun`（阿里云）、`huawei`（华为云）、`aws`（亚马逊云）、`tencent`（腾讯云）

## 输出格式

生成的 markdown 文件包含：
- 快速对比表格（关键指标概览）
- 原始文档内容（供 AI 辅助深度分析）
- 更新日志（近期功能发布）

查看[示例输出](https://github.com/example/sample_output.md)（示例链接）

## 工作原理

1. 依赖检测（缺失时提示安装）
2. 解析文档导航目录
3. 按优先级筛选核心页面（产品概述 > 规格参数 > 计费 > 应用场景）
4. 并发抓取，自动重试
5. 输出去噪后的 markdown，适合 AI 分析

**容错机制**：
- JavaScript 渲染失败时的 HTTP 降级
- 目录解析失败时的预配置深链
- 华为云域名降级（.cn → .com）

## 注册为 Claude Code 技能

将此工具注册到 Claude Code CLI：

```bash
# 复制或软链接到 ~/.claude/skills/
cp -r cloud-product-analysis ~/.claude/skills/

# 或创建软链接
ln -s $(pwd) ~/.claude/skills/cloud-product-analysis
```

然后在 Claude Code 中：
```
用户：对比阿里云和 AWS 的 ECS 产品
Claude：[自动调用 cloud-product-analysis 技能]
```

## 贡献指南

欢迎贡献！改进方向：
- 添加更多云厂商（GCP、Azure）
- 添加更多产品类别
- 提升内容提取准确率
- 增加集成测试

## 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE) 文件。
