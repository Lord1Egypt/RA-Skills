# Audit-Ledger 文件系统交接规范

> **编码者 ↔ 审查者之间的结构化交接面。** 所有交接通过文件系统完成，不通过共享上下文传递。这是保证审查独立性的核心机制——审查者只读取交付物，不继承编码者的思考过程。

---

## 目录结构

```
.workbuddy/audit-ledger/
├── round-1/
│   ├── deliverable.md          # 编码者交付物（代码+自测+规格书引用）
│   ├── review-report.md        # 审查者报告（falsifiable receipt 集合）
│   ├── reviewer-memory.md      # 审查者私有记忆（编码者不可读）
│   └── fix-report.md           # 编码者修复报告（逐条回应审查意见）
├── round-2/
│   ├── deliverable.md          # 编码者重新交付（修复后+变更说明）
│   ├── review-report.md
│   ├── reviewer-memory.md
│   └── fix-report.md
├── round-3/
│   ├── deliverable.md
│   ├── review-report.md
│   ├── reviewer-memory.md
│   └── fix-report.md
└── final/
    └── approved-receipt.md     # 审查通过收据（含所有审查意见+修复证据）
```

---

## 交接协议

| 步骤 | 执行者 | 状态 | 动作 | 产出文件 | 读取文件 |
|------|--------|------|------|---------|---------|
| 1 | 编码者 | 编码完成 | 编码 + 自测 + 准备交付物 | `round-N/deliverable.md` | — |
| 2 | 审查者 | 待审查 | 读取交付物 + 读取上轮记忆 + 执行审查 | `round-N/review-report.md` + `round-N/reviewer-memory.md` | `round-N/deliverable.md` + `round-(N-1)/reviewer-memory.md` |
| 3 | 审查者 | 审查中 | 判定：通过 / 不通过 / Stall | 更新 `review-report.md` 顶部状态 | — |
| 4 | 编码者 | 待修复 | 读取审查报告 + 逐条修复 | `round-N/fix-report.md` | `round-N/review-report.md` |
| 5 | 编码者 | 修复中 | 修复代码 + 验证 + 准备下轮交付 | `round-(N+1)/deliverable.md` | — |
| 6 | 系统 | 循环或结束 | 检查轮次+Stall → 继续或停止 | — | — |

**流转状态机：**

```
[编码完成] → deliverable.md → [待审查]
     ↑                              ↓
[修复中] ← fix-report.md ← [待修复] ← [审查中] 审查者启动
     ↑                              ↓
[待审查] ← 修复完成 ← [修复中] ← [不通过] review-report.md
     ↑                              ↓
[通过] ← approved-receipt.md ← [通过] 🔴=0, 🟡≤3
     ↑                              ↓
[人工介入] ←──────── 第3轮仍未通过或 Stall 触发 ───┘
```

---

## 并发控制：轮次锁定机制

> **核心原则：审查者启动审查后，编码者不得修改 deliverable.md，防止"边审边改"导致审查结论失效。**

### 状态锁定规则

| 状态 | deliverable.md | review-report.md | fix-report.md | 说明 |
|------|---------------|-----------------|--------------|------|
| 待审查 | 只读（编码者可追加） | 不存在 | 不存在 | 编码者已提交，等待审查 |
| **审查中** | **只读（任何人不可修改）** | 审查者可写 | 不存在 | 审查者已启动，文件锁定 |
| 待修复 | 只读 | 只读 | 编码者可写 | 审查完成，编码者准备修复 |
| 修复中 | 只读 | 只读 | 编码者可写 | 编码者在修复中，不修改交付物 |
| 通过 | 只读 | 只读 | 只读 | 最终归档 |

### 锁定实现约定

1. **审查者启动审查时**（状态→审查中）：
   - 在 `review-report.md` 顶部写入 `LOCK: [timestamp]` 标记
   - 编码者看到 LOCK 标记后不得修改 deliverable.md
   - 违规修改视为无效，审查者可要求重新提交新轮次

