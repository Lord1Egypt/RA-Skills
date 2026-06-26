# FastOCR - OCR Tool (v1.1.0)
# MIT License - Open Source

import sys
import os
import re
from pathlib import Path
from datetime import datetime
from rapidocr_onnxruntime import RapidOCR


class FastOCRSkill:
    STANDARD_TAX_RATES = ['0%', '3%', '5%', '6%', '9%', '10%', '13%', '16%']
    OCR_CORRECTIONS = {'O': '0', 'I': '1', 'S': '5', 'B': '8'}
    
    def __init__(self):
        self.ocr = RapidOCR()
    
    def ocr_image(self, image_path):
        if not os.path.exists(image_path):
            return {"success": False, "error": "File not found"}
        result, elapse = self.ocr(image_path)
        lines = [{"text": line[1], "confidence": float(line[2])} for line in result] if result else []
        return {
            "success": True,
            "full_text": "\n".join([line["text"] for line in lines]),
            "lines": lines,
            "elapsed_ms": elapse * 1000 if elapse else 0
        }
    
    def extract_invoice(self, text):
        result = {'invoice_basic': {}, 'buyer': {}, 'seller': {}, 'amount': {}}
        match = re.search(r'发票代码 [：:\s]*(\d{10,12})', text)
        if match:
            result['invoice_basic']['invoice_code'] = match.group(1)
        match = re.search(r'发票号码 [：:\s]*(\d{8})', text)
        if match:
            result['invoice_basic']['invoice_number'] = match.group(1)
        match = re.search(r'购买方.*?识别号 [：:\s]*([A-Z0-9]{15,18})', text, re.IGNORECASE)
        if match:
            result['buyer']['tax_id'] = match.group(1)
        match = re.search(r'销售方.*?识别号 [：:\s]*([A-Z0-9]{15,18})', text, re.IGNORECASE)
        if match:
            result['seller']['tax_id'] = match.group(1)
        match = re.search(r'[（(]小写 [）)]\s*[￥¥]?\s*([\d.]+)', text)
        if match:
            result['amount']['amount_with_tax'] = float(match.group(1))
        return result
    
    def ocr_invoice(self, image_path):
        ocr_result = self.ocr_image(image_path)
        structured = self.extract_invoice(ocr_result['full_text'])
        return {"success": True, "ocr_result": ocr_result, "structured_data": structured}
    
    def extract_train_ticket(self, text):
        result = {'ticket_type': 'train_ticket', 'ticket_basic': {}, 'journey': {}, 'price': {}}
        match = re.search(r'([CGDKZT]\d+)', text)
        if match:
            result['ticket_basic']['train_number'] = match.group(1)
        match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', text)
        if match:
            result['ticket_basic']['datetime'] = match.group(1)
        match = re.search(r'([\d.]+) 元', text)
        if match:
            result['price']['amount'] = float(match.group(1))
        return result
    
    def ocr_train_ticket(self, image_path):
        ocr_result = self.ocr_image(image_path)
        data = self.extract_train_ticket(ocr_result['full_text'])
        return {"success": True, "ocr_result": ocr_result, "structured_data": data}


def main():
    if len(sys.argv) < 2:
        print("Usage: python rapidocr_minimal.py [ocr|invoice|train] <image_path>")
        sys.exit(1)
    skill = FastOCRSkill()
    cmd = sys.argv[1].lower()
    path = sys.argv[2] if len(sys.argv) > 2 else None
    if not path:
        print("Error: No image path provided")
        sys.exit(1)
    if cmd == 'ocr':
        result = skill.ocr_image(path)
    elif cmd == 'invoice':
        result = skill.ocr_invoice(path)
    elif cmd == 'train':
        result = skill.ocr_train_ticket(path)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
    print(f"Success: {result['success']}")
    if 'structured_data' in result:
        print(f"Data: {result['structured_data']}")


if __name__ == '__main__':
    main()
