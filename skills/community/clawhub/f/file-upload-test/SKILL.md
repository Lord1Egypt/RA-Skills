---
name: file-upload
description: 上传文件到内部 BS3 存储（免签名）。Use when user asks to upload files, images, documents to storage, or get a shareable URL for a file.
metadata:
  {
    "openclaw":
      {
        "emoji": "📤",
        "requires": { "bins": ["python3"], "pip": ["boto3", "botocore"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "packages": ["boto3", "botocore"],
              "label": "Install boto3 and botocore via pip",
            },
          ],
      },
  }
---

# File Upload Skill

上传文件到内部 BS3 存储，生成可分享的文件 URL。

---

## 🔐 前置条件

### 1. 安装依赖

```bash
pip3 install boto3 botocore
```

### 2. 网络要求

- **内网访问**: 需要在内网环境使用
- **Endpoint**: `http://bs3-hb1.internal`
- **免签名**: 无需配置 AWS credentials

---

## 📦 功能说明

### 支持的操作

| 操作 | 说明 | 输入 | 输出 |
|------|------|------|------|
| `upload_file` | 上传本地文件 | 文件路径 | 文件 URL |
| `upload_bytes` | 上传二进制数据 | 文件名 + 数据 | 文件 URL |

### 特性

- ✅ **自动去重**: 上传文件名自动添加 8 位 UUID 前缀，防止重名覆盖
- ✅ **免签名**: 内网免认证，直接上传
- ✅ **固定 Bucket**: `kkim-mario-claw`
- ✅ **CDN 加速**: 返回 `bs3-hb1.corp.tencent.com` 域名 URL

---

## 🚀 使用方法

### 命令行方式

```bash
# 上传文件
python3 ~/.openclaw/workspace/skills/file-upload/upload.py upload_file /path/to/file.png

# 输出示例
https://bs3-hb1.corp.tencent.com/kim-mario-claw/abc12345_file.png
```

### Python API 方式

```python
from upload import upload_file, upload_bytes

# 上传文件
url = upload_file("my-image.png", "/path/to/file.png")
print(url)

# 上传二进制数据
with open("/path/to/file.png", "rb") as f:
    data = f.read()
url = upload_bytes("my-image.png", data)
print(url)
```

---

## 📋 使用场景

### 场景 1: 上传图片

**用户说:**
- "帮我上传这张图片"
- "把这个文件传到 BS3"
- "生成一个图片的分享链接"

**处理流程:**
1. 获取文件路径
2. 调用 `upload_file`
3. 返回 URL

### 场景 2: 上传文档

**用户说:**
- "上传这个 PDF 文件"
- "把报告传到存储"

**处理流程:**
1. 获取文件路径
2. 调用 `upload_file`
3. 返回 URL

### 场景 3: 上传二进制数据

**用户说:**
- "保存这段数据"
- "上传这个截图"

**处理流程:**
1. 获取二进制数据
2. 调用 `upload_bytes`
3. 返回 URL

---

## 📁 文件结构

```
~/.openclaw/workspace/skills/file-upload/
├── SKILL.md          # 技能文档
├── upload.py         # Python 脚本
└── .env              # 可选配置（如需要）
```

---

## ⚠️ 注意事项

### 1. 内网限制

- 只能在内网使用
- Endpoint: `http://bs3-hb1.internal`
- 外网无法访问

### 2. Bucket 说明

- **Bucket**: `kkim-mario-claw`
- **用途**: 临时存储，非永久保存
- **建议**: 重要文件请备份到其他存储

### 3. 文件名处理

- 自动添加 8 位 UUID 前缀
- 示例：`file.png` → `a1b2c3d4_file.png`
- 目的：防止同名文件覆盖

### 4. 返回 URL 格式

```
https://bs3-hb1.corp.tencent.com/kim-mario-claw/{uuid}_{filename}
```

### 5. 有效期

- **链接有效期：7 天**
- 超时后文件可能无法访问
- 重要文件请及时下载保存


## 📞 常见问题

### Q: 上传失败怎么办？

**检查项:**
1. ✅ 是否在内网
2. ✅ 是否安装了 `boto3` 和 `botocore`
3. ✅ 文件路径是否正确
4. ✅ 网络是否能访问 `bs3-hb1.internal`

### Q: 如何验证上传成功？

访问返回的 URL，能正常下载/查看即成功。

### Q: 文件会永久保存吗？

Bucket 名称包含 `temp`，建议作为临时存储，重要文件请备份。

---

*Last updated: 2026-03-07*
