import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_stock_review(stock_code, days=365):
    """
    生成股票复盘报告（使用备用接口）
    :param stock_code: 股票代码
    :param days: 分析天数，默认近一年
    :return: 复盘报告文本
    """
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
    
    report = []
    report.append("=" * 50)
    report.append(f"📊 股票复盘报告：{stock_code}")
    report.append(f"📅 分析时间段：{start_date} 至 {end_date}")
    report.append("=" * 50)
    
    # 1. 行情走势分析
    report.append("\n📈 一、行情走势分析")
    report.append("-" * 30)
    try:
        kline_data = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        if not kline_data.empty:
            latest = kline_data.iloc[-1]
            report.append(f"最新收盘价：{latest['收盘']:.2f} 元")
            report.append(f"今日涨跌幅：{latest['涨跌幅']:.2f}%")
            report.append(f"今日成交量：{latest['成交量']:,} 手")
            report.append(f"今日成交额：{latest['成交额']/10000:.2f} 万元")
            report.append(f"近{days}天最高价：{kline_data['最高'].max():.2f} 元")
            report.append(f"近{days}天最低价：{kline_data['最低'].min():.2f} 元")
            report.append(f"近{days}天累计涨跌幅：{((latest['收盘']/kline_data.iloc[0]['收盘'])-1)*100:.2f}%")
            
            # 计算均线
            kline_data['MA5'] = kline_data['收盘'].rolling(5).mean()
            kline_data['MA10'] = kline_data['收盘'].rolling(10).mean()
            kline_data['MA20'] = kline_data['收盘'].rolling(20).mean()
            kline_data['MA60'] = kline_data['收盘'].rolling(60).mean()
            
            latest_ma = kline_data.iloc[-1]
            report.append(f"\n均线系统：")
            report.append(f"MA5：{latest_ma['MA5']:.2f} 元")
            report.append(f"MA10：{latest_ma['MA10']:.2f} 元")
            report.append(f"MA20：{latest_ma['MA20']:.2f} 元")
            report.append(f"MA60：{latest_ma['MA60']:.2f} 元")
            
            # 判断均线走势
            if latest_ma['MA5'] > latest_ma['MA10'] > latest_ma['MA20']:
                report.append("均线形态：多头排列，趋势向上")
            elif latest_ma['MA5'] < latest_ma['MA10'] < latest_ma['MA20']:
                report.append("均线形态：空头排列，趋势向下")
            else:
                report.append("均线形态：震荡整理，方向不明")
        else:
            report.append("❌ 行情数据获取失败")
    except Exception as e:
        report.append(f"❌ 行情数据获取失败：{str(e)}")
    
    # 2. 实时行情补充
    report.append("\n📊 二、实时行情补充")
    report.append("-" * 30)
    try:
        spot_data = ak.stock_zh_a_spot_em()
        stock_data = spot_data[spot_data['代码'] == stock_code]
        if not stock_data.empty:
            stock_info = stock_data.iloc[0]
            report.append(f"股票名称：{stock_info['名称']}")
            report.append(f"最新价：{stock_info['最新价']} 元")
            report.append(f"涨跌幅：{stock_info['涨跌幅']}%")
            report.append(f"涨跌额：{stock_info['涨跌额']} 元")
            report.append(f"换手率：{stock_info['换手率']}%")
            report.append(f"量比：{stock_info['量比']}")
            report.append(f"市盈率：{stock_info['市盈率-动态']}")
            report.append(f"市净率：{stock_info['市净率']}")
            report.append(f"总市值：{stock_info['总市值']/100000000:.2f} 亿元")
            report.append(f"流通市值：{stock_info['流通市值']/100000000:.2f} 亿元")
        else:
            report.append("❌ 实时行情获取失败")
    except Exception as e:
        report.append(f"❌ 实时行情获取失败：{str(e)}")
    
    # 3. 板块与概念（内置数据库）
    report.append("\n🏷️ 三、板块与概念")
    report.append("-" * 30)
    concept_db = {
        # 农业板块
        "600313": {"name": "农发种业", "industry": "种植业与林业", "concepts": ["农垦改革", "乡村振兴", "农业种植", "国企改革", "土地流转"]},
        "000998": {"name": "隆平高科", "industry": "种植业与林业", "concepts": ["种业", "乡村振兴", "粮食安全", "转基因", "央企国资改革"]},
        "002041": {"name": "登海种业", "industry": "种植业与林业", "concepts": ["种业", "转基因", "农业种植", "乡村振兴", "融资融券"]},
        "600598": {"name": "北大荒", "industry": "种植业与林业", "concepts": ["大豆", "乡村振兴", "农业种植", "土地流转", "黑龙江自贸区"]},
        "300189": {"name": "神农科技", "industry": "种植业与林业", "concepts": ["种业", "转基因", "乡村振兴", "粮食安全", "海南自贸区"]},
        "603366": {"name": "日出东方", "industry": "家用电器", "concepts": ["太阳能", "空气能", "区块链", "储能", "光伏"]},
        # 电机板块
        "300660": {"name": "江苏雷利", "industry": "电力设备", "concepts": ["电机", "新能源汽车", "机器人", "光伏", "储能", "智能家居"]},
        "002176": {"name": "江特电机", "industry": "电力设备", "concepts": ["电机", "新能源汽车", "锂电池", "风电", "军工"]},
        "600580": {"name": "卧龙电驱", "industry": "电力设备", "concepts": ["电机", "新能源汽车", "机器人", "高铁", "工业4.0"]},
        # 新能源
        "002594": {"name": "比亚迪", "industry": "汽车", "concepts": ["新能源汽车", "动力电池", "半导体", "储能", "整车"]},
        "300750": {"name": "宁德时代", "industry": "电力设备", "concepts": ["动力电池", "储能", "新能源汽车", "锂电池", "钠电池"]},
        # 消费
        "600519": {"name": "贵州茅台", "industry": "食品饮料", "concepts": ["白酒", "消费龙头", "MSCI概念", "沪股通", "融资融券"]},
        "000858": {"name": "五粮液", "industry": "食品饮料", "concepts": ["白酒", "消费龙头", "MSCI概念", "深股通", "融资融券"]},
        # 金融
        "600036": {"name": "招商银行", "industry": "银行", "concepts": ["银行龙头", "MSCI概念", "沪股通", "融资融券", "富时罗素概念"]},
        "000001": {"name": "平安银行", "industry": "银行", "concepts": ["银行", "MSCI概念", "深股通", "融资融券", "富时罗素概念"]},
    }
    
    if stock_code in concept_db:
        info = concept_db[stock_code]
        report.append(f"股票名称：{info['name']}")
        report.append(f"所属行业：{info['industry']}")
        report.append(f"涉及概念：{'、'.join(info['concepts'])}")
    else:
        report.append("股票信息：暂无内置数据，可补充到概念数据库")
    
    # 4. 综合分析
    report.append("\n🔍 四、综合分析")
    report.append("-" * 30)
    try:
        trend_score = 0
        # 均线趋势
        if '均线形态' in str(report):
            for line in report:
                if '多头排列' in line:
                    trend_score += 2
                elif '空头排列' in line:
                    trend_score -= 2
                break
        
        # 涨跌幅
        if '今日涨跌幅' in str(report):
            for line in report:
                if '今日涨跌幅' in line:
                    change = float(line.split('：')[1].replace('%', '').strip())
                    if change > 3:
                        trend_score += 1
                    elif change < -3:
                        trend_score -= 1
                    break
        
        # 量比
        if '量比' in str(report):
            for line in report:
                if '量比' in line:
                    ratio = float(line.split('：')[1].strip())
                    if ratio > 2:
                        trend_score += 1
                    elif ratio < 0.5:
                        trend_score -= 1
                    break
        
        # 市盈率
        if '市盈率' in str(report):
            for line in report:
                if '市盈率-动态' in line:
                    pe = line.split('：')[1].strip()
                    if pe != '-' and float(pe) < 20:
                        trend_score += 1
                    elif pe != '-' and float(pe) > 100:
                        trend_score -= 1
                    break
        
        if trend_score >= 3:
            report.append("综合评级：✅ 看好，趋势向好，可适当关注")
        elif trend_score >= 0:
            report.append("综合评级：⚪ 中性，震荡整理，观望为主")
        else:
            report.append("综合评级：⚠️ 谨慎，趋势偏弱，注意风险")
    except Exception as e:
        report.append(f"综合评级：数据不足，无法判断")
    
    # 免责声明
    report.append("\n" + "=" * 50)
    report.append("⚠️ 免责声明：本报告仅供参考，不构成任何投资建议。")
    report.append("   股市有风险，投资需谨慎。")
    report.append("=" * 50)
    
    return '\n'.join(report)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python review.py <股票代码> [分析天数]")
        print("示例：python review.py 600313 365")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 365
    
    report = get_stock_review(stock_code, days)
    print(report)
