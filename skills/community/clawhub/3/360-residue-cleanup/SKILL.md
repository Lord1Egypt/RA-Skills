---
name: 360-residue-cleanup
description: 安全清理 Windows 上 360 全家桶（安全卫士、杀毒、安全浏览器、驱动大师、捆绑安装的「悟空」游戏等）的安装目录、用户数据、注册表键、服务与失效驱动残骸。先只读扫描出清单，判定活跃安装/纯残骸/混合三态，经用户逐项确认、备份关键数据后分批次移入回收站或隔离区（可回滚），删不掉的生成提权脚本交给用户手动执行。当用户说「清理360」「卸载360」「卸干净360」「清掉360残留」「删除360目录和文件」「360卸载不了/卸不干净」时使用。绝不拉起残骸状态的 uninst.exe（它会在不存在的服务上空等卡死）。
agent_created: true
slug: 360-residue-cleanup
displayName: 360 全家桶残留安全清理
version: 1.0.0
category: it-ops-security
subCategories: [itops-troubleshooting]
visibility: public
license: MIT
homepage: https://github.com/oracis/360-residue-cleanup
repository: https://github.com/oracis/360-residue-cleanup
---

# 360 全家桶残留安全清理

## Overview

清理 360 产品在 Windows 上留下的目录、用户数据、注册表键、服务和失效驱动。
核心是**三态判定**——活跃安装走官方卸载、纯残骸直接文件级清理——以及一套
在 WorkBuddy 沙箱限制下依然能安全推进的流程（扫描 → 确认 → 备份 → 清理 → 验收）。

## 安全铁律（任何情况下不可跳过）

1. **先只读扫描出清单，再谈删除。** 不扫清楚不动手。
2. **删除必须经用户逐项确认。** 尤其 `Wukong`（悟空游戏）和浏览器书签这类需单独判断的项。
3. **先备份，后删除。** 360 书签（`secoresdk\360se6\User Data\Default\360Bookmarks`）必须先另存；注册表必须先导出 `.reg`。
4. **可回滚优先。** 文件和目录优先移入回收站；系统保护位置用隔离目录，绝不默认永久删除。
5. **分批次、逐批验证。** 每批后确认实际状态，失败立即停。
6. **删不掉如实报告。** 环境权限做不到时，生成提权脚本交用户，不假装完成、不强绕安全策略。
7. **残骸态绝不拉 uninst.exe。** 它会在已不存在的 `360Box64` 服务上空等卡死（见 `references/360-fingerprints.md` §5）。

## 主流程

### Step 0 — 加载参考知识

按需读取（首次清理时两份都读）：
- `references/360-fingerprints.md` —— 360 各产品的指纹位置、驱动后缀规律、误报排除、三态判定规则。
- `references/sandbox-limits.md` —— 当前沙箱被拦的调用、回收站可用范围、批量删除的坑。

### Step 1 — 只读扫描，产出清单

执行扫描脚本（全程只读，不删任何东西、不停进程、不改注册表）：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/scan_360.ps1 -OutFile .\scan-result.json
```

脚本输出 JSON：每个命中项含 `category/path/kind/size_mb/exists/needs_admin/confidence`，
并给出顶层 `state`（`active` / `residue` / `clean`）和 `false_positives`（误报提示）。

**向用户展示清单**时用表格分组：目录 / 浏览器数据 / 驱动 / 注册表 / 服务，
标注体积、`confidence`（confirmed / suspicious）和 `needs_admin`。
`confidence=suspicious` 的项（如 `Wukong`）**单独列出请用户判断**，不要默认纳入删除。

### Step 2 — 三态判定，决定打法

| state | 判定依据 | 打法 |
|---|---|---|
| `active` | Uninstall 项有 360 登记，服务真实在跑 | **先走官方卸载**（设置→应用→卸载，或 uninst.exe），卸载后再扫描清残留。不要直接删文件 |
| `residue` | 无 Uninstall 登记，但有 360 目录/注册表/驱动痕迹 | **直接文件级清理**，不拉 uninst.exe（它会在空服务上死等） |
| `clean` | 无任何痕迹 | 报告"未发现 360 残留"，结束 |

判定依据和卸载程序的坑详见 `references/360-fingerprints.md` §4–§7。

### Step 3 — 确认范围与方式

用选择题向用户确认两件事：
1. **删哪些**（全选残骸 / 仅小体积 / 是否含 `Wukong` / 是否先备份书签）。
2. **删除方式**（移入回收站推荐 / 永久删除——需明确警示不可恢复）。

用户确认后才进入删除。**用户没确认前不删任何东西。**

### Step 4 — 备份关键数据

- 书签：`360Bookmarks` 另存到备份目录（见 `references/360-fingerprints.md` §1 浏览器数据的关键区分）。
- 注册表：导出所有待删键为 `.reg`。
- 备份目录建议放在会话工作区下，便于找回。

### Step 5 — 分批次清理

**当前沙箱能做的**（用户目录，回收站可用）：
用已加载的 .NET 类型删除，不要 `Add-Type`（被拦）：
```powershell
[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($path,'OnlyErrorDialogs','SendToRecycleBin')
```
注意：**先收集完整路径数组再逐个删**，不要在 `Get-ChildItem -Recurse` 管道里边枚举边删（会静默失败）。

**当前沙箱做不了的**（`Program Files` / `System32` / 注册表）：
这些位置回收站报 "not supported"、写操作 Access denied，沙箱非管理员。
→ 生成提权脚本 `scripts/cleanup_360_admin.ps1`（按需填入本次清单），
告诉用户**右键"以管理员身份运行"**。脚本自带管理员检查、注册表备份、回收站/隔离区降级、
服务 sc delete、逐步验证。详见 `references/sandbox-limits.md` §3、§5。

### Step 6 — 验收与报告

用 `Test-Path -LiteralPath` 逐项验证（不要用 Bash `find`，有缓存会误报）。
向用户报告：
- 已清除项（进回收站，可恢复）；
- 需提权手动完成的项 + 脚本路径 + 运行命令；
- 备份位置（书签 / 注册表 / 隔离区）；
- 若仍有残留，附带原因的手动清单。

## 判断边界

- **只处理 360 及其明确捆绑产物**。名字碰巧含 360 的用户文件（如 GitHub CLI 日志）按误报排除，不删。
- **`Wukong` 签名方是光锐恒宇而非奇虎 360**，属于捆绑安装的游戏，必须用户明确确认才删。
- **不动仍在运行的系统组件**：若发现 `.sys` 后缀的活跃 360 驱动或真实在跑的服务，先停下确认，不按残骸处理。
- **注册表无备份不动手**——这是底线。

## Resources

### scripts/
- `scan_360.ps1` —— 只读扫描，输出含三态判定的 JSON 清单。
- `cleanup_360_admin.ps1` —— 需管理员的清理脚本模板（可接 `-TargetsFile` 用扫描结果驱动）。

### references/
- `360-fingerprints.md` —— 目录/注册表/服务/驱动指纹、误报排除、三态判定、uninst.exe 空等坑。
- `sandbox-limits.md` —— 沙箱被拦调用、回收站兼容矩阵、批量删除与提权脚本注意事项。
