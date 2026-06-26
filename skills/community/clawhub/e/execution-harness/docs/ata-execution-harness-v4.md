# Execution Harness: 用 17 个 Bash 脚本治好 Claude Code Agent 的 6 种"不靠谱"

"重构这 7 个文件。"

Agent 改完 2 个，回了一句"其余文件的修改方式类似"，然后停了。

`cargo build` 失败。Agent 用一模一样的参数重试了 12 次。容器里根本没装 cargo。

花了 20 轮讨论决定用 Redis。Context 压缩之后，agent 开始写 Memcached 的配置代码。

5 个 worker agent 同时改 `config.yaml`。Agent A 读文件，Agent B 写文件，Agent A 基于过期内容覆写——Agent B 的改动消失了。

tmux 里跑着 3 个 agent。其中一个触发 429 限速，屏幕上显示"Press Enter to retry"。没人按。30 分钟后那个 pane 还挂在那。

Agent 改完 TypeScript 文件直接 `git commit`。你 pull 下来，`tsc` 报了一屏类型错误。

这 6 个场景都是可预测的。不是模型不行，是执行层没人管。Execution Harness 就干这个——17 个 bash hook 脚本 + 21 个设计模式，对着 agent 翻车的 6 个方向一个一个堵。基于 Claude Code 的 hook 协议，不调模型，不是框架。就管执行层。

---

## TL;DR

- Hook 是确定性的，prompt 是概率性的。凡是能用 hook 做的事，用 prompt 做就是在赌运气。
- Agent 的 6 类翻车有固定模式：提前停、重试死循环、压缩失忆、文件冲突、限速挂死、提交烂代码。每一类都有对应的 bash 脚本堵上。
- 40 个 pattern 从 6 个源蒸馏而来，不是凭空设计。17 个脚本有 90 个 pytest 测试覆盖。
- 每个轴是独立的 Claude Code skill，可以只装一个轴解决一个问题，不用全套上。
- 所有阻止 agent 继续的机制都必须有安全阀。没有安全阀的 enforcement 会变成 trap——agent 卡死比提前退出更糟。

---

## Execution Harness 做了什么

在 agent 外面加一层 bash hook，把"prompt 说了 agent 不一定听"的规则变成"系统级拦截，绕不过去"。

40 个 pattern，6 个维度：

| 问题 | 对应轴 | 代表性 pattern |
|------|--------|---------------|
| 做一半就停了 | execution-loop | Ralph Stop hook 阻止提前退出 |
| 同一个错误重试 12 次 | tool-governance | 3 次提示 + 5 次 block |
| 压缩后忘了关键决策 | context-memory | Handoff 写磁盘，压缩删不掉 |
| 5 个 agent 改同一个文件 | multi-agent | File claim lock 防并发 |
| 限速后 tmux 挂死 | error-recovery | 脚本扫 tmux pane 自动发 Enter |
| 提交了编译不过的代码 | quality-verification | 每次编辑后自动跑 linter |

17 个 bash 脚本可以直接用，23 个 design pattern 提供思路。

---

## 6 个翻车场景

这 6 个场景都是真实遇到过的，不是假设。用 Claude Code 做稍微复杂一点的任务，大概率会撞上其中几个。

### 做了一半就停了

给 agent 一个跨 7 个文件的重构任务。改完 2 个，停了：

> 已完成重构，其余文件的修改方式类似。

5 个文件没动。你说"继续"，它再改 2 个又停。再"继续"，又 2 个。你变成了一台人肉"继续"按键。

不是偶发，而且第一次遇到的时候真的很恼火。改完 2 个文件，agent 觉得已经展示了"怎么改"，对它来说任务完成了。但你的 7 个文件是一个原子任务——改了 2 个不改剩下 5 个，不如一个都不改。

Interactive 模式下每次 `end_turn` 都是退出点。没有外力阻止，agent 会在每个"看起来差不多了"的节点停下来。Ralph Persistent Loop（Pattern 1.1）就是那个外力——Stop hook 在 agent 每次试图退出时拦住它。

### 同一个错误重试 12 次

容器里没装 `cargo`。

Agent 跑 `cargo build`。失败。"让我再试一次。" 又是 `cargo build`。失败。参数一字不改。到第 12 次的时候你已经盯着屏幕看了 5 分钟。

原因比你想的简单。`PostToolUseFailure` 只给 agent 看到这一次的错误。没有计数器告诉它"你用同样的方式失败了 12 次"。对 agent 来说每次都是全新的"再试试"。Tool Error Escalation（Pattern 2.1）加了这个计数器——连续 3 次开始提醒，5 次直接 block。

### 压缩后忘了关键决策

20 轮讨论，最终选了 Redis。理由充分：项目已有依赖，团队有运维经验，Memcached 被明确排除。

继续干活。Context window 用到 95%，Claude Code 触发 Full Compact。压缩后，agent 开始写 Memcached 的连接池配置。

"我们不是决定用 Redis 吗？"——"抱歉，让我切换到 Redis。"

但如果你没注意到呢？它可能基于 Memcached 写了 3 个文件，code review 时你才发现整个缓存层用错了方案。

压缩本身没错——context 是有限的。问题在于你控制不了它留什么丢什么。"用 Redis"这个结论可能留下了。但"为什么排除 Memcached"？丢了。推理既不是代码也不是结论，压缩算法眼里它就是可删的废话。

所以我们把决策写磁盘。Handoff Documents（Pattern 3.1）在阶段结束时把 Decided/Rejected/Risks 写进文件，压缩动不了它。

### 5 个 agent 编辑同一个文件

Coordinator 分派 5 个 worker 做不同子任务。看起来分工明确。但 3 个 worker 都需要改 `config.yaml`——一个加数据库配置，一个加缓存配置，一个加日志配置。

时间线：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">Lost Update 时间线</div>
<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
<div style="width:36px;text-align:right;font-size:12px;font-weight:600;color:#666">t=0</div>
<div style="flex:1;background:#eff6ff;border:1px solid #93c5fd;border-radius:6px;padding:8px 12px;font-size:12px">Agent A 读取 config.yaml（<b>版本 1</b>）</div>
</div>
<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
<div style="width:36px;text-align:right;font-size:12px;font-weight:600;color:#666">t=1</div>
<div style="flex:1;background:#faf5ff;border:1px solid #c4b5fd;border-radius:6px;padding:8px 12px;font-size:12px">Agent B 读取 config.yaml（<b>版本 1</b>）</div>
</div>
<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
<div style="width:36px;text-align:right;font-size:12px;font-weight:600;color:#666">t=2</div>
<div style="flex:1;background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:8px 12px;font-size:12px">Agent B 写入 config.yaml（<b>版本 2</b>：加了缓存配置）</div>
</div>
<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
<div style="width:36px;text-align:right;font-size:12px;font-weight:600;color:#dc2626">t=3</div>
<div style="flex:1;background:#fef2f2;border:2px solid #fca5a5;border-radius:6px;padding:8px 12px;font-size:12px"><b style="color:#dc2626">Agent A 写入 config.yaml（版本 1 + 数据库配置）→ Agent B 的缓存配置消失了</b></div>
</div>
<div style="display:flex;align-items:center;gap:10px">
<div style="width:36px;text-align:right;font-size:12px;font-weight:600;color:#666">t=4</div>
<div style="flex:1;background:#fefce8;border:1px solid #fde68a;border-radius:6px;padding:8px 12px;font-size:12px">Agent C 读取 config.yaml → 只看到数据库配置，以为没人配过缓存</div>
</div>
</div>

经典的 lost update。数据库领域有锁、MVCC、CAS，但 agent 之间共享的是裸文件系统——Read 读、Write 写，中间零并发控制。更隐蔽的是 agent 压根不知道其他 agent 存在。A 不知道 B 在改同一个文件，也不会检查。File Claim and Lock（Pattern 4.3）让 agent 在编辑前写一个 claim 标记，其他 agent 看到标记就等。

### 限速后 tmux 挂死

tmux 里 3 个 pane，3 个 agent 并发跑。常见场景。

一个 agent 撞上 429 限速：

```
⚠ Rate limited. Press Enter to retry...
```

在正常使用中，你按一下 Enter 就好了。但这是无人值守的 tmux session——可能是你开在 EC2 上跑过夜任务的那种。

没人按。那个 pane 就挂在那。30 分钟后你看了一眼，还在等。另外两个 agent 做完了，但它们依赖这个 agent 的输出，整条流水线停了。解法朴素到有点丢人——一个 cron 脚本每 30 秒扫一遍 tmux pane 的输出，看到 "Press Enter" 就发一个 Enter。但它确实管用。

### 提交了编译不过的代码

Agent 修改了一个 TypeScript 文件，改完后直接 `git commit`。`Write` 工具返回 success——文件确实写进去了。Agent 认为任务完成。

你 pull 下来跑 `tsc`：

```
src/handlers.ts:45:12 - error TS2345: Argument of type 'string' is not 
  assignable to parameter of type 'number'.
src/handlers.ts:67:8 - error TS2304: Cannot find name 'CacheConfig'.
```

两个类型错误。Agent 改了函数签名但没更新调用方，还引用了一个未导入的类型。

编辑和验证是分离的。Agent 写完文件不会自动跑 linter，commit 前也不会跑 `tsc`。`Write` 工具只管"文件写没写进去"，内容对不对它不管。

3 个互相依赖的文件，每个都有类型错误，错误级联放大。写的时候发现是 1 分钟的事，3 个文件之后回头修要半小时。Post-Edit Diagnostics（Pattern 6.1）用 PostToolUse hook 在每次编辑后自动跑 linter，错误通过 `additionalContext` 即时反馈给 agent。

---

## 10 条设计原则背后的 Tradeoff

不是 slogan。每一条背后都有一个具体的翻车场景。

### M1: Hook 是确定性的，Prompt 是概率性的

你在 CLAUDE.md 里写"不要重试超过 3 次"。大多数时候 agent 会遵守。但在压力下——比如它真的很想让 `cargo build` 跑通——它会"合理化"自己的行为："之前的 3 次是不同的上下文，这次是新的尝试"，然后继续重试。

你没法说它违反了指令——它确实给出了"理由"。Prompt 是建议，不是命令。Agent 有空间解释自己为什么没违规。

