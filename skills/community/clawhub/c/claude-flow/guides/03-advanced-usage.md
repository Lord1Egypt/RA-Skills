# 高级用法

## 多 LLM 提供商切换

Claude-Flow 支持在不同 LLM 提供商之间切换，并自动故障切换：

```bash
# 配置多个提供商
npx ruflo@latest config set provider anthropic --api-key $ANTHROPIC_API_KEY
npx ruflo@latest config set provider openai --api-key $OPENAI_API_KEY
npx ruflo@latest config set provider google --api-key $GOOGLE_API_KEY

# 指定智能体使用特定提供商
npx ruflo@latest agent spawn coder \
  --provider anthropic \
  --model claude-opus-4-7 \
  --task "实现复杂算法"

# 经济型任务使用便宜模型
npx ruflo@latest agent spawn documenter \
  --provider anthropic \
  --model claude-haiku-4-5-20251001 \
  --task "生成 API 文档"

# 使用本地 Ollama
npx ruflo@latest agent spawn researcher \
  --provider ollama \
  --model llama3.2 \
  --task "技术调研"
```

---

## 自定义智能体

创建自己的专业智能体：

```javascript
// agents/custom-agent.js
module.exports = {
  name: "data-analyst",
  description: "专门处理数据分析和可视化任务的智能体",
  capabilities: ["data_analysis", "visualization", "statistics"],
  
  systemPrompt: `You are an expert data analyst. 
  Focus on: statistical analysis, data quality, visualization recommendations.
  Always provide actionable insights with quantified impact.`,
  
  tools: ["read_file", "write_file", "execute_code"],
  
  hooks: {
    beforeTask: async (task) => {
      // 预处理任务
      return task;
    },
    afterTask: async (result) => {
      // 后处理结果
      return result;
    }
  }
};
```

```bash
# 注册自定义智能体
npx ruflo@latest agent register agents/custom-agent.js

# 使用自定义智能体
npx ruflo@latest agent spawn data-analyst \
  --task "分析 sales.csv，找出销售下降的原因"
```

---

## 向量记忆管理

Claude-Flow 使用 HNSW 向量数据库记录成功模式：

```bash
# 查看记忆使用状态
npx ruflo@latest memory status

# 搜索相关历史模式
npx ruflo@latest memory search "authentication JWT"
npx ruflo@latest memory search "database optimization"

# 导出记忆数据库（备份）
npx ruflo@latest memory export backup-2026.json

# 清理低质量记忆
npx ruflo@latest memory prune --min-confidence 0.7

# 查看智能体学习曲线
npx ruflo@latest hooks intelligence --report
```

---

## Hook 系统

Hook 在智能体生命周期的关键节点自动触发：

```bash
# 查看当前活跃的 Hook
npx ruflo@latest hooks list

# 启用代码质量 Hook（每次代码生成后自动运行 linter）
npx ruflo@latest hooks enable code-quality

# 启用安全扫描 Hook
npx ruflo@latest hooks enable security-scan

# 查看 Hook 执行日志
npx ruflo@latest hooks logs --last 20
```

---

## 蜂群拓扑详解

```bash
# 层级拓扑（Queen 管理 Worker，适合大任务分解）
npx ruflo@latest swarm start \
  --topology hierarchical \
  --queen-agent architect \
  --worker-agents coder,tester,reviewer,documenter \
  --consensus majority \
  --task "设计和实现完整的电商订单系统"

# 环形拓扑（顺序流水线，适合步骤明确的任务）
npx ruflo@latest swarm start \
  --topology ring \
  --agents researcher,architect,coder,tester \
  --task "技术调研 → 设计 → 实现 → 测试"

# 星形拓扑（一个协调者+多个独立工作者）
npx ruflo@latest swarm start \
  --topology star \
  --coordinator-agent architect \
  --agents coder,coder,coder \   # 多个同类型智能体并行
  --task "并行实现三个独立的 API 端点"
```

---

## WASM 优化引擎

Claude-Flow 包含 WebAssembly 优化引擎，对简单任务跳过 LLM 调用：

```bash
# 查看 WASM 引擎状态
npx ruflo@latest hooks intelligence --wasm-status

# 查看 Token 节省报告（30-50% 压缩）
npx ruflo@latest hooks intelligence --token-report
```

---

## 与 Claude Code 深度集成

在 Claude Code 中，所有 Claude-Flow 功能通过自然语言触发：

```
# 以下对话会自动触发多智能体协作

我需要为新功能编写完整的测试套件，包含单元测试、集成测试和 E2E 测试

帮我重构 services/ 目录，要求：保持向后兼容，提高可测试性，添加类型注解

对 src/api/ 目录进行完整的安全审查，关注 SQL 注入、XSS、认证绕过风险
```

Claude-Flow 的 Hook 系统会自动：
1. 识别任务类型
2. 选择合适的智能体组合
3. 设置蜂群拓扑
4. 协调执行并整合结果

---

## 完成确认检查清单

- [ ] 多 LLM 提供商切换测试（可选）
- [ ] 自定义智能体注册并成功使用（可选）
- [ ] 向量记忆搜索返回相关历史模式
- [ ] 蜂群任务完成，Queen 整合所有工作成果

---

## 相关链接

- [故障排查](../troubleshooting.md)
- [GitHub](https://github.com/ruvnet/claude-flow)
- [Discord](https://discord.com/invite/dfxmpwkG2D)
