---
name: feishu-message-download
description: 从飞书消息中下载文件（视频、图片、文档等）到本地
metadata: {"clawdbot":{"emoji":"📥","requires":{"bins":["python3"],"python_deps":["requests"]}}}
---

# 飞书消息文件下载

从飞书消息中下载文件（视频、图片、文档等）到本地。

## 描述

本 Skill 用于从飞书聊天消息中下载附件到本地，支持视频、图片、文件等多种类型。

下载后的文件可以用于：
- 视频编辑和处理
- 上传到抖音、小红书、B 站等平台
- 本地存档和备份
- AI 分析和处理
- 转发到其他平台

## 功能

- 从飞书消息链接或消息 ID 中提取文件信息
- 支持手动指定 file_key 和 message_id
- 自动获取飞书 tenant_access_token
- 下载文件到本地指定目录

## 安装

```bash
# 安装依赖
pip install -r requirements.txt
```

## 配置

本 Skill 需要以下飞书应用凭证，可通过以下方式配置：

### 方式 1：OpenClaw 配置（推荐）
在 OpenClaw 配置文件中设置：
```json
{
  "channels": {
    "feishu": {
      "appId": "your_app_id",
      "appSecret": "your_app_secret"
    }
  }
}
```

### 方式 2：环境变量
```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

## 使用方法

### 方法 1：通过消息链接下载
```python
from download import FeishuMessageDownloader

downloader = FeishuMessageDownloader()
downloader.download_from_message_url(
    message_url="https://open.feishu.cn/im/xxx",
    output_dir="~/Downloads"
)
```

### 方法 2：通过消息 ID 和 file_key 下载
```python
from download import FeishuMessageDownloader

downloader = FeishuMessageDownloader()
downloader.download_file(
    message_id="om_xxxxxxxx",
    file_key="file_xxxxxxxx",
    output_dir="~/Downloads",
    filename="my_video.mp4"
)
```

### 方法 3：命令行使用
```bash
# 通过消息链接下载
python download.py --url "https://open.feishu.cn/im/xxx" --output ~/Downloads

# 通过消息 ID 和 file_key 下载
python download.py --message-id "om_xxxxxxxx" --file-key "file_xxxxxxxx" --output ~/Downloads

# 指定保存文件名
python download.py --message-id "om_xxxxxxxx" --file-key "file_xxxxxxxx" --output ~/Downloads --filename "video.mp4"
```

## 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--url` | 飞书消息链接 | 可选 |
| `--message-id` | 消息 ID (om_xxx) | 可选 |
| `--file-key` | 文件 key (file_xxx) | 可选 |
| `--output` | 输出目录，默认为当前目录 | 可选 |
| `--filename` | 保存的文件名 | 可选 |

## 飞书应用权限要求

本 Skill 需要以下飞书应用权限：
- `im:resource` - 访问消息资源

## 支持的文件类型

- **视频文件** (.mp4, .mov, .avi, etc.) - 可用于视频编辑、平台发布
- **图片文件** (.jpg, .png, .gif, .webp, etc.) - 可用于设计、文档制作
- **文档文件** (.pdf, .doc, .xls, .ppt, etc.) - 可用于本地编辑、存档
- **音频文件** (.mp3, .wav, etc.) - 可用于音频处理、转录
- **其他飞书支持的文件类型**

## 典型使用场景

### 场景 1：视频内容发布
用户发送视频到飞书 → 下载到本地 → 发布到抖音/小红书/B 站

```bash
# 下载视频
python download.py --message-id "om_xxx" --file-key "file_xxx" --output ~/Videos

# 然后使用视频发布工具发布到各平台
```

### 场景 2：文档处理
收到飞书文档 → 下载到本地 → 编辑处理 → 重新上传或转发

```bash
python download.py --url "https://open.feishu.cn/im/xxx" --output ~/Documents
```

### 场景 3：图片素材收集
收集飞书群里的图片 → 批量下载 → 用于设计或存档

```python
from download import FeishuMessageDownloader

downloader = FeishuMessageDownloader()
for msg in messages:
    downloader.download_file(
        message_id=msg['id'],
        file_key=msg['file_key'],
        output_dir="~/Pictures/Collection"
    )
```