`PostToolUseFailure` hook 数到 5 直接返回 `{"decision":"deny"}`。Agent 绕不过去。这不是建议，是系统级拦截。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">Prompt vs Hook</div>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<div style="flex:1;min-width:250px;border-radius:8px;padding:14px;background:#fef2f2;border:1px solid #fca5a5">
<div style="font-size:11px;color:#dc2626;font-weight:700;letter-spacing:1px;margin-bottom:10px">PROMPT</div>
<div style="font-size:12px;color:#666;line-height:1.8">
执行保证：<b style="color:#dc2626">概率性</b><br>
绕过可能：Agent 可以"合理化"<br>
适用范围：复杂判断、软引导<br>
维护成本：低（改文本）
</div>
</div>
<div style="flex:1;min-width:250px;border-radius:8px;padding:14px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px;margin-bottom:10px">HOOK</div>
<div style="font-size:12px;color:#666;line-height:1.8">
执行保证：<b style="color:#16a34a">确定性</b><br>
绕过可能：无法绕过<br>
适用范围：简单规则、硬约束<br>
维护成本：中（改脚本）
</div>
</div>
</div>
</div>

不是说 prompt 没用。复杂判断（"这段代码需不需要重构"）只能靠 prompt。但"同一个工具同样参数失败超过 5 次就停"这种规则，用 prompt 做就是赌运气。

### M2: 文件系统是最好的通信介质

跨 agent、跨 session、跨 hook 的通信都走磁盘文件。不用数据库，不用消息队列。

Hook 是 bash 脚本。bash 读写文件是天生的。引入 Redis 意味着每个脚本都得装 `redis-cli`，部署变复杂，调试变困难。排查 hook 问题时 `cat` 看状态文件、`jq` 解析 JSON，30 秒搞定。状态在 Redis 里就得连上去 `HGETALL`，出了问题分不清是 hook 逻辑错了还是 Redis 连接断了。

JSON 文件 + 原子写入 + 每个 session 一个目录，够了。

```bash
# 原子写入——写完 tmp 再 rename，保证 crash 时不会留下半写的文件
jq '.iteration = 5' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
```

用 rename 是因为 `jq ... > file` 写到一半 kill 掉，你就有一个半截 JSON。rename 是原子的——要么整个文件更新，要么什么都没变。

代价：文件 I/O 比内存操作慢。5 个 agent 同时更新状态文件会有竞争。Pattern 4.3 File Claim and Lock 部分缓解，但不完美。真正的高并发场景（几十个 agent）可能需要升级到数据库——不过在 Execution Harness 的典型场景（2-5 个 agent，每秒几次状态更新）里，文件系统够用。

### M3: 每个 Enforcement 都必须有安全阀

Ralph 的 Stop hook 会阻止 agent 退出。听起来很好——不让它偷懒嘛。

但想象一下这个场景：agent 遇到了 401 认证错误。它没有权限访问某个 API，不管重试多少次都不会成功。Ralph 说"不许停"，agent 说"我做不了"。Ralph 继续说"不许停"。死循环。

所以 Ralph 有 5 个安全阀：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:16px">Ralph 的 5 个安全阀</div>
<div style="display:flex;gap:10px;flex-wrap:wrap">
<div style="flex:1;min-width:110px;border-radius:8px;padding:10px;background:#fef2f2;border:1px solid #fca5a5;text-align:center">
<div style="font-size:11px;color:#dc2626;font-weight:700;letter-spacing:1px;margin-bottom:4px">Context 溢出</div>
<div style="font-size:11px;color:#666">context >= 95%<br>必须放行，否则崩溃</div>
</div>
<div style="flex:1;min-width:110px;border-radius:8px;padding:10px;background:#fef2f2;border:1px solid #fca5a5;text-align:center">
<div style="font-size:11px;color:#dc2626;font-weight:700;letter-spacing:1px;margin-bottom:4px">认证失败</div>
<div style="font-size:11px;color:#666">401/403 → 停用 Ralph<br>立即放行</div>
</div>
<div style="flex:1;min-width:110px;border-radius:8px;padding:10px;background:#fefce8;border:1px solid #fde68a;text-align:center">
<div style="font-size:11px;color:#a16207;font-weight:700;letter-spacing:1px;margin-bottom:4px">CANCEL 信号</div>
<div style="font-size:11px;color:#666">用户创建 cancel 文件<br>放行 + 清理状态</div>
</div>
<div style="flex:1;min-width:110px;border-radius:8px;padding:10px;background:#eff6ff;border:1px solid #93c5fd;text-align:center">
<div style="font-size:11px;color:#3b82f6;font-weight:700;letter-spacing:1px;margin-bottom:4px">闲置超时</div>
<div style="font-size:11px;color:#666">2 小时无活动<br>放行 + 标记 stale</div>
</div>
<div style="flex:1;min-width:110px;border-radius:8px;padding:10px;background:#f0fdf4;border:1px solid #86efac;text-align:center">
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px;margin-bottom:4px">迭代上限</div>
<div style="font-size:11px;color:#666">达到 max_iterations<br>放行 + 标记完成</div>
</div>
</div>
</div>

推论：设计一个阻止机制，就必须同时设计它的失效条件。不然你造的不是护栏，是陷阱。

"那就设宽松一点，100 轮上限？"也不行。Agent 第 15 轮进入 compliance mode——表面继续工作，实际产出空洞——后面 85 轮纯浪费 token。安全阀的参数是经验值，没有万能数字。

### M4: Session 级别的隔离

一个 session 的状态不能泄漏到另一个。听着像废话，但实现中很容易出错。

错误示例：

```bash
# 所有 session 共用一个错误计数文件
STATE_FILE="tool-errors.json"  # ← bug: 没有 session_id
```

正确做法：

```bash
STATE_FILE="sessions/${SESSION_ID}/tool-errors.json"
```

Claude Code 可以同时跑多个 session。Session A 做前端，session B 跑测试。共用错误计数器的话，A 的 `npm build` 失败 3 次会影响 B 的计数，B 在调 npm 时被错误拦截。

所有状态文件路径都包含 `session_id`。不含的就是 bug。

跨 session 的信息传递只有两种合法方式：
1. Handoff 文档（3.1）——显式写入的阶段总结
2. Memory Consolidation（3.3）——有门控的记忆合并

### M5: 不确定就放行

状态文件不存在、JSON 解析失败、Session ID 拿不到、hook 的输入读不到——全部默认放行。

```bash
[ -f "$STATE_FILE" ] || { echo '{"continue":true}'; exit 0; }  # 无状态则放行
```

`echo '{"continue":true}'; exit 0` 是每个 hook 的第一行逻辑。Hook 出了问题不应该变成 agent 不能工作。

唯一例外：安全 guard。`tool-input-guard.sh` 检测 `rm -rf /`、`curl | sh` 时翻转为 fail-closed——宁可误拦。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:16px">Fail-Open vs Fail-Closed</div>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<div style="flex:3;min-width:250px;border-radius:8px;padding:14px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px;margin-bottom:8px">FAIL-OPEN（默认）</div>
<div style="font-size:12px;color:#666;line-height:1.8">
状态文件不存在 → 放行<br>
JSON 解析失败 → 放行<br>
Session ID 未知 → 放行
</div>
</div>
<div style="flex:2;min-width:180px;border-radius:8px;padding:14px;background:#fef2f2;border:2px solid #fca5a5">
<div style="font-size:11px;color:#dc2626;font-weight:700;letter-spacing:1px;margin-bottom:8px">FAIL-CLOSED（安全例外）</div>
<div style="font-size:12px;color:#666;line-height:1.8">
检测到 <code>rm -rf /</code> → 拦截<br>
检测到 <code>curl | sh</code> → 拦截
</div>
</div>
</div>
</div>

反直觉——安全机制大部分时候选择"不起作用"。但替代方案更差。Hook 拿不到状态文件就 block 的话，新环境第一次跑 Claude Code，session 目录还没建，所有 hook 全拦。体验就是"什么都干不了"。然后你卸了整套 hook。

### M6: 干预要和任务复杂度成正比

5 分钟改个 typo 不需要 Ralph、不需要 doubt gate、不需要 post-edit diagnostics。2 小时的跨 15 个文件的重构全都需要。

Pattern 1.3 Adaptive Complexity Triage 按任务复杂度自动选 harness 强度：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:16px">Harness 强度三档</div>
<div style="border-radius:8px;padding:12px;background:#f0fdf4;border:1px solid #86efac;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px">简单</span><span style="font-size:12px;color:#666"> — 改 typo、加注释</span></div>
<div style="display:flex;gap:4px"><span style="background:#dcfce7;border:1px solid #86efac;border-radius:6px;padding:2px 8px;font-size:11px">tool-input-guard</span></div>
</div>
</div>
<div style="border-radius:8px;padding:12px;background:#fefce8;border:1px solid #fde68a;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">
<div><span style="font-size:11px;color:#a16207;font-weight:700;letter-spacing:1px">中等</span><span style="font-size:12px;color:#666"> — 修 bug、加功能</span></div>
<div style="display:flex;gap:4px;flex-wrap:wrap"><span style="background:#fef3c7;border:1px solid #fde68a;border-radius:6px;padding:2px 8px;font-size:11px">+ post-edit-check</span><span style="background:#fef3c7;border:1px solid #fde68a;border-radius:6px;padding:2px 8px;font-size:11px">+ tool-error-tracker</span></div>
</div>
</div>
<div style="border-radius:8px;padding:12px;background:#fef2f2;border:1px solid #fca5a5">
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">
<div><span style="font-size:11px;color:#dc2626;font-weight:700;letter-spacing:1px">复杂</span><span style="font-size:12px;color:#666"> — 大重构、架构改动</span></div>
<div style="display:flex;gap:4px;flex-wrap:wrap"><span style="background:#fee2e2;border:1px solid #fca5a5;border-radius:6px;padding:2px 8px;font-size:11px">+ ralph</span><span style="background:#fee2e2;border:1px solid #fca5a5;border-radius:6px;padding:2px 8px;font-size:11px">+ doubt-gate</span><span style="background:#fee2e2;border:1px solid #fca5a5;border-radius:6px;padding:2px 8px;font-size:11px">+ drift-reanchor</span><span style="background:#fee2e2;border:1px solid #fca5a5;border-radius:6px;padding:2px 8px;font-size:11px">+ test-before-commit</span></div>
</div>
</div>
</div>

