---
name: customer-crm
version: "1.0.0"
description: 客户关系管理+来源追踪(DEF-44合并customer-source-tracker)。管理客户档案、复购推荐、来源归因(公众号/闲鱼/抖音/...)。触发：auto-delivery发货后回调/公众号用户互动/复购推荐
tools: [read, exec]
dependencies: []
metadata:
  layer: plugin
  priority: P1
  category: ecom-ops
  openclaw:
    emoji: "👥"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: ["SILICONFLOW_API_KEY"]
      config:
        - mcp.servers.xianyu-agent-mcp
        - mcp.servers.wechat-official-account-mcp
---

# 客户关系管理+来源追踪

**版本**: v1.0 | **优先级**: P1 | **状态**: 🟢 可用 | **来源**: DEF-44公众号引流闭环(合并customer-source-tracker)

## 来源追踪功能（铁律10：合并到现有Skill而非独立新建）

### 来源类型

| 来源 | 标识 | 触发条件 |
|:-----|:-----|:---------|
| 公众号 | wechat_official | wx_reply_message回复用户时自动记录 |
| 闲鱼 | xianyu | confirm_delivery_by_buyer确认下载时自动记录 |
| 抖音 | douyin | content-matrix发布后用户私信时记录 |
| 快手 | kuaishou | content-matrix发布后用户私信时记录 |
| 直接访问 | direct | 无来源标识时默认 |

### 来源数据存储

- 闲鱼来源: `data/xianyu_agent_states/tenant_{tenant_id}_state.json` → `customer_sources` 字段
- 公众号来源: `data/config/wx_source_tracker.json` → openid → source=wechat_official
- 统一归因: 合并到 `daily-briefing` Cron（在daily-briefing执行时追加来源归因统计）

### 使用场景

1. 公众号用户关注后互动 → wx_set_auto_reply引导加群 → wx_reply_message回复 → 来源记录为wechat_official
2. 闲鱼买家确认收货 → confirm_delivery_by_buyer → 来源记录为xianyu
3. 复购推荐 → 根据来源偏好推荐对应渠道的专属商品

## 工作流

### 主流程: 客户来源归因

1. **来源识别**
   - 从wx_source_tracker.json读取公众号来源
   - 从tenant_state的customer_sources读取闲鱼来源
   - 合并为统一客户视图

2. **归因统计**
   - 按来源分组统计客户数
   - 计算各来源转化率
   - 输出到daily-briefing Cron

3. **复购推荐**
   - 根据来源偏好推荐商品
   - 公众号来源→推荐课程/定制开发
   - 闲鱼来源→推荐数字商品/会员专属商品

### 闲鱼消息触发客户档案同步(B3-07/R-98闭环连接)

本工作流声明xianyu-auto-reply→customer-crm→repurchase-guide的完整闭环链路,满足R-98闭环连接规范。xianyu-auto-reply在消息处理流程的步骤6.6主动同步客户档案到customer-crm,customer-crm维护客户视图供repurchase-guide复购推荐使用。

#### 闭环链路图

```
xianyu-auto-reply(消息处理)
    │
    └─[步骤6.6同步]──> customer-crm(客户档案建立/更新)
                              │
                              ├─[来源归因]──> daily-briefing(归因统计)
                              │
                              └─[客户视图]──> repurchase-guide(复购推荐)
                                                  │
                                                  └─[复购消息]──> xianyu-auto-reply(发送复购引导)
```

#### 触发时机

| 触发事件 | 触发条件 | 同步字段 | 来源 |
|:---------|:---------|:---------|:-----|
| 首次咨询 | customer_status=free(首次消息) | buyer_id+source=xianyu+free | xianyu-auto-reply步骤6.6 |
| 状态升级 | consulting→ordered(付款成功) | +ordered+total_spent+total_orders | xianyu-auto-reply步骤6.6 |
| 复购触发 | ordered→repurchased(二次咨询) | +repurchased+last_interaction | xianyu-auto-reply步骤6.6 |
| 确认收货 | confirm_delivery_by_buyer事件 | +delivery_confirmed+source=xianyu | xianyu-agent-mcp事件 |

#### 工作流步骤

1. **接收同步请求** — customer-crm接收xianyu-auto-reply步骤6.6的record_source调用
   - 输入: `{action:record_source, customer_id:{buyer_id}, source:xianyu, platform:xianyu, tenant_id:{tenant_id}}`
   - 附加字段(可选): customer_status/sales_stage/total_spent/total_orders/last_interaction
