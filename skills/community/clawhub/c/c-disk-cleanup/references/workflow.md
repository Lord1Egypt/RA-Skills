# 详细作战手册（agent 执行参考）

本文件是 `c-disk-cleanup-pro` 的底层参考，包含各阶段确切命令、校验与排错。**执行前必读，且任何改动类动作都必须先经用户确认。**

总体原则（与 SKILL.md 铁律一致）：**先只读扫描 → 出菜单讲人话 → 用户确认 → 只搬不删 → 记习惯**。

---

## 0. 只读体检（永远先跑）

用 `scripts/scan_cdrive.ps1` 打印 C 盘空间与大户清单。也可手动：

```powershell
# C盘空间
(Get-PSDrive C).Free
# 顶层目录大小
Get-ChildItem C:\ -Directory | ForEach-Object {
  $sz=(Get-ChildItem $_.FullName -Recurse -EA 0 | Measure-Object Length -Sum).Sum
  [pscustomobject]@{Name=$_.Name;MB=[math]::Round($sz/1MB)}
} | Sort-Object MB -Desc | Select -First 15
```

> 关键认知：C 盘回收站删除/移动**不释放** C 盘空间（数据仍在 C）。要真腾空间必须搬到别的盘。

---

## A 阶段：缓存/临时清理（最安全、最先做，需用户确认清单）

候选：应用缓存与临时目录（`AppData\Local\*\Temp`、`*-updater`、`pip`、各 `Temp`）。
排除可能含用户数据的目录（豆包、剪映、WPS、微信/QQ 收件等），**单独列给用户决定**。

执行（确认后，用 safe_ops.ps1 的 MoveToBackup，只搬不删）：

```powershell
# 示例：把用户临时文件搬到备份盘（需先确认 + 指定备份盘）
powershell -ExecutionPolicy Bypass -File scripts/safe_ops.ps1 `
  -Action MoveToBackup -Path "$env:USERPROFILE\AppData\Local\Temp" -BackupDrive D -Confirmed
```

校验：再跑 `scan_cdrive.ps1` 看 C 盘剩余是否上升、源目录是否已腾空、备份盘是否落地。

---

## B 阶段：桌面/下载迁移（junction 重定向，零丢失，需用户确认）

把 `Desktop`/`Downloads` 内容搬到备份盘，在 C 盘原路径建**目录联接（junction）**，文件用起来一样，但物理在别的盘。

```powershell
# 1) 搬到备份盘
Move-Item "$env:USERPROFILE\Desktop\*"    "D:\C盘整理\用户文件\桌面\"
Move-Item "$env:USERPROFILE\Downloads\*"  "D:\C盘整理\用户文件\下载\"
# 2) 建 junction 让原路径继续可用（PowerShell 的 New-Item 最稳）
New-Item -ItemType Junction -Path "$env:USERPROFILE\Desktop"   -Target "D:\C盘整理\用户文件\桌面"  -Force
New-Item -ItemType Junction -Path "$env:USERPROFILE\Downloads" -Target "D:\C盘整理\用户文件\下载" -Force
```

### ⚠️ 进程锁是头号敌人（必读）
- Word/WPS 打开文档会生成 `~$*.doc` 排他锁文件，连带父目录删/改名都会失败。
- 企业微信会锁 `Downloads`。
- **可靠解法**：先确认 D 盘副本完整 → 把持锁父目录**同盘改名让位**（`Move-Item "桌面" "C:\__桌面残留__"`）→ 立刻建 junction → 残留 `~$*` 关掉程序后自然消失。数据已在 D 盘，不会丢。

---

## C 阶段：NTFS 透明压缩 Program Files（可选进阶，需用户确认）

对大、静态、EXE/DLL 多的程序目录做透明压缩，**文件位置不变、程序照常跑**，且**幂等可逆**。

```powershell
compact.exe /c /s:"C:\Program Files (x86)\Microsoft" /i /q
compact.exe /c /s:"C:\Program Files\Common Files" /i /q
```

排除正在运行的程序目录、系统自管目录（WindowsApps、NVIDIA 驱动）。

---

## D 阶段：系统组件清理（DISM + CompactOS，需管理员，需用户确认）

### 前置：确认管理员
```powershell
net session >$null 2>&1; if($LASTEXITCODE -eq 0){"ADMIN_OK"}else{"NOT_ADMIN"}
```

### 只读诊断（先给方案）
```powershell
DISM.exe /Online /Cleanup-Image /AnalyzeComponentStore
compact /compactos:query
```

### 执行（标准安全项，不加 /ResetBase 以免无法卸载旧更新）
```powershell
DISM.exe /Online /Cleanup-Image /StartComponentCleanup
compact /compactos:always
```
两者均微软官方、可逆（`compact /compactos:never` 还原）。WinSxS 大量是系统共享不可回收，实际净增约 2–5 GB 属正常。

---

## 关键坑（实战血泪）

1. **Git Bash 双引号 `\r` 转义陷阱**：`cmd //c "echo C:\reg.txt"` 中 `\r` 被解析成回车，路径错乱。对 `cmd //c` 一律用单引号。
2. **反复 `taskkill explorer` 会搞坏 cmd 子进程输出管道**：改用 PowerShell 自带命令，或把结果 `> file` 落盘再读。
3. **PowerShell 执行 compact/DISM 长输出会断管**：命令结果一律 `| Set-Content file` 落盘，读取时用 `-replace "\r","\n"` 清洗。
4. **junction 创建竞态（explorer 自重启）**：用 `New-Item -ItemType Junction` 最稳；若 explorer 抢建空文件夹，先 `Move-Item` 父目录让位再建。
5. **外部进程锁（Word/企业微信/浏览器/杀软）**：先让用户关程序或重启，不要硬刚。

---

## 收尾清单

- 每阶段后汇报释放量（`(Get-PSDrive C).Free` 前后对比）。
- 清理本任务临时诊断 `*.txt`，**保留备份目录里的真实文件**与 `habit.json`。
- 告诉用户：备份放哪、怎么找回、是否要"最后一步才真删"（由用户决定，助手不主动删）。
- 更新 `habit.json`：备份盘、敢清类别、是否允许自动、频率。
