---
name: ClawHub Push Skill
slug: clawhub-push-skill
description: "一键推送 skill 到 ClawHub registry，自动处理 acceptLicenseTerms 和文件格式问题"
type: skill
version: 1.0.0
author: Lin
license: MIT
---

# ClawHub Push Skill

自动修复 ClawHub CLI 的 `acceptLicenseTerms` bug，一键推送 skill 到 ClawHub registry。

## 功能

- ✅ 自动获取正确的 token 路径（支持新版 `~/.config/clawhub/token.json`）
- ✅ 自动修复 `acceptLicenseTerms` 参数问题
- ✅ 自动处理 `tags` 数组格式
- ✅ 支持单个文件上传（不打包）
- ✅ 支持批量推送整个目录

## 使用方法

### 推送单个 skill

```bash
# 使用默认配置推送
clawhub-push /path/to/skill

# 或指定 slug 和版本
clawhub-push /path/to/skill --slug my-skill --version 1.0.0
```

### 批量推送

```bash
# 推送 skills 目录下所有变更
clawhub-push-batch ~/.openclaw/workspace/skills
```

## 技术细节

### 修复的问题

1. **Token 路径问题**：新版 ClawHub 将 token 存储在 `~/.config/clawhub/token.json`，旧版在 `~/.clawhub/token`

2. **acceptLicenseTerms 问题**：CLI 的 FormData 中缺少该字段，需要在 payload JSON 中添加 `acceptLicenseTerms: true`

3. **Tags 格式问题**：`tags` 必须是数组 `["latest"]` 而不是字符串

4. **文件上传方式**：必须用 `-F "files=@文件名"` 分别上传每个文件，不能用 tar.gz 打包

### API 端点

- Registry: `https://clawhub.ai`
- Publish API: `POST /api/v1/skills`
- Payload 格式：
  ```json
  {
    "slug": "skill-slug",
    "version": "1.0.0",
    "displayName": "Skill Name",
    "tags": ["latest"],
    "acceptLicenseTerms": true
  }
  ```

## Changelog

### 1.0.0
- Initial release
- 修复 acceptLicenseTerms bug
- 支持单个和批量推送
- 自动检测 token 位置
