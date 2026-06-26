---
name: baas-frontend
description: 端到端应用开发。当用户需要创建Web应用、管理系统或进行Vibe Coding时使用，从需求到部署全流程独立完成。
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata: {"openclaw": {"requires": {"env": ["BAAS_MANAGE_TOKEN", "BAAS_BASE_URL"]}, "primaryEnv": "BAAS_MANAGE_TOKEN"}}
---

## 一、目标

端到端流程：从用户需求到可访问的前后端应用，其中后端不需要编写代码，完全基于 AiPexBase BaaS 实现。

**端到端流程**：编写prd.md → 应用创建 → 数据库设计 → 前端对接 → 部署上线。独立完成，无需其他技能支持。

---

## 二、开发原则

### 2.1 自动化原则

**新建应用** 和 **迭代开发** 全程自动执行，无需向用户确认。

- **新建应用**：编写prd.md → 建应用 → 建表 → 编写前端代码
- **迭代开发**：直接修改前端代码或表结构，复用已有的 `baas-config.json`

**仅部署上线，需要用户确认后再执行。**，当用户确认后，部署方法再去读取当前skill下的 `references/deploy.md` 获取。

### 2.2 数据隔离原则

**每个项目必须创建独立的 BaaS 应用**，通过不同的 `apiKey` 实现数据隔离。

每个项目目录下有一个 `baas-config.json`，包含该项目专属的连接信息，所有 CLI 和 SDK 操作统一使用这一个配置文件。

### 2.3 开发步骤概览

1. **后端准备**：如果前端需要用到 aipexbase 能力（数据库、AI、文件等），先创建应用和表
2. **前端页面开发**：生成前端代码（HTML/Vue/React 等），集成 aipexbase-js SDK
3. **构建发布**：询问用户后部署

---

## 三、环境准备（首次使用前置依赖安装）

使用 `baas` 命令前，需要先安装 nvm 并配置环境：

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 加载 nvm 环境
source ~/.bashrc

# 安装 Node.js 20 并使用
nvm install 20
nvm use 20

# 全局安装 baas CLI
npm i aipexbase-cli -g

