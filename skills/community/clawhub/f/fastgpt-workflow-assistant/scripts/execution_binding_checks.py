"""Finite checks for flat JS main parameters and baseline HTTP output contracts.

Not a JS parser. Complex/dynamic signatures require bound execution tests.
"""
import re


def flat_main_parameters(code):
    match = re.search(r"\bfunction\s+main\s*\(\s*\{([^{}]*)\}\s*(?:=\s*\{\s*\}\s*)?\)", code)
    if not match:
        return None
    fields = []
    for item in match.group(1).split(','):
        item = item.strip()
        if not item:
            continue
        part = re.fullmatch(r"([A-Za-z_$][\w$]*)(?:\s*:\s*[A-Za-z_$][\w$]*)?(\s*=\s*[^,]+)?", item)
        if not part:
            return None
        fields.append((part.group(1), part.group(2) is not None))
    return fields


def check(nodes, baseline=None):
    result = []
    def add(code, node, message, severity='error'):
        result.append(dict(code=code, severity=severity, message=message,
                           node_id=node.get('nodeId', ''), path='$.nodes',
                           suggested_fix='补齐实际输入绑定或核对目标实例输出契约，再运行bound数据链及最终回复合同'))
    reference_http = [n for n in (baseline or {}).get('nodes', [])
                      if n.get('flowNodeType') == 'httpRequest468']
    baseline_keys = {o.get('key') for n in reference_http for o in n.get('outputs', []) if isinstance(o, dict)}
    for node in nodes:
        inputs = {i.get('key'): i for i in node.get('inputs', []) if isinstance(i, dict)}
        if node.get('flowNodeType') == 'code':
            language = inputs.get('codeType', {}).get('value', 'js')
            code = inputs.get('code', {}).get('value')
            if language not in ('js', 'javascript') or not isinstance(code, str):
                continue
            fields = flat_main_parameters(code)
            if fields is None:
                continue
            for key, has_default in fields:
                if key not in inputs:
                    if not has_default:
                        add('FG095', node, 'main参数未声明实际输入键：' + key)
                    continue
                item = inputs[key]
                if 'reference' in item.get('renderTypeList', []) and isinstance(item.get('value'), list):
                    value = item['value']
                    if len(value) != 2 or not all(isinstance(v, str) and v for v in value):
                        add('FG096', node, '输入引用必须是非空[nodeId, outputId]：' + key)
                elif 'value' not in item and 'defaultValue' not in item and not has_default:
                    add('FG096', node, '输入已声明但未绑定值或引用：' + key)
        if node.get('flowNodeType') == 'httpRequest468':
            outputs = [o for o in node.get('outputs', []) if isinstance(o, dict)]
            keys = {o.get('key') for o in outputs}
            suspect = {'system_httpResponse', 'system_http_raw_response'} - baseline_keys
            for key in keys & suspect:
                add('FG097', node, 'HTTP输出仅在候选中自行声明，缺少平台依据：' + key,
                    'error' if reference_http else 'warning')
            if 'httpRawResponse' in baseline_keys and 'httpRawResponse' not in keys:
                add('FG097', node, 'HTTP节点缺少目标基线的httpRawResponse输出')
            if reference_http:
                for output in outputs:
                    if output.get('type') in ('static', 'error') and output.get('key') not in baseline_keys:
                        add('FG097', node, '静态HTTP输出不在目标基线契约：' + str(output.get('key')))
    return result
