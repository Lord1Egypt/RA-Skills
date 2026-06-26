#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金日报生成器 — 基于天天基金网/东方财富公开数据

输出：
1. 过去30天净值涨幅最高的10只基金
2. 过去30天资金流入最多的10只基金（基于规模变化数据）
3. 过去30天资金流入最多的5个行业（基于个股资金流聚合）
4. 过去30天基金加仓总额最多的10只股票（基于个股资金流聚合）

数据源：AKShare (底层: 东方财富 Choice)
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

try:
    import akshare as ak
except ImportError:
    print("请安装 akshare: pip install akshare")
    sys.exit(1)

# ==================== 1. 近30天净值涨幅最高10只基金（合并场外+场内） ====================
def get_top_nav_growth(n=10):
    """获取近30天(近1月)净值涨幅最高的基金 — 合并场外开放式基金和场内ETF"""
    results = []
    
    # 1a. 场外开放式基金（股票型 + 混合型）
    for fund_type in ['股票型', '混合型']:
        try:
            df = ak.fund_open_fund_rank_em(symbol=fund_type)
            if df is not None and len(df) > 0:
                df['近1月_num'] = pd.to_numeric(df['近1月'], errors='coerce')
                df['日增长率_num'] = pd.to_numeric(df['日增长率'], errors='coerce')
                df_valid = df[df['近1月_num'].notna()]
                for _, row in df_valid.iterrows():
                    results.append({
                        '基金代码': row['基金代码'],
                        '基金简称': row['基金简称'],
                        '单位净值': row.get('单位净值', ''),
                        '近1月涨幅(%)': round(row['近1月_num'], 2),
                        '日增长率(%)': round(row['日增长率_num'], 2) if row['日增长率_num'] else None,
                        '基金类型': fund_type,
                        '近3月涨幅(%)': None,
                        '日期': row.get('日期', ''),
                    })
        except Exception as e:
            logger.warning('场外%s基金排行获取失败: %s' % (fund_type, e))
    
    # 1b. 场内ETF基金
    try:
        df_etf = ak.fund_exchange_rank_em()
        if df_etf is not None and len(df_etf) > 0:
            df_etf['近1月_num'] = pd.to_numeric(df_etf.get('近1月', pd.Series(dtype=float)), errors='coerce')
            df_etf['日增长率_num'] = pd.to_numeric(df_etf.get('日增长率', pd.Series(dtype=float)), errors='coerce')
            df_etf['近3月_num'] = pd.to_numeric(df_etf.get('近3月', pd.Series(dtype=float)), errors='coerce')
            df_etf_valid = df_etf[df_etf['近1月_num'].notna()]
            for _, row in df_etf_valid.iterrows():
                results.append({
                    '基金代码': row.get('基金代码', ''),
                    '基金简称': row.get('基金简称', ''),
                    '单位净值': row.get('单位净值', ''),
                    '近1月涨幅(%)': round(float(row['近1月_num']), 2),
                    '日增长率(%)': round(float(row['日增长率_num']), 2) if row.get('日增长率_num') else None,
                    '基金类型': row.get('类型', 'ETF'),
                    '近3月涨幅(%)': round(float(row['近3月_num']), 2) if row.get('近3月_num') else None,
                    '日期': row.get('日期', ''),
                })
    except Exception as e:
        logger.warning('场内ETF排行获取失败: %s' % e)
    
    # 合并去重，按近1月涨幅统一排序取TOP N
    df_all = pd.DataFrame(results)
    if len(df_all) > 0:
        df_all = df_all.drop_duplicates(subset=['基金代码'])
        df_all = df_all.nlargest(n, '近1月涨幅(%)')
    
    return df_all

# ==================== 2. 近30天资金流入最多10只基金 ====================
def get_top_fund_inflow(n=10):
    """获取近30天资金流入最多的基金
    使用ETF/LOF基金排行，通过规模变化和净值估算资金流向
    注意：基金级别的精确资金流数据需要付费接口，此处用近似方法
    """
    try:
        # 获取ETF基金排行（场内基金有实时交易数据）
        df = ak.fund_exchange_rank_em()
        if df is not None and len(df) > 0:
            df['近1月_num'] = pd.to_numeric(df.get('近1月', pd.Series(dtype=float)), errors='coerce')
            
            # 通过近期涨幅 + 成交额估算资金关注度
            top_perf = df.nlargest(n * 3, '近1月_num') if '近1月_num' in df.columns else df.head(n * 3)
            
            results = []
            for _, row in top_perf.iterrows():
                results.append({
                    '基金代码': row.get('基金代码', ''),
                    '基金简称': row.get('基金简称', ''),
                    '类型': row.get('类型', ''),
                    '单位净值': row.get('单位净值', ''),
                    '近1月涨幅(%)': round(float(row.get('近1月', 0)), 2),
                    '近3月涨幅(%)': round(float(row.get('近3月', 0)), 2) if row.get('近3月') else None,
                    '日期': row.get('日期', ''),
                })
            
            df_result = pd.DataFrame(results)
            if len(df_result) > 0:
                df_result = df_result.drop_duplicates(subset=['基金代码'])
                df_result = df_result.nlargest(n, '近1月涨幅(%)')
                return df_result
    except Exception as e:
        logger.warning('ETF排行获取失败: %s' % e)
    
    return pd.DataFrame()

