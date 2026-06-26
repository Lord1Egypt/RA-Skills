#!/usr/bin/env python3
"""
执行Excel数据查询
用法: python query_data.py <文件路径> <sheet名> '<查询JSON>'
输出: JSON格式，包含查询结果、统计信息

查询JSON格式:
{
  "filters": [{"column": "列名", "operator": "==|!=|>|<|>=|<=|contains", "value": "值"}],
  "groupby": ["列名1", "列名2"],
  "aggregations": [{"column": "列名", "func": "sum|mean|count|max|min", "alias": "别名"}],
  "sort": [{"column": "列名", "asc": true|false}],
  "limit": 100
}
"""

import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta


def parse_date(value):
    """解析日期表达式"""
    if isinstance(value, str):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if value == "今天":
            return today
        elif value == "昨天":
            return today - timedelta(days=1)
        elif value.endswith("天前"):
            days = int(value.replace("天前", ""))
            return today - timedelta(days=days)
        elif value == "本周":
            return today - timedelta(days=today.weekday())
        elif value == "上周":
            return today - timedelta(days=today.weekday() + 7)
        elif value == "本月":
            return today.replace(day=1)
        elif value == "上月":
            if today.month == 1:
                return today.replace(year=today.year - 1, month=12, day=1)
            return today.replace(month=today.month - 1, day=1)
    
    return value


def apply_filters(df, filters):
    """应用筛选条件"""
    for f in filters:
        col = f["column"]
        op = f["operator"]
        val = parse_date(f["value"])
        
        if op == "==":
            df = df[df[col] == val]
        elif op == "!=":
            df = df[df[col] != val]
        elif op == ">":
            df = df[df[col] > val]
        elif op == "<":
            df = df[df[col] < val]
        elif op == ">=":
            df = df[df[col] >= val]
        elif op == "<=":
            df = df[df[col] <= val]
        elif op == "contains":
            df = df[df[col].astype(str).str.contains(str(val), na=False)]
    
    return df


def apply_aggregation(df, groupby, aggregations):
    """应用聚合"""
    if not aggregations:
        return df
    
    agg_dict = {}
    for agg in aggregations:
        col = agg["column"]
        func = agg["func"]
        alias = agg.get("alias", f"{col}_{func}")
        agg_dict[col] = func
    
    if groupby:
        result = df.groupby(groupby).agg(agg_dict).reset_index()
        # 重命名列
        if len(aggregations) == 1:
            result.columns = groupby + [aggregations[0].get("alias", aggregations[0]["column"])]
        else:
            # 处理多列聚合的列名
            new_cols = groupby[:]
            for agg in aggregations:
                new_cols.append(agg.get("alias", f"{agg['column']}_{agg['func']}"))
            result.columns = new_cols[:len(result.columns)]
    else:
        result = df.agg(agg_dict).to_frame().T
    
    return result


def format_value(val):
    """格式化数值"""
    if pd.isna(val):
        return "-"
    elif isinstance(val, (int, np.integer)):
        return f"{val:,}"
    elif isinstance(val, (float, np.floating)):
        return f"{val:,.2f}"
    elif isinstance(val, pd.Timestamp):
        return val.strftime("%Y-%m-%d")
    else:
        return str(val)


def generate_insights(df, query):
    """生成数据洞察"""
    insights = []
    
    if len(df) == 0:
        return ["暂无数据"]
    
    # 数值列分析
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col in query.get("groupby", []):
            continue
        
        mean_val = df[col].mean()
        max_val = df[col].max()
        min_val = df[col].min()
        
        insights.append(f"{col}平均: {format_value(mean_val)}, 最高: {format_value(max_val)}, 最低: {format_value(min_val)}")
    
    # 趋势分析（如果有日期列）
    date_cols = [c for c in df.columns if '日期' in c or '时间' in c or 'date' in c.lower()]
    if date_cols and len(df) > 1:
        date_col = date_cols[0]
        numeric_col = numeric_cols[0] if len(numeric_cols) > 0 else None
        
        if numeric_col:
            first_val = df.iloc[0][numeric_col]
            last_val = df.iloc[-1][numeric_col]
            if first_val != 0:
                change_pct = (last_val - first_val) / first_val * 100
                trend = "上升" if change_pct > 0 else "下降"
                insights.append(f"整体趋势: {trend} {abs(change_pct):.1f}%")
    
    return insights if insights else ["数据已展示"]


def query_data(file_path, sheet_name, query_json):
    """执行数据查询"""
    start_time = datetime.now()
    
    try:
        # 读取数据
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        total_rows = len(df)
        
        # 清理数据
        df = df.dropna(how='all')
        df.columns = df.columns.astype(str).str.strip()
        
        # 尝试转换日期列
        for col in df.columns:
            if '日期' in col or '时间' in col or 'date' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
        
        # 应用筛选
        filters = query_json.get("filters", [])
        if filters:
            df = apply_filters(df, filters)
        
        filtered_rows = len(df)
        
        # 应用聚合
        groupby = query_json.get("groupby", [])
        aggregations = query_json.get("aggregations", [])
        if groupby or aggregations:
            df = apply_aggregation(df, groupby, aggregations)
        
        # 应用排序
        sort_rules = query_json.get("sort", [])
        for rule in sort_rules:
            col = rule["column"]
            asc = rule.get("asc", True)
            df = df.sort_values(by=col, ascending=asc)
        
        # 应用限制
        limit = query_json.get("limit", 1000)
        df = df.head(limit)
        
        # 计算耗时
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # 格式化结果
        result_data = []
        for _, row in df.iterrows():
            result_data.append({k: format_value(v) for k, v in row.items()})
        
        # 生成洞察
        insights = generate_insights(df, query_json)
        
        return {
            "success": True,
            "query": query_json,
            "stats": {
                "total_rows": total_rows,
                "filtered_rows": filtered_rows,
                "result_rows": len(df),
                "elapsed_seconds": round(elapsed, 3)
            },
            "columns": list(df.columns),
            "data": result_data,
            "insights": insights
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({
            "success": False,
            "error": "用法: python query_data.py <文件路径> <sheet名> '<查询JSON>'"
        }, ensure_ascii=False))
        sys.exit(1)
    
    file_path = sys.argv[1]
    sheet_name = sys.argv[2]
    query_json = json.loads(sys.argv[3])
    
    result = query_data(file_path, sheet_name, query_json)
    print(json.dumps(result, ensure_ascii=False, default=str))
