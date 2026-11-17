# 错误码定义 - customer-crm

> 错误码来源：`skills/customer-crm/SKILL.md` 异常处理表。

## 错误码列表

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| CRM-ERR-01 | 客户ID(customer_id)为空 | 返回 VALUE_ERROR，跳过同步，提示提供 customer_id |
| CRM-ERR-02 | 来源类型未知 | 默认归类为 direct，记录 warning，不影响主流程 |
| CRM-ERR-03 | 租户状态文件不存在 | 创建新文件并初始化空 customer_sources，继续流程 |
| CRM-ERR-04 | 复购推荐无历史数据 | 返回空推荐列表，标记 new_customer |
| CRM-ERR-05 | daily-briefing 归因失败 | 跳过归因统计，不影响主同步流程 |
| CRM-ERR-06 | 复购触发写入失败 | 跳过复购触发，不影响主同步流程，记录 warning |
| CRM-SUCCESS-01 | 操作成功 | 正常返回 success=true 及 data |

## 错误码分类

| 分类 | 错误码 | 说明 |
|:-----|:-------|:-----|
| 参数校验类 | CRM-ERR-01, CRM-ERR-02 | 输入参数缺失或来源不可识别，采用默认值/拒绝策略 |
| 存储/IO 类 | CRM-ERR-03, CRM-ERR-06 | 租户状态文件或触发文件读写异常，自愈或跳过 |
| 业务降级类 | CRM-ERR-04, CRM-ERR-05 | 无历史数据或归因失败，返回空结果/跳过统计 |
| 成功 | CRM-SUCCESS-01 | 同步/查询/归因操作正常完成 |

## 处理原则

- 同步类异常（CRM-ERR-01/03/06）遵循 R-98 异步最终一致：不影响 xianyu-auto-reply 主流程。
- 归因/统计类异常（CRM-ERR-05）非阻断，仅记录 warning。
- 参数缺失（CRM-ERR-01）返回 VALUE_ERROR 并跳过同步；来源未知（CRM-ERR-02）降级为 direct。
- 所有错误返回统一结构：`{success:false, data:{}, error:"...", code:"CRM-ERR-XX"}`。

## 标准错误响应结构

```json
{
  "success": false,
  "data": {},
  "error": "customer_id 不能为空",
  "code": "CRM-ERR-01"
}
```

成功响应使用 `CRM-SUCCESS-01`，data 中包含 recorded/source/by_source/repurchase_recommendation 等字段（来源: SKILL.md§输出格式）。

## 异常与降级

| 异常场景 | 降级策略 |
|:---------|:---------|
| customer-crm 整体不可用 | xianyu-auto-reply 主流程继续，记录 warning 日志（R-98 异步最终一致） |
| 复购触发写入失败 | 跳过复购触发，主同步流程正常完成 |
| 租户状态文件不存在 | 创建新文件并初始化空 customer_sources |
