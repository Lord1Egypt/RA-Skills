---
name: cookie-manager
description: Cookie统一管理器,合并保活+紧急修复+健康检查三合一。功能:1.定时HTTP保活所有平台Cookie(闲鱼/抖音/快手/小红书/B站等13平台) 2.健康度评分0-100+健康度<60触发保活+3次连续失败写tenant_notification 3.4端Cookie同步检查与自动修复(fishclaw JSON/.env/global_config.yml/auto-reply API) 4.批量失效(≥2个)启动降级运营模式+备用Cookie自动切换+扫码恢复 5.多租户Cookie恢复SOP(备份恢复→备用切换→紧急告警三级降级)。触发:Cookie保活/Cookie检查/定时保活/Cookie过期告警/Cookie同步/Cookie批量失效/Cookie降级/cookie-keepalive-cycle/cookie-refresh/多租户Cookie恢复
version: 3.0.0
tools: [read, exec]
dependencies: []
metadata:
  layer: infrastructure
  priority: P0
  category: ecom-ops
  openclaw:
    emoji: "🍪"
    color: "#8e44ad"
    vibe: "professional"
    os: ["win32", "linux", "darwin"]
    exec_scripts:
      - cookie_keeper.py
      - keepalive.py
      - cookie_keepalive.py
      - cookie_emergency_manager.py
      - tenant_cookie_recovery.py
    requires:
      bins: ["python"]
      env:
        - SILICONFLOW_API_KEY
        - XIANYU_COOKIE_1
        - PG_DSN
        - COOKIE_ENCRYPTION_KEY
      config:
        - mcp.servers.fishclaw-mcp
---

> **核心功能**: 本技能提供+健康检查三合一等能力。


# Cookie统一管理器 v3.0

**合并来源**: cookie-keeper v2.0 + cookie-keepalive-service v1.0 + cookie-emergency v1.0
**优先级**: P0 | **所属层**: 基础设施层(Cookie健康)
**存储路径统一**: data/content/cookies/{tenant_id}/{platform}_{account}.json

## 使用场景

1. Cron定时保活: 每2天自动检查+保活所有闲鱼Cookie(来源:P1-14保活频率优化)
2. 多平台健康度扫描: 每6小时扫描所有租户13平台Cookie健康度(0-100)
3. Cookie过期告警: Cookie失效或即将过期时QQBot推送管理员
4. 4端Cookie同步: 检查fishclaw-mcp JSON/.env/global_config.yml/auto-reply API四端一致性
5. Cookie批量失效应急: ≥2个Cookie同时失效时启动降级运营模式
6. 多租户Cookie恢复: 备份恢复→备用切换→紧急告警三级降级策略(DEF-66)

## 工作流

### 步骤1: Cookie保活(主流程)

1. 接收保活请求(mode=keep_alive|check|force_refresh|sync)
   - 验证: mode参数为keep_alive/check/force_refresh/sync之一,默认keep_alive
   - 执行: `python skills/cookie-manager/scripts/cookie_keeper.py --mode {mode} --tenant_id {tenant_id}`

2. HTTP轻量检查+保活所有Cookie
   - 从fishclaw-mcp JSON文件读取Cookie(权威源,统一路径data/content/cookies/)
   - 对每个Cookie发送HTTP GET到目标平台验证有效性
   - 有效Cookie的HTTP访问本身即为保活(来源:HTTP请求刷新服务端会话)
   - 多账号间隔≥17分钟(来源:01手册§十10.1风控安全线)

3. 按检查结果分级处理
   - Cookie有效且age<5天: 记录健康状态,无需操作
   - Cookie有效但age≥5天: 发出WARNING告警,建议续期(来源:P1-14 5天安全线)
   - Cookie有效但age≥25天: 发出CRITICAL告警,需立即续期
   - Cookie失效: 发出CRITICAL告警,通知管理员扫码

4. 4端Cookie同步检查(Cookie有效时)
   - 以fishclaw-mcp JSON为权威源,通过unb字段比对其他3端一致性
   - 发现不同步时自动执行同步: 将fishclaw-mcp的Cookie分发到其他3端
   - 同步结果记录到告警日志

