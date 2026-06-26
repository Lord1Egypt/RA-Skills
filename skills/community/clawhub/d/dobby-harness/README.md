# Dobby-harness Skill

> 多 Agent 编排 · 生产级工作流 · 自进化系统

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://clawhub.ai/skills/dobby-harness)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-purple)](https://openclaw.ai)

---

## 🎯 简介

Dobby-harness 是一个完整的多 Agent 编排系统，为 OpenClaw Agent 提供：

- 💻 **编程专家能力** — 代码审查、测试生成、文档自动化
- 🦾 **Harness 编排能力** — 多 Agent 协同、任务分解、并行执行
- 🧠 **自进化能力** — WAL 持久化、模式识别、知识沉淀

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install dobby-harness
```

### 基础用法

```javascript
import { HarnessOrchestrator } from 'dobby-harness/harness/orchestrator.js';

const orchestrator = new HarnessOrchestrator();

const result = await orchestrator.execute({
  task: '分析项目代码质量',
  pattern: 'parallel',
  subTasks: [
    { task: '检查代码风格', agent: 'linter' },
    { task: '检查安全漏洞', agent: 'security' },
    { task: '检查性能问题', agent: 'performance' },
  ]
});

console.log(`完成：${result.completed}/${result.total}`);
```

---

## 📚 核心功能

### 1. 任务分解模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `parallel` | 完全并行 | 独立子任务 |
| `sequential` | 顺序执行 | 有依赖关系 |
| `map-reduce` | 映射归约 | 批量处理 + 聚合 |
| `pipeline` | 流水线 | 多阶段处理 |
| `fan-out` | 扇出探索 | 多方案对比 |

### 2. 生产工作流

- **Code Review** — 自动代码审查
- **Test Gen** — 测试用例生成
- **Doc Gen** — 文档自动生成
- **CI/CD** — 持续集成配置

### 3. 自进化系统

- **WAL Protocol** — 预写日志协议
- **Working Buffer** — 工作缓冲区
- **Pattern Recognition** — 模式识别

---

## 📖 文档

- [SKILL.md](./SKILL.md) - 技能使用说明
- [HARNESS-ARCHITECTURE.md](./HARNESS-ARCHITECTURE.md) - 核心架构设计
- [WORKFLOWS.md](./WORKFLOWS.md) - 工作流使用指南
- [SELF-IMPROVEMENT.md](./SELF-IMPROVEMENT.md) - 自进化系统
- [SECURITY-AUDIT.md](./SECURITY-AUDIT.md) - 安全审计报告
- [PUBLISH-GUIDE.md](./PUBLISH-GUIDE.md) - 发布指南

---

## 🧪 测试

```bash
# 运行测试套件
node tests/test-suite.js

# 运行演示
node examples/harness-demo.js
```

---

## 📊 性能指标

| 组件 | 平均耗时 | 说明 |
|------|---------|------|
| Orchestrator | ~50ms | 5 个子任务并行 |
| WAL | ~2ms | 单次事务 |
| Buffer | ~1ms | 单次读写 |

**测试通过率**: 100% (23+ 测试用例)

---

## 🛡️ 安全状态

- **总体评分**: 82.5/100 🟢
- **严重风险**: 0
- **高风险**: 0

详见 [SECURITY-AUDIT.md](./SECURITY-AUDIT.md)

---

## 🤝 贡献

欢迎贡献代码、文档和建议！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing`)
5. 创建 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🙏 致谢

- **作者**: Dobby 🧦
- **平台**: [OpenClaw](https://openclaw.ai)
- **社区**: [OpenClaw Discord](https://discord.com/invite/clawd)

---

## 📞 支持

- **GitHub Issues**: https://github.com/Panb-KG/dobby-harness/issues
- **ClawHub**: https://clawhub.ai/skills/dobby-harness

---

*最后更新：2026-04-18 | 版本：1.0.0*
