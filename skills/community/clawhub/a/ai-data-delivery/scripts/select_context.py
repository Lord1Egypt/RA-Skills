#!/usr/bin/env python3
"""Select declared context for one local metric. Selection is NOT authorization."""
import argparse
import copy
import json
from _contract import load, object_digest, top_shape_error, write, keys
from _sql import metric_dependencies


def select_context(model, metric_id, columns=None):
    error = top_shape_error(model)
    if error:
        raise ValueError(error)
    metrics = [m for m in model.get('metrics', []) if m.get('id') == metric_id]
    if len(metrics) != 1:
        raise ValueError('指标不存在或 ID 不唯一')
    metric = metrics[0]
    datasets = [d for d in model.get('datasets', []) if d.get('name') == metric.get('dataset')]
    if len(datasets) != 1:
        raise ValueError('指标来源不存在或名称不唯一')
    dataset = datasets[0]
    declared_names = [f['name'] for f in dataset.get('fields', [])]
    if len(declared_names) != len(set(declared_names)):
        raise ValueError('来源字段名重复，不能确定依赖')
    dep = metric_dependencies(metric, dataset)
    if dep['error']:
        raise ValueError(dep['error'])
    if columns is not None and not isinstance(columns, list):
        raise ValueError('明细字段必须为列表')
    columns = list(columns or [])
    if any(not isinstance(x, str) or not x for x in columns) or len(set(columns)) != len(columns):
        raise ValueError('明细字段必须为非空且不重复的名称列表')
    required = set(dep['fields']) | set(columns) | set(keys(dataset.get('primary_key')))
    required.update(x for x in (metric.get('time_field'), dataset.get('tenant_field')) if x)
    declared = {f['name'] for f in dataset.get('fields', [])}
    if not required <= declared:
        raise ValueError('引用字段不存在：' + ', '.join(sorted(required - declared)))
    selected = copy.deepcopy(dataset)
    selected['fields'] = [f for f in selected.get('fields', []) if f['name'] in required]
    citations = [{'path': f'metrics[id={metric_id}]', 'sha256': object_digest(metric)},
                 {'path': f'datasets[name={dataset["name"]}]', 'sha256': object_digest(dataset)}]
    entity = None
    ref = dataset.get('ontology_ref')
    if ref:
        matches = [e for e in (model.get('ontology') or {}).get('entities', [])
                   if ref in (e.get('uid'), e.get('name'))]
        if len(matches) != 1:
            raise ValueError('数据集的本体绑定失效或存在歧义')
        original = matches[0]
        entity = {k: copy.deepcopy(original[k]) for k in ('uid', 'name', 'note', 'evidence') if k in original}
        citations.append({'path': f'ontology.entities[ref={ref}]', 'sha256': object_digest(original)})
    payload = {'metric': copy.deepcopy(metric), 'dataset': selected, 'entity_excerpt': entity}
    return {'schema_version': '1.0', 'status': 'selected', 'request': {'metric': metric_id, 'columns': columns},
            'model_sha256': object_digest(model), 'payload_sha256': object_digest(payload),
            'source_mode': 'snapshot', 'context': payload, 'citations': citations,
            'boundaries': ['只选择已声明的单表指标及其依赖；未执行查询、权限认证或业务确认。',
                           '保留原证据等级；model_inferred 不会升级为 owner_confirmed。',
                           '模型中的外部链接未读取；本体仅含对象摘要，未携带关系推理或其他对象。',
                           '其他指标/表未进入本包；描述文本未经敏感信息识别，不可把裁剪当作脱敏。']}


def verify_context(model, package):
    if not isinstance(package, dict) or not isinstance(package.get('request'), dict):
        return {'status': 'rejected', 'error': {'code': 'CONTEXT_INVALID', 'message': '不是有效上下文包'}}
    if package.get('model_sha256') != object_digest(model):
        return {'status': 'rejected', 'error': {'code': 'CONTEXT_STALE', 'message': '来源模型已变更；重新选择上下文，不复用旧包'}}
    try:
        req = package['request']
        fresh = select_context(model, req.get('metric'), req.get('columns'))
        if fresh != package:
            raise ValueError('上下文内容、来源指纹或引用与当前模型不符')
        return {'status': 'matched', 'model_sha256': fresh['model_sha256'], 'payload_sha256': fresh['payload_sha256']}
    except (ValueError, TypeError, KeyError) as exc:
        return {'status': 'rejected', 'error': {'code': 'CONTEXT_INVALID', 'message': str(exc)}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model', required=True)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--metric')
    group.add_argument('--check', help='核对已有上下文包；模型变化或内容篡改时拒绝')
    p.add_argument('--columns', default='', help='本次明细需要的字段，逗号分隔；不代表获权字段')
    p.add_argument('--out', required=True)
    a = p.parse_args()
    try:
        model = load(a.model)
        result = verify_context(model, load(a.check)) if a.check else select_context(model, a.metric, a.columns.split(',') if a.columns else [])
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        result = {'status': 'rejected', 'error': {'code': 'CONTEXT_INVALID', 'message': str(exc)}}
    write(a.out, result)
    print(json.dumps({'status': result['status'], 'out': a.out}, ensure_ascii=False))
    return 2 if result['status'] == 'rejected' else 0


if __name__ == '__main__':
    raise SystemExit(main())
