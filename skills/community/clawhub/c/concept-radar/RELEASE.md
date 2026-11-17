# 发布排除说明

发布 `concept-radar` 时，以 `.skillignore` 为排除清单。

必须排除：

- `__pycache__/`、`*.pyc`、测试覆盖率与本地工具缓存。
- `runtime/`、`state.json`、`candidates.json`、`concept-radar.md/json` 等运行产物。
- `.env`、token、cookie、open_id、私有作者池配置及其他凭证。
- 抓取到的正文、临时 selection、调试日志和失败响应。

应保留：

- `SKILL.md`、`README.md`、`RELEASE.md` 与 `.skillignore`。
- `scripts/`、`references/`、`config/*.example.yaml`、`examples/` 和 `tests/`。

注意：仓库级 `.trae/concept-radar/` 是运行数据目录，不属于 Skill 发布包；旧的
`.trae/skills/weekly-concept-radar/` 是独立 Skill，也不应被合并或删除。
