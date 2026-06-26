---
name: clawhub-automation
description: ClawHub零代码跨生态自动化Skill | No-code cross-platform automation for ClawHub with WeChat, DingTalk, Feishu, WPS integration
---

# ClawHub 零代码跨生态自动化 Skill

让无代码基础的用户也能在3分钟内搭建跨平台自动化流程，连接微信、钉钉、飞书、WPS等国内主流生态。

## 核心功能

| 功能模块 | 说明 |
|---------|------|
| **国内生态接口对接** | 微信、钉钉、飞书、WPS、腾讯文档、阿里云盘 |
| **零代码流程配置** | 可视化拖拽，3分钟完成配置 |
| **AI流程智能生成** | 自然语言指令自动生成流程 |
| **执行监控与兜底** | 与重试降级Skill联动，成功率≥95% |
| **模板中心** | 50+高频场景模板一键复用 |

## 快速开始

```python
from scripts.workflow_engine import WorkflowEngine
from scripts.ai_flow_generator import AIFlowGenerator

# AI生成流程
ai_gen = AIFlowGenerator()
workflow = ai_gen.generate("微信收到文件自动同步到阿里云盘")

# 执行流程
engine = WorkflowEngine()
engine.run(workflow)
```

## 安装

```bash
pip install -r requirements.txt
```

## 项目结构

```
clawhub-automation/
├── SKILL.md                 # Skill说明
├── README.md                # 完整文档
├── requirements.txt         # 依赖
├── config/
│   └── connectors.yaml      # 生态连接器配置
├── scripts/                 # 核心模块
│   ├── workflow_engine.py   # 流程引擎
│   ├── connector_manager.py # 生态连接器
│   ├── ai_flow_generator.py # AI流程生成
│   ├── template_center.py   # 模板中心
│   ├── execution_monitor.py # 执行监控
│   └── permission_manager.py # 权限管理
├── templates/               # 场景模板
├── examples/                # 使用示例
└── tests/                   # 单元测试
```

## 运行测试

```bash
cd tests
python test_automation.py
```

## 详细文档

请参考 `README.md` 获取完整API文档和使用指南。