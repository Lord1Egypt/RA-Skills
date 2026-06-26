#!/usr/bin/env python3
"""
四网站整合查询脚本 v3.0
功能：
1. 企查查/天眼查搜索 + 截图
2. 公司详情页抓取 + 截图
3. 生成 Markdown + PDF 报告

使用方法：
    python3 query_all_v2.py "中国银联股份有限公司"
"""

import json
import os
import sys
import time
import subprocess
import re
from datetime import datetime
from pathlib import Path

# ========== 配置 ==========
SKILL_DIR = Path(__file__).parent
SESSION_DIR = SKILL_DIR / "session"
SCREENSHOT_DIR = Path("/Users/sunguangning/clawd/reports/due-diligence/screenshots")
REPORT_DIR = Path("/Users/sunguangning/clawd/reports/due-diligence")
DEFAULT_SESSION = "due-diligence"

# 确保目录存在
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ========== 工具函数 ==========

def run_agent_browser(cmd, timeout=60):
    """执行 agent-browser 命令"""
    full_cmd = f"agent-browser --session-name {DEFAULT_SESSION} {cmd}"
    try:
        result = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def get_company_folder(company_name):
    """获取公司专属文件夹路径"""
    safe_name = re.sub(r'[^\w\u4e00-\u9fff-]', '_', company_name)
    folder_name = f"{safe_name}_{datetime.now().strftime('%Y%m%d')}"
    company_folder = SCREENSHOT_DIR / folder_name
    company_folder.mkdir(parents=True, exist_ok=True)
    return company_folder

def save_screenshot(page_name, company_folder):
    """截取当前页面截图"""
    screenshot_path = company_folder / f"{page_name}.png"
    result = run_agent_browser(f"screenshot {screenshot_path}")
    if "✓" in result or screenshot_path.exists():
        print(f"    📸 截图: {page_name}.png")
        return str(screenshot_path)
    else:
        print(f"    ⚠️ 截图失败: {page_name}")
        return None

def wait_for_page(seconds=3):
    """等待页面加载"""
    time.sleep(seconds)

# ========== 数据抓取函数 ==========

def query_qcc(company_name, company_folder):
    """查询企查查"""
    print("\n🔍 正在查询企查查...")
    
    data = {"source": "企查查", "query_time": datetime.now().isoformat()}
    
    try:
        # 1. 打开搜索页
        search_url = f"https://www.qcc.com/search?key={company_name}"
        run_agent_browser(f'open "{search_url}"')
        wait_for_page(5)
        
        # 2. 截图搜索结果
        save_screenshot("01_qcc_search", company_folder)
        
        # 3. 获取搜索结果列表文本
        text = run_agent_browser('eval "document.body.innerText.substring(0, 10000)"')
        data["search_result"] = text[:8000] if text and len(text) > 100 else text
        
        # 4. 查找并点击公司详情链接
        detail_url = run_agent_browser(
            'eval "document.querySelector(\'.company-name a\')?.href || '
            'document.querySelector(\'.name a\')?.href || '
            'Array.from(document.querySelectorAll(\'a\')).find(a => '
            'a.innerText.includes(\'' + company_name + '\') && a.href.includes(\'firm\'))?.href || \'\'"'
        )
        
        if detail_url and "qcc.com/firm/" in detail_url:
            # 5. 打开公司详情页
            run_agent_browser(f'open "{detail_url}"')
            wait_for_page(5)
            
            # 6. 截图详情页
            save_screenshot("02_qcc_company_detail", company_folder)
            
            # 7. 获取详情页内容
            detail_text = run_agent_browser('eval "document.body.innerText.substring(0, 20000)"')
            data["detail"] = detail_text[:18000] if detail_text and len(detail_text) > 100 else detail_text
            
            # 8. 获取截图路径
            data["screenshots"] = {
                "search": "01_qcc_search.png",
                "detail": "02_qcc_company_detail.png"
            }
        
        print("    ✅ 企查查查询完成")
        
    except Exception as e:
        print(f"    ❌ 企查查查询失败: {e}")
        data["error"] = str(e)
    
    return data

