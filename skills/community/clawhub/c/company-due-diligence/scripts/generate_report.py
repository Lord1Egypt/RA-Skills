#!/usr/bin/env python3
"""
生成尽职调查报告 - 详细版格式

使用方法:
    python scripts/generate_report.py "公司名称" --output report.md
    python scripts/generate_report.py "公司名称" --output report.pdf
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from markdown import markdown
import weasyprint

# 配置
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "scripts" / "data"
REPORT_DIR = Path("/Users/sunguangning/clawd/reports/due-diligence")
SCREENSHOT_DIR = Path("/Users/sunguangning/clawd/reports/due-diligence/screenshots")

def find_latest_data(company_name):
    """查找最新的查询数据文件"""
    safe_name = company_name.replace(" ", "_").replace("/", "_")
    if DATA_DIR.exists():
        files = sorted(DATA_DIR.glob(f"{safe_name}_*.json"), reverse=True)
        if files:
            return files[0]
    return None

def find_screenshot_folder(company_name):
    """查找公司的截图文件夹"""
    if not SCREENSHOT_DIR.exists():
        return None
    
    safe_name = company_name.replace(" ", "_").replace("/", "_")
    today = datetime.now().strftime('%Y%m%d')
    
    # 优先找今天的文件夹
    folder_name_today = f"{safe_name}_{today}"
    if (SCREENSHOT_DIR / folder_name_today).exists():
        return SCREENSHOT_DIR / folder_name_today
    
    # 找最新的文件夹
    folders = sorted(SCREENSHOT_DIR.glob(f"{safe_name}_*"), reverse=True)
    for folder in folders:
        if folder.is_dir():
            return folder
    
    return None

def copy_screenshots(source_folder, dest_folder):
    """复制截图到报告目录"""
    import shutil
    
    dest_folder = Path(dest_folder)
    screenshots_dest = dest_folder / "screenshots"
    screenshots_dest.mkdir(parents=True, exist_ok=True)
    
    copied = []
    for img in Path(source_folder).glob("*.png"):
        shutil.copy2(img, screenshots_dest)
        copied.append(img.name)
    
    if copied:
        print(f"  📸 已复制 {len(copied)} 张截图到: {screenshots_dest}")

def find_latest_data(company_name):
    """查找最新的查询数据文件"""
    safe_name = company_name.replace(" ", "_").replace("/", "_")
    if DATA_DIR.exists():
        files = sorted(DATA_DIR.glob(f"{safe_name}_*.json"), reverse=True)
        if files:
            return files[0]
    return None

def parse_qichacha(raw_data):
    """解析企查查数据"""
    data = {}
    text = raw_data.get("raw_data", "") if raw_data else ""
    
    # 提取关键信息
    patterns = {
        "注册资本": r"注册资本[：:]*(\d+[\d,\.]*)",
        "法定代表人": r"法定代表人[：:]*([^\s\n]+)",
        "成立日期": r"成立日期[：:]*(\d{4}-\d{2}-\d{2})",
        "统一社会信用代码": r"统一社会信用代码[：:]*([A-Z0-9]+)",
        "联系电话": r"电话[：:]*([^\s]+)",
        "官网": r"官网[：:]*([^\s]+)",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1).strip()
    
    # 经营状态
    if "存续" in text:
        data["经营状态"] = "存续"
    elif "注销" in text:
        data["经营状态"] = "注销"
    
    # 风险信息
    match = re.search(r"自身风险.*?(\d+)", text)
    if match:
        data["自身风险"] = match.group(1) + "条"
    
    match = re.search(r"关联风险.*?(\d+)", text)
    if match:
        data["关联风险"] = match.group(1) + "条"
    
    # 股东信息
    if "股东" in text:
        shareholders = []
        for line in text.split('\n'):
            if "股东" in line and len(line) < 50:
                shareholders.append(line.strip())
        if shareholders:
            data["股东列表"] = shareholders[:10]
    
    return data

def parse_eastmoney(raw_data):
    """解析东方财富数据"""
    data = {}
    text = raw_data.get("raw_data", "") if raw_data else ""
    
    patterns = {
        "总市值": r"总市值[：:]*(\d+[\d,\.]*)",
        "流通市值": r"流通市值[：:]*(\d+[\d,\.]*)",
        "总股本": r"总股本[：:]*(\d+[\d,\.]*)",
        "流通股": r"流通股[：:]*(\d+[\d,\.]*)",
        "每股净资产": r"每股净资产[：:]*(\d+[\d,\.]*)",
        "市盈率": r"市盈.*?(\d+[\d,\.]*)",
        "市净率": r"市净率[：:]*(\d+[\d,\.]*)",
        "净利润": r"净利润[：:]*([\d,\.]+)",
        "总营收": r"总营收[：:]*([\d,\.]+)",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1).strip()
    
    # 股权质押
    match = re.search(r"质押总比例(\d+[\d,\.]*)%", text)
    if match:
        data["股权质押比例"] = match.group(1) + "%"
    
    # 昨收价
    match = re.search(r"昨收[：:]*(\d+[\d,\.]*)", text)
    if match:
        data["昨收价"] = match.group(1) + "元"
    
    # 涨停跌停
    match = re.search(r"涨停[：:]*(\d+[\d,\.]*)", text)
    if match:
        data["涨停价"] = match.group(1) + "元"
    
    match = re.search(r"跌停[：:]*(\d+[\d,\.]*)", text)
    if match:
        data["跌停价"] = match.group(1) + "元"
    
    return data

def parse_wenshu(raw_data):
    """解析裁判文书网数据"""
    data = {}
    text = raw_data.get("raw_data", "") if raw_data else ""
    
    # 文书总数
    match = re.search(r"共检索到\s*(\d+)\s*篇", text)
    if match:
        data["文书总数"] = match.group(1) + "篇"
    
    # 年份分布
    years = {}
    for match in re.finditer(r"(\d{4})\((\d+)\)", text):
        years[match.group(1)] = match.group(2)
    if years:
        data["年份分布"] = years
    
    # 案由分布
    case_types = {}
    patterns = [
        (r"民间借贷\((\d+)\)", "民间借贷"),
        (r"贷款\((\d+)\)", "贷款"),
        (r"合同\((\d+)\)", "合同纠纷"),
    ]
    for pattern, name in patterns:
        match = re.search(pattern, text)
        if match:
            case_types[name] = match.group(1) + "件"
    if case_types:
        data["案由分布"] = case_types
    
    return data

def generate_report_content(company_name, qcc_data, em_data, wenshu_data, stock_code=None):
    """生成详细报告内容"""
    qcc = parse_qichacha(qcc_data) if qcc_data else {}
    em = parse_eastmoney(em_data) if em_data else {}
    wenshu = parse_wenshu(wenshu_data) if wenshu_data else {}
    
    # 风险评估
    risk_level = "低"
    risk_items = []
    
    if qcc.get("自身风险"):
        count = int(qcc.get("自身风险", "0").replace("条", ""))
        if count > 100:
            risk_level = "中"
            risk_items.append("自身风险较多")
    
    if wenshu.get("文书总数"):
        count = int(wenshu.get("文书总数", "0").replace("篇", ""))
        if count > 50:
            risk_level = "中"
            risk_items.append("诉讼案件较多")
    
    if em.get("股权质押比例"):
        try:
            ratio = float(em.get("股权质押比例", "0").replace("%", ""))
            if ratio > 20:
                risk_level = "高"
                risk_items.append("股权质押比例较高")
        except:
            pass
    
    report = f"""# {company_name}尽职调查报告

