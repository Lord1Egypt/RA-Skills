#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

#!/usr/bin/env python3
"""
Smart slide generation - automatically select template based on content.
Usage: python smart_generate.py --output <dir> --content <content.json>
"""

import sys
import json
import argparse
import os
import re
from pathlib import Path

# Import generators
sys.path.insert(0, str(Path(__file__).parent))
from generate_html import TEMPLATES


def analyze_content_type(content: str) -> str:
    """Analyze content and determine best template type."""
    content_lower = content.lower()
    
    # Keywords for each template type
    keywords = {
        'problem': ['%', '比例', '占比', '增长', '下降', '统计', '数据', '调查', '现状', '问题', '痛点', '挑战', '分析'],
        'solution': ['步骤', '方案', '实施', '方法', '流程', '措施', '路径', '建议', '解决', '推进', '阶段'],
        'matrix': ['矩阵', '选择', '优先', '战略', '决策', '象限', '分类', '评估', '定位'],
        'compare': ['对比', '比较', 'vs', 'versus', '优', '劣', 'before', 'after', '推荐', '避免', 'do', "don't"],
        'process': ['流程', '过程', '工作流', '审批', '环节', '节点', '决策点', '分支']
    }
    
    # Count matches for each type
    scores = {}
    for template_type, words in keywords.items():
        score = sum(1 for word in words if word in content_lower)
        scores[template_type] = score
    
    # Check for percentage patterns (problem type)
    if re.search(r'\d+%', content):
        scores['problem'] += 5
    
    # Check for step patterns (solution type)
    if re.search(r'[第步骤一二三四五六七八九十]+', content):
        scores['solution'] += 3
    
    # Get best match
    best_type = max(scores, key=scores.get)
    return best_type if scores[best_type] > 0 else 'solution'


def parse_slides_from_content(content: str) -> list:
    """Extract structured slides from content."""
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    slides = []
    current_slide = None
    
    for line in lines:
        # Detect title (short line, possibly with numbering)
        if len(line) < 30 and (re.match(r'^[一二三四五六七八九十\d\.、]+', line) or line.endswith('?') or line.endswith('？')):
            if current_slide:
                slides.append(current_slide)
            current_slide = {'title': re.sub(r'^[一二三四五六七八九十\d\.、\s]+', '', line), 'content': []}
        elif current_slide:
            # Add as content point
            if not line.startswith('#'):  # Skip markdown headers
                current_slide['content'].append(line)
    
    if current_slide:
        slides.append(current_slide)
    
    return slides