全部启用的代价：hook 有开销。改个 README 触发 `tsc` 类型检查，浪费时间。Ralph 在简单任务中更麻烦——agent 在"我改完了"和"hook 说不许停"之间拉扯几轮，最后憋出一些无意义的"额外改进"来满足要求。你以为在提质量，其实在消耗 token。

### M7: 先观测，再干预

先部署 `tool-error-tracker.sh`（PostToolUseFailure hook）记录失败次数，再部署 `tool-error-advisor.sh`（PreToolUse hook）阻止重试。顺序不能反。

只装 advisor 没装 tracker 会怎样——advisor 要读错误计数文件来决定是否 block，但没有 tracker 去写这个文件。Advisor 永远读到"文件不存在"，按 M5 放行，永远不触发 block。

这两个脚本构成一个 observe-then-intervene 配对：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">M7: Observe → Intervene</div>
<div style="border-radius:8px;padding:14px;background:#eff6ff;border:1px solid #93c5fd;margin-bottom:8px">
<div style="font-size:11px;color:#3b82f6;font-weight:700;letter-spacing:1px;margin-bottom:6px">OBSERVE</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
<span style="background:#dbeafe;border:1px solid #93c5fd;border-radius:6px;padding:4px 10px;font-size:12px">PostToolUseFailure</span>
<span style="color:#bbb">→</span>
<span style="background:#dbeafe;border:1px solid #93c5fd;border-radius:6px;padding:4px 10px;font-size:12px">tracker 记录错误</span>
<span style="color:#bbb">→</span>
<span style="background:#dbeafe;border:1px solid #93c5fd;border-radius:6px;padding:4px 10px;font-size:12px">写入 tool-errors.json</span>
</div>
</div>
<div style="text-align:center;color:#bbb;font-size:11px;margin:4px 0">↓ 数据流</div>
<div style="border-radius:8px;padding:14px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px;margin-bottom:6px">INTERVENE</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
<span style="background:#dcfce7;border:1px solid #86efac;border-radius:6px;padding:4px 10px;font-size:12px">PreToolUse</span>
<span style="color:#bbb">→</span>
<span style="background:#dcfce7;border:1px solid #86efac;border-radius:6px;padding:4px 10px;font-size:12px">advisor 读取错误</span>
<span style="color:#bbb">→</span>
<span style="background:#dcfce7;border:2px solid #86efac;border-radius:6px;padding:4px 10px;font-size:12px;font-weight:600;color:#16a34a">count >= 5? BLOCK</span>
</div>
</div>
</div>

更广义地说：想干预，先有数据。这也是为什么 6 个轴里 tool-governance（含 tracker）应该在 error-recovery（依赖 tracker 数据）之前装好。

### M8: 知识写磁盘，不信 LLM 摘要

"为什么选 Redis 不选 Memcached？"

如果这个决策存在 context 里，它会被压缩。压缩后可能只剩"使用 Redis 做缓存"，至于为什么排除 Memcached 的推理过程——没了。

Handoff 文档的 5 段式结构就是为了解决这个问题：

```markdown
# Handoff: cache-implementation

## Decided
- 选择 Redis 作为缓存方案（项目已有 Redis 依赖）
- LRU 策略，TTL 5 分钟

## Rejected
- 排除 Memcached：团队无运维经验
- 排除本地文件缓存：不支持多实例部署

## Risks
- Redis 单点故障需要 Sentinel（当前未配置）

## Files Modified
- src/cache/redis_client.py — 新建
- src/api/handlers.py:45-67 — 添加缓存查询层

## Remaining
- Sentinel 配置（下个迭代）
- 缓存预热逻辑
```

注意 **Rejected** 段。这是整个 handoff 中价值最高的部分。"选了什么"是结论，"排除了什么以及为什么"是推理。压缩会保留结论，但推理只有写进磁盘文件才能存活。

和内置压缩互补。内置压缩管"怎么高效用 context window"，handoff 管"什么东西不许丢"。

### M9: Coordinator 是大脑，不是邮局

Coordinator 从 worker 拿到 research 结果，然后说：

> "Based on your findings, fix the bug."

Research 的原始数据原封不动扔给了 implementation worker。没消化，没筛选，没判断。

邮局模式。Worker 在缺乏上下文的情况下干活，产出质量赌运气。它可能抓住 research 里某个不重要的细节大做文章，真正的关键发现反而被忽略。

Coordinator 应该消化 research 结果，写一份 synthesis：根因是什么、依据在哪、接下来改哪个文件。把 synthesis 交给 implementation worker，不是把原始数据扔过去。

多了一步，但这步就是 coordinator 存在的理由。跳过了，你就是在让一个没有全局视角的 worker 做决策。

### M10: 做不到就说做不到

Hook 不能切换模型。Claude Code 的 hook API 没有这个接口。

Pattern 5.6 Model Fallback Advisory 的做法：在 `additionalContext` 里建议 agent "考虑换个模型"。但 agent 可以无视这个建议。

这个 pattern 标着 `[ADVISORY ONLY]`。不是假装能工作——它确实只是建议，不是保证。

标的理由：静默失效是最差的结果。你以为"hook 会自动降级到更强的模型"，基于这个假设安排了过夜任务。结果能力不存在，任务失败了 8 小时你才知道。

不限于模型切换。Doubt gate 会对代码注释里的"should be"误报——这也标出来了，比假装不存在强。

---

## 6 轴架构：只装你需要的

40 个 pattern 分布在 6 个独立的轴上。每个轴是一个独立的 Claude Code skill——你可以只装 execution-loop 解决"agent 总是提前退出"的问题，完全不碰其他 5 个轴。

```
execution-harness/
├── principles.md                    ← 10 条设计原则
├── execution-loop/                  ← 让 agent 继续工作直到完成
│   ├── SKILL.md                     7 patterns
│   ├── scripts/                     ralph-stop-hook, doubt-gate, drift-reanchor...
│   └── references/                  每个 pattern 的深度参考
├── tool-governance/                 ← 让工具使用安全可控
│   ├── SKILL.md                     6 patterns
│   ├── scripts/                     tool-error-tracker, tool-input-guard...
│   └── references/
├── context-memory/                  ← 让知识跨压缩存活
│   ├── SKILL.md                     8 patterns
│   ├── scripts/                     context-usage, compaction-extract
│   └── references/
├── multi-agent/                     ← 让多个 agent 协同而非冲突
│   ├── SKILL.md                     6 patterns（全部 design）
│   └── references/
├── error-recovery/                  ← 让 agent 从故障中恢复
│   ├── SKILL.md                     7 patterns
│   ├── scripts/                     rate-limit-recovery
│   └── references/
└── quality-verification/            ← 让输出质量有保障
    ├── SKILL.md                     6 patterns
    ├── scripts/                     post-edit-check, bracket-hook, test-before-commit
    └── references/
```

### 轴之间的关系

没有硬依赖，但有协作关系。装了上游轴，下游轴工作得更好：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">轴间协作关系</div>
<div style="display:flex;gap:16px;flex-wrap:wrap">
<div style="flex:1;min-width:200px">
<div style="border-radius:8px;padding:12px;background:#eff6ff;border:1px solid #93c5fd;margin-bottom:4px">
<div style="font-size:12px"><b>tool-governance</b><br><span style="color:#666">tracker 记录错误数据</span></div>
</div>
<div style="text-align:center;color:#bbb;font-size:11px">↓ 提供数据</div>
<div style="border-radius:8px;padding:12px;background:#fef3c7;border:1px solid #fde68a;margin-top:4px">
<div style="font-size:12px"><b>error-recovery</b><br><span style="color:#666">基于错误频率决定降级</span></div>
</div>
</div>
<div style="flex:1;min-width:200px">
<div style="border-radius:8px;padding:12px;background:#f0fdf4;border:1px solid #86efac;margin-bottom:4px">
<div style="font-size:12px"><b>execution-loop</b><br><span style="color:#666">ralph 控制执行循环</span></div>
</div>
<div style="text-align:center;color:#bbb;font-size:11px">↓ 阶段边界</div>
<div style="border-radius:8px;padding:12px;background:#faf5ff;border:1px solid #c4b5fd;margin-top:4px">
<div style="font-size:12px"><b>context-memory</b><br><span style="color:#666">阶段结束时提取 handoff</span></div>
</div>
</div>
<div style="flex:1;min-width:200px">
<div style="border-radius:8px;padding:12px;background:#fef2f2;border:1px solid #fca5a5;margin-bottom:4px">
<div style="font-size:12px"><b>quality-verification</b><br><span style="color:#666">post-edit 发现错误</span></div>
</div>
<div style="text-align:center;color:#bbb;font-size:11px">↓ 错误数据</div>
<div style="border-radius:8px;padding:12px;background:#eff6ff;border:1px solid #93c5fd;margin-top:4px">
<div style="font-size:12px"><b>tool-governance</b><br><span style="color:#666">tracker 记录这些错误</span></div>
</div>
</div>
</div>
</div>

不装上游也能跑——只是少数据。比如 error-recovery 没有 tool-governance 的错误计数，限速恢复（5.1）照常工作，但基于错误频率的工具降级（5.5）就没数据可用了。

### 40 个 Pattern：每个轴里到底有什么

