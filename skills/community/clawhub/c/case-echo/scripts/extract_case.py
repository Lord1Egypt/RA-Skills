#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re


def extract_case(text: str) -> dict:
    result = {
        "sex": None,
        "age": None,
        "diagnosis": None,
        "stage": None,
        "egfr": None,
        "pd_l1": None,
        "brain_metastasis": None,
        "raw_text": text.strip()
    }

    # 性别
    if "男" in text:
        result["sex"] = "男"
    elif "女" in text:
        result["sex"] = "女"

    # 年龄
    age_match = re.search(r'(\d{1,3})\s*岁', text)
    if age_match:
        result["age"] = int(age_match.group(1))

    # 分期
    stage_match = re.search(r'([IVX]+期|[ⅠⅡⅢⅣ]+期)', text, re.IGNORECASE)
    if stage_match:
        result["stage"] = stage_match.group(1)

    # PD-L1
    pdl1_match = re.search(r'PD-?L1\s*([0-9]+%)', text, re.IGNORECASE)
    if pdl1_match:
        result["pd_l1"] = pdl1_match.group(1)

    # EGFR
    egfr_match = re.search(r'(EGFR[^，。,；;\n]*)', text, re.IGNORECASE)
    if egfr_match:
        result["egfr"] = egfr_match.group(1).strip()

    # 脑转移
    if re.search(r'无脑转移', text):
        result["brain_metastasis"] = "无"
    elif re.search(r'脑转移', text):
        result["brain_metastasis"] = "有"

    # 诊断：简单演示版
    diagnosis_patterns = [
        r'(右肺腺癌)',
        r'(左肺腺癌)',
        r'(肺腺癌)',
        r'(肺鳞癌)',
        r'(非小细胞肺癌)',
        r'(小细胞肺癌)'
    ]
    for pattern in diagnosis_patterns:
        m = re.search(pattern, text)
        if m:
            result["diagnosis"] = m.group(1)
            break

    return result


def main():
    parser = argparse.ArgumentParser(description="Extract simple structured fields from a Chinese case description.")
    parser.add_argument("--text", required=True, help="Case description text")
    args = parser.parse_args()

    data = extract_case(args.text)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
