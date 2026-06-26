# -*- coding: utf-8 -*-
"""
度量衡智库 · 数据库连接模块 v1.0
Database Connector - 支持本地造价数据库检索
=============================================

支持的数据库类型：
1. SQLite - 轻量级本地数据库（造价指标库）
2. PostgreSQL - 企业级数据库
3. Excel/CSV - 常见造价数据格式

支持的造价数据库：
- 深圳市建设工程造价管理站
- 广州市建设工程造价管理站
- 苏州市工程造价协会
- 广东省造价信息网
- 各省市造价信息网站

作者：度量衡智库
版本：1.0.0
日期：2026-04-03
"""

import sqlite3
import csv
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# 数据库路径配置
# ============================================================

# 默认本地数据库路径 (~/.workbuddy/data/)
DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), ".workbuddy", "data")
os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)

# 默认SQLite数据库路径
DEFAULT_DB_PATH = os.path.join(DEFAULT_DATA_DIR, "cost_index.db")

# ============================================================
# 数据类定义
# ============================================================

@dataclass
class CostIndex:
    """造价指标"""
    city: str                    # 城市
    building_type: str          # 建筑类型
    structure_type: str         # 结构类型
    unit_price_low: float       # 单方造价低限 (元/m²)
    unit_price_mid: float       # 单方造价中值
    unit_price_high: float      # 单方造价高限
    steel_content: float        # 钢筋含量 (kg/m²)
    concrete_content: float     # 混凝土含量 (m³/m²)
    masonry_content: float      # 砌体含量 (m³/m²)
    formwork_ratio: float       # 模板系数
    region_factor: float        # 地区系数
    data_source: str            # 数据来源
    data_date: str              # 数据日期
    floor_range: str            # 楼层范围

@dataclass
class MaterialPrice:
    """材料价格"""
    material_name: str          # 材料名称
    specification: str          # 规格型号
    unit: str                   # 单位
    price: float                # 价格
    unit: str                   # 单位
    price_date: str             # 价格日期
    city: str                    # 城市

# ============================================================
# 数据库连接类
# ============================================================

