import sys
import json
import argparse
from .parser import load_toml
from .solver import Solver
from .analyzer import Analyzer

def main():
    parser = argparse.ArgumentParser(description='流体网络求解器')
    parser.add_argument('file', help='TOML 文件路径')
    parser.add_argument('--scenario', '-s', help='指定工况名', default=None)
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    args = parser.parse_args()

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            toml_str = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)

    try:
        net = load_toml(toml_str)
    except Exception as e:
        print(f"解析 TOML 失败: {e}")
        sys.exit(1)

    solver = Solver(net)
    if args.scenario:
        net_scenario = solver.apply_scenario(args.scenario)
    else:
        if net.scenarios:
            first_scenario = next(iter(net.scenarios))
            net_scenario = solver.apply_scenario(first_scenario)
        else:
            net_scenario = net

    result = solver.solve_linear(net_scenario)
    analyzer = Analyzer(net)
    report = analyzer.analyze(result, net_scenario)

    output = {
        'pressures': result['pressures'],
        'flows': {f"{k[0]}->{k[1]}": v for k, v in result['flows'].items()},
        'analysis': report
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print("=== 压力分布 ===")
        for node, p in result['pressures'].items():
            print(f"{node}: {p:.4f}")
        print("\n=== 流量分布 ===")
        for (f,t), q in result['flows'].items():
            print(f"{f} -> {t}: {q:.4f}")
        print("\n=== 分析报告 ===")
        for load_id, info in report['loads'].items():
            status = info['status']
            p = info['pressure']
            q = info['flow']
            reasons = info['reasons']
            connected = info.get('connected', False)
            print(f"{load_id}: 状态={status}, 压力={p:.4f}, 流量={q:.4f}, 连通={'是' if connected else '否'}" + (f", 原因={reasons}" if reasons else ""))
        print("\n=== 连通性 ===")
        for load_id, connected in report.get('connectivity', {}).items():
            print(f"{load_id}: {'连通' if connected else '不连通'}")

if __name__ == '__main__':
    main()