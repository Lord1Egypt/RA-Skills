# fu-mu-gong-ke 审计修复记录 v2.4.1

> 来源：NVIDIA SkillSpector 审计报告（79 findings）
> 修复日期：2026-06-23

## 审计发现与修复对照

| # | 审计发现 | 严重程度 | 修复方式 | 文件 |
|---|---------|---------|---------|------|
| 1 | `scripts/maintenance.py` 自动 git push/publish（育儿技能不应有此功能） | 🔴 高 | 删除文件 | `scripts/maintenance.py` (DELETED) |
| 2 | 数据存储路径 `~/.hermes/still_growing/` 与 SKILL.md 声明的 `SKILL_DIR/data/` 不一致 | 🔴 高 | 统一到 `SKILL_DIR/data/` | `scripts/action_planner.py` |
| 3 | 危机检测后继续分析（声明停止但实际继续） | 🔴 高 | 早退逻辑——检测到痛苦关键词立即返回转介信息 | `scripts/heartflow_defense_upgrade.py` |
| 4 | SKILL.md 声明不完整（能力范围、网络请求、存储路径） | 🔴 高 | 诚实声明能力边界、存储路径、无网络请求、无自动发布 | `SKILL.md` |
| 5 | 绝对路径 `/Users/apple/` 泄露环境结构 | 🟡 中 | 改为相对路径 | 3个文件 |
| 6 | "Child Development AI, 2024" 引用不标准（看起来像虚构） | 🟡 中 | 改为 `arXiv:2405.19275` 预印本标准引用 | `theory/心理学基础.md` |
| 7 | 缺少"不替代专业帮助"用户警告 | 🟡 中 | SKILL.md description 加警告横幅 | `SKILL.md` |
| 8 | Vague Triggers 可能假阳性触发危机路由 | 🟡 中 | 标注"用于身份识别，不单独触发危机路由" | `SKILL.md` |
| 9 | `scripts/visualize.py` 语法错误（`"""` 在 `exit(0)` 后） | 🟢 低 | 改为注释 | `scripts/visualize.py` |

## 修复模式（可复用）

### 模式1：审计报告分类修复

```
读取审计报告 → 按严重程度分类(P0/P1/P2) → 批量修复 → 逐项验证 → 版本升级 → 同步
```

**关键步骤**：
1. 先用 `search_files` 确认所有问题在代码中真实存在（避免跨版本误报）
2. 每个修复后立即验证（语法检查 + 功能验证）
3. 最终全量验证（语法/隐私/一致性）

### 模式2：育儿技能不应包含的设施

| 不应包含 | 原因 | 替代方案 |
|---------|------|---------|
| git push/publish 自动化 | 攻击面扩大，数据可能泄露 | 手动操作 |
| 用户家目录持久化 | 隐私风险，用户不知情 | 技能目录下的 data/ |
| 危机分析不停止 | 安全风险，可能延误转介 | 早退 + 仅转介 |
| 绝对路径 | 环境泄露，不可移植 | 相对路径/SKILL_DIR 变量 |

### 模式3：危机早退逻辑（关键安全修复）

```python
# Step 1: 自欺检测
deception_report = self.self_deception.detect(text)

# 心虫 shouldBeSilent: 检测到痛苦信号立即停止所有分析
if not deception_report.detected and any(p in text for p in _SILENCE_FOR_PAIN_PATTERNS):
    return UpgradeDefenseReport(
        # ... 仅含转介建议，不含任何分析性内容
        overall_recommendations=[
            "对方在痛苦中，此刻沉默或共情比分析更重要",
            "心虫 shouldBeSilent 规则触发：停止所有防御分析",
            "如需专业帮助，请拨打心理援助热线：400-161-9995"
        ],
        # 所有分析字段为空
        layers={}, child_needs={}, misalignment_analysis=[],
    )
```

## 隐私清理模式

```bash
# 搜索绝对路径
grep -r "/Users/apple/" --include="*.py" --include="*.md" .

# 搜索不正确的数据路径
grep -r "still_growing" --include="*.py" .
```

## 验证命令

```bash
# 1. Python 语法检查
for f in $(find scripts/ -name "*.py"); do
    python3 -c "compile(open('$f').read(), '$f', 'exec')" 2>&1 || echo "FAIL: $f"
done

# 2. 隐私检查
grep -r "/Users/apple/" . --include="*.py" --include="*.md" && echo "⚠️ FOUND" || echo "✅ CLEAN"

# 3. 数据路径检查
grep -r "still_growing" . --include="*.py" && echo "⚠️ FOUND" || echo "✅ CLEAN"
```
