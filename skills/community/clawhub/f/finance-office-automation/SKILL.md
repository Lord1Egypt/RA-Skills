---
name: Financial Office Automation Assistant
slug: finance-office-automation
description: AI-powered financial office automation — covers document processing, meeting minutes, email drafting, report summarization, and workflow automation. Built for financial professionals' daily productivity. Keywords: office automation, document processing, workflow automation, productivity tools, 办公自动化, 文档处理, 工作流自动化, 效率工具, 会议纪要, 邮件起草, 报告撰写, 智能助手, RPA, 流程机器人.
version: "3.0.1"
---

# Financial Office Automation Assistant / 金融办公自动化助手

> **English:** AI-powered office automation — covers documents, emails, reports, workflows.
>
> **中文:** 办公自动化——覆盖文档、邮件、报告、工作流。

---


### 金融监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 金融监管 | 2026年Q1：金融办公自动化合规要求提升 | 办公自动化模板需纳入2026年合规要求 |
| 金融监管 | 监管报告模板需更新（NFRA新规、反洗钱等） | 办公自动化模板需纳入2026年合规要求 |
| 金融监管 | 内部审批流程需纳入合规审查节点 | 办公自动化模板需纳入2026年合规要求 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **重复工作多** | 报表、报告重复劳动 | 自动化模板 |
| **沟通效率低** | 邮件、纪要耗时长 | AI辅助写作 |
| **文档格式乱** | 格式不统一 | 标准模板 |
| **流程繁琐** | 审批流程长 | 工作流优化 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** office automation, document processing, workflow automation, productivity tools

**中文触发词（优先）：** 办公自动化 / 文档处理 / 工作流 / 效率工具 / 邮件 / 会议纪要 / 报告 / 审批

---

## Core Capabilities / 核心能力

### 1. Document Templates / 文档模板

```python
DOCUMENT_TEMPLATES = {
    "会议纪要": {
        "结构": "会议基本信息 → 讨论事项 → 决议 → 行动项 → 下次会议安排",
        "要素": ["时间", "参与人", "议题", "决议", "责任人", "截止日期"]
    },
    "工作邮件": {
        "类型": ["请示邮件", "汇报邮件", "知会邮件", "邀请邮件"],
        "结构": "称呼 → 正文 → 行动呼吁 → 落款"
    },
    "周报/月报": {
        "结构": "本周/本月总结 → 主要成果 → 问题与挑战 → 下周/下月计划"
    }
}
```

### 2. Workflow Templates / 工作流模板

```python
WORKFLOW_TEMPLATES = {
    "合同审批": {
        "步骤": ["发起申请", "部门负责人审核", "法务审核", "财务审核", "分管领导审批", "完成归档"],
        "时限": [1, 2, 3, 2, 1]
    },
    "报销审批": {
        "步骤": ["提交发票", "部门初审", "财务复核", "领导审批", "出纳付款"],
        "时限": [1, 1, 2, 1, 1],
        "金额阈值": {
            "<1000": "部门负责人审批",
            "1000-5000": "财务复核",
            ">5000": "领导审批"
        }
    }
}
```

---

## Disclaimer

This skill provides office automation tools for educational purposes.
