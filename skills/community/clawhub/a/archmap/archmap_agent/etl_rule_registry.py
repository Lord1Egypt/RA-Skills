"""ETL 底层规则注册表（agent-harness 舌苔 ETL 34 条规则 R1-R34，2026-08-05 源码实读；2026-08-10 都江堰工单 W1-W4/W6 回填）。

每条规则含：唯一编码 ETL-{分层}-{序号}、规则标识 R#、关键词标签、源码定位（文件:函数名，
行号由 etl_profiler 运行时 grep 解析防漂移）、配置路径、参数基线、依赖规则、下游消费者、风险、
历史改动、测试引用。零虚构：history 仅记录已知改造，无记录标「暂无记录」。
"""
import json
from pathlib import Path

# 7 分层目录树（用户设计文档：预处理清洗→Chunk分片→向量化写入→一致性对账→隔离存储→异常重试→ETL编排）
LAYERS = [
    ("ETL-PREP", "预处理清洗"),
    ("ETL-CHUNK", "Chunk分片"),
    ("ETL-VEC", "向量化写入"),
    ("ETL-CHECK", "一致性对账"),
    ("ETL-STORE", "隔离存储"),
    ("ETL-RETRY", "异常重试"),
    ("ETL-ORCH", "ETL编排"),
]

# 检测 ETL 项目的特征目录（存在任一即触发 ETL 探查产出）
# 前三项为内置私有项目（tongue_diagnosis）历史特征，保留不删（向后兼容）；
# 后三项为通用生态特征目录（项目可配置覆盖改造新增）。
ETL_DETECT_DIRS = ("tongue_diagnosis/etl", "etl_config", "etl/core",
                   "etl", "etl_pipeline", "pipelines")

# 搜索索引关键字 → 规则编码（⑦ etl_rule_search_index.json 的检索快捷索引）
KEYWORD_INDEX = {
    "幂等": ["ETL-ORCH-01", "ETL-CHECK-01", "ETL-VEC-02", "ETL-CHUNK-01"],
    "chunk_id": ["ETL-CHECK-01", "ETL-STORE-01", "ETL-CHUNK-01"],
    "切片": ["ETL-CHUNK-02", "ETL-CHUNK-03", "ETL-CHUNK-05"],
    "分片": ["ETL-CHUNK-02", "ETL-CHUNK-03", "ETL-CHUNK-05"],
    "embedding": ["ETL-VEC-01"],
    "向量": ["ETL-VEC-01", "ETL-VEC-02"],
    "覆写": ["ETL-VEC-02", "ETL-CHECK-01"],
    "重试": ["ETL-VEC-03", "ETL-RETRY-01"],
    "并行": ["ETL-VEC-03"],
    "BM25": ["ETL-VEC-04"],
    "outbox": ["ETL-CHECK-03", "ETL-ORCH-04"],
    "对账": ["ETL-CHECK-05"],
    "shard_meta": ["ETL-CHECK-04", "ETL-CHECK-05"],
    "删除": ["ETL-STORE-02"],
    "pdf_index": ["ETL-STORE-03"],
    "水印": ["ETL-PREP-03"],
    "清洗": ["ETL-PREP-03"],
    "打标": ["ETL-PREP-01", "ETL-ORCH-07", "ETL-PREP-05"],
    "脉象": ["ETL-PREP-01", "ETL-PREP-05"],
    "parser": ["ETL-PREP-02"],
    "格式": ["ETL-PREP-02", "ETL-RETRY-01"],
    "错误语义": ["ETL-RETRY-01"],
    "降级": ["ETL-RETRY-01"],
    "框架": ["ETL-ORCH-02"],
    "节点": ["ETL-ORCH-02"],
    "契约": ["ETL-ORCH-03"],
    "配置": ["ETL-ORCH-08", "ETL-VEC-01"],
    "workers": ["ETL-VEC-03", "ETL-ORCH-08"],
    "retro": ["ETL-ORCH-07"],
    "skill_gen": ["ETL-ORCH-07"],
    "dataset_id": ["ETL-PREP-04", "ETL-PREP-05"],
    "分类": ["ETL-PREP-04", "ETL-PREP-05"],
    "并发": ["ETL-STORE-04"],
    "上传": ["ETL-STORE-02", "ETL-STORE-03"],
    "增量": ["ETL-ORCH-01"],
    "迁移": ["ETL-CHECK-03", "ETL-RETRY-01"],
    "deferred": ["ETL-ORCH-09", "ETL-ORCH-10", "ETL-CHECK-03", "ETL-CHECK-05"],
    "延迟入库": ["ETL-ORCH-09", "ETL-ORCH-10"],
    "洪峰": ["ETL-ORCH-09"],
    "配额": ["ETL-ORCH-10"],
    "岁修": ["ETL-CHECK-05"],
    "weir_height": ["ETL-PREP-03"],
}

