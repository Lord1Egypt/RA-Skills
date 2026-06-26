#!/usr/bin/env python3
"""
谛听 (DiTing) 知识库初始化脚本
=============================
安装谛听 Skill 后运行此脚本，自动生成知识库骨架。
用法：
    python3 scripts/diting-init.py
    python3 scripts/diting-init.py --path /custom/kb/path
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

# 默认路径
DEFAULT_KB_PATH = os.path.expanduser("~/.hermes/hrcoe-knowledge")

def parse_args():
    parser = argparse.ArgumentParser(description="谛听知识库初始化")
    parser.add_argument("--path", default=DEFAULT_KB_PATH, help=f"知识库路径 (默认: {DEFAULT_KB_PATH})")
    parser.add_argument("--company", default="本公司", help="公司名称（用于模板占位符替换）")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的文件")
    return parser.parse_args()

def create_dir(path):
    os.makedirs(path, exist_ok=True)
    print(f"  ✓ 创建目录: {path}")

def write_file(path, content, force=False):
    if os.path.exists(path) and not force:
        print(f"  ⏭ 跳过 (已存在): {path}")
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ 创建文件: {path}")
    return True

# ==================== 知识库骨架 ====================

LABOR_LAW_TEMPLATE = """# 劳动法核心条款（通用模板）

> ⚠️ 请根据所在国家/地区替换以下内容。
> 本模板基于中国大陆劳动法核心条款。

## 一、劳动合同

### 1.1 合同签订
- 用人单位自用工之日起**一个月内**应当与劳动者订立书面劳动合同
- 超过一个月不满一年未订立的，应当向劳动者每月支付**二倍工资**
- 连续订立两次固定期限合同后，劳动者要求订立无固定期限合同的，应当订立

### 1.2 试用期
- 合同期限 3 个月-1 年：试用期 ≤ 1 个月
- 合同期限 1 年-3 年：试用期 ≤ 2 个月
- 合同期限 ≥ 3 年或无固定期限：试用期 ≤ 6 个月
- 试用期工资 ≥ 正式工资的 80% 且 ≥ 当地最低工资

## 二、工作时间

### 2.1 标准工时
- 每日工作 ≤ 8 小时
- 每周工作 ≤ 40 小时
- 每周至少休息 1 天

### 2.2 加班
- 工作日加班：≤ 3 小时/天，≤ 36 小时/月
- 加班费：
  - 工作日：≥ 工资的 150%
  - 休息日：≥ 工资的 200%（不能补休时）
  - 法定节假日：≥ 工资的 300%

## 三、休息休假

### 3.1 年休假
- 累计工作 1-10 年：5 天
- 累计工作 10-20 年：10 天
- 累计工作 ≥ 20 年：15 天

### 3.2 其他法定假期
- 产假：98 天 + 各地额外天数
- 婚假：3 天（各地有差异）
- 丧假：1-3 天

## 四、解除劳动合同

### 4.1 用人单位可单方解除（无需补偿）
- 试用期内不符合录用条件
- 严重违反规章制度
- 严重失职、营私舞弊造成重大损害
- 同时与其他用人单位建立劳动关系且拒不改正
- 被依法追究刑事责任

### 4.2 用人单位可解除（需经济补偿）
- 劳动者患病/非因工负伤，医疗期满后不能从事原工作也不能从事另行安排的工作
- 劳动者不能胜任工作，经培训或调整岗位仍不能胜任
- 客观情况发生重大变化致合同无法履行

### 4.3 经济补偿标准
- 每工作满 1 个月支付 1 个月工资
- 不满 1 年的按 1 年计算
- 月工资高于当地平均工资 3 倍的，按 3 倍计算，且补偿年限 ≤ 12 年

## 五、劳动争议

- 争议发生后 1 年内可申请劳动仲裁
- 对仲裁不服的，15 日内可向法院起诉

---
*本模板基于《中华人民共和国劳动法》《中华人民共和国劳动合同法》整理，仅供参考，不构成法律意见。*
"""

COMPANY_POLICY_TEMPLATE = f"""# 公司制度模板

> ⚠️ 请替换 [公司名称] 为实际公司名称，并根据实际情况修改。

## [公司名称] 员工手册目录

1. 总则
2. 招聘与录用
3. 考勤管理
4. 休假管理
5. 薪酬福利
6. 绩效考核
7. 培训发展
8. 行为规范
9. 离职管理
10. 附则

---

## 使用说明