2. **建立/更新客户档案** — 在`data/xianyu_agent_states/tenant_{tenant_id}_state.json`的`customer_sources`字段写入/更新客户记录
   - 新客户: 创建档案,source=xianyu,first_seen=当前时间
   - 老客户: 更新last_interaction+total_spent+total_orders+customer_status+sales_stage
3. **触发复购推荐**(异步) — 当customer_status升级到ordered或repurchased时,异步通知repurchase-guide
   - 通知方式: 写入`data/repurchase_triggers/{buyer_id}.json`(原子写入)
   - 触发条件: ordered→repurchased(订单≥2) 或 累计消费≥200(白银会员阈值,来源:01手册§六6.1)
4. **归因统计累积**(异步) — 累积到daily-briefing Cron执行时统一输出归因报告
5. **返回同步结果** — 返回`{success:true, data:{recorded:true, source:xianyu, customer_id:{buyer_id}}}`

#### 异常处理

| 异常 | 处理 | 错误码 |
|:-----|:-----|:-------|
| xianyu-auto-reply同步请求customer_id为空 | 返回VALUE_ERROR,跳过同步 | CRM-ERR-01 |
| 租户状态文件不存在 | 创建新文件并初始化空customer_sources | CRM-ERR-03 |
| 复购触发写入失败 | 跳过复购触发,不影响主同步流程,记录warning | CRM-ERR-06 |
| customer-crm不可用 | xianyu-auto-reply主流程继续,记录warning日志(R-98异步最终一致) | - |

#### 验证状态

- ✅ xianyu-auto-reply dependencies已声明customer-crm(SKILL.md第10行)
- ✅ xianyu-auto-reply步骤6.6已定义customer-crm同步流程
- ✅ customer-crm支持record_source action(原SKILL.md输入格式)
- ✅ customer-crm闲鱼来源记录已存在(原"主流程:客户来源归因"第2项)
- ✅ repurchase-guide已声明依赖(xianyu-auto-reply dependencies第8行原已声明)
- ✅ xianyu-auto-reply工作流"确认收货后→触发repurchase-guide"已存在(自动发货流程末尾)
- **结论**: 闲鱼自动回复→CRM→复购闭环已连接,验证通过

## 输入格式

```json
{
  "action": "record_source",
  "customer_id": "xianyu_user_12345",
  "source": "xianyu",
  "platform": "xianyu",
  "tenant_id": "default"
}
```

支持action: record_source(记录来源)/get_customer_profile(获取客户档案)/recommend_repurchase(复购推荐)/attribute_stats(归因统计)

## 输出格式

```json
{
  "success": true,
  "data": {
    "customer_id": "xianyu_user_12345",
    "source": "xianyu",
    "recorded": true,
    "by_source": {
      "wechat_official": 45,
      "xianyu": 120,
      "douyin": 30,
      "direct": 15
    },
    "repurchase_recommendation": [
      {"product": "AI写作Prompt包", "reason": "曾购买AI工具类商品"}
    ]
  },
  "error": null,
  "code": "CRM-SUCCESS-01"
}
```

## 异常处理

| 异常 | 错误码 | 处理 |
|:-----|:-------|:-----|
| 客户ID为空 | CRM-ERR-01 | 返回VALUE_ERROR,提示提供customer_id |
| 来源类型未知 | CRM-ERR-02 | 默认归类为direct,记录warning |
| 租户状态文件不存在 | CRM-ERR-03 | 创建新文件并初始化空customer_sources |
| 复购推荐无历史数据 | CRM-ERR-04 | 返回空推荐列表,标记new_customer |
| daily-briefing归因失败 | CRM-ERR-05 | 跳过归因统计,不影响主流程 |

## 示例

### 示例1: 记录闲鱼来源
```json
输入: {"action":"record_source","customer_id":"xianyu_user_12345","source":"xianyu"}
输出: {"success":true,"data":{"recorded":true,"source":"xianyu"}}
```

### 示例2: 归因统计
```json
输入: {"action":"attribute_stats","tenant_id":"default"}
输出: {"success":true,"data":{"by_source":{"wechat_official":45,"xianyu":120,"douyin":30,"direct":15},"total_customers":210}}
```
