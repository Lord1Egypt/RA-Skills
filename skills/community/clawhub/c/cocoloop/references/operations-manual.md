# Cocoloop 运维手册

这份手册只服务仓库维护者和后续接手的 Agent，默认留在本地，不进入提交。

## 1. 维护目标

日常维护主要看这几件事：

- 线上 API 是否可用
- 本地 `cocoloop` skill 是否是最新版
- 已知平台安装链路是否还正确
- 发布前回归是否通过
- 出问题时能不能快速回滚

## 2. 仓库现状约束

当前仓库的维护边界：

- CLI 只负责网络 API wrapper 和已知安装流程 wrapper
- 搜索判断、fallback 探索、候选选择和未知环境安装由 Agent 负责
- 测试文件只留本地，不进入提交
- 未实装能力只留在 PRD，不提前写占位代码

## 3. 日常巡检

### 3.1 看工作区状态

先确认本地有没有未提交改动：

```bash
git status --short --branch
```

如果工作区不干净，先区分：

- 用户自己的文档改动
- 当前维护任务改动
- 不该一起发的临时文件

### 3.2 看当前 CLI 是否还能跑

```bash
bash -n scripts/cocoloop.sh scripts/lib/*.sh
```

如果这里失败，先修语法问题，再做其他动作。

## 4. 线上 API 检查

当前 base URL：

```text
https://api.cocoloop.cn/api/v1
```

先检查基础健康：

```bash
bash scripts/cocoloop.sh healthcheck
```

再检查一个真实搜索：

```bash
bash scripts/cocoloop.sh search --query chrome
```

建议重点关注：

- `health/ping`
- `health/`
- `store/skills`
- `store/skills/{id}`
- `safescan/agent-skill-paths`
- `safescan/client/check-upgrade`

如果搜索或详情异常，先分清是：

- 网络层故障
- API 路由故障
- 上游数据异常
- CLI 展示归一化异常

## 5. 更新本地 cocoloop skill

当仓库代码已经更新，需要让本机 Agent 读到最新版 skill 时，执行：

```bash
bash scripts/cocoloop.sh install . --scope user --force
```

预期结果：

- `STORE_PATH` 指向 `~/.cocoloop/skills/cocoloop`
- `TARGET_PATH` 指向当前 Agent 的用户级技能目录
- `INSTALL_STRATEGY` 优先是 `symlink`

更新后要立刻做一次实际调用测试，确认当前 Agent 已经能读到新版 skill。

## 6. 已知平台安装链路检查

当前已知平台：

- `codex`
- `claude-code`
- `openclaw`
- `opencode`
- `molili`

先看本机识别到的当前平台和路径：

```bash
bash scripts/cocoloop.sh paths
```

如果要单独检查某个平台：

```bash
bash scripts/cocoloop.sh paths --agent opencode --os macos
```

重点确认：

- 平台识别是不是对的
- 项目级目录是不是对的
- 用户级目录是不是对的
- 远端路径信息是否和本地实现冲突

Molili 当前以本地确认规则为准：

- macOS/Linux: `~/.molili/workspaces/default/active_skills`
- Windows: `\.molili\workspaces\default\active_skills`

## 7. 发布前最小回归

每次发布前至少跑这组：

```bash
bash -n scripts/cocoloop.sh scripts/lib/*.sh
bash scripts/cocoloop.sh search --query chrome
bash scripts/cocoloop.sh search --query gstack
bash scripts/cocoloop.sh inspect using-superpowers
```

如果当前机器环境允许，再补：

```bash
bash scripts/cocoloop.sh install . --scope user --force
bash scripts/cocoloop.sh paths
```

发布前重点看：

- `search` 是否同时汇总官方和本地已知 Agent 结果
- 本地已知 Agent 命中时，是否提示可移植
- 空结果是否返回 `STATUS: no-results`
- `inspect` 未命中时是否稳定返回 `not-found`
- `install` 是否仍然遵守 `review-required` 和 `handoff-to-agent`

## 8. 提交和发布

先确认这次要发哪些文件，不要把无关改动一起带上。

常用步骤：

```bash
git status --short
git add <需要发布的文件>
git commit -m "<message>"
git push origin main
```

如果有本地维护手册、测试文件或临时产物，确认它们已经被 `.gitignore` 排除。

## 9. 回滚

如果这次发布后发现行为异常，先找刚刚推送的提交：

```bash
git log --oneline -n 5
```

优先做两件事：

- 重新安装上一个稳定版本的本地 `cocoloop` skill
- 回退远端代码到上一个稳定提交

如果只是本地 skill 异常，先重新安装：

```bash
bash scripts/cocoloop.sh install . --scope user --force
```

如果是远端提交需要回退，按团队约定选择回滚方式。默认不要直接用破坏性命令，除非已经确认影响范围。

## 10. 常见故障

### 10.1 搜索有官方结果，但看起来不对

先区分：

- 是 API 返回的候选本身就不对
- 还是 CLI 展示字段错位

可以直接用 `curl` 对比原始接口返回。

### 10.2 本地明明装过 skill，搜索却没看到

先检查目录：

- 当前 Agent 的项目级目录
- 当前 Agent 的用户级目录
- `~/.cocoloop/skills`

再确认该 skill 根目录里是否真的有 `SKILL.md`。

### 10.3 install 直接返回 handoff-to-agent

这通常是正常保护，不一定是 bug。优先判断：

- 当前环境是不是未知平台
- 当前来源是不是页面链接、文章页或不支持的归档
- 已知安装流是不是失效了

### 10.4 search 提示可移植

这说明本地其他已知 Agent 环境里已经有相近或同名 skill。

下一步应该先问用户：

- 要不要直接移植到当前环境
- 还是继续走官方安装

不要在没确认前直接移动或覆盖。

## 11. 文档入口

- 普通使用说明看 `README.md`
- Skill 行为定义看 `SKILL.md`
- 搜索细节看 `references/search-guide.md`
- 安装细节看 `references/install-guide.md`
- 卸载细节看 `references/uninstall-guide.md`
- 这份手册只用于本地维护