### 场景 4：AI 处理流程
下载飞书文件 → AI 分析/处理 → 生成报告或内容

```python
# 下载视频
downloader = FeishuMessageDownloader()
result = downloader.download_file(message_id, file_key, "~/AI_Input")

# 使用 AI 处理
# ... AI 处理代码 ...
```

## 使用建议

1. **批量下载**：可以结合飞书消息列表 API，批量下载多个文件
2. **自动命名**：如果不指定 filename，会自动使用原始文件名
3. **目录管理**：建议按日期或项目分类保存文件
4. **定期清理**：下载后的文件记得定期清理，避免占用过多空间

## API 端点

```
GET https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{file_key}?type=file
```

## 返回结果

成功下载后返回保存的文件路径：
```python
{
    "success": True,
    "file_path": "/path/to/downloaded/file.mp4",
    "file_size": 1234567,
    "filename": "file.mp4"
}
```

## 错误处理

可能的错误情况：
- 凭证无效或过期
- 消息不存在或无权访问
- 文件不存在或已过期
- 网络连接问题

## 注意事项

1. **文件下载链接有过期时间**，请及时下载（通常 7 天）
2. **大文件下载可能需要较长时间**，请耐心等待
3. **确保应用有访问该消息的权限**，否则无法下载
4. **下载后的文件处理**：
   - 视频文件：可用于剪辑、转码、发布到视频平台
   - 图片文件：可用于编辑、压缩、格式转换
   - 文档文件：可用于内容提取、格式转换、打印
5. **存储空间**：定期清理下载的文件，避免占用过多磁盘空间
6. **隐私合规**：下载的文件仅供个人使用，注意数据安全和隐私保护

## 与其他 Skill 的配合

本 Skill 可以与以下类型的 Skill 配合使用：

| 配合 Skill 类型 | 使用场景 |
|-------------|---------|
| 视频发布 Skill | 下载飞书视频 → 发布到抖音/小红书/B 站 |
| 视频处理 Skill | 下载视频 → 剪辑/转码/压缩 |
| AI 分析 Skill | 下载文件 → AI 分析/总结/提取 |
| 文档处理 Skill | 下载文档 → 编辑/转换/合并 |
| 云存储 Skill | 下载文件 → 上传到云盘/网盘 |

## 完整工作流程示例

### 飞书视频 → 抖音发布 完整流程

```bash
# 步骤 1：从飞书下载视频
python download.py \
  --message-id "om_x100b523c2b77fd30c24abb58a94deee" \
  --file-key "file_v3_0010e_dc672f40-87b6-4d67-b69d-e40290032c2g" \
  --output ~/.openclaw/workspace \
  --filename "douyin_video.mp4"

# 步骤 2：（可选）视频处理
# ffmpeg -i douyin_video.mp4 -c:v libx264 -c:a aac output.mp4

# 步骤 3：发布到抖音
# 使用抖音发布工具或手动上传
```

### 批量处理飞书文件

```python
from download import FeishuMessageDownloader
import os

# 初始化下载器
downloader = FeishuMessageDownloader()

# 批量下载多个文件
messages = [
    {"message_id": "om_xxx1", "file_key": "file_xxx1", "type": "video"},
    {"message_id": "om_xxx2", "file_key": "file_xxx2", "type": "image"},
    {"message_id": "om_xxx3", "file_key": "file_xxx3", "type": "document"},
]

output_base = "~/Downloads/Feishu_Files"

for msg in messages:
    # 按类型分类保存
    type_dir = os.path.join(output_base, msg['type'])
    os.makedirs(type_dir, exist_ok=True)
    
    result = downloader.download_file(
        message_id=msg['message_id'],
        file_key=msg['file_key'],
        output_dir=type_dir
    )
    
    if result['success']:
        print(f"✅ 下载成功：{result['file_path']}")
    else:
        print(f"❌ 下载失败：{result.get('error')}")
```

## 作者

勇哥的小飞侠 🧚🏻‍♀️🌸🧚🏻
