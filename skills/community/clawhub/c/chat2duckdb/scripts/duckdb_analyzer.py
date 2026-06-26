#!/usr/bin/env python3
"""
DuckDB 数据分析核心脚本
支持数据文件注册、查询执行、数据抽样和错误处理

优化内容:
1. 改进错误处理和 SQL 校正
2. 增强 describe 模式的统计功能
3. 添加详细的错误诊断信息
"""

import argparse
import os
import sys
import re
import time
import duckdb
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime


class SQLCorrectionEngine:
    """SQL 校正引擎 - 智能识别和修复常见 SQL 错误"""
    
    def __init__(self):
        self.correction_patterns = {
            'syntax_error': [
                (r';\s*$', ''),  # 移除末尾分号
                (r';;+', ';'),  # 移除多余分号
                (r',\s*(FROM|WHERE|GROUP|ORDER|LIMIT)', r'\1'),  # 移除多余的逗号
                (r'(\w+)\s*,\s*', r'\1, '),  # 规范化逗号后的空格
            ],
            'quote_error': [
                # 移除双引号转单引号的规则，因为 DuckDB 标准语法使用双引号标识标识符
                # (r'"([^"]*)"', r"'\1'"),  # 已移除：双引号转单引号
            ],
            'chinese_punctuation': [
                (r'，', ','),  # 中文逗号转英文逗号
                (r'；', ';'),  # 中文分号转英文分号
                (r'（', '('),  # 中文括号转英文括号
                (r'）', ')'),  # 中文括号转英文括号
            ]
        }
    
    def correct(self, sql: str, error_msg: str, available_columns: List[str] = None) -> Tuple[str, List[str]]:
        """
        智能校正 SQL
        
        Args:
            sql: 原始 SQL
            error_msg: 错误信息
            available_columns: 可用的列名列表
            
        Returns:
            (校正后的 SQL, 应用的校正操作列表)
        """
        corrected_sql = sql.strip()
        corrections_applied = []
        error_lower = error_msg.lower()
        
        # 0. 中文字段处理 - 自动添加双引号
        corrected_sql, chinese_corrections = self._quote_chinese_columns(corrected_sql, available_columns)
        corrections_applied.extend(chinese_corrections)
        
        # 0.5 中文标点转英文标点
        for pattern, replacement in self.correction_patterns['chinese_punctuation']:
            new_sql = re.sub(pattern, replacement, corrected_sql)
            if new_sql != corrected_sql:
                corrected_sql = new_sql
                corrections_applied.append(f"中文标点校正：{pattern} -> {replacement}")
        
        # 1. 语法错误校正
        if any(keyword in error_lower for keyword in ['syntax error', 'parse error']):
            for pattern, replacement in self.correction_patterns['syntax_error']:
                new_sql = re.sub(pattern, replacement, corrected_sql, flags=re.IGNORECASE)
                if new_sql != corrected_sql:
                    corrected_sql = new_sql
                    corrections_applied.append(f"语法校正：{pattern} -> {replacement}")
        
        # 2. 列名错误校正
        if 'column' in error_lower and ('not found' in error_lower or 'does not exist' in error_lower):
            col_match = re.search(r'column "([^"]+)"', error_lower)
            if col_match and available_columns:
                wrong_col = col_match.group(1)
                best_match = self._find_similar_column(wrong_col, available_columns)
                if best_match:
                    # 使用更精确的匹配，只替换未加引号的列名
                    corrected_sql = re.sub(
                        r'(?<!")\b' + re.escape(wrong_col) + r'\b(?!")',
                        f'"{best_match}"',
                        corrected_sql,
                        flags=re.IGNORECASE
                    )
                    corrections_applied.append(f"列名校正：{wrong_col} -> \"{best_match}\" (DuckDB 语法要求)")
        
        # 3. 表名错误校正
        if 'relation' in error_lower and 'does not exist' in error_lower:
            corrections_applied.append("检测到表名错误，请检查表名是否正确")
        
        # 4. 引号校正
        for pattern, replacement in self.correction_patterns['quote_error']:
            new_sql = re.sub(pattern, replacement, corrected_sql)
            if new_sql != corrected_sql:
                corrected_sql = new_sql
                corrections_applied.append(f"引号校正")
        
        # 5. 大小写规范化
        corrected_sql = self._normalize_sql_case(corrected_sql)
        
        return corrected_sql, corrections_applied
    
    def _quote_chinese_columns(self, sql: str, available_columns: List[str] = None) -> Tuple[str, List[str]]:
        """
        为中文字段名自动添加双引号（包括列名和别名）
        
        Args:
            sql: 原始 SQL
            available_columns: 可用的列名列表
            
        Returns:
            (处理后的 SQL, 校正操作列表)
        """
        corrections = []
        processed_sql = sql
        
        if available_columns:
            # 找出包含中文的列名
            chinese_columns = [col for col in available_columns if self._contains_chinese(col)]
            
            # 按长度降序排序，先处理长列名，避免短列名匹配干扰
            chinese_columns.sort(key=len, reverse=True)
            
            # 为每个中文字段添加双引号（如果还没有的话）
            for col in chinese_columns:
                # 只匹配未加引号的字段名
                # 使用负向前瞻和负向后瞻确保不匹配已加引号的字段
                # 匹配：前面不是双引号，后面不是双引号
                pattern = r'(?<!")' + re.escape(col) + r'(?!")'
                # 在当前的 processed_sql 中查找（而不是原始 SQL）
                if re.search(pattern, processed_sql):
                    # 确保不会重复添加引号
                    if f'"{col}"' not in processed_sql:
                        processed_sql = re.sub(pattern, f'"{col}"', processed_sql)
                        # 如果列名包含空格或特殊字符，添加额外提示
                        if ' ' in col or '-' in col or ':' in col:
                            corrections.append(f"中文字段加引号 (DuckDB 语法要求): {col} -> \"{col}\"")
                        else:
                            corrections.append(f"中文字段加引号：{col} -> \"{col}\"")
        
        # 处理 AS 别名中的中文（为所有 AS 后的中文字段添加双引号）
        # 匹配 AS 后面的中文字段（未加引号的），直到遇到逗号、空格、右括号或语句结束
        as_alias_pattern = r'\bAS\s+([\u4e00-\u9fff][\u4e00-\u9fff\w_]*)(?=\s*(?:,|\)|ORDER|GROUP|WHERE|FROM|$))'
        for match in re.finditer(as_alias_pattern, processed_sql, re.IGNORECASE):
            alias = match.group(1)
            if f'"{alias}"' not in processed_sql:
                # 检查别名前面是否已经有引号
                start_pos = match.start(1)
                if start_pos > 0 and processed_sql[start_pos-1] != '"':
                    processed_sql = processed_sql.replace(f'AS {alias}', f'AS "{alias}"', 1)
                    corrections.append(f"AS 别名加引号：{alias} -> \"{alias}\"")
        
        return processed_sql, corrections
    
    def _contains_chinese(self, text: str) -> bool:
        """检查字符串是否包含中文字符"""
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        return bool(chinese_pattern.search(text))
    
    def _find_similar_column(self, wrong_col: str, available_columns: List[str]) -> Optional[str]:
        """
        查找最相似的列名
        
        Args:
            wrong_col: 错误的列名
            available_columns: 可用的列名列表
            
        Returns:
            最相似的列名，如果没有找到则返回 None
        """
        wrong_col_lower = wrong_col.lower()
        
        # 1. 首先尝试精确匹配（不区分大小写）
        for col in available_columns:
            if col.lower() == wrong_col_lower:
                return col
        
        # 2. 尝试前缀匹配 - 检查错误列名是否是某个可用列名的前缀
        # 这对于处理包含空格的列名特别有用（DuckDB 会截断空格后的内容）
        prefix_matches = []
        for col in available_columns:
            col_lower = col.lower()
            # 检查 wrong_col 是否是 col 的前缀
            if col_lower.startswith(wrong_col_lower):
                prefix_matches.append((len(col), col))  # 按长度排序
        
        if prefix_matches:
            # 返回最长的匹配（最具体的匹配）
            prefix_matches.sort(key=lambda x: x[0], reverse=True)
            return prefix_matches[0][1]
        
        # 3. 尝试子串匹配 - 检查 col 是否包含 wrong_col
        substring_matches = []
        for col in available_columns:
            col_lower = col.lower()
            if wrong_col_lower in col_lower and len(wrong_col) > 2:  # 避免太短的匹配
                substring_matches.append((len(col), col))
        
        if substring_matches:
            # 返回最长的匹配
            substring_matches.sort(key=lambda x: x[0], reverse=True)
            return substring_matches[0][1]
        
        # 4. 使用编辑距离进行模糊匹配
        min_distance = float('inf')
        best_match = None
        
        for col in available_columns:
            distance = self._levenshtein_distance(wrong_col_lower, col.lower())
            if distance < min_distance and distance <= 2:
                min_distance = distance
                best_match = col
        
        return best_match
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """计算编辑距离"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _normalize_sql_case(self, sql: str) -> str:
        """规范化 SQL 关键字大小写"""
        keywords = ['select', 'from', 'where', 'group by', 'order by', 'limit', 
                   'and', 'or', 'as', 'count', 'sum', 'avg', 'min', 'max', 'desc', 'asc']
        
        normalized = sql
        for keyword in keywords:
            pattern = r'\b' + keyword + r'\b'
            normalized = re.sub(pattern, keyword.upper(), normalized, flags=re.IGNORECASE)
        
        return normalized


class DuckDBAnalyzer:
    """DuckDB 数据分析器"""
    
    def __init__(
        self,
        file_path: str,
        table_name: str = "data",
        excel_sheet: Optional[str] = None,
        persist_db_path: Optional[str] = None,
        persist_table: bool = False
    ):
        """
        初始化 DuckDB 分析器
        
        Args:
            file_path: 数据文件路径
            table_name: 注册的表名，默认为 'data'
            excel_sheet: Excel 工作表名称，不指定时读取第一个工作表
            persist_db_path: DuckDB 数据库文件路径，不指定则使用内存数据库
            persist_table: 是否将注册表持久化到数据库文件
        """
        self.file_path = file_path
        self.table_name = table_name
        self.excel_sheet = excel_sheet
        self.persist_db_path = persist_db_path
        self.persist_table = persist_table
        self.conn = None
        self.columns = []
        self.sql_corrector = SQLCorrectionEngine()
        self._connect()
        self._register_table()
    
    def _connect(self):
        """建立 DuckDB 连接"""
        try:
            if self.persist_db_path:
                db_dir = os.path.dirname(os.path.abspath(self.persist_db_path))
                if db_dir and not os.path.exists(db_dir):
                    os.makedirs(db_dir, exist_ok=True)
                self.conn = duckdb.connect(self.persist_db_path)
            else:
                self.conn = duckdb.connect()
            self.conn.execute("SET memory_limit='4GB'")
        except Exception as e:
            raise RuntimeError(f"无法建立 DuckDB 连接：{str(e)}")
    
    def _register_table(self):
        """将数据文件注册为表"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"数据文件不存在：{self.file_path}")
        
        file_ext = os.path.splitext(self.file_path)[1].lower()
        create_stmt = "CREATE OR REPLACE TABLE" if self.persist_table else "CREATE OR REPLACE TEMP TABLE"
        
        try:
            if file_ext == '.csv':
                self.conn.execute(f"{create_stmt} {self.table_name} AS SELECT * FROM read_csv_auto('{self.file_path}')")
            elif file_ext == '.json':
                self.conn.execute(f"{create_stmt} {self.table_name} AS SELECT * FROM read_json_auto('{self.file_path}')")
            elif file_ext == '.parquet':
                self.conn.execute(f"{create_stmt} {self.table_name} AS SELECT * FROM read_parquet('{self.file_path}')")
            elif file_ext in ('.xlsx', '.xls'):
                read_kwargs = {}
                if self.excel_sheet:
                    read_kwargs["sheet_name"] = self.excel_sheet
                excel_df = pd.read_excel(self.file_path, **read_kwargs)
                excel_df = self._prepare_dataframe_for_registration(excel_df)
                self.conn.register("__excel_data__", excel_df)
                self.conn.execute(f"{create_stmt} {self.table_name} AS SELECT * FROM __excel_data__")
                self.conn.unregister("__excel_data__")
            else:
                raise ValueError(f"不支持的文件格式：{file_ext}")
            
            schema = self.conn.execute(f"DESCRIBE {self.table_name}").fetchdf()
            self.columns = list(schema['column_name'])
            
        except Exception as e:
            raise RuntimeError(f"无法注册数据表：{str(e)}")

    def _prepare_dataframe_for_registration(self, df: pd.DataFrame) -> pd.DataFrame:
        prepared = df.replace([np.inf, -np.inf], np.nan)
        # 重命名列，将特殊字符（-、空格等）替换为下划线，避免 SQL 解析歧义
        new_columns = {}
        for col in prepared.columns:
            new_col = col.replace('-', '_').replace(' ', '_').replace('(', '_').replace(')', '_')
            if new_col != col:
                new_columns[col] = new_col
        if new_columns:
            prepared = prepared.rename(columns=new_columns)
        return prepared
    
    def describe(self, detailed: bool = True) -> Dict[str, Any]:
        """
        获取表结构和数据统计信息
        
        Args:
            detailed: 是否返回详细统计信息
            
        Returns:
            包含表结构和统计信息的字典
        """
        try:
            schema = self.conn.execute(f"DESCRIBE {self.table_name}").fetchdf()
            stats = self.conn.execute(f"SELECT COUNT(*) as total_rows FROM {self.table_name}").fetchdf()
            sample = self.conn.execute(f"SELECT * FROM {self.table_name} LIMIT 5").fetchdf()
            
            result = {
                "schema": schema.to_dict('records'),
                "total_rows": int(stats['total_rows'].iloc[0]),
                "sample": sample.to_dict('records'),
                "columns": list(schema['column_name']),
                "column_types": {row['column_name']: row['column_type'] for _, row in schema.iterrows()}
            }
            
            if detailed:
                result["detailed_stats"] = self._get_detailed_statistics()
            
            return result
        except Exception as e:
            raise RuntimeError(f"无法获取数据描述：{str(e)}")
    
    def _get_detailed_statistics(self) -> Dict[str, Any]:
        """获取详细的统计信息"""
        stats = {}
        
        try:
            numeric_stats = self._get_numeric_statistics()
            if numeric_stats:
                stats["numeric_columns"] = numeric_stats
            
            categorical_stats = self._get_categorical_statistics()
            if categorical_stats:
                stats["categorical_columns"] = categorical_stats
            
            date_stats = self._get_date_statistics()
            if date_stats:
                stats["date_columns"] = date_stats
            
            stats["data_quality"] = self._get_data_quality_stats()
            
        except Exception as e:
            stats["error"] = str(e)
        
        return stats
    
    def _get_numeric_statistics(self) -> Dict[str, Any]:
        """获取数值列的统计信息"""
        numeric_stats = {}
        
        for col in self.columns:
            try:
                query = f"""
                SELECT 
                    COUNT({col}) as non_null_count,
                    MIN({col}) as min_val,
                    MAX({col}) as max_val,
                    AVG({col}) as avg_val,
                    STDDEV({col}) as stddev_val,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {col}) as median_val
                FROM {self.table_name}
                WHERE {col} IS NOT NULL AND typeof({col}) IN ('INTEGER', 'BIGINT', 'DOUBLE', 'FLOAT')
                """
                result = self.conn.execute(query).fetchone()
                
                if result and result[0] > 0:
                    numeric_stats[col] = {
                        "non_null_count": int(result[0]) if result[0] is not None else 0,
                        "min": float(result[1]) if result[1] is not None else None,
                        "max": float(result[2]) if result[2] is not None else None,
                        "mean": round(float(result[3]), 2) if result[3] is not None else None,
                        "std": round(float(result[4]), 2) if result[4] is not None else None,
                        "median": round(float(result[5]), 2) if result[5] is not None else None
                    }
            except:
                continue
        
        return numeric_stats
    
    def _get_categorical_statistics(self) -> Dict[str, Any]:
        """获取分类列的统计信息"""
        categorical_stats = {}
        
        for col in self.columns:
            try:
                query = f"""
                SELECT 
                    COUNT(DISTINCT {col}) as unique_count,
                    MODE({col}) as mode_val
                FROM {self.table_name}
                WHERE typeof({col}) = 'VARCHAR'
                """
                result = self.conn.execute(query).fetchone()
                
                if result:
                    top_values_query = f"""
                    SELECT {col}, COUNT(*) as cnt
                    FROM {self.table_name}
                    WHERE {col} IS NOT NULL
                    GROUP BY {col}
                    ORDER BY cnt DESC
                    LIMIT 10
                    """
                    top_values = self.conn.execute(top_values_query).fetchdf()
                    
                    categorical_stats[col] = {
                        "unique_count": int(result[0]) if result[0] is not None else 0,
                        "most_common": str(result[1]) if result[1] is not None else None,
                        "top_values": top_values.to_dict('records') if not top_values.empty else []
                    }
            except:
                continue
        
        return categorical_stats
    
    def _get_date_statistics(self) -> Dict[str, Any]:
        """获取日期列的统计信息"""
        date_stats = {}
        
        for col in self.columns:
            try:
                query = f"""
                SELECT 
                    MIN({col}) as min_date,
                    MAX({col}) as max_date,
                    COUNT(DISTINCT {col}) as unique_dates
                FROM {self.table_name}
                WHERE typeof({col}) IN ('DATE', 'TIMESTAMP', 'TIMESTAMP_NS', 'TIMESTAMP_MS', 'TIMESTAMP_US')
                """
                result = self.conn.execute(query).fetchone()
                
                if result and result[0] is not None:
                    date_stats[col] = {
                        "min_date": str(result[0]),
                        "max_date": str(result[1]),
                        "unique_dates": int(result[2])
                    }
            except:
                continue
        
        return date_stats
    
    def _get_data_quality_stats(self) -> Dict[str, Any]:
        """获取数据质量统计"""
        quality_stats = {
            "total_rows": 0,
            "columns": {}
        }
        
        try:
            total = self.conn.execute(f"SELECT COUNT(*) FROM {self.table_name}").fetchone()[0]
            quality_stats["total_rows"] = int(total)
            
            for col in self.columns:
                null_count = self.conn.execute(
                    f"SELECT COUNT(*) FROM {self.table_name} WHERE {col} IS NULL"
                ).fetchone()[0]
                
                quality_stats["columns"][col] = {
                    "null_count": int(null_count),
                    "null_percentage": round((null_count / total * 100), 2) if total > 0 else 0,
                    "non_null_count": int(total - null_count)
                }
        
        except Exception as e:
            quality_stats["error"] = str(e)
        
        return quality_stats
    
    def query(self, sql: str, sample_fraction: Optional[float] = None) -> pd.DataFrame:
        """
        执行 SQL 查询
        
        Args:
            sql: SQL 查询语句
            sample_fraction: 数据抽样比例 (0-1)，None 表示不抽样
            
        Returns:
            查询结果 DataFrame
        """
        try:
            if sample_fraction is not None:
                if "WHERE" in sql.upper():
                    base_sql, where_part = sql.split("WHERE", 1)
                    sampled_sql = f"{base_sql} WHERE RANDOM() < {sample_fraction} AND {where_part}"
                else:
                    sampled_sql = f"{sql} WHERE RANDOM() < {sample_fraction}"
                
                result = self.conn.execute(sampled_sql).fetchdf()
            else:
                result = self.conn.execute(sql).fetchdf()
            
            return result
        except Exception as e:
            raise RuntimeError(f"查询执行失败：{str(e)}")
    
    def query_with_retry(self, sql: str, max_retries: int = 3, 
                        sample_fraction: Optional[float] = None) -> Tuple[pd.DataFrame, int, List[str]]:
        """
        带重试机制的查询执行
        
        Args:
            sql: SQL 查询语句
            max_retries: 最大重试次数
            sample_fraction: 数据抽样比例
            
        Returns:
            (查询结果 DataFrame, 重试次数，应用的校正操作列表)
        """
        last_error = None
        current_sql = sql
        all_corrections = []
        
        for attempt in range(max_retries + 1):
            try:
                result = self.query(current_sql, sample_fraction)
                return result, attempt, all_corrections
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    corrected_sql, corrections = self.sql_corrector.correct(
                        current_sql, str(e), self.columns
                    )
                    all_corrections.extend(corrections)
                    if corrections:
                        current_sql = corrected_sql
        
        raise RuntimeError(f"查询执行失败，已重试 {max_retries} 次：{str(last_error)}")
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="DuckDB 数据分析工具")
    parser.add_argument("--file_path", required=True, help="数据文件路径")
    parser.add_argument("--table_name", default="data", help="表名 (默认：data)")
    parser.add_argument("--excel_sheet", help="Excel 工作表名称（仅 xlsx/xls 生效）")
    parser.add_argument("--persist_db_path", help="DuckDB 数据库文件路径（启用数据库持久化）")
    parser.add_argument("--persist_table", action="store_true", help="将注册表持久化到数据库文件（默认临时表）")
    parser.add_argument("--mode", required=True, choices=["describe", "query"], 
                       help="操作模式：describe(数据描述), query(数据查询)")
    parser.add_argument("--sql", help="SQL 查询语句 (query 模式必需)")
    parser.add_argument("--sample_fraction", type=float, 
                       help="数据抽样比例 (0-1)，不指定则不抽样")
    parser.add_argument("--max_retries", type=int, default=3, 
                       help="最大重试次数 (默认：3)")
    parser.add_argument("--output", help="输出文件路径 (可选)")
    parser.add_argument("--simple", action="store_true", 
                       help="简单模式，不生成详细统计信息")
    
    args = parser.parse_args()
    
    try:
        with DuckDBAnalyzer(
            args.file_path,
            args.table_name,
            args.excel_sheet,
            args.persist_db_path,
            args.persist_table
        ) as analyzer:
            if args.mode == "describe":
                start_time = time.time()
                result = analyzer.describe(detailed=not args.simple)
                elapsed = time.time() - start_time
                
                print("=" * 80)
                print("DuckDB 数据分析报告")
                print("=" * 80)
                print(f"文件路径：{args.file_path}")
                print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"执行时间：{elapsed:.2f}秒")
                print("=" * 80)
                
                print(f"\n【基本信息】")
                print(f"总行数：{result['total_rows']:,}")
                print(f"列数：{len(result['columns'])}")
                
                print(f"\n【表结构】")
                for col in result['schema']:
                    print(f"  - {col['column_name']}: {col['column_type']}")
                
                if 'detailed_stats' in result:
                    stats = result['detailed_stats']
                    
                    if 'numeric_columns' in stats:
                        print(f"\n【数值列统计】")
                        for col, col_stats in stats['numeric_columns'].items():
                            print(f"\n  {col}:")
                            print(f"    非空值：{col_stats['non_null_count']:,}")
                            if col_stats['mean'] is not None:
                                print(f"    平均值：{col_stats['mean']:,.2f}")
                                print(f"    中位数：{col_stats['median']:,.2f}")
                                print(f"    标准差：{col_stats['std']:,.2f}")
                                print(f"    最小值：{col_stats['min']:,.2f}")
                                print(f"    最大值：{col_stats['max']:,.2f}")
                    
                    if 'categorical_columns' in stats:
                        print(f"\n【分类列统计】")
                        for col, col_stats in stats['categorical_columns'].items():
                            print(f"\n  {col}:")
                            print(f"    唯一值数量：{col_stats['unique_count']:,}")
                            print(f"    最常见值：{col_stats['most_common']}")
                            if col_stats['top_values']:
                                print(f"    前 5 个最常见值:")
                                for val in col_stats['top_values'][:5]:
                                    print(f"      - {val.get(col, 'N/A')}: {val.get('cnt', 0):,}次")
                    
                    if 'date_columns' in stats:
                        print(f"\n【日期列统计】")
                        for col, col_stats in stats['date_columns'].items():
                            print(f"\n  {col}:")
                            print(f"    最早日期：{col_stats['min_date']}")
                            print(f"    最晚日期：{col_stats['max_date']}")
                            print(f"    唯一日期数：{col_stats['unique_dates']:,}")
                    
                    if 'data_quality' in stats:
                        print(f"\n【数据质量】")
                        quality = stats['data_quality']
                        print(f"  总行数：{quality['total_rows']:,}")
                        has_null = False
                        for col, col_stats in quality['columns'].items():
                            if col_stats['null_count'] > 0:
                                print(f"  {col}: 缺失 {col_stats['null_count']:,} ({col_stats['null_percentage']}%)")
                                has_null = True
                        if not has_null:
                            print(f"  所有列数据完整，无缺失值")
                
                print(f"\n【数据样本 (前 5 行)】")
                print(pd.DataFrame(result['sample']).to_string(index=False))
                
                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        import json
                        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
                    print(f"\n结果已保存到：{args.output}")
            
            elif args.mode == "query":
                if not args.sql:
                    print("错误：query 模式需要指定 --sql 参数", file=sys.stderr)
                    sys.exit(1)
                
                print("=" * 80)
                print("DuckDB SQL 查询执行")
                print("=" * 80)
                print(f"执行 SQL: {args.sql}")
                if args.sample_fraction:
                    print(f"数据抽样比例：{args.sample_fraction}")
                print("=" * 80)
                
                start_time = time.time()
                result, retries, corrections = analyzer.query_with_retry(
                    args.sql, 
                    args.max_retries,
                    args.sample_fraction
                )
                elapsed = time.time() - start_time
                
                if corrections:
                    print(f"\n【SQL 校正记录】")
                    for correction in corrections:
                        print(f"  ✓ {correction}")
                
                print(f"\n【查询结果】")
                print(f"执行时间：{elapsed:.2f}秒")
                print(f"重试次数：{retries}")
                print(f"结果行数：{len(result):,}")
                print(f"\n数据预览:")
                print(result.to_string(index=False))
                
                if args.output:
                    file_ext = os.path.splitext(args.output)[1].lower()
                    if file_ext == '.csv':
                        result.to_csv(args.output, index=False)
                    elif file_ext == '.json':
                        result.to_json(args.output, orient='records', force_ascii=False)
                    elif file_ext == '.parquet':
                        result.to_parquet(args.output, index=False)
                    elif file_ext in ('.xlsx', '.xls'):
                        result.to_excel(args.output, index=False, engine='openpyxl')
                    else:
                        result.to_csv(args.output, index=False)
                    print(f"\n结果已保存到：{args.output}")
    
    except Exception as e:
        print(f"\n错误：{str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
