#!/usr/bin/env python3
"""
数据源 Schema 解析脚本

功能：
1. 读取 CSV/Excel 文件
2. 分析前N行数据，推断每列的数据类型
3. 区分维度（dimension）和度量（measure）字段
4. 生成 JSON schema 配置文件

使用方式：
python scripts/data_schema_parser.py --file data.csv --preview-rows 10
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

try:
    import pandas as pd
except ImportError:
    print("错误：需要安装 pandas 库")
    print("安装命令：pip install pandas openpyxl")
    sys.exit(1)


def infer_column_type(series: pd.Series) -> str:
    """
    推断列的数据类型

    Args:
        series: pandas Series

    Returns:
        数据类型字符串：'numeric', 'date', 'string', 'boolean'
    """
    # 尝试转为数值
    try:
        pd.to_numeric(series, errors='raise')
        return 'numeric'
    except (ValueError, TypeError):
        pass

    # 尝试转为日期（抑制警告）
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=UserWarning)
            pd.to_datetime(series, errors='raise')
        return 'date'
    except (ValueError, TypeError):
        pass

    # 尝试转为布尔值
    unique_values = series.dropna().unique()
    if len(unique_values) <= 2 and all(
        str(v).lower() in ['true', 'false', 'yes', 'no', '1', '0']
        for v in unique_values
    ):
        return 'boolean'

    # 默认为字符串
    return 'string'


def categorize_column(name: str, dtype: str, unique_count: int, total_count: int) -> str:
    """
    列别字段是维度（dimension）还是度量（measure）

    Args:
        name: 列名
        dtype: 数据类型
        unique_count: 唯一值数量
        total_count: 总行数

    Returns:
        'dimension' 或 'measure'
    """
    # 基于启发式规则判断
    if dtype == 'date':
        return 'dimension'
    elif dtype == 'string':
        return 'dimension'
    elif dtype == 'boolean':
        return 'dimension'
    elif dtype == 'numeric':
        # 数值类型的判断逻辑
        # 如果唯一值比例很小（如少于 10%），可能是分类字段
        unique_ratio = unique_count / total_count if total_count > 0 else 0

        # 检查列名是否包含维度关键词
        dimension_keywords = ['id', 'code', 'type', 'name', 'category', 'region', 'level', 'grade']
        if any(keyword in name.lower() for keyword in dimension_keywords):
            return 'dimension'

        # 如果唯一值很少，可能是分类字段
        if unique_ratio < 0.1 or unique_count < 10:
            return 'dimension'

        # 检查列名是否包含度量关键词
        measure_keywords = [
            'amount', 'count', 'value', 'price', 'cost', 'revenue', 'sales',
            'profit', 'rate', 'ratio', 'percent', 'growth', 'increase',
            'quantity', 'volume', 'weight', 'score', 'time', 'duration',
            '金额', '数量', '占比', '率', '增长', '销量', '收入', '成本'
        ]
        if any(keyword in name.lower() for keyword in measure_keywords):
            return 'measure'

        # 默认：如果是数值型且唯一值较多，视为度量
        return 'measure'

    return 'dimension'


def parse_data_file(file_path: str, preview_rows: int = 10) -> Dict[str, Any]:
    """
    解析数据文件并生成 schema

    Args:
        file_path: 文件路径
        preview_rows: 预览行数

    Returns:
        schema 字典
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    # 根据文件扩展名选择读取方式
    file_ext = path.suffix.lower()

    try:
        if file_ext == '.csv':
            df = pd.read_csv(file_path, nrows=preview_rows)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, nrows=preview_rows)
        else:
            raise ValueError(f"不支持的文件格式：{file_ext}")
    except Exception as e:
        raise Exception(f"读取文件失败：{e}")

    if df.empty:
        raise ValueError("文件为空或无法解析")

    # 分析每一列
    columns = []
    for col_name in df.columns:
        series = df[col_name]

        # 去除空值进行推断
        series_nonnull = series.dropna()
        unique_count = len(series_nonnull.unique())

        # 推断数据类型
        dtype = infer_column_type(series_nonnull)

        # 分类维度或度量
        category = categorize_column(col_name, dtype, unique_count, len(series))

        # 生成列描述
        column_info = {
            "name": str(col_name),
            "type": dtype,
            "category": category,
            "description": "",
            "unique_count": unique_count,
            "sample_values": list(series_nonnull.head(3).astype(str).tolist())
        }

        columns.append(column_info)

    # 生成 schema
    schema = {
        "data_source": str(file_path),
        "file_type": file_ext,
        "total_columns": len(columns),
        "preview_rows": len(df),
        "schema": {
            "columns": columns
        },
        "sample_data": df.head(3).fillna("").to_dict('records')
    }

    return schema


def main():
    parser = argparse.ArgumentParser(
        description='数据源 Schema 解析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  python scripts/data_schema_parser.py --file data.csv
  python scripts/data_schema_parser.py --file data.xlsx --preview-rows 20
  python scripts/data_schema_parser.py --file data.csv --output schema.json
        """
    )

    parser.add_argument(
        '--file',
        required=True,
        help='数据文件路径（支持 CSV、Excel）'
    )

    parser.add_argument(
        '--preview-rows',
        type=int,
        default=10,
        help='预览行数（默认：10）'
    )

    parser.add_argument(
        '--output',
        help='输出文件路径（默认：打印到控制台）'
    )

    args = parser.parse_args()

    try:
        # 解析数据文件
        schema = parse_data_file(args.file, args.preview_rows)

        # 输出结果
        output_json = json.dumps(schema, ensure_ascii=False, indent=2)

        if args.output:
            # 写入文件
            output_path = Path(args.output)
            output_path.write_text(output_json, encoding='utf-8')
            print(f"Schema 配置已保存到：{args.output}")
        else:
            # 打印到控制台
            print(output_json)

    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
