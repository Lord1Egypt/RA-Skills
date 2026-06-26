---
name: byteplan-api
description: BytePlan 数据平台 API 封装。提供登录认证、模型查询、数据获取等接口。可被其他 skill（如 byteplan-ppt、byteplan-word、byteplan-video）依赖使用。
---

# BytePlan API Skill

## 概述

提供 BytePlan 数据平台的 JavaScript API 封装，支持：
- 登录认证（支持 dev/uat 环境）
- 用户与租户管理
- 模型查询与数据获取
- 字段类型值获取（DIM/LIST/LOV/LEVEL）

## 依赖此 Skill 的其他 Skill

- [byteplan-ppt](../byteplan-ppt/SKILL.md) - 数据分析 PPT 报告生成
- [byteplan-word](../byteplan-word/SKILL.md) - 数据分析 Word 文档报告生成
- [byteplan-video](../byteplan-video/SKILL.md) - 数据可视化视频生成

## 环境配置

### 支持的环境

| 环境值 | API 地址 | 说明 |
|-------|---------|------|
| `dev` | https://dev.byteplan.com | 开发环境（密码明文传输） |
| `uat` | https://uatapp.byteplan.com | UAT 环境（密码 RSA 加密） |

### 环境选择

**重要**：首先询问用户选择登录环境：

```json
{
  "questions": [
    {
      "header": "登录环境",
      "question": "请选择 BytePlan 登录环境",
      "options": [
        { "label": "开发环境 (dev)", "description": "https://dev.byteplan.com，密码明文传输" },
        { "label": "UAT 环境 (uat)", "description": "https://uatapp.byteplan.com，密码加密传输" }
      ],
      "multiSelect": false
    }
  ]
}
```

### 环境配置文件位置

**凭证存储路径**：`~/.byteplan/.env`（用户主目录下的 byteplan 文件夹）

登录成功后，系统会自动在此目录下创建 `.env` 文件，存储账号密码和 token 信息：

```env
BP_ENV=dev                          # dev: 开发环境, uat: UAT环境
BP_USER=你的手机号
BP_PASSWORD="你的密码"
# 以下字段由系统自动管理（登录成功后自动写入）
ACCESS_TOKEN=                        # 访问令牌
REFRESH_TOKEN=                       # 刷新令牌
TOKEN_EXPIRES_IN=                    # 过期时间戳
```

**目录结构**：
```
~/.byteplan/
├── .env              # 凭证和 token（全局共享）
└── workspaces/       # 各分析主题的工作目录（可选）
    ├── 计算机资产折旧_20260331_224600/
    │   ├── analysisPlan.json
    │   └── analysis_report.md
    └── 库存周转分析_20260401_103000/
    │   ├── analysisPlan.json
    │   └── analysis_report.md
    └ ...
```

**注意**：
- 如果密码包含 `#` 等特殊字符，请用引号包裹以防止截断
- `.env` 文件中的 `BP_ENV` 可指定环境，优先使用用户选择的环境
- `ACCESS_TOKEN`、`REFRESH_TOKEN`、`TOKEN_EXPIRES_IN` 由系统自动管理，**请勿手动修改**
- 凭证文件统一存储在 `~/.byteplan/.env`，不同分析主题共享同一账号信息

### UAT 环境注意事项

1. 登录前会自动获取公钥并对密码进行 RSA 加密
2. 公钥 API 返回格式为 `{ id, key }`，脚本已兼容处理
3. 登录表单必须包含 `publicKeyId` 字段
4. 如遇到 `DECODER routines::unsupported` 错误，说明公钥格式化有问题

### 首次使用流程

如果用户没有 `.env` 文件或文件中缺少账号密码，**必须询问用户输入**：

1. 询问用户名（手机号）
2. 询问密码
3. 使用输入的凭证进行登录
4. 登录成功后，可选择将凭证保存到 `.env` 文件

## API 参考

### 导入方式

```javascript
// 从 byteplan-api skill 导入
import { login, loginWithEnv, getUserInfo, setEnvironment } from '/Users/fudebao/.claude/skills/byteplan-api/scripts/api.js';
```

### 环境管理

| 函数 | 描述 |
|------|------|
| `setEnvironment(env)` | 设置登录环境（'dev' 或 'uat'） |
| `getEnvironment()` | 获取当前环境 |
| `getBaseUrl()` | 获取当前环境的基础 URL |

### 登录认证

