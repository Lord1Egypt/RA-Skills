# 基金运营工作流 Skill 📊

**基于《公募基金互金电商业务搭建工作流》+ MBTI 特质匹配 + STAR+ 合规前置框架**

**版本：** v2.0.0（2026-03-26 升级）

**核心升级：**
- ✅ 采用 STAR+ 合规前置框架（所有提示词统一结构）
- ✅ 细化到子节点层面（实施层差异化管理）
- ✅ 驾驭 AI 四原则（给角色 + 给框架 + 给约束 + 给痛点）

---

## 🎯 一句话介绍

帮助用户构建基金运营工作流，将 6 大工作流节点与 16 型 MBTI 特质精准匹配，每个节点调用最适合的 MBTI 类型，并整合核心方法论 + 合规提示词。

---

## 📐 核心架构

```
战略层
├─ 内：梳理资源，寻找优势 → INTJ（战略眼光）
└─ 外：梳理资源，寻找优势 → ENFJ（感染力）

执行层（6 大节点）
├─ 收集（ENFP）→ 思维跳跃，发现新想法
├─ 归档（ISTJ）→ 执行规划，遵守规则
├─ 策略（INTP）→ 逻辑思维，系统分析
├─ 实施（ENTJ）→ 执行力，高效领导
├─ 测试（ISFJ）→ 责任感，可靠完成任务
└─ 监控（INFJ）→ 洞察力，理解复杂模型
```

---

## 🚀 快速开始

### 5 分钟上手

1. **阅读主文档：** `SKILL.md`（理解整体架构）
2. **查看快速指南：** `QUICKSTART.md`（5 分钟快速上手）
3. **参考实战案例：** `examples/case-study.md`（真实案例参考）

### 使用示例

**场景 1：从 0 到 1 搭建业务**
```
@ant 帮我搭建基金互金电商业务的工作流
```

**场景 2：优化现有工作流**
```
@ant 使用 fund-operation-workflow skill，诊断当前问题
```

**场景 3：团队角色分配**
```
@ant 我们团队 6 人，如何用 MBTI 分配工作流角色？
```

---

## 📁 目录结构

```
fund-operation-workflow/
├── SKILL.md                          # 技能主文档（必读）
├── README.md                         # 入口文档（本文件）
├── QUICKSTART.md                     # 快速启动指南
│
├── references/                       # 参考文档
│   ├── mbti-mapping.md              # MBTI 特质匹配详解
│   ├── compliance-checklist.md      # 合规检查清单（按节点）
│   └── star-framework.md            # STAR+ 合规前置框架详解（v2.0 新增）
│
├── prompts/                          # 提示词模板（v2.0 已升级）
│   ├── 01-collect-enfp.md           # 收集节点（ENFP）
│   ├── 02-archive-istj.md           # 归档节点（ISTJ）
│   ├── 03-strategy-intp.md          # 策略节点（INTP）
│   ├── 04-implement-entj.md         # 实施节点（ENTJ）
│   ├── 05-test-isfj.md              # 测试节点（ISFJ）
│   └── 06-monitor-infj.md           # 监控节点（INFJ）
│
└── examples/                         # 实战案例
    └── case-study.md                # 完整实战案例
```

---

## 🎯 适用场景

### ✅ 推荐使用

- 基金公司从 0 到 1 搭建互金电商业务
- 运营团队分工与角色分配
- 工作流 SOP 标准化
- 合规审查嵌入日常工作流
- 现有工作流优化与迭代

### ❌ 不推荐使用

- 非金融行业的运营工作（需调整合规部分）
- 个人投资者（本技能面向机构）
- 替代专业合规审查（需配合持牌合规人员）

---

## 📊 技能类型

| 维度 | 说明 |
|------|------|
| **技能类型** | 通用技能 🟡 |
| **Anthropic 分类** | 业务流程与团队自动化 |
| **复杂度** | 中高（6 节点 + MBTI 匹配 + 合规） |
| **使用频率** | 项目制（从 0 到 1 或季度优化） |

---

## 🔑 核心亮点

### 1. MBTI 特质精准匹配

每个节点匹配最适合的 MBTI 类型，发挥人格优势：

| 节点 | MBTI | 匹配理由 |
|------|------|---------|
| 收集 | ENFP | 思维跳跃，发现他人难以察觉的新想法 |
| 归档 | ISTJ | 遵守规则，有条理，可靠执行 |
| 策略 | INTP | 逻辑推理，系统性分析复杂问题 |
| 实施 | ENTJ | 迅速制定计划，高效领导团队 |
| 测试 | ISFJ | 可靠完成任务，关注细节 |
| 监控 | INFJ | 洞察力，理解复杂模型概念 |