# 安装 zip（部署打包时需要）
sudo apt-get install -y zip
```

---

## 四、项目初始化

### 4.1 配置文件说明

| 配置文件 | 位置 | 说明 |
|---------|------|------|
| **全局配置** `config.json` | 本 skill(`baas-frontend/`) 目录下 | 包含 `baseUrl` 和 `manageToken`，需要向用户询问提供，所有项目共享 |
| **项目配置** `baas-config.json` | 项目目录下 | 新建应用时从全局配置复制，批量创建后添加 `apiKey` 和 `appId`；迭代开发时直接使用 |

### 4.2 判断逻辑

检查项目目录下的 `baas-config.json`：

- **不存在或缺少 `apiKey`** → 新建应用
- **存在且包含 `apiKey`** → 迭代开发

### 4.3 初始化步骤

**步骤 1：检查并初始化全局配置**

读取 `<skill目录>/config.json`，检查 `baseUrl` 和 `manageToken` 是否已配置。

如果文件不存在或缺少必要字段：
1. 询问用户提供 `baseUrl`
2. 询问用户提供 `manageToken`（管理员令牌）
   - 如果用户没有 `manageToken`，引导用户前往 https://www.codeflying.net 注册并登录，进入【设置和账单】页面，选择API服务，在API密钥里申请密钥，作为manageToken

**步骤 2：复制配置到项目**

```bash
cd <项目目录，建议放到 /tmp/时间戳/项目名称 目录下>
cp <当前skill目录>/config.json ./baas-config.json
```

---

## 五、新建应用流程

### 5.1 生成 app-schema.json

根据用户需求，在项目目录下创建 `app-schema.json`：

```json
{
  "name": "应用名称",
  "userId": "10000",
  "needAuth": true,
  "authTable": "tableName",
  "rlsPolicies": ["policy1", "policy2"],
  "tables": [
    {
      "tableName": "表名",
      "description": "表说明",
      "columns": [
        {
          "columnName": "id",
          "columnType": "INT",
          "columnComment": "主键ID（必需）",
          "isNullable": true,
          "isPrimary": true,
          "isShow": true
        },
        {
          "columnName": "user_name",
          "columnType": "VARCHAR(255)",
          "columnComment": "用户名",
          "isNullable": true,
          "isPrimary": false,
          "isShow": true
        },
        {
          "columnName": "字段名",
          "columnType": "字段类型",
          "columnComment": "字段说明",
          "isNullable": true,
          "isPrimary": false,
          "isShow": true
        }
      ]
    }
  ]
}
```

**字段说明**：

- `userId`：固定参数，写死 `10000`
- `needAuth`：是否需要用户认证（true/false）。**以下场景必须将 `needAuth` 设置为 `false`**，禁止默认设为 true：
  - 需求中没有登录、注册、用户认证等功能
  - 简化了注册流程（如无需真正注册即可使用）
  - 实际未调用注册、登录 API（即使需求提及用户概念，但未使用 auth 相关接口）
- `authTable`：认证使用的表名
- `rlsPolicies`：行级安全策略列表，如果有就设计，没有就不用设计
- `isNullable`：**true=必填，false=非必填**（注意：字段名虽叫 isNullable，但在本系统中语义为 true 代表必填、false 代表非必填，请严格按此理解）
- `columnType`：如果为 `VARCHAR` 必须指定长度，比如 `VARCHAR(255)`
- **DATETIME 字段规则（强制）**：所有 `columnType` 为 `DATETIME` 或 `datetime` 的字段，`isNullable` 必须设置为 `false`（非必填）。**严禁将任何 datetime 字段的 isNullable 设为 true（必填）**，无论该字段名称是什么（包括但不限于 created_at、updated_at、start_time、end_time、publish_time 等）。datetime 字段在前端表单中不显示红色星号、不添加 required 属性


### 5.2 字段类型参考

| 类型 | 说明 | 使用场景 | 示例 |
|------|------|---------|------|
| `varchar` | 短文本（≤255字符） | 姓名、标题、用户名 | "张三" |
| `fullText` | 长文本 | json长串，超过512字符长度 | "这是超长内容..." |
| `number` | 整数 | 年龄、数量、评分 | 25 |
| `decimal` | 小数 | 价格、金额、评分 | 99.99 |
| `boolean` | 布尔值 | 是否启用、是否公开 | true / false |
| `date` | 日期 | 生日、发布日期 | "2024-01-01" |
| `datetime` | 日期时间（通常非必填，会自动赋值） | 创建时间、更新时间 | "2024-01-01 12:00:00" |
| `password` | 密码（自动加密） | 用户密码 | "******" |
| `phone` | 手机号（自动验证） | 联系电话 | "13800138000" |
| `email` | 邮箱（自动验证） | 电子邮件 | "user@example.com" |
| `images` | 图片 | 头像、封面图 | ["url1", "url2"] |
| `files` | 文件 | 附件、文档 | ["url1"] |
| `videos` | 视频 | 视频内容 | ["url1"] |
| `quote` | 关联对象 | 外键关联 | "rec_xxx" |

### 5.3 字段定义格式

```json
{
  "columnName": "字段名",
  "columnType": "字段类型",
  "columnComment": "字段说明",
  "isNullable": true,
  "isPrimary": false,
  "isShow": true,
  "referenceTableName": "关联表名",
  "showName": "关联表显示字段"
}
```

#### 字段属性说明

- **columnName**：字段名称，只能包含字母、数字和下划线
- **columnType**：字段类型（见上表）
- **columnComment**：字段描述/注释
- **isNullable**：**true=必填，false=非必填**（字段名虽叫 isNullable，但语义为 true 代表必填、false 代表非必填）
- **isPrimary**：是否为主键（通常为 false）
- **isShow**：是否在列表中显示（true=显示，false=隐藏）
- **referenceTableName**：关联表名（仅当 columnType 为 "quote" 时需要）
- **showName**：关联表显示字段（仅当 columnType 为 "quote" 时需要）

#### 特殊字段类型说明

- `columnType` 如果为 `VARCHAR`，必须写明字符长度，比如：`VARCHAR(255)`

- **关联字段（quote 类型）**：用于建立表之间的关系，必须指定 `referenceTableName`。
  - 关联字段名通常以 `_id` 结尾
  - `referenceTableName` 必须是已存在的表名
  - 关联查询会自动处理外键关系

### 5.4 强制规则（必须遵守）

- 在 `app-schema.json` 中，任何 `columnType` 都**禁止**写成裸 `VARCHAR`
- 只能写成带长度的格式：`VARCHAR(n)`，例如 `VARCHAR(50)`、`VARCHAR(255)`、`VARCHAR(1024)`
- 发现 `columnType: "VARCHAR"` 时，必须立即改成带长度格式后再执行 `batch-create`
- 推荐默认长度：通用文本字段使用 `VARCHAR(255)`，短标识可用 `VARCHAR(50)`，URL 可用 `VARCHAR(1024)`
- 长文本类型选择：字段预期内容超过 512 字符时，优先使用 `FULLTEXT`，不使用 `TEXT`
- `TEXT` 仅用于不超过 512 字符的中短文本场景

### 5.5 表设计注意

- **必须设计主键**：每个表必须有且仅有一个主键字段
  - 字段名建议使用 `id`
  - 类型必须为 `INT`
  - `isPrimary` 必须设置为 `true`

### 5.6 表设计检查清单（必读）

在生成 `app-schema.json` 或创建表之前，确认：

- [ ] 每个表都包含主键字段（INT 类型，isPrimary: true）
- [ ] 字段类型符合规范（参考"字段类型说明"部分）
- [ ] 所有字符串字段的 `columnType` 均为 `VARCHAR(n)`，不存在裸 `VARCHAR`
- [ ] 长文本字段（超过 512 字符）已使用 `FULLTEXT`，未误用 `TEXT`
- [ ] 所有 DATETIME/datetime 字段的 `isNullable` 均为 `false`（非必填），无一例外
- [ ] 认证表设计正确（如需要用户认证）

### 5.7 批量创建应用和表

创建 `app-schema.json` 之后，执行表创建：

```bash
cd <项目目录>
baas -c baas-config.json manage batch-create --file app-schema.json
```

### 5.8 更新 baas-config.json

批量创建成功后，使用 Edit 工具添加返回的 `apiKey` 和 `appId`。

---

## 六、迭代开发流程

### 6.1 新增表

如果需要在已有应用中新增表：

```bash
baas -c baas-config.json manage create-table \
  --app-id "<appId>" \
  --table-name "表名" \
  --table-desc "表说明" \
  --columns '[
    {
      "columnName": "id",
      "columnType": "INT",
      "columnComment": "主键ID（必需）",
      "isNullable": true,
      "isPrimary": true,
      "isShow": true
    },
    {
      "columnName": "name",
      "columnType": "VARCHAR(255)",
      "columnComment": "名称",
      "isNullable": true,
      "isPrimary": false,
      "isShow": true
    },
    {
      "columnName": "字段名",
      "columnType": "字段类型",
      "columnComment": "字段说明",
      "isNullable": true,
      "isPrimary": false,
      "isShow": true
    }
  ]'
