# Edict - 三省六部制多智能体编排系统

## 简介

Edict 是一个仿唐制三省六部制的 OpenClaw 多智能体编排与治理系统，提供9个专业AI智能体、实时仪表板、模型配置和完整审计跟踪。

## 快速开始

```bash
# 安装
pip install edict-openclaw

# 或使用
skillhub install edict
```

```python
from edict import EdictSystem

# 初始化
edict = EdictSystem()

# 启动治理体系
edict.launch_governance(
    dashboard=True,
    audit=True,
    auto_scale=True
)
```

## 系统架构

- **三省**: 中书省(决策)、门下省(审核)、尚书省(执行)
- **六部**: 吏部(人事)、户部(财务)、礼部(规范)、兵部(安全)、刑部(合规)、工部(工程)

## 文档

详见 [SKILL.md](./SKILL.md)

## 许可证

MIT License
