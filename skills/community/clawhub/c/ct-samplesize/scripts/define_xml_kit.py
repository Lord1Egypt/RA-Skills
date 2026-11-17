#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
define_xml_kit.py — Define-XML 2.1 规范生成套件（ct- 系列共享件，BASE.md §16.8）

真源：ct-base/scripts/define_xml_kit.py。叶子技能（ct-sdtm / ct-tlf / …）vendor
字节级副本，由 shared_sync_check（_PY_STRICT）+ publish_inject（SHARED_ASSETS）
双闸门保证一致——叶子侧不得只改本地，改进先回底座再同步。

实现源自 ct-sdtm v1.3.0 的 build_define_xml 规范化重构（对齐官方
define2-1-0.xsl 实际消费的 2.1 结构）：odm:Description 双语标签、def:Origin
子元素（Type 属性）、def:DisplayFormat、ItemRef@Role/@MethodOID、标准
def:ValueListDef / def:WhereClauseDef（RangeCheck@def:ItemOID + CheckValue）、
def:CommentDef、元素顺序对齐 2.1 schema。ODM 命名空间恒为
http://www.cdisc.org/ns/odm/v1.3（"1.3.2" 仅是 ODMVersion 属性值）。

数据属地原则：本套件只含「结构生成」，数据由叶子侧注册提供方（set_providers）：
  - load_domain_ref(dom) -> 域参考 dict（ct-sdtm: references/domains/*.json）
  - load_value_level_rules(dom) -> 值级规则 dict（ct-sdtm: value_level_rules）
  - parse_codelist(text) -> list | None（受控术语串解析）
  - var_core_req(dom, var) -> bool（域内 Required 判定，供 ItemRef@Mandatory）
未注册时走通用回退（无域参考 → 变量名作标签、按命名推断 Origin/格式）。

summary 覆盖（逐域，不依赖提供方即可定制）：
  - structure / class / label / comment / purpose：ItemGroupDef 级
  - codelists / codelist_refs：显式受控术语值集与引用（ref 无值集 → raise）
  - var_meta：{var: (en, zh, role, type) 4 元组 | dict(label, label_zh, role,
    type, origin)}——ItemDef 级标签 / 角色 / 类型 / Origin 覆盖
meta 覆盖（文件级）：originator / study_description / mdv_name / file_oid_prefix。

纯本地、零联网、仅标准库。License：MIT（继承 ct-base）。
"""
import os


# ─── 叶子侧数据提供方（§16.8 数据属地：结构在底座，数据在叶子）────────────
_PROVIDERS = {'load_domain_ref': None, 'load_value_level_rules': None,
              'parse_codelist': None, 'var_core_req': None}


def set_providers(load_domain_ref=None, load_value_level_rules=None,
                  parse_codelist=None, var_core_req=None):
    """注册叶子侧数据提供方；未注册的项走通用回退（见模块 docstring）。"""
    if load_domain_ref is not None:
        _PROVIDERS['load_domain_ref'] = load_domain_ref
    if load_value_level_rules is not None:
        _PROVIDERS['load_value_level_rules'] = load_value_level_rules
    if parse_codelist is not None:
        _PROVIDERS['parse_codelist'] = parse_codelist
    if var_core_req is not None:
        _PROVIDERS['var_core_req'] = var_core_req


def _load_domain_ref(dom):
    """回退：无提供方时返回空参考（调用方按无参考路径优雅降级）。"""
    fn = _PROVIDERS['load_domain_ref']
    return fn(dom) if fn else {}


def _load_value_level_rules(dom):
    """回退：无提供方时无值级规则（不生成 def:ValueListRef）。"""
    fn = _PROVIDERS['load_value_level_rules']
    return fn(dom) if fn else {}


def _parse_codelist(cl):
    """回退：无提供方时不解析受控术语串（不生成 CodeList）。"""
    fn = _PROVIDERS['parse_codelist']
    return fn(cl) if fn else None


def _var_core_req(dom, var):
    """回退：无提供方时无非 Required 判定（Mandatory 仅按 Identifier 恒等判）。"""
    fn = _PROVIDERS['var_core_req']
    return bool(fn(dom, var)) if fn else False


# 与 ct-sdtm sdtm_build.build_suppqual 保持一致的 SUPP 字段集（SUPPQUAL
# ItemGroupDef/ItemDef 生成用；叶子可经 set_providers 之外直接改此常量——
# 改动须先回 ct-base 真源再同步）。
SUPP_FIELDS = ['STUDYID', 'RDOMAIN', 'USUBJID', 'IDVAR', 'IDVARVAL',
               'QNAM', 'QLABEL', 'QVAL', 'QORIG', 'QEVAL']

_ODM_NS = 'http://www.cdisc.org/ns/odm/v1.3'
_DEF_NS = 'http://www.cdisc.org/ns/def/v2.1'

# 高频受控术语解码（英文/中文），未列出的项以 CodedValue 自身作 Decode
_CT_DECODE = {
    'M': ('Male', '男'), 'F': ('Female', '女'), 'U': ('Unknown', '未知'),
    'UNKNOWN': ('Unknown', '未知'), 'NOT REPORTED': ('Not Reported', '未报告'),
    'OTHER': ('Other', '其他'),
    'WHITE': ('White', '白人'),
    'BLACK OR AFRICAN AMERICAN': ('Black or African American', '黑人或非裔美国人'),
    'ASIAN': ('Asian', '亚洲人'),
    'AMERICAN INDIAN OR ALASKA NATIVE': ('American Indian or Alaska Native',
                                         '美洲印第安人或阿拉斯加原住民'),
    'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER': ('Native Hawaiian or Other Pacific Islander',
                                                 '夏威夷原住民或其他太平洋岛民'),
    'HISPANIC OR LATINO': ('Hispanic or Latino', '西班牙裔或拉丁裔'),
    'NOT HISPANIC OR LATINO': ('Not Hispanic or Latino', '非西班牙裔或拉丁裔'),
    'YEARS': ('Years', '岁'), 'MONTHS': ('Months', '月'), 'WEEKS': ('Weeks', '周'),
    'DAYS': ('Days', '天'), 'HOURS': ('Hours', '小时'), 'MINUTES': ('Minutes', '分钟'),
    'SCREENING': ('Screening', '筛选'), 'TREATMENT': ('Treatment', '治疗'),
    'FOLLOW-UP': ('Follow-up', '随访'), 'WASHOUT': ('Washout', '洗脱'),
    'RUN-IN': ('Run-in', '导入'), 'OTHER': ('Other', '其他'),
    'MILD': ('Mild', '轻度'), 'MODERATE': ('Moderate', '中度'),
    'SEVERE': ('Severe', '重度'), 'NA': ('Not Applicable', '不适用'),
    'Y': ('Yes', '是'), 'N': ('No', '否'),
    'DOSE NOT CHANGED': ('Dose Not Changed', '剂量未变'),
    'DOSE REDUCED': ('Dose Reduced', '剂量降低'),
    'DRUG WITHDRAWN': ('Drug Withdrawn', '停药'),
    'NOT APPLICABLE': ('Not Applicable', '不适用'),
    'RELATED': ('Related', '相关'),
    'PROBABLY RELATED': ('Probably Related', '很可能相关'),
    'POSSIBLY RELATED': ('Possibly Related', '可能相关'),
    'UNLIKELY RELATED': ('Unlikely Related', '可能无关'),
    'UNRELATED': ('Unrelated', '无关'), 'MISSING': ('Missing', '缺失'),
    'RECOVERED/RESOLVED': ('Recovered/Resolved', '痊愈/解决'),
    'RECOVERING/RESOLVING': ('Recovering/Resolving', '恢复中/解决中'),
    'NOT RECOVERED/NOT RESOLVED': ('Not Recovered/Not Resolved', '未痊愈/未解决'),
    'FATAL': ('Fatal', '致死'), 'DEATH': ('Death', '死亡'),
    'ORAL': ('Oral', '口服'), 'INTRAVENOUS': ('Intravenous', '静脉'),
    'INTRAMUSCULAR': ('Intramuscular', '肌肉'), 'SUBCUTANEOUS': ('Subcutaneous', '皮下'),
    'TOPICAL': ('Topical', '局部'), 'RECTAL': ('Rectal', '直肠'),
    'INHALATION': ('Inhalation', '吸入'), 'TRANSDERMAL': ('Transdermal', '透皮'),
    'DISPOSITION EVENT': ('Disposition Event', '处置事件'),
    'PROTOCOL MILESTONE': ('Protocol Milestone', '方案里程碑'),
    'OTHER EVENT': ('Other Event', '其他事件'),
    'ONE': ('One', '一'), 'MANY': ('Many', '多'),
    'LOW': ('Low', '低'), 'NORMAL': ('Normal', '正常'), 'HIGH': ('High', '高'),
    'ABNORMAL': ('Abnormal', '异常'),
    'BEFORE': ('Before', '之前'), 'AFTER': ('After', '之后'),
    'COINCIDENT': ('Coincident', '同时'), 'ONGOING': ('Ongoing', '持续'),
    'DURING': ('During', '期间'),
}

# RELREC 无域 JSON，内置最小 metadata（仅用于 Define-XML 变量级描述）
_RELREC_META = {
    'STUDYID': ('Study Identifier', '研究标识符', 'Identifier', 'Char'),
    'RDOMAIN': ('Related Domain', '关联域', 'Identifier', 'Char'),
    'USUBJID': ('Unique Subject Identifier', '受试者唯一标识', 'Identifier', 'Char'),
    'IDVAR': ('Identifying Variable', '识别变量', 'Identifier', 'Char'),
    'IDVARVAL': ('Identifying Variable Value', '识别变量值', 'Identifier', 'Char'),
    'RELTYPE': ('Relationship Type', '关系类型', 'Variable', 'Char'),
    'RELID': ('Relationship Identifier', '关系标识符', 'Variable', 'Char'),
}


# 默认登记的实施指南标准（Define-XML 2.1 def:Standards 段；CORE/P21 的
# Define-XML 检查均要求此段，缺失则官方查看器"研究标准"表空白）。
# skill 基线固定 SDTMIG v3.4；若某域采用 SENDIG/ADaMIG，由调用方经
# build_define_xml(meta={'standards': [...]}) 覆盖。
_DEFAULT_STANDARDS = [
    {'oid': 'STD.CDISC.SDTMIG.3.4', 'name': 'SDTMIG', 'type': 'IG',
     'publishing_set': 'CDISC', 'version': '3.4', 'status': 'Final',
     'date': '2022-09-30'},
]


def _def_datatype(var_name, json_type):
    n = var_name.upper()
    if json_type == 'Num' or n.endswith('STRESN'):
        if n.endswith(('SEQ', 'DY', 'STDY', 'ENDY')):
            return 'integer'
        return 'float'
    if n.endswith(('DTC', 'STDTC', 'ENDTC')):
        return 'datetime'
    if n.endswith(('DATE', 'STDAT', 'ENDAT')):
        return 'date'
    return 'text'


def _def_length(datatype, var_name):
    return {'integer': 8, 'float': 12, 'date': 10, 'datetime': 20,
            'text': 200}.get(datatype, 200)


def _def_origin(var_name, dom=None):
    """推断/读取变量 Origin（用于 Define-XML ItemDef@def:Origin）。

    JSON 变量若提供 'origin' 字段则优先采用；否则按命名/类型推断（v0.7.0）：
      DOMAIN / --DY / --STDY / --ENDY / --STRESN / EPOCH / USUBJID -> Derived
      其余 -> CRF
    """
    if dom:
        try:
            ref = _load_domain_ref(dom)
            v = next((x for x in ref.get('variables', []) if x['name'] == var_name), {})
            if v.get('origin'):
                return v['origin']
        except Exception:
            pass
    n = var_name.upper()
    if n in ('DOMAIN',) or n.endswith(('DY', 'STDY', 'ENDY')) or n.endswith('STRESN') \
            or n == 'EPOCH':
        return 'Derived'
    if n == 'USUBJID':
        return 'Derived'
    return 'CRF'


def _def_format(var_name, json_type=None, dom=None):
    """推断/读取变量 SAS 格式（用于 Define-XML ItemDef@def:Format）。

    JSON 变量若提供 'format' 字段则优先采用；否则按命名/类型推断（v0.7.0）：
      *DTC/*STDTC/*ENDTC         -> E8601DT（ISO 日期时间）
      *DAT/*STDAT/*ENDAT/*DATE   -> E8601DA（ISO 日期）
      *STRESN                    -> best12.（数值结果）
      *SEQ/*DY/*STDY/*ENDY       -> best8.（整数）
      Num 类型（其余）           -> best12.
      Char 类型                  -> ''（无格式，不写属性）
    """
    if dom:
        try:
            ref = _load_domain_ref(dom)
            v = next((x for x in ref.get('variables', []) if x['name'] == var_name), {})
            if v.get('format'):
                return v['format']
        except Exception:
            pass
    n = var_name.upper()
    if n.endswith(('DTC', 'STDTC', 'ENDTC')):
        return 'E8601DT'
    if n.endswith(('DAT', 'STDAT', 'ENDAT', 'DATE')):
        return 'E8601DA'
    if n.endswith('STRESN'):
        return 'best12.'
    if n.endswith(('SEQ', 'DY', 'STDY', 'ENDY')):
        return 'best8.'
    if json_type == 'Num':
        return 'best12.'
    return ''


def _def_class(ref_class):
    if not ref_class:
        return ''
    return ref_class.upper()


def _def_keys(dom, fields):
    """推断 ItemGroup 键变量及顺序（Define-XML 2.1 ItemRef@KeySequence）。

    XSL displayItemGroupKeys（define2-1-0.xsl L2942）据此渲染查看器"键"列；
    不设置则键列全空。通用观察类：USUBJID→1、[DOMAIN→2]、末尾 --SEQ→末位；
    SUPP<DOMAIN>：STUDYID/RDOMAIN/USUBJID/IDVAR/IDVARVAL/QNAM/QVAL 顺序。
    """
    seq = 0
    out = {}
    if dom and dom.startswith('SUPP'):
        for k in ('STUDYID', 'RDOMAIN', 'USUBJID', 'IDVAR', 'IDVARVAL',
                  'QNAM', 'QVAL'):
            if k in fields:
                seq += 1
                out[k] = seq
        return out
    for k in ('USUBJID', 'DOMAIN'):
        if k in fields:
            seq += 1
            out[k] = seq
    tail = next((f for f in fields if f.endswith('SEQ')), None)
    if tail:
        seq += 1
        out[tail] = seq
    return out


def build_define_xml(out_dir, summary, studyid, define_version='2.1', meta=None):
    """生成 Define-XML v2.1 规范结构（ODM v1.3.2 载体）递交文件。

    v1.3.0 元数据结构规范化（对齐官方 define2-1-0.xsl 实际消费的 2.1 结构）：
      - ItemDef / ItemGroupDef 标签走 odm:Description/odm:TranslatedText（双语）；
        官方 XSL 对 def:Label 零消费（1.0 时代词汇，已废除）；
      - def:Origin 改为 ItemDef 子元素（Type 属性，CT：CRF/Derived/...），
        替代 1.0 时代的 def:Origin 属性写法；
      - SAS 显示格式用 def:DisplayFormat 属性（def:Format 非 2.1 词汇）；
      - Role 挂 ItemRef@Role（ItemDef 上不再挂 def:Role）；
      - 派生方法用 ItemRef@MethodOID（ODM 标准属性）+ MethodDef@Type（普通属性），
        不再用 def:MethodOID / def:Type / ItemDef 子元素 MethodRef；
      - 值级元数据：def:ValueListDef / def:WhereClauseDef 独立元素 +
        ValueListDef/ItemRef@def:WhereClauseOID 关联；条件经
        RangeCheck(@def:ItemOID, @Comparator, @SoftHard) + odm:CheckValue 表达；
        （旧版嵌套 WhereClause/Comparison + def:ParentItem 为自造结构，已废除）
      - 注释：def:CommentDef（Description/TranslatedText）+ @def:CommentOID 引用，
        替代 def:Comment 属性；
      - ItemDef 值级引用用 def:ValueListRef（def 命名空间，2.1 词汇）；
      - 元素顺序对齐 2.1 schema：ItemGroupDef*/ItemDef* → CodeList* →
        MethodDef* → def:ValueListDef* → def:WhereClauseDef* → def:CommentDef*。

    内容层次：ItemGroupDef（每个生成域 + SUPP<DOMAIN>）、ItemDef（每个变量，
    双语标签）、CodeList（受控术语值集，双语 Decode）、MethodDef（派生变量
    推导方法）、值级 ValueListDef/WhereClauseDef（LB/VS/AE/DS/EX）。
    """
    import datetime as _dt
    try:
        import xml.etree.ElementTree as ET
        ET.register_namespace('', _ODM_NS)
        ET.register_namespace('def', _DEF_NS)
    except Exception:
        ET = None

    gen_doms = [d for d, s in summary.items() if s.get('out')]
    meta = meta or {}
    _originator = meta.get('originator', 'ct-sdtm sdtm_build.py')
    _study_desc = meta.get('study_description', 'CDISC SDTMIG v3.4 数据集（ct-sdtm 生成）')
    _mdv_name = meta.get('mdv_name', 'SDTMIG v3.4')
    _file_prefix = meta.get('file_oid_prefix', f'ct-sdtm.{studyid}')
    as_of = _dt.date.today().isoformat()

    # def 前缀声明：def 同时用于元素（def:Origin / def:ValueListDef …）与属性
    # （def:Structure / def:CommentOID …）。v1.3.0 起 def 元素真实存在，
    # ElementTree 会在根元素自动输出 xmlns:def（属性前缀随之生效），无需手动声明。
    root = ET.Element(f'{{{_ODM_NS}}}ODM', {
        'ODMVersion': '1.3.2',
        'FileOID': f'{_file_prefix}.define.xml',
        'FileType': 'Snapshot',
        'AsOfDate': as_of,
        'CreationDateTime': _dt.datetime.now().isoformat(timespec='seconds'),
        'Originator': _originator,
    })
    study = ET.SubElement(root, f'{{{_ODM_NS}}}Study', {'OID': f'STUDY.{studyid}'})
    gv = ET.SubElement(study, f'{{{_ODM_NS}}}GlobalVariables')
    ET.SubElement(gv, f'{{{_ODM_NS}}}StudyName').text = studyid
    ET.SubElement(gv, f'{{{_ODM_NS}}}StudyDescription').text = \
        _study_desc
    ET.SubElement(gv, f'{{{_ODM_NS}}}ProtocolName').text = studyid
    mdv = ET.SubElement(study, f'{{{_ODM_NS}}}MetaDataVersion', {
        'OID': f'MDV.{studyid}.1', 'Name': _mdv_name,
        'def:DefineVersion': define_version})

    code_lists = {}    # tuple(values) -> (cl_oid, Element)（共享 CT，detached）
    vl_cls = []        # 值级 CodeList Element（detached，统一挂载）
    methods = {}       # (dom, var) -> m_oid
    comment_defs = {}  # text -> com_oid
    vl_entries = []    # (dom, vl_oid, wc_oid|None, it_oid, order, wvar, wval)

    def _com_oid(text):
        """def:CommentDef 去重登记：返回 CommentOID 或 None。"""
        if not text:
            return None
        oid = comment_defs.get(text)
        if not oid:
            oid = f'COM.{len(comment_defs) + 1}'
            comment_defs[text] = oid
        return oid

    def _description(parent, en, zh):
        """odm:Description/odm:TranslatedText 双语标签（en 必写；zh 异于 en 才写）。"""
        d = ET.SubElement(parent, f'{{{_ODM_NS}}}Description')
        ET.SubElement(d, f'{{{_ODM_NS}}}TranslatedText',
                      {'xml:lang': 'en'}).text = en or ''
        if zh and zh != en:
            ET.SubElement(d, f'{{{_ODM_NS}}}TranslatedText',
                          {'xml:lang': 'zh'}).text = zh

    def _var_meta(dom, var_name):
        _ov = (summary.get(dom) or {}).get('var_meta') or {}
        _o = _ov.get(var_name)
        if _o is not None:
            if isinstance(_o, dict):
                return (_o.get('label') or var_name,
                        _o.get('label_zh') or _o.get('label') or var_name,
                        _o.get('role') or _def_role_guess(var_name),
                        _o.get('type') or 'Char')
            return _o
        if dom == 'RELREC':
            return _RELREC_META.get(var_name, (var_name, var_name, 'Variable', 'Char'))
        try:
            ref = _load_domain_ref(dom)
        except Exception:
            return (var_name, var_name, _def_role_guess(var_name), 'Char')
        v = next((x for x in ref.get('variables', []) if x['name'] == var_name), None)
        if not v:
            return (var_name, var_name, _def_role_guess(var_name), 'Char')
        return (v.get('label', var_name), v.get('labelZh', var_name),
                v.get('role', _def_role_guess(var_name)), v.get('type', 'Char'))

    def _def_role_guess(var_name):
        n = var_name.upper()
        if n in ('STUDYID', 'USUBJID', 'SUBJID', 'DOMAIN', 'RDOMAIN', 'IDVAR',
                 'IDVARVAL', 'RELID', 'RELTYPE', 'SEQ', 'SPSEQ'):
            return 'Identifier'
        if n.endswith(('DTC', 'STDTC', 'ENDTC', 'DATE', 'STDAT', 'ENDAT', 'DY',
                       'STDY', 'ENDY', 'EPOCH')):
            return 'Timing'
        if n.endswith(('TEST', 'TESTCD', 'TERM', 'CAT', 'SCAT', 'DECOD', 'TRT')):
            return 'Topic'
        return 'Variable'

    # ---- def:Standards（2.1 schema：MetaDataVersion 首个子元素；XSL
    #      tableStandards L710 渲染"研究标准"表，缺失则空表）----
    _standards = meta.get('standards') or _DEFAULT_STANDARDS
    if _standards:
        _st_root = ET.SubElement(mdv, f'{{{_DEF_NS}}}Standards')
        for _st in _standards:
            _st_attrs = {
                'OID': _st['oid'], 'Name': _st['name'], 'Type': _st['type'],
                'PublishingSet': _st.get('publishing_set', 'CDISC'),
                'Version': _st['version'], 'Status': _st.get('status', 'Final'),
                'Date': _st.get('date', '2022-09-30'),
            }
            if _st.get('comment'):
                _st_attrs['def:CommentOID'] = _com_oid(_st['comment'])
            _st_root.append(ET.Element(f'{{{_DEF_NS}}}Standard', _st_attrs))

    # ---- ItemGroupDef + ItemDef（ValueListRef/CodeListRef 同步挂 ItemDef）----
    for dom in gen_doms:
        s = summary[dom]
        fields = s['fields']
        ref = {}
        try:
            ref = _load_domain_ref(dom)
        except Exception:
            pass
        ig_oid = f'IG.{dom}'
        ig = ET.SubElement(mdv, f'{{{_ODM_NS}}}ItemGroupDef', {
            'OID': ig_oid, 'Name': dom,
            'Repeating': 'Yes' if any(f.endswith('SEQ') for f in fields) else 'No',
            'IsReferenceData': 'No',
            'SASDatasetName': dom,
            'def:Structure': s.get('structure') or ref.get('structure') or 'One record per subject',
            'def:Class': (s.get('class') or _def_class(ref.get('class', '')) or
                          ('RELATIONSHIP' if dom == 'RELREC' else '')),
            'def:Domain': dom,
        })
        if s.get('purpose'):
            ig.set('Purpose', s['purpose'])
        ig_name_en = s.get('label') or ref.get('name_en') or ref.get('name') or dom
        # 域参考文件无中文域名词（name 为缩写/英短名），Description 只写 en
        _description(ig, ig_name_en, None)
        ig_comment = s.get('comment') or ref.get('description') or ref.get('description_en') or ''
        if ig_comment:
            ig.set('def:CommentOID', _com_oid(ig_comment))

        order = 0
        keys_map = _def_keys(dom, fields)
        for var in fields:
            order += 1
            label_en, label_zh, role, jtype = _var_meta(dom, var)
            dt = _def_datatype(var, jtype)
            ln = _def_length(dt, var)
            _ov = (s.get('var_meta') or {}).get(var) or {}
            origin = ((isinstance(_ov, dict) and _ov.get('origin'))
                      or _def_origin(var, dom))
            it_oid = f'IT.{dom}.{var}'
            desc = ''
            desc_en = ''
            try:
                v = next((x for x in ref.get('variables', []) if x['name'] == var), {})
                desc = v.get('description', '')
                desc_en = v.get('description_en', '')
            except Exception:
                pass
            fmt = _def_format(var, jtype, dom)
            it_attrs = {
                'OID': it_oid, 'Name': var, 'DataType': dt, 'Length': str(ln),
                'SASFieldName': var,
            }
            # 注释仅在有实质信息（变量描述）时挂 def:CommentOID（2.1 结构）
            if desc or desc_en:
                it_attrs['def:CommentOID'] = _com_oid(
                    f'{desc} / {desc_en}' if desc and desc_en else (desc or desc_en))
            if fmt:
                it_attrs['def:DisplayFormat'] = fmt
            it = ET.SubElement(mdv, f'{{{_ODM_NS}}}ItemDef', it_attrs)
            _description(it, label_en, label_zh)
            # def:Origin 子元素（2.1：Type 属性，替代 1.0 def:Origin 属性）
            ET.SubElement(it, f'{{{_DEF_NS}}}Origin', {'Type': origin})
            # ----------------------------------------------------------------
            # 值级元数据（P1-7）：def:ValueListRef + 值级 CodeList（detached）
            # ----------------------------------------------------------------
            vl_rules = _load_value_level_rules(dom).get(var, [])
            if vl_rules:
                for ri, rule in enumerate(vl_rules):
                    wvar = rule.get('where_var', '')
                    wval = str(rule.get('where_val', '*'))
                    clist_vals = _parse_codelist(rule.get('codelist', '')) or []
                    vl_oid = f'VL.{dom}.{var}.{ri + 1}'
                    wc_oid = (f'WC.{dom}.{var}.{ri + 1}'
                              if (wvar and wval != '*') else None)
                    if clist_vals:
                        vl_cl = ET.Element(f'{{{_ODM_NS}}}CodeList', {
                            'OID': f'CL.VL.{dom}.{var}.{ri + 1}',
                            'Name': f'{var}.when.{wvar}.{wval}',
                            'DataType': 'text'})
                        for val in clist_vals:
                            item = ET.SubElement(vl_cl, f'{{{_ODM_NS}}}CodeListItem',
                                                 {'CodedValue': val})
                            de = ET.SubElement(item, f'{{{_ODM_NS}}}Decode')
                            en, zh = _CT_DECODE.get(val, (val, val))
                            ET.SubElement(de, f'{{{_ODM_NS}}}TranslatedText',
                                          {'xml:lang': 'en'}).text = en
                            ET.SubElement(de, f'{{{_ODM_NS}}}TranslatedText',
                                          {'xml:lang': 'zh'}).text = zh
                        vl_cls.append(vl_cl)
                    vl_entries.append((dom, vl_oid, wc_oid, it_oid, ri + 1,
                                       wvar, wval))
                    ET.SubElement(it, f'{{{_DEF_NS}}}ValueListRef',
                                  {'ValueListOID': vl_oid})
            else:
                # 回退：普通 CodeList（条件无关）
                allowed = None
                try:
                    v = next((x for x in ref.get('variables', []) if x['name'] == var), {})
                    allowed = _parse_codelist(v.get('codelist'))
                except Exception:
                    pass
                cl_ref = (s.get('codelist_refs') or {}).get(var)
                if cl_ref and cl_ref not in (s.get('codelists') or {}):
                    raise ValueError(
                        f"CodeListRef '{cl_ref}'（{dom}.{var}）未提供值集："
                        f"须在 summary['{dom}']['codelists'] 给出 values"
                        f"（Define-XML 2.1 禁止空引用/占位值集）")
                if allowed:
                    key = tuple(allowed)
                    hit = code_lists.get(key)
                    if not hit:
                        cl_oid = f'CL.{len(code_lists) + 1}'
                        cl = ET.Element(f'{{{_ODM_NS}}}CodeList', {
                            'OID': cl_oid, 'Name': var, 'DataType': 'text'})
                        for val in allowed:
                            item = ET.SubElement(cl, f'{{{_ODM_NS}}}CodeListItem',
                                                 {'CodedValue': val})
                            de = ET.SubElement(item, f'{{{_ODM_NS}}}Decode')
                            en, zh = _CT_DECODE.get(val, (val, val))
                            ET.SubElement(de, f'{{{_ODM_NS}}}TranslatedText',
                                          {'xml:lang': 'en'}).text = en
                            ET.SubElement(de, f'{{{_ODM_NS}}}TranslatedText',
                                          {'xml:lang': 'zh'}).text = zh
                        code_lists[key] = (cl_oid, cl)
                    else:
                        cl_oid = hit[0]
                    ET.SubElement(it, f'{{{_ODM_NS}}}CodeListRef',
                                  {'CodeListOID': cl_oid})
                elif cl_ref:
                    ET.SubElement(it, f'{{{_ODM_NS}}}CodeListRef',
                                  {'CodeListOID': cl_ref})
            # ItemRef（ItemGroupDef 下）：MethodOID / Role 为 ODM 标准属性
            mand = 'Yes' if (role == 'Identifier' or var in ('STUDYID', 'DOMAIN')
                             or _var_core_req(dom, var)) else 'No'
            iref_attrs = {'ItemOID': it_oid, 'OrderNumber': str(order),
                          'Mandatory': mand,
                          'KeySequence': str(keys_map.get(var, ''))}
            if role:
                iref_attrs['Role'] = role
            if origin == 'Derived':
                m_oid = f'MT.{dom}.{var}'
                methods[(dom, var)] = m_oid
                iref_attrs['MethodOID'] = m_oid
            ET.SubElement(ig, f'{{{_ODM_NS}}}ItemRef', iref_attrs)

        # SUPPQUAL 关联（若本域生成了 SUPP）
        if s.get('suppqual'):
            supp_oid = f'IG.SUPP{dom}'
            sig = ET.SubElement(mdv, f'{{{_ODM_NS}}}ItemGroupDef', {
                'OID': supp_oid, 'Name': f'SUPP{dom}', 'Repeating': 'Yes',
                'IsReferenceData': 'No', 'SASDatasetName': f'SUPP{dom}',
                'def:Structure': 'One record per supplemental qualifier',
                'def:Class': 'SUPPLEMENTARY QUALIFIERS', 'def:Domain': dom})
            _description(sig, f'Supplemental Qualifiers for {dom}',
                         f'{dom} 补充限定词')
            supp_keys = _def_keys(f'SUPP{dom}', SUPP_FIELDS)
            for i, sf in enumerate(SUPP_FIELDS):
                se, sz, sr, sj = _var_meta('SUPP', sf)
                sdt = _def_datatype(sf, sj)
                sit = ET.SubElement(mdv, f'{{{_ODM_NS}}}ItemDef', {
                    'OID': f'IT.SUPP{dom}.{sf}', 'Name': sf, 'DataType': sdt,
                    'Length': str(_def_length(sdt, sf)),
                    'SASFieldName': sf})
                _description(sit, se, sz)
                ET.SubElement(sit, f'{{{_DEF_NS}}}Origin', {'Type': 'CRF'})
                sir = ET.SubElement(sig, f'{{{_ODM_NS}}}ItemRef', {
                    'ItemOID': f'IT.SUPP{dom}.{sf}', 'OrderNumber': str(i + 1),
                    'Mandatory': 'Yes' if sf in ('STUDYID', 'RDOMAIN', 'USUBJID',
                                                 'IDVAR', 'IDVARVAL', 'QNAM', 'QVAL')
                    else 'No',
                    'KeySequence': str(supp_keys.get(sf, ''))})
                if sr:
                    sir.set('Role', sr)

    # ---- CodeList（统一挂载，对齐 schema 顺序：ItemGroupDef/ItemDef 之后）----
    for cl_oid, cl_el in code_lists.values():
        mdv.append(cl_el)
    for cl_el in vl_cls:
        mdv.append(cl_el)

    # ---- 显式提供的 CodeList（叶子侧受控术语值集，如 ADaM CT 引用）----
    for _dom in gen_doms:
        for cl_oid, cl_def in (summary[_dom].get('codelists') or {}).items():
            cl = ET.SubElement(mdv, f'{{{_ODM_NS}}}CodeList', {
                'OID': cl_oid, 'Name': cl_def.get('name', cl_oid),
                'DataType': cl_def.get('data_type', 'text')})
            for val in cl_def.get('values', []):
                code, en, zh = (val if isinstance(val, tuple)
                                else (val, val, val))
                _item = ET.SubElement(cl, f'{{{_ODM_NS}}}CodeListItem',
                                      {'CodedValue': code})
                _de = ET.SubElement(_item, f'{{{_ODM_NS}}}Decode')
                ET.SubElement(_de, f'{{{_ODM_NS}}}TranslatedText',
                              {'xml:lang': 'en'}).text = en
                ET.SubElement(_de, f'{{{_ODM_NS}}}TranslatedText',
                              {'xml:lang': 'zh'}).text = zh

    # ---- MethodDef（派生方法）----
    _method_text = {
        'USUBJID': ('Unique Subject Identifier Derivation',
                    'USUBJID = STUDYID + "-" + SUBJID（受试者唯一标识合成）'),
        'DOMAIN': ('Domain Abbreviation', 'DOMAIN 由映射引擎按域缩写赋值'),
        'EPOCH': ('Epoch Derivation',
                  'EPOCH 由记录日期相对 RFSTDTC/RFENDTC 推导：'
                  '日期<RFSTDTC 为 SCREENING，RFSTDTC≤日期≤RFENDTC 为 TREATMENT，'
                  '日期>RFENDTC 为 FOLLOW-UP'),
    }

    for (dom, var), m_oid in methods.items():
        if var == 'EPOCH':
            name, desc = _method_text['EPOCH']
        elif var == 'USUBJID':
            name, desc = _method_text['USUBJID']
        elif var == 'DOMAIN':
            name, desc = _method_text['DOMAIN']
        elif var.endswith('STRESN'):
            name, desc = ('Numeric Result Derivation',
                          f'{var} 由对应 --ORRES 数值化得到（非数值置空）')
        elif var.endswith(('DY', 'STDY', 'ENDY')):
            name, desc = ('Study Day Derivation',
                          f'{var} = (记录日期 - RFSTDTC) + 1（RFSTDTC 当天为 Study Day 1）')
        else:
            name, desc = ('Derived Variable', f'{var} 由映射引擎推导')
        mt = ET.SubElement(mdv, f'{{{_ODM_NS}}}MethodDef', {
            'OID': m_oid, 'Name': name, 'Type': 'Computation'})
        d = ET.SubElement(mt, f'{{{_ODM_NS}}}Description')
        ET.SubElement(d, f'{{{_ODM_NS}}}TranslatedText',
                      {'xml:lang': 'en'}).text = desc
        ET.SubElement(d, f'{{{_ODM_NS}}}TranslatedText',
                      {'xml:lang': 'zh'}).text = desc

    # ---- def:ValueListDef / def:WhereClauseDef（2.1 独立元素 + OID 关联）----
    for dom, vl_oid, wc_oid, it_oid, vl_order, wvar, wval in vl_entries:
        vld = ET.SubElement(mdv, f'{{{_DEF_NS}}}ValueListDef', {'OID': vl_oid})
        iref_attrs = {'ItemOID': it_oid, 'OrderNumber': str(vl_order),
                      'Mandatory': 'No'}
        if wc_oid:
            iref_attrs['def:WhereClauseOID'] = wc_oid
        ET.SubElement(vld, f'{{{_ODM_NS}}}ItemRef', iref_attrs)
    for dom, vl_oid, wc_oid, _it, _o, wvar, wval in vl_entries:
        if not wc_oid:
            continue
        wc = ET.SubElement(mdv, f'{{{_DEF_NS}}}WhereClauseDef', {'OID': wc_oid})
        rc = ET.SubElement(wc, f'{{{_ODM_NS}}}RangeCheck', {
            'Comparator': 'EQ', 'SoftHard': 'Soft',
            f'{{{_DEF_NS}}}ItemOID': f'IT.{dom}.{wvar}'})
        ET.SubElement(rc, f'{{{_ODM_NS}}}CheckValue').text = wval

    # ---- def:CommentDef（2.1：注释为独立元素 + OID 引用）----
    for text, com_oid in comment_defs.items():
        cd = ET.SubElement(mdv, f'{{{_DEF_NS}}}CommentDef', {'OID': com_oid})
        d = ET.SubElement(cd, f'{{{_ODM_NS}}}Description')
        ET.SubElement(d, f'{{{_ODM_NS}}}TranslatedText').text = text

    path = os.path.join(out_dir, 'define.xml')
    tree = ET.ElementTree(root)
    tree.write(path, encoding='utf-8', xml_declaration=True)

    # ── 生成后自校验（P21 DefineValidator 同构）──
    issues = validate_define_xml(path)

    return path, issues


# ─── 独立 Define-XML 校验通道（P21 DefineValidator 同构）──────────────────────

def validate_define_xml(xml_path):
    """独立 Define-XML 校验通道（对齐 P21 DefineValidator）。

    校验：
    1. 所有 CodeList/ItemGroupDef/ItemDef/MethodDef/ValueListDef/
       WhereClauseDef/CommentDef 的 OID 全局唯一。
    2. def:ValueListRef 指向存在的 ValueListDef。
    3. def:WhereClauseRef 指向存在的 WhereClauseDef。
    4. ItemRef@ItemOID 指向存在的 ItemDef。
    5. ItemRef@MethodOID 指向存在的 MethodDef。

    返回 issue 列表（空列表 = 通过）。每条 issue 为 dict：
    {'rule_id': str, 'severity': str, 'message': str}。
    severity 取值：Reject / Error / Warning。
    """
    import xml.etree.ElementTree as ET
    issues = []
    try:
        tree = ET.parse(xml_path)
    except Exception as e:
        issues.append({
            'rule_id': 'DEFINE.PARSE.001',
            'severity': 'Reject',
            'message': f'XML 解析失败：{e}',
        })
        return issues

    root = tree.getroot()
    # 命名空间映射
    _ns = {'odm': _ODM_NS, 'def': _DEF_NS}

    # 收集所有 OID 索引
    _oid_index = {}  # oid -> (tag_short, element)

    def _short(tag):
        if tag.startswith('{' + _ODM_NS + '}'):
            return 'odm:' + tag.split('}', 1)[1]
        if tag.startswith('{' + _DEF_NS + '}'):
            return 'def:' + tag.split('}', 1)[1]
        return tag

    # ── 遍历所有元素收集 OID ──
    for elem in root.iter():
        oid = elem.get('OID')
        if oid:
            tag_s = _short(elem.tag)
            if oid in _oid_index:
                prev_tag, _ = _oid_index[oid]
                issues.append({
                    'rule_id': 'DEFINE.OID.001',
                    'severity': 'Error',
                    'message': f'OID 重复：{oid}（{tag_s} 与 {prev_tag} 冲突）',
                })
            _oid_index[oid] = (tag_s, elem)

    # ── 1. ItemRef@ItemOID 指向 ItemDef ──
    for elem in root.iter():
        if elem.tag == '{' + _ODM_NS + '}ItemRef':
            item_oid = elem.get('ItemOID')
            if item_oid and item_oid not in _oid_index:
                issues.append({
                    'rule_id': 'DEFINE.LINK.001',
                    'severity': 'Error',
                    'message': f'ItemRef 指向不存在的 ItemDef：ItemOID={item_oid}',
                })
            method_oid = elem.get('MethodOID')
            if method_oid and method_oid not in _oid_index:
                tag, _ = _oid_index.get(method_oid, (None, None))
                if tag != 'odm:MethodDef':
                    issues.append({
                        'rule_id': 'DEFINE.LINK.002',
                        'severity': 'Warning',
                        'message': f'ItemRef@MethodOID 指向不存在的 MethodDef：{method_oid}',
                    })

    # ── 2. def:ValueListRef 指向 ValueListDef ──
    for elem in root.iter():
        if elem.tag == '{' + _DEF_NS + '}ValueListRef':
            vl_oid = elem.get('ValueListOID')
            if vl_oid and vl_oid not in _oid_index:
                issues.append({
                    'rule_id': 'DEFINE.LINK.003',
                    'severity': 'Error',
                    'message': f'ValueListRef 指向不存在的 ValueListDef：{vl_oid}',
                })

    # ── 3. def:WhereClauseRef 指向 WhereClauseDef ──
    for elem in root.iter():
        if elem.tag == '{' + _DEF_NS + '}WhereClauseRef':
            wc_oid = elem.get('WhereClauseOID')
            if wc_oid and wc_oid not in _oid_index:
                issues.append({
                    'rule_id': 'DEFINE.LINK.004',
                    'severity': 'Error',
                    'message': f'WhereClauseRef 指向不存在的 WhereClauseDef：{wc_oid}',
                })

    # ── 4. def:CodeListRef 指向 CodeList ──
    for elem in root.iter():
        if elem.tag == '{' + _ODM_NS + '}CodeListRef':
            cl_oid = elem.get('CodeListOID')
            if cl_oid and cl_oid not in _oid_index:
                issues.append({
                    'rule_id': 'DEFINE.LINK.005',
                    'severity': 'Error',
                    'message': f'CodeListRef 指向不存在的 CodeList：{cl_oid}',
                })

    # ── 5. ItemGroupDef 至少有一个 ItemRef ──
    for elem in root.iter():
        if elem.tag == '{' + _ODM_NS + '}ItemGroupDef':
            refs = elem.findall('odm:ItemRef', _ns)
            if not refs:
                name = elem.get('Name', '(unnamed)')
                issues.append({
                    'rule_id': 'DEFINE.STRUCT.001',
                    'severity': 'Warning',
                    'message': f'ItemGroupDef {name} 无 ItemRef 子元素',
                })

    # ── 6. ItemDef 必有 Name + DataType ──
    for elem in root.iter():
        if elem.tag == '{' + _ODM_NS + '}ItemDef':
            if not elem.get('Name'):
                issues.append({
                    'rule_id': 'DEFINE.ATTR.001',
                    'severity': 'Error',
                    'message': 'ItemDef 缺少 Name 属性',
                })
            if not elem.get('DataType'):
                name = elem.get('Name', '(unnamed)')
                issues.append({
                    'rule_id': 'DEFINE.ATTR.002',
                    'severity': 'Warning',
                    'message': f'ItemDef {name} 缺少 DataType 属性',
                })

    # ── 7. CodeListRef 目标必须为 CodeList 类型 ──
    for elem in root.iter():
        if elem.tag == '{' + _ODM_NS + '}CodeListRef':
            cl_oid = elem.get('CodeListOID')
            if cl_oid and cl_oid in _oid_index:
                tag, _ = _oid_index[cl_oid]
                if tag != 'odm:CodeList':
                    issues.append({
                        'rule_id': 'DEFINE.LINK.006',
                        'severity': 'Warning',
                        'message': f'CodeListRef 指向非 CodeList 元素：{cl_oid}（{tag}）',
                    })

    return issues


