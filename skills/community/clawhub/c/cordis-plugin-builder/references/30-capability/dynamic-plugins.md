# 动态 Cordis 插件：运行时开发（实测契约）

> 动态插件 = `cordis_define` 提交一段 JS 代码 → `cordis_run` 在当前进程激活。**进程内、重启即失、
> 纯 JS**（不能 import 磁盘模块）。适合实验/临时扩展；正式功能固化为静态插件（见 [deployment-overview.md](../50-ship/deployment-overview.md)）。

## 1. 生命周期脑图

```
cordis_define ──→ cordis_run ──→ (运行中) ──→ cordis_stop ──→ cordis_run(再激活)
   │(记录代码)      │(激活)        │            │(暂停,保留定义)
   │                │              │            └─→ cordis_undefine(永久删)
   │                └─ awaiting-approval → 授权 → starting → 完成
   └─ 定义不执行 apply；重启后全部丢失
```

## 2. 构建流程（标准四步）

1. **查接口**：`cordis_inspect_list` → 对每个要用的 Service/Event/Builtin/Slot 精确查询（不猜 API）。
2. **写代码**：`code.host` / `code.client` 各为普通 JS 函数体，返回 Cordis Plugin。
3. **提交**：`cordis_define`（新插件给 3–6 字母语义前缀；改已有用 `kind:'existing'` + 原 pluginId）→ 得 `pluginId` + `packageId`。
4. **激活**：`cordis_run`（首跑/重启 `run`；切版本 `update`）→ 可能返回 `awaiting-approval` 或 `starting`——**都不是成功**，等系统通过 steering 回报最终状态。

## 3. 双平台 Builtin（实测）

| | Host | Client |
|---|---|---|
| 可用 | `ctx`、`harness`、`console`、`btoa/atob`、`TextEncoder/Decoder` | `ctx`、`React`(仅 createElement)、`host`、`styles`、`console` |
| 工具注册 | `harness.defineTool` / `harness.registerTool(ctx, tool)` | — |
| Host RPC | `harness.handle(method, handler)` | `host.call(method, args)`（仅 JSON） |

## 4. 硬约束（违反即失败）

- **纯 JS**：无 `import`/`require`/TS/JSX/装饰器；Client 用 `React.createElement`。
- **全局只信 Builtin**：不假设 `process`/`Buffer`/`window`/`document`/`fetch`/原生 `setTimeout`；定时器是 `timer` Service（`inject: ['timer']`）。
- **服务访问**：可选依赖 `ctx.get('name')` + undefined 检查；硬依赖才 `inject`（`ctx.name` 未声明 inject 会被 Guard 拒）。
- **副作用可逆**：`ctx.on()`/`ctx.effect()` 自带 disposer；工具/Slot/主题/定时器保留返回的 disposer；stop/update/undefine 全部回卷。
- **不序列化 live 数据**：不 JSON.stringify/structuredClone Service、Session、Event 载荷；只读叶子字段。
- **异步不等待**：授权/浏览器结果在本轮 Tool 内等不到——返回后等 steering；失败用 `cordis_inspect_self` 读诊断。

## 5. 版本与授权语义

- Package **不可变**：改代码 = 追加新 Package，永不覆盖旧版。
- `currentPackageId` = 最近成功；`nextPackageId` = 待授权/激活/最近失败。
- 单勾授权当前版本；双勾授权未来版本；**技术失败后授权仍有效**。
- 更新失败**不会**自动回滚旧 Run——恢复需显式 `run` current。

## 6. 修复流程（技术失败）

```
cordis_run 失败
   │
   ▼
① cordis_inspect_self 读源码+报错
   │
   ▼
② 涉及未知能力？ ──是──► 重新 list/query Provider
   │否
   ▼
③ 同一 Plugin 追加新 Package（不覆盖失败版）
   │
   ▼
④ cordis_run 用新 packageId + 正确 mode
   │        update=重试 next / run=回滚 current
   ▼
⑤ 用户拒绝授权？ ──是──► 停止，不再自动重试
```

1. `cordis_inspect_self(pluginId, packageId)` 读源码 + 报错。
2. 涉及未知能力 → 重新 list/query Provider。
3. 同一 Plugin 追加新 Package（不覆盖失败的）。
4. `cordis_run` 用新 packageId + 正确 mode（`update` 重试 / `run` 回滚）。
5. 用户拒绝授权后**不再自动重试**。

## 7. 动态 vs 静态：何时用哪个

| 场景 | 选 |
|---|---|
| 验证一个想法、临时工具/UI、探针 | 动态 |
| 有依赖的正式插件（dsh-memory 类） | 静态（cordis.patch.yml 装配） |
| 先动态试 → 验证后固化 | 动态验证 → 抄成静态插件 + npm pack |

### 持久 Client-Host 通信的陷阱与替代

动态插件的 `harness.handle` + `host.call` 是 Client-Host 通信的便捷方式，但**不持久**（重启丢失）。如果 Client UI 需要持久通信层：

- ❌ **不要**把生产 UI 的 RPC 桥接放在动态插件里——每次重启都要手动重建
- ✅ **改用** `webServer.register()` HTTP 端点（源码加载插件可用，重启不丢）
- 详见 `client-ui.md` 第 3.5 节
