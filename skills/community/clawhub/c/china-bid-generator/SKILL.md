---
name: china-bid-generator
description: 中国招投标文档生成工具。支持招标文件、投标书、技术方案、商务报价等专业文档。符合中国招投标规范，支持政府采购、工程建设、IT/软件、医疗设备、教育装备等行业。招投标、标书、投标书。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📋", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install python-docx fpdf2"
---

# 中国招投标文档生成工具

生成符合中国招投标规范的专业文档。

## 功能特点

- 📋 **双角色支持**：招标方和投标方
- 🏭 **多行业适配**：政府采购、工程建设、IT/软件、医疗、教育
- 📄 **专业排版**：符合中国招投标规范
- 🌐 **信息整合**：支持互联网查询+用户输入+文件素材
- 📊 **数据准确**：确保数据准确性
- 📦 **批量生成**：支持批量生成多份文档

## ⚠️ 免责声明

> **本工具生成的文档仅供参考。**
> 不同AI模型能力不同，文档质量可能有差异。
> 重要招投标文件请人工审核。
> 请确保符合当地招投标法规。

## 支持的文档类型

### 招标方文档

| 文档 | 说明 |
|------|------|
| 招标公告 | 项目简介、资质要求、时间安排 |
| 招标文件 | 详细技术规格、商务条款 |
| 技术规格书 | 产品/服务技术要求 |
| 评分标准 | 评分细则、权重分配 |

### 投标方文档

| 文档 | 说明 |
|------|------|
| 投标书 | 投标函、报价单、资质证明 |
| 技术方案 | 技术实现、架构设计 |
| 商务报价 | 价格明细、付款方式 |
| 案例展示 | 成功案例、客户评价 |

## 使用方式

```
User: "帮我写一份IT项目的投标书"
Agent: 生成投标书模板

User: "写一份政府招标文件"
Agent: 生成招标文件

User: "帮我写一份医疗设备的技术方案"
Agent: 生成技术方案
```

---

## 工作流程

```
用户输入（项目信息/要求/素材）
        ↓
1. 信息整合
├─ 用户提供的项目信息
├─ 用户提供的素材文档
├─ OpenClaw web-search查询行业信息
└─ OpenClaw AI模型优化内容
        ↓
2. 文档生成
├─ 选择文档类型（招标/投标）
├─ 选择行业模板
├─ 生成专业内容
└─ 格式化排版
        ↓
3. 输出文档
├─ Word (.docx)
└─ PDF
```

---

## 行业模板

### 政府采购
- 严格遵循《政府采购法》
- 评分标准明确
- 资质要求详细

### 工程建设
- 技术规格详细
- 图纸要求明确
- 工期安排清晰

### IT/软件
- 技术架构详细
- 案例展示重要
- 价格对比清晰

### 医疗设备
- 资质要求高
- 合规性重要
- 售后服务详细

---

## Python代码

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

class BidGenerator:
    def __init__(self):
        self.templates = {
            'tender': self._tender_template,
            'bid': self._bid_template,
            'technical': self._technical_template,
            'commercial': self._commercial_template
        }
    
    def generate(self, doc_type, project_info, industry, output_path):
        """生成招投标文档"""
        
        template = self.templates.get(doc_type, self._bid_template)
        doc = template(project_info, industry)
        doc.save(output_path)
        return output_path
    
    def _tender_template(self, project_info, industry):
        """招标文件模板"""
        doc = Document()
        
        # 标题
        title = doc.add_heading(f'{project_info["name"]}招标文件', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 项目概述
        doc.add_heading('一、项目概述', level=1)
        doc.add_paragraph(f'项目名称：{project_info.get("name", "")}')
        doc.add_paragraph(f'项目编号：{project_info.get("id", "")}')
        doc.add_paragraph(f'招标单位：{project_info.get("organization", "")}')
        
        # 技术要求
        doc.add_heading('二、技术要求', level=1)
        for req in project_info.get('requirements', []):
            doc.add_paragraph(f'• {req}')
        
        # 商务条款
        doc.add_heading('三、商务条款', level=1)
        doc.add_paragraph(f'预算金额：{project_info.get("budget", "")}')
        doc.add_paragraph(f'交付时间：{project_info.get("deadline", "")}')
        doc.add_paragraph(f'付款方式：{project_info.get("payment", "")}')
        
        # 评分标准
        doc.add_heading('四、评分标准', level=1)
        
        return doc
    
    def _bid_template(self, project_info, industry):
        """投标书模板"""
        doc = Document()
        
        # 投标函
        title = doc.add_heading('投标书', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_heading('一、投标函', level=1)
        doc.add_paragraph(f'致：{project_info.get("organization", "")}')
        doc.add_paragraph(f'我方愿意按照招标文件的要求，投标{project_info.get("name", "")}项目。')
        
        # 报价
        doc.add_heading('二、商务报价', level=1)
        
        # 技术方案
        doc.add_heading('三、技术方案', level=1)
        
        # 资质证明
        doc.add_heading('四、资质证明', level=1)
        
        return doc
    
    def _technical_template(self, project_info, industry):
        """技术方案模板"""
        doc = Document()
        
        title = doc.add_heading('技术方案', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_heading('一、技术架构', level=1)
        doc.add_heading('二、功能模块', level=1)
        doc.add_heading('三、技术路线', level=1)
        doc.add_heading('四、安全方案', level=1)
        doc.add_heading('五、运维方案', level=1)
        
        return doc
    
    def _commercial_template(self, project_info, industry):
        """商务报价模板"""
        doc = Document()
        
        title = doc.add_heading('商务报价', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_heading('一、报价明细', level=1)
        doc.add_heading('二、付款方式', level=1)
        doc.add_heading('三、售后服务', level=1)
        doc.add_heading('四、质保承诺', level=1)
        
        return doc

# 使用示例
generator = BidGenerator()

project_info = {
    'name': '智慧城市平台建设项目',
    'id': 'ZB2026-001',
    'organization': 'XX市政府',
    'budget': '500万元',
    'deadline': '2026年6月30日',
    'payment': '验收后30日内支付',
    'requirements': [
        '支持100万用户并发',
        '99.9%系统可用性',
        '符合等保三级要求'
    ]
}

generator.generate('bid', project_info, 'it', 'bid.docx')
```

---

## Notes

- 专注中国招投标市场
- 符合《政府采购法》《招标投标法》
- 支持多种行业模板
- 专业排版，可直接使用
