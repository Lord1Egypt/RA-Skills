# CODESYS Toolkit

CODESYS/InoProShop PLC 自动编程工具集。

## 文件清单

本 skill 包含 8 个工具文件：

| 文件 | 功能 |
|------|------|
| `check_compile.py` | 编译结果探测 |
| `dialog_monitor.ps1` | 对话框监控（WinEvent Hook） |
| `env_setup.ps1` | 环境配置（自动检测 InoProShop） |
| `export_pou.py` | POU 导出（工程→st/目录） |
| `generator_runner.py` | 工程生成器（模板→完整工程） |
| `list_devices.py` | 设备枚举 |
| `patch_pou.py` | POU 补丁（增量更新） |
| `run_script.ps1` | 统一启动器 |

## 获取工具文件

工具文件来源于美的集团内部 GitLab 仓库。

### 方式一：运行下载脚本（需要 GitLab 访问权限）

```powershell
.\download_tools.ps1
```

### 方式二：手动下载

从以下仓库下载 `scripts/tools/` 目录下的所有文件：

```
https://git.midea.com/DEP-IMRC/IIET/auto/auto-rd-group/2026/mra0626c15-plc/skills/codesys-auto-programmer/-/tree/master/scripts/tools
```

放置到本 skill 的 `scripts/tools/` 目录下。

## 使用方法

详见 [SKILL.md](./SKILL.md)

## 依赖

- InoProShop V1.9.0.1+
- PowerShell 5.1+
- IronPython 2.7（InoProShop 内置）
- Windows 10/11
