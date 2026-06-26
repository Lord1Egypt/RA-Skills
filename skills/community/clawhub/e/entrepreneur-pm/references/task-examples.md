# 任务包案例库

## 案例 1：产品文案批量更新（成功案例）

**背景**：Lee 要求更新 19 款产品的英文文案，加入代发免责和退款保障。

**任务包（实际使用版本）：**

```
任务目标：为 leevar.store 全部 19 款产品重写 Shopify 产品详情页英文文案并更新到 Shopify

背景：
- 产品都是代发模式，需要客户知道是从国际仓发货
- 需要建立购买信任（退款保障、安全支付）

具体要求：
1. 文案结构：Hook + Why You'll Love It(5 bullets) + Perfect For + Specs表格 + Shipping & Promise
2. Shipping部分固定文字（见下方模板）
3. Anti-Bark Collar特殊合规要求：不得提及IP67/waterproof
4. 通过 Shopify REST API PUT 更新 body_html

输出要求：
- 直接更新 Shopify，不需要先生成文件
- 验证方法：GET 该产品，检查 body_html 包含 "Shipping & Our Promise" 字样
- 报告写入 /workspace/tasks/daily/YYYY-MM-DD-copy-update.md

禁止事项：
- 不得修改价格、标题、SKU
- Anti-Bark Collar 不得写 IP67 / waterproof / 电池时长
```

**结果**：19/19 成功，主页同步更新 ✅

**经验**：
- 合规限制必须在任务包中明确列出禁止词，否则 Agent 容易遗漏
- 验证方法要具体（检查特定字符串），不能只说"确认已更新"

---

## 案例 2：期权分析（双分析师协作）

**背景**：Lee 问下周期权怎么做，有 $100 预算。

**任务包设计：**

```
任务目标：找到下周 $100 以内可买的最佳单腿期权（只能买 Call/Put，不能做价差）

背景：
- Lee 只有 $100，Level 1 期权权限（只能买单腿）
- 需要有明确催化剂的标的
- 接受最大亏损 = 权利金

具体要求：
1. 扫描 SPY/QQQ/NVDA/META/MU/TSLA 等主要标的
2. 找期权 Ask 在 $0.50-$1.00/股（即 $50-100/手）的机会
3. 每个候选必须有：催化剂事件、技术面方向、IV 评估

输出要求：
- 最终给出 1-2 个具体推荐（执行价、到期日、当前 Ask 价）
- 格式：Lee 可以直接在 App 里操作的步骤
- 报告写入 /workspace/trading/
```

**结果**：找到 NVDA $200C (3/21)，$50-90/手，GTC 催化剂 ✅

**经验**：
- 搜索实际期权价格时，MarketWatch 等网站很多内容是动态加载的，需要用 Yahoo Finance 直链（`yahoo.com/quote/NVDA260321C00200000`）
- 财报前 IV 会大幅推高近月期权成本，预算 $100 在这种环境下很有限
- 下次直接搜 `{TICKER}{DATE}C{STRIKE}` 格式的 Yahoo Finance 期权直链

---

## 案例 3：产品变体添加（GraphQL 路径）

**背景**：为 17 款产品添加颜色/尺寸/款式变体。

**关键技术发现：**
- Shopify REST API 2024-01 的 `PUT /products/{id}.json` **不支持直接修改 options 名称**
- 正确路径：用 GraphQL `productOptionsCreate`（2023-10+ API）
- `productUpdate` mutation 支持同时设置 options 和 variants
- 添加变体时，原来的 "Default Title" 变体需要特殊处理（不能直接删除再加，否则第一个新变体也会丢失）

**下次执行模板：**

```python
# Step 1：创建新 options
mutation = """
mutation productOptionsCreate($productId: ID!, $options: [OptionCreateInput!]!, $variantStrategy: ProductOptionCreateVariantStrategy) {
  productOptionsCreate(productId: $productId, options: $options, variantStrategy: $variantStrategy) {
    userErrors { field message code }
    product { options { id name values { id name } } }
  }
}
"""

# Step 2：用 productVariantsBulkCreate 添加剩余变体
# Step 3：用 productVariantsBulkDelete 删除 Default Title
```

---

## 案例 4：任务路由失误复盘

**失误**：把"验证 Shopify 产品图片是否显示"任务分配给了 API subagent，结果只能检查 URL 状态码，无法看到实际渲染效果。

**正确路由**：视觉验证任务 → cloud browser（截图）

**规则沉淀**：
> URL 状态码检查（200/404）→ API/exec
> 视觉渲染验证（图片是否实际显示，布局是否正确）→ cloud browser + 截图

---

## 模板库

### 快速任务包（5分钟内可完成的任务）

```markdown
任务：[一句话描述]
工具：[exec / API / browser]
输出：[直接告知 Lee 结果 / 写入文件路径]
验证：[如何确认完成]
```

### 研究任务包

```markdown
任务：研究 [主题]
来源：[网站优先级：官方文档 > 权威媒体 > 社区]
输出格式：Markdown，包含来源 URL
深度：[摘要(500字) / 深度(2000字) / 原始数据]
截止：[立即 / 今天 / 下次巡逻]
```

### Agent 协作任务包

```markdown
任务目标：[最终结果]
执行 Agent：[Agent A 做 X，Agent B 做 Y]
交接协议：
  - A 完成后输出到：[路径]
  - B 接收后执行：[步骤]
汇报：两个 Agent 完成后，主 Agent 整合报告给 Lee
```
