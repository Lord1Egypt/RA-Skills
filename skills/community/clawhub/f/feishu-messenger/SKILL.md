# Feishu Messenger - 飞书消息发送技能

## 📋 技能概述

提供飞书消息发送能力，支持文本、图片、文件等多种消息类型。

**核心能力**:
- 📝 发送文本消息
- 📸 发送图片（自动预览）
- 📄 发送文件（任意格式）
- 🎯 支持私聊和群聊

---

## 🚀 快速开始

### 基础用法

```bash
# 发送文本消息
openclaw message send \
  --channel feishu \
  --target ou_xxxxx \
  --message "你好，这是一条测试消息"
```

### 发送图片

```bash
# 1. 复制图片到工作区
cp /path/to/image.png ~/.openclaw/workspace/

# 2. 发送（使用相对路径）
openclaw message send \
  --channel feishu \
  --target ou_xxxxx \
  --message "📸 测试图片" \
  --media ./image.png
```

### 发送文件

```bash
# 1. 复制文件到工作区
cp /path/to/document.pdf ~/.openclaw/workspace/

# 2. 发送（使用相对路径）
openclaw message send \
  --channel feishu \
  --target ou_xxxxx \
  --message "📄 文档请查收" \
  --media ./document.pdf
```

---

## 📚 完整参数

| 参数 | 简写 | 说明 | 必填 |
|------|------|------|------|
| `--channel` | - | 渠道类型 (`feishu`) | ✅ |
| `--target` | - | 接收者 ID (open_id 或 chat_id) | ✅ |
| `--message` | - | 消息文本 | ✅ |
| `--media` | - | 媒体文件路径（相对路径） | ❌ |
| `--filename` | - | 自定义文件名 | ❌ |

### Target 格式

```
# 私聊用户
ou_6650e2645a6e8f4c7363cbbfd6bbcf33

# 群聊
chat_xxxxx
```

---

## 🎯 使用场景

### 场景 1: 发送通知消息

```bash
openclaw message send \
  --channel feishu \
  --target ou_xxxxx \
  --message "⏰ 提醒：下午 3 点有会议"
```

### 场景 2: 发送截图

```bash
# 截取屏幕
screenshot /tmp/screenshot.png

# 复制到工作区并发送
cp /tmp/screenshot.png ~/.openclaw/workspace/
cd ~/.openclaw/workspace
openclaw message send \
  --channel feishu \
  --target ou_xxxxx \
  --message "📸 问题截图" \
  --media ./screenshot.png
```

### 场景 3: 发送日志文件

```bash
# 打包日志
tar -czf logs.tar.gz logs/

# 发送
cp logs.tar.gz ~/.openclaw/workspace/
cd ~/.openclaw/workspace
openclaw message send \
  --channel feishu \
  --target ou_xxxxx \
  --message "📦 日志文件已打包" \
  --media ./logs.tar.gz
```

### 场景 4: 批量发送通知

```bash
# 发送给多人
for user in ou_001 ou_002 ou_003; do
  openclaw message send \
    --channel feishu \
    --target $user \
    --message "📢 系统维护通知：今晚 23:00-01:00"
done
```

---

## ⚠️ 重要注意事项

### 路径要求（关键！）

| 路径类型 | 示例 | 结果 |
|---------|------|------|
| ✅ **相对路径** | `./image.png` | **正常显示** |
| ❌ 绝对路径 | `/tmp/image.png` | 可能失败或显示为附件 |
| ❌ 波浪号路径 | `~/image.png` | 被安全策略阻止 |

**最佳实践**: 始终将文件复制到工作区后使用 `./` 相对路径。

### 文件大小限制

| 类型 | 限制 |
|------|------|
| 图片 | 最大 10MB |
| 文件 | 最大 50MB |
| 视频 | 最大 100MB |

### 支持的文件格式

**图片**: PNG, JPG, GIF, WebP, BMP  
**文档**: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX  
**压缩**: ZIP, RAR, 7Z, TAR.GZ  
**其他**: TXT, CSV, MD, JSON, XML

---

## 🔧 Python API 调用

```python
import subprocess

def send_feishu_message(target, message, media_path=None):
    """发送飞书消息"""
    cmd = [
        'openclaw', 'message', 'send',
        '--channel', 'feishu',
        '--target', target,
        '--message', message
    ]
    
    if media_path:
        cmd.extend(['--media', media_path])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

# 使用示例
send_feishu_message(
    'ou_xxxxx',
    '📄 报告已生成',
    './report.pdf'
)
```