### 2. TASK+ 合规提示词

每个节点内置合规检查清单，确保业务合规：

- ✅ 适当性管理
- ✅ 营销话术合规
- ✅ 数据隐私保护
- ✅ 用户分层公平性
- ✅ 合规测试覆盖

### 3. 实战案例参考

提供完整的实战案例，包括：

- 从 0 到 1 搭建过程
- 各节点执行细节
- 踩坑记录与经验总结
- 可复用资产（SOP/模板/工具）

---

## ⚠️ 重要注意事项

### 1. MBTI 是参考，不是绝对

- ✅ 作为角色分配的参考框架
- ❌ 不要机械匹配，忽视实际能力
- ✅ 允许跨类型协作，发挥互补优势

### 2. 合规前置，不是后置

- ✅ 每个节点嵌入合规检查
- ❌ 不要等执行完再做合规审查
- ✅ 合规部门全程参与

### 3. 本技能不替代专业合规审查

- ✅ 作为合规工作的辅助工具
- ❌ 不替代持牌合规人员的专业审查
- ✅ 需配合具体公司实际情况调整

---

## 📚 学习路径

### 入门（1 天）
- [ ] 阅读 `SKILL.md`
- [ ] 阅读 `QUICKSTART.md`
- [ ] 了解 MBTI 基础概念

### 进阶（1 周）
- [ ] 精读 `references/mbti-mapping.md`
- [ ] 精读 `references/compliance-checklist.md`
- [ ] 阅读 `examples/case-study.md`

### 实战（1 月）
- [ ] 选择具体业务场景
- [ ] 完整跑通 6 个节点
- [ ] 产出实际成果

### 精通（3 月+）
- [ ] 优化提示词模板
- [ ] 沉淀 SOP 和最佳实践
- [ ] 分享给其他团队

---

## 🔗 相关技能

- `decision-system` - 决策系统（配合战略层决策）
- `proactive-agent` - 主动代理（自动化执行）
- `investment-framework` - 投资框架（宏观视角）

---

## 📊 使用统计

- ⭐ GitHub Star: [![GitHub stars](https://img.shields.io/github/stars/lj22503/fund-operation-workflow?style=social)](https://github.com/lj22503/fund-operation-workflow/stargazers)
- 📥 ClawHub 下载：[查看统计](https://clawhub.com/skills/fund-operation-workflow)
- 👥 活跃用户：[USAGE_TRACKING.md](USAGE_TRACKING.md)

**你也在用？** [登记使用情况](USAGE_TRACKING.md)，领取福利包！

---

## 🎁 福利与追踪

### 领取福利包

**完成使用登记，你将获得：**
- 📦 完整提示词模板包（6 大节点×子节点，Markdown 可编辑版）
- 📋 STAR+ 合规前置框架速查卡（PDF 可打印）
- ✅ 合规检查清单（可打印版）
- 💬 加入"基金运营 AI 交流群"

**登记方式：**
1. 微信登记（推荐）：扫描二维码，回复"运营工作流"
2. 飞书表格：https://my.feishu.cn/base/xxxxxx
3. GitHub Issue：https://github.com/lj22503/fund-operation-workflow/issues/1

**👉 详情查看：** [USAGE_TRACKING.md](USAGE_TRACKING.md)

---

## 📞 支持与反馈

- **问题反馈**：[GitHub Issues](https://github.com/lj22503/fund-operation-workflow/issues)
- **使用登记**：[USAGE_TRACKING.md](USAGE_TRACKING.md)
- **微信咨询**：[你的微信号]
- **作者**：燃冰 + ant
- **版本**：v2.0.0（2026-03-26 升级）

**贡献者：**
- 燃冰：需求提出 + 架构设计
- ant：Skill 设计与文档编写

---

## 📝 更新日志

### v1.0.0 (2026-03-26)
- ✅ 初始版本发布
- ✅ 完成 6 个节点提示词模板
- ✅ 完成 MBTI 匹配详解
- ✅ 完成合规检查清单
- ✅ 完成实战案例

---

## 📄 许可证

本技能采用 [待填写] 许可证。

---

*祝你使用愉快！如有任何问题，欢迎反馈。*
