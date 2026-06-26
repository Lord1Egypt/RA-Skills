# 桌面整理 Skill 使用说明

## 🌟 跨平台版本

**支持系统**：macOS、Linux、Windows

本版本已优化，**无需修改路径配置**，会自动适配不同系统和用户目录！

---

## 📥 安装方法

### 方法 1：手动安装（推荐）

1. 解压 `desktop-organizer.zip`
2. 将 `desktop-organizer` 文件夹复制到以下位置：
   - **macOS/Linux**: `~/.workbuddy/skills/`
   - **Windows**: `%USERPROFILE%\.workbuddy\skills\`
3. 重启 WorkBuddy（如果正在运行）
4. 完成！

### 方法 2：通过 WorkBuddy 导入

如果 WorkBuddy 支持 skill 导入功能，可直接导入 zip 文件。

---

## 🚀 使用方法

安装完成后，直接对 WorkBuddy 说：

```
帮我整理桌面
```

会自动执行：
1. 检测操作系统并自动设置桌面路径
2. 扫描桌面所有文件和文件夹
3. 自动备份整个桌面（带时间戳）
4. 按规则移动文件到指定目录
5. 输出整理报告

---

## ⚙️ 路径适配说明

### 自动适配的路径

本 skill 使用占位符 `{DESKTOP_PATH}`，会自动解析为实际路径：

| 系统 | {DESKTOP_PATH} 实际值 | 示例 |
|------|---------------------|------|
| macOS | `~/Desktop` | `/Users/你的用户名/Desktop` |
| Linux | `~/Desktop` | `/home/你的用户名/Desktop` |
| Windows | `%USERPROFILE%\Desktop` | `C:\Users\你的用户名\Desktop` |

### 默认目标路径

所有文件和文件夹默认移动到 `{DESKTOP_PATH}/文档/`：

| 系统 | 实际目标路径 |
|------|-------------|
| macOS | `~/Desktop/文档/` |
| Linux | `~/Desktop/文档/` |
| Windows | `%USERPROFILE%\Desktop\文档\` |

### 如需修改目标路径

如果不想放在 `文档/` 文件夹，修改 `SKILL.md` 中的规则表格：

**只需修改 `{DESKTOP_PATH}/...` 后面的部分**，例如：

```
原规则：{DESKTOP_PATH}/文档/
改成：{DESKTOP_PATH}/我的文件/
或者：{DESKTOP_PATH}/分类/
```

> ⚠️ 不要修改 `{DESKTOP_PATH}` 本体，保持它不变！

---

## 📋 默认规则

### 文件夹分类
所有桌面文件夹 → 移动到 `{DESKTOP_PATH}/文档/`（目标文件夹本身除外）

### 文件类型分类
| 类型 | 默认目标路径 |
|------|-------------|
| 图片 | `{DESKTOP_PATH}/文档/` |
| 文档 | `{DESKTOP_PATH}/文档/` |
| 表格 | `{DESKTOP_PATH}/文档/` |
| 视频 | `{DESKTOP_PATH}/文档/` |
| 音频 | `{DESKTOP_PATH}/文档/` |
| 压缩包 | `{DESKTOP_PATH}/文档/` |
| 安装包 | `{DESKTOP_PATH}/文档/` |
| 代码文件 | `{DESKTOP_PATH}/文档/` |

### 保留规则
- `note.txt` 文件保留在桌面（如不需要可删除规则 2）

---

## ⚠️ 注意事项

1. **跨平台兼容**：macOS、Linux、Windows 均可使用，无需额外配置
2. **备份策略**：每次整理前会自动备份到 `{DESKTOP_PATH}_Backup_<日期时间>/`
3. **冲突处理**：目标位置已存在同名文件时，默认跳过不移动
4. **自动化**：全程无需人工确认，自动执行
5. **安全性**：绝对不会跳过备份步骤

---

## 🔧 自定义规则

### 示例 1：分类到不同文件夹

修改规则 1，让不同类型文件去不同地方：

```
| 文件类型 | 扩展名 | 移动到 |
|---------|--------|--------|
| 图片 | .png .jpg | {DESKTOP_PATH}/图片/ |
| 文档 | .pdf .doc | {DESKTOP_PATH}/文档/ |
| 视频 | .mp4 .mov | {DESKTOP_PATH}/视频/ |
```

### 示例 2：按项目关键词分类

修改规则 2，将文件名包含关键词的文件归类：

```
| 文件名包含关键词 | 移动到 |
|----------------|--------|
| 项目A | {DESKTOP_PATH}/项目A/ |
| 财务 | {DESKTOP_PATH}/财务/ |
| 工作 | {DESKTOP_PATH}/工作/ |
```

### 示例 3：分类到系统标准目录

（适用于 macOS/Linux，需确保目录存在）

```
| 文件类型 | 扩展名 | 移动到 |
|---------|--------|--------|
| 图片 | .png .jpg | ~/Pictures/桌面图片/ |
| 文档 | .pdf .doc | ~/Documents/桌面文档/ |
| 视频 | .mp4 .mov | ~/Movies/桌面视频/ |
```

> 💡 使用 `~` 或绝对路径也可以，skill 会自动处理

---

## 🐛 常见问题

### Q1: 我和朋友的桌面路径不一样怎么办？
**A:** 不用担心！本版本已自动适配，无需修改路径配置。它会自动识别：
- 你朋友是 macOS 用户：自动使用 `~/Desktop/`
- 你朋友是 Windows 用户：自动使用 `%USERPROFILE%\Desktop\`

### Q2: Windows 上使用 PowerShell 命令有问题吗？
**A:** skill 中已提供 PowerShell 命令示例，WorkBuddy 会根据系统自动选择合适的命令。

### Q3: 桌面被清理乱了怎么办？
**A:** 备份在桌面根目录的 `Desktop_Backup_<时间戳>/` 文件夹，可以从备份恢复。

### Q4: 我想保留某些文件不移动怎么办？
**A:** 编辑 SKILL.md：
- 方法 1：在「规则 2」中添加文件名关键词
- 方法 2：在「规则 3」中列出要保留的文件名

### Q5: 支持递归整理子文件夹吗？
**A:** 当前默认只整理桌面根目录，如需递归整理子文件夹，修改 SKILL.md 中的「整理范围」配置。

### Q6: Windows 上中文路径和文件名有问题吗？
**A:** 本 skill 支持中文文件名，使用 PowerShell 命令可以正确处理中文字符。

---

## 📝 技术说明

### 路径占位符系统

| 占位符 | 用途 | 自动解析结果 |
|--------|------|-------------|
| `{DESKTOP_PATH}` | 桌面路径 | `~/Desktop`（Mac/Linux）或 `%USERPROFILE%\Desktop`（Windows） |
| `{BACKUP_PREFIX}` | 备份路径前缀 | `~/Desktop_Backup_`（Mac/Linux）或 `%USERPROFILE%\Desktop_Backup_\`（Windows） |

### 平台检测

执行时会自动检测操作系统：
- 检测到 Unix-like（macOS/Linux）：使用 bash/sh 命令
- 检测到 Windows：使用 PowerShell 命令

---

## 📞 反馈与支持

如有问题或建议，欢迎反馈给分享者！

**祝你使用愉快！** 🎉
