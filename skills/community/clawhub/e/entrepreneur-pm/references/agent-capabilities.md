# Agent 能力矩阵

## Leevar 团队全员能力表

| Agent / 路径 | 工具权限 | 专属 Skill | 输出格式 | 不能做 |
|-------------|---------|-----------|---------|-------|
| **主 Agent (Leevar)** | 全部 MCP 工具 | 所有 Skill | 任意 | 直接执行长时任务 |
| **sessions_spawn subagent** | 继承主 Agent | 需在任务包中指定 | 文件/报告 | 持久状态记忆 |
| **MarketWatcher** | batch_web_search, exec | options-trader | JSON/Markdown | 实际下单交易 |
| **SocialAgent** | batch_web_search, write | social-media | 草稿文件 | 直接发布（需 Lee 审批）|
| **SupplierAgent** | batch_web_search, exec | dropshipping | JSON 供应商报告 | 支付/下单 |
| **ContentAgent** | image_synthesize, write | content-marketing | 图文内容包 | 发布到平台 |
| **OutreachAgent** | batch_web_search, write | b2c-marketing | leads/草稿 | 直接发消息（需审批）|
| **cloud browser** | browser 全部操作 | playwright-mcp | 截图/DOM | 本地设备操作 |
| **LocalAgent/Hex** | 本地浏览器 | - | 截图/操作结果 | 云端操作 |

---

## 工具能力边界

### batch_web_search
- ✅ 最多 10 个查询/次
- ✅ 支持：search, news, shopping, videos, places
- ❌ 无法抓取需要登录的页面
- ❌ 无法执行 JavaScript 渲染页面

### extract_content_from_websites
- ✅ 最多 10 个 URL/次
- ✅ 支持 mode: auto/curl_only/browser_only
- ❌ 无法抓取 PDF（用 extract_pdfs_*）
- ❌ 动态 JS 内容需用 browser_only 模式

### image_synthesize
- ✅ 最多 10 个请求/次
- ✅ 支持参考图（input_files/input_urls）
- ✅ 支持分辨率：1K/2K/4K
- ❌ 不保证与真实产品照片完全一致（AI 生成）

### exec
- ✅ 可运行 Python3、Node.js、curl、bash
- ✅ 支持后台运行（background=true）
- ❌ 无交互式命令（no TTY）
- ❌ 重复调用同一操作会触发 loop detection

### Shopify API
- GraphQL: `https://nsb9ct-sc.myshopify.com/admin/api/2024-01/graphql.json`
- REST: `https://nsb9ct-sc.myshopify.com/admin/api/2024-01/{resource}.json`
- Token: 在 `/home/minimax/.openclaw/secrets/.env` 的 SHOPIFY_ADMIN_TOKEN
- ⚠️ 添加/修改变体需要用 GraphQL（REST 不支持 options 修改）
- ⚠️ 删除变体需要保留至少一个变体

---

## Agent 专长评分（1-5）

| 能力 | Leevar | MarketWatcher | SocialAgent | SupplierAgent | ContentAgent |
|------|--------|--------------|-------------|--------------|-------------|
| Shopify 操作 | 5 | 1 | 1 | 1 | 1 |
| 市场数据分析 | 3 | 5 | 2 | 3 | 1 |
| 文案创作 | 4 | 1 | 5 | 2 | 5 |
| 供应商研究 | 3 | 2 | 1 | 5 | 1 |
| 视觉内容 | 3 | 1 | 4 | 1 | 5 |
| 代码执行 | 4 | 3 | 1 | 2 | 1 |
| 策略规划 | 5 | 4 | 3 | 3 | 2 |

---

## 任务规模分类

| 规模 | 时间 | 处理方式 |
|------|------|---------|
| 微任务 | <2分钟 | Leevar 直接处理 |
| 小任务 | 2-10分钟 | Leevar 直接处理或简单 exec |
| 中任务 | 10-30分钟 | sessions_spawn (mode=run) |
| 大任务 | 30分钟-2小时 | sessions_spawn + 自动报告 |
| 超大任务 | >2小时 | 拆分 → 多个 subagent 并行 |

**并行执行规则：**
- 互相独立的任务：可以同时 spawn 多个 subagent
- 有依赖关系：必须串行（A 完成后 B 才能开始）
- 最大并行数建议：≤3 个（避免资源竞争和 loop detection）

---

## 关键约束速查

### 永远不做（Iron Rules）
- 不打印/记录完整 API Token、密码、Cookie
- 不在 /workspace/ 存储密钥（用 /home/minimax/.openclaw/secrets/）
- 不自称"已完成"但没有实际验证
- 不替 Lee 做付款/发布/广告预算操作
- 不修改 openclaw.json（用 gateway(action="config.patch")）

### 总是要做
- 任务完成后写验证步骤
- 报告格式：Goal / Current state / What I did / What I verified / Status / Next step
- 中文说明 + 英文可直接使用的文案
- 遇到阻塞：说明阻塞原因，不是沉默
