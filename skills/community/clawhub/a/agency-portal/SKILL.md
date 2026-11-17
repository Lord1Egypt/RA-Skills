---
name: agency-portal
version: "1.7.0"
description: "代运营客户自助门户+管理员后台,提供租户登录/注册/套餐/素材/报告/续费/审批/反馈/平台绑定/配额/计费/品牌管理/数据统计/竞品监控/数字人/充值等187个MCP工具(server.py @mcp.tool实测)+199个HTTP handler(portal_server.py _handle_方法)。触发: 租户入驻/续费/素材管理/内容审批/巡检/反馈处理/配额查询/账单/品牌管理/数据统计/竞品监控/数字人/充值"
tools: [read, memory_search]
dependencies: []
metadata:
  layer: product
  priority: P1
  category: agency-ops
  openclaw:
    emoji: "🏢"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: ["AGENCY_PORTAL_JWT_SECRET", "AGENCY_ADMIN_SECRET", "AGENCY_PORTAL_PORT"]
      config: ["mcp.servers.agency-portal-mcp"]
    mcp:
      server: agency-portal-mcp
      transport: stdio
      command: python
      args: ["-u", "d:\\JueJin\\mcps\\agency-portal-mcp\\server.py"]
      cwd: "d:\\JueJin\\mcps\\agency-portal-mcp"
    department: libu_hr
    business_flows: [CP-15, CP-16, CP-17, CP-18, CP-19, CP-20]
---

# 代运营客户门户 v1.7

租户自助门户+管理员后台,提供187个MCP工具(server.py @mcp.tool实测)+199个HTTP handler(portal_server.py _handle_方法),覆盖登录/注册/套餐/素材/报告/续费/内容方向/审批/反馈/平台绑定/配额/计费/发布记录/退款/支付/月度账单/品牌管理/数据统计/竞品监控/数字人/充值全流程。

## 套餐体系

| 套餐 | 月价 | 每周选题 | 每日视频 | 平台数 | 地域定向 |
|:-----|:-----|:---------|:---------|:-------|:---------|
| basic 基础版 | ¥298 | 3/周 | 0 | 5 | 否 |
| standard 专业版 | ¥698 | 10/周 | 1 | 12 | 是 |
| premium 旗舰版 | ¥1,298 | 不限 | 2 | 16 | 是 |

## 使用场景

1. 租户入驻(CP-15): 运营方为客户创建门户账号+租户+订阅+目录
2. 租户登录/仪表盘: JWT认证(24h有效期)，聚合订阅/素材/报告/发布统计
3. 素材管理: 上传/查看/删除素材文件
4. 报告获取: 日/周/月度运营报告
5. 套餐续费(CP-17): 续费或升级套餐
6. 内容审批(CP-18): 批准/拒绝待发布内容
7. 反馈沟通(CP-20): 租户提交反馈，管理员回复
8. 管理员: 租户管理/套餐变更(CP-16)/全局概览/到期检查/巡检(CP-19)/反馈回复

## 工作流

### 租户侧

#### W1: 租户入驻(CP-15)
1. 调用portal_register(tenant_slug/username/password/tenant_name/plan)
2. 验证套餐有效性+标识唯一性
3. 创建租户记录+订阅(默认1个月)+素材目录+发布日志目录
4. 返回租户ID+门户URL

#### W2: 登录+仪表盘
1. portal_login → 验证凭据 → JWT Token(24h)
2. portal_get_dashboard → 聚合: 租户信息+订阅+素材数+报告+发布统计

#### W3: 素材管理
1. portal_list_assets → portal_upload_asset → portal_delete_asset

#### W4-W7: 报告/续费/审批/反馈
1. 报告: portal_get_reports(period_type)
2. 续费: portal_renew_subscription(plan/months) → admin_confirm_renewal审批
3. 审批: portal_list_pending_content → portal_approve_content(content_id/action)
4. 反馈: portal_submit_feedback(content/category) → 生成fb_xxxxxxxx

#### W8: 平台账号绑定
1. portal_get_platforms → 查看支持平台列表
2. portal_bind_platform_account(platform/account_name/agree_terms) → 绑定
3. portal_list_bound_accounts → 查看已绑定账号
4. portal_unbind_platform_account(platform/account_name) → 解绑

#### W9: 配额与计费
1. portal_get_quota → 查看日配额/月配额/已用量
2. portal_get_usage_stats(days) → 查看使用统计
3. portal_get_billing → 查看账单+超量费+降级状态
4. portal_get_payment_code(amount/payment_type) → 生成付款码
5. portal_record_publish(token/content_type/title/platform) → 记录发布并检查配额

#### W10: 其他租户操作
1. portal_update_directions(token/directions) → 更新内容方向
2. portal_change_password(token/old_password/new_password) → 修改密码
3. portal_toggle_auto_publish(token/enabled) → 开关自动发布
4. portal_get_service_agreement(token) → 查看服务协议

### 管理员侧

#### W8: 管理员登录+全局概览
1. admin_login(password) → 验证AGENCY_ADMIN_SECRET → admin Token(8h)
2. admin_get_overview → 聚合: 租户数/收入/套餐分布/到期提醒/待处理反馈

#### W9: 租户管理
1. admin_list_tenants → admin_get_tenant_detail → admin_update_tenant_plan / admin_toggle_tenant / admin_delete_tenant

