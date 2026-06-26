#!/usr/bin/env python3
"""
PMC/arXiv PDF自动下载 + 数据提取
功能：从PubMed ID获取PMC PDF，提取关键指标
"""

import requests
import sys
import json
import os
import re
import time
from pathlib import Path

PMC_API = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa_file_list.cgi"
PUBMED_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

class PMCPDFFetcher:
    def __init__(self, output_dir="/tmp/pmc_pdfs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def get_pmcid_from_pmid(self, pmid):
        """从PMID获取PMCID"""
        try:
            url = f"{PUBMED_API}/elink.fcgi"
            params = {
                'dbfrom': 'pubmed',
                'db': 'pmc',
                'id': pmid,
                'retmode': 'json'
            }
            r = requests.get(url, params=params, timeout=15)
            data = r.json()
            
            # 提取PMCID
            linksets = data.get('linksets', [])
            if linksets and 'linksetdbs' in linksets[0]:
                for db in linksets[0]['linksetdbs']:
                    if db.get('dbto') == 'pmc':
                        return db['links'][0]
            return None
        except Exception as e:
            print(f"获取PMCID失败: {e}")
            return None
    
    def check_pmc_fulltext(self, pmcid):
        """检查PMC是否有开放获取全文"""
        try:
            url = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
            params = {
                'verb': 'GetRecord',
                'identifier': f'oai:pubmedcentral.nih.gov:{pmcid}',
                'metadataPrefix': 'pmc'
            }
            r = requests.get(url, params=params, timeout=15)
            if r.status_code == 200 and '<error' not in r.text:
                return True
            return False
        except:
            return False
    
    def download_pmc_pdf(self, pmcid, card_id):
        """下载PMC PDF"""
        pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf"
        pdf_path = self.output_dir / f"{card_id}_pmc.pdf"
        
        try:
            print(f"  下载PDF: {pdf_url}")
            r = requests.get(pdf_url, timeout=30, stream=True)
            if r.status_code == 200:
                with open(pdf_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"  ✅ 下载成功: {pdf_path}")
                return str(pdf_path)
            else:
                print(f"  ❌ 下载失败: HTTP {r.status_code}")
                return None
        except Exception as e:
            print(f"  ❌ 下载错误: {e}")
            return None
    
    def extract_from_pdf(self, pdf_path, card_id):
        """从PDF提取关键数据"""
        try:
            import pdfplumber
            
            print(f"  解析PDF: {pdf_path}")
            
            extracted_data = {
                'card_id': card_id,
                'pdf_path': pdf_path,
                'text_samples': [],
                'metrics': {}
            }
            
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                
                # 提取前10页文本（通常是方法学和结果）
                for i, page in enumerate(pdf.pages[:10]):
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
                        if i < 3:  # 保存前3页样本
                            extracted_data['text_samples'].append(text[:500])
                
                # 提取关键指标
                extracted_data['metrics'] = self._extract_metrics(full_text)
                
            return extracted_data
            
        except Exception as e:
            print(f"  ❌ PDF解析错误: {e}")
            return None
    
    def _extract_metrics(self, text):
        """从文本提取关键指标"""
        metrics = {}
        text_lower = text.lower()
        
        # 提取AUC
        auc_patterns = [
            r'auc\s*[=:of]*\s*(0\.\d{2,3})',
            r'area under (?:the )?curve\s*[=:]*\s*(0\.\d{2,3})',
            r'c-statistic\s*[=:]*\s*(0\.\d{2,3})',
        ]
        for pattern in auc_patterns:
            match = re.search(pattern, text_lower)
            if match:
                metrics['auc'] = float(match.group(1))
                break
        
        # 提取样本量
        sample_patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*(?:patients?|subjects?|participants?|cases?)',
            r'(?:n\s*=\s*|sample size\s*[=:]?\s*)(\d{1,3}(?:,\d{3})*)',
            r'total\s+of\s+(\d{1,3}(?:,\d{3})*)',
        ]
        for pattern in sample_patterns:
            match = re.search(pattern, text_lower)
            if match:
                metrics['sample_size'] = match.group(1).replace(',', '')
                break
        
        # 提取准确率/敏感性/特异性
        acc_patterns = [
            r'accurac(?:y|ies)\s*[=:]*\s*(\d{1,2}\.\d?)%?',
            r'sensitivit(?:y|ies)\s*[=:]*\s*(\d{1,2}\.\d?)%?',
            r'specificit(?:y|ies)\s*[=:]*\s*(\d{1,2}\.\d?)%?',
        ]
        for pattern in acc_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                metrics['accuracy_values'] = [float(m) for m in matches[:3]]
                break
        
        # 提取P值
        p_match = re.search(r'p\s*[<>=]\s*([\d.]+)', text_lower)
        if p_match:
            metrics['p_value'] = p_match.group(0)
        
        # 提取成本/费用
        cost_patterns = [
            r'(?:saved|reduction|decrease)\s*(?:of\s*)?\$?([\d,]+(?:\.\d{2})?)',
            r'cost\s*(?:saving|reduction)\s*[=:]*\s*([\d.]+%?)',
        ]
        for pattern in cost_patterns:
            match = re.search(pattern, text_lower)
            if match:
                metrics['cost_data'] = match.group(1)
                break
        
        return metrics
    
    def process_card(self, card_id, pmid):
        """处理单个卡片"""
        print(f"\n处理 {card_id} (PMID: {pmid})")
        
        # 1. 获取PMCID
        pmcid = self.get_pmcid_from_pmid(pmid)
        if not pmcid:
            print(f"  ❌ 无PMCID，跳过")
            return None
        print(f"  PMCID: {pmcid}")
        
        # 2. 检查是否有全文
        if not self.check_pmc_fulltext(pmcid):
            print(f"  ❌ 无开放获取全文")
            return None
        print(f"  ✅ 有开放获取全文")
        
        # 3. 下载PDF
        pdf_path = self.download_pmc_pdf(pmcid, card_id)
        if not pdf_path:
            return None
        
        # 4. 解析PDF
        result = self.extract_from_pdf(pdf_path, card_id)
        
        # 5. 保存结果
        if result:
            result_file = self.output_dir / f"{card_id}_extracted.json"
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"  ✅ 结果保存: {result_file}")
            
            # 显示提取的数据
            metrics = result['metrics']
            if metrics:
                print(f"  📊 提取数据:")
                for key, value in metrics.items():
                    print(f"    - {key}: {value}")
            else:
                print(f"  ⚠️ 未提取到关键指标")
        
        return result


