"""Lossless data export, fixed Cypher, no database connection or code from source material."""
import csv
import hashlib
import io
import json
import zipfile

from workbench.semantic_package import asset_dependencies


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def export_neo4j(package):
    """Return a self-contained import ZIP. Snapshot namespaces avoid cross-project ID collisions."""
    namespace = hashlib.sha256(encoded(package.manifest).encode()).hexdigest()
    entries = {}
    def table(name, fields, rows):
        out = io.StringIO(newline='')
        writer = csv.writer(out, lineterminator='\n')
        writer.writerow(['namespace', *fields])
        for row in rows:
            writer.writerow([namespace, *row])
        entries[name+'.csv'] = out.getvalue().encode('utf-8')
    table('snapshots', ['snapshot_id','manifest_json','model_json','sources_json','task_json'], [[
        package.manifest['snapshot_id'], encoded(package.manifest), encoded(package.model),
        encoded(package.source_records), encoded(package.task_record)]])
    table('assets', ['id','kind','name','definition','domain','status','scope_json','asset_json'], [
        [a['id'],a['kind'],a['name'],a.get('definition',''),a.get('domain',''),a['status'],encoded(a.get('scope')),encoded(a)]
        for a in package.index.values()])
    refs, relations, evidence = [], [], []
    missing = []
    for a in package.index.values():
        for raw in asset_dependencies(a, include_execution=package.manifest['scope'].get('include_execution',False)):
            target = package.redirects.get(raw,raw)
            if target in package.index:
                refs.append([a['id'],target])
            else:
                missing.append({'from':a['id'],'to':raw})
        if a['kind'] in {'relation', 'mapping'}:
            start,end = (package.redirects.get(a[k],a[k]) for k in ('from','to'))
            if start in package.index and end in package.index:
                relations.append([a['id'],start,end,a.get('predicate',''),a.get('relation_type','business')])
        for item in a.get('evidence',[]):
            # Store exact provenance as data, including manual declarations; never execute it.
            evidence.append([hashlib.sha256(encoded([a['id'],item]).encode()).hexdigest(),a['id'],encoded(item)])
    table('references',['from_id','to_id'],refs)
    table('relationships',['id','from_id','to_id','predicate','relation_type'],relations)
    table('evidence',['id','asset_id','evidence_json'],evidence)
    entries['import.cypher'] = CYPHER.encode()
    entries['README.md'] = README.encode()
    manifest = {'format':'ai-data-delivery/neo4j-csv/1','namespace':namespace,
        'snapshot_id':package.manifest['snapshot_id'],'draft':package.manifest['draft'],
        'complete':package.manifest['complete'],'missing_dependencies':missing,
        'counts':{'assets':len(package.index),'references':len(refs),'relationships':len(relations),'evidence':len(evidence)},
        'files':{n:hashlib.sha256(b).hexdigest() for n,b in entries.items()}}
    entries['export-manifest.json']=(encoded(manifest)+'\n').encode()
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(entries.items()):
            info=zipfile.ZipInfo(name,(2020,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data)
    return out.getvalue(),manifest


CYPHER = """// Neo4j 5.x+; static labels and file names. Run sequentially, no APOC required.
CREATE CONSTRAINT add_snapshot_key IF NOT EXISTS FOR (n:SemanticSnapshot) REQUIRE n.namespace IS UNIQUE;
CREATE CONSTRAINT add_asset_key IF NOT EXISTS FOR (n:SemanticAsset) REQUIRE (n.namespace, n.id) IS UNIQUE;
CREATE CONSTRAINT add_evidence_key IF NOT EXISTS FOR (n:SemanticEvidence) REQUIRE (n.namespace, n.id) IS UNIQUE;
LOAD CSV WITH HEADERS FROM 'file:///snapshots.csv' AS row
MERGE (s:SemanticSnapshot {namespace:row.namespace})
SET s.snapshot_id=row.snapshot_id, s.manifest_json=row.manifest_json, s.model_json=row.model_json,
    s.sources_json=row.sources_json, s.task_json=row.task_json;
LOAD CSV WITH HEADERS FROM 'file:///assets.csv' AS row
MATCH (s:SemanticSnapshot {namespace:row.namespace})
MERGE (a:SemanticAsset {namespace:row.namespace,id:row.id})
SET a.kind=row.kind,a.name=row.name,a.definition=row.definition,a.domain=row.domain,
    a.status=row.status,a.scope_json=row.scope_json,a.asset_json=row.asset_json
MERGE (s)-[:CONTAINS]->(a);
LOAD CSV WITH HEADERS FROM 'file:///references.csv' AS row
MATCH (a:SemanticAsset {namespace:row.namespace,id:row.from_id})
MATCH (b:SemanticAsset {namespace:row.namespace,id:row.to_id})
MERGE (a)-[:DEPENDS_ON]->(b);
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
MATCH (a:SemanticAsset {namespace:row.namespace,id:row.from_id})
MATCH (b:SemanticAsset {namespace:row.namespace,id:row.to_id})
MERGE (a)-[r:SEMANTIC_RELATION {id:row.id}]->(b)
SET r.predicate=row.predicate,r.relation_type=row.relation_type;
LOAD CSV WITH HEADERS FROM 'file:///evidence.csv' AS row
MATCH (a:SemanticAsset {namespace:row.namespace,id:row.asset_id})
MERGE (e:SemanticEvidence {namespace:row.namespace,id:row.id})
SET e.evidence_json=row.evidence_json
MERGE (a)-[:EVIDENCED_BY]->(e);
"""

README = """# Import a reviewed semantic snapshot into Neo4j / 导入已核对的语义快照

1. Inspect export-manifest.json and the original semantic package: draft and completeness remain unchanged. This export does not approve knowledge.
2. Copy the five CSV files into a dedicated Neo4j instance's configured import directory. Do not replace another import's files.
3. Run import.cypher sequentially with Neo4j Browser or cypher-shell -d <database> -f import.cypher. Credentials belong to your Neo4j client, not this bundle. File import must be enabled by its administrator. Set `db.import.csv.legacy_quote_escaping=false` for standard CSV quoting; the import preserves JSON backslashes. Managed services without local file import require their supported CSV upload workflow.
4. Query `MATCH (a:SemanticAsset)-[r:SEMANTIC_RELATION]->(b) RETURN a,r,b` to inspect the graph. Filter every Agent query by the namespace in export-manifest.json. Read asset_json for full scope, properties and evidence; read the SemanticSnapshot manifest_json for draft/completeness and sources_json for exact provenance.

1. 核对 export-manifest.json 与原始语义包；草稿及完整性标志原样保留，导出不等于批准知识。
2. 把五个 CSV 放入指定 Neo4j 实例的 import 目录，不覆盖他人的导入文件。
3. 在 Neo4j Browser 顺序执行 import.cypher，或使用 cypher-shell -d <database> -f import.cypher。凭据只交给 Neo4j 客户端。本地文件导入须由管理员开启，并设置 `db.import.csv.legacy_quote_escaping=false`，按标准 CSV 保留 JSON 反斜杠；不支持本地文件的托管服务需采用平台 CSV 上传方式。
4. Agent 查询必须限定清单中的 namespace，读取 asset_json 中的范围、属性与依据，结合快照 manifest_json 的草稿及完整性标志、sources_json 的来源定位。上面的查询可查看有向关系。

Every semantic asset remains a node, including relationship definitions. Business edges preserve direction and reference their relationship asset ID. DEPENDS_ON records dependencies, never a new business claim. Evidence and complete original JSON travel with the snapshot. Reimporting the same snapshot uses MERGE; a new snapshot gets its own namespace and does not overwrite/delete earlier knowledge. Run one import at a time. Draft missing dependencies remain explicit in export-manifest.json and model_json, without fabricated edges. Labels and Cypher are fixed; names, predicates and source text are CSV data only. No SQL, script, trigger or action contained in metadata is executed. This bundle does not upload anything or make a database the workbench's primary store.

每个语义资产都保留为节点（包括关系定义）。业务连线保留方向和关系资产 ID；DEPENDS_ON 仅表达依赖。证据和完整原始 JSON 随包交付。同一快照可顺序重复导入；新快照隔离存储，不删除或覆盖旧知识。草稿缺失依赖保留在清单与模型中，不伪造连线。标签及 Cypher 固定，名称、谓词和原文只作为 CSV 数据；不会执行元数据中的 SQL、脚本或动作。工具只生成文件，不自动上传，也不把 Neo4j 设为工作台强制主存储。
"""
