# CLI Proxy 源码架构详解

## 关键源码文件

| 文件 | 作用 |
|---|---|
| `internal/config/config.go` | `SanitizeCodexKeys()` 清理没有 base-url 的 codex-api-key |
| `internal/watcher/clients.go` | `reloadClients` 加载认证文件和 API key |
| `internal/watcher/dispatcher.go` | `refreshAuthState` / `dispatchAuthUpdates` / `dispatchLoop` auth 分发 |
| `internal/watcher/synthesizer/file.go` | `synthesizeFileAuths` 从认证文件生成 auth（JWT id_token→plan_type） |
| `internal/watcher/synthesizer/config.go` | `synthesizeCodexKeys` 从配置生成 codex-api-key auth |
| `internal/access/reconcile.go` | API 认证 provider 的 reconcile |
| `internal/registry/model_registry.go` | `GetModelProviders` / `RegisterClient` / `addModelRegistration` 模型注册表 |
| `internal/registry/models/models.json` | 内嵌模型定义 |
| `sdk/cliproxy/service.go` | `registerModelsForAuth` / `registerResolvedModelsForAuth` 模型注册入口 |
| `sdk/cliproxy/auth/conductor.go` | `Manager.Execute` 请求执行（provider_not_found 来源） |
| `sdk/api/handlers/handlers.go` | `getRequestDetails` / `ExecuteWithAuthManager` |
| `sdk/api/handlers/openai/openai_handlers.go` | `ChatCompletions` / `handleNonStreamingResponse` |
| `sdk/api/handlers/openai/openai_images_handlers.go` | 图片生成 Responses API 转发 |
| `internal/util/provider.go` | `GetProviderName` / `ResolveAutoModel` |
| `internal/thinking/suffix.go` | `ParseSuffix` thinking 后缀解析 |
| `internal/watcher/config_reload.go` | 配置热重载（debounced，SHA256 hash 比对） |

## 认证加载链路（完整）

```
config.yaml + auth-dir
    │
    ▼
reloadClients()  ← 启动时 + 配置热重载触发
    │
    ▼
snapshotCoreAuths()
    ├── synthesizeApiKeyAuths()      — openai_api_keys from config
    ├── synthesizeCodexKeys()        — codex_api_keys from config
    └── synthesizeFileAuths()         — JSON files from auth-dir
    │
    ▼
refreshAuthState()
    │
    ▼
prepareAuthUpdatesLocked()
    ├── diff old vs new auths
    └── generate add/update/remove ops
    │
    ▼
dispatchAuthUpdates()
    │
    ▼
consumeAuthUpdates()  ← dispatchLoop goroutine
    │
    ▼
handleAuthUpdate()
    ├── applyCoreAuthAddOrUpdate()
    │   └── registerModelsForAuth()
    └── applyCoreAuthRemove()
```

## 模型注册逻辑

`registerModelsForAuth(auth)` 根据认证类型决定模型集：

```go
func registerModelsForAuth(auth *core.CoreAuth) {
    switch {
    case auth.CodexAuth != nil:
        if auth.PlanType == "free" {
            models = GetCodexFreeModels()
        } else {
            models = GetCodexProModels()
        }
    case auth.OpenAIAuth != nil:
        models = defaultModels  // gpt-4o, gpt-4o-mini
    }
    registerResolvedModelsForAuth(auth, models)
}
```

**关键点：** `synthesizeCodexKeys`（从 config.yaml 的 codex_api_keys 生成）不设 `plan_type`，因此走 default 分支 → `GetCodexProModels()`（比 Free 多 spark 模型）。

`synthesizeFileAuths`（从 auth-dir 的 JSON 文件生成）会从 JWT `id_token` 的 `plan_type` 字段提取：
- `"plan_type": "codex"` → Codex Pro
- 其他或无 → Codex Free

## 常见误解澄清

### "auth providers unchanged" 不是模型注册问题

日志中的 `auth providers unchanged` 来自 `dispatchAuthUpdates` 中的 reconcile 过程——它将新的认证列表与当前状态对比，无变化时不触发更新。

**这不代表模型注册失败。** 模型注册只在 `applyCoreAuthAddOrUpdate` 中触发，它是 auth 更新链路的一部分，不是独立的 reconcile。

### 管理 API 不显示 auth-dir 不意味着配置无效

```go
// internal/watcher/dispatcher.go
type AuthState struct {
    Auths []*core.CoreAuth `json:"-"`
    // ...
}
```

`json:"-"` 标签意味着管理 API 的 JSON 序列化会排除这些字段。管理 API 返回的信息是安全裁剪过的。
