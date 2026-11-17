# -*- coding: utf-8 -*-
# generator_runner.py
#
# 通用工程生成器。由 env.json 的 workspace_dir/template 驱动，
# 扫描 st/ 目录创建全部 POU/GVL/DUT，挂载主程序，保存并编译。
#

# 调用方式：$runScript generate
#
# env.json 相关字段：
#   template        - 模板 .project 路径（必填）
#   workspace_dir   - 项目工作目录（st/、log/ 均在此下）（必填）
#   extra_libraries - 逗号分隔的库名，如 "SysCom, 3.3.2.50 (System)"（可选）
#   task_mounts     - 已迁移到 workspace_dir/task_mounts.json（项目级隔离）
#
# 日志写入：<workspace_dir>/log/generator_runner_log.txt
# （与 run_script.ps1 的 ${scriptBase}_log.txt 规则严格对齐）
import os, codecs, json, time, shutil, hashlib

# ── 路径推算 ──
# 优先从环境变量读取（由 run_script.ps1 注入），无论脚本放在哪个目录都可靠。
# fallback：按 __file__ 层级计算（scripts/tools/ 下上三层到 skill 根）。
_skill_dir = os.environ.get('INOPRO_SKILL_DIR', '').strip()
if not _skill_dir:
    _skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_env_json  = os.path.join(_skill_dir, u'references', u'env.json')

# ── 读取 env.json ──
raw  = open(_env_json, 'rb').read()
if raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
_env = json.loads(raw.decode('utf-8'))

_ws_dir  = _env.get(u'workspace_dir', u'').strip()
_template = _env.get(u'template', u'').strip()
_extra_libs_raw = _env.get(u'extra_libraries', u'').strip()
_extra_libs = [l.strip() for l in _extra_libs_raw.split(u',') if l.strip()] if _extra_libs_raw else []
# task_mounts: read from workspace_dir/task_mounts.json; fallback to first template PROGRAM if absent.
# NOTE: Keep in sync with _load_task_mounts_from_json() in patch_pou.py.

def _load_task_mounts_from_json(ws_dir):
    _tm_path = os.path.join(ws_dir, u'task_mounts.json')
    if not os.path.exists(_tm_path):
        return {}
    try:
        _tm_raw = open(_tm_path, 'rb').read()
        if _tm_raw.startswith(b'\xef\xbb\xbf'):
            _tm_raw = _tm_raw[3:]
        _tm_data = json.loads(_tm_raw.decode('utf-8'))
        if not isinstance(_tm_data, dict):
            return {}
        result = {}
        for task_name, val in _tm_data.items():
            if isinstance(val, dict):
                result[task_name] = {
                    u'pous':     val.get(u'pous', []),
                    u'mode':     val.get(u'mode', u'append'),
                    u'interval': val.get(u'interval', None),
                    u'priority': val.get(u'priority', None),
                    u'create':   bool(val.get(u'create', False)),
                }
            elif isinstance(val, list):
                result[task_name] = {u'pous': val, u'mode': u'append', u'interval': None, u'priority': None, u'create': False}
        return result
    except:
        return {}

_task_mounts = _load_task_mounts_from_json(_ws_dir)

_st_dir  = os.path.join(_ws_dir, u'st')
_log_dir = os.path.join(_ws_dir, u'log')

# ── 日志初始化（路径规则与 run_script.ps1 严格对齐：脚本名_log.txt） ──
_script_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
_log_path    = os.path.join(_log_dir, _script_name + u'_log.txt')

if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)

_log_fh = codecs.open(_log_path, u'w', encoding=u'utf-8')

def log(msg):
    if isinstance(msg, bytes):
        msg = msg.decode(u'utf-8', u'replace')
    elif not isinstance(msg, unicode):
        msg = unicode(msg)
    line = u'[{}] {}'.format(time.strftime(u'%H:%M:%S'), msg)
    _log_fh.write(line + u'\n')
    _log_fh.flush()

def fatal(msg):
    log(u'FATAL: ' + msg)
    log(u'=== done ===')
    system.exit()

# ── 前置检查 ──
log(u'=== generator_runner start ===')
log(u'skill_dir  : ' + _skill_dir)
log(u'workspace  : ' + _ws_dir)
log(u'template   : ' + _template)
log(u'st_dir     : ' + _st_dir)
if _extra_libs:
    log(u'extra_libs : ' + u', '.join(_extra_libs))
if _task_mounts:
    log(u'task_mounts: ' + u', '.join(u'{}({})'.format(k, u','.join(v.get(u'pous', []))) for k, v in _task_mounts.items()))

if not _ws_dir:
    fatal(u'workspace_dir is empty in env.json')
if not _template:
    fatal(u'template is empty in env.json')
if not os.path.exists(_template):
    fatal(u'template not found: ' + _template)
if not os.path.exists(_st_dir):
    fatal(u'st/ dir not found: ' + _st_dir)

