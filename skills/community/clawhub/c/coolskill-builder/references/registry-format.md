# Registry 格式规范

## 目录结构

```
registry/
├── index.json                    # 全局索引：只存元数据
└── {skill-id}/                   # 例：data-parse-7a2
    ├── v1.0.0/                   # 版本 1.0.0（只读归档）
    │   ├── skill.yaml
    │   ├── impl.py
    │   ├── test.py
    │   └── manifest.json
    ├── v1.0.1/                   # 版本 1.0.1（当前 latest）
    │   └── ...
    └── latest -> v1.0.1          # 符号链接或索引指向
```

## index.json 格式

```json
{
  "skills": {
    "{skill-id}": {
      "name": "{skill_name}",
      "latest": "{version}",
      "versions": {
        "{version}": {
          "st": "stable|draft|deprecated",
          "t": "ISO8601-timestamp",
          "path": "{skill-id}/{version}"
        }
      }
    }
  }
}
```

## 版本递增规则

| 场景 | 当前版本 | 新版本 |
|------|---------|--------|
| 首次生成 | — | 1.0.0 |
| 迭代/修复 | 1.0.0 | 1.0.1 |
| 功能重大变更 | 1.0.1 | 1.1.0 |
| 破坏性重构 | 1.1.0 | 2.0.0 |

历史版本永久保留，禁止覆盖。

## GitHub 同步（可选）

环境变量：
- `GITHUB_TOKEN`: GitHub Personal Access Token
- `GITHUB_REPO`: 格式 `owner/repo`

使用 urllib.request + json + os + base64 实现，零第三方依赖。

首次配置检测：若环境变量缺失，输出配置提示并继续本地注册。
