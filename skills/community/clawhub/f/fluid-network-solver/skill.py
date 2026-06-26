import sys
import json
from src.parser import load_toml
from src.solver import Solver
from src.analyzer import Analyzer

def solve_network(toml_string: str, scenario: str = None) -> dict:
    """
    输入 TOML 字符串和工况名（可选），返回求解结果和分析报告（字典）
    """
    net = load_toml(toml_string)
    solver = Solver(net)
    if scenario and scenario in net.scenarios:
        net_scenario = solver.apply_scenario(scenario)
    else:
        net_scenario = net
    result = solver.solve_linear(net_scenario)
    # 将 numpy 类型转换为 Python 原生类型
    pressures = {k: float(v) for k, v in result['pressures'].items()}
    flows = {f"{k[0]}->{k[1]}": float(v) for k, v in result['flows'].items()}
    analyzer = Analyzer(net)
    report = analyzer.analyze(result)
    # 分析报告中的 flow 和 pressure 也是 numpy 类型，转换为 float
    for load_id, info in report['loads'].items():
        if 'flow' in info:
            info['flow'] = float(info['flow'])
        if 'pressure' in info and info['pressure'] is not None:
            info['pressure'] = float(info['pressure'])
    return {
        'pressures': pressures,
        'flows': flows,
        'analysis': report
    }

if __name__ == '__main__':
    # 从标准输入读取 JSON
    data = json.load(sys.stdin)
    toml_str = data.get('toml')
    scenario = data.get('scenario')
    if not toml_str:
        print(json.dumps({'error': 'Missing toml field'}))
        sys.exit(1)
    try:
        output = solve_network(toml_str, scenario)
        print(json.dumps(output))
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)