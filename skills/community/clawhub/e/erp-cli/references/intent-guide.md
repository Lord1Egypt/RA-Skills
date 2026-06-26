# 意图路由指南

当用户请求难以判断归属哪个模块时，参考本指南。

## 易混淆场景快速对照表

| 用户说... | 真实意图 | 应该用 | 不要用 | 理由 |
|-----------|---------|--------|--------|------|
| "查一下工单" / "我的工单" / "我有什么工单" | 我的待办工单列表 | `workorder +list` | — | 默认查我的待办（未处理的） |
| "看看我所有工单" / "我经办的工单" / "我处理过的工单" | 我经办过的工单（含历史） | `workorder +handle-list` | `workorder +list` | +list 是当前待办，不含已完成 |
| "查工单总览" | 全集团工单总览 | `api POST /workorder/master/getAllList` | `workorder +list` | 需有总览权限，看全部工单 |
| "5栋水管漏了，建个工单" | 创建报修工单 | `workorder +create` | — | 先确认项目、类型、紧急程度 |
| "分派工单123给张三" | 分派工单 | 先 `workorder +search-user --nick-name 张三` 拿 userId → `workorder +apportion` | — | 需先拿到 userId 和 nickName 拼成 `--assignees userId:nickName` |
| "这个工单什么情况" / "工单详情" / "处理记录" | 查工单详情含处理记录 | `workorder +info --id <id> --dept-id <deptId>` | `workorder +list` | 已知编号需先 `+list` 拿 id 和 deptId |
| "有多少待办工单" | 各状态数量统计 | `api POST /workorder/master/myTaskCount` | `workorder +list` | 只要数量不要列表 |
| "登录" | Device Flow 登录 | `--as <身份> auth login-start` + `--as <身份> auth login-wait` | — | 两步：先拿链接发给用户，再轮询等结果。`--as` 从企业微信 Sender ID 取 |
| "查看登录了谁" | 多用户列表 | `auth list` | — | 列出当前 profile 所有 namespace 的登录状态 |
| "切换到测试环境" | 切换 profile | `--profile <name>` | — | 配置已通过 config init --name 创建过 |

---

## 典型场景详解

### 1. 查工单的三种方式

**用 `workorder +list` 的场景**：
- "查我的待办" / "我的工单" / "我有什么工单" / "处理中的工单"
- 只看自己当前需要处理的（未结束）工单
- 默认行为，是查工单的首选命令

**用 `workorder +handle-list` 的场景**：
- "我经手过哪些工单" / "我处理过的工单" / "我经办的"
- 包含已完成、已关闭的历史记录（后端走 `work_order_hi_master_handling` 历史表）
- 用法：`erp-cli --as <身份> workorder +handle-list [--handle-status 0-5] [--page N]`

**用 `getAllList` 的场景**：
- "项目所有工单" / "工单总览" / "全公司的工单"
- 看不属于自己的工单，需要总览权限
- 走 api 兜底：`erp-cli --as <身份> api POST /workorder/master/getAllList --data '...'`

**判断关键**：
- 用户范围是"我" + 当前未处理 → `+list`
- 用户范围是"我" + 历史所有 → `+handle-list`
- 用户范围是"所有" → `getAllList`

---

### 2. 工单状态决定可用操作

工单是流程驱动的。当用户说"处理一下工单123"时，**不要直接执行 +complete**，先看工单当前状态：

```bash
# 1. 查工单详情（拿到 workOrderStatus 和后续操作必备字段）
erp-cli --as <身份> workorder +info --id 323407 --dept-id 301619

# 2. 看返回的 workOrderStatus 字段
#    "1" 待分派 → +apportion
#    "2" 待接单 → +take（待实现）
#    "3" 处理中 → +complete（待实现） 或 +follow（待实现）
#    "4" 待确认 → +confirm（待实现）
#    "5" 待回访 → +visit（待实现）
```

**判断关键**：状态决定能做什么操作，不要假设当前状态就是"处理中"。状态不对就直接告诉用户当前状态，不要尝试调用接口让后端报错。

---

### 3. 写操作必经的几个动作

任何写操作（+create / +apportion / +complete / +confirm 等）执行前都要：

1. **状态前置检查**：先 `+info` 确认 `workOrderStatus` 与目标操作匹配
2. **备注字段主动询问**：备注/说明类字段（如 `--remark`）执行前主动问用户"是否需要填写XX备注"
   - 用户说要填 → 用用户原话填
   - 用户说不填 / 不需要 / 没了 → 不传该字段
   - **不要自己编造备注内容**
3. **dry-run 预览**：`--dry-run` 看 method/path 都对了再正式发
4. **用户确认后执行**：把操作摘要给用户（操作类型 + 工单号 + 关键参数），用户明确同意后才去掉 dry-run

---

### 4. 写操作 code=204 流程（指定下一步处理人）

部分流程节点要求当前操作人指定下一步的处理人。后端通过 `code=204` 告知 CLI 需要再传一次参数：

```
第一次调用：+apportion --id ... --dept-id ... --current-task-id ... --work-order-class-id ... --work-order-class-name ...
   ↓
后端返回 code=204，msg=processBusinessId（如 "301063"）
   ↓
搜索处理人：+search-user --nick-name 张三
   ↓ 拿到 userId 和 nickName
重新调用：+apportion 同样参数 + --process-business-id 301063 --assignees 317713:张三
   ↓
后端返回 code=200，分派成功
```

**判断关键**：
- 不是所有工单的分派都需要指定处理人，**先不传 `--assignees` 试一次**
- 如果第一次返回 `code=200` → 完成，不需要二次提交
- 如果第一次返回 `code=204` → action=specify_handler，按 hint 二次提交

