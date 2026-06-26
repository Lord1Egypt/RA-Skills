# Failure Modes

## Blocking readiness

- 可以生成 truthful package
- 不能把 `ready_for_submission = false` 翻成 `true`

## Missing real files

- 如果定位不到真实源文件路径，不得生成“看似完整”的 zip
- 缺文件要结构化失败或 partial

## Invalid agent selection

以下情况必须失败：

- 选中不存在的资产
- 改写 lifecycle readiness
- 与已验证 lifecycle 结果冲突
