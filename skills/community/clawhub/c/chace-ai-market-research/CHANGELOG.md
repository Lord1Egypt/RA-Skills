# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-26

### Added
- 初始版本发布
- 核心编排引擎（三阶段流程：采集→分析→报告）
- crawl4ai 集成（模拟数据层）
- trendradar 集成（模拟数据层）
- product-research 框架占位
- agentmemory 可选存储
- Markdown 报告生成（微信友好格式）
- CLI 入口 (`bin/run`)
- 完整文档（SKILL.md, README.md, Requirements.md）
- MIT 许可证

### Fixed
- N/A (initial release)

### Known Issues
- 实际 MCP 调用未实现（当前使用模拟数据）
- 自动来源发现功能待开发
- product-research 分析框架未深度集成
- 缺乏 CI/CD 自动化测试

## [Planned] - Upcoming

### v0.2.0
- [ ] 真实 MCP 调用（crawl4ai + trendradar）
- [ ] 向量历史对比（vector-memory）
- [ ] 自动来源发现（Google 搜索 + 排名筛选）

### v0.3.0
- [ ] product-research 技能完整集成
- [ ] HTML 可视化报告版
- [ ] 多语言支持（中/英）

### v1.0.0
- [ ] 完整测试覆盖
- [ ] CI/CD 流水线
- [ ] ClawHub 上架审核
- [ ] Docker 容器化