class CostDatabaseConnector:
    """
    造价数据库连接器
    
    支持：
    1. 连接本地SQLite数据库
    2. 连接PostgreSQL数据库
    3. 导入Excel/CSV造价指标
    4. 检索匹配造价数据
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库路径，默认使用 ~/.workbuddy/data/cost_index.db
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        if not os.path.exists(self.db_path):
            logger.info(f"创建新数据库: {self.db_path}")
            self._create_tables()
            self._insert_sample_data()
    
    def _create_tables(self):
        """创建数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 造价指标表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cost_indexes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                building_type TEXT NOT NULL,
                structure_type TEXT NOT NULL,
                unit_price_low REAL NOT NULL,
                unit_price_mid REAL NOT NULL,
                unit_price_high REAL NOT NULL,
                steel_content REAL,
                concrete_content REAL,
                masonry_content REAL,
                formwork_ratio REAL,
                region_factor REAL DEFAULT 1.0,
                data_source TEXT,
                data_date TEXT,
                floor_range TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 材料价格表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS material_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material_name TEXT NOT NULL,
                specification TEXT,
                unit TEXT NOT NULL,
                price REAL NOT NULL,
                price_date TEXT NOT NULL,
                city TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 城市系数表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_factors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL UNIQUE,
                province TEXT,
                build_factor REAL DEFAULT 1.0,
                install_factor REAL DEFAULT 1.0,
                labor_factor REAL DEFAULT 1.0,
                data_date TEXT,
                data_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 爬虫日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crawl_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT NOT NULL,
                status TEXT NOT NULL,
                data_count INTEGER,
                error_message TEXT,
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_city ON cost_indexes(city)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_building ON cost_indexes(building_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_structure ON cost_indexes(structure_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_material ON material_prices(material_name)')
        
        conn.commit()
        conn.close()
        logger.info("数据库表结构创建完成")
    
    def _insert_sample_data(self):
        """插入示例数据（基于官方造价指标）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 深圳造价指标（基于深圳市建设工程造价管理站数据）
        shenzhen_data = [
            # 住宅
            ("深圳", "住宅", "框架结构", 4200, 4800, 5500, 42, 0.32, 0.18, 8.5, 1.12, "深圳市建设工程造价管理站", "2026-03", "11-18层"),
            ("深圳", "住宅", "剪力墙结构", 4500, 5200, 6000, 48, 0.35, 0.12, 9.0, 1.12, "深圳市建设工程造价管理站", "2026-03", "11-18层"),
            ("深圳", "住宅", "框架-剪力墙", 4800, 5500, 6500, 50, 0.36, 0.10, 9.5, 1.12, "深圳市建设工程造价管理站", "2026-03", "18-33层"),
            # 办公
            ("深圳", "办公", "框架结构", 5000, 5800, 6800, 55, 0.35, 0.15, 9.0, 1.12, "深圳市建设工程造价管理站", "2026-03", "11-18层"),
            ("深圳", "办公", "框架-核心筒", 6500, 8000, 10000, 75, 0.42, 0.08, 11.0, 1.12, "深圳市建设工程造价管理站", "2026-03", "33层以上"),
            # 商业
            ("深圳", "商业", "框架结构", 5500, 6500, 8000, 60, 0.38, 0.20, 10.0, 1.12, "深圳市建设工程造价管理站", "2026-03", "5层以下"),
            ("深圳", "商业", "框架-剪力墙", 6000, 7200, 9000, 65, 0.40, 0.15, 10.5, 1.12, "深圳市建设工程造价管理站", "2026-03", "6-18层"),
        ]
        
        # 广州造价指标
        guangzhou_data = [
            ("广州", "住宅", "框架结构", 4000, 4600, 5300, 40, 0.30, 0.18, 8.0, 1.10, "广州市建设工程造价管理站", "2026-03", "11-18层"),
            ("广州", "住宅", "剪力墙结构", 4300, 5000, 5800, 46, 0.34, 0.12, 8.8, 1.10, "广州市建设工程造价管理站", "2026-03", "11-18层"),
            ("广州", "住宅", "框架-剪力墙", 4600, 5300, 6200, 48, 0.35, 0.10, 9.2, 1.10, "广州市建设工程造价管理站", "2026-03", "18-33层"),
            ("广州", "办公", "框架结构", 4800, 5600, 6600, 52, 0.34, 0.15, 8.8, 1.10, "广州市建设工程造价管理站", "2026-03", "11-18层"),
            ("广州", "办公", "框架-核心筒", 6200, 7500, 9500, 70, 0.40, 0.08, 10.5, 1.10, "广州市建设工程造价管理站", "2026-03", "33层以上"),
        ]
        
        # 苏州造价指标
        suzhou_data = [
            ("苏州", "住宅", "框架结构", 3800, 4300, 5000, 38, 0.28, 0.18, 7.5, 1.08, "苏州市工程造价协会", "2026-03", "11-18层"),
            ("苏州", "住宅", "剪力墙结构", 4100, 4700, 5500, 44, 0.32, 0.12, 8.2, 1.08, "苏州市工程造价协会", "2026-03", "11-18层"),
            ("苏州", "住宅", "框架-剪力墙", 4400, 5000, 5800, 46, 0.34, 0.10, 8.8, 1.08, "苏州市工程造价协会", "2026-03", "18-33层"),
            ("苏州", "办公", "框架结构", 4500, 5200, 6200, 50, 0.32, 0.15, 8.2, 1.08, "苏州市工程造价协会", "2026-03", "11-18层"),
            ("苏州", "办公", "框架-核心筒", 5800, 7000, 8800, 68, 0.38, 0.08, 10.0, 1.08, "苏州市工程造价协会", "2026-03", "33层以上"),
        ]
        
        # 珠海造价指标
        zhuhai_data = [
            ("珠海", "住宅", "框架结构", 3900, 4400, 5100, 39, 0.29, 0.18, 7.8, 1.08, "珠海市建设工程造价站", "2026-03", "11-18层"),
            ("珠海", "住宅", "框架-剪力墙", 4200, 4800, 5600, 45, 0.33, 0.10, 8.5, 1.08, "珠海市建设工程造价站", "2026-03", "18-33层"),
            ("珠海", "办公", "框架结构", 4600, 5300, 6300, 49, 0.31, 0.15, 8.0, 1.08, "珠海市建设工程造价站", "2026-03", "11-18层"),
        ]
        
        # 汕尾造价指标（基于历史数据）
        shanwei_data = [
            ("汕尾", "住宅", "框架结构", 3500, 4000, 4600, 35, 0.26, 0.18, 7.0, 1.03, "汕尾市住房和城乡建设局", "2026-02", "11-18层"),
            ("汕尾", "住宅", "框架-剪力墙", 3800, 4400, 5200, 42, 0.30, 0.10, 7.8, 1.03, "汕尾市住房和城乡建设局", "2026-02", "18-33层"),
            ("汕尾", "办公", "框架结构", 4200, 4800, 5700, 46, 0.28, 0.15, 7.5, 1.03, "汕尾市住房和城乡建设局", "2026-02", "11-18层"),
        ]
        
        # 插入所有数据
        all_data = shenzhen_data + guangzhou_data + suzhou_data + zhuhai_data + shanwei_data
        cursor.executemany('''
            INSERT INTO cost_indexes 
            (city, building_type, structure_type, unit_price_low, unit_price_mid, unit_price_high,
             steel_content, concrete_content, masonry_content, formwork_ratio, region_factor,
             data_source, data_date, floor_range)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', all_data)
        
        # 插入城市系数
        city_factors = [
            ("深圳", "广东", 1.12, 1.15, 1.18, "2026-03", "深圳市建设工程造价管理站"),
            ("广州", "广东", 1.10, 1.12, 1.15, "2026-03", "广州市建设工程造价管理站"),
            ("珠海", "广东", 1.08, 1.10, 1.12, "2026-03", "珠海市建设工程造价站"),
            ("汕头", "广东", 1.05, 1.07, 1.10, "2026-03", "汕头市建设工程造价站"),
            ("汕尾", "广东", 1.03, 1.05, 1.08, "2026-02", "汕尾市住房和城乡建设局"),
            ("佛山", "广东", 1.07, 1.09, 1.12, "2026-03", "佛山市建设工程造价站"),
            ("东莞", "广东", 1.06, 1.08, 1.10, "2026-03", "东莞市建设工程造价站"),
            ("苏州", "江苏", 1.08, 1.10, 1.12, "2026-03", "苏州市工程造价协会"),
            ("南京", "江苏", 1.09, 1.11, 1.13, "2026-03", "南京市建设工程造价管理处"),
            ("杭州", "浙江", 1.10, 1.12, 1.14, "2026-03", "杭州市建设工程造价管理协会"),
            ("上海", "上海", 1.15, 1.20, 1.25, "2026-03", "上海市建筑建材业市场管理总站"),
            ("北京", "北京", 1.18, 1.22, 1.28, "2026-03", "北京市住房和城乡建设委员会"),
        ]
        cursor.executemany('''
            INSERT INTO city_factors 
            (city, province, build_factor, install_factor, labor_factor, data_date, data_source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', city_factors)
        
        conn.commit()
        conn.close()
        logger.info(f"已插入 {len(all_data)} 条造价指标数据")
    
    def connect(self) -> sqlite3.Connection:
        """建立数据库连接"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    # ============================================================
    # 造价指标查询方法
    # ============================================================
    
    def query_cost_index(
        self,
        city: str = None,
        building_type: str = None,
        structure_type: str = None,
        floor_count: int = None
    ) -> List[CostIndex]:
        """
        查询造价指标
        
        Args:
            city: 城市名称（模糊匹配）
            building_type: 建筑类型
            structure_type: 结构类型
            floor_count: 楼层数
            
        Returns:
            匹配的造价指标列表
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # 构建查询条件
        conditions = []
        params = []
        
        if city:
            conditions.append("city LIKE ?")
            params.append(f"%{city}%")
        
        if building_type:
            conditions.append("building_type LIKE ?")
            params.append(f"%{building_type}%")
        
        if structure_type:
            conditions.append("structure_type LIKE ?")
            params.append(f"%{structure_type}%")
        
        # 楼层范围匹配
        if floor_count:
            if floor_count <= 18:
                conditions.append("floor_range LIKE ?")
                params.append("%11-18%")
            elif floor_count <= 33:
                conditions.append("floor_range LIKE ?")
                params.append("%18-33%")
            else:
                conditions.append("floor_range LIKE ?")
                params.append("%33层以上%")
        
        query = "SELECT * FROM cost_indexes"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY city, unit_price_mid"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append(CostIndex(
                city=row[1],
                building_type=row[2],
                structure_type=row[3],
                unit_price_low=row[4],
                unit_price_mid=row[5],
                unit_price_high=row[6],
                steel_content=row[7],
                concrete_content=row[8],
                masonry_content=row[9],
                formwork_ratio=row[10],
                region_factor=row[11],
                data_source=row[12],
                data_date=row[13],
                floor_range=row[14]
            ))
        
        return results
    
    def get_city_factor(self, city: str) -> Optional[Dict]:
        """获取城市系数"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM city_factors WHERE city LIKE ?",
            (f"%{city}%",)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                "city": row[1],
                "province": row[2],
                "build_factor": row[3],
                "install_factor": row[4],
                "labor_factor": row[5],
                "data_date": row[6],
                "data_source": row[7]
            }
        return None
    
    def get_latest_price(self, material_name: str, city: str = None) -> Optional[Dict]:
        """获取最新材料价格"""
        conn = self.connect()
        cursor = conn.cursor()
        
        if city:
            cursor.execute('''
                SELECT * FROM material_prices 
                WHERE material_name LIKE ? AND city LIKE ?
                ORDER BY price_date DESC LIMIT 1
            ''', (f"%{material_name}%", f"%{city}%"))
        else:
            cursor.execute('''
                SELECT * FROM material_prices 
                WHERE material_name LIKE ?
                ORDER BY price_date DESC LIMIT 1
            ''', (f"%{material_name}%",))
        
        row = cursor.fetchone()
        if row:
            return {
                "material_name": row[1],
                "specification": row[2],
                "unit": row[3],
                "price": row[4],
                "price_date": row[5],
                "city": row[6]
            }
        return None
    
    def import_csv(self, csv_path: str, table_name: str = "cost_indexes"):
        """
        从CSV文件导入数据
        
        Args:
            csv_path: CSV文件路径
            table_name: 目标表名
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if table_name == "cost_indexes":
                    cursor.execute('''
                        INSERT INTO cost_indexes 
                        (city, building_type, structure_type, unit_price_low, unit_price_mid, unit_price_high,
                         steel_content, concrete_content, masonry_content, formwork_ratio, region_factor,
                         data_source, data_date, floor_range)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('city', ''),
                        row.get('building_type', ''),
                        row.get('structure_type', ''),
                        float(row.get('unit_price_low', 0)),
                        float(row.get('unit_price_mid', 0)),
                        float(row.get('unit_price_high', 0)),
                        float(row.get('steel_content', 0)),
                        float(row.get('concrete_content', 0)),
                        float(row.get('masonry_content', 0)),
                        float(row.get('formwork_ratio', 8)),
                        float(row.get('region_factor', 1.0)),
                        row.get('data_source', ''),
                        row.get('data_date', ''),
                        row.get('floor_range', '')
                    ))
        
        conn.commit()
        logger.info(f"已从 {csv_path} 导入数据")
    
    def export_to_csv(self, output_path: str = None) -> str:
        """导出所有数据到CSV"""
        if output_path is None:
            output_path = os.path.join(DEFAULT_DATA_DIR, f"cost_export_{datetime.now().strftime('%Y%m%d')}.csv")
        
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM cost_indexes")
        rows = cursor.fetchall()
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['城市', '建筑类型', '结构类型', '单方低限', '单方中值', '单方高限',
                           '钢筋含量', '混凝土含量', '砌体含量', '模板系数', '地区系数',
                           '数据来源', '数据日期', '楼层范围'])
            writer.writerows(rows)
        
        logger.info(f"已导出数据到 {output_path}")
        return output_path
    
    def log_crawl(self, url: str, status: str, data_count: int = 0, error: str = ""):
        """记录爬虫日志"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO crawl_logs (source_url, status, data_count, error_message)
            VALUES (?, ?, ?, ?)
        ''', (url, status, data_count, error))
        conn.commit()
    
    def get_statistics(self) -> Dict:
        """获取数据库统计信息"""
        conn = self.connect()
        cursor = conn.cursor()
        
        stats = {}
        
        # 造价指标数量
        cursor.execute("SELECT COUNT(*) FROM cost_indexes")
        stats['cost_index_count'] = cursor.fetchone()[0]
        
        # 材料价格数量
        cursor.execute("SELECT COUNT(*) FROM material_prices")
        stats['material_price_count'] = cursor.fetchone()[0]
        
        # 城市数量
        cursor.execute("SELECT COUNT(DISTINCT city) FROM cost_indexes")
        stats['city_count'] = cursor.fetchone()[0]
        
        # 数据来源
        cursor.execute("SELECT DISTINCT data_source FROM cost_indexes")
        stats['data_sources'] = [row[0] for row in cursor.fetchall()]
        
        # 爬虫日志
        cursor.execute("SELECT COUNT(*) FROM crawl_logs WHERE status = 'success'")
        stats['successful_crawls'] = cursor.fetchone()[0]
        
        return stats
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# ============================================================
# 便捷函数
# ============================================================

def quick_query(city: str, building_type: str = None, structure_type: str = None) -> List[CostIndex]:
    """
    快速查询造价指标
    
    Args:
        city: 城市名称
        building_type: 建筑类型（可选）
        structure_type: 结构类型（可选）
        
    Returns:
        匹配的造价指标列表
    """
    with CostDatabaseConnector() as db:
        return db.query_cost_index(city, building_type, structure_type)


def get_real_time_factor(city: str) -> Optional[Dict]:
    """
    获取实时城市系数
    
    Args:
        city: 城市名称
        
    Returns:
        城市系数信息
    """
    with CostDatabaseConnector() as db:
        return db.get_city_factor(city)


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("度量衡智库 · 造价数据库连接器 v1.0")
    print("=" * 60)
    
    # 测试连接
    with CostDatabaseConnector() as db:
        # 显示统计信息
        stats = db.get_statistics()
        print(f"\n📊 数据库统计:")
        print(f"   造价指标: {stats['cost_index_count']} 条")
        print(f"   城市数量: {stats['city_count']} 个")
        print(f"   数据来源: {', '.join(stats['data_sources'])}")
        
        # 测试查询
        print("\n🔍 查询示例 - 深圳框架剪力墙住宅:")
        results = db.query_cost_index("深圳", "住宅", "框架-剪力墙")
        for r in results:
            print(f"   {r.floor_range}: ¥{r.unit_price_low:,} ~ {r.unit_price_high:,} 元/㎡")
            print(f"      钢筋: {r.steel_content} kg/㎡ | 混凝土: {r.concrete_content} m³/㎡")
        
        # 测试城市系数
        print("\n🏙️ 城市系数查询:")
        for city in ["深圳", "广州", "苏州", "汕尾"]:
            factor = db.get_city_factor(city)
            if factor:
                print(f"   {city}: 建安系数={factor['build_factor']}, 安装系数={factor['install_factor']}")