# ── 清理 export 残留文件（防止 ObjectNameNotUniqueExceptionEx） ──
_export_artifacts_removed = 0
for _dp, _dns, _fns in os.walk(_st_dir):
    for _fn in _fns:
        _full = os.path.join(_dp, _fn)
        if _fn.startswith(u'PLC_PRG.') and _fn.endswith(u'.st'):
            os.remove(_full)
            log(u'Removed export artifact: ' + _fn)
            _export_artifacts_removed += 1
_tm_path = os.path.join(_ws_dir, u'task_mounts.json')
if os.path.exists(_tm_path):
    os.remove(_tm_path)
    log(u'Removed export artifact: task_mounts.json')
    _export_artifacts_removed += 1
_committed_path = os.path.join(_st_dir, u'.committed.json')
if os.path.exists(_committed_path):
    os.remove(_committed_path)
    log(u'Removed .committed.json')
    _export_artifacts_removed += 1
if _export_artifacts_removed > 0:
    log(u'Cleaned {} export artifact(s)'.format(_export_artifacts_removed))

# ── 推算项目名和目标 .project 路径 ──
_project_name = os.path.basename(_ws_dir.rstrip(u'/\\'))
_new_project  = os.path.join(_ws_dir, _project_name + u'.project')
log(u'project    : ' + _new_project)

# ── 复制模板（先删旧文件避免只读属性冲突） ──
if os.path.exists(_new_project):
    os.remove(_new_project)
shutil.copy(_template, _new_project)
log(u'Copied template -> ' + _new_project)

# ── 打开工程，置询等待加载（最长 30s） ──
proj = projects.open(_new_project)
_w = 0
while _w < 30:
    time.sleep(1); _w += 1
    try:
        _ch = proj.get_children()
        if _ch and len(list(_ch)) > 0:
            break
    except:
        pass
log(u'Project loaded ({}s).'.format(_w))

# ── 查找 IEC 容器 ──
# 两遍搜索：优先找名为 Application 的容器（AM600/H5U 模板），
# 找不到再 fallback 到任意 ScriptIecLanguageObjectContainerObject（AM522/TT）。
def find_iec_container(proj):
    def _find_app(node, depth):
        if depth > 6: return None
        try: children = node.get_children()
        except: return None
        for c in children:
            try:
                if c.get_name() == u'Application' and \
                   u'ScriptIecLanguageObjectContainerObject' in unicode(c):
                    return c
            except: pass
        for c in children:
            r = _find_app(c, depth + 1)
            if r: return r
        return None
    def _find_any(node, depth):
        if depth > 6: return None
        try: children = node.get_children()
        except: return None
        for c in children:
            if u'ScriptIecLanguageObjectContainerObject' in unicode(c): return c
        for c in children:
            r = _find_any(c, depth + 1)
            if r: return r
        return None
    result = _find_app(proj, 0)
    if result: return result
    return _find_any(proj, 0)

iec = find_iec_container(proj)
if not iec:
    fatal(u'IEC container not found in project tree')
log(u'IEC container: ' + unicode(iec.get_name()))

# ── 文件夹工具 ──
def _find_child_group(parent, name):
    try: children = parent.get_children()
    except: return None
    for child in (children or []):
        try: n = child.get_name()
        except: continue
        if n == name:
            has_d = getattr(child, u'textual_declaration',    None) is not None
            has_i = getattr(child, u'textual_implementation', None) is not None
            if not has_d and not has_i:
                return child
    return None

def find_or_create_group_path(root, path_list):
    node = root
    for part in path_list:
        child = _find_child_group(node, part)
        if child is None:
            node.create_folder(part)
            child = _find_child_group(node, part)
            if child is None:
                log(u'[WARN] could not create folder: ' + part)
                return node  # fallback: use current level
        node = child
    return node

# ── 从单文件 .st 内容第一行读取 ST 关键字判断 IEC 对象类型 ──
def _plain_kind_from_content(content, pou_name):
    """从已读取的 .st 文本返回 'pou'/'gvl'/'dut_struct'/'dut_enum'，失败时按前缀 fallback。
    单文件 POU 格式：文件第一个非注释行为 FUNCTION_BLOCK/PROGRAM/FUNCTION 关键字，
    声明区和实现区写在同一文件中，结尾为 END_FUNCTION_BLOCK/END_PROGRAM/END_FUNCTION。
    """
    try:
        for raw_line in content.splitlines():
            line = raw_line.strip().upper()
            if not line or line.startswith(u'//') or line.startswith(u'(*'):
                continue
            if line.startswith(u'FUNCTION_BLOCK ') or line == u'FUNCTION_BLOCK':
                return u'pou'
            if line.startswith(u'PROGRAM ') or line == u'PROGRAM':
                return u'pou'
            if line.startswith(u'FUNCTION ') and not line.startswith(u'FUNCTION_BLOCK'):
                return u'pou'
            if line.startswith(u'VAR_GLOBAL'):
                return u'gvl'
            if line.startswith(u'TYPE '):
                rest = line[5:].strip()
                colon_idx = rest.find(u':')
                if colon_idx >= 0:
                    after_colon = rest[colon_idx + 1:].strip()
                    if after_colon.startswith(u'STRUCT'):
                        return u'dut_struct'
                    if after_colon.startswith(u'(') or after_colon.startswith(u'ENUM'):
                        return u'dut_enum'
                continue
            if line.startswith(u'STRUCT'):
                return u'dut_struct'
            if line.startswith(u'('):
                return u'dut_enum'
            break
    except:
        pass
    if pou_name.startswith(u'P_') or pou_name.startswith(u'PRG'):
        return u'pou'
    if pou_name.startswith(u'FC_') or pou_name.startswith(u'FB_'):
        return u'pou'
    if pou_name.startswith(u'DUT_'):
        return u'dut_struct'
    if pou_name.startswith(u'ENUM_'):
        return u'dut_enum'
    return u'gvl'

