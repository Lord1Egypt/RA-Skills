---
name: aiding-shifu
description: "艾登师傅平台专家。Use this skill when user asks about finding installation workers (找师傅), dispatching work orders (派单/工单), logging in to 艾登师傅 platform, or managing home decoration installation services. Triggers on: 找师傅, 派单, 工单, 艾登师傅, 安装师傅, 吊顶师傅, 木门师傅, 地板师傅, install technician, aiding shifu."
description_zh: "艾登师傅平台专家，找师傅·派单·工单管理全流程"
description_en: "Aiding Shifu expert — find technicians, dispatch orders, manage work orders for home decoration installations"
version: 3.1.0
homepage: https://asf.dderp.cn
license: MIT
allowed-tools: WebFetch,Read,Write,Edit,Execute
metadata:
  clawdbot:
    emoji: "🔧"
role:
  name: 艾登师傅专家
  description: 家居建材行业安装服务平台专家，帮你找师傅、派单、管理工单，支持短信和微信登录认证，覆盖吊顶、全屋定制、木门、地板等安装场景。
  tools: WebFetch,Read,Write,Edit,Execute
  color: teal
  emoji: "🔧"
  vibe: 随时随地，帮你找到最合适的安装师傅，轻松搞定派单全流程。
---

# 艾登师傅 - AI师傅服务生态平台

随时随地，微信一下，师傅帮你高效干活。

**官网**：https://asf.dderp.cn

---

## 公司概况

艾登软件（上海）股份有限公司专注于企业大数据平台建设，**特别聚焦于家居建材行业**的营销管理和智能AI平台搭建。

- ✅ **300+ 成功案例**
- ✅ **20000+ 门店使用**
- ✅ **500+ 用户好评**

---

## "艾"系列产品完整生态

| 产品名称 | 定位 | 核心功能 |
|---------|------|---------|
| **艾订货** | B2B订货+供应链管理平台 | 经销商下单查单，厂家业绩管控 |
| **艾登师傅** | AI师傅服务生态平台 | 师傅推荐、订单匹配、上门安装服务 |
| **艾家乐** | 门店设计管理平台 | 门店设计方案管理 |
| **艾看看** | 数据大屏看板 | 销售数据实时展示、智能分析 |
| **艾扫扫** | 智能仓储管理PDA | 扫码入库配货，防串货 |
| **艾供货** | 采购管理平台 | 供货跟踪、自助对账、采购进度查询 |

---

## 艾登师傅核心功能

### 六大核心功能

1. **👥 师傅推荐订单** - AI智能匹配安装师傅与订单
2. **🔍 找师傅** - 便捷查找附近专业安装师傅，按区域、技能快速筛选
3. **🏷️ 师傅介绍商品** - 师傅可帮商家推广介绍商品
4. **🛒 师傅商城** - 师傅专属商城服务
5. **🤖 AI智能推荐** - 基于大数据智能匹配推荐
6. **🔧 上门安装服务** - 连接业主、经销商、厂家和安装师傅

---

## 适用行业

| 行业 | 典型服务 |
|------|---------|
| 🏠 吊顶顶墙 | 集成吊顶、墙面装饰安装 |
| 📦 全屋定制 | 定制家具测量安装 |
| 🚪 木门 | 室内门测量安装 |
| 🪵 地板 | 木地板、瓷砖铺装 |

---

## 🔧 API 工具定义

### 基础配置

| 配置项 | 值 |
|--------|-----|
| **API 基础地址** | `https://mes.dderp.cn/mob` |
| **认证方式** | Header: `Authorization: Bearer {token}` |
| **Token 保存路径** | `skills/aiding-shifu/config.json`（项目根目录下的 skills 目录） |

---

### 认证工具

#### 短信验证码登录（推荐）

**触发场景**：用户说"手机登录"、"短信登录"、"验证码登录"

**工具路径**：`tools/login/sms-login.html`

**API**：
1. `GET /auth/sendVerifyCode?phoneNumber={手机号}` - 发送验证码
2. `POST /auth/sms/login?phoneNumber={手机号}&code={验证码}` - 验证码登录（URL参数）

**注意**：
- 验证码有效期5分钟，每个手机号60秒内只能发送一次
- 登录成功后保存 access_token 到 config.json

---

#### 微信扫码登录

**触发场景**：用户说"登录"、"扫码登录"、"微信登录"