---

## 📝 完整工作流程

### 步骤 1: 准备文件

```bash
# 确保文件在工作区
cd ~/.openclaw/workspace

# 如果需要，从其他地方复制
cp /path/to/file.ext ./
```

### 步骤 2: 发送消息

```bash
openclaw message send \
  --channel feishu \
  --target ou_xxxxx \
  --message "消息内容" \
  --media ./file.ext
```

### 步骤 3: 验证结果

检查返回：
- ✅ `✅ Sent via Feishu. Message ID: om_xxxxx`
- ❌ 错误信息（检查路径、权限等）

---

## ⚠️ 常见问题

### 问题 1: 文件发送失败

**症状**: 提示找不到文件或发送失败

**解决**:
```bash
# 检查文件是否存在
ls -la ./file.ext

# 确保使用相对路径
# ✅ 正确：./file.ext
# ❌ 错误：/home/user/file.ext
```

### 问题 2: 图片显示为附件而不是预览

**症状**: 收到的是文件附件，不是图片预览

**原因**: 使用了绝对路径

**解决**:
```bash
# 复制文件到工作区
cp /tmp/image.png ~/.openclaw/workspace/

# 使用相对路径发送
cd ~/.openclaw/workspace
openclaw message send --media ./image.png ...
```

### 问题 3: 提示权限不足

**症状**: `Permission denied`

**解决**:
```bash
# 检查文件权限
chmod 644 ./file.ext

# 或重新复制文件
cp /path/to/file.ext ./
```

### 问题 4: 找不到 target ID

**症状**: 不知道用户的 open_id

**解决**:
```bash
# 方法 1: 从飞书 URL 获取
# 用户个人资料页面 URL 包含 open_id

# 方法 2: 使用飞书 API 查询
# 参考飞书开放平台文档

# 方法 3: 从消息事件获取
# 当用户发消息给你时，sender_id 就是 open_id
```

---

## 🎯 最佳实践

### 1. 文件管理

```bash
# 创建临时文件夹
mkdir -p ~/.openclaw/workspace/temp/

# 使用后清理
rm ~/.openclaw/workspace/temp/*
```

### 2. 消息模板

```bash
# 定义消息模板
NOTIFY_MSG="⏰ 提醒：{{content}}"
ERROR_MSG="❌ 错误：{{content}}"
SUCCESS_MSG="✅ 成功：{{content}}"

# 使用
openclaw message send \
  --channel feishu \
  --target ou_xxxxx \
  --message "${SUCCESS_MSG//\{\{content\}\}/任务完成}"
```

### 3. 错误处理

```bash
#!/bin/bash

send_with_retry() {
    local target=$1
    local message=$2
    local media=$3
    
    for i in {1..3}; do
        if openclaw message send \
            --channel feishu \
            --target "$target" \
            --message "$message" \
            --media "$media" 2>&1 | grep -q "✅ Sent"; then
            echo "发送成功"
            return 0
        fi
        echo "重试 $i/3..."
        sleep 2
    done
    
    echo "发送失败"
    return 1
}
```

---

## 📚 相关资源

- [飞书开放平台](https://open.feishu.cn/)
- [OpenClaw message 文档](https://docs.openclaw.ai/tools/message)
- [飞书消息 API](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)

---

## 🧪 测试清单

### 已完成测试 ✅

| 类型 | 文件 | 状态 | 消息 ID |
|------|------|------|---------|
| 文本消息 | - | ✅ | - |
| PNG 图片 | smiley_test.png | ✅ | om_x100b547f66ac7ca4c4acde68c243266 |
| TXT 文件 | test_file.txt | ✅ | om_x100b547f735e00a0b27929fac63a897 |
| PDF 文档 | test_doc.pdf | ✅ | om_x100b547f09b4e500c2a36e51156b11b |
| Word 文档 | test_doc.docx | ✅ | om_x100b547f092a08acc3e8972049d6347 |
| 相对路径 | ./xxx | ✅ | - |

### 待测试 ⏳

- [ ] 发送群聊消息
- [ ] 发送大文件 (>10MB)
- [ ] 发送 Excel 表格
- [ ] 发送 PPT 演示文稿

---

**版本**: v1.1  
**创建时间**: 2026-03-14 09:05 AM  
**更新时间**: 2026-03-14 09:06 AM  
**作者**: Han's AI Assistant  
**状态**: ✅ 已验证 (文本/图片/TXT/PDF/Word)