def _split_pou_single_file(content, pou_name):
    """将单文件 POU 内容拆分为 (pou_type, decl_text, impl_text)。
    CODESYS 声明区 = FUNCTION_BLOCK/PROGRAM/FUNCTION 行 + 所有 VAR...END_VAR 块。
    实现区 = 声明区之后到 END_FUNCTION_BLOCK/END_PROGRAM/END_FUNCTION 之前的代码。
    返回 PouType 由文件第一行关键字决定，fallback 按文件名前缀。
    """
    lines = content.splitlines()
    header_idx = -1
    end_keyword = u''
    pou_type = None
    for i, raw_line in enumerate(lines):
        stripped = raw_line.strip().upper()
        if not stripped or stripped.startswith(u'//') or stripped.startswith(u'(*'):
            continue
        if stripped.startswith(u'FUNCTION_BLOCK'):
            header_idx = i; end_keyword = u'END_FUNCTION_BLOCK'; pou_type = PouType.FunctionBlock; break
        if stripped.startswith(u'PROGRAM'):
            header_idx = i; end_keyword = u'END_PROGRAM'; pou_type = PouType.Program; break
        if stripped.startswith(u'FUNCTION') and not stripped.startswith(u'FUNCTION_BLOCK'):
            header_idx = i; end_keyword = u'END_FUNCTION'; pou_type = PouType.Function; break
        break  # 第一个非注释行不是 POU 关键字，无法解析

    if pou_type is None:
        # fallback：按文件名前缀
        if pou_name.startswith(u'P_') or pou_name.startswith(u'PRG'):
            pou_type = PouType.Program
        elif pou_name.startswith(u'FC_'):
            pou_type = PouType.Function
        else:
            pou_type = PouType.FunctionBlock

    if header_idx < 0 or not end_keyword:
        log(u'[WARN] _split_pou_single_file: cannot parse structure of {}, using full content as decl'.format(pou_name))
        return pou_type, content, u''

    end_idx = -1
    for i in range(len(lines) - 1, header_idx, -1):
        if lines[i].strip().upper() == end_keyword:
            end_idx = i; break

    if end_idx < 0:
        log(u'[WARN] _split_pou_single_file: {} not found in {}, using full content as decl'.format(end_keyword, pou_name))
        return pou_type, content, u''

    # 找到最后一个 END_VAR 行的位置（声明区结束处）
    last_end_var_idx = -1
    in_var_block = False
    for i in range(header_idx, end_idx):
        stripped = lines[i].strip().upper()
        if stripped.startswith(u'VAR') and not stripped.startswith(u'VAR_') or \
           stripped.startswith(u'VAR_INPUT') or stripped.startswith(u'VAR_OUTPUT') or \
           stripped.startswith(u'VAR_IN_OUT') or stripped.startswith(u'VAR_GLOBAL') or \
           stripped.startswith(u'VAR_EXTERNAL') or stripped.startswith(u'VAR_TEMP') or \
           stripped.startswith(u'VAR_STAT') or stripped.startswith(u'VAR_ACCESS'):
            in_var_block = True
        if stripped == u'END_VAR' and in_var_block:
            last_end_var_idx = i
            in_var_block = False

    if last_end_var_idx < 0:
        # 没有 VAR 块（如无变量的 PROGRAM），声明区仅含头行
        decl_lines = lines[header_idx:header_idx + 1]
        impl_lines = lines[header_idx + 1:end_idx]
    else:
        decl_lines = lines[header_idx:last_end_var_idx + 1]
        impl_lines = lines[last_end_var_idx + 1:end_idx]

    # 去除实现区首尾空行
    decl_text = u'\n'.join(decl_lines)
    impl_text  = u'\n'.join(impl_lines).strip()
    return pou_type, decl_text, impl_text