2. **审查者完成审查时**（状态→待修复）：
   - 更新 `review-report.md` 顶部状态为 `STATUS: 待修复`
   - 此时 deliverable.md 仍保持只读，编码者只写 fix-report.md

3. **编码者准备下轮交付时**（状态→待审查）：
   - 创建新的 `round-(N+1)/deliverable.md`
   - 新轮次 deliverable.md 为可写，直到审查者再次锁定

---

## 文件格式规范

### 1. deliverable.md（编码者交付物）

```markdown
# 交付物：Round-[N]

## 元信息
- 功能模块：[模块名称]
- 关联规格书：[文件路径或内容摘要]
- 编码日期：[YYYY-MM-DD]
- 本轮编码者：[AI角色/人名]

## 代码变更清单

| 文件 | 变更类型 | 变更说明 |
|------|---------|---------|
| [路径] | 新增 | [描述] |
| [路径] | 修改 | [描述] |
| [路径] | 删除 | [描述] |

## 自测结果

### 测试统计
- 正向用例：X个 | 通过：X个 | 失败：0个
- 异常用例：X个 | 通过：X个 | 失败：0个
- 边界用例：X个 | 通过：X个 | 失败：0个
- 混沌注入：X个 | 通过：X个 | 失败：0个

### 覆盖率
- 行覆盖率：X%（目标：>80%）
- 分支覆盖率：X%（目标：>80%）
- 异常分支覆盖率：X%（目标：>80%）

### 手动验证
- [ ] 正向流程手动验证通过
- [ ] 异常流程手动验证通过
- [ ] 降级流程手动验证通过

## 本轮修复摘要（Round > 1 时必填）

| 审查意见ID | 审查意见摘要 | 修复方式 | 验证方式 | 状态 |
|-----------|------------|---------|---------|------|
| R-001 | [摘要] | [修改了哪行/怎么改的] | [跑测试/手动验证] | ✅已修复 |
| S-003 | [摘要] | [修改了哪行/怎么改的] | [跑测试/手动验证] | ✅已修复 |
| S-005 | [摘要] | [解释为什么不需要修复] | [依据] | 🔄争议 |

## 编码者声明
- [ ] 已执行开发前检查（历史弯路/规格书/架构约束）
- [ ] 已执行编码后检查（异常处理/测试/覆盖率）
- [ ] 已记录本轮弯路（如有）到 lessons-learned.md
```

### 2. review-report.md（审查者报告）

