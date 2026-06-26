# 📥 飞书消息文件下载

从飞书消息中下载文件（视频、图片、文档等）到本地。

## ✨ 功能特性

- 📥 支持下载飞书消息中的各种文件类型
- 🔗 自动解析飞书消息链接提取 file_key
- 🎯 支持手动指定 message_id 和 file_key
- 🔐 自动获取飞书 tenant_access_token
- 📁 自定义输出目录和文件名
- 🚀 支持命令行和 Python 脚本调用

## 📦 安装

### 方式 1：通过 ClawHub 安装（推荐）

```bash
clawhub install feishu-message-download
```

### 方式 2：手动安装

```bash
# 克隆仓库
git clone https://github.com/Cindypapa/feishu-message-download.git
cd feishu-message-download

# 安装依赖
pip install -r requirements.txt
```

## 🔧 配置

### 方式 1：OpenClaw 配置（推荐）

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "channels": {
    "feishu": {
      "appId": "cli_xxxxxxxxxxxxx",
      "appSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### 方式 2：环境变量

```bash
export FEISHU_APP_ID="cli_xxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## 📖 使用方法

### 方法 1：通过消息链接下载

```bash
python download.py --url "https://open.feishu.cn/im/xxx" --output ~/Downloads
```

### 方法 2：通过消息 ID 和 file_key 下载

```bash
python download.py \
  --message-id "om_xxxxxxxx" \
  --file-key "file_xxxxxxxx" \
  --output ~/Downloads
```

### 方法 3：指定保存文件名

```bash
python download.py \
  --message-id "om_xxxxxxxx" \
  --file-key "file_xxxxxxxx" \
  --output ~/Downloads \
  --filename "my_video.mp4"
```

### 方法 4：Python 脚本调用

```python
from download import FeishuMessageDownloader

downloader = FeishuMessageDownloader()

# 从消息链接下载
result = downloader.download_from_message_url(
    message_url="https://open.feishu.cn/im/xxx",
    output_dir="~/Downloads"
)

# 或通过 message_id + file_key 下载
result = downloader.download_file(
    message_id="om_xxxxxxxx",
    file_key="file_xxxxxxxx",
    output_dir="~/Downloads",
    filename="my_video.mp4"
)

if result["success"]:
    print(f"下载成功：{result['file_path']}")
else:
    print(f"下载失败：{result['error']}")
```

## 📋 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--url`, `-u` | 飞书消息链接 | 可选 |
| `--message-id`, `-m` | 消息 ID (om_xxx) | 可选 |
| `--file-key`, `-f` | 文件 key (file_xxx) | 可选 |
| `--output`, `-o` | 输出目录，默认为当前目录 | 可选 |
| `--filename`, `-n` | 保存的文件名 | 可选 |
| `--app-id` | 飞书应用 ID（可选） | 可选 |
| `--app-secret` | 飞书应用 Secret（可选） | 可选 |

## 📁 支持的文件类型

| 类型 | 扩展名 | 用途 |
|------|--------|------|
| 🎬 视频 | .mp4, .mov, .avi, .wmv | 视频编辑、平台发布 |
| 🖼️ 图片 | .jpg, .png, .gif, .webp | 设计素材、文档制作 |
| 📄 文档 | .pdf, .doc, .xls, .ppt | 本地编辑、存档 |
| 🎵 音频 | .mp3, .wav, .m4a | 音频处理、转录 |

## 🎯 典型使用场景

### 场景 1：飞书视频 → 抖音发布

```bash
# 步骤 1：下载飞书视频
python download.py \
  --message-id "om_x100b523c2b77fd30c24abb58a94deee" \
  --file-key "file_v3_0010e_dc672f40-87b6-4d67-b69d-e40290032c2g" \
  --output ~/.openclaw/workspace \
  --filename "douyin_video.mp4"

# 步骤 2：使用视频发布工具发布到抖音
# ...
```

### 场景 2：批量下载飞书文件

```python
from download import FeishuMessageDownloader
import os

downloader = FeishuMessageDownloader()

messages = [
    {"message_id": "om_xxx1", "file_key": "file_xxx1", "type": "video"},
    {"message_id": "om_xxx2", "file_key": "file_xxx2", "type": "image"},
    {"message_id": "om_xxx3", "file_key": "file_xxx3", "type": "document"},
]

for msg in messages:
    type_dir = os.path.join("~/Downloads/Feishu_Files", msg['type'])
    result = downloader.download_file(
        message_id=msg['message_id'],
        file_key=msg['file_key'],
        output_dir=type_dir
    )
    print(f"{'✅' if result['success'] else '❌'} {result.get('file_path', result.get('error'))}")
```

### 场景 3：AI 处理流程

```python
from download import FeishuMessageDownloader

# 下载视频
downloader = FeishuMessageDownloader()
result = downloader.download_file(message_id, file_key, "~/AI_Input")

if result["success"]:
    # 使用 AI 处理视频
    # ... AI 分析代码 ...
    pass
```

## 🔐 飞书应用权限要求

需要在飞书开放平台申请应用并配置以下权限：

- `im:resource` - 访问消息资源
- `im:message` - 读取消息内容（用于提取 file_key）

## ⚠️ 注意事项

1. **文件下载链接有过期时间** - 飞书文件通常在 7 天后过期，请及时下载
2. **大文件下载** - 大文件可能需要较长时间，请耐心等待
3. **权限要求** - 确保应用有访问该消息的权限
4. **存储空间** - 定期清理下载的文件，避免占用过多磁盘空间
5. **隐私合规** - 下载的文件仅供个人使用，注意数据安全和隐私保护

## 🛠️ 故障排查

### 问题 1：未找到飞书 App ID

**错误信息**: `未找到飞书 App ID`

**解决方案**:
- 检查是否已设置环境变量 `FEISHU_APP_ID`
- 或检查 `~/.openclaw/openclaw.json` 中是否配置了 `channels.feishu.appId`

### 问题 2：获取 access token 失败

**错误信息**: `获取 access token 失败`

**解决方案**:
- 检查 App ID 和 App Secret 是否正确
- 确认飞书应用已发布且有相应权限

### 问题 3：下载文件失败

**错误信息**: `下载文件失败`

**解决方案**:
- 检查 message_id 和 file_key 是否正确
- 确认文件未过期（飞书文件有效期 7 天）
- 检查网络连接是否正常

## 📚 相关资源

- [飞书开放平台文档](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)
- [飞书消息 API](https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN)
- [GitHub 仓库](https://github.com/Cindypapa/feishu-message-download)
- [ClawHub 页面](https://clawhub.ai/skills/feishu-message-download)

## 📝 更新日志

### v1.0.0 (2026-04-04)
- ✨ 初始版本发布
- 📥 支持飞书消息文件下载
- 🔗 支持消息链接解析
- 🔐 自动获取 access token
- 📁 自定义输出目录和文件名

## 👨‍💻 作者

勇哥的小飞侠 🧚🏻‍♀️🌸🧚🏻

## 📄 许可证

MIT License
