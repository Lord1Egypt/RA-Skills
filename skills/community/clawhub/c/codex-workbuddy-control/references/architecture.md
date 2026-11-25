# 架构与状态机

## 设计目标

用普通文件和纯标准库脚本完成跨应用协作，不依赖聊天窗口注入、运行中数据库、云模型或常驻任务。自动触发器可以更换，文件协议保持稳定。

## 角色

| 角色 | 负责 | 不负责 |
|---|---|---|
| Codex | 实现、自测、最终验收、合并、发布 | 代替 WorkBuddy 在验收包中自报独立结论 |
| WorkBuddy | 资料/报告/表格；WBV 只读复跑；WBC 隔离候选 | 修改 Codex 生产代码、修复验收失败、合并、发布 |
| 用户 | 授权数据外发、决定返工或发布 | 不被要求手工复制整段测试日志 |

## 目录

```text
<WB_BUS_HOME>/
├── bus.json
├── tasks/<ID>/任务包.md
├── queue/
│   ├── pending/<ID>.json
│   ├── claimed/<ID>.json
│   ├── completed/<ID>.json
│   └── failed/<ID>.json
├── candidates/<ID>.json
├── 待验证/<ID>.md
├── 已验证/<ID>.md
├── 返工/<ID>.md
└── shared/
    ├── 任务台账.md
    └── 复盘/YYYY-MM.md
```

路径都可由 CLI 参数或环境变量覆盖。发布包不得包含运行时生成的台账、回执或业务路径。

## 编号

| 前缀 | 含义 | 完成条件 |
|---|---|---|
| `WB-YYYYMMDD-NNN` | WorkBuddy 执行任务 | 交付物和回执存在，Codex 核对实际结果 |
| `WBV-YYYYMMDD-NNN` | Codex 交付的只读验收 | WorkBuddy 复跑并给出 `WB_PASS/WB_FAIL/WB_PARTIAL` |
| `WBC-YYYYMMDD-NNN` | WorkBuddy 直接做的隔离候选 | Codex 最终复跑并写 `验证结果.md` |

编号在一个总线根内全局唯一。`WB_FAIL` 后修复必须新建 `WBV-*`，不得复用或改写失败回执。

## 正向验收状态机

```text
Codex 自测 PASS
→ dispatch/verify 生成任务包与 SHA-256
→ queue: pending
→ claim
→ queue: claimed
→ WorkBuddy 逐条复跑
→ 写 回执包.md
→ complete
→ queue: completed
→ Codex 读取结论
   ├─ WB_PASS → 完成
   ├─ WB_FAIL → 修复后新建 WBV
   └─ WB_PARTIAL → 补缺口或交用户决定
```

WorkBuddy 的退出码和输出必须进入回执。Codex 的旧证据只用于定位，不替代复跑。无法安全复跑时只能 `WB_PARTIAL`。

## 反向候选状态机

```text
用户直接在 WorkBuddy 指派代码/Skill
→ WorkBuddy 只写隔离候选
→ 候选目录写 验证请求.md
→ 总线写 待验证/<编号>.md
→ 状态 WAITING_VERIFY
→ 用户回 Codex：“验收 <编号>”
→ Codex 检查差异并实际复跑
   ├─ PASS → 写 验证结果.md，入口移到 verified
   └─ FAIL → 写返工结果和返工入口
```

没有后台轮询。这样避免 WorkBuddy 反复唤醒 Codex、空烧 Token。

## 原子性

- 队列文件使用临时文件、`fsync` 和 `os.replace` 原子落盘。
- claim/complete 使用短时锁文件，避免两个 worker 同时领取同一任务。
- 锁只保护队列元数据，不执行任务内容，不调用模型。
- 每个完成动作要求实际回执存在；壳层失败与验收结论分开处理。

## WorkBuddy 未接入

自动触发器、Helper、launchd、GUI 权限都不是协议必需项。没有接入时：

1. 仍然 `dispatch` 或 `verify` 建包。
2. 人工把 `tasks/<ID>/任务包.md` 交给 WorkBuddy。
3. WorkBuddy 读包、写回执或验证请求。
4. 仍在原总线执行 `claim` 和 `complete`，保留同一台账与状态证据。

## 共享记录

- 台账：建包时登记 `QUEUED/WAITING_VERIFY`，完成时更新真实结果、回执和复盘入口。
- 复盘：按 `YYYY-MM.md` 追加一条，写目标、结果、证据、风险和后续动作。
- 两个工作区不合并；候选和回执通过文件路径引用，不复制原始资料。

## 低 Token 边界

- 空队列不启动任何模型。
- 自动触发器若存在，只做“文件检查 → 满足条件才唤醒”。
- 不恢复每小时 ACTIVE 自动轮询；不让 WorkBuddy 后台轮询 Codex。
- 本 Skill 不声称账单节省比例；只描述可观测的负载减少。
