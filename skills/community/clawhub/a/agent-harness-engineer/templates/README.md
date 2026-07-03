# Agent Harness Engineer - 项目模板

三个规模级别的 Agent 项目模板:

## minimal - 极简快速原型
适合: 快速验证想法、单文件 Agent、学习目的

- 2个源文件: `main.py` + `agent.py`
- 无工具系统、无权限管理
- 单轮 LLM 调用封装
- ~100 行总代码量

## professional - 生产就绪单体
适合: 真实项目、团队协作、需工具系统的 Agent

- 完整模块分层: agent/ llm/ tools/ permissions/ utils/
- 7个Continue站点的主循环
- 抽象接口 (LLM, ToolRegistry, Permission)
- ~800 行总代码量

## enterprise - 分布式微服务
适合: 高并发、多租户、可观测性要求高的平台

- 所有 Professional 功能 + 分布式特性
- Redis 会话、PostgreSQL 持久化
- OpenTelemetry 追踪、Prometheus 指标
- Docker Compose 部署
- FastAPI API 服务
- 多 Agent 编排

## 使用方式

根据用户需求选择规模级别, AI 会填充对应模板的 TODO 标记位:

```
用户: "帮我创建一个简单的 Python Agent"
→ 自动选择 minimal 模板

用户: "搭建生产级 Agent, 需要工具系统和权限控制"
→ 自动选择 professional 模板

用户: "构建企业级 Agent 平台, 支持多租户和可观测性"
→ 自动选择 enterprise 模板
```