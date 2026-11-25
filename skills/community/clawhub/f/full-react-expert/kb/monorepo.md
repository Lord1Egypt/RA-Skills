---
subdomain: monorepo
version: 9
updated: 2026-11-17
---
# Monorepo

## 定位与心智模型

React 全栈 monorepo 主流栈（2026）：**pnpm 12.21.0（Rust 重写，已 stable）**（依赖管理，pnpm.io + registry latest 锚定）+ **Turborepo 2.11.11**（任务编排/缓存，npm registry 锚定）+ **changesets 3.0.3**（库发布，changesets.dev 锚定）。职责切分一句话：**pnpm 管包与依赖，turbo 管任务与缓存，changesets 管版本与发布**——三者各司其职，不混用。

Turborepo 官方定位（turborepo.dev 锚定，域名已从 turbo.build 迁移）："**build system for coding agents**" [官方文档](https://turborepo.dev)——增量构建 + 远程缓存 + 按变更裁剪。

工具链版本主线（2026-11-16 锚定）：**TypeScript 双线并行**——6.0.3（最后 JS 代码库版本，工具链兼容线）与 **7.0.2（Go 原生 10×，registry latest）**，选线按 [MO-12] 矩阵；lint 主线：**eslint 10** + typescript-eslint 8.73.0（typescript <6.1.0）/ @biomejs/biome 2.6.8 / oxlint 1.93.0 / prettier 3.10.1。

## 法则

[MO-1] **MUST**: 依赖管理单一工具链：pnpm 用 pnpm-workspace.yaml，npm 用 package.json workspaces——NEVER 双轨混写。
- 违反后果: workspace 解析混乱，幽灵依赖加倍。
- 溯源: [模型经验]

[MO-2] **MUST**: 幽灵依赖报错的正解是补声明；shamefully-hoist 仅限旧工具临时兼容。
- 违反后果: 隔离被整体关闭，幽灵依赖问题被掩盖而非解决。
- 溯源: [官方文档](https://pnpm.io)（符号链接语义）

[MO-3] **MUST**: 包间互引用 `workspace:*`/`workspace:^`，发布前确认替换语义与工具链支持。
- 违反后果: 发布产物残留 workspace 协议，消费方安装失败。
- 溯源: [官方文档](https://pnpm.io)

[MO-4] **MUST**: turbo 构建链任务用 `dependsOn: ["^build"]`（依赖先构建）；`["build"]`（全包同名任务）仅限确有全局前置的场景。
- 违反后果: 串行拖慢或依赖未构建就引用。
- 溯源: [官方文档](https://turborepo.dev/docs)（任务语义）

[MO-5] **MUST**: 缓存任务必须配全 `outputs`（Next 项目排除 `.next/cache`）与参与 key 的 `env`；dev/watch 任务必须 `persistent: true`。
- 违反后果: 缓存命中但产物缺失；旧缓存复用假结果；turbo 挂死。
- 溯源: [模型经验]

[MO-6] **MUST**: 运行时依赖声明在子包，NEVER 放根 package.json。
- 违反后果: pnpm 隔离下子包运行时缺模块。
- 溯源: [模型经验]

[MO-7] **MUST**: 发版流程固定为 build → version → publish（CI 内），发布包 build 产物必须新鲜；不发布包必须 `private: true`（全局宪法 LAW-10）。
- 违反后果: 发出旧 dist；apps 误发公共 npm。
- 溯源: [模型经验]

[MO-8] **MUST**: changeset 与变更同 PR 提交；合入 main 的变更必须有对应 changeset（或显式标注不发布）。
- 违反后果: 下个版本静默漏发。
- 溯源: [官方文档](https://changesets.dev)

[MO-9] **NEVER**: 新项目不选 lerna（维护减活）——2026 主流 pnpm + Turborepo + changesets。
- 违反后果: 生态停滞、安全补丁滞后。
- 溯源: [模型经验]

[MO-10] **MUST**: turbo.json 用 `tasks` 键（`pipeline` 为历史版本）。
- 违反后果: 旧键被忽略，任务图不生效。
- 溯源: [官方文档](https://turborepo.dev/docs)

[MO-11] **MUST**: pnpm 12（Rust 重写）CLI 语法核对：关闭冻结安装用 `--no-frozen-lockfile`（**`--frozen-lockfile false` 写法本身被拒绝**）；`--resolution-only` 已移除，peer 检查用 `pnpm peers check`。
- 违反后果: CI 脚本沿旧写法直接报错（写法被拒，不是语义降级）。
- 溯源: [官方文档](https://pnpm.io)

[MO-12] **MUST**: TypeScript 版本按工具链兼容矩阵选线：typescript-eslint（typescript >=4.8.4 <6.1.0）与 Volar 型框架（Vue/Svelte/Astro/MDX）项目锁 TS 6.x；纯 tsc CLI 项目可上 TS 7；依赖程序化 API 的工具须 TS 7.1+（7.0 无 API）。
- 违反后果: typescript-eslint peer 不满足；Volar 语言工具失效；依赖 tsserver API 的工具崩溃。
- 溯源: [官方文档](https://devblogs.microsoft.com/typescript/announcing-typescript-7-1-beta/) + registry peer 区间锚定

[MO-13] **MUST**: 依赖版本治理用根 pnpm-workspace.yaml `overrides`（选择器 `父@范围>依赖`、类型限定 :prod/:optional/:peer、`-` 移除、`catalog:` 引用）；改依赖代码用 `pnpm patch` → `patch-commit`（patchedDependencies 登记）；NEVER 用 patch 改依赖的 package.json（依赖关系改动用 overrides）。
- 违反后果: 子包/.npmrc 里的 overrides 不生效；patch 改 package.json 不受支持、升级即丢。
- 溯源: [官方文档](https://pnpm.io/settings/dependency-resolution) + [官方文档](https://pnpm.io/cli/patch)

[MO-14] **MUST**: Docker/独立目录部署单个 workspace 包用 `pnpm --filter=<pkg> --prod deploy <dir>`（v12.2+ 自动把 workspace 依赖改写为 file: 依赖；filter 须恰好选中一个项目）；产物文件集遵循 pack 规则。
- 违反后果: 镜像装全仓 node_modules 超大/幽灵依赖；ERR_PNPM_CANNOT_DEPLOY_MANY/ERR_PNPM_DEPLOY_DIR_NOT_EMPTY。
- 溯源: [官方文档](https://pnpm.io/cli/deploy)

[MO-15] **MUST**: snapshot 发布必须 `changeset publish --tag <tag>`（NEVER 裸 publish——latest dist-tag 会被 0.0.0-xxx 污染，用户 npm install 默认装到快照版）；snapshot 的 version 产物 NEVER push/merge 回任何分支。
- 违反后果: latest 指向 snapshot；快照版本号污染仓库历史。
- 溯源: [官方文档](https://changesets.dev/guide/snapshot-releases)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| pnpm-workspace.yaml | workspace 包声明（packages 列表） |
| 幽灵依赖 | 未在 package.json 声明却 import 到的包——pnpm 符号链接结构默认**隔离** |
| `workspace:*` 协议 | 包间互引；发布时 pnpm 替换为真实版本 |
| catalog: | pnpm 集中版本表：`catalog:`/`catalogs:` 定义在 pnpm-workspace.yaml，包内依赖用 `catalog:` 协议引用，发布时替换为真实版本；未匹配报 `ERR_PNPM_CATALOG_ENTRY_NOT_FOUND_FOR_SPEC` |
| catalogMode | pnpm 12.3+ catalog 自动更新策略：`manual`/`strict`/`prefer` |
| turbo 任务 | turbo.json 定义；`dependsOn: ["^build"]` = 先构建依赖的包 |
| 远程缓存 | Vercel 托管/自托管；CI 命中跳过执行 |
| changeset | `.changeset/*.md` 变更记录 → version 消费 → publish 发布 |
| fixed / independent | monorepo 版本策略：整组同版 vs 各包独立 |
| pnpm 12 Rust 重写 | pnpm 12.21.0 = Rust 实现已 stable（registry latest）；CLI 语法有破坏性变化（[MO-11]） |
| 供应链默认防护 | pnpm 12 默认开启：minimumReleaseAge 默认 1440 分钟（24h 内新包不装）/ allowBuilds（install 脚本白名单）/ blockExoticSubdeps（默认 true，阻断异源传递依赖）；**trustPolicy 默认 off**（显式配 no-downgrade 才启用）[冲突消解] |
| remoteCache.signature | turbo 远程缓存产物签名（HMAC-SHA256，密钥 TURBO_REMOTE_CACHE_SIGNATURE_KEY）——校验失败按 cache miss 静默降级 |
| TS 7（Go 原生） | typescript 7.0.2（registry latest）；10× 编译提速；7.0 无程序化 API（7.1 Beta 已补） |
| @typescript/typescript6 | TS 6 兼容包：tsc6 可执行 + TS 6.0 API 再导出；npm alias 与 typescript@7 并存 |
| overrides | 根 pnpm-workspace.yaml 依赖覆写：`父@范围>依赖` 选择器/:prod·:optional·:peer 类型限定/`-` 删除/`pkg@` 收敛覆盖 [MO-13] |
| patchedDependencies | pnpm patch-commit 登记的代码补丁；键优先级 精确版本 > 范围 > 仅包名 [MO-13] |
| pnpm deploy | 子集部署：`pnpm --filter=<pkg> --prod deploy <dir>`，workspace 依赖改写为 file: 依赖 [MO-14] |
| pre 模式 | `changeset pre enter <tag>` 写 .changeset/pre.json；版本 1.0.0-beta.0、dist-tag=tag；version 后 changesets 移入 .changeset/pre/（留给 stable changelog） |
| snapshot | `changeset version --snapshot [tag]` → 0.0.0-{tag}-{datetime}；publish 必带 --tag [MO-15] |

## 最佳实践

### 场景：仓库初始化（[MO-1]/[MO-9]）

推荐路径：pnpm + Turborepo + changesets；目录约定 apps（不发 npm，private）+ packages（发布）。

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'        # 应用（不发 npm，private: true）
  - 'packages/*'    # 库（发布）
```

边界条件：pnpm 与 npm 的 `--filter` 语法不同，勿混用（[MO-1]）。

### 场景：版本集中管理（catalog:，pnpm 12）

推荐路径：pnpm-workspace.yaml 用 `catalog:`（默认目录）/`catalogs:`（命名目录）定义集中版本表 → 各包依赖字段写 `catalog:` / `catalog:<name>` 协议 → 发布时自动替换为真实版本。终结多包版本漂移（[MO-3] 的集中化形态）。

```yaml
# pnpm-workspace.yaml
packages: ['apps/*', 'packages/*']
catalog:
  react: '^19.3.0'
catalogs:            # 命名目录（多版本共存场景）
  react18:
    react: '^18.3.0'
```

```jsonc
// packages/ui/package.json
{ "dependencies": { "react": "catalog:", "zod": "catalog:" } }
```

边界条件（[官方文档](https://pnpm.io/catalogs)）：
- 未找到条目报 **`ERR_PNPM_CATALOG_ENTRY_NOT_FOUND_FOR_SPEC`**（拼写/漏定义第一排查点）
- `catalogMode`（12.3+）：`manual`（手动管理）/`strict`/`prefer`（自动更新策略）
- workspace 依赖可进 catalog（12.2+）：条目可写 `"pkg": "workspace:*"`；`file:`/`link:` 协议 12.6+ 可用
- 清理未用条目用 `catalogPrune`

### 场景：workspace: 协议与本地链接（[MO-3]）

推荐路径（[官方文档](https://pnpm.io/workspaces)，2026-11-15 深度补强）：**`linkWorkspacePackages` 默认 false**——本地包默认不链接（从 registry 下载），`workspace:` 协议才强制链接本地；协议拒绝解析到 registry 之外的任何东西（`workspace:2.0.0` 本地无 2.0.0 即安装失败，杜绝"本地有就用本地"的不确定性）。

| 写法 | 安装行为 | 发布替换 |
|---|---|---|
| `workspace:*` / 裸 `workspace:` | 链接本地任意版本 | 替换为实际版本（精确） |
| `workspace:^` / `workspace:~` | 链接本地 | `^x.y.z` / `~x.y.z` |
| `workspace:^1.5.0` | 本地须满足范围 | `^1.5.0` |
| `workspace:../foo` | 相对路径链接 | 转常规版本说明 |
| 别名 `"bar": "workspace:foo@*"` | 链接本地 foo | `npm:foo@1.0.0` |

边界条件：**v12.7+ 自动转换**——npm/Yarn/Bun 仓库（package.json `workspaces`）无 pnpm-workspace.yaml 时 `pnpm install` 自动创建（已有不覆盖；只读 pnpm-workspace.yaml；`--ignore-workspace` 跳过）；`injectWorkspacePackages`/`dependenciesMeta[].injected` 硬链注入（TS 项目配 `syncInjectedDepsAfterScripts` 同步构建产物）；循环依赖安装警告 + 递归任务报 `ERR_PNPM_TASK_CYCLE`（`ignoreWorkspaceCycles` 降级 / `disallowWorkspaceCycles` 禁止）。

### 场景：依赖治理（[MO-2]/[MO-6]/[MO-3]）

推荐路径：迁移 pnpm 后报幽灵依赖逐个**补声明**（这是特性不是 bug）；跨包统一版本用 `catalog:`；运行时依赖声明在子包；包间互引 `workspace:*`（`*` 发布替换为精确版本，`^` 为 caret 版本——确认工具链支持替换）。

```bash
# don't：shamefully-hoist 掩盖问题
# .npmrc: shamefully-hoist=true

# do：补声明
pnpm --filter @acme/ui add lodash-es
```

### 场景：依赖覆写与补丁（[MO-13]）

推荐路径：版本对不齐/传递依赖漂移用根 pnpm-workspace.yaml `overrides`（**仅根级**——pnpm 12 配置主体在 pnpm-workspace.yaml，.npmrc 只保留 auth/registry/TLS/proxy/local-address）；改依赖代码用 `pnpm patch <pkg>@<ver>` → 编辑 → `pnpm patch-commit <dir>`（自动登记 patchedDependencies）。

```yaml
# pnpm-workspace.yaml（根）
overrides:
  'qar@1>zoo': '^1.2.3'        # 父>子选择器：仅 qar@1 下的 zoo
  '@mui/*>react:peer': '^19'   # 通配 + 限定 peer
  'foo:optional': '^2'         # 依赖类型限定 :prod/:optional/:peer
  'bar': '-'                   # 删除依赖
  'baz': 'catalog:'            # 引用 catalog 集中版本
  'qux@': '1.5.0'              # 收敛覆盖：同包多版本收敛为一个精确版本
```

边界条件：补丁解出到 `node_modules/.pnpm_patches/<pkg>`（`--edit-dir` 可改；**须先 install** 否则 `ERR_PNPM_PATCH_NO_LOCKFILE`）；patchedDependencies 键优先级 **精确版本 > 范围 > 仅包名**（多版本时 patch 命令交互选择，全应用则键不带版本）；**NEVER patch 改依赖的 package.json**——依赖关系用 overrides/pnpmfile（[MO-13]）；`allowUnusedPatches` 默认 false（补丁未实际应用装不上）；`ERR_PNPM_PATCH_EDIT_DIR_EXISTS`/`ERR_PNPM_EDIT_DIR_NOT_EMPTY` 清理编辑目录；收敛覆盖值必须精确版本（否则 `ERR_PNPM_INVALID_CONVERGENCE_OVERRIDE`；常规覆盖优先于收敛覆盖）；peer 覆写语义：范围/workspace:/catalog: 值→替换 peer 范围，link:/file:/npm: 值→peerDependencies 不动；配套：packageExtensions 补缺失 peer 声明、allowedDeprecatedVersions 压弃用告警、update.ignoreDeps 锁定不升级、update.changeset 生成变更意图。

### 场景：子集部署（pnpm deploy，[MO-14]）

推荐路径：Docker/独立目录部署单个 workspace 包用 `pnpm --filter=<pkg> --prod deploy <dir>`（v12.2+：workspace 依赖自动改写为 deploy lockfile 里的 `file:` 依赖，无需 injectWorkspacePackages）。

```dockerfile
# 官方多阶段模板（node:22-alpine 运行时）
FROM node:22-alpine AS builder
RUN corepack enable
WORKDIR /repo
COPY . .
RUN pnpm install --frozen-lockfile
RUN pnpm --filter=@acme/web build          # 先构建（deploy 只搬产物不构建）
RUN pnpm --filter=@acme/web --prod deploy /app

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app .
CMD ["node", "dist/main.js"]
```

边界条件：filter 必须**恰好选中一个项目**（`ERR_PNPM_NOTHING_TO_DEPLOY`/`ERR_PNPM_CANNOT_DEPLOY_MANY`）；目标非空须 `--force`（`ERR_PNPM_DEPLOY_DIR_NOT_EMPTY`）；peer 版本歧义报 `ERR_PNPM_DEPLOY_AMBIGUOUS_PEER`（用 overrides 钉死）；产物文件集遵循 pack 规则（files/.npmignore/.gitignore；`deployAllFiles: true` 全量拷贝）；被 deploy 项目**不跑 prepare**；`SOURCE_DATE_EPOCH` 环境变量可复现构建（12.15+）；`--legacy`/`forceLegacyDeploy` 回退旧行为；enableGlobalVirtualStore 被忽略（virtual store 本地化）。

### 场景：任务图配置（[MO-4]/[MO-5]/[MO-10]）

推荐路径：`tasks` 键（[MO-10]）→ build 用 `^build` → outputs 配全 → env 声明 → dev 任务 persistent。

```jsonc
{
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**", ".next/**", "!.next/cache/**"] },
    "dev": { "cache": false, "persistent": true },
    "test": { "dependsOn": ["build"] }
  }
}
```

边界条件：lint/test 无依赖关系别挂 `^build`（拖慢且无收益）。

### 场景：CI 裁剪（增量构建）

推荐路径：PR 只跑受影响包——`turbo run build test --filter=...[origin/main]`；**任务级精准检测用 `turbo query affected --packages --exit-code`**（2026-11-16 深化，见下）；远程缓存（Vercel 托管/自托管）打不开时静默退化为本地缓存，注意 CI 日志确认命中。

### 场景：发布流程（[MO-7]/[MO-8]）

推荐路径：changeset 与变更同 PR（[MO-8]）→ CI 固定 build → version → publish（[MO-7]）→ apps 与不发包 `private: true`；版本策略 fixed（整组同版）vs independent（各包独立）按消费方选。

changesets v3 关键事实（[官方文档](https://changesets.dev/guide/config)，2026-11-15 锚定）：

- **`access` 默认 `"restricted"`**：scoped 包按私有发布——**公开发布的库必须显式 `"access": "public"`**（防误发公开的安全默认，也是 scoped 包 publish 失败的常见根因）；可被包内 `publishConfig.access` 覆盖（单包级调整免改全局 config）；防发布用包内 `"private": true`（`ignore` 仅临时用）
- **`privatePackages` 默认 `{ version: false, tag: false }`**：私有包默认不版本化不打 tag（v2 时代默认版本化；曾用 ignore 压测试夹具的可移除）
- **`changeset version` 无可发布变更时退出码 1**（v2 为成功空跑）——CI 脚本必须容忍（snapshot/自动发布任务尤其）
- CLI 改名：`changeset tag` → **`changeset git-tag`**；`--sinceMaster` 移除 → `--since=<branch>`
- config：`baseBranch` 默认 `"main"`；`prettier` 字段 → `format`（`auto/prettier/oxfmt/deno/biome/dprint/false`，auto 自动探测）；`changedFilePatterns`（picomatch）细粒度控制什么算变更；`updateInternalDependencies` 默认 `"patch"`（依赖内部包的联动跳版幅度，可选 `"minor"`）；`bumpVersionsWithWorkspaceProtocolOnly` 默认 `false`（true 时仅 `workspace:` 协议依赖联动跳版）；实验项 `useCalculatedVersionForSnapshots` → `snapshot.useCalculatedVersion`
- **要求**：Node `^22.11 || ^24 || >=26`、pnpm ≥10、npm ≥10.9、Yarn ≥4.5.2（Yarn Classic 不支持）；全包 **ESM**
- GitHub Actions 用 **`changesets/action@v2`**（v1 仅配 v2 CLI）：inputs 改名 `version`→`version-script`、`publish`→`publish-script`、`commit`→`commit-message`、`title`→`pr-title`
- peer dependency 更新对依赖方的 bump 从 major 改为 **patch**（真实破坏需显式 major changeset）

### 场景：预发布与快照发布（pre 模式/snapshot，[MO-15]）

推荐路径：beta/rc 预发布走 **pre 模式**——`changeset pre enter <tag>`（写 `.changeset/pre.json`）→ 正常 add/version/publish（版本 `1.0.0-beta.0`、npm dist-tag=tag）→ `changeset pre exit`（只写退出意图，不实际 version）→ 照常 version/publish 得 stable + latest。PR 预览/nightly 走 **snapshot**——`changeset version --snapshot [tag]`（版本 `0.0.0-{tag}-{datetime}`）→ `changeset publish --tag <tag>`。

```bash
# pre 模式（alpha→beta→rc 换 tag：直接改 pre.json 的 tag 值）
changeset pre enter beta
changeset version          # 产 1.0.0-beta.0；changesets 不删除——移入 .changeset/pre/
changeset publish          # dist-tag=beta
changeset pre exit         # 退出后照常 version/publish → stable + latest

# snapshot（PR 预览/nightly）
changeset version --snapshot pr-123
changeset publish --tag pr-123    # [MO-15] 必带 --tag，否则 latest 被 0.0.0-xxx 污染
```

边界条件：**不能只对部分包进入 pre 模式**（PreState 全仓生效——子集 prerelease 场景改用 snapshot 或手动 dist-tag）；进 pre 前先发一次 stable 清空存量 changesets（否则全混入首个 prerelease）；**prerelease 版本不满足多数 semver range**（`2.1.0-beta.0` 不满足 `^2.0.0`）→ **依赖它的包也被联动 bump**（比正常发布范围更大：pkg-a 1.0.0 依赖 pkg-b ^2.0.0，pkg-b 发 2.1.0-beta.0 时 pkg-a 也被 bump 到 1.0.1-beta.0 依赖 ^2.1.0-beta.0）；pre 模式中未发布过的新包除 prerelease tag 外还打 **latest tag**（npm 强制所有包有 latest）；`pre exit` 后 `.changeset/pre/` 里的 changesets 全部并入 stable changelog——pre 期专属临时修复应在退出前编辑/删除；snapshot：`--no-git-tag` 跳过 git tag；**version 产物仅供安装验证，不 push/merge 任何分支**（[MO-15]）；分支隔离模式（next 分支做 prerelease）改 baseBranch + CI 放行该分支——合并回主线前还原 baseBranch；替代方案 pkg.pr.new（临时 registry，PR 即装，防污染 npm 版本与 tag）。

### 场景：pnpm 12（Rust 重写）迁移差异（[MO-11]）

pnpm 12.21.0 = **Rust 重写版已 stable**（registry latest 标签锚定，2026-11-16）。8 项关键差异：

| # | 差异 | 说明 |
|---|---|---|
| 1 | project-aware global bins | `devEngines.runtime` 可钉 Node 版本（免 nvm/volta） |
| 2 | Git 依赖 HTTPS-only | SSH 记法不再写入 lockfile |
| 3 | 命名即真包管理器 + `pnx` | 包管理器直接执行入口 |
| 4 | 循环依赖图 | workspace 循环下 lockfile 仍确定性 |
| 5 | packageImportMethod | Linux 默认 hardlink-first |
| 6 | engineStrict | engines 不满足直接失败 |
| 7 | `--resolution-only` 移除 | 替代：`pnpm peers check` |
| 8 | `--frozen-lockfile false` 拒绝 | 替代：`--no-frozen-lockfile` |

供应链默认防护（settings 文档锚定 2026-11-17）：`minimumReleaseAge` 默认 1440 分钟（新发布的包 24h 内不装，防投毒抢跑）/ `allowBuilds`（install 脚本白名单）/ `blockExoticSubdeps` 默认 true（阻断异源传递依赖）；**`trustPolicy` 默认 off**（显式配 no-downgrade 才启用——「新项目供应链防护」为 pnpm 官网宣传口径，见冲突消解记录）。

边界条件：CI 脚本里 grep 所有 `pnpm install` 调用核对旧写法（[MO-11] 第一排查点）；workspace/catalog 语义（`workspace:` 协议、`catalog:`、`catalogMode`）在 Rust 重写后保持兼容。

### 场景：Remote Caching 与产物签名

推荐路径：`turbo login` / `turbo link`（Vercel 托管，免费；SSO 用 `--sso-team`）→ turbo.json 配 `remoteCache.signature` → CI 注入 `TURBO_REMOTE_CACHE_SIGNATURE_KEY`。

- **产物签名**：HMAC-SHA256——命中远程缓存先验签，**校验失败按 cache miss 静默重跑**（不中断但也不复用可疑产物）；CI 日志确认命中数防"全量重跑没发现"
- **日志也被缓存 replay**：`turbo run` 输出含缓存命中任务的日志回放——排查"日志里看到了但实际没跑"
- 自托管：v8 开放 API 规格（自建缓存服务器按规格实现即可接入）

### 场景：turbo query 变更检测与 CI 决策（2026-11-16 深化）

推荐路径（[官方文档](https://turborepo.dev/docs/reference/query)）：`turbo query` 对 monorepo 跑 GraphQL——无参开 GraphiQL、`--schema` 出 schema、传 .gql 文件；**纯计划面**（不执行任务不查缓存命中）。CI 跳过决策用 shorthand：

```bash
# 任务级检测比包级精确：.md 变更不触发 inputs 排除 *.md 的任务
turbo query affected --packages my-app --exit-code   # 0 无/1 有/2 错误
turbo query affected --tasks build test --packages web --base main
```

- **turbo-ignore 已弃用** → `turbo query affected`（--task→--tasks、--fallback→--base）；JSON 输出带 `reason`（`FileChanged`/`LockfileChanged`/`RootInternalDepChanged`（根包内部依赖变——**全包选中+全局 hash 变，所有缓存任务 miss**）/`GlobalDepsChanged`/`GitRefNotFound` 等 15 类——reason 是诊断输出非配置），**推荐解析 JSON 拿 reason 做细化决策**
- **浅克隆陷阱**：比较要求 base..head 全在 checkout——GitHub Actions 用 `actions/checkout` 的 `filter: blob:none` + `fetch-depth: 0`（blobless clone），否则全部视为变更
- 任务计划：`affectedTasks` + `withDependencies`（去重、含叶节点；directDependencies 下只选 `fullName` 防图输出爆炸）；任务 `hash`/`hashReason` 与 `turbo run --dry=json` 一致；`logFile` 在 `cache: false` 时为 null
- tags 过滤：包级 turbo.json `"tags": [...]` + `has: {field: TAG, value: "..."}`（大小写敏感）

### 场景：架构守护与多技术栈（boundaries / microfrontends / 多语言）

- **`turbo boundaries`（Experimental，RFC vercel/turborepo#9435）**：查两类 workspace 违规——import 包目录外文件、import package.json 未声明依赖；Tags 规则：包加 `"tags": ["internal"]`，根 turbo.json `boundaries.tags` 里 `dependencies: {deny/allow}`（本包可依赖谁）与 `dependents: {deny}`（谁可依赖本包），列表可混 tag 与包名，**规则传递应用于依赖的依赖**
- **多前端本地联调（microfrontends 代理）**（[官方文档](https://turborepo.dev/docs/guides/microfrontends)）：父应用放 `microfrontends.json` → `turbo dev` 起代理（默认 **3024**）+ 注入 `TURBO_MFE_PORT` + 按路径分发；脚本接 `--port $(turbo get-mfe-port)`；routing paths 支持 `:param`/`:path*`/`:path+`（大小写敏感）；**无 routing 的应用唯一=兜底默认**；`development.fallback` 可代理到生产（`--filter` 跑子集仍无缝）；**仅限本地**——生产组合是自己的基础设施；跨应用 SPA `<Link>` 会报错（不同应用非 SPA）；装 `@vercel/microfrontends` 自动让位（配置兼容渐进迁移）
- **多语言 workspace**（[官方文档](https://turborepo.dev/docs/guides/multi-language)）：通用模式=每项目一个 package.json（scripts 调外部 CLI）+ `workspace:*` 依赖与原生工程引用**双轨手动同步** + 工具链 pin 文件（如 .NET global.json）进 `globalDependencies`（**turbo 不检测已装 SDK 版本——升级必须改文件才失效缓存**）；**实验性原生 workspace**：Rust（Cargo）/ Python（uv）/ Go——从原生 workspace 文件发现项目与依赖（Experimental 相位）
- **弃用清单（新代码禁用，[官方文档](https://turborepo.dev/docs/support-policy)）**：`turbo-ignore`、`turbo scan`、`--parallel`（→ persistent+with）、`--no-cache`（→ `--cache=local:r,remote:r`）、`TURBO_REMOTE_ONLY`（→ `TURBO_CACHE`）、`--daemon/--no-daemon`（daemon 已不用）、`--graph` 的 png/jpg/pdf/json（3.0 移除——用 svg/html/mermaid/.dot 或 turbo query）、`prune --scope`（→ 位置参数）、**根级 `globalDependencies`/`globalEnv`/`globalPassThroughEnv`（→ globalConfiguration Future Flag 的 global 键）**；LTS：大版本自下一个大版本发布日起支持两年（1.x 已 EOL 2026-06-04）；支持 pnpm 8+/npm 8+/yarn 1+（含 PnP）/bun 1.2+/nub/aube

### 场景：TypeScript 6/7 双线选型与 lint 工具链矩阵（[MO-12]）

**TS 双线**（registry 锚定，2026-11-16）：6.0.3（2026-03-23，**最后 JS 代码库版本**，工具链兼容线）｜ **7.0.2（2026-07-08，Go 原生 10×，latest 标签）** ｜ 7.1.0-beta（2026-10-20，**补齐程序化 API**）。

选线矩阵（[MO-12]）：

| 项目形态 | 选线 | 理由 |
|---|---|---|
| typescript-eslint 项目（几乎全部） | **TS 6.x**（6.0.3） | peer typescript >=4.8.4 **<6.1.0**——支持 TS 6.0、不支持 TS 7 |
| Vue/Svelte/Astro/MDX（Volar 型） | **TS 6.x** | 语言工具依赖程序化 API，TS 7.0 无 API |
| 纯 tsc CLI / 大仓类型检查提速 | TS 7 可上 | Go 原生 10×；并行控制 `--checkers N`/`--builders N`/`--singleThreaded` |
| 需要程序化 API 的工具链 | 等 TS 7.1+ | 7.1 Beta：模块化入口（typescript/sync、typescript/async、typescript/fs、typescript/ast）+ API/Program/Snapshot 均 **Disposable**（Go 侧内存不归 JS GC，须 `using` 或手动 dispose） |

并存方案：**`@typescript/typescript6` 兼容包**（tsc6 可执行 + TS 6.0 API 再导出）或 npm alias（`"typescript6": "npm:typescript@6.0.3"`）——TS 7 环境（如 Nest 12 线）里局部用 TS 6 工具链。

TS 6.0 升级硬错误清单（旧配置直接报错）：target es5 / moduleResolution node|node10|classic / **baseUrl 不再支持（paths 相对项目根解析）** / **types 默认 []**（未显式声明则无全局类型——@types/node 项目必配）/ import assert → with / esModuleInterop 不可 false；行为变化：模板字面量类型按 Unicode 码点。

TS 7.1 方向（Beta，2026-10-20）：**Content Mappers**——tsconfig `contentMappers: [{ package, extensions, options }]` + `tsc --runExternalCode`，单文件组件（Vue/Svelte/Astro/MDX/CSS Modules）官方支持方案（Volar 核心模型成一等公民）；Import Attributes in Ambient Modules；Source Phase Imports（`import source`）；`--target es2026` 稳定；7.0→7.1 Beta 编译时间 -13%~-47%、内存 -16%~-50%。

**lint 工具链矩阵**（registry 锚定，2026-11-16）：

| 工具 | 版本 | 关键约束 |
|---|---|---|
| eslint | **10.15.0**（v10 大版本） | Node ^20.19/^22.13/>=24；maintenance 线 9.39.5 |
| typescript-eslint | 8.73.0 | peer eslint ^8.57/^9/^10 + typescript >=4.8.4 **<6.1.0** |
| @biomejs/biome | 2.6.8 | 单二进制 lint+format（eslint+prettier 一体替代选项） |
| oxlint | 1.93.0 | Rust linter；TS 规则配套 oxlint-tsgolint |
| prettier | 3.10.1 | 3.x 线稳定 |

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | 迁 pnpm 后大量 `Module not found` | 幽灵依赖暴露（pnpm 默认隔离是特性） | 补声明 [MO-2]；hoist 仅临时 |
| 2 | 全包 build 先跑完才开始本包 / 依赖没构建就引用 | `["build"]` 与 `["^build"]` 混淆 | 构建链 `^build` [MO-4] |
| 3 | CI 缓存命中后下游 import 不到 dist | outputs 漏配 | [MO-5]（Next 排除 cache） |
| 4 | 改了 env/输入仍用旧缓存（或永不命中） | 缓存 key 漂移 | env/inputs 显式声明 [MO-5] |
| 5 | 发布产物残留 workspace 协议 | 替换语义想当然 | [MO-3] 确认工具链支持 |
| 6 | 子包运行时缺模块 | 运行时依赖放根 package.json | [MO-6] |
| 7 | publish 了旧 dist；apps 误发公共 npm | 忘 build / 漏 private | CI 顺序 + private [MO-7] |
| 8 | turbo 等 dev server 结束挂死 | dev 任务忘 `persistent: true` | [MO-5] |
| 9 | CI 里 `changeset version` 莫名挂（无变更时） | v3 无可发布变更退出码 1 | 脚本容忍空发布 [MO-7] |
| 10 | scoped 库 `changeset publish` 报无权限/403 | v3 `access` 默认 `"restricted"` | config 显式 `"access": "public"` |
| 11 | catalog 引用装包报 `ERR_PNPM_CATALOG_ENTRY_NOT_FOUND_FOR_SPEC` | pnpm-workspace.yaml 漏定义/拼写错 | 补 catalog 条目；`catalogPrune` 清理 |
| 12 | pnpm 12 CI 报 `--frozen-lockfile false` 无效 | Rust 重写拒绝该写法本身 | 改 `--no-frozen-lockfile` [MO-11] |
| 13 | pnpm 12 `--resolution-only` 命令不存在 | 已移除 | `pnpm peers check` [MO-11] |
| 14 | 上 TS 7 后 typescript-eslint 装不上/报 peer 冲突 | peer typescript <6.1.0（不支持 TS 7） | 该项目锁 TS 6.x（@typescript/typescript6）[MO-12] |
| 15 | 上 TS 7 后 Vue/MDX/Astro/Svelte 语言工具失效 | Volar 型工具依赖程序化 API，TS 7.0 无 API | 锁 TS 6.x；等 TS 7.1+ API [MO-12] |
| 16 | 升 TS 6.0 报 baseUrl/target es5/moduleResolution node 硬错误 | 6.0 起这些配置不再支持 | 移除 baseUrl（paths 相对项目根）；target ≥es2015；moduleResolution bundler/node16+；types 显式声明（默认 []） |
| 17 | CI 任务疑似没吃远程缓存全量重跑 | 签名校验失败按 cache miss 静默降级 | 配 remoteCache.signature + 密钥；CI 日志确认命中数 |
| 18 | overrides 写在子包/.npmrc 不生效 | 仅根 pnpm-workspace.yaml 支持 overrides | 移到根 [MO-13] |
| 19 | pnpm patch 报 ERR_PNPM_PATCH_NO_LOCKFILE；编辑目录残留报错 | 未先 install；上次编辑目录未清 | 先 install；--edit-dir 指定/清理 [MO-13] |
| 20 | patch 改依赖 package.json 不生效 | patch 仅支持改代码 | 依赖关系用 overrides [MO-13] |
| 21 | deploy 报 ERR_PNPM_CANNOT_DEPLOY_MANY/DEPLOY_DIR_NOT_EMPTY | filter 选中多项目；目标目录非空 | 恰好一个项目；--force [MO-14] |
| 22 | Docker 镜像塞全仓 node_modules 超大 | 未用 deploy 子集 | pnpm deploy + file: 依赖改写 [MO-14] |
| 23 | 想只给部分包发 beta | pre 模式全仓生效，不支持子集 | 全仓 pre 或 snapshot/手动 dist-tag |
| 24 | pre 模式下依赖包未联动到 beta 版本 | prerelease 不满足 ^range——依赖包也会被 bump | 预期联动面比 stable 发布更大 |
| 25 | snapshot 发布后用户 npm install 装到 0.0.0-xxx | 裸 publish 无 --tag，latest dist-tag 被污染 | publish 必带 --tag [MO-15] |
| 26 | 退出 pre 后 stable changelog 混入 pre 期临时修复 | .changeset/pre/ 里的 changesets 退出后全并入 | 退出前编辑/删除 pre 文件夹条目 |

**Top 展开：坑点 1（幽灵依赖，最高频）**：npm/yarn 扁平 node_modules 下未声明的包"碰巧"能 import；pnpm 真实符号链接结构默认**隔离**，未声明的包装不进来——报错是特性不是 bug。正解逐个补声明；`shamefully-hoist=true` 只作旧工具兼容的临时手段（[MO-2]）。

## API/配置速查表

| 配置 | 要点 | 易错点 |
|---|---|---|
| pnpm-workspace.yaml | `packages: ['apps/*', 'packages/*']` | 与 npm `workspaces` 字段混写 [MO-1] |
| `--filter` | `pnpm --filter <pkg> run x` / `turbo run x --filter=...[origin/main]` | pnpm 与 turbo filter 语法不同 |
| turbo.json tasks | `build: { dependsOn: ["^build"], outputs: [...] }` | `^` 语义 [MO-4]；键名 tasks [MO-10] |
| persistent: true | dev/watch 类任务 | 忘加挂死 [MO-5] |
| env 字段 | 参与缓存 key 的环境变量 | 漏声明 → 旧缓存复用 [MO-5] |
| `npx changeset` | 交互生成变更记录 | 忘写 changeset 合入 main → 静默漏发 [MO-8] |
| `changeset version/publish` | 消费+升版+CHANGELOG / 发 npm | publish 前 build 遗漏 [MO-7]；无变更退出码 1（v3） |
| `changeset git-tag` | v3 名（旧 `changeset tag`） | CI 沿用旧名静默失败 |
| `.changeset/config.json` | `access`（默认 restricted）/`privatePackages`（默认双 false）/`baseBranch`（默认 main）/`format`/`changedFilePatterns`/`fixed`/`linked`/`ignore` | 公开库忘 `"access": "public"` |
| `catalog:` 协议 | pnpm-workspace.yaml 定义 + 依赖字段引用；命名目录 `catalog:<name>` | 发布替换语义 [MO-3]；漏定义报错 |
| `--no-frozen-lockfile` | pnpm 12 关闭冻结安装（`--frozen-lockfile false` 写法被拒） | [MO-11] |
| `pnpm peers check` | peer 依赖检查（替代已移除的 `--resolution-only`） | [MO-11] |
| remoteCache.signature | turbo 远程缓存产物签名（HMAC-SHA256；密钥 TURBO_REMOTE_CACHE_SIGNATURE_KEY） | 校验失败静默按 cache miss |
| overrides | 根 pnpm-workspace.yaml：选择器/类型限定/`-` 删除/`pkg@` 收敛/catalog: 引用 | 子包不生效 [MO-13] |
| pnpm patch / patch-commit | 补丁流：解出编辑 → 提交登记 patchedDependencies | 须先 install；NEVER 改 package.json [MO-13] |
| pnpm deploy | `pnpm --filter=<pkg> --prod deploy <dir>`（12.2+ file: 改写） | 恰好一个项目；目标非空 --force [MO-14] |
| patchedDependencies / allowUnusedPatches | 补丁登记与未用补丁策略（默认 false） | 键优先级 精确 > 范围 > 仅名 |
| @typescript/typescript6 | TS 6 兼容包：tsc6 + TS 6.0 API 再导出 | 与 typescript@7 npm alias 并存 [MO-12] |
| remote cache | Vercel 托管或自托管 | 打不开时静默退化为本地缓存 |
| `changeset pre enter/exit <tag>` | pre 模式开关（写 .changeset/pre.json；exit 只写意图不实际 version） | 不支持部分包；换 tag 直接改 pre.json |
| `changeset version --snapshot [tag]` | 快照版本 0.0.0-{tag}-{datetime}（无 tag 则 0.0.0-{datetime}） | 产物仅供安装验证，不 push/merge [MO-15] |
| `changeset publish --tag <tag>` | snapshot 发布必带 tag；`--no-git-tag` 跳过 git tag | 裸 publish 污染 latest [MO-15] |

## 版本注意

- **pnpm 12.21.0 = Rust 重写已 stable**（registry latest 标签锚定，2026-11-16）——8 项差异与供应链默认防护见「场景：pnpm 12 迁移」；CLI 破坏性变化（[MO-11]）：`--frozen-lockfile false` 拒绝→`--no-frozen-lockfile`、`--resolution-only` 移除→`pnpm peers check` [官方文档](https://pnpm.io)；catalog 关键面不变：命名目录、`catalogMode`（12.3+）、workspace 依赖进 catalog（12.2+）、`file:`/`link:`（12.6+）、`catalogPrune` [官方文档](https://pnpm.io/catalogs)
- **pnpm 配置中枢迁移**（[官方文档](https://pnpm.io/settings)，2026-11-17）：pnpm 12 配置主体在 **pnpm-workspace.yaml**——.npmrc 只保留 auth/registry/TLS/proxy/local-address 五类；overrides/patch/settings 全进 pnpm-workspace.yaml；registry 类 URL 设置不展开环境变量
- **pnpm deploy/patch/overrides 锚定**（v12.2.0+ 文档，2026-11-17）：deploy 恰好一项目/file: 改写/pack 规则产物集/SOURCE_DATE_EPOCH（12.15）/prepare 不跑；patch 须先 install/patch-commit 登记/键优先级 精确>范围>仅名/allowUnusedPatches 默认 false；overrides 仅根/选择器/收敛覆盖/peer 覆写语义 [官方文档](https://pnpm.io/cli/deploy)、[官方文档](https://pnpm.io/cli/patch)、[官方文档](https://pnpm.io/settings/dependency-resolution)
- **TypeScript 双线**（registry 锚定，2026-11-16）：**7.0.2（Go 原生 10×，latest 标签）**｜ 6.0.3（最后 JS 代码库版本）｜ 7.1.0-beta。**7.0 无程序化 API**（7.1 Beta 已补：模块化入口 typescript/sync|async|fs|ast + Disposable API + Snapshots + Content Mappers 单文件组件方案 + es2026 target）[官方文档](https://devblogs.microsoft.com/typescript/announcing-typescript-7-1-beta/)；兼容包 **@typescript/typescript6**（tsc6 + TS 6.0 API 再导出，支持与 TS 7 并存）；TS 6.0 硬错误：target es5/moduleResolution node|node10|classic/**baseUrl 不再支持（paths 相对项目根）**/**types 默认 []**/import assert→with/esModuleInterop 不可 false；TS 7 并行控制 `--checkers N`/`--builders N`/`--singleThreaded`
- **lint 生态矩阵**（registry 锚定，2026-11-16）：**eslint 10.15.0**（v10 大版本；maintenance 9.39.5；Node ^20.19/^22.13/>=24）/ **typescript-eslint 8.73.0**（peer eslint ^8.57/^9/^10 + typescript >=4.8.4 **<6.1.0——支持 TS 6.0、不支持 TS 7**）/ @biomejs/biome 2.6.8 / oxlint 1.93.0（TS 规则配套 oxlint-tsgolint）/ prettier 3.10.1
- **Turborepo 2.11.11**（npm registry `turbo` 锚定，2026-11-15；含 SLSA provenance）；官网 **turborepo.dev**（域名从 turbo.build 迁移），定位 "build system for coding agents" [官方文档](https://turborepo.dev)；Remote Caching 免费（turbo login/link、SSO `--sso-team`）；**产物签名 remoteCache.signature + TURBO_REMOTE_CACHE_SIGNATURE_KEY（HMAC-SHA256，校验失败按 cache miss）**；日志也被缓存 replay；自托管 v8 开放 API 规格
- turbo.json 现行键名为 `tasks`（旧 `pipeline` 为历史版本键）（[MO-10]）
- **changesets 3.0.3**（@changesets/cli，changesets.dev 官方站 + registry 双重锚定，2026-11-15）；v3 breaking：`access` 默认 `"restricted"`、`privatePackages` 默认不版本化、`version` 空跑退出码 1、`tag`→`git-tag`、`--sinceMaster`→`--since`、`prettier`→`format`、`changesets/action@v2`、ESM only、Yarn Classic 不支持；要求 Node `^22.11 || ^24 || >=26` / pnpm ≥10 / npm ≥10.9 / Yarn ≥4.5.2 [官方文档](https://changesets.dev/guide/migration)
- **changesets prerelease/snapshot 锚定**（2026-11-17）：pre enter/exit 流程与 pre.json（PreState）；prerelease 不满足 semver range 的依赖联动 bump；pre 模式 version 后 changesets 移入 .changeset/pre/（退出后并入 stable changelog）；新包额外打 latest tag（npm 强制）；分支隔离模式（next 分支改 baseBranch + CI 放行，合并回前还原）[官方文档](https://changesets.dev/guide/prereleases)；snapshot 版本格式 0.0.0-{tag}-{datetime}、publish 必带 --tag、--no-git-tag、version 产物不 push 原则、pkg.pr.new 替代 [官方文档](https://changesets.dev/guide/snapshot-releases)

## 与其他子领域的集成要点

- **vite-tooling**：workspace 内 Vite 项目复用根配置（`mergeConfig`）；alias 指向 workspace 包 → 见 `kb/vite-tooling.md`
- **Testing**：`turbo run test` 进任务图；CI `--filter` 裁剪 → 见 `kb/testing.md`
- **nextjs**：`.next/**` 缓存排除（`!.next/cache/**`）；Next 项目在 turbo 任务图中 outputs 配置 → 见 `kb/nextjs.md`
- **nestjs**：Nest 库包发布走 changesets；Nest 12 ESM 包在 workspace 内互引注意模块制一致 → 见 `kb/nestjs.md`
- **全仓 TS/lint 版本统一**：typescript / eslint / prettier 版本进 catalog 集中管理；TS 6/7 选线全仓评估（typescript-eslint 与 Volar 型框架锁 TS 6.x，[MO-12]）→ 见本文件「TypeScript 6/7 双线选型」

## 来源索引

- Turborepo 官网（域名迁移/定位语/文档入口）：https://turborepo.dev [官方文档]
- turbo 版本锚定（2.11.11）：https://registry.npmjs.org/turbo/latest [官方文档]
- pnpm 官方文档（workspace/catalog/幽灵依赖语义/pnpm 12）：https://pnpm.io [官方文档]
- pnpm catalog（完整字段语法）：https://pnpm.io/catalogs [官方文档]
- pnpm workspace（workspace: 协议/linkWorkspacePackages 默认 false/v12.7 自动转换/注入依赖）：https://pnpm.io/workspaces [官方文档]
- pnpm 12 Rust 重写（latest 标签/8 项差异/供应链默认防护）：https://pnpm.io + https://registry.npmjs.org/pnpm/latest [官方文档]
- TypeScript 7.1 Beta 公告（程序化 API/Content Mappers/es2026/性能数据）：https://devblogs.microsoft.com/typescript/announcing-typescript-7-1-beta/ [官方文档]
- TypeScript 双线版本锚定（7.0.2 latest/6.0.3/@typescript/typescript6）：https://registry.npmjs.org/typescript/latest、https://registry.npmjs.org/@typescript%2Ftypescript6/latest [官方文档]
- lint 生态版本锚定：https://registry.npmjs.org/eslint/latest、https://registry.npmjs.org/@typescript-eslint%2Feslint-plugin/latest、https://registry.npmjs.org/@biomejs%2Fbiome/latest、https://registry.npmjs.org/oxlint/latest、https://registry.npmjs.org/prettier/latest [官方文档]
- Turborepo Remote Caching（免费/签名/自托管 API 规格）：https://turborepo.dev/docs [官方文档]
- **turbo query（GraphQL 查询/shorthand ls·affected/reason 15 类/浅克隆 blobless 要求/turbo-ignore 弃用迁移表/affectedUsingTaskInputs）**：https://turborepo.dev/docs/reference/query [官方文档]
- **turbo boundaries + Tags（Experimental，两类违规检查/allow·deny 规则传递）**：https://turborepo.dev/docs/reference/boundaries [官方文档]
- **Microfrontends（microfrontends.json/3024 代理/get-mfe-port/routing 语法/fallback/仅本地/@vercel/microfrontends 让位）**：https://turborepo.dev/docs/guides/microfrontends [官方文档]
- **多语言 workspace（package.json 桥接模式/实验性 Rust·Python·Go 原生 workspace）**：https://turborepo.dev/docs/guides/multi-language [官方文档]
- **支持策略（LTS 两年/包管理器矩阵/Experimental·Deprecated 全清单/根级 global* 迁移 globalConfiguration）**：https://turborepo.dev/docs/support-policy [官方文档]
- Changesets 官方站（3.0.3/安装要求/getting started）：https://changesets.dev [官方文档]
- Changesets 配置文件全字段：https://changesets.dev/guide/config [官方文档]
- Changesets v2→v3 迁移指南（breaking 全清单）：https://changesets.dev/guide/migration [官方文档]
- Changesets Prereleases（pre enter/exit 流程/pre.json/换 tag/prerelease 联动 bump/新包 latest tag/.changeset/pre 文件夹管理/分支隔离模式）：https://changesets.dev/guide/prereleases [官方文档]
- Changesets Snapshot Releases（version --snapshot/0.0.0-{tag}-{datetime}/publish --tag 必带/--no-git-tag/不 push 原则/pkg.pr.new 替代）：https://changesets.dev/guide/snapshot-releases [官方文档]
- pnpm deploy（v12.2+ file: 改写/Docker 多阶段模板/错误码族/pack 规则产物集/SOURCE_DATE_EPOCH/deployAllFiles）：https://pnpm.io/cli/deploy [官方文档]
- pnpm patch（patch/patch-commit 工作流/patchedDependencies 键优先级/allowUnusedPatches/NEVER patch 改 package.json）：https://pnpm.io/cli/patch [官方文档]
- pnpm overrides 与依赖解析（选择器/类型限定/收敛覆盖/peer 覆写语义/packageExtensions/allowedDeprecatedVersions）：https://pnpm.io/settings/dependency-resolution [官方文档]
- pnpm settings（pnpm 12 配置中枢迁移 pnpm-workspace.yaml/.npmrc 五类保留）：https://pnpm.io/settings [官方文档]
- [模型经验]：坑点 1-8 的故障模式与修复、`^build` 语义、outputs/env 配置、发版 CI 顺序、目录约定——适用 pnpm 8+/turbo 1.10+/changesets 3+；坑点 9-11 为 v3/catalog 文档锚定
- 法则条款来源：corpus/react/monorepo/elicited/05-laws.md（法则化萃取）

## 冲突消解记录

| 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|
| Turborepo 官网为 turbo.build | 域名迁至 **turborepo.dev**，定位 "build system for coding agents" | 采用文档：引用与来源更新 |
| lerna 是 monorepo 默认方案 | 2026 主流 pnpm + turbo + changesets（lerna 维护减活） | 认知校正 [MO-9]：新项目不选 lerna |
| turbo.json 用 `pipeline` 键 | 现行键名 `tasks` | 采用现行 [MO-10]：骨架用 tasks |
| 幽灵依赖报错是 pnpm 的 bug | 默认隔离为特性（shamefully-hoist 只是兼容开关） | 采用文档语义 [MO-2]：补声明为正解 |
| changesets config `access` 默认公开（public） | v3 默认 **`"restricted"`**（npm scoped 私有为安全默认） | 采用文档：公开发布显式 `"access": "public"` |
| `changeset version` 无变更时空跑成功 | v3 无可发布变更**退出码 1** | 采用文档：CI 脚本显式容忍 |
| `prettier` 字段控制格式化 | v3 改为 `format`（auto 探测，支持 oxfmt/deno/biome/dprint） | 采用文档 |
| pnpm catalog 仅概念性知晓 | pnpm 12 完整字段语法（catalogMode/命名目录/catalogPrune/workspace 依赖进 catalog） | 采用文档：场景与速查表回填 |
| linkWorkspacePackages 默认链接本地包 | **默认 false**——workspace: 协议才链接 | 采用文档：互引一律显式 workspace: 协议 |
| pnpm 12 为 JS 实现（仅配置面变化） | **Rust 重写已 stable**——CLI 语法有破坏性变化（`--frozen-lockfile false` 拒绝等） | 采用文档 [MO-11]：CI 脚本核对旧写法 |
| TS 7 全面替代 TS 6，可直接升级 | 双线并行：typescript-eslint（<6.1.0）与 Volar 型工具不支持 TS 7；7.0 无程序化 API | 采用文档 [MO-12]：按工具链矩阵选线 |
| turbo 远程缓存只缓存产物 | 日志也被缓存 replay；产物可签名校验（校验失败按 cache miss） | 采用文档：签名 + CI 日志确认命中 |
| 供应链默认防护免配即得（含 trustPolicy: no-downgrade） | settings/dependency-resolution：**trustPolicy 默认 off**；真实默认为 minimumReleaseAge 1440 分钟 + blockExoticSubdeps true | 采用 settings 文档：trustPolicy 需显式配置；「新项目防护」限定为 pnpm 官网宣传口径 |
| pnpm 配置主体在 .npmrc | pnpm 12 配置主体在 pnpm-workspace.yaml——.npmrc 只保留 auth/registry/TLS/proxy/local-address | 采用文档：overrides/settings 全进 pnpm-workspace.yaml |
| patch 可改依赖 package.json | patch 仅支持改代码——依赖关系改动用 overrides/pnpmfile | 采用文档 [MO-13] |
| pre 模式 version 后 changesets 照常删除 | 不删除——移入 .changeset/pre/ 留给 stable changelog（可编辑/删除） | 采用文档 |
| prerelease 版本满足 ^range、依赖包不需联动 | prerelease 不满足多数 semver range——依赖包也被联动 bump（比 stable 发布范围大） | 采用文档 [坑点 24] |
| snapshot 发布可与普通发布同命令（裸 publish） | 必带 --tag——裸 publish 使 latest dist-tag 指向 snapshot | 采用文档 [MO-15] |
