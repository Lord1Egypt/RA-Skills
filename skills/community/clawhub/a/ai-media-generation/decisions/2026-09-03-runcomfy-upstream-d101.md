# D101 — runcomfy 上游风险评估与 source.path 校正

**日期**：2026-09-03
**仓库**：ai-media-generation（Level A / 100，维持不变）
**类型**：上游风险调查（规则 3 派生来源复核）+ 来源元数据校正

## 背景

ai-media-generation 的 4 个子技能（image-generation / image-editing / video-generation /
video-editing）均 `source.type: derived`，全部派生自单一上游
`prime-skills/runcomfy-agent-skills`。此前维护遗留清单将其标记为「runcomfy 上游风险（pending 人工）」。
本次无人值守运行将其作为唯一可安全推进的原子单元，做只读调查 + 校正。

## 上游健康度复核（gh api，2026-09-03）

| 指标 | 值 | 结论 |
|------|-----|------|
| archived | false | 未归档 |
| disabled | false | 未禁用 |
| pushed_at | 2026-05-15 | 代码最后推送（与本地 `source.updated` 一致） |
| updated_at | 2026-09-01 | 近期有活动（star/issue 级，非代码推送） |
| visibility | public | 公开可访问 |
| stargazers | 41 / forks 9 | 小众但活跃，skills.sh 安装量 351K+（口径不同，非缺陷） |

**结论：上游未消亡「doomsday」风险不成立**——仓库活着、公开、未归档禁用，skills.sh 四条 slug 均 308 可达。

## 发现的真实缺陷：source.path 路径不准确

上游技能目录位于**仓库根级**（`ai-image-generation/`、`image-edit/`、`ai-video-generation/`、
`video-edit/`），而非 `skills/` 前缀。本地 4 个 SKILL.md 的 `source.path` 错误地写成
`skills/<name>/SKILL.md`，经 `gh api .../contents/skills/<name>/SKILL.md` 验证均返回 **Not Found**；
正确根级路径均 **OK**。属门禁盲区内隐患（审计脚本不校验 source.path 上游可达性），类似 D57/D55 靠人工抽查发现。

## 修复（纯元数据，零内容改动）

4 个子技能 `source.path` 前缀 `skills/` 移除：
- image-generation: `skills/ai-image-generation/SKILL.md` → `ai-image-generation/SKILL.md`
- image-editing: `skills/image-edit/SKILL.md` → `image-edit/SKILL.md`
- video-generation: `skills/ai-video-generation/SKILL.md` → `ai-video-generation/SKILL.md`
- video-editing: `skills/video-edit/SKILL.md` → `video-edit/SKILL.md`

`source.updated: 2026-05-15` 保持不变（与上游 pushed_at 一致，准确，不硬改）。
`source.url`（skills.sh slug）经 308 验证正确，未动。

## 剩余风险（留人工，非本单元范围）

**单点上游集中度风险**：本仓库 4/4 子技能全部派生自同一上游仓库，若上游未来归档/改名，
4 个派生技能将同时失去来源锚点。当前上游健康，暂不动作；建议人工评估是否引入第二来源或本地镜像，
属策略层面，不在无人值守自动改写范围内。

## 验证

- `audit_architecture.py --repo ai-media-generation --strict` → A/100，EXIT 0
- `audit_readme_gates.py --repo ai-media-generation --strict` → error=0/warning=0，EXIT 0
