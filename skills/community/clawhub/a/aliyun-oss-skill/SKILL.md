---
name: aliyun-oss
description: |
  阿里云 OSS 对象存储技能。支持文件上传、下载、列出、删除、获取 URL 等操作。
  两层架构：Node.js SDK（优先）→ ossutil CLI。
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["node"], "packages": ["ali-oss"] },
        "install":
          [
            { "id": "ali-oss-sdk", "kind": "node", "package": "ali-oss", "label": "Install ali-oss Node.js SDK" },
          ],
      },
  }
---

# ☁️ 阿里云 OSS 技能

通过 **Node.js SDK** / **ossutil CLI** 管理阿里云对象存储。

---

## 🎯 执行策略（两层降级）

| 优先级 | 工具 | 使用场景 |
|--------|------|----------|
| **1** | Node.js SDK (`ali-oss`) | 优先使用 |
| **2** | ossutil CLI | 备选 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/aliyun-oss-skill

# 运行自动安装
bash scripts/setup.sh
```

### 2. 配置凭证

```bash
bash scripts/setup.sh \
  --access-key-id "YOUR_ACCESS_KEY_ID" \
  --access-key-secret "YOUR_ACCESS_KEY_SECRET" \
  --region "oss-cn-hangzhou" \
  --bucket "mybucket"
```

### 3. 测试连接

```bash
node scripts/oss_node.mjs test-connection
```

---

## 📋 使用示例

### 上传文件

```bash
node scripts/oss_node.mjs upload \
  --local "/path/to/file.txt" \
  --key "uploads/file.txt"
```

### 列出文件

```bash
node scripts/oss_node.mjs list --prefix "uploads/" --limit 100
```

### 下载文件

```bash
node scripts/oss_node.mjs download \
  --key "uploads/file.txt" \
  --local "/path/to/save.txt"
```

### 删除文件

```bash
node scripts/oss_node.mjs delete --key "uploads/file.txt" --force
```

### 获取文件 URL

```bash
# 公开空间
node scripts/oss_node.mjs url --key "uploads/file.txt"

# 私有空间（1小时有效）
node scripts/oss_node.mjs url --key "uploads/file.txt" --private --expires 3600
```

---

## 🔧 Node.js SDK API

| 命令 | 说明 |
|------|------|
| `upload --local <path> --key <key>` | 上传文件 |
| `download --key <key> --local <path>` | 下载文件 |
| `list [--prefix <p>] [--limit <n>]` | 列出文件 |
| `delete --key <key> [--force]` | 删除文件 |
| `url --key <key> [--private] [--expires <s>]` | 获取 URL |
| `stat --key <key>` | 文件信息 |
| `move --src-key <a> --dest-key <b>` | 移动文件 |
| `copy --src-key <a> --dest-key <b>` | 复制文件 |
| `test-connection` | 测试连接 |

---

## ⚙️ 配置文件

**config/oss-config.json**

```json
{
  "accessKeyId": "YOUR_ACCESS_KEY_ID",
  "accessKeySecret": "YOUR_ACCESS_KEY_SECRET",
  "bucket": "mybucket",
  "region": "oss-cn-hangzhou",
  "domain": "https://cdn.example.com"
}
```

**常用区域**：
- `oss-cn-hangzhou` - 华东1（杭州）
- `oss-cn-shanghai` - 华东2（上海）
- `oss-cn-beijing` - 华北2（北京）
- `oss-cn-shenzhen` - 华南1（深圳）

---

## 🐛 故障排查

| 问题 | 解决 |
|------|------|
| `Cannot find module 'ali-oss'` | `npm install ali-oss` |
| `403 Forbidden` | 检查 AccessKey 权限 |
| `连接超时` | 检查区域代码和网络 |

---

## 📚 相关链接

- [阿里云 OSS Node.js SDK](https://help.aliyun.com/document_detail/32068.html)
- [ossutil 工具](https://help.aliyun.com/document_detail/120075.html)

---

## 📄 许可证

MIT License