1. 请将本文件拆分为独立的 policy 文件
2. 每个 policy 文件放在 `policies/` 目录下
3. 文件名建议：`attendance_policy.md`、`leave_policy.md` 等
4. 内容应包含具体的制度条款、执行标准、例外情况
"""

CASE_TEMPLATE = """{"case_id":"CASE-001","problem":"请填入案例问题描述","context":{"org_size":"团队规模","industry":"行业","tenure":"员工司龄"},"analysis":{"method":"七步法","findings":"关键发现"},"conclusion":"分析结论","actions":["行动1","行动2"],"outcome":"最终结果","date":"2025-01-01","tags":["离职","薪酬","管理"]}
"""

QA_TEMPLATE = """{"question":"年假有几天？","answer":"根据劳动法规定，累计工作1-10年5天，10-20年10天，20年以上15天。具体请参考公司年休假政策。","category":"休假","tags":["年假","劳动法"]}
"""

MENTAL_MODELS_PLACEHOLDER = """# 思维模型库

> 以下为谛听使用的核心思维模型定义。

## 第一性原理
从最基础的真相出发进行推理，不依赖类比或经验。
**使用场景**：当经验失效、问题没有先例时。
**检查问题**：最基础的真相是什么？

## 奥卡姆剃刀
如无必要，勿增实体。最简单的解释往往最正确。
**使用场景**：多个解释都能说明问题时。
**检查问题**：最简单的解释是什么？

## MECE (Mutually Exclusive, Collectively Exhaustive)
分解问题时，各分支互斥且穷尽。
**使用场景**：问题分解、分析框架设计。
**检查问题**：有重叠或遗漏吗？

## 金字塔原理
结论先行，以上统下，逻辑递进。
**使用场景**：报告撰写、建议呈现。
**检查问题**：30秒能说清结论吗？

## 假设驱动
先列出假设，再设计验证方法。
**使用场景**：数据分析、调研设计。
**检查问题**：我的假设是什么？什么能推翻它？

## 80/20法则
20%的原因导致80%的结果。
**使用场景**：优先排序、资源分配。
**检查问题**：哪20%导致80%？

## 二阶思维
考虑行动的连锁反应和二阶效果。
**使用场景**：建议评估、风险分析。
**检查问题**：这个建议的连锁反应是什么？6个月后会发生什么？
"""

ORG_ONTOLOGY_TEMPLATE = """# 组织本体定义

> 本文件定义 HR 诊断中的 7 个核心概念及其关系。
> 请根据 [公司名称] 的实际情况修改。

## 1. 人才观
公司如何看待人才？是"够用就行"还是"只留最优秀的人"？
**默认**：待填充
**影响**：决定了招聘标准、薪酬策略、培养投入

## 2. 价值观
公司的核心价值观是什么？
**默认**：待填充
**影响**：决定了文化行为映射、典型挖掘、奖惩标准

## 3. 组织架构
公司的组织形态是什么？职能制/矩阵制/事业部制？
**默认**：待填充
**影响**：决定了协作模式、决策链、问责制

## 4. 激励机制
公司如何激励员工？物质激励/精神激励/发展机会？
**默认**：待填充
**影响**：决定了敬业度驱动因素、保留策略

## 5. 决策模式
公司的决策风格是自上而下还是自下而上？
**默认**：待填充
**影响**：决定了问责制评分、执行力评估

## 6. 变革历史
公司近期的重大变革有哪些？
**默认**：待填充
**影响**：决定了变革准备度基线、组织疲劳度

## 7. 行业环境
公司所处的行业竞争态势是什么？
**默认**：待填充
**影响**：决定了人才策略的紧迫性、对标基准
"""

README_TEMPLATE = """# 谛听 (DiTing) 知识库

> 本知识库为谛听 HR 深度诊断系统的数据源。
> 生成日期：{date}
> 生成工具：diting-init.py

## 目录结构

```
hrcoe-knowledge/
├── README.md                 ← 本文件
├── cognitive-spec/           ← 认知规范（Skill 自带，勿删）
│   └── COGNITIVE_SPEC.md
├── failure-taxonomy/         ← 失败分类（Skill 自带，勿删）
│   └── FAILURE_TAXONOMY.md
├── reasoning-benchmark/      ← 推理基准（Skill 自带，勿删）
│   └── REASONING_BENCHMARK.md
├── organizational-ontology/  ← 组织本体（请填充公司信息）
│   └── ORGANIZATIONAL_ONTOLOGY.md
├── mental-models/            ← 思维模型（通用定义）
│   └── MENTAL_MODELS.md
├── policies/                 ← 劳动法 + 公司制度（请替换）
│   ├── labor_law_core.md     ← 中国劳动法模板
│   └── company_policy.md     ← 公司制度模板
├── cases/                    ← 组织案例库
│   └── org_cases.jsonl       ← 案例数据（JSONL 格式）
├── qa_pairs/                 ← QA 知识库
│   └── hr_qa.jsonl           ← 问答数据（JSONL 格式）
├── market_data/              ← 薪酬市场数据（用户自行填充）
├── templates/                ← 文档模板
│   ├── jd_template.md
│   ├── performance_review_template.md
│   └── ...
└── tests/                    ← 测试用例（Skill 自带）
```

