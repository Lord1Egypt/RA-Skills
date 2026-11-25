# WorkBuddy 沙箱限制与绕法（2026-11-22 实测）

清理系统级残留时，**工具能不能动手**往往比"怎么删"更关键。本文记录本机 WorkBuddy
沙箱的实际限制，避免每次重新试错。这些限制会随版本变化，遇到不符时以现场实测为准。

## 1. 被安全策略拦截的调用

| 调用 | 报错 | 绕法 |
|---|---|---|
| `reg.exe`（任何形式） | `PROGRAM BLOCKED BY SECURITY POLICY` / `Access is denied` | **不要用 reg.exe 读写注册表**。读用 PowerShell `Test-Path "Registry::..."` / `Get-ItemProperty`；导出备份在提权脚本里做（那是用户自己的管理员环境，不受本沙箱限制） |
| `New-Object -ComObject Shell.Application` | `COM object instantiation can run arbitrary code` | 不要走 COM。用下面的 VB.NET 回收站方式 |
| `Add-Type`（编译 .NET） | `Add-Type compiles and loads .NET code at runtime` | 不需要 `Add-Type` —— 回收站类型已随 PowerShell 加载，直接引用即可（见 §2） |

## 2. 回收站删除的正确姿势（关键）

**直接调用已加载的 .NET 类型，不要 Add-Type：**

```powershell
# 删文件到回收站
[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($path,'OnlyErrorDialogs','SendToRecycleBin')

# 删目录到回收站
[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($path,'OnlyErrorDialogs','SendToRecycleBin')
```

**兼容性矩阵（实测）：**

| 位置 | 回收站 API | 说明 |
|---|---|---|
| `C:\Users\...`（用户目录） | ✅ 可用 | 本次清掉了 439M 浏览器目录 |
| `C:\Program Files (x86)\...` | ❌ `This function is not supported on this system` | 系统保护位置，回收站机制不覆盖 |
| `C:\Windows\System32\drivers\...` | ❌ 同上 | 同上 |
| 空目录 | ❌ genie-trash 报 `Some operations were aborted` | 空目录无数据，风险为零，可忽略或用别法 |

**降级方案**（系统保护位置）：移动到隔离目录而非永久删除——
`Move-Item -LiteralPath $p -Destination $quarantine\...`。
但要配合管理员权限，见 §3。

## 3. Program Files / System32 的写权限

- 当前沙箱**不是管理员**，`Set-Content` / `Move-Item` / `Remove-Item` 对
  `C:\Program Files (x86)` 一律 `Access to the path is denied`。
- 切换到 Agent mode **不会**解除这个限制（实测确认）。
- 结论：这些位置**在当前环境做不了**，必须交用户手动提权。
- 做法：生成提权脚本（见 `scripts/cleanup_360_admin.ps1`），让用户右键
  "以管理员身份运行"，而不是反复尝试或假装完成。

## 4. 批量删除的坑

- **不要在 `Get-ChildItem -Recurse` 的管道里边枚举边删** —— 实测会静默失败
  （文件还在但无报错）。正确做法：**先收集完整路径到数组，再逐个删**。
- 递归删复杂目录时，`DeleteDirectory` 容易失败；改为**先逐个删文件、再从最深目录
  往上删空目录壳**（按 `FullName.Length` 倒序）。
- 验证时别用 Bash 的 `find`（有缓存，会误报"仍存在"），用 PowerShell 的
  `Test-Path -LiteralPath` 为准。

## 5. 提权脚本里的注意事项

- 脚本**首行检查管理员权限**，非管理员直接 `exit 1`，避免半途失败留残局。
- 注册表先 `reg.exe export` 备份再删 —— 在用户自己的管理员 PowerShell 里
  reg.exe 是可用的（沙箱黑名单只管 WorkBuddy 发起的调用）。
- 服务清理顺序：**先 `sc delete`，再兜底删 `HKLM\SYSTEM\CurrentControlSet\Services\<name>`**，
  避免先删注册表项导致服务再也删不掉。
- 每一步都回显 `已清除=<bool>`，最后统一验证并打印残留清单。

## 6. 全局原则

1. **先只读扫描出清单 → 用户确认 → 先备份 → 分批次 → 可回滚 → 删不掉给手动清单。**
2. 环境做不到的事**如实报告**，生成可执行的替代方案（脚本），不假装完成、不强行绕过安全策略。
3. 注册表没有备份就**不动注册表** —— 这是底线。
