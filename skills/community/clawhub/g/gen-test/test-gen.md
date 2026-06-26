---
name: /test-gen
id: test-gen
category: Testing
description: 为当前项目生成单元测试和 E2E 测试（五阶段：文档分析 → 签名分析 → 可测试性评审 → 单测+覆盖率 → E2E）
---

为当前项目生成测试代码。读取 test-gen skill 并按五阶段流程执行。

**Input**: `/test-gen` 后可跟可选参数：

- 无参数 — 全项目扫描
- 模块名或文件路径 — 仅针对指定范围生成测试（如 `/test-gen src/auth`）
- `--unit-only` — 只执行 Phase 1-4（跳过 E2E）
- `--review-only` — 只执行 Phase 1-3（不生成代码，仅输出评审报告）
- `--delta-only` — 仅对 git 变更文件生成测试和变更行覆盖率

参数可组合：`/test-gen src/auth --unit-only`

**Steps**

1. **解析参数**

   从输入中提取：
   - `target`：模块名/文件路径/目录（可选，默认全项目）
   - `mode`：`full`（默认）/ `unit-only` / `review-only` / `delta-only`

   如果无法解析，使用 AskQuestion 让用户选择：

   ```
   请选择测试生成模式：
   - 完整模式（单测 + E2E）
   - 仅单测（跳过 E2E）
   - 仅评审（不生成代码）
   - 仅变更文件（基于 git diff）
   ```

2. **加载 test-gen skill**

   读取 test-gen skill 的 SKILL.md，按其指令执行。

   如果指定了 `target`：
   - Phase 1 的设计文档分析范围缩小到 target 相关模块
   - Phase 2 的签名扫描仅覆盖 target 中的函数
   - Phase 3-5 顺延范围缩减

3. **执行五阶段流程**

   按 test-gen skill 中定义的五阶段顺序执行：

   | 阶段 | full | unit-only | review-only | delta-only |
   |------|------|-----------|-------------|------------|
   | Phase 1: 设计文档分析 | YES | YES | YES | SKIP |
   | Phase 2: 签名黑盒分析 | YES | YES | YES | YES (仅变更文件) |
   | Phase 3: 可测试性评审 | YES | YES | YES | YES (仅变更文件) |
   | Phase 4: 单测 + 覆盖率 | YES | YES | SKIP | YES (仅变更文件) |
   | Phase 5: E2E 测试 | YES | SKIP | SKIP | SKIP |

   每个阶段的详细步骤、STOP 确认点、产出格式均遵循 SKILL.md 的定义。

4. **delta-only 模式的特殊处理**

   - 使用 `git diff --name-only main...HEAD` 获取变更文件列表
   - 过滤出源代码文件（排除测试文件、配置文件等）
   - Phase 2-4 仅针对变更文件中的函数
   - Phase 4 强调变更行覆盖率（delta coverage），全量覆盖率作为参考

5. **产出最终报告**

   汇总所有阶段的产出，格式：

   ```markdown
   # Test Gen 报告

   **模式**: [full / unit-only / review-only / delta-only]
   **范围**: [全项目 / 指定模块]
   **阈值来源**: [.test-gen.yaml / 默认值]

   ## 摘要
   - 扫描函数: N
   - 可测: X | 需重构: Y | 跳过: Z
   - 生成测试: M 个文件
   - 总体覆盖率: XX% (目标: 80%) — 达标/未达标
   - 变更行覆盖率: XX% (目标: 90%) — 达标/未达标
   - 未达标文件: K 个

   [各阶段详细报告]
   ```

**Guardrails**
- 严格按 SKILL.md 定义的五阶段执行，不跳步不改序
- Phase 2 禁止读取函数体（黑盒铁律）
- Phase 3 遇到设计问题必须报告，不生成低质量测试
- 每个 STOP 点必须与用户确认后再继续
- review-only 模式绝不修改任何文件
- delta-only 模式需要 git 可用，否则降级为 full 模式并提示
