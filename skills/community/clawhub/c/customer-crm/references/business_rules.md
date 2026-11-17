# 业务规则 - customer-crm

> 客户关系管理 + 来源追踪（DEF-44合并 customer-source-tracker）。管理客户档案、复购推荐、来源归因。
> 规则来源：`skills/customer-crm/SKILL.md`，并交叉引用设计文档。

## 规则列表

### 来源识别与归因

- 来源类型识别: 客户来源分为 wechat_official(公众号)/xianyu(闲鱼)/douyin(抖音)/kuaishou(快手)/direct(直接访问)，无来源标识时默认 direct (来源: SKILL.md§来源类型)
- 公众号来源记录: wx_reply_message 回复用户时自动记录，存储于 `data/config/wx_source_tracker.json`，openid → source=wechat_official (来源: SKILL.md§来源数据存储)
- 闲鱼来源记录: confirm_delivery_by_buyer 确认下载时自动记录，存储于 `data/xianyu_agent_states/tenant_{tenant_id}_state.json` 的 `customer_sources` 字段 (来源: SKILL.md§来源数据存储)
- 统一归因: 合并到 daily-briefing Cron，执行时追加来源归因统计 (来源: SKILL.md§来源数据存储)

### 客户状态机（闲鱼消息触发同步）

- 客户状态流转: free(首次咨询) → consulting(咨询中) → ordered(付款成功) → repurchased(二次咨询) (来源: SKILL.md§触发时机)
- 首次咨询同步: customer_status=free 时同步 buyer_id + source=xianyu + free (来源: SKILL.md§触发时机)
- 状态升级同步: consulting→ordered 时附加 ordered + total_spent + total_orders (来源: SKILL.md§触发时机)
- 复购触发同步: ordered→repurchased 时附加 repurchased + last_interaction (来源: SKILL.md§触发时机)

### 复购触发条件

- 复购触发条件A: ordered→repurchased（订单数 ≥ 2） (来源: SKILL.md§工作流步骤3)
- 复购触发条件B: 累计消费 ≥ 200（白银会员阈值） (来源: SKILL.md§工作流步骤3，引用 01手册§六6.1 会员体系)
- 触发方式: 写入 `data/repurchase_triggers/{buyer_id}.json`（原子写入），异步通知 repurchase-guide (来源: SKILL.md§工作流步骤3)

### 复购推荐（按来源偏好）

- 公众号来源偏好: 推荐课程 / 定制开发类商品 (来源: SKILL.md§复购推荐)
- 闲鱼来源偏好: 推荐数字商品 / 会员专属商品 (来源: SKILL.md§复购推荐)

### 闭环连接（R-98）

- 闭环链路: xianyu-auto-reply(步骤6.6同步) → customer-crm(档案建立/更新) → repurchase-guide(复购推荐) → xianyu-auto-reply(发送复购引导) (来源: SKILL.md§闭环链路图)
- 异步最终一致: customer-crm 不可用时 xianyu-auto-reply 主流程继续，记录 warning (来源: SKILL.md§异常处理)

## 关键阈值速查表

| 阈值项 | 值 | 来源 |
|:-------|:---|:-----|
| 复购触发-订单数 | ≥ 2 | SKILL.md§工作流步骤3 |
| 复购触发-累计消费 | ≥ 200（白银会员阈值） | SKILL.md§工作流步骤3 / 01手册§六6.1 |
| 客户来源类型数 | 5 种(wechat_official/xianyu/douyin/kuaishou/direct) | SKILL.md§来源类型 |
| 触发写入方式 | 原子写入 `data/repurchase_triggers/{buyer_id}.json` | SKILL.md§工作流步骤3 |

## 说明

- 以上阈值与状态机均来自 SKILL.md 原文，未引入 SKILL.md 未声明的规则。
- 涉及会员等级的阈值（如累计消费≥200）以 SKILL.md 标注的 01手册§六6.1 为准；该会员体系在 repurchase-guide 中标注为 v1.0暂缓，使用时注意当前可用性。
