#!/usr/bin/env python3
"""Reuse declared datasets and keys as ontology candidates; never infer policy."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from _contract import fields, load, relation_id, relation_keys, top_shape_error, write


def stable_id(kind, identity):
    return kind + '_' + hashlib.sha256(identity.encode('utf-8')).hexdigest()[:16]


def derive(model):
    error = top_shape_error(model)
    if error:
        raise ValueError(error)
    result = copy.deepcopy(model)
    datasets = result.get('datasets', [])
    if not datasets:
        raise ValueError('先提供 datasets 元数据；不会从名称猜造表或业务对象')
    if any(not isinstance(d, dict) for d in datasets):
        raise ValueError('datasets 必须为对象列表')
    names = [d.get('name') for d in datasets]
    if any(not isinstance(n, str) or not n for n in names) or len(names) != len(set(names)):
        raise ValueError('数据集 name 必须非空且唯一；同名跨库表须先明确各自身份')
    if result.get('ontology') is None:
        result['ontology'] = {}
    ont = result['ontology']
    entities = ont.setdefault('entities', [])
    relations = ont.setdefault('relations', [])
    if any(not isinstance(xs, list) or any(not isinstance(x, dict) for x in xs) for xs in (entities, relations)):
        raise ValueError('ontology.entities/relations 必须为对象列表')
    refs = {}
    for e in entities:
        for ref in {e.get('name'), e.get('uid')} - {None, ''}:
            if ref in refs and refs[ref] is not e:
                raise ValueError('本体 name/uid 存在歧义，请先修复绑定')
            refs[ref] = e
    bound, summary = {}, {'entities_added': [], 'relations_added': [], 'preserved': [], 'review': []}
    for ds in datasets:
        name, ref = ds['name'], ds.get('ontology_ref')
        if ref:
            if ref not in refs:
                raise ValueError(f'{name}: ontology_ref {ref!r} 失效；不会自动重绑')
            bound[name] = refs[ref]
            summary['preserved'].append(name)
            continue
        uid = stable_id('ent', name)
        if name in refs or uid in refs:
            raise ValueError(f'{name}: 已有同名/同ID对象，请先明确 ontology_ref，不能按名称自动合并')
        fs = ds.get('fields', [])
        if not isinstance(fs, list) or any(not isinstance(f, dict) or not f.get('name') for f in fs):
            raise ValueError(f'{name}: fields 必须是带 name 的字段列表')
        if len({f['name'] for f in fs}) != len(fs):
            raise ValueError(f'{name}: 字段名重复')
        entity = {'uid': uid, 'name': name,
                  'evidence': {'source': 'model_inferred', 'refs': [f'dataset:{name}']},
                  'note': '由元数据生成的结构候选；业务身份、属性含义与适用范围需核对。',
                  'attributes': [{'name': f['name'], 'note': f.get('cn') or f.get('comment') or '含义待核对'} for f in fs]}
        entities.append(entity)
        refs[name] = refs[uid] = entity
        ds['ontology_ref'] = uid
        bound[name] = entity
        summary['entities_added'].append(uid)
        summary['review'].append(f'{name}: 核对业务对象与字段含义，表名/主键不证明业务粒度')
    relrefs = {}
    for rel in relations:
        if rel.get('id'):
            if rel['id'] in relrefs:
                raise ValueError('本体关系ID重复')
            relrefs[rel['id']] = rel
    ids = set()
    by_name = {d['name']: d for d in datasets}
    for edge in result.get('relationships') or []:
        if not isinstance(edge, dict):
            raise ValueError('relationships 必须为对象列表')
        rid = relation_id(edge)
        if rid in ids:
            raise ValueError('数据关系ID重复；并行关系须明确不同ID')
        ids.add(rid)
        if edge.get('from') not in bound or edge.get('to') not in bound:
            raise ValueError(f'{rid}: 关系端点不存在')
        left, right = relation_keys(edge)
        if not set(left) <= fields(by_name[edge['from']]) or not set(right) <= fields(by_name[edge['to']]):
            raise ValueError(f'{rid}: 关系引用字段失效')
        if edge.get('ontology_ref'):
            target = relrefs.get(edge['ontology_ref'])
            if not target or target.get('mapping') != 'equi_key':
                raise ValueError(f'{rid}: 关系投影失效或不是键关联；请先修复')
            if refs.get(target.get('from')) is not bound[edge['from']] or refs.get(target.get('to')) is not bound[edge['to']]:
                raise ValueError(f'{rid}: 业务关系与物理端点不一致；不会改写既有关系')
            continue
        uid = stable_id('rel', rid)
        if uid in relrefs:
            raise ValueError(f'{rid}: 已有关系ID，请先明确 ontology_ref')
        target = {'id': uid, 'from': bound[edge['from']]['name'], 'to': bound[edge['to']]['name'],
                  'predicate': '关联（待确认）', 'mapping': 'equi_key',
                  'evidence': {'source': 'model_inferred', 'refs': [f'relationship:{rid}']},
                  'note': '复用已声明键；业务谓词待核对。没有据此证明基数、引用覆盖或授权。'}
        relations.append(target)
        relrefs[uid] = target
        edge['ontology_ref'] = uid
        summary['relations_added'].append(uid)
        summary['review'].append(f'{rid}: 维护这条关系的业务谓词，不另建逆向副本')
    return result, summary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model', required=True)
    ap.add_argument('--out', required=True, help='新的候选模型文件；不覆盖现有文件')
    args = ap.parse_args()
    try:
        if Path(args.out).exists():
            raise ValueError('输出已存在，拒绝覆盖；请选择新的候选文件')
        model, summary = derive(load(args.model))
        write(args.out, model)
        print(json.dumps({'status': 'candidate', 'output': args.out, **summary}, ensure_ascii=False))
        return 0
    except (ValueError, TypeError, KeyError) as exc:
        print(f'错误：{exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
