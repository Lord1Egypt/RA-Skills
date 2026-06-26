#!/usr/bin/env python3
"""
互认基金月度数据自动更新脚本 - 双月处理版
同时处理上月和本月的 PDF，生成完整的对比数据
"""

import sys
from pathlib import Path

# 导入 OCR 版更新器
sys.path.insert(0, str(Path(__file__).parent))
from auto_update_ocr import FundUpdater


def process_two_months(template_file, pdf_dir_last, pdf_dir_current, output_file):
    """
    处理两个月份的 PDF 数据
    
    Args:
        template_file: Excel 模板路径
        pdf_dir_last: 上月 PDF 文件夹
        pdf_dir_current: 本月 PDF 文件夹
        output_file: 输出文件路径
    """
    skill_path = Path(__file__).parent.parent
    updater = FundUpdater(skill_path)
    
    print("=" * 80)
    print("互认基金月度数据更新 - 双月处理")
    print("=" * 80)
    print(f"\n模板文件：{template_file}")
    print(f"上月 PDF: {pdf_dir_last}")
    print(f"本月 PDF: {pdf_dir_current}")
    print(f"输出文件：{output_file}")
    
    # 重置日期更新标志
    updater._dates_updated = False
    
    # 步骤 1：处理上月 PDF（数据填入列 4）
    print(f"\n{'='*80}")
    print("步骤 1: 处理上月 PDF")
    print(f"{'='*80}")
    updater.update_excel(str(template_file), str(pdf_dir_last), str(output_file), target_month=None)
    
    # 步骤 2：处理本月 PDF（数据填入列 6）
    # 需要重新加载刚保存的文件
    print(f"\n{'='*80}")
    print("步骤 2: 处理本月 PDF")
    print(f"{'='*80}")
    updater._dates_updated = False  # 重置标志
    updater.update_excel(str(output_file), str(pdf_dir_current), str(output_file), target_month=None)
    
    print(f"\n{'='*80}")
    print(f"✅ 完成！输出文件：{output_file}")
    print(f"{'='*80}")
    
    return output_file


def main():
    """主函数"""
    if len(sys.argv) < 5:
        print("用法：python auto_update_two_months.py <template.xlsx> <pdf_last_month/> <pdf_current_month/> <output.xlsx>")
        sys.exit(1)
    
    template_file = Path(sys.argv[1])
    pdf_dir_last = Path(sys.argv[2])
    pdf_dir_current = Path(sys.argv[3])
    output_file = Path(sys.argv[4])
    
    process_two_months(template_file, pdf_dir_last, pdf_dir_current, output_file)


if __name__ == '__main__':
    main()
