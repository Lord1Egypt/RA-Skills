#!/usr/bin/env python3
"""
功能：从PMC论文中提取结构化数据，强制校验
- 如果提取失败，明确报错
- 如果数据不全，标注"未提及"而非模糊填充
"""

import sys
import json
import re
import requests

def extract_from_pmc(pmcid):
    """从PMC获取论文并提取数据"""
    
    # 获取PMC全文
    url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/?format=flat"
    
    try:
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            return {"error": f"获取失败 HTTP {r.status_code}"}
        
        text = r.text[:20000]  # 获取前20000字符
        
        # 提取标题
        title_match = re.search(r'<article-title[^>]*>([^<]+)</article-title>', text)
        title = title_match.group(1).strip() if title_match else "N/A"
        
        # 提取摘要
        abstract_match = re.search(r'<abstract[^>]*>([^<]+)</abstract>', text, re.DOTALL)
        abstract = abstract_match.group(1).strip() if abstract_match else ""
        
        # 尝试从摘要提取数据
        result = {
            "title": title,
            "abstract": abstract[:500] if abstract else "N/A",
            "sample_size": None,
            "main_result": None,
            "cost_impact": None,
            "confidence_interval": None,
            "p_value": None,
            "quote": None
        }
        
        # 提取样本量 - 搜索数字+人/患者/cases
        sample_patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*(?:patients|subjects|participants|cases)',
            r'n\s*=\s*(\d{1,3}(?:,\d{3})*)',
            r'(\d{1,3}(?:,\d{3})*)\s*(?:hospital|ICU|cohort)',
        ]
        for pattern in sample_patterns:
            match = re.search(pattern, abstract, re.IGNORECASE)
            if match:
                result["sample_size"] = match.group(1)
                break
        
        # 提取主要结果 - 百分比
        percent_patterns = [
            r'(\d+\.?\d*)%\s*(?:reduction|decrease|increase|savings|accuracy|sensitivity|specificity|AUC)',
            r'AUC\s*[=:]\s*(\d+\.?\d*)',
            r'(?:sensitivity|specificity|accuracy)\s*[=:]\s*(\d+\.?\d*)%',
        ]
        for pattern in percent_patterns:
            match = re.search(pattern, abstract, re.IGNORECASE)
            if match:
                result["main_result"] = match.group(1) + '%'
                break
        
        # 提取成本
        cost_patterns = [
            r'\$(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:savings|per\s*patient|per\s*visit)',
            r'(\d+\.?\d*)\s*%?\s*(?:cost|saving|reduction)',
        ]
        for pattern in cost_patterns:
            match = re.search(pattern, abstract, re.IGNORECASE)
            if match:
                result["cost_impact"] = match.group(1)
                break
        
        # 提取p值
        p_match = re.search(r'p\s*[=<]\s*(\d+\.?\d*)', abstract, re.IGNORECASE)
        if p_match:
            result["p_value"] = f"p{'<' if '=' not in abstract[p_match.start():p_match.end()] else '='}{p_match.group(1)}"
        
        # 提取置信区间
        ci_match = re.search(r'95%\s*CI\s*[\[\(]([^)\]]+)[\]\)]', abstract, re.IGNORECASE)
        if ci_match:
            result["confidence_interval"] = f"95% CI [{ci_match.group(1)}]"
        
        # 提取原文引用（从摘要前200字）
        if abstract and len(abstract) > 50:
            result["quote"] = abstract[:200]
        
        # 强制校验
        issues = []
        if not result.get("sample_size") or result["sample_size"] in ["N/A", None]:
            issues.append("样本量未提取")
        if not result.get("main_result") or result["main_result"] in ["N/A", None]:
            issues.append("主要结果未提取")
        if not result.get("quote") or result["quote"] in ["N/A", None, ""]:
            issues.append("原文引用缺失")
        
        if issues:
            result["issues"] = issues
            result["extraction_status"] = "incomplete"
        else:
            result["extraction_status"] = "complete"
        
        return result
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 extract-pmc.py <pmcid>")
        sys.exit(1)
    
    pmcid = sys.argv[1]
    result = extract_from_pmc(pmcid)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 如果有error或issues，退出码非0
    if "error" in result or (result.get("issues") and len(result["issues"]) >= 2):
        sys.exit(1)
