# SKILL.md — quality-gate-checker

## Skill 基本信息

| 项目 | 值 |
|------|---|
| Skill 名称 | quality-gate-checker |
| 版本 | v1.0.0 |
| 作者 | CQO-001 |
| 描述 | Skill质量门禁自动化检查器，执行G0-G4五级质量门禁检查，输出合规报告 |
| 适用场景 | Skill发布前质量审核、批量Skill合规检查、CI/CD质量门禁 |

---

## 触发条件

- 需要审核Skill是否符合质量标准
- CI/CD流水线需要自动质量检查
- 批量检查多个Skill的合规性

---

## 执行流程

```
1. 接收待检查Skill路径
2. 执行G0-G4五级门禁检查：
   - G0: 必备文件检查 (SKILL.md, meta.json)
   - G1: SKILL.md格式规范
   - G2: meta.json完整性和版本号合规
   - G3: 安全合规检查 (敏感信息/危险代码)
   - G4: 描述质量评估
3. 计算总分 (每级20分，满分100)
4. 生成检查报告 (quality-gate-report.md)
5. 输出通过/失败判定 (≥80分通过)
```

---

## 质量门禁标准

| 门禁 | 检查内容 | 分值 |
|-----|---------|-----|
| G0 | SKILL.md和meta.json必须存在 | 20 |
| G1 | SKILL.md包含标题、描述、触发条件、执行流程 | 20 |
| G2 | meta.json包含name/version/description/author，版本号格式x.y.z | 20 |
| G3 | 无敏感信息泄露(API key/password/token)，无危险代码(eval/exec) | 20 |
| G4 | SKILL.md内容>500字符，meta.json描述>20字符 | 20 |

**通过标准**: 总分 ≥ 80分，且G3安全门禁必须通过

---

## 使用方法

```bash
# 检查单个Skill
python quality_gate_checker.py <skill_path>

# 示例
python quality_gate_checker.py ./my-skill
```

---

## 输出说明

检查完成后生成 `quality-gate-report.md`，包含：
- 总分和通过状态
- 每项检查的详细结果
- 失败项和警告项清单
- 改进建议

---

## 依赖

- Python 3.8+
- 标准库: os, sys, json, re, pathlib

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0.0 | 2026-04-12 | 初始版本，实现G0-G4五级门禁检查 |
