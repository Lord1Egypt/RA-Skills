#!/usr/bin/env python3
"""Synthetic traffic + retail exercise; writes only into an empty output directory."""
import argparse
import copy
import json
from pathlib import Path
import sqlite3
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _contract import write, readonly
from derive_ontology import derive
from query_bundle import run_bundle
from select_context import select_context, verify_context


def build(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise ValueError('示例输出目录需为空；不会覆盖已有模型或数据')
    definitions = [
        ('traffic', 'companies', ['row_id', 'company_id', 'tenant', 'state', 'industry'],
         [(1,'A','T1','开业','危货'),(2,'A','T1','开业','危货'),(3,None,'T1','开业','危货'),
          (4,'B','T2','开业','危货'),(5,'C','T1','停业','危货'),(6,'D','T1','开业','普货')],
         [{'field':'tenant','values':['T1']},{'field':'state','values':['开业']},{'field':'industry','values':['危货']}],
         [('rows','count','COUNT(*)',3),('present','count','COUNT(company_id)',2),('distinct','count','COUNT(DISTINCT company_id)',1)],
         ['company_id'], [['A'],['A'],[None]]),
        ('retail', 'orders', ['row_id', 'tenant', 'state', 'amount'],
         [(1,'T1','paid',100),(2,'T1','paid',30),(3,'T1','refunded',50),(4,'T2','paid',900)],
         [{'field':'tenant','values':['T1']},{'field':'state','values':['paid']}],
         [('revenue','sum','SUM(amount)',130)], ['amount'], [[100],[30]])]
    results = []
    for name, table, fields, rows, filters, metrics, columns, expected_rows in definitions:
        model = {'version':'synthetic', 'datasets':[{'name':table,'source':table,'grain':'一条原始记录',
                 'primary_key':['row_id'],'tenant_field':'tenant','temporal':{'kind':'current'},
                 'fields':[{'name':f,'role':'pk' if f=='row_id' else 'attr','cn':f} for f in fields]}],
                 'metrics':[{'id':mid,'name':mid,'dataset':table,'type':typ,'expr':expr,'structured':True,
                            'time_requirement':'current','unit':'条' if typ=='count' else '元',
                            'caliber':{'note':'仅所声明范围内的合成演示数据'},'filters':filters}
                            for mid,typ,expr,_ in metrics]}
        model,_ = derive(model)
        write(out/f'{name}.yaml',model)
        db = out/f'{name}.sqlite'
        with sqlite3.connect(db) as conn:
            declaration = ','.join(f+' '+('INTEGER' if f in {'row_id','amount'} else 'TEXT') for f in fields)
            conn.execute(f'CREATE TABLE {table}({declaration})')
            conn.executemany(f'INSERT INTO {table} VALUES ({",".join("?" for _ in fields)})', rows)
        conn = readonly(db)
        try:
            for mid,_,_,gold in metrics:
                result = run_bundle(model, conn, mid, columns)
                assert result['status']=='computed_only',result
                assert result['metric_value']==gold,(mid,result)
                assert result['matched_row_count']==len(expected_rows),(mid,result)
                assert result['detail_rows']==expected_rows,(mid,result)
                write(out/f'{name}-{mid}-result.json',result)
                results.append({'case':f'{name}:{mid}','expected_value':gold,'expected_rows':expected_rows,'status':'pass'})
            package = select_context(model,metrics[0][0],columns)
            write(out/f'{name}-context.json',package)
            assert verify_context(model,package)['status']=='matched'
            changed = copy.deepcopy(model)
            changed['metrics'][0]['filters'][0]['values']=['T2']
            assert verify_context(changed,package)['error']['code']=='CONTEXT_STALE'
            assert package['context']['entity_excerpt']['evidence']['source']=='model_inferred'
        finally:
            conn.close()
    report={'status':'pass','cases':results,'boundary':'固定合成数据；tenant过滤是业务条件演示，不是鉴权。数值预期写死在示例，不从被测SQL计算。'}
    write(out/'demo-report.json',report)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--out',required=True)
    a=p.parse_args(); print(json.dumps(build(a.out),ensure_ascii=False,indent=2))
