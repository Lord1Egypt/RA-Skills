#!/usr/bin/env python3
"""
Portrait 数据导出模块 - 从财务数据文件中提取关键指标
支持从多个年度文件中提取数据
"""

import json
import re
from pathlib import Path
import pandas as pd


def parse_amount(val):
    """解析金额字符串为数字"""
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    # 处理带逗号的字符串，如 "890,900,112.98"
    s = str(val).replace(',', '').replace(' ', '')
    try:
        return float(s)
    except:
        return None


def extract_year_from_pdf_filename(filename: str) -> str:
    """从PDF文件名中提取年份"""
    match = re.search(r'(20\d{2})', filename)
    return match.group(1) if match else None


def get_years_from_pdfs(stock_dir: Path) -> list:
    """从PDF文件名中获取所有年份"""
    years = set()
    pdf_dir = stock_dir.parent.parent / "RAWPDF" / f"{stock_dir.name.split('_')[1]}PDF"
    if pdf_dir.exists():
        for pdf in pdf_dir.glob("*.pdf"):
            year = extract_year_from_pdf_filename(pdf.name)
            if year:
                years.add(year)
    return sorted(list(years), reverse=True)  # 降序排列，最新年份在前


def load_revenue_cost_data(stock, years: list) -> dict:
    """加载营业收入和成本数据"""
    metrics = {}
    revenue_cost_dir = stock.dir_path / "02_利润表附注" / "01_收入成本"
    
    if not revenue_cost_dir.exists():
        return metrics
    
    files = list(revenue_cost_dir.glob("*.xlsx"))
    if not files:
        return metrics
    
    try:
        df = pd.read_excel(files[0], sheet_name=0)
        cols = df.columns.tolist()
        
        # 查找收入列和成本列
        revenue_cols = [c for c in cols if '收入' in str(c) and '发生额' in str(c)]
        cost_cols = [c for c in cols if '成本' in str(c) and '发生额' in str(c)]
        
        # 查找合计行
        for idx, row in df.iterrows():
            item = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
            if '合计' in item or '总计' in item:
                revenue_data = {}
                cost_data = {}
                
                # 按列顺序对应年份（本期=最新年份，上期=次新年份）
                for i, col_name in enumerate(['本期发生额', '上期发生额']):
                    if i < len(years):
                        year = years[i]
                        # 查找匹配的列
                        rev_col = next((c for c in revenue_cols if col_name in str(c)), None)
                        cost_col = next((c for c in cost_cols if col_name in str(c)), None)
                        
                        if rev_col and pd.notna(row.get(rev_col)):
                            revenue_data[year] = parse_amount(row[rev_col])
                        if cost_col and pd.notna(row.get(cost_col)):
                            cost_data[year] = parse_amount(row[cost_col])
                
                if revenue_data:
                    metrics['营业收入'] = revenue_data
                if cost_data:
                    metrics['营业成本'] = cost_data
                break
    except Exception as e:
        print(f"    读取收入成本数据失败: {e}")
    
    return metrics


def load_expense_data(stock, years: list) -> dict:
    """加载期间费用数据"""
    metrics = {}
    expense_dir = stock.dir_path / "02_利润表附注" / "02_期间费用"
    
    if not expense_dir.exists():
        return metrics
    
    expense_mapping = {
        '管理费用': '管理费用',
        '销售费用': '销售费用',
        '研发费用': '研发费用',
        '财务费用': '财务费用'
    }
    
    for expense_keyword, metric_name in expense_mapping.items():
        files = list(expense_dir.glob(f"*{expense_keyword}*.xlsx"))
        if not files:
            continue
        
        try:
            df = pd.read_excel(files[0], sheet_name=0)
            expense_data = {}
            
            # 查找合计行
            for idx, row in df.iterrows():
                item = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                if '合计' in item:
                    # 按本期/上期对应年份
                    for i, col_name in enumerate(['本期发生额', '上期发生额']):
                        if i < len(years):
                            year = years[i]
                            # 查找匹配的列
                            matching_cols = [c for c in df.columns if col_name in str(c)]
                            if matching_cols:
                                val = row.get(matching_cols[0])
                                if pd.notna(val):
                                    expense_data[year] = parse_amount(val)
                    break
            
            if expense_data:
                metrics[metric_name] = expense_data
        except Exception as e:
            print(f"    读取{metric_name}数据失败: {e}")
    
    return metrics


