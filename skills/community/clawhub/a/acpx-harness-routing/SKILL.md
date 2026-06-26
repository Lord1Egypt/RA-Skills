# ACPX Harness Routing

## 原则

当任务明确属于 harness / Claude / Codex / Gemini ACPX 调度任务时，**必须强制套用本 skill**。

组织方式遵循：
1. 先原则
2. 再判断路径
3. 再执行细则

目标只有一个：
- 用最少分叉、最稳的方式，把总控 agent 对 harness 的调度做成可复用工作法

---

## 一句话规则

- **harness 任务必须用本 skill**
- **one-shot：默认 ACP runtime**
- **连续任务：默认 direct acpx named session**
- **Claude：技术架构 / 技术方案**
- **Codex：需求分析 / 代码实现**
- **Gemini：交叉验证 / 第二视角**
- **只要底层走 acpx / harness，就必须落实“全部批准、不等待交互输入”**
- **用户指定优先于默认规则**

---

## 判断树

### 第一步：先判断是否属于 harness 任务
属于以下情况时，直接进入本 skill：
- 需要调度 Claude / Codex / Gemini 做分析、实现、验证
- 需要通过 ACP runtime 或 direct acpx 调用 harness
- 需要 one-shot 或连续多轮 harness 工作流

不属于以上情况时，不用本 skill。

---

### 第二步：选角色
默认分工：
- **Claude**：技术架构、技术方案、结构化技术分析
- **Codex**：需求分析、代码实现
- **Gemini**：交叉验证、第二视角、多文件快速综合

若用户明确指定角色，则覆盖默认分工。

---

### 第三步：选调用路径

#### A. one-shot 任务
默认走：
```text
sessions_spawn(runtime="acp", agentId="claude|codex|gemini", mode="run", ...)
```

适用：
- 单轮分析
- 单轮方案
- 单轮需求分析
- 单轮代码实现
- 单轮验证
- 一次性文件生成

#### B. 连续任务 / 多轮任务
默认走：
```text
direct acpx named session
```

适用：
- 需要连续承接上下文
- 需要同一个 harness 连续几轮工作
- 需要显式控制 session / cwd / timeout / 审批行为

当前约束：
- Telegram 入口下，ACP runtime 的 `thread=true` 不可用
- `mode="session"` 依赖 `thread=true`
- 所以当前 Telegram 总控入口，不把 ACP runtime session 作为连续任务主路径

---

## 硬规则

### 1. 审批与交互规则（强制）
无论是 one-shot 还是 long-run，只要底层走的是 acpx / harness 调度，都必须显式确保采用：
- 全部批准
- 非交互不等待输入

尤其 direct acpx 调用时，默认必须带：

```bash
--approve-all --non-interactive-permissions deny
```

这是强制规则，不能省略。

原因：
过去大量“超时 / 不返回 / 卡住”的情况，根因不是 Claude / Codex 不可用，而是没有显式带上这组参数，导致 harness 在非交互环境里等待输入或反馈。

一句话：
- **只要是 acpx harness 调度，就必须把“全部批准、不等待交互输入”落实到调用参数上。**

---

### 2. 连续会话规则（强制）
连续任务默认走 direct acpx named session，并遵守以下铁律：

#### 铁律 1：创建 / ensure session 时必须显式带 `--cwd`
错误：
```bash
acpx claude sessions ensure --name oc-claude-xxx
```

正确：
```bash
acpx --cwd /path/to/workspace claude sessions ensure --name oc-claude-xxx
```

#### 铁律 2：后续调用必须保持同一 `--cwd`
否则会出现：
- session 找不到
- session 绑错目录
- 连续性失效

#### 铁律 3：session 名统一
默认建议：
- `oc-claude-<conversationId>`
- `oc-codex-<conversationId>`
- `oc-gemini-<conversationId>`

若没有稳定 conversationId，则退化为：
- `oc-<agent>-<taskSlug>-<date>`

---

### 3. 超时规则
默认采用翻倍后的档位：
- 小任务：180
- 中任务：360
- 大任务：600~1200

说明：
- timeout 是上限，不是必须等满
- 任务完成即返回

---

## 执行模板

把 harness 当作执行型 worker，不当作闲聊对象。

任务描述默认使用四段：
1. 目标
2. 边界
3. 输出物
4. 约束

模板：

```text
目标：
<要完成什么>

边界：
<允许看哪里 / 改哪里 / 不准碰什么>

输出物：
<最终要产出什么文件/结论>

约束：
<风格、实现方式、完成后回复格式>
```

---

## 已验证事实

### 已验证通过
1. OpenClaw ACP runtime one-shot 可用
2. direct acpx Claude 可用
3. direct acpx Codex 可用
4. Claude / Codex 可真实写文件
5. direct acpx named session 连续承接可用

### 已验证限制
1. Telegram 入口不支持 ACP `thread=true` thread spawn
2. `mode="session"` 依赖 `thread=true`
3. Telegram 总控入口当前不适合用 ACP runtime 做连续 thread session

---

## 最终落地规则

如果你只记住三件事，就记住这三件事：

1. **harness 任务必须先进入本 skill**
2. **one-shot 走 ACP runtime，连续任务走 direct acpx named session**
3. **只要走 acpx / harness，就必须把“全部批准、不等待交互输入”落实到参数里**
