#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
quant-aio 选股引擎
多因子选股系统 - 基本面 + 技术面 + 资金面

© 2026 SimonsTang / 上海巧未来人工智能科技有限公司 版权所有
开源协议：MIT License
源码开放，欢迎完善，共同进步
GitHub: https://github.com/simonstang/bolong-quant
"""

import os
import sys
import json
import yaml
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import argparse

import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DataFetcher:
    """数据获取器 - 支持tushare/akshare"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.primary = config['data']['primary']
        self.fallback = config['data']['fallback']
        
        # 初始化tushare
        if self.primary == 'tushare' or self.fallback == 'tushare':
            try:
                import tushare as ts
                token = os.getenv('TUSHARE_TOKEN')
                if not token:
                    raise ValueError("TUSHARE_TOKEN 环境变量未设置")
                self.ts = ts.pro_api(token)
                logger.info("✅ tushare 连接成功")
            except Exception as e:
                logger.warning(f"⚠️ tushare 初始化失败: {e}")
                self.ts = None
        
        # 初始化akshare
        if self.primary == 'akshare' or self.fallback == 'akshare':
            try:
                import akshare as ak
                self.ak = ak
                logger.info("✅ akshare 连接成功")
            except Exception as e:
                logger.warning(f"⚠️ akshare 初始化失败: {e}")
                self.ak = None

    def get_stock_list(self) -> pd.DataFrame:
        """获取A股股票列表"""
        # 先尝试tushare
        try:
            if self.ts:
                df = self.ts.stock_basic(exchange='', list_status='L')
                if df is not None and not df.empty:
                    return df[['ts_code', 'name', 'market', 'list_date']]
        except Exception as e:
            logger.warning(f"tushare获取股票列表失败: {e}")
        
        # akshare备用
        try:
            if self.ak:
                import akshare as ak
                logger.info("使用akshare获取股票列表...")
                df = ak.stock_info_a_code_name()
                if df is not None and not df.empty:
                    df = df.rename(columns={'code': 'ts_code', 'name': 'name'})
                    df['market'] = 'A股'
                    df['list_date'] = ''
                    return df
        except Exception as e:
            logger.warning(f"akshare获取股票列表失败: {e}")
        
        return pd.DataFrame()

    def get_daily_basic(self, ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取日线基础数据"""
        try:
            if self.ts:
                df = self.ts.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date)
                return df
        except Exception as e:
            logger.debug(f"获取 {ts_code} 日线数据失败: {e}")
        return pd.DataFrame()

    def get_fina_indicator(self, ts_code: str) -> pd.DataFrame:
        """获取财务指标"""
        try:
            if self.ts:
                df = self.ts.fina_indicator(ts_code=ts_code, fields='ts_code,ann_date,roe,gross_margin,net_margin')
                return df.sort_values('ann_date', ascending=False).head(1)
        except Exception as e:
            logger.debug(f"获取 {ts_code} 财务指标失败: {e}")
        return pd.DataFrame()

    def get_income(self, ts_code: str) -> pd.DataFrame:
        """获取收入数据"""
        try:
            if self.ts:
                df = self.ts.income(ts_code=ts_code, fields='ts_code,ann_date,revenue,n_income')
                return df.sort_values('ann_date', ascending=False).head(2)
        except Exception as e:
            logger.debug(f"获取 {ts_code} 收入数据失败: {e}")
        return pd.DataFrame()

    def get_north_money(self) -> pd.DataFrame:
        """获取北向资金数据"""
        try:
            if self.ts:
                df = self.ts.moneyflow_hsgt(start_date=(datetime.now() - timedelta(days=10)).strftime('%Y%m%d'))
                return df
        except Exception as e:
            logger.debug(f"获取北向资金失败: {e}")
        return pd.DataFrame()


class FactorCalculator:
    """因子计算器"""
    
    def __init__(self, config: Dict, factors_config: Dict):
        self.config = config
        self.factors_config = factors_config
        self.weights = factors_config['weights']

    def calculate_fundamentals_score(self, stock_data: Dict) -> float:
        """计算基本面得分"""
        score = 0
        weight_sum = 0
        
        factors = self.factors_config['fundamentals']
        
        # PE估值
        if 'pe' in stock_data and stock_data['pe'] > 0:
            pe = stock_data['pe']
            pe_config = factors['valuation']['pe']
            if pe_config['min'] <= pe <= pe_config['max']:
                pe_score = (pe_config['max'] - pe) / (pe_config['max'] - pe_config['min'])
                score += pe_score * pe_config['weight']
                weight_sum += pe_config['weight']
        
        # ROE盈利能力
        if 'roe' in stock_data and stock_data['roe'] > 0:
            roe = stock_data['roe']
            roe_config = factors['profitability']['roe']
            if roe >= roe_config['min']:
                roe_score = min(roe / 30, 1.0)  # 归一化到0-1
                score += roe_score * roe_config['weight']
                weight_sum += roe_config['weight']
        
        # 营收增速
        if 'revenue_growth' in stock_data and stock_data['revenue_growth'] > 0:
            growth = stock_data['revenue_growth']
            growth_config = factors['growth']['revenue_growth_yoy']
            if growth >= growth_config['min']:
                growth_score = min(growth / 50, 1.0)  # 归一化
                score += growth_score * growth_config['weight']
                weight_sum += growth_config['weight']
        
        if weight_sum > 0:
            return (score / weight_sum) * 100
        return 0

    def calculate_technical_score(self, stock_data: Dict) -> float:
        """计算技术面得分"""
        score = 0
        weight_sum = 0
        
        factors = self.factors_config['technical']
        
        # 价格在20日均线上方
        if 'price_above_ma20' in stock_data and stock_data['price_above_ma20']:
            score += factors['trend']['ma20_above']['weight']
            weight_sum += factors['trend']['ma20_above']['weight']
        
        # RSI指标
        if 'rsi' in stock_data:
            rsi = stock_data['rsi']
            rsi_config = factors['momentum']['rsi']
            if rsi_config['min'] <= rsi <= rsi_config['max']:
                rsi_score = 1.0 - abs(rsi - 50) / 50  # 越接近50越好
                score += rsi_score * rsi_config['weight']
                weight_sum += rsi_config['weight']
        
        # 量比
        if 'volume_ratio' in stock_data and stock_data['volume_ratio'] > 0:
            vol_ratio = stock_data['volume_ratio']
            vol_config = factors['volume']['volume_ratio']
            if vol_ratio >= vol_config['min']:
                vol_score = min(vol_ratio / 3, 1.0)  # 归一化
                score += vol_score * vol_config['weight']
                weight_sum += vol_config['weight']
        
        if weight_sum > 0:
            return (score / weight_sum) * 100
        return 0

    def calculate_sentiment_score(self, stock_data: Dict) -> float:
        """计算资金面得分"""
        score = 0
        weight_sum = 0
        
        factors = self.factors_config['sentiment']
        
        # 北向资金
        if 'north_money_3d' in stock_data and stock_data['north_money_3d'] > 0:
            score += factors['north_money']['net_inflow_3d']['weight']
            weight_sum += factors['north_money']['net_inflow_3d']['weight']
        
        if weight_sum > 0:
            return (score / weight_sum) * 100
        return 0

    def calculate_total_score(self, stock_data: Dict) -> float:
        """计算综合得分"""
        fund_score = self.calculate_fundamentals_score(stock_data)
        tech_score = self.calculate_technical_score(stock_data)
        sent_score = self.calculate_sentiment_score(stock_data)
        
        total = (
            fund_score * self.weights['fundamentals'] +
            tech_score * self.weights['technical'] +
            sent_score * self.weights['sentiment']
        )
        
        return total


class StockPicker:
    """选股主类"""
    
    def __init__(self, config_path: str = 'config/config.yaml', factors_path: str = 'config/factors.yaml'):
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        with open(factors_path, 'r', encoding='utf-8') as f:
            self.factors_config = yaml.safe_load(f)
        
        # 初始化组件
        self.fetcher = DataFetcher(self.config)
        self.calculator = FactorCalculator(self.config, self.factors_config)
        
        # 创建输出目录
        Path(self.config['stock_picker']['output_dir']).mkdir(parents=True, exist_ok=True)

    def pick_stocks(self, strategy: str = 'momentum', top_n: int = 20) -> pd.DataFrame:
        """执行选股"""
        logger.info(f"🚀 开始选股 - 策略: {strategy}, TOP: {top_n}")
        
        # 获取股票列表
        stocks = self.fetcher.get_stock_list()
        if stocks.empty:
            logger.error("❌ 无法获取股票列表")
            return pd.DataFrame()
        
        logger.info(f"📊 获取 {len(stocks)} 只股票")
        
        # 计算每只股票的得分
        results = []
        for idx, row in stocks.iterrows():
            ts_code = row['ts_code']
            
            # 模拟数据（实际应从数据源获取）
            stock_data = {
                'ts_code': ts_code,
                'name': row['name'],
                'pe': np.random.uniform(10, 50),
                'roe': np.random.uniform(5, 30),
                'revenue_growth': np.random.uniform(0, 50),
                'rsi': np.random.uniform(30, 70),
                'volume_ratio': np.random.uniform(0.5, 3),
                'price_above_ma20': np.random.choice([True, False]),
                'north_money_3d': np.random.uniform(-1000, 5000),
            }
            
            # 计算得分
            total_score = self.calculator.calculate_total_score(stock_data)
            
            results.append({
                'ts_code': ts_code,
                'name': row['name'],
                'score': total_score,
                'pe': stock_data['pe'],
                'roe': stock_data['roe'],
                'revenue_growth': stock_data['revenue_growth'],
                'rsi': stock_data['rsi'],
                'volume_ratio': stock_data['volume_ratio'],
            })
            
            if (idx + 1) % 100 == 0:
                logger.info(f"⏳ 已处理 {idx + 1}/{len(stocks)} 只股票")
        
        # 排序并取TOP N
        df_results = pd.DataFrame(results)
        df_results = df_results.sort_values('score', ascending=False).head(top_n)
        
        logger.info(f"✅ 选股完成，TOP {top_n} 结果:")
        logger.info(f"\n{df_results.to_string()}")
        
        return df_results

    def save_results(self, df: pd.DataFrame, strategy: str = 'momentum'):
        """保存选股结果"""
        if df.empty:
            logger.warning("⚠️ 无结果可保存")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"{self.config['stock_picker']['output_dir']}/picks_{strategy}_{timestamp}.csv"
        
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"💾 结果已保存: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='quant-aio 选股引擎')
    parser.add_argument('--strategy', default='momentum', help='选股策略: momentum/value/growth/break_through')
    parser.add_argument('--top', type=int, default=20, help='输出TOP N只股票')
    parser.add_argument('--config', default='config/config.yaml', help='配置文件路径')
    parser.add_argument('--factors', default='config/factors.yaml', help='因子配置文件路径')
    
    args = parser.parse_args()
    
    try:
        picker = StockPicker(args.config, args.factors)
        results = picker.pick_stocks(strategy=args.strategy, top_n=args.top)
        picker.save_results(results, strategy=args.strategy)
        
        logger.info("🎉 选股完成！")
        
    except Exception as e:
        logger.error(f"❌ 选股失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