```markdown
# 审查报告：Round-[N]

## 审查状态
- 轮次：N/3
- 判定：[通过 / 不通过 / Stall]
- 判定理由：[一句话说明]

## 审查统计
- 审查文件数：X
- 审查代码行数：X
- 外部调用总数：X | 有异常处理：Y | 缺失：Z
- catch块总数：X | 有效处理：Y | 假处理：Z
- 异常场景 vs 正向场景：X:Y（目标：≥1:1）
- 🔴阻塞项：X | 🟡建议项：Y | 💭小改进：Z

## 敏感信息扫描（审查者输出前必做）

> **审查者在完成 review-report.md 前，必须扫描以下敏感信息，发现后立即替换为 `[REDACTED]` 或删除。**

| 扫描项 | 风险 | 处理方式 |
|--------|------|---------|
| API密钥 / token / secret | 泄露可导致未授权访问 | 替换为 `[REDACTED]`，不显示任何实际字符 |
| 数据库连接字符串 | 泄露可导致数据泄露 | 替换为 `[REDACTED]` |
| 服务器内部路径 | 泄露系统结构 | 替换为 `[内部路径]` |
| 用户真实数据（手机号/邮箱） | 隐私泄露 | 脱敏处理：138****1234 |
| 环境变量名含敏感值 | 泄露配置信息 | 只保留变量名，值替换为 `[REDACTED]` |

- [ ] **扫描确认**：审查者已扫描报告中的敏感信息？
- [ ] **替换确认**：所有敏感信息已替换或脱敏？

## Token 预算追踪

> **每轮审查后记录预估token消耗，用于监控审查成本、优化审查效率。**

| 项目 | 预估消耗 | 说明 |
|------|---------|------|
| 审查代码行数 | X行 | 每行≈10-20 tokens |
| 审查文件数 | X个 | 每个文件≈100-200 tokens（上下文） |
| 输出审查报告 | X tokens | 阻塞项+建议项+小改进的详细描述 |
| **本轮总计** | **~X tokens** | 建议控制在3000-5000 tokens/轮 |
| 累计消耗 | X tokens | 全轮次累计 |
| 预算状态 | ✅充足/⚠️接近上限/❌超支 | 单功能预算建议≤15000 tokens |

### 审查效率指标

| 指标 | 计算公式 | 目标 |
|------|---------|------|
| 问题密度 | 阻塞项数 / 审查代码行数 | >0.5%（每200行至少1个阻塞项） |
| 审查深度 | 异常场景覆盖数 / 规格书场景数 | ≥80% |
| 修复命中率 | 上轮建议本轮修复数 / 上轮建议总数 | ≥80%（<80%说明建议不具体） |

## 🔴 阻塞项（必须修复，不通过）

### R-001 `[file:line]` [问题类型]
- **位置**：`[精确路径:行号]`
- **问题**：[一句话描述]
- **证据**：[代码片段或场景描述]
- **修复标准**：[修复后必须满足的具体条件]
- **验证方式**：[审查者如何确认已修复]
- **来源**：首次发现 / 上轮延续（R-XXX）

### R-002 ...

## 🟡 建议项（应该修复，>3个不通过）

### S-001 `[file:line]` [问题类型]
...

## 💭 小改进（锦上添花）

### N-001 `[file:line]` [问题类型]
...

## 缺失场景（规格书有但代码未处理）

| 场景 | 规格书引用 | 优先级 | 建议处理 |
|------|-----------|--------|---------|
| [场景] | F? | P0/P1 | [建议] |

## 审查者总体评价

**优点：**
- [值得肯定的地方]

**主要问题：**
- [一句话总结]

**下一步：**
- [修复方向 / 通过确认]

## Stall 检测

- 上轮 🔴阻塞项：[X] | 本轮 🔴阻塞项：[Y] | 变化：[X-Y]
- 上轮 🟡建议项：[X] | 本轮 🟡建议项：[Y] | 变化：[X-Y]
- 重复问题（上轮提出本轮仍存在）：
  - [file:line] [问题]（上轮 R-XXX，本轮仍存在）
  - [file:line] [问题]（上轮 S-XXX，本轮仍存在）
- Stall 判定：[未触发 / 已触发：类型+原因]
```

### 3. reviewer-memory.md（审查者私有记忆）

> **⚠️ 编码者不得读取或修改此文件。这是审查者的跨轮次记忆，包含怀疑和追踪。**

```markdown
# Reviewer Memory

> 更新日期：[YYYY-MM-DD HH:MM]
> 当前追踪轮次：N/3
> 功能模块：[模块名称]
> 审查者：[AI角色/人名]

## 上一轮怀疑清单（本轮必须验证）

| 编号 | 上轮轮次 | 位置 | 怀疑内容 | 本轮验证结果 | 验证说明 | 状态 |
|------|---------|------|---------|------------|---------|------|
| S-001 | Round-1 | file:line | [描述] | ✅已修复 | [说明] | 已解决 |
| S-002 | Round-1 | file:line | [描述] | ❌仍存在 | [说明] | 持续追踪 → 升级🔴 |
| S-003 | Round-1 | file:line | [描述] | ⚠️部分修复 | [说明] | 持续追踪 |

## 新发现的可疑模式（供下轮追踪）

| 编号 | 位置 | 模式描述 | 怀疑理由 | 建议下轮重点检查 |
|------|------|---------|---------|----------------|
| S-004 | file:line | [描述] | [为什么可疑] | [检查方向] |
| S-005 | file:line | [描述] | [为什么可疑] | [检查方向] |

## 已验证有效的改进（记录成功模式）

| 改进项 | 来源弯路 | 验证轮次 | 效果 | 备注 |
|--------|---------|---------|------|------|
| [改进描述] | LL-XXX | Round-2 | ✅有效 | [说明] |

## 审查者备注（供自己参考）
- [编码者容易忽略的模式]
- [需要特别关注的模块]
- [上轮审查中发现的系统性问题]
```

