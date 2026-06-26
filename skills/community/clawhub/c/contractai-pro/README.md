# 📋 ContractAI Pro - 专业级合同审查专家

> 让AI成为你的专属法务，3分钟完成专业合同审查

## ✨ 功能特性

### 🔍 智能风险识别
- 8大风险规则库，覆盖常见合同陷阱
- 自动分级：高/中/低三级风险
- 精准定位：显示风险条款所在行号
- 法律依据：引用《民法典》等法律法规

### ✍️ 合同自动生成
- 4大类合同模板：买卖合同、劳动合同、房屋租赁合同、保密协议
- 一键填充：自动生成合同编号、日期等
- 金额大写：自动转换中文大写金额

### 📊 专业审查报告
- 风险统计汇总
- 逐条风险详情分析
- 修改建议优先级排序
- 总体评价和签署建议

## 🚀 快速开始

### 安装依赖
```bash
# Python 3.6+ 即可运行，无需额外依赖
python --version
```

### 合同审查
```bash
# 基本审查
python scripts/review_contract.py --file examples/sample_contract.txt

# 导出审查报告
python scripts/review_contract.py --file contract.txt --export report.md

# 简要输出（仅显示风险统计）
python scripts/review_contract.py --file contract.txt --brief
```

### 合同生成
```bash
# 查看可用模板
python scripts/generate_contract.py --list

# 生成买卖合同
python scripts/generate_contract.py \
  --template 买卖合同 \
  --partyA "甲方公司名称" \
  --partyA_rep "法定代表人姓名" \
  --partyA_addr "甲方地址" \
  --partyA_tel "甲方电话" \
  --partyB "乙方公司名称" \
  --partyB_rep "乙方代表人" \
  --partyB_addr "乙方地址" \
  --partyB_tel "乙方电话" \
  --product_name "产品名称" \
  --product_spec "规格型号" \
  --quantity 100 \
  --unit_price 1000 \
  --total_amount 100000 \
  --output my_contract.md
```

## 📋 风险规则说明

| 规则ID | 风险名称 | 风险等级 | 说明 |
|-------|---------|---------|------|
| R001 | 违约金比例过高 | 🔴高 | 超过30%可能被法院调减 |
| R002 | 单方解约权不对等 | 🔴高 | 违反公平原则，可能无效 |
| R003 | 争议解决地不利 | 🟡中 | 增加维权成本 |
| R004 | 保密期限过长 | 🟡中 | 实际履行困难 |
| R005 | 试用期超期 | 🔴高 | 违反《劳动合同法》 |
| R006 | 竞业补偿过低 | 🟡中 | 低于法定标准 |
| R007 | 免责条款过宽 | 🔴高 | 可能被认定无效 |
| R008 | 缺少必备条款 | 🟡中 | 合同完整性不足 |

## 📂 目录结构

```
contract-review-pro/
├── SKILL.md              # 技能说明文档
├── README.md             # 使用说明
├── scripts/              # 脚本目录
│   ├── review_contract.py    # 合同审查脚本
│   └── generate_contract.py  # 合同生成脚本
├── templates/            # 模板目录（可扩展）
└── examples/             # 示例文件
    ├── sample_contract.txt   # 示例合同
    └── generated_contract.md # 生成的合同示例
```

## 🎯 使用场景

### 🏢 企业法务
- 快速筛查合同风险
- 批量审查采购/销售合同
- 生成标准合同模板

### 👔 企业管理者
- 合同签署前风险自查
- 了解合同关键条款
- 避免常见合同陷阱

### 💼 创业者
- 快速生成标准合同
- 降低法务成本
- 规避法律风险

## ⚠️ 重要提示

1. **本工具仅供参考**，AI审查结果不能替代专业法律意见
2. **重要合同请咨询律师**，特别是涉及大额交易或复杂条款时
3. **使用前请备份**原始合同文件
4. **定期更新规则库**以适应最新法律法规

## 🔧 扩展开发

### 添加新的风险规则
编辑 `scripts/review_contract.py` 中的 `RISK_RULES` 列表，添加新的规则：

```python
{
    "id": "R009",
    "name": "风险名称",
    "level": "high",  # high/medium/low
    "category": "分类",
    "patterns": [r"正则表达式1", r"正则表达式2"],
    "risk": "风险说明",
    "suggestion": "修改建议",
    "law_ref": "法律依据"
}
```

### 添加新的合同模板
编辑 `scripts/generate_contract.py` 中的 `CONTRACT_TEMPLATES` 字典：

```python
"新模板名称": {
    "name": "模板显示名称",
    "description": "模板说明",
    "template": """模板内容，使用{变量名}占位""",
    "required_fields": ["变量1", "变量2", ...]
}
```

## 📞 技术支持

如有问题或建议，欢迎反馈。

---

**让AI守护你的每一份合同！** 🛡️