Pattern 分三种：**script**（bash 脚本，配到 settings.json 就能用）、**design**（设计指南 + 伪代码，按场景适配）、**config**（配置模板，改路径就行）。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">40 Pattern 分类总览</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
<div style="flex:1;min-width:160px;border-radius:8px;padding:12px;background:#f0fdf4;border:1px solid #86efac;text-align:center">
<div style="font-size:24px;font-weight:700;color:#16a34a">13</div>
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px">SCRIPT</div>
<div style="font-size:11px;color:#666;margin-top:4px">可直接执行的 bash 脚本</div>
</div>
<div style="flex:1;min-width:160px;border-radius:8px;padding:12px;background:#eff6ff;border:1px solid #93c5fd;text-align:center">
<div style="font-size:24px;font-weight:700;color:#3b82f6">22</div>
<div style="font-size:11px;color:#3b82f6;font-weight:700;letter-spacing:1px">DESIGN</div>
<div style="font-size:11px;color:#666;margin-top:4px">设计指南 + 伪代码参考</div>
</div>
<div style="flex:1;min-width:160px;border-radius:8px;padding:12px;background:#fefce8;border:1px solid #fde68a;text-align:center">
<div style="font-size:24px;font-weight:700;color:#a16207">4</div>
<div style="font-size:11px;color:#a16207;font-weight:700;letter-spacing:1px">CONFIG</div>
<div style="font-size:11px;color:#666;margin-top:4px">配置模板，改路径就行</div>
</div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:6px">
<div style="display:flex;align-items:center;gap:6px;flex:1;min-width:200px;border-radius:6px;padding:8px 10px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:11px;font-weight:700;color:#16a34a;white-space:nowrap">EXECUTION LOOP</div>
<div style="display:flex;gap:3px;flex-wrap:wrap">
<span style="background:#dcfce7;border-radius:4px;padding:1px 6px;font-size:10px;color:#16a34a">3 script</span>
<span style="background:#dbeafe;border-radius:4px;padding:1px 6px;font-size:10px;color:#3b82f6">3 design</span>
<span style="background:#fef3c7;border-radius:4px;padding:1px 6px;font-size:10px;color:#a16207">1 config</span>
</div>
</div>
<div style="display:flex;align-items:center;gap:6px;flex:1;min-width:200px;border-radius:6px;padding:8px 10px;background:#fef2f2;border:1px solid #fca5a5">
<div style="font-size:11px;font-weight:700;color:#dc2626;white-space:nowrap">TOOL GOVERNANCE</div>
<div style="display:flex;gap:3px;flex-wrap:wrap">
<span style="background:#dcfce7;border-radius:4px;padding:1px 6px;font-size:10px;color:#16a34a">4 script</span>
<span style="background:#fef3c7;border-radius:4px;padding:1px 6px;font-size:10px;color:#a16207">2 config</span>
</div>
</div>
<div style="display:flex;align-items:center;gap:6px;flex:1;min-width:200px;border-radius:6px;padding:8px 10px;background:#faf5ff;border:1px solid #c4b5fd">
<div style="font-size:11px;font-weight:700;color:#7c3aed;white-space:nowrap">CONTEXT MEMORY</div>
<div style="display:flex;gap:3px;flex-wrap:wrap">
<span style="background:#dcfce7;border-radius:4px;padding:1px 6px;font-size:10px;color:#16a34a">2 script</span>
<span style="background:#dbeafe;border-radius:4px;padding:1px 6px;font-size:10px;color:#3b82f6">6 design</span>
</div>
</div>
<div style="display:flex;align-items:center;gap:6px;flex:1;min-width:200px;border-radius:6px;padding:8px 10px;background:#fefce8;border:1px solid #fde68a">
<div style="font-size:11px;font-weight:700;color:#a16207;white-space:nowrap">MULTI-AGENT</div>
<div style="display:flex;gap:3px;flex-wrap:wrap">
<span style="background:#dbeafe;border-radius:4px;padding:1px 6px;font-size:10px;color:#3b82f6">6 design</span>
</div>
</div>
<div style="display:flex;align-items:center;gap:6px;flex:1;min-width:200px;border-radius:6px;padding:8px 10px;background:#eff6ff;border:1px solid #93c5fd">
<div style="font-size:11px;font-weight:700;color:#3b82f6;white-space:nowrap">ERROR RECOVERY</div>
<div style="display:flex;gap:3px;flex-wrap:wrap">
<span style="background:#dcfce7;border-radius:4px;padding:1px 6px;font-size:10px;color:#16a34a">1 script</span>
<span style="background:#dbeafe;border-radius:4px;padding:1px 6px;font-size:10px;color:#3b82f6">6 design</span>
</div>
</div>
<div style="display:flex;align-items:center;gap:6px;flex:1;min-width:200px;border-radius:6px;padding:8px 10px;background:#f3f4f6;border:1px solid #e5e7eb">
<div style="font-size:11px;font-weight:700;color:#666;white-space:nowrap">QUALITY VERIF.</div>
<div style="display:flex;gap:3px;flex-wrap:wrap">
<span style="background:#dcfce7;border-radius:4px;padding:1px 6px;font-size:10px;color:#16a34a">3 script</span>
<span style="background:#dbeafe;border-radius:4px;padding:1px 6px;font-size:10px;color:#3b82f6">1 design</span>
<span style="background:#fef3c7;border-radius:4px;padding:1px 6px;font-size:10px;color:#a16207">1 config</span>
</div>
</div>
</div>
</div>

#### Execution Loop — 7 个 pattern，治"做一半就停了"

| # | Pattern | 类型 | 干什么 |
|---|---------|------|--------|
| 1.1 | Ralph persistent loop | script | Stop hook 阻止提前退出，5 个安全阀保底 |
| 1.2 | Doubt gate | script | 检测"可能""大概"等投机语言，要求 agent 先验证再说 |
| 1.3 | Adaptive complexity triage | design | 按任务复杂度自动选 harness 强度——改 typo 不需要全套 |
| 1.4 | Task completion verifier | script | 读任务清单，有未完成项就不让停 |
| 1.5 | Drift re-anchoring | script | 每 N 轮重新注入原始任务描述，防止跑偏 |
| 1.6 | Headless execution control | config | `-p` 模式没有 Stop hook，用 `--max-turns` + 进程重启替代 |
| 1.7 | Iteration-aware messaging | design | 第 5 轮和第 45 轮的 block 消息不该一样，分阶段调语气 |

代表性脚本：`ralph-stop-hook.sh`（124 行）、`doubt-gate.sh`（43 行）。

#### Tool Governance — 6 个 pattern，治"重试死循环"和"危险命令"

| # | Pattern | 类型 | 干什么 |
|---|---------|------|--------|
| 2.1 | Tool error escalation | script | 连续 3 次提示、5 次直接 block |
| 2.2 | Denial circuit breaker | script | 用户否决了工具调用，agent 换个措辞再来——追踪否决次数，3 次警告 |
| 2.3 | Checkpoint + rollback | script | 跑 `rm -rf` 之类的破坏性命令前自动 `git stash` |
| 2.4 | Graduated permission rules | config | 按风险分层：读文件自动放行，写文件需确认，`rm` 直接拦 |
| 2.5 | Component-scoped hooks | config | 不同任务启用不同 hook 组合 |
| 2.6 | Tool input guard | script | 拦截 `rm -rf /`、`curl | sh` 等已知危险模式 |

`tool-error-tracker.sh` + `tool-error-advisor.sh` 是 M7 原则的典型——observer 和 blocker 必须成对部署。

#### Context & Memory — 8 个 pattern，治"压缩后失忆"

| # | Pattern | 类型 | 干什么 |
|---|---------|------|--------|
| 3.1 | Handoff documents | design | 阶段边界写 Decided/Rejected/Remaining，推理过程写磁盘 |
| 3.2 | Compaction memory extraction | script | 检测到压缩将发生时，抢先把关键知识快照到 handoff 文件 |
| 3.3 | Three-gate memory consolidation | design | 跨 session 记忆合并，时间/数量/锁三道门控防写冲突 |
| 3.4 | Token budget allocation | design | 给 agent 注入"你还剩多少 context"的预算感知 |
| 3.5 | Context token count | script | 从 transcript 提取 input token 数——虽然不知道总窗口多大 |
| 3.6 | Filesystem as working memory | design | 用 `.working-state/` 目录存活跃工作状态，不靠 context |
| 3.7 | Compaction quality audit | design | 压缩后验证关键信息还在不在——如果 Rejected 段消失了就报警 |
| 3.8 | Auto-compact circuit breaker | design | 连续 3 次 compact 失败后停止尝试，等 Reactive Compact 兜底 |

#### Multi-Agent — 6 个 pattern，全部是 design，没有脚本

多 agent 编排差异太大——coordinator 模式和 swarm 模式的实现完全不同，硬编码脚本反而限制适用性。这个轴提供的是"怎么想"。

| # | Pattern | 干什么 |
|---|---------|--------|
| 4.1 | Three delegation modes | Coordinator / Fork / Swarm 三种模式的选型指南和适用场景 |
| 4.2 | Shared task list protocol | 用文件做任务协调，替代内存中的任务队列 |
| 4.3 | File claim and lock | 编辑前写 claim 标记，其他 agent 看到标记就等或换文件 |
| 4.4 | Agent workspace isolation | 每个 agent 用独立 git worktree，根源上避免文件冲突 |
| 4.5 | Synthesis gate | coordinator 必须先综合 worker 结果再委派——不当邮局 |
| 4.6 | Review-execution separation | 写代码和审代码用不同 agent，自己审自己等于没审 |

#### Error Recovery — 7 个 pattern，治"挂死"和"crash 丢进度"

| # | Pattern | 类型 | 干什么 |
|---|---------|------|--------|
| 5.1 | Rate limit recovery | script | cron 脚本扫描 tmux pane，检测到 "Press Enter" 就自动发 |
| 5.2 | Crash state recovery | design | 检测残留的 ralph.json / tool-errors.json，从断点恢复 |
| 5.3 | Stale session daemon | design | 死 session 的知识回收——handoff 还在，可以喂给新 session |
| 5.4 | MCP reconnection | design | MCP server 断连后指数退避重连，不要 agent 手动重启 |
| 5.5 | Graceful tool degradation | design | 首选工具挂了，降级到替代工具（比如 rg 挂了用 grep） |
| 5.6 | Model fallback advisory | design | 连续失败 3 次建议换模型——但只是建议，hook 切不了模型 `[ADVISORY ONLY]` |
| 5.7 | Anti-stampede retry asymmetry | design | 前台任务遇 529 可重试，后台任务（summary/compaction）立即放弃不重试 |

`rate-limit-recovery.sh` 不是 hook，是独立 cron 脚本。

#### Quality & Verification — 6 个 pattern，治"提交烂代码"