# ── DUT enum → GVL INT constants converter ──
def _enum_to_gvl_constants(dut_text, dut_name):
    """Parse a DUT enum (TYPE X : (...); END_TYPE) and convert to GVL VAR_GLOBAL with INT constants.
    Example input:  TYPE E_State : (IDLE:=0, RUN:=1, STOP:=2); END_TYPE
    Example output: VAR_GLOBAL\n    E_State_IDLE : INT := 0;\n    E_State_RUN  : INT := 1;\n    ...END_VAR
    """
    import re as _re
    entries = []
    _m = _re.search(u'\(([^)]+)\)', dut_text, _re.DOTALL)
    if _m:
        body = _m.group(1)
        for item in body.split(u','):
            item = item.strip()
            if not item:
                continue
            if u':=' in item:
                parts = item.split(u':=')
                ename = parts[0].strip()
                eval_ = parts[1].strip().rstrip(u',')
            else:
                ename = item.strip()
                eval_ = u''
            entries.append((ename, eval_))
    if not entries:
        log(u'[WARN] _enum_to_gvl_constants: no entries parsed from "{}", using empty GVL'.format(dut_name))
        return u'VAR_GLOBAL\nEND_VAR'
    auto_val = 0
    lines = [u'VAR_GLOBAL']
    for ename, eval_ in entries:
        if eval_:
            try:
                auto_val = int(eval_)
            except:
                pass
        else:
            eval_ = unicode(auto_val)
        lines.append(u'    {}_{} : INT := {};'.format(dut_name, ename, eval_))
        auto_val += 1
    lines.append(u'END_VAR')
    return u'\n'.join(lines)

# ── Safe text document write helper ──
def _write_td(td, text):
    """Safe full replacement of ScriptTextDocument content with verify+retry.
    Primary: td.replace(text) — single-arg whole-doc replace (API confirmed in 3.5.10+).
    After write, verify td.text matches input. If not, retry with fallback methods.
    Fallback 1: append + remove prefix.
    Fallback 2: loop remove + insert.
    """
    for _attempt in range(3):
        if _attempt == 0:
            try:
                td.replace(text)
            except:
                continue
        elif _attempt == 1:
            try:
                default_len = td.length
                td.append(text)
                if default_len > 0:
                    td.remove(0, default_len)
            except:
                continue
        else:
            try:
                while td.length > 0:
                    td.remove(0, td.length)
                td.insert(0, text)
            except:
                break
        try:
            actual = td.text
            if actual is not None and actual.strip() == text.strip():
                return
            log(u'[WARN] _write_td verify mismatch (attempt {}), td.length={} expected={}'.format(_attempt + 1, len(actual) if actual else -1, len(text)))
        except:
            pass
    log(u'[WARN] _write_td all attempts exhausted for text length={}'.format(len(text)))

