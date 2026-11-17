---
name: device-operations
version: "1.0.0"
description: "多终端设备自动化与AI视觉理解引擎，支持Android(uiautomator2)设备控制、微信/闲鱼/抖音场景自动化、AutoGLM视觉理解、智能路由(规则/AI/混合)、规则引擎与自学习、多终端协同调度、9平台内容发布。触发: 设备操作/微信发消息/闲鱼发布/抖音发布/多平台内容分发/AI视觉分析/规则优化"
tools: [read, write, memory_search]
dependencies: []
metadata:
  layer: plugin
  priority: P0
  category: device-ops
  openclaw:
    emoji: "⚙️"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: ["SILICONFLOW_API_KEY"]
      config: ["mcp.servers.device-operations-mcp"]
---

> **核心功能**: 本技能提供/规则优化等能力。


# 多终端设备自动化与AI视觉理解引擎

Android设备控制，微信/闲鱼/抖音场景自动化，AutoGLM视觉理解，智能路由与规则自学习，9平台内容发布。

## 使用场景

1. 闲鱼App批量操作（发布/擦亮/管理）
2. 微信自动化（发消息/收红包/通知卖家）
3. 抖音视频发布与数据分析
4. 9平台内容分发（抖音/快手/小红书/B站/视频号/TikTok/百家号/抖音图文/批量发布）
5. AI视觉理解与屏幕分析（AutoGLM GLM-4.1V-9B）
6. 复杂社交场景理解（朋友圈/评论/信息流）
7. 自动规则生成与优化
8. 多终端协同任务调度

## 工作流

### 微信场景自动化
1. smart_execute(app:"wechat", action:"send_message", params:{contact, message})
2. 收红包: smart_execute(app:"wechat", action:"receive_redpacket", params:{timeout})
3. 失败→自动降级为AutoGLM视觉理解模式

### 闲鱼/抖音场景自动化
1. 闲鱼发布: smart_execute(app:"xianyu", action:"list_product", params:{title, price, description})
2. 抖音发布: smart_execute(app:"douyin", action:"post_video", params:{title, tags, video_path})
3. 失败→自动降级为AutoGLM视觉理解模式

### 多平台内容发布
1. 单平台: device_publish_to_{platform}(支持8个国内平台)
2. 批量: device_batch_publish(platforms[], video_path, title, content, images, agent_id, account)
3. 自动间隔10-40秒防封，PPS人设验证+标题差异化适配
4. 各平台标题长度自动适配(抖音≤100/快手≤200/小红书≤20/B站≤80/视频号≤1000/TikTok≤150/百家号≤30)

### Android设备基础操作
device_send_message / device_screenshot / device_tap / device_swipe / device_install_app / device_status / device_publish_moment / device_like

### 断点续传
device_batch_status(task_id?) / device_resume_batch(task_id, resume_from?)

### AutoGLM AI视觉理解
- autoglm_analyze: 截图分析(general/interaction/social)
- autoglm_explore: 探索未知APP UI结构
- autoglm_understand_scenario: 理解复杂社交场景(moments/comment/feed)
- autoglm_generate_rule: 基于操作轨迹生成新规则
- autoglm_handle_exception: 操作异常恢复建议
- autoglm_handle_error: AutoGLM自身运行时错误处理

### 智能路由与规则引擎
- smart_execute: 智能执行(force_mode: rule_based/autoglm/hybrid)
- get_router_stats / get_rule / list_rules / optimize_rules / get_rule_stats

### 自学习系统
- self_learning_record: 记录执行结果
- self_learning_analyze: 分析执行模式发现规律
- self_learning_report: 生成自学习报告

### 多终端协同调度
- multi_device_submit: 提交任务(priority: critical/high/normal/low/background)
- multi_device_schedule: 分配任务到最佳设备并执行
- multi_device_status: 查询设备状态和负载

## 异常处理

| 异常 | 错误码 | 处理 |
|:-----|:-------|:-----|
| 设备连接超时 | DEVICE_TIMEOUT | 重试3次，3次失败降级手动 |
| APP启动失败 | APP_START_FAILED | 检查Bundle ID，尝试重装 |
| 联系人未找到 | CONTACT_NOT_FOUND | AutoGLM视觉模式查找 |
| 发布被拦截 | PUBLISH_BLOCKED | 降低频率，间隔≥5秒重试 |
| AutoGLM分析失败 | AUTOGLM_ERROR | 降级为规则驱动模式 |
| 规则匹配失败 | RULE_NOT_FOUND | autoglm_generate_rule生成新规则 |
| 平台不支持 | UNSUPPORTED_PLATFORM | 跳过该平台 |
| Cookie过期 | COOKIE_EXPIRED | 重新登录获取新Cookie |