def load_balance_sheet_data(stock, years: list) -> dict:
    """加载资产负债表数据"""
    metrics = {}
    bs_dir = stock.dir_path / "01_资产负债表附注"
    
    if not bs_dir.exists():
        return metrics
    
    # 应收账款
    ar_files = list(bs_dir.glob("*应收*账龄*.xlsx"))
    if ar_files:
        try:
            df = pd.read_excel(ar_files[0], sheet_name=0)
            # 取最后一行作为合计
            last_row = df.iloc[-1]
            ar_data = {}
            
            # 查找年份列（通常是数字列名）
            year_cols = [c for c in df.columns if str(c).isdigit() and len(str(c)) == 4]
            for i, col in enumerate(year_cols):
                if i < len(years):
                    year = years[i]
                    val = last_row.get(col)
                    if pd.notna(val):
                        ar_data[year] = parse_amount(val)
            
            if ar_data:
                metrics['应收账款'] = ar_data
        except Exception as e:
            print(f"    读取应收账款数据失败: {e}")
    
    # 存货
    inv_files = list(bs_dir.glob("*存货*.xlsx"))
    if inv_files:
        try:
            df = pd.read_excel(inv_files[0], sheet_name=0)
            last_row = df.iloc[-1]
            inv_data = {}
            
            year_cols = [c for c in df.columns if str(c).isdigit() and len(str(c)) == 4]
            for i, col in enumerate(year_cols):
                if i < len(years):
                    year = years[i]
                    val = last_row.get(col)
                    if pd.notna(val):
                        inv_data[year] = parse_amount(val)
            
            if inv_data:
                metrics['存货'] = inv_data
        except Exception as e:
            print(f"    读取存货数据失败: {e}")
    
    # 5. 研发创新数据
    mda_dir = stock.dir_path / "11_管理层讨论与分析"
    if mda_dir.exists():
        # 在研项目数量 - 使用最新年份的数据
        rnd_files = list(mda_dir.glob("**/*在研项目*.xlsx"))
        if rnd_files:
            try:
                df = pd.read_excel(rnd_files[0], sheet_name=0)
                # 统计总行数作为项目数量（简化处理）
                rnd_count = {}
                for year in years[:2]:  # 给最近两年相同的数据
                    rnd_count[year] = len(df)
                if rnd_count:
                    metrics['在研项目数量'] = rnd_count
                    print(f"    在研项目: {len(df)} 个")
            except Exception as e:
                print(f"    读取在研项目数据失败: {e}")
        
        # 知识产权数量
        ip_files = list(mda_dir.glob("**/*知识产权*.xlsx"))
        if ip_files:
            try:
                df = pd.read_excel(ip_files[0], sheet_name=0)
                ip_count = {}
                for year in years[:2]:
                    ip_count[year] = len(df)
                if ip_count:
                    metrics['知识产权数量'] = ip_count
                    print(f"    知识产权: {len(df)} 项")
            except Exception as e:
                print(f"    读取知识产权数据失败: {e}")
    
    # 6. 供应链风险数据（客户/供应商集中度）
    if mda_dir.exists():
        # 客户集中度
        customer_files = list(mda_dir.glob("**/*客户*.xlsx"))
        if customer_files:
            try:
                df = pd.read_excel(customer_files[0], sheet_name=0)
                print(f"    客户文件列名: {df.columns.tolist()[:5]}")
                # 查找占比数据
                customer_conc = {}
                for i, year in enumerate(years[:2]):
                    # 简化：取第一行的占比值
                    ratio_col = None
                    for col in df.columns:
                        if '比例' in str(col) or '占比' in str(col) or '%' in str(col):
                            ratio_col = col
                            break
                    
                    if ratio_col:
                        val = df[ratio_col].iloc[0]
                        if pd.notna(val):
                            customer_conc[year] = parse_amount(val)
                            print(f"      {year} 客户集中度: {val}")
                if customer_conc:
                    metrics['客户集中度'] = customer_conc
            except Exception as e:
                print(f"    读取客户集中度数据失败: {e}")
        
        # 供应商集中度
        supplier_files = list(mda_dir.glob("**/*供应商*.xlsx"))
        if supplier_files:
            try:
                df = pd.read_excel(supplier_files[0], sheet_name=0)
                print(f"    供应商文件列名: {df.columns.tolist()[:5]}")
                supplier_conc = {}
                for i, year in enumerate(years[:2]):
                    ratio_col = None
                    for col in df.columns:
                        if '比例' in str(col) or '占比' in str(col) or '%' in str(col):
                            ratio_col = col
                            break
                    
                    if ratio_col:
                        val = df[ratio_col].iloc[0]
                        if pd.notna(val):
                            supplier_conc[year] = parse_amount(val)
                            print(f"      {year} 供应商集中度: {val}")
                if supplier_conc:
                    metrics['供应商集中度'] = supplier_conc
            except Exception as e:
                print(f"    读取供应商集中度数据失败: {e}")
    
    return metrics