# ── 通用扫描 st/ 目录，创建所有 POU / GVL / DUT / Action ──
# 单文件 .st 类型识别规则（统一格式）：
#   读第一个非注释行关键字：
#   FUNCTION_BLOCK/PROGRAM/FUNCTION → POU（单文件格式，声明区+实现区在同一文件）
#   VAR_GLOBAL → GVL
#   TYPE…STRUCT → DUT Structure
#   TYPE…( 或 ENUM → DUT Enumeration
#   fallback：文件名前缀 P_/PRG/FB_/FC_→POU，DUT_→Structure，ENUM_→Enumeration，其余→GVL
# Action 识别规则（.act.st 文件）：
#   必须放在父 POU 同名子目录下，例如：
#   st/程序/P_Main/ACT_Init.act.st  -> 父 POU = P_Main，Action 名 = ACT_Init
#   与 export_pou.py 导出目录结构严格对应
created_pous = []   # 记录所有新建节点名，用于后续挂载去重
act_queue    = []   # [(act_name, abs_path, parent_pou_name), ...]  第二遍处理
for dirpath, dirnames, filenames in os.walk(_st_dir):
    dirnames.sort()
    filenames.sort()

    rel = os.path.relpath(dirpath, _st_dir)
    path_list = [] if rel == u'.' else rel.replace(u'/', os.sep).split(os.sep)

    single_map = []   # [fname, ...]

    for fname in filenames:
        if fname.endswith(u'.act.st'):
            # .act.st 所在目录名即为父 POU 名
            if path_list:
                parent_pou_name = path_list[-1]
                act_name = fname[:-len(u'.act.st')]
                act_queue.append((act_name, os.path.join(dirpath, fname), parent_pou_name))
            else:
                log(u'[WARN] .act.st at st/ root has no parent POU dir, skip: ' + fname)
        elif fname.endswith(u'.st'):
            single_map.append(fname)

    if not single_map:
        continue

    grp = find_or_create_group_path(iec, path_list) if path_list else iec

    # GVL / DUT / 单文件 POU── 读文件内容第一行关键字判断类型，前缀做 fallback
    for fname in single_map:
        name = fname[:-len(u'.st')]
        plain_abs = os.path.join(dirpath, fname)
        raw_content = codecs.open(plain_abs, u'r', u'utf-8').read()
        kind = _plain_kind_from_content(raw_content, name)

        # When a POU has actions it lives in a same-name subdirectory:
        #   st/程序/P_Main/P_Main.st
        # path_list ends with the POU name as an extra directory layer.
        # For POU nodes, strip that last element so grp points to the
        # correct CODESYS folder (e.g. ['程序']), not a non-existent nested
        # folder. GVL/DUT placed inside a same-name dir is unusual but handled
        # the same way for consistency.
        effective_path_list = path_list
        if path_list and path_list[-1] == name:
            effective_path_list = path_list[:-1]
            grp_for_node = find_or_create_group_path(iec, effective_path_list) if effective_path_list else iec
        else:
            grp_for_node = grp
        if kind == u'pou':
            # 单文件 POU 格式：解析拆分声明区和实现区，类型由内容第一行关键字决定
            pou_type, decl_text, impl_text = _split_pou_single_file(raw_content, name)
            node = grp_for_node.create_pou(name, pou_type)
            _write_td(node.textual_declaration, decl_text)
            if impl_text:
                _write_td(node.textual_implementation, impl_text)
            created_pous.append(name)
            _type_label = {PouType.Program: u'Program', PouType.Function: u'Function'}.get(pou_type, u'FunctionBlock')
            log(u'Created POU(single-file): {} [{}]'.format(name, _type_label))
        elif kind == u'dut_struct':
            node = grp_for_node.create_dut(name, DutType.Structure)
            _write_td(node.textual_declaration, raw_content)
            created_pous.append(name)
            log(u'Created GVL/DUT: {} [{}]'.format(name, kind))
        elif kind == u'dut_enum':
            log(u'[WARN] DUT Enumeration "{}" has known write bug in InoProShop V1.9. Auto-downgrading to GVL with INT constants.'.format(name))
            node = grp_for_node.create_gvl(name)
            text = _enum_to_gvl_constants(raw_content, name)
            _write_td(node.textual_declaration, text)
            created_pous.append(name)
            log(u'Created GVL/DUT: {} [gvl(enum->gvl)]'.format(name))
        else:
            node = grp_for_node.create_gvl(name)
            _write_td(node.textual_declaration, raw_content)
            created_pous.append(name)
            log(u'Created GVL/DUT: {} [{}]'.format(name, kind))

log(u'All POU/GVL/DUT nodes created ({}): {}'.format(len(created_pous), u', '.join(created_pous)))

# ── 第二遍：创建 Action 节点（依赖父 POU 已存在） ──
# find_pou: 在整个工程树中按名称查找已创建的 POU 节点
def find_pou_in_tree(root, name, depth=0):
    if depth > 8: return None
    try: children = root.get_children()
    except: return None
    for c in (list(children) if children else []):
        try:
            cname = c.get_name()
            if cname == name:
                has_d = getattr(c, u'textual_declaration',    None) is not None
                has_i = getattr(c, u'textual_implementation', None) is not None
                if has_d or has_i:
                    return c
        except: pass
        result = find_pou_in_tree(c, name, depth + 1)
        if result: return result
    return None

if act_queue:
    log(u'Creating {} Action node(s)...'.format(len(act_queue)))
    for act_name, act_abs_path, parent_pou_name in act_queue:
        parent_node = find_pou_in_tree(iec, parent_pou_name)
        if parent_node is None:
            log(u'[WARN] parent POU "{}" not found, skip Action: {}'.format(parent_pou_name, act_name))
            continue
        try:
            act_node = parent_node.create_action(act_name)
            impl_text = codecs.open(act_abs_path, u'r', u'utf-8').read()
            _write_td(act_node.textual_implementation, impl_text)
            log(u'Created Action: {}.{}'.format(parent_pou_name, act_name))
        except Exception as ex:
            log(u'[WARN] create_action failed for {}.{}: {}'.format(parent_pou_name, act_name, unicode(ex)))
else:
    log(u'No Action nodes to create')

# ── 添加额外库引用（由 env.json 的 extra_libraries 字段驱动） ──
if _extra_libs:
    def find_libman(proj):
        result = [None]
        def _s(node, d):
            if d > 6 or result[0]: return
            try: ch = node.get_children()
            except: return
            for c in (ch or []):
                if u'ScriptLibManObject' in unicode(c):
                    result[0] = c; return
                _s(c, d + 1)
        _s(proj, 0)
        return result[0]

    libman = find_libman(proj)
    if libman:
        try:
            existing = [unicode(lib) for lib in (libman.get_libraries() or [])]
        except:
            existing = []
        for lib_name in _extra_libs:
            already = any(lib_name.split(u',')[0].strip() in e for e in existing)
            if not already:
                try:
                    libman.references.add_library(lib_name)
                    log(u'Added library: ' + lib_name)
                except Exception as ex:
                    log(u'[WARN] add_library failed for "' + lib_name + u'": ' + unicode(ex))
            else:
                log(u'Library already present, skip: ' + lib_name)
    else:
        log(u'[WARN] LibMan node not found, libraries not added: ' + u', '.join(_extra_libs))

