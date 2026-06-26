# 阿里云 OSS 技能 - 使用示例

本文档包含阿里云 OSS 技能的各种使用示例。

---

## 📤 示例1：上传文件

### 在 OpenClaw 中

**用户说：**
```
帮我上传 /backups/daily-20260301.tar.gz 到阿里云 OSS
```

**AI 执行：**
```
使用 Node.js SDK 脚本上传
```

**返回：**
```
✅ 上传成功！

文件：daily-20260301.tar.gz
大小：15.2 MB
URL：https://bucket.oss-cn-hangzhou.aliyuncs.com/backups/daily-20260301.tar.gz
```

### 命令行方式

```bash
node scripts/oss_node.mjs upload \
  --local /backups/daily-20260301.tar.gz \
  --key backups/daily-20260301.tar.gz
```

---

## 📋 示例2：列出文件

### 在 OpenClaw 中

**用户说：**
```
列出阿里云 OSS backups 目录下的所有文件
```

**返回：**
```
📋 共找到 15 个文件：

backups/backup-20260301.tar.gz  - 15.2 MB  - 2026-03-01 20:00
backups/backup-20260228.tar.gz  - 14.8 MB  - 2026-02-28 20:00
backups/backup-20260227.tar.gz  - 16.1 MB  - 2026-02-27 20:00
...
```

### 命令行方式

```bash
# 列出所有文件
node scripts/oss_node.mjs list

# 列出指定前缀的文件
node scripts/oss_node.mjs list --prefix backups/ --limit 50

# JSON 格式输出
node scripts/oss_node.mjs list --prefix backups/ --format json
```

---

## 🔗 示例3：获取文件 URL

### 在 OpenClaw 中

**用户说：**
```
给我 images/photo.jpg 的访问链接，1小时有效
```

**返回：**
```
🔗 临时访问链接（1小时有效）：

https://bucket.oss-cn-hangzhou.aliyuncs.com/images/photo.jpg?OSSAccessKeyId=...&Expires=...&Signature=...
```

### 命令行方式

```bash
# 公开 URL
node scripts/oss_node.mjs url --key images/photo.jpg

# 私有 URL（1小时有效）
node scripts/oss_node.mjs url --key documents/report.pdf --private --expires 3600
```

---

## 🗑️ 示例4：删除文件

### 在 OpenClaw 中

**用户说：**
```
删除阿里云 OSS 上的 old-backup.tar.gz
```

**AI 执行：**
```
1. 先确认：是否真的要删除？
2. 用户确认后执行删除
```

**返回：**
```
✅ 删除成功！

文件：old-backup.tar.gz
```

### 命令行方式

```bash
# 删除单个文件（需要确认）
node scripts/oss_node.mjs delete --key backups/old-backup.tar.gz

# 强制删除（不需要确认）
node scripts/oss_node.mjs delete --key backups/old-backup.tar.gz --force

# 批量删除
cat > delete-list.txt << EOF
backups/backup-20260101.tar.gz
backups/backup-20260102.tar.gz
EOF

node scripts/oss_node.mjs batch-delete --file delete-list.txt
```

---

## 📊 示例5：获取文件信息

### 在 OpenClaw 中

**用户说：**
```
查看 documents/report.pdf 的详细信息
```

**返回：**
```
📊 文件信息：

文件名：documents/report.pdf
大小：2.5 MB
类型：application/pdf
ETag："abc123..."
修改时间：2026-03-01 15:30:00
```

### 命令行方式

```bash
node scripts/oss_node.mjs stat --key documents/report.pdf
```

---

## 📥 示例6：下载文件

### 在 OpenClaw 中

**用户说：**
```
从阿里云 OSS 下载 documents/report.pdf 到本地
```

**返回：**
```
✅ 下载成功！

文件：documents/report.pdf
大小：2.5 MB
保存到：/downloads/report.pdf
```

### 命令行方式

```bash
node scripts/oss_node.mjs download \
  --key documents/report.pdf \
  --local /downloads/report.pdf
```

---

## 🤖 示例7：自动化备份脚本

### 完整脚本

```bash
#!/bin/bash

# 每日备份脚本
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d)
BACKUP_FILE="backup-${DATE}.tar.gz"

# 1. 创建备份
echo "📦 创建备份..."
tar -czf "${BACKUP_DIR}/${BACKUP_FILE}" /data

# 2. 上传到阿里云 OSS
echo "📤 上传到阿里云 OSS..."
cd /home/node/.openclaw/workspace/skills/aliyun-oss-skill
node scripts/oss_node.mjs upload \
  --local "${BACKUP_DIR}/${BACKUP_FILE}" \
  --key "backups/${BACKUP_FILE}"

# 3. 清理本地旧备份（保留7天）
echo "🗑️  清理旧备份..."
find ${BACKUP_DIR} -name "backup-*.tar.gz" -mtime +7 -delete

# 4. 清理云端旧备份（保留30天）
echo "🗑️  清理云端旧备份..."
node -e "
const { execSync } = require('child_process');
const cutoff = Date.now() - (30 * 24 * 60 * 60 * 1000);

const files = JSON.parse(execSync('node scripts/oss_node.mjs list --prefix \"backups/\" --format json'));

for (const file of files) {
  if (file.mtime * 1000 < cutoff) {
    execSync(\`node scripts/oss_node.mjs delete --key \${file.key} --force\`);
    console.log(\`已删除: \${file.key}\`);
  }
}
"

echo "✅ 备份完成！"
```

---

## 📝 示例8：批量操作

### 批量上传图片

```javascript
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const imageDir = '/path/to/images';
let uploaded = 0;

fs.readdirSync(imageDir).forEach(filename => {
  if (filename.endsWith('.jpg') || filename.endsWith('.png') || filename.endsWith('.gif')) {
    const localPath = path.join(imageDir, filename);
    const key = `images/${filename}`;

    try {
      execSync(`node scripts/oss_node.mjs upload --local "${localPath}" --key "${key}"`);
      console.log(`✅ ${filename} 上传成功`);
      uploaded++;
    } catch (error) {
      console.error(`❌ ${filename} 上传失败:`, error.message);
    }
  }
});

console.log(`\n✅ 共上传 ${uploaded} 个文件`);
```

---

## 🎯 更多示例

查看 [SKILL.md](../SKILL.md) 获取更多详细信息和 API 文档。
