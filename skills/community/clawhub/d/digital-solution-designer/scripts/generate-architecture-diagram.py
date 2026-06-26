#!/usr/bin/env python3
"""
架构图生成脚本

功能：将 Graphviz DOT 格式的架构描述转换为可视化图表（PNG/SVG/PDF）
支持类型：业务架构图、功能架构图、数据架构图、技术架构图、流程图
支持特性：子图（subgraph）、样式（style）、颜色（color）、层级（rank）

使用方式：
    python generate-architecture-diagram.py --diagram-type business --input business.dot --output business.png
    python generate-architecture-diagram.py --diagram-type functional --input functional.dot --output functional.svg
    python generate-architecture-diagram.py --template business-4layer --output business.png
"""

import argparse
import json
import os
import re
import sys
from graphviz import Digraph, Source


# 中文字体映射
FONT_MAP = {
    'linux': 'WenQuanYi Micro Hei',
    'darwin': 'PingFang SC',
    'win32': 'Microsoft YaHei',
    'windows': 'Microsoft YaHei',
}

def get_chinese_font():
    """根据操作系统返回支持中文的字体名称"""
    platform = sys.platform.lower()
    for key, font in FONT_MAP.items():
        if key in platform:
            return font
    return 'SimHei'  # 默认中文字体


