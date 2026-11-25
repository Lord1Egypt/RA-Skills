# 排障

## 先看实际状态

```bash
python3 scripts/wb_bus.py status
find "<WB_BUS_HOME>/queue" -maxdepth 2 -type f -print
```

不要先重新派发。先确认任务是否在 pending、claimed、completed 或 failed，再决定动作。

## 任务一直在 pending

- 自动触发器未运行或权限不足。
- 没有 WorkBuddy worker 调用 `claim`。
- 任务包或队列 JSON 损坏。

处理：检查任务包存在；人工执行 `claim`；把真实 package 路径按 `references/开工提示词.md` 交给 WorkBuddy。不要复制第二份任务。

## 任务卡在 claimed

- WorkBuddy 崩溃、关闭或未调用 `complete`。
- 回执已写但完成命令未执行。

处理：先看 `receipt_path` 是否存在。存在则核对内容后执行 `complete`；不存在则让原 worker 继续。确认 worker 已失联且需要重派时，手工把 JSON 移回 pending前先备份并写审计。

## complete 提示回执不存在

- 路径错误，或只写了草稿未保存。
- 回执被移动/删除。
- 模板被误复制为空文件。

处理：找到实际回执，确认非空且包含真实证据；不要创建空回执绕过检查。

## WBV 回执没有结论码

必须包含且只使用：

- `WB_PASS`
- `WB_FAIL`
- `WB_PARTIAL`

没有结论码、只写“通过”、没有实际 EXIT 或无法复跑时不得标记通过。补验使用新包，不修改旧回执。

## 复验命令 EXIT=127

先判断是工具缺失还是交付失败。WorkBuddy shell 不保证有 `rg`、`codex` 或交互式别名。改用 Python、绝对路径工具或纯 shell 后新建验收编号。不要为了命令通过而改规则文本。

## 文件哈希不一致

判 `WB_FAIL`。保留差异和验收包，停止合并/发布；Codex 从版本控制或备份恢复后另建新验收包。不得覆盖 WorkBuddy 的回执。

## WBC 入口缺失

候选目录必须有 `验证请求.md`，总线应有 `待验证/<编号>.md`。缺任一项先补请求，不要用一句“已经测过”代替。用户回 Codex 输入“验收 `<编号>`”才启动最终复跑。

## 自动触发器失效

- 检查监听程序、日志、权限和运行状态。
- 检查 pending>0、claimed=0；已有 claimed 时不要重复触发。
- 空队列不启动模型。
- 不恢复每小时 ACTIVE 轮询，不重建需要系统权限的 Helper。
- 修不好就用手动兜底，任务包和队列不丢。

## 数据边界触发

命令需要联网、上传、调用云 OCR/视觉、写生产数据库或扩大外发范围时立即停止。记录范围为 `PARTIAL` 或 `FAIL`，由用户决定。不得自行扩大授权。

## 台账或复盘写入失败

任务结果仍保留在队列 JSON 和回执中。先修复目录权限/路径，再运行 `complete`，不要手工伪造完成状态。若台账行已存在，脚本只追加一次复盘，不重复创建任务。

## 清理

只清理本次测试产生的临时目录、`__pycache__` 和缓存。任务包、回执、候选、原始资料、交付物、台账和复盘必须保留。批量删除优先 `find -delete`，不要使用 `rm -rf`。
