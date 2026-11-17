# 认知偏差顾问 (Cognitive Bias Advisor)

覆盖**决策、学习、行动、沟通、影响、管理**六大人生领域的认知偏差 Skill。基于查理·芒格"人类误判心理学"+经典认知偏差理论，通过领域路由+逐题诊断帮助用户识别思维盲区，输出偏差应对策略和话术模板。

## 六大领域

| 领域 | 核心能力 | 偏差数 |
|------|---------|--------|
| 🎯 决策 | 十问框架自检 + 自适应/完整/极速三模式 + 评估报告 | 10 |
| 📚 学习 | 达克效应/后见之明/知识诅咒/避免不一致性 | 6 |
| 🚀 行动 | 现状偏误/双曲贴现/决策疲劳 | 5 |
| 💬 沟通 | 谈判/反馈/亲子/日常四场景 + 三步说服法 | 5 |
| 🧲 影响 | 默认效应/社会证明/稀缺效应 | 6 |
| 👥 管理 | 红队蓝队/止损触发器/匿行评估/推翻奖励 | 9 |

> 完整的触发词表、使用流程、恢复机制见 [SKILL.md](./SKILL.md)。

## 安装

### ClawHub

```bash
clawhub skill install cognitive-bias-advisor
```

### SkillHub.cn

访问 [SkillHub Marketplace](https://skillhub.cn) 搜索「认知偏差决策顾问」，或 CLI 安装：

```bash
skillhub install cognitive-bias-advisor-pro
```

### GitHub 手动安装

```bash
git clone https://github.com/jacksu/cognitive-bias-advisor.git
# 将 SKILL.md + references/ 放入 Agent skills 目录
```

或下载 [最新 Release](https://github.com/jacksu/cognitive-bias-advisor/releases) ZIP 解压。

### 验证

在 Agent 中输入 `帮我决策一件事`，若进入引导流程即安装成功。

## 文件结构

```
SKILL.md                     # 主入口：触发条件 + 领域路由 + 输出模板 + 反例黑名单
references/
├── q1-*.md ~ q10-*.md       # 决策十问题库（10 个）
├── bias-*.md                # 芒格倾向参考（3 个）
└── domain-*.md              # 六领域诊断流程（6 个）
```

## 许可

MIT © [认知偏差决策顾问](https://github.com/jacksu/cognitive-bias-advisor)
