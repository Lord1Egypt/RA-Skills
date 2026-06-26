# C18 - 微云

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C18 |
| 连接器名 | tencent-weiyun |
| 显示名 | 微云 |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 存储 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 文件上传 | 上传文件到微云 |
| 文件下载 | 从微云下载文件 |
| 文件管理 | 创建/删除/移动文件夹 |
| 文件列表 | 列出目录内容 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
└── L2-auth-storage-C18-tencent-weiyun-list-files.py  # 列出文件
```

### 环境变量配置

```bash
export TENCENT_WEIYUN_CLIENT_ID="your_client_id"
export TENCENT_WEIYUN_CLIENT_SECRET="your_client_secret"
```

### 鉴权方式

**API Key / SMTP**：
1. 在平台开放平台注册账号
2. 获取 API Key 或 SMTP 授权码
3. 请求时携带凭证

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
