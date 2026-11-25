# 360 残留指纹库（2026-11-22 本机实测）

本文记录 360 全家桶在 Windows 上留下的痕迹位置与命名规律，供扫描和判定使用。
**所有条目均以实测为准，非猜测。** 体积为当时实测值，仅作量级参考。

## 1. 安装 / 数据目录

| 路径 | 归属 | 实测体积 | 备注 |
|---|---|---|---|
| `C:\Program Files (x86)\360\360Safe` | 360 安全卫士 | 59M / 59 文件 | 主程序残骸；常见 `deepscan`/`ipc`/`netmon`/`safemon`/`SoftMgr`/`sweeper`/`Utils` 子目录 |
| `C:\Program Files (x86)\Wukong` | 「悟空」游戏 | 20M / 36 文件 | ⚠️ 数字签名方是**光锐恒宇(北京)科技**，非奇虎 360 主品牌，但内置大量 `360*.dll`，是装 360 时捆绑安装的。删前须向用户确认 |
| `C:\ProgramData\360SD\Quarant` | 360 杀毒隔离区 | 37K / 2 文件 | `360safe.Summary.dat`、`360SD.Summary.union1` |
| `C:\ProgramData\360Safe` | 360 卫士配置 | 0.8M | 易漏，扫 `ProgramData` 顶层时才会命中 |
| `%APPDATA%\360Login` | 登录配置 | ~1K | |
| `%APPDATA%\360Safe` | 用户配置 | 0（空壳） | 目录可能残留但已空 |
| `%APPDATA%\secoresdk\360se6` | **360 安全浏览器** | **439M** | ⚠️ 藏在 `secoresdk` 容器里，**容器名不含 360**，常规 `*360*` 扫描会漏 |

### 浏览器数据的关键区分
`secoresdk\360se6` 下有两块：
- `Application\`（439M）—— 程序文件，占了绝大部分体积。
- `User Data\Default\360Bookmarks`（10KB）—— **唯一有保留价值的个人数据**（书签，加密存储）。
  清理前**必须先备份**这一个文件，其余可全清。

## 2. 内核驱动残骸（`C:\Windows\System32\drivers`）

360 驱动被停用时会改成**非法后缀**，这是识别"已失效残骸"的关键特征：

| 文件名示例 | 后缀特征 | 状态 |
|---|---|---|
| `360AntiHacker64.removed` | `.removed` | 已失效 |
| `360AntiHijack64.removed` | `.removed` | 已失效 |
| `360AntiSteal64.removed` | `.removed` | 已失效 |
| `360Box64.sys.426` | `.sys.<数字>` | 已失效 |
| `360FsFlt.sys.587` | `.sys.<数字>` | 已失效 |
| `360netmon.old` | `.old` | 已失效 |

**判定规则**：名字以 `360` 开头但**后缀不是 `.sys`** 的，一律是失效残骸，可清。
若发现仍是 `.sys` 的，说明驱动可能还活着，须先确认服务状态再动。

## 3. 注册表键

```
HKLM\SOFTWARE\WOW6432Node\360DrvMgr
HKLM\SOFTWARE\WOW6432Node\360Safe
HKCU\SOFTWARE\360X
HKCU\SOFTWARE\360ChromeXX
HKCU\SOFTWARE\360CleanProX
HKCU\SOFTWARE\360DayPop
HKCU\SOFTWARE\360Game5
HKCU\SOFTWARE\360Newsld
HKCU\SOFTWARE\360se6
HKCU\SOFTWARE\360SoftWareMgr
HKCU\SOFTWARE\360WallPaper
```

服务项（在 `HKLM\SYSTEM\CurrentControlSet\Services\` 下）：
`Q360AMPPL`（360 主服务，常见状态 Stopped/Disabled）、`ZhuDongFangYu`（主动防御）、
`360Box64`（微过滤驱动）、`360netmon`（网络监控）。

⚠️ 注意：**注册表服务项可能已不存在**（本案 `360Box64`/`360netmon` 就没有），
但 `Win32_Service` 查询 `Q360AMPPL` 仍显示 Stopped —— 说明它处于半残状态。
清理脚本对各服务都做了"存在性检查 + sc delete + 兜底删注册表项"三重处理。

## 4. 卸载登记（三态判定的依据）

查这三个位置的 Uninstall 项，`DisplayName` 匹配 `360|奇虎|Wukong|悟空`：
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*
HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*
```

**本案实测：Uninstall 项为空，但 `C:\Program Files (x86)\360\360Safe\uninst.exe` 仍在**
（版本 12.0.0.1731，产品名"360安全卫士安装程序"）。
→ 这是**残骸态**的典型特征：安装登记已无，卸载程序只是没删掉的壳。

## 5. 卸载程序的坑：空等服务卡死

实测：以 `uninst.exe /S` 拉起后，卡在：
```
WARNING: Waiting for service '360Box mini-filter driver (360Box64)' to stop...
```
反复刷屏不退。**原因**：`360Box64` 服务项在注册表根本不存在、驱动文件已改名
`.sys.426` 失效——卸载程序在等一个不存在的服务，自己逻辑死循环。

→ **残骸态下绝不可依赖 uninst.exe**，它不是"停不下来"，是"在空等"。
→ 反之，**活跃态**（Uninstall 项存在、服务真实在跑）才应优先走官方卸载。

## 6. 误报排除（不要删）

| 项目 | 原因 |
|---|---|
| `%LOCALAPPDATA%\GitHub CLI\run-log-36099486093-*.zip` | 文件名碰巧含 `360`，是 GitHub CLI 运行日志 |
| 任何名字含 360 但与上述指纹无关的用户文件 | 按 `confidence=suspicious` 标出，交用户判断 |

## 7. 三态判定规则

| 状态 | 判定条件 | 打法 |
|---|---|---|
| `active` | Uninstall 项存在 360 登记 | 优先走官方卸载程序，卸载后再扫描残留 |
| `residue` | 无 Uninstall 登记，但有目录/注册表/驱动痕迹 | 直接文件级清理，**不拉 uninst.exe** |
| `clean` | 无任何痕迹 | 结束 |
