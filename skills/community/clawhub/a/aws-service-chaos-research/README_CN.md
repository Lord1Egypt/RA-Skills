[English](README.md) | [中文](README_CN.md)

# AWS 服务混沌工程与高可用测试研究 Skill

一个 Agent Skill，用于为任意 AWS 服务生成全面的混沌工程和高可用测试方案，采用 **Scenario Library 优先** 策略。

## 问题背景

在规划 AWS 服务的混沌工程或高可用验证时，工程师面临以下挑战：

- **FIS Scenario Library 仅限控制台** — AWS 官方预定义的复合场景（如 AZ 电力中断）无法通过 CLI 或 API 查询，很容易被遗漏。
- **FIS Action 可用性因 Region 而异** — 在 `us-east-1` 可用的 action 在 `ap-southeast-1` 可能不存在，导致错误假设。
- **即使没有原生 FIS Action，Scenario Library 仍然适用** — 像 AZ 电力中断这样的复合场景可以间接影响没有专用 FIS action 的服务（如 MSK），但用户往往不知道。
- **文档分散** — 相关信息散布在 User Guide、Blog、Well-Architected Lens、Troubleshooting 页面和 FIS 参考文档中，手动汇总耗时。

## 核心功能

1. **Scenario Library 研究** — 读取最新的 FIS Scenario Library 文档，发现 AWS 官方预定义的复合韧性测试场景。始终最先执行（最高优先级）。
2. **FIS Action 发现** — 通过 `aws fis list-actions` 查询（或回退到文档搜索）目标 Region 中服务特定的故障注入 action。
3. **文档研究** — 通过 [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) 搜索 AWS 官方文档，查找 HA/DR 最佳实践、故障模式和测试方法。
4. **报告生成** — 将所有发现编译成结构化报告，包含场景矩阵、优先级排序、实施最佳实践和可操作的下一步建议。

## 前置条件

| 依赖 | 用于 | 说明 |
|------|------|------|
| [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) | Scenario Library + 文档研究 | 提供 `aws___search_documentation`、`aws___read_documentation`、`aws___recommend` 工具 |
| AWS CLI (`aws`) | FIS Action 发现（首选） | CLI 不可用时回退到文档搜索 |

## 工作流程概览

```
步骤 1: 识别目标服务 + 确定 Region
         ↓
步骤 2: 读取 FIS Scenario Library 文档 [最高优先级]
         ├── Scenario Library 总览 + 场景参考页
         ├── 详细场景页（AZ 电力中断、AZ 应用慢速等）
         └── 提取 sub-action、资源标签、时长、前提条件
         ↓
步骤 3: 查询 FIS Action (list-actions --region)
         ├── 3a: 获取目标 Region 的全部 FIS action
         ├── 3b: 按服务关键字过滤
         └── 3c: 可选收集 cross-cutting action
         ↓
         ┌─── ≥1 个服务专用 action ────┐─── 0 个 action ────┐
         ↓                              ↓                     │
步骤 4: FIS 增强路径              步骤 5: 纯文档路径             │
         ├── 4a: 按故障域分组       ├── 5a: 6 组文档搜索        │
         ├── 4b: 服务内置故障注入    ├── 5b: 读取关键页面        │
         └── 4c: 5 组文档搜索       └── 5c: 编制替代方案        │
         ↓                              ↓                     │
         └────────────┬─────────────────┘                     │
                      ↓
步骤 6: 编译输出报告（7 个章节）
```

## 报告结构

每份生成的报告都包含以下 7 个章节：

| # | 章节 | 内容 |
|---|------|------|
| 1 | **执行摘要** | 服务、Region、FIS 支持状况、相关 Scenario Library 场景、核心建议 |
| 2-N | **各服务章节** | FIS 原生场景、服务内置故障注入、环境观察（无 FIS action 时为替代测试方法） |
| N+1 | **Scenario Library and Cross-Cutting** | Scenario Library 复合场景（最高优先级）、Cross-cutting actions（可选） |
| N+2 | **推荐测试优先级** | 所有场景按 P0-P3 排序并说明原因，附 FIS 实验创建提示（action + 目标占位符）方便快速创建实验 |
| N+3 | **实施最佳实践** | Stop Condition、稳态定义、DNS/连接处理、爆炸半径控制 |
| N+4 | **参考资料** | 仅来自实际搜索结果的链接（不编造） |
| N+5 | **下一步建议** | 3-4 条可操作建议 |

## 优先级指南

| 级别 | 判定标准 | 示例 |
|------|----------|------|
| **P0 必测** | Scenario Library 中直接影响目标服务的复合场景；主节点故障转移 | AZ 电力中断（含 RDS failover）、ElastiCache TestFailover |
| **P1 高** | AZ 级隔离、网络分区 | AZ 应用慢速、`network:disrupt-connectivity` |
| **P2 中** | 性能退化、只读副本故障 | 副本延迟、跨 AZ 流量慢速 |
| **P3 可选** | API 限流、跨 Region DR、cross-cutting action | `inject-api-throttle-error`、跨 Region 连接 |