| # | Pattern | 类型 | 干什么 |
|---|---------|------|--------|
| 6.1 | Post-edit diagnostics | script | 每次 Write/Edit 后跑 linter/type checker，错误即时反馈 |
| 6.2 | Hook runtime profiles | config | minimal / standard / strict 三档，一键切 hook 强度 |
| 6.3 | Session turn metrics | script | 记录每轮耗时和 turn 计数，用来调安全阀参数 |
| 6.4 | Test-before-commit gate | script | `git commit` 前自动跑测试，不过不让提 |
| 6.5 | Atomic state writes | design | write-to-temp-then-rename，crash 时不留半截 JSON |
| 6.6 | Session state hygiene | design | 定期清理 stale session 目录和 orphaned lock 文件 |

下面集中看 5 个最核心的 pattern。

---

## Deep Dive: 5 个核心 Pattern

5 个 pattern，每个按问题→方案→代码→tradeoff 展开。代码都是简化版，完整版在仓库里。

### Ralph Persistent Loop (Pattern 1.1)

**问题在哪**

Claude Code 的 interactive 模式下，agent 每次 `end_turn` 后等你发新消息。对于"重构这 7 个文件"这种任务，agent 改完 2 个文件觉得"差不多了"就停了。你得反复说"继续"，像一台人肉 cron。

Agent 不一定在偷懒。改完 2 个文件后，它觉得已经展示了修改模式，剩下的"类似"。在它看来这就算完成了。但你要的是 7 个文件全改完。

**怎么治**

Claude Code 的 Stop hook 在 agent 每次试图结束时触发。注意时机——不是它在想"要不要停"，是它已经决定停了，hook 才拦住。读状态文件，任务没完就返回 `{"decision":"block","reason":"..."}`，阻止退出并注入继续工作的指令。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">Ralph 执行循环</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;align-items:center;margin-bottom:16px">
<span style="background:#dbeafe;border:1px solid #93c5fd;border-radius:6px;padding:6px 12px;font-size:12px"><b>Agent 工作</b></span>
<span style="color:#bbb">→</span>
<span style="background:#dbeafe;border:1px solid #93c5fd;border-radius:6px;padding:6px 12px;font-size:12px"><b>尝试 end_turn</b></span>
<span style="color:#bbb">→</span>
<span style="background:#fef3c7;border:2px solid #fde68a;border-radius:6px;padding:6px 12px;font-size:12px;font-weight:600;color:#a16207"><b>Stop Hook 触发</b></span>
</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
<div style="border-radius:8px;padding:12px;background:#f0fdf4;border:1px solid #86efac;min-width:160px;text-align:center">
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px;margin-bottom:4px">安全阀命中</div>
<div style="font-size:12px;color:#666">401/403 / cancel / 超时 / 迭代上限</div>
<div style="margin-top:6px;font-size:12px;color:#16a34a;font-weight:600">→ 放行退出</div>
</div>
<div style="border-radius:8px;padding:12px;background:#fef2f2;border:1px solid #fca5a5;min-width:160px;text-align:center">
<div style="font-size:11px;color:#dc2626;font-weight:700;letter-spacing:1px;margin-bottom:4px">任务未完成</div>
<div style="font-size:12px;color:#666">active=true, iteration &lt; max</div>
<div style="margin-top:6px;font-size:12px;color:#dc2626;font-weight:600">→ BLOCK + 注入指令 → 继续工作</div>
</div>
</div>
</div>

初始化：

```bash
# 创建 session 状态，设最多 50 轮
bash execution-loop/scripts/ralph-init.sh my-task 50
# 输出: Ralph initialized: sessions/my-task/ralph.json (max 50 iterations)
```

状态文件长这样：

```json
{
  "session_id": "my-task",
  "active": true,
  "iteration": 0,
  "max_iterations": 50,
  "created_at": "2026-04-05T10:00:00Z",
  "last_checked_at": "2026-04-05T10:00:00Z"
}
```

Stop hook 核心逻辑（`ralph-stop-hook.sh` 简化版，完整 124 行见仓库）：

```bash
# 读 hook 输入
INPUT=$(head -c 20000)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')

STATE_FILE="sessions/${SESSION_ID}/ralph.json"
[ -f "$STATE_FILE" ] || { echo '{"continue":true}'; exit 0; }  # 无状态则放行（M5）

ACTIVE=$(jq -r '.active' "$STATE_FILE")
[ "$ACTIVE" = "true" ] || { echo '{"continue":true}'; exit 0; }

ITERATION=$(jq -r '.iteration' "$STATE_FILE")
MAX=$(jq -r '.max_iterations' "$STATE_FILE")

# 安全阀 1: 认证失败立即放行
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""')
if echo "$LAST_MSG" | grep -qiE '401|403|unauthorized|forbidden'; then
  jq '.active = false | .deactivation_reason = "auth_error"' \
    "$STATE_FILE" > tmp && mv tmp "$STATE_FILE"
  echo '{"continue":true}'; exit 0
fi

# 安全阀 4: 迭代上限
if [ "$ITERATION" -ge "$MAX" ]; then
  jq '.active = false | .deactivation_reason = "max_iterations"' \
    "$STATE_FILE" > tmp && mv tmp "$STATE_FILE"
  echo '{"continue":true}'; exit 0
fi

# 阻止退出，递增计数器
NEW_ITER=$((ITERATION + 1))
jq --argjson i "$NEW_ITER" '.iteration = $i' "$STATE_FILE" > tmp && mv tmp "$STATE_FILE"

# Block 消息使用反推理阻断措辞
jq -n --arg r "[RALPH LOOP ${NEW_ITER}/${MAX}] Task is NOT done. \
Do NOT rationalize that the remaining work can be done in a follow-up. \
Do NOT claim completion with caveats like 'mostly done' or 'should work'. \
Check your original task and verify EVERY requirement is met." \
  '{"decision":"block","reason":$r}'
```

Block 消息的措辞是刻意的。"Do NOT rationalize" 不是客气话，是针对 LLM 逃逸策略的硬对抗。Agent 第 10 轮会说"主要工作已完成，剩余可在后续处理"——听着合理，但它在找借口停下来。消息预判了这种措辞，提前堵死。

Crash 恢复也内置了。`ralph-init.sh` 检测到残留状态时自动从上次迭代继续：

```bash
# 上次 session 在第 37 轮 crash 了
bash execution-loop/scripts/ralph-init.sh my-task 50
# 输出: Resuming ralph from iteration 37 (previous state: active=true, reason=stale)
```

**代价是什么**

Hook 是确定性的，block 消息的效果不是。Agent 第 15 轮开始"应付"——表面继续工作，实际做一些无关紧要的"改进"来满足"不许停"的要求。我们叫这个 compliance mode。Pattern 1.7 Iteration-Aware Messaging 在不同阶段换不同语气的 block 消息，有帮助但治不根。

Ralph 只在 interactive 模式有用。Headless（`-p`）没有 Stop 事件，得用 `--max-turns` + 进程重启。

50 轮上限不是万能数字。简单的 10 轮够了，跨 20 个文件的重构要 200 轮。

### Tool Error Escalation (Pattern 2.1)

容器没装 cargo。Agent 跑 `cargo build`，失败，下一步又是 `cargo build`。参数一模一样，结果一模一样。5 次、10 次。

`PostToolUseFailure` 只让 agent 看到这一次的错误。没有人告诉它"你用同样的方式失败了 5 次"。每次都是一个独立的"再试试"。

**两个 hook 配合**

遵循 M7 observe-then-intervene：

1. `tool-error-tracker.sh`（PostToolUseFailure hook）——每次工具失败后记录 `tool_name + input_hash + count`
2. `tool-error-advisor.sh`（PreToolUse hook）——下次调用同一工具前，如果 count >= 5，block

关键设计：用 input_hash（工具输入前 200 字符的 MD5）区分"同一命令重试"和"换了参数的新尝试"。如果 agent 把 `cargo build` 改成 `cargo build --release`，hash 不同，计数器重置。只有完全相同的 tool + 完全相同的输入才累计。

三级升级：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">Tool Error 三级升级</div>
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
<div style="width:70px;text-align:right;font-size:12px;font-weight:600;color:#666">1-2 次</div>
<div style="flex:1;background:#f3f4f6;border:1px solid #e5e7eb;border-radius:6px;padding:8px 12px">
<div style="background:#e5e7eb;border-radius:4px;height:8px;width:20%"></div>
<div style="font-size:11px;color:#666;margin-top:4px">只记录，不干预</div>
</div>
</div>
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
<div style="width:70px;text-align:right;font-size:12px;font-weight:600;color:#a16207">3-4 次</div>
<div style="flex:1;background:#fefce8;border:1px solid #fde68a;border-radius:6px;padding:8px 12px">
<div style="background:#fde68a;border-radius:4px;height:8px;width:60%"></div>
<div style="font-size:11px;color:#a16207;margin-top:4px"><b>软提示</b> "考虑换参数？缺依赖？" — 概率性，agent 可忽略</div>
</div>
</div>
<div style="display:flex;align-items:center;gap:10px">
<div style="width:70px;text-align:right;font-size:12px;font-weight:600;color:#dc2626">5+ 次</div>
<div style="flex:1;background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:8px 12px">
<div style="background:#fca5a5;border-radius:4px;height:8px;width:100%"></div>
<div style="font-size:11px;color:#dc2626;margin-top:4px"><b>直接 DENY</b> — 确定性，agent 绕不过</div>
</div>
</div>
</div>

Tracker 代码（`tool-error-tracker.sh`）：

```bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')
INPUT_HASH=$(echo "$INPUT" | jq -Sc '.tool_input // ""' | head -c 200 | md5)

STATE_FILE="sessions/${SESSION_ID}/tool-errors.json"

if [ -f "$STATE_FILE" ]; then
  PREV_TOOL=$(jq -r '.tool_name' "$STATE_FILE")
  PREV_HASH=$(jq -r '.input_hash' "$STATE_FILE")
  PREV_COUNT=$(jq -r '.count' "$STATE_FILE")

  if [ "$PREV_TOOL" = "$TOOL" ] && [ "$PREV_HASH" = "$INPUT_HASH" ]; then
    COUNT=$((PREV_COUNT + 1))   # 同工具+同输入 → 累加
  else
    COUNT=1                      # 不同 → 重置
  fi
else
  COUNT=1
fi

# 原子写入
jq -n --arg tool "$TOOL" --arg hash "$INPUT_HASH" --argjson count "$COUNT" \
  '{tool_name:$tool, input_hash:$hash, count:$count}' > tmp && mv tmp "$STATE_FILE"

# 3+ 次注入提示
if [ "$COUNT" -ge 5 ]; then
  echo "MUST use an alternative approach. Failed $COUNT times with identical input."
elif [ "$COUNT" -ge 3 ]; then
  echo "Failed $COUNT times with same input. Missing dependency? Wrong parameters?"
fi
```

