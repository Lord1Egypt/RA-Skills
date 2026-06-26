#!/usr/bin/env python3
"""
财务数据获取模块

从 Tushare API 获取上市公司财务数据，支持多年度历史数据获取
"""

import os
import pandas as pd
import tushare as ts
from typing import Optional, Dict, List
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FinancialDataFetcher:
    """财务数据获取器"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化数据获取器

        Args:
            token: Tushare Token，默认从环境变量读取
        """
        self.token = token or os.getenv('TUSHARE_TOKEN')
        if not self.token:
            raise ValueError(
                "未找到 Tushare Token。请设置环境变量 TUSHARE_TOKEN。\n"
                "获取 Token: https://tushare.pro"
            )
        
        self.pro = ts.pro_api(self.token)
        logger.info("✅ Tushare API 初始化成功")

    def fetch_all_financial_data(
        self,
        ts_code: str,
        years: int = 10,
        report_type: str = '1'  # '1' = 年报
    ) -> Dict[str, pd.DataFrame]:
        """
        获取完整的财务数据集

        Args:
            ts_code: 股票代码 (如 '000001.SZ')
            years: 获取历史年数
            report_type: 报告类型 ('1'年报, '2'中报, '3'季报, '4'季报)

        Returns:
            Dict: 包含资产负债表、利润表、现金流量表、财务指标等
        """
        logger.info(f"📊 开始获取 {ts_code} 财务数据，历史 {years} 年...")
        
        # 计算日期范围
        current_year = datetime.now().year
        start_date = f"{(current_year - years)}1231"
        end_date = f"{current_year}1231"
        
        result = {}
        
        # 1. 获取资产负债表
        logger.info("  [1/6] 获取资产负债表...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                balance = self.pro.balancesheet(
                    ts_code=ts_code,
                    start_date=start_date,
                    end_date=end_date,
                    report_type=report_type
                )
                if not balance.empty:
                    balance = balance.sort_values('end_date', ascending=True)
                    result['balance'] = balance
                    logger.info(f"       ✅ 资产负债表: {len(balance)} 条记录")
                else:
                    logger.warning(f"       ⚠️ 资产负债表: 无数据")
                    result['balance'] = pd.DataFrame()
                break  # 成功则退出重试循环
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"       ⚠️ 资产负债表获取失败 (尝试 {attempt+1}/{max_retries}): {e}")
                    time.sleep(1)  # 等待1秒后重试
                else:
                    logger.error(f"       ❌ 资产负债表获取失败 (已重试{max_retries}次): {e}")
                    result['balance'] = pd.DataFrame()
        
        time.sleep(0.3)  # API频率限制
        
        # 2. 获取利润表
        logger.info("  [2/6] 获取利润表...")
        try:
            income = self.pro.income(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                report_type=report_type
            )
            if not income.empty:
                income = income.sort_values('end_date', ascending=True)
                result['income'] = income
                logger.info(f"       ✅ 利润表: {len(income)} 条记录")
            else:
                logger.warning(f"       ⚠️ 利润表: 无数据")
                result['income'] = pd.DataFrame()
        except Exception as e:
            logger.error(f"       ❌ 利润表获取失败: {e}")
            result['income'] = pd.DataFrame()
        
        time.sleep(0.3)
        
        # 3. 获取现金流量表
        logger.info("  [3/6] 获取现金流量表...")
        try:
            cashflow = self.pro.cashflow(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                report_type=report_type
            )
            if not cashflow.empty:
                cashflow = cashflow.sort_values('end_date', ascending=True)
                result['cashflow'] = cashflow
                logger.info(f"       ✅ 现金流量表: {len(cashflow)} 条记录")
            else:
                logger.warning(f"       ⚠️ 现金流量表: 无数据")
                result['cashflow'] = pd.DataFrame()
        except Exception as e:
            logger.error(f"       ❌ 现金流量表获取失败: {e}")
            result['cashflow'] = pd.DataFrame()
        
        time.sleep(0.3)
        
        # 4. 获取财务指标
        logger.info("  [4/6] 获取财务指标...")
        try:
            fina_indicator = self.pro.fina_indicator(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            if not fina_indicator.empty:
                fina_indicator = fina_indicator.sort_values('end_date', ascending=True)
                result['fina_indicator'] = fina_indicator
                logger.info(f"       ✅ 财务指标: {len(fina_indicator)} 条记录")
            else:
                logger.warning(f"       ⚠️ 财务指标: 无数据")
                result['fina_indicator'] = pd.DataFrame()
        except Exception as e:
            logger.error(f"       ❌ 财务指标获取失败: {e}")
            result['fina_indicator'] = pd.DataFrame()
        
        time.sleep(0.3)
        
        # 5. 获取公司基本信息
        logger.info("  [5/6] 获取公司基本信息...")
        try:
            stock_basic = self.pro.stock_basic(
                ts_code=ts_code,
                fields='ts_code,name,area,industry,market,list_date,is_hs,st_status'
            )
            if not stock_basic.empty:
                result['stock_info'] = stock_basic.iloc[0].to_dict()
                logger.info(f"       ✅ 公司信息: {result['stock_info'].get('name', 'N/A')}")
            else:
                logger.warning(f"       ⚠️ 公司信息: 无数据")
                result['stock_info'] = {}
        except Exception as e:
            logger.error(f"       ❌ 公司信息获取失败: {e}")
            result['stock_info'] = {}
        
        time.sleep(0.3)
        
        # 6. 获取审计意见
        logger.info("  [6/6] 获取审计意见...")
        try:
            audit = self.pro.fina_audit(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            if not audit.empty:
                audit = audit.sort_values('end_date', ascending=True)
                result['audit'] = audit
                logger.info(f"       ✅ 审计意见: {len(audit)} 条记录")
            else:
                logger.warning(f"       ⚠️ 审计意见: 无数据")
                result['audit'] = pd.DataFrame()
        except Exception as e:
            logger.error(f"       ❌ 审计意见获取失败: {e}")
            result['audit'] = pd.DataFrame()
        
        # 数据完整性统计
        total_records = sum(len(df) for df in result.values() if isinstance(df, pd.DataFrame))
        logger.info(f"📊 数据获取完成: 共 {total_records} 条记录")
        
        return result

    def get_industry_peers(
        self,
        ts_code: str,
        industry: Optional[str] = None
    ) -> List[str]:
        """
        获取同行业可比公司

        Args:
            ts_code: 目标公司代码
            industry: 行业代码（如未提供则从公司信息获取）

        Returns:
            List: 同行业公司代码列表
        """
        logger.info(f"🔍 获取 {ts_code} 同行业可比公司...")
        
        # 获取行业分类
        if not industry:
            try:
                classify = self.pro.index_classify(src='SW2021')
                # 尝试获取申万行业分类
                industry_info = self.pro.stock_basic(ts_code=ts_code, fields='industry')
                if not industry_info.empty:
                    industry = industry_info.iloc[0]['industry']
                    logger.info(f"   目标公司行业: {industry}")
            except Exception as e:
                logger.warning(f"   获取行业分类失败: {e}")
                return []
        
        if not industry:
            logger.warning("   无法确定行业分类，跳过同行获取")
            return []
        
        # 获取同行业公司
        try:
            peers = self.pro.stock_basic(
                industry=industry,
                fields='ts_code,name',
                list_status='L'  # 仅上市公司
            )
            
            if peers.empty:
                logger.warning(f"   未找到同行业公司")
                return []
            
            peer_codes = peers['ts_code'].tolist()
            peer_codes.remove(ts_code)  # 移除目标公司
            
            logger.info(f"   ✅ 找到 {len(peer_codes)} 家同行业公司")
            
            # 限制数量（避免API过多调用）
            return peer_codes[:20]  # 最多20家
            
        except Exception as e:
            logger.error(f"   ❌ 同行业获取失败: {e}")
            return []

    def fetch_peer_financial_indicator(
        self,
        peer_codes: List[str],
        year: str
    ) -> pd.DataFrame:
        """
        获取同行业公司财务指标（用于行业对比）

        Args:
            peer_codes: 同行业公司代码列表
            year: 年份（如 '2025'）

        Returns:
            pd.DataFrame: 同行业财务指标汇总
        """
        logger.info(f"📊 获取同行业财务指标 ({year}年)...")
        
        end_date = f"{year}1231"
        start_date = f"{year}0101"
        
        peer_data = []
        
        for i, code in enumerate(peer_codes):
            logger.info(f"   进度: {i+1}/{len(peer_codes)} - {code}")
            
            try:
                df = self.pro.fina_indicator(
                    ts_code=code,
                    start_date=start_date,
                    end_date=end_date
                )
                
                if not df.empty:
                    # 取最新年报数据
                    latest = df[df['ann_date'] == df['ann_date'].max()]
                    if not latest.empty:
                        peer_data.append(latest.iloc[0])
                
                time.sleep(0.2)  # API频率限制
                
            except Exception as e:
                logger.warning(f"   {code} 获取失败: {e}")
                continue
        
        if peer_data:
            result = pd.DataFrame(peer_data)
            logger.info(f"   ✅ 成功获取 {len(result)} 家同行数据")
            return result
        else:
            logger.warning("   ⚠️ 未获取到任何同行数据")
            return pd.DataFrame()

    def get_announcements(
        self,
        ts_code: str,
        start_date: str,
        end_date: str,
        keywords: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        获取公司公告（用于交叉验证）

        Args:
            ts_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            keywords: 关键词过滤（如 ['财务', '审计', '违规']）

        Returns:
            pd.DataFrame: 公告列表
        """
        logger.info(f"📰 获取公司公告...")
        
        try:
            ann = self.pro.news_content(
                ts_code=ts_code,
                start_date=start_date.replace('-', ''),
                end_date=end_date.replace('-', ''),
                fields='ts_code,ann_date,title,content'
            )
            
            if ann.empty:
                logger.warning("   ⚠️ 未找到公告")
                return pd.DataFrame()
            
            # 关键词过滤
            if keywords:
                mask = ann['title'].str.contains('|'.join(keywords), case=False, na=False)
                if 'content' in ann.columns:
                    mask |= ann['content'].str.contains('|'.join(keywords), case=False, na=False)
                ann = ann[mask]
            
            logger.info(f"   ✅ 找到 {len(ann)} 条相关公告")
            return ann
            
        except Exception as e:
            logger.error(f"   ❌ 公告获取失败: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    # 测试用例
    fetcher = FinancialDataFetcher()
    
    # 测试获取完整数据
    data = fetcher.fetch_all_financial_data('000001.SZ', years=5)
    
    print("\n=== 数据获取测试结果 ===")
    for key, value in data.items():
        if isinstance(value, pd.DataFrame):
            print(f"{key}: {len(value)} 条记录")
        elif isinstance(value, dict):
            print(f"{key}: {value.get('name', 'N/A')}")