---
name: clawhub-publish-workflow
description: "将技能发布到 ClawHub 的完整工作流程。使用时机：(1) 创建要发布的新技能，(2) 使用双评估系统评估和改进技能，(3) 修复自动+手动检查发现的问题，(4) 发布到 ClawHub，(5) 安全扫描检查技能，(6) 任何技能发布过程。本工作流程包括：捆绑的 evaluator.py（5维）、捆绑的 eval-skill.py（ISO 25010）、捆绑的 guard_scanner.py（安全扫描）、完整工具参考、25项标准评分表和分步发布指南。适用于任何想与社区分享技能的 OpenClaw 代理。包含安全扫描步骤以避免被标记为 suspicious 或 malicious。"
---

# 📦 ClawHub 发布工作流程

> 将技能发布到 ClawHub 的完整工作流程

| 信息 | 值 |
|------|-----|
| **版本** | 1.3.0 — 2026-05-07 |
| **状态** | 运行中 |

---

## 1. 目的和范围

### 目标

为任何 OpenClaw 代理提供使用双评估系统将技能发布到 ClawHub 的完整工作流程。

### 通用设计

适用于任何 OpenClaw 代理，无论集群或环境如何。

### 使用时机

| 触发器 | 行动 |
|--------|------|
| 创建要发布的新技能 | 遵循此工作流程 |
| 需要评估和改进 | 使用捆绑的双评估器 |
| 发布到 ClawHub | 遵循所有步骤 |
| 修复失败的评估 | 运行评估 + 修复 |

---

## 2. 捆绑工具

| 文件 | 系统 | 用途 |
|------|------|------|
| `evaluator.py` | 5维 | 彩色5维评估 |
| `eval-skill.py` | ISO 25010 | 自动结构检查（13项测试） |
| `references/tools.md` | — | 完整工具参考 |

### 双评估系统

```
┌─────────────────────────────────────────────┐
│         CLAWHUB 发布工作流程                │
├─────────────────────────────────────────────┤
│  1. eval-skill.py (ISO 25010)              │
│     → 自动检查（13项测试）                  │
│     → 目标：90%+ 结构分数                   │
│                                             │
│  2. evaluator.py (5维)                      │
│     → 5维度 × 20% = 100                    │
│     → 目标：70+ 分数                        │
│                                             │
│  3. 手动（25项标准）                       │
│     → ISO 25010 评分表（8个类别）           │
│     → 目标：80+ 分数                        │
└─────────────────────────────────────────────┘
```

---

## 3. 完整工作流程

### 步骤 1：创建 SKILL.md

```
任务：
1. 用英文创建 SKILL.md（ impersonal，通用）
2. 包含 name + description 的 frontmatter
3. 遵循标准技能结构
4. 使其适用于任何代理
```

**Frontmatter 模板：**
```yaml
---
name: skill-name
description: "技能描述。使用时机：(1) 触发器1，(2) 触发器2，(3) 触发器3。提供 X、Y、Z。"
---
```

### 步骤 2：自动 ISO 25010 检查

```bash
# 运行自动结构检查
python3 eval-skill.py <skill-path> --verbose

# 目标：90%+（13项中通过12项以上）
```

### 步骤 3：5维评估

```bash
# 运行完整5维评估
python3 evaluator.py <skill-path> --verbose --improve

# 目标：70+ 分数
```

### 步骤 4：手动25项标准评估

使用评分表评估：

| 类别 | 最高分 | 得分 |
|------|--------|------|
| 功能适用性 | /12 | |
| 可靠性 | /12 | |
| 性能 | /8 | |
| 可用性（AI） | /12 | |
| 可用性（人类） | /8 | |
| 安全性 | /12 | |
| 可维护性 | /12 | |
| 代理特定 | /24 | |
| **总计** | **/100** | |

### 步骤 5：修复问题

| 低分区域 | 修复方法 |
|----------|----------|
| 结构 <15 | 添加缺失部分、格式 |
| 清晰度 <15 | 添加示例、命令、约束 |
| 完整性 <15 | 添加工具、前提条件、错误 |
| 一致性 <15 | 添加样式标记、命名一致性 |
| 功能性 <15 | 修复命令语法 |

### 步骤 6：重新评估

```bash
# 继续直到达到目标
python3 eval-skill.py <path> --verbose  # 目标：90%+
python3 evaluator.py <path> --verbose    # 目标：70+
```

### 步骤 7：发布

