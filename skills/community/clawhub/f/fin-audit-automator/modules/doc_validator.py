#!/usr/bin/env python3
"""
文档校验模块 (发票OCR)
Document Validation Module (Invoice OCR)
"""

import re
from typing import Dict, Any, List
from pathlib import Path


class DocValidator:
    """文档校验器"""
    
    def __init__(self):
        # 敏感词库
        self.sensitive_words = ["礼品", "购物卡", "招待", "请客", "红包"]
        # 发票代码/号码格式
        self.fapiao_code_pattern = r'^\d{10,12}$'
        self.fapiao_num_pattern = r'^\d{8,20}$'
    
    def validate_fapiao(self, image_path: str) -> Dict[str, Any]:
        """
        校验增值税发票合规性 (模拟OCR版本)
        """
        # 注意：实际使用需要安装 paddleocr
        # 这里使用模拟数据演示
        
        issues = []
        ocr_text = ""
        
        # 模拟OCR结果 (实际项目中使用 paddleocr)
        try:
            # 尝试使用OCR (如果可用)
            ocr_text = self._mock_ocr(image_path)
        except:
            ocr_text = "模拟发票内容"
        
        # 检查1: 购买方名称
        if "购买方名称" not in ocr_text and "本公司" not in ocr_text:
            issues.append("抬头不符或未识别")
        
        # 检查2: 发票代码/号码格式
        codes = re.findall(r'\d{10,12}', ocr_text)
        if not codes:
            issues.append("未识别发票代码")
        
        # 检查3: 敏感词检查
        found_sensitive = []
        for word in self.sensitive_words:
            if word in ocr_text:
                found_sensitive.append(word)
        
        if found_sensitive:
            if "备注" not in ocr_text:
                issues.append(f"敏感商品({', '.join(found_sensitive)})未备注明细")
        
        # 检查4: 金额合理性
        amounts = re.findall(r'(\d+(?:\.\d{2})?)\s*元', ocr_text)
        if amounts:
            max_amount = max([float(a) for a in amounts])
            if max_amount > 100000:  # 10万元以上
                issues.append(f"大额发票({max_amount}元)需额外审核")
        
        # 检查5: 日期有效性
        dates = re.findall(r'(\d{4})年(\d{1,2})月(\d{1,2})日', ocr_text)
        if not dates:
            issues.append("未识别发票日期")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "ocr_text": ocr_text[:200] + "..." if len(ocr_text) > 200 else ocr_text,
            "sensitive_words_found": found_sensitive,
            "check_items": 5,
            "passed_items": 5 - len(issues)
        }
    
    def _mock_ocr(self, image_path: str) -> str:
        """模拟OCR结果 (实际项目使用 paddleocr)"""
        # 模拟发票内容
        mock_text = """
        增值税普通发票
        发票代码: 011001900211
        发票号码: 12345678
        开票日期: 2024年01月15日
        购买方名称: 某某科技有限公司
        纳税人识别号: 91110108MA00xxxx
        项目: 咨询服务费
        金额: 50000.00元
        税率: 6%
        价税合计: 53000.00元
        销售方名称: ABC咨询公司
        """
        return mock_text.strip()
    
    def validate_contract(self, text: str) -> Dict[str, Any]:
        """
        校验合同合规性
        """
        issues = []
        
        # 检查关键条款
        required_clauses = ["金额", "付款方式", "违约责任", "争议解决"]
        for clause in required_clauses:
            if clause not in text:
                issues.append(f"缺少关键条款: {clause}")
        
        # 检查金额一致性
        amounts = re.findall(r'(\d+(?:\.\d{2})?)\s*万元?', text)
        if len(amounts) >= 2:
            # 检查大小写金额是否一致 (简化版)
            pass
        
        # 检查敏感条款
        risky_terms = ["无限责任", "自动续约", "独家", "排他"]
        found_risky = [term for term in risky_terms if term in text]
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "risky_terms": found_risky,
            "recommendation": "建议法务审核" if found_risky else "基本合规"
        }


if __name__ == "__main__":
    # 测试
    validator = DocValidator()
    
    # 测试发票校验
    result = validator.validate_fapiao("test_invoice.jpg")
    print("发票校验结果:")
    print(f"  是否合规: {result['valid']}")
    print(f"  问题: {result['issues']}")
    
    # 测试合同校验
    contract_text = "合同金额100万元，付款方式月付，违约责任按法律规定"
    result2 = validator.validate_contract(contract_text)
    print("\\n合同校验结果:")
    print(f"  是否合规: {result2['valid']}")
    print(f"  问题: {result2['issues']}")
