# GitHub Actions 部署指南（Hugo -> GitHub Pages）

目标：提交后自动构建 Hugo，并发布到 GitHub Pages，获得公网可访问 URL。

## 0. 部署引导文档落地位置（强约束）

`hugo-github-deploy-guide.md` 必须放在当前 Hugo 工作目录，不允许写入 `~/.openclaw`。

标准路径：

`<workspacePath>/hugo-github-deploy-guide.md`

## 1. 前置条件

```markdown
□ 已有 GitHub 远程仓库（origin）
□ 当前分支可 push
□ Hugo 站点可本地构建（`hugo` 成功）
```

默认仓库策略（推荐）：

- 默认使用用户主页仓库：`<githubUser>.github.io`
- 默认站点 URL：`https://<githubUser>.github.io/`（无项目前缀）
- 仅在用户明确要求时，才使用子项目路径模式 `https://<githubUser>.github.io/<repo>/`

自定义域名策略（可选）：

- 部署前提醒用户可配置自定义域名（例如 `blog.example.com`）
- 若用户确认配置，必须同步修改：
  1. Hugo 配置中的 `baseURL`
  2. `static/CNAME` 文件（文件内容仅为域名）

## 2. 工作流文件

路径：`.github/workflows/hugo-pages.yml`

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches:
      - <defaultBranch>
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5
        with:
          enablement: true

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: "0.150.0"
          extended: true

      - name: Build
        run: hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## 3. Pages 设置引导

仓库中执行：

1. `Settings -> Pages`
2. `Build and deployment -> Source` 选择 `GitHub Actions`
3. 保持默认即可，后续由工作流自动发布

> 将 `<defaultBranch>` 替换为仓库实际默认分支（例如 `main` 或 `master`）。

> 若你希望提前验证 Node24 兼容，可在 workflow 顶层增加：
>
> ```yaml
> env:
>   FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
> ```
>
> 主页仓库模式默认建议 `baseURL = "https://<githubUser>.github.io/"`；
> 若启用自定义域名，改为 `baseURL = "https://<customDomain>/"`。

## 4. 托管执行命令模板

```bash
cat > "<workspacePath>/hugo-github-deploy-guide.md" <<'EOF'
# Hugo GitHub Pages Deploy Guide
1. Ensure Pages Source is GitHub Actions
2. Push to main branch to trigger deployment
3. Verify Actions success and visit site URL
EOF
git -C "<workspacePath>" add .github/workflows/hugo-pages.yml
git -C "<workspacePath>" add hugo-github-deploy-guide.md
git -C "<workspacePath>" commit -m "ci(hugo): add GitHub Pages workflow"
git -C "<workspacePath>" push -u origin "<currentBranch>"
```

自定义域名修改模板（按需执行）：

```bash
# 1) 修改 Hugo 配置中的 baseURL
# 例如在 hugo.toml 中设置：
# baseURL = "https://<customDomain>/"

# 2) 写入 CNAME（纯域名，不带协议）
printf '%s\n' "<customDomain>" > "<workspacePath>/static/CNAME"

# 3) 提交并推送
git -C "<workspacePath>" add hugo.toml
git -C "<workspacePath>" add static/CNAME
git -C "<workspacePath>" commit -m "chore(hugo): configure custom domain"
git -C "<workspacePath>" push origin "<currentBranch>"
```

## 5. 发布结果识别

- 默认（主页仓库模式）：
  - `https://<githubUser>.github.io/`
- 子项目模式（非默认）：
  - `https://<githubUser>.github.io/<repo>/`
- 自定义域名模式（可选）：
  - `https://<customDomain>/`

## 6. 常见失败与恢复

1. `No Pages site found`：未将 Pages Source 设置为 `GitHub Actions`。
   - 已在模板中通过 `enablement: true` 增加自动启用兜底，若仍失败通常是权限问题。
2. `Permission denied`：仓库权限不足，确认 Actions 权限与仓库可写权限。
3. 主题资源缺失：使用主题子模块时，确认 checkout 启用了 `submodules: recursive`。
4. 样式路径错乱：检查 `baseURL` 与仓库访问路径是否匹配。
5. 自定义域名未生效：检查 DNS 解析、`static/CNAME` 内容、Pages 自定义域名设置是否一致。
