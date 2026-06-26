---
name: ci-package-deploy-notify
version: 1.0.7
description: "仅当用户明确要求触发 Jenkins 打包/部署，并在成功后发送飞书部署提醒时使用。适用于用户明确点名要打包某些服务、选择环境或分支、等待构建完成后通知部署的场景。模型只负责决定参数，实际执行必须调用本 skill 自带脚本。"
metadata:
  requires:
    bins: ["python3"]
---

# ci-package-deploy-notify

把“触发打包/部署 + 成功后发飞书通知”的流程交给固定脚本处理；**不要让模型自己临时拼 Jenkins 或飞书请求**。

## 何时使用

**只有当用户明确要求“现在触发打包 / 触发部署 / 发部署提醒”时才使用。**

当用户表达这些意图时使用：
- 明确要求触发某些服务打包
- 明确要求触发 Jenkins CI / CI/CD
- 明确要求打包完成后发部署提醒
- 明确要求构建完成后发打包通知
- 明确要求**打包并部署 / 直接部署**
- 明确指定环境、服务、改动说明，并要求通知 SQA / 部署群

以下情况**不要触发本 skill**：
- 只是讨论发版方案、发布时间、部署流程
- 只是查询构建状态 / Jenkins 状态 / 是否发过版
- 只是记录发版信息到文档 / 表格 / sheet
- 只是提到“发布/部署/发版”这些词，但没有明确要求“现在执行”
- 只是询问“能不能打包/能不能部署/这个 skill 是干什么的”

## 模型职责

模型只做这些事：
1. 先判断用户是不是在**明确要求立即执行**；不是的话不要触发
2. 提取服务/仓库列表
3. 判断环境或分支（如 dev / test / demo / sit）
4. 判断 job 类型（ci / cd）
5. 提取改动说明 `changes`
6. 如有需要，决定要 @ 的同事名
7. **根据用户意图选择执行链路**：
   - 用户说“打包通知部署 / 打包后通知测试部署” → 走 `ci`
   - 用户说“打包并部署 / 直接部署” → 默认走 `cd`，即 **复用 CI job + `AUTO_CD=true`**
   - 只有在用户明确要求“**单独部署**”时，才走独立 CD job
8. **将当前会话里真实发起人的 Feishu 标识透传给脚本**：优先使用当前消息发送者的 `open_id`（通常就是会话元数据里的 `sender_id` / `open_id`），拿不到时才回退 `user_id` 或配置里的默认发起人
9. 调用固定脚本
10. 回报结果或错误

模型**不要**：
- 自己调用 Jenkins API
- 自己构造飞书卡片
- 自己重写等待/轮询逻辑
- 在回复里暴露 token / webhook / secret

## 执行方式

脚本路径：`scripts/ci_package_deploy_notify.py`

基础调用：

```bash
python3 <skill_dir>/scripts/ci_package_deploy_notify.py \
  --repos cloud-mall cloud-device \
  --branch test \
  --changes "修复支付回调" \
  --initiator-id "ou_xxx" \
  --initiator-name "张三"
```

触发 CI/CD：

```bash
python3 <skill_dir>/scripts/ci_package_deploy_notify.py \
  --repos cloud-mall \
  --branch demo \
  --job-type cd \
  --changes "联调完成" \
  --initiator-id "ou_xxx" \
  --initiator-name "张三"
```

说明：
- `job-type=ci` 时：**只触发 CI**，成功后发送 **打包通知** 卡片，语义是“已经打包完成，请按需部署”
- `job-type=cd` 时：**默认复用 CI job，并通过 `AUTO_CD=true` 继续部署**，成功后发送 **部署通知** 卡片
- CD 触发方式支持两种：
  - **默认模式**：复用 CI job，通过 `AUTO_CD=true` 继续部署
  - **单独部署模式**：仅在明确需要“单独部署”时，才使用独立 CD job，并通过 `PROJECTS` 等参数选择服务
- 两种卡片都会带上服务、环境/分支、改动说明、发起人、SQA 信息

指定 @ 成员：

```bash
python3 <skill_dir>/scripts/ci_package_deploy_notify.py \
  --repos cloud-mall cloud-device \
  --branch test \
  --changes "发布完成" \
  --at Felix,Zack \
  --initiator-id "ou_xxx" \
  --initiator-name "张三"
```

## 参数整理规则

- `--repos`：优先使用 config.json 里的仓库键名；若配置了 `service_aliases`，也可使用其中的兼容名。像 `dl-admin` 这类独立服务，应该在 `repos` 中单独配置，**不要误配成其他服务别名**
- `--branch`：优先由用户明确指定；当前 skill 只支持 `dev / test / demo / sit`，不支持 `prod / master`
- `--job-type`：默认 `ci`
  - 用户说“打包通知部署 / 打包后通知测试部署”时，用 `ci`
  - 用户说“打包并部署 / 直接部署”时，用 `cd`
- 当前默认 CD 走 **`AUTO_CD=true`** 这条链路；只有用户明确要求“单独部署”时，才切到独立 CD job。不要让模型自己拼 job 参数
- `--changes`：必须提供；若用户没说，先追问一次
- `--at`：可选，多个名字用逗号分隔；脚本会优先精确匹配，再做包含匹配和模糊匹配，尽量容忍拼写不准，但如果同时匹配到多个候选会直接报错要求明确
- `--initiator-id`：**默认传当前消息发送者的 `open_id`**；在 Feishu 会话里，优先取会话元数据中的 `sender_id` / `open_id`，只有拿不到时才退回 `user_id`
- `--initiator-name`：可选；如果会话里拿不到可读姓名，可以不传，不要为了补名字阻塞执行
- 若未传 `--initiator-id`，脚本才会回退到配置中的默认发起人；因此正常调用时应始终透传当前真实发起人的 open_id
- 若用户只是“咨询能不能做”或“问怎么打包”，不要自行补参数后直接执行
- 若缺少 `repos / branch / changes` 中任一关键参数，先追问，不要半猜测执行

## 输出说明

脚本会按顺序执行：
1. 触发前先检查 Jenkins 队列 / 正在运行的同 job、同分支、同 job_type 任务
2. 若已存在相同参数任务，则跳过重复触发并直接等待现有任务完成
3. 否则触发 Jenkins job
4. 轮询 Jenkins 队列/构建状态
5. 全部成功后发送飞书部署提醒
6. 输出最终结果

成功时重点汇报：
- 哪些服务触发成功
- 是否命中“重复触发防重”并复用已有 queue/build
- CI 是否完成
- 若用户要求部署，**AUTO_CD 链路是否完成**；若明确走单独部署场景，再看独立 CD job 是否完成
- 飞书通知是否已发送
- 当前发送的是**打包通知**还是**部署通知**
- 卡片中是否带上了环境/分支信息
- **发起人是否使用了当前消息发送者的 open_id**
- SQA 是否命中模糊匹配；若匹配不明确，需直接报错并要求明确名字
- 若未拿到当前消息发送者 open_id，是否回退到了默认发起人

失败时直接汇报失败服务和原因。
如果用户给了 `prod / master`，应直接报“当前 skill 不支持该环境”。

## 安全说明

- 凭据来自同目录 `config.json`
- 不要在聊天里复述 token / webhook / app secret / jenkins api_token

## 维护说明

- 当脚本或 `SKILL.md` 更新后，如需让其他有权限的 agent 也拿到同一版本，使用 `clawhub`/技能同步流程进行发布或同步，不要只改当前工作区副本后就默认其他 agent 已生效。