5. 同步token_manager状态
   - 调用fishclaw-mcp check_cookie_validity获取Playwright深度检查结果
   - 将结果同步到auto_ops token_manager.update()

6. 多平台健康度扫描(keepalive模式)
   - 执行: `python skills/cookie-manager/scripts/keepalive.py --tenant {tenant_id}`
   - 扫描data/content/cookies/目录所有租户Cookie文件
   - 健康度评分: 年龄>7天扣(age-7)*5(最多扣30)+HTTP失效扣50
   - 健康度<60触发HTTP保活访问,3次连续失败写tenant_notification
   - 每次访问写cookie_access_audit审计表

7. 输出保活报告
   - 格式: {success:bool, data:{total, valid, invalid, alerts_sent, sync_status, health_details}, error, code}

### 步骤2: Cookie紧急修复(批量失效应急)

1. 触发检测
   - 接收失效事件: {failed_cookies, total_cookies, backup_available}
   - 验证触发条件: failed_cookies数量≥2(CRITICAL级别)
   - 单个Cookie失效→交由步骤1常规处理,不启动应急
   - 执行: `python skills/cookie-manager/scripts/cookie_emergency_manager.py --mode detect --failed-cookies '{json}' --total-cookies {N}`

2. 立即启动降级运营模式
   - 暂停所有Cron发布任务(matrix-publish/xianyu-manager)
   - 暂停auto-delivery自动发货(切换为手动确认模式)
   - 保留xianyu-auto-reply客服功能(仅回复不触发发货,使用降级模板"系统维护中,稍后回复您")
   - 记录降级开始时间到data/auto_ops/degraded_mode.json
   - 来源:01手册§十风控安全线

3. 发送紧急告警
   - 通过QQBot+微信Channel双通道发送CRITICAL告警
   - 告警模板: "Cookie批量失效: {N}个账号Cookie失效,已启动降级运营模式"
   - 执行: `python d:/JueJin/scripts/notification.py send_alert --level CRITICAL --message "告警内容"`

4. 尝试自动恢复
   - 检查.env中是否有备用Cookie(XIANYU_COOKIE_2/3/4/5)
   - 如有备用Cookie→验证有效性→自动切换(间隔≥17分钟,来源:01手册§十10.1)
   - 如无备用Cookie→通知董事长扫码恢复
   - 执行: `python skills/cookie-manager/scripts/cookie_emergency_manager.py --mode recover --account-id {id}`

5. 扫码恢复后处理
   - 验证新Cookie有效性,同步到4端(逐端同步,失败重试3次)
   - 恢复后首次操作延迟≥5分钟(确保Cookie稳定)
   - 逐步恢复Cron任务: 先恢复xianyu-manager,再恢复matrix-publish
   - 恢复auto-delivery自动发货模式
   - 执行: `python skills/cookie-manager/scripts/cookie_emergency_manager.py --mode exit`

6. 多租户Cookie恢复SOP(DEF-66)
   - 三级降级策略: 备份恢复→备用Cookie切换→触发紧急告警
   - 执行: `python skills/cookie-manager/scripts/tenant_cookie_recovery.py --auto`
   - 恢复结果记录到data/openclaw/recovery_log.jsonl

### 步骤3: Cookie健康检查

1. 单账号检查(mode=check)
   - 执行: `python skills/cookie-manager/scripts/cookie_keeper.py --mode check --tenant_id {tenant_id}`
   - 仅检查不发送告警,返回状态JSON

2. 4端同步检查(mode=sync)
   - 执行: `python skills/cookie-manager/scripts/cookie_keeper.py --mode sync --tenant_id {tenant_id}`
   - 检查fishclaw JSON/.env/global_config.yml/auto-reply API四端一致性
   - 发现不同步时自动修复

3. 降级模式状态查询
   - 执行: `python skills/cookie-manager/scripts/cookie_emergency_manager.py --mode status`
   - 返回当前降级模式状态+备用Cookie信息

4. 多租户状态检查
   - 执行: `python skills/cookie-manager/scripts/tenant_cookie_recovery.py --check-all`
   - 检查所有租户Cookie状态(healthy/expired/warning/missing)