def generate_smart_slides(content: str, output_dir: str) -> dict:
    """Generate slides with automatic template selection."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract slides from content
    slides = parse_slides_from_content(content)
    
    if not slides:
        return {"success": False, "error": "No slides extracted from content"}
    
    generated = []
    
    for i, slide in enumerate(slides):
        # Analyze content type
        slide_content = slide['title'] + ' ' + ' '.join(slide.get('content', []))
        template_type = analyze_content_type(slide_content)
        
        # Prepare data based on template type
        if template_type == 'problem':
            # Extract percentages from content with smart label inference
            stats = []
            
            # Pattern: percentage followed by context
            for match in re.finditer(r'(\d+(?:\.\d+)?)\s*%\s*', slide_content):
                value = float(match.group(1))
                
                # Look back 20 chars for context (what the percentage refers to)
                start = max(0, match.start() - 20)
                context = slide_content[start:match.start()].strip()
                
                # Infer label from context keywords
                label = '指标'
                context_lower = context.lower()
                
                if any(kw in context_lower for kw in ['增长', '同比', '环比']):
                    label = '增长率'
                elif any(kw in context_lower for kw in ['占', '占比', '份额']):
                    label = '占比'
                elif any(kw in context_lower for kw in ['覆盖', '渗透']):
                    label = '覆盖率'
                elif any(kw in context_lower for kw in ['满意', '好评']):
                    label = '满意度'
                elif any(kw in context_lower for kw in ['用户', '客户', '企业']):
                    label = '用户增长率'
                elif any(kw in context_lower for kw in ['营收', '收入', '销售']):
                    label = '营收增长'
                
                stats.append({
                    'value': value,
                    'label': label,
                    'unit': '%',
                    'color': 'red' if value > 50 else 'orange'
                })
            
            data = {
                'eyebrow': f'第{i+1}页',
                'title': slide['title'],
                'description': slide['content'][0] if slide['content'] else '',
                'insight': slide['content'][-1] if len(slide['content']) > 1 else '',
                'stats': stats[:3] if stats else None
            }
        elif template_type == 'solution':
            data = {
                'eyebrow': f'第{i+1}页',
                'title': slide['title'],
                'steps': [{'number': f'0{j+1}', 'title': item[:10], 'detail': item} for j, item in enumerate(slide['content'][:5])]
            }
        elif template_type == 'compare':
            mid = len(slide['content']) // 2
            data = {
                'title': slide['title'],
                'left_items': slide['content'][:mid],
                'right_items': slide['content'][mid:]
            }
        else:
            data = {
                'title': slide['title'],
                'content': slide['content']
            }
        
        # Generate HTML
        output_file = os.path.join(output_dir, f'slide_{i+1:02d}.html')
        generator = TEMPLATES.get(template_type, TEMPLATES['solution'])
        html = generator(data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        generated.append({
            'file': output_file,
            'template': template_type,
            'title': slide['title']
        })
    
    return {
        'success': True,
        'output_dir': output_dir,
        'slides': generated,
        'total': len(generated)
    }


def generate_from_structured_slides(slides_data: dict, output_dir: str) -> dict:
    """Generate slides from structured JSON (from read_content.py --slides)."""
    os.makedirs(output_dir, exist_ok=True)
    
    slides = slides_data.get('slides', [])
    if not slides:
        return {"success": False, "error": "No slides in input data"}
    
    generated = []
    
    for i, slide in enumerate(slides):
        # Get title and content
        title = slide.get('title', f'幻灯片 {i+1}')
        content = slide.get('content', [])
        
        # Join content for analysis
        content_text = title + ' ' + ' '.join(content if isinstance(content, list) else [content])
        
        # Analyze content type
        template_type = analyze_content_type(content_text)
        
        # Prepare data based on template type
        if template_type == 'problem':
            # Extract percentages from content with smart label inference
            stats = []
            content_items = content if isinstance(content, list) else [content]
            
            for item in content_items:
                for match in re.finditer(r'(\d+(?:\.\d+)?)\s*%\s*', str(item)):
                    value = float(match.group(1))
                    
                    # Look back for context
                    start = max(0, match.start() - 20)
                    context = str(item)[start:match.start()].strip()
                    
                    # Infer label from context
                    label = '指标'
                    context_lower = context.lower()
                    
                    if any(kw in context_lower for kw in ['增长', '同比', '环比']):
                        label = '增长率'
                    elif any(kw in context_lower for kw in ['占', '占比', '份额']):
                        label = '占比'
                    elif any(kw in context_lower for kw in ['覆盖', '渗透']):
                        label = '覆盖率'
                    elif any(kw in context_lower for kw in ['满意', '好评']):
                        label = '满意度'
                    
                    stats.append({
                        'value': value,
                        'label': label,
                        'unit': '%',
                        'color': 'red' if value > 50 else 'orange'
                    })
            
            data = {
                'eyebrow': f'第{i+1}页',
                'title': title,
                'description': content[0] if isinstance(content, list) and content else str(content),
                'insight': content[-1] if isinstance(content, list) and len(content) > 1 else '',
                'stats': stats[:3] if stats else None
            }
        elif template_type == 'solution':
            items = content if isinstance(content, list) else [content]
            data = {
                'eyebrow': f'第{i+1}页',
                'title': title,
                'steps': [{'number': f'0{j+1}', 'title': item[:10], 'detail': item} for j, item in enumerate(items[:5])]
            }
        elif template_type == 'compare':
            items = content if isinstance(content, list) else [content]
            mid = len(items) // 2
            data = {
                'title': title,
                'left_items': items[:mid] if mid > 0 else items,
                'right_items': items[mid:] if mid > 0 else []
            }
        else:
            data = {
                'title': title,
                'content': content if isinstance(content, list) else [content]
            }
        
        # Generate HTML
        output_file = os.path.join(output_dir, f'slide_{i+1:02d}.html')
        generator = TEMPLATES.get(template_type, TEMPLATES['solution'])
        html = generator(data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        generated.append({
            'file': output_file,
            'template': template_type,
            'title': title
        })
    
    return {
        'success': True,
        'output_dir': output_dir,
        'slides': generated,
        'total': len(generated)
    }


def main():
    parser = argparse.ArgumentParser(description='Smart slide generation')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    parser.add_argument('--content', '-c', help='Content text or JSON file')
    
    args = parser.parse_args()
    
    # Load content
    if args.content:
        if os.path.exists(args.content):
            with open(args.content, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            try:
                data = json.loads(args.content)
            except:
                data = {'text': args.content}
    else:
        data = json.load(sys.stdin)
    
    # Check if it's structured slides from read_content.py
    if 'slides' in data:
        result = generate_from_structured_slides(data, args.output)
    else:
        # Raw text content
        content = data.get('text', data.get('content', ''))
        result = generate_smart_slides(content, args.output)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