---

### 5. workorder 状态参数：直传后端字段值

CLI 的状态 flag **直接传后端字段值**，不做友好名映射。AI 根据用户口语，对照 `products/workorder.md` 的速查表选择数值。

**`+list`（我的待办）→ `--work-order-status`**：
- 用户说"我的待办 / 我的工单" → 不传（全部）
- 用户说"等我分派的 / 没派出去的" → `1`
- 用户说"等我接的 / 派给我还没接的" → `2`
- 用户说"处理中的 / 我正在做的" → `3`
- 用户说"等我确认的 / 待验收的" → `4`
- 用户说"待我回访的" → `5`

**`+handle-list`（我经办的）→ `--handle-status`**：
- 用户说"我经办的 / 我处理过的 / 历史工单" → 不传（全部）
- 用户说"我创建的 / 我报修的" → `0`
- 用户说"我分派出去的 / 我派单的" → `1`
- 用户说"我接过的 / 我接单的" → `2`
- 用户说"我做过的 / 我处理过的" → `3`
- 用户说"我确认过的 / 我验收过的" → `4`
- 用户说"我回访过的" → `5`

⚠️ **同样的数字，含义完全不同**：
- `+list --work-order-status 1` = 待分派的待办
- `+handle-list --handle-status 1` = 我分派过的经办
不要搞混两个 flag。

---

### 6. 登录的"两步"和身份隔离

**两步登录流程（AI Agent 必须使用）**：
- 用户说"登录" → 先 `--as <身份> auth login-start` 拿链接，再 `--as <身份> auth login-wait` 等结果
- 用户首次使用，还未登录 → 同上
- 用户说"切换账号" → 先 `--as <身份> auth logout` 再两步登录
- 用户说"查看登录了哪些账号" → `auth list`

**`--as` 身份来源**：
- 企业微信 / OpenClaw 场景：从消息上下文的 `Sender ID` 提取（如 `XingWenKai`）
- 本地 Claude Code 单人场景：用任意稳定标识，比如 `me`
- **`--as` 强制必传**，所有命令都必须带，CLI 否则直接拒绝
- 注意两步必须用相同的 `--as` 值

**Token 过期处理**：
- 业务命令返回 `{"ok":false,"error":{"type":"auth","code":3}}` 时说明 token 过期
- **CLI 不会自动登录**，必须由 AI 重新发起两步登录流程
- error.hint 字段会给出完整的重登录命令，照着执行即可

---

## 跨产品工作流路由

以下场景需要多个模块配合完成，注意上下文传递顺序。

### 创建工单（待实现 contact / project / dict）

用户说"5栋水管漏了，建个报修工单"：

```bash
# 1. 查用户所在的项目列表（待实现 project 模块）
# 2. 查工单类型字典（待实现 dict 模块）
# 3. 让用户确认项目、类型、紧急程度
# 4. 创建工单（dry-run 预览）
erp-cli --as <身份> workorder +create --dept-id <projectId> --class-id <typeId> \
  --content "5栋水管漏水" --level high --dry-run

# 5. 用户确认后真正创建
erp-cli --as <身份> workorder +create --dept-id <projectId> --class-id <typeId> \
  --content "5栋水管漏水" --level high
```

### 分派工单给指定人

用户说"把工单 GD202605201410000036 分派给张三"：

```bash
# 1. 从工单号反查 id 和 deptId（用 +list 或在已有上下文里找）
erp-cli --as me workorder +list

# 2. 查工单详情，确认状态=1(待分派) 并拿到 currentTaskId / workOrderClassId / workOrderClassName
erp-cli --as me workorder +info --id 323285 --dept-id 402632

# 3. 主动问用户：是否填写分派备注？

# 4. 先尝试不指定处理人分派（dry-run 后用户确认再执行）
erp-cli --as me workorder +apportion \
  --id 323285 --dept-id 402632 \
  --current-task-id 2056980870245388288 \
  --work-order-class-id 300679 --work-order-class-name 室内报修

# 5a. 如果返回 code=200 → 完成
# 5b. 如果返回 code=204 → 需要指定处理人，搜张三：
erp-cli --as me workorder +search-user --nick-name 张三
# → 拿到 userId 317819, nickName 张三

# 6. 二次提交带上 --process-business-id（msg 字段返回的值）和 --assignees
erp-cli --as me workorder +apportion \
  --id 323285 --dept-id 402632 \
  --current-task-id 2056980870245388288 \
  --work-order-class-id 300679 --work-order-class-name 室内报修 \
  --process-business-id 301063 \
  --assignees 317819:张三
```

**关键点**：
- 分派前先用 `+info` 看 `workOrderStatus` 必须是 `1`（待分派），不是就告诉用户当前状态
- 第一次先不传 `--assignees`，让后端决定是否需要指定处理人
- `--work-order-class-name` 必传，否则处理记录里"工单类型：null"
- 多人分派：`--assignees 317819:张三,300156:李四`

### 查工单含费用明细（待实现 charge）

用户说"工单323407花了多少钱"：

```bash
# 1. 查工单详情
erp-cli --as <身份> workorder +info --id 323407 --dept-id 301619

# 2. 查工单关联费用（待实现 charge 模块，目前走 api 兜底）
erp-cli --as <身份> api GET /workorder/master/getWorkOrderCharge?id=323407
```

**搜不到时不要猜，要问用户。** 例如用 `+search-user` 搜"张三"找到多个同名 → 把列表给用户让他选；搜不到 → 告诉用户"未找到此员工，请确认姓名或提供工号"。