#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据持久化模块

使用 SQLite 存储历史新闻和分析结果，支持趋势分析

用法:
    python database.py init              # 初始化数据库
    python database.py show-stats        # 显示统计数据
    python database.py export --format csv  # 导出数据
"""

import sqlite3
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class FinanceNewsDB:
    """财经新闻数据库"""
    
    def __init__(self, db_path: str = "finance_news.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 新闻表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source TEXT,
            publish_time TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 情感分析结果表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news_id INTEGER,
            sentiment TEXT,  -- positive/negative/neutral
            sentiment_score INTEGER,  -- 0-100
            confidence TEXT,  -- high/medium/low
            sentiment_label TEXT,  -- 🟢/🔴/⚪
            reasoning TEXT,
            timeframe TEXT,  -- short/medium/long
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (news_id) REFERENCES news(id)
        )
        """)
        
        # 影响评估表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS impact_assessment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER,
            sector TEXT,
            ticker TEXT,
            impact TEXT,  -- positive/negative/neutral
            magnitude TEXT,  -- high/medium/low
            FOREIGN KEY (analysis_id) REFERENCES sentiment_analysis(id)
        )
        """)
        
        # 关键信息表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS key_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER,
            point_type TEXT,  -- company/person/location/event
            content TEXT,
            FOREIGN KEY (analysis_id) REFERENCES sentiment_analysis(id)
        )
        """)
        
        # 简报表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS briefings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            briefing_type TEXT,  -- brief/full/industry/stock
            period TEXT,  -- daily/weekly/monthly
            content TEXT,
            total_news INTEGER,
            positive_count INTEGER,
            negative_count INTEGER,
            neutral_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_url ON news(url)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_time ON news(publish_time)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment ON sentiment_analysis(sentiment)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment_time ON sentiment_analysis(analyzed_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_impact_ticker ON impact_assessment(ticker)")
        
        conn.commit()
        conn.close()
        print(f"✅ 数据库初始化完成：{self.db_path}")
    
    def insert_news(self, news_items: List[Dict[str, Any]]) -> List[int]:
        """插入新闻列表，返回新闻 ID 列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        news_ids = []
        for item in news_items:
            try:
                cursor.execute("""
                INSERT OR IGNORE INTO news (title, url, source, publish_time, summary)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    item.get('title', ''),
                    item.get('url', ''),
                    item.get('source', ''),
                    item.get('time', ''),
                    item.get('summary', '')
                ))
                
                # 获取新闻 ID
                cursor.execute("SELECT id FROM news WHERE url = ?", (item.get('url', ''),))
                result = cursor.fetchone()
                if result:
                    news_ids.append(result[0])
            except Exception as e:
                print(f"插入新闻失败：{e}")
        
        conn.commit()
        conn.close()
        return news_ids
    
    def insert_sentiment_analysis(self, news_id: int, analysis: Dict[str, Any]) -> int:
        """插入情感分析结果，返回分析 ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO sentiment_analysis 
        (news_id, sentiment, sentiment_score, confidence, sentiment_label, reasoning, timeframe)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            news_id,
            analysis.get('sentiment', 'neutral'),
            analysis.get('sentiment_score', 50),
            analysis.get('confidence', 'medium'),
            analysis.get('sentiment_label', '⚪'),
            analysis.get('reasoning', ''),
            analysis.get('timeframe', 'short')
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return analysis_id
    
    def insert_impact_assessment(self, analysis_id: int, impacts: List[Dict[str, str]]):
        """插入影响评估"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for impact in impacts:
            cursor.execute("""
            INSERT INTO impact_assessment (analysis_id, sector, ticker, impact, magnitude)
            VALUES (?, ?, ?, ?, ?)
            """, (
                analysis_id,
                impact.get('sector', ''),
                impact.get('ticker', ''),
                impact.get('impact', 'neutral'),
                impact.get('magnitude', 'medium')
            ))
        
        conn.commit()
        conn.close()
    
    def insert_key_points(self, analysis_id: int, points: List[str], point_type: str = 'general'):
        """插入关键信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for point in points:
            cursor.execute("""
            INSERT INTO key_points (analysis_id, point_type, content)
            VALUES (?, ?, ?)
            """, (analysis_id, point_type, point))
        
        conn.commit()
        conn.close()
    
    def save_briefing(self, briefing_type: str, period: str, content: str, 
                      total: int, positive: int, negative: int, neutral: int):
        """保存简报"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO briefings (briefing_type, period, content, total_news, positive_count, negative_count, neutral_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (briefing_type, period, content, total, positive, negative, neutral))
        
        conn.commit()
        conn.close()
    
    def get_sentiment_trend(self, days: int = 30) -> List[Dict[str, Any]]:
        """获取情感趋势（最近 N 天）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute("""
        SELECT 
            DATE(analyzed_at) as date,
            sentiment,
            COUNT(*) as count,
            AVG(sentiment_score) as avg_score
        FROM sentiment_analysis
        WHERE analyzed_at >= ?
        GROUP BY DATE(analyzed_at), sentiment
        ORDER BY date
        """, (cutoff_date,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'date': row[0],
                'sentiment': row[1],
                'count': row[2],
                'avg_score': row[3]
            })
        
        conn.close()
        return results
    
    def get_stock_sentiment(self, ticker: str, days: int = 30) -> List[Dict[str, Any]]:
        """获取特定股票的情感趋势"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute("""
        SELECT 
            DATE(sa.analyzed_at) as date,
            sa.sentiment,
            sa.sentiment_score,
            sa.confidence,
            n.title,
            n.url
        FROM sentiment_analysis sa
        JOIN impact_assessment ia ON sa.id = ia.analysis_id
        JOIN news n ON sa.news_id = n.id
        WHERE ia.ticker = ? AND sa.analyzed_at >= ?
        ORDER BY sa.analyzed_at DESC
        """, (ticker, cutoff_date))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'date': row[0],
                'sentiment': row[1],
                'score': row[2],
                'confidence': row[3],
                'title': row[4],
                'url': row[5]
            })
        
        conn.close()
        return results
    
    def get_industry_summary(self, days: int = 7) -> Dict[str, Any]:
        """获取行业摘要（最近 N 天）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute("""
        SELECT 
            ia.sector,
            COUNT(*) as news_count,
            SUM(CASE WHEN ia.impact = 'positive' THEN 1 ELSE 0 END) as positive_count,
            SUM(CASE WHEN ia.impact = 'negative' THEN 1 ELSE 0 END) as negative_count,
            SUM(CASE WHEN ia.impact = 'neutral' THEN 1 ELSE 0 END) as neutral_count
        FROM impact_assessment ia
        JOIN sentiment_analysis sa ON ia.analysis_id = sa.id
        WHERE sa.analyzed_at >= ? AND ia.sector != ''
        GROUP BY ia.sector
        ORDER BY news_count DESC
        """, (cutoff_date,))
        
        results = {}
        for row in cursor.fetchall():
            results[row[0]] = {
                'total': row[1],
                'positive': row[2],
                'negative': row[3],
                'neutral': row[4]
            }
        
        conn.close()
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # 新闻总数
        cursor.execute("SELECT COUNT(*) FROM news")
        stats['total_news'] = cursor.fetchone()[0]
        
        # 分析总数
        cursor.execute("SELECT COUNT(*) FROM sentiment_analysis")
        stats['total_analysis'] = cursor.fetchone()[0]
        
        # 情感分布
        cursor.execute("""
        SELECT sentiment, COUNT(*) 
        FROM sentiment_analysis 
        GROUP BY sentiment
        """)
        stats['sentiment_distribution'] = {
            row[0]: row[1] for row in cursor.fetchall()
        }
        
        # 简报总数
        cursor.execute("SELECT COUNT(*) FROM briefings")
        stats['total_briefings'] = cursor.fetchone()[0]
        
        # 最近分析时间
        cursor.execute("SELECT MAX(analyzed_at) FROM sentiment_analysis")
        stats['last_analysis'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def export_data(self, format: str = 'csv', output_file: str = 'export_data'):
        """导出数据"""
        conn = sqlite3.connect(self.db_path)
        
        if format == 'csv':
            import csv
            
            # 导出新闻
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM news")
            
            with open(f'{output_file}_news.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'title', 'url', 'source', 'publish_time', 'summary', 'created_at'])
                writer.writerows(cursor.fetchall())
            
            # 导出情感分析
            cursor.execute("""
            SELECT sa.id, n.title, sa.sentiment, sa.sentiment_score, sa.confidence, sa.reasoning, sa.analyzed_at
            FROM sentiment_analysis sa
            JOIN news n ON sa.news_id = n.id
            """)
            
            with open(f'{output_file}_sentiment.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'title', 'sentiment', 'score', 'confidence', 'reasoning', 'analyzed_at'])
                writer.writerows(cursor.fetchall())
            
            print(f"✅ 数据已导出到 {output_file}_*.csv")
        
        elif format == 'json':
            cursor = conn.cursor()
            
            # 导出完整数据
            cursor.execute("""
            SELECT n.title, n.url, n.source, n.publish_time, 
                   sa.sentiment, sa.sentiment_score, sa.confidence, sa.reasoning
            FROM news n
            JOIN sentiment_analysis sa ON n.id = sa.news_id
            ORDER BY sa.analyzed_at DESC
            LIMIT 1000
            """)
            
            data = []
            for row in cursor.fetchall():
                data.append({
                    'title': row[0],
                    'url': row[1],
                    'source': row[2],
                    'publish_time': row[3],
                    'sentiment': row[4],
                    'score': row[5],
                    'confidence': row[6],
                    'reasoning': row[7]
                })
            
            with open(f'{output_file}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 数据已导出到 {output_file}.json")
        
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='财经新闻数据库管理')
    
    parser.add_argument('action', type=str, 
                        choices=['init', 'show-stats', 'export', 'trend', 'industry'],
                        help='操作类型')
    parser.add_argument('--db', type=str, default='finance_news.db',
                        help='数据库文件路径')
    parser.add_argument('--format', type=str, default='csv',
                        choices=['csv', 'json'],
                        help='导出格式')
    parser.add_argument('--output', type=str, default='export_data',
                        help='输出文件名')
    parser.add_argument('--days', type=int, default=30,
                        help='查询天数')
    parser.add_argument('--ticker', type=str, default='',
                        help='股票代码')
    
    args = parser.parse_args()
    
    db = FinanceNewsDB(args.db)
    
    if args.action == 'init':
        print("✅ 数据库已初始化")
    
    elif args.action == 'show-stats':
        stats = db.get_statistics()
        print("\n📊 数据库统计")
        print("=" * 50)
        print(f"总新闻数：{stats['total_news']}")
        print(f"总分析数：{stats['total_analysis']}")
        print(f"总简报数：{stats['total_briefings']}")
        print(f"\n情感分布:")
        for sentiment, count in stats['sentiment_distribution'].items():
            print(f"  {sentiment}: {count}")
        print(f"\n最后分析时间：{stats['last_analysis']}")
    
    elif args.action == 'export':
        db.export_data(args.format, args.output)
    
    elif args.action == 'trend':
        if args.ticker:
            results = db.get_stock_sentiment(args.ticker, args.days)
            print(f"\n📈 {args.ticker} 情感趋势（最近{args.days}天）")
            for r in results[:10]:
                print(f"  {r['date']}: {r['sentiment']} ({r['score']}) - {r['title'][:50]}")
        else:
            results = db.get_sentiment_trend(args.days)
            print(f"\n📊 整体情感趋势（最近{args.days}天）")
            for r in results[:20]:
                print(f"  {r['date']}: {r['sentiment']} - {r['count']}条，均分{r['avg_score']:.1f}")
    
    elif args.action == 'industry':
        results = db.get_industry_summary(args.days)
        print(f"\n🏢 行业摘要（最近{args.days}天）")
        for sector, data in results.items():
            pos_pct = data['positive'] / data['total'] * 100 if data['total'] > 0 else 0
            print(f"  {sector}: {data['total']}条新闻，利好{pos_pct:.1f}%")


if __name__ == '__main__':
    main()
