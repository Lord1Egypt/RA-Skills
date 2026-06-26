# CNC Quote Workflow

🦫 **CNC智能报价Workflow - 多Agent协作闭环**

从黑盒24h到白盒10min，实现智能报价闭环。

## 一句话故事

"10年制造业老师傅用 ClawHub 已发布的 CNC Quote Skill + OpenClaw Workflow，实现从黑盒24h 到白盒10min 的智能报价闭环"

## 参赛信息

- **主赛道**: Workflow Hacker
- **副赛道**: Agent Worker
- **版本**: v2.0.2

## 核心特性

- ⚡ 10分钟报价（行业平均24h+）
- 📊 白盒报价，完整成本分解
- 🧠 3个Agent协作，自我辩论
- 🏆 效率提升144倍

## 快速开始

```bash
# 安装依赖
pip install pyyaml

# 运行示例
python workflow_engine.py
```

## 文件结构

```
├── workflow.yaml         # Workflow定义
├── agent1_parser.py      # Agent1: 输入解析
├── agent2_rag.py         # Agent2: RAG检索
├── agent3_meta.py        # Agent3: 元认知审核
├── workflow_engine.py    # Workflow编排引擎
├── rule_only.py          # Rule-Only兜底引擎
├── config.json           # 配置文件
└── requirements.txt      # 依赖列表
```

## 作者

- **Timo** (miscdd@163.com)
- 海狸 (Beaver) - 靠得住、能干事、在状态

## License

MIT License