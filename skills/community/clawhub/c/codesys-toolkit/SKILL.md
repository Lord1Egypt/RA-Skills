---
name: codesys-toolkit
version: 1.0.0
description: "Automate CODESYS/InoProShop PLC programming �� project generation, POU export/patching, compile c..."
tags: [codesys, inoproshop, plc, automation, iec61131-3, structured-text]
---

# CODESYS Toolkit

CODESYS/InoProShop PLC 自动编程工具集，实现�?AI 生成代码�?PLC 工程的完整闭环�?
## 适用场景

- 需要自动化生成 CODESYS 工程（从模板 + st/ 目录�?- 需要导出已有工程的 POU/GVL/DUT 到文本文�?- 需要增量补丁（只更新变更的 POU，避免全量覆写）
- 需要自动编译并检测错�?警告
- 需要枚举可�?PLC 设备型号
- 需要监�?InoProShop 弹窗（错误对话框检测）

## 支持�?PLC 型号

| 型号 | 容器类型 | 说明 |
|------|----------|------|
| AM600 | Application (IEC) | 高端控制�?|
| H5U | Application (IEC) | 中端控制�?|
| AM522 | 任意 IEC 容器 | 经济型控制器 |
| TT | 任意 IEC 容器 | 文本终端 |

## 工具清单

| 工具 | 语言 | 功能 |
|------|------|------|
| `env_setup.ps1` | PowerShell | 环境检测：自动发现 InoProShop.exe、Profile，缓存到 env.json |
| `run_script.ps1` | PowerShell | 统一启动器：杀旧进程→启动→tail日志→摘�?|
| `dialog_monitor.ps1` | PowerShell+C# | 对话框监控：WinEvent Hook 零轮询检测弹�?|
| `export_pou.py` | IronPython | POU 导出：递归遍历→st/ 目录→镜像文件夹结构 |
| `generator_runner.py` | IronPython | 工程生成：模板→创建 POU/GVL/DUT→挂�?Task→编�?|
| `patch_pou.py` | IronPython | POU 补丁：增量更新（快照 diff）→覆写→编�?|
| `check_compile.py` | IronPython | 编译检查：触发编译→轮询→解析错误/警告 |
| `list_devices.py` | IronPython | 设备枚举：列出所有可用控制器型号 |

## 快速开�?
### 1. 环境检测（首次使用�?
```powershell
. "skills\codesys-toolkit\scripts\tools\env_setup.ps1"
# 自动检�?InoProShop.exe 路径�?Profile
# 结果写入 references\env.json
```

### 2. 配置 env.json

```json
{
  "exe": "C:\\InoProShop\\InoProShop.exe",
  "profile": "InoProShop(V1.9.0.1)",
  "skill_dir": "D:\\path\\to\\codesys-toolkit",
  "workspace_dir": "D:\\path\\to\\project_workspace",
  "template": "D:\\path\\to\\template.project",
  "patch_target": "D:\\path\\to\\target.project",
  "extra_libraries": "SysCom, 3.3.2.50 (System)"
}
```

### 3. 导出已有工程

```powershell
.\scripts\tools\run_script.ps1 export
# �?.project 中的所�?POU/GVL/DUT 导出�?st/ 目录
# 生成 .committed.json 快照（用于后续增量补丁）
```

### 4. AI 生成/修改代码

�?`st/` 目录下编�?`.st` 文件（单文件格式：声明区+实现区合并）

### 5. 增量补丁

```powershell
.\scripts\tools\run_script.ps1 patch
# 自动检�?st/ 中变更的文件（对�?.committed.json�?# 只补丁变更的 POU，保存并编译
```

### 6. 编译检�?
```powershell
.\scripts\tools\run_script.ps1 check
# 触发编译，轮询等待完成，解析错误/警告�?```

### 7. 从模板生成新工程

```powershell
.\scripts\tools\run_script.ps1 generate
# 复制模板→创�?POU/GVL/DUT→挂�?Task→编�?```

## 单文�?POU 格式

所�?POU 使用单文件格式（声明�?实现区合并到一�?.st 文件）：

