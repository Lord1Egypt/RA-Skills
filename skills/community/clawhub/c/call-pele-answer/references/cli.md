# pe 命令、路由器与计时

## 目录
- 三个入口
- 其他命令
- 路由器
- 计时与自我优化

## 三个入口

- **`pe answer 回答.md -o 页面.html`**（默认）：路由、组合、派生、渲染一个进程完成，约 0.3 秒（6 块，TypeSafe）。
- **`pe render 稿件.md -o 页面.html`**：你已知道每块的形式，直接写稿件。可从 stdin 读：
  ```bash
  node "${SKILL_DIR}/scripts/pe.mjs" render - -o "<绝对路径>.html" <<'PE_EOF'
  …稿件…
  PE_EOF
  ```
- **`pe options 稿件.md [--json]`**：每块列出准入通过的组件（JEV 概率 + 脚本证据）和“接近门槛”的组件。准入 = 组件自己声明的硬条件（脚本查，如有不同百分比、≥2 个日期、≥3 个路径）全过 + JEV 对它的是/否问题 ≥ 门槛。离线时只给脚本能担保的组件。不预设任何组合。
- **`pe assemble 稿件.md --block <n|标题> --use a,b --as views|stack [-o out.md]`**：把选中组件的骨架拼进这一块；`views` 让原文成为最后一个视图，`stack` 追加在正文后。
- **`pe tune`**：对比“提供过的组件”和“稿件里真正用到的组件”（`~/.call-pele-answer/offers.jsonl`、`usage.jsonl`），提供 ≥8 次使用率 <10% 的门槛 +0.03，没提供却被用 ≥3 次的 −0.03，写到 `admission.json`。设 `PE_NO_LOG=1` 不记录。
- **`pe route answer.md -o draft.md`**：形式拿不准时，路由器逐块给形式，组合器按整页调整；简单形状（时间线、占比、线性步骤、状态转移）直接生成，同一块有多种看法时生成 `views`。按 `<!-- TODO … -->` 补成真实内容、删注释，再 `pe render draft.md`。

## 其他命令

- `pe render 稿件 --output markdown`：压平成聊天 Markdown（分步 → 编号拍，多视图 → 首选视图，图保留 mermaid 围栏）。
- `pe patch <page.html> --panel "块标题" <<'PE_EOF' … PE_EOF`：只改一块。
- `pe check <稿件>`：只检查不出页。
- `pe info`：当前加载的形式、路由器、适配器、主题、输出、规则、插件。
- `pe config set router hybrid`：设默认路由器；`pe route … --device mobile`：窄屏读者。

## 路由器

| `--router` | 怎么问 | 需要 | 实测 |
|---|---|---|---|
| `auto` / `jev`（默认） | 每块 42 道原子是非题，所有块一次请求；代码规则定首选形式和候选。有 `TYPESAFE_API_KEY` 先直连，失败退 `jev-free`，再退 `local` | — | 82 块标注集留出命中 90.2%；5 块一页约 1.5 秒 |
| `jev-free` | 同上，固定经 classifier.dev 转发 | 无 key | 同上 |
| `classifier` | classifier.dev 批量，形式 + 图类型 | 无 key | 20/20，约 1.5 秒 |
| `typesafe` | TypeSafe System One，每块多问题并行 + 置信度门控 | `TYPESAFE_API_KEY` | 19/20，约 0.2 秒 |
| `systemone-free` | 同上，经 classifier.dev 匿名转发，按 IP 限额 | 无 key | 19/20，3–5 秒 |
| `hybrid` | classifier 定形式，System One 复核数据图/流程/低置信度块 | 无 key | 20/20，1.3–4 秒 |
| `local` | 本地关键词规则 | 离线 | 14/20，约 0 ms |

- 失败自动沿降级链走到 `local`，输出会注明。
- **隐私**：除 `local` 外，内容会发到第三方。内部代码、客户数据、未公开信息用 `local` 或自建端点（`plugins.md`）。
- `jev` 规则在 `scripts/core/facets.mjs`：问题、规则、代码硬条件、优先级、覆盖表都在这一处，改完用 `eval/jev-facets/bench.mjs` 回归。
- 门控：没有具体数字不画数据图；一句话能说清不升级；带分支的流程不自动生成线性流程图。
- key 由代理注入（Node 不读 HTTPS_PROXY）时，命令前加 `NODE_USE_ENV_PROXY=1`。
- 路由按块缓存（`~/.call-pele-answer/cache/route.json`，`PE_CACHE=0` 关闭）：改稿后只有改动的块走网络。

