---
name: desktop-organizer
description: 桌面文件整理技能。当用户要求整理、清理或归类电脑桌面文件时，应使用本技能。它提供了标准化的安全操作流程，并根据预定义的分类规则将文件移动到对应文件夹。支持跨平台（macOS、Linux、Windows）。
---

# 桌面文件整理技能

## 概述

本技能用于整理用户电脑桌面上的文件。整理前会自动备份，并按照预定义的分类规则将文件移动到指定目录。

**跨平台支持**：macOS、Linux、Windows

---

## 系统配置

在执行整理前，首先确定当前操作系统和桌面路径：

### 路径映射表

| 平台 | 桌面路径 | 备份路径前缀 |
|------|----------|--------------|
| macOS/Linux | `~/Desktop/` | `~/Desktop_Backup_` |
| Windows | `%USERPROFILE%\Desktop\` | `%USERPROFILE%\Desktop_Backup_\` |

**使用说明**：
- `~` 表示用户主目录（macOS/Linux）
- `%USERPROFILE%` 表示用户主目录（Windows）

**执行时需先运行以下命令获取实际路径**：

```bash
# macOS/Linux
DESKTOP_PATH="$HOME/Desktop"
BACKUP_PREFIX="$HOME/Desktop_Backup_"

# Windows (PowerShell)
$DESKTOP_PATH = "$env:USERPROFILE\Desktop"
$BACKUP_PREFIX = "$env:USERPROFILE\Desktop_Backup_"
```

---

## 使用前必读：安全规范

整理桌面属于**批量文件操作**，存在不可逆风险。每次执行时必须严格遵守以下步骤：

1. **备份桌面**：在移动任何文件之前，先将桌面完整备份到 `{BACKUP_PREFIX}<日期时间>/`
2. **执行整理**：备份确认成功后，再按规则移动文件。
3. **验证结果**：移动完成后，列出各目标文件夹内容供用户确认。

> ⚠️ 绝对不允许跳过备份步骤。

---

## 分类规则

> 📝 **填写说明**：以下是规则模板，请按照注释提示填写你的实际规则。
> 每条规则格式：文件类型/名称特征 → 移动到哪个文件夹。

> ⚠️ **跨平台路径表示**：
> - `{DESKTOP_PATH}` 表示桌面路径（自动适配）
> - 例如：`{DESKTOP_PATH}/文档/` 会自动解析为 `~/Desktop/文档/`（Mac/Linux）或 `%USERPROFILE%\Desktop\文档\`（Windows）

### 规则 0：文件夹分类

| 类型 | 说明 | 移动到 |
|------|------|--------|
| 文件夹 | 桌面根目录下的所有文件夹（目标文件夹本身除外） | `{DESKTOP_PATH}/文档/` |

> ⚠️ 移动文件夹时，若目标位置已存在同名文件夹，遵循规则 4 的冲突处理策略（当前：跳过不移动）。

---

### 规则 1：按文件类型分类（示例，可修改）

| 文件类型  | 扩展名                                          | 移动到                       |
|-------|----------------------------------------------|---------------------------|
| 图片    | `.jpg` `.jpeg` `.png` `.gif` `.webp` `.heic` | `{DESKTOP_PATH}/文档/` |
| 文档    | `.pdf` `.doc` `.docx` `.txt` `.md`                 | `{DESKTOP_PATH}/文档/`      |
| 表格    | `.xls` `.xlsx` `.csv`                        | `{DESKTOP_PATH}/文档/`      |
| 视频    | `.mp4` `.mov` `.avi` `.mkv`                  | `{DESKTOP_PATH}/文档/`         |
| 音频    | `.mp3` `.wav` `.flac` `.aac`                 | `{DESKTOP_PATH}/文档/`          |
| 压缩包   | `.zip` `.rar` `.7z` `.tar` `.gz`             | `{DESKTOP_PATH}/文档/`     |
| 安装包   | `.dmg` `.pkg` `.exe`                         | `{DESKTOP_PATH}/文档/`     |
| 代码文件  | `.py` `.js` `.ts` `.java` `.sh`              | `{DESKTOP_PATH}/文档/`      |

<!-- ✏️ 你可以增删上表中的行，或者改变目标文件夹路径 -->

---

### 规则 2：按文件名关键词分类（可选，不需要可删除）

> 如果某些文件名包含特定关键词，优先按此规则处理，忽略规则 1。

| 文件名包含关键词            | 移动到 |
|---------------------|--------|
| `note.txt` | `{DESKTOP_PATH}/` |

<!-- ✏️ 按你的实际需求填写关键词和目标路径，可以增加或删除行 -->

---

### 规则 3：特殊处理规则（可选）

> 以下文件类型/名称不移动，保留在桌面。

**保留在桌面的文件：**
- note.txt
- 最近 3 天内创建的文件不移动（填写：是 或 否）：否

---

### 规则 4：冲突处理

当目标位置已存在同名文件时：
- [x] 跳过不移动

<!-- ✏️ 在你想要的选项前打 [x]，删除其他两行 -->

---

## 操作流程

执行整理时，按以下顺序操作：

### 第一步：检测系统并设置路径

**macOS/Linux**：
```bash
OS="unix"
DESKTOP_PATH="$HOME/Desktop"
BACKUP_PREFIX="$HOME/Desktop_Backup_"
```

**Windows**：
```powershell
$OS = "windows"
$DESKTOP_PATH = "$env:USERPROFILE\Desktop"
$BACKUP_PREFIX = "$env:USERPROFILE\Desktop_Backup_"
```

### 第二步：预检查

```bash
# macOS/Linux
ls -la "$DESKTOP_PATH/"

