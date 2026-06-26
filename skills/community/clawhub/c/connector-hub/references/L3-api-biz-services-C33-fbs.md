# C33 - 福帮手

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C33 |
| 连接器名 | fbs-connector |
| 显示名 | 福帮手 |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 业务服务 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 服务请求 | 创建服务请求 |
| 状态查询 | 查询请求状态 |
| 工单管理 | 工单创建/查询 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
└── L3-api-biz-services-C33-fbs-create-request.py  # 创建服务请求
```

### 环境变量配置

```bash
export FBS_API_KEY="your_api_key"
```

### 鉴权方式

**API Key**：
1. 在平台开放平台注册账号
2. 获取 API Key
3. 请求时携带 API Key

**环境变量配置**：
```bash
export API_KEY="your_api_key"
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
| 凭证更新 | 重新申请 API Key |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 迁移 | 重配连接器 | 改 API 地址 |
