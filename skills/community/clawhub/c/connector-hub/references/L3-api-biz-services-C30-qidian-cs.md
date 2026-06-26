# C30 - 腾讯企点客服

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C30 |
| 连接器名 | tencent-qidian-cs |
| 显示名 | 腾讯企点客服 |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 业务服务 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 会话管理 | 创建/查询会话 |
| 消息发送 | 发送客服消息 |
| 工单管理 | 创建/查询工单 |
| 统计查询 | 客服统计数据 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L3-api-biz-services-C30-qidian-cs-create-session.py  # 创建会话
└── L3-api-biz-services-C30-qidian-cs-send-reply.py      # 发送回复
```

### 环境变量配置

```bash
export QIDIAN_CS_APP_ID="your_app_id"
export QIDIAN_CS_APP_SECRET="your_app_secret"
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