def query_tyc(company_name, company_folder):
    """查询天眼查"""
    print("\n🔍 正在查询天眼查...")
    
    data = {"source": "天眼查", "query_time": datetime.now().isoformat()}
    
    try:
        # 1. 打开搜索页
        search_url = f"https://www.tianyancha.com/search?key={company_name}"
        run_agent_browser(f'open "{search_url}"')
        wait_for_page(5)
        
        # 2. 截图搜索结果
        save_screenshot("03_tyc_search", company_folder)
        
        # 3. 获取搜索结果文本
        text = run_agent_browser('eval "document.body.innerText.substring(0, 10000)"')
        data["search_result"] = text[:8000] if text and len(text) > 100 else text
        
        # 4. 查找公司详情链接
        detail_url = run_agent_browser(
            'eval "Array.from(document.querySelectorAll(\'a\')).find(a => '
            'a.innerText.includes(\'' + company_name + '\') && a.href.includes(\'company\'))?.href || \'\'"'
        )
        
        if detail_url and ("tianyancha.com/company/" in detail_url or "tianyancha.com/firm/" in detail_url):
            # 5. 打开公司详情页
            run_agent_browser(f'open "{detail_url}"')
            wait_for_page(5)
            
            # 6. 截图详情页
            save_screenshot("04_tyc_company_detail", company_folder)
            
            # 7. 获取详情页内容
            detail_text = run_agent_browser('eval "document.body.innerText.substring(0, 15000)"')
            data["detail"] = detail_text[:13000] if detail_text and len(detail_text) > 100 else detail_text
            
            data["screenshots"] = {
                "search": "03_tyc_search.png",
                "detail": "04_tyc_company_detail.png"
            }
        
        print("    ✅ 天眼查查询完成")
        
    except Exception as e:
        print(f"    ❌ 天眼查查询失败: {e}")
        data["error"] = str(e)
    
    return data

def query_eastmoney(company_name, stock_code, company_folder):
    """查询东方财富"""
    print("\n🔍 正在查询东方财富...")
    
    data = {"source": "东方财富", "query_time": datetime.now().isoformat()}
    
    try:
        if stock_code:
            url = f"https://quote.eastmoney.com/{stock_code}.html"
        else:
            url = f"https://so.eastmoney.com/Search?searchkey={company_name}"
        
        run_agent_browser(f'open "{url}"')
        wait_for_page(5)
        
        # 截图
        save_screenshot("05_eastmoney", company_folder)
        
        # 获取内容
        text = run_agent_browser('eval "document.body.innerText.substring(0, 8000)"')
        data["content"] = text[:7000] if text and len(text) > 100 else text
        
        print("    ✅ 东方财富查询完成")
        
    except Exception as e:
        print(f"    ⚠️ 东方财富查询跳过: {e}")
        data["skip"] = True
    
    return data

def query_wenshu(company_name, company_folder):
    """查询裁判文书网"""
    print("\n🔍 正在查询裁判文书网...")
    
    data = {"source": "中国裁判文书网", "query_time": datetime.now().isoformat()}
    
    try:
        run_agent_browser('open "http://wenshu.court.gov.cn/"')
        wait_for_page(3)
        save_screenshot("06_wenshu_home", company_folder)
        
        # 尝试搜索
        run_agent_browser(f'fill @e15 "{company_name}"')
        run_agent_browser("press Enter")
        wait_for_page(5)
        save_screenshot("07_wenshu_result", company_folder)
        
        text = run_agent_browser('eval "document.body.innerText.substring(0, 5000)"')
        data["content"] = text[:5000] if text and len(text) > 100 else text
        
        print("    ✅ 裁判文书网查询完成")
        
    except Exception as e:
        print(f"    ⚠️ 裁判文书网查询跳过: {e}")
        data["skip"] = True
    
    return data

# ========== 报告生成函数 ==========

def generate_markdown_report(company_name, data, output_path):
    """生成 Markdown 格式的尽调报告"""
    
    report = f"""# {company_name} 尽职调查报告

**报告日期**：{datetime.now().strftime('%Y年%m月%d日')}  
**查询渠道**：企查查、天眼查  
**报告编号**：DD-{datetime.now().strftime('%Y%m%d')}-001

---

## 一、公司基本信息

"""
    
    # 解析企查查数据
    qcc_data = data.get("sources", {}).get("qichacha", {})
    qcc_detail = qcc_data.get("detail", "")
    
    # 提取基本信息
    report += self_parse_qcc_basic(qcc_detail, qcc_data)
    
    # 添加截图说明
    report += f"""
---

## 二、截图证据

| 序号 | 来源 | 说明 | 文件 |
|------|------|------|------|
| 1 | 企查查 | 搜索结果页 | 01_qcc_search.png |
| 2 | 企查查 | 公司详情页 | 02_qcc_company_detail.png |
| 3 | 天眼查 | 搜索结果页 | 03_tyc_search.png |
| 4 | 天眼查 | 公司详情页 | 04_tyc_company_detail.png |
"""
    
    # 天眼查数据
    tyc_data = data.get("sources", {}).get("tianyancha", {})
    if tyc_data.get("search_result"):
        report += f"""

---

## 三、天眼查数据摘要

```
{tyc_data.get("search_result", "")[:3000]}
```

"""
    
    report += f"""
---

## 四、数据来源

- **企查查** (qcc.com) - 工商信息查询
- **天眼查** (tianyancha.com) - 企业信息查询

**查询时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

*本报告由企业尽调自动化工具生成*  
*数据仅供参考，以官方披露为准*
"""
    
    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"    📝 Markdown报告已生成: {output_path.name}")
    return output_path