## 输入格式

```json
{
  "mode": "keep_alive|check|force_refresh|sync|detect|degrade|recover|exit|status",
  "tenant_id": "",
  "account_index": 0,
  "failed_cookies": [],
  "total_cookies": 0
}
```

## 输出格式

```json
{
  "success": true,
  "data": {
    "total": 3,
    "valid": 2,
    "invalid": 1,
    "results": [{"account": "account_1", "valid": true, "age_days": 2.5, "status": "healthy"}],
    "alerts_sent": 1,
    "token_manager_synced": true,
    "next_check": "2026-07-22T09:00:00",
    "sync_status": {"env_file": {"unb_match": true}, "global_config": {"unb_match": true}},
    "health_details": [{"tenant_id": "T01", "platform": "xianyu", "health_score": 85.0}]
  },
  "error": null,
  "code": "COOKIE_MANAGER_OK"
}
```

## 异常处理

| 异常 | 处理 | code |
|:-----|:-----|:-----|
| 无Cookie配置 | 返回失败+提示配置.env | NO_COOKIE |
| httpx未安装 | 仅格式检查,告警提示安装 | HTTPX_NOT_INSTALLED |
| 网络超时 | 标记为TIMEOUT,下次重试 | TIMEOUT |
| fishclaw-mcp不可用 | 跳过深度检查,仅HTTP检查 | MCP_UNAVAILABLE |
| QQBot告警失败 | 降级为本地文件日志 | ALERT_FAILED |
| DB未连接 | 仍执行Cookie检查+保活,跳过审计写入 | DB_NOT_CONNECTED |
| 备用Cookie也失效 | 全部暂停+紧急CRITICAL告警 | BACKUP_FAILED |
| 4端同步失败 | 逐端重试3次,记录失败端 | SYNC_PARTIAL_FAILED |
| 降级模式启动失败 | 记录错误+发送ERROR告警+人工介入 | DEGRADE_FAILED |
| Cookie切换触发风控 | 立即停止切换+等待≥17分钟后重试 | RATE_LIMITED |
| Fernet解密失败 | 跳过该Cookie,记录审计 | DECRYPT_FAILED |

## 风控规则

| 规则 | 阈值 | 来源 |
|:-----|:-----|:-----|
| 多账号操作间隔 | ≥17分钟 | 01手册§十10.1 |
| Cookie年龄WARNING阈值 | 5天 | P1-14优化 |
| Cookie年龄CRITICAL阈值 | 25天 | 业务连续性保障 |
| 保活频率 | 每2天 | P1-14优化(原3天) |
| 健康度保活阈值 | <60触发 | v4.0设计文档§3.7.6 |
| 连续失败告警阈值 | ≥3次 | tenant_notification WARNING |
| 降级模式期间 | 仅保留客服回复,暂停发布/擦亮/发货 | 01手册§十风控安全线 |
| 恢复后首次操作延迟 | ≥5分钟 | 确保Cookie稳定 |

## 示例

### 示例1: Cron定时保活

```
触发: Cron每2天执行
输入: {mode: "keep_alive", tenant_id: ""}
执行: python skills/cookie-manager/scripts/cookie_keeper.py --mode keep_alive
结果: 检查3个Cookie,2个有效1个失效,发送1条CRITICAL告警,同步token_manager,4端同步检查
```

### 示例2: Cookie批量失效应急

```
触发: 检测到2个Cookie同时失效
执行:
  1. cookie_emergency_manager.py --mode detect --failed-cookies '[{...},{...}]' --total-cookies 3
  2. 启动降级运营模式,暂停Cron发布+自动发货
  3. 发送CRITICAL告警
  4. cookie_emergency_manager.py --mode recover --account-id account_1 (切换备用Cookie)
  5. 董事长扫码恢复account_2
  6. cookie_emergency_manager.py --mode exit (退出降级模式)
结果: 降级2小时后恢复,备用Cookie切换1个,扫码恢复1个
```

## R72.1保护声明

本Skill实现R72.1: Cookie保活(健康度评分+主动/被动刷新)不可删除。
复用cookie_manager统一入口(R18合规),不创建新PG表。
