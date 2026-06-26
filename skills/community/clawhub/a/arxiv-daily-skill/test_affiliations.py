#!/usr/bin/env python3
"""
从 arXiv 页面提取机构信息 - 优化版
尝试多种策略，选择最可靠的结果
"""

import urllib.request
import re
import json

def extract_affiliations_from_arxiv(arxiv_id):
    """
    从 arXiv HTML 页面提取机构信息
    策略：
    1. 查找作者下方的机构行
    2. 查找已知机构名称
    3. 从 PDF 链接元数据推断
    """
    try:
        url = f"https://arxiv.org/abs/{arxiv_id}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 清理 HTML 标签但保留结构
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        affiliations = []
        
        # 策略 1: 查找已知顶级机构（高置信度）
        top_institutions = {
            # 中国
            'Tsinghua': 'Tsinghua University',
            'Peking': 'Peking University',
            'Shanghai Jiao Tong': 'Shanghai Jiao Tong University',
            'Zhejiang': 'Zhejiang University',
            'USTC': 'University of Science and Technology of China',
            'Nanjing': 'Nanjing University',
            'Fudan': 'Fudan University',
            'THUNLP': 'THUNLP',
            'MSRA': 'Microsoft Research Asia',
            
            # 美国
            'Stanford': 'Stanford University',
            'MIT': 'Massachusetts Institute of Technology',
            'Berkeley': 'UC Berkeley',
            'Carnegie Mellon': 'Carnegie Mellon University',
            'Harvard': 'Harvard University',
            'Princeton': 'Princeton University',
            'Cornell': 'Cornell University',
            'UW': 'University of Washington',
            'Georgia Tech': 'Georgia Institute of Technology',
            
            # 公司
            'Google': 'Google Research',
            'Microsoft': 'Microsoft Research',
            'Meta': 'Meta AI',
            'OpenAI': 'OpenAI',
            'Anthropic': 'Anthropic',
            'DeepMind': 'DeepMind',
            'IBM': 'IBM Research',
            'Amazon': 'Amazon Science',
            'Apple': 'Apple ML',
            'NVIDIA': 'NVIDIA Research',
            'ByteDance': 'ByteDance',
            'Tencent': 'Tencent',
            'Alibaba': 'Alibaba',
            'Baidu': 'Baidu',
            
            # 欧洲
            'ETH': 'ETH Zurich',
            'Oxford': 'University of Oxford',
            'Cambridge': 'University of Cambridge',
            'EPFL': 'EPFL',
            'MPI': 'Max Planck Institute',
        }
        
        for keyword, full_name in top_institutions.items():
            if keyword.lower() in text.lower():
                # 验证上下文（确保是机构提及，不是引用）
                pattern = r'[^.]{0,40}' + re.escape(keyword) + r'[^.]{0,40}'
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    # 检查是否是作者机构上下文
                    if any(w in match.lower() for w in ['author', 'university', 'institute', 'lab', 'research', 'dept', 'computer']):
                        if full_name not in affiliations:
                            affiliations.append(full_name)
                        break
        
        # 策略 2: 查找标准机构模式
        if not affiliations:
            patterns = [
                r'([A-Z][a-zA-Z]* University(?: of [A-Z][a-zA-Z ]+)?)',
                r'([A-Z][a-zA-Z]* Institute of Technology)',
                r'([A-Z][a-zA-Z]* Institute(?: of [A-Z][a-zA-Z ]+)?)',
                r'((?:Google|Microsoft|Meta|OpenAI|Anthropic|DeepMind) (?:Research|AI|Labs)?)',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    clean = match.strip()
                    if (10 < len(clean) < 60 and 
                        'arXiv' not in clean and
                        'License' not in clean and
                        clean not in affiliations):
                        affiliations.append(clean)
        
        # 策略 3: 查找 GitHub 代码仓库线索
        github_match = re.search(r'github\.com/([^/\s"]+/[^/\s"]+)', html)
        if github_match and not affiliations:
            repo = github_match.group(1)
            # 知名组织
            org_mapping = {
                'thunlp': ['Tsinghua University', 'THUNLP'],
                'google-research': ['Google Research'],
                'microsoft': ['Microsoft Research'],
                'meta-llama': ['Meta AI'],
                'openai': ['OpenAI'],
                'anthropics': ['Anthropic'],
                'deepmind': ['DeepMind'],
            }
            for org, affil in org_mapping.items():
                if org in repo.lower():
                    affiliations.extend(affil)
                    break
        
        # 去重并限制数量
        seen = set()
        unique = []
        for a in affiliations:
            key = a.lower()[:30]
            if key not in seen:
                seen.add(key)
                unique.append(a)
        
        return unique[:3]
        
    except Exception as e:
        print(f"  ⚠️ 获取失败：{e}")
        return []


if __name__ == "__main__":
    import sys
    
    # 测试论文列表
    test_papers = [
        ('2604.12986', 'Parallax - Agent Safety'),
        ('2604.13016', 'OPD - Tsinghua'),
        ('2604.13006', 'Instruction Collapse'),
        ('2604.13029', 'Visual DPO'),
        ('2604.13021', 'CT Enterography'),
    ]
    
    print("🔍 测试机构信息提取...\n")
    
    results = {}
    for arxiv_id, desc in test_papers:
        print(f"📄 {arxiv_id} - {desc}")
        affils = extract_affiliations_from_arxiv(arxiv_id)
        results[arxiv_id] = affils
        if affils:
            print(f"   ✅ {affils}")
        else:
            print(f"   ❌ 未找到机构信息")
        print()
    
    # 输出 Python 字典格式
    print("\n📋 硬编码字典（可复制到 fetch_arxiv.py）:")
    print("KNOWN_AFFILIATIONS = {")
    for arxiv_id, affils in results.items():
        if affils:
            print(f"    '{arxiv_id}': {json.dumps(affils, ensure_ascii=False)},")
    print("}")
