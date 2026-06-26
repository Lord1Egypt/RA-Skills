# 从 GENERIC 到 POWERFUL：一套让 Skill 自动变好的评估和改进系统

> 11 个管线 skill + 2 个辅助工具，20000 行 Python，397 个测试。
> 各 skill 已独立发布到 ClawHub（如 `openclaw skills install improvement-learner`），完整仓库见 [GitHub](https://github.com/lanyasheng/auto-improvement-orchestrator-skill)。

**TL;DR**

结构评分和执行效果 R²=0.00——SKILL.md 写得再漂亮，跟 AI 能不能做对事没有任何统计关系。Skill 的价值是注入项目知识，不是让模型变聪明，但注入有代价：旧的失败修好了，新的失败冒出来。Pareto front 是 98 行 Python 写的，拦住了至少三个 skill 不被"优化"搞坏——加权总分会藏住维度退步，逐维度守底线才安全。先有评估再做改进，反过来一切白搭。agent 跑长任务会自己停（40% 的 session 提前终止），Ralph Stop Hook 拦住它让它继续干。

---

## R²=0.00——改了 Skill 之后怎么知道是变好了还是变差了

我搭了一套系统来评估和自动改进 Skill——先写了个评分器，九个维度打分，4 个评审角色按 skill 类别差异化权重。28 个 skill 跑了一遍。分布合理。

然后我拿真实任务验证了一下。

**结构评分和实际执行效果的相关系数是 R² = 0.00。**

不是接近零，是字面意义上的零。SKILL.md 写得再漂亮——frontmatter 完整、When to Use 齐全、示例代码丰富——跟 AI 能不能在真实场景下正确执行，**没有任何统计关系**。一个评分 0.88 的 skill 反而比评分 0.70 的执行更差。

**目前市面上所有基于文档结构打分的 skill 评估方案，包括 ClawHub 的 skill-quality-check、PromptFoo 的 assertion 检查，从根本上就测错了东西。** 测的是"文档卫生"，不是"指导质量"。

我原来的思路全错了。不能只检查文档写得好不好，得让 AI 真正拿着 SKILL.md 去跑任务，看它能不能做对。做不对的信息反馈回来，自动改 SKILL.md，再跑，再验证，直到它好使为止。

背景补一句：OpenClaw 生态的 Skill 已经上万（VoltAgent 精选集 5000+），团队内部也有几十个。写不难，难的是改完判断效果——手动试几次、凭感觉觉得"还行"，规模上来后不够用了。

搭的过程比结果有意思。

## 偷师：从蒸馏别人的仓库开始

Claude Code 的 Skill 就是一个 SKILL.md 文件加几个脚本，告诉 AI 遇到特定任务该怎么干。GitHub 上有人整理了不错的合集：alirezarezvani/claude-skills 有 10 个质量模式，affaan-m/everything-claude-code 搞了 116 个 skill 的架构。我不想从零写，想拿来改改用。

手动抄一两个没问题。但 skill 一多（我陆续看中了三四十个），一个个搬就烦了。我写了个 skill-distill 工具，喂进去 N 个功能有重叠的 skill，它把知识分成交集、独有、冲突、冗余四类，让你确认合并方案，然后吐出一个蒸馏版。

### 蒸馏案例：deslop（反 AI 味写作）

GitHub 上有两个相关 skill：slopbuster（280 行，英文为主，覆盖学术/代码/散文三种模式）和 humanizer（559 行，偏通用文本去 AI 痕迹）。两个 skill 有大量重叠：都列了 AI 高频词表，都有评分量表，都做模式替换。但 slopbuster 有代码注释专用模式，humanizer 有更细的语气校准。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="border-radius:12px;padding:20px;background:#f8fafc;border:1px solid #e2e8f0">
<div style="font-size:12px;font-weight:700;color:#334155;letter-spacing:1px;margin-bottom:14px">🧪 deslop 蒸馏过程</div>
<div style="display:flex;gap:8px;margin-bottom:12px">
<div style="flex:1;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:12px;text-align:center">
<b>slopbuster</b><br/><span style="font-size:11px;color:#666">280 行 | 英文为主<br/>学术/代码/散文三模式</span>
</div>
<div style="flex:1;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:12px;text-align:center">
<b>humanizer</b><br/><span style="font-size:11px;color:#666">559 行 | 通用文本<br/>voice calibration</span>
</div>
<div style="flex:1;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:12px;text-align:center">
<b>中文写作笔记</b><br/><span style="font-size:11px;color:#666">手写 | 四字堆砌<br/>被动过多、企业套话</span>
</div>
</div>
<div style="text-align:center;margin:8px 0">
<span style="display:inline-block;background:#e9d5ff;border:1px solid #c4b5fd;border-radius:8px;padding:8px 16px">
<b>skill-distill</b>：交集去重 / 独有保留 / 冲突手动裁决
</span>
</div>
<div style="text-align:center;color:#999;margin:4px 0">↓</div>
<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:12px;text-align:center">
<b style="color:#16a34a">deslop</b><br/>
<span style="font-size:11px;color:#666">221 行 SKILL.md + 561 行 references<br/>
中英文覆盖 | 两次 pass（去模式→注灵魂）| 20+ AI 模式检测表</span>
</div>
<div style="margin-top:10px;font-size:11px;color:#666">
<b>交集</b>：AI 词汇表、评分标准 → 合并去重进 body<br/>
<b>独有</b>：slopbuster 代码模式 → "不适用场景"指向原 skill；humanizer voice calibration → references/<br/>
<b>冲突</b>：em dash 容忍度不同 → 弹出让我手动选
</div>
</div>
</div>

这篇文章本身就是用 deslop 从 7.5 分改到 8.4 分的。

### 蒸馏案例：execution-harness（agent 全链路执行可靠性）

这个 skill 比"agent 不要半路停"大得多。它管 dispatched agent 从生到死的四件事：启动时初始化状态、跑的时候保持 context 不丢、出错了怎么升级恢复、结束后清理状态和合并记忆。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="border-radius:12px;padding:20px;background:#f8fafc;border:1px solid #e2e8f0">
<div style="font-size:12px;font-weight:700;color:#334155;letter-spacing:1px;margin-bottom:14px">🔧 蒸馏来源（6 个源 → v1.0 21 个 pattern → v2.0 38 个 pattern）</div>
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px">
<div style="flex:1;min-width:140px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:10px">
<b style="font-size:11px">claude-reviews-claude</b><br/><span style="font-size:10px;color:#666">17 篇架构文章<br/>→ Handoff 文档、Compaction 提取</span>
</div>
<div style="flex:1;min-width:140px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:10px">
<b style="font-size:11px">OMC (npm 源码)</b><br/><span style="font-size:10px;color:#666">→ Ralph Stop hook、Cancel TTL<br/>⚠️ headless 模式不触发</span>
</div>
<div style="flex:1;min-width:140px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:10px">
<b style="font-size:11px">ccunpacked.dev</b><br/><span style="font-size:10px;color:#666">Claude Code 拆解<br/>→ Context 估算、四级压缩</span>
</div>
<div style="flex:1;min-width:140px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:10px">
<b style="font-size:11px">claude-howto</b><br/><span style="font-size:10px;color:#666">实践 tips<br/>→ 工具错误升级、权限否决</span>
</div>
<div style="flex:1;min-width:140px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:10px">
<b style="font-size:11px">ClawHub 社区</b><br/><span style="font-size:10px;color:#666">harness-engineer 等<br/>→ Doubt Gate、Hook Profiles</span>
</div>
<div style="flex:1;min-width:140px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:10px">
<b style="font-size:11px">Anthropic 官方</b><br/><span style="font-size:10px;color:#666"><a href="https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents">harness engineering</a><br/>→ executor/grader 分离</span>
</div>
</div>
</div>
</div>

Anthropic 官方的 [harness engineering](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 也贡献了几个关键 pattern：executor/grader 分离、长任务外部记忆、hook bracket 测量。

初版蒸馏出 21 个 pattern。后来在实际使用中不断补充，v2.0 扩展到 **38 个 pattern，6 个轴**（每个轴是一个独立的子 skill）：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="border-radius:12px;padding:20px;background:#f8fafc;border:1px solid #e2e8f0">
<div style="font-size:12px;font-weight:700;color:#334155;letter-spacing:1px;margin-bottom:14px">⚙️ execution-harness v2.0：38 个 pattern × 6 轴</div>

<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px">
<div style="flex:1;min-width:160px;background:#eff6ff;border:1px solid #93c5fd;border-radius:8px;padding:10px">
<b style="color:#2563eb">execution-loop</b><br/>
<span style="font-size:11px;color:#666">Ralph Stop hook<br/>Doubt Gate<br/>Cancel TTL</span><br/>
<span style="font-size:10px;background:#dbeafe;border-radius:4px;padding:2px 6px">提前停止、投机性完成</span>
</div>
<div style="flex:1;min-width:160px;background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:10px">
<b style="color:#16a34a">context-memory</b><br/>
<span style="font-size:11px;color:#666">Handoff 文档<br/>Compaction Extract<br/>Token Budget</span><br/>
<span style="font-size:10px;background:#dcfce7;border-radius:4px;padding:2px 6px">压缩丢信息、token 超预算</span>
</div>
<div style="flex:1;min-width:160px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:10px">
<b style="color:#dc2626">error-recovery</b><br/>
<span style="font-size:11px;color:#666">Rate Limit Recovery<br/>Model Fallback<br/>Crash Resume</span><br/>
<span style="font-size:10px;background:#fee2e2;border-radius:4px;padding:2px 6px">限速、降级、crash 恢复</span>
</div>
</div>
<div style="display:flex;gap:8px;flex-wrap:wrap">
<div style="flex:1;min-width:160px;background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:10px">
<b style="color:#a16207">tool-governance</b><br/>
<span style="font-size:11px;color:#666">Error Escalation<br/>Permission Denial<br/>Destructive Op Guard</span><br/>
<span style="font-size:10px;background:#fef9c3;border-radius:4px;padding:2px 6px">工具死循环、权限否决</span>
</div>
<div style="flex:1;min-width:160px;background:#faf5ff;border:1px solid #c4b5fd;border-radius:8px;padding:10px">
<b style="color:#7c3aed">multi-agent</b><br/>
<span style="font-size:11px;color:#666">Coordinator/Fork/Swarm<br/>Hook Profiles<br/>Scoped Hooks</span><br/>
<span style="font-size:10px;background:#ede9fe;border-radius:4px;padding:2px 6px">并行调度、协调模式</span>
</div>
<div style="flex:1;min-width:160px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px">
<b style="color:#334155">quality-verification</b><br/>
<span style="font-size:11px;color:#666">Post-Edit Diagnostics<br/>Hook Bracket<br/>Session Metrics</span><br/>
<span style="font-size:10px;background:#f1f5f9;border-radius:4px;padding:2px 6px">编辑后检查、指标测量</span>
</div>
</div>

<div style="margin-top:12px;padding:10px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;font-size:11px">
⚠️ <b>踩坑</b>：OMC 的 Ralph 有个文档没写的细节：<b>只在 interactive 模式下工作</b>，headless <code>-p</code> 模式的 Stop hook 不触发。在源码里花了两个小时才确认。
</div>
<div style="margin-top:6px;font-size:11px;color:#666">质量分从 0.63 升到 0.93。来源跨越博客、npm 源码、技术拆解网站、tips 集合、ClawHub 社区 skill 五种格式。</div>
</div>
</div>

## 整体架构：三层流水线

11 个管线 skill 分三层（评估→改进→控制），另外 skill-forge 和 skill-distill 是辅助工具（造 skill 和合并 skill）。管线跑通后拿 prompt-hardening、deslop、release-notes、code-review 等多个 skill 做过验证——文章后面的数据来自这些验证。prompt-hardening 在仓库内，deslop 单独维护（ClawHub: [deslop-cn](https://clawhub.com/lanyasheng/deslop-cn)）。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">

<div style="display:flex;gap:12px;margin-bottom:16px">
<div style="flex:1;border-radius:12px;padding:16px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:11px;font-weight:700;color:#16a34a;letter-spacing:1px;margin-bottom:10px">📊 评估层（三信号）</div>
<div style="display:flex;gap:8px">
<div style="flex:1;background:#fff;border:1px solid #bbf7d0;border-radius:8px;padding:10px;text-align:center">
<b>learner</b><br/><span style="color:#666;font-size:11px">结构 lint<br/>$0.5/次<br/>9维 + LLM judge</span>
</div>
<div style="flex:1;background:#fff;border:1px solid #bbf7d0;border-radius:8px;padding:10px;text-align:center">
<b>evaluator</b><br/><span style="color:#666;font-size:11px">执行测试<br/>$3-5/次<br/>claude -p 真实调用</span>
</div>
<div style="flex:1;background:#fff;border:1px solid #bbf7d0;border-radius:8px;padding:10px;text-align:center">
<b>session-feedback</b><br/><span style="color:#666;font-size:11px">用户隐式反馈<br/>$0<br/>JSONL 解析</span>
</div>
</div>
</div>
</div>

<div style="text-align:center;color:#999;margin:4px 0;font-size:18px">↓ 信号汇入 ↓</div>

<div style="border-radius:12px;padding:16px;background:#eff6ff;border:1px solid #93c5fd;margin-bottom:16px">
<div style="font-size:11px;font-weight:700;color:#2563eb;letter-spacing:1px;margin-bottom:10px">🔄 改进层（5 阶段流水线 + trace-aware 重试）</div>
<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">
<div style="background:#fff;border:1px solid #bfdbfe;border-radius:8px;padding:8px 12px;text-align:center"><b>generator</b><br/><span style="font-size:10px;color:#666">生成候选</span></div>
<div style="color:#999">→</div>
<div style="background:#fff;border:1px solid #bfdbfe;border-radius:8px;padding:8px 12px;text-align:center"><b>discriminator</b><br/><span style="font-size:10px;color:#666">4种打分</span></div>
<div style="color:#999">→</div>
<div style="background:#fff;border:1px solid #bfdbfe;border-radius:8px;padding:8px 12px;text-align:center"><b>evaluator*</b><br/><span style="font-size:10px;color:#666">跑真实任务</span></div>
<div style="color:#999">→</div>
<div style="background:#fff;border:1px solid #bfdbfe;border-radius:8px;padding:8px 12px;text-align:center"><b>executor</b><br/><span style="font-size:10px;color:#666">应用+备份</span></div>
<div style="color:#999">→</div>
<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:8px 12px;text-align:center"><b style="color:#dc2626">gate</b><br/><span style="font-size:10px;color:#666">6层门禁</span></div>
</div>
<div style="margin-top:8px;padding:8px;background:#fefce8;border:1px solid #fde68a;border-radius:8px;font-size:11px">
↩️ <b>Ralph Wiggum 重试</b>：gate=revert → 提取 failure trace → 注入 generator → 跳过已失败3次的策略 → 重试<br/>
<span style="color:#666">* evaluator 对低风险 docs 类候选自动跳过（adaptive complexity）</span>
</div>
</div>

<div style="text-align:center;color:#999;margin:4px 0;font-size:18px">↓ keep / pending / reject ↓</div>

<div style="display:flex;gap:12px">
<div style="flex:1;border-radius:12px;padding:16px;background:#faf5ff;border:1px solid #c4b5fd">
<div style="font-size:11px;font-weight:700;color:#7c3aed;letter-spacing:1px;margin-bottom:10px">⚙️ 控制层</div>
<div style="display:flex;gap:8px">
<div style="flex:1;background:#fff;border:1px solid #ddd6fe;border-radius:8px;padding:10px;text-align:center">
<b>autoloop</b><br/><span style="color:#666;font-size:11px">连续跑<br/>5种终止条件<br/>handoff 文档</span>
</div>
<div style="flex:1;background:#fff;border:1px solid #ddd6fe;border-radius:8px;padding:10px;text-align:center">
<b>benchmark-store</b><br/><span style="color:#666;font-size:11px">Pareto front<br/>质量分级<br/>per-dim 容差</span>
</div>
<div style="flex:1;background:#fff;border:1px solid #ddd6fe;border-radius:8px;padding:10px;text-align:center">
<b>execution-harness</b><br/><span style="color:#666;font-size:11px">38 patterns × 6 轴<br/>Ralph/Handoff<br/>独立仓库</span>
</div>
</div>
</div>
</div>

</div>

### Skill 速查

每个 skill 做什么、数据怎么流转：

| # | 层 | Skill | 做什么 | 关键输出 |
|---|:--:|-------|--------|---------|
| ① | 评估 | **learner** | 9 维结构评分（accuracy 用 LLM judge，其余代码检查），4 角色加权 | `{accuracy: 0.83, tier: "SOLID"}` |
| ② | 评估 | **evaluator** | 拿 SKILL.md 让 `claude -p` 真跑任务，三种 judge（关键词/pytest/LLM） | `{pass_rate: 0.86}` |
| ③ | 评估 | **session-feedback** | 从会话日志挖用户纠正信号，算 correction_rate | `feedback.jsonl` |
| ④ | 改进 | **generator** | 读反馈 + failure trace，生成改进候选，失败 3 次自动跳过 | `candidates.json` |
| ⑤ | 改进 | **discriminator** | 4 种打分叠加，DISPUTED 进人工队列 | `ranking.json` |
| ⑥ | 改进 | **executor** | 应用候选到文件，自动备份，支持 `--dry-run` | `execution.json` |
| ⑦ | 改进 | **gate** | 6 层门禁，Pareto per-dim 容差 | `decision: keep/revert` |
| ⑧ | 改进 | **orchestrator** | 串联 ④→⑤→②→⑥→⑦，失败时提取 trace 重试 | `pipeline-summary.json` |
| ⑨ | 控制 | **autoloop** | 外层循环，5 种终止条件，crash 后自动恢复 | `autoloop_state.json` |
| ⑩ | 控制 | **benchmark-store** | Pareto front + 质量分级 | regression check |
| ⑪ | 控制 | **execution-harness** | 38 pattern × 6 轴，v2.0 [独立仓库](https://github.com/lanyasheng/execution-harness) | — |
| | *工具* | **skill-forge** | 从 spec 生成 skill + task_suite.yaml | skill 目录 |
| | *工具* | **skill-distill** | N 个重叠 skill → 1 个蒸馏版 | 蒸馏后 skill |
| | *验证* | **prompt-hardening** | 16 个 prompt 强化模式，evaluator 的 A/B 测试目标 | — |
| | *外部* | **deslop** | 反 AI 味两次 pass，不在本仓库，ClawHub: [deslop-cn](https://clawhub.com/lanyasheng/deslop-cn) | — |

### 一次完整改进的数据流

一个 skill 从评估到改进完成，数据经过这些节点：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="border-radius:12px;padding:20px;background:#f8fafc;border:1px solid #e2e8f0">
<div style="font-size:12px;font-weight:700;color:#334155;margin-bottom:12px">📦 数据流示例：改进 release-notes skill</div>
<div style="font-size:11px;line-height:1.8">
<b>1.</b> <code>learner</code> 读 SKILL.md → 发现 accuracy=0.68（缺 module mapping）→ 弱维度信息写入 state<br/>
<b>2.</b> <code>session-feedback-analyzer</code> 读会话日志 → 发现 release-notes 被用户纠正 5 次，4 次在 accuracy 维度 → <code>feedback.jsonl</code><br/>
<b>3.</b> <code>generator</code> 读 state + feedback.jsonl + 历史 trace → 生成 3 个候选（加 module mapping 表 / 补 example / 加 guardrail）→ <code>candidates.json</code><br/>
<b>4.</b> <code>discriminator</code> 打分 → 候选 1 得分 7.2（accept），候选 2 得分 5.8（hold），候选 3 得分 4.1（reject）→ <code>ranking.json</code><br/>
<b>5.</b> <code>evaluator</code> 跑 7 个 task → 候选 1 通过率 86%（baseline 也是 86%，但失败的任务不同了，模块分类修好了）→ <code>evaluation.json</code><br/>
<b>6.</b> <code>executor</code> 应用候选 1 → 备份原文件 → 写 diff → <code>execution.json</code><br/>
<b>7.</b> <code>gate</code> 6 层检查 → Schema ✅ Compile ✅ Lint ✅ Regression ✅ Review ✅ Human ✅ → <code>decision: keep</code><br/>
<b>8.</b> <code>benchmark-store</code> 记录新分数到 Pareto front → <code>release-notes: SOLID (0.831)</code>
</div>
</div>
</div>

## R²=0.00 的细节：为什么结构评分预测不了执行效果

开头提到 R²=0.00，这里展开讲数据。

learner 的 9 个评分维度：

| 维度 | 检查什么 | 备注 |
|------|---------|------|
| coverage | SKILL.md 该有的段落有没有（When to Use、example、Output…） | 只看内容，不看项目结构 |
| completeness | 项目工件（scripts/tests/references）| 按 category 差异化：tool 类要 scripts+tests，knowledge 类要 references 深度 |
| accuracy | 指令质量——AI 拿着它能不能做对事 | 默认 LLM-as-Judge，$0.5/次 |
| reliability | 有没有测试、脚本能不能跑 | 纯指令型 skill 默认满分 |
| efficiency | 不冗余、长文用 references/ 做渐进式展开 | |
| security | 没有硬编码密钥、没有危险模式 | |
| trigger_quality | frontmatter 描述够不够准、触发词清不清晰 | |
| leakage | 没有内部路径、内部工具名泄漏 | |
| knowledge_density | 每个知识单元有没有足够深度 | |

权重分两层。第一层是 4 个评审角色，各有侧重——user 最看重 trigger_quality（能不能找到这个 skill），developer 最看重 reliability（有没有测试），security_auditor 最看重 security+leakage，architect 最看重 knowledge_density。第二层是类别修正：tool 类 skill 被 developer 评审时，reliability 的基础权重 0.20 乘以 1.5 倍修正系数，归一化后约 0.26，占比明显上升。knowledge 类 skill 的 completeness 权重乘以 0.6——因为 knowledge 类没有 scripts/ 是正常的，不该因此扣分。

4 个角色独立打分。tier 判定一致就是 CONSENSUS，分歧就是 DISPUTED，进人工队列。

28 个 skill 跑了一遍，零个达到 POWERFUL（>= 85%）。

然后我做了一件关键的事：拿真实任务验证。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="display:flex;gap:16px">
<div style="flex:1;border-radius:12px;padding:20px;background:#fef2f2;border:1px solid #fca5a5">
<div style="font-size:12px;font-weight:700;color:#dc2626;letter-spacing:1px;margin-bottom:14px">📊 结构评分 vs 执行通过率</div>
<table style="width:100%;border-collapse:collapse;font-size:12px">
<tr style="border-bottom:1px solid #fecaca"><td style="padding:6px"><b>Skill</b></td><td style="padding:6px">Learner 分</td><td style="padding:6px">执行通过率</td></tr>
<tr style="background:#fff"><td style="padding:6px">skill-creator</td><td style="padding:6px">0.715</td><td style="padding:6px;color:#16a34a"><b>100% ✓</b></td></tr>
<tr><td style="padding:6px">deslop</td><td style="padding:6px">0.754</td><td style="padding:6px;color:#16a34a"><b>100% ✓</b></td></tr>
<tr style="background:#fff"><td style="padding:6px">improvement-gate</td><td style="padding:6px">0.754</td><td style="padding:6px;color:#dc2626"><b>71% ✗</b></td></tr>
<tr><td style="padding:6px">skill-distill</td><td style="padding:6px">0.756</td><td style="padding:6px">86%</td></tr>
<tr style="background:#fff"><td style="padding:6px">prompt-hardening</td><td style="padding:6px"><b>0.802</b></td><td style="padding:6px">86%</td></tr>
</table>
<div style="margin-top:12px;padding:10px;background:#fef2f2;border:1px solid #f87171;border-radius:8px">
<b style="color:#dc2626">R² = 0.00 &nbsp;|&nbsp; r = -0.40（反向！）</b><br/>
<span style="color:#666;font-size:11px">learner 分越高 → 执行通过率越低。分数最高的 prompt-hardening (0.802) 执行反而不是最好的。</span>
</div>
</div>

<div style="flex:1;border-radius:12px;padding:20px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:12px;font-weight:700;color:#16a34a;letter-spacing:1px;margin-bottom:14px">🔍 26 个检查项拆解</div>
<div style="background:#fff;border:1px solid #bbf7d0;border-radius:8px;padding:12px;margin-bottom:8px">
<b>17/26 零方差</b><br/>
<span style="color:#666;font-size:11px">所有 skill 都通过 → 无法区分好坏</span>
</div>
<div style="background:#fff;border:1px solid #bbf7d0;border-radius:8px;padding:12px;margin-bottom:8px">
<b>6/26 有区分度</b><br/>
<span style="color:#666;font-size:11px">有正有负，但不稳定</span>
</div>
<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:12px">
<b style="color:#dc2626">3/26 反向预测</b><br/>
<span style="color:#666;font-size:11px">• version 字段 (r=-0.76)<br/>• references 目录 (r=-0.54)<br/>• 示例含 I/O (r=-0.54)<br/>通过 → 实际执行更差</span>
</div>
<div style="margin-top:12px;padding:10px;background:#f0fdf4;border:1px solid #86efac;border-radius:8px;font-size:11px">
<b>结论</b>：不是"结构不重要"，而是"检查测错了东西"。最用心维护 frontmatter 的人，可能把精力花在了文档美化而不是指令质量上。
</div>
</div>
</div>
</div>

### 从 regex 到 LLM-as-Judge

最早的 accuracy 评估用 regex 做。检查"有没有代码示例"就是 grep 一下有没有 ``` 代码块。这个做法的问题：一个 skill 可以有 10 个代码块但全是语法展示（`python3 script.py --flag`），没有一个展示输入→输出的完整示例。regex 检查通过，但质量其实很差。

换成 LLM-as-Judge 后，accuracy 检查变成了把 SKILL.md 发给 Claude，让它从 5 个维度打分：clarity、specificity、completeness、actionability、differentiation。

成本从 $0（regex）涨到 ~$0.5/eval，区分度确实上来了。17/26 零方差的问题消失了。

但 R² 还是 0.00。

问题不在方法上。"文档质量"和"指导质量"就是两件事——文档写得好让人觉得专业，但 AI 执行的时候根本不在乎你的 frontmatter 有没有 version 字段。这个认知花了很久才接受。

### 三个信号比一个总分靠谱

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0">
<div style="display:flex;gap:8px">
<div style="flex:1;background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:12px;text-align:center">
<b>learner</b><br/><span style="font-size:11px;color:#666">结构 lint | $0.5/次<br/>R²=0.00 vs 执行</span>
</div>
<div style="flex:1;background:#eff6ff;border:1px solid #93c5fd;border-radius:8px;padding:12px;text-align:center">
<b>evaluator</b><br/><span style="font-size:11px;color:#666">执行测试 | $3-5/次<br/>claude -p 真实调用</span>
</div>
<div style="flex:1;background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:12px;text-align:center">
<b>session-feedback</b><br/><span style="font-size:11px;color:#666">用户隐式反馈 | $0<br/>correction_rate</span>
</div>
</div>
<div style="text-align:center;margin:6px 0;font-size:11px;color:#999">三个信号分别输入 → Pareto front（learner+evaluator） / generator（feedback hotspot）</div>
</div>

### Task Suite 执行测试

执行层是真金白银。task suite 格式：

```yaml
skill_id: "release-notes-generator"
tasks:
  - id: "leakage-01"
    description: "iOS notes must not contain Android keywords"
    judge:
      type: "llm-rubric"
      rubric: |
        Check output does NOT contain "Kotlin", "Android", "Java".
        Score 1.0 if clean, 0.0 if any leakage.
      pass_threshold: 0.8
```

三种 judge：ContainsJudge（关键词检查）、PytestJudge（pytest 验证）、LLMRubricJudge（语义评分）。

### Skill 到底有没有用？

prompt-hardening skill 的 7 个任务，加载 skill 和裸跑 Claude 的通过率一样（都是 86%），但挂的任务不同：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="display:flex;gap:16px">
<div style="flex:1;border-radius:12px;padding:16px;background:#eff6ff;border:1px solid #93c5fd">
<div style="font-size:12px;font-weight:700;color:#2563eb;letter-spacing:1px;margin-bottom:10px">🔵 裸跑 Claude（无 Skill）— 86% 通过</div>
<div style="display:flex;gap:4px;flex-wrap:wrap">
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">P1 ✅</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">P5 ✅</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">审计格式 ✅</span>
<span style="background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:4px 8px;font-size:11px"><b>CLI路径 ❌</b></span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">模式 ✅</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">可靠性 ✅</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">端到端 ✅</span>
</div>
<div style="margin-top:8px;font-size:11px;color:#666">失败原因：不知道 audit.sh 的路径（训练数据里没有）</div>
</div>

<div style="flex:1;border-radius:12px;padding:16px;background:#faf5ff;border:1px solid #c4b5fd">
<div style="font-size:12px;font-weight:700;color:#7c3aed;letter-spacing:1px;margin-bottom:10px">🟣 加载 Skill — 也是 86% 通过</div>
<div style="display:flex;gap:4px;flex-wrap:wrap">
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">P1 ✅</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">P5 ✅</span>
<span style="background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:4px 8px;font-size:11px"><b>审计格式 ❌</b></span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">CLI路径 ✅</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">模式 ✅</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">可靠性 ✅</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px;font-size:11px">端到端 ✅</span>
</div>
<div style="margin-top:8px;font-size:11px;color:#666">失败原因：Skill 改变了输出偏好，省略了 /16 后缀</div>
</div>
</div>
<div style="margin-top:8px;padding:10px;background:#fefce8;border:1px solid #fde68a;border-radius:8px;font-size:12px">
<b>通过率一样，但失败的任务不同。</b> Skill 的价值在注入项目特定知识（audit.sh 路径），不是让 Claude 变聪明。但注入知识有代价，注意力分配变了，新的失败模式出现了。所以<b>评估不能只看聚合通过率</b>，得跟踪逐任务的 pass/fail 变化。
</div>
</div>

### 从会话日志挖用户纠正信号

task suite 测的是作者预设的场景。用户在真实使用中遇到的问题，task suite 未必覆盖。session-feedback-analyzer 从 Claude Code 的会话日志里挖隐式反馈：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0">
<div style="border-radius:12px;padding:16px;background:#fefce8;border:1px solid #fde68a">
<div style="font-size:11px;font-weight:700;color:#a16207;margin-bottom:10px">📡 session-feedback-analyzer 处理流程</div>
<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;font-size:12px">
<span style="background:#fff;border:1px solid #fde68a;border-radius:6px;padding:4px 8px">~/.claude/projects/*.jsonl</span>
<span style="color:#999">→</span>
<span style="background:#fff;border:1px solid #fde68a;border-radius:6px;padding:4px 8px">detect_skill_invocations()</span>
<span style="color:#999">→</span>
<span style="background:#fff;border:1px solid #fde68a;border-radius:6px;padding:4px 8px">classify_outcome()<br/><span style="font-size:10px">3-turn 窗口</span></span>
<span style="color:#999">→</span>
<span style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:4px 8px">feedback.jsonl</span>
<span style="color:#999">→</span>
<span style="background:#eff6ff;border:1px solid #93c5fd;border-radius:6px;padding:4px 8px">correction_rate<br/><span style="font-size:10px">per skill</span></span>
</div>
</div>
</div>

纠正信号检测规则：

| 信号 | 检测方式 | 置信度 |
|------|---------|--------|
| 明确否定 | "不对"/"错了"/"wrong" | 0.9 |
| 撤销操作 | git checkout/restore | 0.9 |
| 部分纠正 | 接受词 + 转折词（"可以但是"） | 0.7 |
| 静默继续 | 用户换话题，未纠正 | 0.6 |

在我的 session 数据上跑了一遍：28 个反馈事件，code-review-enhanced 被纠正最多（9 次）。这跟我的体感一致，它生成的 review 评论经常需要我手动调整措辞和优先级。

## 失败了就别再试同一招——自动改进的核心问题

直接重试不行。LLM 容易翻来覆去犯同一个错。我们叫它 "Ralph Wiggum loop"，说着 "I'm helping!" 然后帮倒忙。

改进层的五个阶段（generator→discriminator→evaluator→executor→gate）已经在架构图里展示过。这里重点讲让它真正跑通的两个机制：**失败追踪**和**门禁**。

失败追踪的数据结构：

```json
{
  "type": "failure_trace",
  "candidate_id": "docs-accuracy-001",
  "decision": "revert",
  "reason": "accuracy regressed 12%",
  "gate_blockers": ["RegressionGate: accuracy 0.85 -> 0.75"]
}
```

generator 读到"docs-accuracy 策略在 accuracy 维度上失败了 3 次"，就跳过这个策略。思路来自 trace-aware reflection——把失败的具体原因注入下一轮生成的 prompt，让 LLM 避开已知的死路。

### Gate 六层门禁

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0">
<div style="display:flex;gap:4px;align-items:center;flex-wrap:wrap">
<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:6px 10px;text-align:center;font-size:11px"><b>1</b> Schema</div>
<div style="color:#999;font-size:10px">→</div>
<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:6px 10px;text-align:center;font-size:11px"><b>2</b> Compile</div>
<div style="color:#999;font-size:10px">→</div>
<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:6px;padding:6px 10px;text-align:center;font-size:11px"><b>3</b> Lint</div>
<div style="color:#999;font-size:10px">→</div>
<div style="background:#eff6ff;border:1px solid #93c5fd;border-radius:6px;padding:6px 10px;text-align:center;font-size:11px"><b>4</b> Regression<br/><span style="font-size:9px;color:#666">Pareto per-dim</span></div>
<div style="color:#999;font-size:10px">→</div>
<div style="background:#eff6ff;border:1px solid #93c5fd;border-radius:6px;padding:6px 10px;text-align:center;font-size:11px"><b>5</b> Review<br/><span style="font-size:9px;color:#666">盲审共识</span></div>
<div style="color:#999;font-size:10px">→</div>
<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:6px 10px;text-align:center;font-size:11px"><b>6</b> Human<br/><span style="font-size:9px;color:#666">高风险审批</span></div>
</div>
<div style="font-size:11px;color:#666;margin-top:6px">Schema/Compile/Regression/Review 为阻塞层（fail = reject）；Lint 和 HumanReview 为建议层（fail = warn）。Regression 容差按维度：security 2%、efficiency 10%、其他 5%</div>
</div>

RegressionGate 用的 Pareto front，代码（`lib/pareto.py`）：

```python
DEFAULT_TOLERANCES = {"security": 0.02, "efficiency": 0.10}
DEFAULT_TOLERANCE = 0.05

def check_regression(self, scores, tolerances=None):
    tols = {**self.DEFAULT_TOLERANCES, **(tolerances or {})}
    for dim, best in best_per_dim.items():
        tol = tols.get(dim, self.DEFAULT_TOLERANCE)
        if new_score < best * (1 - tol):
            regressions.append({"dimension": dim, "best": best,
                                "new": new_score, "tolerance": tol})
```

security 容差 2%，efficiency 容差 10%，其他 5%。为什么不统一？安全退步的代价比效率波动高一个数量级，拿同一把尺子量不合理。

为什么不用一个总分？accuracy=0.85/coverage=0.70 改成 accuracy=0.70/coverage=0.85，加权得分完全相同。但准确度被毁了。Pareto front 要求每个维度独立不退步。

### 执行可靠性：agent 为什么老停

这些自动改进任务丢进 tmux session 让 dispatched agent 跑。但 Claude Code agent 有个毛病：它经常觉得自己"做完了"然后停下来，实际上只改了一半。我在批量改进 28 个 skill 的时候，大概有 40% 的 session 是 agent 跑到一半自己停了。

### Ralph：拦住不让停

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="border-radius:12px;padding:20px;background:#eff6ff;border:1px solid #93c5fd">
<div style="font-size:12px;font-weight:700;color:#2563eb;letter-spacing:1px;margin-bottom:14px">🔁 Ralph Stop Hook 交互流程</div>

<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:8px 12px;min-width:80px;text-align:center"><b>Agent</b></div>
<div style="color:#999">—— end_turn ——→</div>
<div style="background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:8px 12px;min-width:120px;text-align:center"><b>ralph-stop-hook.sh</b><br/><span style="font-size:10px">读 ralph.json<br/>iteration=3/10</span></div>
<div style="color:#dc2626">—— ✋ block ——→</div>
<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:8px 12px"><span style="font-size:11px;color:#dc2626">"[RALPH LOOP 3/10] Task NOT done"</span></div>
</div>

<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:8px 12px;min-width:80px;text-align:center"><b>Agent</b></div>
<div style="color:#999">—— end_turn ——→</div>
<div style="background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:8px 12px;min-width:120px;text-align:center"><b>ralph-stop-hook.sh</b><br/><span style="font-size:10px">读 ralph.json<br/>iteration=10/10</span></div>
<div style="color:#16a34a">—— ✅ allow ——→</div>
<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:8px 12px"><span style="font-size:11px;color:#16a34a">正常结束</span></div>
</div>

<div style="margin-top:12px;display:flex;gap:6px;flex-wrap:wrap">
<span style="background:#fff;border:1px solid #bfdbfe;border-radius:6px;padding:4px 8px;font-size:11px">🛡️ context >= 95%</span>
<span style="background:#fff;border:1px solid #bfdbfe;border-radius:6px;padding:4px 8px;font-size:11px">🔑 认证错误 401/403</span>
<span style="background:#fff;border:1px solid #bfdbfe;border-radius:6px;padding:4px 8px;font-size:11px">🚫 cancel 信号 (30s TTL)</span>
<span style="background:#fff;border:1px solid #bfdbfe;border-radius:6px;padding:4px 8px;font-size:11px">⏰ 闲置 > 2小时</span>
<span style="background:#fff;border:1px solid #bfdbfe;border-radius:6px;padding:4px 8px;font-size:11px">🔢 达到 max_iterations</span>
</div>
<div style="font-size:11px;color:#666;margin-top:6px">五个安全阀，任一触发则 allow，防止 Ralph 把 agent 永远困住</div>
</div>
</div>

### Handoff：context 压缩了怎么办

Claude Code 压缩 context 时，设计决策、被否决的方案、已知风险会被丢掉。Handoff 文档解决这个问题：agent 在阶段结束时写 `handoffs/stage-N.md`，包含 Decided/Rejected/Risks/Remaining。文件在磁盘上，不受 context 压缩影响。

## 管用吗？4 个 Skill 的批量验证

### 批量改进 4 个 GENERIC Skill

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="border-radius:12px;padding:20px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:12px;font-weight:700;color:#16a34a;letter-spacing:1px;margin-bottom:14px">📈 4 个 GENERIC Skill → 全部 SOLID（平均 +0.138，费用 $15-20）</div>
<table style="width:100%;border-collapse:collapse;font-size:12px">
<tr style="border-bottom:2px solid #86efac"><td style="padding:8px"><b>Skill</b></td><td style="padding:8px">改进前</td><td style="padding:8px">改进后</td><td style="padding:8px">提升</td><td style="padding:8px">保留/尝试</td></tr>
<tr style="background:#fff"><td style="padding:8px">system-maintenance</td><td style="padding:8px"><span style="color:#dc2626">0.653</span></td><td style="padding:8px"><span style="color:#16a34a"><b>0.803</b></span></td><td style="padding:8px;color:#16a34a">+0.150</td><td style="padding:8px">3/3</td></tr>
<tr><td style="padding:8px">perf-profiler</td><td style="padding:8px"><span style="color:#dc2626">0.661</span></td><td style="padding:8px"><span style="color:#16a34a"><b>0.803</b></span></td><td style="padding:8px;color:#16a34a">+0.142</td><td style="padding:8px">2/3</td></tr>
<tr style="background:#fff"><td style="padding:8px">component-dev</td><td style="padding:8px"><span style="color:#dc2626">0.665</span></td><td style="padding:8px"><span style="color:#16a34a"><b>0.798</b></span></td><td style="padding:8px;color:#16a34a">+0.133</td><td style="padding:8px">1/3</td></tr>
<tr><td style="padding:8px">release-notes</td><td style="padding:8px"><span style="color:#dc2626">0.681</span></td><td style="padding:8px"><span style="color:#16a34a"><b>0.831</b></span></td><td style="padding:8px;color:#16a34a">+0.150</td><td style="padding:8px">3/3</td></tr>
</table>
<div style="margin-top:10px;font-size:11px;color:#666">
最大单项跳跃：<b>reliability 0.30 → 1.00</b>（learner 发现 skill 有脚本但没测试，自动生成测试桩，通过了）<br/>
保留率 1/3 ~ 3/3 说明 gate 在工作——被 Pareto 拦住的候选确实会造成维度退步
</div>
</div>
</div>

### 自评：9 维 + 4 角色 + 类别修正

用新体系（9 维 × 4 角色 × category modifier）跑了仓库内的 13 个 skill（execution-harness 和 deslop 已独立，不在此列）：

| Skill | 分数 | Tier | 共识 |
|-------|:----:|------|:----:|
| benchmark-store | 95.5 | POWERFUL | CONSENSUS |
| generator | 95.0 | POWERFUL | CONSENSUS |
| gate | 93.3 | POWERFUL | CONSENSUS |
| executor | 93.0 | POWERFUL | CONSENSUS |
| discriminator | 92.9 | POWERFUL | CONSENSUS |
| orchestrator | 91.7 | POWERFUL | CONSENSUS |
| learner | 91.3 | POWERFUL | CONSENSUS |
| prompt-hardening | 89.4 | POWERFUL | MOSTLY_AGREED |
| evaluator | 84.2 | SOLID | MOSTLY_AGREED |
| skill-forge | 84.2 | SOLID | MOSTLY_AGREED |
| skill-distill | 83.0 | SOLID | MOSTLY_AGREED |
| autoloop | 81.3 | SOLID | MOSTLY_AGREED |
| session-feedback | 78.2 | SOLID | DISPUTED |

8/13 POWERFUL，均分 88.7%。最初只有 3 个 POWERFUL（均分 83.3%），短板是 knowledge_density——7 个 skill 的 SKILL.md 段落太薄，补了 why 段落和代码示例后全部上来了。session-feedback 分最低（78.2），因为它没有 references/ 目录，completeness 检查扣了分。

### 跟 DSPy/PromptFoo/LangSmith 比，差别在哪

好工具不少。DSPy 做 prompt 优化，PromptFoo 做 assertion 检查，LangSmith 做可观测性，Karpathy 的 autoresearch 做单标量自动优化。我们借鉴了很多，但做的事不太一样：从跑测试到改 SKILL.md 到再跑测试，不断循环，针对 Skill 而不是 prompt token。

| 系统 | 优化对象 | 粒度 | diff 可读？ | 多维度？ | 反馈来源 |
|------|---------|------|:-----------:|:-------:|---------|
| **本项目** | SKILL.md 文档 | 段落 | ✅ | 9维 Pareto | task suite + 用户隐式反馈 |
| DSPy | prompt token | token | ❌ | 单目标 | 用户定义 metric |
| TextGrad | LLM 输出变量 | token | ❌ | 单目标 | LLM "梯度" |
| MOPrompt | prompt 优化 | prompt | ✅ | Pareto front | 多目标演化搜索 |
| PromptFoo | prompt assertion | prompt | ✅ | 单维 | assertion suite |
| LangSmith | agent trace | trace | N/A | 多 metric | 可观测性平台 |
| Karpathy autoresearch | train.py | 文件 | ✅ | 单标量 | 训练 loss |

表里最明显的区别在两列："diff 可读？"和"多维度？"。

DSPy 的 MIPROv2 在 token 粒度上做贝叶斯搜索，跑完你看 diff 经常不知道为什么删了一个逗号或换了一个 "please"。我们改的是 SKILL.md 里的段落和示例，每个 diff 人能读、能判断、能手动回滚。搜索空间小很多，但对 skill 来说够用。

另一个区别是多维度。DSPy、Karpathy autoresearch、PromptFoo 都用单一标量做优化目标。单一标量容易藏住 tradeoff：accuracy 从 0.83 涨到 0.91，trigger_quality 从 0.80 掉到 0.55，算加权得分居然还涨了 0.02。如果没有 Pareto front 拦住这种候选，skill 就废了。

LangSmith 采集 trace 但主要输出到 dashboard 给人看。我们的 session-feedback-analyzer 不停在 dashboard 这一步——从 Claude Code 会话日志提取用户纠正信号，直接喂给 generator 驱动下一轮改进。RLHF 在模型训练层做类似的事，但在 prompt/skill 层这么做的工具我没见到几个。

睡前设好 cost cap 和终止条件，启动 autoloop-controller，第二天看报告。Karpathy 用 700 次实验两天提升了 11%，我们在 4 个 skill 上平均 +0.138，费用 $15-20。

### 睡前启动，第二天看报告

autoloop-controller 包了个外层循环，检测五种停止信号：

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0">
<div style="border-radius:12px;padding:16px;background:#faf5ff;border:1px solid #c4b5fd">
<div style="font-size:11px;font-weight:700;color:#7c3aed;margin-bottom:10px">🔄 autoloop 循环 + 5 种终止条件</div>
<div style="text-align:center;margin-bottom:8px">
<span style="background:#fff;border:1px solid #ddd6fe;border-radius:8px;padding:6px 12px;font-size:12px"><b>run_pipeline()</b></span>
<span style="color:#999;margin:0 8px">→</span>
<span style="background:#fff;border:1px solid #ddd6fe;border-radius:8px;padding:6px 12px;font-size:12px"><b>检查终止条件</b></span>
<span style="color:#999;margin:0 8px">→</span>
<span style="background:#fff;border:1px solid #ddd6fe;border-radius:8px;padding:6px 12px;font-size:12px"><b>写 handoff</b></span>
<span style="color:#999;margin:0 8px">↩️</span>
</div>
<div style="display:flex;gap:4px;flex-wrap:wrap">
<span style="background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:4px 8px;font-size:11px">🔢 max_iterations 到了</span>
<span style="background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:4px 8px;font-size:11px">💰 cost_cap 超了</span>
<span style="background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:4px 8px;font-size:11px">📈 分数平台期</span>
<span style="background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:4px 8px;font-size:11px">🔄 keep-reject 震荡</span>
<span style="background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:4px 8px;font-size:11px">👤 correction_rate 没下降</span>
</div>
</div>
</div>

状态持久化到 JSON，进程挂了重启接着跑。每轮写一份 `handoffs/iteration-N.md`，记 Decided/Rejected/Scores/Remaining——context 压缩丢不掉这些，因为它们在磁盘上。

### 数字和教训

4 个 GENERIC skill 全部升到 SOLID，平均 +0.138，总费用 $15-20。仓库内 13 个 skill 在新 9 维体系下均分 88.7%，8/13 达到 POWERFUL。session-feedback-analyzer 从真实会话提取了 28 个反馈事件，code-review-enhanced 被纠正 9 次——跟我的体感完全一致。397 个测试全过，依赖只有 pyyaml 和 pytest（evaluator 的 `claude -p` 除外）。已经发到 ClawHub 了。

教训说三个。

第一个：先有评估再做改进。我最初反过来了——先写 generator 和 executor，改完不知道好不好。掉头先做评估之后一切才顺起来。听起来像废话，做起来真的会忘。

第二个：Pareto front 是 ROI 最高的组件。98 行 Python，拦住了至少三个 skill 不被"优化"搞坏。加权得分的陷阱防不胜防——accuracy 涨了但 trigger_quality 崩了，总分居然还涨 0.02。

第三个：成本控制是设计约束，不是事后补丁。evaluator 一次 $3-5，100 个 skill 的团队一个月可能烧 $5000。conditional evaluation（低分候选跳过 evaluator）省了 60%，但这是后来才加的。早知道应该一开始就设计进去。

## 下一步

### 循环依赖怎么破：GAN 式对抗生成

说清楚这个问题到底是什么。

传统做法：一个人写 SKILL.md，同一个人写 task suite 来测试。问题是，你写的测试自然会覆盖你写的内容。skill-creator 的 accuracy 评分 0.70（最低），但 evaluator pass rate 100%（最高）。不是它真的好，是 task suite 恰好只测了它教的东西。这像考试出题人自己做自己的卷子。

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:24px 0">
<div style="display:flex;gap:16px">
<div style="flex:1;border-radius:12px;padding:20px;background:#fef2f2;border:1px solid #fca5a5">
<div style="font-size:12px;font-weight:700;color:#dc2626;letter-spacing:1px;margin-bottom:14px">❌ 传统方式：自己出题自己考</div>
<div style="background:#fff;border:1px solid #fecaca;border-radius:8px;padding:12px;margin-bottom:8px"><b>作者写 SKILL.md</b><br/><span style="color:#666">"当需要生成 release notes 时，按模块分类"</span></div>
<div style="text-align:center;color:#999;margin:4px 0">↓ 同一个人</div>
<div style="background:#fff;border:1px solid #fecaca;border-radius:8px;padding:12px;margin-bottom:8px"><b>作者写 task_suite.yaml</b><br/><span style="color:#666">"测试：能不能按模块分类？" → 当然能</span></div>
<div style="text-align:center;color:#999;margin:4px 0">↓</div>
<div style="background:#fef2f2;border:1px solid #f87171;border-radius:8px;padding:12px"><b style="color:#dc2626">100% 通过 ≠ 真的好</b><br/><span style="color:#666">只是自洽，没覆盖作者没想到的场景</span></div>
</div>

<div style="flex:1;border-radius:12px;padding:20px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:12px;font-weight:700;color:#16a34a;letter-spacing:1px;margin-bottom:14px">✅ GAN 式：生成器 vs 对抗测试器</div>
<div style="background:#fff;border:1px solid #bbf7d0;border-radius:8px;padding:12px;margin-bottom:8px"><b>Generator 改进 SKILL.md</b><br/><span style="color:#666">优化段落、补示例、加 guardrails</span></div>
<div style="text-align:center;color:#999;margin:4px 0">↓ 不同角色</div>
<div style="background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:12px;margin-bottom:8px"><b style="color:#a16207">Adversarial Tester 造对抗测试</b><br/><span style="color:#666">"找一个能让这个 skill 失败的输入"<br/>不看 task suite，只看 SKILL.md 找弱点</span></div>
<div style="text-align:center;color:#999;margin:4px 0">↓</div>
<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:12px"><b style="color:#16a34a">通过对抗测试 = 真的强</b><br/><span style="color:#666">因为测试者的目标就是让你失败</span></div>
</div>
</div>
</div>

GAN 的思路：generator 和 discriminator 互相博弈。在 skill 场景下：

- **Generator**（已有）：读 SKILL.md，生成改进候选
- **Adversarial Tester**（新角色）：读 SKILL.md，专找没覆盖的边界情况，造能让 skill 挂的测试
- **Evaluator**（已有）：跑这些对抗测试，看 skill 扛不扛得住

不需要"社区参与"或"不同的人来写"。同一个 LLM，两个 prompt 角色，激励方向相反——一个想让 skill 更好，一个想让 skill 挂。

缓解循环依赖，我在试三个办法。session-feedback-analyzer 从用户实际使用中挖独立信号，不依赖作者写的 task suite。null-skill calibration 在跑测试前先让裸跑 Claude 过一遍，能过的任务直接扔掉——它们测不出 skill 的价值。GAN 式对抗测试生成让 adversarial tester 专门找 skill 的弱点，用对抗来代替自测。

### 没做完的

副作用追踪。prompt-hardening 那个例子一直困扰我——加载 skill 后通过率跟裸跑一样 86%，但挂的任务换了。CLI 路径任务从 fail 变 pass，审计格式任务从 pass 变 fail。evaluator 报出来的聚合 pass rate 是一样的，根本看不出问题。我需要的是逐任务 diff：version A 和 version B 之间，哪些任务翻转了？翻转的原因是什么？这个还没写。

多模型衰减。`--model` 参数加了，一直没跑。我想验证的事情很具体：同一组测试在 Opus 上过 90%，Haiku 上还能过多少？如果 Haiku 掉到 40%，说明 skill 写的是暗示不是指令——模型不够聪明就读不懂。衰减曲线越平，说明指令写得越扎实。没数据之前这只是猜测。

### 跑一下

```bash
git clone https://github.com/lanyasheng/auto-improvement-orchestrator-skill.git
pip install pyyaml pytest

# 打分
python3 skills/improvement-learner/scripts/self_improve.py \
  --skill-path /your/skill --max-iterations 1

# 自动改进 5 轮
python3 skills/improvement-learner/scripts/self_improve.py \
  --skill-path /your/skill --max-iterations 5

# 从 Claude Code 会话日志里提取反馈
python3 skills/session-feedback-analyzer/scripts/analyze.py \
  --output feedback.jsonl
```

除了 pyyaml 和 pytest 没有别的依赖。evaluator 跑真实任务需要 `claude -p`，那是另一回事。

GitHub: [lanyasheng/auto-improvement-orchestrator-skill](https://github.com/lanyasheng/auto-improvement-orchestrator-skill) / ClawHub 各 skill 独立发布（如 `openclaw skills install improvement-learner`）

这个项目现在最大的瓶颈不是代码，是 task suite。一个人写的 skill 只有同一个人测，测出来 100% 通过率说明不了什么——出题人做自己的卷子永远满分。打破这个循环的办法就一个：让别人来写测试。你手上有 skill 的话，挑一个你觉得写得一般的，给它造三个刁钻的测试用例，提个 PR。一个好的 adversarial test 比十个 SKILL.md 段落改进都有价值。
