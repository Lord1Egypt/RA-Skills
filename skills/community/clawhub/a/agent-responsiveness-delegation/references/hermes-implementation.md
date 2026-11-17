# 示例实现（Hermes）· 「重活外派 + 随时应答」的落地细节

> **本页是「示例实现（Hermes）」一页，其他平台可以整页忽略。**
> `SKILL.md` 的规则与脚本是平台无关的；这一页只记录 **Hermes** 这一个平台在落地时的真实配置项、坑与验证口径，
> 供读源码级细节的人参考。换平台时，把下表的 Hermes 项按你平台的对应机制替换即可。

---

## 一、规则块写到哪（本页对应落地器的 Hermes 分支）

| 落点 | 路径 | 说明 |
|---|---|---|
| 主目录 SOUL | `<HERMES_HOME>/SOUL.md` | 主 Agent 的系统级人设/铁律文件，置顶写入 |
| 各 profile SOUL | `<HERMES_HOME>/profiles/<profile>/SOUL.md` | 每个 profile 各一份，**必须逐个写**（profile 的指令文件相互独立） |

配套模板示例（置顶铁律块的写法）：

```markdown
## ⚡ 重活外派 · 随时应答（作业纪律）· 最高优先

**角色定位：主脑 = 规划 · 统筹 · 验收 · 整合结论；执行一律下沉子代理。**

0. **先判级再动手（四级分流）**
   - L0 问答 → 直接答，不派，1 轮出结果。
   - L1 单步快活（≤1 次工具调用且 ≤20 秒）→ 直接干，不派。
   - L2 多步 / 长活 / 批量多条目 / 联网抓取 / 多文件 → 一律派子代理。
   - L3 需用户拍板（口径未定、涉及取舍/预算/对外承诺）→ 先回一句"这要您定 X"，不闷头干。
1. 重活一律出主脑：L2 全部派出去；主脑只做拆解、派活、验收、汇报。
2. 派完立刻收尾让出对话：回一句"已派出（谁在干什么）"后结束本回合；禁止干等。
3. 长命令不许堵主脑：>60 秒的命令用后台执行 + 完成通知。
4. 子代理只回收结论 + 产物路径；整合分析由主脑做。
5. 用户插话最高优先：先应一声，能答就答；答不了也必须先回。
6. 需要提问的活留在主脑（子代理问不了人）。
```

---

## 二、Hermes 侧的机制配置（真实键名）

Hermes 把「随时能插话 + 子代理并发」拆成三个配置面：

```yaml
# config.yaml
display:
  busy_input_mode: interrupt    # 忙碌期插话语义：立即重定向
  busy_ack_enabled: true        # 插话后回一个 ⚡ 回执

delegation:
  max_concurrent_children: 6    # 同时可跑的子代理数（上游默认 3，无硬上限；>10 只打成本告警日志）
  independent_completions: true # 每个子代理各自回报，不被最慢的拖住

agent:
  gateway_notify_interval: 30   # 长任务进度播报间隔（默认 180 太钝）
```

旧键 `max_concurrent` / `max_async_children` 已废弃，会被迁移折进 `max_concurrent_children`。
子代理模型由 `delegation.provider` / `delegation.model` 决定；不配则继承主脑（付费）。
**后台活对速度不敏感 → 子代理走低成本通道最划算**（主脑保持不被占用即可）。

### 插话模式：必须选 `interrupt`，别选 `steer`（实测）

- `interrupt`（**推荐**）：走「活跃轮重定向」——模型请求期**立即**取消该次请求、把纠正当成**真实用户消息**注入、循环重试（已完成的工作保留）；工具执行期请求前台命令 `yield` 转后台（**不杀活**）；**有子代理在跑时自动降级排队**以保护子代理不被级联取消。
- `steer`：把话附在「最后一条工具结果」上，**等这批工具跑完才送达**——主代理若在前台跑长命令（构建/抓取/轮询），会一直卡到命令退出。**不是"随时能插话"的选项。**
- `queue`：等整回合结束才被读到。
- 空闲时（重活已派出去、回合已结束）根本走不到 busy 逻辑 → 用户消息就是普通新回合，秒答。

### 生效时机

SOUL、display、delegation 都是**进程启动时读一次**，改完必须重启对应网关；改自己（当前 profile）时要用独立进程延迟重启，否则杀网关会中断当前回复。

---

## 三、坑（Hermes 实测）

- **环境变量优先于 config**：`HERMES_GATEWAY_BUSY_INPUT_MODE` 走 `_env_or_cfg_str()` = `env or cfg`，env 有值就压过 `config.yaml`；User/Machine 级没设才安全。网关用系统计划任务启动（干净环境），别从自己的 shell 里 `Popen` 直接拉（会继承 stale env）。
- 网关启动时会把 display 段的值 `_bridge_section_to_env` 写回 env → 计划任务启动 + config 有 key = 生效。
- `schtasks /End` 只终止任务实例的包装进程，**杀不掉真正的 python 子进程**（制造"假重启"）。
- **每个 profile 的 skills 目录是独立的**（default 在 `<HERMES_HOME>/skills`，成员在 `<HERMES_HOME>/profiles/<p>/skills`）→ 新技能要逐个复制，别只装一处。
- 子代理**不能**用 `clarify` / `delegate_task` / `memory` / `cronjob` —— 要问人、要建定时、要写长期记忆的活必须留在主脑。
- 同一个 profile 下 `<HERMES_HOME>/profiles/default/SOUL.md` 是残留件、**不被加载**（真身是根目录 `SOUL.md`），别改错文件，否则该块会在系统提示里出现两次。

---

## 四、验证口径（别人问"真生效了吗"时照着答）

1. 每个 SOUL 能 grep 到铁律标题、且位于文件前 1/3（置顶）。
2. 每个 config.yaml：`display.busy_input_mode`=interrupt、`busy_ack_enabled`=true、`delegation.max_concurrent_children`≥6、`independent_completions`=true（`yaml.safe_load` 通过）。
3. 各网关进程 CreationDate 晚于改动时间（别只看进程数）。
4. `hermes [-p X] prompt-size` 的系统提示字符数按新增块增长 → 证明 SOUL 真被加载。
5. 用户真插话一次 → 收到 ⚡ 回执且回复未被打断 = 端到端通过。

> 一句话：**纪律与脚本看 `SKILL.md`，Hermes 的机制与参数看这一页。**
