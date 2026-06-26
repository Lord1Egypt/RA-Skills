# Changelog

All notable changes to the GcadClaw skill package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-26

### Added
- 初始版本发布
- 通过 pygcadwin 实现 GstarCAD 二维图纸自然语言生成
- 支持机械零件、装配体的 DWG 自动化输出
- 强制截图反馈机制（PNG 截图不可跳过）
- 实体验证（before/after 实体状态对比）
- 修复循环：自动分类问题、最小化修复、重新验证
- 默认三视图输出（俯视图、正视图、右视图）
- 通过 PyPI 安装 pygcadwin
- 支持离心叶轮、圆形法兰、U型支架、L型支架、电子外壳、行星齿轮组、径向发动机气缸、校准块、螺旋楼梯、阶梯轴键槽等示例
- 反馈产物：brief.md、actions.jsonl、before/after_entities.json、review.png、feedback.md、.dwg
- 自动 Python 环境安装脚本（setup_python_env.py）和验证脚本（validate_env.py）
