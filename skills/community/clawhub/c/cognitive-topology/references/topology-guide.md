# Cognitive Topology 参考

## 与 Stello 的功能对应

| Stello 功能 | 本技能实现 | 状态 |
|------------|-----------|------|
| 对话自动分裂 | sessions_spawn 多分支 | ✅ 已实现 |
| 三层分级记忆 | L3=Session历史, L2=文件, L1=synthesis | ✅ 已实现 |
| 全局意识整合 | ct_integrate.py 汇总 L2 | ✅ 已实现 |
| 星空图可视化 | 文本树状结构 | ⚠️ 简化版 |
| 跨分支 insight | Main Session synthesis | ✅ 已实现 |

## L2 文件格式标准

每个分支写入 L2 时必须遵循以下格式：

```markdown
# {branch_id}

**任务**: {具体任务描述}

**状态**: ✅ 已完成

**完成时间**: {ISO时间}

---

## 结论

{核心结论，一句话概括}

## 依据

{支撑结论的具体依据、分析过程、数据引用}

## 下一步建议

{可选，基于分析的建议}
```

## 分支任务执行模板

当启动一个分支 Agent 时，任务描述应包含：

1. **具体目标** — 要分析什么
2. **L2 输出路径** — 明确写入位置
3. **格式要求** — 按照上面的标准格式
4. **完成通知** — 调用 ct_complete.py 标记完成

示例：
```
分析AI板块短期机会。

输出要求：
- 将结论写入 /root/.openclaw/workspace/cognitive-topology/branches/{branch_id}_L2.md
- 格式遵循标准L2模板（结论/依据/建议）
- 完成后执行: python3 /root/.openclaw/workspace/skills/cognitive-topology/scripts/ct_complete.py {branch_id}
- 打印"✅ 分支完成"
```

## 状态检查流程

1. 调用 `ct_status.py` 查看当前拓扑状态
2. 等待所有分支 status=done
3. 调用 `ct_integrate.py` 生成 synthesis
4. Main Session 读取 synthesis 回复用户
