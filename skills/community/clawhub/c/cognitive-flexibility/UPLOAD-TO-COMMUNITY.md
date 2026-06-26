# Cognitive Flexibility Skill 社区发布说明

**版本:** v2.1.0  
**发布时间:** 2026-04-05  
**作者:** 道师 (optimizer)  
**许可:** MIT License

---

## 📦 Skill 简介

**Cognitive Flexibility Skill** 让 AI 像人类一样灵活运用知识。

基于李德毅院士的"四种认知模式"理论，实现：
- **OOA** 经验模式（记忆驱动）
- **OODA** 推理模式（知识驱动）
- **OOCA** 创造模式（联想驱动）
- **OOHA** 发现模式（假说驱动）

支持自动模式切换和元认知监控。

---

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| **4 种认知模式** | OOA/OODA/OOCA/OOHA |
| **自动模式切换** | 根据任务特征自动选择最佳模式 |
| **元认知监控** | 自我评估、置信度评估、改进建议 |
| **使用追踪** | 完整的使用日志和效果统计 |
| **测试覆盖** | 100% 测试通过率 |

---

## 🚀 快速开始

### 安装

```bash
# 使用 ClawHub 安装
clawhub install cognitive-flexibility

# 或手动安装
# 下载本 Skill 到 skills 目录
```

### 使用

```python
from scripts.cognitive_controller import CognitiveController

# 创建控制器
controller = CognitiveController(confidence_threshold=0.7)

# 执行任务（自动选择模式）
task = "分析用户反馈数据"
result = await controller.process(task, tools=tools)

print(f"模式：{result['mode']}")
print(f"答案：{result['answer']}")
print(f"置信度：{result['assessment']['overall_score']:.2f}")
```

---

## 📊 测试结果

**测试通过率:** 100% (6/6)

- ✅ OODA Reasoner
- ✅ Pattern Matcher
- ✅ Self Assessor
- ✅ Cognitive Controller
- ✅ Creative Explorer
- ✅ Hypothesis Generator

---

## 📁 文件结构

```
cognitive-flexibility/
├── scripts/              # 核心代码
│   ├── chain_reasoner.py
│   ├── pattern_matcher.py
│   ├── self_assessor.py
│   ├── cognitive_controller.py
│   ├── creative_explorer.py
│   ├── hypothesis_generator.py
│   └── usage_monitor.py
├── references/           # 参考资料
│   └── ooda-guide.md
├── tests/                # 测试用例
│   └── test_cognitive_skills.py
├── SKILL.md              # Skill 元数据
├── README.md             # 使用指南
└── MONITORING-GUIDE.md   # 监控指南
```

---

## 🔒 隐私说明

**本 Skill 已清理所有敏感信息：**
- ✅ 无 API keys
- ✅ 无 tokens
- ✅ 无用户数据
- ✅ 无外部依赖

**注意:** 使用监控功能会在本地生成日志（`logs/` 目录），仅存储在本地。

---

## 📋 系统要求

| 要求 | 说明 |
|------|------|
| Python | >=3.8 |
| OpenClaw | >=2026.3.28 |
| 依赖 | 无外部依赖 |

---

## 📖 文档

- **README.md** - 快速入门
- **MONITORING-GUIDE.md** - 监控功能指南
- **RELEASE-NOTES.md** - 发布说明
- **PUBLISH-GUIDE.md** - 发布指南

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**反馈渠道:**
- GitHub Issues
- OpenClaw Community
- ClawHub

---

## 📜 许可

MIT License

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-04-05 | 新增使用监控功能 |
| 2.0.0 | 2026-04-05 | 实现 OOCA/OOHA 模式 |
| 1.0.0 | 2026-04-05 | 初始版本 |

---

_道师出品 · Cognitive Flexibility Skill v2.1.0_

**发布日期:** 2026-04-05  
**状态:** ✅ 准备上传到社区
