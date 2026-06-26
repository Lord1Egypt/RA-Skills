# CI/CD Pipeline Toolkit | CI/CD流水线工具包

English | [中文](#中文文档)

## Overview

CI/CD Pipeline Toolkit is a comprehensive DevOps automation framework supporting GitHub Actions, GitLab CI, and Jenkins. It simplifies the creation, management, and monitoring of continuous integration and deployment pipelines.

## Features

- 🔄 **Multi-Platform Support**: GitHub Actions, GitLab CI, Jenkins
- 🚀 **Automated Workflow Generation**: Generate CI/CD configs from templates
- 📊 **Pipeline Monitoring**: Track execution status across platforms
- 🎯 **Smart Deployment**: Automated environment-specific deployments
- 🔧 **Customizable Templates**: Pre-built templates for common stacks

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### GitHub Actions
```python
from cicd_toolkit import GitHubActionsWorkflow

workflow = GitHubActionsWorkflow("python-ci")
workflow.add_trigger("push", branches=["main"])
workflow.add_job("test", {
    "runs-on": "ubuntu-latest",
    "steps": [
        {"uses": "actions/checkout@v4"},
        {"uses": "actions/setup-python@v4", "with": {"python-version": "3.11"}},
        {"run": "pytest"}
    ]
})
workflow.save(".github/workflows/python-ci.yml")
```

### GitLab CI
```python
from cicd_toolkit import GitLabCIConfig

config = GitLabCIConfig()
config.add_stage("build")
config.add_job("build", {"stage": "build", "script": ["npm build"]})
config.save(".gitlab-ci.yml")
```

## CLI Usage

```bash
# Generate workflow
python scripts/github_workflow_generator.py --name deploy --type docker

# Monitor pipeline
python scripts/pipeline_monitor.py --platform github --repo owner/repo
```

## License
MIT

---

## 中文文档

## 概述

CI/CD流水线工具包是一个全面的DevOps自动化框架，支持GitHub Actions、GitLab CI和Jenkins。它简化了持续集成和部署流水线的创建、管理和监控。

## 功能特性

- 🔄 **多平台支持**: GitHub Actions、GitLab CI、Jenkins
- 🚀 **自动工作流生成**: 从模板生成CI/CD配置
- 📊 **流水线监控**: 跨平台跟踪执行状态
- 🎯 **智能部署**: 自动化环境特定部署
- 🔧 **可定制模板**: 常见技术栈的预建模板

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

见上方英文示例。

## 许可证
MIT