# 预设架构图模板
TEMPLATES = {
    'business-4layer': {
        'name': '四层业务架构图',
        'description': '战略层→业务域层→业务能力层→业务流程层',
        'dot': '''digraph G {{
    rankdir=TB;
    node [shape=box, style="rounded,filled"];

    subgraph cluster_strategy {{
        label="战略层";
        style=dashed;
        bgcolor="#E8F0FE";
        s1 [label="战略目标1"];
        s2 [label="战略目标2"];
    }}

    subgraph cluster_domain {{
        label="业务域层";
        style=dashed;
        bgcolor="#E6F4EA";
        d1 [label="业务域A"];
        d2 [label="业务域B"];
        d3 [label="业务域C"];
    }}

    subgraph cluster_capability {{
        label="业务能力层";
        style=dashed;
        bgcolor="#FFF3E0";
        c1 [label="能力1"];
        c2 [label="能力2"];
        c3 [label="能力3"];
        c4 [label="能力4"];
    }}

    subgraph cluster_process {{
        label="业务流程层";
        style=dashed;
        bgcolor="#FCE4EC";
        p1 [label="流程1"];
        p2 [label="流程2"];
        p3 [label="流程3"];
    }}

    s1 -> d1;
    s1 -> d2;
    s2 -> d2;
    s2 -> d3;
    d1 -> c1;
    d1 -> c2;
    d2 -> c2;
    d2 -> c3;
    d3 -> c3;
    d3 -> c4;
    c1 -> p1;
    c2 -> p1;
    c2 -> p2;
    c3 -> p2;
    c3 -> p3;
    c4 -> p3;
}}'''
    },
    'functional-3layer': {
        'name': '三层功能架构图',
        'description': '展现层→应用层→数据层',
        'dot': '''digraph G {{
    rankdir=TB;
    node [shape=box, style="rounded,filled"];

    subgraph cluster_presentation {{
        label="展现层";
        style=dashed;
        bgcolor="#E8F0FE";
        web [label="Web端"];
        app [label="APP端"];
        mini [label="小程序"];
    }}

    subgraph cluster_application {{
        label="应用层";
        style=dashed;
        bgcolor="#E6F4EA";
        mod1 [label="核心业务模块"];
        mod2 [label="支撑服务模块"];
        mod3 [label="管理后台模块"];
    }}

    subgraph cluster_data {{
        label="数据层";
        style=dashed;
        bgcolor="#FFF3E0";
        db [label="数据库"];
        cache [label="缓存"];
        mq [label="消息队列"];
    }}

    web -> mod1;
    web -> mod2;
    app -> mod1;
    app -> mod3;
    mini -> mod1;
    mod1 -> db;
    mod1 -> cache;
    mod2 -> db;
    mod2 -> mq;
    mod3 -> db;
}}'''
    },
    'data-flow': {
        'name': '数据流架构图',
        'description': '数据采集→数据存储→数据处理→数据应用',
        'dot': '''digraph G {{
    rankdir=LR;
    node [shape=box, style="rounded,filled"];

    subgraph cluster_collect {{
        label="数据采集";
        style=dashed;
        bgcolor="#E8F0FE";
        src1 [label="业务系统"];
        src2 [label="IoT设备"];
        src3 [label="外部数据"];
    }}

    subgraph cluster_storage {{
        label="数据存储";
        style=dashed;
        bgcolor="#E6F4EA";
        dw [label="数据仓库"];
        dl [label="数据湖"];
        db [label="业务数据库"];
    }}

    subgraph cluster_process {{
        label="数据处理";
        style=dashed;
        bgcolor="#FFF3E0";
        etl [label="ETL"];
        quality [label="数据质量"];
        gov [label="数据治理"];
    }}

    subgraph cluster_app {{
        label="数据应用";
        style=dashed;
        bgcolor="#FCE4EC";
        report [label="报表分析"];
        bi [label="BI可视化"];
        ai [label="智能分析"];
    }}

    src1 -> etl;
    src2 -> etl;
    src3 -> etl;
    etl -> quality;
    quality -> gov;
    gov -> dw;
    gov -> dl;
    dw -> report;
    dw -> bi;
    dl -> ai;
    dl -> bi;
}}'''
    },
    'technical-microservice': {
        'name': '微服务技术架构图',
        'description': '接入层→网关层→服务层→中间件层→基础设施层',
        'dot': '''digraph G {{
    rankdir=TB;
    node [shape=box, style="rounded,filled"];

    subgraph cluster_access {{
        label="接入层";
        style=dashed;
        bgcolor="#E8F0FE";
        lb [label="负载均衡"];
        cdn [label="CDN"];
    }}

    subgraph cluster_gateway {{
        label="网关层";
        style=dashed;
        bgcolor="#E6F4EA";
        gw [label="API网关"];
        auth [label="认证授权"];
    }}

    subgraph cluster_service {{
        label="服务层";
        style=dashed;
        bgcolor="#FFF3E0";
        svc1 [label="业务服务A"];
        svc2 [label="业务服务B"];
        svc3 [label="基础服务"];
    }}

    subgraph cluster_middleware {{
        label="中间件层";
        style=dashed;
        bgcolor="#F3E5F5";
        reg [label="服务注册"];
        cfg [label="配置中心"];
        mq [label="消息队列"];
    }}

    subgraph cluster_infra {{
        label="基础设施层";
        style=dashed;
        bgcolor="#FCE4EC";
        k8s [label="容器平台"];
        monitor [label="监控告警"];
        log [label="日志中心"];
    }}

    lb -> gw;
    cdn -> gw;
    gw -> auth;
    gw -> svc1;
    gw -> svc2;
    gw -> svc3;
    svc1 -> reg;
    svc1 -> cfg;
    svc1 -> mq;
    svc2 -> reg;
    svc2 -> mq;
    svc3 -> cfg;
    k8s -> svc1 [style=dashed];
    k8s -> svc2 [style=dashed];
    k8s -> svc3 [style=dashed];
    monitor -> log [style=dashed];
}}'''
    },
    'gov-cloud': {
        'name': '政务云架构图',
        'description': '公众层→政务外网→业务应用层→数据共享层→基础设施层',
        'dot': '''digraph G {{
    rankdir=TB;
    node [shape=box, style="rounded,filled"];

    subgraph cluster_public {{
        label="公众服务层";
        style=dashed;
        bgcolor="#E8F0FE";
        portal [label="政务门户"];
        mini [label="政务小程序"];
        app [label="政务APP"];
    }}

    subgraph cluster_network {{
        label="政务外网";
        style=dashed;
        bgcolor="#E6F4EA";
        firewall [label="防火墙"];
        waf [label="WAF"];
    }}

    subgraph cluster_biz {{
        label="业务应用层";
        style=dashed;
        bgcolor="#FFF3E0";
        oneNet [label="一网通办"];
        oneSupervise [label="一网统管"];
        dataOpen [label="数据开放"];
    }}

    subgraph cluster_data {{
        label="数据共享层";
        style=dashed;
        bgcolor="#F3E5F5";
        exchange [label="数据交换平台"];
        catalog [label="数据目录"];
        sharing [label="数据共享平台"];
    }}

    subgraph cluster_infra {{
        label="基础设施层";
        style=dashed;
        bgcolor="#FCE4EC";
        cloud [label="政务云"];
        security [label="安全合规"];
        trust [label="信创适配"];
    }}

    portal -> firewall;
    mini -> firewall;
    app -> firewall;
    firewall -> waf;
    waf -> oneNet;
    waf -> oneSupervise;
    waf -> dataOpen;
    oneNet -> exchange;
    oneSupervise -> exchange;
    dataOpen -> catalog;
    exchange -> sharing;
    catalog -> sharing;
    sharing -> cloud;
    sharing -> security;
    sharing -> trust;
}}'''
    },
}


