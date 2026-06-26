# C盘安全清理 Skill

## 元数据（触发层）

- name: c-drive-safe-cleanup
- description: 在 Windows 的 C 盘上执行“白名单目录”的安全清理。仅扫描临时文件、缓存、日志、预读、AppData 暂存和（若已安装）WPS 暂存/缓存目录；逐项用中文解释用途与清理影响，并逐项询问“是否清理”；仅在用户明确同意后删除目录内容（保留目录本身）；最终输出 Markdown 清理日志。禁止全盘扫描、禁止自动删除下载/桌面大文件、禁止修改注册表、禁止触碰系统核心目录。用于用户明确希望释放 C 盘空间且要求安全可控清理的场景。

## 目标

在不触碰系统核心目录的前提下，按白名单目录做垃圾扫描；逐项解释用途与影响；逐项征求用户确认；仅在确认后清理目录内容（保留目录）；最后输出 Markdown 清理日志。

## 适用场景（When）

- 用户明确要求“清理 C 盘空间”“清理缓存/临时文件/日志垃圾”“C盘满了”。
- 用户接受“只清理安全目录白名单”，不做全盘扫描。

## 不适用场景（When NOT to use）

- 用户要求全盘扫描、自动删除下载/桌面大文件、修改注册表。
- 用户要求删除系统核心目录内容（如 `C:\Windows\System32`、`C:\Windows\WinSxS`、`C:\Program Files`）。

## 强制安全边界

> 安全边界详细规则见：`references/safety.md`

1. 仅允许访问并处理“白名单目录”。
2. 绝不递归扫描白名单外路径。
3. 删除动作只删除目录下内容，不删除目录本身。
4. 每个目录必须单独确认后才可执行删除。
5. 对下载/桌面大文件只提醒，不自动删除。
6. 不执行注册表读写或系统配置变更。

## 白名单目录（Windows / C盘）

> 说明：以下为默认白名单。实际执行前需先判断路径是否存在。

1. `%TEMP%`（当前用户临时目录）
2. `%LOCALAPPDATA%\Temp`
3. `%WINDIR%\Temp`
4. `%WINDIR%\Prefetch`
5. `%LOCALAPPDATA%\Microsoft\Windows\INetCache`（浏览器/系统网络缓存）
6. `%LOCALAPPDATA%\Microsoft\Windows\WER`（错误报告缓存）
7. `%LOCALAPPDATA%\CrashDumps`（崩溃转储）
8. `%LOCALAPPDATA%\Packages\*\LocalCache`（商店应用缓存）
9. `%PROGRAMDATA%\Microsoft\Windows\DeliveryOptimization\Cache`（更新分发缓存）
10. `%LOCALAPPDATA%\D3DSCache`（图形着色器缓存）
11. `%LOCALAPPDATA%\NVIDIA\DXCache` 与 `%LOCALAPPDATA%\NVIDIA\GLCache`（若存在）
12. `%APPDATA%`、`%LOCALAPPDATA%` 下已卸载应用遗留缓存目录（仅限明确匹配 `cache/tmp/log` 命名且可识别为非系统应用）
13. WPS 缓存/暂存目录（仅在检测到已安装 WPS 时启用）：
   - `%APPDATA%\kingsoft\office6\temp`
   - `%LOCALAPPDATA%\Kingsoft\WPS Office\*cache*`
   - `%LOCALAPPDATA%\Kingsoft\WPS Office\addons\pool\win-i386`
   - 其他位于 `C:` 且可明确识别为 WPS 临时/缓存语义的目录（名称包含 `temp/cache/backup`，且不在系统核心目录内）

### WPS 目录启用条件

- 仅当检测到 WPS 安装痕迹时才纳入扫描（如存在 `WPS.exe`、`Kingsoft` 相关安装路径或上述用户目录）。
- 若未检测到安装痕迹，则跳过所有 WPS 相关目录，不报错。

## 每类目录的中文解释模板（Explain）

对每个目录必须输出三段说明：

- **这个目录做什么**：一句话说明用途。
- **为什么会产生垃圾**：说明缓存、日志、崩溃文件累积原因。
- **删除影响**：说明是否会导致首次启动变慢、需重新生成缓存，且不影响系统核心功能。