RULES: list[dict] = [
    # ── ETL-ORCH 编排 ──
    {"code": "ETL-ORCH-01", "rid": "R1", "name": "三线合一统一入口",
     "layer": "ETL-ORCH", "keywords": ["统一入口", "route_and_ingest", "三线合一", "格式路由"],
     "summary": "单入口 route_and_ingest 一次调用完成 洪峰闸→格式路由→解析→切片→24字段组装→配额闸→批量embedding→outbox记账→BM25→shard_meta 全链路；解析/嵌入失败或未注册格式返回 error 且不写 outbox；洪峰/配额超限返回 deferred 且不写向量库。返回契约 {doc_unique_id, channel, total, written, missing, status, outbox, error}，status ∈ full_ready/partial_ready/deferred/error",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "route_and_ingest"}],
     "config": [], "params": {},
     "depends": ["ETL-ORCH-02", "ETL-ORCH-09", "ETL-ORCH-10", "ETL-CHUNK-04", "ETL-VEC-01", "ETL-CHECK-03", "ETL-VEC-04", "ETL-CHECK-04"],
     "consumers": ["backend/api/pdf_storage.py::chunk_pdf", "backend/customer_service/migrate_etl_merge.py（若存在）", "scripts/rebuild_kb_from_retro_skills.py"],
     "risk_level": "高", "risk_desc": "三线入库流量单点；改签名/返回契约直接波及 PDF 上传、迁移重跑、复盘入库三方调用方",
     "history": ["2026-08-05 三线合一：PDF+通用线接入统一入口", "2026-08-05 框架化改造：主体薄封装 build_ingest_pipeline()",
                 "2026-08-10 都江堰 W2/W3：入口前置 peak 洪峰闸（E12 deferred）+ 链内 quota 配额闸（E13 deferred）"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py", "tests/test_tongue_etl/test_framework.py",
               "tests/test_tongue_etl/test_peak_gate.py", "tests/test_tongue_etl/test_quota_gate.py"],
     "notes": "status=error 时 outbox=None 且不写向量库；status=deferred 时 outbox 记账 deferred 待岁修重放；框架 9 节点 trace 全量日志"},
    {"code": "ETL-ORCH-02", "rid": "R2", "name": "9 节点链 + error_policy 三分支",
     "layer": "ETL-ORCH", "keywords": ["框架", "节点", "error_policy", "abort", "propagate", "degrade"],
     "summary": "固定顺序 route→parse→chunk→build_chunks→quota→embed→outbox→bm25→shard_meta；state.error 置位即中断。abort（route/parse/chunk/build_chunks/quota/embed 异常→error 不写 outbox）；propagate（outbox 异常原样上抛，三方调用方依赖）；degrade（bm25/shard_meta 异常→degraded 继续，reconciler 自愈）",
     "src": [{"file": "tongue_diagnosis/etl/framework/graph.py", "fn": "Graph.run"},
             {"file": "tongue_diagnosis/etl/framework/node.py", "fn": "Node.run"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_route"}],
     "config": [], "params": {},
     "depends": ["ETL-RETRY-01"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::route_and_ingest"],
     "risk_level": "高", "risk_desc": "节点顺序/中断语义/降级策略改动改变全链路行为；自定义管道 Graph().register(Node(...)) 对外能力",
     "history": ["2026-08-05 自研轻量节点框架新增（零第三方依赖，LangGraph 思路）",
                 "2026-08-10 都江堰 W3：build_chunks 后插入 quota 节点（宝瓶口配额闸，abort），8→9 节点"],
     "tests": ["tests/test_tongue_etl/test_framework.py"],
     "notes": "monkeypatch 兼容：节点函数体留在 ingest_router 模块级，framework 不静态 import"},
    {"code": "ETL-ORCH-03", "rid": "R4", "name": "24 字段统一契约（frozen v1.0）",
     "layer": "ETL-ORCH", "keywords": ["契约", "24字段", "frozen", "api_contract"],
     "summary": "下游 ADAPTER/DELETE/MIGRATE 禁止自定数据结构。必填：chunk_id(int64)/chunk_text/embedding/project_type/doc_unique_id/meta(JSON)；可选：agent_role/node_type/doc_category/version/valid/tag/tongue_shard/pulse_position/pulse_main/pulse_sub/coating_tag/created_at/updated_at/source_mtime/business_category/content_hash/fragment_type/fragment_seq",
     "src": [{"file": "deliverables/tongue-etl-merge-v1/api_contract.json", "pattern": "B_chunks_unified_fields"}],
     "config": [], "params": {},
     "depends": ["ETL-ORCH-06", "ETL-CHUNK-01"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::build_chunks", "tongue_diagnosis/etl/etl_pipeline.py::_sync_doc_outbox"],
     "risk_level": "高", "risk_desc": "契约结构冻结；新增/改名/删除字段需同步 ADAPTER/DELETE/MIGRATE 全部消费方",
     "history": ["2026-08-05 三线合一冻结统一 24 字段（api_contract.json）"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": "边界：契约文本写 384 维，实际 BGE-M3 1024 维（见 ETL-VEC-01）"},
    {"code": "ETL-ORCH-04", "rid": "R6", "name": "写路径单点",
     "layer": "ETL-ORCH", "keywords": ["写路径", "单点", "_sync_doc_outbox"],
     "summary": "写路径只允许出现一次 _sync_doc_outbox；禁止新代码 import etl.core.general / etl.dispatcher / etl.worker（废弃线）",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_outbox"}],
     "config": [], "params": {},
     "depends": ["ETL-CHECK-03"],
     "consumers": [],
     "risk_level": "中", "risk_desc": "新增写路径即违反契约；废弃模块 import 复活会双写",
     "history": ["2026-08-05 通用文档 ETL 整线删除并入三线合一"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": ""},
    {"code": "ETL-ORCH-05", "rid": "R7", "name": "三源通道判定（CC-07）",
     "layer": "ETL-ORCH", "keywords": ["通道", "source_type", "tongue", "pdf", "general", "project_type"],
     "summary": "source_meta.source_type 优先（tongue/pdf/general）；否则扩展名推导：.rag_doc.md→tongue、.pdf→pdf、其余→general。project_type：pdf→pdf_import、general→general、tongue→meta 透传",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_resolve_channel"}],
     "config": [], "params": {},
     "depends": ["ETL-CHUNK-04"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::build_chunks"],
     "risk_level": "中", "risk_desc": "通道判定影响切片选择与 project_type 标记；客服侧无 project_type 过滤（K11）",
     "history": ["2026-08-05 三线合一新增三源标记"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": ""},
    {"code": "ETL-ORCH-06", "rid": "R10", "name": "meta.id_meta 统一结构",
     "layer": "ETL-ORCH", "keywords": ["meta", "id_meta", "JSON"],
     "summary": "固定键 {id_generation_mode: content_hash_int64, channel, doc_unique_id, chunk_seq, display_id_rule: 统一规则v1}；PDF 附加 source_filename/paragraph_seq/sentence_seq/pdf_extend（chunk_cover_page/block_type）",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_chunk_meta"}],
     "config": [], "params": {"id_generation_mode": "content_hash_int64", "display_id_rule": "统一规则v1"},
     "depends": ["ETL-ORCH-03", "ETL-CHUNK-01"],
     "consumers": ["backend/customer_service/rag_engine.py（素材元数据回读）"],
     "risk_level": "中", "risk_desc": "检索侧读取 meta 字段；结构变更影响存量数据可读性",
     "history": ["2026-08-05 三线合一统一 meta 结构"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": ""},
    {"code": "ETL-ORCH-07", "rid": "R12", "name": "skill_gen retro 打标块",
     "layer": "ETL-ORCH", "keywords": ["skill_gen", "retro", "复盘", "打标"],
     "summary": "source_type==skill_gen 强制覆写：project_type=skill_gen / node_type=archive / pulse_main=佳脉 / coating_tag=复盘经验 / tongue_shard=tongue_spleen / pulse_position=guan / business_category=佳脉",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_build_chunks"}],
     "config": [], "params": {"project_type": "skill_gen", "node_type": "archive", "pulse_main": "佳脉", "coating_tag": "复盘经验", "tongue_shard": "tongue_spleen", "pulse_position": "guan", "business_category": "佳脉"},
     "depends": ["ETL-ORCH-03"],
     "consumers": ["~/.claude/retro-skills-registry 复盘入库链路（GENERATE 落库）"],
     "risk_level": "中", "risk_desc": "复盘入库检索（source_type 直召回 K12 skill_gen 映射）依赖此覆写",
     "history": ["2026-08-05 三线合一加入 retro 打标块"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": ""},
    {"code": "ETL-ORCH-08", "rid": "R32", "name": "ETL 配置项",
     "layer": "ETL-ORCH", "keywords": ["配置", "etl.yaml", "workers", "reconcile"],
     "summary": "workers=4 / max_retry_rounds=5 / reconcile.enabled=true / reconcile.batch_size=200 / peak.defer_enabled=true / peak.max_inflight_docs=8 / kb_quota.enabled=true / kb_quota.max_chunks_per_shard=0（0=不限）",
     "src": [{"file": "tongue_diagnosis/etl_config/etl.yaml", "pattern": "etl:"}],
     "config": ["tongue_diagnosis/etl_config/etl.yaml"],
     "params": {"workers": 4, "max_retry_rounds": 5, "reconcile.enabled": True, "reconcile.batch_size": 200,
                "peak.defer_enabled": True, "peak.max_inflight_docs": 8,
                "kb_quota.enabled": True, "kb_quota.max_chunks_per_shard": 0},
     "depends": ["ETL-VEC-03", "ETL-CHECK-05"],
     "consumers": ["tongue_diagnosis/etl/etl_pipeline.py::_parallel_write_chunks",
                   "tongue_diagnosis/etl/etl_pipeline.py::_load_reconcile_config（Phase 9 岁修触发）",
                   "tongue_diagnosis/etl/ingest_router.py::_load_peak_config/_load_quota_config"],
     "risk_level": "中", "risk_desc": "workers/重试轮数影响并行写一致性窗口；peak/kb_quota 闸值影响入库吞吐与延迟；reconcile.batch_size 仍未消费（run_reconcile 无 batch 入参）",
     "history": ["2026-08-05 v3.0 覆写写入配置定稿",
                 "2026-08-10 都江堰 W2/W3/W4：新增 peak/kb_quota 段；reconcile.enabled 接线 Phase 9（_fire_reconcile 后台线程）"],
     "tests": ["tests/test_tongue_etl/test_parallel_write.py", "tests/test_tongue_etl/test_reconciler.py",
               "tests/test_tongue_etl/test_peak_gate.py", "tests/test_tongue_etl/test_quota_gate.py"],
     "notes": ""},
    {"code": "ETL-ORCH-09", "rid": "R33", "name": "peak 洪峰闸（鱼嘴 E12 deferred）",
     "layer": "ETL-ORCH", "keywords": ["洪峰", "peak", "deferred", "并发闸", "E12"],
     "summary": "入口前置并发占位闸：_INFLIGHT_DOCS 全局计数 + threading.Lock；inflight >= max_inflight_docs → E12 整文档 deferred（outbox 记账 status=deferred，不写向量库，不重试即丢，岁修重放后自然入库）；管道执行完 finally _peak_exit 释放占位（下限 0）；defer_enabled=false 时闸停用",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_peak_try_enter"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_peak_exit"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_write_deferred"}],
     "config": ["tongue_diagnosis/etl_config/etl.yaml"],
     "params": {"peak.defer_enabled": True, "peak.max_inflight_docs": 8},
     "depends": ["ETL-CHECK-03"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::route_and_ingest"],
     "risk_level": "中", "risk_desc": "进程内计数器——多进程部署下各进程独立计数（不跨进程限流）；异常路径 finally 释放防泄漏",
     "history": ["2026-08-10 都江堰 W2：实证放弃 peak_overflow_ratio 自适应分流，改并发占位闸 + deferred 出口"],
     "tests": ["tests/test_tongue_etl/test_peak_gate.py"],
     "notes": "deferred 文档由 reconciler 跳过对账；重放入库走同一入口自然纳入"},
    {"code": "ETL-ORCH-10", "rid": "R34", "name": "kb_quota 宝瓶口配额闸（E13 deferred）",
     "layer": "ETL-ORCH", "keywords": ["配额", "quota", "deferred", "宝瓶口", "E13"],
     "summary": "9 节点链第 5 位 quota 节点（abort）：分片=单文档（tongue_{doc_unique_id}），故单分片配额 ≡ 单文档 chunk 数上限，纯查询式无需 ALTER TABLE；len(chunks) > max_chunks_per_shard → state.error 置 E13 → 整文档 deferred（同 _write_deferred 出口）；enabled=false 或 limit<=0 放行",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_quota"}],
     "config": ["tongue_diagnosis/etl_config/etl.yaml"],
     "params": {"kb_quota.enabled": True, "kb_quota.max_chunks_per_shard": 0},
     "depends": ["ETL-ORCH-02", "ETL-CHECK-03"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::_run_pipeline（E13 → deferred 返回）"],
     "risk_level": "中", "risk_desc": "默认 0=不限即不生效；开启后超限文档延后入库（不丢失）；等值边界放行（>才拦截）",
     "history": ["2026-08-10 都江堰 W3：实证放弃 ALTER TABLE 配额字段方案（W5 随之废弃），改查询式文档级配额"],
     "tests": ["tests/test_tongue_etl/test_quota_gate.py"],
     "notes": "边界等值放行已测；E13 文案断言于测试"},
    # ── ETL-PREP 预处理清洗 ──
    {"code": "ETL-PREP-01", "rid": "R11", "name": "coating_tag_index 打标链",
     "layer": "ETL-PREP", "keywords": ["脉象", "苔质", "脏腑", "脉位", "coating_tag", "打标"],
     "summary": "脉象→苔质→脏腑分片→脉位四层推断；脉象→苔质硬映射（佳脉→光洁明润苔/平和脉→薄白淡苔/短脉→白腻苔/滑脉→白厚腻苔/洪脉→黄燥苔/涩脉→灰浊燥苔）；6 类脉象关键词兜底 _PULSE_FALLBACK=平和脉；9 脏腑分片关键词 10 条（舌尖→tip…兜底 full）；分片→脉位映射（tip/heart/liver→cun；spleen/stomach/gall→guan；kidney/body_fluid/coat_color/full→chi）",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "coating_tag_index"},
             {"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "classify_business_category"}],
     "config": [], "params": {"_PULSE_FALLBACK": "平和脉"},
     "depends": ["ETL-ORCH-03"],
     "consumers": ["tongue_diagnosis/retrieval/bm25_index.py（pulse_position 三分区）", "backend/customer_service/rag_engine.py（元数据过滤）"],
     "risk_level": "中", "risk_desc": "映射表改动影响 BM25 三分区归属与检索分层；脉象关键词兜底影响无关键词文档",
     "history": ["2026-08-05 舌苔 v3.0 沿用"],
     "tests": ["tests/test_tongue_etl/test_cs_mapping.py", "tests/test_tongue_etl/test_ingest_router.py"],
     "notes": "chunk_id 在打标后计算（build_chunks 先 coating_tag_index 再 compute_chunk_id）"},
    {"code": "ETL-PREP-02", "rid": "R22", "name": "parser 注册表规则",
     "layer": "ETL-PREP", "keywords": ["parser", "注册表", "格式", "get_parser"],
     "summary": "路由层零解析逻辑；register(exts) 装饰器注册、get_parser(path) 按后缀命中，未注册→ValueError；.rag_doc.md 优先拦截（防 .md 被 text_parser 吞掉）；parser 协议返回 dict 必含 raw_text，可选 sections/pdf_extend/parse_errors",
     "src": [{"file": "tongue_diagnosis/etl/parsers/__init__.py", "fn": "register"},
             {"file": "tongue_diagnosis/etl/parsers/__init__.py", "fn": "get_parser"}],
     "config": [], "params": {},
     "depends": ["ETL-ORCH-01", "ETL-RETRY-01"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::_node_parse"],
     "risk_level": "中", "risk_desc": "新格式=注册新 parser（14 种已注册：.rag_doc.md/.pdf/.txt/.md/.docx/.doc/.wps/.xlsx/.xls/.csv/.pptx/.ppt/.html/.htm）；未注册→E1 error",
     "history": ["2026-08-05 通用文档 ETL 6 parser 迁入 + pdf parser 注册"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": "supported_exts()/PARSER_REGISTRY 对外能力"},
    {"code": "ETL-PREP-03", "rid": "R27", "name": "PDF 文本预处理",
     "layer": "ETL-PREP", "keywords": ["水印", "清洗", "噪声", "dirty"],
     "summary": "水印检测：短行重复 ≥ max(watermark_repeat_min, 总行数×watermark_repeat_ratio)；模式：纯数字页码/URL/confidential/draft/版权字样，最多 watermark_max_count 条。脏数据判定（任一触发 needs_clean）：控制字符>control_char_max/连续换行≥newline_min_run/孤立单字符行>orphan_line_max/噪声字符占比>noise_ratio。全局清洗：统一换行、压缩连续换行为 2、去除重复短行（≤short_line_dedup_max_len 字符）。全部阈值经 load_weir_height() 读 chunking.yaml weir_height 段（9 字段，默认值兜底+模块缓存）",
     "src": [{"file": "backend/api/pdf_storage.py", "fn": "_detect_watermark"},
             {"file": "backend/api/pdf_storage.py", "fn": "_detect_dirty_data"},
             {"file": "backend/api/pdf_storage.py", "fn": "_global_clean_pdf_text"},
             {"file": "tongue_diagnosis/etl/weir_height.py", "fn": "load_weir_height"}],
     "config": ["tongue_diagnosis/etl_config/chunking.yaml"],
     "params": {"watermark_repeat_min": 3, "watermark_repeat_ratio": 0.05, "watermark_max_count": 20,
                "noise_ratio": 0.05, "control_char_max": 5, "orphan_line_max": 5,
                "newline_min_run": 3, "newline_target_run": 2, "short_line_dedup_max_len": 40},
     "depends": ["ETL-CHUNK-05"],
     "consumers": ["backend/api/pdf_storage.py::_global_preprocess_pdf_text"],
     "risk_level": "中", "risk_desc": "预处理质量直接影响切片与检索命中；误删正文短行=信息丢失",
     "history": ["2026-08-05 三线合一沿用 PDF 预处理",
                 "2026-08-10 都江堰 W1：9 项阈值从代码常量收敛至 chunking.yaml weir_height 段（newline_target_run 配置存在但代码压缩目标写死 2，未消费）"],
     "tests": ["tests/test_tongue_etl/test_pdf_adapter.py"],
     "notes": ""},
    {"code": "ETL-PREP-04", "rid": "R29", "name": "PDF dataset_id 关键词路由",
     "layer": "ETL-PREP", "keywords": ["dataset_id", "关键词", "分类"],
     "summary": "corrupt→Corrupt Dataset；block/stuck/timeout/积压→Block Dataset；peak/burst/并发→Peak Dataset；redundant/expired/归档→Redundant Dataset；benchmark/标杆→Healthy Dataset；默认 Peaceful Dataset",
     "src": [{"file": "backend/api/pdf_storage.py", "fn": "_route_pdf_dataset"}],
     "config": [], "params": {"默认": "Peaceful Dataset"},
     "depends": [],
     "consumers": ["backend/api/pdf_storage.py::upload_pdf"],
     "risk_level": "低", "risk_desc": "关键词命中顺序决定分类归属；仅影响展示分类",
     "history": ["2026-08-05 三线合一沿用"],
     "tests": ["tests/test_tongue_etl/test_pdf_api_switch.py"],
     "notes": ""},
    {"code": "ETL-PREP-05", "rid": "R30", "name": "业务数据集分类映射",
     "layer": "ETL-PREP", "keywords": ["分类", "脉象", "docs_raw"],
     "summary": "docs_raw 目录→6 类脉象：spec_test_spec/…→佳脉；spec_business_spec/requirement/skill_docs/root→平和脉；bug_record/after_support→短脉；archive→滑脉；前缀匹配，默认平和脉",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "classify_business_category"}],
     "config": [], "params": {"默认": "平和脉"},
     "depends": [],
     "consumers": ["tongue_diagnosis/etl/etl_pipeline.py::run_etl"],
     "risk_level": "低", "risk_desc": "前缀匹配顺序敏感；仅影响 business_category 标注",
     "history": ["2026-08-05 舌苔 v2.0 沿用"],
     "tests": ["tests/test_tongue_etl/test_cs_mapping.py"],
     "notes": ""},
    # ── ETL-CHUNK Chunk分片 ──
    {"code": "ETL-CHUNK-01", "rid": "R5", "name": "chunk_seq 从 1 起（CC-01 冻结）",
     "layer": "ETL-CHUNK", "keywords": ["chunk_seq", "序号", "CC-01"],
     "summary": "禁止下游改 0 起，否则 compute_chunk_id 结果漂移破坏幂等",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "chunk_doc"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_split_raw_text"}],
     "config": [], "params": {"chunk_seq_start": 1},
     "depends": ["ETL-CHECK-01"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::build_chunks"],
     "risk_level": "高", "risk_desc": "序号起点变更→全部 chunk_id 漂移→全库重灌；CC-01 冻结",
     "history": ["2026-08-05 三线合一冻结"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": ""},
    {"code": "ETL-CHUNK-02", "rid": "R13", "name": "chunk_doc 四级语义切片",
     "layer": "ETL-CHUNK", "keywords": ["切片", "语义", "chunk_doc", "min_chars", "max_chars", "overlap"],
     "summary": "L1 保护区（<!--CHUNK_PROTECT--> 整块不拆）→ L2 语义合并（<min_chars 并入前块）→ L3 原生标题拆分（仅 ##/### 切分，# 保留）→ L4 阈值硬切（按段落/句子，段落间加 overlap）。默认 min_chars=300/max_chars=600/overlap=50；无法定位的 paragraph_seq/sentence_seq 置 None（禁止编造）",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "chunk_doc"},
             {"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "_load_chunking_config"}],
     "config": ["tongue_diagnosis/etl_config/chunking.yaml"],
     "params": {"min_chars": 300, "max_chars": 600, "overlap": 50},
     "depends": ["ETL-CHUNK-01"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::_sections_to_chunks", "tongue_diagnosis/etl/etl_pipeline.py::run_etl"],
     "risk_level": "高", "risk_desc": "切片参数/逻辑变化→chunk_text 变化→chunk_id 全变→全量重灌+BM25 重建",
     "history": ["2026-08-05 舌苔 v3.0 沿用（四级语义切片）"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py", "tests/test_tongue_etl/test_framework.py"],
     "notes": "chunking.yaml 中配置（检查实际文件层级）"},
    {"code": "ETL-CHUNK-03", "rid": "R14", "name": "通用通道兜底分片",
     "layer": "ETL-CHUNK", "keywords": ["raw_text", "兜底", "段落"],
     "summary": "raw_text 按 \\n\\n 段落聚合 ≥600 字符成块（chunk_seq 1 起）；有语义 sections 走 sections→markdown→chunk_doc（header→#×level、code→``` 围栏）",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_split_raw_text"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_sections_to_chunks"}],
     "config": [], "params": {"max_chars": 600},
     "depends": ["ETL-CHUNK-02"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::_node_chunk"],
     "risk_level": "中", "risk_desc": "兜底切片无语义保护；通用通道文档切片质量依赖此路径",
     "history": ["2026-08-05 通用文档 ETL 并入统一管道"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": ""},
    {"code": "ETL-CHUNK-04", "rid": "R15", "name": "通道切片选择",
     "layer": "ETL-CHUNK", "keywords": ["直通", "sections", "切片选择"],
     "summary": "tongue/pdf 且有 sections→sections 直通不重切；否则语义 sections 重切；再否则 raw_text 兜底；空结果→E3 短路",
     "src": [{"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_chunk"}],
     "config": [], "params": {},
     "depends": ["ETL-CHUNK-03", "ETL-RETRY-01"],
     "consumers": [],
     "risk_level": "中", "risk_desc": "选择顺序决定三通道切片路径（C15 双通道直通）",
     "history": ["2026-08-05 三线合一新增"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py", "tests/test_tongue_etl/test_framework.py"],
     "notes": "E3 空内容：chunk 节点自设 state.error 短路，outbox 未写"},
    {"code": "ETL-CHUNK-05", "rid": "R28", "name": "PDF 切片与 block_type",
     "layer": "ETL-CHUNK", "keywords": ["PDF", "block_type", "页码映射"],
     "summary": "段落聚合 ≤600 字符、chunk 间 50 overlap、页码均匀映射 start_page=(i*total_pages//n)+1；block_type：单行 title 大写<120 字→header、含 |.*|.*|→table、含 def/class/import→code、行首 ^\\d+[.、]→list、否则 para",
     "src": [{"file": "backend/api/pdf_storage.py", "fn": "_split_paragraphs_and_pages"},
             {"file": "backend/api/pdf_storage.py", "fn": "_block_tag_and_fragment_clean"}],
     "config": [], "params": {"段落上限": 600, "overlap": 50, "start_page": "(i*total_pages//n)+1"},
     "depends": ["ETL-PREP-03", "ETL-CHUNK-01"],
     "consumers": ["backend/api/pdf_storage.py::chunk_pdf"],
     "risk_level": "中", "risk_desc": "block_type 判定顺序敏感；页码映射影响 pdf_extend.chunk_cover_page",
     "history": ["2026-08-05 三线合一沿用"],
     "tests": ["tests/test_tongue_etl/test_pdf_adapter.py"],
     "notes": ""},
    # ── ETL-VEC 向量化写入 ──
    {"code": "ETL-VEC-01", "rid": "R16", "name": "embedding 全局单点配置",
     "layer": "ETL-VEC", "keywords": ["embedding", "BGE-M3", "维度", "embedding.yaml"],
     "summary": "模型/维度/设备统一读 config/embedding.yaml，三链路共用，禁止硬编码。当前：BAAI/bge-m3、1024 维、device=mps、batch=32；内置 HF_ENDPOINT=hf-mirror.com；sentence-transformers 优先、transformers 均值池化兜底（truncation 256）、懒加载",
     "src": [{"file": "etl/common/embedding_config.py", "fn": "get_embedding_config"},
             {"file": "tongue_diagnosis/vector_store/lancedb_manager.py", "fn": "compute_embeddings"}],
     "config": ["config/embedding.yaml"],
     "params": {"model_name": "BAAI/bge-m3", "dimension": 1024, "device": "mps", "batch_size": 32},
     "depends": [],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::_compute_embeddings", "tongue_diagnosis/vector_store/lancedb_manager.py::compute_embeddings"],
     "risk_level": "高", "risk_desc": "维度变更需向量库全量重建；模型切换影响检索语义；契约 api_contract 仍写 384 维（已知边界）",
     "history": ["2026-08-04 BGE-M3 升级 1024 维（embedding.yaml 注释）"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py"],
     "notes": "边界 1：契约文本 384 vs 实际 1024 漂移"},
    {"code": "ETL-VEC-02", "rid": "R17", "name": "覆写写入语义（v3.0）",
     "layer": "ETL-VEC", "keywords": ["覆写", "merge_insert", "幂等"],
     "summary": "merge_insert(chunk_id).when_matched_update_all().when_not_matched_insert_all()——同 ID 更新、新 ID 追加；同一 chunk_id 重试只会覆盖，永不追加新行",
     "src": [{"file": "tongue_diagnosis/vector_store/lancedb_manager.py", "fn": "write_chunks_overwrite"}],
     "config": [], "params": {"写入模式": "merge_insert on chunk_id"},
     "depends": ["ETL-CHECK-01"],
     "consumers": ["tongue_diagnosis/etl/etl_pipeline.py::_parallel_write_chunks", "tongue_diagnosis/etl/etl_pipeline.py::etl_single_doc"],
     "risk_level": "高", "risk_desc": "v3.0 核心；改回 upsert 语义破坏幂等（旧 upsert_chunks 保留给 retro_skill_writer/迁移脚本）",
     "history": ["2026-08-05 v3.0 覆写一致性改造（根治重试双倍行）"],
     "tests": ["tests/test_tongue_etl/test_overwrite_write.py", "tests/test_tongue_etl/test_parallel_write.py"],
     "notes": ""},
    {"code": "ETL-VEC-03", "rid": "R18", "name": "并行写与重试",
     "layer": "ETL-VEC", "keywords": ["并行", "workers", "重试", "线程池"],
     "summary": "按文档分组→组内 chunks[i::workers] 互不相交子集→线程池并行覆写；失败子集逐轮重试，每轮独立新连接。默认 workers=4 / max_retry_rounds=5",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "_parallel_write_chunks"},
             {"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "_write_subset"}],
     "config": ["tongue_diagnosis/etl_config/etl.yaml"],
     "params": {"workers": 4, "max_retry_rounds": 5},
     "depends": ["ETL-VEC-02", "ETL-ORCH-08"],
     "consumers": ["tongue_diagnosis/etl/etl_pipeline.py::run_etl", "tongue_diagnosis/etl/etl_pipeline.py::etl_single_doc"],
     "risk_level": "高", "risk_desc": "workers/重试轮数影响一致性窗口；E5 部分失败→partial_ready+last_error（列前 5 缺失 chunk_id）",
     "history": ["2026-08-05 v3.0 多线程并行写"],
     "tests": ["tests/test_tongue_etl/test_parallel_write.py"],
     "notes": ""},
    {"code": "ETL-VEC-04", "rid": "R26", "name": "BM25 三重索引",
     "layer": "ETL-VEC", "keywords": ["BM25", "pulse_position", "cun", "guan", "chi"],
     "summary": "按 pulse_position（cun/guan/chi）物理隔离三个 .pkl 分区；无状态、可从 LanceDB 全量重建；中文按字/英文按空格分词（rank_bm25 BM25Okapi）；默认 top_k=20；支持 tongue_shard/pulse_main 元数据预过滤再评分；结果含 chunk_id/bm25_score(round4)/rank/text/tongue_shard/pulse_main",
     "src": [{"file": "tongue_diagnosis/retrieval/bm25_index.py", "fn": "BM25IndexManager.build_all"},
             {"file": "tongue_diagnosis/retrieval/bm25_index.py", "fn": "BM25IndexManager.search_all"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_rebuild_bm25_for_chunks"}],
     "config": [], "params": {"top_k": 20, "分区": "cun/guan/chi"},
     "depends": ["ETL-PREP-01"],
     "consumers": ["backend/customer_service/rag_engine.py（BM25 反幻觉门禁 0.5 / 双路召回）"],
     "risk_level": "中", "risk_desc": "客服检索门禁依赖；E8 失败仅告警降级由 reconciler 自愈",
     "history": ["2026-08-05 三线合一内嵌重建（按 pulse_position 分区）"],
     "tests": ["tests/test_tongue_etl/test_ingest_router.py", "tests/test_tongue_etl/test_framework.py"],
     "notes": ""},
    # ── ETL-CHECK 一致性对账 ──
    {"code": "ETL-CHECK-01", "rid": "R8", "name": "content-hash chunk_id（幂等基石）",
     "layer": "ETL-CHECK", "keywords": ["chunk_id", "md5", "int64", "幂等"],
     "summary": "chunk_id = md5(doc_unique_id|chunk_seq|chunk_text) 前 8 字节 → 正整数 int64；同内容幂等覆写，内容变更产生新 ID（旧行由 reconciler 清除）",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "compute_chunk_id"}],
     "config": [], "params": {"算法": "md5(doc_unique_id|chunk_seq|chunk_text) 前 8 字节→int64"},
     "depends": ["ETL-CHUNK-01", "ETL-CHUNK-02"],
     "consumers": ["tongue_diagnosis/etl/ingest_router.py::build_chunks", "tongue_diagnosis/vector_store/lancedb_manager.py（主键）"],
     "risk_level": "高", "risk_desc": "算法改动→全库 chunk_id 失效；doc_unique_id/chunk_seq/chunk_text 任一参与方变化即漂移",
     "history": ["2026-08-05 v3.0 稳定 chunk_id（根治重试双倍行）"],
     "tests": ["tests/test_tongue_etl/test_overwrite_write.py", "tests/test_tongue_etl/test_chunk_id.py"],
     "notes": "跨 source_type 全局唯一（chunk_id_generator 存量对齐约束）"},
    {"code": "ETL-CHECK-02", "rid": "R9", "name": "辅助哈希",
     "layer": "ETL-CHECK", "keywords": ["doc_unique_id", "content_hash", "sha256"],
     "summary": "doc_unique_id = sha256(doc_path)[:16]；content_hash = sha256(doc_unique_id+chunk_text) 完整 hex 供旧调用方去重",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "compute_doc_unique_id"},
             {"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "compute_content_hash"}],
     "config": [], "params": {"doc_unique_id": "sha256(doc_path)[:16]", "content_hash": "sha256(doc_unique_id+chunk_text) hex"},
     "depends": ["ETL-CHECK-01"],
     "consumers": ["backend/api/pdf_storage.py（删除三候选 doc_unique_id 之一）"],
     "risk_level": "低", "risk_desc": "doc_unique_id 计算方式影响删除匹配与 shard 命名",
     "history": ["2026-08-05 沿用"],
     "tests": ["tests/test_tongue_etl/test_overwrite_write.py"],
     "notes": ""},
    {"code": "ETL-CHECK-03", "rid": "R19", "name": "outbox 记账状态机",
     "layer": "ETL-CHECK", "keywords": ["outbox", "full_ready", "partial_ready", "pending", "后置校验"],
     "summary": "pending→full_ready（幂等终态）| pending→partial_ready（终态，missing 记 last_error）| deferred（E12/E13 延迟终态：洪峰/配额超限整文档延后，0 写 0 缺，reconciler 跳过对账，重放后自然入库）；写入前 upsert(pending)→写后独立连接 check_chunks_exist 后置校验（异常全判缺失）→全齐 full_ready/有缺 partial_ready；写入线程不更新 outbox（统一主线程记账防并发竞态）",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "_sync_doc_outbox"},
             {"file": "tongue_diagnosis/etl/sql_meta.py", "fn": "upsert_outbox"},
             {"file": "tongue_diagnosis/etl/sql_meta.py", "fn": "mark_doc_ready"},
             {"file": "tongue_diagnosis/vector_store/lancedb_manager.py", "fn": "check_chunks_exist"}],
     "config": [], "params": {"状态机": "pending→full_ready|partial_ready（幂等终态）；deferred（E12/E13 延迟终态）", "缺失展示": "前 5 个 chunk_id"},
     "depends": ["ETL-VEC-03", "ETL-CHECK-01"],
     "consumers": ["tongue_diagnosis/etl/reconciler.py::run_reconcile", "scripts/rebuild_kb_from_retro_skills.py（幂等重跑）"],
     "risk_level": "高", "risk_desc": "记账一致性：异常全判缺失→partial 误报；E7 后置校验缺失不做全删回滚（覆写语义下删除破坏幂等）",
     "history": ["2026-08-05 v3.0 A 文档记账（expected/written chunk_id 集合）",
                 "2026-08-10 都江堰 W2/W3：新增 deferred 状态（E12/E13 延迟入库出口 _write_deferred）"],
     "tests": ["tests/test_tongue_etl/test_sql_meta.py", "tests/test_tongue_etl/test_overwrite_write.py"],
     "notes": "outbox 异常 propagate 上抛（三方调用方依赖）"},
    {"code": "ETL-CHECK-04", "rid": "R20", "name": "shard_meta 写规则",
     "layer": "ETL-CHECK", "keywords": ["shard_meta", "index_manifest", "ready"],
     "summary": "向量+BM25 强一致后同步写；shard_name=tongue_{doc_unique_id}；min/max_chunk_id/chunk_count/status=ready；index_manifest 承载 pdf_extend 文档级字段（契约 D1）；失败仅告警由 reconciler 自愈；不用 daemon 线程",
     "src": [{"file": "tongue_diagnosis/etl/etl_pipeline.py", "fn": "_write_shard_meta_sync"},
             {"file": "tongue_diagnosis/etl/sql_meta.py", "fn": "write_shard_meta"}],
     "config": [], "params": {"shard_name": "tongue_{doc_unique_id}", "status": "ready"},
     "depends": ["ETL-VEC-04"],
     "consumers": ["backend/customer_service/kb_shard.py（分片区间 min/max 检索约束 K9）"],
     "risk_level": "中", "risk_desc": "客服检索按 shard 区间收敛；shard 缺失→检索扫描退化或空结果",
     "history": ["2026-08-05 v3.0 shard_meta 同步写"],
     "tests": ["tests/test_tongue_etl/test_sql_meta.py"],
     "notes": "index_manifest 合并 pdf_extend（_node_shard_meta 组装）"},
    {"code": "ETL-CHECK-05", "rid": "R21", "name": "reconciler 集合级对账",
     "layer": "ETL-CHECK", "keywords": ["对账", "孤儿", "自愈", "reconciler"],
     "summary": "① 孤儿清除（向量表中非 expected_chunk_ids 旧行按 chunk_id 删）② shard_meta 自愈（缺失/不符/非 ready 补写）③ 缺失统计 ④ deferred 跳过（洪峰/配额延迟文档未入库，直接 continue 不误判缺失，重放后自然纳入）。统计键 {docs, orphan_removed, missing_chunks, shard_meta_repaired}",
     "src": [{"file": "tongue_diagnosis/etl/reconciler.py", "fn": "run_reconcile"}],
     "config": ["tongue_diagnosis/etl_config/etl.yaml"],
     "params": {"统计键": "docs/orphan_removed/missing_chunks/shard_meta_repaired", "batch_size": 200},
     "depends": ["ETL-CHECK-03", "ETL-CHECK-04"],
     "consumers": ["tongue_diagnosis/etl/etl_pipeline.py::_fire_reconcile（Phase 9 主流水线完成后 daemon 线程触发，reconcile.enabled 门控）",
                   "scripts/reconcile_daily_clean.py（岁修 CLI，JSON stdout，失败 exit 1）", "运维巡检/scripts 定时任务"],
     "risk_level": "中", "risk_desc": "孤儿清除需 chunk_id 稳定；误删=数据丢失（双下标差集删除语义）",
     "history": ["2026-08-05 v3.0 集合级对账器新增",
                 "2026-08-10 都江堰 W4/W6：Phase 9 主流水线接线（_load_reconcile_config + _fire_reconcile）；deferred 文档跳过；reconcile_daily_clean.py 岁修脚本"],
     "tests": ["tests/test_tongue_etl/test_reconciler.py"],
     "notes": ""},
    # ── ETL-STORE 隔离存储 ──
    {"code": "ETL-STORE-01", "rid": "R23", "name": "SqliteRangeIdGenerator 存量对齐",
     "layer": "ETL-STORE", "keywords": ["chunk_id", "区间预分配", "存量对齐", "SqliteRangeIdGenerator"],
     "summary": "初始化时 last_allocated 对齐 dataset_chunk_meta.MAX(chunk_id)（跨 source_type 全局唯一），防表重建后分配撞既有行；区间预分配",
     "src": [{"file": "etl/common/chunk_id_generator.py", "fn": "SqliteRangeIdGenerator"}],
     "config": [], "params": {"对齐源": "dataset_chunk_meta.MAX(chunk_id)"},
     "depends": ["ETL-CHECK-01"],
     "consumers": ["旧存量写入路径（迁移/旧调用方）"],
     "risk_level": "中", "risk_desc": "表重建后不对齐→分配撞既有行；CHUNK_ID_GENERATOR_MODE 选择否则按 DATABASE_URL 推断",
     "history": ["2026-08-05 三线合一 chunk_id 对齐"],
     "tests": ["tests/test_tongue_etl/test_chunk_id.py"],
     "notes": ""},
    {"code": "ETL-STORE-02", "rid": "R24", "name": "PDF 删除五层清理",
     "layer": "ETL-STORE", "keywords": ["删除", "五层", "pdf_storage"],
     "summary": "① 向量行（三候选 doc_unique_id：登记值/compute_doc_unique_id/存量 PDF-{id}）→② outbox+shard_meta→③ DatasetChunkMeta 存量 pdf 行→④ 物理文件→⑤ 轻量登记",
     "src": [{"file": "backend/api/pdf_storage.py", "fn": "delete_pdf"}],
     "config": [], "params": {},
     "depends": ["ETL-CHECK-03", "ETL-STORE-03"],
     "consumers": ["前端 delete 按钮→/api/dataset-ops/pdf DELETE"],
     "risk_level": "高", "risk_desc": "漏层=孤儿数据残留；删错=用户数据丢失（三候选 ID 匹配容错）",
     "history": ["2026-08-05 三线合一五层删除链路"],
     "tests": ["tests/test_tongue_etl/test_pdf_api_switch.py", "tests/test_tongue_etl/test_pdf_sql_deprecate.py"],
     "notes": ""},
    {"code": "ETL-STORE-03", "rid": "R25", "name": "pdf_index.json 轻量登记",
     "layer": "ETL-STORE", "keywords": ["pdf_index", "轻量登记", "原子写"],
     "summary": "字段 id/file_name/file_path/file_size/created_at/parsed/chunk_count/total_pages/dataset_id/error/doc_unique_id；原子写入（.tmp+replace）；list 自愈 _heal_pdf_index 三方对齐（物理文件+migration_map+向量库，按 meta.source_filename 反查 doc_unique_id、从 index_manifest.total_page 回填）",
     "src": [{"file": "backend/api/pdf_storage.py", "fn": "_load_pdf_index"},
             {"file": "backend/api/pdf_storage.py", "fn": "_save_pdf_index"},
             {"file": "backend/api/pdf_storage.py", "fn": "_heal_pdf_index"}],
     "config": [], "params": {"写入": "原子 .tmp+replace"},
     "depends": [],
     "consumers": ["backend/api/pdf_storage.py::list_pdfs", "backend/api/pdf_storage.py::delete_pdf"],
     "risk_level": "中", "risk_desc": "登记与物理文件/向量库三方不一致→list 自愈补登记；heal 逻辑改动影响回填正确性",
     "history": ["2026-08-05 PDF API 数据源切换（DQ-7）"],
     "tests": ["tests/test_tongue_etl/test_pdf_api_switch.py"],
     "notes": ""},
    {"code": "ETL-STORE-04", "rid": "R31", "name": "并发初始化竞态",
     "layer": "ETL-STORE", "keywords": ["并发", "初始化", "already exists"],
     "summary": "多 worker 同时创建空库，already exists 时幂等二次打开",
     "src": [{"file": "tongue_diagnosis/vector_store/lancedb_manager.py", "fn": "VectorStore._open_or_create"}],
     "config": [], "params": {},
     "depends": [],
     "consumers": ["tongue_diagnosis/vector_store/lancedb_manager.py::VectorStore"],
     "risk_level": "中", "risk_desc": "并发初始化失败→首次并行写报错；幂等二次打开防竞态",
     "history": ["2026-08-05 v3.0 沿用"],
     "tests": ["tests/test_tongue_etl/test_parallel_write.py", "tests/test_tongue_etl/test_overwrite_write.py"],
     "notes": ""},
    # ── ETL-RETRY 异常重试 ──
    {"code": "ETL-RETRY-01", "rid": "R3", "name": "E1-E13 错误语义",
     "layer": "ETL-RETRY", "keywords": ["错误语义", "E1", "E8", "E12", "E13", "降级", "partial_ready"],
     "summary": "E1 格式不支持→unsupported format: .xxx 不写 outbox；E2 解析失败→abort 返回 error；E3 空内容→empty content: no chunks produced 短路；E4 embedding 失败→不写 outbox；E5 写入部分失败→重试5轮后 partial_ready+last_error（列前5个缺失 chunk_id）；E6 重试耗尽→partial_ready（迁移重跑幂等）；E7 后置校验缺失→partial_ready，不执行全删回滚；E8 BM25 失败→仅告警降级 reconciler 自愈；E9 shard_meta 写失败→捕获仅告警；E10/E11 迁移中断/源文件缺失→幂等重跑/跳过计入报告；E12 洪峰超限→inflight>=max_inflight_docs 整文档 deferred（outbox 记账不写向量库）；E13 配额超限→shard chunks N>limit 整文档 deferred（同出口）",
     "src": [{"file": "tongue_diagnosis/etl/framework/node.py", "fn": "Node.run"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_parse"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_chunk"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_bm25"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_peak_try_enter"},
             {"file": "tongue_diagnosis/etl/ingest_router.py", "fn": "_node_quota"}],
     "config": [], "params": {"E1 文案": "unsupported format: .xxx", "E3 文案": "empty content: no chunks produced", "E5 重试轮数": 5,
                              "E12 文案": "E12 peak deferred: inflight>=N", "E13 文案": "E13 quota exceeded: shard chunks N>M"},
     "depends": ["ETL-ORCH-02", "ETL-VEC-03"],
     "consumers": ["全部三线调用方（outbox propagate 异常语义）"],
     "risk_level": "高", "risk_desc": "error 文案有测试断言（改文案即红测试）；outbox 异常传播被 pdf_storage/migrate/retro 三方依赖；E7 不做全删回滚是覆写幂等前提",
     "history": ["2026-08-05 框架化改造将 E1-E11 语义落地 error_policy 三分支",
                 "2026-08-10 都江堰 W2/W3：新增 E12（洪峰）/E13（配额）deferred 语义"],
     "tests": ["tests/test_tongue_etl/test_framework.py", "tests/test_tongue_etl/test_ingest_router.py",
               "tests/test_tongue_etl/test_peak_gate.py", "tests/test_tongue_etl/test_quota_gate.py"],
     "notes": "degrade 路径保留原文案「BM25/shard_meta 降级（reconciler 将自愈）」"},
]

RULES_BY_CODE: dict[str, dict] = {r["code"]: r for r in RULES}

# 解析深度分级（二期）：risk_level → priority 默认推导；单条规则可显式写 "priority" 字段覆盖
RISK_TO_PRIORITY = {"高": "P0", "中": "P1", "低": "P2"}


def rule_priority(rule: dict) -> str:
    """规则解析优先级：P0 深度解析 / P1 标准解析 / P2 轻量解析（仅文件存在性检查）。"""
    return rule.get("priority") or RISK_TO_PRIORITY.get(rule["risk_level"], "P1")


def layer_name(code: str) -> str:
    """按编码前缀返回分层中文名。"""
    return next((n for c, n in LAYERS if code.startswith(c)), "未分层")


def downstream_codes(code: str) -> list[str]:
    """计算某规则的下游依赖（被哪些规则 depends）。"""
    return sorted(c for c, r in RULES_BY_CODE.items() if code in r["depends"])


def resolve_dependencies() -> dict[str, list[str]]:
    """返回全量依赖闭包方向图 {code: downstream_codes}。"""
    return {c: downstream_codes(c) for c in RULES_BY_CODE}


# ─── 配置契约清单（第 8 项产出：配置-代码契约漂移检测） ──────────────
# kind=config_field：file=yaml 路径（键实存检查，None 跳过）+ code_file=代码特征串 grep 文件
#   read 特征串（读入代码） + use 特征串（消费于逻辑，use 命中 0 即未接线）
# kind=code_residual：代码内残留参数（symbol 定位函数体 + use 模式命中 0 即 stale）
CONFIG_CONTRACTS: list[dict] = [
    {"kind": "config_field", "rule": "ETL-ORCH-08", "file": "tongue_diagnosis/etl_config/etl.yaml", "key": "etl.workers",
     "code_file": "tongue_diagnosis/etl/etl_pipeline.py", "read": 'config.get("workers"', "use": "workers=config.get",
     "note": "并行写线程数（_write_subset 线程池）"},
    {"kind": "config_field", "rule": "ETL-ORCH-08", "file": "tongue_diagnosis/etl_config/etl.yaml", "key": "etl.max_retry_rounds",
     "code_file": "tongue_diagnosis/etl/etl_pipeline.py", "read": 'config.get("max_retry_rounds"', "use": "max_retry_rounds=config.get",
     "note": "失败子集最大重试轮数"},
    {"kind": "config_field", "rule": "ETL-CHECK-05", "file": "tongue_diagnosis/etl_config/etl.yaml", "key": "reconcile.enabled",
     "code_file": "tongue_diagnosis/etl/etl_pipeline.py", "read": "_load_reconcile_config", "use": 'reconcile_cfg.get("enabled"',
     "note": "2026-08-10 W4 已接线：Phase 9 reconcile_cfg.get(\"enabled\") 门控 _fire_reconcile"},
    {"kind": "config_field", "rule": "ETL-CHECK-05", "file": "tongue_diagnosis/etl_config/etl.yaml", "key": "reconcile.batch_size",
     "code_file": "tongue_diagnosis/etl/reconciler.py", "read": "batch_size", "use": "batch_size",
     "note": "已知漂移：run_reconcile 无 batch_size 入参，字段仍未消费（W4 仅接线 enabled）"},
    {"kind": "config_field", "rule": "ETL-ORCH-09", "file": "tongue_diagnosis/etl_config/etl.yaml", "key": "peak.defer_enabled",
     "code_file": "tongue_diagnosis/etl/ingest_router.py", "read": "_load_peak_config", "use": 'peak["defer_enabled"]',
     "note": "洪峰闸总开关（false 时不占位直接入管道）"},
    {"kind": "config_field", "rule": "ETL-ORCH-09", "file": "tongue_diagnosis/etl_config/etl.yaml", "key": "peak.max_inflight_docs",
     "code_file": "tongue_diagnosis/etl/ingest_router.py", "read": "_load_peak_config", "use": 'peak["max_inflight_docs"]',
     "note": "并发在途文档上限（超限 E12 deferred）"},
    {"kind": "config_field", "rule": "ETL-ORCH-10", "file": "tongue_diagnosis/etl_config/etl.yaml", "key": "kb_quota.enabled",
     "code_file": "tongue_diagnosis/etl/ingest_router.py", "read": "_load_quota_config", "use": 'quota.get("enabled"',
     "note": "配额闸总开关"},
    {"kind": "config_field", "rule": "ETL-ORCH-10", "file": "tongue_diagnosis/etl_config/etl.yaml", "key": "kb_quota.max_chunks_per_shard",
     "code_file": "tongue_diagnosis/etl/ingest_router.py", "read": "_load_quota_config", "use": 'quota.get("max_chunks_per_shard"',
     "note": "单文档 chunk 数上限（0=不限；超限 E13 deferred）"},
    {"kind": "config_field", "rule": "ETL-PREP-03", "file": "tongue_diagnosis/etl_config/chunking.yaml", "key": "weir_height.watermark_repeat_min",
     "code_file": "backend/api/pdf_storage.py", "read": "load_weir_height", "use": 'cfg["watermark_repeat_min"]',
     "note": "水印短行重复下限（与其余 7 字段同经 load_weir_height 消费）"},
    {"kind": "config_field", "rule": "ETL-PREP-03", "file": "tongue_diagnosis/etl_config/chunking.yaml", "key": "weir_height.newline_target_run",
     "code_file": "backend/api/pdf_storage.py", "read": "load_weir_height", "use": 'cfg["newline_target_run"]',
     "note": "已知漂移：配置存在但换行压缩目标写死 2（_global_clean_pdf_text 替换串硬编码 \\n\\n），字段未消费"},
    {"kind": "config_field", "rule": "ETL-VEC-01", "file": "config/embedding.yaml", "key": "model_name",
     "code_file": "tongue_diagnosis/vector_store/lancedb_manager.py", "read": 'cfg["model_name"]', "use": 'SentenceTransformer(cfg["model_name"]',
     "note": "BGE-M3 嵌入模型名（三链路单点）"},
    {"kind": "config_field", "rule": "ETL-VEC-01", "file": "config/embedding.yaml", "key": "dimension",
     "code_file": "tongue_diagnosis/vector_store/lancedb_manager.py", "read": 'cfg["dimension"]', "use": 'get_embedding_config()["dimension"]',
     "note": "向量维度（_get_embedding_dim 消费）"},
    {"kind": "config_field", "rule": "ETL-VEC-01", "file": "config/embedding.yaml", "key": "device",
     "code_file": "tongue_diagnosis/vector_store/lancedb_manager.py", "read": 'cfg["device"]', "use": 'device=cfg["device"]',
     "note": "推理设备 mps/cpu/cuda"},
    {"kind": "config_field", "rule": "ETL-VEC-01", "file": "config/embedding.yaml", "key": "batch_size",
     "code_file": "tongue_diagnosis/vector_store/lancedb_manager.py", "read": 'cfg["batch_size"]', "use": 'cfg["batch_size"]',
     "note": "已知漂移：get_embedding_config 读入返回，ETL 批量计算无消费点"},
    {"kind": "config_field", "rule": "ETL-ORCH-07", "file": None, "key": None,
     "code_file": "backend/customer_service/rag_engine.py", "read": "max_ctx_tokens", "use": "ctx_tokens",
     "note": "已知漂移：schema/DB/API 三处定义（config_schemas/models/config_router），rag_engine 检索链路无消费"},
    {"kind": "code_residual", "rule": "ETL-ORCH-07", "file": None, "key": None,
     "code_file": "backend/customer_service/rag_engine.py", "symbol": "def _rrf_fuse",
     "use": "weights[", "note": "已知漂移：weights 参数存在但实现写死 1.0（注释自认命名空间权重已废弃）；_RRF_K=60 硬编码"},
]

# ─── 运行时配置读取表（原 etl_profiler._CONFIG_READS，迁入注册表结构） ──────
# {规则编码: (配置文件相对路径, [(注册表参数键名, 配置文件点号路径)])}
# 项目自定义注册表 JSON 中以 "config_reads" 键提供同构结构（元组写作数组）。
CONFIG_READS: dict[str, tuple] = {
    "ETL-ORCH-08": ("tongue_diagnosis/etl_config/etl.yaml",
                    [("workers", "etl.workers"), ("max_retry_rounds", "etl.max_retry_rounds"),
                     ("reconcile.enabled", "reconcile.enabled"), ("reconcile.batch_size", "reconcile.batch_size")]),
    "ETL-VEC-01": ("config/embedding.yaml",
                   [("model_name", "model_name"), ("dimension", "dimension"),
                    ("device", "device"), ("batch_size", "batch_size")]),
    "ETL-CHUNK-02": ("tongue_diagnosis/etl_config/chunking.yaml",
                     [("min_chars", "chunking.min_chars"), ("max_chars", "chunking.max_chars"),
                      ("overlap", "chunking.overlap_chars")]),
}


# ═══════════════════════════════════════════════════════════════════════════
# 项目可配置注册表覆盖（通用生态组件改造）
#
# 若 <source_root>/archmap/etl_rule_registry.json 存在，则完全替代内置
# RULES/KEYWORD_INDEX/LAYERS/CONFIG_CONTRACTS/ETL_DETECT_DIRS/CONFIG_READS。
# JSON 结构镜像本模块 Python 数据结构（元组写作数组）：
#   {
#     "layers":           [["ETL-PREP", "预处理清洗"], ...],          # 必需
#     "rules":            [{"code": ..., "rid": ..., ...}, ...],       # 必需，字段同内置 RULES
#     "keyword_index":    {"关键词": ["ETL-XXX-01", ...], ...},        # 必需
#     "config_contracts": [{"kind": ..., "rule": ..., ...}, ...],      # 必需（可为空数组）
#     "etl_detect_dirs":  ["my_etl", ...],                             # 必需（可为空数组）
#     "config_reads":     {"ETL-XXX-01": ["rel.yaml", [["k", "a.b"]]]} # 可选，默认 {}
#   }
# 损坏（非 JSON / 缺必需字段 / 结构非法）时抛 RegistryError（带文件路径与原因），
# 绝不静默回退内置注册表——防止私有规则被误套到不匹配的项目上。
# ═══════════════════════════════════════════════════════════════════════════

REGISTRY_FILENAME = "archmap/etl_rule_registry.json"

_REGISTRY_REQUIRED_KEYS = ("layers", "rules", "keyword_index", "config_contracts", "etl_detect_dirs")

_RULE_REQUIRED_FIELDS = ("code", "rid", "name", "layer", "keywords", "summary", "src",
                         "config", "params", "depends", "consumers",
                         "risk_level", "risk_desc", "history", "tests", "notes")


class RegistryError(ValueError):
    """项目自定义 ETL 注册表损坏（路径与原因见异常信息）。不静默回退内置注册表。"""


class Registry:
    """一份 ETL 规则注册表的解析视图：内置默认 或 项目 JSON 覆盖。

    属性镜像原模块级常量（rules/keyword_index/layers/config_contracts/
    etl_detect_dirs/config_reads/rules_by_code），方法镜像原模块级辅助函数
    （rule_priority/layer_name/downstream_codes/resolve_dependencies）。
    """

    def __init__(self, *, layers, rules, keyword_index, config_contracts,
                 etl_detect_dirs, config_reads=None, source: str = "builtin",
                 path: "Path | None" = None):
        self.layers = [tuple(p) for p in layers]
        self.rules = rules
        self.keyword_index = keyword_index
        self.config_contracts = config_contracts
        self.etl_detect_dirs = tuple(etl_detect_dirs)
        # config_reads：JSON 中数组写法规整为元组写法，与内置结构一致
        self.config_reads = {
            code: (rel, [tuple(pair) for pair in pairs])
            for code, (rel, pairs) in (config_reads or {}).items()
        }
        self.source = source          # "builtin" 或自定义 JSON 的字符串路径
        self.path = path              # 自定义 JSON 的 Path；内置为 None
        self.rules_by_code: dict[str, dict] = {r["code"]: r for r in rules}

    @property
    def is_custom(self) -> bool:
        """是否项目自定义覆盖注册表（自定义 → detect 必触发）。"""
        return self.path is not None

    def rule_priority(self, rule: dict) -> str:
        return rule_priority(rule)

    def layer_name(self, code: str) -> str:
        return next((n for c, n in self.layers if code.startswith(c)), "未分层")

    def downstream_codes(self, code: str) -> list[str]:
        return sorted(c for c, r in self.rules_by_code.items() if code in r["depends"])

    def resolve_dependencies(self) -> dict[str, list[str]]:
        return {c: self.downstream_codes(c) for c in self.rules_by_code}


def _registry_fail(path: Path, reason: str) -> "RegistryError":
    return RegistryError(f"ETL 注册表损坏：{path} —— {reason}。"
                         f"修复该 JSON 或删除它以回退内置注册表（禁止静默回退）。")


def _validate_registry_json(data, path: Path) -> dict:
    """结构校验：缺必需字段 / 类型非法 / 引用悬空均抛 RegistryError（明确信息）。"""
    if not isinstance(data, dict):
        raise _registry_fail(path, "顶层必须是 JSON 对象")
    for key in _REGISTRY_REQUIRED_KEYS:
        if key not in data:
            raise _registry_fail(path, f"缺少必需字段 \"{key}\"（必需：{list(_REGISTRY_REQUIRED_KEYS)}）")

    layers = data["layers"]
    if not isinstance(layers, list) or not all(
            isinstance(p, (list, tuple)) and len(p) == 2 and all(isinstance(x, str) for x in p)
            for p in layers):
        raise _registry_fail(path, '"layers" 必须是 [[编码, 中文名], ...] 数组')

    rules = data["rules"]
    if not isinstance(rules, list) or not rules:
        raise _registry_fail(path, '"rules" 必须是非空数组')
    codes = set()
    for i, r in enumerate(rules):
        if not isinstance(r, dict):
            raise _registry_fail(path, f'"rules"[{i}] 必须是对象')
        missing = [f for f in _RULE_REQUIRED_FIELDS if f not in r]
        if missing:
            raise _registry_fail(path, f'"rules"[{i}] 缺少必需字段 {missing}')
        if r["code"] in codes:
            raise _registry_fail(path, f'规则编码重复：{r["code"]}')
        codes.add(r["code"])
        if not isinstance(r["src"], list) or not all(isinstance(s, dict) and "file" in s for s in r["src"]):
            raise _registry_fail(path, f'规则 {r["code"]} 的 "src" 必须是含 "file" 键的对象数组')
        for list_field in ("keywords", "config", "depends", "consumers", "history", "tests"):
            if not isinstance(r[list_field], list):
                raise _registry_fail(path, f'规则 {r["code"]} 的 "{list_field}" 必须是数组')
        if not isinstance(r["params"], dict):
            raise _registry_fail(path, f'规则 {r["code"]} 的 "params" 必须是对象')
        for dep in r["depends"]:
            if dep not in codes and not any(x["code"] == dep for x in rules):
                raise _registry_fail(path, f'规则 {r["code"]} 依赖未注册编码：{dep}')

    keyword_index = data["keyword_index"]
    if not isinstance(keyword_index, dict):
        raise _registry_fail(path, '"keyword_index" 必须是对象 {关键词: [编码, ...]}')
    for kw, kw_codes in keyword_index.items():
        if not isinstance(kw_codes, list) or not all(isinstance(c, str) for c in kw_codes):
            raise _registry_fail(path, f'"keyword_index" 关键词 "{kw}" 的值必须是编码字符串数组')
        for c in kw_codes:
            if c not in codes:
                raise _registry_fail(path, f'"keyword_index" 关键词 "{kw}" 索引了未注册编码：{c}')

    contracts = data["config_contracts"]
    if not isinstance(contracts, list) or not all(isinstance(c, dict) for c in contracts):
        raise _registry_fail(path, '"config_contracts" 必须是对象数组（可为空）')
    for i, c in enumerate(contracts):
        if c.get("kind") not in ("config_field", "code_residual") or "rule" not in c:
            raise _registry_fail(path, f'"config_contracts"[{i}] 需含 kind(config_field|code_residual) 与 rule')

    detect_dirs = data["etl_detect_dirs"]
    if not isinstance(detect_dirs, list) or not all(isinstance(d, str) for d in detect_dirs):
        raise _registry_fail(path, '"etl_detect_dirs" 必须是字符串数组（可为空）')

    config_reads = data.get("config_reads", {})
    if not isinstance(config_reads, dict):
        raise _registry_fail(path, '"config_reads" 必须是对象 {编码: [配置文件, [[参数键, 点号路径], ...]]}')
    for code, entry in config_reads.items():
        ok = (isinstance(entry, (list, tuple)) and len(entry) == 2 and isinstance(entry[0], str)
              and isinstance(entry[1], list)
              and all(isinstance(p, (list, tuple)) and len(p) == 2 for p in entry[1]))
        if not ok:
            raise _registry_fail(path, f'"config_reads" 条目 "{code}" 结构非法，应为 ["rel.yaml", [["key", "a.b"]]]')
    return data


# 注册表缓存：{resolved_root: (json_mtime_ns | None, Registry)}；mtime 变化自动重载
_REGISTRY_CACHE: dict[str, tuple] = {}

_BUILTIN_REGISTRY = Registry(
    layers=LAYERS, rules=RULES, keyword_index=KEYWORD_INDEX,
    config_contracts=CONFIG_CONTRACTS, etl_detect_dirs=ETL_DETECT_DIRS,
    config_reads=CONFIG_READS, source="builtin", path=None)


def get_registry(source_root: "str | Path") -> Registry:
    """按 source_root 解析 ETL 注册表：项目 JSON 覆盖优先，否则内置默认。

    - <source_root>/archmap/etl_rule_registry.json 存在 → 加载并校验后完全替代内置；
      损坏抛 RegistryError（带路径与原因），不静默回退。
    - 不存在 → 返回内置注册表（行为与改造前完全一致）。
    """
    root = Path(source_root).resolve()
    json_path = root / REGISTRY_FILENAME
    mtime = json_path.stat().st_mtime_ns if json_path.is_file() else None
    cached = _REGISTRY_CACHE.get(str(root))
    if cached and cached[0] == mtime:
        return cached[1]

    if mtime is None:
        reg = _BUILTIN_REGISTRY
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as e:
            raise _registry_fail(json_path, f"读取失败：{e}") from e
        except json.JSONDecodeError as e:
            raise _registry_fail(json_path, f"JSON 语法错误：第 {e.lineno} 行第 {e.colno} 列：{e.msg}") from e
        data = _validate_registry_json(data, json_path)
        reg = Registry(
            layers=data["layers"], rules=data["rules"], keyword_index=data["keyword_index"],
            config_contracts=data["config_contracts"], etl_detect_dirs=data["etl_detect_dirs"],
            config_reads=data.get("config_reads", {}),
            source=str(json_path), path=json_path)
    _REGISTRY_CACHE[str(root)] = (mtime, reg)
    return reg


def clear_registry_cache() -> None:
    """清空注册表缓存（测试用；正常运行按文件 mtime 自动失效）。"""
    _REGISTRY_CACHE.clear()
