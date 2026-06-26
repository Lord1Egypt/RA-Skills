# C21 - 北大法宝

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C21 |
| 连接器名 | pkulaw |
| 显示名 | 北大法宝 |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 企业/商业信息查询 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 法律法规 | 法律法规检索 |
| 司法案例 | 司法案例检索 |
| 法条 | 法条检索 |
| 期刊 | 法学期刊检索 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L3-api-enterprise-C21-pkulaw-search-law.py   # 法律法规检索
└── L3-api-enterprise-C21-pkulaw-search-case.py  # 司法案例检索
```

### 环境变量配置

```bash
export PKULAW_API_KEY="your_api_key"
```

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 迁移 | 重配连接器 | 改 API 地址 |

### 鉴权方式

**API Key**：
1. 在北大法宝开放平台注册账号
2. 获取 API Key
3. 请求时携带 API Key

**环境变量配置**：
```bash
export PKULAW_API_KEY="your_api_key"
```

### 核心脚本示例

使用 connector-hub 技能中的脚本：

```bash
python scripts/L3-api-enterprise-C21-pkulaw-search-law.py [参数]
python scripts/L3-api-enterprise-C21-pkulaw-search-case.py [参数]
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| API 变更 | 改 API 域名即可 |
| 凭证更新 | 重新申请 API Key |
| 工作流 | 无需修改 |