**报告日期**：{datetime.now().strftime('%Y年%m月%d日')}  
**调查对象**：{company_name}  
{f'**股票代码**：{stock_code}' if stock_code else ''}
**报告类型**：尽职调查报告

---

## 一、公司基本信息

### 1.1 工商登记信息

| 项目 | 内容 |
|------|------|
| **公司全称** | {company_name} |
| **统一社会信用代码** | {qcc.get('统一社会信用代码', '-')} |
| **法定代表人** | {qcc.get('法定代表人', '-')} |
| **注册资本** | {qcc.get('注册资本', '-')} |
| **成立日期** | {qcc.get('成立日期', '-')} |
| **经营状态** | {qcc.get('经营状态', '-')} |
| **联系电话** | {qcc.get('联系电话', '-')} |
| **官方网站** | {qcc.get('官网', '-')} |

### 1.2 公司简介

{company_name}是一家依法设立的企业。"""

    # 股权结构
    if qcc.get("股东列表"):
        report += f"""

### 1.3 股权结构

| 股东名称 | 备注 |
|----------|------|
"""
        for shareholder in qcc["股东列表"][:10]:
            report += f"| {shareholder} | - |\n"

    # 财务数据
    report += f"""

---

## 二、财务数据

### 2.1 股票行情数据

| 指标 | 数值 |
|------|------|
| **昨收价** | {em.get('昨收价', '-')} |
| **涨停价** | {em.get('涨停价', '-')} |
| **跌停价** | {em.get('跌停价', '-')} |
"""

    if em.get("总市值"):
        report += f"""

### 2.2 市值数据

| 指标 | 数值 |
|------|------|
| **总市值** | {em.get('总市值', '-')}亿元 |
| **流通市值** | {em.get('流通市值', '-')}亿元 |
| **总股本** | {em.get('总股本', '-')}亿股 |
| **流通股** | {em.get('流通股', '-')}亿股 |
| **每股净资产** | {em.get('每股净资产', '-')}元 |
"""

    if em.get("市盈率"):
        report += f"""

### 2.3 财务指标

| 指标 | 数值 |
|------|------|
| **市盈率（动）** | {em.get('市盈率', '-')} |
| **市净率** | {em.get('市净率', '-')} |
| **总营收** | {em.get('总营收', '-')}亿元 |
| **净利润** | {em.get('净利润', '-')}万元 |
"""

    if em.get("股权质押比例"):
        report += f"""

