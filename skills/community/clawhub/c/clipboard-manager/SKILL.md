---
name: clipboard-manager
version: 1.0.0
description: 剪贴板历史管理工具。保存剪贴板历史，快速搜索和重复粘贴。适合频繁复制粘贴的用户。
author: 你的名字
triggers:
  - "剪贴板"
  - "复制历史"
  - "粘贴板"
  - "剪贴板历史"
---

# Clipboard Manager 📋

管理剪贴板历史，快速搜索和重复粘贴。

## 功能

- 📋 自动保存剪贴板历史
- 🔍 快速搜索历史记录
- 📌 固定常用内容
- 🗑️ 清理历史
- ⌨️ 快速粘贴

## 使用方法

### 查看历史

```bash
python3 scripts/clipboard.py history
```

### 搜索

```bash
python3 scripts/clipboard.py search "关键词"
```

### 固定内容

```bash
python3 clipboard.py pin 1
```

### 粘贴

```bash
python3 clipboard.py paste 1
```

### 清空历史

```bash
python3 clipboard.py clear
```

## 配置

```bash
# 最大保存条数
export CLIPBOARD_MAX=100
```

## 示例

```bash
# 查看最近10条
python3 scripts/clipboard.py history --limit 10

# 搜索包含 "密码" 的记录
python3 scripts/clipboard.py search "密码"

# 固定第1条
python3 scripts/clipboard.py pin 1
```
