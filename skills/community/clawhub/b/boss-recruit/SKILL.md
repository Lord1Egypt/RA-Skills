---
name: boss-recruit
version: 1.0.0
description: BOSS直聘招聘助手。处理"新招呼"收件箱：读候选人在线简历同步飞书多维表格，有附件简历则零弹窗下载并同步，没附件则主动发消息要简历。内置反风控节奏层（随机延时/批量上限/验证码熔断/权益耗尽诊断/防发错人）。当用户提到 Boss直聘招聘、处理新招呼、候选人简历同步飞书、批量打招呼要简历时使用。
metadata:
  openclaw:
    requires:
      bins: [node, opencli]
---

# Boss 招聘助手 (boss-recruit)

把 Boss 招聘端的"新招呼收件箱"自动化：**读简历 → 同步飞书人才库 → 有附件下附件、没附件要简历**，全程走反风控节奏层模拟真人，避免封号。

> 路线：**OpenCLI 确定性命令（零 LLM 成本、快、稳）+ 反风控节奏层（确定性逻辑沉在代码里）**。不靠 LLM 即兴点页面。

## 何时使用

- 处理 Boss"新招呼/牛人发起"收件箱
- 候选人在线简历 / 附件简历同步到飞书多维表格
- 受控地主动给候选人发消息要附件简历

## 阻断式前置条件（缺一不可）

1. `opencli doctor` 全绿（daemon + Browser Bridge 扩展 + connectivity）
2. Chrome **当前活动标签页**是已登录的 **Boss 招聘端**页面（脚本 bind 当前 tab）
3. **已配置飞书目标表**（运行过 `setup.mjs`，见下）

不满足时**先停下来引导用户补齐**，不要硬跑。

## 配置飞书目标表（首次必做）

"同步到哪张表"**不硬编码**，由 setup 解析飞书链接并持久化到 `~/.opencli/boss-recruit/target.json`。两种后端：

| 后端 | 命令 | 适用 | 凭证 |
|------|------|------|------|
| **授权码 (base-api)** ⭐ | `node scenarios/setup.mjs <base链接> --token <pt-授权码>` | **可分发**给任意 HR | 多维表格「更多→高级权限→获取授权码」；**只认 /base/ 链接(个人端)，不支持 /wiki/(企业端)** |
| lark-cli (OAuth) | `node scenarios/setup.mjs <飞书链接>` | 本机自用 | 你已登录的 lark-cli |

> 授权码模式等价小良知聘后端的 `baseopensdk.BaseClient(app_token + personal_base_token)`，纯 HTTP 直连 `base-api.feishu.cn`，无 SDK 依赖。
> `node scenarios/setup.mjs --show` 查看当前配置。

## 三个场景（本版本已交付场景1）

| 场景 | 状态 | 入口 |
|------|------|------|
| ① 新招呼收件箱 | ✅ 已交付 | `scenarios/inbox.mjs` |
| ② 推荐列表主动打招呼 | ⏳ 规划中 | 复用底座 |
| ③ 搜索牛人按画像找人 | ⏳ 需先写"搜索牛人"适配器 | — |

## 运行场景1

```bash
node ~/.claude/skills/boss-recruit/scenarios/inbox.mjs            # 默认: 只读+同步全自动, 打招呼 DRY-RUN(只演示不真发)
node ~/.claude/skills/boss-recruit/scenarios/inbox.mjs --limit 5  # 单轮处理上限(默认5)
node ~/.claude/skills/boss-recruit/scenarios/inbox.mjs --live     # 🔴 真发要简历消息(对外动作!)
node ~/.claude/skills/boss-recruit/scenarios/inbox.mjs --force    # 重扫已处理候选人
```

### 安全模型（重要）

- **只读+同步默认全自动**：读简历、建/更飞书记录、下载附件——这些无对外副作用，直接跑。
- **打招呼默认 DRY-RUN**：要简历是**对外发消息、不可撤回**。默认只打印将发送的话术，不真发。
  - 确认话术和节奏没问题后，才加 `--live` 真发。
  - **首次 `--live` 务必小批量**（`--limit 2~3`）盯着跑。
- 触发验证码/登录失效/频控/权益耗尽 → **自动熔断暂停**，保留进度。

## 架构

```
config.mjs              字段映射/话术模板/节奏参数
lib/
  rhythm.mjs            反风控节奏层: 随机延时/拟人点击打字/风控熔断/三次身份校验/批量控制器/暂停态
  task-memory.mjs       状态机+记忆: 未读优先/去重/断点续跑 (~/.opencli/boss-recruit/task-memory.json)
  target.mjs            飞书目标表解析/持久化（授权码 base-api 或 lark-cli）
  feishu.mjs            飞书同步 dispatch: 档案→人才表(幂等建/更)、附件PDF→简历附件字段
  feishu-base.mjs       授权码 base-api 后端（纯 HTTP，无 SDK 依赖）
scenarios/
  setup.mjs            首次配置飞书目标表
  inbox.mjs            场景1编排: recommend→去重→resume→同步→attachment→要简历→控节奏→汇报
adapters/boss/
  attachment.js        OpenCLI 适配器：零弹窗下载附件简历（需装到 ~/.opencli/clis/boss/）
references/
  anti-detection.md    反风控/拟人操作规范，所有"写"动作的硬约束
```

## 依赖的 OpenCLI 命令

- `opencli boss recommend` — 拉新招呼收件箱（`friend/greetRecSortList`）
- `opencli boss resume <uid>` — 读在线简历档案
- `opencli boss attachment <uid>` — **零弹窗**下载附件简历 PDF（本 skill 配套适配器，装在 `~/.opencli/clis/boss/attachment.js`）
- `opencli boss send <uid> <text>` — 发消息（仅 `--live` 时调用）

## 状态机

```
pending → resume_read → (有附件) attachment_received → synced
                      → (无附件) attachment_requested → (候选人发来) → synced
                      → resume_read_failed (下轮优先补读)
                      → rejected
异常暂停: paused_for_{risk_signal, boss_contact_quota_exhausted, wrong_candidate_thread, switch_thread, send_message, ...}
```

## 反风控要点（详见 references/anti-detection.md）

1. 单轮 ≤ 5 人，相邻动作**随机 25~70s**（非固定）
2. 每 3 人做一次风控/状态校验
3. **连续 3 次打招呼失败 → 优先判定当日沟通权益耗尽**（不是 selector 问题）
4. 发消息前**三次身份校验**防发错人；一人一事务
5. 原生 CDP 点击 + 逐字输入，不用 DOM `.click()` / 瞬时填充
6. 验证码/登录失效/频控 → 立即熔断停整轮
