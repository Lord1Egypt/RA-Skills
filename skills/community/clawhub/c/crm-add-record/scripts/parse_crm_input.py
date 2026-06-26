#!/usr/bin/env python3
"""
CRM Input Parser
Extracts structured information from natural language CRM input.
"""

import re
import json
import sys
from typing import Dict, Optional

def parse_crm_input(user_input: str) -> Dict[str, str]:
    """
    Parse user input and extract CRM record information.

    Args:
        user_input: Natural language input string

    Returns:
        Dict with keys: phone, contact, region, basic_info
    """
    result = {
        'phone': '',
        'contact': '',
        'region': '',
        'basic_info': ''
    }

    # Remove common punctuation and normalize
    text = user_input.replace('，', ',').replace('。', '').replace('、', ',').strip()

    # Extract phone number (11 digits starting with 1)
    phone_match = re.search(r'1[3-9]\d{9}', text)
    if phone_match:
        result['phone'] = phone_match.group()
        text = text.replace(result['phone'], '').strip()

    # Extract contact name (Chinese characters 1-3 chars, optional title)
    contact_match = re.search(r'([\u4e00-\u9fa5]{1,3})(?:先生|女士|总|经理|主任)?', text)
    if contact_match:
        result['contact'] = contact_match.group()
        text = text.replace(result['contact'], '').strip()

    # Extract region (city/province 2-4 Chinese chars)
    region_keywords = ['省', '市', '区', '县', '地区', '区域']
    region_pattern = f"([\\u4e00-\\u9fa5]{{2,4}}(?:{'|'.join(region_keywords)})?)"
    region_match = re.search(region_pattern, text)
    if region_match:
        result['region'] = region_match.group()
        text = text.replace(result['region'], '').strip()

    # Remaining text goes to basic_info
    # Clean up remaining text
    basic_info = re.sub(r'[,\s，、]+', ' ', text).strip()
    result['basic_info'] = basic_info

    return result


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: parse_crm_input.py '<user_input>'"}))
        sys.exit(1)

    user_input = sys.argv[1]
    result = parse_crm_input(user_input)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