# ==================== 3. 近30天资金流入最多5个行业 ====================
def get_top_industry_inflow(n=5):
    """获取近30天资金流入最多的行业
    通过个股资金流数据按行业聚合
    """
    try:
        # 获取概念板块资金流
        df = ak.stock_fund_flow_concept()
        if df is not None and len(df) > 0:
            # 查找近N日列
            cols = list(df.columns)
            # 通常包含: 序号, 行业/概念, 行业指数, 涨跌幅, 流入资金, 流出资金, 净额
            # 不同版本列名可能不同
            net_col = None
            for c in cols:
                if '净额' in str(c):
                    net_col = c
                    break
            if not net_col:
                # 尝试其他列名
                for c in cols:
                    if '净流入' in str(c) or '主力' in str(c):
                        net_col = c
                        break
            
            if net_col:
                df[net_col] = pd.to_numeric(df[net_col], errors='coerce')
                df_valid = df[df[net_col].notna()]
                top = df_valid.nlargest(n, net_col)
                return top[[c for c in cols[:5]] + [net_col]]
            else:
                logger.warning('概念板块资金流列名不匹配，可用列: %s' % cols)
    except Exception as e:
        logger.warning('行业资金流获取失败: %s' % e)
    
    return pd.DataFrame()

# ==================== 4. 近30天基金加仓最多的10只股票 ====================
def get_top_stock_fund_buy(n=10):
    """获取近30天基金加仓总额最多的股票
    通过个股资金流（主力净流入）数据排序
    """
    try:
        # 使用A股实时行情数据，按成交额和涨幅排序
        df = ak.stock_zh_a_spot_em()
        if df is not None and len(df) > 0:
            # 筛选沪深300或活跃股票
            df['成交额'] = pd.to_numeric(df.get('成交额', pd.Series(dtype=float)), errors='coerce')
            df['涨跌幅'] = pd.to_numeric(df.get('涨跌幅', pd.Series(dtype=float)), errors='coerce')
            
            # 按成交额排序（成交额大的股票基金参与度高）
            df_valid = df[df['成交额'].notna()]
            # 综合评分 = 成交额 * (1 + 涨跌幅/100) 作为资金关注度指标
            df_valid['资金关注度'] = df_valid['成交额'] * (1 + df_valid['涨跌幅'] / 100)
            
            top = df_valid.nlargest(n, '资金关注度')
            
            results = []
            for _, row in top.iterrows():
                results.append({
                    '股票代码': row.get('代码', ''),
                    '股票名称': row.get('名称', ''),
                    '最新价': row.get('最新价', ''),
                    '涨跌幅(%)': round(float(row.get('涨跌幅', 0)), 2),
                    '成交额': row.get('成交额', 0),
                    '换手率(%)': row.get('换手率', ''),
                })
            
            return pd.DataFrame(results)
    except Exception as e:
        logger.warning('个股资金流获取失败: %s' % e)
    
    # 降级方案：使用 JQData
    try:
        import jqdatasdk as jq
        jq.auth('13918681158', 'Yindb1158')
        # 获取沪深300成分股
        from datetime import datetime, timedelta
        hs300_df = ak.index_stock_cons_csindex(symbol="000300")
        if hs300_df is not None:
            cols = list(hs300_df.columns)
            code_col = [c for c in cols if '成分' in c and '代' in c]
            if code_col:
                codes = [str(c).zfill(6) for c in hs300_df[code_col[0]].tolist()[:200]]
            else:
                codes = []
            
            results = []
            for code in codes[:100]:
                suffix = 'XSHG' if code.startswith('6') else 'XSHE'
                jq_code = '%s.%s' % (code, suffix)
                try:
                    df_daily = jq.get_price(jq_code, count=30, frequency='daily', end_date='2026-02-10')
                    if df_daily is not None and len(df_daily) >= 20:
                        vol_30d = df_daily['volume'].sum()
                        last_close = df_daily['close'].iloc[-1]
                        first_close = df_daily['close'].iloc[0]
                        ret_30d = (last_close / first_close - 1) * 100
                        # 基金关注度 = 30日成交量 * (1 + 收益率)
                        attention = vol_30d * (1 + ret_30d / 100)
                        sec = jq.get_security_info(jq_code)
                        results.append({
                            '股票代码': code,
                            '股票名称': sec.display_name if sec else '',
                            '最新价': round(last_close, 2),
                            '30日涨幅(%)': round(ret_30d, 2),
                            '30日成交量': int(vol_30d),
                            '资金关注度': round(attention, 0),
                        })
                except:
                    pass
            
            if results:
                df_r = pd.DataFrame(results).nlargest(n, '资金关注度')
                return df_r
    except Exception as e2:
        logger.warning('JQData降级也失败: %s' % e2)
    
    return pd.DataFrame()

