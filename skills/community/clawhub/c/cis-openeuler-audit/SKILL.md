---
name: cis-openeuler-audit
description: "审计 OpenEuler 系统与对应 RHEL CIS Benchmark 的合规差异，生成合规报告。"
---

# CIS Benchmark 合规审计 — OpenEuler

针对 OpenEuler 系统，通过版本兼容矩阵匹配对应 RHEL 版本，对照其 CIS Benchmark 进行合规审计，输出差异分析报告。

## 使用方式

```
老大，审计 OpenEuler 合规情况
老大，运行 CIS 审计
老大，检查这台机器的安全基线
```

## 工作流

1. **确定目标系统** — 确认待审计的 OpenEuler 主机及版本
2. **匹配 RHEL 基准** — 查 `references/version-matrix.md` 确定对应 CIS Benchmark 版本
3. **收集基线** — 在目标系统上运行 `scripts/collect-baseline.sh`，生成带时间戳的基线快照
4. **差异分析** — 运行 `scripts/diff-analysis.py`，比对基线结果与 CIS Benchmark 映射表中的检查项
5. **输出报告** — 生成 Markdown 格式的合规报告（通过/失败/手动验证），保存在 `reports/` 目录

## 文件结构

```
cis-openeuler-audit/
├── SKILL.md                          # 本文件 — skill 定义与工作流
├── scripts/
│   ├── collect-baseline.sh           # 在 OpenEuler 主机上收集系统基线
│   └── diff-analysis.py             # 基线 vs CIS Benchmark 差异分析
├── references/
│   ├── version-matrix.md             # OpenEuler ↔ RHEL 版本兼容矩阵
│   └── cis-rhel-benchmark-mapping.md # CIS Benchmark 检查项 ↔ OpenEuler 等效检查
└── reports/                          # 审计报告输出目录（自动生成）
```

## 设计原则

- **以脚本为主导** — SKILL.md 定义流程，具体逻辑交给脚本。模型无关。
- **配置驱动** — 映射表、版本矩阵、例外规则在 `references/` 中，不硬编码。
- **幂等执行** — 每次生成带时间戳的报告，不修改目标系统配置，只做审计。
- **增量更新** — 已有基线时，只分析有变动的部分（diff 上一次基线文件）。

## 自动化触发

| 场景 | 触发方式 |
|------|----------|
| 一次性审计 | 手动触发（通过 QQ/Signal 指令） |
| 定时巡检 | 配合 cron 定期执行 |
| CI/CD 集成 | 新节点上线后自动执行 |

## 安全注意事项

- 基线收集脚本使用 `sudo`，需确保执行用户有相应权限
- 审计报告可能包含敏感配置信息，存储时注意权限控制
- 不在未获得授权的主机上执行审计
