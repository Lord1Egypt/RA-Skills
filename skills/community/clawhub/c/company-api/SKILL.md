---
name: company-api
description: "陀螺匠公司内部平台接口集成。用于查询日报、项目、财务、客户、合同等公司数据。Token 自动管理，过期自动重新登录。专为使用 陀螺匠 后台的团队设计。"
---

# 陀螺匠 · 公司平台接口

专为 **陀螺匠** 后台用户设计，查询日报、项目、财务、客户、合同等公司运营数据。

## 快速开始

```bash
# 1. 进入技能目录
cd 你的工作目录/skills/company-api

# 2. 运行配置向导（首次使用）
bash scripts/api.sh setup

# 3. 按提示输入你的账号信息即可使用
```

## 前置依赖

- `jq`（JSON处理，`apt install jq`）
- `curl`（系统通常自带）
- `python3`（用于JSON生成）

## 配置说明

首次运行 `setup` 命令，按提示输入：
1. **API地址**（如 `https://你的域名/api`）
2. **开放平台 access_key / secret_key**（从系统后台获取）
3. **登录手机号 + 密码**

配置保存后，所有接口**自动管理 Token**，过期自动重新登录，无需手动维护。

## 文件结构

```
company-api/
├── SKILL.md              # 本文件
├── scripts/
│   └── api.sh            # API 脚本（功能入口）
├── .api-config.json      # 你的配置（自动创建）
└── .token-cache.json     # 登录 Token 缓存（自动管理）
```

## 所有命令

| 命令 | 用法 | 说明 |
|------|------|------|
| `setup` | `scripts/api.sh setup` | **首次配置向导** |
| `auth` | `scripts/api.sh auth` | 刷新开放平台 Token |
| `login` | `scripts/api.sh login` | 账号密码登录（Token过期自动调用） |
| `save-token` | `scripts/api.sh save-token <token>` | 手动保存Token |
| `daily` | `scripts/api.sh daily [页] [条数] [时间]` | 查日报列表 |
| `projects` | `scripts/api.sh projects [页] [条数]` | 查项目列表 |
| `project-info` | `scripts/api.sh project-info <项目id>` | 查看项目详情（含成员、客户） |
| `project-add` | `scripts/api.sh project-add <名称> <客户eid> [合同cid] [负责人uid]` | 创建项目 |
| `task-add` | `scripts/api.sh task-add <项目id> <任务名> [负责人uid]` | 创建项目任务 |
| `bills` | `scripts/api.sh bills [页] [条数]` | 查财务/账单 |
| `customers` | `scripts/api.sh customers [页] [条数]` | 查客户列表 |
| `contracts` | `scripts/api.sh contracts [页] [条数]` | 查合同列表 |
| `contract-form` | `scripts/api.sh contract-form` | 查合同创建页数据（客户ID、分类ID） |
| `products` | `scripts/api.sh products [页] [条数]` | 查产品列表 |
| `product-add` | `scripts/api.sh product-add <名称> [分类] [单位]` | 添加产品 |
| `product-attrs` | `scripts/api.sh product-attrs` | 查产品SKU（含unique ID） |
| `product-cate` | `scripts/api.sh product-cate` | 查产品分类 |
| `status` | `scripts/api.sh status` | 查看 Token 状态 |

## Token 自动管理

接口请求时**先直接请求**，如果返回 Token 过期，自动重新登录获取新 Token 并重试，对使用者完全透明，无需手动维护。

## 数据关系

```
日报（daily）  → 员工每天工作记录
项目（projects）→ 开发任务管理
合同（contracts）→ 客户签约/收款
财务（bills）  → 收支记录
客户（customers）→ 客户信息
产品（products）→ 服务/商品目录
```

## 注意事项

- 配置文件中包含账号密码，请勿分享给他人
- `.api-config.json` 和 `.token-cache.json` 包含敏感信息，建议加入 `.gitignore`