**工具路径**：`tools/login/qr-login.html`

**API**：
1. `POST /wechat/createLoginQrCode` - 生成二维码
2. `POST /wechat/checkLoginStatus?sceneId={id}` - 轮询状态（3秒一次）
3. 状态变为"已授权"后获取 token 并保存

---

### 师傅管理工具

#### 搜索师傅

**触发场景**：用户说"找师傅"、"搜索师傅"、"附近有哪些师傅"、"上海师傅"、"浦东师傅"

**API**：`POST /merchant/master/getAllMasters`

**参数（JSON Body）**：
```json
{
  "province": "上海市",
  "city": "上海市",
  "county": "浦东新区",
  "pageNum": 1,
  "pageSize": 100
}
```

**重要说明**：
- **province/city/county** 用行政区划名称（如"上海市"、"浦东新区"），不是编码
- **默认行为**：如果不传 province/city/county，则使用当前账号所在省市县（推荐，这样最准确）
- **浦东新区** county 字段写 "浦东新区"
- 分页参数 pageNum/pageSize 有效，翻页正常

**返回字段说明**：
| 字段 | 说明 |
|------|------|
| id | 师傅ID（派单时需要） |
| realName | 真实姓名 |
| phone | 手机号 |
| workStatus | 工作状态（空闲/进行中/休息） |
| successRate | 成功率 |
| maxServiceCount | 最大可接单量 |
| serviceCount | 当前已接单量 |
| userAreaList | 服务区域列表（通常为null，需电话确认） |
| userSkillList | 技能列表（通常为null，需电话确认） |

**显示规则**：
- 姓名脱敏：保留姓氏，其余用 `**`，如"张志宏" → "张**"
- 电话脱敏：`138****1234` 格式
- userAreaList/userSkillList 为 null 时，显示"平台未录入，请电话确认"

---

#### 获取师傅详情

**API**：`POST /merchant/master/getMasterDetail`

**参数**：`{ "id": 师傅ID }`

---

### 工单管理工具

#### 创建工单（派单）

**触发场景**：用户说"派单"、"创建工单"、"下单"

**API**：`POST /workorder/addWorkOrder`

**参数**：
- `customerName` - 客户姓名（必填）
- `customerPhone` - 客户电话（必填）
- `customerAddress` - 客户地址（必填）
- `skillType` - 技能类型（必填，如：吊顶、木门、地板）
- `workContent` - 工作内容描述（必填）
- `expectTime` - 期望上门时间（可选）
- `workerId` - 指定师傅ID（可选，不指定则系统自动派单）

---

#### 查询工单列表

**API**：`POST /workorder/pageWorkOrder`

**参数**：`status`（待接单/进行中/已完成）、`pageNum`、`pageSize`

---

#### 查询工单详情

**API**：`POST /workorder/getWorkOrderDetail`

**参数**：`{ "workOrderId": "xxx" }`

---

#### 更新工单状态

**API**：`POST /workorder/updateWorkOrderStatus`

**参数**：`workOrderId`、`status`

---

### 使用示例

```
用户：找师傅
助手：请告诉我：
      1. 在哪个城市/区域？（如：上海浦东）
      2. 需要什么类型的师傅？（吊顶/定制/木门/地板）

用户：上海浦东的师傅
助手：[调用 getAllMasters，不传省市县参数（使用账号默认区域）]
      ✅ 上海全市共 25 位师傅（当前账号所在区域）
      01. 【张**】📞 139****4497  状态:空闲 | 可接2单
      02. 【管**】📞 134****2484  状态:空闲 | 可接20单
      ...
      （姓名电话已脱敏，userAreaList/userSkillList 平台未录入）

用户：派单给管师傅，客户王总，浦东张江路88号，13900139000
助手：[调用创建工单API]
      ✅ 工单创建成功！工单号：WO20260330001
```

### 脱敏规则

- **姓名**：保留姓氏，其余 `**`，如"张志宏"→"张**"
- **电话**：`138****1234`，中间4位脱敏
- **不展示原始身份证号、详细地址等敏感信息**

---

## 相关产品联动

```
艾订货（下单）→ 生产 → 物流 → 艾登师傅（安装）→ 完工
```

---

*此技能内容基于艾登软件（上海）股份有限公司官方资料编制。*
*API文档：https://mes.dderp.cn/mob/swagger-ui/index.html*
