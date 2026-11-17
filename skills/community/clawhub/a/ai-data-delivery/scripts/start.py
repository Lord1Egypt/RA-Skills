#!/usr/bin/env python3
"""Open a local workbench with optional synthetic demo or existing files."""
import argparse
import base64
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'scripts'))


def prepare(project, demo=None, model=None, ddl=None, sample=None, provenance='unknown'):
    from workbench.service import Service
    from workbench.demo import sample as demo_sample, write_snapshot
    from derive_ontology import derive
    project=Path(project).resolve()
    initializing=bool(demo or model or ddl or sample)
    if (project/'project.sqlite').exists():
        if initializing:
            raise ValueError('项目已存在；不会覆盖。去掉导入/演示参数继续使用，或指定新的 --project 目录。')
        return Service(project),{'status':'reopened','project':str(project)}
    if demo and any((model,ddl,sample)):
        raise ValueError('演示与真实资料不能混合初始化；请分别使用项目目录。')
    if model and ddl:
        raise ValueError('模型与DDL二选一导入')
    inputs={kind:Path(value).resolve() for kind,value in [('model',model),('ddl',ddl),('sample',sample)] if value}
    for kind,path in inputs.items():
        if not path.is_file():raise ValueError(f'{kind} 文件不存在：{path}')
    project.parent.mkdir(parents=True,exist_ok=True)
    # Prepare separately, then install exactly one closed SQLite file without overwrite.
    with tempfile.TemporaryDirectory(prefix='.delivery-start-',dir=project.parent) as temporary:
        temp=Path(temporary);service=Service(temp/'project')
        def import_bytes(kind,name,data,source='unknown'):
            service.import_file({'revision':service.store.read()['revision'],'kind':kind,'filename':name,
                                 'content':base64.b64encode(data).decode(),'provenance':source})
        if demo:
            m,rows,columns,expected=demo_sample(demo);m,_=derive(m)
            snapshot=temp/'synthetic.sqlite';write_snapshot(snapshot,m,rows)
            import_bytes('model','synthetic-'+demo+'.json',json.dumps(m,ensure_ascii=False).encode())
            import_bytes('sample','synthetic-'+demo+'.sqlite',snapshot.read_bytes(),'demo')
            def label(doc):
                doc['name']='合成演示 · '+('交通' if demo=='traffic' else '零售')
                doc['tutorial']={'kind':demo,'synthetic':True,'metric':next(iter(expected)),
                                 'columns':columns,'expected':expected}
            service.store.change(service.store.read()['revision'],'local','标记合成演示与练习目标',label)
        else:
            for kind,path in inputs.items():
                import_bytes(kind,path.name,path.read_bytes(),provenance if kind=='sample' else 'unknown')
        project.mkdir(parents=True,exist_ok=True)
        os.link(service.store.path,project/'project.sqlite')  # Atomic create, fails if another initializer won.
    return Service(project),{'status':'prepared','project':str(project),'demo':demo,
                             'boundary':'本机单人项目；演示不是生产验证。' if demo else ('已导入现有文件；未自动确认业务含义。' if inputs else '已创建空项目；可在工作台导入资料。')}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',required=True,help='保存工作成果的项目目录；重开时使用同一路径')
    source=p.add_mutually_exclusive_group()
    source.add_argument('--demo',nargs='?',const='traffic',choices=['traffic','retail'],help='可选合成演示，默认交通')
    source.add_argument('--model',help='已有 YAML/JSON 语义模型')
    source.add_argument('--ddl',help='已有 SQLite/MySQL CREATE TABLE 文件，只解析不执行')
    p.add_argument('--sample',help='独立SQLite数据快照，可选')
    p.add_argument('--provenance',choices=['unknown','demo','deidentified','production'],default='unknown')
    p.add_argument('--prepare-only',action='store_true',help='仅准备项目，不启动服务')
    p.add_argument('--port',type=int,default=0,help='本机端口，默认自动选择，不占用其他服务')
    a=p.parse_args(argv)
    if not 0<=a.port<=65535:p.error('port 必须在0–65535之间')
    try:
        _,result=prepare(a.project,a.demo,a.model,a.ddl,a.sample,a.provenance)
        print(json.dumps(result,ensure_ascii=False),flush=True)
        if a.prepare_only:
            import shlex
            path=Path(a.project).resolve().as_posix()
            quoted=("'"+path.replace("'","''")+"'") if os.name=='nt' else shlex.quote(path)
            print('继续打开：python scripts/start.py --project '+quoted)
            return 0
        from workbench.serve import main as serve
        return serve(['--project',str(Path(a.project).resolve()),'--port',str(a.port)])
    except ImportError as exc:
        print('缺少运行依赖。请在本skill目录执行 python -m pip install -r requirements.txt，然后重试。',file=sys.stderr)
        return 2
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print('无法打开项目：'+str(exc),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