Advisor 代码（`tool-error-advisor.sh`）：

```bash
PREV_COUNT=$(jq -r '.count // 0' "$STATE_FILE")
PREV_TOOL=$(jq -r '.tool_name' "$STATE_FILE")
PREV_HASH=$(jq -r '.input_hash' "$STATE_FILE")

# 同 tool + 同 input + 5 次以上 → deny
if [ "$PREV_TOOL" = "$TOOL" ] && [ "$PREV_HASH" = "$INPUT_HASH" ] && \
   [ "$PREV_COUNT" -ge 5 ]; then
  echo '{"hookSpecificOutput":{"permissionDecision":"deny",
    "reason":"BLOCKED: Failed 5+ times with identical input. Use a different approach."}}'
else
  echo '{"continue":true}'
fi
```

**哪里粗糙**

3 次的软提示，agent 可以无视。5 次的 deny 绕不过。中间 2 次缓冲是有意的——也许第 3 次 agent 真的换了策略。

Input hash 只取前 200 字符。长命令前 200 字符相同但后面不同，也会被判为"相同输入"。刻意的取舍——取整个输入做 hash 没必要，有些工具输入可以很大。

计数器也不分错误类型。5 次 "command not found" 和 5 次 "permission denied" 同等对待。粗粒度，但够用。想更精细就得解析错误消息，脚本复杂度翻倍。

### Handoff Documents (Pattern 3.1)

Context window 会被压缩。这不是 bug——context 是有限的。但你控制不了压缩保留什么。

Claude Code 有 4 级压缩，从轻到重：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:16px">Context 4 级压缩</div>
<div style="border-radius:8px;padding:10px 14px;background:#f0fdf4;border:1px solid #86efac;margin-bottom:6px">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-size:11px;color:#16a34a;font-weight:700">L1 MICROCOMPACT</span><span style="font-size:12px;color:#666"> — 删旧 tool results</span></div>
<div style="font-size:11px;color:#666">压缩 10-50K | 成本 零</div>
</div>
</div>
<div style="border-radius:8px;padding:10px 14px;background:#eff6ff;border:1px solid #93c5fd;margin-bottom:6px">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-size:11px;color:#3b82f6;font-weight:700">L2 SESSION MEMORY</span><span style="font-size:12px;color:#666"> — 用预建摘要替换</span></div>
<div style="font-size:11px;color:#666">压缩 60-80% | 成本 零</div>
</div>
</div>
<div style="border-radius:8px;padding:10px 14px;background:#fefce8;border:1px solid #fde68a;margin-bottom:6px">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-size:11px;color:#a16207;font-weight:700">L3 FULL COMPACT</span><span style="font-size:12px;color:#666"> — LLM 生成摘要</span></div>
<div style="font-size:11px;color:#666">压缩 80-95% | 一次 API 调用</div>
</div>
</div>
<div style="border-radius:8px;padding:10px 14px;background:#fef2f2;border:2px solid #fca5a5">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-size:11px;color:#dc2626;font-weight:700">L4 REACTIVE COMPACT</span><span style="font-size:12px;color:#666"> — 413 错误触发应急压缩</span></div>
<div style="font-size:11px;color:#dc2626;font-weight:600">可变 | 应急</div>
</div>
</div>
</div>

L1 只删 tool results，影响最小。L3 才是杀手——LLM 生成摘要，推理过程（"为什么排除方案 B"）是最先被丢的。既不是结论也不是代码，压缩算法看它就像多余的对话。

**解法：写磁盘**

不靠 context，靠文件系统。阶段结束时把关键决策写进磁盘文件。

5 段式结构：

```markdown
# Handoff: cache-implementation

## Decided
- 选择 Redis 作为缓存方案（项目已有 Redis 依赖）
- LRU 策略，TTL 5 分钟

## Rejected
- 排除 Memcached：团队无运维经验
- 排除本地文件缓存：不支持多实例部署

## Risks
- Redis 单点故障需要 Sentinel（当前未配置）
- 缓存穿透风险

## Files Modified
- src/cache/redis_client.py — 新建
- src/api/handlers.py:45-67 — 添加缓存查询层

## Remaining
- Sentinel 配置（下个迭代）
- 缓存预热逻辑
```

存储在 `sessions/<session-id>/handoffs/stage-<n>.md`。下一阶段的 agent 启动时读取最新的 handoff。

**Rejected** 段价值最高。"选了 Redis"是结论，10 个字够了。"为什么不选 Memcached"是推理——压缩会丢的就是这部分。不写 Rejected，下一个 agent 看到"用 Redis"，又花 5 轮讨论"为什么不用 Memcached"。

**三个已知问题**

第一，handoff 是 prompt 驱动的——你得告诉 agent "阶段结束时写 handoff"。它可以不听。配合 Pattern 1.4 Task Completion Verifier 检查 handoff 文件是否存在，能缓解但不根治——又回到了 prompt vs hook 的老问题。

第二，handoff 会累积。每阶段 500 字，10 个阶段就是 5000 字注入 context。Pattern 3.3 Three-Gate Memory Consolidation 做合并去重，但本质上是在用一种 context 开销换另一种。

第三，跨阶段矛盾。Stage-2 推翻了 stage-1 的决策但没更新 stage-1 的 handoff。后面的 agent 读到两份矛盾的 handoff，不知道信哪个。这个问题 Execution Harness 当前没解决。

### Synthesis Gate (Pattern 4.5)

Coordinator 收到 3 个 worker 的 research 结果。最偷懒的做法：

```
"Based on the findings above, implement the fix."
```

一句话，coordinator 变邮局了。Implementation worker 拿到一堆原始数据，自己去理解、去筛选。问题是 worker 没有全局视角——3 个 worker 的发现哪些矛盾、哪些更可靠，它不知道。

Anthropic 的多 agent 博客直接叫它反模式。Coordinator 存在的意义是综合判断，不是当传话筒。

| | 邮局模式 | Synthesis 模式 |
|---|---|---|
| Coordinator 做什么 | 转发 worker 原始输出 | 消化、综合、形成行动计划 |
| Worker 收到什么 | 一堆原始 research 数据 | 结论 + 依据 + 明确的行动项 |
| Worker 需要判断什么 | 哪些发现重要、哪些可以忽略 | 只需执行明确的计划 |
| 产出质量 | 不可控——取决于 worker 的理解 | 可控——行动计划已经过审 |

在 Research 和 Implementation 之间插一道 gate。Coordinator 必须先产出 synthesis 文档（Conclusion、Evidence、Action Plan），gate 脚本检查存在性和结构完整性，过了才能启动 implementation worker。

```bash
SYNTHESIS=".coordination/synthesis.md"

# 检查 1：文件存在且非空
if [ ! -s "$SYNTHESIS" ]; then
  echo "GATE FAILED: synthesis.md 不存在或为空"
  exit 1
fi

# 检查 2：最小长度（不能一句话打发）
LINES=$(wc -l < "$SYNTHESIS")
if [ "$LINES" -lt 10 ]; then
  echo "GATE FAILED: synthesis.md 只有 ${LINES} 行，内容不充分"
  exit 1
fi

# 检查 3：必须包含关键结构
for SECTION in "Conclusion" "Action Plan" "Evidence"; do
  if ! grep -qi "$SECTION" "$SYNTHESIS"; then
    echo "GATE FAILED: 缺少必要节: ${SECTION}"
    exit 1
  fi
done

echo "GATE PASSED"
```

Gate 通过后，把 synthesis 作为 implementation worker 的输入：

```bash
claude -p --max-turns 50 \
  "根据以下 synthesis 执行实现。$(cat .coordination/synthesis.md)"
```

**代价**

多了一个串行步骤。Synthesis 是流水线瓶颈，不能并行化。

而且检查是浅层的。Coordinator 写出格式正确但内容空洞的 synthesis——有 "Conclusion" 标题但结论是废话——gate 拦不住。深层验证需要 LLM 判断，成本和延迟都上去了。

简单任务里强制 synthesis 是浪费时间。M6 说了，简单任务跳过。但"什么算简单"本身就需要判断。

### Post-Edit Diagnostics (Pattern 6.1)

`Write` 返回 success。文件写进去了。但有类型错误。

Agent 不知道。继续改下一个文件——这个文件 import 了上一个有错的模块。3 个文件后错误级联。

`Write` 只管"文件有没有写进去"，不管内容对不对。合理——它不该知道什么是 TypeScript。但编辑和诊断之间有个 gap 需要填。

**用 PostToolUse hook 填**

PostToolUse hook，matcher 设为 `Write|Edit|MultiEdit`。每次文件编辑完成后，对修改的文件跑 linter / type checker，把错误通过 `additionalContext` 反馈给 agent。

配置：

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "bash quality-verification/scripts/post-edit-check.sh",
        "async": true
      }]
    }]
  }
}
```

脚本按文件扩展名选择诊断工具：

```bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
[ -f "$FILE" ] || exit 0

ERRORS=""
case "$FILE" in
  *.py)
    LINT=$(ruff check "$FILE" --no-fix 2>&1 | head -5) || true
    [ -n "$LINT" ] && ERRORS="${ERRORS}ruff: ${LINT}\n"
    TYPE=$(pyright "$FILE" 2>&1 | grep -E 'error|Error' | head -3) || true
    [ -n "$TYPE" ] && ERRORS="${ERRORS}pyright: ${TYPE}\n"
    ;;
  *.ts|*.tsx)
    TYPE=$(npx tsc --noEmit "$FILE" 2>&1 | grep 'error TS' | head -3) || true
    [ -n "$TYPE" ] && ERRORS="${ERRORS}tsc: ${TYPE}\n"
    ;;
  *.rs)
    CHECK=$(cargo check 2>&1 | grep '^error' | head -3) || true
    [ -n "$CHECK" ] && ERRORS="${ERRORS}cargo: ${CHECK}\n"
    ;;
  *.go)
    VET=$(go vet "$FILE" 2>&1 | head -3) || true
    [ -n "$VET" ] && ERRORS="${ERRORS}go vet: ${VET}\n"
    ;;
  *.sh)
    SC=$(shellcheck "$FILE" 2>&1 | head -5) || true
    [ -n "$SC" ] && ERRORS="${ERRORS}shellcheck: ${SC}\n"
    ;;