### 2.4 股权质押情况

| 项目 | 数据 |
|------|------|
| **质押比例** | {em.get('股权质押比例', '-')} |

"""

    # 诉讼数据
    report += f"""

---

## 三、诉讼与法律纠纷

### 3.1 裁判文书网查询结果

| 项目 | 数据 |
|------|------|
| **文书总数** | {wenshu.get('文书总数', '-')} |
"""

    if wenshu.get("年份分布"):
        report += f"""
### 3.2 年份分布

"""
        for year, count in sorted(wenshu["年份分布"].items(), reverse=True):
            report += f"- {year}年: {count}件\n"

    if wenshu.get("案由分布"):
        report += f"""
### 3.3 主要案由

"""
        for case_type, count in wenshu["案由分布"].items():
            report += f"- {case_type}: {count}\n"

    # 风险评估
    report += f"""

---

## 四、风险评估

### 4.1 风险等级

| 风险类型 | 数量 |
|----------|------|
| **自身风险** | {qcc.get('自身风险', '-')} |
| **关联风险** | {qcc.get('关联风险', '-')} |
| **诉讼案件** | {wenshu.get('文书总数', '-')} |

**综合风险等级**: {risk_level}风险

"""

    if risk_items:
        report += f"**风险点**: {('、'.join(risk_items))}\n"

    # 综合评估
    report += f"""

---

## 五、综合评估

### 5.1 优势

1. ✅ 上市公司，信息公开透明
2. ✅ 注册资本具有一定规模
3. ✅ 有一定的市场影响力

### 5.2 风险点

"""
    for item in risk_items:
        report += f"1. ⚠️ {item}\n"

    if not risk_items:
        report += "暂无明显风险点\n"

    report += f"""

---

## 数据来源

1. 企查查 (qcc.com) - 工商信息
2. 东方财富 (eastmoney.com) - 股票行情、财务数据
3. 中国裁判文书网 (wenshu.court.gov.cn) - 诉讼记录

---

**报告生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}  
**数据获取工具**: agent-browser (Playwright CLI)

---

*本报告仅供参考，不构成投资建议*
"""
    return report

def convert_to_pdf(md_file):
    """将Markdown转换为PDF"""
    if not md_file or not md_file.exists():
        return None
    
    pdf_file = md_file.with_suffix('.pdf')
    
    try:
        md_content = md_file.read_text(encoding="utf-8")
        html_content = markdown(md_content, extensions=['tables'])
        
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'SimSun', sans-serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 25px; }}
        h3 {{ color: #666; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        weasyprint.HTML(string=full_html).write_pdf(pdf_file)
        return str(pdf_file)
    except Exception as e:
        print(f"  ⚠️ PDF生成失败: {e}")
        return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="生成尽职调查报告")
    parser.add_argument("company", help="公司名称")
    parser.add_argument("--data", "-d", help="指定数据文件")
    parser.add_argument("--code", help="股票代码(可选)")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--no-pdf", action="store_true", help="不生成PDF")
    args = parser.parse_args()
    
    company_name = args.company
    output_path = Path(args.output)
    
    # 加载数据
    data_file = None
    if args.data:
        data_file = Path(args.data)
    else:
        data_file = find_latest_data(company_name)
    
    if not data_file or not data_file.exists():
        print(f"错误: 未找到数据文件")
        sys.exit(1)
    
    print(f"从数据文件生成报告: {data_file}")
    
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    sources = data.get("sources", {})
    qcc_data = sources.get("qichacha", {})
    em_data = sources.get("eastmoney", {})
    wenshu_data = sources.get("wenshu", {})
    
    # 查找截图文件夹
    screenshot_folder = find_screenshot_folder(company_name)
    if screenshot_folder:
        print(f"📸 找到截图文件夹: {screenshot_folder}")
    
    # 生成报告
    print(f"生成报告: {company_name}")
    report_content = generate_report_content(company_name, qcc_data, em_data, wenshu_data, args.code)
    
    # 保存Markdown
    if output_path.suffix == ".pdf":
        md_file = output_path.with_suffix('.md')
    else:
        md_file = output_path
    md_file.parent.mkdir(parents=True, exist_ok=True)
    md_file.write_text(report_content, encoding="utf-8")
    print(f"  📝 Markdown报告: {md_file}")
    
    # 复制截图到报告目录
    if screenshot_folder:
        copy_screenshots(screenshot_folder, md_file.parent)
    
    # 生成PDF
    if str(output_path).endswith('.pdf') or not args.no_pdf:
        pdf_file = convert_to_pdf(md_file)
        if pdf_file:
            # 也复制截图到PDF同目录
            if screenshot_folder:
                copy_screenshots(screenshot_folder, Path(pdf_file).parent)
            print(f"✅ 报告生成完成: {pdf_file}")
            return
    
    print(f"✅ 报告生成完成: {md_file}")

if __name__ == "__main__":
    main()