# ── 挂载所有新建 Program 到 Task ──
# 策略 A（task_mounts 已配置）：通过官方 pous API 全量替换 Task 的程序调用列表
# 策略 B（task_mounts 未配置，兜底行为）：全部追加到第一个模板 PROGRAM 的实现区
new_names = set(created_pous)
prg_names = [n for n in created_pous if n.startswith(u'P_') or n.startswith(u'PRG')]

def _find_task_config(node, depth=0):
    """递归查找 Task Configuration 节点（ScriptTaskConfigObject）。"""
    if depth > 6: return None
    try: children = node.get_children()
    except: return None
    for c in (list(children) if children else []):
        try:
            if u'ScriptTaskConfigObject' in unicode(c):
                return c
        except: pass
        result = _find_task_config(c, depth + 1)
        if result: return result
    return None

def _find_task_node(task_config, task_name):
    """在 Task Configuration 下查找指定名称的 Task 节点（ScriptTaskObject）。"""
    try: children = task_config.get_children()
    except: return None
    for c in (list(children) if children else []):
        try:
            if c.get_name() == task_name and u'ScriptTaskObject' in unicode(c):
                return c
        except: pass
    return None

def _find_shell_program(node, depth=0):
    """在 Application 下查找模板自带的壳 PROGRAM（排除本次新建的）。
    用于 _pous_mount 清除孤立壳节点，以及策略 B 兜底挂载。
    """
    if depth > 8: return None
    try: children = node.get_children()
    except: return None
    for c in (list(children) if children else []):
        try:
            cname = c.get_name()
            if cname in new_names:
                continue
            td = getattr(c, u'textual_declaration',    None)
            ti = getattr(c, u'textual_implementation', None)
            if td is not None and ti is not None:
                if u'PROGRAM' in td.text.upper():
                    return c
        except: pass
        result = _find_shell_program(c, depth + 1)
        if result: return result
    return None

def _set_task_properties(task_node, task_name, interval):
    """设置 Task 的 interval 属性。
    注意：priority 不在此处设置，task.priority 是受约束字段，
    写入任意字符串会破坏 Task 配置，导致 UI 打开时报 "value cannot be null"。
    优先级请在 InoProShop UI 中手动设置。
    """
    if interval is not None:
        try:
            task_node.interval = unicode(interval)
            log(u'pous_mount: Task "{}" interval set to {}'.format(task_name, interval))
        except Exception as ex:
            log(u'[WARN] set interval failed for "{}": {}'.format(task_name, unicode(ex)))

def _pous_mount(task_name, task_cfg, prg_list):
    """
    通过 ScriptTaskObject.pous 全量替换 Task 的程序调用列表（generate 行为）。
      1. 若 create=true 且 Task 不存在，调用 task_cfg.create_task(name) 创建新 Task
      2. 若 interval 有值且 Task 是本次新建的，设置 interval
      3. 获取 pous，remove 多余旧条目 + add 缺失新条目
      4. 从 Application 删掉模板壳 PROGRAM（避免孤立节点）
    返回 True 表示成功，False 表示失败（降级到策略 B）。
    """
    if not prg_list:
        log(u'[WARN] _pous_mount called with empty prg_list for task: ' + task_name)
        return False

    task_cfg_node = _find_task_config(proj)
    if task_cfg_node is None:
        log(u'[WARN] Task Configuration not found; falling back for task: ' + task_name)
        return False

    task_node = _find_task_node(task_cfg_node, task_name)
    should_create = task_cfg.get(u'create', False)

    if task_node is None:
        if should_create:
            log(u'Task "{}" not found, creating (create=true)...'.format(task_name))
            try:
                task_cfg_node.create_task(task_name)
                log(u'Task "{}" created OK'.format(task_name))
                task_node = _find_task_node(task_cfg_node, task_name)
                if task_node is None:
                    log(u'[WARN] Task "{}" created but node not found; skipping'.format(task_name))
                    return False
            except Exception as ex:
                log(u'[WARN] create_task("{}") failed: {}; skipping'.format(task_name, unicode(ex)))
                return False
        else:
            log(u'[WARN] Task "{}" not found and create=false; skipping'.format(task_name))
            return False

    # 设置 interval — 仅对本次新建的 Task 有效（should_create=True）；
    # 已存在于模板中的 Task 不触碰任何属性：模板已配好 interval/priority/watchdog 等，
    # 脚本写入反而可能损坏内部状态（UI 双击报 "value cannot be null"）。
    if should_create:
        _set_task_properties(task_node, task_name, task_cfg.get(u'interval', None))

    try:
        pous = task_node.pous
    except Exception as ex:
        log(u'[WARN] task.pous not available ({}); falling back'.format(unicode(ex)))
        return False

    # 全量替换 pous：只用 add/remove(name)，不用 replace(index)/remove(index)
    # 外来工程 Task pous 内部索引与 Python list index 不对应，按 index 操作会抛异常
    try:
        existing_names = [unicode(x).strip() for x in list(pous)]
        new_set   = set(prg_list)
        exist_set = set(existing_names)
        for old_name in existing_names:
            if old_name not in new_set:
                try:
                    pous.remove(old_name)
                    log(u'pous_mount: remove "{}" from Task "{}"'.format(old_name, task_name))
                except Exception as ex2:
                    log(u'[WARN] pous.remove("{}") failed: {}'.format(old_name, unicode(ex2)))
        for new_name in prg_list:
            if new_name not in exist_set:
                try:
                    pous.add(new_name)
                    log(u'pous_mount: add "{}" to Task "{}"'.format(new_name, task_name))
                except Exception as ex2:
                    log(u'[WARN] pous.add("{}") failed: {}'.format(new_name, unicode(ex2)))
        log(u'pous_mount: Task "{}" pous updated -> [{}]'.format(task_name, u', '.join(prg_list)))
    except Exception as ex:
        log(u'[WARN] pous update failed: ' + unicode(ex))

    # 删除 Application 里的模板壳 PROGRAM（避免孤立节点）
    shell_node = _find_shell_program(iec)
    if shell_node is not None:
        shell_name = u'<unknown>'
        try: shell_name = shell_node.get_name()
        except: pass
        try:
            shell_node.remove()
            log(u'pous_mount: removed shell PROGRAM "{}"'.format(shell_name))
        except Exception as ex:
            log(u'[WARN] remove shell PROGRAM failed (non-fatal): ' + unicode(ex))

    # 立即 save() 将 pous 变更持久化到磁盘
    # save_as() 在某些 CODESYS 版本中会从内存重建 XML，pous 修改可能丢失；
    # 先 save() 将 Task 引用写入文件，再 save_as() 到目标路径，双重保险。
    try:
        proj.save()
        log(u'pous_mount: intermediate save() OK (pous changes flushed)')
    except Exception as ex:
        log(u'[WARN] pous_mount: intermediate save() failed (non-fatal): ' + unicode(ex))

    return True