def generate_diagram_from_source(dot_content: str, output_path: str) -> str:
    """
    使用 Source 直接渲染 DOT 内容（支持完整 DOT 语法，包括 subgraph、style、color 等）

    Args:
        dot_content: Graphviz DOT 格式的完整图表描述
        output_path: 输出文件路径（PNG、SVG 或 PDF）

    Returns:
        输出文件路径
    """
    if not dot_content or dot_content.strip() == "":
        raise ValueError("DOT 内容不能为空")

    output_format = output_path.split('.')[-1].lower()
    if output_format not in ['png', 'svg', 'pdf']:
        raise ValueError(f"不支持的输出格式: {output_format}，支持的格式: png, svg, pdf")

    # 替换字体为系统中文字体
    chinese_font = get_chinese_font()
    # 替换 DOT 内容中的 Arial 字体为支持中文的字体
    dot_content = dot_content.replace('Arial', chinese_font)

    try:
        src = Source(dot_content, format=output_format)
        output_base = output_path.replace(f'.{output_format}', '')
        result_path = src.render(output_base, cleanup=True)
        return result_path
    except Exception as e:
        raise Exception(f"生成架构图失败: {str(e)}")


def generate_diagram(dot_content: str, output_path: str, diagram_type: str = "architecture") -> str:
    """
    生成架构图（兼容旧版 API，内部调用 Source 模式）

    Args:
        dot_content: Graphviz DOT 格式的图表描述
        output_path: 输出文件路径（PNG、SVG 或 PDF）
        diagram_type: 图表类型（用于设置图表属性）

    Returns:
        输出文件路径
    """
    # 如果内容包含 digraph/strict digraph 关键字，直接使用 Source 模式
    if re.search(r'(strict\s+)?digraph\s+\w+', dot_content):
        return generate_diagram_from_source(dot_content, output_path)

    # 否则使用旧版 Digraph 对象模式（兼容简单格式）
    if not dot_content or dot_content.strip() == "":
        raise ValueError("DOT 内容不能为空")

    output_format = output_path.split('.')[-1].lower()
    if output_format not in ['png', 'svg', 'pdf']:
        raise ValueError(f"不支持的输出格式: {output_format}，支持的格式: png, svg, pdf")

    chinese_font = get_chinese_font()

    if diagram_type in ['data']:
        graph_attr = {'rankdir': 'LR', 'fontname': chinese_font, 'fontsize': '12'}
    else:
        graph_attr = {'rankdir': 'TB', 'fontname': chinese_font, 'fontsize': '12'}

    dot = Digraph(engine='dot', format=output_format)
    dot.graph_attr.update(graph_attr)
    dot.node_attr.update({'fontname': chinese_font, 'fontsize': '11'})
    dot.edge_attr.update({'fontname': chinese_font, 'fontsize': '10'})

    try:
        if 'digraph' in dot_content:
            start = dot_content.find('{')
            end = dot_content.rfind('}')
            if start != -1 and end != -1:
                body = dot_content[start + 1:end].strip()
            else:
                body = dot_content
        else:
            body = dot_content

        for line in body.split(';'):
            line = line.strip()
            if not line:
                continue

            if '->' not in line and '[' in line:
                node_def = line.split('[', 1)
                if len(node_def) == 2:
                    node_name = node_def[0].strip()
                    attrs_str = node_def[1].rstrip(']').strip()
                    attrs = {}
                    for attr in attrs_str.split(','):
                        attr = attr.strip()
                        if '=' in attr:
                            key, value = attr.split('=', 1)
                            attrs[key.strip()] = value.strip().strip('"')
                    label = attrs.get('label', node_name)
                    shape = attrs.get('shape', 'box')
                    style = attrs.get('style', '')
                    fillcolor = attrs.get('fillcolor', '')
                    node_kwargs = {'label': label, 'shape': shape}
                    if style:
                        node_kwargs['style'] = style
                    if fillcolor:
                        node_kwargs['fillcolor'] = fillcolor
                    dot.node(node_name, **node_kwargs)
            elif '->' in line:
                edge_def = line.split('->', 1)
                if len(edge_def) == 2:
                    node1 = edge_def[0].strip()
                    rest = edge_def[1].strip()
                    if '[' in rest:
                        node2 = rest.split('[', 1)[0].strip()
                        attrs_str = rest.split('[', 1)[1].rstrip(']').strip()
                        attrs = {}
                        for attr in attrs_str.split(','):
                            attr = attr.strip()
                            if '=' in attr:
                                key, value = attr.split('=', 1)
                                attrs[key.strip()] = value.strip().strip('"')
                        label = attrs.get('label', '')
                        style = attrs.get('style', '')
                        edge_kwargs = {}
                        if label:
                            edge_kwargs['label'] = label
                        if style:
                            edge_kwargs['style'] = style
                        dot.edge(node1, node2, **edge_kwargs)
                    else:
                        dot.edge(node1, rest)

    except Exception as e:
        raise Exception(f"解析 DOT 内容失败: {str(e)}")

    try:
        output_base = output_path.replace(f'.{output_format}', '')
        result_path = dot.render(output_base, cleanup=True)
        return result_path
    except Exception as e:
        raise Exception(f"生成架构图失败: {str(e)}")


