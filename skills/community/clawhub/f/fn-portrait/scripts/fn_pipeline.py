#!/usr/bin/env python3
"""
FN Portrait Pipeline - OpenClaw Skill Entry Point
================================================
Usage: python fn_pipeline.py <stock_code> <stock_name> [years] [plate]
"""

import sys
import os
import shutil
import argparse
from pathlib import Path

# Get skill directory
SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import modules
from ReportLinkCrawler2 import CrawlerConfig, CNINFOClient, PLATE_NAME_MAP
from TextAnalysis9 import run as ta_run
from LLM2Excel3 import batch_process
from CompanyPortrait import DataIndex, plot_all_charts


def check_llm(model_name="gemma3:1b"):
    """Check if LLM service is ready"""
    if os.environ.get('DEEPSEEK_API_KEY'):
        print(f"✅ DeepSeek API ready")
        return True
    if os.environ.get('KIMI_API_KEY'):
        print(f"✅ Moonshot API ready")
        return True

    import urllib.request
    import json
    try:
        req = urllib.request.Request('http://127.0.0.1:11434/api/tags', method='GET')
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            models = [m['name'] for m in data.get('models', [])]
            if model_name in models:
                print(f"✅ Ollama ready, model {model_name} available")
                return True
            else:
                print(f"❌ Model {model_name} not found, installed: {models}")
                return False
    except Exception as e:
        print(f"❌ Ollama not ready: {e}")
        return False


def download_pdfs(stock_code: str, stock_name: str, years: list, plate: str, rawpdf_dir: Path):
    """Download annual report PDFs from CNINFO"""
    print(f"\n{'='*60}")
    print(f"📥 Step 1: Download Annual Report PDFs")
    print(f"{'='*60}")
    print(f"Stock: {stock_code} {stock_name}")
    print(f"Years: {', '.join(map(str, years))}")
    print(f"Plate: {plate}")

    stock_pdf_dir = rawpdf_dir / f"{stock_name}PDF"
    stock_pdf_dir.mkdir(parents=True, exist_ok=True)
    print(f"PDF save directory: {stock_pdf_dir}")

    plate_code = PLATE_NAME_MAP.get(plate, 'shkcp')
    downloaded = []

    for year in years:
        config = CrawlerConfig(
            target_year=year,
            report_type='年报',
            plate=plate_code,
            output_dir=str(stock_pdf_dir),
            delay_between_downloads=1.0,
        )
        client = CNINFOClient(config)

        start_date = f"{year}-03-01"
        end_date = f"{year+1}-04-30"

        print(f"\n  Searching {year} annual report ({start_date} ~ {end_date})...")
        results = client.search_announcements(start_date, end_date)

        stock_results = [
            r for r in results
            if r.get("secCode") == stock_code or stock_name in r.get("secName", "")
        ]

        if not stock_results:
            print(f"  ⚠️ No {year} annual report found")
            continue

        EXCLUDE_KEYWORDS = ['英文', '摘要', '已取消', '修订版', '更正后', 'XBRL']
        result = None
        for r in stock_results:
            if r.get("secCode") == stock_code:
                title = r.get("announcementTitle", "")
                if not any(kw in title for kw in EXCLUDE_KEYWORDS):
                    result = r
                    break

        if not result:
            for r in stock_results:
                if r.get("secCode") == stock_code:
                    result = r
                    break

        if not result:
            result = stock_results[0]

        adjunct_url = result.get("adjunctUrl", "")
        if not adjunct_url:
            print(f"  ⚠️ No PDF link")
            continue

        filename = f"{stock_code}_{stock_name}_{year}年报.pdf"
        save_path = stock_pdf_dir / filename

        if save_path.exists():
            print(f"  ⏭️ Already exists: {filename}")
            downloaded.append(save_path)
            continue

        success = client.download_pdf(
            adjunct_url=adjunct_url,
            save_path=str(save_path),
            company_code=stock_code,
            company_name=stock_name,
        )

        if success:
            print(f"  ✅ Downloaded: {filename}")
            downloaded.append(save_path)
        else:
            print(f"  ❌ Download failed")

    return downloaded, stock_pdf_dir


