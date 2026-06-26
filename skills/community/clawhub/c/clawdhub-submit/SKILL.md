---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 5eb26843fb91efc246502b0e56d5f566
    PropagateID: 5eb26843fb91efc246502b0e56d5f566
    ReservedCode1: 3046022100efa81f19ced3305b14d7a9cb9cc41d0296403c489eae7eb8da5b7c6ffa6809eb022100a7ad882a4d493992b10642cfe599fecdd41516cc2562916422fca86e19839dec
    ReservedCode2: 3045022100faadfbb863a85d110aeaea25c467102581292eb83809c41fc0856fc885b949db022024ab3430faa50e9c7e07734ddd9c3a61d2e92a6b2d0eb58130c9d2ac29eb34db
---

# ClawdHub Skill 提交工具

自动引导用户完成 ClawdHub skill 发布流程。

## 触发条件

当用户提到以下关键词时激活：
- "提交 skill"
- "发布 skill"
- "上传 skill"
- "clawdhub submit"
- "skill 被关闭"
- "PR 自动关闭"

## 功能

### 1. 诊断问题

检测以下常见问题：
- Token 是否已接受许可条款
- Skill 文件结构是否正确
- _meta.json 格式是否有效

### 2. 解决指南

#### 问题1：Token 未接受许可条款

**症状**：
```
Publish payload: acceptLicenseTerms: invalid value
```

**解决方法**：
1. 打开 https://clawdhub.ai/upload
2. 使用 GitHub 账号登录
3. 在网页上接受开发者条款
4. 完成后回来重新发布

#### 问题2：Skill 文件结构错误

**必需文件**：
```
skill-name/
├── SKILL.md        # 必需：使用文档
├── _meta.json      # 可选：元信息
└── scripts/        # 可选：支持脚本
```

**_meta.json 示例**：
```json
{
  "slug": "my-skill",
  "name": "我的技能",
  "version": "1.0.0",
  "description": "技能描述",
  "tags": ["工具", "实用"]
}
```

### 3. 一键检查清单

检查本地 skill 目录：
```bash
# 1. 检查 SKILL.md 存在
ls -la */SKILL.md

# 2. 检查 _meta.json 格式
cat */_meta.json | python3 -m json.tool

# 3. 检查文件大小（太大会被拒绝）
du -sh */
```

### 4. 备用方案

如果网页端遇到问题，可尝试：

#### 方案A：本地 CLI 发布
```bash
# 安装 clawdhub
npm install -g clawdhub

# 登录（需要网页端先接受条款）
clawdhub login --token YOUR_TOKEN

# 发布
clawdhub publish ./your-skill --name "你的技能" --slug "your-skill"
```

#### 方案B：GitHub Fork + 网站导入
1. Fork https://github.com/openclaw/skills
2. 在自己仓库添加 skill
3. 在 clawdhub.ai 使用 "Import from GitHub" 功能

## 重要说明

### 为什么 PR 被自动关闭？

openclaw/skills 仓库是**只读镜像**，所有内容自动从 clawdhub.com 同步。**不接受直接 PR**。

### 正确发布流程

```
本地开发 → clawdhub.ai 上传 → 自动同步到 GitHub
```

### ClawdHub vs GitHub

| 平台 | 用途 |
|------|------|
| clawdhub.ai | **主站**：发布、管理 skill |
| github.com/openclaw/skills | **镜像**：只读备份 |

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| acceptLicenseTerms invalid | 未在网页接受条款 | 去网页登录接受 |
| Rate limit exceeded | API 请求过多 | 等待 1 分钟重试 |
| SERVICE_NOT_AVAILABLE | 部分 API 需要企业认证 | 使用基础 API |
| 401 Unauthorized | Token 无效或过期 | 重新登录 |

## 技术细节

### ClawdHub CLI

```bash
# 搜索 skill
clawdhub search 高德

# 安装 skill
clawdhub install amap-search

# 查看已安装
clawdhub list

# 更新所有
clawdhub update
```

### API 端点

- 网站：https://clawdhub.ai
- 文档：https://docs.openclaw.ai/zh-CN/tools/clawhub
- GitHub：https://github.com/clawd-hub/clawdhub
