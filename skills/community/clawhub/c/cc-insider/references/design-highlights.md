# 设计亮点与调试

## 架构级设计亮点

| 设计 | 原理 | 价值 |
|------|------|------|
| buildTool defaults | fail-closed | 默认最严格，减少安全风险 |
| ToolUseContext | 单一执行状态对象 | 工具执行所需一切可注入 |
| contentReplacementState fork克隆 | 保证 fork 决策一致性 | 避免上下文分裂导致模型行为错乱 |
| readFileState LRU + loadedNestedMemoryPaths dedup | 性能+准确双保险 | 避免同一 CLAUDE.md 被多次注入 |
| renderedSystemPrompt 冻结 | 避免 GrowthBook 冷→热导致 cache bust | fork 时 prompt 描述可能变化导致 cache 失效 |
| Task ID 36进制+8字节随机 | 2.8 万亿组合 | 足够抵御 symlink 攻击 |
| maxResultSizeChars | 磁盘兜底 | 超过阈值写入磁盘而不是塞 context |
| Tool.shouldDefer | 延迟加载 | MCP 工具很多，全量加载不现实 |
| auto-background 15秒 | 平衡等待与阻塞 | 大多数命令完成，又不至于太久 |
| sed 模拟写入 | 预览确认后才执行 | 不可逆操作的安全保障 |
| sed \_simulatedSedEdit omit | 模型不能自己设置 | 防止模型构造任意文件写入 |
| Coordinator Synthesize-first | 不 delegation of understanding | 保证 Coordinator 真正理解问题后才给指令 |
| Hook if "no match → skip" | 复合命令逐子命令匹配 | 安全无死角 |
| lazySchema() | 延迟解析 | 避免模块加载时的循环依赖 |
| Generator for shell progress | 可 yield 多次 | shell 输出是流式的，Promise 只能返回一次 |

---

## 调试线索

### 命令卡住/无响应

```
排查步骤：
1. 检查是否有 `sleep N`（N≥2秒）模式
   → 建议用 Monitor 工具（事件驱动 vs 轮询）

2. 检查是否 45 秒无输出且像交互提示符
   → 通知已发给模型："命令可能在等交互输入"

3. 检查后台任务状态
   → ~/.claude/.task-output/{taskId}

4. 检查 auto-background 是否触发
   → 15秒超时自动后台化
```

### 权限异常

```
排查步骤：
1. 检查 ~/.claude/settings.json 中的 rules 配置
2. 检查 Hook 规则是否匹配（glob 模式）
3. 复合命令会 split 逐子命令匹配
4. 检查 sed _simulatedSedEdit 是否被 omit（安全关键）
```

### 上下文过大/爆 token

```
排查步骤：
1. 检查 contentReplacementState decisions
   → 哪些内容被标记为"太大"并替换为磁盘路径

2. 检查是否有大结果被写入磁盘
   → ~/.claude/.tool-results/{uuid}

3. Session 太长时会 compact（自动）
   → renderedSystemPrompt 冻结

4. 检查 CLAUDE.md 嵌套
   → loadedNestedMemoryPaths 防重
```

### MCP 工具不工作

```
排查步骤：
1. MCP 服务器连接状态：pending / connected / failed
2. AgentTool 等待机制：最多等 30 秒
3. requiredMcpServers 验证：连接≠认证通过
4. shouldDefer：是否被 ToolSearch 激活
```

---

## 常见问题 Q&A

**Q: 为什么要用 36 进制生成 Task ID？**
A: 36进制（0-9 + a-z）让 ID 更短（8字节→约13字符），同时避免混淆（没有大写 O/l）。足够抵御 symlink 攻击（2.8 万亿组合）。

**Q: fork 为什么要克隆 contentReplacementState？**
A: 如果 fork 和父进程对同一 tool result 做出不同的"太大"判断，父进程收到 preview，子进程收到全文，导致上下文不一致。

**Q: sed 为什么要模拟写入而不是直接执行？**
A: 如果直接执行 sed，用户拒绝权限后修改已发生不可逆。_simulatedSedEdit 让用户预览确认后才真正写入。

**Q: 为什么 MCP 工具默认 shouldDefer？**
A: MCP 服务器可能有成百上千个工具，第一轮全量加载 system prompt 会爆 token budget。延迟加载让 ToolSearch 按需触发。

**Q: auto-background 为什么是 15 秒？**
A: 15秒足够让大多数命令完成或产生可见输出，又不至于阻塞主 agent 太长时间。太长→用户等待焦虑，太短→很多命令被后台化。

**Q: 为什么 hook 的 if 是"no match → skip"而不是"match 才执行"？**
A: 因为复合命令（ls && git push）需要逐子命令匹配。如果整条命令匹配才执行，ls 不会触发 hook，但 ls 本身可能是危险的。

**Q: LocalShellTask 为什么用 generator 函数而不是 Promise？**
A: Generator 可以 yield 多次进度（每条输出都 yield），Promise 只能返回一次。shell 命令的输出是流式的，需要多次 yield。

**Q: 为什么 BashTool.outputSchema 里的 stderr 永远为空字符串''？**
A: 因为 stderr 已经 merge 到 stdout 里了（shell 的 2>&1）。分开返回会造成信息丢失和 UI 渲染不一致。