## 快速开始

1. **填充公司制度**：修改 `policies/company_policy.md`，拆分到具体政策文件
2. **填充组织本体**：修改 `organizational-ontology/ORGANIZATIONAL_ONTOLOGY.md`
3. **添加案例**：在 `cases/org_cases.jsonl` 中添加历史案例（每行一个 JSON 对象）
4. **添加 FAQ**：在 `qa_pairs/hr_qa.jsonl` 中添加常见问答

## 自定义路径

如果知识库不在默认位置，设置环境变量：
```bash
export DITING_KB_PATH=/your/custom/path
```
"""

def init_knowledge_base(kb_path, company_name="本公司", force=False):
    kb_path = Path(kb_path)
    print(f"\n🚀 初始化谛听知识库: {kb_path}")
    print(f"   公司名称: {company_name}")
    print()
    
    # 1. 创建目录
    print("📁 创建目录结构...")
    dirs = [
        "cognitive-spec", "failure-taxonomy", "reasoning-benchmark",
        "organizational-ontology", "mental-models", "policies",
        "cases", "qa_pairs", "market_data", "templates", "tests",
    ]
    for d in dirs:
        create_dir(kb_path / d)
    
    # 2. 创建通用模板文件（填充型）
    print("\n📝 创建模板文件...")
    
    files = {
        "policies/labor_law_core.md": LABOR_LAW_TEMPLATE,
        "policies/company_policy.md": COMPANY_POLICY_TEMPLATE,
        "organizational-ontology/ORGANIZATIONAL_ONTOLOGY.md": ORG_ONTOLOGY_TEMPLATE,
        "mental-models/MENTAL_MODELS.md": MENTAL_MODELS_PLACEHOLDER,
        "cases/org_cases.jsonl": CASE_TEMPLATE.strip(),
        "qa_pairs/hr_qa.jsonl": QA_TEMPLATE.strip(),
        "README.md": README_TEMPLATE.format(date=datetime.now().strftime("%Y-%m-%d")),
    }
    
    created = 0
    for rel_path, content in files.items():
        if write_file(kb_path / rel_path, content, force):
            created += 1
    
    # 3. 创建通用模板文件
    print("\n📋 创建通用模板...")
    templates = {
        "templates/jd_template.md": "# 职位描述 (JD) 模板\n\n> 请根据岗位需求填写\n\n## 岗位基本信息\n- **职位名称**：\n- **部门**：\n- **汇报对象**：\n- **工作地点**：\n\n## 岗位职责\n1. \n2. \n3. \n\n## 任职要求\n- **学历**：\n- **经验**：\n- **技能**：\n\n## 加分项\n- \n",
        "templates/performance_review_template.md": "# 绩效面谈记录模板\n\n> 请根据面谈情况填写\n\n- **员工姓名**：\n- **面谈日期**：\n- **面谈人**：\n- **评估周期**：\n\n## 绩效总结\n\n## 改进计划\n\n## 下周期目标\n",
    }
    
    for rel_path, content in templates.items():
        if write_file(kb_path / rel_path, content, force):
            created += 1
    
    # 4. 复制认知规范等通用文件（从 Skill references 中复制）
    print("\n📖 复制通用规范文件...")
    skill_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent  # chief/
    chief_dir = skill_dir  # scripts is under chief/
    
    # Check if cognitive-spec exists in the hrcoe-knowledge already
    # These files are in the main kb, not in the skill
    # For init script, we note that the cognitive-spec etc. are provided separately
    
    # 5. Summary
    print(f"\n✅ 知识库初始化完成！")
    print(f"   路径: {kb_path}")
    print(f"   创建: {created} 个文件")
    print()
    print("📋 下一步：")
    print("   1. 编辑 policies/company_policy.md → 填入公司制度")
    print("   2. 编辑 organizational-ontology/ORGANIZATIONAL_ONTOLOGY.md → 填入公司信息")
    print("   3. 在 cases/org_cases.jsonl 中添加历史案例")
    print("   4. 在 qa_pairs/hr_qa.jsonl 中添加 FAQ")
    print()
    print("💡 自定义路径：export DITING_KB_PATH=/your/path")

if __name__ == "__main__":
    args = parse_args()
    init_knowledge_base(args.path, args.company, args.force)