#### W10: 代运营巡检(CP-19)
1. admin_patrol → 遍历active租户检查: 素材充足(≥1)/自动发布状态/内容方向/发布进度(≥50%)
2. 返回巡检报告: 活跃数/问题数/问题明细

#### W11-W12: 到期检查/反馈处理
1. 到期: admin_check_expiry(days=7) → 分类expired/expiring
2. 反馈: admin_list_feedbacks → admin_reply_feedback

#### W13: 租户审批与归档
1. admin_approve_tenant(tenant_slug/action) → 审批/拒绝新租户
2. admin_auto_downgrade_expired(grace_days) → 自动降级到期租户
3. admin_archive_old_tenants(archive_days) → 归档旧租户

#### W14: 退款与支付
1. admin_process_refund(tenant_slug/reason/refund_months) → 处理退款
2. admin_confirm_payment(payment_id/transaction_ref) → 确认支付

#### W15: 月度账单
1. admin_generate_monthly_billing(month) → 生成月度账单

#### W16: 配额调整
1. portal_update_quota(admin_token/tenant_id/daily_graphic_quota/daily_video_quota) → 管理员调整配额

## 输入格式

```json
// 租户注册
{"tenant_slug": "kebab-case标识", "username": "登录名", "password": "密码", "tenant_name": "名称", "plan": "basic|standard|premium"}
// 租户登录
{"username": "用户名", "password": "密码"}
// 内容审批
{"token": "JWT Token", "content_id": "内容ID", "action": "approve|reject"}
```

> 完整输入/输出格式、错误码、MCP工具清单、数据存储路径详见 scripts/agency_portal_reference.json

## 输出格式

```json
{
  "success": true,
  "data": {
    "tenant_id": "tnt_xxxxxxxxxxxx",
    "tenant_slug": "kebab-case标识",
    "tenant_name": "星辰科技",
    "plan": "standard",
    "subscription_status": "active",
    "expires_at": "2026-07-11T00:00:00Z",
    "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_expires_in": 86400,
    "dashboard_summary": {
      "assets_count": 12,
      "reports_count": 5,
      "today_publish_count": 1,
      "quota_used": {"daily_graphic": 3, "daily_video": 1},
      "quota_limit": {"daily_graphic": 10, "daily_video": 1}
    }
  },
  "error": null,
  "code": null
}
```

字段说明:
- `tenant_id`: 租户唯一ID(tnt_前缀)
- `plan`: 套餐类型(basic/standard/premium)
- `subscription_status`: 订阅状态(active/expired/suspended)
- `jwt_token`: JWT Token(24h有效期,登录后返回)
- `dashboard_summary`: 仪表盘聚合数据(素材数/报告数/今日发布/配额使用)

错误响应示例:
```json
{
  "success": false,
  "data": {},
  "error": "认证失败:密码错误",
  "code": "AUTH_002"
}
```

> 完整输出JSON格式+17个错误码详见 scripts/agency_portal_reference.json

## 异常处理

| 关键异常 | 错误码 | 处理方式 |
|:---------|:-------|:---------|
| 认证失败(密码错/过期/暂停) | AUTH_001-005 | 重新登录或联系管理员 |
| 套餐/注册无效 | PLAN_001/REG_001-002 | 使用有效值或更换标识 |
| 租户/内容/反馈不存在 | TENANT_001/CONTENT_001-002/FEEDBACK_001-002 | 检查ID拼写 |
| 依赖MCP不可用 | MCP_001 | 降级返回部分数据，检查MCP Server状态 |

> 完整17个错误码详见 scripts/agency_portal_reference.json

## 示例

### 示例: 租户入驻+登录+查看仪表盘

1. portal_register(tenant_slug="xingchen-tech", username="xingchen", password="<YOUR_PASSWORD>", tenant_name="星辰科技", plan="standard")
2. portal_login(username="xingchen", password="<YOUR_PASSWORD>") → JWT Token
3. portal_get_dashboard(token="abc123...") → 套餐专业版/订阅活跃/素材0/今日发布0

> 更多示例(管理员巡检/内容审批)详见 scripts/agency_portal_reference.json

## 三省六部归口

| 归口 | 部门 | 职责 |
|:-----|:-----|:-----|
| 租户入驻/巡检/反馈 | 吏部(libu_hr) | 客户关系管理+门户操作 |
| 套餐变更/续费/到期 | 吏部(libu_hr)执行+户部(hubu_finance)审批 | 吏部操作MCP+户部核算定价 |
| 内容审批 | 礼部(libu_content) | 内容发布审核 |

## 变更历史

| 版本 | 日期 | 变更内容 |
|:-----|:-----|:---------|
| v1.7 | 2026-07-11 | 工具数68→187(@mcp.tool实测),同步199个HTTP handler,修正SKILL.md工具数与实际不符(#20修复) |
| v1.6 | 2026-06-11 | 工具数47→68,新增数字人3个+充值3个+品牌2个+数据统计3个+竞品3个+发布记录2个+余额3个+对账1个,修复SKILL.md工具数不一致 |
| v1.5 | 2026-05-31 | 工具数36→47,新增平台绑定/配额/计费/退款/支付/账单工作流,修复RLS安全 |
| v1.4 | 2026-05-14 | 新增CP-18/19/20，管理员侧新增3个工具 |
| v1.0 | 2026-05-06 | 初始版本 |
