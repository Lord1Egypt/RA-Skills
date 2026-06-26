# 🦐 RoundTable Skill 打包说明

## 📦 打包信息

- **版本**: 0.9.0
- **打包时间**: 2026-03-19
- **作者**: Your Name &lt;your-email@example.com&gt;
- **许可**: MIT
- **GitHub**: https://github.com/Krislu1221/Claw-roundtable-skill *(待上线)*

---

## 📊 核心特性（0.9.0）

| 特性 | 说明 |
|--------|------|
| **5 轮讨论** | R1 独立→R2 引用→R3 批判→R4 辩论→R5 总结 |
| **强制批判** | R3 必须识别 5 个风险 + 3 个缺陷 |
| **上下文传递** | 每轮注入完整讨论历史 |
| **方案演进** | R4 必须标注修改对比表 |
| **分歧裁决** | R5 必须裁决所有分歧 |
| **周级计划** | 产出 8 周行动计划（W1-W8） |

---

## 📜 版本历史

### 0.9.0 (2026-03-19) - 基于真实测试优化
- ✅ 完整 5 轮流程（R1-R5）
- ✅ 强制批判深度（5 风险 +3 缺陷）
- ✅ 方案动态演进（R4 标注修改）
- ✅ 分歧明确裁决（R5 必须裁决）
- ✅ 产出可直接执行（周级计划 + 风险预案）
- ✅ 触发词识别（RoundTable/圆桌会议/圆桌讨论等）
- ✅ 真实子 Agent 调用（sessions_spawn）
- ✅ 上下文传递（每轮注入完整历史）

### 0.1.0 (2026-03-17) - 初始版本
- ✅ 基础 RoundTable 框架
- ✅ 3 专家角色定义
- ✅ 5 轮讨论流程
- ✅ 前端查看器

---

## 📁 文件清单

```
roundtable-skill/
├── README.md                   # GitHub 首页文档
├── SKILL.md                    # 技能说明文档
├── PACKAGE.md                  # 打包说明（本文件）
├── LICENSE                     # MIT 许可证
├── requirements.txt            # Python 依赖
├── __init__.py                 # 模块导出
├── clawhub.json                # ClawHub 配置
├── roundtable_engine.py        # 执行引擎（核心）
├── roundtable_notifier.py      # 通知模块
├── agent_selector.py           # Agent 选择器
├── prompts/
│   ├── framework.md            # 提示词框架 0.9.0
│   └── README.md               # 提示词说明
├── templates/
│   ├── software-development.md # 软件开发模板
│   ├── product-planning.md     # 产品规划模板
│   └── business-research.md    # 商业研究模板
└── roundtable-viewer/          # 前端查看器
    ├── index.html
    ├── data.json
    └── assets/
```

---

## 🔧 安装步骤

### 1. 复制到 Skills 目录

```bash
cp -r roundtable-skill \
      ~/.openclaw/workspace/skills/
```

### 2. 验证安装

```bash
cd ~/.openclaw/workspace/skills/roundtable-skill
python3 -c "import roundtable_engine; print('✅ 模块加载成功')"
```

### 3. 前置要求

- Python 3.8+
- OpenClaw 环境
- 依赖安装：`pip install -r requirements.txt`

---

## 🚀 使用方式

### 快速激活

```
请你 RoundTable 讨论一下：{你的议题}
```

### 完整示例

```
请你 RoundTable 多 Agent 深度讨论

**议题**: 智能待办应用技术方案设计

**行业类型**: software-development

**参与专家**: 工程专家、体验专家、测试专家

**期望产出**: 技术方案 + 8 周行动计划
```

---

## 🎯 输出物

### 最终决策报告
- 讨论概要（各专家观点总结表）
- 最终决策（已确定事项 + 分歧裁决）
- 技术方案（技术栈表格 + 架构）
- 8 周行动计划（周级任务表）
- 风险提醒（Top 3 风险表）

### 过程文档
- R1-R4 完整讨论记录
- 每轮修改对比表
- 风险演进追踪

### 可执行性验证
- [ ] R1 包含至少 1 个对比表格
- [ ] R2 包含至少 3 处引用标注
- [ ] R3 包含至少 5 个风险 + 3 个缺陷
- [ ] R4 包含修改对比表格
- [ ] R5 包含周级计划表（至少 8 周）
- [ ] R5 包含 Top 3 风险表

**通过率目标**: 90%+

---

## ⚠️ 隐私清理说明

已清理的隐私信息：
- ❌ 飞书应用 ID
- ❌ 工作目录路径
- ❌ 个人身份信息
- ❌ 内部服务器地址

可公开分享的信息：
- ✅ 技术栈选型
- ✅ 讨论流程
- ✅ 输出格式
- ✅ 配置参数

---

## 📞 技术支持

- **问题反馈**: https://github.com/Krislu1221/Claw-roundtable-skill/issues *(待上线)*
- **文档**: https://docs.openclaw.ai/skills/roundtable *(待上线)*
- **社区**: https://discord.gg/clawd

---

*打包完成，可以安全分享！* 🎉