> 完整输入/输出JSON格式、所有MCP工具参数、3个示例详见 scripts/device_operations_reference.json

## 输入格式

```json
{
  "action": "smart_execute|device_publish_to_*|device_batch_publish|autoglm_analyze|multi_device_submit",
  "app": "wechat|xianyu|douyin|kuaishou|xiaohongshu|bilbili|videoaccount|tiktok|baijiahao",
  "action_type": "send_message|list_product|post_video|publish_moment|like",
  "params": {
    "contact": "联系人名称",
    "message": "消息内容",
    "title": "商品/视频标题",
    "price": 99.00,
    "description": "商品描述",
    "video_path": "data/videos/<参数>.mp4",
    "images": ["img1.jpg", "img2.jpg"],
    "tags": ["标签1", "标签2"],
    "account": "default|account_1"
  },
  "force_mode": "rule_based|autoglm|hybrid",
  "platforms": ["douyin", "kuaishou", "xiaohongshu"],
  "priority": "critical|high|normal|low|background"
}
```

字段说明:
- `action`: 操作类型(smart_execute智能执行/device_publish_to_{platform}单平台发布/device_batch_publish批量发布/autoglm_analyze视觉分析/multi_device_submit多终端任务)
- `app`: 目标APP(wechat微信/xianyu闲鱼/douyin抖音等9平台)
- `action_type`: 具体动作(send_message发消息/list_product发布商品/post_video发布视频等)
- `params`: 操作参数(contact联系人/message消息/title标题/price价格/video_path视频路径/images图片数组/tags标签数组)
- `force_mode`: 路由模式(rule_based规则/autoglm视觉/hybrid混合,默认hybrid)
- `platforms`: 批量发布平台列表(device_batch_publish使用)
- `priority`: 任务优先级(multi_device_submit使用,critical最高/background最低)

## 输出格式

```json
{
  "success": true,
  "data": {
    "action": "smart_execute",
    "app": "wechat",
    "action_type": "send_message",
    "executed_mode": "rule_based",
    "contact": "卖家A",
    "sent_time": "2026-05-14T10:30:00",
    "duration_ms": 1500,
    "screenshots": ["data/screenshots/exec_001_step1.png"],
    "batch_status": null,
    "router_stats": {
      "rule_hit": true,
      "autoglm_fallback": false,
      "retry_count": 0
    }
  },
  "error": null,
  "code": null
}
```

字段说明:
- `executed_mode`: 实际执行模式(rule_based规则命中/autoglm视觉降级)
- `duration_ms`: 执行耗时(毫秒)
- `screenshots`: 执行过程截图路径数组(用于审计追溯)
- `batch_status`: 批量发布状态(device_batch_publish返回,含各平台成功/失败列表)
- `router_stats`: 路由统计(rule_hit是否规则命中/autoglm_fallback是否视觉降级/retry_count重试次数)

## 示例

### 微信通知卖家（人工接管场景）

1. smart_execute(app:"wechat", action:"send_message", params:{contact:"卖家A", message:"买家张三咨询退款问题"})
2. 输出: `{success:true, data:{contact:"卖家A", sent_time:"2026-05-14T10:30:00"}}`

> 批量发布/AutoGLM分析示例详见 scripts/device_operations_reference.json

---

## 变更历史

| 版本 | 日期 | 变更说明 |
|:-----|:-----|:---------|
| v1.0 | 2026-04-05 | 初稿（基础功能:Android设备控制+微信/闲鱼/抖音自动化） |
| v2.0 | 2026-05-12 | 多终端协同+9平台内容发布+AutoGLM视觉理解 |
| v3.0 | 2026-05-21 | 熔断保护(10个发布工具@with_circuit_breaker)+智能路由(规则/AI/混合) |
| v4.0 | 2026-06-21 | BUG-280修复:device-operations-mcp/engines子目录9个文件从logging.getLogger迁移到db_logger统一入口(android_engine/autoglm_engine/autoglm_wechat_operator/autoglm_wechat_script_generator/autoglm_wechat_explorer/multi_device_manager/rule_engine/self_learning/social_upload_engine) |
| v4.1 | 2026-06-22 | BUG-320修复:4个文件残留logging.调用清理(autoglm_engine.py/autoglm_wechat_explorer.py/multi_device_manager.py/smart_router.py),将logging.error/warning/debug替换为logger.error/warning/dbg(使用已迁移的db_logger实例) |
| v4.2 | 2026-06-22 | BUG-321修复:model_monitor.py冗余_logger定义清理(line 57重复定义的_logger变量删除) |
