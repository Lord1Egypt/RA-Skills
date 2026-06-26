# Changelog

## 1.1.2

Release theme: tighten release trust by aligning metadata, repository links, and validation gates.

What changed:
- Update package, Clawhub, skill, and metadata versions to the same release number
- Replace stale `openclaw-skill-changebrief` links with the actual `harrylabsj/changebrief` repository
- Add `npm run verify` as a release gate for syntax checks, unit tests, CLI smoke tests, and metadata consistency
- Run verification automatically before `npm run publish:clawhub`

Suggested one-line changelog:
- Align ChangeBrief metadata and repository links, and add a release verification gate before publishing.

## 1.0.1

Release theme: 修正首发发布路径，确保线上版本对应真正的 ChangeBrief skill 包。

What changed:
- 使用绝对路径重新发布 `changebrief`，避免误把上层 workspace 打进同名 slug
- 保持产品定位、CLI、测试和文档不变，修正线上包内容与本地仓库一致

Suggested one-line changelog:
- Fix the published package path so ChangeBrief ships the correct skill files and metadata.

## 1.0.0

Release theme: 给知识线补上一层真正可用的“增量变化层”。

What changed:
- 新建 `ChangeBrief` 产品线定位，明确它不是再做一个知识库，而是做“最近到底变了什么”的变化简报层
- 新增最小 CLI，支持 `brief`、`changes`、`invalidations`、`conflicts`、`priorities`、`analyze`
- 实现前后快照对比逻辑，用于识别重要新增、说法变化、失效结论和决策冲突
- 补齐 `README`、`RELEASE`、`package.json`、测试和发布脚本，整理成可发布仓库

Suggested one-line changelog:
- Initial release of ChangeBrief: compare previous and current knowledge snapshots to surface what changed, what became stale, and what deserves action now.