def generate_from_template(template_name: str, output_path: str) -> str:
    """
    使用预设模板生成架构图

    Args:
        template_name: 模板名称
        output_path: 输出文件路径

    Returns:
        输出文件路径
    """
    if template_name not in TEMPLATES:
        available = ', '.join(TEMPLATES.keys())
        raise ValueError(f"未知模板: {template_name}，可用模板: {available}")

    template = TEMPLATES[template_name]
    return generate_diagram_from_source(template['dot'], output_path)


def main():
    parser = argparse.ArgumentParser(
        description='生成架构图（支持 Graphviz DOT 格式和预设模板）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 从 DOT 文件生成架构图
  python generate-architecture-diagram.py --diagram-type business --input business.dot --output business.png

  # 使用预设模板生成架构图
  python generate-architecture-diagram.py --template business-4layer --output business.png

  # 列出所有可用模板
  python generate-architecture-diagram.py --list-templates

  # 从标准输入读取 DOT 内容
  echo "digraph G { A -> B }" | python generate-architecture-diagram.py --output test.png
        """
    )

    parser.add_argument(
        '--diagram-type',
        choices=['business', 'functional', 'data', 'technical', 'flow'],
        default='architecture',
        help='图表类型（business: 业务架构, functional: 功能架构, data: 数据架构, technical: 技术架构, flow: 流程图）'
    )

    parser.add_argument(
        '--input', '-i',
        help='输入文件路径（Graphviz DOT 格式），如果不指定则从标准输入读取'
    )

    parser.add_argument(
        '--output', '-o',
        help='输出文件路径（支持格式: png, svg, pdf）'
    )

    parser.add_argument(
        '--template', '-t',
        help='使用预设模板生成架构图'
    )

    parser.add_argument(
        '--list-templates', action='store_true',
        help='列出所有可用的预设模板'
    )

    args = parser.parse_args()

    # 列出模板
    if args.list_templates:
        templates_info = []
        for key, tmpl in TEMPLATES.items():
            templates_info.append({
                'name': key,
                'display_name': tmpl['name'],
                'description': tmpl['description']
            })
        print(json.dumps(templates_info, ensure_ascii=False, indent=2))
        return

    # 模板模式
    if args.template:
        if not args.output:
            print("错误: 使用模板模式时必须指定 --output 参数", file=sys.stderr)
            sys.exit(1)
        try:
            result = generate_from_template(args.template, args.output)
            result_data = {"status": "success", "output": result, "template": args.template}
            print(json.dumps(result_data, ensure_ascii=False))
        except Exception as e:
            print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
            sys.exit(1)
        return

    # DOT 文件/标准输入模式
    if not args.output:
        print("错误: 必须指定 --output 参数", file=sys.stderr)
        sys.exit(1)

    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                dot_content = f.read()
        except FileNotFoundError:
            print(json.dumps({"status": "error", "message": f"文件不存在: {args.input}"}, ensure_ascii=False))
            sys.exit(1)
        except Exception as e:
            print(json.dumps({"status": "error", "message": f"读取文件失败: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
    else:
        dot_content = sys.stdin.read()

    try:
        result = generate_diagram(dot_content, args.output, args.diagram_type)
        result_data = {"status": "success", "output": result, "diagram_type": args.diagram_type}
        print(json.dumps(result_data, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
