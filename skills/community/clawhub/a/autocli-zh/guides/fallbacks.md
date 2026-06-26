# Fallbacks

在 autocli 需要进入排障、补卡或自定义扩展分支时使用本文件。

## 第一动作

若只是常规环境排障，可先执行：

```bash
autocli doctor
```

但若排障将涉及登录态站点、浏览器桥接状态、Chrome 扩展连接检查，或需要指导用户调整浏览器侧环境，先说明会触达浏览器侧状态并获得同意。

## 健康状态参考

理想情况下应看到：
- Chrome/Chromium: ✓
- Daemon running: ✓
- Chrome extension connected: ✓

## 常见问题

### daemon 未运行
可能表现：
- 命令长时间挂起
- 依赖浏览器登录态的网站无响应

优先检查：
- Chrome 是否已打开
- 重启 Chrome 后再执行 `autocli doctor`

### Chrome 扩展未连接
可能表现：
- 浏览器型站点命令失败
- 公开站点命令可能正常，登录态站点异常

优先检查：
- 扩展是否启用
- Chrome 是否刚重启但扩展尚未恢复
- 再次执行 `autocli doctor`

### 登录态失效
可能表现：
- 结果为空
- 返回不完整
- 某个站点单独失败

优先检查：
- 用户是否仍登录目标网站
- 必要时让用户在 Chrome 中重新登录后再试

### 外部 CLI 缺失
可能表现：
- `gh`、`docker`、`kubectl` 等透传命令失败

说明：
- 这不等于 autocli 核心故障
- 只代表对应外部 CLI 未安装或不可用

## 自定义适配器触发条件

当满足以下条件时，读取 `guides/custom-adapters.md`：
- 已确认用户要访问的网站应由 autocli 承接
- 已用 `autocli <site> --help` 与相关子命令 `--help` 确认后，仍找不到可完成目标的现成命令
- 需要为该网站补一个新的 autocli 适配器

进入该分支前，必须先告知用户：将为该网站自动创建 autocli 自定义适配器。

## 自动补写 target reference 触发条件

当满足以下条件时，读取 `guides/reference-bootstrap.md`，按统一模板补写 `references/<target>.md`：
- 已确认用户请求的目标由 autocli 现成命令支持
- `references/<target>.md` 当前不存在
- 本轮已可直接用 autocli 成功回应用户
- 需要为下次复用补写该目标 reference

## 回退规则

- 若是读操作，且 autocli 当前不可用，可再考虑其他合适工具。
- 若是写操作，不得静默切换到其他执行路径。
