#!/usr/bin/env python3
"""
知识库生成器 — 阶段3 自动化工具

用法:
  python3 knowledge_gen.py <workspace-path> <industry-type>

示例:
  python3 knowledge_gen.py ~/.qclaw/workspace-industrial-fund-diligence 股权投资
  
输出:
  workspace/<agent-id>/knowledge/industry_data.json
"""
import sys
import json
from pathlib import Path
from datetime import datetime

TEMPLATES = {
    "产业园区": {
        "data_sources": [
            "园区企业名录（ Excel/腾讯文档）",
            "房源销控表（腾讯文档智能表格）",
            "租金报价表（腾讯文档智能表格）",
            "客户跟进记录（腾讯文档智能表格）",
            "产业政策库（腾讯文档）",
            "竞品情报库（腾讯文档）"
        ],
        "report_templates": [
            "招商周报模板",
            "客户跟进记录模板",
            "选址建议书模板",
            "竞品分析报告模板"
        ]
    },
    "股权投资": {
        "data_sources": [
            "清科投资界数据库",
            "企查查/天眼查（企业工商信息）",
            "国家知识产权局（专利数据）",
            "上市公司财报（ PDF/网页）",
            "裁判文书网（法律诉讼）",
            "36氪/投资界/亿欧（新闻资讯）"
        ],
        "report_templates": [
            "尽调报告模板",
            "投资建议书模板",
            "估值模型模板（ Excel）"
        ]
    },
    "企业服务": {
        "data_sources": [
            "企业客户名录（腾讯文档）",
            "SLA工单记录（腾讯文档智能表格）",
            "费用催缴记录（腾讯文档智能表格）"
        ],
        "report_templates": [
            "企业服务周报模板",
            "SLA合规报告模板"
        ]
    },
    "房产": {
        "data_sources": [
            "房源数据库（腾讯文档智能表格）",
            "市场评估报告（ PDF/腾讯文档）",
            "客户偏好记录（腾讯文档）"
        ],
        "report_templates": [
            "房产分析报告模板",
            "投资建议书模板"
        ]
    }
}

def main():
    if len(sys.argv) < 3:
        print("用法: python3 knowledge_gen.py <workspace-path> <industry-type>")
        print("示例: python3 knowledge_gen.py ~/.qclaw/workspace-industrial-fund-diligence 股权投资")
        print("\n支持的行业类型: " + ", ".join(TEMPLATES.keys()))
        sys.exit(1)

    workspace = Path(sys.argv[1]).expanduser()
    industry = sys.argv[2]

    if not workspace.exists():
        print(f"❌ 工作区不存在: {workspace}")
        sys.exit(1)

    if industry not in TEMPLATES:
        print(f"❌ 不支持的行业类型: {industry}")
        print("支持的类型: " + ", ".join(TEMPLATES.keys()))
        sys.exit(1)

    # Create knowledge directory
    knowledge_dir = workspace / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    # Generate industry_data.json
    data = {
        "industry": industry,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "data_sources": TEMPLATES[industry]["data_sources"],
        "report_templates": TEMPLATES[industry]["report_templates"],
        "notes": "请在实际操作中补充真实数据源链接和访问凭证"
    }

    output_file = knowledge_dir / "industry_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ 知识库已生成: {output_file}")
    print(f"  行业: {industry}")
    print(f"  数据源: {len(data['data_sources'])} 个")
    print(f"  报告模板: {len(data['report_templates'])} 个")
    print(f"\n⚠️  请编辑该文件，补充真实数据源！")

if __name__ == "__main__":
    main()