| 函数 | 描述 |
|------|------|
| `login(username, password, env?)` | 使用凭证登录（自动处理 RSA 加密，**自动保存 token**） |
| `loginWithEnv()` | 使用 `.env` 凭证登录（自动使用缓存 token，**自动续期**） |
| `loginWithEnv(env, forceReLogin)` | 强制重新登录 |
| `getToken()` | 从 `.env` 获取 token |

```javascript
// 方式 1：自动使用缓存 token（推荐）
// 首次登录会保存 token，后续调用自动复用
import { loginWithEnv } from './api.js';
const result = await loginWithEnv();
const token = result.access_token;
if (result._cached) {
  console.log('使用缓存的 token'); // 无需重新登录
}

// 方式 2：强制重新登录
const result = await loginWithEnv('dev', true); // forceReLogin = true

// 方式 3：手动传入凭证（也会自动保存 token）
import { login } from './api.js';
const result = await login('手机号', '密码', 'dev');
const token = result.access_token;
```

### Token 持久化

登录成功后，系统会自动将以下信息保存到 `~/.byteplan/.env` 文件：

| 字段 | 说明 |
|------|------|
| `ACCESS_TOKEN` | 访问令牌 |
| `REFRESH_TOKEN` | 刷新令牌 |
| `TOKEN_EXPIRES_IN` | 过期时间戳（毫秒） |

**自动续期机制**：
- `loginWithEnv()` 会自动检查 token 是否过期
- 如果 token 有效（未过期或距离过期超过 5 分钟），直接使用缓存
- 如果 token 过期，自动使用保存的账号密码重新登录

**持久化流程**：
```
1. 用户输入账号密码 → login()
2. 登录成功 → 自动创建 ~/.byteplan/ 目录
3. 自动保存 ACCESS_TOKEN, REFRESH_TOKEN, TOKEN_EXPIRES_IN 到 ~/.byteplan/.env
4. 后续调用 → loginWithEnv() 自动使用缓存 token
5. token 过期 → 自动重新登录并更新 ~/.byteplan/.env
```

### 用户与租户

| 函数 | 描述 |
|------|------|
| `getUserInfo(token)` | 获取用户和租户信息，返回 `{ user: {...}, tenantList: [...] }` |
| `switchTenant(token, tenantId)` | 切换租户上下文 |

```javascript
// 获取用户信息和可用租户列表
const userInfo = await getUserInfo(token);
// userInfo.user = { name, userName, tenantName, ... }
// userInfo.tenantList = [{ tenantId, tenantName }, ...]

// 如需切换到特定租户
await switchTenant(token, tenantId);
```

### 模型查询

| 函数 | 描述 |
|------|------|
| `queryModels(token, options?)` | 列出可用模型 |
| `getModelColumns(token, modelCodes)` | 获取模型字段定义 |
| `getModelData(token, modelCode, params)` | 查询模型数据 |

#### 返回值格式说明（重要）

**⚠️ 所有 API 函数直接返回后端响应，无需额外处理：**

| 函数 | 返回值类型 | 说明 |
|------|-----------|------|
| `queryModels()` | `Array` | **直接返回数组**，可用 `models.map()` 遍历 |
| `getModelColumns()` | `Object` | 返回 `{ data: [...], ... }` 结构 |
| `getModelData()` | `Object` | 返回 `{ data: [...], total: number }` 结构，用 `.data` 取数据 |

```javascript
// ❌ 错误用法：queryModels 返回的是数组，不要加 .data
const models = await queryModels(token);
const list = models.data;  // 错误！models 本身就是数组

// ✅ 正确用法：直接遍历
const models = await queryModels(token);
const modelList = models.map(m => ({ name: m.modelName, code: m.modelCode }));
// models.length = 模型总数

// ✅ getModelData 返回的是对象，需要用 .data 取数据数组
const result = await getModelData(token, 'model_code');
const items = result.data;      // 数据数组
const total = result.total;     // 总记录数

// ✅ getModelColumns 返回的是对象
const columns = await getModelColumns(token, ['model_code_1']);
// columns.data = 字段定义数组
```

### 字段类型值获取

| 函数 | 描述 |
|------|------|
| `getDimValues(token, dimCode, options?)` | 获取 DIM 字段可选值 |
| `getListValues(token, listCode, options?)` | 获取 LIST 字段可选值 |
| `getLovValues(token, lovCode, options?)` | 获取 LOV 字段可选值 |
| `getLevelValues(token, levelCode, options?)` | 获取 LEVEL 字段可选值 |

