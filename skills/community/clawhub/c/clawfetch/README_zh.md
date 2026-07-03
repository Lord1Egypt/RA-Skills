# clawfetch Skill

这个目录是面向 OpenClaw/ClawHub 的 `clawfetch` npm CLI 薄层 skill 包装。它不是独立 scraper 项目，也不复制 clawfetch 源码。

## 为什么存在

这个 skill 让 Agent 能把 clawfetch 当成受控工具调用，用于把一般网页、GitHub README 页面和 Reddit 线程转换成适合知识库处理的 markdown。真正的抓取实现、runtime 生命周期、站点策略和错误恢复都仍然只由 clawfetch CLI 负责。

## 首次可用安装模型

安装这个 skill wrapper 不等于已经得到可直接运行的 clawfetch 环境。第一次使用时，Agent 必须完成下面所有阶段。

1. 安装或复制这个 skill wrapper 目录。
2. 进入已安装的 skill 目录，也就是包含 `SKILL.md` 和 `bootstrap_deps.sh` 的目录。
3. 把已发布的 npm CLI bootstrap 到当前 skill 目录：

```bash
cd <installed skill directory>
sh bootstrap_deps.sh
```

4. 通过 CLI 安装 browser runtime：

```bash
node node_modules/clawfetch/clawfetch.js runtime install
```

5. 抓取前检查 runtime：

```bash
node node_modules/clawfetch/clawfetch.js runtime check
```

只有第 5 步成功后，Agent 才应该把 clawfetch 视为已经可以执行 browser-backed 抓取。

可选 smoke test：

```bash
node node_modules/clawfetch/clawfetch.js https://example.com
```

成功时应输出 `--- METADATA ---` 和 `--- MARKDOWN ---`。

bootstrap 脚本会把已发布的 `clawfetch` npm 包安装到当前 skill 目录，形成 `node_modules/clawfetch`，并在报告成功前验证 `node_modules/clawfetch/clawfetch.js` 确实存在。它不安装 browser runtime，不执行 `git clone`，不下载源码树，不修改全局 npm 状态，不改系统 PATH，也不安装无关工具。

默认情况下，脚本跟随项目根目录 `package.json` 中的版本。如果这个 wrapper 被单独分发、读不到项目根目录，则回退到脚本中固定记录的版本。这个 fallback 只是为了独立 ClawHub 分发场景存在，维护时必须和当前对外发布的 CLI 版本保持一致。

## 配置文件

这个 skill 随包包含正式配置文件：

```text
clawfetch.toml
```

在正常 skill 布局中，CLI 入口是：

```text
node_modules/clawfetch/clawfetch.js
```

这个 CLI 会把当前 skill 目录下的 `clawfetch.toml` 解析为固定宿主配置。
它不会从调用方当前工作目录向上搜索。FlareSolverr 的长期配置应维护在这个
文件里，而不是放进 `node_modules/clawfetch`，因为 `node_modules/clawfetch`
是 npm 安装产物，bootstrap、repair 或 upgrade 时可能被替换。

默认配置：

```toml
[flaresolverr]
enabled = false
# url = "http://127.0.0.1:8191"
max_timeout_ms = 60000
```

如需启用 FlareSolverr，请编辑 `clawfetch.toml`，把 `enabled` 改为 `true`，
并填入可访问的 `url`，例如本机的 `http://127.0.0.1:8191`，或 Docker /
服务网络里的 `http://flaresolverr:8191`。`FLARESOLVERR_URL` 仍然兼容旧流程
和临时覆盖，但不再是推荐的主配置路径。

## 使用方式

bootstrap 且 `runtime check` 成功之后，通过本地 CLI 调用：

```bash
node node_modules/clawfetch/clawfetch.js https://example.com/article
node node_modules/clawfetch/clawfetch.js https://github.com/owner/repo
node node_modules/clawfetch/clawfetch.js https://www.reddit.com/r/example/comments/...
```

runtime 生命周期命令也必须走 CLI：

```bash
node node_modules/clawfetch/clawfetch.js runtime install
node node_modules/clawfetch/clawfetch.js runtime check
node node_modules/clawfetch/clawfetch.js runtime repair
node node_modules/clawfetch/clawfetch.js runtime upgrade
node node_modules/clawfetch/clawfetch.js runtime diagnose --json
```

skill 层不直接管理 browser runtime。它应该把 CLI 输出的 `NEXT:` 提示展示给 Agent 或操作者，而不是发明另一套恢复路径。

browser runtime 的安装位置和生命周期由 CLI / 项目本体决定。这个 wrapper 不参与路径选择、runtime 修复逻辑或版本匹配。

如果安装或检查失败，运行：

```bash
node node_modules/clawfetch/clawfetch.js runtime diagnose --json
```

然后按照 CLI 输出的 `NEXT:` 提示处理，不要在 skill 层发明另一套绕行方案。

## 边界

这个 skill 不实现抓取逻辑、浏览器启动逻辑、Playwright 包解析、browser runtime 管理、GitHub fast-path、Reddit RSS 处理、FlareSolverr 支持或 markdown 转换。

这个 skill 也不隐藏下载逻辑，不 clone 仓库，不做与抓取无关的文件系统操作，也不作为通用 shell 工具使用。

ClawHub 发布的 skill 内容遵循其 registry 侧的授权策略；`clawfetch` npm CLI 包仍然单独使用 Apache-2.0 授权。
