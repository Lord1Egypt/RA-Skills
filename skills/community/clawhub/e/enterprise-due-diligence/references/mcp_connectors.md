# MCP 连接器参考

## 企查查公开接口

### 接口地址
```
https://open.api.qichacha.com
```

### 所需配置
1. 前往 https://open.api.qichacha.com 注册开发者账号
2. 获取 API Token
3. 设置环境变量 QICHACHA_TOKEN

### 支持的查询能力
- 企业工商信息：名称、统一社会信用代码、法人、注册资本
- 股权结构：股东列表、持股比例
- 司法诉讼：诉讼记录、被执行信息
- 知识产权：商标、专利、软著
- 变更记录：法人/注册资本/地址变更
- 行政处罚：处罚记录
- 分支机构
- 对外投资

### 当前状态
**未启用** — 通过 public API 使用

### 启用步骤
1. 注册企查查开发者账号，获取 Token
2. 设置环境变量 QICHACHA_TOKEN
3. 脚本已预留接口，自动检测 Token 可用性

---

## 天眼查 MCP Connector

### 端点
```
https://mcp.tianyancha.com/v1
streamableHttp
```

### 认证
- 方式: Authorization header
- 需要: TIANYANCHA_API_KEY

### 当前状态
**未启用** — 需要 API Key

### 启用步骤
1. 获取天眼查 MCP API Key
2. 在 ~/.workbuddy/.mcp.json 中设置 TIANYANCHA_API_KEY 环境变量
3. 将天眼查 connector 的 disabled 设为 false
4. 重启 WorkBuddy

---

## 启信慧眼 MCP Connector

### 端点
```
https://mcp.qixin.com/mcp
streamableHttp
```

### 认证
- 方式: Authorization: Bearer {QIXIN_API_KEY}
- 需要: QIXIN_API_KEY

### 当前状态
**未启用** — 需要 API Key

### 启用步骤
1. 获取启信慧眼 MCP API Key
2. 在 ~/.workbuddy/.mcp.json 中设置 QIXIN_API_KEY 环境变量
3. 将启信慧眼 connector 的 disabled 设为 false
4. 重启 WorkBuddy

---

## MCP 数据字段映射

| 数据字段 | 企查查 | 天眼查 | 启信慧眼 |
|----------|--------|--------|----------|
| 企业名称 | ✅ | ✅ | ✅ |
| 统一社会信用代码 | ✅ | ✅ | ✅ |
| 法定代表人 | ✅ | ✅ | ✅ |
| 注册资本 | ✅ | ✅ | ✅ |
| 成立日期 | ✅ | ✅ | ✅ |
| 注册地址 | ✅ | ✅ | ✅ |
| 经营范围 | ✅ | ✅ | ✅ |
| 股权结构 | ✅ | ✅ | ✅ |
| 实控人 | ✅ | ✅ | ✅ |
| 诉讼记录 | ✅ | ✅ | ✅ |
| 被执行信息 | ✅ | ✅ | ✅ |
| 失信信息 | ✅ | ✅ | ✅ |
| 行政处罚 | ✅ | ✅ | ✅ |
| 商标 | ✅ | ✅ | ✅ |
| 专利 | ✅ | ✅ | ✅ |
| 软著 | ✅ | ✅ | ✅ |
| 变更记录 | ✅ | ✅ | ✅ |
| 分支机构 | ✅ | ✅ | ✅ |
| 对外投资 | ✅ | ✅ | ✅ |
| 融资历史 | ✅ | ✅ | ✅ |
| 高管信息 | ✅ | ✅ | ✅ |
| 财务数据 | ❌ | ❌ | ❌ |
