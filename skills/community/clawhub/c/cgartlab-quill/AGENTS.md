# AGENTS.md — quill

> 结构化长文写作框架 Skill：两段式写作（起草期/校订期）+ 四文件思维标本（claim/evidence/audience/style）+ 全程模型驱动无脚本，把模糊的写作意图转化为可验证、可追溯的结构化长文。

> **会话约定**：开始任何工作前，先读根目录 `LESSONS.md`（本仓库从真实失误沉淀的「教训→规则」清单）并遵循其中所有规则；遇到新失误按其 §维护 追加。

> **发布**：走 GitHub Release——打 `v<版本>` tag → 建 Release → `.github/workflows/publish.yml` 自动发 ClawHub / SkillHub。发布包由 `.github/actions/publish` 的打包步骤生成（排除 `evals/`、`docs/`、dev-doc 与 `.git`/`.github`），**排除清单只写那一处**；`release` 事件没有 `inputs`，发布模式按 `github.event_name` 解析。

详见 `README.md`（与 `SKILL.md` 如存在）。提交遵循 Conventional Commits；`main` 走 PR 合并。
