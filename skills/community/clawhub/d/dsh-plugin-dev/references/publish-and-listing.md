# 发布与收录指南（DSH 插件）

> 来源：官方 develop/basic/publish + 社区实证指南 anweat/dsh-plugin-dev-guide（2026-08/09 实测）。
> 基线：`dsh-v0.1.1-rc.2`、`pnpm@11.7.0`。

## 1. 五级复用形态（打包不是必须的）

"打包"只是传输载体；安装型分发唯一绕不开的是**构建产物**（Node 按 `main` 解析 JS）。
**纯 JS 骨架（本 skill 脚手架产出）无构建环节，直接处于形态②起步位。**

| 形态 | 复用什么 | 打包？ | 构建？ | 场景 |
|---|---|---|---|---|
| ① `--patch` 指向源码 | 源码文件（绝对路径） | 否 | 否（tsx 直载 .ts） | 开发期 |
| ② `dsh plugin add ./<目录>` | 含 package.json 的目录 | 否 | 是（一次，产 lib/） | 内部分发 |
| ③ `add github:<user>/<repo>` | 源码仓库 | 否 | 是（安装时 prepare） | 社区分发 |
| ④ `add <npm包名>`（推荐） | npm registry | 是 | 是（prepublishOnly） | 社区分发，包名即身份 |
| ⑤ `add ./x.tgz` | tarball | 是 | 是 | 邮件/Release 资产/评审 |

## 2. 本地验证（发布前必做）

```bash
cd <插件目录>
npm pack                                   # 纯 JS 骨架无需 build
# 端到端：临时 profile 装 tarball（模拟社区用户，不碰现有 profile）
cd <deepseek-harness 仓库根>
corepack pnpm dsh plugin --profile dsh-plugin-test add <插件目录>/dsh-xxx-0.1.0.tgz
corepack pnpm dsh --profile dsh-plugin-test --dump-config   # 应出现 "# == dsh-xxx" 层
Remove-Item -Recurse -Force <DSH_HOME>/profiles/dsh-plugin-test   # 用完删除
```

`plugin add` 后 bundle 自动追加进 `dsh.profile.bundles`（reconcile）。

## 3. 通道 A：npm（推荐）

```bash
npm whoami          # 未登录先 npm login
cd <插件目录>
npm publish         # scoped 包必须 npm publish --access public
```

- **名字被占？用 scoped 包名** `@<npm账号>/dsh-<名称>`：命名空间归账号所有永不冲突。
  同步改三处：package.json name、cordis.patch.yml 里 `name: '@scope/pkg'`（**必须加引号**）、安装命令。
- **403 Two-factor authentication**：CI 发布必须用 **Automation token**（classic token 勾 Automation）或开启 Bypass 2FA 的 Granular token；普通 publish token 在 CI 必 403。
- **发布成功但装不到（"not in the npm registry"）**：abbreviated metadata 在 publish 后 **1–2 分钟**才生成，期间 `npm view` 正常但 pnpm 安装 404。验证：
  `curl -H "Accept: application/vnd.npm.install-v1+json" https://registry.npmjs.org/<包名>` 返回 200 再装。别误判 restricted 或删包重发。
- **CI 里 `npm publish dist/*.tgz` 报 git ls-remote 错**：glob 展开后不带 `./` 前缀会被 npm 11 当 GitHub shorthand 去 ssh 拉取。必须写 `npm publish ./dist/*.tgz`。
- `npm view <pkg> dist-tags`：官方包 `latest` 可能是历史遗留，开发线看 `next`。

## 4. 通道 B：GitHub 仓库

仓库结构即 bundle 包（源码 + package.json + cordis.patch.yml）。