```bash
# 登录
clawhub login --token <token> --no-browser

# 检查 slug 可用性
clawhub inspect <slug> 2>&1

# 发布
clawhub publish <path> \
  --slug <slug> \
  --name "<名称>" \
  --version 1.0.0 \
  --changelog "<更改内容>"
```

### 步骤 8：验证

```bash
clawhub inspect <slug>
```

---

## 4. 评估目标

| 系统 | 指标 | 目标 | 命令 |
|------|------|------|------|
| ISO 25010 | 结构 | 90%+ | `eval-skill.py --verbose` |
| 5维 | 分数 | 70+ | `evaluator.py --verbose` |
| 手动 | 25项标准 | 80+ | 评分表评分 |

---

## 5. 常见问题

### "Slug 已被占用"
→ 使用替代：`yourname-<skill-name>`

### "API token 无效"
→ 在 https://clawhub.com/settings/tokens 获取新 token

### "名称不匹配"
→ 重命名目录以匹配 frontmatter `name:`

### 修复后分数仍 < 70
→ 首先关注得分最低的维度

---

## 6. 边缘情况

| 情况 | 解决方案 |
|------|----------|
| 无 frontmatter | 在开头添加 `---` 和 name + description |
| 缺少工具部分 | 记录所有必需工具 |
| 无示例 | 添加至少2个具体示例 |
| SKILL.md 非常长 | 如需要则拆分到 references/ |
| scripts 目录为空 | 删除空目录 |

---

## 7. 技能结构模板

```markdown
---
name: skill-name
description: "技能描述。使用时机：(1) 触发器1，(2) 触发器2。"
---

# 技能名称

## 1. 目的和范围

## 2. 捆绑工具

## 3. 前提条件

## 4. 使用方法
```bash
# 命令
```

## 5. 示例

## 6. 约束

## 7. 错误处理

## 8. 边缘情况
```

---

_In Altum Per Partage._
📦 ClawHub 发布工作流程 v1.3
---

## 8. SECURITY SCAN (REQUIRED before publish)

**Before publishing ANY skill, scan it for security threats:**

```bash
# Run security scan
python3 guard_scanner.py <skill-path> --json

# Verify CLEAN or LOW only before publishing
# MEDIUM = manual review required
# HIGH/CRITICAL = DO NOT PUBLISH
```

**Avoid these patterns that trigger security alerts:**
See `references/security-patterns.md` for the full list.

Abstracted dangerous pattern categories:
- Code execution patterns (see reference file for details)
- Network exfiltration patterns (see reference file for details)
- Shell injection patterns (see reference file for details)
- Hardcoded agent-specific paths
- Documented malware distribution patterns

**Security scan targets:**

| Threat Level | Score | Action |
|--------------|-------|--------|
| CLEAN | 0 | ✅ Ready to publish |
| LOW | 1-19 | ✅ OK with monitoring |
| MEDIUM | 20-49 | ⚠️ Manual review first |
| HIGH | 50-79 | ❌ Fix before publish |
| CRITICAL | 80+ | ❌ DO NOT PUBLISH |

---

## 9. EXACT PUBLISH RECIPE

```bash
# 1. CHECK SECURITY FIRST
python3 guard_scanner.py <skill-path> --json
# Must return CLEAN before continuing

# 2. RUN ISO 25010 CHECKS
python3 eval-skill.py <skill-path> --verbose
# Must be 90%+ (12/13 passes)

# 3. FIX ANY FAILURES
# - Add frontmatter if missing
# - Extend description to 50+ chars with "Use when" triggers
# - Remove hardcoded paths
# - Add scripts/ if empty, remove if unused

# 4. RE-RUN UNTIL 90%+

# 5. CHECK SECURITY AGAIN
python3 guard_scanner.py <skill-path> --json

# 6. PUBLISH
clawhub publish <skill-path> \
  --slug <your-name>-<skill-name> \
  --version X.Y.Z \
  --changelog "Description of changes"

# 7. VERIFY
clawhub inspect <slug>
```

**Critical success criteria:**

1. ✅ Security scan = CLEAN (0)
2. ✅ ISO 25010 = 90%+ (12/13)
3. ✅ No hardcoded paths (especially /media/ezekiel/)
4. ✅ No agent-specific references (Merlin, Ezekiel, Morgana, Papa)
5. ✅ Frontmatter with name + description (50+ chars)
6. ✅ Description includes "Use when" triggers

_In Altum Per Recipe._