示例：

- `%TEMP%`
  - 作用：程序运行时的临时文件存放区。
  - 垃圾来源：安装包解压、更新中间文件、程序异常退出残留。
  - 删除影响：可安全清理，个别程序首次打开可能稍慢。

- `WPS 缓存/暂存目录`
  - 作用：存放 WPS 文档编辑过程中的自动保存、预览和插件缓存文件。
  - 垃圾来源：历史编辑残留、异常退出后的临时副本、组件更新缓存。
  - 删除影响：不会删除正式文档，但可能清空最近临时记录，首次打开 WPS 相关功能可能重新生成缓存。

## 交互确认规则（Ask）

按目录逐项提问，不得一次性默认全选。

额外约束：

- 目录大小必须基于实际扫描结果，禁止凭经验或猜测填写“可释放空间”。
- 若目录不存在，必须明确标注“未检测到该路径，估计可释放 0 B”，不得将其计入任何汇总。
- 涉及 WPS 时，需区分“检测到安装痕迹”与“检测到可清理目录”，禁止混用表述。

提问模板：

`目录：<路径>`
`预计可释放：<大小>`
`说明：<作用/来源/影响>`
`是否清理该目录？（是/否/跳过）`

规则：

- 选择“是”：进入删除步骤。
- 选择“否”或“跳过”：记录为未清理，继续下一项。
- 用户未明确回答“是”时，禁止删除。

## 执行删除规则（Execute）

1. 删除前再次确认目标路径在白名单内。
2. 删除目录内文件和子目录，保留根目录。
3. 遇到“文件占用/权限不足”：
   - 跳过该文件；
   - 继续清理其余内容；
   - 在日志中记录失败原因。
4. 删除后重新统计该目录已释放空间。

## 日志规则（Log）

清理完成后，生成 Markdown 日志文件：

- 建议路径：`tasks/evaluation-<YYYY-MM-DD>-c-disk-cleanup.md`
- 必填字段：
  - 操作时间
  - 操作系统与盘符
  - 清理策略（白名单、逐项确认、不做项）
  - 每个目录的处理结果（已清理/跳过/失败）
  - 每项释放空间与总释放空间
  - 失败项与原因
  - 用户确认记录（逐项）

日志模板：

```markdown
# C盘清理日志

- 时间：2026-04-21 20:30:00
- 盘符：C:
- 策略：仅白名单目录；逐项确认；不扫全盘；不删下载/桌面大文件；不改注册表

## 明细

| 目录 | 说明 | 用户选择 | 结果 | 释放空间 |
|---|---|---|---|---|
| %TEMP% | 临时文件目录 | 是 | 已清理 | 1.2 GB |
| %WINDIR%\Prefetch | 预读缓存 | 跳过 | 未执行 | 0 GB |
| %LOCALAPPDATA%\CrashDumps | 崩溃转储 | 是 | 部分失败（2文件占用） | 0.8 GB |

## 汇总

- 总释放空间：2.0 GB
- 失败项：2 个文件（占用中）
```

## 不做事项（Must Not）

- 不扫描全盘。
- 不自动删除用户下载/桌面大文件（仅提醒可手动处理）。
- 不修改注册表。
- 不处理系统核心目录和系统关键组件目录。

## 执行检查清单（Checklist）

- [ ] 只使用白名单目录
- [ ] 每个目录都给出中文解释
- [ ] 每项都拿到用户确认
- [ ] 删除仅发生在确认项
- [ ] 删除后统计释放空间
- [ ] 生成 Markdown 日志并给出路径

## 推荐脚本实现

- 脚本路径：`script/c-drive-safe-cleanup.ps1`
- 运行方式（PowerShell）：
  - `powershell -ExecutionPolicy Bypass -File ".\script\c-drive-safe-cleanup.ps1"`
  - 演练模式（仅扫描/确认/日志，不删除）：
    - `powershell -ExecutionPolicy Bypass -File ".\script\c-drive-safe-cleanup.ps1" -DryRun`
  - 可选自定义日志路径：
    - `powershell -ExecutionPolicy Bypass -File ".\script\c-drive-safe-cleanup.ps1" -LogOutputPath ".\tasks\evaluation-2026-04-22-c-disk-cleanup.md"`