def _mount_programs_by_call(target_node, prg_list):
    """向 target_node 的实现区追加 prg_list 中所有 Program 的调用行（透传声明方式，兜底用）。"""
    ti = target_node.textual_implementation
    current = ti.text if ti.length > 0 else u''
    for prg_name in prg_list:
        call_line = prg_name + u'();\n'
        if prg_name + u'()' not in current:
            ti.insert(ti.length, call_line)
            current += call_line
            log(u'Mounted {}() -> {}'.format(prg_name, target_node.get_name()))
        else:
            log(u'{}() already mounted, skip'.format(prg_name))

if not prg_names:
    log(u'No P_/PRG programs to mount')
else:
    # 策略 B（默认）：在模板已有的挂载 Program 实现区末尾追加调用。
    # pous API（策略 A）在此版本 InoProShop 中无法持久化 remove 操作，
    # 因此新建工程统一采用追加方式——模板自带的 Program 已挂载到 MainTask，
    # 在其实现区追加 P_XXX() 即可被 Task 扫描到，无需修改 Task 配置。
    #
    # task_mounts.json 中 create=true 的条目仍会创建新 Task（不挂载 pous），
    # 供用户后续在 UI 中手动配置，或由 patch 流程处理。
    existing_main = _find_shell_program(proj)
    if existing_main:
        log(u'Mounting all Programs to template PROGRAM "{}": {}'.format(
            existing_main.get_name(), u', '.join(prg_names)))
        _mount_programs_by_call(existing_main, prg_names)
    else:
        log(u'[WARN] no template PROGRAM found, please mount manually: ' + u', '.join(prg_names))

    # 处理 task_mounts 中 create=true 的条目（仅创建空 Task，不挂载 pous）
    if _task_mounts:
        _tc = _find_task_config(proj)
        for task_name, task_cfg in _task_mounts.items():
            if task_cfg.get(u'create', False) and _tc is not None:
                if _find_task_node(_tc, task_name) is None:
                    try:
                        _tc.create_task(task_name)
                        log(u'[INFO] created new Task "{}" (create=true)'.format(task_name))
                    except Exception as _ex_ct:
                        log(u'[WARN] create_task("{}") failed: {}'.format(task_name, unicode(_ex_ct)))

# ── 保存 ──
log(u'Saving...')
try:
    proj.save_as(_new_project)
    log(u'Saved: ' + _new_project)
except Exception as e:
    log(u'[WARN] save_as failed: ' + unicode(e) + u', trying save()')
    try:
        proj.save()
        log(u'Saved (fallback save())')
    except Exception as e2:
        fatal(u'save failed: ' + unicode(e2))