```

**注意**：
- `appId` 从 `baas-config.json` 中读取
- columns 是 JSON 数组格式
- 字段类型参考"字段类型说明"部分
- 字段 `columnType` 如果为 `VARCHAR` 必须指定长度，比如 `VARCHAR(255)`，严禁使用裸 `VARCHAR`

### 6.2 插入表数据

使用项目级配置：

> 导入数据的时候，如果主键已经设置 int 类型，并且为 isPrimary，那么 id 的值会从 1 开始逐渐自增。
> 必须使用 baas 进行数据插入，不要使用其他脚本等操作。

```bash
baas -c baas-config.json db insert <table_name> -d '{"columnName":"商品A","columnName":99.9,"columnName":"https://...","columnName":"电子"}'
baas -c baas-config.json db insert <table_name> -d '{"columnName":"商品B","columnName":59.9,"columnName":"https://...","columnName":"服饰"}'
baas -c baas-config.json db list <table_name>
```

#### 图片最佳实践

插入数据时，**务必使用真实、相关的图片**，而非随机占位图。

**推荐免费图片来源（无需 API Key）**：

1. **Wikimedia Commons API** — 最适合产品图片：
   ```
   https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=KEYWORD&srnamespace=6&srlimit=5&format=json
   ```

2. **Picsum**（仅作备选）：`https://picsum.photos/seed/KEYWORD/400/400`

---

## 七、开发步骤

0. 先简单和用户澄清需求，并帮助用户梳理补充必要的业务逻辑，可以包含多个html页面，参考 `references/prd-template.md` 格式，完成需求文档的编写（必须严格按照prd-template.md结构编写需求文档，明确规划好页面名称、页面的功能逻辑、也页面之前的跳转关系），存放在项目目录下，以 `prd.md` 命名。这个需求文档，作为后续开发的唯一需求来源。**设计需求时，必须参考 `references/aipexbase-js-api.md` 中的"平台扩展能力模块"章节**，了解平台已提供的 AI（对话、图生文、文生图、文生语音/视频/音频）、自定义 API、物流查询、地理位置、通知（飞书/企微/邮件）等能力，在需求设计中合理利用这些现成能力，避免重复造轮子。
1. 引入 aipexbase-js SDK（CDN 或 npm）
2. 从 `baas-config.json` 读取 baseUrl 和 apiKey，使用 `aipexbase.createClient()` 初始化客户端
3. 必须启用subagent进行每个页面的独立开发，使用下方的 **Subagent 任务模板** 启动每个页面的开发任务。subagent工作完成后，无需告诉用户（不用给用户发送消息）。