def extract_data(rawpdf_dir: Path, output_dir: Path, stock_code: str, stock_name: str):
    """Extract structured data from PDFs"""
    print(f"\n{'='*60}")
    print(f"🔍 Step 2: PDF Structured Extraction (TextAnalysis9)")
    print(f"{'='*60}")

    pdf_files = list(rawpdf_dir.glob(f"{stock_code}_{stock_name}_*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found for {stock_code}")
        return False

    print(f"Found {len(pdf_files)} PDF files")

    temp_input = output_dir / "_temp_input"
    temp_input.mkdir(exist_ok=True)
    for f in pdf_files:
        shutil.copy(f, temp_input / f.name)

    failed = ta_run(
        input_dir=str(temp_input),
        output_dir=str(output_dir),
        max_workers=2,
    )

    shutil.rmtree(temp_input, ignore_errors=True)

    if failed:
        print(f"\n⚠️ {len(failed)} files failed:")
        for p, e in failed.items():
            print(f"  {os.path.basename(p)}: {e[:200]}")
    else:
        print(f"\n✅ All PDFs extracted successfully")

    return len(failed) == 0


def llm_analysis(output_dir: Path, stock_code: str, stock_name: str):
    """LLM semantic analysis - 只分析当前股票的数据"""
    print(f"\n{'='*60}")
    print(f"🧠 Step 3: LLM Semantic Analysis (LLM2Excel3)")
    print(f"{'='*60}")

    if os.environ.get('DEEPSEEK_API_KEY'):
        provider = 'deepseek'
        model = 'deepseek-chat'
    elif os.environ.get('KIMI_API_KEY'):
        provider = 'moonshot'
        model = 'kimi-k2p5'
    else:
        provider = 'ollama'
        model = 'gemma3:1b'

    # 创建临时目录，只包含当前股票的数据
    company_dir = output_dir / f"{stock_code}_{stock_name}"
    if not company_dir.exists():
        print(f"⚠️ 未找到公司数据目录: {company_dir}")
        return

    # 调用 batch_process 分析当前股票
    # 注意：batch_process 会扫描 base_dir 下的所有公司
    # 我们需要修改逻辑，只处理当前股票
    from LLM2Excel3 import LLMCombinedAnalyzer
    
    analyzer = LLMCombinedAnalyzer(model=model, provider=provider)
    
    # 查找当前股票的文本文件
    txt_files = list(company_dir.rglob("*.txt"))
    
    if not txt_files:
        print(f"⚠️ 未找到文本文件: {company_dir}")
        return
    
    print(f"  找到 {len(txt_files)} 个文本文件")
    
    # 准备保存结果
    import pandas as pd
    all_business_results = []
    all_rd_results = []
    
    # 分析每个文本文件
    for txt_file in txt_files:
        print(f"  分析: {txt_file.name}")
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 根据文件路径判断分析类型
            rel_path = txt_file.relative_to(company_dir)
            
            if '经营情况' in str(rel_path) or '业务与行业' in str(rel_path):
                result = analyzer.analyze_business(text, stock_code, stock_name)
                if result and result.get('success') and 'data' in result:
                    all_business_results.extend(result['data'])
                    print(f"    ✅ 经营分析完成: {len(result['data'])} 条记录")
                else:
                    print(f"    ⚠️ 经营分析未返回结果")
            elif '核心' in str(rel_path) or '研发' in str(rel_path):
                result = analyzer.analyze_rd(text, stock_code, stock_name)
                if result and result.get('success') and 'data' in result:
                    all_rd_results.extend(result['data'])
                    print(f"    ✅ 研发分析完成: {len(result['data'])} 条记录")
                else:
                    print(f"    ⚠️ 研发分析未返回结果")
            else:
                # 默认分析
                result = analyzer.analyze_business(text, stock_code, stock_name)
                if result and result.get('success') and 'data' in result:
                    all_business_results.extend(result['data'])
                    print(f"    ✅ 分析完成: {len(result['data'])} 条记录")
                else:
                    print(f"    ⚠️ 分析未返回结果")
                
        except Exception as e:
            print(f"    ❌ 分析失败: {e}")
    
    # 保存结果到 Excel
    if all_business_results or all_rd_results:
        output_file = company_dir / f"{stock_code}_{stock_name}_LLM分析结果.xlsx"
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            if all_business_results:
                df_business = pd.DataFrame(all_business_results)
                df_business.to_excel(writer, sheet_name='经营情况分析', index=False)
                print(f"    💾 经营情况分析: {len(all_business_results)} 条记录")
            if all_rd_results:
                df_rd = pd.DataFrame(all_rd_results)
                df_rd.to_excel(writer, sheet_name='研发成果分析', index=False)
                print(f"    💾 研发成果分析: {len(all_rd_results)} 条记录")
        print(f"  ✅ LLM分析结果已保存: {output_file.name}")
    else:
        print(f"  ⚠️ 没有分析结果需要保存")

    print(f"\n✅ LLM analysis complete")


def generate_portrait(output_dir: Path, stock_code: str, stock_name: str):
    """Generate Portrait chart"""
    print(f"\n{'='*60}")
    print(f"📊 Step 4: Generate Portrait Chart")
    print(f"{'='*60}")

    index = DataIndex(output_dir)
    stock = index.search(stock_code)

    if stock is None:
        print(f"❌ No data found for {stock_code}")
        return False

    portraits_dir = output_dir.parent / "portraits"
    portraits_dir.mkdir(exist_ok=True)
    save_path = portraits_dir / f"Portrait_{stock.code}_{stock.name}.png"

    plot_all_charts(stock, save_path=save_path)
    print(f"\n✅ Portrait saved: {save_path}")
    return True


def parse_years(years_str: str):
    """Parse year range string"""
    if not years_str:
        return [2023, 2024, 2025]
    if "-" in years_str:
        start, end = years_str.split("-", 1)
        return list(range(int(start), int(end) + 1))
    else:
        return [int(years_str)]


def main():
    parser = argparse.ArgumentParser(description='FN Portrait Pipeline')
    parser.add_argument('stock_code', help='Stock code (6 digits)')
    parser.add_argument('stock_name', help='Company name in Chinese')
    parser.add_argument('--years', '-y', default='2023-2025', help='Year range (default: 2023-2025)')
    parser.add_argument('--plate', '-p', default='科创板', help='Stock plate (default: 科创板)')
    parser.add_argument('--rawpdf-dir', default='RAWPDF', help='PDF download directory')
    parser.add_argument('--output-dir', default='output2', help='Output directory')
    parser.add_argument('--skip-download', action='store_true', help='Skip download step')
    parser.add_argument('--skip-extract', action='store_true', help='Skip extraction step')
    parser.add_argument('--skip-llm', action='store_true', help='Skip LLM analysis')
    parser.add_argument('--skip-portrait', action='store_true', help='Skip portrait generation')
    args = parser.parse_args()

    # Setup paths
    skill_dir = Path(__file__).parent.parent
    rawpdf_dir = skill_dir / args.rawpdf_dir
    output_dir = skill_dir / args.output_dir
    rawpdf_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    years = parse_years(args.years)
    print(f"🎯 Target: {args.stock_code} {args.stock_name}")
    print(f"📅 Years: {', '.join(map(str, years))}")

    # Step 1: Download PDFs
    stock_pdf_dir = rawpdf_dir / f"{args.stock_name}PDF"
    if not args.skip_download:
        downloaded, stock_pdf_dir = download_pdfs(
            args.stock_code, args.stock_name, years, args.plate, rawpdf_dir
        )
        if not downloaded:
            print("\n❌ Download failed, pipeline terminated")
            return 1
    else:
        print("\n⏭️ Skipping download step")

    # Step 2: Extract data
    if not args.skip_extract:
        success = extract_data(stock_pdf_dir, output_dir, args.stock_code, args.stock_name)
        if not success:
            print("\n⚠️ Extraction had failures, continuing...")
    else:
        print("\n⏭️ Skipping extraction step")

    # Step 3: LLM analysis
    if not args.skip_llm:
        if not check_llm():
            print("\n❌ LLM not ready, skipping LLM analysis")
            return 1
        llm_analysis(output_dir, args.stock_code, args.stock_name)
    else:
        print("\n⏭️ Skipping LLM analysis")

    # Step 4: Generate Portrait
    if not args.skip_portrait:
        generate_portrait(output_dir, args.stock_code, args.stock_name)
    else:
        print("\n⏭️ Skipping portrait generation")

    print(f"\n{'='*60}")
    print(f"🎉 Pipeline Complete!")
    print(f"{'='*60}")
    portrait_path = output_dir.parent / 'portraits' / f'Portrait_{args.stock_code}_{args.stock_name}.png'
    print(f"Portrait: {portrait_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