esac

if [ -n "$ERRORS" ]; then
  MSG=$(echo -e "$ERRORS" | head -10)
  jq -n --arg ctx "Post-edit diagnostics found issues: $MSG" \
    '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":$ctx}}'
fi
```

**和 Pattern 2.1 的区别**

两者在故障模型上互补。2.1 管"工具跑不起来"，6.1 管"工具跑完了但产出有问题"。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">两类工具故障</div>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<div style="flex:1;min-width:250px;border-radius:8px;padding:14px;background:#fef2f2;border:1px solid #fca5a5">
<div style="font-size:11px;color:#dc2626;font-weight:700;letter-spacing:1px;margin-bottom:10px">2.1 TOOL ERROR ESCALATION</div>
<div style="font-size:12px;color:#666;line-height:1.8">
触发：工具调用<b>失败</b><br>
场景：cargo build 找不到命令<br>
Hook：PreToolUse + PostToolUseFailure<br>
干预：<b style="color:#dc2626">阻止下次调用</b>
</div>
</div>
<div style="flex:1;min-width:250px;border-radius:8px;padding:14px;background:#fefce8;border:1px solid #fde68a">
<div style="font-size:11px;color:#a16207;font-weight:700;letter-spacing:1px;margin-bottom:10px">6.1 POST-EDIT DIAGNOSTICS</div>
<div style="font-size:12px;color:#666;line-height:1.8">
触发：工具调用<b>成功</b><br>
场景：文件写入成功但有类型错误<br>
Hook：PostToolUse<br>
干预：<b style="color:#a16207">注入错误反馈</b>
</div>
</div>
</div>
</div>

**async 的双刃剑**

`async: true` 不阻塞后续工具调用——但 agent 可能在收到诊断结果之前就开始编辑下一个文件。B 依赖 A 的类型定义，A 的诊断还没跑完 agent 已经在改 B 了。这种场景下 async 来不及。

大项目上 `cargo check` 跑 30 秒以上也不稀奇。频繁小编辑会让诊断排队。Debounce 能优化，当前脚本没做。

没装 linter 按 M5 静默跳过，不会因为少了 `ruff` 就不让你写代码。

---

## 3 步安装

### Step 1: Clone

```bash
git clone https://github.com/lanyasheng/execution-harness.git
cd execution-harness
```

### Step 2: 配置 hooks

把 hook 脚本路径加到 `~/.claude/settings.json`。以下是最小起步配置——覆盖了"提前退出"和"重试死循环"两个最常见的问题：

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [
        {
          "type": "command",
          "command": "bash /path/to/execution-loop/scripts/ralph-stop-hook.sh"
        },
        {
          "type": "command",
          "command": "bash /path/to/execution-loop/scripts/doubt-gate.sh"
        },
        {
          "type": "command",
          "command": "bash /path/to/quality-verification/scripts/bracket-hook.sh",
          "async": true
        }
      ]
    }],
    "PostToolUseFailure": [{
      "hooks": [{
        "type": "command",
        "command": "bash /path/to/tool-governance/scripts/tool-error-tracker.sh",
        "async": true
      }]
    }],
    "PreToolUse": [{
      "hooks": [
        {
          "type": "command",
          "command": "bash /path/to/tool-governance/scripts/tool-error-advisor.sh"
        },
        {
          "type": "command",
          "command": "bash /path/to/tool-governance/scripts/tool-input-guard.sh"
        }
      ]
    }],
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "bash /path/to/quality-verification/scripts/post-edit-check.sh",
        "async": true
      }]
    }]
  }
}
```

把 `/path/to/` 替换成你 clone 下来的实际路径。

### Step 3: 启动 Ralph（可选）

如果你的任务需要持续执行：

```bash
# session-id 任意取名，50 是最大迭代数
bash execution-loop/scripts/ralph-init.sh my-task 50

# 设置环境变量，让 hook 知道当前 session
export NC_SESSION=my-task

# 正常使用 Claude Code，Stop hook 自动阻止提前退出
```

取消 Ralph：

```bash
bash execution-loop/scripts/ralph-cancel.sh my-task
```

### 依赖

只需要 `bash`、`jq`、`python3`（跑测试用）。诊断相关的 `ruff`、`pyright`、`shellcheck`、`tsc` 是可选的——没装就静默跳过，不影响其他功能。

---

## 蒸馏方法论：38 个 Pattern 从哪来

40 个 pattern 不是从零设计的。6 个源，每个贡献了不同视角。

### 6 个源

