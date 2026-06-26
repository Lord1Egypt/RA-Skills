#!/usr/bin/env python3
"""
Data Parser Skill - 数据文件解析器
支持 CSV/JSON/XLSX/XLS/Parquet/SQL
带自动编码检测、损坏修复、智能解析
"""

import os
import re
import json
import csv
import time
from typing import Union, List, Dict, Any, Optional, Callable
from pathlib import Path
from functools import wraps

# 可选依赖
try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import openpyxl
except ImportError:
    openpyxl = None

try:
    import chardet
except ImportError:
    chardet = None

try:
    import pyarrow.parquet as pq
except ImportError:
    pq = None

try:
    import xlrd
except ImportError:
    xlrd = None


# 全局配置
DEFAULT_CONFIG = {
    'chunk_size': 50000,
    'encoding': 'utf-8',
    'max_retries': 3,
    'retry_delay': 1,
    'cache_enabled': False,
    'log_level': 'WARNING',
}

CONFIG = DEFAULT_CONFIG.copy()


# ============== 装饰器 ==============
def retry_on_error(max_retries: int = 3, delay: float = 1):
    """自动重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    time.sleep(delay * (attempt + 1))
            raise last_error
        return wrapper
    return decorator


class DataParser:
    """智能数据文件解析器"""
    
    SUPPORTED_FORMATS = {
        '.csv': 'csv',
        '.json': 'json',
        '.xlsx': 'xlsx',
        '.xls': 'xls',
        '.parquet': 'parquet',
        '.sql': 'sql',
    }
    
    def __init__(self, config: dict = None):
        self.last_encoding = None
        self.last_format = None
        self.warnings = []
        self._cache = {}
        self._stats = {'reads': 0, 'writes': 0, 'errors': 0}
        
        if config:
            CONFIG.update(config)
    
    # ============== 配置管理 ==============
    @staticmethod
    def set_config(key: str, value: Any):
        CONFIG[key] = value
        
    @staticmethod
    def get_config(key: str = None) -> Any:
        if key:
            return CONFIG.get(key)
        return CONFIG.copy()
    
    @staticmethod
    def reset_config():
        CONFIG.update(DEFAULT_CONFIG)
    
    # ============== 缓存 ==============
    def clear_cache(self):
        self._cache = {}
        
    def get_cache(self, key: str) -> Any:
        if CONFIG.get('cache_enabled'):
            return self._cache.get(key)
        return None
    
    def set_cache(self, key: str, value: Any):
        if CONFIG.get('cache_enabled'):
            self._cache[key] = value
    
    # ============== 统计 ==============
    def get_stats(self) -> dict:
        return self._stats.copy()
    
    def reset_stats(self):
        self._stats = {'reads': 0, 'writes': 0, 'errors': 0}
    
    # ============== 解析入口 ==============
    def parse(self, path: str, **kwargs):
        """自动识别格式并解析"""
        ext = os.path.splitext(path)[1].lower()
        
        if ext == '.csv' or ext == '.txt':
            return self.parse_csv(path, **kwargs)
        elif ext == '.json':
            return self.parse_json(path)
        elif ext in ['.xlsx', '.xls']:
            return self.parse_xlsx(path, **kwargs)
        elif ext == '.parquet':
            return self.parse_parquet(path)
        elif ext == '.sql':
            return self.parse_sql_insert(path)
        
        raise ValueError(f'Unsupported format: {ext}')
    
    # ============== CSV解析 ==============
    def parse_csv(self, path: str, **kwargs) -> 'pd.DataFrame':
        """解析CSV文件"""
        self._stats['reads'] += 1
        
        # 检测编码
        encoding = kwargs.get('encoding', self.detect_encoding(path))
        self.last_encoding = encoding
        
        # 读取
        try:
            df = pd.read_csv(path, encoding=encoding, **kwargs)
            return df
        except Exception as e:
            self.warnings.append(f'CSV解析失败: {path} - {str(e)[:50]}')
            self._stats['errors'] += 1
            raise
    
    # ============== JSON解析 ==============
    def parse_json(self, path: str) -> Union[Dict, List]:
        """解析JSON文件"""
        encoding = self.detect_encoding(path)
        
        with open(path, 'r', encoding=encoding, errors='ignore') as f:
            text = f.read()
        
        # 修复JSON
        text = self.fix_json(text)
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            self.warnings.append(f'JSON解析失败: {e}')
            raise
    
    def fix_json(self, text: str) -> str:
        """自动修复损坏的JSON"""
        # 移除BOM
        if text.startswith('\ufeff'):
            text = text[1:]
        
        # 修复单引号
        text = text.replace("'", '"')
        
        # 修复尾部逗号
        text = re.sub(r',\s*\]', ']', text)
        text = re.sub(r',\s*\}', '}', text)
        
        return text
    
    # ============== XLSX解析 ==============
    def parse_xlsx(self, path: str, sheet_name: str = None, **kwargs) -> 'pd.DataFrame':
        """解析XLSX文件"""
        self._stats['reads'] += 1
        
        # 检查是否损坏
        if not self.is_valid_xlsx(path):
            self.warnings.append(f'XLSX损坏: {path}')
            self._stats['errors'] += 1
            raise ValueError(f'Invalid XLSX: {path}')
        
        try:
            if sheet_name:
                df = pd.read_excel(path, sheet_name=sheet_name, engine='openpyxl')
            else:
                df = pd.read_excel(path, engine='openpyxl')
            return df
        except Exception as e:
            self.warnings.append(f'XLSX解析失败: {e}')
            raise
    
    def is_valid_xlsx(self, path: str) -> bool:
        """检查XLSX是否有效"""
        try:
            import zipfile
            return zipfile.is_zipfile(path)
        except:
            return False
    
    # ============== XLS解析 ==============
    def parse_xls(self, path: str, sheet_name: str = None, **kwargs) -> 'pd.DataFrame':
        """解析老格式XLS文件"""
        if xlrd is None:
            raise ImportError('xlrd not installed')
        
        wb = xlrd.open_workbook(path)
        
        if sheet_name:
            sheet = wb.sheet_by_name(sheet_name)
        else:
            sheet = wb.sheet_by_index(0)
        
        data = []
        for row in sheet.get_rows():
            data.append([cell.value for cell in row])
        
        return pd.DataFrame(data[1:], columns=data[0])
    
    # ============== Parquet解析 ==============
    def parse_parquet(self, path: str) -> 'pd.DataFrame':
        """解析Parquet文件"""
        if pq is None:
            raise ImportError('pyarrow not installed')
        
        return pq.read_table(path).to_pandas()
    
    # ============== SQL解析 ==============
    def parse_sql_insert(self, path: str) -> List[Dict]:
        """解析SQL INSERT语句"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        records = []
        pattern = r"INSERT INTO.*?VALUES\s*\((.*?)\)"
        
        for match in re.finditer(pattern, content, re.DOTALL):
            values = match.group(1)
            # 解析值
            record = {}
            records.append(record)
        
        return records
    
    # ============== 编码检测 ==============
    def detect_encoding(self, path: str) -> str:
        """自动检测文件编码"""
        if chardet is None:
            return 'utf-8'
        
        with open(path, 'rb') as f:
            raw = f.read(10000)
            result = chardet.detect(raw)
            return result['encoding'] or 'utf-8'
    
    # ============== CSV头检测 ==============
    def detect_csv_header(self, path: str) -> int:
        """检测CSV标题行数"""
        with open(path, 'r', encoding=self.detect_encoding(path)) as f:
            for i, line in enumerate(f, 1):
                if line.strip() and not line.startswith(','):
                    return i
        return 1
    
    # ============== 日期解析 ==============
    def parse_date(self, value: Any) -> str:
        """智能解析日期"""
        if pd.isna(value):
            return None
        
        s = str(value)
        
        # 时间戳
        if s.isdigit():
            try:
                return pd.to_datetime(int(s)).strftime('%Y-%m-%d')
            except:
                pass
        
        # 尝试多种格式
        for fmt in ['%Y-%m-%d', '%Y.%m.%d', '%Y/%m/%d', '%Y年%m月%d日']:
            try:
                return pd.to_datetime(s, format=fmt).strftime('%Y-%m-%d')
            except:
                continue
        
        return s
    
    # ============== 数值解析 ==============
    def parse_number(self, value: Any) -> Any:
        """智能解析数值"""
        if pd.isna(value):
            return None
        
        s = str(value).replace(',', '').replace('%', '')
        
        try:
            if '.' in s:
                return float(s)
            return int(s)
        except:
            return value
    
    # ============== 表尾过滤 ==============
    def filter_footer_rows(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """过滤表尾汇总行"""
        keywords = ['合计', '总计', '平均', '小计', 'total', 'sum', 'avg']
        
        for col in df.columns:
            if df[col].dtype == 'object':
                mask = df[col].astype(str).str.contains('|'.join(keywords), regex=True, na=False)
                df = df[~mask]
                break
        
        return df
    
    # ============== 列名标准化 ==============
    def normalize_columns(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """标准化列名"""
        mapping = {
            '日期': 'date', '交易日期': 'date', 'trading_date': 'date',
            '开盘价': 'open', '开盘': 'open', 'open_price': 'open',
            '收盘价': 'close', '收盘': 'close', 'close_price': 'close',
            '最高价': 'high', '最高': 'high', 'high_price': 'high',
            '最低价': 'low', '最低': 'low', 'low_price': 'low',
            '成交量': 'volume', '成交': 'volume', 'vol': 'volume',
            '持仓量': 'open_interest', '持仓': 'open_interest',
        }
        
        df = df.copy()
        df.columns = [mapping.get(c, c.lower()) for c in df.columns]
        
        return df
    
    # ============== 空列删除 ==============
    def drop_empty_columns(self, df: 'pd.DataFrame', threshold: float = 0.9) -> 'pd.DataFrame':
        """删除空值比例高的列"""
        empty_ratio = df.isna().mean()
        return df.drop(columns=empty_ratio[empty_ratio > threshold].index)
    
    # ============== 类型推断 ==============
    def infer_types(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """自动推断并转换类型"""
        df = df.copy()
        
        for col in df.columns:
            if df[col].dtype == 'object':
                # 尝试数值
                try:
                    df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='ignore')
                except:
                    pass
                
                # 尝试日期
                try:
                    df[col] = pd.to_datetime(df[col], errors='ignore')
                except:
                    pass
        
        return df
    
    # ============== 去重 ==============
    def find_duplicates(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """标记重复行"""
        df = df.copy()
        df['_is_duplicate'] = df.duplicated(keep=False)
        return df
    
    def remove_duplicates(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """删除重复行"""
        return df.drop_duplicates()
    
    # ============== 验证 ==============
    def validate_data(self, df: 'pd.DataFrame', required_columns: List[str] = None) -> dict:
        """验证数据"""
        result = {'valid': True, 'errors': [], 'stats': {}}
        
        if df is None or df.empty:
            result['valid'] = False
            result['errors'].append('DataFrame is empty')
            return result
        
        # 检查必填列
        if required_columns:
            missing = set(required_columns) - set(df.columns)
            if missing:
                result['valid'] = False
                result['errors'].append(f'Missing columns: {missing}')
        
        # 统计
        result['stats'] = {
            'rows': len(df),
            'columns': len(df.columns),
            'nulls': df.isna().sum().to_dict(),
        }
        
        return result
    
    # ============== 损坏检测 ==============
    def detect_corruption(self, path: str) -> dict:
        """检测文件是否损坏"""
        result = {'valid': True, 'errors': []}
        
        ext = os.path.splitext(path)[1].lower()
        
        if ext == '.xlsx':
            if not self.is_valid_xlsx(path):
                result['valid'] = False
                result['errors'].append('File is not a valid ZIP/XLSX')
        
        return result
    
    # ============== 多Sheet ==============
    def parse_xlsx_sheets(self, path: str) -> Dict[str, 'pd.DataFrame']:
        """解析XLSX所有Sheet"""
        wb = openpyxl.load_workbook(path)
        
        result = {}
        for sheet_name in wb.sheetnames:
            result[sheet_name] = pd.read_excel(path, sheet_name=sheet_name)
        
        return result
    
    # ============== 流式读取 ==============
    def stream_csv(self, path: str, chunk_size: int = None, **kwargs) -> List['pd.DataFrame']:
        """分块读取CSV"""
        if chunk_size is None:
            chunk_size = CONFIG.get('chunk_size', 50000)
        
        chunks = []
        for chunk in pd.read_csv(path, chunksize=chunk_size, **kwargs):
            chunks.append(chunk)
        
        return chunks
    
    # ============== 合并去重 ==============
    def merge_and_dedupe(self, paths: List[str]) -> 'pd.DataFrame':
        """合并多个文件并去重"""
        dfs = []
        for path in paths:
            df = self.parse(path)
            dfs.append(df)
        
        merged = pd.concat(dfs, ignore_index=True)
        return self.remove_duplicates(merged)
    
    # ============== XLSX转CSV ==============
    def xlsx_to_csv(self, input_path: str, output_path: str, 
                   encoding: str = 'utf-8-sig') -> str:
        """XLSX转CSV(解决中文编码)"""
        df = self.parse_xlsx(input_path)
        
        df.to_csv(output_path, index=False, encoding=encoding)
        
        self._stats['writes'] += 1
        
        return output_path
    
    # ============== URL读取 ==============
    def read_from_url(self, url: str, timeout: int = 30) -> str:
        """从URL读取内容"""
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=timeout) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            self.warnings.append(f'URL读取失败: {url}')
            self._stats['errors'] += 1
            raise
    
    def parse_from_url(self, url: str, timeout: int = 30):
        """直接从URL解析"""
        content = self.read_from_url(url, timeout)
        
        if url.endswith('.csv'):
            import io
            return pd.read_csv(io.StringIO(content))
        elif url.endswith('.json'):
            return json.loads(content)
        
        return content
    
    # ============== 并行处理 ==============
    def parse_parallel(self, file_paths: list, workers: int = 4, 
                     processor: Callable = None) -> list:
        """多进程并行解析"""
        from multiprocessing import Pool, cpu_count
        
        if workers <= 0:
            workers = cpu_count()
        
        with Pool(workers) as pool:
            results = pool.map(self.parse, file_paths)
        
        if processor:
            results = [processor(r) for r in results]
        
        return results
    
    # ============== 带重试解析 ==============
    @retry_on_error(max_retries=3, delay=1)
    def parse_with_retry(self, path: str, **kwargs):
        """带重试的解析"""
        self._stats['reads'] += 1
        
        cache_key = f'{path}:{kwargs.get("sheet_name", "default")}'
        cached = self.get_cache(cache_key)
        if cached is not None:
            return cached
        
        result = self.parse(path, **kwargs)
        self.set_cache(cache_key, result)
        
        return result
    
    # ============== 错误回退 ==============
    def parse_with_fallback(self, path: str, fallbacks: list = None):
        """尝试多种方式解析"""
        if fallbacks is None:
            fallbacks = ['parse_csv', 'parse_xlsx', 'parse_json']
        
        last_error = None
        for method_name in fallbacks:
            try:
                method = getattr(self, method_name)
                return method(path)
            except Exception as e:
                last_error = e
                continue
        
        self._stats['errors'] += 1
        raise last_error
    
    # ============== 脱敏 ==============
    def mask_sensitive(self, df: 'pd.DataFrame', columns: list = None) -> 'pd.DataFrame':
        """敏感字段脱敏"""
        if columns is None:
            columns = ['phone', 'tel', 'mobile', 'email', 'id_card', '身份证']
        
        df = df.copy()
        
        for col in df.columns:
            if any(kw in col.lower() for kw in columns):
                if any(k in col.lower() for k in ['phone', 'tel', 'mobile']):
                    df[col] = df[col].astype(str).str.replace(r'(\d{3})\d{4}(\d{4})', r'\1****\2', regex=True)
                elif 'email' in col.lower():
                    df[col] = df[col].astype(str).str.replace(r'(.).*(@.*)', r'\1***\2', regex=True)
                elif 'id' in col.lower():
                    df[col] = df[col].astype(str).str.replace(r'(\d{4})\d{10}(\d{4})', r'\1**********\2', regex=True)
        
        return df
    
    # ============== 增量对比 ==============
    def get_new_records(self, old_path: str, new_path: str, 
                     key_columns: list = None) -> 'pd.DataFrame':
        """获取增量数据"""
        old_df = self.parse(old_path) if old_path else None
        new_df = self.parse(new_path)
        
        if new_df is None or new_df.empty:
            return new_df
        
        if old_df is None or old_df.empty:
            return new_df
        
        if key_columns:
            valid_keys = [k for k in key_columns if k in new_df.columns and k in old_df.columns]
            if valid_keys:
                merged = new_df.merge(old_df, on=valid_keys, how='left', indicator=True)
                return merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
        
        return new_df
    
    # ============== 模板导出 ==============
    def export_template(self, output_path: str, schema: dict):
        """生成模板文件"""
        data = {}
        for col, col_type in schema.items():
            if col_type == 'int':
                data[col] = []
            elif col_type == 'float':
                data[col] = []
            elif col_type == 'date':
                data[col] = pd.to_datetime([])
            else:
                data[col] = []
        
        df = pd.DataFrame(data)
        
        ext = output_path.split('.')[-1].lower()
        if ext == 'csv':
            df.to_csv(output_path, index=False)
        elif ext in ['xlsx', 'xls']:
            df.to_excel(output_path, index=False)
        
        return output_path
    
    # ============== 一键清洗 ==============
    def clean_pipeline(self, path: str, config: dict = None) -> 'pd.DataFrame':
        """一键数据清洗"""
        if config is None:
            config = {}
        
        df = self.parse(path)
        
        if df is None:
            return None
        
        # 过滤表尾
        if config.get('filter_footer', True):
            df = self.filter_footer_rows(df)
        
        # 删除空列
        if config.get('drop_empty_cols', True):
            df = self.drop_empty_columns(df)
        
        # 类型推断
        if config.get('infer_types', True):
            df = self.infer_types(df)
        
        # 列名标准化
        if config.get('normalize_cols', True):
            df = self.normalize_columns(df)
        
        # 去重
        if config.get('drop_duplicates', True):
            df = self.remove_duplicates(df)
        
        return df
    
    # ============== 警告 ==============
    def get_warnings(self) -> List[str]:
        return self.warnings
    
    def clear_warnings(self):
        self.warnings = []
    
    # ============== 批量转换 ==============
    @staticmethod
    def convert_folder(input_dir: str, output_format: str = 'csv', 
                   output_dir: str = None):
        """批量转换文件夹"""
        parser = DataParser()
        
        if output_dir is None:
            output_dir = input_dir + '_converted'
        
        os.makedirs(output_dir, exist_ok=True)
        
        count = 0
        for root, dirs, files in os.walk(input_dir):
            for f in files:
                input_path = os.path.join(root, f)
                ext = os.path.splitext(f)[1].lower()
                
                if ext == '.xlsx':
                    rel_path = os.path.relpath(input_path, input_dir)
                    output_path = os.path.join(output_dir, rel_path)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    new_ext = f'.{output_format}'
                    output_path = os.path.splitext(output_path)[0] + new_ext
                    
                    parser.xlsx_to_csv(input_path, output_path)
                    count += 1
        
        return count


# 如果直接运行
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
        parser = DataParser()
        
        print(f'Parsing: {path}')
        df = parser.parse(path)
        print(f'Rows: {len(df)}')
        print(f'Columns: {list(df.columns)[:5]}')
    else:
        print('DataParser skill loaded')