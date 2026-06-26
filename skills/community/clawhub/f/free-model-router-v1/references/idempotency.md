# 安装幂等性指南

> 本技能支持幂等安装 — 多次触发 setup 不会产生副作用。

## 已安装状态检测

Agent 在触发 setup 前,应检查以下指标判断是否已安装:

| 检查项 | 判断方式 |
|--------|---------|
| Router 是否运行 | `curl http://127.0.0.1:5678/api/status` 返回 `running: true` |
| OpenClaw 是否已配置 | openclaw.json 中存在 `free-model-router` provider |
| cron 任务是否已注册 | `cron list` 检查 `free-model-router-event-check` 和 `free-model-router-daily-status` |

## 幂等行为

- **Router 启动**:已运行则跳过
- **OpenClaw 配置**:已写入 `free-model-router` provider 则跳过
- **初始化**:重复执行时,仅同步 provider 列表,**不会覆盖用户手动设置的主备模型**
- **cron 任务**:先删除旧任务再添加新任务，确保新配置生效
- **API Key / 主模型设置**:用户手动配置的值始终保留

## 二次安装输出

当用户第二次触发 setup 时,CLI 会输出当前状态摘要:

```
free-model-router 已安装,当前状态:
  Router: 运行中 (http://127.0.0.1:5678)
  OpenClaw: 已配置 (free-model-router provider)
  已配置 Provider: openrouter, modelscope
  事件检查任务: 已注册
  每日状态汇报: 已注册

提示:如需重新配置,请先运行 providers 查看当前状态
```

如果仅缺失 cron 任务,会提示缺失的部分:

```
--- 缺失的定时任务 ---
请使用 OpenClaw 内置 cron 工具注册以下缺失的定时任务:
### 任务: free-model-router-event-check
...
```

## 注意事项

- 如果已安装(Router 运行 + OpenClaw 已配置),setup 命令会输出当前状态摘要而非重新配置
- 注册 cron 任务时，先用 `cron delete` 删除旧任务，再用 `cron add` 添加新任务
- 这种方式确保新版本的定时任务配置能够正确生效