def self_parse_qcc_basic(text, raw_data):
    """从企查查文本中提取基本信息"""
    lines = []
    
    # 公司名称
    if "中国银联" in text or "公司名称" in text:
        name_match = re.search(r'([^\s公司]+股份有限公司|[^\s公司]+有限公司)', text)
        if name_match:
            lines.append(f"- **公司名称**：{name_match.group(1)}")
    
    # 统一社会信用代码
    credit_code = re.search(r'统一社会信用代码[：:]\s*([A-Z0-9]+)', text)
    if credit_code:
        lines.append(f"- **统一社会信用代码**：{credit_code.group(1)}")
    
    # 法定代表人
    legal_person = re.search(r'法定代表人[：:]\s*([^\s]+)', text)
    if legal_person:
        lines.append(f"- **法定代表人**：{legal_person.group(1)}")
    
    # 注册资本
    capital = re.search(r'注册资本[：:]\s*([\d.]+[万千百]?元?)', text)
    if capital:
        lines.append(f"- **注册资本**：{capital.group(1)}")
    
    # 成立日期
    date = re.search(r'成立日期[：:]\s*([\d-]+)', text)
    if date:
        lines.append(f"- **成立日期**：{date.group(1)}")
    
    # 登记状态
    status = re.search(r'(存续|吊销|注销|撤销|在业)', text)
    if status:
        lines.append(f"- **登记状态**：{status.group(1)}")
    
    # 企业类型
    biz_type = re.search(r'企业类型[：:]\s*([^\n]+)', text)
    if biz_type:
        lines.append(f"- **企业类型**：{biz_type.group(1).strip()}")
    
    # 联系电话
    phone = re.search(r'(?:电话|手机)[：:]\s*([^\s\n]+)', text)
    if phone:
        lines.append(f"- **联系电话**：{phone.group(1)}")
    
    # 地址
    address = re.search(r'(?:地址|注册地址)[：:]\s*([^\n]{10,100})', text)
    if address:
        lines.append(f"- **地址**：{address.group(1).strip()}")
    
    # 员工人数
    employees = re.search(r'(?:员工人数|人员规模)[：:]\s*([^\s\n]+)', text)
    if employees:
        lines.append(f"- **员工人数**：{employees.group(1)}")
    
    if lines:
        return "\n".join(["| 项目 | 内容 |", "|------|------|"] + 
                         [f"| {l.split('：')[0].replace('- **', '')} | {l.split('：')[1].replace('**', '')} |" 
                          for l in lines[:15]])
    
    return "_（企查查详情页数据解析中...）_"

def generate_pdf(md_file, company_name):
    """将 Markdown 转换为专业 PDF """
    if not md_file or not md_file.exists():
        print(f"    ⚠️ Markdown文件不存在，跳过PDF生成")
        return None
    
    pdf_file = md_file.with_suffix('.pdf')
    
    # 读取 HTML 模板
    template_file = SKILL_DIR / "assets" / "report_template.html"
    if not template_file.exists():
        print(f"    ⚠️ HTML模板不存在，跳过PDF生成")
        return None
    
    try:
        with open(template_file, "r", encoding="utf-8") as f:
            template = f.read()
        
        # 使用 pandoc 将 Markdown 转为 HTML
        html_file = md_file.with_suffix('.html')
        
        # 转为基础 HTML
        result = subprocess.run(
            f'pandoc "{md_file}" -o "{html_file}" --standalone --metadata title="{company_name}"',
            shell=True, capture_output=True, text=True, timeout=30
        )
        
        if not html_file.exists():
            print(f"    ⚠️ HTML转换失败")
            return None
        
        # 读取转换后的 HTML
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 提取 body 内容并放入模板
        import re
        body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
        if body_match:
            body_content = body_match.group(1)
        else:
            body_content = html_content
        
        # 组合最终 HTML
        final_html = template.replace('$body$', body_content).replace('$title$', f"{company_name} - 尽职调查报告")
        
        # 保存最终 HTML
        final_html_file = md_file.with_suffix('.styled.html')
        with open(final_html_file, "w", encoding="utf-8") as f:
            f.write(final_html)
        
        # 使用 Chrome 打印为 PDF
        chrome_cmd = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_cmd):
            result = subprocess.run([
                chrome_cmd,
                "--headless",
                "--disable-gpu",
                "--print-to-pdf=" + str(pdf_file),
                "--print-to-pdf-no-header",
                "--margins=10",
                f"file://{final_html_file}"
            ], capture_output=True, timeout=60)
            
            if pdf_file.exists():
                # 清理临时文件
                if html_file.exists():
                    html_file.unlink()
                if final_html_file.exists():
                    final_html_file.unlink()
                
                print(f"    📄 PDF报告已生成: {pdf_file.name}")
                return str(pdf_file)
        
    except Exception as e:
        print(f"    ⚠️ PDF生成失败: {e}")
    
    return None

