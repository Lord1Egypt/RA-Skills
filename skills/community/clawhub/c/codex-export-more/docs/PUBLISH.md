# 发布指南

本工具可分发到三个渠道：npm、PyPI、clawhub（Codex skill）。CI 已配置 `publish.yml`，打 `v*` 标签可自动发布 npm/PyPI；clawhub 需本地执行。

> 发布前请先在仓库根目录添加 `LICENSE` 文件（如 MIT），再对外发布。

## 1. npm

包名 `codex-export-more`（已确认可用）。

```bash
npm login                      # 首次：npm adduser
npm publish                    # 首次发布
npm version patch              # 后续版本号递增
npm publish
```

回滚/下线：`npm deprecate codex-export-more@<版本> "原因"`（推荐）；紧急删除用 `npm unpublish codex-export-more@<版本>`（有严格限制，谨慎）。

## 2. PyPI

包名 `codex-export-more`（已确认可用）。

```bash
python -m pip install --upgrade build twine
python -m build                # 生成 sdist + wheel（dist/）
twine upload dist/*
```

首次发布需在 https://pypi.org/manage/account/token/ 创建 API token，并配置到 CI：
仓库 Settings → Secrets and variables → Actions → `PYPI_API_TOKEN`。

PyPI 不允许随意删除发布版本；需要下线时在 PyPI 后台对版本执行 yank。

## 3. clawhub（Codex skill）

仓库内已包含 `SKILL.md` 与 `package.json`（clawhub 元数据基础）。发布：

```bash
clawhub login                  # 首次：GitHub 授权
clawhub skill publish . --slug codex-export-more --name "Codex Export More"
```

消费者安装：

```bash
npx clawhub@latest install codex-export-more
```

clawhub 发布流自带安全审查与版本管理；发布前确认 `SKILL.md` 的 description 覆盖了 `--brief/--redact/--since/--until/--grep/--append/--interactive/--sessions/--watch` 等能力。

## 4. CI 自动发布

在 GitHub 仓库配置两个 Secrets：

- `PYPI_API_TOKEN`：PyPI API token
- `NPM_TOKEN`：npm 自动发布 token（`npm token create`）

配置完成后打标签即可自动发布：

```bash
git tag v0.1.0
git push origin v0.1.0
```

注意：clawhub 发布需要本地 GitHub 授权，不走 CI。

## 版本策略

- 功能分支小步提交 → 合并 `main` → 打 `v*` 标签触发发布。
- 版本号语义：破坏性变更升 minor 或 major；新增功能升 minor；修复升 patch。
