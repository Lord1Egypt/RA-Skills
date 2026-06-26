# Failure Modes

## Routing failures

- 如果 agent 的 route decision 不合法或缺少文件，返回结构化错误，并把这一批记为失败。
- 不要把 route 决策失败伪装成低层工具失败。
- 不要在没有明确理由时把文件硬改成 `skip`。
- 如果模型连续失败且 pipeline 启用了 fallback，可以回退到 `suggested_route`，但必须显式记 step，并把该批次标记为 `warning` 而不是静默成功。

## Partial success

- 单文件失败时保留成功文件
- `status` 应为 `partial`
- 必须保留 `failed_files`
- 已成功但补充分支失败时，进入 `warning_files`
- 不支持或低价值格式进入 `skipped_files`

## Storage failure

如果低层提取成功但 `upsert_parsed_files` 失败：

- 返回结构化存储错误
- 不要声称材料已经进入库
- 不要继续推荐后续 skills

## Skip policy

这些情况优先 `skip`：

- office 临时锁文件
- `.zip`
- `.mhtml`
- `.tif/.tiff`
- 明显不是材料资产的低价值文件
