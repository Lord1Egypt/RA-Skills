#!/usr/bin/env python3
"""Data Parser Enhanced - 数据解析增强"""

import os
import json
import csv
import io
import zipfile
import tarfile
from datetime import datetime


# ==================== 压缩文件支持 ====================
class ArchiveParser:
    """压缩文件解析"""
    
    def parse_zip(self, path, file_pattern=None):
        """解析ZIP"""
        results = []
        with zipfile.ZipFile(path, 'r') as zf:
            for name in zf.namelist():
                if file_pattern and file_pattern not in name:
                    continue
                if not name.endswith('/'):
                    results.append({
                        'name': name,
                        'size': zf.getinfo(name).file_size,
                        'data': zf.read(name)
                    })
        return results
    
    def parse_tar(self, path, file_pattern=None):
        """解析TAR"""
        results = []
        with tarfile.open(path, 'r') as tf:
            for member in tf.getmembers():
                if file_pattern and file_pattern not in member.name:
                    continue
                if member.isfile():
                    results.append({
                        'name': member.name,
                        'size': member.size,
                        'data': tf.extractfile(member).read()
                    })
        return results
    
    def list_contents(self, path):
        """列出内容"""
        results = []
        if path.endswith('.zip'):
            with zipfile.ZipFile(path, 'r') as zf:
                results = zf.namelist()
        elif path.endswith(('.tar', '.tar.gz', '.tgz')):
            with tarfile.open(path, 'r') as tf:
                results = [m.name for m in tf.getmembers()]
        return results


# ==================== XML解析 ====================
class XMLParser:
    """XML解析"""
    
    def parse(self, content):
        """解析XML"""
        try:
            import xml.etree.ElementTree as ET
            return ET.fromstring(content)
        except:
            return None
    
    def to_dict(self, element):
        """XML转字典"""
        result = {}
        if element.text and element.text.strip():
            return element.text
        for child in element:
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(self.to_dict(child))
            else:
                result[child.tag] = self.to_dict(child)
        return result


# ==================== YAML解析 ====================
class YAMLParser:
    """YAML解析"""
    
    def parse(self, content):
        """解析YAML"""
        try:
            import yaml
            return yaml.safe_load(content)
        except ImportError:
            return self._simple_parse(content)
    
    def _simple_parse(self, content):
        """简单解析"""
        result = {}
        for line in content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip()
        return result


# ==================== INI文件解析 ====================
class INIParser:
    """INI文件解析"""
    
    def parse(self, content):
        """解析INI"""
        result = {}
        section = 'default'
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                result[section] = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                if section not in result:
                    result[section] = {}
                result[section][key.strip()] = value.strip()
        return result


# ==================== 固定宽度文件 ====================
class FixedWidthParser:
    """固定宽度文件解析"""
    
    def parse(self, lines, widths):
        """解析固定宽度文件"""
        results = []
        for line in lines:
            if len(line) >= sum(widths):
                row = []
                pos = 0
                for width in widths:
                    row.append(line[pos:pos+width].strip())
                    pos += width
                results.append(row)
        return results


# ==================== 数据验证器 ====================
class DataValidator:
    """数据验证"""
    
    def __init__(self):
        self.rules = []
    
    def add_rule(self, column, rule_type, value):
        """添加验证规则"""
        self.rules.append({'column': column, 'type': rule_type, 'value': value})
    
    def validate(self, df):
        """验证数据"""
        errors = []
        for rule in self.rules:
            col = rule['column']
            if col not in df.columns:
                errors.append(f"Column {col} not found")
                continue
            
            if rule['type'] == 'not_null':
                nulls = df[df[col].isnull()]
                if len(nulls) > 0:
                    errors.append(f"{col} has {len(nulls)} null values")
            
            elif rule['type'] == 'unique':
                duplicates = df[df[col].duplicated()]
                if len(duplicates) > 0:
                    errors.append(f"{col} has {len(duplicates)} duplicates")
            
            elif rule['type'] == 'min':
                if df[col].min() < rule['value']:
                    errors.append(f"{col} below minimum {rule['value']}")
            
            elif rule['type'] == 'max':
                if df[col].max() > rule['value']:
                    errors.append(f"{col} above maximum {rule['value']}")
        
        return errors
    
    def validate_csv(self, path):
        """验证CSV"""
        import pandas as pd
        df = pd.read_csv(path)
        return self.validate(df)


# ==================== 数据采样 ====================
class DataSampler:
    """数据采样"""
    
    def random_sample(self, df, n=None, frac=None):
        """随机采样"""
        return df.sample(n=n, frac=frac) if hasattr(df, 'sample') else df
    
    def stratified_sample(self, df, column, n):
        """分层采样"""
        return df.groupby(column).apply(lambda x: x.sample(n=min(n, len(x))))
    
    def time_sample(self, df, freq):
        """时间采样"""
        if hasattr(df, 'resample'):
            return df.resample(freq).mean()
        return df


# ==================== 数据统计 ====================
class DataStats:
    """数据统计"""
    
    def basic_stats(self, df):
        """基本统计"""
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'memory': df.memory_usage(deep=True).sum() if hasattr(df, 'memory_usage') else 0,
            'null_counts': df.isnull().sum().to_dict() if hasattr(df, 'isnull') else {},
        }
    
    def column_stats(self, df, column):
        """列统计"""
        return {
            'mean': df[column].mean() if hasattr(df[column], 'mean') else None,
            'median': df[column].median() if hasattr(df[column], 'median') else None,
            'std': df[column].std() if hasattr(df[column], 'std') else None,
            'min': df[column].min() if hasattr(df[column], 'min') else None,
            'max': df[column].max() if hasattr(df[column], 'max') else None,
        }
    
    def outlier_detection(self, df, column, method='iqr'):
        """异常值检测"""
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[column] < Q1 - 1.5*IQR) | (df[column] > Q3 + 1.5*IQR)]
            return outliers
        return df


if __name__ == "__main__":
    print("Data Parser Enhanced loaded")