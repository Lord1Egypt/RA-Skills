---
name: 提取WallpaperEngine静态壁纸
description: 从 Wallpaper Engine 的 scene.pkg 文件（PKGV0023/PKGV0024 格式）中提取静态壁纸 PNG 图片，含全部 mipmap 分辨率层级。当用户提供 scene.pkg 路径并要求提取壁纸、素材、纹理时触发。
agent_created: true
---

# 提取 Wallpaper Engine 静态壁纸

## 概述

从 Wallpaper Engine `.pkg` 文件（PKGV0023/PKGV0024 格式）中提取全部资源，并从 `.tex` 纹理文件中恢复嵌入的 PNG 壁纸图像（含多级 mipmap）。两种版本的二进制结构完全一致，仅 magic 版本号不同。

## PKGV00xx 文件格式

二进制格式由 Header + 条目元信息 + 数据区组成：

### Header (16 bytes)
| 偏移 | 大小 | 类型   | 说明                              |
|------|------|--------|-----------------------------------|
| 0    | 4    | uint32 | 条目数量                          |
| 4    | 8    | bytes  | Magic "PKGV0023" 或 "PKGV0024"   |
| 12   | 4    | uint32 | Header 标志（通常等于条目数）      |

### 每个条目的元信息（字段间无对齐填充）
| 偏移 | 大小 | 类型   | 说明                              |
|------|------|--------|-----------------------------------|
| 0    | 4    | uint32 | 文件名长度 (N)                    |
| 4    | N    | bytes  | 文件名 (UTF-8, 无填充)            |
| 4+N  | 4    | uint32 | 数据偏移（相对于 data_start）      |
| 8+N  | 4    | uint32 | 数据大小 (bytes)                  |

**关键细节：** 文件名后没有 4 字节对齐填充，两个 uint32 紧跟在文件名之后。

### 数据区
所有文件数据起始于 `data_start = 元信息结束位置`。条目中存储的 offset 是相对于 `data_start` 而非文件开头。

## .tex 纹理格式

Wallpaper Engine `.tex` 文件中内嵌了多个 PNG 图像流，通常为同一纹理的多个 mipmap 分辨率（如 4K / 1080p / 540p 等）。提取方法：

1. 扫描 PNG 签名 (`\x89PNG\r\n\x1a\n`)
2. 逐 chunk 解析（IHDR -> 数据块 -> IEND）确定每个 PNG 的精确边界
3. 逐个保存，按分辨率命名

## 工作流程

### 步骤 1：运行提取脚本

```
python scripts/extract_pkg.py <scene.pkg路径> [输出目录]
```

若省略输出目录，则在 pkg 文件旁自动创建 `*_extracted` 目录。

脚本功能：
- 解析 PKGV00xx 头部和条目元信息
- 按目录结构提取全部文件
- 扫描 `.tex` 文件中的嵌入 PNG，输出全部 mipmap 层级
- 最大尺寸保存为 `wallpaper.png`，其余为 `wallpaper_{宽}x{高}.png`

### 步骤 2：确认主壁纸

最大尺寸的 PNG（通常 3840x2160 或 1920x1080）即为主壁纸。`scene.json` 可确认场景配置。

### 步骤 3：交付结果

通过 `deliver_attachments` 将提取的 PNG 交付给用户，主壁纸在前，mipmap 层级按需附加。
