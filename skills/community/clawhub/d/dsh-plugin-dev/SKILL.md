---
name: dsh-plugin-dev
description: Develop, verify, package, publish and list DeepSeek Harness (DSH) plugins. Scaffolds a runnable dsh.bundle plugin (package.json manifest + cordis.patch.yml + tool plugin), runs mechanical exit-code checks, and walks the npm/GitHub/tarball publish paths plus the awesome-dsh-plugin listing PR. Use when the user wants to create, develop, package, publish, debug or list a DSH / DeepSeek Harness plugin for the SkillHub plugin marketplace. 触发词：DSH 插件、DeepSeek Harness 插件、插件广场插件、开发 DSH 插件、dsh plugin、插件收录、awesome-dsh、cordis 插件。
version: 1.0.0
license: MIT
---

# DSH 插件开发助手

帮用户从零做出一个**可安装、可发布、可收录**的 DeepSeek Harness（DSH）插件。
本 skill 目录下自带两个零依赖脚本：`scripts/scaffold.mjs`（生成骨架）与 `scripts/check-plugin.mjs`（机械自检，退出码裁决）。

## 背景速览（30 秒）

- DSH = DeepSeek Harness，底层是 vendored Cordis 框架，「一切皆插件」。
- 社区分发范式 = **npm 包 + `dsh.bundle` manifest + `dsh plugin add`**。
- SkillHub 插件广场（1.5 万+）只是该生态的索引站，数据自动从 GitHub 同步——**收录的唯一入口是 PR 到 awesome-dsh-plugin 仓库**。
- 当前基线：`dsh-v0.1.1-rc.2`、`pnpm@11.7.0`、Node ^22.19 || >=24。DSH 处于破坏性演进期，不承诺旧版兼容。

## 工作流（按序执行，不要跳步）

### 1. 需求确认

向用户确认（一次问清）：

- 插件做什么？→ 最常见是**注册一个模型可调用的工具**（tool）；也可能是服务、事件监听、Web 前端。
- npm 包名：推荐 `dsh-<名称>`，或用 scoped 名 `@<npm账号>/dsh-<名称>` 防抢占（scoped 必须显式 `--access public`）。
- 有没有 npm 账号 / GitHub 仓库？（决定走哪条发布通道）

### 2. 生成骨架

```bash
node <本skill目录>/scripts/scaffold.mjs --dir <目标目录> --id <插件id> [--pkg <包名>] [--tool <工具名>]
```

产出（纯 ESM JS，**免构建、免 prepare 授权**，npm 可直发）：

- `package.json`：已声明 `dsh.bundle` manifest（只声明 `dsh.client` 会被拒；无 `dsh.bundle` 只会被当普通依赖安装并告警）
- `cordis.patch.yml`：`- insert:` 一行，`name` 写包名（Node 解析，不是源码路径）
- `index.js`：最小可用工具插件（defineTool）
- `README.md` + `.github/workflows/publish.yml`（推 tag 自动发 npm + GitHub Release）+ `.gitignore`

### 3. 实现插件

在骨架 `index.js` 上改。工具 DSL 速查：

```js
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = '<插件id>'
export const inject = ['tools']

export function apply(ctx) {
  ctx.tools.register(defineTool({
    name: 'my_tool',                                   // 工具名，勿与其他插件撞名
    description: '一句话说清工具用途',                    // 会展示给模型
    parameters: { q: { type: 'string', required: true, description: '参数说明' } },
    output: { schema: { type: 'string' }, render: (_args, v) => [{ type: 'text', text: v }] },
    async execute(args) { return `result: ${args.q}` }, // 返回值须符合 output.schema
  }))
}
```

细节规范（Config schema、服务、事件、生命周期、manifest、陷阱）→ **读 `references/plugin-spec.md`**，写完代码前必读其「陷阱」一节。

### 4. 机械自检（发布前必过）

```bash
node <本skill目录>/scripts/check-plugin.mjs <插件目录> [--listing <data/plugins/xxx.yml>]
```

退出码裁决：**0=PASS，1=FAIL，2=用法/内部错误**。模型只允许转述输出块，无权改判。
FAIL 项逐条修复后重跑，直到 PASS 才进入发布。

### 5. 发布（三选一，推荐 npm）

| 通道 | 用户安装 | 前提 |
|---|---|---|
| **npm（推荐）** | `dsh plugin --profile <p> add <包名>` | `npm publish`（scoped 加 `--access public`） |
| GitHub 仓库 | `add github:<user>/<repo>` | 纯 JS 骨架免 prepare；TS 必须自包含 `prepare` 构建脚本 |
| tarball | `add ./x-0.1.0.tgz` | `npm pack` 产物，零权限 |

发布细节（2FA/Automation token、scoped 规则、abbreviated metadata 延迟、CI 配置）→ **读 `references/publish-and-listing.md`**。

### 6. 收录到插件广场

PR 到 `github.com/awesome-dsh-plugin/awesome-dsh-plugin`，**只新增一个文件** `data/plugins/<owner>__<repo>.yml`。
硬要求（CI 会自动查，缺一即拒）：真实可用代码（纯 README 仓库不收）、仓库创建满 1 天、GitHub topic 加 `dsh-plugin`、描述与代码相符（写了几个工具就得有几个）、值里含 `": "` 必须加引号。
字段与分类池、PR 模板 → **读 `references/publish-and-listing.md`** 第 6 节。

### 7. 验证安装链路（可选，有 DSH 环境时）

```bash
cd <deepseek-harness 仓库根>
pnpm dsh plugin --profile dsh-plugin-test add <插件目录>   # 或 tgz / npm 包名
pnpm dsh --profile dsh-plugin-test --dump-config | findstr <插件id>   # 应看到 "# == <包名>" 层
# 用完删除：Remove-Item -Recurse -Force <DSH_HOME>/profiles/dsh-plugin-test
```