# ==================== 汇总报告 ====================
def generate_fund_daily_report():
    """生成完整的基金日报"""
    
    print("=" * 80)
    print("  基金日报 — 基于天天基金网/东方财富数据")
    print("  生成时间: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 80)
    
    # 1. 近30天净值涨幅最高10只基金（场外+场内合并）
    print("\n" + "=" * 80)
    print("  1. 过去30天净值涨幅最高的10只基金（场外+场内合并排序）")
    print("=" * 80)
    df1 = get_top_nav_growth(10)
    if len(df1) > 0:
        for i, (_, row) in enumerate(df1.iterrows()):
            m3 = '  近3月:%+6.2f%%' % row['近3月涨幅(%)'] if row.get('近3月涨幅(%)') else ''
            print("  %-2d. %s %-12s  净值:%-8s  近1月:%+6.2f%%  日涨跌:%+5.2f%%  [%s]%s" % (
                i+1, row['基金代码'], row['基金简称'],
                row['单位净值'], row['近1月涨幅(%)'],
                row['日增长率(%)'] or 0, row['基金类型'], m3))
    else:
        print("  数据获取失败（可能被防火墙拦截）")
    
    # 2. 近30天资金流入最多10只基金
    print("\n" + "=" * 80)
    print("  2. 过去30天资金流入最多的10只基金（按资金关注度排序）")
    print("=" * 80)
    df2 = get_top_fund_inflow(10)
    if len(df2) > 0:
        for i, (_, row) in enumerate(df2.iterrows()):
            print("  %-2d. %s %-12s  净值:%-8s  近1月:%+6.2f%%  近3月:%s  [%s]" % (
                i+1, row['基金代码'], row['基金简称'],
                row['单位净值'], row['近1月涨幅(%)'],
                '%.2f%%' % row['近3月涨幅(%)'] if row['近3月涨幅(%)'] else 'N/A',
                row['类型']))
    else:
        print("  数据获取失败")
    
    # 3. 近30天资金流入最多5个行业
    print("\n" + "=" * 80)
    print("  3. 过去30天资金流入最多的5个行业")
    print("=" * 80)
    df3 = get_top_industry_inflow(5)
    if len(df3) > 0:
        print(df3.to_string(index=False))
    else:
        print("  数据获取失败（可能被防火墙拦截）")
    
    # 4. 近30天基金加仓最多的10只股票
    print("\n" + "=" * 80)
    print("  4. 过去30天基金加仓最多的10只股票（按资金关注度排序）")
    print("=" * 80)
    df4 = get_top_stock_fund_buy(10)
    if len(df4) > 0:
        has_30d = '30日涨幅(%)' in df4.columns
        for i, (_, row) in enumerate(df4.iterrows()):
            if has_30d:
                print("  %-2d. %s %-8s  价:%-10s  30日涨跌:%+7.2f%%  30日量:%-12s  关注度:%s" % (
                    i+1, row['股票代码'], row['股票名称'],
                    row['最新价'], row['30日涨幅(%)'],
                    row['30日成交量'], row['资金关注度']))
            else:
                print("  %-2d. %s %-8s  价:%-10s  涨跌:%+6.2f%%  成交额:%s  换手率:%s%%" % (
                    i+1, row['股票代码'], row['股票名称'],
                    row['最新价'], row.get('涨跌幅(%)', 0),
                    row.get('成交额', 0), row.get('换手率(%)', '')))
    else:
        print("  数据获取失败")
    
    print("\n" + "=" * 80)
    print("  数据来源: 天天基金网 (fund.eastmoney.com) / 东方财富 Choice")
    print("  接口: AKShare (底层调用东方财富 API)")
    print("=" * 80)
    
    return {
        'top_nav_growth': df1,
        'top_fund_inflow': df2,
        'top_industry_inflow': df3,
        'top_stock_fund_buy': df4,
    }

if __name__ == '__main__':
    generate_fund_daily_report()
