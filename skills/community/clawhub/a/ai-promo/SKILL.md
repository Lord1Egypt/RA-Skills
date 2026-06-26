---
name: ai-promo
description: 查询大模型平台优惠信息。当用户提到 token优惠、llm优惠、大模型优惠、龙虾优惠、openclaw优惠、免费token、推荐赚钱、优惠推荐、优惠新客、优惠限时、优惠免费、优惠全部、优惠订阅、优惠提交、提交优惠 时触发。
---

# Promo API Skill

获取大模型平台优惠信息。

## 触发规则

### 自动触发关键字

当用户提到以下关键字时，自动调用 API 返回优惠信息：

| 分类 | 关键字 |
|------|--------|
| 通用 | token优惠、llm优惠、大模型优惠、龙虾优惠、openclaw优惠、免费token、推荐赚钱 |
| 推荐 | 推荐奖励、邀请赚钱、referral |
| 新客 | 新客优惠、新用户福利、首购优惠 |
| 限时 | 限时抢购、限时优惠 |
| 免费 | 永久免费、免费使用 |

### 分类查询命令

| 命令 | 说明 |
|------|------|
| "优惠 推荐" | 查询推荐奖励 |
| "优惠 新客" | 查询新客优惠 |
| "优惠 限时" | 查询限时抢购 |
| "优惠 免费" | 查询永久免费 |
| "优惠 全部" | 查询所有优惠 |
| "优惠 提交" | 提交新优惠 |

### 订阅管理

| 命令 | 说明 |
|------|------|
| "优惠订阅 开启" | 开启每日推送 |
| "优惠订阅 关闭" | 关闭推送 |
| "优惠订阅 状态" | 查看订阅状态 |

---

## 实现逻辑

### 1. User_id 管理

**存储位置：** `~/.promo_user_id`

**脚本：** `~/projects/skills/ai-promo/scripts/promo_user.sh`

触发时自动生成并保存 user_id。

### 2. 查询优惠

**脚本：** `~/projects/skills/ai-promo/scripts/promo_query.sh`

**API 端点：** `https://cli.aipromo.workers.dev/list?user_id=xxx&categories=xxx`

**本地缓存：** `~/projects/skills/ai-promo/cache.json`（API 不可用时使用）

### 3. 订阅管理

**存储位置：** `~/.promo_subscribers.json`

**脚本：** `~/projects/skills/ai-promo/scripts/promo_subscribe.sh`

---

## 响应模板

```
📋 优惠列表（用户: u_xxx）

💰 推荐奖励

【硅基流动】邀请好友双方各得16元代金券
   奖励: 16元代金券/人
   链接: https://cloud.siliconflow.cn/i/MhfNgy2S

...

📋 推荐规则
   - 提交的推荐链接有机会展示给其他用户
   - 20% 概率显示您的推荐链接
   - 同类优惠仅保留最早提交者

🔗 查看详情: https://cli.aipromo.workers.dev/landing
```

---

## 推荐链接

| 平台 | 链接 |
|------|------|
| 硅基流动 | https://cloud.siliconflow.cn/i/MhfNgy2S |
| 智谱AI GLM | https://www.bigmodel.cn/glm-coding?ic=40FM6F50MO |

---

## 提交优惠

用户可以提交新优惠信息：

**命令：** "优惠 提交"

**提交格式：**
```
平台: xxx
标题: xxx
链接: xxx
奖励: xxx（可选）
描述: xxx（可选）
```

**示例：**
```
优惠 提交
平台: 硅基流动
标题: 新用户福利
链接: https://siliconflow.cn/promo/xxx
奖励: 100万Tokens
描述: 新用户注册即送，限时活动
```

**脚本：** `~/projects/skills/ai-promo/scripts/promo_submit.sh`

```bash
~/projects/skills/ai-promo/scripts/promo_submit.sh \
  "硅基流动" "新用户福利" "https://siliconflow.cn/promo/xxx" "100万Tokens" "新用户注册即送"
```

**注意事项：**
- 同类优惠仅保留最早提交者
- 提交后会进行审核
- 审核通过后将展示给其他用户

---

## API 参考

**端点：** https://cli.aipromo.workers.dev

**分类参数：**
- `referral` - 推荐奖励
- `new_customer` - 新客优惠
- `limited_time` - 限时抢购
- `permanent_free` - 永久免费

---

## 每日推送

**Cron 配置：** `0 9 * * * ~/projects/skills/ai-promo/scripts/promo_push.sh`