```structured-text
FUNCTION_BLOCK FB_Motor
VAR
    bStart : BOOL;
    bRunning : BOOL;
END_VAR

// 实现�?IF bStart THEN
    bRunning := TRUE;
ELSE
    bRunning := FALSE;
END_IF

END_FUNCTION_BLOCK
```

### 文件命名规则

| 类型 | 后缀 | 示例 |
|------|------|------|
| POU (FB/Program/Function) | `.st` | `FB_Motor.st` |
| Action | `.act.st` | `ACT_Init.act.st` |
| GVL | `.st` (�?VAR_GLOBAL 开�? | `GVL_Config.st` |
| DUT Structure | `.st` (�?TYPE...STRUCT 开�? | `DUT_State.st` |
| DUT Enum | `.st` (�?TYPE...ENUM 开�? | `ENUM_Mode.st` |

### 目录结构（镜像工程文件夹�?
```
st/
├── 程序/
�?  ├── P_Main.st                    <- Program POU
�?  └── P_Main/
�?      └── ACT_Init.act.st          <- Action (在父 POU 同名子目�?
├── FB功能�?
�?  ├── FB_Motor.st
�?  └── FB_Cylinder.st
├── GVL/
�?  └── GVL_Config.st
└── DUT/
    └── DUT_State.st
```

## 增量补丁机制

### 快照文件 (.committed.json)

```json
{
  "程序/P_Main.st": "a1b2c3d4e5f6...",
  "FB功能�?FB_Motor.st": "f6e5d4c3b2a1..."
}
```

### 工作流程

1. `export_pou.py` 导出后写�?`.committed.json`（基线）
2. AI 修改 st/ 中的文件
3. `patch_pou.py` 对比当前 MD5 vs 基线
4. 只补丁变更的文件
5. 编译成功后更�?`.committed.json`

## 对话框监�?
`dialog_monitor.ps1` 使用 WinEvent Hook 零轮询检�?InoProShop 弹窗�?
- 监听 `EVENT_OBJECT_SHOW` 事件
- 只检�?`#32770` 类（标准对话框）
- �?PID 过滤（只监控当前 InoProShop 进程�?- 按标题过滤（默认 "InoProShop"�?- 提取对话框内容（Static 控件文本 + Button 文本�?
## 错误处理

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `InoProShop.exe not found` | 未安装或路径未检�?| 运行 `env_setup.ps1` |
| `IEC container not found` | 工程结构异常 | 检�?.project 文件 |
| `workspace_dir 未设置` | env.json 配置缺失 | 手动编辑 env.json |
| `ObjectNameNotUniqueExceptionEx` | POU 名称冲突 | 删除 st/ 中的重复文件 |

### 日志位置

所有日志写�?`<workspace_dir>/log/` 目录�?
- `export_pou_log.txt`
- `patch_pou_log.txt`
- `check_compile_log.txt`
- `generator_runner_log.txt`
- `list_devices_log.txt`

## 依赖

- **InoProShop** V1.9.0.1+（含 CODESYS Scripting API�?- **PowerShell** 5.1+
- **IronPython** 2.7（InoProShop 内置�?- **Windows** 10/11

## 注意事项

1. **Python 2 语法**：IronPython 脚本使用 `unicode()`、`codecs.open()` �?Python 2 语法
2. **UTF-8 �?BOM**：env.json 必须 UTF-8 �?BOM（IronPython 2.7 json.load 不识�?BOM�?3. **路径硬编码禁�?*：所有路径通过 env.json 或环境变量传�?4. **单实�?*：run_script.ps1 默认杀掉旧 InoProShop 进程（`-NoKill` 可跳过）
5. **编译超时**：默�?60 秒，大工程可能需要调�?
## 来源

本工具集基于美的集团智能装备研究�?CODESYS 自动编程项目，由李冉（Li Ran）开发，尹德斌（Paudy）整合为独立 skill�?
原始仓库：`https://git.midea.com/DEP-IMRC/IIET/auto/auto-rd-group/2026/mra0626c15-plc/skills/codesys-auto-programmer`
