# 法大大文件签署 - 完整签署生命周期 Skill

基于法大大 FASC API 5.0 的完整签署 Skill，覆盖发起、查询、撤回、下载全生命周期。

## 功能特性

- **一键发起签署** - 只需提供合同文件和签署方信息，即可快速发起签署
- **多签署方支持** - 支持个人签署方和企业签署方
- **模板发起** - 支持使用预先创建的签署模板快速发起
- **已有流程查询** - 查询当前账号下的所有签署任务
- **撤回签署** - 撤回尚未完成的签署任务
- **下载已签合同** - 下载已完成签署的合同文件

## 快速开始

### 1. 安装 Skill

```bash
# Skill 自动安装，无需手动操作
```

### 2. 配置凭证

在环境变量中配置法大大 API 凭证：

```bash
export FADADA_APP_ID="your_app_id"
export FADADA_APP_SECRET="your_app_secret"
export FADADA_OPEN_CORP_ID="your_open_corp_id"  # 可选
export FADADA_ENV="production"  # 或 "uat"（测试环境）
```

### 3. 上传文件并发起签署

```bash
# 进入 skill 目录
cd ~/.workbuddy/skills/fadada-document-sign

# 上传文件
python scripts/upload_file.py --file-path "/path/to/contract.pdf" --file-name "合同.pdf"

# 发起签署
python scripts/initiate_sign.py \
  --task-name "劳动合同签署" \
  --file-ids '["file_id_from_upload"]' \
  --signers '[{"name":"张三","phone":"13800138000","actorType":"person"}]'
```

### 4. 使用模板发起

```bash
# 查询模板列表
python scripts/list_templates.py

# 查询模板详情
python scripts/get_template_detail.py --template-id "template_id"

# 基于模板发起签署
python scripts/initiate_sign.py \
  --task-name "劳动合同签署" \
  --template-id "template_id" \
  --signers '[{"name":"张三","phone":"13800138000","actorType":"person","participantId":"xxx"}]'
```

### 5. 查询签署状态

```bash
python scripts/query_sign_status.py --task-id "task_id"
```

## 目录结构

```
fadada-document-sign/
├── SKILL.md                    # Skill 主文件（AI Agent 触发配置）
├── README.md                   # 使用说明
├── _skillhub_meta.json         # Marketplace 元数据
├── scripts/
│   ├── utils.py                # 公共工具函数
│   ├── upload_file.py          # 上传文件
│   ├── initiate_sign.py        # 发起签署
│   ├── list_templates.py       # 查询模板列表
│   ├── get_template_detail.py  # 查询模板详情
│   ├── list_sign_tasks.py      # 查询已有流程
│   ├── query_sign_status.py    # 查询签署状态
│   ├── cancel_sign_task.py     # 撤回签署任务
│   └── download_signed_contract.py  # 下载已签署合同
├── assets/
│   ├── upload_contract_card.json    # 上传卡片
│   ├── file_select_card.json        # 文件选择卡片
│   ├── signers_data_card.json       # 签署方信息卡片
│   ├── start_result_card.json       # 结果展示卡片
│   ├── template_list_card.json      # 模板列表卡片
│   ├── task_list_card.json          # 任务列表卡片
│   ├── error_card.json              # 错误提示卡片
│   └── screenshots/                # 使用截图（待添加）
└── references/
    └── FASC_API_Reference.md    # API 参考文档
```

## API 凭证获取指引

### 操作流程

正式环境应用上线需完成以下步骤：

| 步骤 | 内容 | 详细说明 |
|:---:|------|---------|
| 1 | 个人注册&认证 | 企业管理员完成个人实名认证 |
| 2 | 企业创建&认证 | 创建企业并完成企业实名认证 |
| 3 | 创建应用并启用 | 创建应用并提交审核启用 |
| 4 | **获取凭证** | **获取 AppID、AppSecret、openCorpId** |
| 5 | 配置正式环境 | 替换为正式环境信息 |

> **详细操作指引**：https://dev.fadada.com/api-guide/YYNLQW2Z2W/9QMQ2MU4FGK3AOXA

---

### 第一步：创建应用并启用