- **纯 JS 包**：无构建环节，仓库即可被 `dsh plugin add github:<user>/<repo>` 直接安装。
- **TS 包**：必须自包含 `prepare` 脚本（git 安装后 pnpm 运行它），构建不得依赖仓库外上下文。
  且 pnpm ≥10 用户须在 profile 的 `pnpm-workspace.yaml` 加白名单后重跑：
  ```yaml
  allowBuilds:
    dsh-xxx: true
  ```
  这是"允许该包在安装时于用户机器上执行代码"的信任决定，README 要写清并建议钉 commit（`github:you/repo#<sha>`）。
- 仓库加 topic **`dsh-plugin`**（github.com/topics/dsh-plugin 是社区聚合地）；README 顶部写安装命令。
- 可补 GitHub Release 附 tgz 资产（用户 `dsh plugin add ./xxx.tgz` 直装）。

## 5. 通道 C：tarball / 本地路径（零权限）

```bash
npm pack
dsh plugin --profile web add ./dsh-xxx-0.1.0.tgz    # 或直接 ./dsh-xxx 目录
```

无构建权限、无网络依赖，适合内网/评审；缺点是升级靠手动替换。

## 6. CI 自动发布（脚手架已生成 .github/workflows/publish.yml）

推 tag（`git tag v0.1.1 && git push origin v0.1.1`）即自动：校验 tag==version → pack → npm publish（`--provenance --access public`）→ GitHub Release 附 tgz。
一次性配置：

1. npmjs.com/settings/<用户名>/tokens → Generate New Token → **Automation**
2. GitHub 仓库 Settings → Secrets → Actions → 新建 `NPM_TOKEN`
3. （可选）Settings → Environments → `npm-publish` → Required reviewers 人工把关

不想发布只预演：Actions 手动运行 workflow 不勾 publish（dry-run pack）。tag 与 version 不匹配时 pack job 直接失败，不会触碰 registry。

## 7. 收录到 awesome-dsh-plugin（插件广场唯一入口）

SkillHub 插件广场是索引站，数据自动从开源生态同步，**无需也无法在 SkillHub 提交插件**。
收录方式：向 `github.com/awesome-dsh-plugin/awesome-dsh-plugin` 发 PR，**只新增一个文件**：

`data/plugins/<owner>__<repo>.yml`

```yaml
url: https://github.com/<owner>/<repo>
name: <owner>/<repo>
category: tools
description:
  en: 'Blocks destructive commands before the tool call runs'
  zh: 可选，中文描述
```

**分类池（category 必选，只能选其一）**：
`agi` `ui` `usage` `theme` `model` `identity` `session` `memory` `tools` `wsl` `browser` `vision` `voice` `docs` `skill` `workflow` `git` `notify` `dev` `security` `remote` `market` `fun`

**收录硬要求（CI 自动查，缺一即拒）**：

1. 真实可用代码——占位/纯 README 仓库不收；
2. 仓库创建**满 1 天**（所以尽早建仓库推骨架，哪怕半成品）；
3. 活跃维护；
4. GitHub 仓库 topic 加 `dsh-plugin`；
5. 描述必须与代码相符——README/description 声称几个工具，代码里就得真有几个；
6. YAML 值含 `": "` 必须加引号（`en: 'Search: web and docs'`），否则解析报错；
7. `url` 必须等于仓库 URL；
8. 推荐 npm 发布（用户免 allowBuilds 授权）或 GitHub Release tarball（可选 `tarball:` 字段指向 https .tgz，**文件名不带版本号**防 404）。

收录后 SkillHub 插件广场会在同步周期内自动出现。

## 8. 生态定位参考（2026-08/10 调研）

- 现有插件集中在 ui/theme/tui 类（如 dsh-web-ui、dsh-cc-tui、dsh-deep-whale）；**security 类仅 cc-safety-net（1.8k stars）**；AI 代码质量/交付验证类为空白。
- DSH 官方在 `packages/bundle` 之外不维护插件市场——"npm 发布 + GitHub topic 曝光 + awesome-dsh 收录"就是当前全部社区分发路径。