def calculate_derived_metrics(metrics: dict) -> dict:
    """计算派生指标"""
    # 计算毛利率
    if '营业收入' in metrics and '营业成本' in metrics:
        gross_margin = {}
        for year in metrics['营业收入'].keys():
            revenue = metrics['营业收入'].get(year)
            cost = metrics['营业成本'].get(year)
            if revenue and cost and revenue > 0:
                gross_margin[year] = round((revenue - cost) / revenue * 100, 2)
        if gross_margin:
            metrics['毛利率'] = gross_margin
    
    # 计算期间费用率
    if '营业收入' in metrics:
        for expense_type in ['管理费用', '销售费用', '研发费用']:
            if expense_type in metrics:
                expense_rate = {}
                for year in metrics['营业收入'].keys():
                    revenue = metrics['营业收入'].get(year)
                    expense = metrics[expense_type].get(year)
                    if revenue and expense and revenue > 0:
                        expense_rate[year] = round(expense / revenue * 100, 2)
                if expense_rate:
                    metrics[f'{expense_type}率'] = expense_rate
    
    # 计算总期间费用
    period_expenses = {}
    for expense_type in ['管理费用', '销售费用', '研发费用', '财务费用']:
        if expense_type in metrics:
            for year, val in metrics[expense_type].items():
                if year not in period_expenses:
                    period_expenses[year] = 0
                if val:
                    period_expenses[year] += val
    
    if period_expenses:
        metrics['期间费用合计'] = period_expenses
        
        # 计算期间费用率
        if '营业收入' in metrics:
            period_expense_rate = {}
            for year in metrics['营业收入'].keys():
                revenue = metrics['营业收入'].get(year)
                expense = period_expenses.get(year)
                if revenue and expense and revenue > 0:
                    period_expense_rate[year] = round(expense / revenue * 100, 2)
            if period_expense_rate:
                metrics['期间费用率'] = period_expense_rate
    
    return metrics


def load_financial_metrics(stock):
    """从各个财务数据文件中提取关键指标"""
    # 获取年份列表
    years = get_years_from_pdfs(stock.dir_path)
    if not years:
        years = ['2025', '2024', '2023']  # 默认年份
    
    print(f"    检测到年份: {years}")
    
    # 加载各类数据
    metrics = {}
    metrics.update(load_revenue_cost_data(stock, years))
    metrics.update(load_expense_data(stock, years))
    metrics.update(load_balance_sheet_data(stock, years))
    
    # 计算派生指标
    metrics = calculate_derived_metrics(metrics)
    
    return metrics, years


def save_portrait_data(stock, output_dir: Path):
    """
    从股票数据中提取关键指标并保存为 JSON
    """
    print(f"  📊 正在提取 {stock.code} {stock.name} 的财务数据...")
    
    metrics, years = load_financial_metrics(stock)
    
    portrait_data = {
        "code": stock.code,
        "name": stock.name,
        "years": years,
        "metrics": metrics
    }
    
    # 保存 JSON
    portrait_dir = output_dir / "portrait_data"
    portrait_dir.mkdir(exist_ok=True)
    json_file = portrait_dir / f"{stock.code}_{stock.name}_portrait_data.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(portrait_data, f, ensure_ascii=False, indent=2)
    
    print(f"  💾 Portrait 数据已保存: {json_file} ({len(years)} 年, {len(metrics)} 项指标)")
    for metric_name in sorted(metrics.keys()):
        print(f"      - {metric_name}")
    
    return json_file


if __name__ == "__main__":
    # 测试代码
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from CompanyPortrait import DataIndex
    
    output_dir = Path("output2")
    index = DataIndex(output_dir)
    stocks = index.list_all()
    
    for stock in stocks[:1]:
        save_portrait_data(stock, output_dir)
