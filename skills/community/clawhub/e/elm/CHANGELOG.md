# Changelog

## 2.0.1

Release theme: 修正安全扫描风险点，把账号认证改为用户自助完成。

What changed:
- 移除对登录秘密信息作为 skill 输入的要求
- 把登录流程改成用户在饿了么官方页面自行完成认证，skill 只接管登录后的已认证会话
- 保留自然语言下单、地址搜索、优惠比较、购物车构建和支付前交接能力
- 收紧 README、package、Clawhub 文案，避免把 skill 描述成会代用户处理登录秘密信息

Suggested one-line changelog:
- Tightened elm security boundaries so users authenticate themselves in the official Ele.me login flow before the skill resumes cart building.

## 2.0.0

Release theme: 从“饿了么值不值得下单”升级为“饿了么下单协助执行”。

What changed:
- 把 skill 定位从公开决策建议改为基于用户授权的下单协助
- 新增自然语言输入结构：地址、商品、具体要求和预算
- 新增登录后会话承接、按地址搜索、购物车构建、支付前交接流程
- 强化优惠券、红包、满减、配送费、包装费、ETA 的真实结算比较
- 明确安全边界：只承接用户已认证会话并加购物车，不保存敏感信息，不代用户支付
- 同步升级 README、package、Clawhub 发布文案

Suggested one-line changelog:
- Upgraded elm from a promo-decision skill into an assisted Ele.me ordering copilot that resumes after user authentication, builds the best cart, and hands off at payment.

## 1.3.0

Release theme: 从基础饿了么说明升级为“红包是不是真省钱”的行动型决策。

What changed:
- 重写 skill 定位，默认输出直接动作建议
- 强化红包真假价值、满减门槛、真实到手价、配送与商家风险判断
- 收紧 package、Clawhub、README 文案，突出“这一单到底该不该下”

Suggested one-line changelog:
- Upgraded elm into an action-first Ele.me decision skill focused on whether hongbao and threshold promos create real savings.

## 1.0.0

Release theme: 饿了么行动型外卖决策首发版。

What ships:
- 新增 elm skill
- 重点判断红包真假价值、满减门槛、真实到手价、配送与商家风险
- 输出收敛到“这一单到底该不该下”
- 补齐 README、package、Clawhub 发布文案

Suggested one-line changelog:
- Launch elm, an action-first Ele.me ordering decision skill focused on whether hongbao and threshold promos create real savings.