```javascript
// 获取维度值
const dimValues = await getDimValues(token, 'dim_code', {
  modelCode: 'model_code',
  colName: 'field_name',
  page: 0,
  size: 100
});

// 获取列表值
const listValues = await getListValues(token, 'list_code', {
  modelCode: 'model_code',
  colName: 'field_name'
});

// 获取 LOV 值
const lovValues = await getLovValues(token, 'lov_code', {
  keywords: '搜索关键词'
});

// 获取层级值
const levelValues = await getLevelValues(token, 'level_code', {
  modelCode: 'model_code',
  colName: 'field_name'
});
```

## 查询语法

### 条件结构

```javascript
{
  type: 'condition',
  field: '字段名',
  operator: '=',  // 支持: =, !=, >, <, >=, <=, LIKE, IN, BETWEEN
  value: '值'
}
```

### 条件组结构（多条件）

```javascript
{
  type: 'group',
  logic: 'AND',  // AND 或 OR
  children: [
    { type: 'condition', field: '字段1', operator: '=', value: '值1' },
    { type: 'condition', field: '字段2', operator: '>', value: '值2' }
  ]
}
```

### 特殊字段类型

对于 DIM、LIST、LOV、LEVEL 类型字段：
- 直接使用原字段名（不需要拼接 `.code` 或 `.name`）
- 使用编码值进行筛选

```javascript
// 示例：按性别筛选（DIM 类型）
{ field: 'sex', operator: '=', value: '1' }  // '1' = 男性编码

// 示例：按学科筛选（LIST 类型）
{ field: 'subject', operator: '=', value: 'math' }
```

### 聚合查询

```javascript
const result = await getModelData(token, 'model_code', {
  groupFields: ['category'],
  functions: [
    { func: 'sum', field: 'amount', alias: 'total_amount' },
    { func: 'avg', field: 'price', alias: 'avg_price' }
  ]
});
```

## 完整登录示例

```javascript
import { login, loginWithEnv, getUserInfo } from './api.js';
import { existsSync } from 'fs';
import { homedir } from 'os';
import path from 'path';

// 凭证文件路径
const BYTEPLAN_DIR = path.join(homedir(), '.byteplan');
const ENV_FILE = path.join(BYTEPLAN_DIR, '.env');

// 用户选择的环境
let selectedEnv = 'dev';

// 尝试使用 ~/.byteplan/.env 凭证登录
let token;
if (existsSync(ENV_FILE)) {
  try {
    const result = await loginWithEnv();
    token = result.access_token;
  } catch (e) {
    // 凭证无效，需要询问用户
  }
}

// 如果没有 token，询问用户输入账号密码
if (!token) {
  // 使用 AskUserQuestion 询问用户名和密码
  // const username = ...;
  // const password = ...;
  const result = await login(username, password, selectedEnv);
  token = result.access_token;
}

// ✅ 显示当前租户信息
const userInfo = await getUserInfo(token);
const currentTenant = userInfo.user?.tenantName || '未知租户';
const userName = userInfo.user?.name || userInfo.user?.userName || '未知用户';

`✅ 登录成功！
   环境: ${selectedEnv === 'dev' ? '开发环境' : 'UAT 环境'}
   用户: ${userName}
   当前租户: ${currentTenant}`;
```

## 注意事项

- **首次使用时**：如果没有 `~/.byteplan/.env` 文件或 token 无效，必须询问用户输入账号密码
- **登录成功后**：必须调用 `getUserInfo` 获取并显示当前租户信息，让用户知道在哪个租户下操作
- **登录失败时**：提示用户检查账号密码是否正确，重新输入
- **Token 自动持久化**：`login()` 和 `loginWithEnv()` 成功后会自动创建 `~/.byteplan/` 目录并保存 token 到 `.env`，无需手动保存
- **自动续期**：`loginWithEnv()` 会自动检测 token 过期并在需要时重新登录
- **凭证共享**：所有分析主题共享 `~/.byteplan/.env` 中的账号信息，避免重复登录
- 密码中的特殊字符需要用引号包裹
- 筛选时使用正确的字段类型（DIM/LIST/LOV/LEVEL）
- API 基础 URL 为 `https://dev.byteplan.com`
- 模型查询已设置默认 menu headers
