# 插件以什么形式进入 DSH / Deployment 流程 / 卸载（实测 2026-08，dsh-memory 全链路）

> 环境准备与安装方式见 [environment.md](../10-setup/environment.md)。本文件解决"插件以什么形式进入 DSH、怎么部署、怎么卸载"——**部署形态**与代码形态正交。
> 代码形态（[plugin-forms.md](../00-understanding/plugin-forms.md) 的函数/对象/Service）解决"插件长什么样"。

## 1. 六种插件形式（部署/分发形态）

```
┌─────────────────────────────────────────────────────────┐
│  磁盘持久（重启还在）                                      │
│  ① Bundle 插件    → profile 能力底座（内置，只读）          │
│  ② 声明式装配插件  → cordis.patch.yml 里的行（用户加装）    │
│  ③ Agent Preset   → 会话级组合（一个会话有什么）            │
│  ④ Skill          → 技能/方法论（SKILL.md，非 Cordis）     │
├─────────────────────────────────────────────────────────┤
│  进程内临时（重启即失）                                    │
│  ⑤ 动态 Cordis 插件 → cordis_define/run 即时激活           │
│  ⑥ Client 插件     → 浏览器侧 bundle（HMR 热更）           │
└─────────────────────────────────────────────────────────┘
```

| 形式 | 形态 | 作用域 | 持久 | 适合 |
|---|---|---|---|---|
| ① Bundle | 随 DSH 分发的组合包，`dsh.profile.bundles` 列出 | 整个 profile | ✅ | 官方能力底座，普通项目不碰 |
| ② 声明式装配 | 磁盘包/源码目录，patch 层 `insert:` 挂一行 | 整个 DSH 进程 | ✅ | **默认落地形态**：有依赖的正式插件（dsh-memory 即此） |
| ③ Agent Preset | `agent.cordis.yml` 会话组合 | 单会话 | ✅ | 角色/任务工具集、团队模板 |
| ④ Skill | `SKILL.md`（name/description + 正文） | 会话目录 | ✅ | 流程知识复用，零代码 |
| ⑤ 动态 Cordis | `cordis_define` 提交 JS 代码 | 当前进程 | ❌ | 实验/调试/临时扩展 |
| ⑥ Client 插件 | client 包 bundle | 浏览器 | ✅ | 正式前端 UI/主题 |

### 关键区分：⑤ vs ②（最容易混）

- **⑤ 动态插件**：纯 JS、进程内、重启即失、**不能 import 磁盘模块**——只适合临时实验。
- **② 声明式装配**：磁盘文件/包、有依赖、HMR 可热更——正式功能必须走这里。
- 判断口诀：有第三方依赖的正式插件**绝不用动态方式**；先用 ⑤ 验证想法，再固化成 ②。

## 2. 七种 Deployment 流程（变更如何进入运行中的 DSH）

| 流程 | 变更入口 | 生效方式 | 免重启 |
|---|---|---|---|
| ① 配置层部署 | 编辑 `cordis.patch.yml`（profile/home 层） | HMR 事务性重装配 | ✅ |
| ② 包安装部署 | `dsh plugin --profile <n> add <spec>` | bundle 层需重启；非 bundle + patch 行走 ① | ⚠️ |
| ③ 源码/Workspace | file:// 直连 / workspace 包 | HMR 或重启 | ⚠️ |
| ④ 动态部署 | `cordis_define`/`run` | 进程内即时 | ✅ |
| ⑤ Client 部署 | dev:web watcher / build | 开发态 HMR；生产态 build+重启+刷新 | ⚠️ |
| ⑥ Skill 部署 | 复制到 skills 目录 | watcher 即时生效 | ✅ |
| ⑦ Preset 部署 | `agentPresets.copy` → 编辑 → 挂载验证 | 新会话选择时生效 | ✅（新会话） |

### 重启 vs 免重启速查

| 变更 | 免重启？ | 生效时机 |
|---|---|---|
| profile/home `cordis.patch.yml` | ✅ | 保存后立刻（watcher） |
| bundle 层（`dsh plugin add` bundle 包） | ❌ | 重启进程 |
| 非 bundle 包 + patch 行 | ✅ | 走 ① |
| 动态插件 | ✅ | run 激活后 |
| client 包 dev 态 | ✅ | watcher 编译后 |
| client 包生产态 | ❌ | build + 重启 + 刷新 |
| skill | ✅ | 复制后 |
| preset | ✅ | 创建会话时 |

## 3. 声明式插件的卸载流程（实测）

声明式插件卸载 **不走 `cordis_undefine`**（那是 ⑤ 动态插件的工具）——卸载 = **从装配配置移除该行**，由 HMR watcher 自动拆除：

```
① 备份 ──► ② 移除 ──► ③ 等待 HMR ──► ④ 验证两信号 ──► ⑤ 可回滚
 │          │            │              │               │
 │ 含插件行   │ 删 insert  │ watchUserPatches│ 子进程消失   │ 备份写回
 │ 供回滚    │ patch→[]  │ →事务重装配     │ 工具列表清空  │ →HMR重装
 │          │ 不动根yml  │ →disposer回卷   │              │
 │          │            │ →子进程优雅关    │              │
 │          │            │                 │              │
 └──────────┴────────────┴─────────────────┴──────────────┘
```

