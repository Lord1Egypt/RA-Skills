# AI办公本 Skill

AI办公本 Skill 用于在 OpenClaw 中访问 思必驰AI办公本能力：

- 笔记：列表、详情、删除
- 待办：增删改查
- 标签知识库：同步、查询、绑定
- 个人数据库检索：笔记/待办语义搜索

## 安装

将本目录作为 skill 包导入 OpenClaw，核心文件为 `SKILL.md`。

## 运行前准备

建议配置环境变量：

```bash
export AIWORK_BASE_URL="https://aiworks.cn"
```

## 认证说明

- `authToken`（`AIWORK_AUTH_TOKEN`） 在开放平台安装 Skill 时下发给 OpenClaw。
- 受保护接口统一 Header：
  - `Authorization: Bearer {AIWORK_AUTH_TOKEN}`

## 文档索引

- 完整 API：`api_reference.md`
- 技能说明：`SKILL.md`
- 细节补充：`references/api-details.md`
