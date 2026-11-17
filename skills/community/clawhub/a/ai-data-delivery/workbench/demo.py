"""Small synthetic fixtures for the first-run workbench, never customer data."""
import copy
import sqlite3


def sample(kind):
    if kind == 'traffic':
        table='companies'
        labels={'row_id':'记录编号','company_id':'企业标识','tenant':'主体','state':'经营状态','industry':'行业'}
        rows=[(1,'A','T1','开业','危货'),(2,'A','T1','开业','危货'),(3,None,'T1','开业','危货'),
              (4,'B','T2','开业','危货'),(5,'C','T1','停业','危货'),(6,'D','T1','开业','普货')]
        filters=[{'field':'tenant','values':['T1']},{'field':'state','values':['开业']},{'field':'industry','values':['危货']}]
        metrics=[('rows','开业危货记录行数','count','COUNT(*)',3),
                 ('present','有企业标识的记录数','count','COUNT(company_id)',2),
                 ('distinct','去重企业标识数','count','COUNT(DISTINCT company_id)',1)]
        columns=['company_id'];details=[['A'],['A'],[None]]
    elif kind == 'retail':
        table='orders';labels={'row_id':'订单编号','tenant':'主体','state':'支付状态','amount':'金额'}
        rows=[(1,'T1','paid',100),(2,'T1','paid',30),(3,'T1','refunded',50),(4,'T2','paid',900)]
        filters=[{'field':'tenant','values':['T1']},{'field':'state','values':['paid']}]
        metrics=[('revenue','已支付订单金额','sum','SUM(amount)',130)];columns=['amount'];details=[[100],[30]]
    else:
        raise ValueError('演示仅支持 traffic 或 retail')
    model={'version':'synthetic-'+kind,'datasets':[{'name':table,'cn':'企业记录' if kind=='traffic' else '订单',
           'source':table,'grain':'一条原始记录','primary_key':['row_id'],'tenant_field':'tenant',
           'temporal':{'kind':'current'},'ai':{'instructions':'仅合成学习样例，不代表真实客户或完整业务统计。'},
           'fields':[{'name':f,'cn':label,'type':'INTEGER' if f in {'row_id','amount'} else 'TEXT',
                      'role':'pk' if f=='row_id' else 'attr'} for f,label in labels.items()]}],
           'metrics':[{'id':mid,'name':name,'dataset':table,'type':typ,'expr':expr,'structured':True,
                      'time_requirement':'current','unit':'个' if mid=='distinct' else '条' if typ=='count' else '元',
                      'caliber':{'note':'仅T1主体及所声明状态/行业内的合成记录；不自动补齐缺失数据。'},
                      'filters':copy.deepcopy(filters)} for mid,name,typ,expr,value in metrics]}
    return model,rows,columns,{mid:{'metric_value':value,'matched_row_count':len(details),'detail_rows':details}
                              for mid,name,typ,expr,value in metrics}


def write_snapshot(path, model, rows):
    ds=model['datasets'][0]
    conn=sqlite3.connect(path)
    try:
        conn.execute('CREATE TABLE '+ds['source']+'('+','.join(f['name']+' '+f['type'] for f in ds['fields'])+')')
        conn.executemany('INSERT INTO '+ds['source']+' VALUES ('+','.join('?' for _ in ds['fields'])+')',rows)
        conn.commit()
    finally:
        conn.close()
