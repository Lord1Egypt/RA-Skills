#!/usr/bin/env python3
"""
PMC全文获取（XML/OAI方式，避免reCAPTCHA）
功能：使用OAI-PMH API获取PMC全文内容
"""

import requests
import xml.etree.ElementTree as ET
import json
import re
import time
from pathlib import Path

class PMCFullTextFetcher:
    """PMC全文获取器（XML方式）"""
    
    def __init__(self, output_dir="/tmp/pmc_fulltext"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.pmc_api = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
        self.pubmed_api = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        
    def get_pmcid_from_pmid(self, pmid):
        """从PMID获取PMCID"""
        try:
            url = f"{self.pubmed_api}/elink.fcgi"
            params = {
                'dbfrom': 'pubmed',
                'db': 'pmc',
                'id': pmid,
                'retmode': 'json'
            }
            r = requests.get(url, params=params, timeout=15)
            data = r.json()
            
            linksets = data.get('linksets', [])
            if linksets and 'linksetdbs' in linksets[0]:
                for db in linksets[0]['linksetdbs']:
                    if db.get('dbto') == 'pmc':
                        return str(db['links'][0])
            return None
        except Exception as e:
            print(f"获取PMCID失败: {e}")
            return None
    
    def fetch_pmc_fulltext(self, pmcid):
        """获取PMC全文（XML格式）"""
        try:
            params = {
                'verb': 'GetRecord',
                'identifier': f'oai:pubmedcentral.nih.gov:{pmcid}',
                'metadataPrefix': 'pmc'
            }
            
            print(f"  获取PMC全文: {pmcid}")
            r = requests.get(self.pmc_api, params=params, timeout=20)
            
            if r.status_code != 200:
                print(f"  ❌ 获取失败: HTTP {r.status_code}")
                return None
            
            # 解析XML
            try:
                root = ET.fromstring(r.content)
                
                # 提取正文
                ns = {'pmc': 'https://dtd.nlm.nih.gov/ncbi/pmc/articleset/',
                      'xlink': 'http://www.w3.org/1999/xlink'}
                
                # 提取所有段落文本
                body = root.find('.//pmc:body', ns)
                if body is None:
                    print(f"  ❌ 无正文内容")
                    return None
                
                full_text = ""
                for elem in body.iter():
                    if elem.text and elem.tag.endswith(('p', 'sec', 'title')):
                        full_text += elem.text + "\n"
                
                print(f"  ✅ 获取成功 ({len(full_text)} 字符)")
                return full_text
                
            except ET.ParseError as e:
                print(f"  ❌ XML解析失败: {e}")
                return None
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            return None
    
    def extract_metrics(self, text):
        """从全文提取关键指标"""
        metrics = {}
        text_lower = text.lower()
        
        # 提取AUC
        auc_patterns = [
            r'auc\s*[=:of]*\s*(0\.\d{2,3})',
            r'c-statistic\s*[=:]*\s*(0\.\d{2,3})',
            r'area under.*curve\s*[=:]*\s*(0\.\d{2,3})',
        ]
        for pattern in auc_patterns:
            match = re.search(pattern, text_lower)
            if match:
                metrics['auc'] = float(match.group(1))
                break
        
        # 提取样本量
        sample_patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*(?:patients?|subjects?|participants?|cases?|individuals?)',
            r'(?:n\s*=\s*|sample size\s*[=:]?\s*)(\d{1,3}(?:,\d{3})*)',
            r'total\s+(?:of\s+)?(\d{1,3}(?:,\d{3})*)',
        ]
        for pattern in sample_patterns:
            match = re.search(pattern, text_lower)
            if match:
                metrics['sample_size'] = int(match.group(1).replace(',', ''))
                break
        
        # 提取准确率
        acc_match = re.search(r'accurac(?:y|ies)\s*[=:]*\s*(\d{1,2}\.\d?)%?', text_lower)
        if acc_match:
            metrics['accuracy'] = float(acc_match.group(1))
        
        # 提取敏感性/特异性
        sens_match = re.search(r'sensitivit(?:y|ies)\s*[=:]*\s*(\d{1,2}\.\d?)%?', text_lower)
        if sens_match:
            metrics['sensitivity'] = float(sens_match.group(1))
        
        spec_match = re.search(r'specificit(?:y|ies)\s*[=:]*\s*(\d{1,2}\.\d?)%?', text_lower)
        if spec_match:
            metrics['specificity'] = float(spec_match.group(1))
        
        # 提取P值
        p_match = re.search(r'p\s*[<>=]\s*0?\.\d+', text_lower)
        if p_match:
            metrics['p_value'] = p_match.group(0)
        
        return metrics
    
    def process_card(self, card_id, pmid):
        """处理单个卡片"""
        print(f"\n处理 {card_id} (PMID: {pmid})")
        
        # 获取PMCID
        pmcid = self.get_pmcid_from_pmid(pmid)
        if not pmcid:
            print(f"  ❌ 无PMCID")
            return None
        print(f"  PMCID: {pmcid}")
        
        # 获取全文
        fulltext = self.fetch_pmc_fulltext(pmcid)
        if not fulltext:
            return None
        
        # 提取指标
        metrics = self.extract_metrics(fulltext)
        
        result = {
            'card_id': card_id,
            'pmid': pmid,
            'pmcid': pmcid,
            'fulltext_length': len(fulltext),
            'metrics': metrics,
            'text_preview': fulltext[:1000]
        }
        
        # 保存结果
        result_file = self.output_dir / f"{card_id}_fulltext.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ 结果保存: {result_file}")
        
        if metrics:
            print(f"  📊 提取数据:")
            for key, value in metrics.items():
                print(f"    - {key}: {value}")
        else:
            print(f"  ⚠️ 未提取到关键指标")
        
        return result


def batch_process(source_file):
    """批量处理"""
    with open(source_file) as f:
        papers = json.load(f)
    
    fetcher = PMCFullTextFetcher()
    results = []
    
    for paper in papers:
        card_id = paper.get('card_id')
        pmid = paper.get('pmid')
        
        if pmid:
            time.sleep(0.5)  # 限速
            result = fetcher.process_card(card_id, pmid)
            if result and result['metrics']:
                results.append(result)
    
    print(f"\n=== 批量处理完成 ===")
    print(f"总计: {len(papers)} 篇")
    print(f"有全文: {len([r for r in results if r])} 篇")
    print(f"有数据: {len([r for r in results if r and r['metrics']])} 篇")
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        batch_process(sys.argv[1])
    else:
        print("用法: python fetch-pmc-fulltext.py <papers.json>")