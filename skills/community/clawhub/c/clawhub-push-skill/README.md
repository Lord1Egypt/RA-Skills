# ClawHub Push Skill

一键推送 skill 到 ClawHub registry，自动处理 `acceptLicenseTerms` 和文件格式问题。

## 问题背景

ClawHub CLI 在推送时遇到以下问题：
1. `acceptLicenseTerms: invalid value` - 缺少必要的许可确认字段
2. `tags: an array` - tags 必须是数组格式
3. Token 路径变更 - 新版在 `~/.config/clawhub/token.json`

## 安装

```bash
# 通过 ClawHub 安装（发布后）
clawhub install clawhub-push-skill

# 或手动安装
cd /path/to/skill
npm install -g .
```

## 使用方法

### 推送单个 skill

```bash
# 使用 SKILL.md 中的元数据推送
clawhub-push /path/to/skill

# 或指定参数
clawhub-push /path/to/skill --slug my-skill --version 1.0.0 --name "My Skill"
```

### 批量推送

```bash
# 推送 skills 目录下所有变更
clawhub-push-batch ./skills
```

## 技术实现

### 修复的核心问题

1. **Token 路径**：支持新旧两种 token 存储位置
   - 新版：`~/.config/clawhub/token.json`
   - 旧版：`~/.clawhub/token`

2. **Payload 格式**：
   ```json
   {
     "slug": "skill-slug",
     "version": "1.0.0",
     "displayName": "Skill Name",
     "tags": ["latest"],
     "acceptLicenseTerms": true
   }
   ```

3. **文件上传方式**：使用 FormData 分别上传每个文件，不用 tar.gz 打包

### API 端点

- **Registry**: `https://clawhub.ai`
- **Publish API**: `POST /api/v1/skills`
- **Auth**: `Authorization: Bearer <token>`

## 依赖

- Node.js 18+
- js-yaml
- FormData (Node 18+ 内置)

## License

MIT
