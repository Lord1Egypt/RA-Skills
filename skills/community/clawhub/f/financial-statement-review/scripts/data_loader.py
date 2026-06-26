"""
数据加载模块 - 加载会计准则、税法规定、检查清单等数据
"""
import csv
import os
from typing import Dict, List, Any

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
REFERENCES_DIR = os.path.join(os.path.dirname(__file__), '..', 'references')


def load_csv_data(filename: str) -> List[Dict[str, str]]:
    """加载CSV数据文件"""
    filepath = os.path.join(DATA_DIR, filename)
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"加载文件 {filename} 出错: {e}")
        return []


def load_accounting_standards() -> List[Dict[str, str]]:
    """加载会计准则数据"""
    return load_csv_data('accounting_standards.csv')


def load_tax_risk_indicators() -> List[Dict[str, str]]:
    """加载税务风险指标数据"""
    return load_csv_data('tax_risk_indicators.csv')


def load_review_checklists() -> List[Dict[str, str]]:
    """加载审查检查清单"""
    return load_csv_data('review_checklists.csv')


def load_financial_anomalies() -> List[Dict[str, str]]:
    """加载财务异常指标数据"""
    return load_csv_data('financial_anomalies.csv')


def get_accounting_standard_by_code(code: str) -> Dict[str, str]:
    """根据准则编号获取会计准则信息"""
    standards = load_accounting_standards()
    for standard in standards:
        if standard.get('准则编号') == code:
            return standard
    return {}


def get_accounting_standard_by_name(name: str) -> Dict[str, str]:
    """根据准则名称获取会计准则信息"""
    standards = load_accounting_standards()
    for standard in standards:
        if name in standard.get('准则名称', ''):
            return standard
    return {}


def get_tax_risks_by_type(tax_type: str) -> List[Dict[str, str]]:
    """根据税种获取税务风险指标"""
    risks = load_tax_risk_indicators()
    return [r for r in risks if r.get('税种') == tax_type]


def get_high_risk_indicators() -> List[Dict[str, str]]:
    """获取高风险指标"""
    risks = load_tax_risk_indicators()
    return [r for r in risks if r.get('风险等级') == '高']


def get_review_checklist_by_phase(phase: str) -> List[Dict[str, str]]:
    """根据审查阶段获取检查清单"""
    checklists = load_review_checklists()
    return [c for c in checklists if c.get('审查阶段') == phase]


def search_anomalies_by_type(anomaly_type: str) -> List[Dict[str, str]]:
    """根据异常类型搜索财务异常指标"""
    anomalies = load_financial_anomalies()
    return [a for a in anomalies if anomaly_type in a.get('异常类型', '')]


def load_reference_file(filename: str) -> str:
    """加载参考文档内容"""
    filepath = os.path.join(REFERENCES_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return f"读取文件出错: {e}"


if __name__ == '__main__':
    # 测试数据加载
    print("=== 会计准则示例 ===")
    standards = load_accounting_standards()
    for s in standards[:3]:
        print(f"{s['准则编号']}: {s['准则名称']}")
    
    print("\n=== 高风险税务指标 ===")
    high_risks = get_high_risk_indicators()
    for r in high_risks[:3]:
        print(f"[{r['税种']}] {r['风险指标']}")
