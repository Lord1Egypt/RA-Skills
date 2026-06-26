# 状态文件结构约定

状态文件路径：

`~/.openclaw/state/hugo-publisher-state.json`

## JSON Schema（逻辑约束，多工作目录）

```json
{
  "activeWorkspace": "/absolute/path/to/hugo/workspace",
  "projects": {
    "/absolute/path/to/hugo/workspace": {
      "gitRoot": "/absolute/path/to/hugo/workspace",
      "currentBranch": "main",
      "templateType": "builtin",
      "templateName": "PaperMod",
      "templateSource": "https://github.com/adityatelange/hugo-PaperMod.git",
      "lastPreviewCommand": "hugo server --buildDrafts --bind 127.0.0.1 --port 1313",
      "lastPreviewUrl": "http://127.0.0.1:1313",
      "unpublishedArticleCount": 2,
      "hasUnpublishedArticles": true,
      "lastCommitHash": "a1b2c3d",
      "lastCommitMessage": "docs(hugo): publish new post",
      "deployProvider": "github-pages",
      "deployWorkflowFile": ".github/workflows/hugo-pages.yml",
      "deployGuidePath": "/absolute/path/to/hugo/workspace/hugo-github-deploy-guide.md",
      "customDomain": "blog.example.com",
      "domainConfigFiles": [
        "hugo.toml",
        "static/CNAME"
      ],
      "lastDeployUrl": "https://example.github.io/blog/",
      "lastDeployStatus": "success",
      "initialized": true,
      "updatedAt": "2026-03-23T10:00:00Z"
    }
  },
  "updatedAt": "2026-03-23T10:00:00Z"
}
```

## 字段定义

| 字段 | 必填 | 说明 |
|------|------|------|
| `activeWorkspace` | 是 | 当前激活的工作目录 |
| `projects` | 是 | 按工作目录分组的项目状态映射 |
| `projects.<workspace>.gitRoot` | 是 | 对应项目 Git 根目录 |
| `projects.<workspace>.currentBranch` | 否 | 当前分支名 |
| `projects.<workspace>.templateType` | 否 | 模板类型：`builtin`、`custom`、`empty` |
| `projects.<workspace>.templateName` | 否 | 模板名，例如 `PaperMod` |
| `projects.<workspace>.templateSource` | 否 | 模板来源（Git URL 或 `builtin:<name>`） |
| `projects.<workspace>.lastPreviewCommand` | 否 | 最近一次预览命令 |
| `projects.<workspace>.lastPreviewUrl` | 否 | 最近一次预览地址 |
| `projects.<workspace>.unpublishedArticleCount` | 否 | 未发布文章变更数量 |
| `projects.<workspace>.hasUnpublishedArticles` | 否 | 是否存在未发布文章 |
| `projects.<workspace>.lastCommitHash` | 否 | 最近一次提交短哈希 |
| `projects.<workspace>.lastCommitMessage` | 否 | 最近一次提交信息 |
| `projects.<workspace>.deployProvider` | 否 | 部署渠道，例如 `github-pages` |
| `projects.<workspace>.deployWorkflowFile` | 否 | 工作流文件路径 |
| `projects.<workspace>.deployGuidePath` | 否 | 部署引导文档路径，固定在工作目录下 |
| `projects.<workspace>.customDomain` | 否 | 自定义域名（如 `blog.example.com`） |
| `projects.<workspace>.domainConfigFiles` | 否 | 域名修改涉及的文件列表 |
| `projects.<workspace>.lastDeployUrl` | 否 | 最近一次部署可访问 URL |
| `projects.<workspace>.lastDeployStatus` | 否 | 最近一次部署状态（`success`/`failed`/`pending`） |
| `projects.<workspace>.initialized` | 否 | 是否完成首次初始化闭环 |
| `projects.<workspace>.updatedAt` | 是 | 项目级更新时间 |
| `updatedAt` | 是 | 全局更新时间 |

## 更新时机

必须在以下时机写回状态：

1. 成功解析或切换工作目录后
2. Hugo 模板初始化或模板选择确认后
3. Git 仓库检测/初始化完成后
4. Hugo 预览成功后
5. 检测到未发布文章数量变化后
6. Git 提交完成后
7. GitHub Actions 部署状态更新后
8. 任务异常退出前（写入当前上下文，便于恢复）

## 读取策略

1. 优先读取 `activeWorkspace` 作为默认上下文。
2. 若用户本轮显式指定目录，切换 `activeWorkspace` 并定位到 `projects[workspace]`。
3. 若 `projects[workspace]` 不存在，创建新项目状态并进入首次初始化阶段。

## 兼容与容错

- 允许缺失非必填字段，不应阻断流程。
- 发现路径不存在时，不直接失败；进入“目录确认/创建”引导。
- 发现 `lastPreviewUrl` 不可访问时，仅作为历史信息展示，不视为错误。
- `projects` 中存在多个目录时，只更新当前 `activeWorkspace` 对应项。
