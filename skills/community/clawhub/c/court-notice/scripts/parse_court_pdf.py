#!/usr/bin/env python3
"""
法院文书PDF解析脚本
从PDF中提取关键信息：案号、案由、被传唤人、开庭时间、地点
"""

import sys
import re
import json
from pypdf import PdfReader

def parse_court_pdf(pdf_path):
    """解析法院文书PDF，提取关键信息"""
    
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    # 提取案号
    case_no_match = re.search(r'（(\d{4})[^）]*\d+号', text)
    case_no = case_no_match.group(0).strip() if case_no_match else ""
    
    # 提取案由（案由：后面内容）
    case_type_match = re.search(r'案　?由[：:]\s*(.+)', text)
    case_type = case_type_match.group(1).strip() if case_type_match else ""
    
    # 提取被传唤人
    person_match = re.search(r'被传唤人[：:]\s*([^\n（ footprints]+)', text)
    person = person_match.group(1).strip() if person_match else ""
    
    # 提取开庭时间
    time_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日[^0-9\n]{0,10}\d{1,2}[：:]\d{2})', text)
    hearing_time = time_match.group(1).strip() if time_match else ""
    
    # 提取开庭地点
    location_match = re.search(r'开庭地点[：:]\s*(.+)', text)
    location = location_match.group(1).strip() if location_match else ""
    
    # 判断文书类型
    is_summons = bool(re.search(r'开\s*庭|传\s*唤|出\s*庭\s*通\s*知', text))
    is_dismissal = bool(re.search(r'撤诉|裁定准予', text))
    
    if is_dismissal:
        doc_type = "撤诉裁定"
    elif is_summons:
        doc_type = "传票"
    else:
        doc_type = "其他"
    
    return {
        "case_no": case_no,
        "case_type": case_type,
        "person": person,
        "hearing_time": hearing_time,
        "location": location,
        "doc_type": doc_type,
        "full_text": text
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 parse_court_pdf.py <pdf路径>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    result = parse_court_pdf(pdf_path)
    
    print("=== 解析结果 ===")
    print(f"文书类型: {result['doc_type']}")
    print(f"案号: {result['case_no']}")
    print(f"案由: {result['case_type']}")
    print(f"被传唤人: {result['person']}")
    print(f"开庭时间: {result['hearing_time']}")
    print(f"开庭地点: {result['location']}")
    print()
    print("=== 全文 ===")
    print(result['full_text'])

if __name__ == "__main__":
    main()
