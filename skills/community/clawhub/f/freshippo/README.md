# Freshippo Skill v2.1.2

盒马鲜生安全购物决策助手 Skill，支持生鲜选购、购物清单规划、配送时段建议、会员/优惠核对清单和手动下单交接。

This published skill is decision-assist only. It does not log in, change in-app product lists, reserve delivery slots, submit orders, choose addresses, apply coupons, or pay. If a separate host environment provides an audited account-changing tool, that action is outside this skill and must require fresh user confirmation.

## 功能特性

- 🔍 **商品搜索建议**：给出搜索关键词、筛选维度、对比表
- 🥬 **生鲜选购**：新鲜度、产地、溯源码判断
- 💰 **价格/会员核对**：提示用户在 App 内手动核对普通价、会员价、优惠券
- 🧾 **购物清单**：数量、替代品、预算、避免浪费
- 🚚 **配送时段建议**：基于新鲜度和用餐时间推荐主/备选窗口
- 📋 **手动下单交接**：用户本人在盒马 App 内核对商品清单、地址、配送时段、订单提交和支付

## 安全边界

| 操作 | Agent | 用户 |
|------|-------|------|
| 搜索建议/对比 | ✅ | 可复核 |
| 新鲜度/预算/替代品建议 | ✅ | 可复核 |
| App 内商品清单/用券/选地址 | ❌ | ✅ |
| 选择配送时段/提交订单/支付 | ❌ | ✅ |

## 工作流程

```text
发现 → 对比 → 生成购物清单 → 用户手动在盒马 App 核对商品/优惠/配送 → 用户本人提交订单并支付
```

## 使用示例

```text
用户：帮我买盒马的三文鱼
Agent：搜索建议 → 对比新鲜度 → 生成数量/替代品/时段建议
用户：在盒马 App 手动录入商品清单、选地址、选配送、提交订单并支付
```

## 安装

```bash
clawhub install freshippo
```

## License

MIT
