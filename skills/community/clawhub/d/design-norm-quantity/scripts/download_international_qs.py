# -*- coding: utf-8 -*-
"""
度量衡智库 · 国际QS资料下载器 v1.0
=====================================

下载RICS、Arcadis、利比等国际QS咨询公司的标准和方法论文档

来源：
1. RICS New Rules of Measurement (NRM 1-3)
2. RICS Cost Analysis and Benchmarking
3. Arcadis Construction Cost Handbook
4. HKIS Practice Notes for Quantity Surveyors
5. CIOB Code of Practice
"""

import os
import urllib.request
import urllib.error
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 国际QS标准PDF下载列表
QS_PDF_SOURCES = {
    # RICS New Rules of Measurement
    "nrm1_order_of_cost_estimating": {
        "url": "https://www.rics.org/content/dam/ricsglobal/documents/standards/nrm_1_order_of_cost_estimating_and_cost_planning_2nd_edition_rics.pdf",
        "description": "RICS NRM1 - Cost Estimating and Cost Planning",
        "size_mb": 3.5
    },
    "nrm2_detailed_measurement": {
        "url": "https://www.rics.org/content/dam/ricsglobal/documents/standards/october_2021_nrm_2.pdf",
        "description": "RICS NRM2 - Detailed Measurement for Building Works",
        "size_mb": 2.0
    },
    "nrm3_cost_planning": {
        "url": "https://edshare.gcu.ac.uk/3948/2/PDF/NRM24~27.pdf",
        "description": "RICS NRM3 - Cost Planning and Design Development",
        "size_mb": 1.5
    },
    
    # RICS Cost Analysis
    "cost_analysis_benchmarking": {
        "url": "https://www.rics.org/content/dam/ricsglobal/documents/standards/Cost-analysis-and-benchmarking_2nd-edition.pdf",
        "description": "RICS Cost Analysis and Benchmarking 2nd Edition",
        "size_mb": 4.0
    },
    
    # Arcadis Cost Handbook
    "arcadis_cch_2025": {
        "url": "https://media.arcadis.com/-/media/project/arcadiscom/com/perspectives/asia/publications/cch/2025/2025-cnhk-cost-handbookfinal-online.pdf",
        "description": "Arcadis China & Hong Kong Cost Handbook 2025",
        "size_mb": 8.0
    },
    
    # HKIS Practice Notes
    "hkis_qs_cost_plans": {
        "url": "https://wwvv.hkis.org.hk/ufiles/QS-costplans2016.pdf",
        "description": "HKIS Practice Notes for Quantity Surveyors - Cost Plans",
        "size_mb": 1.0
    },
    
    # Davis Langdon Quarterly Report
    "dls_quarterly_q1_2023": {
        "url": "https://dlsconsultant.com/wp-content/uploads/2024/02/DLS-Quarterly-Report-Q1-2023-20250509.pdf",
        "description": "Davis Langdon Quarterly Construction Cost Report Q1 2023",
        "size_mb": 2.0
    },
    
    # Quantity Surveyor's Pocket Book
    "qs_pocket_book": {
        "url": "https://www.iqytechnicalcollege.com/quantitysurveyorspocketbook.pdf",
        "description": "Quantity Surveyor's Pocket Book",
        "size_mb": 5.0
    },
    
    # CIOB Code of Practice
    "ciob_project_management": {
        "url": "https://assets.thalia.media/doc/artikel/cfb/b63/cfbb6327f516071fbfc2bc715c9b854000f165f5.pdf",
        "description": "CIOB Code of Practice for Project Management",
        "size_mb": 3.0
    },
}

def get_download_dir():
    """获取下载目录"""
    base_dir = Path(__file__).parent.parent
    download_dir = base_dir / "data" / "international_qs"
    download_dir.mkdir(parents=True, exist_ok=True)
    return download_dir

def download_pdf(name: str, info: dict) -> bool:
    """
    下载单个PDF文件
    
    Args:
        name: 文件标识名
        info: 包含url和description的字典
    
    Returns:
        bool: 下载是否成功
    """
    download_dir = get_download_dir()
    file_path = download_dir / f"{name}.pdf"
    
    # 如果文件已存在，跳过
    if file_path.exists():
        logger.info(f"[SKIP] {name} already exists")
        return True
    
    url = info["url"]
    description = info["description"]
    
    logger.info(f"[DOWNLOAD] {name}: {description}")
    logger.info(f"[URL] {url}")
    
    try:
        # 创建请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        
        # 下载文件
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
            
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(content)
            
            file_size = len(content) / (1024 * 1024)  # MB
            logger.info(f"[SUCCESS] Downloaded {name}: {file_size:.2f} MB")
            return True
            
    except urllib.error.HTTPError as e:
        logger.error(f"[HTTP ERROR] {name}: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        logger.error(f"[URL ERROR] {name}: {e.reason}")
    except Exception as e:
        logger.error(f"[ERROR] {name}: {str(e)}")
    
    return False

def download_all() -> dict:
    """
    下载所有PDF文件
    
    Returns:
        dict: 下载结果统计
    """
    download_dir = get_download_dir()
    logger.info("=" * 60)
    logger.info("度量衡智库 · 国际QS资料下载器 v1.0")
    logger.info("=" * 60)
    logger.info(f"Download Directory: {download_dir}")
    logger.info(f"Total Files: {len(QS_PDF_SOURCES)}")
    logger.info("=" * 60)
    
    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }
    
    for name, info in QS_PDF_SOURCES.items():
        success = download_pdf(name, info)
        if success:
            results["success"].append(name)
        else:
            results["failed"].append(name)
    
    # 打印结果
    logger.info("=" * 60)
    logger.info("下载结果统计")
    logger.info("=" * 60)
    logger.info(f"成功: {len(results['success'])}/{len(QS_PDF_SOURCES)}")
    logger.info(f"失败: {len(results['failed'])}/{len(QS_PDF_SOURCES)}")
    
    if results["failed"]:
        logger.warning("失败的文件:")
        for name in results["failed"]:
            logger.warning(f"  - {name}")
    
    logger.info("=" * 60)
    logger.info("下载完成!")
    logger.info("=" * 60)
    
    return results

def list_downloaded_files() -> list:
    """列出已下载的文件"""
    download_dir = get_download_dir()
    files = list(download_dir.glob("*.pdf"))
    
    logger.info("=" * 60)
    logger.info("已下载的国际QS资料")
    logger.info("=" * 60)
    
    for f in files:
        size_mb = f.stat().st_size / (1024 * 1024)
        logger.info(f"  {f.name} ({size_mb:.2f} MB)")
    
    logger.info(f"\n总计: {len(files)} 个文件")
    logger.info("=" * 60)
    
    return files

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_downloaded_files()
        else:
            # 下载指定文件
            name = sys.argv[1]
            if name in QS_PDF_SOURCES:
                download_pdf(name, QS_PDF_SOURCES[name])
            else:
                logger.error(f"Unknown file: {name}")
                logger.info(f"Available files: {', '.join(QS_PDF_SOURCES.keys())}")
    else:
        download_all()
