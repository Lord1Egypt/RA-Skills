# gaokao-volunteer

> 高考志愿填报AI助手 — WorkBuddy Skill

基于位次法和线差法，提供分数匹配、院校推荐、冲稳保方案生成、志愿梯度检查。覆盖全国31省新老高考模式。

## 功能

- 📊 分数定位：线差分析 + 位次换算 + 等效分跨年对比
- 🎯 院校匹配：位次法（主）+ 线差法（辅）双算法交叉验证
- 🚀 冲稳保方案：自动生成45/96/9志愿的结构化填报方案
- 📋 省份适配：14省志愿填报规则内置（湖北/广东/山东/浙江/四川/湖南...）
- 📄 HTML报告：交互式报告含梯度分布条、院校表格、风险警告
- 🔍 实时数据：WebSearch自动搜索当年批次线和投档线

## 触发方式

在 WorkBuddy 中说以下任意关键词即可激活：

- "帮我填志愿" / "高考志愿填报"
- "XX分能上什么大学"
- "冲稳保怎么填"
- "查分数线 / 院校推荐 / 专业推荐"

## 安装

### 方式一：直接安装
```bash
# 解压到 WorkBuddy skills 目录
unzip gaokao-volunteer.zip -d ~/.workbuddy/skills/
```

### 方式二：ClawHub 安装
在 ClawHub 搜索 "gaokao-volunteer" 一键安装。

## 技能结构

```
gaokao-volunteer/
├── SKILL.md                    # 主指令文件
├── README.md
├── scripts/
│   ├── ranking_matcher.py      # 位次法匹配引擎
│   ├── score_delta.py          # 线差法计算
│   ├── risk_classifier.py      # 冲稳保三档分类器
│   └── plan_generator.py       # HTML方案生成器
├── references/
│   ├── province_rules.json     # 14省填报规则
│   ├── university_basics.json  # 40+院校基础信息
│   └── major_catalog.json      # 14大类专业+关键词映射
└── assets/
    └── report_template.html    # HTML报告模板
```

## 使用示例

```
用户: 湖北物理类650分位次4500想学计算机
WorkBuddy: [搜索2026批次线] → [位次匹配] → [冲稳保分类] → [生成HTML报告]
```

示例报告预览：
![示例报告](./screenshot.png)

## License

MIT-0