### 4. fix-report.md（编码者修复报告）

```markdown
# 修复报告：Round-[N]

## 元信息
- 对应审查报告：`.workbuddy/audit-ledger/round-N/review-report.md`
- 修复日期：[YYYY-MM-DD]
- 编码者：[AI角色/人名]

## 阻塞项修复

### R-001 [审查意见摘要]
- **审查意见**：[引用原文]
- **修复方式**：[具体修改了哪些文件/行]
- **修复后代码**：[关键代码片段]
- **验证方式**：[跑测试/手动验证]
- **验证结果**：✅通过
- **状态**：✅已修复

### R-002 ...

## 建议项修复

### S-001 [审查意见摘要]
- **审查意见**：[引用原文]
- **修复方式**：[描述]
- **验证结果**：✅通过
- **状态**：✅已修复

### S-003 [审查意见摘要]
- **审查意见**：[引用原文]
- **争议说明**：[为什么认为不需要修复/改为其他方式]
- **编码者依据**：[引用规格书/设计文档/其他依据]
- **状态**：🔄争议（建议审查者确认）

## 未修复项说明

| 审查意见 | 未修复原因 | 编码者依据 | 建议处理方式 |
|---------|----------|-----------|------------|
| [意见] | [原因] | [依据] | [建议] |

## 修复后自测
- [ ] 所有原测试仍通过
- [ ] 新增修复相关测试通过
- [ ] 覆盖率未下降
- [ ] 手动验证通过

## 下一轮交付物准备
- [ ] 已更新 deliverable.md（Round-N+1）
- [ ] 已包含修复摘要
- [ ] 已包含争议说明（如有）
```

### 5. approved-receipt.md（审查通过收据）

```markdown
# 审查通过收据

> 功能模块：[模块名称]
> 最终轮次：Round-N/3
> 通过日期：[YYYY-MM-DD]

## 审查历史

| 轮次 | 判定 | 🔴阻塞项 | 🟡建议项 | 主要问题 | 修复情况 |
|------|------|---------|---------|---------|---------|
| Round-1 | 不通过 | X | Y | [摘要] | 全部修复 |
| Round-2 | 不通过 | X | Y | [摘要] | 全部修复 |
| Round-3 | 通过 | 0 | 2 | [摘要] | — |

## 最终审查统计
- 审查文件数：X
- 审查代码行数：X
- 总阻塞项发现：X（全部修复）
- 总建议项发现：Y（已修复：A，接受：B，延期：C）
- 总小改进：Z
- 异常审计覆盖率：X%

## 遗留问题（如有）
| 问题 | 严重度 | 处理方式 | 责任人 | 目标日期 |
|------|--------|---------|--------|---------|
| [描述] | 🟡 | 下个PR修复 | | [日期] |

## 审查者签字
- 审查者：[AI角色/人名]
- 判定：通过
- 签字日期：[YYYY-MM-DD]

## 编码者签字
- 编码者：[AI角色/人名]
- 确认：所有阻塞项已修复，遗留问题已记录
- 签字日期：[YYYY-MM-DD]
```

---

## 状态流转规则