| 项目 | 看了什么 | 提取了什么 |
|------|---------|----------|
| [harness-books](https://github.com/wquguru/harness-books) | Anthropic 和 OpenAI 的 harness engineering 文章解读 | 10 条设计原则的理论框架 |
| [claude-reviews-claude](https://github.com/openedclaude/claude-reviews-claude) | Claude Code v2.1.88 的源码分析 | 压缩机制、hook 协议、session 管理的内部实现细节 |
| [ccunpacked.dev](https://ccunpacked.dev/) | Claude Code 的工具全景和隐藏功能 | hook stdin/stdout 协议的具体行为 |
| [claude-howto](https://github.com/luongnv89/claude-howto) | Hook 扩展点的 API 教程 | 各种 hook type 的输入输出格式 |
| Claude Code 源码 | 泄露的 TypeScript 源码，直接读 | 4 级压缩的触发条件和内部行为、Stop/PreToolUse 等 hook event 的完整 stdin schema、session 状态管理的文件结构 |
| ClawHub harness skills | 社区贡献的 execution-harness 类 skill 合集 | 实战中验证过的 hook 脚本写法、常见踩坑（比如 jq 在 Alpine 上的兼容问题）、async hook 的 timing 行为 |

6 个源，每个都有盲区：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:16px">6 个蒸馏源的覆盖关系</div>
<div style="display:flex;gap:6px;flex-wrap:wrap">
<div style="flex:1;min-width:140px;border-radius:8px;padding:10px;background:#eff6ff;border:1px solid #93c5fd;text-align:center">
<div style="font-size:11px;color:#3b82f6;font-weight:700;margin-bottom:4px">harness-books</div>
<div style="font-size:11px;color:#666">理论框架</div>
<div style="font-size:10px;color:#999;margin-top:2px">没代码</div>
</div>
<div style="flex:1;min-width:140px;border-radius:8px;padding:10px;background:#f0fdf4;border:1px solid #86efac;text-align:center">
<div style="font-size:11px;color:#16a34a;font-weight:700;margin-bottom:4px">claude-reviews-claude</div>
<div style="font-size:11px;color:#666">源码级架构</div>
<div style="font-size:10px;color:#999;margin-top:2px">不管最佳实践</div>
</div>
<div style="flex:1;min-width:140px;border-radius:8px;padding:10px;background:#fefce8;border:1px solid #fde68a;text-align:center">
<div style="font-size:11px;color:#a16207;font-weight:700;margin-bottom:4px">ccunpacked.dev</div>
<div style="font-size:11px;color:#666">工具全景</div>
<div style="font-size:10px;color:#999;margin-top:2px">浅</div>
</div>
<div style="flex:1;min-width:140px;border-radius:8px;padding:10px;background:#faf5ff;border:1px solid #c4b5fd;text-align:center">
<div style="font-size:11px;color:#7c3aed;font-weight:700;margin-bottom:4px">claude-howto</div>
<div style="font-size:11px;color:#666">API 教程</div>
<div style="font-size:10px;color:#999;margin-top:2px">零散</div>
</div>
<div style="flex:1;min-width:140px;border-radius:8px;padding:10px;background:#fef2f2;border:2px solid #fca5a5;text-align:center">
<div style="font-size:11px;color:#dc2626;font-weight:700;margin-bottom:4px">Claude Code 源码</div>
<div style="font-size:11px;color:#666">一手权威</div>
<div style="font-size:10px;color:#999;margin-top:2px">需要自己啃</div>
</div>
<div style="flex:1;min-width:140px;border-radius:8px;padding:10px;background:#f3f4f6;border:1px solid #e5e7eb;text-align:center">
<div style="font-size:11px;color:#666;font-weight:700;margin-bottom:4px">ClawHub skills</div>
<div style="font-size:11px;color:#666">实战踩坑</div>
<div style="font-size:10px;color:#999;margin-top:2px">接地气</div>
</div>
</div>
</div>

单看任何一个都不够，交叉验证才能分清哪些 pattern 真有效。

### 蒸馏过程

先通读 6 个源的所有文档和代码，标注每个值得提取的 pattern。标准就一条："如果不做这件事，agent 会以可预测的方式失败。"不确定的标 maybe，最后淘汰了一半。

然后按失败模式分到 6 个轴里。一个 pattern 只能属于一个轴。横跨两个的（比如"错误重试后降级"）拆成两个独立 pattern。

每个 pattern 再分级：逻辑通用的做成 script，场景差异太大的标 design，纯配置的标 config。17 个 script 类 pattern 最终落地为 bash 脚本，stdin 读 JSON，stdout 写 JSON。90 个 pytest 测试覆盖所有 script。

### 刻意不做的事

蒸馏中排除了几类东西：

- **编排 runtime**（DAG 执行引擎、任务调度器、fan-in/fan-out 基础设施）——我们有多 agent 协调的 design pattern（Pattern 4.1-4.6，教你选 coordinator 还是 swarm、怎么防文件冲突），但不做跑这些模式的 runtime。模式是"怎么想"，runtime 是"怎么跑"，后者不在范围内。
- **Prompt engineering 技巧**——M1 说了，hook 是确定性的，prompt 是概率性的。Execution Harness 的定位是确定性机制。
- **模型选择和路由**——hook 切不了模型（M10），假装能做只会误导用户。
- **项目特定配置**——`tsconfig.json` 在哪、`ruff` 规则怎么配，这些留给用户。Pattern 提供的是通用机制，不是特定项目的配置文件。

---

## 写 Hook 之前应该知道的事

这几个坑都来自 Claude Code 源码。不知道的话，hook 写出来看着对，跑起来不对。

### PreToolUse 能改工具输入

PreToolUse hook 不止 allow/deny。它还能改参数：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">PreToolUse 三种响应</div>
<div style="display:flex;gap:10px;flex-wrap:wrap">
<div style="flex:1;min-width:150px;border-radius:8px;padding:12px;background:#f0fdf4;border:1px solid #86efac;text-align:center">
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px;margin-bottom:6px">ALLOW / DENY</div>
<div style="font-size:12px;color:#666">放行或拦截<br>最常用</div>
</div>
<div style="flex:1;min-width:150px;border-radius:8px;padding:12px;background:#eff6ff;border:2px solid #93c5fd;text-align:center">
<div style="font-size:11px;color:#3b82f6;font-weight:700;letter-spacing:1px;margin-bottom:6px">MODIFY INPUT</div>
<div style="font-size:12px;color:#666">改工具参数后放行<br>如：给 rm 加 --dry-run</div>
</div>
<div style="flex:1;min-width:150px;border-radius:8px;padding:12px;background:#fefce8;border:1px solid #fde68a;text-align:center">
<div style="font-size:11px;color:#a16207;font-weight:700;letter-spacing:1px;margin-bottom:6px">INJECT CONTEXT</div>
<div style="font-size:12px;color:#666">不改工具调用<br>给 agent 补充信息</div>
</div>
</div>
</div>

`updatedInput` 让 hook 从门卫变成了改装工。给 bash 命令自动加 `timeout 60`，给 `rm` 改成 `rm --dry-run` 先看看会删什么——不拦截，但偷偷改安全了。

### 多个 Hook 同时响应时的聚合规则

3 个 PreToolUse hook 同时响应时，输出按以下规则合并：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">Hook 输出聚合规则</div>
<div style="border-radius:8px;padding:12px;background:#fef2f2;border:1px solid #fca5a5;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-size:11px;color:#dc2626;font-weight:700">permissionDecision</span></div>
<div style="font-size:12px;color:#666"><b>最严格的赢</b> — 一个 deny 就全 deny</div>
</div>
</div>
<div style="border-radius:8px;padding:12px;background:#fefce8;border:1px solid #fde68a;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-size:11px;color:#a16207;font-weight:700">updatedInput</span></div>
<div style="font-size:12px;color:#666"><b>最后一个赢</b> — 按 settings.json 顺序，后面的覆盖前面的</div>
</div>
</div>
<div style="border-radius:8px;padding:12px;background:#f0fdf4;border:1px solid #86efac">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-size:11px;color:#16a34a;font-weight:700">additionalContext</span></div>
<div style="font-size:12px;color:#666"><b>拼接</b> — 所有 hook 的 context 信息都会传给 agent</div>
</div>
</div>
</div>

`updatedInput` 是 last-one-wins 意味着 hook 的顺序有影响。如果 Hook A 加了 `--dry-run`，Hook B 加了 `--timeout 30`，只有 `--timeout 30` 生效。要两个都保留，得在一个 hook 里合并。

### Auto-Compact 也有 Circuit Breaker

压缩不是每次都成功。Claude Code 内置了 `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3`——连续失败 3 次就停止尝试。曾有 1,279 个 session 出现 50+ 次连续 compact 失败，浪费约 250K API 调用/天，之后加上了这个熔断。

Hook 依赖 compact 事件时要注意——circuit breaker 跳过 compact 时你的 hook 不触发。Context 持续膨胀，直到 API 返回 413 才触发 Reactive Compact——到那时候已经晚了。

### 前台重试、后台放弃

529（API overloaded）不是 429（你被限速了）。529 是服务端全局过载——你重试只会火上浇油。

Claude Code 的做法：前台请求遇 529 重试最多 3 次。后台请求——摘要、分类器、background compaction——遇 529 直接放弃，不重试。

Async hook 也是后台任务。`async: true` 的脚本失败了直接 `exit 0`，让 agent 继续。别在脚本里加 retry loop。系统最忙的时候，后台重试是压死骆驼的最后一根稻草。

---

## 已知限制

### Context 使用率无法精确获取

Claude Code 不向 hook 暴露 `context_window_size`。Hook 只能从 transcript 文件里读 `input_tokens` 的原始数值，但不知道总窗口大小，算不出百分比。

Ralph 本来想做"context >= 95% 时放行退出"的安全阀——做不了。只能依赖 Claude Code 自己的 reactive compaction 处理溢出。未来 hook API 暴露 window size 的话，这个阀可以补上。

### 模型切换是建议而非执行

Hook 不能切换模型。Pattern 5.6 的 `additionalContext` 只能说"考虑换个模型"。Agent 可以忽略。

在实际使用中，如果一个任务在 Sonnet 上连续失败 3 次，最有效的做法是你手动切到 Opus。Hook 能做的只是提醒你这件事。

### Doubt Gate 有误报

"should be"、"I think" 在代码注释和引用中也会匹配。脚本用 sed 过滤掉代码块和 blockquote，但不能完全消除误报。

One-shot guard 机制防止死循环：doubt gate 第一次触发时写一个 `.doubt-gate-fired` 文件，第二次 Stop 时读到这个文件直接放行。这保证了 doubt gate 最多触发一次——触发后 agent 去验证，验证完再次 Stop 时不会被同一个 gate 再拦一次。

### Denial Tracker 靠推断

Claude Code 没有"用户否决了工具调用"的专用 hook event。`denial-tracker.sh` 从 assistant 消息推断否决——检测 "I understand, I won't..." 之类的措辞。准确率取决于 agent 的回复风格。如果 agent 被否决后没有用这类措辞回复，tracker 会漏掉。

### Drift Re-anchoring 依赖外部设置

原始任务描述需要通过 `reanchor.json` 或 `original-task.md` 文件提前配置。如果你忘了初始化这个文件，re-anchoring 不会触发——按 M5 静默跳过。

这是一个 UX 问题：用户需要记住"开始大任务前先配 reanchor"。如果能从 Claude Code 的 session 元数据自动提取初始 prompt 就不需要这步，但当前 hook API 不暴露这个信息。

### Multi-Agent 全部是 Design Pattern

Multi-Agent 轴的 6 个 pattern 都是 design 类型，没有可执行脚本。

多 agent 编排差异太大。Coordinator 模式和 swarm 模式的实现完全不同；2 个 agent 和 20 个 agent 的协调方式不同；worktree 隔离取决于任务性质。硬编码一个脚本覆盖所有场景，要么太简陋，要么太复杂没人维护。

这个轴提供的价值是"怎么想"——什么时候用 coordinator、什么时候用 fork、file claim lock 的伪代码长什么样——而不是"复制这个脚本就行"。

---

## 反模式表

搭自己的 execution harness 时这 8 个坑最容易踩。

| # | 反模式 | 症状 | 怎么修 |
|---|--------|------|--------|
| 1 | **只用 prompt 不用 hook** | Agent 在 CLAUDE.md 里写了"不要重试超过 3 次"但实际重试了 8 次 | 简单规则用 hook 做（M1）。"不超过 3 次"= PostToolUseFailure 计数器 + PreToolUse blocker |
| 2 | **Enforcement 没有安全阀** | Agent 在 Stop hook 循环里卡死——无法退出，也无法完成任务 | 每个 block 机制必须有退出条件（M3）。最少加闲置超时和迭代上限 |
| 3 | **状态文件没有 session 隔离** | Session A 的错误计数影响了 Session B 的工具调用 | 所有状态文件路径包含 `session_id`（M4）。没有 session_id 的路径是 bug |
| 4 | **Hook 在异常时 block** | 新环境没有 session 目录，所有 hook 都拦截所有操作，agent 什么都干不了 | 默认 fail-open（M5）。`[ -f "$STATE_FILE" ] \|\| { echo '{"continue":true}'; exit 0; }` |
| 5 | **简单任务上全套 hook** | 改个 typo 触发了 Ralph + doubt gate + post-edit diagnostics，3 轮才结束 | 按任务复杂度选 hook（M6）。简单任务只保留 tool-input-guard |
| 6 | **只装 advisor 不装 tracker** | tool-error-advisor 永远读不到错误计数文件，永远不触发 block | 先部署观测再部署干预（M7）。tracker 和 advisor 必须成对安装 |
| 7 | **Coordinator 当邮局** | "Based on your findings, fix it" → worker 拿到原始数据不知道从何下手 | Coordinator 先消化、综合、判断，再委派（M9）。用 synthesis gate 强制这一步 |
| 8 | **假装能做实际做不到的事** | 文档说"hook 会自动切换模型"但实际 API 不支持，用户基于错误假设做决策 | 做不到就标 `[ADVISORY ONLY]`（M10）。静默失效比标注 advisory 更糟 |

---

## Sources

| 项目/文档 | 链接 | 贡献 |
|-----------|------|------|
| Harness Engineering | [github.com/wquguru/harness-books](https://github.com/wquguru/harness-books) | 10 条设计原则的理论框架 |
| Claude Reviews Claude | [github.com/openedclaude/claude-reviews-claude](https://github.com/openedclaude/claude-reviews-claude) | Claude Code 源码级架构分析 |
| ccunpacked.dev | [ccunpacked.dev](https://ccunpacked.dev/) | 工具全景、隐藏功能 |
| claude-howto | [github.com/luongnv89/claude-howto](https://github.com/luongnv89/claude-howto) | Hook 扩展点 API 教程 |
| Claude Code 源码 | 泄露的 TypeScript 源码 | 压缩机制、hook schema、session 管理内部实现 |
| ClawHub harness skills | 社区 skill 合集 | 实战 hook 脚本、踩坑记录、async timing 行为 |
| Anthropic Harness Engineering | [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 官方设计原则 |
| OpenAI Harness Engineering | [openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/) | 跨厂商验证 |
| Anthropic Multi-Agent Blog | Anthropic "Building multi-agent systems" blog | Coordinator synthesis 原则 |
| hermes-agent | [github.com/nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | IterationBudget 分阶段压力注入、自动模型切换、shadow git rollback |
| Execution Harness | [github.com/lanyasheng/execution-harness](https://github.com/lanyasheng/execution-harness) | 本项目 |

<!-- deslop score: 9.4/10, round 5 -->
