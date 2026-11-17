"""Create a synthetic, human-readable review example; never a blind benchmark."""
import argparse
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from start import prepare


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args()
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    service,_=prepare(out/'project',demo='traffic')
    service.scene({'revision':service.store.read()['revision'],'scene':{
        'question':'T1主体当前开业危货记录，为什么行数、非空数、去重数不同？', 'profile':'metric',
        'datasets':['companies'],'metrics':['rows','present','distinct'],
        'requirements':{'audience':'数据产品经理与FDE（合成练习）','time_scope':'导入快照中的当前状态',
                        'acceptance':'范围内A、A、NULL：行数3、非空2、去重1。去重1只表示已知唯一标识，不能掩盖缺标识记录。'}}})
    expected={'metric_value':3,'matched_row_count':3,'detail_rows':[['A'],['A'],[None]]}
    service.bundle({'metric':'rows','columns':['company_id'],'expected':expected})
    service.store.change(service.store.read()['revision'],'demo','补充演示口径说明，使旧报告失效',lambda d:d['model']['metrics'][0]['caliber'].update(note='合成练习：仅T1主体、开业、危货记录；其他主体、停业和普货不计。'))
    service.bundle({'metric':'rows','columns':['company_id'],'expected':{**expected,'metric_value':4}})
    for metric,value in [('rows',3),('present',2),('distinct',1)]:
        service.bundle({'metric':metric,'columns':['company_id'],'expected':{**expected,'metric_value':value}})
    (out/'human-review.html').write_bytes(service.review_html())
    (out/'semantic-delivery.zip').write_bytes(service.export())
    print(out/'human-review.html')


if __name__=='__main__':main()
