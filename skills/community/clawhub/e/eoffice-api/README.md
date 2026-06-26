# eoffice-skill

泛微 e-office 协同办公系统的 OpenClaw Skill。

让 AI Agent 能够通过自然语言操作 OA 系统，包括用户管理、部门管理、审批流程等。

## 功能特性

- **用户管理** - 查询、新建、编辑、删除用户
- **部门管理** - 部门树形结构、CRUD 操作
- **建模数据** - 自定义建模的数据操作
- **附件管理** - 文件上传下载

## 安装

### 前置要求

- OpenClaw / Clawdbot 已安装
- Python 3.7+ (用于 token 获取脚本)
- requests 库: `pip install requests`

### 安装步骤

1. **通过 ClawHub 安装**（推荐）

```bash
openclaw skill install eoffice-api
```

2. **手动安装**

```bash
# 克隆或下载此仓库
git clone https://github.com/yourname/eoffice-skill.git

# 进入目录
cd eoffice-skill

# 链接到 OpenClaw
openclaw skill link ./eoffice-skill
```

## 配置

安装后，需要配置 OA 系统的连接信息：

### 1. 获取 OA OpenAPI 凭证

1. 登录 OA 系统管理后台
2. 进入「开放平台」→「应用管理」
3. 选择「测试环境」或「正式环境」Tab
4. 点击「新建应用」，填写应用信息：
   - **应用名称**：给应用起个名字
   - **用户身份字段**：选择用什么字段识别用户（账号/工号/手机号）
   - **授权人员**：哪些 OA 用户可以使用此应用（白名单）
5. 创建完成后，在应用列表点击「查看」获取：
   - **Agent ID**
   - **Secret**

详细步骤请参考：[OA 开放平台应用管理说明](https://service.e-office.cn/knowledge/detail/49/ke7d0a3)

> 注意：如果选择「测试环境」，则 `EOFFICE_BASE_URL` 应指向测试环境地址

### 2. 配置环境变量

在 OpenClaw 的 `openclaw.json` 或 `.env` 中配置：

```json
{
  "skills": {
    "entries": {
      "eoffice-api": {
        "env": {
          "EOFFICE_BASE_URL": "https://oa.yourcompany.com/server",
          "EOFFICE_AGENT_ID": "100001",
          "EOFFICE_SECRET": "your-secret-key-here",
          "EOFFICE_USER": "your-account"
        }
      }
    }
  }
}
```

### 环境变量说明

| 变量 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `EOFFICE_BASE_URL` | 是 | OA 系统部署地址 | `https://oa.example.com/server` |
| `EOFFICE_AGENT_ID` | 是 | 应用 Agent ID | `100001` |
| `EOFFICE_SECRET` | 是 | 应用密钥 | `abc123...` |
| `EOFFICE_USER` | 是 | 用户标识（必须与应用配置中的「用户身份字段」匹配） | `admin` 或 `18612345678` |

> **用户身份字段**：在 OA 应用管理中可配置为 `user_accounts`（账号）、`user_job_number`（工号）或 `phone_number`（手机号），`EOFFICE_USER` 的值必须与此处配置的类型一致。

## 使用示例

### 查询用户

```
用户: 查找所有姓张的研发部员工

Agent: 我来帮你查询姓张的研发部员工...

curl -X POST "https://oa.example.com/server/api/hrm/lists" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"search": {"user_name": ["张", "like"]}}'

找到 3 名员工：
1. 张三 - 研发部 - 高级工程师
2. 张四 - 研发部 - 技术专家
3. 张五 - 研发部 - 初级工程师
```

### 新建用户

```
用户: 帮我新建一个用户，用户名 zhangsan，姓名张三，部门研发部

Agent: 好的，我来为你创建用户...

POST /api/hrm/add
{
  "user_accounts": "zhangsan",
  "user_name": "张三",
  "dept_id": 20,
  "role_id": [1],
  "user_status": 1,
  "allow_login": 1,
  "wap_allow": 1,
  "sex": 1
}

用户创建成功！
user_id: WV00000693
```

### 查询部门

```
用户: 显示公司部门结构

Agent: 以下是公司部门组织架构：

总公司
├── 技术部
│   ├── 研发组
│   └── 测试组
├── 市场部
│   ├── 销售组
│   └── 推广组
└── 行政部
```

## 文件结构

```
eoffice-skill/
├── SKILL.md                    # Skill 主文件
├── README.md                   # 本文件
├── references/
│   └── api.md                 # 完整 API 文档
└── scripts/
    └── get-token.py           # Token 获取脚本
```

## 开发

### 本地测试

```bash
# 设置环境变量
export EOFFICE_BASE_URL="https://oa.example.com/server"
export EOFFICE_AGENT_ID="100001"
export EOFFICE_SECRET="your-secret"
export EOFFICE_USER="admin"

# 测试 token 获取
python scripts/get-token.py
```

### 发布更新

```bash
# 1. 更新版本号（修改 SKILL.md 中的 version）
# 2. 提交并推送到 GitHub
git add .
git commit -m "v1.1.0: 新增 xxx 功能"
git push

# 3. 在 ClawHub 上发布新版本
```

## API 文档

详细接口说明请查看 [references/api.md](references/api.md)。

## 许可证

MIT License

## 支持

- 提交 Issue: https://github.com/yourname/eoffice-skill/issues
- 文档: https://docs.openclaw.ai/tools/skills
