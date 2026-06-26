# C25 - CNB 司内版

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C25 |
| 连接器名 | cnb-woa |
| 显示名 | CNB 司内版 |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 代码托管 |
| 替代难度 | 简单 |

## 连接器能力

同 CNB，司内版本。

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L3-api-code-hosting-C25-cnb-woa-repo-operations.py  # 仓库操作
└── L3-api-code-hosting-C25-cnb-woa-mr-operations.py    # MR 操作
```


### 鉴权方式

**Token**：
1. 在平台开放平台注册账号
2. 获取 Personal Access Token
3. 请求时携带 Token

**环境变量配置**：
```bash
export API_TOKEN="your_token"
```

### 核心脚本示例

使用 connector-hub 技能中的脚本：

```bash
python scripts/$(basename "$f" .md).py [参数]
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| API 变更 | 改 API 域名即可 |
| 凭证更新 | 重新申请 Token |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 迁移 | 重配连接器 | 改 API 地址 |
