# Cookie 与登录态

## 零配置优先

| 工具 | Cookie 来源 | 配置 |
|------|-----------|------|
| opencli | Chrome Extension 直连 | 零配置 |
| agent-browser | --profile / --auto-connect | 指定参数 |
| browser-use | --connect | 需 Chrome 开调试端口 |
| Stagehand / Zendriver | 文件注入 | sync-cookies.sh export |

## opencli 的 Cookie 机制

Extension Bridge 让浏览器自身发请求，自动带所有 Cookie。SSO token 过期时返回 302 或 exit 77，回 Chrome 重新登录即可。

## 文件导出（仅按需）

```bash
bash scripts/sync-cookies.sh export     # 导出到 unified-state.json
bash scripts/sync-cookies.sh status     # 查看
bash scripts/sync-cookies.sh health     # 健康检查
```

存储: `~/.browser-ops/cookie-store/unified-state.json`
