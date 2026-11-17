---
name: bat-ps1-dev
description: "Windows/Linux batch + PowerShell script dev experience vault — encoding pitfalls, cmd syntax traps, PS 5.1/7 compat, cross-platform gotchas, security tool best practices. 批处理/PowerShell 脚本开发经验库，编码陷阱、cmd 语法坑、PS兼容、跨平台坑、安全工具最佳实践。Keywords: bat, cmd, PowerShell, ps1, pwsh, BOM, CRLF, 闪退, 乱码, Windows scripting"
version: "1.71.0"
author: "SilverFox Detector 项目实战总结"
created: "2026-08-17"
updated: "2026-09-01"
---

# Windows 批处理 / PowerShell 脚本开发经验库

> 从「银狐木马检测工具」Windows .bat + PowerShell 双文件架构开发中总结的全部踩坑与最佳实践。
> 适用于:制作 .bat 启动器、.ps1 引擎、跨平台(pwsh)脚本。

## 0. 持续更新协议(活文档,强制)

**本 skill 是活文档,必须随经验与错误持续累加更新,不是一次性产物。**

触发更新的时机(遇到即记,事后补):
- 开发/调试 .bat、.ps1、pwsh 脚本时**踩到新坑、发现新现象、找到新对策**
- 用户提出新需求,带来新的最佳实践(如交互模式、跨平台适配)
- 实测(含 Linux pwsh 验证)暴露了纯静态分析发现不了的问题

更新规则:
1. **追加到对应章节**(编码→§1、cmd→§2、PS兼容→§3、跨平台→§4、工程实践→§5、实测→§6),没有合适章节就新增小节。
2. **每条记录格式**:`问题 | 现象/报错 | 对策`(表格行或列表),注明来源(如"v1.29 交互模式实战")。
3. **同步更新** `version`(小改+0.0.1、新增章节+0.1.0)与 `updated` 日期。
4. 每次使用本 skill 后,若对话中出现了值得沉淀的经验,**主动补录**,并在回复中告知"已更新 skill"。
5. **更新前必过脱敏核查(强制)**: 写任何新记录前, 必须对照下方「脱敏核查清单」逐项排查, 命中即改写/删除后再落盘; 发现历史条目遗留敏感信息也一并脱敏(本协议本身就是因历史条目漏脱敏而补强)。
6. **修改后必做自查(强制)**: 写完/改完即对照下方「修改后自查清单」逐项核验, 未全部通过不自认任务完成; 自查发现的脱敏遗漏/版本漂移/格式断裂/副本不一致立即修。
7. **每次修改必须更新版本号(强制)**: 任何对 skill 内容的改动(新增章节/修订条目/补脱敏)都必须同步: ① frontmatter `version`(语义化 +0.0.1=小修订/补条, +0.1.0=新增章节/新实战); ② `updated` 日期; ③ 「更新日志(倒序)」顶部新增对应条目。版本号须与最新日志条目一致, 否则「修改后自查清单」版本同步项判不通过。本规则本身因"修了档1崩溃却忘了同步二进制/skill 版本号, 用户无从判断部署的是哪版"而补强。

**脱敏与隐私协议(强制,与上面同等优先级):**
- 本 skill **只沉淀技术经验与踩坑根因**, 不承载任何可溯源到具体环境/个人的信息。
- **禁止落盘**: 临时下载/分享链接(含云存储 `?q-sign-*`/`?sign=*`/`?token=` 等签名参数)、bucket/APPID/存储地域、内网/私有 IP 与 `.internal`/`.local` 域名、邮箱/电话/微信/QQ/身份证等个人身份、本机绝对路径(`/root/...`、`/home/<user>/...`、`uploads/` 等特指本机的路径)。
- **允许保留**: 通用技术示例(如 Linux 临时目录 `/tmp/` 泛指、`C:\Program Files\...` 作为 Windows 路径范式、`.zip` 泛指打包)、代码范式、纯技术名词(`secret`/`signature` 等作为术语而非真实密钥)、已公开的项目名与版本号。
- **沉淀前自检**: 写任何记录前先问"这条是否暴露了某次具体会话/某台机器/某个账号?"——若是, 改写为去标识化的技术描述再落盘。

