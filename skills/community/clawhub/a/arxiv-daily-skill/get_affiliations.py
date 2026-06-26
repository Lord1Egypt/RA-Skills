#!/usr/bin/env python3
# 获取论文机构信息 - 辅助脚本

import urllib.request
import re
import json

def get_paper_affiliations(arxiv_id):
    """
    从 arXiv HTML 页面提取机构信息
    返回：机构列表
    """
    try:
        url = f"https://arxiv.org/abs/{arxiv_id}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 清理 HTML
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        
        # 知名机构列表（按优先级）
        known_orgs = [
            # 中国高校
            'Tsinghua University', 'Peking University', 'Shanghai Jiao Tong University',
            'Zhejiang University', 'University of Science and Technology of China',
            'Nanjing University', 'Fudan University', 'Harbin Institute of Technology',
            'Beihang University', 'Tongji University',
            '清华大学', '北京大学', '上海交通大学', '浙江大学', '中国科学技术大学',
            '南京大学', '复旦大学', '哈尔滨工业大学', '北京航空航天大学', '同济大学',
            
            # 国际高校
            'MIT', 'Stanford University', 'Carnegie Mellon University', 'UC Berkeley',
            'Harvard University', 'Princeton University', 'Yale University',
            'University of Washington', 'Georgia Institute of Technology',
            'ETH Zurich', 'University of Toronto', 'McGill University',
            'University of Cambridge', 'University of Oxford',
            
            # 研究机构
            'Microsoft Research', 'Google Research', 'Meta AI', 'Meta FAIR',
            'OpenAI', 'Anthropic', 'DeepMind', 'IBM Research', 'Amazon Science',
            'Apple Machine Learning', 'NVIDIA Research', 'Adobe Research',
            'Salesforce Research', 'ByteDance', 'Tencent', 'Alibaba', 'Baidu',
            
            # 其他
            'Institute', 'Laboratory', 'Lab', 'Research Center', 'AI Lab'
        ]
        
        affiliations = []
        
        # 查找已知机构
        for org in known_orgs:
            if org.lower() in text.lower():
                # 找到上下文
                pattern = r'[^.,]{0,30}' + re.escape(org) + r'[^.,]{0,30}'
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    clean = match.strip()
                    if len(clean) > len(org) * 0.8 and len(clean) < 100:
                        if org not in [a for a in affiliations]:
                            affiliations.append(org)
                        break
        
        # 如果没有找到已知机构，尝试通用模式
        if not affiliations:
            patterns = [
                r'([A-Z][a-zA-Z]* University)',
                r'([A-Z][a-zA-Z]* Institute of Technology)',
                r'((?:Microsoft|Google|Meta|OpenAI|Anthropic|DeepMind) (?:Research|AI|Labs)?)',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if match not in affiliations and len(match) < 60:
                        affiliations.append(match)
        
        # 限制数量
        return list(dict.fromkeys(affiliations))[:3]  # 去重并保持顺序
        
    except Exception as e:
        return []

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        arxiv_id = sys.argv[1]
        affils = get_paper_affiliations(arxiv_id)
        print(json.dumps(affils, ensure_ascii=False))
    else:
        # 测试
        test_ids = ['2604.12986', '2604.13016', '2604.13006']
        for aid in test_ids:
            affils = get_paper_affiliations(aid)
            print(f"{aid}: {affils}")