## 双路径架构

Skill 根据 FIS action 可用性自动选择路径：

**FIS 增强路径**（找到 ≥1 个原生 action）：
- 按故障域分组 FIS action（实例、存储、网络、AZ、Region、API）
- 检查服务内置故障注入能力（如 Aurora `ALTER SYSTEM CRASH`、ElastiCache `test-failover`）
- 执行 5 组顺序文档搜索作为补充

**纯文档路径**（0 个原生 action）：
- 执行 6 组顺序文档搜索，覆盖 HA、DR、混沌、最佳实践、故障排查和 API 参考
- 编制间接 FIS 方法和 AWS API / 控制台替代方案
- 步骤 2 中的 Scenario Library 发现仍然适用

## 工具依赖

| 分组 | 工具 | 用途 |
|------|------|------|
| **A — Scenario Library** | `aws___read_documentation` | 读取 FIS Scenario Library 页面（仅控制台可见，无法通过 CLI 查询） |
| **B — FIS Actions** | AWS CLI `aws fis list-actions` | 首选：实时查询目标 Region 的 FIS action |
| **B — FIS Actions** | `aws___search_documentation` | 备选：CLI 不可用时搜索 FIS action 参考文档 |
| **C — 文档研究** | `aws___search_documentation` | 搜索官方文档（博客、用户指南、故障排查） |
| **C — 文档研究** | `aws___read_documentation` | 读取完整文档页面 |
| **C — 文档研究** | `aws___recommend` | 发现关联文档 |

**约束：** 所有文档研究仅使用 A/B/C 组工具，不使用 SearXNG 或其他外部搜索引擎。

## 目录结构

```
aws-service-chaos-research/
├── SKILL.md                              # Skill 主定义文件（Agent 执行指令）
├── README.md                             # 英文版 PRD / 用户文档
├── README_CN.md                          # 本文件（中文版 PRD / 用户文档）
└── references/
    ├── search-queries.md                 # 搜索查询模板 + FIS Scenario Library URL
    └── output-template.md                # 报告输出格式规范
```

## 使用示例

**单个服务：**
```
"RDS chaos testing in us-west-2"
"How to test HA of ElastiCache Redis?"
"对 EKS 做混沌测试"
```

**多个服务：**
```
"Chaos testing for EKS, RDS, MSK, and ElastiCache in us-west-2"
"帮我生成 us-east-1 区域 Aurora 和 DynamoDB 的混沌测试报告"
```

**没有 FIS Action 的服务：**
```
"How resilient is my MSK cluster?"
"OpenSearch fault injection testing"
"对 MSK 做高可用验证"
```

## 关键设计决策

1. **Scenario Library 始终优先** — FIS Scenario Library 复合场景是最真实的韧性测试，因为它们同时模拟多服务故障（如 AZ 断电同时影响计算、网络和数据库）。始终在查询单个 FIS action 之前先获取 Scenario Library。

2. **Scenario Library 是文档驱动的** — 与可以通过 `list-actions` 查询的 FIS action 不同，Scenario Library 场景仅限控制台。Skill 必须通过读取文档来发现它们，因此步骤 2 是文档获取步骤，而非 CLI 步骤。

3. **全程 Region 感知** — FIS action 可用性因 Region 而异。Skill 先确定目标 Region，所有 CLI 调用传 `--region`，输出中明确标注 Region。

4. **顺序执行 MCP 请求** — 所有文档搜索和页面读取逐一顺序执行，避免 aws-knowledge-mcp-server 的速率限制。速度较慢但可靠。

5. **Cross-cutting actions 为可选** — 网络中断、API 故障注入和 EC2 操作可以间接影响几乎任何服务。仅在相关时包含，在输出中明确标记为可选。

6. **Scenario Library 交叉引用去重** — 如果某个 FIS action 已作为 Scenario Library 复合场景的 sub-action 出现，则在 per-service 表格中标注（如 "同时是 AZ 电力中断的 sub-action"），而非重复列出。如果某服务的所有 FIS action 均被 Scenario Library 场景覆盖，则省略该服务的 FIS 原生小节，替换为一句说明指向 Scenario Library 章节。

7. **语言跟随用户** — 所有输出使用与用户对话相同的语言（中文、英文等）。

## 已知限制

- 依赖 aws-knowledge-mcp-server 的可用性；如果 MCP 服务器未配置，文档研究无法运行（FIS CLI 查询仍可使用）。
- 顺序文档采集需要约 30-60 秒（5-6 次查询 + 3-5 次页面读取）。
- Scenario Library 内容反映读取时的文档状态；新增场景需要重新读取文档。
- Skill 仅生成测试建议和报告，不会自动执行 FIS 实验或创建实验模板。
- Cross-cutting action 的相关性取决于上下文；Skill 使用启发式规则（VPC、EC2、PrivateLink）来决定是否包含。