# ── committed snapshot（供首次 patch 建立 diff 基准） ──
# NOTE: _build_current_hashes/_save_committed mirror the same functions in patch_pou.py.
def _build_current_hashes(st_dir):
    """Return dict: rel_path -> md5 for every .st file under st_dir."""
    result = {}
    for dp, dns, fns in os.walk(st_dir):
        for fn in fns:
            if fn.endswith('.st') and not fn.startswith('.'):
                ap = os.path.join(dp, fn)
                rp = os.path.relpath(ap, st_dir).replace(os.sep, '/')
                try:
                    result[rp] = hashlib.md5(open(ap, 'rb').read()).hexdigest()
                except: pass
    return result

def _save_committed(st_dir, committed_dict):
    """Write .committed.json — call after every successful save()."""
    sp = os.path.join(st_dir, u'.committed.json')
    keys = sorted(committed_dict.keys())
    sb = u'{\n'
    for i, k in enumerate(keys):
        comma = u',' if i < len(keys) - 1 else u''
        sb += u'  "{}": "{}"{}\n'.format(k, committed_dict[k], comma)
    sb += u'}'
    try:
        f = codecs.open(sp, 'w', 'utf-8')
        f.write(sb)
        f.close()
        log(u'committed snapshot written ({} files)'.format(len(keys)))
    except Exception as e:
        log(u'[WARN] could not write .committed.json: ' + unicode(e))

if os.path.exists(_st_dir):
    _save_committed(_st_dir, _build_current_hashes(_st_dir))

time.sleep(3)

# ── 编译 ──
def do_build(timeout=90):
    """触发编译，轮询等待完成，解析并记录错误/警告数。"""
    import re as _re
    build_cmd = None
    for cmd in system.commands:
        tl = list(cmd.tokens or [])
        if u'project' in tl and u'buildactiveapp' in tl:
            build_cmd = cmd; break
    if build_cmd is None:
        fatal(u'buildactiveapp command not found, compile not executed')

    for _c in (system.get_message_categories() or []):
        try:
            _desc = system.get_message_category_description(_c)
            if u'\u7f16\u8bd1' in _desc or u'build' in _desc.lower() or u'compil' in _desc.lower():
                system.clear_messages(_c); break
        except: pass

    build_cmd.execute()
    log(u'Build command issued, waiting (max {}s)...'.format(timeout))

    _done = False; _waited = 0
    while _waited < timeout:
        time.sleep(1); _waited += 1
        try:
            for _c in (system.get_message_categories() or []):
                try: _desc = system.get_message_category_description(_c)
                except: _desc = u''
                if u'\u7f16\u8bd1' in _desc or u'build' in _desc.lower() or u'compil' in _desc.lower():
                    for _m in (system.get_message_objects(_c) or []):
                        _ms = unicode(_m)
                        if u'\u7f16\u8bd1\u5b8c\u6210' in _ms or u'errors' in _ms.lower():
                            _done = True; break
                if _done: break
        except: pass
        if _done: break
    log(u'Build wait done ({}s)'.format(_waited))

    compile_cat = None
    for _c in (system.get_message_categories() or []):
        try:
            _desc = system.get_message_category_description(_c)
            if u'\u7f16\u8bd1' in _desc or u'build' in _desc.lower() or u'compil' in _desc.lower():
                compile_cat = _c; break
        except: pass

    if compile_cat is None:
        log(u'[WARN] compile message category not found'); return

    msgs = list(system.get_message_objects(compile_cat) or [])
    summary_line = u''
    for m in msgs:
        try: line = unicode(m)
        except: line = str(m).decode(u'utf-8', u'replace')
        log(u'  ' + line)
        if u'\u7f16\u8bd1\u5b8c\u6210' in line or u'complete' in line.lower():
            summary_line = line

    _m_err  = _re.search(u'(\\d+)\\s*\u9519\u8bef',  summary_line)
    _m_warn = _re.search(u'(\\d+)\\s*\u8b66\u544a', summary_line)
    n_err  = int(_m_err.group(1))  if _m_err  else -1
    n_warn = int(_m_warn.group(1)) if _m_warn else  0

    if n_err == -1:
        log(u'[WARN] summary line not found, fallback to keyword scan')
        n_err = 0
        for m in msgs:
            try: line = unicode(m)
            except: line = str(m).decode(u'utf-8', u'replace')
            if (u'\u9519\u8bef' in line or u'error' in line.lower()) and \
               (u'0 \u9519\u8bef' not in line and u'0 error' not in line.lower()) and \
               (u'\u7f16\u8bd1\u5b8c\u6210' not in line and u'complete' not in line.lower()):
                n_err += 1

    if n_err > 0:
        log(u'>>> BUILD FAILED - {} error(s) <<<'.format(n_err))
    else:
        log(u'>>> BUILD OK - 0 errors{} <<<'.format(
            u', {} warning(s)'.format(n_warn) if n_warn > 0 else u' 0 warnings'))

log(u'Building...')
do_build()

log(u'=== done ===')
