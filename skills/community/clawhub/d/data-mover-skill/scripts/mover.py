#!/usr/bin/env python3
"""
Data Mover Skill - 跨系统数据自动搬运工
OCR 识别 + 自动复制粘贴 + 多系统支持

作者：于金泽
版本：1.0.0
日期：2026-03-16
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import hashlib

# 尝试导入依赖
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  警告：pyautogui 未安装，自动化功能受限")

try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    print("⚠️  警告：PaddleOCR 未安装，OCR 功能受限")


class DataMover:
    """数据搬运工"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.ocr_engine = None
        self.logs = []
        
        # 初始化 OCR
        if PADDLEOCR_AVAILABLE:
            try:
                self.ocr_engine = PaddleOCR(
                    use_angle_cls=True,
                    lang='ch',
                    show_log=False
                )
                print("✅ OCR 引擎初始化成功")
            except Exception as e:
                print(f"⚠️  OCR 引擎初始化失败：{e}")
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def capture_screenshot(self, region: Tuple = None) -> str:
        """截图"""
        if not PYAUTOGUI_AVAILABLE:
            self.log("pyautogui 不可用，无法截图", "ERROR")
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            screenshot.save(filename)
            self.log(f"截图已保存：{filename}")
            return filename
        except Exception as e:
            self.log(f"截图失败：{e}", "ERROR")
            return None
    
    def ocr_image(self, image_path: str) -> List[Dict]:
        """OCR 识别图片"""
        if not self.ocr_engine:
            self.log("OCR 引擎未初始化", "ERROR")
            return []
        
        try:
            result = self.ocr_engine.ocr(image_path, cls=True)
            
            if not result or not result[0]:
                return []
            
            recognized_data = []
            for line in result[0]:
                bbox, (text, confidence) = line
                recognized_data.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
            
            self.log(f"识别到 {len(recognized_data)} 条数据")
            return recognized_data
        except Exception as e:
            self.log(f"OCR 识别失败：{e}", "ERROR")
            return []
    
    def extract_table(self, recognized_data: List[Dict]) -> List[Dict]:
        """从 OCR 结果提取表格数据"""
        # 简单实现：按行分组
        rows = []
        current_row = []
        last_y = None
        
        for item in recognized_data:
            bbox = item['bbox']
            y_center = (bbox[0][1] + bbox[2][1]) / 2
            
            if last_y and abs(y_center - last_y) > 10:
                # 新行
                if current_row:
                    rows.append(current_row)
                current_row = []
            
            current_row.append(item['text'])
            last_y = y_center
        
        if current_row:
            rows.append(current_row)
        
        # 转换为字典列表（假设第一行是表头）
        if len(rows) < 2:
            return []
        
        headers = rows[0]
        data = []
        
        for row in rows[1:]:
            record = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    record[header] = row[i]
            data.append(record)
        
        self.log(f"提取到 {len(data)} 条记录")
        return data
    
    def validate_data(self, record: Dict, rules: Dict) -> Tuple[bool, List[str]]:
        """验证数据"""
        import re
        
        errors = []
        
        # 必填字段检查
        required = rules.get('required_fields', [])
        for field in required:
            if field not in record or not record[field]:
                errors.append(f"缺少必填字段：{field}")
        
        # 格式验证
        if 'email' in record and 'email' in rules.get('rules', {}):
            pattern = rules['rules']['email']
            if not re.match(pattern, record['email']):
                errors.append(f"邮箱格式错误：{record['email']}")
        
        if 'phone' in record and 'phone' in rules.get('rules', {}):
            pattern = rules['rules']['phone']
            if not re.match(pattern, record['phone']):
                errors.append(f"电话格式错误：{record['phone']}")
        
        return len(errors) == 0, errors
    
    def copy_to_clipboard(self, text: str):
        """复制到剪贴板"""
        if PYAUTOGUI_AVAILABLE:
            pyperclip.copy(text)
            self.log("已复制到剪贴板")
        else:
            # 使用系统命令
            import platform
            system = platform.system()
            if system == 'Windows':
                subprocess.run(['clip'], input=text.encode(), shell=True)
            elif system == 'Darwin':
                subprocess.run(['pbcopy'], input=text.encode())
            else:  # Linux
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode())
    
    def paste_from_clipboard(self) -> str:
        """从剪贴板粘贴"""
        if PYAUTOGUI_AVAILABLE:
            return pyperclip.paste()
        else:
            import platform
            system = platform.system()
            if system == 'Windows':
                result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], 
                                      capture_output=True, text=True)
                return result.stdout
            elif system == 'Darwin':
                result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                return result.stdout
            else:  # Linux
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                      capture_output=True, text=True)
                return result.stdout
    
    def move_data_excel_to_crm(self, excel_file: str, mapping: Dict) -> Dict:
        """Excel → CRM 数据搬运（模拟）"""
        self.log(f"开始从 Excel 搬运数据：{excel_file}")
        
        # 读取 Excel（需要 pandas）
        try:
            import pandas as pd
            df = pd.read_excel(excel_file)
            records = df.to_dict('records')
            self.log(f"读取到 {len(records)} 条记录")
        except ImportError:
            self.log("pandas 未安装，无法读取 Excel", "ERROR")
            return {'success': False, 'error': 'pandas not installed'}
        except Exception as e:
            self.log(f"读取 Excel 失败：{e}", "ERROR")
            return {'success': False, 'error': str(e)}
        
        # 处理记录
        results = {
            'total': len(records),
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        validation_rules = self.config.get('validation', {})
        
        for i, record in enumerate(records, 1):
            self.log(f"处理记录 {i}/{len(records)}", "DEBUG")
            
            # 字段映射
            mapped_record = {}
            for source_field, target_field in mapping.items():
                if source_field in record:
                    mapped_record[target_field] = record[source_field]
            
            # 数据验证
            is_valid, errors = self.validate_data(mapped_record, validation_rules)
            
            if is_valid:
                # 模拟写入 CRM（实际需要 CRM API）
                self.log(f"✅ 记录 {i} 验证通过", "DEBUG")
                results['success'] += 1
            else:
                self.log(f"❌ 记录 {i} 验证失败：{errors}", "WARNING")
                results['failed'] += 1
                results['errors'].append({
                    'record': i,
                    'errors': errors
                })
        
        return results
    
    def run_demo(self):
        """运行演示"""
        self.log("=" * 60)
        self.log("🚀 Data Mover Skill 演示")
        self.log("=" * 60)
        
        print("\n功能演示:")
        print("1. 截图 OCR 识别")
        print("2. Excel → CRM 数据搬运")
        print("3. 邮件 → Excel 数据提取")
        print("4. 批量 PDF 处理")
        print()
        
        # 演示配置
        demo_config = {
            'validation': {
                'enabled': True,
                'rules': {
                    'email': r'^[\w.-]+@[\w.-]+\.\w+$',
                    'phone': r'^1[3-9]\d{9}$'
                },
                'required_fields': ['name', 'phone']
            }
        }
        
        self.config = demo_config
        
        # 演示数据验证
        self.log("\n📋 演示数据验证:")
        test_records = [
            {'name': '张三', 'phone': '13800138000', 'email': 'zhangsan@example.com'},
            {'name': '李四', 'phone': '1380013800', 'email': 'lisi@example.com'},  # 电话错误
            {'name': '王五', 'phone': '', 'email': 'wangwu@example.com'},  # 缺少电话
        ]
        
        for record in test_records:
            is_valid, errors = self.validate_data(record, demo_config['validation'])
            status = "✅" if is_valid else "❌"
            print(f"{status} {record['name']}: {'验证通过' if is_valid else ', '.join(errors)}")
        
        print()
        self.log("=" * 60)
        self.log("✅ 演示完成")
        self.log("=" * 60)
        
        return {
            'demo': True,
            'status': 'success',
            'message': '演示完成，技能已就绪'
        }


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Data Mover Skill - 跨系统数据搬运工')
    parser.add_argument('--demo', action='store_true', help='运行演示')
    parser.add_argument('--ocr', type=str, help='OCR 识别图片')
    parser.add_argument('--screenshot', action='store_true', help='截图并识别')
    parser.add_argument('--excel', type=str, help='Excel 文件路径')
    parser.add_argument('--mapping', type=str, help='映射配置文件')
    parser.add_argument('--config', type=str, help='配置文件路径')
    
    args = parser.parse_args()
    
    # 加载配置
    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
    
    # 创建搬运工
    mover = DataMover(config)
    
    # 执行操作
    if args.demo:
        result = mover.run_demo()
    elif args.ocr:
        result = mover.ocr_image(args.ocr)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.screenshot:
        screenshot = mover.capture_screenshot()
        if screenshot:
            result = mover.ocr_image(screenshot)
            print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.excel:
        mapping = {}
        if args.mapping and os.path.exists(args.mapping):
            with open(args.mapping, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
        result = mover.move_data_excel_to_crm(args.excel, mapping)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