# Windows (PowerShell)
Get-ChildItem -Path $DESKTOP_PATH | Select-Object Name, Length, LastWriteTime
```

将扫描结果整理成表格展示给用户，包含：名称、类型（文件/文件夹）、大小、创建日期。

> 💡 **此步骤仅为展示，无需等待用户确认，直接继续后续步骤。**

### 第三步：备份桌面

**macOS/Linux**：
```bash
BACKUP_DIR="${BACKUP_PREFIX}$(date +%Y%m%d_%H%M%S)"
cp -r "$DESKTOP_PATH/" "$BACKUP_DIR"
echo "备份完成：$BACKUP_DIR"
```

**Windows**：
```powershell
$BACKUP_DIR = "$BACKUP_PREFIX$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item -Path "$DESKTOP_PATH\*" -Destination "$BACKUP_DIR" -Recurse
Write-Host "备份完成：$BACKUP_DIR"
```

备份成功后才可继续。

### 第四步：创建目标文件夹

在移动文件前，确保所有目标文件夹存在：

**macOS/Linux**：
```bash
mkdir -p "{DESKTOP_PATH}/文档/"
```

**Windows**：
```powershell
if (-not (Test-Path "{DESKTOP_PATH}\文档")) {
    New-Item -ItemType Directory -Path "{DESKTOP_PATH}\文档"
}
```

> 注意：将 `{DESKTOP_PATH}` 替换为实际的桌面路径变量

### 第五步：按规则移动文件

参考上方分类规则，依次处理桌面上的每个条目：
1. **文件夹**：先按规则 0 移动所有文件夹到目标目录（跳过目标文件夹自身，如 `文档/`）
2. **文件**：先检查规则 2（关键词匹配），再检查规则 1（文件类型匹配）
3. 如果都不匹配，放入 `{DESKTOP_PATH}/未分类/` 文件夹

**macOS/Linux 移动示例**：
```bash
cd "$DESKTOP_PATH"
# 移动文件夹
for folder in "3D打印" "展会"; do
    if [ -d "$folder" ] && [ ! -d "文档/$folder" ]; then
        mv "$folder" "文档/$folder"
    fi
done
# 移动文件
[ ! -e "文档/file.png" ] && mv file.png "文档/"
```

**Windows 移动示例**：
```powershell
cd $DESKTOP_PATH
# 移动文件夹
if (Test-Path "3D打印" -and -not (Test-Path "文档\3D打印")) {
    Move-Item "3D打印" "文档\"
}
# 移动文件
if (-not (Test-Path "文档\file.png")) {
    Move-Item "file.png" "文档\"
}
```

### 第六步：验证并报告

整理完成后，输出整理报告：
- 总共处理了多少个文件
- 各分类分别移动了多少个
- 未分类文件列表（如有）
- 备份位置

**macOS/Linux**：
```bash
echo "=== 桌面剩余内容 ==="
ls -lh "$DESKTOP_PATH/"
echo ""
echo "=== 文档目录内容 ==="
ls -lh "$DESKTOP_PATH/文档/"
```

**Windows**：
```powershell
Write-Host "=== 桌面剩余内容 ==="
Get-ChildItem -Path $DESKTOP_PATH | Select-Object Name, Length
Write-Host ""
Write-Host "=== 文档目录内容 ==="
Get-ChildItem -Path "$DESKTOP_PATH\文档" | Select-Object Name, Length
```

---

## 其他配置项

<!-- ✏️ 根据需要填写以下选项 -->

**整理范围**：
- [x] 只整理桌面根目录的文件（不进入子文件夹）
- [ ] 递归整理桌面所有子文件夹内的文件

**空文件夹处理**：
- [x] 整理后删除桌面上的空文件夹
- [ ] 保留空文件夹

**整理后的桌面备份**：
- [x] 保留备份（手动删除）
- [ ] 整理确认无误后自动删除备份

---

## 平台差异说明

### macOS/Linux 特有
- 使用 `~` 表示用户主目录
- 命令：`ls`, `cp`, `mv`, `mkdir`
- 路径分隔符：`/`

### Windows 特有
- 使用 `%USERPROFILE%` 表示用户主目录
- 命令：`Get-ChildItem`, `Copy-Item`, `Move-Item`（PowerShell）
- 路径分隔符：`\`

### 路径占位符
在规则配置中使用 `{DESKTOP_PATH}` 占位符，执行时需替换为实际路径：
- macOS/Linux: `~/Desktop`
- Windows: `%USERPROFILE%\Desktop`
