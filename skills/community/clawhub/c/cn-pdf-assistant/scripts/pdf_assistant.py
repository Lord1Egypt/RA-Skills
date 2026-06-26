#!/usr/bin/env python3
"""
PDF智能助手核心脚本
支持摘要、问答、表格提取、翻译、页面操作
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional

import PyPDF2
import pdfplumber


def extract_text(pdf_path: str, pages: Optional[List[int]] = None) -> Dict:
    """
    提取PDF文本内容
    
    Args:
        pdf_path: PDF文件路径
        pages: 指定页码列表（None表示全部）
        
    Returns:
        {
            'text': 完整文本,
            'pages': 每页文本列表,
            'total_pages': 总页数,
            'metadata': PDF元数据
        }
    """
    result = {
        'text': '',
        'pages': [],
        'total_pages': 0,
        'metadata': {}
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            result['total_pages'] = len(pdf.pages)
            result['metadata'] = pdf.metadata or {}
            
            page_range = pages if pages else range(len(pdf.pages))
            
            for i in page_range:
                if i < len(pdf.pages):
                    page = pdf.pages[i]
                    page_text = page.extract_text() or ''
                    result['pages'].append({
                        'page_num': i + 1,
                        'text': page_text,
                        'char_count': len(page_text)
                    })
                    result['text'] += f"\n\n--- 第{i+1}页 ---\n\n{page_text}"
        
        return result
        
    except Exception as e:
        return {'error': f'PDF读取失败: {str(e)}'}


def generate_summary(pdf_path: str, max_length: int = 500) -> Dict:
    """
    生成PDF内容摘要
    
    策略：
    1. 提取前3页 + 后2页（通常是摘要和结论）
    2. 识别章节标题
    3. 统计关键词频率
    """
    data = extract_text(pdf_path)
    
    if 'error' in data:
        return data
    
    # 提取关键页面内容
    key_content = ''
    pages = data['pages']
    
    # 前3页
    for p in pages[:3]:
        key_content += p['text'] + '\n'
    
    # 后2页（如果有）
    if len(pages) > 5:
        for p in pages[-2:]:
            key_content += p['text'] + '\n'
    
    # 提取章节标题（简单启发式）
    headings = []
    lines = key_content.split('\n')
    for line in lines:
        line = line.strip()
        # 章节标题特征：短行、数字编号、无标点结尾
        if 5 < len(line) < 50 and not line.endswith(('。', '，', '.', ',')):
            if re.match(r'^(第[一二三四五六七八九十\d]+章|Chapter \d+|\d+\.[\d\.]*|\d+、)', line):
                headings.append(line)
    
    # 统计关键词（简单词频）
    words = re.findall(r'[\u4e00-\u9fa5]{2,}|[a-zA-Z]{4,}', key_content)
    word_freq = {}
    for w in words:
        w = w.lower()
        if len(w) > 1:
            word_freq[w] = word_freq.get(w, 0) + 1
    
    # 取高频词（排除常见词）
    stop_words = {'this', 'that', 'with', 'from', 'they', 'have', 'been', 'their', 'were', 'which', 'would', 'there', 'could', 'should'}
    keywords = sorted(
        [(w, c) for w, c in word_freq.items() if w not in stop_words and c > 1],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    # 生成摘要文本
    summary_text = f"""📄 文档摘要

📖 基本信息：
- 文件名：{os.path.basename(pdf_path)}
- 总页数：{data['total_pages']} 页
- 总字数：约 {sum(p['char_count'] for p in pages)} 字符

📋 章节结构：
{chr(10).join(['• ' + h for h in headings[:8]]) if headings else '• 未识别到明确章节标题'}

🔑 关键词：
{', '.join([w for w, c in keywords]) if keywords else '暂无'}

📝 内容预览：
{key_content[:max_length]}...