**脱敏核查清单(每次落盘前必过, 命中即改/删):**
- [ ] **云存储签名链接**: `?q-sign-*`/`?sign=`/`?token=`/`?expires=`/`q-key-time=`/`q-signature=` → 整段删除, 只留"用户提供的 zip/skill 文件"等泛指描述(链接含临时签名, 暴露 bucket/APPID/签名算法)
- [ ] **密钥/AccessKey**: `AKID...`/`SecretKey`/`sk-`/`x-oss-`/`q-ak=`/`q-key=` → 删除
- [ ] **本机绝对路径**: `/root/`/`/home/<user>/`/`/workspace/`/`uploads/`/`/tmp/<具体项目名>`/`codebuddy` session 路径等特指某次会话/某台机器的 → 改泛指(`<交付目录>`/`<临时目录>`/`C:\Program Files\` 范式)或删除(注: `/workspace/` 也是本机路径, 须脱敏)
- [ ] **具体签名/哈希/commit 串**: 真实 `sig=...`/具体 build 指纹/具体 commit hash → 改技术描述("签名校验通过(64 位 salt 混淆级)")
- [ ] **机器名/内网 IP/私有域名**: 主机名、内网 IP、`.internal`/`.local` 域名、端口映射 → 删除
- [ ] **个人身份**: 邮箱/电话/微信/QQ/身份证 → 删除
- [ ] **允许保留**: 已公开项目名/版本号、API 名词、代码常量(如 `ID_BTN_INSTALL_SVC=1050`)、通用路径范式、`secret`/`signature` 作术语(非真实值)

**修改后自查清单（强制, 每次写完即执行, 未过不自认完成）:**
- [ ] **脱敏复查(必跑 grep)**: 全文档扫描 `q-sign`/`?sign=`/`?token=`/`AKID`/`SecretKey`/`sk-`/`q-ak=`、本机路径 `/root/`/`/home/<user>/`/`uploads/`、真实 `sig=...`/具体 build 指纹; 对 `/workspace/` 须人工确认仅出现在"禁则反例"中, 无具体交付文件名泄露。
  - 自查命令(参考): `grep -nE "q-sign|AKID|SecretKey|/root/|/home/|uploads/|sig=[0-9a-f]{8,}" 本skill.md || echo "✔ 无敏感泄露"`
- [ ] **版本与日志同步(每次必 bump)**: frontmatter `version` 等于更新日志最新条目, 且**本次修改已按规则 +0.0.1/+0.1.0 bump**、`updated` 日期已更新; 交付二进制若一并改了, 其内部版本号/构建标签也须同步 bump(曾出现"修了崩溃却忘改版本, 用户无法判断部署的是哪版")。
- [ ] **格式完好**: Markdown 未断裂——代码块成对、列表层级正确、反引号/加粗配对; 新增小节编号连续不重不漏。
- [ ] **副本一致(若有多份)**: 主文件与交付目录副本 `diff` 必须一致(曾因只改一处导致两份漂移, 泄露/未脱敏版本被带出去)。
- [ ] **内容自洽**: 新增/修改的"对策/修复"须与代码实际改动一致, 不写未验证的断言(如声称"窗口正常"须来自日志实证, 而非推测)。

---

## 0.1 按症状快速索引(遇到问题先查这里)

> 本 skill 章节编号是按时间倒序追加(§14-§39 实战经验在前, §1-§13 基础在后)。遇到具体症状时, 用下表定位最相关的章节, 避免重走猜错的路。

| 症状/场景 | 优先读 | 备注 |
|----------|--------|------|
| bat 闪退/语法错 | §1, §11, §29 | 嵌套括号陷阱最常见 |
| PS 5.1 无输出 exit 1 | §21 | 双重 BOM 静默拒绝执行 |
| bat 转码后乱码/二次损坏 | §35 | 转码脚本非幂等, UTF-8 误读 GBK 文件再写回所致 |
| 合并/重构旧 bat 工具箱 | §36 | 动手前必跑 goto/标签对照, 辅助转码脚本只写 ASCII |
| GUI 不出现(双击无界面) | §13, §14, §15, §16, §19 | **必读 §19 真因**, §17/§18 是证伪的弯路 |
| 看门狗无限重启 | §16, §31 | 致命错误退出前必须 removeGuardFlag |
| 1114 错误(DLL 初始化失败) | §16 → §17 → §18 → **§19** | §17/§18 的"360 hook"假设已被证伪, 真因是自保护缓解策略 |
| UAC 提权失败/提权后无界面 | §13, §22 | 用 `--elevated-run` 直接模拟提权子实例排查 |
| Start-Process -ArgumentList 坑 | §22 | $args 恒为 null + 不接受空集合 |
| Wine 验证"假装正常" | §12, §13, §14 | 凡依赖真实 Windows 加载器行为的 bug, 纯 wine 复现不出 |
| BOM/编码乱码 | §1, §21, §23 | chcp 65001 与 GBK 脚本混合必乱 |
| hosts 劫持检测/修复 | §28 | 下载失败排障链, -EncodedCommand 避开引号地狱 |
| 拦截系统关机 | §24 | 杀 shutdown.exe 无效, 必须 WM_QUERYENDSESSION=FALSE |
| 看门狗 PID 复用残留 | §31 | PID 被新进程复用导致误判存活 |
| Get-AuthenticodeSignature 卡死 | §32 | 对大文件/云盘占位文件会挂起数分钟 |
| pwsh 别名 9020 错误 | §20 | WindowsApps 应用执行别名在长中文路径下失败 |
| TrimEnd/参数集互斥 | §23 | PS 5.1 字符串转 char 的隐式转换坑 |
| 交付物审查 | §29 | goto 标签集合求差集 + 版本链漂移自查 |
| 发布自动化 | §34 | 文本替换定界 + GUI 单实例 |
| 桌面端页面能开但永远空/功能静默失效 | §37, §38 | MethodChannel 无桌面实现; §37 识别+纯Dart适配, §38 三分法 |
| zip/.mcworld/mrpack 打包后嵌套文件丢失 | §38 | Windows 反斜杠条目分隔符 |
| Forge/NeoForge 中文或空格路径安装必挂 | §38 | Java 加载器四连坑(argfile/JVM编码/runInShell/javaagent) |
| 给第三方软件加/取消开机启动 | §39 | Run 键带空格路径必须"自带引号"落盘; set /p 先清空防残留 |

**新读者建议路径**: 先扫 §1-§13 基础(编码/cmd/PS兼容/跨平台/实测/交付检查), 再按需查 §14-§39 实战条目。§14-§19 的"猜错→证伪→真凶"链建议完整读一遍——这是本 skill 最有价值的部分, 能避免你重走相同的弯路。

## 14. lazyDLL 懒加载失败是 panic 不是 error → 可选 DLL 调用来就崩(2026-08-22 v2.15.9 实战)

**症状**: Go 写的 Windows GUI 程序在某台真机双击**直接崩溃**(FATAL: `A dynamic link library (DLL) initialization routine failed`, GetLastError=1114), 看门狗无限重启; 但在 Wine/Linux 验证里**窗口正常创建**, 仿佛没毛病。

**根因(真机, Wine 看不到)**: `golang.org/x/sys/windows` 的 `LazyProc.Call` 在底层 `LoadLibrary` 失败时(该 DLL 的 `DllMain` 返回 FALSE, 如受 EDR/AV 拦截或 SxS 损坏)会**直接 `panic`**, 而不是返回 `(r1,r2,err)`。旧代码用 `if ret == 0 { ... 可忽略 ... }` 只防得住"函数返回 FALSE", **防不住 LoadLibrary 的 panic** —— 于是可选 DLL(`ole32` 的 `CoInitializeEx`/`CoTaskMemFree`/`OleInitialize`、`comctl32` 的 `InitCommonControlsEx`、`wintrust`/`crypt32`/`comdlg32`/`shell32` 等)一旦加载失败就整进程崩, GUI 永远不显示。

**为什么 Wine 验证"假装正常"**: Wine 下这些系统 DLL 能正常 `LoadLibrary`, 所以 `winMain` 一路走到 `CreateWindowExW` 出窗口; 真机 DLL 加载失败才暴露 panic。与 §13(UAC 被 Wine 降级)同源——**凡是"依赖真实 Windows 加载器行为"的 bug, 纯 `wine xxx.exe` 都复现不出**。

**对策(统一 `safeCall` 包装)**:
```go
// 把 LoadLibrary 的 panic 转成 (ok=false) 返回, 调用方 best-effort 降级
func safeCall(p *windows.LazyProc, a ...uintptr) (r1, r2 uintptr, err error, ok bool) {
    defer func() {
        if rec := recover(); rec != nil {
            err = fmt.Errorf("lazy 调用 %s 失败(可能 DLL 加载失败: %v)", p.Name, rec)
            r1, r2, ok = 0, 0, false
        }
    }()
    r1, r2, err = p.Call(a...)
    ok = true
    return
}
```
- 所有**可选 DLL** 的懒调用统一走 `safeCall`: GUI 初始化(`CoInitializeEx`/`InitCommonControlsEx`)、剪贴板(`OleInitialize`/`CoTaskMemFree`)、打开/选择文件(`GetOpenFileNameW`/`SHBrowseForFolderW`)、签名校验(`WinVerifyTrust`/`CryptQueryObject`)。
- 失败即 `logf` 点名 + 继续(主窗口照常显示, 仅该 DLL 对应功能降级); `ole32` 失败时 `CoUninitialize`/`CoTaskMemFree` 也走 `safeCall` 避免二次 panic。
- 注: `user32`/`kernel32`/`advapi32`/`ntdll` 是 Go 运行时导入表强制加载的, 不会走 lazy 路径, 无需包。

**验证清单**:
- [ ] 所有可选 DLL 的 `.Call()` 已被 `safeCall` 包裹(直接 `.Call()` 仅限 user32/kernel32 等必加载 DLL)。
- [ ] Wine 回归: `wine xxx.exe` 仍 `主窗口创建成功`(确认 safeCall 改动无副作用)。
- [ ] 真机若某 DLL 失败, 日志须点名该 DLL 且**不崩溃**(继续显示 GUI), 而非 FATAL。

**排查铁律**: 真机 FATAL 报 `DLL initialization routine failed` 而 Wine 正常 → 九成是 lazyDLL 加载 panic, 不是窗口逻辑问题; 把所有可选 DLL 调用换成 `safeCall` 即可。需真机堆栈确认时, 让用户贴日志里 `堆栈见日志` 的堆栈。


## 15. 启动期加载非必需 DLL(ole32/comctl32)拖垮 GUI + 部署版本不可辨识(2026-08-22 v2.15.10 实战)

**症状**: 档1(tier=1)真机双击直接崩溃(FATAL: `DLL initialization routine failed`=1114), 看门狗无限重启; 但 Wine 验证窗口正常。给档1 打上 safeCall 后仍崩——进一步发现**用户跑的是旧二进制**: 日志既无 safeCall 诊断行(`自保护[COM]: ...`)、也无 `LoadLibraryEx ole32.dll:` 前缀, 即"修复是否部署"无法从日志判断。

**根因(双因)**:
1. **崩溃真因**: `winMain` 启动期就调 `CoInitializeEx`(ole32)/`InitCommonControlsEx`(comctl32)。这两个 DLL **非必需**——控件全是系统内置 Button/Edit/Static, comctl32 仅用于 v5 公共控件且 `DwICC=0` 即不初始化任何控件; 但其 `DllMain` 一旦被 EDR/AV 拦截或 SxS 损坏返回 FALSE, `LoadLibrary` 即 1114 panic → 整进程崩、GUI 永不显示。
2. **部署不可辨识**: 旧版日志只打 `启动 v2.15.9`, 与修复版文本几乎一致, 用户无法确认双击的是哪份 exe; 看门狗可能锁住旧 exe 导致覆盖失败, 于是"修了但没生效"反复出现。

**对策**:
- 启动期**彻底移除** ole32/comctl32 初始化, 改为窗口创建完后、且**仅文件夹对话框**需要时再 `CoInitializeEx`(仍走 safeCall 兜底); 控件为系统内置, 移除后 GUI 功能零损失。
- 二进制加 `buildTag` 常量并打印到启动日志首行(`启动 v2.15.10 (tier=N) build=p2-...`), 标题栏版本号 +0.0.1; 用户看日志首行即可确认部署的是哪版。
- FATAL recover 增加 `runtime.Stack` 把完整堆栈写进 `SilverFoxDetector.log`, 真机再崩也能拿到精确 DLL/调用栈。

**验证清单**:
- [ ] `winMain` 启动路径(主窗口创建前)不再有任何 ole32/comctl32 调用(仅 user32/kernel32 等必加载 DLL)。
- [ ] 日志首行含 `build=` 标签且版本号已 bump(用户可据此确认部署)。
- [ ] Wine 回归: `wine xxx.exe` 仍 `主窗口创建成功`。

**排查铁律**: 真机 FATAL 报 `DLL initialization routine failed` 而 Wine 正常 → 先让用户贴日志首行确认**跑的是哪版 build**(多数情况是旧 exe 未覆盖/看门狗锁住); 若确是新版仍崩, 看 `崩溃堆栈:` 段定位精确 DLL。凡是"启动期加载非必需 DLL"都要移出启动路径。


## 16. 必加载 DLL(user32)在启动期被拦截 → 1114 + 看门狗无限重启(2026-08-22 v2.15.11 实战)

> 与 §14(lazyDLL panic)、§15(非必需 DLL 启动期)同级但**更隐蔽**: 这次崩的是**必加载的 `user32.dll` 本身**, 且暴露出"看门狗无限重启循环"这一二次伤害。

- **症状**: v2.15.10 仍"无界面", 日志首行已是新 `build=`(说明跑的是新 exe), 但 `winMain` 第一个 `user32` 调用(`LoadCursorW`/`RegisterClassExW`)直接 panic, FATAL `A dynamic link library (DLL) initialization routine failed.`(错误 **1114**), 看门狗反复"第 N 次自动重启"。
- **根因(两层)**:
  1. **必加载 DLL 也被拦截**: `winMain` 启动期首个 GUI 调用(`LoadCursorW`, 属 `user32.dll`)走的是裸 `LazyProc.Call`, 未包 `safeCall`。本机安全软件(EDR/杀毒)在进程启动期拦截 `user32.dll`(或其依赖)加载、`DllMain` 返回 FALSE → `LoadLibrary` 返回 1114 → `LazyProc.Call` **直接 panic**(§14 已证)。`user32` 是纯 Win32 GUI 命脉, 它加载失败 GUI 在应用层无解——但崩溃必须优雅化。
  2. **看门狗无限重启循环(二次伤害, 真凶)**: ① `winMain` panic 被 `main` 顶层 `recover` 接住; ② `recover` 里调 `showFatal`, 而 `showFatal` 又用 `user32` 的 `MessageBoxW` → 此时 `user32` 已毒化, **二次 panic 且无兜底** → 主进程硬崩; ③ 看门狗(主进程 `winMain` 前已 spawn, 独立进程)见主 PID 消失且**存活标记(guardFlag)未被移除** → 判"被强杀" → 重启; ④ 每次重启再 spawn 新看门狗(旧看门狗因互斥退出), `selfGuardMaxKills=5` 封顶对"每轮换新看门狗"无效 → **死循环**。
- **对策(四刀)**:
  1. `winMain` 内**所有 `user32` 启动期调用**(`LoadCursorW`/`LoadIconW`/`RegisterClassExW`×2/`CreateWindowExW`/消息循环)一律改 `safeCall` → DLL 加载失败返回**明确错误**而非 panic; 光标/图标失败降级为 0(用系统默认)。
  2. `safeCall` 错误信息精确定位**过程名 + 错误 1114** 文本, 崩溃日志一眼看出是 `user32` 类过程。
  3. `showFatal`/`msgBoxInfo`/`msgBoxQuestion` 全部改 `safeCall` → `user32` 不可用时弹窗调用**安全降级, 绝不二次 panic**(掐断循环关键之一)。
  4. 致命 GUI 初始化失败时调 `removeGuardFlag()` → 看门狗判"**正常退出**"而非"被 kill" → **掐断无限重启循环**(关键之二); 同时日志写入**排查建议清单**(管理员运行 / 杀软排除 / 改名排除路径拦截 / `sfc /scannow`)。
- **验证**: ① 正常机器(Wine)`主窗口创建成功`, 无 panic; ② 模拟 `user32` 加载失败(把 `user32` 指向不存在 DLL 名编译)→ 明确错误 + 排查建议入日志, **看门狗"自动重启"次数=0**(循环已断)。
- **诚实边界**: 错误 1114 是 `LoadLibrary` 级失败, 属 OS/安全软件层; 应用层无法强制让被拦截的 `user32` 加载成功。修复只解决"崩溃 + 无限重启 + 无诊断", GUI 能否出现取决于环境层拦截是否解除(管理员运行 / 杀软排除 / 改名 / 修系统文件)。

**验证清单**:
- [ ] `winMain` 每个 `user32` 启动调用都走 `safeCall`(grep `winMain` 内不再有裸 `.Call(` 到 user32 proc)。
- [ ] `showFatal`/`msgBoxInfo`/`msgBoxQuestion` 走 `safeCall`(防止 user32 不可用时二次 panic)。
- [ ] `main` 两处 `winMain` 错误路径都调 `removeGuardFlag()` + 写排查建议。
- [ ] 模拟 user32 失败: 看门狗"自动重启"次数=0, 日志出现 `GUI 初始化失败(致命, 不再重启)`。

**排查铁律**: `winMain` 里**哪怕必加载 DLL 的调用也要包 `safeCall`**——因为"必加载"只是假设, 真机 EDR 能让任何 DLL 的 `LoadLibrary` 失败; 且**任何兜底 `recover` 链里再调用的函数若仍依赖那个失败的 DLL, 必二次 panic**, 弹窗/日志必须自身安全降级。看门狗"正常退出 vs 被 kill"的判定只看存活标记, 致命错误退出前**必须 removeGuardFlag** 否则变无限重启。


## 17. 360 主动防御 hook LoadLibraryExW → user32 加载 1114(2026-08-22 v2.15.12 实战)

> ⚠️ **本节结论已被证伪——跳过此节, 直接看 §19 真因。**
> 本节把 1114 错误归因于"360 主动防御 hook `LoadLibraryExW`", 但用户**完全退出 360 后 v2.15.13 仍报 1114**, 证伪了这个假设。真正根因见 §19: 自带的 `procMitSignature=0x1|0x2` 签名策略逻辑矛盾 + `procMitDynamicCode` 拦截了 user32 加载。本节保留作为"猜错方向"的调试历史档, 不作为解决方案依据——请勿据此在 AV/EDR 上追加假设。

> 与 §16 同级: 崩溃循环已掐断, 但 GUI 仍不出现。这次问题不在应用层 panic, 而在**安全软件对特定 Windows loader API 的 hook**。

- **症状**: v2.15.11 后日志不再"第 N 次自动重启", 看门狗正确判定"主进程正常退出", 但反复出现:
  ```
  LoadCursorW 失败(可能 user32.dll 加载被本机安全软件拦截)
  GUI 初始化失败(致命, 不再重启): RegisterClassExW 失败: user32.dll 可能在本机被安全软件(EDR/杀毒)拦截(错误 1114, DLL 初始化失败)
  ```
  用户已将工具目录加入 360 "开发者模式"信任列表, 问题依旧。
- **根因**: Windows GUI 子系统进程启动时, OS 加载器已**隐式映射** `user32.dll` / `gdi32.dll` 到进程地址空间。但 Go 的 `golang.org/x/sys/windows` 在第一次 `LazyProc.Call()` 时会显式走 `LoadLibraryExW("user32.dll", LOAD_LIBRARY_SEARCH_SYSTEM32)` 获取模块句柄再 `GetProcAddress`。**360 主动防御在驱动层 hook 了 `LoadLibraryExW` 这条显式加载路径**, 返回 1114, 导致 GUI 初始化失败。"开发者模式"只减少弹窗/信任编译输出目录, 不等于关闭主动防御。
- **绕过思路(实验性, v2.15.12)**: 对 `user32.dll` / `gdi32.dll` 改用 `LoadLibraryW` 而非 `LoadLibraryExW` 加载。两条路径在 Windows loader 中实现不同、调用号不同, 可能绕过只 hook `LoadLibraryExW` 的 EDR/AV。具体做法:
  - 本地 fork `golang.org/x/sys/windows`(`xsys/`);
  - 在 `LazyDLL.Load()` 中对 `user32.dll`/`gdi32.dll` 先尝试 `LoadDLL(d.Name)`(内部即 `LoadLibraryW`), 失败再回退到带 `LOAD_LIBRARY_SEARCH_SYSTEM32` 的 `loadLibraryEx`;
  - `go.mod` 增加 `replace golang.org/x/sys => ./xsys`;
  - 保留 §16 的 `safeCall` 与 `removeGuardFlag` 逻辑不变。
- **验证**: Wine 回归仍 `主窗口创建成功`; 真实 360 环境需用户实测。若 `LoadLibraryW` 也被 hook, 则属安全软件层的彻底拦截, 应用层无解, 只能在 360 设置中进一步放行(见排障清单)。
- **诚实边界**: `user32.dll` 是 Windows GUI 程序的必需 DLL。应用层能做的是:
  1. 不因加载失败 panic / 死循环;
  2. 尝试绕过最常见的 `LoadLibraryExW` hook;
  3. 日志精确指出是 `user32` 类过程返回 1114;
  4. 给出环境层排障清单。
  如果安全软件在驱动层对 `user32.dll` 做了彻底拦截, 最终必须在安全软件层面放行本程序。

**排障清单(给用户)**:
1. 把三个 exe 文件单独加入 360 信任区(不只是目录开发者模式):
   - 360 安全卫士 → 木马查杀 → 信任区 → 添加信任文件 → 依次添加 `SilverFox.exe`、`SilverFox.Heartbeat.exe`、`SilverFox.Hard.com`。
2. 临时关闭 360 "主动防御服务"测试:
   - 360 设置中心 → 主动防御服务 → 取消勾选 → 确定。
3. 临时完全退出 360 测试(测试完重新开启)。
4. 把 `SilverFox.exe` 复制到 `C:\temp\app.exe` 运行, 排除按文件名/路径拦截。
5. 右键 → 以管理员身份运行。
6. 以管理员运行 `sfc /scannow` 与 `DISM /Online /Cleanup-Image /RestoreHealth` 修复系统文件。

**验证清单**:
- [ ] 本地 fork 的 `xsys/windows/dll_windows.go` 仅对 `user32.dll` / `gdi32.dll` 改 LoadLibraryW-first, 其他 DLL 保持 `loadLibraryEx` 不变。
- [ ] 正常环境(Wine)回归通过: `主窗口创建成功`, 无 panic。
- [ ] 日志首行版本/ `build=` 标签已同步升级到 v2.15.12。
- [ ] 交付包包含 `xsys/` 目录与 `go.mod` 的 `replace` 行, 用户可复现构建。

**排查铁律**: 当用户说"加了杀软信任目录还是不行"时, 要区分"信任目录"与"主动防御 hook"——很多杀软即使信任目录也会继续监控系统 API 调用。GUI 程序若连 `user32.dll` 的显式加载都被拦截, 要么换 loader API 绕过, 要么只能在该安全软件里进一步放行。


## 18. LoadLibraryW 也被 hook → 改用 GetModuleHandleEx 取已加载句柄(2026-08-22 v2.15.13 实战)

> 继 §17 之后: `LoadLibraryW` 绕过失败, 说明安全软件拦截的是"对 user32/gdi32 做任何显式加载", 而不仅仅是 `LoadLibraryExW`。

- **症状**: v2.15.12 在真实 360 环境下日志仍为:
  ```
  LoadCursorW 失败(可能 user32.dll 加载被本机安全软件拦截)
  GUI 初始化失败(致命, 不再重启): RegisterClassExW 失败: user32.dll 可能在本机被安全软件(EDR/杀毒)拦截(错误 1114, DLL 初始化失败)
  ```
  Wine 下一切正常, 说明代码逻辑无误。
- **根因再深入**: 360 主动防御对 `user32.dll` / `gdi32.dll` 的**任何显式加载**(`LoadLibraryExW`/`LoadLibraryW`)都做了拦截并返回 1114。但 Windows GUI 子系统进程启动时, OS 加载器已经**隐式映射**了这两个 DLL, 正常程序本不该再显式加载。
- **最终绕过(v2.15.13)**: 本地 fork `golang.org/x/sys/windows`, 在 `LazyDLL.Load()` 中对 `user32.dll`/`gdi32.dll` 优先使用 `GetModuleHandleEx(0, name, &h)` 直接获取**已加载模块句柄**, 完全不调用 `LoadLibrary*`。若失败再回退 `LoadLibraryW`, 最后回退 `loadLibraryEx`。
  - `GetModuleHandleEx` 只查询已加载模块, 不触发 DllMain, 不经过 360 hook 的显式加载路径;
  - 这是应用层对"必加载 DLL 被拦截"能做的最后一次绕过尝试。
- **验证**: Wine 回归 `主窗口创建成功`; 真实 360 环境待测。
- **诚实边界**: 若安全软件做了沙箱隔离或对 `GetModuleHandleEx` 也做了限制, 则应用层彻底无解, 只能在该安全软件中放行本程序。

**排障清单(给用户, 若 v2.15.13 仍失败)**:
1. 把当前三个 exe 文件**单独**加入 360 信任区(不只是目录):
   - 360 安全卫士 → 木马查杀 → 信任区 → 添加信任文件
   - 依次添加 `SilverFox.exe`、`SilverFox.Heartbeat.exe`、`SilverFox.Hard.com`
   - 注意: 旧文件名(如 `silverfoxdetector.exe`)的信任对当前新文件名无效。
2. 临时关闭 360 "主动防御服务"测试。
3. 临时完全退出 360 测试。
4. 把 `SilverFox.exe` 复制到 `C:\temp\app.exe` 运行, 排除按文件名/路径拦截。
5. 右键 → 以管理员身份运行。
6. 执行 `sfc /scannow` + `DISM /Online /Cleanup-Image /RestoreHealth` 修复系统文件。

**验证清单**:
- [ ] 本地 fork 的 `xsys/windows/dll_windows.go` 对 `user32.dll`/`gdi32.dll` 优先 `GetModuleHandleEx`, 且不破坏其他 DLL 的 `loadLibraryEx` 路径。
- [ ] 正常环境(Wine)回归通过: `主窗口创建成功`, 无 panic。
- [ ] 日志首行版本/ `build=` 标签已同步升级到 v2.15.13。
- [ ] 交付包包含 `xsys/` 目录与 `go.mod` 的 `replace` 行。

**排查铁律**: 当 `LoadLibraryW` 和 `LoadLibraryExW` 都被 hook 时, 唯一还能尝试的是 `GetModuleHandleEx`——因为 GUI 子系统已隐式加载了 user32/gdi32。如果连已加载模块句柄都拿不到, 说明安全软件对进程做了沙箱/隔离或更底层限制, 必须在安全软件层解决。

> **⚠ 更正(2026-08-22)**: 本节"360 主动防御 hook `LoadLibrary*`"的结论**已被实机证伪**——用户完全退出 360 后 v2.15.13 仍报 1114。真正根因见 **§19: 自带的自保护缓解策略(`procMitSignature=0x1|0x2` 逻辑矛盾 + `procMitDynamicCode`)拦截了 user32 加载**。本节的 `GetModuleHandleEx` 绕过只是"猜外部原因"阶段的尝试, 实际无效, 请勿据此继续在 AV/EDR 上追加假设。

## 19. 真凶是自带的自保护缓解策略(非 360)——v2.15.14 实战(2026-08-22)

> **重要更正**: §17、§18 把方向归到"360 主动防御 hook `LoadLibrary*`", **这是错误方向**。
> 用户对 v2.15.13 的实测日志显示:**已完全退出 360, 双击仍报 `LoadCursorW 失败` / `RegisterClassExW 失败(错误 1114)`**,
> 且日志首行已是新 build(说明跑的就是新 exe)。360 退了还 1114, 直接证伪了"360 hook"假设。
> 真正拦截 user32 的, 是**我们自己的 `hardenProcess()` 给 GUI 主进程施加的缓解策略**。

- **症状(v2.15.13 实机日志)**: 360 已退, `LoadCursorW 失败` / `LoadIconW 失败` / `GUI 初始化失败: ...user32.dll...(错误 1114, DLL 初始化失败)`; 看门狗已正确"主进程正常退出"(v2.15.11 的循环修复仍有效)。管理员/非管理员都挂, 首次双击就挂。
- **根因(代码层, 确定性)**: `hardenProcess()` → `applyMitigation(CurrentProcess())` 给**加载 user32 的 GUI 主进程本身**施加了:
  ```go
  {procMitSignature, 0x1 | 0x2},   // MicrosoftSignedOnly | StoreSignedOnly ← 逻辑矛盾!
  {procMitDynamicCode, 0x1},       // ProhibitDynamicCode / ACG
  {procMitStrictHandle, 0x1},
  ```
  1. **`procMitSignature = 0x1 | 0x2`** 要求镜像"必须 Microsoft 签名 *且* 必须 Store 签名", 逻辑矛盾——没有任何 DLL 能同时满足。`user32.dll`(仅 Microsoft 签名、非 Store 签名)在**加载期被签名策略直接拦截**, `LoadLibrary` 返回 **1114(DLL 初始化失败)**。
  2. **`procMitDynamicCode`(ProhibitDynamicCode/ACG)** 同样可能在 `user32` 的 `DllMain` 初始化期干扰。
  - 自保护在 `winMain` 之前运行, 所以 GUI 进程启动即被自己的策略锁死 user32。管理员/非管理员都执行 `hardenProcess`, 故都挂。
- **为什么会被误导**: 1114 的错误信息文案写的是"可能被本机安全软件(EDR/杀毒)拦截", 加上本机确有 360, 自然先入为主归到 360。教训:**用户一句"360 退了还不行"就是最强反证, 应立即放弃外部假设、回查自身代码。**
- **v2.15.14 修复(两道保险)**:
  1. `applyMitigation()` 仅保留 `procMitImageLoad(PreferSystem32Images, 0x4)`——该策略只"优先 system32", **不拦截系统 GUI DLL 加载**, 且有防 DLL 劫持正向价值; 移除签名/动态代码/严格句柄三项激进策略(它们对只加载受信系统 DLL 的 GUI 进程无必要, 却足以自断 GUI)。
  2. 新增 `preloadGUIBasics()`:在 `protectSelfDACL()` 之前先把 `user32.dll`/`gdi32.dll` 用 `windows.LoadLibrary` 映射进进程(不 FreeLibrary, 保留映射), 即使策略对加载期有影响, `winMain` 也可复用已加载模块。
  - 激进策略本应只作用于**运行非受信代码的引擎子进程**(`runSilverFox` 分支), 而非 GUI 主进程; 后续如需对引擎子进程施加, 应在子进程分支按需单独设置。
- **验证**: Wine 冒烟测试 `预加载探针: user32.dll 加载成功` + `主窗口创建成功 hwnd=0x...`; Wine 不强制执行缓解策略故无法复现 1114, 但代码层根因为确定性修复, 实机应正常弹界面。
- **脱敏**: 本条不承载机器路径/签名/密钥。

**排障铁律(升级版)**:
1. 当"已退出某安全软件仍 1114"时, **第一反应是回查自身进程做了什么**(尤其自保护/缓解策略/注入/token 操作), 而不是继续在外部安全软件上追加假设。
2. 给**自身进程**施加 `ProcessSignaturePolicy` / `ProcessDynamicCodePolicy`(ACG) 等加载期策略前, 必须确认 GUI 进程依赖的系统 DLL(user32/gdi32/...)不受影响——`MicrosoftSignedOnly|StoreSignedOnly` 这类"与"组合是典型自杀写法。
3. 进程缓解策略应只施加于**真正运行非受信代码**的子进程, GUI 主进程只加载受信系统 DLL, 不该吃激进策略。
4. 错误信息文案不要硬编码"被安全软件拦截"这类诱导性归因; 应写中性描述 + 通用排障清单, 避免误导后续排查。

## 20. WindowsApps 应用执行别名 pwsh 在 RunAs/-File 长中文路径下返回 9020 —— 启动器必须"真实路径优先+候选验证+别名兜底告警"(2026-08-22 v2.15.15 实战)

**症状**: bat 启动器(非管理员)命中 `WindowsApps\pwsh.exe` 应用执行别名后调用 `-NoProfile -File engine.ps1`, PowerShell 引擎进程直接失败(9020), 退出码非 0, 引擎未运行; 换真实安装路径 `C:\Program Files\PowerShell\7\pwsh.exe` 则完全正常。

**根因**: 安装 PowerShell 7 后 `%LOCALAPPDATA%\Microsoft\WindowsApps\pwsh.exe` 必然存在(应用执行别名), 但该别名在 UAC/RunAs 提权、长中文路径、或非交互环境下执行 `-File` 会返回 9020; `Test-Path` 能命中别名, 因此"能找到 pwsh 就用它"的简单逻辑必然踩中别名陷阱。

**对策(启动器 v1.57, 四步)**:
1. 优先级1: 真实安装路径候选(64/32位 PowerShell 7 → System32/SysWOW64 5.1), 每个候选 `call :PS_VALIDATE` 用 `-Command "exit 0"` 实际验证, 失败清空候选(验证而非仅 Test-Path);
2. 优先级2: `where pwsh`/`where powershell` PATH 搜索, 用子串替换法排除 WindowsApps 命中(管道+延迟展开陷阱), 同样逐候选验证;
3. 优先级3: WindowsApps 别名仅最后兜底, 命中时控制台+日志双告警(`[may cause 9020 under UAC/RunAs]`);
4. 引擎调用行追加 `2>> log` 捕获 stderr, stdout 保留交互菜单。

**教训**: ①"找到即用"≠"可用"——凡涉及执行别名/链接/伪路径, 命中后必须实际验证一次(exit 0); ②UAC/RunAs 场景会放大别名差异, 非管理员验证通过不代表提权后可用; ③系统盘路径候选应显式列出并逐项验证, 不要依赖 PATH 顺序。

**脱敏**: 本条不承载机器路径/签名/密钥(安装路径为 Windows 通用范式)。

## 21. 双重 BOM 写入导致脚本被 PowerShell 5.1 静默拒绝执行(无输出 exit 1) —— 编辑回写时严禁重复前置 BOM(2026-08-23 v2.15.15 实战)

**症状**: 引擎 ps1 经"升级脚本回写"后, 双击/命令行执行**无任何输出**且退出码 1(引擎未启动); 简单脚本同目录正常, 语法解析(Parser::ParseFile)通过, 文件中后期探针全部不显示, 但**文件最前面额外加的第一行 Write-Host 能显示**。

**根因**: 回写脚本 `"﻿" + text` 前置 BOM, 而解码时用了 `decode('utf-8')`(未剥原 BOM → text 已含 `\ufeff` 字符) → 文件头变成**双重 BOM**(`EF BB BF EF BB BF`)。PowerShell 5.1 读取时剥离一个 BOM, 剩余 `\ufeff` 位于首行注释前, 导致脚本被**静默拒绝执行**(无报错、无输出、RC=1; 探针插在首行注释之后故全部不显示)。

**对策(铁律)**:
1. **有 BOM 的文件回写**: 一律 `open(path,'rb').read()` → `decode('utf-8-sig')`(先剥掉 BOM) → 修改 → `encode('utf-8')` → 若要 BOM 则**只前置一次** `b"\xef\xbb\xbf"`。
2. **写完必检文件头**: `open(path,'rb').read(6).hex()` 应为 `efbbbf23...`(单 BOM)或 `2320...`(无 BOM), 严禁 `efbbbfefbbbf`。
3. **"第一行探针"技巧**: 脚本无输出时, 先在文件**第 1 行**(BOM 后第一字符位置)加 Write-Host 验证执行, 再按需二分——第一行能显示而后续探针全不显示 ⇒ 加载/解析层问题(如双重 BOM), 而非脚本逻辑问题。
4. v1.53.0 交付的 v2.15.15 即因此坑实机失败(用户实机 + 无交互复现双重确认), 修复为单 BOM 后引擎正常。

**脱敏**: 本条不承载机器路径/签名/密钥。

## 22. bat 提权调用 Start-Process -ArgumentList 双坑: "-Command 字符串"下 $args 恒为 null + 不接受空集合(2026-08-23 v2.15.17 实战)

**症状**: bat 内 UAC 提权 `powershell -Command "Start-Process -FilePath '%~f0' -ArgumentList $args -WorkingDirectory ... -Verb RunAs" %*`, 用户选择"申请管理员权限"后 PowerShell 报 `无法对参数"ArgumentList"执行参数验证。该参数为 Null、为空或参数集合的某个元素包含 Null 值`, 提权失败降级普通权限(引擎能跑但 HKLM/服务扫描受限)。

**坑1 - $args 恒为 null**: `-Command "字符串"`(字符串形式)时, **$args 自动变量恒为 null**(仅 `-Command {scriptblock} 尾参` 形式才把后续 token 传给 $args); 期望 `%*` 通过 `-Command "..." %*` 变成 $args 数组是错误假设。

**坑2 - 空集合也报错**: 即使换成 `$a=@(); if ($env:X) { $a = $env:X -split ' ' }` 再 `-ArgumentList $a`, **空数组 @() 依然报同一错误**(验证信息要求集合非空且无 null 元素)——空参场景必须**省略 -ArgumentList 参数**, 用双分支。

**对策(验证过)**: bat 侧 `set "SF_ELEV_ARGS=%*"` → PS 内 `$a=@(); if ($env:SF_ELEV_ARGS) { $a = $env:SF_ELEV_ARGS -split ' ' }; if ($a.Count -gt 0) { Start-Process ... -ArgumentList $a ... } else { Start-Process ... }`; 当前调用面参数均无空格(-split ' ' 安全; 含空格参数需引号解析慎重)。

**验证方法**: 本地等价脚本(不带 -Verb RunAs, FilePath 用 cmd.exe + Hidden + PassThru + Stop-Process)分别测带参(CNT=2)与空参(OK)两分支, 确认无 ParameterBindingValidationException 再交付; 真 UAC 弹窗由用户实测。

**脱敏**: 本条不承载机器路径/签名/密钥。

## 23. PowerShell 踩坑三连: TrimEnd 字符串转 char、Register-CimIndicationEvent 参数集互斥、chcp 65001 与 GBK 脚本混合乱码(2026-08-23 v2.15.18 实战)

**坑1 - TrimEnd 传双反斜杠字符串(易看走眼)**: `$d.TrimEnd('\\', '/')` —— PowerShell 单引号里 `\\` 是**两个反斜杠字符**, 而 TrimEnd 的 trimChars 参数按 char 转换, 报 `无法将"\\"转换为类型"System.Char": 字符串的长度只能为一个字符`。**正确写法: `'\'`(一个反斜杠)**。经验: 单引号字符串中反斜杠**不是转义符**, 写多少就有多少个。

**坑2 - Register-CimIndicationEvent 参数集互斥**: `Register-CimIndicationEvent -ClassName Win32_ProcessStartTrace -Query $query` 报 `无法将参数"Query"绑定到目标...无法解析参数集名称` —— `-ClassName` 与 `-Query` **属于不同参数集, 不能同时指定**; 用 `-Query` 时去掉 `-ClassName`(WQL 里已含类名)。

**坑3 - chcp 65001 与 GBK bat 混合乱码**: 控制台 `chcp 65001` 后, 编码为 GBK 的 bat 自身 `echo` 中文被按 UTF-8 解码 → 乱码; 而 PowerShell 侧若又设置 OutputEncoding=UTF8(与 cmd 混用) 则引擎输出正常/bat 乱码。**统一方案(Windows 中文环境): bat 不 chcp(保持系统默认 936) + 引擎 `if ($env:OS -eq 'Windows_NT') { [Console]::OutputEncoding = GetEncoding(936) }`, 两侧同为 936 才一致**。注意 PowerShell 重定向(`>`)输出受 `[Console]::OutputEncoding` 影响, 子进程也会继承控制台代码页。

**脱敏**: 本条不承载机器路径/签名/密钥。

## 24. 拦截系统关机: 杀 shutdown.exe 无效, 必须隐藏窗口 + WM_QUERYENDSESSION=FALSE(2026-08-23 v2.15.19 实战)

**教训核心**: 用户态拦截关机,**杀进程(shutdown.exe)无法阻止系统关机** —— shutdown 请求已提交会话管理器(LSM), 杀进程不撤销; 实测拦截日志显示"已阻止(Sys32)"但系统仍关机。

**真正机制**: 系统关机流程(WM_QUERYENDSESSION)会向进程的**顶层窗口**广播; 窗口回调返回 **FALSE(0)** → 关机/注销/重启被拒绝(用户关机会被取消)。console 进程**没有窗口** = 收不到该消息 = 默认允许关机。**必须**:
1. 注册隐藏窗口(RegisterClassExW + CreateWindowExW, style=0 不显示; 隐藏窗口同样收系统广播);
2. **独立线程**运行 GetMessageW 消息循环(PS 主线程会被阻塞, 必须 Thread + C# 实现消息循环);
3. WndProc 中 `WM_QUERYENDSESSION(0x11) 返回 IntPtr.Zero(=FALSE)`; `WM_ENDSESSION(0x16)返回 0`;
4. ShutdownBlockReasonCreate(hwnd, reason) 提供系统提示原因(辅助, 不阻止);
5. 引擎退出/正常检测结束时 Stop(): ShutdownBlockReasonDestroy + PostThreadMessage(WM_QUIT)。
6. 杀进程/事件订阅保留作为兜底(拦截 /t 型延迟关机), 但不作为主手段。

**Register-CimIndicationEvent vs Register-WmiEvent**: CIM cmdlet 对 WMI trace 事件类(Win32_ProcessStartTrace 等)支持不佳(返回 null, 后续 Register-ObjectEvent -InputObject 报"参数为空值"); 老 API **Register-WmiEvent -Query -Action** 兼容性更好。

**脱敏**: 本条不承载机器路径/签名/密钥。

## 25. Add-Type C# 两连坑: ref 实参未初始化(CS0165) + DllImport 模块写错(kernel32/user32)(2026-08-23 v2.15.20 实战)

**坑1 - ref 实参未显式初始化(编译错误)**: `MSG m; while (GetMessageW(ref m, ...) > 0) {...}` —— C# 规则: **ref 实参必须已明确赋值**, 否则 CS0165 `使用了未赋值的局部变量 m`(哪怕 DllImport 运行时其实会赋值)。**修复: `MSG m = new MSG();`**。教训: 传给 ref/out 参数的局部变量必须显式初始化, 不要依赖被调方法"肯定会赋值"。

**坑2 - DllImport 模块名写错(编译过/运行崩)**: `[DllImport("user32.dll")] GetModuleHandleW` —— **GetModuleHandleW 在 kernel32.dll**, 不在 user32.dll; 编译能过(模块名只是字符串)但运行时 `无法在 DLL "user32.dll" 中找到名为 GetModuleHandleW 的入口点`。**教训: Add-Type 的 DllImport 只有运行时才校验; 函数所在模块要查准(kernel32/kernelbase/user32/advapi32/wintrust...)**。

**坑3 - 隐含检测**: 引擎实机日志 `[关机拦截] 层3 初始化失败 (非致命): 无法添加类型。出现编译错误。` —— Add-Type -ErrorAction SilentlyContinue 吞掉了细节, 只留一句"编译错误"; **诊断方法: 本地提取 C# 用 Add-Type -ErrorAction Stop 单测, 把 C# 代码抽出来独立编译定位报错行**。

**脱敏**: 本条不承载机器路径/签名/密钥。

## 26. 多档交付入口命名: 面向用户的文件名 + 强制关机(/f)的用户态边界(2026-08-23 v2.15.21 实战)

**入口命名(交付规范)**: 多档二进制(主/心跳/硬核)若只按内部代号命名(SilverFox.Heartbeat.exe/SilverFox.Hard.com), 用户遇到"主程序打不开"时不知道点哪个。**交付名应按用户意图命名**: 档2/档3 改为「如果主程序打不开点我.exe / .com」(同名主体按扩展名区分)。**注意**: 改名只影响交付包文件名, 脚本/代码不得硬编码文件名(本产品经 grep 确认无硬引用, 但改名前必须全仓 grep `Heartbeat|Hard\.com`), 且 exe 内部走 `os.Executable()` 自引用(看门狗/守护 spawn 自身, 与文件名无关)。

**QUERYENDSESSION 拦截的边界**: 隐藏窗口 + WM_QUERYENDSESSION=FALSE 可阻止**非强制**关机/注销/重启; 但 **`shutdown /s /f`(强制)时系统发出 CRITICAL 标志的 QUERYENDSESSION, 返回 FALSE 不可靠/被忽略** —— 用户态无法阻止强制关机(需内核驱动/设置策略)。**诊断法**: WndProc 收到 QUERYENDSESSION 时写 `%TEMP%\sf_sg_query.log`(时间+返回值), 用户测试后查该文件: 有记录=消息到达返回 FALSE(非强制场景应被阻止); 无记录=用户用了 /f 或消息未广播。

**脱敏**: 本条不承载机器路径/签名/密钥。

## 27. 万能下载器脚本: 便携 + 动态识别 + 启动检测 + 按序降级(2026-08-23 v2.15.22 实战)

**需求**: 交付包附"一键下载并打开第三方工具(压缩包)"的独立脚本, 要求: ①全便携(%~dp0, 绝无本机绝对路径, 可拷到任何电脑); ②下载产物放**独立统一文件夹**(如 `%~dp0tools\<工具名>\`, 不污染主目录); ③目标软件可能更新/改名/结构变化 → **动态扫描识别**(dir 通配取候选, 不硬编码); ④启动后**检测进程**是否真的起来(tasklist findstr 候选进程名/主程序名), 没起来就**按结构顺序降级试下一个入口**; ⑤支持 DRYRUN 检测模式(环境变量, 只下载解压识别不启动, 便于自动化测试)。

**踩坑**: ①脚本内 echo 行含圆括号且位于 if/&&/|| 块内 → cmd 报"此时不应有 X"/语法错(本 skill §11 教训的又一次实战复现, 块内 echo 一律方括号); ②dir 通配必须考虑**文件名前缀**: 目标文件叫"急救箱运行不了...exe", 模式写 `运行不了*.exe` 不匹配, 应 `*运行不了*.exe`; ③curl 进度输出走 stderr, 自动化捕获时用 `>nul 2>&1` 或容忍; ④下载用 `curl -L` 优先, 回退 `Invoke-WebRequest -UseBasicParsing`; 解压用 `Expand-Archive -Force`(5.1 对中文路径 OK)。

**脱敏**: 本条不承载机器路径/签名/密钥。

## 28. hosts 劫持自检链: 下载失败 -> UAC 提权 -> 检测/移除 360 域名重定向 -> 重试(2026-08-23 v2.15.23 实战)

**场景**: 工具自动下载第三方包失败, 怀疑 hosts 被劫持(伪装域名指向恶意 IP 导致下载被劫/被断)。**排障链(bat 内可落地)**:
1. **先探测连通**: curl -sL -r 0-1023 下载头验证 HTTP 200/206 (完整下载前先探测);
2. **失败 -> 提权检查**: `whoami /groups | findstr /i "S-1-16-12288"` 判断管理员, 非管理员用 Start-Process -Verb RunAs 提权**重跑自身并带标记参数**(如 /fix-hosts; 本 skill §22 的 env 传数组+空参双分支写法), 新实例执行修复;
3. **检测/修复 hosts**: `C:\Windows\System32\drivers\etc\hosts` -> 先备份(hosts_backup_时间戳, 放独立文件夹) -> 正则 `(?i)(360safe|360\.cn|360\.com|qihoo|totalsecurity...)` 匹配 **非注释且以 IP 开头** 的行(`^\s*[^#]`) -> 移除 -> 原编码写回(CRLF);
4. **重试下载**; 仍失败则提示手动(防死循环: 带标记重跑后不再提权)。
**实现技巧**: 幂等 PS 脚本用 **-EncodedCommand(base64 UTF-16LE)** 嵌入 bat, 彻底避开 cmd 引号/转义地狱(在生成脚本时用 python 编码); bat 读 `%1` 标记分支处理。**边界**: 仅处理明确域名条目, 注释行与无关行一律保留; 修改系统文件前必须备份。

**脱敏**: 本条不承载机器路径/签名/密钥。


### 28.1 安全工具特别提醒: -EncodedCommand 与恶意软件混淆手法撞脸(2026-08-25 补)

> 本条是对 §28 的反向补充——`-EncodedCommand` 技术上是对的(避开 cmd 引号/转义地狱), 但在**开源防御性安全工具**这个特殊场景下有额外考量。

**问题**: `-EncodedCommand(base64 UTF-16LE)` 是银狐/Gh0st 等恶意家族**自己的混淆手法**——把 PS 脚本 BASE64 编码后传给 `powershell.exe -EncodedCommand`, 躲避字符串扫描和命令行审计。作为**防御性安全工具**用同样的手法会让:
- 沙箱/EDR 第一眼就警觉(行为特征命中恶意家族模式)
- 人工分析师审 bat 时看到 `-EncodedCommand` 会先怀疑这是不是恶意脚本
- 杀软云信誉积累阶段可能因此被判"风险"权重高

**适用场景区分**:
- **内部工具/一次性脚本**: 用 `-EncodedCommand` 没问题, 避开引号地狱的实际收益大
- **开源防御性安全工具(对外发布)**: 建议改用**独立 .ps1 文件 + `-File` 调用**——脚本逻辑写在明文 .ps1 里, bat 只做 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Check-HostsHijack.ps1" -Arg1 "..."` 的调度, 更透明、可审计、与恶意手法不撞脸

**额外好处**: 独立 .ps1 文件可以被 git diff 追踪变更、被 IDE 语法高亮、被 PowerShell 静态分析器(PSScriptAnalyzer)检查, 而 BASE64 内嵌脚本这些能力全部失去。

**反向教训来源**: 2026-08-25 在对银狐样本 `install_h8.0.10.exe` 的逆向分析中, 样本第3层载荷就是用 20 字节循环 XOR 加密 PowerShell 命令, 解密后含 `Add-MpPreference -ExclusionPath 'C:\'` 等攻击命令——防御性工具用 `-EncodedCommand` 等于把自己和这类样本放在同一个行为特征桶里。

**脱敏**: 本条不承载机器路径/签名/密钥。


## 29. 交付物审查: 顺序执行穿入排障段 + goto 指向不存在标签 + 版本链漂移自查(2026-08-23 v2.15.24 实战)

**场景**: 用户要求"检查并优化全部代码/说明/逻辑不通/旧无效代码"。静态审查 + 控制流走查发现三类真问题:

**坑1 - 顺序执行"穿入"下游标签段**: bat 在 `if exist X (goto :A) else (...)` 后**没有显式终止分支**, 顺序执行会掉进后续 `:TRY_UAC_...`/`:FIX_...` 排障标签段(标签定义不阻断执行流!)。本案例: 下载成功后本应解压, 却一路执行进"下载失败排障段"——已提权的窗口会误触发 hosts 修复。**对策**: 每个成功/失败分支的末尾必须显式 `goto :下一段` 或 `exit /b`; 审查时对每个"条件跳转"追踪"未跳转时顺序落到哪一行"。

**坑2 - goto :DOWNLOAD 指向不存在的标签**: 排障段末尾 `goto :DOWNLOAD`(意图"修复后重试下载"), 但脚本从未定义 `:DOWNLOAD` 标签 → 一旦走到该行, cmd 报"找不到批处理标签 - DOWNLOAD"(且在 `if not exist` 块内极易被吞/直接退出)。**对策**: 静态自查 `goto` 集合与 `^:` 标签集合求差集(排除内置 `:eof`), 任何 `goto` 目标必须存在; 并把"下载段"提升为真正的 `:DOWNLOAD` 标签 + 失败分支用 `if defined SF_FIXED` 防重试死循环。

**坑3 - 版本链漂移(文档/入口 bat 停在旧版)**: 多轮迭代中 exe/ps1/SKILL 都 bump 了, 但① `银狐检测所有程序无法运行时请看此文档.txt` 仍是 v2.15.21; ② 两个入口 bat 仍是 v2.15.21; ③ 主 bat 头注释 "v1.59" 与 banner "v1.60" 不一致; ④ UI ps1 头部 "v1.0"。**对策**: 每轮交付前 grep 全目录 `v\d+\.\d+\.\d+` 统计分布, 与当前版本对照; 头注释/标题行单独检查(它们最易漏)。

**坑4 - 死代码**: `echo [OK] 下载完成` 位于 `exit /b 1` 之后(config 流不可达)。**对策**: 审查时对 `exit /b`/`goto :eof` 之后的代码段检查可达性。

**坑5 - manifest 重签算法(权威, 与 Go exe 层 runIntegrityCheck 严格一致)**: `payload = strings.Join(entries, "\n") + "\n" + signed + SALT`, 其中 **signed 是完整行(含 "signed=" 前缀)且与 SALT 之间没有任何换行**! v2.15.24 因 python 重签时多写了 `\n`, Go 层校验必失败("清单签名无效"弹窗, 而 python 回读自验却通过——因为自验用了同样的错误算法)。**铁律**: ① 重签前先读 `main.go` runIntegrityCheck 的 payload 拼接原文, 照抄, 不要凭记忆; ② 自验必须"用 Go 的提取逻辑"(`^[^|]+\|[0-9a-fA-F]{64}$`, 排除 signed=/sig= 行)重算 sig 对比; ③ 最终以"用户实机跑 exe 无弹窗"为真验证, python 自验只能证明"自洽"不能证明"与 Go 一致"; ④ 改完 main.go 若涉及校验算法, 必须重编译三档。

**脱敏**: 本条不承载机器路径/签名/密钥。

- **v1.62.0 (2026-08-23)**:**新增「交付物审查: 顺序执行穿入排障段 + goto 不存在标签 + 版本链漂移」实战(v2.15.24)**:① **坑1**: bat 条件分支后未显式终止, 顺序执行穿入下游排障标签段(下载成功后误触发 hosts 修复)——标签定义不阻断执行流, 成功/失败分支末尾必须显式 goto / exit; ② **坑2**: `goto :DOWNLOAD` 指向不存在的标签(静态求差集验证: goto 集合 - 标签集合, 排除 :eof); ③ **坑3**: 版本链漂移自查(grep 全目录版本串分布, 文档/入口 bat/头注释最易漏); ④ **坑4**: `exit /b` 之后死代码不可达; ⑤ **坑5**: manifest 重签条目提取必须排除 signed=/sig= 行, 且回读验证 sig; ⑥ 脱敏: 不承载机器路径/签名/密钥。
- **v1.62.1 (2026-08-23)**:**修正 §29 坑5: manifest 签名算法与 Go 层严格一致**——`payload = entries.join("\n") + "\n" + signed(带前缀) + SALT`, signed 与 SALT 无换行; v2.15.24 首次重签多写 `\n` 导致实机"完整性自检清单签名无效", 已改 `baf148e168b4dadf` 并重新打包上传。**教训**: 重签算法必须照抄 Go 源码 runIntegrityCheck, 且 python 自验自洽 ≠ 与 Go 一致, 以实机 exe 无弹窗为准。

## 30. 专杀工具改名链 + 交互三选一 + 工作目录触发杀软教训(2026-08-23 v2.15.34 实战)

**场景**: 用户要求把检测工具全面改名为「顽固木马扫描专杀-银狐特攻」并做功能整体升级(扫描+主动防护 -> 用户选择隔离/删除)。

**坑1 - 改名必须全链**(任一漏改=用户可见的旧名):
- 主程序 exe 名(`SilverFox.exe` -> 中文名) -> 引擎 bat 路径引用(main.go 里 `"legacy", "xxx.bat"`) -> bat 文件名(必须同步改名+引用) -> **manifest 条目名**(`integrity.manifest` 里 `银狐木马检测.bat` 条目必须 `RENAME` 映射, 只改文件不改清单条目=实机"文件被篡改/缺失") -> 报告/隔离区前缀(引擎 ps1 里的字符串常量) -> AppTitle/窗口标题/按钮文案 -> 入口 bat/README/文档里对 exe 名的引用 -> versioninfo FileDescription -> 旧 exe 移备份(勿删, 用户选择)。
- 自查: `grep -r "旧名" 交付目录` 全扫(覆盖 UTF-8/UTF-16LE/GBK 三种编码), 二进制要搜 utf-16-le。

**坑2 - 交互三选一(隔离/删除/跳过)**:
- 删除必须"先备份再删": `Quarantine $path "删除前备份" -Force` 成功后再 `Remove-Item -LiteralPath $path`; 备份失败**绝不执行删除**(防误删不可恢复)。
- 删除确认必须二次确认(y/n), 且提示"物理删除+留底"。
- 保留第 3 选项"跳过", 尊重用户不处理的权利。

**坑3 - 工作目录触发杀软(重要!)**:
- 本机杀软对含"病毒/木马/专杀/删除/隔离/PowerShell 注入特征"字符串的**临时脚本**在**C 盘用户目录**下会疯狂报毒(误报), 而 **E:\工具\5 工作区**在白名单区不报。
- **铁律**: 所有中间脚本/临时文件(生成/打包/校验 .py .ps1 .txt)一律放**工作区目录**(如 `E:\工具\5\02_升级工作区\work\`), 严禁写 `C:\Users\<user>\...\.cowork-temp` 等 C 盘路径; 已污染的 C 盘临时文件必须清理(删除前 AskUserQuestion 确认)。
- 若用户明确"在这个文件夹下工作", 后续所有工具调用写文件的目标都要跟随。

**坑4 - manifest 重签时条目录入要恢复**: 从 zip 备份的旧 manifest 提取完整 33 条顺序(含后续改名的文件), 做 RENAME 映射再重算, 未知丢失条目会导致实机完整性自检报"文件被篡改"。

**脱敏**: 本条不含机器路径/密钥(工作目录仅作范式引用)。

## 31. 看门狗 PID 复用残留 + exe 双编码版本校验 + 控制台引擎 GUI 进度展示(2026-08-23 v2.15.35 实战)

**场景**: 用户反馈"关闭工具后后台仍有进程" + "扫描黑窗口没内容, 扫描干脆做成 UI 展示"。

**坑1 - 看门狗按 PID 轮询会因 PID 复用永不退出(后台进程残留真因)**:
- 症状: 主程序正常退出(guard flag 已删), 但后台残留一个与主程序同名的 exe(约 2MB、无窗口、命令行 `--watchdog <pid> --tier N`)。
- 根因: 看门狗 `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, pid)` 轮询 PID 判断主进程存活; 主进程死后其 PID 被系统其它进程**复用** -> OpenProcess 恒成功 -> 看门狗误判"主进程还活着" -> 永不退出。
- 修复: 看门狗持有**进程句柄**并 `WaitForSingleObject(h, 2s)` —— 进程句柄锁定的是同一进程对象(Win32 进程对象句柄), 不受 PID 复用影响; 进程终止时句柄变为 signaled(WAIT_OBJECT_0=0 终止 / WAIT_TIMEOUT=0x102 存活)。重启主进程后须重新 `OpenProcess` 拿新句柄(句柄不随 PID 更新)。
- **坑**: golang.org/x/sys/windows 里没有 `PROCESS_SYNCHRONIZE` 常量(编译报 undefined), 正确的是 `windows.SYNCHRONIZE`(0x00100000, 与 PROCESS_QUERY_LIMITED_INFORMATION 等组合); OpenProcess 需要的权限权限在 PROCESS_SYNCHRONIZE 缺失时 WaitForSingleObject 会失败。
- 自查: `tasklist /v` / `Get-Process` 看残留无窗口同名进程 + `Get-CimInstance Win32_Process` 看 CommandLine 是否 `--watchdog`。

**坑2 - 搜 exe 内版本串要双编码(UTF-8 + UTF-16LE)**:
- Go 源码里的字符串常量(如 AppTitle/buildTag)在 PE 中存储为 **UTF-8**; versioninfo 资源(FixedFileInfo/StringFileInfo)字符串存储为 **UTF-16LE**。
- 只搜 UTF-16LE 会漏掉 Go 常量(显示 0 假失败); 只搜 UTF-8 会漏掉 versioninfo。
- goversioninfo 警告 `FixedFileInfo.FileVersion (x.y.z.0) and StringFileInfo.FileVersion (x.y.w.0) do not match` = versioninfo.json 的**数字版本(Patch)**与**字符串版本("2.15.34.0")**没同步, 两处都要改。
- Comments/FileDescription 等 StringFileInfo 字段对外可见(exe 属性), 命名铁律同样适用。
- **坑**: manifest 的 `sig=` 行只存**前 16 位**(sha256(payload) 十六进制前 16 字符) —— Go 层 `calcSig := hex[:16]` 与文件 sig 直接 EqualFold 比较; 存 64 位完整签名 => 16 vs 64 永远不相等 => 实机必弹「完整性自检: 清单签名无效」(python 自验自洽也会 PASS, 只有实机 exe 能暴露, 同 §29 坑5 教训)。

**坑3 - 控制台交互引擎的进度无法整体重定向**:
- 引擎(ps1)含 Read-Host/pause/三选一交互, `cmd /c bat > file` 整体重定向会破坏交互/挂起。
- 折中: 引擎在**阶段边界**调 `Add-Content -LiteralPath $ProgressLog -Value $msg -Encoding UTF8` 双写进度文件(UTF-8, 扫描开始前 Clear-Content); GUI 主程序 `go watchScanProgress`: 每 500ms `os.ReadFile` 增量, 文本变化即 `SendMessage(WM_SETTEXT)` 刷新到界面多行 EDIT; 引擎进程结束(`engineAlive()==false`)约 4s 后停止轮询保留最后进度。
- 控制台窗口保留(完整输出+交互), GUI 只作进度面板, 两者并行不冲突。

**脱敏**: 本条不含机器路径/密钥(工作目录仅作范式引用)。

## 32. 目录扫描验签挂起: Get-AuthenticodeSignature 对每个文件都跑会卡死(2026-08-24 v2.15.36 实战)

**场景**: 用户反馈扫描"一直卡在这里"(GUI 进度停在第 N 行, 报告停在某个进度百分比不动)。实测: [2/7] 文件扫描到 3500/14820 停 15 分钟无进展。

**根因**: 文件遍历循环里对**每个文件**(含图片/文档/text)都调用 `Test-TrustedSigner`/`Test-SafeHarbor`, 它们内部 `Get-AuthenticodeSignature -FilePath` —— 该 API 对**大文件(几十 MB)/云盘占位文件(OneDrive 未下载)/畸形 PE/网络路径**会**挂起数分钟甚至更久**。第一个扫描批次目录(AppData, 多小 exe)顺畅, 第二批次(下载/文档目录, 大文件)在遇到"毒丸"文件时卡死。

**修复**:
- 验签**前置条件**: 必须先读文件头确认 PE(MZ)+ 大小 <= 50MB, 才调用验证; 非 PE/超大文件跳过验签(哈希比对兜底)。
- 白名单(路径/名称, 纯字符串快)优先, 签名验证(慢 IO)靠后。
- 观察类验签(未签名驱动 .sys)同样加大小上限。
- **注意**: 循环内 `return` = 退出整个函数(致命), 应 `continue` 跳过当前文件。

**诊断法**: 报告台账有进度明细(每 500 条), 看进度停在哪 + 该目录文件类型; 找到挂起文件后 `Get-AuthenticodeSignature` 单独计时复现。GUI 进度面板(进度文件轮询)与实际进度对照, 区分"真卡"与"窗口黑屏"(输出流正常但窗口不显示)。

**脱敏**: 本条不含机器路径/密钥(工作目录仅作范式引用)。

## 33. 恢复杀毒软件反推全景 + 批量修改脚本中断丢改动 + 交互确认防误伤(2026-08-24 v2.15.40-44 实战)

**场景**: 用户要求"把常见银狐限制安全软件的行为全部反推到恢复功能", 并写端到端模拟脚本测试。

**反推全景 (restoreav 16 阶段, 银狐限制安全软件手段全集)**:
1. Defender 策略注册表 (Policies 根+Real-Time Protection/SpyNet/Threats/Security Center 子键的 Disable* 值清除)
2. Defender 客户端实际配置 (非 Policies 区, 病毒直接写; DisableRealtimeMonitoring 等)
3. UAC 禁用 (EnableLUA=0 -> 1; 病毒禁 UAC 使安全软件提权失效)
4. 系统工具禁用 (DisableTaskMgr/DisableRegistryTools/DisableCMD; DisallowRun/NoRun 仅提示)
5. Windows Update 禁用 (DisableWindowsUpdateAccess/NoAutoUpdate; 防打补丁)
6. 服务恢复 (Defender 全家 WinDefend/WdNisSvc/SecurityHealthService/Sense/wscsvc/WdBoot/WdFilter + 第三方安全软件服务名正则 360|huorong|hips|antivirus|kaspersky|avp|avast|avg|rising|mfe|mcafee|symantec|norton|qqpc|tencent|safedog|kingsoft|bitdefender|eset|nods32|malwarebytes|fsecure|trendmicro|panda|sophos, Disabled -> sc config auto)
7. hosts 安全厂商域名劫持移除 (0.0.0.0/127.0.0.1 + 厂商域名 -> 备份移除)
8. MpCmdRun -RestoreDefaults
9. Defender 排除项检测 (Exclusions Paths/Extensions/Processes/Threats; temp/appdata/downloads/httpi -> 警告)
10. 服务缺失检测 (Services 键不存在 -> 建议 sfc)
11. 杀软自启动项缺失检测 (Run 名匹配)
12. TamperProtection=0 警告
13. 代理/DNS 异常提示
14. 防火墙状态 (netsh advfirewall; **交互确认再开启, 防误伤故意关闭的用户**)
15. Defender 引擎状态 (Get-MpComputerStatus -> Set-MpPreference 恢复)
16. IFEO 映像劫持 (Image File Execution Options 杀软 exe + Debugger 值 -> 清除)
+ 修复前后对比 (快照 -> 修复 -> 复查, 输出"已验证修复: xxx")

**端到端测试脚本** (restoreav_模拟测试.ps1, 破坏|检查|清理 三模式): 模拟注入 8 项可逆破坏 (Defender 策略×3/客户端/DisableTaskMgr/WindowsUpdate/排除项/IFEO/hosts), 备份到 %TEMP% 支持还原; 引擎修复后"检查"应全绿。

**坑1 - 批量修改脚本中断丢改动**: 一个脚本里多个 rep 连续替换, 最后一个 assert 失败 -> 中断 -> **写盘语句未执行, 前面所有修改全丢** (ID/变量/buildTag 丢失, 编译 undefined)。教训: 关键改动后立即写盘或用小步骤; assert 前打印进度; 每步验证(编译前 grep 关键符号)。

**坑2 - 版本残留三处**: 进度文件首行(Write-ScanProgress 写死 v1.68)、审计日志(写死 v1.55/v1.69)、文档 txt 头部版本(停在 v2.15.35)——每版 bump 必须 grep 全目录版本串(含 ps1 文案/bat/文档), 不只是 main.go。

**坑3 - 自动修复需交互确认**: 防火墙被关可能是病毒也可能是用户故意(玩游戏/内网), 自动开启会误伤 -> 改 Read-Host 确认 (y/n) 且默认 y; 修复类操作对"用户可能故意"的状态要提示。

**脱敏**: 本条不含机器路径/密钥(工作目录仅作范式引用)。

## 34. 发布自动化 + 文本替换定界 + GUI 单实例(2026-08-24 v2.15.50 实战)

**场景**: 8 轮自测期间手工发布流程踩了约 8 个错(undefined/重复声明/误删 30KB/转义/位置错位/正则误匹配/校验逻辑/zip 命名), 遂固化一键发布脚本。

**坑1 - 文本替换必须用"邻近代码边界"定界**: find("查看.")" 定位到远端(同名子串)导致把 58KB 代码替换掉(删 30KB)。对策: 替换段用**下一段代码注释/函数开头**作边界(如 `\t\t// ---- 页面 2 容器`), 且替换后立即编译验证; 较大的替换先打印 span 长度(正常应 <1KB)。

**坑2 - 版本正则要匹配"身份锚点"**: 源码注释含历史版本(v2.15.15/16), 裸正则 `v2\.15\.\d+` 命中注释。对策: 匹配"身份锚点"(如 `AppTitle = "... v2\.15\.\d{2}`), 全量替换前打印数量(正常 15-20 处)。

**坑3 - 发布脚本幂等/校验设计**: 校验不能要求"旧版本=0"(代码已升级再发布时 oldver==ver 必然失败); 只查"目标版本≥3 + tag=1 + versioninfo U16≥2"即可。

**坑4 - GUI 单实例**: 双击二次启动=双窗口+可能双引擎; 用命名互斥(CreateMutex + ERROR_ALREADY_EXISTS)+ FindWindow(类名)激活已有窗口(SW_RESTORE+SetForegroundWindow)+ 退出。看门狗/守护进程各自有独立互斥, 与 GUI 单实例互不影响。

**坑5 - 包内文档更新需重打包**: 修复报告/SKILL 副本在 zip 内, 修改后必须重打包(版本不必 bump, zip 覆盖上传即可); manifest 清单不含文档, sig 不变。

**脱敏**: 本条不含机器路径/密钥(工作目录仅作范式引用)。
## 35. 转码脚本必须幂等可重跑: 编码假设错误导致二次损坏 + 五步自检门禁(2026-08-26 实战)

**场景**: 「网络诊断修复工具」双文件交付(bat 启动器 GBK 编码 + ps1 引擎 UTF-8 BOM), 每轮修改后跑转码脚本规范编码再交付。

**症状**: 第2次跑转码验证脚本时, 脚本仍按 **UTF-8 读**一个**已转成 GBK 的 bat**(第一次转码已完成), UTF-8 解码 GBK 字节产生替换/乱码 → 文件被写坏, 回读一致性校验(GBK 往返 equals)直接 `False`。

**根因**: 转码脚本不幂等 —— 编码假设写死"输入是 UTF-8", 无法应对"输入已是 GBK"的重跑场景。任何"只支持一种输入形态"的转换脚本都会在第二次运行时损坏文件。

**对策**:
1. bat 一律 **GBK 读→GBK 写回**: `[IO.File]::ReadAllText($bat, [Text.Encoding]::GetEncoding(936))` → 规整 CRLF → `WriteAllText($bat, $text, GetEncoding(936))`, 全程 936,**永远不跨编码**"先按 UTF-8 读再写 GBK";
2. 验证三件套: **GBK 往返 equals**(无损) + **无 BOM**(前 3 字节非 EF-BB-BF) + **CRLF 计数**, 三项全过才算转码成功;
3. ps1 侧: 每轮改完必须重新 **UTF-8 带 BOM + CRLF** 转码 —— 通用文本编辑器会把 ps1 写回无 BOM UTF-8, 破坏 PowerShell 5.1 的编码识别; 附 `Parser::ParseFile` 语法复查(`$errs.Count -eq 0` 判定 PARSE OK);
4. **一次性交付门禁编排**(五步全绿才自认完成): 转码(bat GBK 无损往返 / ps1 UTF8BOM) → 字节头验证(首 6 字节 hex) → CRLF 计数 → GBK 回读 equals → Parser 复查;
5. 与 §2 联动复核(本次实战再次验证): bat 启动器全程 goto 结构(无 if/else 括号块、无裸 `()` 文本), PowerShell 候选逐条 `if exist` + `set` + `if not ""=="" goto` 链式探测, `where` 兜底 + errorlevel 判断, 空 `PS_EXE` 断言 `goto NO_PS` 明确报错退出。

**教训**: 转换类脚本的正确性不止"第一次对", 要"第 N 次也对"(幂等); 判断输入形态而不是假设它(读前探字节头), 或让读写编码恒等(GBK 进 GBK 出天然幂等)。

**脱敏**: 本条不承载机器路径/签名/密钥。


## 36. 合并大 bat 工具箱方法论: 标签对照检查前置 + 辅助转码脚本必须纯 ASCII(2026-08-27 实战)

**场景**: 「网络与系统修复工具箱」v1.0 合并工程 —— 旧工具箱(v0.52, 24 个功能项、2000+ 行 bat)与新诊断引擎 network-check.ps1 完全合并为单一入口 bat。

**合并前置三步(动手编辑前必做)**:
1. **备份原件**: `old_toolbox_backup` 目录原样字节拷贝, 不做任何转换 —— 回退保底;
2. **转 UTF-8 工作副本**: GBK 读 → UTF-8 无 BOM 写(无损往返验证), 所有编辑都在 UTF-8 副本上做, 交付前再按 §35 流程转回 GBK —— 编辑期统一 UTF-8, 避免编辑器/工具链的代码页差异干扰;
3. **标签对照检查(合并/大改前必跑)**: `grep -oP 'goto\s+:?\K[A-Za-z0-9_]+'` 提取全部 goto 目标, `grep -E '^:[A-Za-z0-9_]+'` 提取全部标签定义, `comm -23` 求"有 goto 却无标签"差集(**唯一合法豁免 `:eof` 内置伪标签**), 全数对应后才动手编辑 —— 这是 §29「goto 指向不存在标签」的**主动预防版**, 把"运行时才炸"提前到"静态必过"。

**坑A - 辅助转码/生成工具的 ps1 本身必须纯 ASCII(重要)**:
- 第一版 merge-prep.ps1 写了中文注释与中文字符串; PS 5.1 按 **ANSI(936)** 读无 BOM 的 ps1, 中文被逐字节误读成多字节序列, **变量定义行被吞、变量变 null**(报 `Test-Path` / `Join-Path` / "参数为空值");
- 对策: **工具类辅助脚本只写 ASCII 注释与英文串**, 中文只留在成品文件里(bat 用 GBK, ps1 用 UTF-8 BOM);
- 与 §1/§21 同源: 无 BOM 文件的解读编码由系统代码页决定, 不要赌。

**合并原则(大合并不改写)**:
- 尊重旧脚本既有风格(`setlocal enabledelayedexpansion` + `!var!` + `choice /C`), 不做强行重构 —— 旧工具箱 2000+ 行保持原样, 把回归面压到最小;
- 新功能以 goto 标签段落插入: `:EngineDiag` / `:EngineRepair` 调 `%~dp0network-check.ps1 -Mode Check/Repair`; **缺引擎文件时明确报错**, 不静默跳转;
- 主菜单布局: 旧 4 类(系统/网络/常用/特殊)保留 + 顶部新增 `[1]详细诊断` `[2]一键修复` 引擎入口, `[A]请求提权`/`[Q]退出` 沿用, `choice /C` 扩展为 `123456AQ`(keys 列表、提示文案与 ERRORLEVEL 映射同步改全)。

**交付校验**: 复用 §35 五步门禁(bat GBK 无损往返 / 无 BOM / CRLF 计数 / 首6字节 hex / Parser 复查), 全绿后连同引擎 ps1 同目录交付 —— bat 靠 `%~dp0` 定位引擎, 分离即失效。

**教训**: 大合并不等于重写(尊重原风格降低回归面); 动手前的静态门禁(goto/标签对照)比运行时排障便宜得多; 工具脚本自身也要考虑其运行环境的编码假设(辅助 ps1 纯 ASCII 最稳)。

**脱敏**: 本条不承载机器路径/签名/密钥(工具名按已公开项目名保留)。



## 37. Flutter 响应式双端：移动端 MethodChannel 独占功能在桌面端"静默不可用"的识别与纯 Dart 适配(实战)

**场景**: MineAPK 客户端为 Flutter 响应式单代码库(桌面端侧边栏导航 + 移动端底部导航, 共用一套页面)。某页面在桌面端"能打开但永远空列表/数据全无", 移动端正常。

- **症状识别**: 数据来源全部走 `MethodChannel` 原生通道(如 content:// SAF 授权、Shizuku 提权、Android 路径解析、原生 zip 打包导出), 桌面端无对应原生插件实现 → 通道调用抛 `PlatformException` 被各层 try/catch 吞掉 → **降级返回 null/空列表**, 表现是"静默不可用、不报错不崩溃"。
- **排查法**: ① grep `MethodChannel` + `PlatformException` 定位 service 层(功能数据在 service, 不进 UI); ② 对照两端入口清单找缺口(桌面侧边栏导航项 vs 移动端首页快捷卡片, 常见移动端独有的入口缺失于桌面侧边栏); ③ 全库已有平台守卫范本 `isSupported => Platform.isAndroid` + 方法体 `if (!isSupported) return 降级值` + UI 侧 else 分支(如 LAN 悬浮球覆盖层), 新适配照抄该模式。
- **适配手法(纯 Dart 分支, Android 原路径一字不动防回归)**:
  1. **目录定位**: `dart:io` 展开 `%LOCALAPPDATA%`(为空兜底 `%USERPROFILE%\AppData\Local`), 默认路径 + 前缀扫描兜底, 返回"候选列表"; 找不到时把候选路径展示给用户(而不是白屏), 附"先启动一次游戏生成目录"等说明。
  2. **文件扫描**: `Directory` 流式 `await for` 遍历子目录(逐项让出事件循环, 大目录不卡 UI), 以 `level.dat`/`levelname.txt` 存在作为世界的判据; 名称取 `levelname.txt` 首行(trim 后 fallback 目录名); 封面取同级图标文件; 体积用递归求和; 按 mtime 降序。
  3. **打包导出**: `.mcworld` 本质是 zip。用 `archive` 包 `ZipFileEncoder` 流式逐文件 `addFile`(几千个 db/region 文件也不整体入内存), 归档路径=相对世界目录的相对路径(绝不套外层文件夹名, 否则导入错位); 单文件失败(被游戏占用/无权限) try/catch 跳过; 中文名需先清洗 Windows 非法字符 `\ / : * ? " < > |`。
  4. **UI 平台分流**: 所有原生入口按钮按平台分流(桌面 FAB 文案改为"打开目录"、教程/权限弹窗隐藏、空状态显示候选路径 + 打开文件夹/重新扫描按钮)。
  5. **图标本地化**: Android 的 `content://` URI 走 `Image.network`, 桌面本地绝对路径走 `Image.file` —— 用 `^[A-Za-z]:[\\/]` 或 `file://` 前缀判别, **不能无脑把 Image.network 全替换**(会破坏 Android 端)。
- **教训**:
  1. "页面能开但永远空" 第一时间查 service 层 MethodChannel 的 catch 降级, 不要先猜 UI。
  2. 直接 `import` 传递依赖(如 `archive`)必须显式写进 pubspec 并 `pub get`, 否则 `depend_on_referenced_packages` 告警。
  3. 平台分支完整隔离在 `Platform.isWindows`/`isDesktop` 之后, Android 原路径零改动, 用全量 `flutter analyze` 保 0 error 防回归。
  4. 桌面端无原生通道时优先用 `dart:io` + 标准包补 Dart 实现, 不必为此开发原生插件。
- **脱敏**: 本条不承载本机路径/签名/密钥/账号; 目录一律用 `%LOCALAPPDATA%`/`%USERPROFILE%` 范式, 方法通道名与世界文件名按已公开项目名保留。

## 38. Windows 桌面端确定性漏洞审计与修复清单(实战)

> 对 Flutter 响应式双端项目做 Windows 端代码审计，修复了一批"桌面端必现"的确定性问题。三路并行审计(进程/路径/文件、移动端插件误用、UI 列表/索引/null 崩溃)交叉验证。

- **A. MethodChannel 移动端独占 → 桌面"静默降级"**(识别特征:页面能开但永远空/功能静默失效)
  - 地图管理/世界属性/SAF 选目录/Shizuku/广告 SDK/QQ 绑定/扫码/文件选择——全是 Android 原生通道,Windows 无实现。
  - 识别法:grep `MethodChannel` + `PlatformException` 定位 service;功能数据全走 service 不进 UI。
  - 守卫模式:`isSupported => Platform.isAndroid` + 方法体 `if (!isSupported) return 降级值` + UI 侧分支。
  - 修复分层:**有桌面等价能力的给桌面分支**(文件选择→`file_selector` 系统对话框;本地通知→`WindowsInitializationSettings`/`WindowsNotificationDetails`);**无意义的能力桌面隐藏**(QQ 绑定入口、看广告按钮禁用/隐藏);**需要 UI 出路的给占位**(桌面扫码页显示"请用手机扫码"占位,不构造摄像头)。
- **B. zip 打包条目分隔符**(mrpack/.mcworld 必现)
  - Windows 上 `path.relative` 返回 `\`;zip 规范条目必须 `/`。`ArchiveFile(name)` 带反斜杠 → 导入器(MrpackImporter/Modrinth)认不出,嵌套文件静默丢失。
  - 对策:`archivePath.replaceAll(r'\', '/')`,对已是 `/` 的路径幂等安全。
- **C. wmic 已从 Win11 24H2+ 移除**(3 处) → PowerShell `Get-CimInstance`(总内存/可用内存/进程工作集)。旧代码全部返回 8192/4096 假值,内存自适应被静默限死。
- **D. Java 加载器链(4 子问题,安装 Forge/NeoForge 中文/空格路径必挂)**
  1. @argfile 裸 token:Java 按空白拆 token + 平台 charset 读 → 带空格的 classpath/中文路径被拆断/乱码。对策:每条含空格/引号/反斜杠的 token 用双引号包裹。
  2. JVM 读 argfile:argfile 按 UTF-8 写,JDK8/11 默认按平台码页(GBK)读 → 显式加 `-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8`。
  3. `runInShell: !isFullPath && isWindows`:走 cmd.exe 会重新拆分参数 + OEM 码页转码损坏 → 恒 `false`(无 shell 时 Dart/Windows 仍按系统可执行搜索规则找 java,不需要 shell)。
  4. `-javaagent:` argv 预加引号:Process.start 底层拼命令行会自动给含空格参数加引号,预加的引号被 CreateProcess 二次解析残留 → 去掉预加引号。
- **E. Microsoft Store WindowsApps 0 字节 java 跳板**:`where java` 可能返回该别名,运行会弹商店。过滤 `\windowsapps\` 路径 + 0 字节文件;并由 `java -version` 运行时验证兜底。
- **F. reg query 解析**:输出形如 "值名 + REG_SZ + 数据",旧代码 `split('REG_')[0]` 只拿到值名。用 `RegExp(r'REG_\w+\s+(.+)$')` 取数据;环境变量(`LOCALAPPDATA`/`APPDATA`)判空,避免拼出 `null\路径`。
- **G. 服务器动态类型强转全是崩点**:`user['level'] as int` / `(certification??0) as int` / `count as int` / `exp_percent` 直接除——服务器可能给字符串/浮点。对策统一 `int.tryParse(x?.toString() ?? '') ?? 0`;进度条 `double.tryParse + clamp(0,1)`。
- **H. `substring(0, 10)` 先判 `length >= 10`**(8 处,服务器日期可能是 "2026-1-5" 短串)。抽共享工具 `safeDate10()` 一处实现全项目复用。
- **脱敏**: 本条不承载本机路径/签名/密钥/账号;目录一律用 `%LOCALAPPDATA%`/`%USERPROFILE%` 范式,方法通道名按已公开项目保留。

## 39. 开机启动管理 bat: 注册表 Run 键写带空格路径 + set /p 残留值(2026-09-01 实战)

**场景**: 给第三方 GUI 程序(安装路径含空格, 如 `%LOCALAPPDATA%\Programs\<应用>\<名称 app>.exe`)写"开机启动管理"bat 工具(菜单: 添加/取消/查状态)。

- **A. Run 键值必须"自带引号"落盘(核心坑)**: `reg add "%KEY%" /v Name /t REG_SZ /d "%APP_PATH%" /f` 只保证 bat/cmd 解析层不炸, **写进注册表的值没有引号**——登录时 Explorer 执行 Run 键值按空格切分, 空格后的部分被当参数 → 启动失败或弹"找不到文件"。正确写法 **`/d "\"%APP_PATH%\""`**: `\"` 经 cmd 解析 + `CommandLineToArgvW` 双层处理后以**字面引号**落盘, 最终值为 `"C:\...\my app.exe"`(整体带引号)。可用 `reg query` 回读验证值首尾确有引号。
- **B. 注册表 HKCU Run 优于启动文件夹**: 启动文件夹放 bat 每次登录闪 conhost 黑框; **Run 键直接指向 exe 无窗口**。且 HKCU 当前用户可写**无需管理员权限**(HKLM 才需要), 工具通用性最好。若目标软件自带"开机启动"官方设置则优先用官方的, 注册表方案作兜底/批量管理。
- **C. `set /p` 残留值(菜单循环隐患)**: `set /p` 在用户**直接回车(空输入)时不修改变量**, 上一轮输入残留 → 菜单 `goto menu` 循环里必须先 `set "choice="` 清空再 `set /p choice=`, 否则一次有效输入被永久复用(误触同一菜单项/死循环)。**交互变量每次读取前先清空是通用规则**。
- **D. Run 项存在性判断与取消**: `reg query "%KEY%" /v Name 2>nul` + `if errorlevel 1` 判断是否存在(普通行的 `2>nul` 无需转义; 仅 `for /f` 内才要 `2^>nul`); 取消用 `reg delete ... >nul 2>&1`, 对不存在的键也无害, 无需前置判断。
- **E. 交付规范复用**: GBK 编码 + `chcp 936` + CRLF 行尾(§1); 交互提示用 `echo` 单独输出、`set /p var=` 不带提示串(中文提示在部分环境解析不稳); 添加前 `if not exist "%APP_PATH%"` 先验证目标存在, 不盲写注册表。

**脱敏**: 本条不承载机器路径/签名/密钥/账号; 示例路径用 `%LOCALAPPDATA%`/`%APP_PATH%` 范式泛指, 应用名以 `<应用>` 泛指。

更新日志(倒序):
- **v1.71.0 (2026-09-01)**:**新增「开机启动管理 bat」实战(§39)**:① **Run 键值必须"自带引号"落盘**: `reg add /d "%PATH%"` 只保证 cmd 层不炸, 注册表里存的值无引号, Run 键执行时带空格路径被截断 → 必须 `/d "\"%PATH%\""`(`\"` 双层解析后字面引号落盘, `reg query` 回读验证); ② **HKCU Run 优于启动文件夹**(直接指 exe 无黑框 + 无需管理员权限); ③ **`set /p` 空输入不修改变量**→菜单循环交互变量必须读取前 `set "var="` 清空, 防上一轮输入残留误触; ④ `reg query 2>nul + if errorlevel 1` 判存在性, `reg delete >nul 2>&1` 幂等取消; ⑤ §0.1 索引补 1 行 + 实战范围 §14-§38→§14-§39; ⑥ **版本链漂移修正**: frontmatter 停在 1.69.0 而日志已到 v1.70.0(v1.70.0 发布时漏 bump), 本次一并修正; ⑦ 脱敏: 不承载机器路径/签名/密钥/账号。
- **v1.70.0 (2026-08-29)**:**第三次双副本分叉合流——新增 Windows 桌面端 Flutter 适配两章**:用户侧副本(2026-08-28 迭代)新增两章, 原编号 §35/§36 与主线已发布 tag 链的 §35(转码幂等)/§36(合并工具箱)冲突, 合流重编号为 §37/§38, 用户侧原版本号 v1.68.0/v1.69.0 让位主线(以 ClawHub tag 链为准, §29 版本链漂移原则): ① **§37 Flutter 响应式双端**(原§35): 移动端 MethodChannel 独占功能在桌面端"静默不可用"(PlatformException 被 catch 降级空值)的识别与纯 Dart 适配——症状识别(页面能开但永远空)/排查法(grep MethodChannel 定位 service 层 + 两端入口清单对照, 复用 isSupported 守卫范本)/适配手法(目录定位 %LOCALAPPDATA%+前缀扫描兜底 / Directory 流式扫描 / ZipFileEncoder 流式打包 / UI 平台分流 / 图标 content:// 与本地路径正则判别)/教训(显式 pubspec 声明传递依赖 / 分支全隔离在 Platform.isX 后防 Android 回归); ② **§38 Windows 桌面端确定性漏洞审计与修复清单**(原§36): A MethodChannel 桌面静默降级三分法(桌面分支/隐藏/占位)、B zip 条目分隔符 replaceAll('\\','/')、C wmic→PowerShell CIM、D Java 加载器四连坑(argfile 引号包裹+JVM UTF-8+runInShell 恒 false+-javaagent 去预引号)、E WindowsApps 0字节 java 跳板过滤、F reg query 正则取数据段、G 服务器动态类型 tryParse+clamp、H substring 先判长(共享 safeDate10); ③ **§0.1 索引补 3 行**(桌面空数据/zip 嵌套丢失/中文路径 Java 挂), 实战章节范围 §14-§36→§14-§38; ④ **合流要点**: 主线的 §0.1 索引/§17 证伪引导/§28.1 撞脸提醒/双语 description 为用户侧副本所缺, 两侧互补无覆盖冲突(除编号); ⑤ 脱敏: 不承载机器路径/签名/密钥/账号。
- **v1.69.0 (2026-08-27)**:**新增「合并大工具箱方法论」实战 + 二次分叉副本合流**:① **新增 §36**(正文展开): 合并前置三步(备份原件→UTF-8 工作副本→**标签对照检查**: goto 目标/标签定义 comm -23 求差集唯一豁免 :eof, §29 goto 坑的主动预防版); **辅助转码 ps1 必须纯 ASCII**(PS 5.1 按 ANSI936 读无 BOM ps1, 中文注释致变量定义行被吞/变量 null); 合并原则尊重旧风格不强改(goto 标签段插入新引擎入口、缺引擎明确报错、choice /C 扩展同步 ERRORLEVEL 映射); 交付复用 §35 五步门禁+同目录交付; ② **二次合流**: 用户侧分叉副本(v1.67.2 经验仅日志先行、正文未落章)并入本主线, 落成 §36 正文章节; 两副本曾对 v1.67.1 各有赋值, 以已发布 tag 链(v1.68.0)为准; ③ §0.1 症状索引补「合并/重构旧 bat 工具箱」行, 实战章节范围描述更新为 §14-§36; ④ 脱敏: 不承载机器路径/签名/密钥。
- **v1.68.0 (2026-08-26)**:**新增「转码脚本必须幂等可重跑」实战(网络诊断修复工具双文件交付)+ 双副本合流**:① **坑(编码 §35)**: 转码脚本假设输入永远 UTF-8, 第2次重跑时已转成 GBK 的 bat 被 UTF-8 解码写坏, 回读 equals=False —— **转换类脚本要"第 N 次也对", 不能只保证第一次**; ② **对策**: bat 一律 GBK 读→GBK 写回(全程 936 不跨编码, 天然幂等), 验证三件套(GBK 往返 equals + 无 BOM + CRLF 计数); ps1 每轮重转 UTF-8 BOM+CRLF 并附 Parser::ParseFile 复查; ③ **五步交付门禁**: 转码→字节头→CRLF 计数→回读 equals→Parser 复查, 全绿才自认完成; ④ §0.1 症状索引补对应行; ⑤ **双副本合流与版本链修正**: 两份分叉副本(不同会话并行迭代)合并为单一事实源, frontmatter version 从滞留的 1.67.1 直接对齐并超越 tag 链(此前 tag 已至 1.67.3 而 frontmatter 未同步)——正是 §29 坑3 版本链漂移的自我复现, 已修; ⑥ 脱敏: 不承载机器路径/签名/密钥。
- **v1.67.1 (2026-08-25)**:**审查/导航增强(非实战, 维护修订)**:① **新增 §0.1「按症状快速索引」**: 924 行文档按时间倒序追加导致新读者难定位, 新增按症状(闪退/PS无输出/GUI不出现/1114/UAC失败/Wine假装正常/看门狗无限重启/hosts劫持等)的章节导航表, 标注"必读 §19 真因"避免读者重走 §17/§18 弯路; ② **§17 标题前加 ⚠️ 已被证伪引导**: 原 §17 标题缺引导标记(仅 §18 末尾有更正), 读者看完 §17 可能照着做; 新增标题前置引导块, 指明"跳过此节, 直接看 §19"; ③ **新增 §28.1「安全工具特别提醒: -EncodedCommand 与恶意软件混淆手法撞脸」**: 对 §28 的反向补充——开源防御性安全工具用 `-EncodedCommand` 会与银狐/Gh0st 的混淆手法撞脸(沙箱/EDR 警觉+分析师误判+云信誉权重高), 建议改用独立 .ps1 + `-File` 调用; 反向教训来源: 2026-08-25 对银狐样本 `install_h8.0.10.exe` 逆向, 样本第3层载荷正是 20字节循环XOR加密的 PowerShell 命令; ④ 脱敏: 本条不承载机器路径/签名/密钥。
- **v1.67.0 (2026-08-24)**:**新增「发布自动化 + 文本替换定界 + GUI 单实例」实战(v2.15.50)**:① **文本替换定界**: find 定位同名子串会误删大段代码, 用邻近代码注释/函数头作边界 + 替换后立即编译 + 打印 span; ② **版本正则用身份锚点**(AppTitle), 勿用裸正则(命中历史注释); ③ **发布脚本幂等**: 校验只查目标版本存在, 勿要求旧版=0; ④ **GUI 单实例**: 命名互斥+FindWindow 类名激活已有窗口后退出, 与看门狗互斥独立; ⑤ 包内文档更新需重打包(zip 覆盖即可, manifest 不含文档 sig 不变); ⑥ 脱敏: 不承载机器路径/签名/密钥。

- **v1.66.0 (2026-08-24)**:**新增「恢复杀毒软件反推全景 + 批量修改脚本中断丢改动」实战(v2.15.40-44)**:① **restoreav 16 阶段反推全景**: Defender策略/客户端、UAC、系统工具禁用、WindowsUpdate、服务(Defender全家+第三方正则)、hosts劫持、MpCmdRun、排除项、服务缺失、自启动缺失、TamperProtection、代理DNS、防火墙(交互确认)、Defender引擎状态、IFEO映像劫持 + 修复前后对比; ② **端到端测试脚本**(破坏|检查|清理, 8项可逆注入+备份还原); ③ **坑**: 批量修改脚本一个 assert 失败中断 -> 写盘未执行 -> 前面修改全丢(导致 undefined 编译错), 应小步修改及时写盘; ④ **版本残留三处**: 进度首行/审计日志/文档头部写死旧版本, 每版 grep 全目录; ⑤ **防误伤**: 防火墙自动恢复改交互确认; ⑥ 脱敏: 不承载机器路径/签名/密钥。

- **v1.65.0 (2026-08-24)**:**新增「目录扫描验签挂起」实战(v2.15.36)**:① 根因: 遍历循环对每个文件调 Get-AuthenticodeSignature 验签, 大文件/云盘占位/畸形PE 会挂起数分钟 => 扫描卡死(实测 3500/14820 停 15 分钟); ② 修复: 验签前置 PE(MZ头)+<=50MB 条件, 白名单(快)优先签名验证(慢), .sys 观察验签同样限大小; 循环内 return=退出整个函数(应 continue); ③ 诊断: 报告进度明细(每500)定位卡点目录+文件类型, GUI 进度面板与实际进度对照区分"真卡"与"窗口黑屏"; ④ 脱敏: 不承载机器路径/签名/密钥。

- **v1.64.0 (2026-08-23)**:**新增「看门狗 PID 复用残留 + exe 双编码版本校验 + 控制台引擎 GUI 进度展示」实战(v2.15.35)**:① **看门狗 PID 复用**: 按 PID 轮询 OpenProcess 检测进程存活, 主进程死后 PID 被复用 => 看门狗永不退出(后台残留同名无窗口 exe); 修复=持有进程句柄 WaitForSingleObject(WAIT_TIMEOUT=0x102 存活/WAIT_OBJECT_0=0 终止), 重启后重新 OpenProcess; 注意 x/sys/windows 常量是 SYNCHRONIZE 不是 PROCESS_SYNCHRONIZE; ② **exe 版本串双编码**: Go 字符串常量在 PE 中为 UTF-8, versioninfo 资源为 UTF-16LE, 校验须两种编码分别搜; versioninfo.json 数字版本与字符串版本("x.y.z.0")都要改, 否则 goversioninfo 警告不匹配; ③ **GUI 进度**: 控制台交互引擎不能整体重定向输出, 折中=阶段边界双写进度文件(UTF-8)+GUI 轮询 WM_SETTEXT 刷新, 黑窗口保留完整交互; ④(教训补)**manifest sig= 行 16 位**: sig= 行存前16位(Go calcSig=hex[:16] 比较), 存 64 位实机必报签名无效; ④ 脱敏: 不承载机器路径/签名/密钥。

- **v1.63.0 (2026-08-23)**:**新增「专杀工具改名链 + 交互三选一 + 工作目录触发杀软」实战(v2.15.34)**:① **改名全链自查**: exe 名/bat 路径引用/bat 文件名(同步改名+引用)/**manifest 条目名必须 RENAME 映射**(只改名不改清单=实机"文件被篡改")/报告前缀/AppTitle/按钮/入口文档/versioninfo, grep 覆盖 UTF-8+UTF-16LE+GBK; 旧文件移备份勿删; ② **交互三选一**: 删除必须先备份(Quarantine 成功才 Remove-Item -LiteralPath), 备份失败绝不删除, 二次确认, 保留跳过选项; ③ **工作目录铁律**: 中间脚本/临时文件一律放工作区(E:\工具\5), 严禁 C 盘用户目录(杀软对含"病毒/木马/专杀/删除/PowerShell注入"字符串的 C 盘脚本疯狂报毒), 清理已污染文件需确认; ④ **manifest 恢复**: 从 zip 备份取完整条目顺序重算(勿丢失); ⑤ 脱敏: 不承载机器路径/签名/密钥。

- **v1.61.0 (2026-08-23)**:**新增「hosts 劫持自检链」实战(v2.15.23)**:① 下载失败自动排障: 连通探测 -> 非管理员 UAC 提权重跑(带 /fix-hosts 标记, 防循环) -> 备份 hosts + 正则移除 360 相关域名重定向行(保留注释/无关行, 原编码 CRLF 写回) -> 重试下载; ② **技巧**: 幂等修复脚本用 -EncodedCommand(base64 UTF-16LE) 嵌入 bat, 避免 cmd 转义地狱; ③ 实测: 副本 hosts REMOVED=2(0.0.0.0 dl.360safe.com / 127.0.0.1 360.cn), 注释与 baidu 行保留, 备份生成; ④ 判断管理员: whoami /groups findstr S-1-16-12288; ⑤ 脱敏: 不承载机器路径/签名/密钥。
- **v1.60.0 (2026-08-23)**:**新增「万能下载器脚本: 便携+动态识别+启动检测+按序降级」实战(v2.15.22)**:① 一键下载并打开第三方工具包(官方压缩包)的独立脚本: %~dp0 便携、下载产物独立文件夹 tools\<工具名>\、动态扫描候选(适配更新/改名)、启动后 tasklist 检测进程、未运行则按顺序尝试下一个入口(主程序->请双击.com->运行不了.exe->引导bat->加强版bat); ② **块内 echo 圆括号坑再复现**(§11 教训): curl 回退行/解压失败行/DRYRUN 行均中招, 修方括号; ③ dir 模式注意文件名前缀(`*运行不了*.exe` 而非 `运行不了*.exe`); ④ curl stderr 进度条污染捕获, 用 >nul 2>&1; ⑤ 支持 SF_360_DRYRUN=1 检测模式供自动化测试; ⑥ 脱敏: 不承载机器路径/签名/密钥。
- **v1.59.0 (2026-08-23)**:**新增「多档交付入口命名 + QUERYENDSESSION 强制关机边界」实战(v2.15.21)**:① 档2/档3 交付文件名改为用户可理解入口(如果主程序打不开点我.exe/.com), 改名前全仓 grep 确认无硬编码引用, exe 内 os.Executable() 自适应; ② **强制关机边界**: shutdown /s /f 时 QUERYENDSESSION 带 CRITICAL 标志, 返回 FALSE 不可靠 —— 用户态无法阻止强制关机(需驱动); 非强制关闭可被阻止; ③ **诊断法**: WndProc 收到 QUERYENDSESSION 写 sf_sg_query.log(时间+wParam+返回值), 实机测试后可确认消息是否到达; ④ **脱敏**: 不承载机器路径/签名/密钥。
- **v1.58.0 (2026-08-23)**:**新增「Add-Type C# 两连坑: ref 实参未初始化 CS0165 / DllImport 模块写错 kernel32 vs user32」实战(v2.15.20)**:① **实机日志**: `层3 初始化失败 ... 编译错误` —— 隐藏窗口从未创建, WM_QUERYENDSESSION 从未生效(前版拦截失败的真因); ② **坑1**: `MSG m; GetMessageW(ref m,...)` CS0165(实参需显式初始化), 修 `new MSG()`; ③ **坑2**: `GetModuleHandleW` DllImport 写在 user32.dll(实际 kernel32), 编译过运行崩(入口点找不到); ④ **诊断法**: 提取 C# 用 `Add-Type -ErrorAction Stop` 单测定位; ⑤ **命名规范**: 检测工具对外名称统一「银狐检测工具 (SilverFox Detector)」, 不出现"银狐木马 (SilverFox)"式自报名称(易被误认为病毒本体); ⑥ **脱敏**: 不承载机器路径/签名/密钥。
- **v1.57.0 (2026-08-23)**:**新增「拦截系统关机: 杀 shutdown.exe 无效, 须隐藏窗口+WM_QUERYENDSESSION=FALSE」实战(v2.15.19)**:① **实机证实**: 层1 杀 shutdown.exe 并记录"已阻止", 但系统仍关机(请求已提交 LSM, 杀进程不撤销); ② **正确机制**: WM_QUERYENDSESSION 广播至顶层窗口, 返回 FALSE 即拒绝关机/注销/重启; console 无窗口收不到消息; ③ **实现**: 隐藏窗口(CreateWindowExW style=0)+独立线程 GetMessage 循环+WndProc 对 0x11 返回 FALSE+ShutdownBlockReasonCreate 提示+Stop 时 PostThreadMessage(WM_QUIT)+Destroy; ④ **踩坑**: Register-CimIndicationEvent 对 Win32_ProcessStartTrace 返回 null -> Register-ObjectEvent -InputObject 报空值, 换 Register-WmiEvent -Action; ⑤ **脱敏**: 不承载机器路径/签名/密钥。
- **v1.56.0 (2026-08-23)**:**新增「PowerShell 踩坑三连: TrimEnd 字符串转 char / Register-CimIndicationEvent 参数集互斥 / chcp 65001 与 GBK 脚本混用乱码」实战(v2.15.18)**:① TrimEnd `'\\'` 双反斜杠字符串转 char 失败(单引号中反斜杠非转义符), 白名单目录前缀匹配处崩; ② WMI 订阅 `-ClassName`+`-Query` 同用报"无法解析参数集名称"(参数集互斥, 删 -ClassName); ③ chcp 65001 后 bat 自身 GBK echo 乱码且与引擎 UTF8 输出混用, 统一为 936(bat 不 chcp + 引擎 Windows_NT 下 GetEncoding(936)); ④ 收尾提示: PowerShell 重定向输出与子进程编码均受控制台代码页影响; ⑤ 脱敏: 不承载机器路径/签名/密钥。
- **v1.55.0 (2026-08-23)**:**新增「bat 提权调用 Start-Process -ArgumentList 双坑」实战(v2.15.17)**:① **坑1**: `-Command "字符串"` 模式下 $args 恒为 null(仅 scriptblock 尾参形式才传参), 原写法规避了 v2.15.3 的合并参数问题却引入 null 崩溃; ② **坑2**: Start-Process -ArgumentList **不接受空集合 @()**(报"为 Null、为空或包含 Null 元素"), 空参场景必须省略 -ArgumentList 双分支; ③ **对策**: env 变量传 %* + -split 数组化 + Count>0 双分支(当前调用面参数无空格); ④ **验证**: 本地等价双分支测试(带参 CNT=2 / 空参 OK)通过后交付, 真 UAC 由用户实测; ⑤ **脱敏**: 本条不承载机器路径/签名/密钥。
- **v1.54.1 (2026-08-23)**:**v2.15.16 发布同步(双重 BOM 修复正式版)**: ① 修复应用: 引擎/UI ps1 单 BOM + 引擎 banner 版本同步 v1.60 + bat/UI/Go 头注释标注 v2.15.16; exe 重编译 buildTag `p8-20260823-bom-fix`; ② manifest 重签(3 文件哈希, signed 随发布日更新, 33/33 校验通过); ③ 教训复述: 回写带 BOM 文件必须 `decode('utf-8-sig')` 剥 BOM 且写回只前置一次(§21)。
- **v1.54.0 (2026-08-23)**:**新增「双重 BOM 写入导致 PS 5.1 静默拒绝执行」实战(v2.15.15 BOM 修复)**:① **症状**: 升级脚本回写后的引擎 ps1 **无输出退出码 1**; 语法解析通过、后期探针不显示、但文件最前面加的第一行 Write-Host 正常显示; ② **根因**: 回写时 `"\ufeff" + text` 前置 BOM + `decode('utf-8')` 未剥原 BOM → **双重 BOM**(`EF BB BF EF BB BF`), PS 5.1 剥一个后剩余 `\ufeff` 在首行注释前 → 脚本静默拒绝执行; ③ **对策铁律**: 有 BOM 文件用 `decode('utf-8-sig')` 剥 BOM 再改; BOM 只前置一次; 写完必查 `read(6).hex() != 'efbbbfefbbbf'`; "第一行探针"二分法定位加载层问题; ④ **验证**: 单 BOM 修复后引擎正常 banner+报告生成; ⑤ **脱敏**: 本条不承载机器路径/签名/密钥。
- **v1.53.0 (2026-08-22)**:**新增「WindowsApps 应用执行别名 pwsh 在 RunAs/-File 长中文路径下返回 9020」实战(v2.15.15) + 引擎 v1.60 降误报 + 二进制升 v2.15.15**:① **9020 根因**: bat 启动器命中 `WindowsApps\pwsh.exe` 应用执行别名, 该别名在 UAC/RunAs/长中文路径下执行 `-File` 报 9020(真实安装路径正常); "Test-Path 命中即用"是元凶; ② **启动器 v1.57 修复(四步)**: 真实安装路径优先(64/32位 PS7 + System32/SysWOW64 5.1)逐候选 `-Command "exit 0"` 验证 + PATH 搜索排除 WindowsApps + 别名仅兜底且控制台/日志双告警 + 引擎调用 stderr 捕获; ③ **引擎 v1.60 降误报**: 签名安全港 Test-SafeHarbor(Program Files + 有效 Authenticode 签名豁免启发式噪音, 恶意哈希命中仍隔离) + 弱信号权重下调(RANDOM_NAME_EXE 5/PERSIST_APPDATA 5/WIN_HIDDEN 5/IEX_GENERIC 5/BASE64_GENERIC 2/HIDDEN_PE 15) + 启动环境日志 sf_debug.log(版本/路径/权限/参数, 便于远程诊断 9020); ④ **白名单扩展**: whitelist 追加 28 签名者 + 17 目录(百度/网易/搜狗/爱奇艺/荣耀/华硕/戴尔/惠普/联想/Steam/Epic/Riot/Ubisoft/JetBrains/Docker/VideoLAN); ⑤ **manifest 重签**: 4 个变更文件重算哈希, 条目顺序与签名算法不变, 载荷保持 signed= 整行(Go 层与 PS 层一致); ⑥ **诚实边界**: 安全港只豁免启发式噪音, 不豁免确证 IoC; ⑦ **脱敏**: 本条不承载机器路径/签名/密钥。
- **v1.52.0 (2026-08-22)**:**更正 §17/§18 的"360 hook"错误方向 + 新增「真凶是自带的自保护缓解策略(非 360)」实战(v2.15.14) + 二进制升 v2.15.14**:① **关键反证**: 用户对 v2.15.13 实测, 已完全退出 360 仍报 `LoadCursorW 失败`/`RegisterClassExW 失败(错误 1114)`, 且日志首行是新 build → 证伪"360 hook"假设; ② **真正根因(代码层确定性)**: `hardenProcess()`→`applyMitigation(CurrentProcess())` 给**加载 user32 的 GUI 主进程本身**施加了 `procMitSignature=0x1|0x2`(必须 Microsoft 且必须 Store 签名, 逻辑矛盾, 拦截 user32)与 `procMitDynamicCode`(ACG), 二者在 DLL 加载期拦截 `user32.dll`, `LoadLibrary` 返回 1114; 自保护先于 `winMain` 运行故 GUI 启动即锁死; 管理员/非管理员都执行 `hardenProcess` 故都挂; ③ **修复两道保险**: `applyMitigation` 仅保留 `procMitImageLoad(PreferSystem32Images, 不拦截加载)`, 移除签名/动态代码/严格句柄三项; 新增 `preloadGUIBasics()` 在 `protectSelfDACL()` 前用 `LoadLibrary` 映射 user32/gdi32(不释放, 保留); ④ **验证**: Wine `主窗口创建成功`; Wine 不强制缓解策略无法复现 1114, 但根因为确定性修复; ⑤ **教训固化为铁律**: "已退出安全软件仍 1114 → 先回查自身进程(自保护/策略/token), 不追加外部假设"; "给自身进程施加 SignaturePolicy/DynamicCodePolicy 前须确认不影响系统 GUI DLL, 与组合签名是自杀写法"; "进程缓解策略只施加于运行非受信代码的子进程"; ⑥ **诚实边界**: 若实机 `预加载探针(自保护前): user32.dll 加载失败` 也出现, 才是真实第三方内核驱动拦截, 需干净启动/卸载驱动验证; ⑦ **脱敏**: 本条不承载机器路径/签名/密钥。
- **v1.51.0 (2026-08-22)**:**新增「LoadLibraryW 也被 hook → 改用 GetModuleHandleEx 取已加载句柄」实战(v2.15.13) + 二进制升 v2.15.13**:① **症状**: v2.15.12 在真实 360 环境下仍报 `LoadCursorW 失败` / `RegisterClassExW 失败(错误 1114)`, Wine 正常; ② **根因再深入**: 360 主动防御对 `user32.dll`/`gdi32.dll` 的**任何显式加载**(`LoadLibraryExW`/`LoadLibraryW`)都返回 1114; ③ **最终绕过**: 本地 fork `golang.org/x/sys/windows`, 在 `LazyDLL.Load()` 中对 `user32.dll`/`gdi32.dll` 优先使用 `GetModuleHandleEx(0, name, &h)` 直接获取 OS 已隐式加载的模块句柄, 完全不调用 `LoadLibrary*`; 失败再回退 `LoadLibraryW`→`loadLibraryEx`; ④ **保留此前加固**: v2.15.11 的 `safeCall`/`removeGuardFlag`、v2.15.12 的 `LoadLibraryW` fallback 全部保留; ⑤ **验证**: Wine 回归 `主窗口创建成功`; 真实 360 环境待测; ⑥ **诚实边界**: 若 360 对 `GetModuleHandleEx` 也做限制或进程被沙箱隔离, 应用层彻底无解, 只能在 360 中放行本程序; ⑦ **脱敏**: 本条不承载机器路径/签名/密钥。
- **v1.50.0 (2026-08-22)**:**新增「360 主动防御 hook LoadLibraryExW → user32 加载 1114」实战(v2.15.12) + 二进制升 v2.15.12**:① **症状**: v2.15.11 后崩溃循环已掐断(看门狗"主进程正常退出"), 但仍无界面, 日志反复报 `LoadCursorW 失败` / `RegisterClassExW 失败: user32.dll 可能在本机被安全软件...拦截(错误 1114)`; 用户已将目录加入 360 开发者模式信任列表, 问题依旧; ② **根因**: Windows GUI 子系统虽已隐式加载 `user32.dll`, 但 Go `x/sys/windows` 的 `LazyProc.Call` 第一次调用时会显式走 `LoadLibraryExW("user32.dll", LOAD_LIBRARY_SEARCH_SYSTEM32)` 获取模块句柄, **360 主动防御在驱动层 hook 该显式加载路径并返回 1114**; "开发者模式"仅减少弹窗/信任编译目录, 不等于关闭主动防御; ③ **绕过(实验性)**: 本地 fork `golang.org/x/sys/windows`(`xsys/`), 在 `LazyDLL.Load()` 中对 `user32.dll`/`gdi32.dll` 先尝试 `LoadLibraryW`(`LoadDLL`), 失败再回退 `loadLibraryEx`(保留安全性), `go.mod` 加 `replace golang.org/x/sys => ./xsys`; ④ **保留 §16 所有加固**: `winMain`/`showFatal` 仍走 `safeCall`, 致命错误仍 `removeGuardFlag()` 掐断循环; ⑤ **验证**: Wine 回归 `主窗口创建成功`; 真实 360 环境待测, 若仍失败说明 `LoadLibraryW` 也被 hook, 属安全软件层彻底拦截, 只能按排障清单进一步放行; ⑥ **诚实边界**: `user32.dll` 是 Windows GUI 必需 DLL, 应用层只能做到不崩溃/尝试绕过/精确定位/给出排障清单, 无法强制让被驱动层拦截的 DLL 加载成功; ⑦ **脱敏**: 本条不承载机器路径/签名/密钥。
- **v1.49.0 (2026-08-22)**:**新增「必加载 DLL(user32)启动期被拦截 → 1114 + 看门狗无限重启」实战(v2.15.11) + 二进制升 v2.15.11**:① **症状**: v2.15.10 仍无界面, 日志首行已是新 build(跑的是新 exe), 但 `winMain` 首个 `user32` 调用(`LoadCursorW`/`RegisterClassExW`, `main.go:1845`)裸 `LazyProc.Call` 直接 panic, FATAL `DLL initialization routine failed`(1114), 看门狗反复重启; ② **根因两层**: (a) 本机 EDR/杀毒在启动期拦截 `user32.dll` 加载→`LoadLibrary` 1114→`LazyProc.Call` panic(§14 同机制, 但这次是**必加载** DLL); (b) `main` 顶层 `recover` 里调 `showFatal` 又用 `user32`(MessageBoxW)→二次 panic 无兜底→硬崩; 看门狗见存活标记未移除→判"被 kill"→重启, 且每次重启换新看门狗使 `selfGuardMaxKills=5` 失效→**无限重启循环**; ③ **对策四刀**: `winMain` 全部 user32 启动调用改 `safeCall`(失败返错误不 panic); `safeCall` 错误定位过程名+1114; `showFatal`/`msgBoxInfo`/`msgBoxQuestion` 改 `safeCall`(防二次 panic); 致命 GUI 错误路径调 `removeGuardFlag()` 让看门狗判"正常退出"→**掐断重启循环**, 并写排查建议清单(管理员/杀软排除/改名/`sfc`); ④ **验证**: Wine 正常机 `主窗口创建成功`; 模拟 user32 失败→看门狗"自动重启"次数=0; ⑤ **诚实边界**: 1114 属 OS/安全软件层, 应用层无法强载被拦 user32, 修复只解决崩溃+循环+诊断, GUI 出现取决于环境层拦截解除; ⑥ **脱敏**: 本条不承载机器/路径/签名。
- **v1.48.0 (2026-08-22)**:**新增「启动期加载非必需 DLL 拖垮 GUI + 部署版本不可辨识」实战(v2.15.10) + 强化版本号规则**:① **崩溃真因**: `winMain` 启动期调 `CoInitializeEx`(ole32)/`InitCommonControlsEx`(comctl32) 这两个非必需 DLL, 其 DllMain 被 EDR/AV/SxS 阻断即 1114 panic 拖垮 GUI; 对策=启动期彻底移除, 仅文件夹对话框按需 `CoInitializeEx`(safeCall 兜底); ② **部署不可辨识**: 旧日志只打 `启动 v2.15.9`, 用户无法判断双击的是哪版 exe(看门狗可能锁旧 exe 致覆盖失败), 故二进制加 `buildTag` 打首行 + 标题版本 +0.0.1, FATAL 增加 `runtime.Stack` 写堆栈; ③ **版本号规则(用户要求, 强制)**: 新增更新规则第7条 + 自查清单版本项补强——每次修改 skill 必须 bump `version`/`updated`/更新日志, 交付二进制一并改时也须同步 bump 内部版本; ④ **脱敏**: 本条不承载机器/路径/签名。
- **v1.47.0 (2026-08-22)**:**新增「lazyDLL 懒加载失败是 panic 不是 error → 可选 DLL 调用来就崩」实战(对应 SilverFox Detector v2.15.9)**:① **症状**: Go Windows GUI 程序真机双击直接崩溃(FATAL: `DLL initialization routine failed`=1114), 看门狗无限重启, 但 Wine 验证窗口正常; ② **根因**: `golang.org/x/sys/windows` 的 `LazyProc.Call` 在 `LoadLibrary` 失败时(可选 DLL 的 DllMain 返回 FALSE, 如 EDR/AV 拦截/SxS 损坏)直接 **panic 而非返回 error**, 旧代码 `if ret==0` 只防"函数返回 FALSE"防不住 panic → 整进程崩; ③ **Wine 假正常**: Wine 下可选 DLL 能正常 LoadLibrary, 与 §13(UAC 降级)同源, 纯 `wine` 复现不出; ④ **对策**: 统一 `safeCall`(defer recover 把 panic 转 ok=false)包裹所有可选 DLL 懒调用(ole32/comctl32/wintrust/crypt32/comdlg32/shell32 及 ole32 的 CoTaskMemFree/OleInitialize), 失败即 logf 点名+继续(主窗口照显示, 仅该功能降级), user32/kernel32 等必加载 DLL 无需包; ⑤ **脱敏**: 本条不承载机器/路径/签名。
- **v1.46.2 (2026-08-22)**:**新增「修改后自查清单(强制)」, 固化到 §0**:① **更新规则第6条**——每次写完/改完必须对照自查清单核验, 未全过不自认完成; ② **自查清单**含脱敏 grep 复查(带参考命令)、版本与日志同步(防"加条目忘改 version"漂移)、格式完好、副本 diff 一致、内容自洽(对策须有日志实证, 不写未验证断言); ③ **动机**: 此前出现 v1.46.0 条目已加但 frontmatter version 仍 1.45.0 的漂移, 以及脱敏改一半残留真实 `sig`/路径, 故将"修改后自查"上升为强制动作。
- **v1.46.1 (2026-08-22)**:**强化「脱敏与隐私协议」, 并补脱敏历史遗留**:① **新增更新规则第5条**——每次落盘前必须过「脱敏核查清单」, 历史条目发现遗留敏感信息也一并脱敏; ② **脱敏核查清单**固化到 §0(云签名链接/密钥/本机路径含 `/workspace/`/具体 sig/机器名内网IP/个人身份 逐项命中即改删, 已公开项目名版本号常量允许保留); ③ **脱敏历史遗漏**: v1.45.0⑩ 的 `/workspace/...` 交付路径改为 `<交付目录>/...`(泛指交付位置); v1.44.0⑦ 的真实 `sig=...`(具体 build 指纹) 改为"签名校验通过(64 位 salt 混淆级, sig 已脱敏)"; ④ **frontmatter version** 由 1.45.0 补正为 1.46.1(此前 v1.46.0 实战条目已加但版本号未同步)。
- **v1.46.0 (2026-08-22)**:**新增「提权子实例(--elevated-run)跳过 GUI 导致双击无界面」实战(对应 SilverFox Detector v2.15.9)**:① **症状**: 档2/档3 程序双击后"没有界面"(GUI 主窗口不出现); ② **根因**: `main()` 对档2/3 启动即 `ensureElevatedOrRestartTier()` 弹 UAC, 接受后 `ShellExecute("runas")` 以 `--elevated-run` 重启自身; 而 `--elevated-run` 分支只做自保 + `runSilverFox(mode)` 直跑检测引擎, **从不调用 `winMain()`** —— 故 GUI 主窗口永远不创建, 用户只看到一个检测控制台(或一闪而过), 误以为"没界面"; ③ **判定铁律**: `wine` 下 `ShellExecute("runas")` 必然失败→优雅降级走到 `winMain`→窗口正常, 所以 Wine 验证会"假装正常", 必须用 `wine xxx.exe --elevated-run` 直接模拟"接受 UAC 后的提权子实例"才能复现"无界面"; ④ **修复**: `--elevated-run` 分支中, 若 `mode==""`(双击启动提权、用户尚未选模式)则改调 `winMain()` 展示 GUI, 仅当带了具体 mode(从 GUI 勾"以管理员身份运行"并点具体按钮触发)才直跑引擎; ⑤ **与活文档去标识化一致**: 仅沉淀技术根因与对策, 不含具体机器/路径/签名链接。
- **v1.45.0 (2026-08-22)**:**新增「三档用户态自保护 + 急救箱」实战(对应 SilverFox Detector v2.15.9)**:① **需求本质**: 单一 exe 走不通(权限/反冻强度不同), 改**同源三二进制**——`SilverFox.exe`(档1 纯用户, 不弹UAC)、`SilverFox.Heartbeat.exe`(档2 双向心跳)、`SilverFox.Hard.com`(档3 硬钩子+高权限守护, 急救箱, 编译为 .com 以模仿系统急救箱紧急态); ② **单源三档实现**: `var buildTierStr = "1"` + `parseBuildTier()`, 编译期 `-ldflags "-X main.buildTierStr=N"` 注入档位(注意 `-X` 只对 `string` 变量生效, 直接注入 `int` 报错); `tierSuffix()` 拼标题; ③ **档1(纯用户, 无UAC)**: 仅既有看门狗自愈 + 文件完整性自检, 高权限扫描仍留在主 GUI 内按需触发; ④ **档2(双向心跳, 需UAC)**: `startBidirectionalHeartbeat()` 主进程按 `hbPollSec=1` 写 `sf_hb_main_*.tmp`(`GetTickCount64` 时间戳), 看门狗 `--tier 2` 写 `sf_hb_watch_*.tmp`; 选**文件心跳而非共享内存**——跨 IL(主进程 Medium/Low vs 守护 High/SYSTEM)文件可读、共享内存受 IL 隔离读不到; ⑤ **档3(硬钩子 + 高权限守护, 需UAC, 急救箱)**: (a)**纯 Go 内联钩子**(`selfguard_hook.go` 新文件): `getNtdllExport` 取 `NtTerminateProcess`/`NtSuspendProcess`/`NtSuspendThread` 地址 + `VirtualProtect` 改 RWX + 头 12 字节写 `E9 rel32` 跳 Go 处理函数 + `VirtualAlloc(PAGE_EXECUTE_READWRITE)` 建 trampoline(备份原头 + 跳回 `origAddr+12`) + `FlushInstructionCache`; 处理函数对**自身**目标(`isSelfProcessHandle` 用 `-1` 伪句柄/`GetProcessId`、`isSelfThreadHandle` 用 `GetThreadId`/`GetProcessIdOfThread`)返回 `STATUS_ACCESS_DENIED(0xC0000022)`, 否则走 trampoline 透传; (b)**高权限守护** `spawnGuardian()` 经 `ShellExecute("runas")` 拉 `--guardian <mainpid> --tier 3`, 守护写 `sf_hb_guard_*.tmp`、探测主进程心跳新鲜度、对被挂起线程 `ResumeThread`、主失联则带 `--guarded` 重启(10s 冷却 `lastRestart`); (c)**可选 LocalSystem 服务** `toggleGuardianService()`: GUI 按钮(`ID_BTN_INSTALL_SVC=1050`, 仅档3)确认后 `sc create/delete SilverFoxGuardian binPath=... start= auto`; ⑥ **防爆递归/分叉炸弹**: 守护重启的主进程带 `--guarded` 不再 spawn 新守护; `guard-flag` 正常退出检查; 心跳文件新鲜度(> `hbTimeoutSec=5`)作权威存活信号, 不依赖硬编码 PID 的 `OpenProcess`; ⑦ **落坑修正**: `windows.ShellExecute` 返回值是 `error`(单值)非 `(ret,err)`, 旧两值写法编译错; `go vet` 对 `unsafe.Pointer`(钩子写入/trampoline/剪贴板/ETW)有 6 处已知误报(安全); ⑧ **cgo C 钩子备选**: 用户要求两种方法都有, 一个不行换另一个, 但沙箱无 `mingw-w64`(`x86_64-w64-mingw32-gcc` 缺失), cgo 跨平台 Windows 编译不可行, 纯 Go trampoline 作唯一落地方案, cgo 在文档中记为设计备选; ⑨ **Wine 验证**: 三档均启动 GUI、钩子安装成功(Wine 支持 `VirtualProtect`/ntdll 布局)、守护拉起、完整性通过、无 panic; UAC 在 Wine 下 `recover()` 优雅降级; ⑩ **交付**: `SilverFox_Detector_Win_GUI_v2.15.9.zip`(三文件 + 完整 `legacy/` + README/versioninfo, 排除日志/`sf_guard.flag`/`sf_hb_*.tmp`) + `<交付目录>/三档自保护与急救箱说明_v2.15.9.md`。
- **v1.44.0 (2026-08-22)**:**新增「EDR-Freeze 反冻防御(用户态纵深) + 全源码漏洞审计」实战(对应 SilverFox Detector v2.15.8)**:① **攻击面**: 攻击者滥用 WER(`WerFaultSecure.exe` 调 `MiniDumpWriteDump`)在转储竞态窗口用 `SuspendThread`/`NtSuspendProcess` 把安全软件线程全挂起→永久"休眠", 绕过看门狗自愈; 这是**利用系统合法设计(非漏洞)**; ② **用户态 vs 内核态边界(必须说清)**: 真正堵死需 `ObRegisterCallbacks`/`NtSuspendThread` 内核回调(需驱动+微软交叉签名); Ring3 无法从根上禁止 SeDebug 持有者再次挂起线程——反冻是"反复拉起"的猫鼠博弈, 能抬高成本/防"一次冻结永久失联", 但不提供内核级不可绕过保证; ③ **用户态三件套(best-effort, 全失败仅日志)**: (a) **心跳反冻** `OpenThread`+`NtQueryInformationThread(ThreadBasicInformation)` 读 `SuspendCount`, >0 即 `ResumeThread` 恢复 + `writeGuardFlag()` 刷新存活标记(关键: 让看门狗区分"被冻结应等待恢复" vs "被杀应重启", 避免冻结期被误重启); (b) **线程挂起监控** `CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD)` 枚举本进程全部线程, 对 `SuspendCount>0` 的线程 `ResumeThread`; (c) **best-effort WER 自禁用** `WerSetFlags(WER_FAULT_REPORTING_NO_HEAP_DUMP=0x4)` 关本进程 WER 堆转储, 缩小可被 MiniDump 的面(Wine 缺该 API 时 `recover()` 兜底跳过); ④ **`threadBasicInfo` 结构体**: 按 ntdll x64 `THREAD_BASIC_INFORMATION` ABI 对齐(`unsafe.Sizeof=64`), `NtQueryInformationThread` 只读至 `sizeof`, `SuspendCount` 偏移正确; ⑤ **漏洞审计修了一个真注入**: 主检测 bat 原 `powershell -Command "... %* ..."` 把 `%*` 原始参数拼进命令字符串 = 命令行注入面(右键 `%1`/恶意 .lnk 可投毒); 改为 `powershell -File engine.ps1 %* /lang=zh`(`-File` 模式参数按字面量传入, 不解析为 PS 代码, 功能等价且消除注入); ⑥ **其余审计通过**: Go exe 所有子进程调用均为参数数组(`exec.Command`/`taskkill /PID <int>`); 注册表右键命令已引号包裹; ps1 的 `Remove-Item`/`Move-Item` Path 为内部变量非用户字符串拼接; `mshta vbscript:MsgBox` 的 `$tipEsc` 已双转义 `'`/`"`; 联网 IOC 仅取自硬编码可信源(非注入); 小工具 `subprocess.Popen(["notepad",path])` 参数数组; ⑦ **遗留建议(非阻塞)**: IOC 源经 HTTPS 从公开 GitHub 拉取**无签名/哈希钉选**(仓库被入侵可投毒 IOC, 影响是误报非 RCE); integrity.manifest 签名是 salt 混淆级(64 位), 建议升级外部可信签名; ⑧ **Wine 验证**: 启动日志确认 `反冻[EDR-Freeze]: 已启动` + `完整性自检通过`(新 manifest 重签后签名校验通过(64 位 salt 混淆级, 具体 sig 已脱敏) + WER 缺失优雅降级, 无 panic。
- **v1.43.0 (2026-08-22)**:**新增「进程与线程监控(用户态 A+B + 先识别再反制)」实战(对应 SilverFox Detector v2.15.7)**:① **需求本质**: 监视所有进程创建/结束, 发现可疑进程试图结束自己就反制; 但**不能一见可疑就杀**——必须先判定"是什么程序", 否则误伤正常软件(更新器/安装包/任务管理器); ② **A+B 双源**: A=Toolhelp 轮询快照(`CreateToolhelp32Snapshot`+`Process32First/Next`, 每~1.5s 差集出新/退进程, 轻量无需特权, 作主检测源); B=ETW 实时(`OpenTrace`+`EnableTraceEx2` 订阅 `Microsoft-Windows-Kernel-Process`+`ProcessTrace`, 延迟远低于轮询, 但**实时会话需管理员且 Wine 无内核提供者** → best-effort, 起不来就 `recover` 静默回退 A); ③ **身份判定(反制前必做)**: 采集 镜像路径/父进程/代码签名(`WinVerifyTrust`+`CryptQueryObject` 分 Microsoft/有效/无效/未签名)/路径启发(是否 System32 vs temp/appdata)/冒充(系统进程名却不在 System32)/父链(父是浏览器/Office/脚本宿主却拉起未签名 exe); 仅"签名缺失/无效 + 路径/冒充/父链异常"组合命中才判可疑; ④ **终止型工具白名单**: taskkill/powershell/ProcessHacker/PCHunter/taskmgr 等 —— **仅当该工具本身非 Microsoft/有效签名才判威胁**, 签名正常的系统工具(如微软 taskmgr)不误杀; ⑤ **反制**: 对"终止型+未签名"进程主动 `TerminateProcess`(自身 High IL 对低 IL 目标有权), best-effort, IL 不足则失败忽略; 自身被终止由既有看门狗自愈; ⑥ **Go 落地坑**: x/sys/windows v0.15.0 **未封装** `CreateToolhelp32Snapshot`/`Process32*`/`OpenTrace`/`ProcessTrace`/`EnableTraceEx2`, 需 `NewProc` 动态加载并手搓结构体; `WINTRUST_DATA` 必须严格对齐 64 位布局(共 72 字节, 否则 `WinVerifyTrust` 越界读→判定失真/崩溃); `syscall.NewCallback` 注册 ETW 回调转 `uintptr` 会触发 go vet 的 unsafe.Pointer 误报(安全, 已知); ⑦ **性能**: 快照阶段只记短名, 全路径 `OpenProcess` 仅对新进程惰性查询, 避免每轮对全部进程 OpenProcess; ⑧ **Wine 验证**: 启动日志确认监控已启动, ETW 回退正常, 无 panic; ⑨ **沉淀位置**: 详见 §5「进程与线程监控(A+B + 先识别再反制)」条。
- **v1.42.0 (2026-08-22)**:**新增「PPL 降级近似自保护」实战(对应 SilverFox Detector v2.15.6)**:① **前提澄清**: 用户想要真 PPL(`PsProtectedSignerAntimalware`), 但**真 PPL 需微软反恶意软件 ELAM 认证签名**, 普通 Authenticode 证书无法让内核以 Antimalware signer 级别启动进程(`NtSetInformationProcess(ProcessProtectionInformation)` / `PROC_THREAD_ATTRIBUTE_PROTECTION_LEVEL` 会被拒); 纯用户态 exe 走不了真 PPL; ② **降级近似(三件套, 无需特殊证书, 普通进程即生效)**: (a) **进程缓解策略** `SetProcessMitigationPolicy`(kernel32, x/sys/windows v0.15.0 未封装需 `NewProc` 动态加载) / 对子进程用 `NtSetInformationProcess`(同名 class 值) —— `ProcessDynamicCodePolicy`(禁动态代码, 防 shellcode/内存注入) + `ProcessSignaturePolicy`(仅微软/Store 签名 DLL, 防 DLL 侧载) + `ProcessImageLoadPolicy`(禁远程/低IL镜像) + `ProcessStrictHandleCheckPolicy`; (b) **MIC 提升** `SetTokenInformation(TokenIntegrityLevel)` 把自身提到 **High(S-1-16-0x3000)**, 低 IL 进程无法 OpenProcess(取 High 而非 System 以免 GUI/COM 异常); (c) **去特权** `AdjustTokenPrivileges` 禁用自身 `SeDebugPrivilege`(降低 Token 被劫持价值); ③ **落地坑**: `GetCurrentProcessToken()` 默认仅 `TOKEN_QUERY`, 设 IL 需 `TOKEN_ADJUST_DEFAULT`、调特权需 `TOKEN_ADJUST_PRIVILEGES` —— **必须 `OpenProcessToken` 显式打开带对应访问权的 Token**, 否则静默失败; `TOKEN_MANDATORY_LABEL` 结构体 x/sys 未定义, 本地定义 `{*SID; DWORD}` 即可; IL RID 常量(`SECURITY_MANDATORY_HIGH_RID=0x3000`)该包未导出, 需自定义; ④ **覆盖引擎子进程**: 对 `cmd.Start()` 后的子进程经 `NtSetInformationProcess(子句柄, ...)` 施加同样的缓解策略(SetProcessMitigationPolicy 仅对自身有效, 子进程必须用 Nt 版); ⑤ **与真 PPL 差距(务必说清)**: 这些是 Ring3 措施, 拥有 SeDebugPrivilege 的管理员理论上仍可绕过(动态代码策略对跨进程写入拦截不如 PPL 彻底), 真 PPL 是 Ring0 内核强制; 降级近似显著抬高攻击成本、挡普通恶意软件, 但非"管理员也无法操作"; ⑥ **Wine 验证**: 启动日志确认 `完整性级别已提升至 High` + `已禁用 SeDebugPrivilege`, 引擎子进程日志确认 `已施加缓解策略`, 未破坏 GUI; ⑦ **沉淀位置**: 详见 §5「PPL 降级近似自保护(用户态三件套)」条。
- **v1.41.0 (2026-08-21)**:**新增「UAC runas 与 Job Object 清理互斥」实战坑(对应 SilverFox Detector v2.15.5 彻底修复提权模式进程残留)**:① **根因**: v2.15.4 用 `ShellExecute("runas")` 提权**单个 cmd.exe 子进程**去跑引擎; 但被 runas 提权的子进程会**脱离父进程 Job Object**(等同 breakaway), 父 exe 退出时 job 管不到它, 只能 best-effort `taskkill`, 而提权引擎权限≥父, 父往往无权结束 → 清理必败, 残留; ② **彻底解法**: 改为用 runas **重启整个 exe 自身**并带内部标记 `--elevated-run <mode>`, 新实例以管理员令牌运行, 其 spawn 的引擎留在**新实例自己的 Job Object** 内, 新实例退出时 OS 自动回收整棵引擎树, 无残留; ③ **配套铁律**: runas 重启的实例必须**阻塞存活到引擎结束再退出**(`waitForEngineTree` 轮询已记录 PID), 否则 job 句柄一关触发 KillOnJobClose 把刚启动的引擎也杀了; ④ **标记风格**: 用双杠 `--elevated-run`(与 `--watchdog`/`--cli` 一致), Go `os.Args` 经 `CommandLineToArgvW` 原样保留, 单杠 `/elevated-run` 会匹配失败; 空模式兜底为 `""` 防 `i+1` 越界; ⑤ **Wine 实测验证**(同日本轮): `wine SilverFoxDetector.exe --elevated-run /diag` 正确命中分支(mode="/diag")、`runSilverFox` 启动 bat、`引擎进程已加入退出清理 Job`、`waitForEngineTree` 正确阻塞; `--elevated-run`(空模式)也正确兜底为 `""`; ⑥ **提权子实例被强杀后的自愈**: 其看门狗重启 exe 时**不带参数**→ 回到普通 GUI 主模式(非 `--elevated-run`), 即自愈后需用户再次点检测才会重新提权 —— 有意为之, 避免自愈循环自动弹 UAC; ⑦ **沉淀位置**: 详见 §5「Job Object 进程树清理 + UAC runas 的互斥」条。
- **v1.40.0 (2026-08-21)**:**新增「子工具模式跳过 PowerShell 查找」坑(对应 SilverFox Detector v2.15.4 修复 `/diag` 误报 PowerShell not found)**:① **根因**: bat 入口先做参数解析, 若 `%~1` 是子工具参数(`/diag`/`/restore`...), 会 `goto TOOL_MODE` 直达各子流程, **完全跳过主流程 STEP2 的 PowerShell 查找**, 导致 `PS_EXE` 未赋值; 而 `:TOOL_DIAG` 用 `if defined PS_EXE` 判断 → 误报 `[FAIL] PowerShell not found`, 即便引擎本身存在; ② **通用规律**: bat 的多入口(双击 GUI_MODE / 子工具 TOOL_MODE / 主扫描)必须**共享同一份前置初始化**(PS 查找、目录等), 任一入口都要保证依赖变量已就绪, 不能只在主流程初始化一次; ③ **对策**: 在 `:TOOL_MODE` 入口 `call :ENSURE_PS` 兜底查找一次(PATH + 常见路径 + WindowsApps + 可执行验证), 与主流程 STEP2 策略一致; `/diag`、`/restore` 等子工具都受益; ④ **顺手坑**: bat 脚本里 `goto` 跨大段复用变量时要小心——被跳过的标签区间里初始化的变量, 在跳转目标里一律视为"可能未初始化"; 用 `grep` 核对每个入口到目标标签之间是否漏了前置步骤。
- **v1.35.0 (2026-08-21)**:**架构变更:自保护从 PowerShell 层下沉到 Go exe**(对应 SilverFox Detector **v2.15.0**):① **变更实质**: 原 §5/§7 记录的 `SelfGuard.ps1`(看门狗+进程 DACL) 与 `SilverFoxDetect.ps1::Test-Integrity`(文件完整性) 全部由 **`SilverFoxDetector.exe` 自身 Go 实现**, 不再依赖 PowerShell 层; ② **exe 三件套**(`main.go`): `protectSelfDACL()`(`OpenProcess`+`ConvertStringSecurityDescriptorToSecurityDescriptorW`+`SetKernelObjectSecurity`, SDDL **`O:SYG:SYD:(A;;GA;;;SY)(A;;GA;;;OW)`** 仅 SYSTEM+Owner 可终止)、`runIntegrityCheck()`(读 `legacy/integrity.manifest`, 用同一 salt `SilverFoxDetector-INTEGRITY-SALT-v1-!@#$%^&*2026` 复算 `sig` 校验清单签名 + 逐文件 SHA256 比对)、`watchdogMain()`/spawnWatchdog(主进程写 `sf_guard.flag` + spawn 自身 `--watchdog <pid>` 子进程, 轮询主 PID, 消失且 flag 在→被 kill 自动重启上限5次, flag 不在→正常退出; `Global\SF-SelfGuard-<exe哈希>` mutex 防重复看门狗); ③ **关键约束**: 自保护**仅在 GUI 主模式启用**, `--cli`/`--register`/`--unregister` 不启用(避免 `os.Exit` 跳过 flag 清理); watchdog 重启主进程时新主进程会再 spawn 看门狗, 但新看门狗因 mutex 被旧看门狗持有而退出 → 仅一个看门狗长驻; ④ **manifest 仍是单一真相源**: 签名 salt / 算法不变, v2.14.1 已重签的 33 条 manifest 继续有效(下沉后 exe 用同一算法校验, 真机应输出"工具完整性校验通过"); ⑤ **§5/§7 历史坑仍有效但对象变了**: 混淆器误伤方法调用(§5 v1.12①)、DACL 用 `OW` 而非 `BA`(§5 v1.12②)、`sf_running.flag`/`sf_guard.flag` 的"残留=被 kill"判定(§5 v1.11④) 等原理仍适用于 exe 版实现; **PowerShell 层 `SelfGuard.ps1` 现仅作兼容/源码参考, 不再是运行时自保护路径**。
- **v1.34.0 (2026-08-21)**:新增 §12 **用 Wine + xvfb 在 Linux 沙箱验证 Windows GUI 程序**(实战落地 SilverFox Detector v2.12~v2.14 验证流程):① 安装 `wine`(无独立 `wine64` 二进制, 用 `wine` 启动器) + `xvfb` + `xdotool`;② 首次跑创建 `~/.wine` prefix 报 `syswow64\rundll32.exe c0000135` 缺 DLL 与 exe 无关, 配 `WINEDLLOVERRIDES="mscoree,mshtml="` + `WINEDEBUG=-all` 跳过弹窗;③ 验证启动: `timeout 40 xvfb-run -a wine SilverFoxDetector.exe` + 读 `SilverFoxDetector.log` 启动序列;④ 验证 WM_COMMAND 路由(§10): xdotool 按 `按钮客户区坐标 + wine 边框偏移(左≈3,上≈23)` 点击, 日志需出 `WM_COMMAND id=10xx code=0`(实测 `id=1030` 拉起 `cmd.exe pid=288`);⑤ 验证 bat 语法(§11): `wine cmd /c 银狐木马检测.bat` 的 GUI_MODE 分支 **不再报 `此时应有 检测工具。`**;⑥ 已知限制: wine 无 Windows PowerShell, bat 末尾 `call SilverFoxUI.ps1` 引擎在 wine 下失败(真机不受影响), Wine 验证覆盖"启动/按钮/bat解析"而非完整检测功能。
- **v1.33.0 (2026-08-20)**:新增 §11 **bat `if (echo ...(...))` 嵌套括号陷阱**(对应 SilverFox Detector v2.14 复盘"GUI 弹窗报 '此时不应有 检测工具。' 闪退"):① **根因**: CMD 解析器对 `if X (cmd1) else (cmd2)` 复合语句体内的 `(` `)` 做**简单括号计数**(不做字符串/上下文感知), 当 if-body 的 echo 字符串里写 `(SilverFox)` 时, 解析器把字符串里的 `(` 当成新嵌套块起点 → 配对错位 → 报 `此时不应有 X` 并立刻终止; ② **典型坑位**: GUI_MODE / TOOL_DIAG 标题、`(集成模式)` 等任意 `(...)` 字面量嵌在 if-body echo 里都触发; ③ **对策**: 用 `[SilverFox]` / `[集成模式]` (方括号对 CMD 解析器无特殊含义), 或 `< >` / 无包围符; ④ **安全边界**: echo 单独用 `(` 是安全的(平级命令), `for /f` 体内也有同样陷阱; ⑤ **顺手清掉 `\r\r\n` 行尾污染**: Python `raw.replace(b'\r\r\n', b'\r\n')` + `re.sub(rb'(?<!\r)\r(?!\n)', b'', raw)`, 验证 `file <bat>` 不再含 "CR line terminators"; ⑥ **排查铁律**: GUI 启动 bat 报错 → 复制 bat 报错行 → grep `if [^()]*\(echo.*\(` 看嵌套; 比 §9 控制台更隐蔽但同样"看起来像 exe 的问题"。
- **v1.32.0 (2026-08-20)**:新增 §10 **Win32 子控件 WM_COMMAND 路由**(对应 SilverFox Detector v2.13 复盘"按钮依然没反应"):① **v2.12 误诊**:凭"控制台窗口没弹"就改 `CREATE_NEW_CONSOLE`, 但用户日志显示点按钮时主窗口**一条 `WM_COMMAND` 都没收到** —— 控制台弹不弹与按钮能否被处理是两回事;② **真因**: v2.11 把功能按钮挂在 `Static` 容器窗口(`pageDetect`/`pageTools`)下, 子控件点击只把 `WM_COMMAND` 发给**直接父窗口**(容器), 而 `Static` 的 `DefWindowProc` **不转发**给 `mainHwnd` → 消息被吞 → 按钮全死; 顶部切换按钮因是 `mainHwnd` 直接子控件"看起来能用", 极具迷惑性;③ **对策**: 注册自定义容器类 `SFContainer`, `wndProc` 仅把 `WM_COMMAND`/`WM_NOTIFY` 转发给 `mainHwnd`(`wParam`/`lParam` 原样保留), 容器改用该类;④ **排查铁律**: 先让用户贴启动日志, 数 `WM_COMMAND` 是否进主窗口过程, 再决定改哪里; **按钮可见 ≠ 按钮可点**。§9 末尾加"误诊更正"链接回本节。
- **v1.31.0 (2026-08-20)**:新增 §9 **Win32 GUI 程序启动 bat/ps1 子进程**(对应 SilverFox Detector v2.11→v2.12 修复"点启动检测无反应"):① **GUI 程序无 console, 直接 `cmd /c bat` 时 cmd.exe `AttachConsole(父进程)` 失败, 子进程静默退出, 用户看到"无反应"** —— 子进程能跑但窗口从未弹;② **双保险对策**: `exec.Command("cmd.exe", "/c", "start", "", bat, mode...)` + `SysProcAttr.CreationFlags=0x10 (CREATE_NEW_CONSOLE)`, 加 `cmd.Dir=bat 所在目录` 显式工作目录;③ **必须 `cmd.Start()` 而非 `Run()`** —— Run 阻塞 GUI goroutine, UI 看起来"无反应";④ **状态栏 + 日志双倍反馈**, 失败 `msgBoxInfo` 显示 bat 完整路径, 一眼看出是否路径错;⑤ **别错用 `/B /MIN`**(抑制窗口), GUI 程序要的是**可见窗口**不是后台, 与 §2.7 的"空标题必须"是两件不同事;⑥ §7 交付清单新增 "GUI 程序启动 bat 必加双保险" 一条, 防回归。
- **v1.16.0 (2026-08-18)**:§5/§7 代码清理实战新坑(对应一次"移除内核驱动加载路径、仅保留关闭记录逻辑"的大改): ① **删变量/函数后必须 grep 残留引用(静默失效)**: 移除 `$script:ExtremeActive` 变量定义后, kill 分支 `if (-not $script:ExtremeActive)` 仍在引用它——PS 未定义变量返回 `$null`, `-not $null` 为 `$true`, 逻辑"碰巧"继续对, 但属脏代码/隐患(与 v1.12.0 混淆误伤同类: 不报错但行为偏离预期); **任何删除函数/变量/参数的改动, 改完必须 `grep -n` 全量扫残留引用**, 不能只信编辑器高亮; ② **manifest 重签必须是"所有源文件改完之后"的最后一步**: 本次先重建 manifest(重算哈希), 之后又 Edit 改了 SelfGuard.ps1 → manifest 内该文件哈希过期、自检报 mismatch; 正确顺序=改完所有源文件 → 最后重建 manifest → 最后跑验签; ③ **manifest 验签脚本自身的正则陷阱**: 自查用 `r'^[^\s|]+\|[0-9a-fA-F]{64}$'` 匹配清单行, raw 字符串里字符类 `[^\s|]` 的 `\s` 被当字面 `\`+`s`(非空白), 路径含 s 字符被排除 → entries=0、误报 MISMATCH; 正解=用 `r'^.+\|[0-9a-fA-F]{64}$'`(路径不含 `|`, 贪婪到末尾 `|hex` 即可), 字符类内 `\s` 在 raw 串语义要当心; ④ **Python 二进制改 GBK bat 复用 v1.12.0⑧**: `open(path,'wb')` 写回 + `split(b'\r\n')`/`join(b'\r\n')` 重拼保 CRLF; 版本号 `data.replace(b'v1.51',b'v1.52')` 全局替换前必须确认只有 banner 行含该串(历史 v1.50 注释保留不动), 写完校验 `crlf==count('\n')` 且 stray-LF=0。
- **v1.17.0 (2026-08-18)**:§5 扫描引擎降误报实战新坑(对应"引入风险评分关联引擎"的大改): ① **单一弱启发式绝不直接判高危, 必须累积风险分跨阈值才升级**: 旧版命令行正则 `base64|iex |-w hidden` 单独命中即 Flag(高危), 计划任务 `\appdata\` 过度匹配(所有正常软件更新任务都中招), WMI 事件筛选器一刀切全标可疑——三大误报源; 正解=定义权重表 `$RISK`(KNOWN_HASH=100/IMPERSONATE_SYS=90/DOUBLE_EXT=85/DL_EXEC_WEB=50/C2_DOMAIN_CMD=45/PERSIST_TEMP=40/UNSIGNED_PERSIST=25/WMI_FILTER=30/WIN_HIDDEN=15/IEX=10/BASE64=5), `Get-RiskVerdict` 按 THREAT≥80 / WARNING 30–79 / CLEAN<30 三档裁决; **弱信号单独(<30)应被忽略(CLEAN), 不进观察清单也不进高危**——`-w hidden`/`iex`/`base64` 单独是纯噪声; 多个弱信号叠加(如 下载执行+temp无签名=115)才升 THREAT, 这才是降误报的核心; ② **Get-RiskVerdict 阈值设定: 噪声信号权重必须 < WARN(30)**: WIN_HIDDEN=15/IEX=10/BASE64=5 都低于 30 → 单独 CLEAN; 若把它们设 ≥30 会变成"待核实"污染观察清单; ③ **PowerShell 含空格可执行路径解析陷阱(高危误报根因)**: 旧代码 `$ex -replace '"','' -split ' ' | Select -First 1` 把 `"C:\Program Files\X\a.exe"` 截断成 `C:\Program` → 后续 Test-TrustedSigner/Test-Whitelist 全失效 → Program Files 下合法签名软件被误判; 必须用 `Get-ExecPath`(引号优先取引号对内; 未引号按 `.exe$` 后缀累积拼接 tokens)正确提取; ④ **C2 域名匹配必须边界感知**: 简单 `($c2Domains.Keys|%{[regex]::Escape($_)}) -join '|'` 子串拼接会让 `notmal.com` 误命中 `mal.com`、`mal.com.evil` 误命中 `mal.com`; 正解 `Test-C2DomainInText` 用 `(?<![a-z0-9.-])域名(?![a-z0-9.-])` 前后边界断言; ⑤ **PowerShell 数组 `-eq 0` 是"过滤"不是"比较"**: 对函数返回的数组 `@()` 写 `(Test-X).Count -eq 0` 才对; 写成 `(Test-X) -eq 0` 会触发数组元素过滤(返回空数组→被 `if` 判为假)→ 单测假失败; ⑥ **验签正则 `\\|` 陷阱再次复现**(同 v1.16.0③): Python raw 串 `r'^.+\\|[0-9a-fA-F]{64}$'` 中 `\\|` 被解析成"反斜杠 或", 应写 `r'^.+\|[0-9a-fA-F]{64}$'`(字面管道用 `\|`); 自查脚本必须先 `print(entries长度)` 确认非 0, 再信 sig_match。
- **v1.15.0 (2026-08-18)**:§5 第十一轮(v1.51 熔断式极端自保护)新坑: ① **用户态防杀天花板**: DACL+心跳自愈双守护已是用戶态能做到的极致, 但仍可被"同时杀两进程"或 SeDebugPrivilege 管理员破防; 用户明确接受"不太合规手段"作为熔断应急——仅当被疯狂关闭(2分钟内≥5次)才升到内核级; ② **熔断式极端自保护架构**: watchdog 每次确认引擎被强杀(进程消失且 sf_running.flag 仍在)→ 向 `sf_kills.log` 追加 ISO 时间戳; `Test-KillStorm` 统计最近120s内条数, ≥5 即"关闭风暴"; 达成→写 `sf_extreme.flag` 持久标志 + 调 `ExtremeProtect.ps1`; ③ **极端手段=测试签名内核驱动** `sfguard.sys`(WDM + `ObRegisterCallbacks` 进程回调, 对受保护 PID 移除 `PROCESS_TERMINATE` 权限位→TerminateProcess 失败"拒绝访问", 标准安全软件进程保护做法, 不返回 ACCESS_DENIED 避免异常/蓝屏); 用户态用 IOCTL(0x222000)把引擎+watchdog 的 PID 刷给驱动(引擎重启 PID 变, 故 watchdog 每10s 刷新一次); ④ **绕开 2026-04 内核签名强制的"不太合规"**: 驱动需 `TESTSIGNING` 模式(`bcdedit /set testsigning on` + 重启)才能加载, `ExtremeProtect.ps1` 自动开启; 这是系统级变更(桌面"测试模式"水印、内核完整性降级), 仅在熔断触发或显式 `/extremeprotect` 时启用, **非默认**; ⑤ **驱动需用户自编译**: 沙箱无 WDK 无法编译验证, 提供 `bin/drivers/sfguard.c` + `sfguard.vcxproj` + `build_driver.bat`(VS2022+WDK 编译 + 自签测试证书 + signtool 测试签名), 必须在虚拟机先验证再上真机(ObRegisterCallbacks 实现不当有 BSOD 风险); ⑥ **重启恢复**: 引擎/ watchdog 启动读 `sf_extreme.flag` 自动恢复极端态(此时 TESTSIGNING 已生效→加载驱动); `/resetextreme` 或 `/softprotect` 清除标志并 `sc delete sfguard` 降回用户态; ⑦ **阈值与计数分离**: 记录关闭次数+时间(`sf_kills.log`)可常驻, 但内核驱动加载(熔断触发)必须严格受阈值门控, 避免常态化合规/稳定风险; ⑧ **manifest 新增 `ExtremeProtect.ps1` 与 `bin/drivers/*` 源码**(不含缺失的 .sys), 改完必须重签(本次 sig 重算=71417e1461a4299a)。
- **v1.14.0 (2026-08-17)**:§5 第十轮(v1.50 心跳自愈+蓝屏降级)新坑: ① **蓝屏威慑对恶意软件无效**: "病毒不是人", 蓝屏没有威慑意义且影响用户业务——蓝屏只能作为 `/bruteprotect` 显式手段, 不能默认; ② **进程防杀核心改为"心跳自愈"双守护**: 引擎被杀→watchdog 复活引擎(已有); watchdog 被杀→引擎检测心跳超时重新 spawn——**单个被杀都能自愈, 只有"同时杀两个进程"才破防**(恶意程序很难做到); 实现: watchdog 轮询循环每次写 `sf_guard.heartbeat`(LastWriteTime 每 2s 刷新), 引擎 `Ensure-Watchdog` 检查心跳 >45s 未更新→判定死亡→重新 spawn, 调用点在扫描前/交互前/完成前; ③ **提取可复用 Spawn-Watchdog 函数**: watchdog spawn 逻辑从 Start-ProcessGuard 抽出为独立函数(cmd start "" /B /MIN + .NET Process), 供首次 spawn 与心跳自愈复用; ④ **测试陷阱: 模拟"文件时间戳"要改 LastWriteTime 而不是写旧内容**: 心跳判断基于 `(Get-Item $hb).LastWriteTime`, 模拟死亡场景必须 `(Get-Item $hb).LastWriteTime = (Get-Date).AddSeconds(-120)`, 往文件里写旧时间字符串无效(LastWriteTime 是实际写入时间); ⑤ 简化原则: 复杂策略(智能计数/多档)若价值存疑应砍掉, 用户要的是"杀不死 + 不打扰", 不是复杂逻辑。
- **v1.13.0 (2026-08-17)**:§2/§3/§5 第九轮(v1.49 智能蓝屏+GUI迁移)新坑: ① **DACL 挡不住 SeDebugPrivilege**: 任务管理器以管理员运行时启用 SeDebugPrivilege, OpenProcess/TerminateProcess 可绕过进程 DACL——"像安全软件那样拒绝访问"对管理员任务管理器做不到; 用户态唯一硬威慑是 **ProcessBreakOnTermination(蓝屏)**; ② **蓝屏策略要"智能"不要默认**: 用户明确"蓝屏不要太多", 设计为 默认不蓝屏 + `/bruteprotect` 强制 + **智能模式(连续被强杀≥2次才主动蓝屏)**: 用 `sf_killcount.flag`(持久化计数)+ `sf_running.flag` 残留判断(残留=上次被强杀, 正常退出会删)→ count>=2 才设 BreakOnTermination; 首次 0 / 被杀1次 1(用户误杀不蓝屏) / 连续2次 2(蓝屏威慑) / 正常退出清零; ③ **watchdog 不设蓝屏**: 蓝屏只由引擎智能触发, watchdog 被杀靠引擎重启后重新 spawn, 避免用户杀 watchdog 也蓝屏; ④ **GUI bat 放 `bin\_gui\` 单独文件夹**: 主入口 bat 无参弹 GUI(根目录), 独立 GUI 快捷入口放 bin\_gui\, 内部路径用 `%~dp0..\SilverFoxUI.ps1`(相对上上级); ⑤ **GUI 新增选项要同步 3 处**: argMap(参数映射)+ 2 个收集 hashtable(预览/启动)+ checkbox 定义, 漏一处 = 勾了不生效; ⑥ manifest 里文件路径变了必须同步(根目录 GUI bat 移走后 FILES 列表要更新, 否则重建报"缺失")。
- **v1.12.0 (2026-08-17)**:§1/§3/§5 第八轮(v1.48 自保护+GUI)新坑: ① **混淆器/打码脚本误伤方法调用是"静默失效"炸弹**: 注释打码用 `w + '(0x'` 模式替换, 把代码里的 `[ProcGuard]::OpenProcess(0x0400...` 也替换成 `[ProcGuard]::[API](0x...` → 运行时抛异常被 try/catch 吞掉 → **DACL 实际没生效, 任务管理器照样能杀进程**(用户实测发现)。**任何打码/混淆只准动注释与引号字符串, 绝不动方法调用 `[Cls]::Api(...)`; 混淆后必须 `grep -c '::OpenProcess('` 验证关键调用完好**; ② **DACL 防管理员杀进程**: 之前 SDDL `(A;;GA;;;SY)(A;;GA;;;BA)` 保留 BA(管理员组)权限 → 管理员任务管理器仍能 TerminateProcess; 改为 **`(A;;GA;;;SY)(A;;GA;;;OW)`(只留 SYSTEM + Owner)** → 任务管理器(普通/管理员)结束进程均"拒绝访问", 仅 SYSTEM 与进程所有者可管理; Owner 有完全控制可随时恢复/正常退出(ExitProcess 不需要权限); ③ **自保护"双击即启动"的实现顺序**: 把 `Start-ProcessGuard` 调用插在 banner 后, 但函数定义在后面 → 运行时"函数不存在"!**调用必须在函数定义之后**(或函数整体提前); 同时 `$SelfProtect`/`$script:ScriptArgs` 要前置初始化, `/noselfprotect` 需在头部预扫描 `$args`(参数解析还没执行); ④ **watchdog 也要 DACL 自保护**: SelfGuard.ps1 启动时用同样 SDDL 给自己设 DACL, 否则任务管理器先杀 watchdog 再杀引擎=守护失效; ⑤ **bat 无参数双击弹 GUI 的模式**: 参数分派段后 `if "%~1"=="" goto GUI_MODE`, GUI 段自包含(找 PS→调 `bin\SilverFoxUI.ps1`→退出), 带参数仍走老 CLI 流程——"主入口 GUI + 老脚本保留"的实现范式; ⑥ **再次踩 §1.3.1 的 `\v` 坑**: Python heredoc 用**非 raw 三引号**字符串写 bat, `WindowsPowerShell\v1.0` 的 `\v` 变垂直制表符 0x0b → bat 静默损坏; **写含 Windows 路径的代码一律 raw 字符串 `r'''...'''`**, 写完扫描 `b<0x20 and b not in (0x09,0x0a,0x0d)`。
- **v1.11.0 (2026-08-17)**:§1/§2/§3/§5/§8 第七轮用户实测反馈修复(v1.43~v1.47)新坑: ① **`Console.OutputEncoding = GetEncoding(936)` 与 bat `chcp 65001` 冲突=退出乱码**: PS 子进程输出按 GBK 编码字节, cmd 按 UTF-8 解码 → 退出段满屏符号乱码(♥♡❤☺♦♣♠•◘○)。对策: 引擎头部**先设 UTF-8**, 仅当系统 CodeSet 非 UTF-8 才回退 936; ② **启发式高危判定必须查白名单/签名**: `Hidden|PE` 直接报高危不查 `Test-Whitelist`/`Test-TrustedSigner` → Bcut/Inno Setup 等合法软件 dll 误报(实测 3 个必剪 dll 全中); 隐藏属性单独不构成威胁证据, 应降级"观察"而非高危; ③ **交互默认开启**: `if ($Interactive)` 只有显式参数才弹菜单, 普通用户扫完直接退"找不到选择界面" → 改为**默认有文件类高危就弹**, 加 `/noask` 关闭(`$AutoAsk` 默认 true); ④ **进程防杀三层**: a) 进程 DACL 移除 Everyone/Users 终止权限(非管理员 taskkill → Access Denied); b) **watchdog 双进程守护**: 引擎被杀自动重启(判断依据: 进程消失但 `sf_running.flag` 仍在=被 kill; 标记被删=正常退出), 单实例互斥防堆积, 连续 5 次停止; c) `/bruteprotect` 硬保护: `NtSetInformationProcess(ProcessBreakOnTermination=29)` 被用户态 kill → 蓝屏威慑, 默认关; ⑤ **Add-Type C# 块整体 base64 编码防杀软**: `Add-Type -TypeDefinition @"..."@` 与 `@'...'@`(两种 here-string 都要匹配) → `([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('...')))`, DllImport/API 名源码不可见, 大幅降启发式误报; 方法调用 `[ProcGuard]::OpenProcess(...)` 无法混淆(改了就调用不了), 但杀软对方法调用权重低, 可接受; ⑥ **bat 多源 PS 搜索**: 只列 4 个固定路径 → `where pwsh`/`where powershell` PATH 搜索 + WindowsApps + Scoop, 且**可执行验证**(`-Command "$null"` 失败则清除); PS_EXE 为空时**强制 FATAL 退出**(`if not defined PS_EXE goto FATAL_NO_PS` + exit /b 4), 否则后续 `"%PS_EXE%" -NoProfile` 空变量展开为 `"" -NoProfile` → cmd 报"找不到文件 -NoProfile"(用户实测截图); ⑦ **cmd `start` 命令第一个引号参数被当窗口标题**: `cmd /c start /B /MIN "pwsh.exe" -NoProfile ...` → "pwsh.exe" 是标题、`-NoProfile` 被当命令 → 弹"找不到文件 -NoProfile"窗口; 修复: **`start "" /B /MIN` 加空标题参数**, 并用 `.NET Process`(`StartInfo.Arguments` 字符串按字面传)替代 `Start-Process -ArgumentList` 数组(PS 5.1/7 对空串/引号元素拼接行为不一致); ⑧ **Python 文本模式写 bat 会把 CRLF 变 LF**(Linux 上 `\n` 当行尾)→ bat 打不开/标签解析错乱/窗口乱码!**写 bat 必须 `open(path,'wb')` 二进制模式 + 手动 `\r\n`, 写完校验 `d.count(b'\r\n') == d.count(b'\n')`**, 同一文件被 Python 文本模式二次写坏=连续两轮踩坑; ⑨ **GUI 启动器经验**: WinForms 控件布局超出窗口尺寸(按钮在 Y=785 窗口 720)→ 设 880 + AutoScroll; PowerShell GUI 事件 scriptblock 闭包可访问函数局部变量(ShowDialog 阻塞期间变量在作用域), 标准模式可放心用; ⑩ **打包 zip 文件名必须带新版本号**: 同名 zip 会被下载器缓存, 用户拿到旧包误以为"没打包"(实测 v1.45 zip 内容正确但用户看到旧文件), 换 `v1.46/v1.47` 文件名强制刷新。
- **v1.10.0 (2026-08-17)**:§2/§5/§7 第六轮逐行精查新坑: ① **PowerShell 单引号正则里 `\M`/`\t`/`\a` 是 .NET 转义**: `'^\Microsoft\'` 的 `\M` 是**非法转义直接抛 RegexParseException**(实测确认, 计划任务模块整体失效), `'(\temp\'` 的 `\t` 是制表符(特征永不命中)——Windows 路径特征正则**必须双反斜杠字面** `\\`; ② **for /f 循环体末尾是 set 时 errorlevel 恒 0**: `for /f ... in (\`ps 2^>nul\`) do (set X=%%a)` 后读 errorlevel 永远 0, 验签恒"通过"形同虚设——改用**临时文件**捕获输出+直接命令的 errorlevel; ③ **ForEach-Object 内 `continue` = break**: 脚本块里 continue 相当于整个管道的 break(不是跳过当前项!), 首个无 cmdline 进程即中止整个进程扫描——必须用 `return` 跳过当前项; ④ **外部命令列解析要对齐真实格式**: ss -tnp 的 Process 列在 `$parts[5]` 不是 [6](State Recv-Q Send-Q Local Peer Process), 列错位=全漏; ⑤ 正则提取哈希要 `\b` 边界, 否则 64 位 SHA 被 32hex 正则切两半入库; ⑥ **汇总报告要按真实计数输出**: 写死"未自动隔离"文案在 /quarantine 模式下是假报告, 用 $qcount 判断; ⑦ urlhaus CSV 解压的 FileStream/GzipStream/ZipArchive 必须 try/finally Dispose, 空 zip 的 Entries[0] 会空引用; ⑧ 备份类修复操作(hosts)必须先成功备份再改, 备份失败要 return 而不是继续覆盖(数据丢失不可逆); ⑨ 交互输入转 [int] 要用 TryParse, 直接 [int]() 遇非数字抛终止错误直通全局 trap 杀引擎; ⑩ bat 括号块内 echo 变量要 !var! 延迟展开(%PSVER%/%SF_FLAG_INFO% 恒空)。
- **v1.9.0 (2026-08-17)**:§8/§5 第五轮深度检测新坑: ① **清单/Flag 行的"路径+[状态]"双段格式是反复踩的坑**: 所有从 `[高危文件][原因] 路径 [状态]` 行提取路径的地方, 必须**先 -replace '\s+\[[^\[\]]*\]\s*$' 剥尾部状态**再取(贪婪 (.+)$ 会把 [建议隔离] 吞进路径, 实测 /interactive 直接崩溃); ② **统计容器($script:susp/$script:observe/$script:qcount)必须在参数解析后显式 =@()/0 初始化**——未初始化时 $null+= 首条变标量, 后续变字符串拼接, 汇总恒报 1 项, 观察清单数据全丢; ③ **Update-IOC 的 update.json 离线包**: JSON 键带引号 `"md5s": [` 而解析正则假设 Python 风格 `md5s = [`, 必须 `"?` 兼容引号; 且**全源失败/解析 0 条时不得覆盖 auto 文件**(保留旧文件+告警), 否则断网更新会把库清空; ④ **auto_hashes/auto_c2 写入后必须让 Load-Hashes 在启动时追加加载**(只写不读 = 更新管线整体失效); ⑤ **子脚本被引擎 `&` 调用时的三个坑**: a) `[Console]::OutputEncoding = GetEncoding(936)` 在 pwsh7/.NET Core 抛异常必须 try/catch+RegisterProvider 兜底(否则第 1 行崩溃); b) **顶层裸 `exit 0` 会终止引擎进程**(退出标记/EXIT 审计/锁清理全不执行, bat 验签误报异常退出)→ 子脚本统一 `exit N`→`return N`; c) 引擎调子脚本要 `@($script:PathArgs)` 转发用户参数(否则 -Recycle/-All 丢失); ⑥ **清单解析正则的 `[ ]` 歧义**: 原路径含 `[` 且无配对 `]` 时 `[^\]]*` 贪婪吞路径 → 恢复错位置 + Rollback 删备份不可逆; 正解=右侧改贪婪 `(.+)$` + 提取时从右往左剥可选后缀; ⑦ 白名单盘符正则 `^[a-z]:` 只认小写 → `[a-zA-Z]`; ⑧ 批量替换时**注释必须放整行语句之后**, 别插进正则/表达式中间(实测把 # 注释替换进 `'^[a-zA-Z]:\\'` 行内导致语法 FAIL)。
- **v1.8.0 (2026-08-17)**:§2/§3/§5 第四轮复查新坑 + **修正 v1.7.0⑤的错误结论**: ① **`shift` 不更新 `%*`**(%* 恒=全部原始参数, 已对照 ss64/微软文档确认)——上一轮"shift 去掉 %1 再透传"无效, 子工具仍收到分派参数; 正解: **`set "SF_EXTRA="` + 逐 `if not "%~2"=="" set "SF_EXTRA=%SF_EXTRA% "%~2""` 显式重建 %2-%9**(set 保留内部引号, 未定义参数自动跳过), 不依赖 shift 语义; ② **MEMORY_BASIC_INFORMATION 必须含 `ushort PartitionId`**(Win10 2004+ 新增, 位于 AllocationProtect 与 RegionSize 之间)——缺它时 **32 位 pwsh 结构偏移错位**(RegionSize 读到 0 → 每进程空转满超时或 VirtualQueryEx 全失败), x64 因对齐巧合不炸, 属"不崩但全漏"; ③ **报告兜底放模式区前是错的**: `if(-not $log)` 恒真 → 主流程每次产生 2 个报告文件(1 空占位); 应把兜底**移入真正用 Add-Report 的函数内部**(Invoke-MemScan/Invoke-DriverAudit 开头); ④ **Stop-ShutdownGuard 回读历史审计日志**: 未启动过守护的模式分支(/restore /mem /update)会把上次运行的拦截事件写进本次报告(假"拦截 N 次") → 加 `$script:ShutdownGuardStarted` 标记, 未启动不回读; ⑤ 任务脚本检测只查 `Actions.Execute` 会漏(脚本通常在 `Actions.Arguments` 如 `powershell -File x.ps1`) → Arguments 也要提取; ⑥ 进程内存扫描必须有**全局时间预算**(60s)+候选上限(40)+单进程上限降 32MB/16MB, 否则几十进程串行数分钟; ⑦ Linux 候选过滤**跳过系统解释器会全漏**: 脚本载荷跑在 /usr/bin/python3 等下面, 应豁免解释器(python/bash/sh/perl/ruby/php/node); ⑧ **sh 启动器前台/后台模式 pwsh 查找候选路径不一致**: 后台有 `$HOME/.local/share/pwsh/pwsh` 前台没有 → 用户目录安装 pwsh 时前台直接失败, 两处候选必须一致; ⑨ schtasks 中文 Win7 表头实际是 `要运行的任务:`(不是"任务要运行")且**没有任务路径字段**, 系统任务排除要靠任务名前缀; ⑩ 可读内存掩码要含 WRITECOPY(0x08)/EXECUTE_WRITECOPY(0x80)(DLL .text 常用); ⑪ bash -c 里 `${ARGS[*]}` 空格合并丢引号 → 每参数包 `\"$a\"` 重建命令串。
- **v1.7.0 (2026-08-17)**:§3/§5 新增内存检测(P/Invoke+proc)与整合回归经验: ① **读进程内存**: Win 用 `Add-Type` C# P/Invoke (OpenProcess(PROCESS_VM_READ|PROCESS_QUERY_INFORMATION)+VirtualQueryEx+ReadProcessMemory), 只读 MEM_COMMIT 且 Protect 可读且非 PAGE_GUARD 区, 分块≤1MB、单进程≤64MB、Stopwatch 15s 超时(防大内存进程拖垮), 地址进位用 `$mbi.BaseAddress.ToInt64() + RegionSize`; Linux 用 `/proc/<pid>/maps` 解析 `start-end r--` 段(跳 vdso/vvar/vsyscall)+`/proc/<pid>/mem` FileStream Seek 按段读, **非 root 被 yama ptrace_scope 拒**需先检查并优雅降级; ② **模式分支在报告路径初始化之前** -> `$log` 为空时 Add-Report 静默丢弃(报告不生成!), 需兜底建报告(注意兜底位置, 见 v1.8.0③); ③ **内存特征过宽误报**: `/tmp/`、`w hidden`、`sh -i` 会命中大量正常进程(实测 docker/node/pm2 全中), 只留明确恶意串(MODBEACON/ReflectiveLoader/msfvenom/FromBase64String/DownloadString/-enc)+C2库, 域名≥4字符/IP≥7字符过滤; ④ 已删 exe 检测(内存驻留木马特征): `/proc/<pid>/exe` readlink 以 `(deleted)` 结尾即命中, 独立于内存读取权限; ⑤ ~~整合 bat 的 %* 透传陷阱: 子工具分派后 `-File script.ps1 %*` 会把分派参数(/restore)一起传给严格 param() 的脚本 -> 参数绑定错误直接失效, 必须 shift 掉 %1 再透传~~(**错误! shift 不更新 %*, 正解见 v1.8.0①**); ⑥ bat 退出码丢失: `endlocal` 与 `exit /b %RC%` 分行时 endlocal 后 %RC% 回退为空, 必须 `endlocal & exit /b %RC%`; ⑦ Get-ScheduledTask 在 Win7/PS5.1 未定义(命令静默失败假报 0 个), 先 `Get-Command` 探测再回退 `schtasks /query /v /fo list`(中英文表头都要匹配); ⑧ Linux root 判断用 `(id -u) -eq 0` 而非 $env:USER(可污染); ⑨ 进程 Path 为空(提权/他人账户)要回退 Win32_Process 映射 + 计入观察清单, 勿静默丢弃。
- **v1.6.2 (2026-08-17)**:§2/§8 新增"整合单入口"实战经验(想法11): ① **多 bat 收敛为一个入口**: 主 bat 开头用 `if /i "%~1"=="/xxx" set "SF_TOOL=xxx"` 参数分派, 子工具走**自包含 TOOL_MODE 段**(查脚本→找PS→提权→调用→退出), 独立标签不干扰主流程 goto 结构(别复用主流程标签, 否则改一处毁全部); ② **UAC 重跑必须带参数**(否则提权后重跑进主流程): 用 `Start-Process -FilePath '%~f0' -ArgumentList $env:SF_UAC_ARG -Verb RunAs`, **先 `set SF_UAC_ARG=/restore` 再让 PowerShell 读 `$env:SF_UAC_ARG`**, 彻底避开 cmd 双引号嵌套地狱(单引号/双引号/反引号在 bat 里互相打架); ③ **integrity.manifest 陷阱**: 改任何被清单记录的文件(含 bat/README/ps1)后**必须同步重算 SHA256 + 整清单重签**(salt 在引擎代码里), 否则引擎每次运行误报"文件被篡改"——前几轮改了 6 个 ps1 却从没更新 manifest, 属历史漏网; ④ **整合时子工具调用保持"直接调 bin/*.ps1 + %* 透传"** 而非改走引擎中转(引擎分支不传参数, 会丢 -Recycle/-All 等开关), 行为与旧版一致回归风险最小; ⑤ 归档旧文件用 `bin/_legacy_bat/` + README 说明而非删除(留后路), 但归档内路径失效要在说明里讲清; ⑥ bat 整块插入必须先对锚点做 CRLF 转换(Python raw 三引号是 LF, 文件是 CRLF, 直接匹配必失败), 且逐锚点 assert。
- **v1.6.1 (2026-08-17)**:§7/§2/§8 第三轮复验新坑: ① **重构残留 `return return`**: 用 `return {ret}` 模板生成代码时 ret='return' 产生 `return return` 语法悬置, 重构后必须 grep 关键字残留; ② **bat 括号块内 `%errorlevel%`/`%变量%` 解析期展开**(取块前值恒错) → 块内判断必须 `!var!` 延迟展开(bat 需 `setlocal EnableDelayedExpansion`); ③ **"含 % 不冒险"的 fallback 写反**: `if ($delPath -match '[%]') { $delPath = $Path }` 把原路径回退给 cmd 恰是未堵住, 应直接 `return` 跳过; ④ **哈希表"名字误导"**: Linux 版 Load-Hashes 把 32/64hex 混存进 `$hashMD5`, 但命中检查用恒空的 `$hashSHA` → SHA256 IOC 永不命中(漏检), 修复后须验证混存语义; ⑤ 隔离失败后**必须补回锁定**(解锁在 try 前, 失败后文件原点无锁); ⑥ 上轮"日志编码修复"因实际格式是 `Out-File -FilePath $X -Append`(带 -FilePath)而没匹配上 → **修复后必须 grep 验证实际生效**; ⑦ 时间窗类参数(验签 30 分钟)要与引擎清理窗口(5 分钟)一致, 否则残留旧标记误判。
- **v1.6.0 (2026-08-17)**:§8/§5 新增辅助脚本审查与重构经验: ① **正则 `^(.*)$` 贪婪匹配会吞入行尾后缀** → 清单解析必须精确锚定可选后缀: `(.*?)(?:\s+\[[^\]]*\])?(?:\s*\|\s*原隔离区:\s*.*)?$` (防恢复落错文件名/回滚失败); ② **`"" | Out-File -Append` 默认 UTF-16, 后续 Add-Content 按 ANSI/UTF8 追加 → 日志中文乱码混排** → 首行必须显式 `-Encoding UTF8`; ③ 辅助脚本与主引擎的**路径回退必须一致** (Clear-Cache 的 LOCALAPPDATA 回退曾与引擎不同, 清不干净); ④ 多脚本复用的"交互序号选择"逻辑抽公共函数 `Get-Selection` (返回 @(-1) 表示取消), 收敛 8 处重复代码, 注意各处块文本细微差异(变量初始化位置/多行 all 分支/文案不同), 需逐处核对; ⑤ 大工程整块替换用**先 dump repr 对比再替换**, 别猜格式(曾因 LF/CRLF、尾随空格、变量初始化顺序差异匹配失败 3 次)。
- **v1.5.0 (2026-08-17)**:§7 新增自查方法论 + §2/§5 补坑: ① **多 agent 并行代码审查** + 逐个复验(不轻信结论, 用 grep/sed 验证每个发现) 是发现隐蔽 bug 的高效方式; ② **`foreach ($a in $args)` 循环内 `$_` 是空**(foreach 不设 `$_`, 只有 ForEach-Object 管道才设)→ 循环内必须用 `$a`(曾致 /threads=N 永不生效); ③ **cmd 里 `goto 未定义标签` 直接终止整个 bat** → 所有 goto 目标必须存在, 自查时 grep 全部 goto 与标签对比; ④ **SYSTEM 计划任务 cmd /c 拼接路径**: cmd 在双引号内仍展开 `%VAR%`, 必须先 `[Environment]::ExpandEnvironmentVariables` 并拒绝残留 `%` 的路径; ⑤ **可预测 /tmp 文件名 + symlink = root 任意文件写**: 写临时文件用 `[IO.File]::Open(path, CreateNew,...)` (O_EXCL 语义) 防符号链接; ⑥ `Move-Item` 等关键操作在全局 `SilentlyContinue` 下**必须显式 `-ErrorAction Stop` + Test-Path 复核**, 否则假成功; ⑦ 前缀匹配 `StartsWith($dir)` 必须补分隔符防 `FooEvil` 绕过; ⑧ 路径提取用 `(\S+)` 遇空格截断 → 改行末 `(.+)$`; ⑨ 关机守护按进程名 kill 会误杀系统/自身触发的合法 shutdown → **系统路径只记录不 kill**, 非系统路径才拦。
- **v1.4.4 (2026-08-17)**:§5 新增网络封锁实战经验: ① Windows 防火墙封禁: `New-NetFirewallRule -Direction Outbound -Action Block` 按 `-RemoteAddress`(IP) 或 `-Program`(进程路径), 需管理员; 查重用 `Get-NetFirewallRule -DisplayName`; ② Linux iptables: `iptables -C OUTPUT -d IP -j DROP` 查重(退出码0=已存在), `-A` 添加 `-D` 删除; **容器默认有 CAP_NET_ADMIN 可真实测试**, 但规则重启即失(未持久化, 工具定位是实时阻断); ③ Linux iptables 无法按进程过滤(需 owner/cgroup match), 进程路径封锁仅记录清单; ④ 规则名用 IP 转义(`-replace '[.:]','_'`)防重名, 进程规则用路径 MD5 前12位; ⑤ 封锁清单同样用「管道符分隔」+ 去重(查重 key 用目标值); ⑥ `/xxx` 管理模式的通用交互(查看清单→序号选择→解除)已复用第 4 处。
- **v1.4.3 (2026-08-17)**:§5 新增威胁锁定实战经验: ① **PowerShell 管道 0 对象不会触发 Set-Content** → 清空文件用 `Clear-Content`, 否则 `$lines | Set-Content` 空数组时文件保持原样(清单删除静默失败!); ② 文件锁定: Linux `chattr +i`(immutable 连 root 也删不掉) 但 **overlay 容器文件系统不支持 chattr**(Operation not permitted), 必须探测降级 `chmod a-w` 弱锁; ③ 弱锁只挡普通用户挡不住 root, 强锁(immutable)才能在真实主机防 root; ④ 锁定前记录原权限(`stat -c %a`), 解锁时恢复, 否则 `chmod a+w` 会把 644 变 666 破坏原权限; ⑤ 锁定清单用「时间|路径|原因|方式|原权限」管道符分隔, 路径含 `|` 的概率极低可安全切分; ⑥ 检测出→加锁、真正隔离/删除前才解锁, **默认只报告模式必须保持锁定**(Quarantine 里解锁要放在 QuarantineMode/Force 判断之后)。
- **v1.4.2 (2026-08-17)**:§5 新增驱动交互删除实战经验: ① **独立模式分支(/drivers /ring0 等)在报告路径段之前就 Exit, 主流程里才定义的变量(如 $qdir)在这些分支里是 $null** → 函数内必须兜底 `if(-not $script:qdir){$script:qdir=Join-Path $script:toolRoot ("银狐木马隔离区_"+...) }; $qdir=$script:qdir`; ② 函数内引用顶层变量要用 `$script:` 前缀读取(函数作用域查不到才向上查 script 作用域, 显式更稳); ③ 删除类交互必须二次确认(选择序号→输入 DELETE 确认词), 用管道 `printf "all\nDELETE\n"` 可自动化测试交互路径; ④ 删除危险对象(驱动/模块)前**先备份到隔离区**, 删除成功才记审计, 失败也留痕; ⑤ 交互逻辑(序号选择/范围解析/DELETE 确认)可复用, 已用于 交互隔离/驱动删除/模块删除 三处。
- **v1.4.1 (2026-08-17)**:§5 新增驱动审计实战经验: ① `/proc/modules` 格式是 `name size refcount used_by [state]`, **第3字段(used_by)常为 `-` 不是数字**, 用 `^(\S+)\s+(\d+)\s+(\d+)\s+\S+` 匹配(第3字段用 `\S+`), 之前用 `\d+` 导致全部行被 continue 跳过→检查数恒为 0; ② Linux 内核模块文件路径只能通过 `modinfo -n` 获取(容器常无 modinfo, 需 `Get-Command modinfo` 探测后优雅降级); ③ 已知恶意模块名单靠文件名匹配即可(不必哈希), 正常模块(ext4/veth/xt_CT)不误报; ④ 驱动/模块审计是慢操作, 主扫描默认只做"已加载"快速检查, 全量(DriverStore/全模块)留给 `/drivers` 独立模式; ⑤ 版本号硬编码在 START 留痕里, 升版本必须同步改(曾漏改导致留痕显示旧版)。
- **v1.4.0 (2026-08-17)**:§5 新增操作留痕(统一审计)实战经验: ① **被全脚本引用的函数(如 Write-AuditLog)必须定义在脚本最前部**(环境准备后), 否则参数解析等前置代码调用时函数未定义→静默失败; ② 后台 Runspace 拦截/处理的事件不会经过主线程函数, 统一审计必须在 **Stop-ShutdownGuard 汇总循环里补写**; ③ 统一审计日志类型标签用英文大写(START/EXIT/MODE/SCAN/IOC/QUARANTINE/INTERACTIVE/SHUTDOWN/ERROR)便于 grep; ④ EXIT 留痕要放在 Stop-ShutdownGuard 之后写, 保证日志顺序 SHUTDOWN→EXIT; ⑤ 审计日志文件要加入 Test-ToolSelfFile 保护列表(防零信任模式误报自身日志); ⑥ `$env:USER` 在 Linux 有值、Windows 为空, `$env:USERNAME` 反之, 跨平台取用户名用 `if($env:USER){$env:USER}else{$env:USERNAME}`。
- **v1.3.1 (2026-08-17)**:§8 新增 Python 写 bat 的转义陷阱: 普通字符串里 `\v` 被解析为垂直制表符(0x0b)、`\7` 被解析为八进制 BEL(0x07), 写进 bat 的 Windows 路径 `PowerShell\v1.0`、`PowerShell\7\pwsh.exe` 会变成控制字符; **对策: 写含 Windows 路径的代码块必须用 raw 字符串 `r"""..."""`**, 写完用 `{b for b in data if b<0x20 and b not in (0x09,0x0a,0x0d)}` 校验无控制字符; 事后 replace 控制字符只能救回字符救不回被吃掉的 `\`; 整块替换 CRLF 文件用「锚点定位 + 切片替换」比整串 replace 稳。
- **v1.3.0 (2026-08-17)**:§5 新增关机拦截实战经验: ① `$ShutdownGuard` 顶层赋值在 `[scriptblock]::Create` 内存加载下函数内 `$script:ShutdownGuard` 读到空→**参数解析段必须用 `$script:VarName` 赋值**;② 后台 Runspace 跨线程不能调主线程函数→**在 Runspace 内直接完成 kill+写日志**, 主线程只做汇总;③ Runspace 写的日志路径和主线程读的路径必须一致(把 `$logDir` 通过 `SetVariable` 传入 Runspace);④ `/proc/<pid>/cmdline` 是 NUL 分隔的字节流, `ReadAllBytes` 后不能直接 `-replace` (byte 数组不支持), 要先 `[Text.Encoding]::UTF8.GetString($raw)` 再 replace;⑤ Linux pwsh 的 `Start-Process` 不支持 `-WindowStyle` 参数(跨平台坑);⑥ 审计日志用正则汇总时 `(.*)` 贪婪匹配在"路径=... 命令行=..."格式下能正常工作(验证过)。
- **v1.2.0 (2026-08-17)**:§5 新增 3 条实战教训: ① 进程匹配会误杀自身启动链(命令行含目标路径)→ 排除 $PID/工具名;② 函数内 $args 是函数参数(空!), 脚本参数用 $script:PathArgs 传;③ 模式分支若调用自定义函数, 分支必须放在函数定义之后(函数定义顺序坑)。
- **v1.1.0 (2026-08-17)**:新增 §0 持续更新协议;§3 补充 Write-Host 参数模式/表达式模式陷阱;新增 §8 文件编辑与 shell 环境坑(zsh glob、CRLF 替换失败、行级编辑、Write 工具重读)。
- **v1.0.0 (2026-08-17)**:初版,整合 v1.0-v1.29 + Linux 版全部经验。

## 1. 编码与行尾(闪退/乱码的根源)

| 问题 | 现象 | 正确做法 |
|---|---|---|
| bat 文件用 UTF-8 但 cmd 默认 GBK | 中文 echo 乱码、命令找不到、闪退 | **中文 Windows 上 bat 存 GBK**(原生代码页 936),不依赖 chcp |
| bat 加 UTF-8 BOM | **cmd 跳过第一行** → `@echo off` 失效 → 回显模式 | **bat 绝不要 BOM** |
| bat 用 LF 行尾 | 部分 Windows 解析失败、闪退 | **bat 必须 CRLF** |
| `chcp 65001` | 部分系统解析器 bug,中文路径下直接退出 | 中文系统不需要 chcp,直接用 GBK |
| ps1 编码 | PowerShell 按 BOM 识别 | **ps1 用 UTF-8 带 BOM** + CRLF |
| **引擎 `Console.OutputEncoding=936` 与 bat `chcp 65001` 冲突(v1.43 实战)** | PS 子进程按 GBK 编码输出,cmd 按 UTF-8 解码 → 退出段满屏符号乱码(♥♡❤☺♦♣♠•◘○) | 引擎头部**先设 UTF-8**,仅当系统 CodeSet 非 UTF-8 才回退 936 |
| **Python 文本模式写 bat 破坏 CRLF(v1.46/1.47 连踩两次!)** | Linux 上 `open(p,'w').write()` 把 `\n` 当行尾 → bat 全部变 LF → Windows 打不开/标签错乱/乱码 | **写 bat 必须 `open(p,'wb')` 二进制模式 + 手动 `\r\n`**,写完校验 `d.count(b'\r\n') == d.count(b'\n')` |

**验证技巧**:Linux 上检查文件字节:
```bash
file foo.bat foo.ps1                          # 看编码
head -c 3 foo.bat | od -An -tx1               # 看是否有 BOM (ef bb bf)
python3 -c "print(open('x.bat','rb').read().count(b'\r\n'))"  # 行尾
```

## 2. cmd 批处理陷阱

1. **括号块内裸括号必崩**:`echo 是否申请权限? [Y=是(弹UAC)]` 中的 `(弹UAC)` 被 cmd 当嵌套块 → 语法崩溃闪退。
   **对策**:整个 bat 用 `goto` 跳转结构,不用 `if (...) else (...)` 括号块;提示文字避免裸 `()`。
2. **`powershell.exe` 可能不在 PATH**:`where powershell` 找不到不代表没装。
   **对策**:多路径探测:
   ```bat
   set "PS_PATHS=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe;%SystemRoot%\SysWOW64\WindowsPowerShell\v1.0\powershell.exe;C:\Program Files\PowerShell\7\pwsh.exe"
   for %%P in ("%PS_PATHS:;=" "%") do ( if exist "%%~P" set "PS_EXE=%%~P" & goto PS_FOUND )
   ```
3. **`for /f` + 反引号 + 嵌套引号**解析错误(usebackq 也踩坑)。
   **对策**:版本号等简单输出用临时文件:
   ```bat
   "%PS_EXE%" -NoProfile -Command "Set-Content $env:TEMP\ver.txt $PSVersionTable.PSVersion.ToString()"
   if exist "%TEMP%\ver.txt" ( set /p VER=<"%TEMP%\ver.txt" & del /q "%TEMP%\ver.txt" )
   ```
4. **`set /p` 读文件乱码**:PS 输出的 UTF-8 文本被 `set /p` 按 GBK 读 → 乱码。
   **对策**:用 `for /f "usebackq tokens=*" %%a in (\`命令\`) do set "VAR=%%a"` 直接捕获 stdout,绕开文件。
5. **UAC 提权后 `exit /b` 闪退**:`Start-Process -Verb RunAs` 返回 0 但实际没拉起新进程时,原进程退出窗口消失。
   **对策**:UAC 失败降级继续;或干脆让用户右键"以管理员身份运行",不自动提权。
6. **中文 bat 文件名没问题**:Windows 文件名 UTF-16,含中文不影响;但**bat 内容**编码要按第 1 节处理。
7. **`cmd start` 第一个引号参数被当窗口标题(v1.47 实战,致命)**:`cmd /c start /B /MIN "pwsh.exe" -NoProfile -File x.ps1` → 第一个引号参数 `"pwsh.exe"` 被 `start` 当成**新窗口标题**,`-NoProfile` 被当成**要执行的命令** → 弹窗"Windows 找不到文件 -NoProfile"。
   **对策**:必须加**空标题参数**:`cmd /c start "" /B /MIN "pwsh.exe" -NoProfile ...`;并建议用 `.NET Process`(`StartInfo.Arguments` 字符串按字面传)替代 `Start-Process -ArgumentList` 数组(PS 5.1/7 对空字符串元素/引号元素拼接行为不一致,易产生双引号嵌套)。
8. **`%PS_EXE%` 空时 `"%PS_EXE%" -NoProfile` → "找不到文件 -NoProfile"**:变量未定义时展开为空字符串 → cmd 把 `-NoProfile` 当要执行的文件 → 弹窗误导。
   **对策**:**PS_EXE 空值断言**——`if not defined PS_EXE goto FATAL_NO_PS` 并 `exit /b 4` 给明确排查提示,绝不继续往下执行。
9. **bat 找 PowerShell 只列固定路径不够**:用户可能通过 scoop/choco/商店/用户目录安装。
   **对策**:**多源搜索** = `where pwsh`/`where powershell`(PATH) + 常见安装位置 + `%LOCALAPPDATA%\Microsoft\WindowsApps\pwsh.exe`(Win11 商店版) + **实际可执行验证**(`"%PS_EXE%" -NoProfile -Command "$null"` 失败则清空)。主流程与子工具流程**两处候选路径必须一致**。

## 3. PowerShell 5.1 / 7 兼容性(最深的坑)

| 坑 | 说明 | 对策 |
|---|---|---|
| **变量名不区分大小写** | `$H`(哈希表)和 `$h`(循环变量)是同一个变量!循环给 `$h` 赋字符串后 `$H[$h]` 崩 "Unable to index" | 变量名避免仅大小写不同的两个变量;用 `$tbl`/`$hv` 等清晰命名 |
| **param 必须第一行** | param 前有任何语句(含注释外的初始化)都报 "无法将 param 识别为 cmdlet" | `param(...)` 必须在 BOM 后第一行 |
| **trap 触发时函数未定义** | trap 从脚本开始就生效,若在函数定义前抛错,trap 内调用该函数 → "not recognized" | **Exit-Tool 等关键函数定义移到脚本最前面**(banner 前) |
| **`GetEncoding(936)` 在 .NET Core 崩** | Linux/pwsh 无此代码页 → 终止性异常 | 先 `[Text.Encoding]::RegisterProvider([Text.CodePagesEncodingProvider]::Instance)` 再 GetEncoding,整体 try/catch 兜底 UTF-8 |
| **字符串拼接里的 `(if(...){...}else{...})`** | PS 5.1 解析为命令调用 → "无法将 if 识别为 cmdlet" | 先 `$s = if(...){...}else{...}` 赋值,再拼接 `$s` |
| **`Set-Content -Encoding ASCII` 丢中文** | 中文变 `?`,若内容被签名则签名不匹配 | 写文件前对内容做 ASCII 净化(`-replace '[^\x20-\x7E]','_'`),再计算签名 |
| **Write-Host 拼接不加括号** | `Write-Host "a" + $x + "b"` 中 `+` 被当参数输出 | **所有拼接加括号**:`Write-Host ("a" + $x + "b")` |
| 单行 `return @{...}` | PS 5.1 偶发 `] expected` 解析错误 | 拆多行,或干脆去掉无用的返回值 |
| 单行 `Register-EngineEvent -Action {...}` | scriptblock 解析陷阱 | 不用或拆多行 |
| `byte[]` 索引 + `-bxor` | PS 5.1 内部错误 | 用 `[int]` 中间值 + `[byte]` 转换,或改用纯 .NET(SHA256) |
| **Add-Type C# 块含杀软敏感 API(v1.45 实战)** | 源码明文 `[DllImport("kernel32.dll")]`/`OpenProcess`/`NtSetInformationProcess`/`ReadProcessMemory` 触发杀软启发式误报 | **C# 块整体 base64 编码运行时解码**:`Add-Type -TypeDefinition ([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('...')))`;注意**双引号 `@"..."@` 与单引号 `@'...'@` 两种 here-string 都要处理**;方法调用 `[Cls]::Api(...)` 无法混淆(改了就调用不了),但杀软对方法调用权重低 |
| **默认交互/无人值守开关(v1.43 实战)** | 交互确认只在显式 `/interactive` 时弹,普通用户扫完直接退 | 默认(`$AutoAsk=$true`)有文件类高危就弹;`/noask` 关闭走无人值守 |

## 4. 跨平台(Linux/pwsh)坑

1. **`$env:TEMP` / `$env:USERPROFILE` 在 Linux 为 null**:`Join-Path $null` → 参数绑定异常。
   **对策**:开头兜底:
   ```powershell
   $script:EnvTmp  = if ($env:TEMP) { $env:TEMP } elseif ($env:TMP) { $env:TMP } else { [System.IO.Path]::GetTempPath() }
   $script:EnvUser = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
   ```
2. **FIFO/管道文件 OpenRead 挂起**:`/tmp/clr-debug-pipe-*.in` 等 Length=0 的 FIFO,`[IO.File]::OpenRead` 阻塞。
   **对策**:读文件头前 `if ($f.Length -ge 2)`,0 字节文件直接跳过。
3. **Windows 专有 cmdlet 不存在**:`Get-CimInstance`/`Get-AuthenticodeSignature` 在 Linux 抛 CommandNotFoundException(终止性)。
   **对策**:模块级 try/catch 包裹,Linux 用 `/proc` 读进程、`ss` 读网络、目录白名单代替签名验证。
4. **进程枚举**:Linux 用 `Get-ChildItem /proc -Directory | ? Name -match '^\d+$'`,读 `cmdline`(NUL 分隔,`-replace "\`0"," "`)。

## 5. 检测/安全工具最佳实践(本项目模式)

- **双文件架构**:`.bat`(GBK/CRLF/无BOM/纯逻辑) + `.ps1`(UTF-8 BOM/引擎)。启动器永不闪退:`pause` 兜底 + 三步留痕(bat日志 + PS调试日志 + 报告)。
- **日志放工具目录,不放 `%USERPROFILE%`**:OneDrive 桌面重定向后用户找不到 `%USERPROFILE%` 下的文件。用 `$toolRoot = Split-Path (Split-Path $PSCommandPath -Parent) -Parent`。
- **统一受控退出**:`Exit-Tool` 函数统一 exit,写"正常退出标记"(明文+SHA256 签名,防伪造;**签名必须基于写入文件的最终内容**,中文先净化)。
- **文件扫描性能**:先文件名启发式(零 IO)→ 缓存命中检查(`大小|修改时间` 做键)→ RunspacePool 多线程算哈希(单次读流同时 SHA256+MD5)→ 缓存持久化(C 盘 `%LOCALAPPDATA%` + 工具目录双写)。
- **全格式恶意文件检测**:不要按扩展名过滤!枚举全部文件,读文件头判断 `MZ`(Windows PE)/`ELF`(Linux),图片/无扩展名伪装 → 高危;正常格式不误报。
- **误报控制**:白名单(签名者/目录/路径/名称)+ 数字签名验证 + 观察清单(与高危分开)。规则宁严勿宽,默认只报告不隔离。
- **启发式高危判定必须先查白名单/签名(v1.43 实战)**:`Hidden|PE` 直接报高危不查 `Test-Whitelist`/`Test-TrustedSigner` → Bcut/Inno Setup 等合法软件 dll 误报(实测必剪 3 个 dll 全中)。**隐藏属性单独不构成威胁证据**,应降级"观察";`PE+无扩展名/图片伪装` 等强特征也要先过签名/目录白名单再报。
- **进程防杀三层(v1.44 实战)**:① 进程 DACL 移除 Everyone/Users 的 PROCESS_TERMINATE(非管理员 taskkill → Access Denied,`SetKernelObjectSecurity` + SDDL `O:SYG:SYD:(A;;GA;;;SY)(A;;GA;;;BA)`);② **watchdog 双进程守护**: 引擎被杀自动重启——判定依据=**进程消失但 `sf_running.flag` 仍在 → 被 kill**(引擎正常退出会删标记);单实例互斥(命名 Mutex/锁目录+PID)防重启堆积;连续 5 次停止防死循环;③ `/bruteprotect` 硬保护: `NtSetInformationProcess(ProcessBreakOnTermination=29)` → 被用户态 kill 直接蓝屏 0xDEADDEAD,默认关闭(威慑恶意软件)。
- **watchdog spawn 要脱离父进程**:`Start-Process -WindowStyle Hidden` 启动的进程是引擎子进程,引擎被 kill 时(进程树被杀)watchdog 连带终止。用 `cmd /c start "" /B /MIN <cmd>`(注意空标题 `""` 见 §2-7)+ `.NET Process` 传参。
- **Job Object 进程树清理 + UAC runas 的互斥(实战,对应 SilverFox Detector v2.15.2/v2.15.5)**:① **清理残留的标准做法**:把启动的引擎进程(及子进程)放进一个 Job Object,设 `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE(0x2000)`;父进程退出时 OS 自动关闭 job 句柄 → 整棵引擎进程树被一并终止。孙进程默认继承父进程的 job(除非显式 `CREATE_BREAKAWAY_FROM_JOB`);② **关键限制**:被 `ShellExecute("runas")` 提权的子进程会**脱离父进程的 Job Object**(等同 breakaway),父进程的 job 再也管不到它 → 父退出时无法回收,只能 best-effort `taskkill`(且提权子进程权限≥父时父往往无权结束,清理必败);③ **彻底解法**:不要 runas 单个子进程,而是**用 runas 重启整个父程序自身**并带一个内部标记(如 `--elevated-run <mode>`),让新实例以提权令牌运行、其 spawn 的引擎留在**新实例自己的 Job Object** 内——新实例退出时 OS 回收其整棵引擎树,无残留;④ **配套铁律**:runas 重启的实例必须**阻塞存活到引擎结束**再退出(轮询记录的 PID 是否全消失),否则 job 句柄一关就 KillOnJobClose 把刚启动的引擎也杀了;⑤ **标记风格统一**:内部标记用双杠 `--elevated-run` 而非单杠 `/elevated-run`,Go 的 `os.Args` 解析 `CommandLineToArgvW` 原样保留,单杠易与 `/path` 参数混淆导致匹配失败;空模式要兜底成 `""`(如普通按钮不带模式),避免 `i+1` 越界。
- **交互式处理**:`/interactive` 参数,检测后列出文件类可疑项,用户序号选择 → 二次确认 → 强制隔离(隔离函数加 `-Force` 开关,默认不移动)。**v1.43 起默认有高危就弹**,`/noask` 关闭。
- **PPL 降级近似自保护(用户态三件套,实战,对应 SilverFox Detector v2.15.6)**:① **真 PPL 走不通的原因**: `PsProtectedSignerAntimalware` 等内核级保护需**微软反恶意软件(ELAM)认证签名**; 普通 Authenticode 证书签的 exe, 内核不会以 Antimalware signer 级别接纳(`NtSetInformationProcess(ProcessProtectionInformation)` / `PROC_THREAD_ATTRIBUTE_PROTECTION_LEVEL` 被拒或启动失败), 纯用户态无法做真 PPL; ② **降级近似(无需特殊证书, 普通进程即生效, 全部 best-effort)**: (a) **进程缓解策略** `SetProcessMitigationPolicy`(kernel32 动态 `NewProc`, 对**自身**有效) / 对**子进程**用 `NtSetInformationProcess`(同名 class 值, 因为 SetProcessMitigationPolicy 仅对自身) —— 设 `ProcessDynamicCodePolicy`(禁动态代码/防 shellcode 注入) + `ProcessSignaturePolicy`(仅微软/Store 签名 DLL, 防侧载) + `ProcessImageLoadPolicy`(禁远程/低 IL 镜像) + `ProcessStrictHandleCheckPolicy`; (b) **MIC 提升** `SetTokenInformation(TokenIntegrityLevel)` 提到 **High(S-1-16-0x3000)**, 低 IL 进程无法 OpenProcess(取 High 不取 System, 避免 GUI/COM 异常); (c) **去特权** `AdjustTokenPrivileges` 禁用 `SeDebugPrivilege`(降 Token 被劫持价值); ③ **Go 落地必坑**: `GetCurrentProcessToken()` 默认仅 `TOKEN_QUERY`, 设 IL 需 `TOKEN_ADJUST_DEFAULT`、调特权需 `TOKEN_ADJUST_PRIVILEGES` → 必须 `OpenProcessToken` 显式打开带对应访问权的 Token, 否则静默失败; `TOKEN_MANDATORY_LABEL` 与该包未导出的 IL RID 常量(`SECURITY_MANDATORY_HIGH_RID=0x3000`)需自行定义; ④ **与真 PPL 的差距(务必向用户说清)**: 这些是 Ring3 措施, 拥有 SeDebugPrivilege 的管理员理论上仍可绕过(动态代码策略对跨进程写入拦截不如 Ring0 强制彻底); 真 PPL 是内核强制, 签名级别不够的进程连 OpenProcess 句柄都拿不到; 降级近似显著抬高攻击成本、挡普通恶意软件, 但**非**"管理员也无法操作"; 取得 ELAM 认证后可在此三层之上补真 PPL(需配套 ELAM 驱动)。
- **进程匹配防误杀(实战)**:`Get-RelatedProcesses` 按命令行匹配目标路径时,**会匹配到工具自身的启动链**(zsh/cmd 命令行里含该路径)→ 把自己杀了。必须:排除 `$PID` 自身、排除命令行含工具名(`SilverFoxDetect`)的进程。
- **进程与线程监控(A+B + 先识别再反制,实战,对应 SilverFox Detector v2.15.7)**:① **监控所有进程的创建/结束**: A=Toolhelp 快照轮询(`CreateToolhelp32Snapshot`+`Process32First/Next`, 每~1.5s 差集出新/退进程, 轻量无需特权, **作主源**); B=ETW 实时(`OpenTrace`+`EnableTraceEx2` 订阅 `Microsoft-Windows-Kernel-Process`+`ProcessTrace`)延迟更低, 但**实时会话需管理员、Wine 无内核提供者** → best-effort, 起不来就 `recover` 回退 A; ② **反制前必判"是什么程序"(铁律!)**: 绝不能见可疑就杀, 否则误伤正常软件(更新器/安装包/崩溃报告/任务管理器); 采集 镜像路径/父进程/代码签名(`WinVerifyTrust`+`CryptQueryObject` → Microsoft/有效/无效/未签名)/路径启发(是否 System32 vs temp·appdata)/冒充(系统进程名却不在 System32)/父链(父是浏览器·Office·脚本宿主却拉起未签名 exe); 仅"签名缺失/无效 + 异常组合"才判可疑; ③ **终止型工具白名单**: taskkill/powershell/ProcessHacker/PCHunter/taskmgr 等 —— **仅当该工具本身非 Microsoft/有效签名才反制**, 签名正常的系统工具不误杀(签名校验天然挡住合法 MS 工具); ④ **反制手段**: 对"终止型+未签名"进程主动 `TerminateProcess`(自身 High IL 对低 IL 目标有权), best-effort, IL 不足则失败忽略; 自身被终止由看门狗自愈; ⑤ **Go 落地坑**: x/sys/windows v0.15.0 **未封装** Toolhelp/ETW/WinVerifyTrust, 全靠 `NewProc` 动态加载 + 手搓结构体; `WINTRUST_DATA` 必须严格对齐 64 位布局(共 72 字节), 否则 `WinVerifyTrust` 越界读→签名判定失真/崩溃; ETW 回调用 `syscall.NewCallback` 转 `uintptr` 触发 go vet 的 unsafe.Pointer 误报(安全, 已知); ⑥ **性能**: 快照只记短名, 全路径 `OpenProcess` 仅对新进程惰性查, 避免每轮对全部进程 OpenProcess; ⑦ **与真"拦截终止"的差距**: 用户态无法直接 hook `TerminateProcess`, 本方案靠"终止型工具+未签名"启发识别潜在攻击者; 若要**内核级实时拦截别人对自己的 TerminateProcess**, 需 `ObRegisterCallbacks`(内核驱动+签名), 与 PPL/ELAM 同属认证投入。
- **函数内 `$args` 是空的(实战)**:`pwsh -File x.ps1 /ring0 /path` 时,脚本顶层 `$args` 有值,但**函数内 `$args` 是函数的参数(空)**。需要把脚本参数传给函数:参数解析时收集 `$script:PathArgs`,函数内用 `$script:PathArgs`。
- **调用函数的模式分支必须在函数定义后(实战)**:`/ring0` 分支在参数解析后直接 `Invoke-Ring0Delete` → "not recognized"(函数定义在后面)。**任何调用自定义函数的顶层分支,必须放在函数定义之后**(或把函数定义提前)。
- **隔离区/删除流程**:先停相关进程(仅匹配目标, 排除自身)→ 清持久化(注册表 Run/计划任务/服务; Linux: crontab/systemd/bashrc)→ 备份到隔离区(可回滚)→ 逐级提权删除(`Remove-Item`→`takeown+icacls`→SYSTEM 计划任务; Linux: `rm`→`chattr -ia`→`sudo`)。
- **哈希缓存防重复**:跨运行持久化,`大小|修改时间` 相同的文件直接复用,不重算。
- **调试 trap**:输出 `ScriptLineNumber` + `Line` 原文到屏幕和日志,用户贴日志即可定位。

## 6. 实测流程(Linux 沙箱验证 Windows 脚本)

即使目标是 Windows,也可以用 **Linux pwsh 实测**:
```bash
# 语法解析(找 ParserError,含行号列号)
pwsh -NoProfile -Command '[System.Management.Automation.Language.Parser]::ParseFile("x.ps1",[ref]$null,[ref]$e)|Out-Null; if($e.Count){$e|%{"L$($_.Extent.StartLineNumber):$($_.Extent.StartColumnNumber) $($_.Message)"}}'
# 实际运行(Windows 专有模块会优雅降级,但启动/退出/日志流程可验证)
pwsh -NoProfile -File x.ps1 /quick
```
- 安装 pwsh(Linux):GitHub 或清华镜像 `github-release/PowerShell/PowerShell/LatestRelease/powershell-*-linux-x64.tar.gz`。
- 注意:PS 7 比 5.1 宽容,语法通过≠5.1 兼容,第 3 节陷阱要主动规避。

## 7. 交付检查清单

- [ ] bat:GBK 编码、CRLF、无 BOM、无裸括号、goto 结构、`pause` 兜底
- [ ] bat:PS_EXE 多源搜索 + 可执行验证 + 空值 FATAL 断言(防"找不到文件 -NoProfile")
- [ ] bat:Python 修改后**二进制写回 + CRLF 数校验**(`wb` 模式,`d.count(b'\r\n')==行数`)
- [ ] ps1:UTF-8 BOM、param 第一行、关键函数提前、trap 输出行号
- [ ] 跨平台:`$env:TEMP/USERPROFILE` 兜底、FIFO 跳过、模块级 try/catch
- [ ] 编码:签名内容 ASCII 净化、Write-Host 拼接加括号、OutputEncoding 与 bat chcp 一致
- [ ] 性能:启发式优先、哈希缓存持久化、多线程
- [ ] 误报:启发式高危判定前查白名单/签名;隐藏属性单独降级观察;默认有高危弹交互
- [ ] 自保护:DACL + watchdog(独立进程 + 单实例 + 连续重启上限) + 关闭次数记录(sf_kills.log, 2分钟内被关闭≥5次→关闭风暴告警); 内核驱动源码(sfguard.sys 等)保留于 bin/ExtremeProtect.ps1 + bin/drivers/, 如需复用直接调用(见 §5)
- [ ] 杀软误报:Add-Type C# 块 base64 编码,源码无 DllImport/敏感 API 明文
- [ ] 日志:工具目录 + 调试 trap
- [ ] manifest:改任何文件后重算 SHA256 + 整清单重签(salt 固定)
- [ ] 打包:zip 文件名带新版本号(防下载缓存),`unzip -p` 抽查包内 bat CRLF/版本
- [ ] **GUI 程序启动 bat: 必加 `cmd /c start "" "<bat_path>"` + `CREATE_NEW_CONSOLE=0x10`(见 §9), 否则控制台窗口不弹**
- [ ] 用 pwsh 语法解析 + 实跑一遍

## 8. 文件编辑与 Shell 环境坑(开发过程本身)

这些不是脚本运行时的坑,而是**在 Linux 沙箱里编辑 Windows 脚本时**踩的,同样值得沉淀:

1. **Python `str.replace` 与 CRLF 不匹配**:用 Python 读文件后 `t.replace(old, new)`,若 `old` 是 LF 字符串而文件是 CRLF,替换**静默失败**(不报错,只是没替换)。
   **对策**:不要用整串多行 replace;改用**单行锚点定位 + 行索引切片**(`lines[i]` 定位后 `lines[:i]+new+lines[i+1:]`),或用 `lines[i].rstrip('\r')` 比较。
2. **`t.split('\n')` 保留 `\r`**:CRLF 文件按 `\n` 分割后每行末尾带 `\r`,`lines[i] == '}'` 永远 False。
   **对策**:比较时用 `.rstrip('\r')`,或直接 `t.splitlines()`(自动处理 CRLF/LF)。
3. **定位函数闭合 `}` 用 `strip()` 会误伤**:`lines[i].strip() == '}'` 会把缩进的 `}`(如 `} catch {}` 内部块)当成函数闭合。
   **对策**:闭合判断必须**严格无前导空格**(`lines[i].rstrip('\r') == '}'`),或从已知函数体特征(如 `return $results`)向后找。
4. **zsh 通配符无匹配即报错**:`rm -f *.txt` 无匹配时 zsh 报 `no matches found` 并**中断整条命令链**(`&&` 后续不执行)。
   **对策**:`rm -f *.txt 2>/dev/null; true`,或 `setopt null_glob`,或避免在无文件时用 glob。
5. **Write 工具重写需先读**:文件被 linter/外部修改后直接 Write 会报 "File has been modified"。**先 Read 再 Write**,或删掉文件后重写。
6. **构造测试样本验证检测逻辑**:做检测类工具时,用几字节的伪样本(`MZ`/`\x7fELF` + 填充)验证规则是否命中,再验证正常文件(如 `\x89PNG`)不误报。测试完**必须清理**。
7. **版本号要三处同步**:PS1 banner、bat 横幅、待办文档——只改一处会导致用户误以为没更新(实测曾因 banner 还是旧版被误判)。
8. **Python `open(p,'w')` 文本模式写 bat = 灾难(v1.46/1.47 连踩两次,必修!)**:Linux 上 Python 文本模式会把 `\n` 写成系统行尾(Linux=`\n`),**CRLF bat 全变 LF** → Windows 打不开、goto 标签解析错乱、乱码。**任何修改 bat 的 Python 操作必须**:
   ```python
   raw = open(p,'rb').read()            # 二进制读
   d = raw.decode('gbk')                # 按 GBK 解码
   d = d.replace('\r\n','\n').replace('\n','\r\n')   # 统一 CRLF
   open(p,'wb').write(d.encode('gbk'))  # 二进制写, 绝不用文本模式!
   assert open(p,'rb').read().count(b'\r\n') == ...  # 写完验证 CRLF 数 = 行数
   ```
   ps1 用 LF 无碍(引擎 LF 正常),**但 bat 必须 CRLF**。
9. **打包 zip 文件名必须带新版本号**:同名 zip 会被用户下载器缓存,拿到旧包误以为"没打包/还是旧脚本"(实测 v1.45 zip 内容正确但用户下载到旧文件)。改版本号即换文件名,强制刷新缓存;交付前 `unzip -p` 抽查包内关键文件(bat CRLF/版本号/引擎混淆特征)确认。
10. **GUI 启动器(Windows Forms)要点**:控件布局超出窗口高度会被截断(按钮在 Y=785 窗口 720)→ 窗口设够大 + `AutoScroll=$true`;PowerShell 事件 scriptblock 闭包可访问函数局部变量(ShowDialog 阻塞期间变量仍在作用域),标准模式放心用;`Add-Type -AssemblyName System.Windows.Forms/System.Drawing` 每次运行幂等。
8. **先验证再批量**:一次改动多处时,先小范围验证语法再铺开;改完立刻 `pwsh` 语法解析 + 实跑,不要等到打包后。

## 9. Win32 GUI 程序启动 bat/ps1 子进程(2026-08-20 v2.12 实战)

**症状**:`GUI.exe`(纯 Win32 无 console, 用 `-H windowsgui` 链接器标志编译)里按按钮启动 `cmd /c xxx.bat`,**控制台窗口从未弹出,UI 状态栏也不更新,用户看到"点了没反应"**。无报错弹窗、无日志异常、exe 进程正常,看似什么也没发生。

**根因**:
1. GUI 程序**没有控制台**——进程启动时不带 console。
2. Go 的 `exec.Command("cmd.exe", "/c", "bat")` 默认 `SysProcAttr.CreationFlags = 0`,cmd.exe 被 CreateProcess 时 Windows 尝试让其**继承父进程 console**。
3. `AttachConsole(parent_pid)` 在父进程没有 console 时**失败**(返回 `ERROR_INVALID_HANDLE`)。
4. cmd.exe 不主动 `CREATE_NEW_CONSOLE` 就**没有任何窗口**——但 cmd.exe 进程能跑下去,bat 内容在内存里执行完,只是输出无处显示。
5. 用户感知 = 完全无反应。状态栏也"看起来不动"(因为卡在 bat 执行中, 但没有反馈)。

**对策(双保险,推荐并列)**:
```go
// 方案 A: cmd /c start "" "full_bat_path" args... (推荐)
//   - start 自身在新进程中启动 bat 并创建新控制台窗口;
//   - 第一个 "" 是 start 的窗口标题(必须存在,空串也行,见 §2.7);
//   - cmd.exe 立即退出, 但 bat 所在窗口保留(没有 /WAIT 标志).
args := []string{"/c", "start", "", fullBatPath}
if mode != "" { args = append(args, mode) }
cmd := exec.Command("cmd.exe", args...)

// 方案 B: 加 CREATE_NEW_CONSOLE 标志(0x10), 让 cmd.exe 自身强制新窗口 (双保险).
cmd.SysProcAttr = &syscall.SysProcAttr{
    HideWindow:    false,
    CreationFlags: 0x00000010, // CREATE_NEW_CONSOLE
}
cmd.Dir = filepath.Dir(fullBatPath) // 显式工作目录, 防诡异 cwd

// 关键日志: 启动前/后必须 logf + setStatus 双重反馈, 用户能看到反馈就排除"无反应".
logf("runSilverFox: 准备启动 bat=%s mode=%q", fullBatPath, mode)
setStatus("正在启动银狐检测引擎: %s ...", filepath.Base(fullBatPath))
if err := cmd.Start(); err != nil {
    msgBoxInfo("启动失败", err.Error()+"\n\nbat: "+fullBatPath)
    return
}
logf("runSilverFox: 已 Start cmd.exe pid=%d", cmd.Process.Pid)
setStatus("已启动 (独立控制台窗口): %s", modeLabel(mode))
```

**验证清单**:
- [ ] GUI 里点按钮, **控制台窗口必须立即弹出**(即便 bat 内容只有 echo)
- [ ] bat 完成的输出**在该窗口里完整可见**(不丢字符)
- [ ] GUI 进程本身**不阻塞**(`cmd.Start()` 而非 `cmd.Run()`)
- [ ] 状态栏在启动前/后各有一次反馈, 用户能感知"点对了,在转"
- [ ] 失败时弹 `msgBoxInfo` 显示 bat 完整路径, 一眼看出是否路径错

**易混淆陷阱**:
- `cmd /c bat` ≠ `cmd /c start "" "bat"`: 前者沿用父进程 console, 后者**强制新进程 + 新窗口**。
- Go 的 `HideWindow: false`(默认)只表示**不隐藏子进程**,不会帮你创建窗口 —— `CREATE_NEW_CONSOLE` 才是关键。
- 如果 bat 内有 `pause`,窗口会停留直到用户按键,这是好事(用户能看到结果);但**用户不知道按了会怎样** —— bat 末尾最好 `echo 完成,按任意键关闭...` 给提示。
- Go 的 `exec.Command(...).Run()` 会**阻塞当前 goroutine** 直到子进程退出 —— GUI 里必须用 `Start()` 异步。否则点完按钮整个 UI 卡死, 看起来"无反应"。

**与 §2.7 的关系**:v2.12 用了 `start "" bat`,而 §2.7 提到 `cmd /c start "" /B /MIN "..."` 强调"空标题必须"。这里没用 `/B /MIN`(那俩标志会**抑制窗口**!),GUI 程序需要的是**可见窗口**而非后台,窗口可见性比标题处理优先级更高 —— 把"如何启动可见窗口"和"如何不掩盖 start 标题问题"分开考虑。

**⚠️ 误诊更正 (v2.13 复盘)**:v2.12 据此改了 `CREATE_NEW_CONSOLE` + `start`,但用户实测反馈按钮**依然没反应**。日志复诊显示点按钮时**主窗口一条 `WM_COMMAND` 都没收到** —— 说明 v2.12 的方向完全错了:**控制台窗口弹不弹与"按钮点击能否被主程序处理"是两回事**。真正的"按钮无反应"根因见 **§10**,与 bat/控制台毫无关系。教训:**不要凭"看起来像"就改代码,先让用户贴启动日志,数 `WM_COMMAND` 是否进主窗口过程**。

## 10. Win32 子控件 WM_COMMAND 路由(容器窗口吞消息,2026-08-20 v2.13 实战)

**症状**:UI 正常显示,所有按钮肉眼可见(顶部切换按钮可用,功能按钮可见但**点击全部无反应**),日志里点按钮时没有 `WM_COMMAND` 记录,直接 `WM_CLOSE`。

**根因(经典 Win32 陷阱)**:
1. Win32 中,子控件(Button/Edit/List 等)点击触发 `BN_CLICKED`,**只把 `WM_COMMAND` 发给它的"直接父窗口"**(`GetParent(控件)`),**不会自动穿过多层父窗口冒泡到最外层**。
2. 本项目 v2.11 起了两个"页面容器" `pageDetect`/`pageTools`,把"启动银狐检测"等所有功能按钮**挂在容器下**(`CreateWindowExW(..., 父=pageDetect, ...)`),而容器用的是系统 **`Static` 类**(默认 `wndProc` = `DefWindowProc`)。
3. `Static` 的 `DefWindowProc` **收到 `WM_COMMAND` 后直接丢弃,不会转发给它的父窗口 `mainHwnd`** → 主窗口过程永远收不到 → `switch id` 永远不执行 → 按钮全死。
4. 顶部切换按钮(`tabBtnDetect`/`tabBtnTools`)因为是 `mainHwnd` 的**直接子控件**,`WM_COMMAND` 直达主过程,所以"看起来能用" —— 这点极具迷惑性,容易让人误判为"只是某个按钮坏了"。

**对策(自定义容器类转发,推荐)**:
```go
// 注册一个专用容器类, 其 wndProc 把 WM_COMMAND/WM_NOTIFY 转发给主窗口.
var containerWndProcCb = syscall.NewCallback(containerWndProc)
func containerWndProc(hwnd windows.HWND, msg uint32, wp, lp uintptr) uintptr {
    if msg == WM_COMMAND || msg == WM_NOTIFY {
        if mainHwnd != 0 {
            procSendMessageW.Call(uintptr(mainHwnd), uintptr(msg), wp, lp)
        }
        return 0
    }
    r, _, _ := procDefWindowProcW.Call(uintptr(hwnd), uintptr(msg), wp, lp)
    return r
}
// 注册: wc.LpfnWndProc = containerWndProcCb; wc.LpszClassName = utf16Ptr("SFContainer")
// 创建容器: CreateWindowExW(..., utf16Ptr("SFContainer"), ..., 父=mainHwnd, ...)
```
- 转发时 **`wParam`(控件 ID + 通知码)、`lParam`(控件 hwnd)原样保留**,主过程 `id := LOWORD(wParam)` 照常识别,无需改动。
- 其余消息(`WM_PAINT`/`WM_SIZE`/鼠标)继续走 `DefWindowProc`,容器照常工作。

**替代方案(不用容器,直接挂 mainHwnd)**:把所有按钮的父窗口直接设为 `mainHwnd`,切页时用 `ShowWindow` 逐个显隐 + 坐标自己加页偏移。优点是不需要转发;缺点是布局/显隐逻辑要手写,控件多了易错。本项目已选"容器 + 转发"方案。

**验证清单**:
- [ ] 启动日志里应出现 `SFContainer 类注册成功 atom=...`
- [ ] 点功能按钮,日志必须打印 `WM_COMMAND id=10xx code=0`(10xx 为按钮 ID)
- [ ] 顶部切换 + 小工具页所有按钮都能触发对应动作
- [ ] 不要再出现"只有顶层按钮能用"的偏科现象

**易混淆陷阱**:
- "按钮可见 ≠ 按钮能点"。可见只是 `WS_VISIBLE`,能否触发逻辑取决于 `WM_COMMAND` 能否到达处理它的 `wndProc`。
- 容器用 `Static`/`Button` 等**系统类**时,它们自带的过程**不会**帮你转发命令;只有你自己的主窗口类(或上面这种自定义转发类)才处理。
- 排查顺序:**先看日志有没有 `WM_COMMAND`** → 没有就查父窗口链 → 发现中间有系统类容器就必杀转发。这是比 §9(控制台)更隐蔽、更常见的"按钮无反应"真因。

## 11. bat `if (echo ...(...))` 嵌套括号陷阱(2026-08-20 v2.14 实战)

**症状**:`GUI 启动 bat 后窗口弹出, 只显示一行 banner + `此时不应有 X。` 就立刻退出到 cmd 提示符, 整个 bat 没跑完`。
- `X` 是 CMD 解析器在不该出现的位置撞到的下一个 token;`此时不应有 X` 是 cmd.exe 系统消息(8000 类), 含义 = "X 在此位置不应出现(语法错误)"。

**根因(CMD 解析器对 if-body 的括号配对追踪)**:
```bat
if "%%LANG%%"=="zh" (echo   银狐木马 (SilverFox) 检测工具 v1.55) else (echo   SilverFox Detector v1.55 - GUI mode)
```
- 父级是 `if X (cmd1) else (cmd2)` 复合语句, CMD 解析器在读 `(cmd1)` 时需要追踪配对的 `)`, **以简单括号计数实现, 不做字符串/上下文感知**。
- 读到 `echo   银狐木马` 时一切正常;读到 `(SilverFox)` 里的 `(` 时, **计数器 +1**(以为开新嵌套块);读到 `(cmd1)` 收尾的 `)` 时, 计数器归零但 cmd 解析器认为这个 `)` 关闭的是嵌套块;接着它看到 `检测工具`, 这时 cmd 解析器**正等一个能结束 if-then 体的东西**(应该是另一个 `)`), 撞到 `检测工具` token → 报 `此时不应有 检测工具。` 并立刻终止整个复合语句。
- 同理, `TOOL_DIAG` 段标题 `(echo   SilverFox 诊断工具 v1.55 (集成模式))` 也有这个 bug(`(集成模式)` 嵌套)。

**对策(用方括号/其他无语法意义字符替代嵌套圆括号)**:
```bat
:: 错 (嵌套括号触发 CMD 解析器 bug):
if "%%LANG%%"=="zh" (echo   银狐木马 (SilverFox) 检测工具 v1.55) else (echo   SilverFox Detector v1.55 - GUI mode)

:: 对 (方括号对 CMD 解析器无特殊含义, 纯字面量):
if "%%LANG%%"=="zh" (echo   银狐木马 [SilverFox] 检测工具 v1.55) else (echo   SilverFox Detector v1.55 - GUI mode)
```
- 也可用 `<SilverFox>`、`` `SilverFox` ``、`SilverFox` (无包围符), 只要不用 `(` `)`。
- 整个 if-then-else 都不要在 echo 字符串里写括号, 包括 `(集成模式)`、`(默认)`、`(默认)` 等。

**安全 vs 不安全场景**:
- ✅ **安全**: `echo (literal) text` —— echo 是**平级**命令, 不在 if-body 复合块内, `(` `)` 是字面量。
- ✅ **安全**: `echo 工具目录自身也检测` —— 完全没有括号。
- ❌ **不安全**: `if "cond" (echo 工具 (SilverFox) 检测工具) else (...)` —— 嵌套在 if-body 的 echo 里有 `(`。
- ❌ **不安全**: `for /f "tokens=1-3" %%A in ('cmd (内嵌括号)') do ...` —— for 体内也做括号计数。

**顺手清理的另一坑(同次发现)**:
- bat 文件历史行尾污染:某些行有 `\r\r\n`(CR-CR-LF 双 CR), 是历史编辑器/Linux pwsh 处理 CRLF 不当造成的。`file` 命令会报 "with CRLF, CR line terminators", Windows cmd 虽能容忍, 但非标准。**修复时用 Python 一次性规范化: `raw.replace(b'\r\r\n', b'\r\n')` + `re.sub(rb'(?<!\r)\r(?!\n)', b'', raw)`**, 然后回写。验证用 `raw.count(b'\r\r\n')` 应为 0, `raw.count(b'\r\n')` 等于行数, 孤立 `\r` 应为 0。

**验证清单**:
- [ ] bat 单独双击也能正常跑到末尾(或预期的 pause 等待点), 没有语法错
- [ ] GUI 启动 bat 后窗口完整弹出, 不再报 `此时不应有 X。`
- [ ] bat 行尾统一 `\r\n` (`file <bat>` 应只报 "CRLF line terminators", 不能再含 "CR line terminators")
- [ ] 修复后用 `grep -nP 'if [^()]*\(echo.*\(' <bat>` 全局扫一遍其他可能的同类陷阱

**易混淆陷阱**:
- 排查顺序: **GUI 启动 bat 弹窗报错 → 截图/复制完整 bat 错误信息 → grep bat 文件, 看 if-body 内 echo 是否含嵌套 `(` `)`**。比 §9 控制台更隐蔽(弹窗有了但内容错), 比 §10 WM_COMMAND 路由更罕见但同样"看起来像 exe 的问题"。
- 不要"以为"是 exe 没传对参数: `start "" "<bat>"` 不带额外参数时 `%~1==""` 走 GUI_MODE 是正确的, 问题不在 exe 在 bat 自身。
- 用 `[ ]` / `< >` / 空白 替代括号, 不要用 `" "` (引号在 bat 里会脱掉特殊字符, 可能引入新问题)。

## 12. 用 Wine + xvfb 在 Linux 沙箱验证 Windows GUI 程序(2026-08-20 v2.12~v2.14 实战)

**为什么做**: 没有真机 Windows, 但能验证 Windows GUI 程序能否启动、资源是否正确嵌入、WM_COMMAND 按钮路由(§10)是否生效、bat 能否被解析(§11 类语法错)。比纯静态审计强得多 —— 真能跑起来看到窗口/日志。

**安装(Ubuntu 22.04)**:
- `apt-get install -y wine` 装的是 `wine` 启动器(元包指向 wine-stable), **没有独立 `wine64` 二进制**, 别用 `wine64` 命令(会 not found)。直接用 `wine`。
- GUI 程序需要 X 显示: `apt-get install -y xvfb xdotool`。
- 首次跑创建 `~/.wine` prefix, wine 9.0 默认尝试 WoW64(报 `syswow64\rundll32.exe c0000135` 缺 DLL), **与你的 exe 无关**, 配置仍完成、程序照常启动。可 `export WINEDLLOVERRIDES="mscoree,mshtml="` 跳过 .NET/IE 弹窗, `WINEDEBUG=-all` 静音。

**验证程序启动 + 资源/布局**:
```bash
Xvfb :99 -screen 0 1280x800x24 &   # 后台虚拟显示
export DISPLAY=:99 WINEDEBUG=-all WINEDLLOVERRIDES="mscoree,mshtml="
cd <解压目录>
timeout 40 xvfb-run -a wine SilverFoxDetector.exe   # GUI 常驻, timeout 到点杀
cat SilverFoxDetector.log   # 看启动序列: 版本 / SFContainer 注册 / WM_CREATE / resizeChildren / 主窗口创建
```

**验证 WM_COMMAND 按钮路由(§10 修复关键)**:
- xdotool 在 wine 窗口内点击按钮坐标: `xdotool search --name "SilverFox Detector"` 找窗口 → `windowmove 40 40` → `getwindowgeometry` 拿屏幕位置 → **按钮客户区坐标 + wine 边框偏移(左≈3, 上≈23) = 屏幕坐标** → `mousemove` + `click 1`。
- 关键证据: 日志出现 `WM_COMMAND id=10xx code=0`。本次实测点"启动银狐检测" → `WM_COMMAND id=1030 code=0 (0x406, 0x0)` → `runSilverFox` 拉起 `cmd.exe pid=288`。**证明 v2.13 容器转发修复在真实运行环境生效**。

**验证 bat 语法(§11 嵌套括号)**:
```bash
cd legacy
wine cmd /c "银狐木马检测.bat"   # 无参 = GUI_MODE, 即 v2.13 真机报错分支
```
- 关键证据: **不再出现 `此时不应有 检测工具。`**, banner 正常打印(`SilverFox Detector v1.56 - GUI mode`)。本次实测确认 v2.14 修复在运行时有效。
- 噪声 `FINDSTR: /i ignored` 是 wine 的 findstr 不完整, 与修复无关。

**Wine 环境已知限制(不是程序 bug)**:
- Wine 没有 Windows PowerShell, 所以 bat 末尾 `call SilverFoxUI.ps1`(银狐检测真实引擎)在 wine 下会失败 —— **真机 Windows 有 pwsh 不受影响**。Wine 验证的是"程序能启动/按钮能点/bat 能解析", 不是"完整检测功能"。
- 中文 bat 文件名(GBK)在 wine 下能被映射(日志路径正常显示中文), 但 bat 内 GBK 中文 echo 在 wine cmd 下可能乱码, 不影响括号语法解析。
- 首次跑 wine 前缀 + 加载 exe 约 5-13s, 脚本里 `sleep 12` 等窗口出现。
- **`SetKernelObjectSecurity` 在 Wine 下会报"失败"(返回伪错误码 `<nil>`)** —— 这是 Wine 未完整实现进程 DACL 设置, **真机 Windows 成功**; 程序已标注"非致命, 不影响运行"。若日志出现此行, 不是 bug。
- **带自保护看门狗的程序, 多次测试间务必先清掉上一轮的看门狗/子进程**, 否则残留看门狗会重启 exe 并往同一日志写"FATAL: CreateWindowExW 失败"等**跨测试污染**(其实是无参重启的 Wine 时序假死, 非代码缺陷)。清场命令: `pkill -9 -f "SilverFoxDetector.exe"`(单独执行, 不要和 `pkill -f wine` 放在同一条命令里, 否则可能误杀正在跑的 xvfb/wine 导致 SIGKILL)。
- 验证内部标记分支(如 `--elevated-run`)时, 用 `wine SilverFoxDetector.exe --elevated-run /diag` 直接调, 日志会打印 `elevated-run 提权子实例: mode="..."` 与 `等待引擎进程树结束...`, 可确认分支命中与 `waitForEngineTree` 阻塞行为。

## 13. 提权子实例(--elevated-run)跳过 GUI 导致"双击无界面"(2026-08-22 v2.15.9 实战)

**症状**: 档2(`SilverFox.Heartbeat.exe`)/档3(`SilverFox.Hard.com`)双击后**没有 GUI 主窗口**(管理员或 UAC 关闭环境下尤甚); 档1(`SilverFox.exe`)双击正常出界面。

**根因(真机 Windows, Wine 看不到)**:
1. `main()` 对 `buildTier>=2` 在启动早期调 `ensureElevatedOrRestartTier()`, 未提权则 `ShellExecute("runas", ..., "--tier N --elevated-run")` 弹 UAC。
2. 用户接受 UAC → 新实例以管理员令牌启动, 参数含 `--elevated-run`(注意: 后面跟的是 `--tier N`, **不是 mode**, 所以 `mode` 解析为空串)。
3. `--elevated-run` 分支只做自保(`protectSelfDACL/hardenProcess/runIntegrityCheck/spawnWatchdog/...`)后直接 `runSilverFox("")` **启动检测引擎**, **整个分支从不调用 `winMain()`** → GUI 主窗口永不创建。
4. 表现 = 用户双击期待 GUI, 却只看到检测控制台(或一闪而过) → "没有界面"。

**为什么 Wine 验证会"假装正常"**: Wine 无 UAC 服务, `ShellExecute("runas")` 返回错误 → `ensureElevatedOrRestartTier` 记"被拒"并 `return`, 原实例继续走到 `winMain()` → 窗口正常创建。所以**纯 `wine xxx.exe` 永远复现不出此 bug**, 必须 `wine xxx.exe --elevated-run` 直接模拟"已接受 UAC 的提权子实例"才能看到"无界面"(日志只有 `elevated-run 提权子实例` + `runSilverFox: 准备启动 bat`, 没有 `主窗口创建成功`)。

**对策(双轨)**:
```go
if mode == "" {
    // 双击启动触发提权(未指定具体模式): 直接展示 GUI 主窗口, 让用户选择操作
    code, err := winMain()
    if err != nil { showFatal(err.Error()); code = 1 }
    removeGuardFlag(); return
}
runSilverFox(mode)   // 仅当从 GUI 勾"以管理员身份运行"并点具体按钮(带了 mode)才直跑引擎
waitForEngineTree(); removeGuardFlag(); return
```
- 双击(无 mode)→ 展示 GUI(进程已提权, 内部按钮无需二次 UAC)。
- GUI 内勾管理员 + 点具体按钮(带 mode)→ 仍按原意直跑该模式引擎, 不弹 GUI。

**验证清单**:
- [ ] `wine xxx.exe --elevated-run` 日志必须出现 `主窗口创建成功`(且不应出现 `runSilverFox: 准备启动 bat`)。
- [ ] `wine xxx.exe --elevated-run /full` 仍 `runSilverFox: 准备启动 bat`、不弹 GUI(按钮触发路径保持)。
- [ ] 档1 双击 `wine SilverFox.exe` 窗口创建正常(本就与提权无关)。

**排查铁律**: "双击没界面"先区分档位 —— 档1 正常则问题在档2/3 的提权分支; 用 `--elevated-run` 直接模拟提权子实例, 看日志有没有 `主窗口创建成功`, 没有就是 `winMain` 被跳过。
