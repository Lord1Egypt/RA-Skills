---
name: biometric-confirm
description: 生物识别二次确认服务,敏感操作(暂停/终止/修改)强制指纹/Face ID验证,普通操作免验证。触发:敏感操作/生物识别/二次确认/指纹验证
tools:
  - Bash
dependencies: []
metadata:
  requires:
    bins: []
    env: []
    config: []
  layer: product
  priority: "P1"
  source: v8.0方案§4.2.11 PROD-11
---

# 生物识别二次确认服务

## 使用场景

用户执行敏感操作(暂停/终止/修改/删除/重置)时,Agent要求生物识别二次确认。普通操作(查看/列表/查询)无需验证。

## 工作流

1. 判断操作敏感性
   - 敏感操作: pause/terminate/modify/delete/reset
   - 普通操作: view/list/query/export

2. 普通操作直接放行
   - 返回: verified=True, sensitive=False

3. 敏感操作要求生物识别
   - 提示用户完成指纹/Face ID验证
   - 调用generate生成令牌: `python scripts/biometric_service.py generate --user-id {user_id} --type fingerprint`

4. 验证生物识别令牌
   - 执行: `python scripts/biometric_service.py verify --user-id {user_id} --operation {operation} --token {token}`
   - 令牌5分钟内有效

5. 验证通过执行操作
   - verified=True: 执行敏感操作
   - verified=False: 拒绝操作

## 输入格式

- user_id: 用户ID
- operation: 操作类型(pause/terminate/modify/view等)
- token: 生物识别令牌(敏感操作必需)

## 输出格式

```json
{
  "success": true,
  "data": {
    "verified": true,
    "operation": "terminate",
    "sensitive": true,
    "verification_method": "biometric",
    "expires_at": "2026-07-08T12:05:00"
  }
}
```

## 异常处理

- 敏感操作无令牌: 返回 BIOMETRIC_REQUIRED
- 令牌无效或过期: 返回 BIOMETRIC_INVALID
- 不支持的生物识别类型: 返回 INVALID_BIOMETRIC_TYPE

## 示例

用户说"终止任务task_123":
1. Agent识别terminate为敏感操作
2. Agent提示"请完成指纹验证"
3. 用户完成指纹验证,获得令牌
4. Agent调用verify验证令牌
5. 验证通过,执行终止操作

来源: v8.0方案§4.2.11 PROD-11 移动端干预生物识别保护