1. **备份**：`Copy-Item cordis.patch.yml "cordis.patch.yml.bak-with-<name>-<ts>"`（含插件行，供回滚）。
2. **移除**：删掉 `- insert: ...` 块，patch 恢复 `[]`。**不动** profile 根 `cordis.yml`（启动时被重写为空）。
3. **等待**：`watchUserPatches` 检测变化 → 事务性重装配 → entry `_dispose()` → 插件 disposer 全回卷 → 子进程优雅关闭。
4. **验证两信号**：常驻子进程消失（`Get-CimInstance Win32_Process -Filter "Name='python.exe'"` 无输出）+ 工具列表清空（`cordis_inspect_query` host/Tool/listTools）。
5. **回滚**：把备份写回 patch → HMR 重新装配。

卸载与装载同一条事务路径：任一 entry 失败整体回滚到上一棵好树，不会半卸载。

| 形态 | 卸载方式 | 持久性 |
|---|---|---|
| 声明式（patch） | 删 patch 行 → HMR 重装配 | 磁盘配置，重启后不加载 |
| Bundle 层 | `dsh plugin --profile <name> remove <package>` / 移出 bundles → 重启 | 磁盘配置 |
| 动态插件 | `cordis_stop`（暂停）/ `cordis_undefine`（永久删） | 进程内，重启本就丢失 |
| Skill | 删 skills 目录 → watcher 即时移除 | 磁盘 |

## 4. dsh plugin 命令参考

`dsh plugin` 底层转发给 pnpm，所有 pnpm 子命令均可使用。

### 安装

```sh
dsh plugin --profile <name> add <package>
```

`--profile` 是**必选参数**，指定目标配置文件（如 `web`、`desktop`）。`<package>` 支持 NPM 包名、GitHub 仓库（`github:owner/repo`）、本地路径（`file:`/`link:`）。

### 卸载

```sh
dsh plugin --profile <name> remove <package>
```

pnpm 执行 `remove` 成功后，`reconcilePlugins` 自动对齐 profile 的 `dsh.profile.bundles` 层列表：

- 包从 `dependencies` 消失且之前在 `bundles` 列表里 → **自动移除**出层栈
- 包仍存在于 `dependencies`（间接依赖）但不再声明 `dsh.bundle` → 从层栈摘除
- 模板内置 bundle（如 `dsh-base`）**不是 dependency**，不会被误删

### 其他子命令

```sh
dsh plugin --profile <name> update <package>    # 更新
dsh plugin --profile <name> why <package>        # 查看依赖原因
dsh plugin --profile <name> list                 # 列出已安装包
```

所有 pnpm 参数原样转发（`allowUnknownOption` + `argument '[args...]'`），pnpm 支持的任何子命令均可使用。

## 5. 实战沉淀

> 来源：DSH-Context-Pro 项目实测

### 4.1 Provider 配置与配额

**429 双形态**：
- `insufficient_quota`：账户余额用尽，需充值
- `rpm exhausted`：每分钟请求数超限。两者都是账户级问题，非代码 bug

**默认 provider**：`settings.yaml` 的 `agent-default-model.provider` 指定实际使用的 provider，不是 `llm-pi-ai.providers` 下的第一个。

**retryPolicy 必须配到实际使用的 provider**：`llm-pi-ai.providers.<provider>.retryPolicy` 才有意义；`maxRetries: 5` + `initialDelayMs: 3000` + `maxDelayMs: 15000` = 5 次指数退避重试（3s→6s→12s→15s→15s，上限 15s）。

**配置变更需重启**：settings.yaml 变更需要重启 dsh web 进程（HMR 只热重载插件装配，不含 provider 配置）。

### 4.2 会话日志解码（崩溃定位利器）

**DSH 会话日志路径**：`~/.dsh/sessions/<session-dir>/<session-id>/session.jsonl.zstd`（zstd 多帧格式）

**解码工具链**：harness 的 `packages/session/session-persistence-jsonl/src/zstd.ts` 的 `scanZstdFrames()` + `zstd-public-decoder.ts` 的 `PublicZstdFrameDecoder` 可逐帧解码。

**关键事件类型**：
| 事件类型 | 含义 |
|---------|------|
| `turn/end` | 含 error message + code，崩溃时查看 |
| `turn/start` | 轮次开始 |
| `step/start` | 步骤开始 |
| `step/end` | 步骤结束 |
| `user/message` | 用户消息 |
| `assistant/message` | 助手回复 |
| `llm/retry` | 含 failure 详情 |
| `assistant/chunk finish` | 含 reason.error |

**崩溃定位法**：
- `turn/end error` 无堆栈但有 error message → 结合前后事件还原
- 无 request/header 说明 LLM 调用前就崩了
- 有 request/header 但无 assistant/chunk 说明 LLM 调用失败