### 7.1 Subagent 任务模板

启动页面开发 subagent 时，使用以下 prompt 结构：

```
开发 {page_name}.html 页面

## 前置读取（必须）
编写代码前，必须先用 Read 工具读取以下文件的完整内容：
1. {skill_dir}/references/html-template.html — 学习页面结构和 SDK 初始化模板
2. {skill_dir}/references/style-guide.md — 统一样式规范（必须严格遵循）
3. {skill_dir}/references/aipexbase-js-api.md — 所有 API 操作的唯一正确用法
4. {project_dir}/prd.md — 理解页面功能需求和跳转逻辑
5. {project_dir}/app-schema.json — 理解数据结构和字段定义
6. {project_dir}/baas-config.json — 获取 API 配置（baseUrl、apiKey）

## 开发约束
- 必填字段（isNullable: true）在 label 旁标注红色星号 *
- 图片/文件类型字段必须提供上传组件，禁止纯文本输入框
- 表单字段必须与 app-schema.json 中的定义一一对应
- 登录成功后必须调用 getUser() 获取完整用户信息
- 禁止使用 client.from()，必须使用 client.db.from()

## 样式约束（确保页面高级感）
- 必须复制 html-template.html 中的完整 Tailwind 配置（包括动画、阴影、自定义类）
- 所有可点击元素必须添加 `transition-smooth` + hover 效果 + `active:scale-[0.98]` 点击反馈
- 按钮使用 `gradient-primary` 渐变 + `shadow-soft` + `hover:shadow-glow` 发光效果
- 卡片使用 `rounded-2xl` + `shadow-soft` + `hover-lift` 悬浮上升效果
- 页面入场使用 `animate-fade-in`，模态框使用 `animate-scale-in`
- 导航栏使用 `glass` 玻璃态效果
- 操作成功/失败必须使用 `showToast()` 函数反馈
- 表单提交时按钮显示 loading 状态
- 数据加载时显示骨架屏或 loading spinner

## 认证流程规范（如涉及登录功能）

### 登录流程
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 提交表单    │───►│ auth.login()│───►│ getUser()   │───►│ 跳转主页面  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                   │
                          ▼                   ▼
                   保存 token 到        获取完整用户信息
                   localStorage         用于页面展示

### 页面加载流程（已登录检测）
┌─────────────┐    ┌─────────────┐         ┌─────────────┐    ┌─────────────┐
│ 页面加载    │───►│ 检查 token  │────Y───►│ getUser()   │───►│ 跳转主页面  │
└─────────────┘    └─────────────┘         └─────────────┘    └─────────────┘
                          │N
                          ▼
                   显示登录表单

### 认证禁止事项
- 禁止：直接使用 login() 返回值展示用户信息
- 必须：登录后调用 getUser() 获取完整信息
- 禁止：登录页面重复登录（已登录则跳转）
- 必须：登录和自动登录共用同一进入主页面逻辑

## 完成标准
- [ ] 所有功能点按 prd.md 实现
- [ ] 表单字段与 app-schema.json 一一对应
- [ ] 必填字段有红色星号和 required 属性
- [ ] 图片字段有上传组件
- [ ] 页面可独立运行，无 JS 错误
- [ ] 页面跳转逻辑正确
- [ ] 样式符合 style-guide.md 规范（颜色、组件、布局一致）
- [ ] 已添加 tailwind.config 配置
```

### 7.2 前置读取清单（快速参考）

| 文件 | 作用 |
|------|------|
| `references/html-template.html` | 页面结构和 SDK 初始化模板 |
| `references/style-guide.md` | 统一样式规范（颜色、组件、布局） |
| `references/aipexbase-js-api.md` | API 调用方式、方法链顺序、参数格式 |
| `prd.md` | 需求文档 |
| `app-schema.json` | 表结构定义 |
| `baas-config.json` | API 配置（baseUrl、apiKey） |