💡 提示：使用 "PDF问答" 功能可深入了解具体内容
"""
    
    return {
        'summary': summary_text,
        'headings': headings[:10],
        'keywords': [w for w, c in keywords],
        'total_pages': data['total_pages'],
        'char_count': sum(p['char_count'] for p in pages)
    }


def extract_tables(pdf_path: str, page_num: Optional[int] = None) -> List[Dict]:
    """
    提取PDF中的表格
    
    Args:
        pdf_path: PDF路径
        page_num: 指定页码（None表示所有页）
        
    Returns:
        表格列表，每个包含page_num, table_num, data, shape
    """
    tables = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages_to_check = [pdf.pages[page_num-1]] if page_num else pdf.pages
            
            for page_idx, page in enumerate(pages_to_check, 1):
                page_tables = page.extract_tables()
                
                for table_idx, table in enumerate(page_tables, 1):
                    if table and len(table) > 1:
                        tables.append({
                            'page_num': page_num if page_num else page_idx,
                            'table_num': table_idx,
                            'data': table,
                            'rows': len(table),
                            'cols': len(table[0]) if table else 0
                        })
        
        return tables
        
    except Exception as e:
        return [{'error': f'表格提取失败: {str(e)}'}]


def answer_question(pdf_path: str, question: str) -> Dict:
    """
    基于PDF内容回答问题（简化版，不含LLM）
    
    策略：
    1. 提取所有文本
    2. 关键词匹配定位相关段落
    3. 返回相关段落及页码
    """
    data = extract_text(pdf_path)
    
    if 'error' in data:
        return data
    
    # 提取问题关键词
    q_keywords = re.findall(r'[\u4e00-\u9fa5]{2,}|[a-zA-Z]{3,}', question.lower())
    q_keywords = [k for k in q_keywords if len(k) > 2]
    
    # 搜索相关段落
    relevant_passages = []
    
    for page in data['pages']:
        page_text = page['text'].lower()
        score = sum(1 for kw in q_keywords if kw in page_text)
        
        if score > 0:
            # 提取包含关键词的句子
            sentences = re.split(r'[。\.\n]', page['text'])
            for sent in sentences:
                sent_score = sum(1 for kw in q_keywords if kw in sent.lower())
                if sent_score > 0:
                    relevant_passages.append({
                        'page': page['page_num'],
                        'text': sent.strip(),
                        'score': sent_score + score
                    })
    
    # 按相关度排序
    relevant_passages.sort(key=lambda x: x['score'], reverse=True)
    
    # 生成回答
    if relevant_passages:
        top_passages = relevant_passages[:5]
        answer = f"根据PDF内容，找到以下相关信息：\n\n"
        for p in top_passages:
            answer += f"📄 第{p['page']}页：{p['text'][:150]}...\n\n"
    else:
        answer = "未在PDF中找到与问题直接相关的内容。\n建议：\n1. 检查问题关键词是否准确\n2. 尝试使用文档中的专业术语\n3. 确认PDF是否包含相关内容"
    
    return {
        'question': question,
        'answer': answer,
        'relevant_pages': list(set(p['page'] for p in relevant_passages[:5])),
        'match_count': len(relevant_passages)
    }


def ocr_pdf(pdf_path: str, lang: str = 'chi_sim+eng') -> Dict:
    """
    对PDF进行OCR识别（支持扫描版PDF）
    
    Args:
        pdf_path: PDF文件路径
        lang: Tesseract语言包（chi_sim+eng=中英文）
        
    Returns:
        {
            'text': 完整OCR文本,
            'pages': 每页OCR文本列表,
            'total_pages': 总页数,
            'confidence_avg': 平均置信度
        }
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
        from PIL import Image
        
        # 转换PDF为图片
        print(f"🖼️  正在将PDF转换为图片...")
        images = convert_from_path(pdf_path, dpi=300)
        
        result = {
            'text': '',
            'pages': [],
            'total_pages': len(images),
            'confidence_avg': 0
        }
        
        total_confidence = 0
        
        for idx, img in enumerate(images, 1):
            print(f"🔍 正在OCR识别第 {idx}/{len(images)} 页...")
            
            # OCR识别
            ocr_data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
            
            # 提取文本
            page_text = pytesseract.image_to_string(img, lang=lang)
            result['pages'].append({
                'page_num': idx,
                'text': page_text,
                'char_count': len(page_text)
            })
            result['text'] += f"\n\n--- 第{idx}页 ---\n\n{page_text}"
            
            # 计算平均置信度
            confidences = [int(c) for c in ocr_data['conf'] if int(c) > 0]
            if confidences:
                page_conf = sum(confidences) / len(confidences)
                total_confidence += page_conf
        
        if result['total_pages'] > 0:
            result['confidence_avg'] = total_confidence / result['total_pages']
        
        print(f"✅ OCR完成！平均置信度: {result['confidence_avg']:.1f}%")
        
        return result
        
    except ImportError as e:
        return {'error': f'缺少依赖库: {str(e)}。请安装: pip install pdf2image pytesseract Pillow'}
    except Exception as e:
        return {'error': f'OCR识别失败: {str(e)}'}


