---
name: bizyair-upload
description: BizyAir 文件上传助手。当用户需要将本地图片、音频、视频等资源上传到 BizyAir 服务器时使用此技能。支持快速上传并获取可访问的 URL。触发场景：用户提到"上传到 BizyAir"、"BizyAir 上传"、"上传图片到 BizyAir"，或者需要获取 BizyAir input resource URL 时。
---

# BizyAir 文件上传助手

本技能帮助你将本地文件（图片、音频、视频等）上传到 BizyAir 服务器，并获取可访问的 URL。

## 功能

- 📤 上传本地文件到 BizyAir 服务器
- 🔗 获取可访问的资源 URL
- 📋 查询已上传的输入资源列表

## 前置准备

1. **获取 API Key**：访问 [BizyAir 控制台](https://bizyair.cn/user/api-key) 获取 API Key
2. **配置环境变量**（推荐）：
   ```bash
   export BIZYAIR_API_KEY="your_api_key_here"
   ```

## 使用方法

### 上传单个文件

当用户需要上传文件时：

```
请帮我把 /path/to/image.png 上传到 BizyAir
```

或者：

```
上传这张图片到 BizyAir 并获取 URL
```

### 批量上传

```
上传这些文件到 BizyAir：
- image1.png
- image2.jpg
- video.mp4
```

### 查询已上传资源

```
查看 BizyAir 中的输入资源列表
```

## 上传流程

技能会自动完成以下步骤：

1. **获取上传凭证** - 从 BizyAir API 获取临时 STS 凭证和 OSS 上传参数
2. **上传到 OSS** - 使用阿里云 OSS SDK 将文件上传到指定存储
3. **提交资源** - 在 BizyAir 系统中注册该资源
4. **返回 URL** - 返回可访问的资源 URL

## 输出示例

上传成功后会返回：

```
✅ 上传成功！
文件名: example.png
URL: https://storage.bizyair.cn/inputs/20250911/xxx.png
Object Key: inputs/20250911/xxx.png
```

## 错误处理

- **API Key 未配置**：提示用户设置 `BIZYAIR_API_KEY` 环境变量或在对话中提供
- **文件不存在**：检查文件路径是否正确
- **上传失败**：显示详细错误信息，可能是网络问题或凭证过期
- **文件类型不支持**：BizyAir 支持常见图片、音频、视频格式

## 注意事项

- STS 凭证是临时的，仅用于上传环节
- 上传后的 URL 可用于 BizyAir 工作流中的 LoadImage、LoadAudio、LoadVideo 等节点
- 建议上传后尽快使用或保存 URL

## 脚本使用

如需直接使用上传脚本：

```bash
python scripts/upload.py <file_path> [--api-key <key>]
```

## 使用效果
![第一次使用配置，会有很多提示。](https://storage.bizyair.cn/inputs/20260313/12aiqEZQO35wUTvYPa8qK7FE63fXD7IM.png)
![第二次快很多，和它说列出 URL 就可以。](https://storage.bizyair.cn/inputs/20260313/VNXiARkDyUMYyZCizGkHmsWOu3UziTyb.png)