1. **入口路径**：`企业设置` → `集成管理` → `应用集成`
2. **创建应用**：点击【创建应用】，填写应用信息
   - 基础信息：应用名称、应用类型（企业应用/第三方应用）
   - 授权范围设置：建议全选
3. **启用应用**：创建后需【申请上线】并提交审核，审核通过后自动启用

---

### 第二步：获取 AppID 和 AppSecret

**AppID（应用标识）**：法大大平台为每个应用生成唯一的标识，用于 API 接口对接时识别不同的应用系统

**AppSecret（应用秘钥）**：与应用标识组成 `<AppId, AppSecret>` 对，用于接入认证和参数签名。为了保证数据安全，请务必不要泄漏 AppSecret

**获取步骤**：

| 步骤 | 操作 |
|:---:|------|
| 1 | 进入 `企业设置` → `集成管理` → `应用集成`，选择已启用的应用 |
| 2 | 点击 AppSecret 的【查看】按钮 |
| 3 | 获取短信验证码并填写验证 |
| 4 | 验证通过后，点击【复制图标】复制 AppID 和 AppSecret |

---

### 第三步：获取 openCorpId

**openCorpId（接入企业唯一标识）**：在创建应用后系统默认生成，已授权全部权限给到应用

**获取位置**：在应用详情页面可直接查看 openCorpId

---

### 凭证配置

| 环境变量 | 说明 | 来源 |
|---------|------|------|
| FADADA_APP_ID | 应用ID（AppID） | 应用详情页 |
| FADADA_APP_SECRET | 应用密钥（AppSecret） | 应用详情页（需验证） |
| FADADA_OPEN_CORP_ID | 企业ID（openCorpId） | 应用详情页 / 自动获取 |
| FADADA_ENV | 环境 (production/uat) | 默认 production |

### 配置示例

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加：
export FADADA_APP_ID="00004016"
export FADADA_APP_SECRET="JWRUWJYOL0QEISHCZQ20UGIGICBOFT9E"
export FADADA_OPEN_CORP_ID="a814cfeeefdb4a5c92b9e147f02fe99d"  # 可选，系统自动获取
export FADADA_ENV="production"  # 或 "uat"（测试环境）
```

> ⚠️ **注意**：openCorpId 可不配置，系统会自动通过 API 获取应用归属企业的 openCorpId

## 签署方类型

### 个人签署

```json
{
  "name": "张三",
  "phone": "13800138000",
  "actorType": "person"
}
```

### 企业签署

```json
{
  "name": "杭州未来科技有限公司",
  "contactName": "李经理",
  "phone": "13800138000",
  "actorType": "corp"
}
```

**contactName 说明**：
- 企业签署时，经办人信息必须填写
- 经办人将收到签署通知短信

## 常见问题

### Q: 文件上传失败？
A: 请确认：
1. 文件格式为 PDF 或 OFD
2. 文件大小不超过 50MB

### Q: 发起签署失败？
A: 请检查：
1. API 凭证是否配置正确
2. 签署方信息是否完整（姓名 + 联系方式）
3. 企业签署方是否填写了经办人（contactName）

### Q: 如何获取签署链接？
A: 发起签署成功后，返回结果中会包含 signUrls 列表，每个签署方对应一个签署链接。

### Q: 如何查询签署状态？
A: 使用 `query_sign_status.py` 脚本：
```bash
python scripts/query_sign_status.py --task-id "task_id"
```

### Q: 部分 API 返回 404 错误？
A: 以下接口可能因账户权限或 API 版本不同而不可用：
- `/sign-task/app/query-list` - 批量查询任务列表
- `/sign-task/app/cancel` - 撤回签署任务
- `/sign-task/app/get-download-url` - 获取合同下载链接

如遇 404 错误，请确认账户是否具备相应权限。

## 版本历史

- **v1.0.0** (2026-05-18)
  - 初始版本发布
  - 支持上传合同文件并发起个人/企业签署
  - 支持基于模板发起签署
  - 支持查询签署模板列表和详情
  - 支持查询已有签署流程
  - 支持查询签署任务状态
  - 支持撤回未完成签署任务
  - 支持下载已签署合同

## License

MIT License
