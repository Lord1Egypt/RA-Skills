---
name: everything-find-files
description: 使用Everything SDK快速搜索本地文件
---

# Everything 文件搜索技能

使用 Everything SDK 在本地快速搜索文件，提供文件详细信息并支持文件发送。

## 使用方法

### 1. 搜索文件

`搜索 [关键词]` - 搜索包含指定关键词的文件

示例：

- `搜索 report.pdf` - 搜索名为 report.pdf 的文件
- `搜索 python` - 搜索包含 python 的文件

### 2. 查看文件详情

`文件 [序号]` - 查看搜索结果中指定序号文件的详细信息

示例：

- `文件 1` - 查看第1个文件的详细信息

### 3. 发送文件

`发送 [序号]` - 发送搜索结果中指定序号的文件

示例：

- `发送 2` - 发送第2个文件

## 功能特性

- 快速文件搜索（使用 Everything SDK）
- 显示搜索结果前10个文件
- 提供文件详细信息（路径、大小、文件名、创建日期、修改日期）
- 支持发送原始文件

## 注意事项

- 需要安装 Everything 软件并确保其正在运行
- Everything SDK 需要放置在以下位置之一：
  - 技能目录下的 `libs` 文件夹中（推荐）
  - 技能根目录下
  - `C:\Program Files\Everything\`
  - `C:\EverythingSDK\DLL\`

## SDK 获取和安装

1. 从 https://www.voidtools.com/support/everything/sdk/ 下载 Everything SDK
2. 解压后，根据你的系统选择：
   - 64位系统：复制 `Everything64.dll`
   - 32位系统：复制 `Everything32.dll`
3. 将 DLL 文件放置在技能的 `libs` 文件夹中或技能根目录下
