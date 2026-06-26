#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
增强版公式PDF转换工具
包含进程清理、自动重试、验证功能
"""

import os
import sys
import subprocess
import time
import argparse
import fitz  # pymupdf

def kill_edge_processes():
    """清理Edge进程"""
    import signal
    try:
        # Windows: 使用taskkill
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], 
                      capture_output=True, check=False)
        time.sleep(1)
        return True
    except Exception as e:
        print(f"清理进程时出错: {e}")
        return False

def verify_formulas_rendered(pdf_path):
    """验证PDF中公式是否已渲染"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        
        # 关键LaTeX原始代码
        latex_patterns = [
            r'\frac', r'\sqrt', r'\lim', r'\sum', r'\int', 
            r'\dfrac', r'\to', r'\infty', r'\ge', r'\le',
            r'\\\[', r'\\\(', r'$$', r'\cdot', r'_{', r'^{'
        ]
        
        found = [p for p in latex_patterns if p in text]
        if found:
            return False, f"发现未渲染代码: {', '.join(found[:3])}"
        return True, "公式已渲染"
    except Exception as e:
        return False, f"验证失败: {e}"

def convert_with_retry(html_path, pdf_path, timeout=30, max_retries=2):
    """带重试的转换"""
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    if not os.path.exists(edge_path):
        return False, f"Edge未找到: {edge_path}"
    
    # 转换为file:// URL
    if not html_path.startswith("file://"):
        file_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    else:
        file_url = html_path
    
    for attempt in range(max_retries):
        print(f"转换尝试 {attempt+1}/{max_retries}")
        
        # 清理进程（仅在第一次尝试后）
        if attempt > 0:
            kill_edge_processes()
            time.sleep(2)
        
        cmd = [
            edge_path,
            "--headless=new",
            f"--virtual-time-budget={timeout * 1000}",
            f"--print-to-pdf={pdf_path}",
            "--no-margins",
            "--disable-gpu",
            "--disable-software-rasterizer",
            file_url
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 15
            )
        except subprocess.TimeoutExpired:
            print(f"  ⏱️ 超时({timeout}s)")
            continue
        
        # 检查是否生成文件
        if not os.path.exists(pdf_path):
            print(f"  ❌ 文件未生成")
            timeout += 5  # 增加等待时间
            continue
        
        # 验证公式
        rendered, msg = verify_formulas_rendered(pdf_path)
        if rendered:
            size = os.path.getsize(pdf_path) / 1024
            return True, f"成功! {size:.1f}KB"
        else:
            print(f"  ⚠️ {msg}")
            timeout += 10  # 增加等待时间
    
    return False, "所有重试均失败"

def main():
    parser = argparse.ArgumentParser(description="公式PDF转换(增强版)")
    parser.add_argument("html_file", help="HTML文件")
    parser.add_argument("-o", "--output", help="PDF输出路径")
    parser.add_argument("-t", "--timeout", type=int, default=30, 
                       help="渲染等待时间(秒)")
    parser.add_argument("-r", "--retries", type=int, default=2,
                       help="重试次数")
    parser.add_argument("--kill-edge", action="store_true",
                       help="转换前清理Edge进程")
    parser.add_argument("--no-verify", action="store_true",
                       help="跳过公式验证")
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.html_file):
        print(f"错误: 文件不存在: {args.html_file}")
        return 1
    
    # 确定输出路径
    if args.output:
        pdf_path = args.output
    else:
        base = os.path.splitext(args.html_file)[0]
        pdf_path = base + ".pdf"
    
    # 清理进程（如果需要）
    if args.kill_edge:
        kill_edge_processes()
        time.sleep(1)
    
    # 转换
    start_time = time.time()
    success, msg = convert_with_retry(
        args.html_file, 
        pdf_path, 
        timeout=args.timeout,
        max_retries=args.retries
    )
    elapsed = time.time() - start_time
    
    if success:
        print(f"✅ {msg}")
        print(f"⏱️ 耗时: {elapsed:.1f}s")
        
        # 最终验证（除非跳过）
        if not args.no_verify:
            rendered, verify_msg = verify_formulas_rendered(pdf_path)
            print(f"🔍 {verify_msg}")
            if not rendered:
                print("⚠️ 注意: 可能存在渲染问题")
        
        return 0
    else:
        print(f"❌ 转换失败: {msg}")
        return 1

if __name__ == "__main__":
    sys.exit(main())