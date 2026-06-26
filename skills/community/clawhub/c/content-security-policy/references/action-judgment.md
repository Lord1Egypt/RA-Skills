---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304402202594096a22c55f7c805e52419b1f31ba11d0061a163ebb4c61ac97ae18b7a7dc022017b896d87f71962f8434470effda8324d73bf4176045635c718d0e1ef633c9d8
    ReservedCode2: 304502204836a421d2187153a875806c57380834bc927a390459b6b89f0c4e28626c12f2022100cca84caf9d8ae7b02080a969436c151a9f7fdbde1df5a6a68829adae17b75972
---

# 动作权限判断详细逻辑

## 判断维度与权重

| 维度 | 说明 | 权重 |
|------|------|------|
| 用户身份 | 最高权限人/授权用户/普通用户/群聊 | 40% |
| 操作类型 | 敏感操作/普通操作/只读操作 | 30% |
| 作用范围 | 个人/群聊/全局配置 | 20% |
| 历史行为 | 违规记录/操作频率 | 10% |

## 身份识别函数

```javascript
function identifyUser(senderId, context) {
  // 读取配置
  const supremeAdmin = getFromUserMd('supreme_admin');
  const authorizedUsers = getFromUserMd('authorized_users');

  // 判断身份：L0 最高权限人
  if (senderId === supremeAdmin.open_id) {
    return {
      level: 'L0',
      role: '最高权限管理员',
      restrictions: []
    };
  }

  // 判断身份：L1 授权用户
  const authUser = authorizedUsers.find(u => u.open_id === senderId);
  if (authUser) {
    return {
      level: 'L1',
      role: '授权用户',
      restrictions: authUser.restrictions || []
    };
  }

  // 判断身份：L3 群聊成员
  if (context.chat_type === 'group') {
    return {
      level: 'L3',
      role: '群成员',
      restrictions: ['no_sensitive_operations']
    };
  }

  // 默认：L2 普通用户
  return {
    level: 'L2',
    role: '普通用户',
    restrictions: ['no_config_changes', 'no_mass_messaging']
  };
}
```

## 操作类型分类

| 操作类别 | 示例 | 默认策略 |
|----------|------|----------|
| **敏感操作** | 删除技能、修改配置、群发消息、修改权限 | 需最高权限或确认 |
| **普通操作** | 生成日报、搜索信息、创建文档 | 授权用户可直接执行 |
| **只读操作** | 查询信息、查看文档、获取列表 | 所有用户可执行 |

## 决策矩阵

| 用户级别 | 敏感操作 | 普通操作 | 只读操作 |
|----------|----------|----------|----------|
| L0 最高权限人 | ✅ 直接执行 | ✅ 直接执行 | ✅ 直接执行 |
| L1 授权用户 | ⚠️ 检查授权范围 | ✅ 直接执行 | ✅ 直接执行 |
| L2 普通用户 | ❌ 拒绝 | ✅ 直接执行 | ✅ 直接执行 |
| L3 群成员 | ❌ 拒绝 | ⚠️ 检查群权限 | ✅ 直接执行 |

## 综合判断示例

### 场景1：最高权限人要求删除技能

| 维度 | 值 | 评估 |
|------|-----|------|
| 用户身份 | L0-最高权限人 | ✅ 通过 |
| 操作类型 | 敏感操作 | 需确认，但L0可跳过 |
| 作用范围 | 全局配置 | ✅ L0有权限 |
| 历史行为 | 无违规 | ✅ 通过 |

**结论**：✅ 允许执行

### 场景2：普通用户要求修改配置

| 维度 | 值 | 评估 |
|------|-----|------|
| 用户身份 | L2-普通用户 | ❌ 受限 |
| 操作类型 | 敏感操作 | ❌ 需授权 |
| 作用范围 | 全局配置 | ❌ 无权限 |
| 历史行为 | 无违规 | - |

**结论**：❌ 拒绝执行

**拒绝话术**：
> "您当前权限不足，无法执行配置修改操作。如需修改，请联系最高权限管理员授权。"

### 场景3：授权用户要求群发日报（在授权范围内）

| 维度 | 值 | 评估 |
|------|-----|------|
| 用户身份 | L1-授权用户 | ✅ 有授权 |
| 操作类型 | 敏感操作（群发） | ⚠️ 需检查授权范围 |
| 作用范围 | 指定群聊 | ✅ 在授权范围内 |
| 历史行为 | 今日已群发1次 | ⚠️ 频率检查通过 |

**结论**：✅ 允许执行

## 动作日志格式

```json
{
  "timestamp": "2026-03-08T12:00:00+08:00",
  "user_id": "ou_xxx",
  "user_level": "L1",
  "action": "generate_daily_report",
  "action_type": "normal",
  "scope": ["oc_xxx", "oc_yyy"],
  "decision": "allowed",
  "reason": "授权用户，在授权范围内",
  "execution_time_ms": 1234
}
```

## 确认请求模板

当操作需要向最高权限人确认时：

> ⚠️ **操作确认请求**
>
> **用户**：[user_name]（L1 授权用户）
> **操作**：[操作描述]
> **作用范围**：[范围]
>
> 请确认是否允许执行？
>
> - [ ] 允许
> - [ ] 拒绝