```python
# 伪代码：Audit-Ledger 状态机

def calculate_similarity(prev_issues, current_issues):
    """
    计算两轮审查问题的类型相似度。
    不仅看问题数量，还看问题类型分布和位置分布。
    """
    if not prev_issues or not current_issues:
        return 0.0
    
    # 类型相似度：相同类型的问题占比
    prev_types = set(i.type for i in prev_issues)
    current_types = set(i.type for i in current_issues)
    type_intersection = len(prev_types & current_types)
    type_union = len(prev_types | current_types)
    type_similarity = type_intersection / type_union if type_union > 0 else 0.0
    
    # 位置相似度：相同位置（file:line）的问题占比
    prev_locations = set(i.location for i in prev_issues)
    current_locations = set(i.location for i in current_issues)
    loc_intersection = len(prev_locations & current_locations)
    loc_union = len(prev_locations | current_locations)
    loc_similarity = loc_intersection / loc_union if loc_union > 0 else 0.0
    
    # 综合相似度（加权平均）
    return 0.6 * type_similarity + 0.4 * loc_similarity

def determine_next_state(round_num, review_report, prev_review_report=None):
    """
    判定下一个状态（增强版：增加问题类型相似度判断）
    """
    blockers = count_blockers(review_report)
    suggestions = count_suggestions(review_report)
    
    # 通过条件
    if blockers == 0 and suggestions <= 3:
        return "APPROVED", generate_approved_receipt()
    
    # 不通过条件
    if blockers > 0 or suggestions > 3:
        # 检查是否超轮次
        if round_num >= 3:
            return "ESCALATE", "超过最大轮次，强制人工介入"
        
        # 检查 Stall（增强版）
        if prev_review_report:
            prev_blockers = count_blockers(prev_review_report)
            prev_suggestions = count_suggestions(prev_review_report)
            
            # 原始 Stall 检测：问题数相同
            if blockers == prev_blockers and suggestions == prev_suggestions:
                return "STALL", "连续2轮问题数相同，停止循环"
            
            # 增强 Stall 检测：问题类型相似度 > 80%
            similarity = calculate_similarity(prev_review_report.issues, review_report.issues)
            if similarity > 0.8:
                return "STALL", f"问题类型相似度 {similarity:.0%} > 80%，视为停滞（拆东墙补西墙）"
            
            # 检查重复问题
            repeat_issues = find_repeat_issues(review_report, prev_review_report)
            if len(repeat_issues) > 0:
                return "STALL", f"{len(repeat_issues)}个问题重复出现，标记为敷衍修复"
        
        return "REJECTED", "需要修复"
    
    return "UNKNOWN", "无法判定"
```

### Stall 判定标准总结

| Stall 类型 | 触发条件 | 说明 |
|-----------|---------|------|
| 数量停滞 | 连续2轮 🔴数量相同 且 🟡数量相同 | 最基础的Stall检测 |
| 类型相似度停滞 | 问题类型相似度 > 80% | 编码者可能将1个大问题拆分为多个小问题，本质未变 |
| 位置重复停滞 | 同一 file:line 的问题连续2轮仍存在 | 编码者敷衍修复，未真正解决 |
| 组合停滞 | 数量下降但类型相似度高 | 典型的"拆东墙补西墙"模式 |

**关键洞察：** Stall 检测不能只看"问题数是否减少"。如果问题数从 10 减到 5，但类型分布和位置分布与上一轮高度相似，说明编码者只是在"拆分问题"而非"解决问题"。

---

---

## 文件权限约定

| 文件 | 可写者 | 可读者 | 说明 |
|------|--------|--------|------|
| `deliverable.md` | 编码者 | 编码者 + 审查者 | 交付物，双方可见 |
| `review-report.md` | 审查者 | 编码者 + 审查者 | 审查报告，双方可见 |
| `fix-report.md` | 编码者 | 编码者 + 审查者 | 修复报告，双方可见 |
| `reviewer-memory.md` | 审查者 | **仅审查者** | 私有记忆，编码者不可读 |
| `approved-receipt.md` | 审查者 | 编码者 + 审查者 | 通过收据，双方可见 |

---

## 与 Ralph 模式的集成

Audit-Ledger 是 Ralph 模式的**物理实现层**。Ralph 模式定义了"循环审查的机械控制规则"，Audit-Ledger 定义了"循环审查的文件交接协议"。两者必须一起使用：

- **Ralph 模式**（在 `engineering-code-reviewer` SKILL.md 中）：定义轮次、Stall、Memory、Receipt 的逻辑规则
- **Audit-Ledger**（本文档）：定义这些规则在文件系统中的具体实现格式

**配套文件：**
- `templates.md` 第12节：Audit-Ledger 快捷模板（单文件版）
- `lessons-feedback-loop.md`：弯路闭环与审查循环的关联
