---
name: cloud-2
slug: cloud-2
displayName: "Cloud"
version: "1.0.0"
summary: "跨iCloud/Google Drive/Dropbox选理同步分享备份个人文件"
description: "跨iCloud/Google Drive/Dropbox选理同步分享备份个人文件。Choose, organize, sync, share, and back up personal files across iCloud,。触发关键词: sync, cloud, organize, choose, share。"
license: "MIT"
tools:
  - read
---

# Cloud

## Triggers

Activate on: iCloud full, cloud storage, backup photos, sync between devices, share folder, Google Drive help, Dropbox issues, "where are my files", storage plan comparison.

## Scope

This skill covers **consumer cloud storage** — the services regular people use for photos, documents, and backups.

**Not this skill:** AWS, Azure, S3 buckets, VPS, Docker, APIs → use `infrastructure`, `s3`, or `server`.

## Quick Service Picker

| Your devices | Best fit | Why |
| --- | --- | --- |
| iPhone + Mac | iCloud | Native integration, seamless |
| Android + Chrome | Google Drive | Included with Gmail, auto photo backup |
| Windows PC | OneDrive | Built into Windows, Office integration |
| Mixed devices | Dropbox | Works equally well everywhere |

For detailed pricing and features, see `services.md`.

## Common Confusions

| What you think | What's actually happening |
| --- | --- |
| "I deleted it from my phone and now it's gone from my laptop" | Sync works as designed — one file, everywhere |
| "iCloud storage full but my phone has space" | Phone storage ≠ iCloud storage |
| "My photos are duplicated everywhere" | Multiple services backing up the same camera roll |
| "I pay for 3 cloud services" | Pick one primary, cancel the rest |

## Storage Full — What to Do

1. **Check what's using space** — Photos usually dominate
2. **Empty trash** — Deleted files count until trash is emptied
3. **Disable duplicate backups** — Pick one photo backup service
4. **Offload old files** — Move archives to external drive

For service-specific cleanup steps, see `cleanup.md`.

## Backup Strategy

* **3-2-1 rule:** 3 copies, 2 different media, 1 offsite
* **Cloud counts as offsite** — but also keep a local backup
* **Check backup status monthly** — don't assume it's working

What to back up and what NOT to store in cloud: see `backup.md`.

## Sharing Files

| Need | Method |
| --- | --- |
| Quick share with anyone | Link (set expiration) |
| Ongoing family access | Shared folder |
| Sensitive documents | Don't use cloud, or encrypt first |

Step-by-step per service: see `sharing.md`.

## Security Basics

* **Enable 2FA** on all cloud accounts
* **Review shared links** quarterly — revoke old ones
* **Don't store unencrypted:** passwords, IDs, financial documents

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent( Code / Cursor / Codex /  CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务

## 核心能力

- Choose, organize, sync, share, and back up personal files across iCloud,
  Google Drive, Dropbox, a
- 触发关键词: sync, cloud, organize, choose, share

## 适用场景

| 场景 | 输入 | 输出 |
|------|------|------|
| 基础使用 | 用户请求 | 处理结果 |

**不适用于**：需要人工判断的复杂决策场景

## 使用流程

1. 确认运行环境满足依赖说明中的要求
2. 根据适用场景选择合适的使用方式
3. 执行操作并检查输出结果
4. 如遇错误，参考错误处理章节

## 示例

### 示例1：基础用法

```
输入: 用户请求
处理: 根据使用流程执行
输出: 处理结果
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 检查网络连接后重试，参考国内替代方案 |

## 常见问题

### Q1: 如何开始使用Cloud？
A: 请先阅读使用流程章节，确认环境满足依赖说明中的要求。

### Q2: 遇到错误怎么办？
A: 请参考错误处理章节，按照表格中的处理方式操作。

### Q3: Cloud有什么限制？
A: 请参考已知限制章节了解具体限制。

## 已知限制

- 需要API Key，无Key环境无法使用
- 依赖云服务，需要网络连接
