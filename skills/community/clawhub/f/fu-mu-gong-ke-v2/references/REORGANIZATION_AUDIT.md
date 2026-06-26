# 技能重组与升级审计报告

## 重组目标
修复 fu-mu-gong-ke 与 parenting-psychology 的功能重复、升级不准确、遗漏问题。

## 发现的核心矛盾

### 1. 数据持久化矛盾（严重）
| 位置 | manifest声明 | 实际行为 |
|------|-------------|---------|
| SKILL.md | 不执行文件写入、数据持久化 | mood_tracker.py、goal_tracker.py 写入 ~/.hermes/still_growing/ |

**影响**：用户可能以为对话是临时的，实际会被记录，隐私风险

### 2. 代码吸收矛盾
| 位置 | manifest声明 | 升级记录描述 |
|------|-------------|-------------|
| SKILL.md | 不执行代码吸收 | CHANGELOG描述从OpenClaw/其他技能吸收代码 |

**影响**：用户期望skill是自包含的，但实际在持续吸收外部内容

### 3. 攻击性表达问题（严重）
punch-lines.md 默认用最强冲突性表达，在育儿心理支持场景中可能导致：
- 对困境父母进一步羞辱
- 破坏信任关系
- 引发防御而非改变

示例：
- ❌ "你孩子不是学会撒谎的。是你教会的。"
- ✅ "撒谎是恐惧的反应，说明家里没有说真话的安全感。"

### 4. 危机处理矛盾
声明危机要立即停止分析，但又对自伤/自杀场景继续分析性对话。

### 5. 网络请求声明矛盾
文档引用OpenAlex API但manifest声称不做外部网络请求。

---

## 修复方案

### Phase 1: 修复manifest与实际行为矛盾
1. 删除所有本地存储脚本（mood_tracker.py、goal_tracker.py等）或明确声明存储行为
2. 更新manifest描述，与实际行为一致
3. 删除所有"代码吸收"相关描述

### Phase 2: 吸收parenting-psychology有用内容
| 来源文件 | 吸收内容 | 处理方式 |
|---------|---------|---------|
| theory/觉察引擎.md | 苏格拉底追问四层架构、具身认知双系统、话语诚实度检测 | 替换现有觉察引擎 |
| theory/好父母的盲区.md | 好父母五种盲区完整框架 | 直接吸收 |
| references/红灯审核矛盾.md | 红灯规则与错位理论矛盾解决方案 | 更新SKILL.md |
| references/skill-audit-workflow.md | 标准审计序列、Git验证流程 | 替换现有文件 |
| references/positive-parenting-tools.md | 工具包（但需删除攻击性内容） | 替换punch-lines.md |
| references/quick-diagnosis.md | 快速诊断映射表 | 替换现有诊断内容 |
| references/meta-prompt-dialogue.md | 元提示对话框架 | 新增到references |
| references/punch-lines.md | 刺穿句（需完全重写表达方式） | 完全重写 |

### Phase 3: 版本升级
- 2.2.2 → 2.3.0
- 同步更新 VERSION、SKILL.md frontmatter、CHANGELOG.md

---

## 执行清单

### 高优先级（安全相关）
- [ ] 删除或重构 mood_tracker.py（数据持久化矛盾）
- [ ] 删除或重构 goal_tracker.py（数据持久化矛盾）
- [ ] 删除或重构 parenting_tracker.py（数据持久化矛盾）
- [ ] 重写 punch-lines.md（攻击性表达问题）
- [ ] 更新 SKILL.md 红灯规则（危机处理矛盾）

### 中优先级（功能优化）
- [ ] 吸收 parenting-psychology/theory/觉察引擎.md
- [ ] 吸收 parenting-psychology/theory/好父母的盲区.md
- [ ] 吸收 parenting-psychology/references/quick-diagnosis.md
- [ ] 吸收 parenting-psychology/references/meta-prompt-dialogue.md

### 低优先级（清理）
- [ ] 删除所有"代码吸收"相关升级描述
- [ ] 删除 OpenAlex API 引用（与manifest不符）
- [ ] 统一版本号

---

*审计时间: 2026-06-01*
*审计工具: clawhub security audit + 本地文件比对*