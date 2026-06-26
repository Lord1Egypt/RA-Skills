---
name: deep-token-saver
description: 综合 token 节省方案。6层技术叠加，从输入/输出/记忆/上下文/审计全链路降本。含Caveman、L0/L1/L2分层、Remnic/QMD持久化、记忆去重、AGENTS压缩、Token审计。
---

# Deep Token Saver — 综合 Token 节省方案

> 6层叠加，从根源省 token，不止压缩一句话。

---

## 层1：输出压缩（Caveman Mode）

| 规则 | 说明 |
|:----|:-----|
| 去冠词/废话/客套 | a/an/the/just/really/basically/当然/没问题 |
| 短句碎片 | 结论先行，不铺垫 |
| 技术内容保持 | 代码块/路径/数字/名称 原样 |
| 切换开关 | 回复走碎片模式。说`正常说话`恢复 |

**省：↓75% 输出 token**

---

## 层2：输入压缩（启动文件 + 记忆）

| 文件 | 处理方式 | 省 |
|:----|:--------|:--:|
| AGENTS.md | 压缩为 caveman 版 | ↓61% |
| SOUL.md | 保持轻量 | — |
| memory 条目 | 定期合并、去重 | ↓20-30% |
| memory-sync | 每日自动归档到 workspace/memory/ | 防膨胀 |

---

## 层3：L0/L1/L2 分层笔记（概念笔记用）

每条概念笔记 frontmatter 加 `abstract:` 字段。我只加载 L0，按需展开：

| 层级 | 内容 | 长度 | 加载策略 |
|:---:|:----|:---:|:--------|
| **L0** | `abstract:` 一句话定义 | ~50 chars | 永远加载 |
| **L1** | 核心规则 | ~200 chars | 按需 |
| **L2** | 全文笔记 | ~500+ chars | 点开才读 |

**省：↓90% 笔记读取 token**

---

## 层4：跨会话记忆持久化（Remnic + QMD）

已装组件：
- `@remnic/cli` + `@remnic/server`
- `remnic-hermes` Python MemoryProvider
- QMD 混合搜索（BM25 + 向量 + 重排序）

开机自启：计划任务 `RemnicServer`

**省：↓全量记忆重复加载**

---

## 层5：记忆去重与合并

定期扫描记忆条目：
- 语义相似条目 → 合并
- 过期/无用条目 → 删除
- 长条目 → 压缩

通过 Remnic API 执行：
```
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:4318/engram/v1/consolidate
```

**省：↓20-30% 记忆空间**

---

## 层6：Token 节省审计

每次回复末尾显示本轮的 token 节省：

```
⚡省: 原本~X 实际~Y 省Z% | 累计省~W
```

数据来源：回复字符数 × 4（1 token ≈ 4 chars）估算。

**省：不直接省，但可视化降本效果**

---

## 总省效果

| 层 | 省多少 | 类型 |
|:--|:-----:|:----|
| 输出压缩 | ↓75% | 每轮 |
| 输入压缩 | ↓61% | 每会话 |
| L0/L1/L2 | ↓90% | 笔记读取 |
| Remnic/QMD | 全量→按需 | 跨会话 |
| 记忆去重 | ↓20-30% | 维护 |
| **合计** | **预估↓80-90%** | **全链路** |

---

## 维护命令

```bash
# 查看 Remnic 状态
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:4318/engram/v1/health

# 手动记忆合并
curl -s -X POST -H "Authorization: Bearer $TOKEN" http://127.0.0.1:4318/engram/v1/consolidate

# 查看 token 节省统计
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:4318/engram/v1/stats

# 手动记忆同步
cd /c/Users/Administrator/workspace && python hermes-memory-sync.py backfill today
```

---

## 故障排除

| 问题 | 解决 |
|:----|:-----|
| Remnic 未运行 | 执行 `start-remnic.bat` 或重启电脑自动启 |
| 记忆条目满了 | 手动执行记忆合并命令 |
| 想正常说话 | 说`正常说话` |