# ========== 主函数 ==========

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 query_all_v2.py \"公司名称\"")
        print("  python3 query_all_v2.py \"公司名称\" --code=sh600816")
        print("  python3 query_all_v2.py \"公司名称\" --skip-pdf")
        sys.exit(1)
    
    company_name = sys.argv[1]
    stock_code = None
    skip_pdf = False
    
    for arg in sys.argv[2:]:
        if arg.startswith("--code="):
            stock_code = arg.replace("--code=", "")
        if arg == "--skip-pdf":
            skip_pdf = True
    
    print(f"\n{'='*50}")
    print(f"🔍 开始尽职调查: {company_name}")
    print(f"{'='*50}")
    
    # 创建公司专属文件夹
    company_folder = get_company_folder(company_name)
    print(f"\n📂 截图保存目录: {company_folder}")
    
    # 检查登录状态
    session_file = SESSION_DIR / f"{DEFAULT_SESSION}.json"
    if not session_file.exists():
        session_file = SESSION_DIR / "due-diligence.json"
    
    if not session_file.exists():
        print(f"\n⚠️ 警告: 未找到登录状态文件")
        print("   请确保已登录企查查和天眼查")
        print("   可以手动登录后运行: agent-browser --session-name due-diligence state save <path>")
    else:
        # 加载登录状态
        result = run_agent_browser(f"state load {session_file}")
        if "✓" in result or "set" in result:
            print("✅ 已加载登录状态")
        else:
            print("⚠️ 登录状态加载可能失败，继续执行...")
    
    # 查询各数据源
    results = {
        "company_name": company_name,
        "query_time": datetime.now().isoformat(),
        "screenshot_folder": str(company_folder),
        "sources": {}
    }
    
    # 企查查查询
    results["sources"]["qichacha"] = query_qcc(company_name, company_folder)
    
    # 天眼查查询
    results["sources"]["tianyancha"] = query_tyc(company_name, company_folder)
    
    # 东方财富查询（可选）
    if stock_code:
        results["sources"]["eastmoney"] = query_eastmoney(company_name, stock_code, company_folder)
    
    # 裁判文书网查询（可选）
    results["sources"]["wenshu"] = query_wenshu(company_name, company_folder)
    
    # 保存原始数据
    data_dir = SKILL_DIR / "data"
    data_dir.mkdir(exist_ok=True)
    safe_name = re.sub(r'[^\w\u4e00-\u9fff-]', '_', company_name)
    data_file = data_dir / f"{safe_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n📁 原始数据已保存: {data_file.name}")
    
    # 生成 Markdown 报告
    print(f"\n📝 正在生成Markdown报告...")
    md_file = REPORT_DIR / f"{safe_name}_尽调报告_{datetime.now().strftime('%Y%m%d')}.md"
    generate_markdown_report(company_name, results, md_file)
    
    # 生成 PDF 报告
    pdf_file = None
    if not skip_pdf:
        print(f"\n📄 正在生成PDF报告...")
        pdf_file = generate_pdf(md_file)
    
    # 完成
    print(f"\n{'='*50}")
    print(f"✅ 尽职调查完成!")
    print(f"{'='*50}")
    print(f"📁 截图目录: {company_folder}")
    print(f"📝 Markdown报告: {md_file}")
    if pdf_file:
        print(f"📄 PDF报告: {pdf_file}")
    print(f"📊 原始数据: {data_file}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
