# 度量衡商事调解智库 v2.0 快速开始指南

## 版本信息

- **版本**: 2.0
- **更新时间**: 2026年4月
- **核心升级**: 案件管理 + 类案检索 + 证据管理 + 进度看板

---

## 一、安装配置

### 1.1 环境要求

```bash
# Python 3.8+
python --version

# 安装依赖
pip install dashscope
```

### 1.2 API Key配置

```bash
# 通义法睿（法律AI增强）
export DASHSCOPE_API_KEY="sk-xxxx"
```

---

## 二、核心功能速查

### 2.1 类案检索

```python
from case_retriever import get_mediation_advice, search_similar_cases

# 获取调解建议报告
report = get_mediation_advice("工期延误", "工期延误责任划分")
print(report)

# 快速检索
cases = search_similar_cases("工程款纠纷", limit=3)
for c in cases:
    print(f"- {c.title}")
```

### 2.2 案件管理

```python
from case_manager import CaseManager, create_new_case

# 快速创建案件
case = create_new_case(
    case_name="某房地产项目工程款纠纷",
    dispute_type="工程款纠纷",
    parties=[
        {"name": "A公司", "role": "发包人", "contact": "138xxxx", "representative": "张某"},
        {"name": "B公司", "role": "承包人", "contact": "139xxxx", "representative": "李某"}
    ],
    amount=8000000
)
print(f"案件ID: {case.case_id}")

# 完整操作
manager = CaseManager()
# 添加争议焦点
manager.add_dispute_point(case.case_id, "工程款金额争议", 3000000, priority=1)
# 记录调解事件
manager.add_event(case.case_id, "首次调解", "双方初步协商", ["张某", "李某"])
# 更新状态
manager.update_case_status(case.case_id, "调解中")
```

### 2.3 证据管理

```python
from evidence_manager import EvidenceManager, submit_evidence

# 提交证据
ev = submit_evidence(
    case_id="CASE-20260404-001",
    evidence_type="合同文件",
    name="建设工程施工合同",
    submitter="承包人",
    description="主合同，约定付款方式"
)
print(f"证据ID: {ev.evidence_id}")

# 审查证据
manager = EvidenceManager()
manager.verify_evidence(
    ev.evidence_id,
    weight="高",
    authenticity="真实有效",
    validity="合法、关联性高"
)

# 生成证据清单
evidence_list = manager.generate_evidence_list(case_id)
print(evidence_list)
```

### 2.4 进度看板

```python
from mediation_dashboard import show_dashboard, show_gantt, get_stats
from case_manager import CaseManager

# 关联案件管理器
case_manager = CaseManager()
dashboard = MediationDashboard(case_manager)

# 显示看板
print(show_dashboard(case_id))

# 显示甘特图
print(show_gantt(case_id))

# 统计信息
stats = get_stats(case_manager)
print(stats)
```

### 2.5 法律AI增强

```python
from legal_ai_hub import legal_search, case_analysis

# 法律检索
result = legal_search("工程款优先受偿权的行使条件")
print(result)

# 案件分析
result = case_analysis("发包人拖欠工程款800万元")
print(result)
```

---

## 三、工作流程示例

### 完整调解流程

```python
# 1. 创建案件
from case_manager import create_new_case
case = create_new_case("某项目工程款纠纷", "工程款纠纷", parties, 8000000)

# 2. 添加争议焦点
from case_manager import CaseManager
manager = CaseManager()
manager.add_dispute_point(case.case_id, "工程款金额", 5000000)
manager.add_dispute_point(case.case_id, "工期延误责任", 3000000)

# 3. 提交证据
from evidence_manager import submit_evidence
submit_evidence(case.case_id, "合同文件", "施工合同", "发包人")
submit_evidence(case.case_id, "变更签证", "签证单#12", "承包人")

# 4. 获取类案参考
from case_retriever import get_mediation_advice
advice = get_mediation_advice("工程款纠纷", "工程款支付条件")

# 5. 记录调解进展
manager.add_event(case.case_id, "首次调解会议", "双方确认争议金额")

# 6. 查看进度
from mediation_dashboard import show_dashboard
print(show_dashboard(case.case_id))

# 7. 达成协议后更新状态
manager.update_case_status(case.case_id, "达成协议")
```

---

## 四、模块对应表

| 功能 | 模块文件 | 主要类 |
|-----|---------|-------|
| 类案检索 | `case_retriever.py` | `CaseRetriever` |
| 案件管理 | `case_manager.py` | `CaseManager` |
| 证据管理 | `evidence_manager.py` | `EvidenceManager` |
| 进度看板 | `mediation_dashboard.py` | `MediationDashboard` |
| AI集成 | `legal_ai_hub.py` | `LegalAIHub` |

---

## 五、常见问题

**Q1: 如何查看所有案件？**
```python
from case_manager import list_all_cases
cases = list_all_cases()  # 所有案件
cases = list_all_cases(status="调解中")  # 筛选状态
```

**Q2: 证据链如何构建？**
```python
chain = manager.build_evidence_chain(
    case_id="xxx",
    dispute_point="工程款争议",
    evidence_ids=["EV-xxx-001", "EV-xxx-002"],
    chain_logic="合同+签证+验收报告形成完整证据链",
    conclusion="支持承包人主张"
)
```

**Q3: 如何对接通义法睿？**
```python
# 确保已配置环境变量
import os
os.environ["DASHSCOPE_API_KEY"] = "your-key"

from legal_ai_hub import legal_search
result = legal_search("工程款优先受偿权")
```

---

## 六、文件结构

```
construction-mediation-kg/
├── SKILL.md                      # 技能主文档
├── manifest.json                 # 技能清单
├── scripts/
│   ├── farui_integration.py      # 通义法睿集成
│   ├── legal_ai_hub.py           # 多后端AI集成
│   ├── case_retriever.py         # 类案检索 ⭐新增
│   ├── case_manager.py           # 案件管理 ⭐新增
│   ├── evidence_manager.py       # 证据管理 ⭐新增
│   ├── mediation_dashboard.py    # 进度看板 ⭐新增
│   └── farui_quickstart.md       # AI集成指南
├── references/                   # 参考资源
│   ├── dispute-types.md
│   ├── batna-framework.md
│   └── ...
└── assets/                       # 静态资源
```

---

## 七、下一步

1. **体验完整流程**：使用上述示例代码创建测试案件
2. **对接AI能力**：配置API Key后测试法律检索
3. **扩展案例库**：在 `case_retriever.py` 中添加更多类案
4. **集成外部系统**：对接MetaLaw等类案检索API

---

**技术支持**：如有问题，请提供具体场景描述。