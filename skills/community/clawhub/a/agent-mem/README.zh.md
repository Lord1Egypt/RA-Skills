# AgentMem — 多Agent记忆+调度系统

> **同时管理「Agent该记住什么」和「谁该去干什么」的开源方案**
> 市场上首个记忆+调度联动的闭环系统

---

## 🧠 核心特色

### 四层记忆分级
| 层级 | 生命周期 | 用途 |
|------|---------|------|
| **HOT** | 实时，2小时 | 当前会话，跨通道互通 |
| **WARM** | 24小时 | 近期摘要，随手可查 |
| **COLD** | 永久 | 重要事实、决策、用户偏好 |
| **ARCHIVE** | 30天 | 历史归档，可检索 |

### 跨通道互通
同一Agent在不同通道（webchat/飞书/Slack/Telegram）的记忆自动共享。
在A通道聊完，B通道的Bot也能接上话。

### 调度+记忆闭环
```
用户请求 → 意图识别 → Agent调度 → 执行 → 日志 → 优化下次调度
```
每次调度自动记录完整链路，下次优先选成功率高的Agent。

### 17个记忆模块
事实提取、BM25+向量融合检索、矛盾检测、知识图谱、遗忘机制、
主动召回、记忆反馈修正、自我审查……覆盖记忆全生命周期。

---

## 📦 快速开始

```bash
pip install -e .

# 写入一条记忆
python -m agent_mem.core.hot_cache write --agent main --channel webchat --text "用户偏好简洁回答" --importance 7

# 跨通道查询（查所有通道）
python -m agent_mem.core.hot_cache query --agent main --limit 5

# 查看调度统计
python -m agent_mem.core.dispatch_logger stats

# 运行记忆引擎
python -m agent_mem.core.engine_v2 --mode daily
```

---

## 📊 与市场主流对比

| 能力 | AgentMem | 说明 |
|------|----------|------|
| 四层时间分级 | ✅ | 记忆按HOT→WARM→COLD→ARCHIVE自然衰减 |
| 跨通道互通 | ✅ | 同一Agent多通道记忆自动共享 |
| 调度+记忆联动 | ✅ | 调度决策→执行→记录→优化，自动闭环 |
| 多Agent隔离 | ✅ | 各Agent记忆独立存储，不混淆 |
| 矛盾检测 | ✅ | 自动检测事实矛盾并标记 |
| 知识图谱因果链 | ✅ | 事件→决策→结果因果链自动关联 |
| 遗忘机制 | ✅ | TTL衰减，自动清理 |
| 主动召回 | ✅ | 话题相关历史经验自动推送 |
| 记忆反馈修正 | ✅ | 自然语言修正已存记忆 |
| 自我审查 | ✅ | 自动提炼规律+成功率追踪 |
| 零外部依赖 | ✅ | 纯Python，只有一个第三方包依赖 |

---

## 📄 协议
MIT License — 随便用，随便改，随便发。

---

## 🌐 链接
- GitHub: https://github.com/wenshuangl/agent-mem
- 项目介绍: [INTRO.md](INTRO.md) (中英双语)
