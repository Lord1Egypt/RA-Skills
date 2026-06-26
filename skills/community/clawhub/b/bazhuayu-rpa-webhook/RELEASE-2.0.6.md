# Release Notes - v2.0.6

**发布日期**: 2026-03-09  
**类型**: Bug 修复版本

---

## 📋 变更概述

v2.0.6 修复了运行任务时企业 ID 显示错误的问题。

---

## 🐛 修复内容

### 问题描述

运行任务时出现以下错误：
```
NameError: name 'enterpriseId' is not defined
```

### 问题原因

在 `bazhuayu-webhook.py` 第 455 行，代码检查了 `enterpriseId` 是否在响应中，但打印时直接使用了未定义的变量名，而不是从 `result` 字典中取值。

### 修复方案

**修改前**:
```python
if 'enterpriseId' in result:
    print(f"企业 ID: {enterpriseId}")  # ❌ 变量未定义
```

**修改后**:
```python
if 'enterpriseId' in result:
    print(f"企业 ID: {result['enterpriseId']}")  # ✅ 从字典取值
```

---

## 📦 文件变更

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `bazhuayu-webhook.py` | 修复 | 修复企业 ID 显示错误 |
| `package.json` | 更新 | 版本号 2.0.5 → 2.0.6，更新 release_notes |

---

## 🎯 影响范围

- ✅ **功能影响**: 无（仅显示问题，不影响实际调用）
- ✅ **兼容性**: 完全向后兼容
- ✅ **数据影响**: 无

---

## 📦 升级指南

### 从 ClawHub 升级

```bash
clawhub update bazhuayu-webhook
```

### 从 GitHub 升级

```bash
cd /root/.openclaw/workspace/skills/bazhuayu-webhook
git pull origin main
```

### 手动安装

```bash
# 删除旧版本
rm -rf /root/.openclaw/workspace/skills/bazhuayu-webhook

# 重新安装
clawhub install bazhuayu-webhook
```

---

## ✅ 验证清单

升级后请验证：

- [ ] 运行任务不再出现 NameError
- [ ] 企业 ID 正确显示在输出中
- [ ] 任务调用成功（HTTP 200）

---

## 📝 示例输出

### 修复前 ❌

```
=== 响应结果 ===
HTTP 状态码：200
✅ 调用成功!
应用 ID (flowId): 67f495bb3f3b31fab6cd9229
运行批次 (flowProcessNo): 639086217362023783
Traceback (most recent call last):
  ...
NameError: name 'enterpriseId' is not defined
```

### 修复后 ✅

```
=== 响应结果 ===
HTTP 状态码：200
✅ 调用成功!
应用 ID (flowId): 67f495bb3f3b31fab6cd9229
运行批次 (flowProcessNo): 639086220306619793
企业 ID: 9b91e297-d0ec-48b9-847e-33123b7200b8
```

---

## 📚 相关资源

- **GitHub 仓库**: https://github.com/blogwebsem/bazhuayu-rpa-webhook
- **ClawHub**: https://clawhub.ai/skills/bazhuayu-webhook
- **八爪鱼 RPA**: https://rpa.bazhuayu.com/

---

**快速修复，让输出更清晰！** 🚀
