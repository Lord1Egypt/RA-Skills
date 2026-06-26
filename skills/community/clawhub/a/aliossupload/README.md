# AliOSSUpload

阿里云 OSS 文件上传工具 Skill，用于 OpenClaw 代理。

## 功能特性

- ✅ 单文件上传到阿里云 OSS
- ✅ 自动读取环境变量配置
- ✅ 返回文件访问 URL
- ✅ 支持自定义 OSS 路径

## 前置要求

1. 阿里云账号
2. 已开通 OSS 服务
3. 已创建 OSS 存储桶（Bucket）

## 环境变量配置

在使用前，需要设置以下环境变量：

```bash
export ALIYUN_OSS_ACCESS_KEY_ID="your-access-key-id"
export ALIYUN_OSS_ACCESS_KEY_SECRET="your-access-key-secret"
export ALIYUN_OSS_ENDPOINT="oss-cn-beijing.aliyuncs.com"
export ALIYUN_OSS_BUCKET="your-bucket-name"
```

### 获取阿里云 AccessKey

1. 登录 [阿里云控制台](https://www.aliyun.com/)
2. 右上角头像 → AccessKey 管理
3. 创建 AccessKey（建议创建 RAM 子账号，授予最小权限）

### RAM 权限策略建议

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "oss:PutObject",
        "oss:GetObject"
      ],
      "Resource": [
        "acs:oss:*:*:your-bucket-name/*"
      ]
    }
  ]
}
```

## 安装

```bash
# 使用 clawhub 安装
npx clawhub install aliossupload

# 或者手动安装到 OpenClaw skills 目录
cp -r aliossupload ~/.agents/skills/
```

## 使用方法

### 在 OpenClaw 中使用

安装后，OpenClaw 会自动加载该 skill。你可以通过自然语言指令使用：

```
"帮我把 /path/to/file.mp4 上传到 OSS"
"上传这个文件到阿里云"
"将图片传到 OSS 并给我链接"
```

### 在 Python 代码中使用

```python
from aliossupload import AliOSSUploader

# 初始化上传器
uploader = AliOSSUploader()

# 上传文件
result = uploader.upload_file(
    local_path="/path/to/local/file.mp4",
    oss_key="videos/my-video.mp4"
)

# 获取上传结果
print(result['url'])  # 文件访问 URL
print(result['key'])  # OSS 中的文件路径
```

## 返回结果格式

```python
{
    "success": True,
    "url": "https://your-bucket.oss-cn-beijing.aliyuncs.com/videos/my-video.mp4",
    "key": "videos/my-video.mp4",
    "bucket": "your-bucket-name",
    "size": 1024000,
    "mime_type": "video/mp4"
}
```

## 常见问题

### Q: 上传失败，提示 "AccessDenied"
A: 检查 AccessKey 是否有 OSS 写入权限，建议检查 RAM 权限策略。

### Q: 上传成功但访问 URL 返回 403
A: Bucket 可能设置为私有，需要生成带签名的 URL，或在 Bucket 设置中开启公共读。

### Q: 环境变量已设置但读取不到
A: 确保环境变量已 export，且在当前 shell 会话中。可以将 export 命令添加到 `~/.bashrc` 或 `~/.zshrc`。

## 许可证

MIT

## 作者

[Your Name]

## 相关链接

- [阿里云 OSS 文档](https://help.aliyun.com/product/31815.html)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [ClawHub](https://clawhub.ai)
