# -*- coding: utf-8 -*-
"""
A股持仓监控助手 - 一键运行
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_menu():
    print("="*60)
    print("A股持仓监控助手 v1.0.0")
    print("="*60)
    print("\n1. 查看持仓报告")
    print("2. 运行选股")
    print("3. 添加股票")
    print("4. 删除股票")
    print("5. 退出")
    print("="*60)

def main():
    while True:
        show_menu()
        choice = input("\n请选择功能 (1-5): ").strip()
        
        if choice == '1':
            print("\n正在生成持仓报告...")
            os.system("python portfolio.py analyze")
        elif choice == '2':
            print("\n正在运行选股...")
            os.system("python selector.py")
        elif choice == '3':
            code = input("股票代码: ")
            cost = input("成本价: ")
            qty = input("数量: ")
            os.system(f"python portfolio.py add {code} --cost {cost} --qty {qty}")
        elif choice == '4':
            code = input("股票代码: ")
            os.system(f"python portfolio.py remove {code}")
        elif choice == '5':
            print("再见！")
            break
        else:
            print("无效选择")
        
        input("\n按回车继续...")

if __name__ == '__main__':
    main()
