# Smart Commit — 变更分析规则

> 版本: v1.0.0 | 更新: 2026-05-21

## 一、Type 判定决策树

```
收到 diff/变更描述
    │
    ├── 新增文件/函数/功能？
    │   └── 是 → feat
    │
    ├── 修复了错误行为？
    │   └── 是 → fix
    │
    ├── 只改了格式/空格/分号？
    │   └── 是 → style
    │
    ├── 移动/重命名/拆分代码，功能不变？
    │   └── 是 → refactor
    │
    ├── 改了文档/注释？
    │   └── 是 → docs
    │
    ├── 新增或修改测试？
    │   └── 是 → test
    │
    ├── 改了构建/依赖/配置？
    │   └── 是 → chore/build/ci（选最具体的）
    │
    ├── 改善了性能（不改变功能）？
    │   └── 是 → perf
    │
    └── 混合变更？
        └── 按最主要变更定 type，body 中说明其他变更
```

## 二、Scope 自动推断规则

### 2.1 从文件路径推断

| 文件路径模式 | 建议 scope |
|-------------|-----------|
| `src/auth/**` | `auth` |
| `src/api/**` | `api` |
| `src/models/**` | `model` 或具体模型名 |
| `src/utils/**` | `utils` |
| `src/components/**` | 组件名 |
| `tests/**` | 被测模块名 |
| `docs/**` | 文档类型 |
| `config/**` | `config` |
| `Dockerfile`, `docker-compose*` | `docker` |
| `package.json`, `go.mod` | `deps` |
| `.github/**` | `ci` |
| `README*`, `CHANGELOG*` | `docs` |

### 2.2 从变更内容推断

| 关键词 | scope |
|--------|-------|
| 登录/注册/认证/授权 | `auth` |
| 数据库/migration/SQL | `db` |
| 缓存/redis/memcached | `cache` |
| 支付/订单/退款 | `payment` |
| 搜索/索引/query | `search` |
| 上传/下载/文件 | `storage` |
| 日志/监控/metrics | `logging` 或 `monitor` |
| 邮件/短信/通知 | `notification` |

## 三、风险等级评估

### 3.1 低风险 🟢

- 纯文档变更
- 新增测试
- 代码格式调整
- 新增独立功能（不修改现有代码）
- README/注释更新

### 3.2 中风险 🟡

- 重构公共工具函数
- 修改配置文件
- 升级依赖版本（非大版本）
- 修改构建脚本
- 新增 API 端点

### 3.3 高风险 🔴

- 修改公开 API 签名
- 修改数据库 schema
- 修改认证/权限逻辑
- 修改支付/交易流程
- 删除功能/字段
- 主版本依赖升级

## 四、自动检测模式

### 4.1 检测项目语言

```
文件后缀 → 项目语言 → commit 风格建议
.go      → Go       → 英文，简洁
.java    → Java     → 英文或中文
.py      → Python   → 英文
.ts/.js  → TS/JS    → 英文
.rs      → Rust     → 英文
```

### 4.2 检测项目规范

如果项目中存在以下文件，调整输出：
- `.commitlintrc*` → 遵循项目 commitlint 配置
- `.conventionalcommits` → 确认使用 Conventional Commits
- `CONTRIBUTING.md` → 遵循贡献指南中的 commit 规范
- `.github/PULL_REQUEST_TEMPLATE.md` → PR 描述按模板

## 五、Diff 分析提示词

当需要从 diff 中提取信息时，按以下维度分析：

1. **统计维度**：新增几行/删除几行/涉及几个文件
2. **语义维度**：这些变更在做什么（新功能/修bug/重构...）
3. **关联维度**：这些文件之间有什么关系（同属一个模块/上下游依赖）
4. **风险维度**：有没有潜在副作用（API变更/数据迁移/权限修改）
5. **完整性维度**：有没有遗漏（改了代码没改测试/改了接口没改文档）
