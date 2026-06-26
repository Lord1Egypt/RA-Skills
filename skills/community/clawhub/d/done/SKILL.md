---
name: done
description: 自动解压并安装技能压缩包到 WSL2 和 Windows 桌面。支持 zip 格式。
---

# Done - 自动技能安装器

## 功能描述

一键自动解压技能压缩包并安装到：
- WSL2 系统：`~/.openclaw/workspace/skills/`
- Windows 桌面：`C:\Users\yanha\Desktop\skills\`

## 使用方法

### 方式一：直接提供压缩包路径

```
帮我 Done 一下 "C:\Users\yanha\Downloads\skill-1.0.0.zip"
```

或

```
done "C:\Users\yanha\Downloads\skill-1.0.0.zip"
```

### 方式二：使用 done/done 关键词

```
帮我 done "C:\Users\yanha\Downloads\skill-1.0.0.zip"
```

## 工作流程

1. **检测路径格式**：支持 Windows 和 Linux 路径
2. **解压压缩包**：自动识别 ZIP 格式
3. **提取技能信息**：读取 SKILL.md 和 _meta.json
4. **安装到 WSL2**：复制到 `~/.openclaw/workspace/skills/<skill-name>/`
5. **备份到 Windows**：复制到桌面 skills 文件夹
6. **清理临时文件**：自动清理解压目录
7. **报告结果**：显示技能信息和安装位置

## 支持的路径格式

### Windows 路径
```
C:\Users\yanha\Downloads\skill-1.0.0.zip
C:/Users/yanha/Downloads/skill-1.0.0.zip
```

### Linux 路径
```
/home/yanha/Downloads/skill-1.0.0.zip
~/Downloads/skill-1.0.0.zip
```

### WSL 挂载路径
```
/mnt/c/Users/yanha/Downloads/skill-1.0.0.zip
```

## 技能信息提取

自动从 `SKILL.md` 提取：
- **技能名称**：name 字段
- **描述**：description 字段
- **主页**：homepage 字段（可选）

## 输出示例

```
✓ 正在处理压缩包: C:\Users\yanha\Downloads\summarize-1.0.0.zip

✓ 已解压
✓ 技能名称: Summarize
✓ 描述: Fast CLI to summarize URLs, local files, and YouTube links

📦 安装位置:
  WSL2: ~/.openclaw/workspace/skills/summarize
  Windows: C:\Users\yanha\Desktop\skills\summarize

✓ 安装完成！
```

## 错误处理

- ❌ 文件不存在 → 提示检查路径
- ❌ 不是 ZIP 文件 → 提示格式错误
- ❌ 缺少 SKILL.md → 提示无效技能包
- ❌ 复制失败 → 显示详细错误信息

## 注意事项

1. **路径中的空格**：请使用引号包裹路径
2. **压缩包格式**：目前只支持 ZIP 格式
3. **技能命名**：自动从 SKILL.md 的 name 字段提取
4. **覆盖安装**：如果技能已存在，会自动覆盖

## 快捷命令

所有以下写法都会触发：

- `Done "路径"`
- `done "路径"`
- `帮我 done "路径"`
- `帮我 Done "路径"`
- `Done 一下 "路径"`
- `done 一下 "路径"`

## 自动化特性

- ✅ 自动转换 Windows 路径到 WSL 路径
- ✅ 自动检测技能名称
- ✅ 自动清理临时文件
- ✅ 双向备份（WSL2 + Windows）
- ✅ 详细的进度反馈

---

版本: 1.0.0
作者: OpenClaw Assistant
