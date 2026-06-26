# C06 - 金山文档

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C06 |
| 连接器名 | kdocs |
| 显示名 | 金山文档 |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 文档/知识库 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 创建文档 | Word/Excel/PPT |
| 编辑文档 | 内容读写 |
| 分享文档 | 权限管理 |
| 导出文档 | 下载为文件 |
| 协作编辑 | 多人实时协作 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
└── L2-auth-docs-kb-C06-kdocs-create-doc.py  # 创建文档
```

### 鉴权方式

**OAuth2**：
1. 在金山文档开放平台创建应用
2. 获取 `app_id` + `app_secret`
3. 用户授权获取 `access_token`
4. Token 有效期 2 小时

**环境变量配置**：
```bash
export KDOCS_APP_ID="your_app_id"
export KDOCS_APP_SECRET="your_app_secret"
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| API 变更 | 改 API 域名即可 |
| 凭证更新 | 重新申请应用凭证 |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 迁移 | 重配连接器 | 改 API 地址 |

### 核心脚本示例

使用 connector-hub 技能中的脚本：

```bash
python scripts/L2-auth-docs-kb-C06-kdocs-create-doc.py [参数]
```
