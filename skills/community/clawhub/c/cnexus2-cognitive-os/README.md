# 🧠 CNexus 2.0 - 个人纯净版

**全息记忆 · 6步认知闭环 · 本地优先的类脑架构**

CNexus 2.0 是一个轻量、可运行、完全本地优先的**个人认知操作系统原型**，专注于实现单机闭环的「观察-认知-决策-表达-存储-反思」完整认知流程。

## 快速启动

```powershell
# 启动 CNexus 运行时
python app_v2.py

# 打开浏览器
open http://127.0.0.1:7865
```

## 架构

- `src/` — 6步纯函数认知内核（reducers, identity, state）
- `core_essence/` — 层不变性系统公理
- `tests/` — 内核合规测试
- `tools/` — 审计与诊断工具
- `config/` — 系统配置
- `_global_registry/` — 全局语义注册表与一致性证明
- `ui/` — 前端（Canvas 2D 记忆星云、聊天、仪表盘）

## 技术栈

Python + TypeScript/React + Canvas 2D + Local LLMs (Ollama)

## 许可证

MIT-0 — 可自由使用、修改、再分发，无需署名。

## 链接

- **GitHub:** https://github.com/plusunm/CNexus2.0
- **运行时:** http://127.0.0.1:7865 (默认)