class ArXivPDFDownloader:
    """arXiv PDF下载器"""
    
    def __init__(self, output_dir="/tmp/arxiv_pdfs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def download_and_extract(self, arxiv_id, card_id):
        """下载并解析arXiv PDF"""
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        pdf_path = self.output_dir / f"{card_id}_arxiv.pdf"
        
        print(f"\n处理 {card_id} (arXiv: {arxiv_id})")
        print(f"  下载: {pdf_url}")
        
        try:
            r = requests.get(pdf_url, timeout=30, stream=True)
            if r.status_code == 200:
                with open(pdf_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"  ✅ 下载成功")
                
                # 解析PDF
                fetcher = PMCPDFFetcher(self.output_dir)
                result = fetcher.extract_from_pdf(str(pdf_path), card_id)
                
                if result:
                    result_file = self.output_dir / f"{card_id}_extracted.json"
                    with open(result_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"  ✅ 结果保存")
                    
                    metrics = result['metrics']
                    if metrics:
                        print(f"  📊 提取数据:")
                        for key, value in metrics.items():
                            print(f"    - {key}: {value}")
                
                return result
            else:
                print(f"  ❌ 下载失败: HTTP {r.status_code}")
                return None
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            return None


def batch_process(source_file):
    """批量处理卡片"""
    import json
    
    with open(source_file) as f:
        papers = json.load(f)
    
    fetcher = PMCPDFFetcher()
    arxiv_fetcher = ArXivPDFDownloader()
    
    results = []
    
    for paper in papers:
        card_id = paper.get('card_id')
        pmid = paper.get('pmid')
        arxiv_id = paper.get('arxiv_id')
        
        if pmid:
            # 限速：3次/秒
            time.sleep(0.4)
            result = fetcher.process_card(card_id, pmid)
            if result:
                results.append(result)
        
        elif arxiv_id:
            time.sleep(0.4)
            result = arxiv_fetcher.download_and_extract(arxiv_id, card_id)
            if result:
                results.append(result)
    
    print(f"\n=== 批量处理完成 ===")
    print(f"总计: {len(papers)} 篇")
    print(f"成功: {len(results)} 篇")
    print(f"失败: {len(papers) - len(results)} 篇")
    
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  单篇: python fetch-pmc-pdf.py <card_id> <pmid>")
        print("  批量: python fetch-pmc-pdf.py --batch <papers.json>")
        sys.exit(1)
    
    if sys.argv[1] == "--batch":
        batch_process(sys.argv[2])
    else:
        card_id = sys.argv[1]
        pmid = sys.argv[2]
        
        fetcher = PMCPDFFetcher()
        result = fetcher.process_card(card_id, pmid)