## 计时与自我优化

- 每次运行把分阶段耗时追加到 `~/.call-pele-answer/logs/runs.jsonl`（`PE_TRACE=0` 关闭；`--trace` 打印；`PE_LOG_DIR` 指到持久位置）。
- Agent 回合计时：Claude Code 装插件后自动记录（`hooks/hooks.json`，只记工具名和耗时，见安全一节）。其他 Agent 每步开始运行 `node ${SKILL_DIR}/scripts/hooks/agent-hook.mjs mark <步骤>`（如 research、write、pe-answer、verify），交付后 `mark end`。
- `pe stats`：各阶段 p50/p95、每回合模型/工具/pe 占比、最慢调用和改法。每约 20 次运行看一次：路由慢 → 换路由器；TODO 多 → 加派生器或直接写表格；模型占比高 → 少写一遍；非 pe 命令多 → 交付前只跑 `pe check`。

## 安全

- **项目配置不受信任**：`./.call-pele-answer.json` 里的 `plugins`、`adapters` 被忽略（stderr 提示）。信任这个仓库时由用户设 `PE_TRUST_PROJECT=1`。
- **密钥**：只读 `TYPESAFE_API_KEY`、`CLASSIFIER_API_KEY`/`CLASSIFY_API_KEY` 和 `PE_KEY_*`；读取集中在 `scripts/core/keys.mjs`。带 key 的请求只走 https（或本机 http）。
- **`src=` 引用**：按真实路径判断，同名前缀的兄弟目录（`../project-x`）和指向外部的符号链接都算目录外，报 `code/outside`。
- **写文件**：`pe check` 不写任何文件。其他命令的临时稿放在 `$TMPDIR/call-pele-answer-<uid>/`（目录 0700、文件 0600）；日志、缓存、状态同样 0600。
- **日志范围**：`runs.jsonl` 只有本工具的阶段耗时；`agent.jsonl` 对其他工具只记工具名和耗时，对 pe 只记 `pe <子命令>`，不记参数、路径、URL；`offers/usage.jsonl` 只存块标题的哈希。
- **`scripts/vendor/pele.mjs`**：打包压缩后的渲染库（MIT，见 `PELE-LICENSE.txt`），里面的 `javascript:`/`data:` 字符串是它的 URL 消毒代码，不联网、不执行外部代码。

## 稿件与围栏写法（从 SKILL.md 移来）

````markdown
---
title: 标题
subtitle: 一句话摘要（可选）
ste: flavored   # 默认；strict 用于步骤、工具描述、Agent 指令；off 关闭
---
核心结论（第一个 ## 之前的文字）。

## 块标题写“读者会明白什么”
正文、列表、表格、```mermaid 图……

```slider label="学习率" default=0.01
@ 0.001
这个取值下的结果（可嵌 ~~~mermaid）
@ 0.01
…
```

```tabs
=== 方案 A
…
=== 方案 B
…
```

```steps title="三次握手" ms=3000
第一拍：一两句旁白 + 图的第一阶段
---
第二拍：只变一样东西
```
````

`tabs` 放不同的答案；`views`（同样写法）放同一内容的不同看法，第一个是首选。其他 front matter 键会显示在页眉。

主图块（≥6 个节点或有分支）可写成 `views`：`=== 图`、`=== 原文`；只有同一批元素有 ≥2 个可比属性时才加 `=== 表格` 视图。


`pe options` 先把块里已有的表格还原成句子再判断，表格本身不算“该用表格”的证据。`table` 组件只在 ≥2 项 × ≥2 个可比属性（≥6 格）时提供；已写表格的形状（步骤、位置、状态、数字、长选项）会在 lint 里给出改用的组件。lint `route/table-heavy`（多于一块只有表格且无 `<!-- pe:use table -->`）是错误，`route/table-shape`、`route/number-table`、`route/dup-fact` 是警告。
