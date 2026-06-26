---
name: bilibili-favorites-downloader
description: |
  下载 Bilibili 用户个人收藏夹视频的工具。当用户提到以下任何场景时必须使用此 Skill：
  - "下载 Bilibili 收藏"、"bilibili 收藏下载"、"备份 bilibili 收藏夹"
  - "下载 B 站收藏"、"B站收藏夹下载"
  - "获取收藏视频列表"、"导出 bilibili 收藏"
  - "download bilibili favorites"、"backup bilibili"

  此 Skill 提供完整的 Bilibili 用户收藏夹视频下载解决方案，包括：
  - 自动获取收藏夹所有视频列表（支持分页）
  - 智能估算视频大小，支持按大小过滤
  - 使用 yt-dlp 下载最高可用清晰度
  - 断点续传，跳过已存在的文件
  - 批量下载，自动处理失效视频
---

# Bilibili 收藏视频下载工具

## 功能概述

此 Skill 用于下载 Bilibili 用户个人的收藏夹视频，支持批量下载、大小过滤、最高清晰度等功能。

## 使用场景

1. **备份收藏夹** - 将收藏的 Bilibili 视频下载到本地
2. **离线观看** - 下载视频以便离线观看
3. **整理收藏** - 获取收藏视频列表并导出

## 前置要求

- Python 3.7+
- yt-dlp (会自动检查并提示安装)
- 网络连接

## Script Directory

Determine this SKILL.md directory as `{baseDir}`.

| Script                        | Purpose                        |
| ----------------------------- | ------------------------------ |
| `scripts/download_favorites.py` | Main python script entry point |

## 使用方法

### 基本用法

用户只需要提供用户个人收藏夹 URL 或收藏夹 ID，工具会自动完成其余工作：
请提示用户在网页上登陆 www.bilibili.com, 进入用户个人收藏夹， 把浏览器地址栏收藏夹URL复制告诉AI

```
  Bilibili 收藏夹URL示例：https://space.bilibili.com/123456/favlist?fid=7890123
```

## Run Script Examples with Params

### 基础使用（下载收藏夹，默认500MB大小限制，推荐首次使用）

```bash
python {baseDir}/scripts/download_favorites.py \
  --url "https://space.bilibili.com/123456/favlist?fid=7890123"
```

### 日常使用（推荐配置，限制300MB大小，指定输出目录）

```bash
python {baseDir}/scripts/download_favorites.py \
  --url "https://space.bilibili.com/123456/favlist?fid=7890123" \
  --size-limit 300 \
  --output-dir ~/Downloads/bilibili_favorites/
```

### 仅获取视频列表（不下载视频）

```bash
python {baseDir}/scripts/download_favorites.py \
  --url "https://space.bilibili.com/123456/favlist?fid=7890123" \
  --list-only
```

### 限制下载数量（只下载前10个视频）

```bash
python {baseDir}/scripts/download_favorites.py \
  --url "https://space.bilibili.com/123456/favlist?fid=7890123" \
  --max-download 10
```

## 参数说明

| 参数                | 说明                           | 默认值                                      |
| ------------------- | ------------------------------ | ------------------------------------------ |
| `--url`             | Bilibili 收藏夹页面 URL         | 必需参数                                    |
| `--size-limit`      | 视频大小限制（MB），超过则跳过    | 500                                        |
| `--output-dir`      | 自定义下载输出目录               | ~/Downloads/bilibili_favorites/            |
| `--list-only`       | 仅获取视频列表，不下载视频        | False                                      |
| `--max-download`    | 最大下载视频数量                 | 无限制（下载全部）                          |
| `--skip-existing`   | 跳过已存在的视频文件（脚本默认行为）| True（无需指定）                            |

### 支持的 URL 格式

- `https://space.bilibili.com/{user_id}/favlist?fid={fav_id}`

## 工作流程

1. **解析收藏夹信息** - 从 URL 中提取用户 ID 和收藏夹 ID
2. **获取视频列表** - 调用 Bilibili API 获取所有收藏视频（支持分页）
3. **估算视频大小** - 使用 yt-dlp 获取视频信息并估算大小
4. **过滤视频** - 根据大小限制过滤视频
5. **批量下载** - 使用 yt-dlp 下载视频，自动合并音视频
6. **生成报告** - 输出下载统计信息

## 输出说明

下载的视频将保存为 MP4 格式，文件名格式为：
```
{视频标题}_{BV号}.mp4
```

## 注意事项

- 下载的视频仅供个人学习使用
- 请遵守 Bilibili 用户协议和相关法律法规
- 部分高清晰度视频需要大会员才能下载
- 失效视频会自动跳过并记录

## 故障排除

### 无法获取视频列表
- 检查收藏夹是否为公开状态
- 检查网络连接
- 确认收藏夹 ID 正确

### 下载速度慢
- 这是正常现象，取决于视频大小和网络状况
- 工具支持断点续传，可以随时中断并继续

### 视频下载失败
- 可能是视频已失效或被删除
- 可能是网络问题，可以重新运行脚本


