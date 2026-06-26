# 企业AI应用诊断工具

帮助企业科学评估AI应用价值，制定可落地的AI转型方案。

## 快速开始

### 1. 运行快速诊断

```bash
cd ~/.openclaw/skills/enterprise-ai-diagnosis/scripts
python3 quick_start.py
```

### 2. 在对话中使用

```
你："帮我诊断一下我们公司能不能用AI"
小龙虾：运行诊断工具，生成完整报告
```

## 功能特点

- ✅ **10分钟快速评估** - 企业AI应用现状评估
- ✅ **AI价值分析** - 每个业务环节的AI适用性评分
- ✅ **ROI计算** - 投入产出比和回报周期
- ✅ **实施路径** - 分阶段实施计划
- ✅ **工具推荐** - 免费到专业工具推荐
- ✅ **风险提示** - 数据安全、员工抵触等风险

## 定价建议

| 版本 | 功能 | 定价 |
|------|------|------|
| 基础版 | 评估+分析 | 99元 |
| 专业版 | 完整诊断+ROI | 199元 |
| 企业版 | 专业版+咨询 | 499元 |

## 文件结构

```
enterprise-ai-diagnosis/
├── SKILL.md              # 技能说明
├── README.md             # 本文件
├── scripts/
│   ├── diagnosis_tool.py # 核心诊断工具
│   └── quick_start.py    # 快速启动脚本
├── templates/
│   └── questionnaire.md  # 问卷模板
└── references/
    ├── case-studies.md   # 案例研究
    └── tool-guide.md     # 工具指南
```

## 使用示例

### 示例1：完整诊断

```python
from diagnosis_tool import EnterpriseAIDiagnosis

diagnosis = EnterpriseAIDiagnosis()

# 1. 收集企业信息
enterprise_info = diagnosis.collect_enterprise_info({
    'company_name': '示例科技',
    'industry': '互联网',
    'scale': '50-100人',
    'employees': 80,
    'budget': 10000,
})

# 2. 分析业务流程
processes = diagnosis.analyze_business_processes([
    {'name': '客服', 'time_cost': 200, 'labor_cost': 30000},
    {'name': '营销', 'time_cost': 100, 'labor_cost': 20000},
])

# 3. 计算ROI
roi = diagnosis.calculate_roi(
    investment={'tools': 10000, 'training': 5000},
    savings={'labor': 50000, 'efficiency': 30000}
)

# 4. 生成报告
report = diagnosis.generate_report(enterprise_info, processes, roi, plan)
```

## 目标客户

- 中小企业主（50-500人）
- 创业者（0-50人团队）
- 企业数字化转型负责人

## 更新日志

- **2026-03-13** - 初始版本发布

---

**小龙虾制作** 🦞