def split_pdf(pdf_path: str, output_dir: str, pages_per_file: int = 1) -> List[str]:
    """
    拆分PDF为多个文件
    
    Args:
        pdf_path: 原PDF路径
        output_dir: 输出目录
        pages_per_file: 每个文件的页数
        
    Returns:
        生成的文件路径列表
    """
    output_files = []
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        base_name = Path(pdf_path).stem
        
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)
            
            for start in range(0, total_pages, pages_per_file):
                writer = PyPDF2.PdfWriter()
                end = min(start + pages_per_file, total_pages)
                
                for i in range(start, end):
                    writer.add_page(reader.pages[i])
                
                output_path = os.path.join(
                    output_dir,
                    f"{base_name}_p{start+1}-{end}.pdf"
                )
                
                with open(output_path, 'wb') as out_f:
                    writer.write(out_f)
                
                output_files.append(output_path)
        
        return output_files
        
    except Exception as e:
        return [f'error: {str(e)}']


def main():
    parser = argparse.ArgumentParser(description='PDF智能助手')
    parser.add_argument('pdf_path', help='PDF文件路径')
    parser.add_argument('--action', '-a', 
                       choices=['summary', 'tables', 'ask', 'split', 'text', 'ocr'],
                       default='summary',
                       help='操作类型')
    parser.add_argument('--question', '-q', help='问答模式的问题')
    parser.add_argument('--page', '-p', type=int, help='指定页码')
    parser.add_argument('--output', '-o', help='输出目录')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(json.dumps({'error': 'PDF文件不存在'}, ensure_ascii=False))
        sys.exit(1)
    
    print(f"📄 处理PDF: {os.path.basename(args.pdf_path)}")
    
    if args.action == 'summary':
        result = generate_summary(args.pdf_path)
        print(result['summary'])
        
    elif args.action == 'tables':
        tables = extract_tables(args.pdf_path, args.page)
        print(f"找到 {len(tables)} 个表格")
        for t in tables:
            if 'error' in t:
                print(f"❌ {t['error']}")
            else:
                print(f"\n📊 第{t['page_num']}页 表格{t['table_num']}: {t['rows']}行×{t['cols']}列")
        
    elif args.action == 'ask':
        if not args.question:
            print(json.dumps({'error': '问答模式需要提供 --question'}, ensure_ascii=False))
            sys.exit(1)
        result = answer_question(args.pdf_path, args.question)
        print(f"\n❓ 问题: {result['question']}")
        print(f"\n💡 回答:\n{result['answer']}")
        
    elif args.action == 'split':
        output_dir = args.output or os.path.expanduser('~/Documents/PDFAssistant/split')
        files = split_pdf(args.pdf_path, output_dir)
        print(f"✅ 已拆分为 {len(files)} 个文件:")
        for f in files:
            if f.startswith('error:'):
                print(f"❌ {f}")
            else:
                print(f"   {f}")
    
    elif args.action == 'text':
        data = extract_text(args.pdf_path, [args.page-1] if args.page else None)
        if 'error' in data:
            print(f"❌ {data['error']}")
        else:
            print(data['text'][:3000])
    
    elif args.action == 'ocr':
        ocr_result = ocr_pdf(args.pdf_path)
        if 'error' in ocr_result:
            print(f"❌ {ocr_result['error']}")
        else:
            print(f"\n📄 OCR识别完成！")
            print(f"   总页数: {ocr_result['total_pages']}")
            print(f"   平均置信度: {ocr_result['confidence_avg']:.1f}%")
            print(f"\n📝 识别文本预览（前500字）:\n{ocr_result['text'][:500]}...")
            
            # 保存完整OCR结果
            output_path = args.output or os.path.expanduser('~/Documents/PDFAssistant/ocr_result.txt')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(ocr_result['text'])
            print(f"\n💾 完整OCR结果已保存: {output_path}")
    
    # 输出JSON结果
    print("\n" + json.dumps({'action': args.action, 'success': True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
