# -*- coding: utf-8 -*-
# patch_pou.py - POU patcher (debug/iteration tool)
# Opens an existing .project, overwrites specified POUs from st/ dir, saves, compiles.

import os
import codecs
import time
import hashlib
import json

# -- path calculation: prefer env var injected by run_script.ps1; fallback to __file__ depth
_skill_dir = os.environ.get('INOPRO_SKILL_DIR', '').strip()
if not _skill_dir:
    _skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -- read env.json early to get workspace_dir
_env_json = os.path.join(_skill_dir, 'references', 'env.json')

def _read_env():
    raw = open(_env_json, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    import json
    return json.loads(raw.decode('utf-8'))

_env = _read_env()

# workspace_dir: must be explicitly set in env.json; empty = fatal error (no silent fallback)
_ws_dir = _env.get('workspace_dir', '').strip()
if not _ws_dir:
    _err_early = os.path.join(_skill_dir, 'scripts', 'workspace', 'log', 'patch_pou_error.txt')
    try:
        if not os.path.exists(os.path.dirname(_err_early)):
            os.makedirs(os.path.dirname(_err_early))
        with open(_err_early, 'ab') as _fe:
            _fe.write(u'[FATAL] workspace_dir \u672a\u8bbe\u7f6e\uff0c\u8bf7\u5148\u5728 env.json \u4e2d\u5199\u5165 workspace_dir \u5b57\u6bb5\n'.encode('utf-8'))
    except:
        pass
    system.exit()

_log_dir = os.path.join(_ws_dir, 'log')
_st_dir  = os.path.join(_ws_dir, 'st')
_out_dir = _ws_dir

if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)

_script_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
_log_path    = os.path.join(_log_dir, _script_name + u'_log.txt')
_err_file    = os.path.join(_log_dir, u'patch_pou_error.txt')

_log_fh = codecs.open(_log_path, u'w', encoding=u'utf-8')

def log(msg):
    if isinstance(msg, bytes):
        msg = msg.decode(u'utf-8', u'replace')
    elif not isinstance(msg, unicode):
        msg = unicode(msg)
    line = u'[{}] {}'.format(time.strftime(u'%H:%M:%S'), msg)
    _log_fh.write(line + u'\n')
    _log_fh.flush()

def err(msg):
    log(u'[ERROR] ' + msg)
    try:
        if isinstance(msg, unicode):
            data = (msg + u'\n').encode(u'utf-8')
        else:
            data = (unicode(msg) + u'\n').encode(u'utf-8')
        with open(_err_file, u'ab') as f:
            f.write(data)
    except:
        pass

def fatal(msg):
    err(msg)
    log(u'=== patch_pou done ===')
    system.exit()

# patch_target: project path to patch; auto-select newest .project if empty
PROJ_PATH = _env.get('patch_target', '').strip()
if not PROJ_PATH:
    candidates = [
        os.path.join(_ws_dir, f)
        for f in os.listdir(_ws_dir)
        if f.endswith('.project') and not f.endswith('.autosave')
    ] if os.path.exists(_ws_dir) else []
    if candidates:
        PROJ_PATH = max(candidates, key=lambda p: os.path.getmtime(p))
        log(u'[INFO] patch_target not set, auto-selected: ' + PROJ_PATH)
    else:
        fatal(u'workspace_dir has no .project file and patch_target not set in env.json')

# patch_pous: comma-separated POU names; empty = auto-detect from snapshot diff
PATCH_POUS_STR = _env.get('patch_pous', '').strip()
PATCH_POUS = [p.strip() for p in PATCH_POUS_STR.split(',') if p.strip()] if PATCH_POUS_STR else []

# patch_no_build: skip compile step
NO_BUILD = str(_env.get('patch_no_build', '')).lower() in ('true', '1', 'yes')

# -- task_mounts: read from workspace_dir/task_mounts.json
# NOTE: Keep in sync with _load_task_mounts_from_json() in generator_runner.py.
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
    except Exception as _tm_ex:
        log(u'[WARN] could not read task_mounts.json: ' + unicode(_tm_ex))
        return {}

TASK_MOUNTS = _load_task_mounts_from_json(_ws_dir)

# ---------------------------------------------------------------------------
# Snapshot diff detection.
#
# Baseline: .committed.json under st/
#   Written by THIS script after each successful save(), and by export_pou.py
#   after export. Records the MD5 hashes of st/ files that are in sync with
#   the .project file content.
#
# Detection logic:
#   1. Load .committed.json. If absent → first run → patch all POUs.
#   2. Compute current MD5 for every .st file under st/.
#   3. Compare current vs committed: changed / added / deleted → derive POU names.
#   4. If patch_pous is explicitly set in env.json, that list overrides detection.
# ---------------------------------------------------------------------------
def _md5_file(filepath):
    try:
        data = open(filepath, 'rb').read()
        return hashlib.md5(data).hexdigest()
    except:
        return None

def _load_committed(st_dir):
    """Load .committed.json baseline. Returns dict or None if not found."""
    sp = os.path.join(st_dir, u'.committed.json')
    if not os.path.exists(sp):
        return None
    try:
        raw = open(sp, 'rb').read().lstrip(b'\xef\xbb\xbf')
        return json.loads(raw.decode('utf-8'))
    except:
        return None

def _save_committed(st_dir, committed_dict):
    """Write .committed.json — call this after every successful save()."""
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
        log(u'committed snapshot updated ({} files)'.format(len(keys)))
    except Exception as e:
        log(u'[WARN] could not write .committed.json: ' + unicode(e))

def _build_current_hashes(st_dir):
    """Return dict: rel_path -> md5 for every .st file under st_dir."""
    result = {}
    for dirpath, dirnames, filenames in os.walk(st_dir):
        for fname in filenames:
            if fname.endswith('.st') and not fname.startswith('.'):
                abs_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(abs_path, st_dir).replace(os.sep, '/')
                h = _md5_file(abs_path)
                if h:
                    result[rel_path] = h
    return result

def _pou_name_from_st(fname):
    if fname.endswith('.act.st'):
        return fname[:-len('.act.st')]
    elif fname.endswith('.st'):
        return fname[:-3]
    return None

def _detect_changed_pous(st_dir):
    old_snap = _load_committed(st_dir)
    if old_snap is None:
        return None  # no baseline → caller patches all

    cur_snap = _build_current_hashes(st_dir)

    changed_pous = set()
    for rel_path, cur_hash in cur_snap.items():
        old_hash = old_snap.get(rel_path)
        if old_hash != cur_hash:
            pou = _pou_name_from_st(os.path.basename(rel_path))
            if pou:
                changed_pous.add(pou)

    for rel_path in old_snap:
        if rel_path not in cur_snap:
            pou = _pou_name_from_st(os.path.basename(rel_path))
            if pou:
                changed_pous.add(pou)

    return sorted(changed_pous)

log(u'--- patch_pou start ---')
log(u'project : ' + PROJ_PATH)
log(u'POUs    : ' + (', '.join(PATCH_POUS) if PATCH_POUS else u'(auto-detect)'))
log(u'st dir  : ' + _st_dir)
log(u'no_build: ' + str(NO_BUILD))

if not os.path.exists(PROJ_PATH):
    fatal(u'project file not found: ' + PROJ_PATH)

# -- read st file by absolute path (POU_MAP now stores abs paths)
def read_st(abs_path):
    if abs_path is None:
        return None
    if not os.path.exists(abs_path):
        log(u'[WARN] st file not found, skip: ' + abs_path)
        return None
    f = codecs.open(abs_path, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    return content

# -- type detection and splitting for single-file POU format

def _plain_kind_from_content(content, pou_name):
    """从已读取的 .st 文本返回 'pou'/'gvl'/'dut_struct'/'dut_enum'，失败时按前缀 fallback。
    注：与 generator_runner.py 中同名函数逻辑相同，如有修改请同步。"""
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
    注：与 generator_runner.py 中同名函数逻辑相同，如有修改请同步。
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
        break

    if pou_type is None:
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
        decl_lines = lines[header_idx:header_idx + 1]
        impl_lines = lines[header_idx + 1:end_idx]
    else:
        decl_lines = lines[header_idx:last_end_var_idx + 1]
        impl_lines = lines[last_end_var_idx + 1:end_idx]

    decl_text = u'\n'.join(decl_lines)
    impl_text  = u'\n'.join(impl_lines).strip()
    return pou_type, decl_text, impl_text

# -- scan st/ recursively; build POU_MAP
# Key: POU name; Value: (file_path, kind, parent_path_list)
# kind: 'pou' | 'gvl' | 'dut_struct' | 'dut_enum' | 'act'
# 'pou' = 单文件格式（.st，内含 FUNCTION_BLOCK/PROGRAM/FUNCTION）
def _build_pou_map(st_dir):
    pou_map = {}
    if not os.path.exists(st_dir):
        log(u'[WARN] st/ dir not found: ' + st_dir)
        return pou_map

    # Collect all .st files recursively
    all_st = []
    for dirpath, dirnames, filenames in os.walk(st_dir):
        for fname in filenames:
            if fname.endswith('.st'):
                all_st.append(os.path.join(dirpath, fname))
    all_st.sort()

    # Helper: get full parent path list relative to st_dir
    def _parent_path(abs_path):
        rel = os.path.relpath(os.path.dirname(abs_path), st_dir)
        if rel == u'.':
            return []
        return rel.split(os.sep)

    act_map   = {}   # act_name -> (abs act path, parent_path_list)
    plain_map = {}   # pou_name -> (abs plain path, parent_path_list)

    for abs_path in all_st:
        fname = os.path.basename(abs_path)
        pp = _parent_path(abs_path)
        if fname.endswith('.act.st'):
            act_name = _pou_name_from_st(fname)
            if act_name in act_map:
                log(u'[WARN] duplicate ACT name "' + act_name + u'", overwriting with: ' + abs_path)
            act_map[act_name] = (abs_path, pp)
        elif fname.endswith('.st'):
            pou_name = _pou_name_from_st(fname)
            if pou_name in plain_map:
                log(u'[WARN] duplicate name "' + pou_name + u'", overwriting with: ' + abs_path)
            plain_map[pou_name] = (abs_path, pp)

    # Build final map: (file_path, kind, parent_path_list)
    # _st_cache: file_path -> content，避免补丁循环中再次读取同一文件
    _st_cache = {}
    for act_name, (act_path, pp) in act_map.items():
        pou_map[act_name] = (act_path, 'act', pp)

    for pou_name, (plain_path, pp) in plain_map.items():
        _cached = read_st(plain_path)
        if _cached is None:
            _cached = u''
        _st_cache[plain_path] = _cached
        real_kind = _plain_kind_from_content(_cached, pou_name)
        # When a POU has actions it is placed inside a same-name subdirectory:
        #   st/程序/P_Main/P_Main.st
        # In this case pp ends with the POU name as an extra directory layer.
        # Strip that last element so the parent_path points to the CODESYS
        # folder that actually contains the POU node (e.g. ['程序']), not to
        # a non-existent '程序/P_Main' folder inside the IDE.
        effective_pp = pp
        if pp and pp[-1] == pou_name:
            effective_pp = pp[:-1]
        pou_map[pou_name] = (plain_path, real_kind, effective_pp)

    return pou_map, _st_cache

POU_MAP, _ST_CACHE = _build_pou_map(_st_dir)

if not POU_MAP:
    log(u'[WARN] no .st files found in st/ dir, will only compile')
else:
    log(u'scanned POUs: ' + u', '.join(sorted(POU_MAP.keys())))

if PATCH_POUS:
    log(u'patch_pous explicitly set, overriding auto-detect')
else:
    _changed = _detect_changed_pous(_st_dir)
    if _changed is not None:
        PATCH_POUS = _changed
        log(u'snapshot diff detected ' + str(len(_changed)) + u' changed POU(s): ' + u', '.join(_changed))
    else:
        PATCH_POUS = sorted(POU_MAP.keys())
        log(u'no snapshot found, patching all POUs (first time)')

# -- find IEC container
def find_iec_container(proj):
    """优先找名为 Application 的 IEC 容器，fallback 到任意 IEC 容器。"""
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
            if u'ScriptIecLanguageObjectContainerObject' in unicode(c):
                return c
        for c in children:
            r = _find_any(c, depth + 1)
            if r: return r
        return None
    result = _find_app(proj, 0)
    if result: return result
    return _find_any(proj, 0)

# -- find POU/ACT by name, recursively searching the entire IEC tree.
# Matches nodes that have textual_declaration OR textual_implementation (real code objects).
# Skips Task-reference nodes (same name, but neither decl nor impl).
# ACTIONs (no decl, has impl) live as children of Program nodes, so we always
# recurse into every node regardless of whether it has decl.
def find_pou(iec, name):
    def _search(node):
        try:
            children = node.get_children()
        except:
            return None
        if not children:
            return None
        for child in children:
            child_name = None
            try:
                child_name = child.get_name()
            except:
                try:
                    child_name = child.get_name(False)
                except:
                    pass

            if child_name == name:
                # Must be a real code object (has decl OR impl), not a Task ref
                has_decl = False
                has_impl = False
                try:
                    has_decl = child.textual_declaration is not None
                except:
                    pass
                try:
                    has_impl = child.textual_implementation is not None
                except:
                    pass
                if has_decl or has_impl:
                    return child
                # Same name but no code -> Task reference node, keep searching

            # Always recurse into every node: both Groups and POU nodes
            # can contain ACTIONs as children.
            result = _search(child)
            if result is not None:
                return result
        return None
    return _search(iec)

# -- find a named group/folder node directly under `parent` (one level only).
# Returns the node if found, else None.
def _find_child_group(parent, name):
    try:
        children = parent.get_children()
    except:
        return None
    if not children:
        return None
    for child in children:
        child_name = None
        try:
            child_name = child.get_name()
        except:
            try:
                child_name = child.get_name(False)
            except:
                pass
        if child_name == name:
            has_decl = False
            has_impl = False
            try:
                has_decl = child.textual_declaration is not None
            except:
                pass
            try:
                has_impl = child.textual_implementation is not None
            except:
                pass
            if not has_decl and not has_impl:
                return child
    return None

# -- find or create the full group path under `root`.
# path_list: e.g. ["FB功能块", "基础FB"]
# For each level: look for existing child group; if not found, create_folder
# then locate the new node via get_children().
# Returns the deepest group node, or root if path_list is empty.
def find_or_create_group_path(root, path_list):
    node = root
    for part in path_list:
        child = _find_child_group(node, part)
        if child is None:
            log(u'[CREATE] folder "' + part + u'" not found under parent, creating...')
            node.create_folder(part)
            # create_folder returns None; locate the new node via get_children
            child = _find_child_group(node, part)
            if child is None:
                log(u'[WARN] create_folder("' + part + u'") succeeded but node not found after creation')
                return node  # fallback: use current level
            log(u'[CREATE] folder "' + part + u'" created OK')
        node = child
    return node

# -- create a new Program POU under the given parent (group node or iec root)
# Returns the new node, or None on failure.
def create_program(parent, pou_name):
    try:
        new_obj = parent.create_pou(pou_name, PouType.Program)
        log(u'[CREATE] created Program "' + pou_name + u'" under parent')
        return new_obj
    except Exception as e:
        log(u'[WARN] create_program failed: ' + unicode(e))
        return None
def _safe_replace(td, text):
    """Safe full replacement of ScriptTextDocument content with verify+retry.
    Primary: td.replace(text) — single-arg whole-doc replace (API confirmed in 3.5.10+).
    After write, verify td.text matches input. If not, retry with fallback methods.
    Fallback 1: loop remove + insert.
    Fallback 2: append + remove prefix.
    """
    for _attempt in range(3):
        if _attempt == 0:
            try:
                td.replace(text)
            except:
                continue
        elif _attempt == 1:
            try:
                while td.length > 0:
                    td.remove(0, td.length)
                td.insert(0, text)
            except:
                continue
        else:
            try:
                default_len = td.length
                td.append(text)
                if default_len > 0:
                    td.remove(0, default_len)
            except:
                break
        try:
            actual = td.text
            if actual is not None and actual.strip() == text.strip():
                return
            log(u'[WARN] _safe_replace verify mismatch (attempt {}), td.length={} expected={}'.format(_attempt + 1, len(actual) if actual else -1, len(text)))
        except:
            pass
    log(u'[WARN] _safe_replace all attempts exhausted for text length={}'.format(len(text)))

def patch_gvl(gvl_obj, decl_content):
    try:
        td = gvl_obj.textual_declaration
        if td is not None:
            _safe_replace(td, decl_content)
            return True
    except Exception as e:
        log(u'[WARN] patch_gvl: ' + unicode(e))
    return False

# -- patch POU
def patch_pou_obj(pou_obj, decl_content, impl_content):
    ok = True
    if decl_content is not None:
        try:
            td = pou_obj.textual_declaration
            if td is not None:
                _safe_replace(td, decl_content)
        except Exception as e:
            log(u'[WARN] patch decl: ' + unicode(e))
            ok = False
    if impl_content is not None:
        try:
            ti = pou_obj.textual_implementation
            if ti is not None:
                _safe_replace(ti, impl_content)
        except Exception as e:
            log(u'[WARN] patch impl: ' + unicode(e))
            ok = False
    return ok

# -- build
def do_build():
    build_cmd = None
    for cmd in system.commands:
        tokens = cmd.tokens
        if tokens is not None:
            tl = list(tokens)
            if 'project' in tl and 'buildactiveapp' in tl:
                build_cmd = cmd
                break
    if build_cmd is None:
        log(u'[WARN] buildactiveapp command not found, skip compile')
        return

    cats_pre = system.get_message_categories()
    for c in cats_pre:
        desc = system.get_message_category_description(c)
        if u'\u7f16\u8bd1' in desc or 'build' in desc.lower() or 'compil' in desc.lower():
            try:
                system.clear_messages(c)
            except:
                pass
            break

    build_cmd.execute()

    # 轮询等待编译完成（检测到"编译完成"消息即提前退出，最长 60s）
    _build_done   = False
    _build_waited = 0
    _build_max    = 60
    while _build_waited < _build_max:
        time.sleep(1)
        _build_waited += 1
        try:
            _cats = system.get_message_categories()
            for _c in _cats:
                _desc = system.get_message_category_description(_c)
                if u'\u7f16\u8bd1' in _desc or 'build' in _desc.lower() or 'compil' in _desc.lower():
                    _msgs = system.get_message_objects(_c)
                    for _m in _msgs:
                        _ms = unicode(_m)
                        if u'\u7f16\u8bd1\u5b8c\u6210' in _ms or 'errors' in _ms.lower():
                            _build_done = True
                            break
                if _build_done:
                    break
        except:
            pass
        if _build_done:
            break
    log(u'build wait done (waited {}s), reading messages...'.format(_build_waited))

    cats = system.get_message_categories()
    compile_cat = None
    for c in cats:
        desc = system.get_message_category_description(c)
        if u'\u7f16\u8bd1' in desc or 'build' in desc.lower() or 'compil' in desc.lower():
            compile_cat = c
            break
    if compile_cat is None:
        log(u'[WARN] compile message category not found')
        return

    msgs = system.get_message_objects(compile_cat)
    # -- 先打印所有消息，同时找汇总行 --
    summary_line = u''
    all_lines = []
    for m in msgs:
        try: line = unicode(m)
        except: line = str(m).decode(u'utf-8', u'replace')
        log(u'  ' + line)
        all_lines.append(line)
        if u'\u7f16\u8bd1\u5b8c\u6210' in line or 'complete' in line.lower():
            summary_line = line

    # -- 从汇总行提取错误/警告数（最可靠，不依赖具体错误行关键词） --
    # 汇总行格式："编译完成 -- N 错误, M 警告"
    import re as _re
    _m_err  = _re.search(u'(\\d+)\\s*\u9519\u8bef',  summary_line)
    _m_warn = _re.search(u'(\\d+)\\s*\u8b66\u544a', summary_line)
    n_err  = int(_m_err.group(1))  if _m_err  else -1
    n_warn = int(_m_warn.group(1)) if _m_warn else  0

    if n_err == -1:
        # 未找到汇总行（极端情况），fallback：关键词扫描具体行
        log(u'[WARN] summary line not found, fallback to keyword scan')
        n_err = 0
        for line in all_lines:
            if (u'\u9519\u8bef' in line or 'error' in line.lower()) and \
               (u'0 \u9519\u8bef' not in line and '0 error' not in line.lower()) and \
               (u'\u7f16\u8bd1\u5b8c\u6210' not in line and 'complete' not in line.lower()):
                n_err += 1

    if n_err > 0:
        err(u'build has {} error(s), fix st/ files and re-run patch_pou.py'.format(n_err))
        log(u'=== BUILD FAILED - {} error(s) ==='.format(n_err))
    else:
        if n_warn > 0:
            log(u'=== BUILD OK - {} warning(s) ==='.format(n_warn))
        else:
            log(u'=== BUILD OK - 0 errors 0 warnings ===')

# =============================================================================
# open project, apply patches
# =============================================================================
log(u'opening project...')
try:
    proj = projects.open(PROJ_PATH)
except Exception as e:
    fatal(u'projects.open() failed: ' + unicode(e))

if proj is None:
    fatal(u'projects.open() returned None')

# 轮询等待工程加载完成（最长 30s，检测到 get_children() 有返回就提前退出）
_wait_max = 30
_waited   = 0
while _waited < _wait_max:
    time.sleep(1)
    _waited += 1
    try:
        _ch = proj.get_children()
        if _ch and len(list(_ch)) > 0:
            break
    except:
        pass
log(u'project opened (waited {}s)'.format(_waited))

iec = find_iec_container(proj)
if not iec:
    fatal(u'IEC container not found')

# -- patch each POU
patched_count = 0
for pou_name in PATCH_POUS:
    if pou_name not in POU_MAP:
        log(u'[WARN] POU "' + pou_name + u'" not in st/ dir, skip')
        continue

    file_path, kind, parent_path = POU_MAP[pou_name]

    pou_obj = find_pou(iec, pou_name)

    # If not found in project, try to create it.
    if pou_obj is None and kind == 'act':
        if parent_path:
            parent_pou_name = parent_path[-1]
            parent_pou_node = find_pou(iec, parent_pou_name)
            if parent_pou_node is None:
                log(u'[SKIP] ' + pou_name + u' - parent POU "' + parent_pou_name + u'" not found, cannot create Action')
            else:
                try:
                    pou_obj = parent_pou_node.create_action(pou_name)
                    log(u'[CREATE] created Action "' + pou_name + u'" under "' + parent_pou_name + u'"')
                except Exception as e:
                    log(u'[WARN] create_action failed for "' + pou_name + u'": ' + unicode(e))
        else:
            log(u'[SKIP] ' + pou_name + u' - .act.st at st/ root has no parent POU dir')

    if pou_obj is None and kind in ('pou', 'gvl', 'dut_struct', 'dut_enum'):
        parent_node = find_or_create_group_path(iec, parent_path)
        if kind == 'pou':
            # 读单文件内容判断 PouType（优先从 _ST_CACHE 取，避免重复读文件）
            raw = _ST_CACHE.get(file_path) or read_st(file_path)
            _pou_type, _, _ = _split_pou_single_file(raw or u'', pou_name)
            _type_label = {PouType.Program: u'Program', PouType.Function: u'Function'}.get(_pou_type, u'FunctionBlock')
            try:
                pou_obj = parent_node.create_pou(pou_name, _pou_type)
                log(u'[CREATE] created {} "{}"'.format(_type_label, pou_name))
            except Exception as e:
                log(u'[WARN] create_pou failed: ' + unicode(e))
        elif kind == 'dut_struct':
            try:
                pou_obj = parent_node.create_dut(pou_name, DutType.Structure)
                log(u'[CREATE] created DUT(Structure) "' + pou_name + u'"')
            except Exception as e:
                log(u'[WARN] create_dut(Structure) failed: ' + unicode(e))
        elif kind == 'dut_enum':
            try:
                pou_obj = parent_node.create_dut(pou_name, DutType.Enumeration)
                log(u'[CREATE] created DUT(Enumeration) "' + pou_name + u'"')
            except Exception as e:
                log(u'[WARN] create_dut(Enumeration) failed: ' + unicode(e))
        else:
            try:
                pou_obj = parent_node.create_gvl(pou_name)
                log(u'[CREATE] created GVL "' + pou_name + u'"')
            except Exception as e:
                log(u'[WARN] create_gvl failed: ' + unicode(e))

    if pou_obj is None:
        log(u'[SKIP] ' + pou_name + u' - not found in project and could not be created')
        continue

    log(u'patching ' + pou_name + u' (kind=' + kind + u') ...')

    if kind == 'gvl' or kind == 'dut_struct' or kind == 'dut_enum':
        decl_content = read_st(file_path)
        if decl_content is None:
            log(u'[SKIP] ' + pou_name + u' - file missing')
            continue
        ok = patch_gvl(pou_obj, decl_content)

    elif kind == 'act':
        impl_content = read_st(file_path)
        if impl_content is None:
            log(u'[SKIP] ' + pou_name + u' - act file missing')
            continue
        ok = True
        try:
            ti = pou_obj.textual_implementation
            if ti is not None:
                _safe_replace(ti, impl_content)
            else:
                log(u'[WARN] ' + pou_name + u' textual_implementation is None')
                ok = False
        except Exception as e:
            log(u'[WARN] patch act impl: ' + unicode(e))
            ok = False

    else:  # kind == 'pou'
        raw_content = _ST_CACHE.get(file_path) or read_st(file_path)
        if raw_content is None:
            log(u'[SKIP] ' + pou_name + u' - st file missing')
            continue
        _, decl_content, impl_content = _split_pou_single_file(raw_content, pou_name)
        ok = patch_pou_obj(pou_obj, decl_content, impl_content if impl_content else None)

    if ok:
        log(u'  [OK] ' + pou_name)
        patched_count += 1
    else:
        log(u'  [WARN] ' + pou_name + u' partial write failure')

log(u'patched ' + str(patched_count) + u' POU(s)')

# -- task_mounts (per-project, from workspace_dir/task_mounts.json)
# mode=append: idempotent append (default, safe for external projects)
# mode=replace: attempt full replace; remove(str) may not persist on external projects
#               (InoProShop V1.9.0.1 known bug), but add(name) is always reliable.
def _apply_task_mounts(proj):
    """Apply TASK_MOUNTS to the project's Task Configuration."""
    if not TASK_MOUNTS:
        return

    log(u'')
    log(u'--- task_mounts ---')

    def _find_task_cfg(node, depth=0):
        if depth > 6: return None
        try: ch = node.get_children()
        except: return None
        for c in (list(ch) if ch else []):
            try:
                if u'ScriptTaskConfigObject' in unicode(c): return c
            except: pass
            r = _find_task_cfg(c, depth + 1)
            if r: return r
        return None

    def _find_task_node(cfg, task_name):
        try:
            children = list(cfg.get_children()) if cfg.get_children() else []
        except:
            return None
        for c in children:
            try:
                if c.get_name() == task_name and u'ScriptTaskObject' in unicode(c):
                    return c
            except: pass
        return None

    task_cfg = _find_task_cfg(proj)
    if task_cfg is None:
        log(u'[WARN] task_mounts: Task Configuration not found, skipping')
        return

    for task_name, cfg in TASK_MOUNTS.items():
        pou_list = cfg.get(u'pous', [])
        mode     = cfg.get(u'mode', u'append')
        if not pou_list:
            continue

        task_node = _find_task_node(task_cfg, task_name)

        if task_node is None:
            if cfg.get(u'create', False):
                log(u'[INFO] task_mounts: Task "{}" not found, creating...'.format(task_name))
                try:
                    task_cfg.create_task(task_name)
                    log(u'Task "{}" created OK'.format(task_name))
                    task_node = _find_task_node(task_cfg, task_name)
                except Exception as ex:
                    log(u'[WARN] create_task("{}") failed: {}'.format(task_name, unicode(ex)))
            else:
                log(u'[WARN] task_mounts: Task "{}" not found'.format(task_name))
                continue

        if task_node is None:
            log(u'[WARN] task_mounts: Task "{}" node not found after create attempt'.format(task_name))
            continue

        try:
            pous = task_node.pous
            existing_names = [unicode(x).strip() for x in list(pous)]
            log(u'Task "{}" mode={} existing: [{}]'.format(task_name, mode, u', '.join(existing_names)))
        except Exception as ex:
            log(u'[WARN] task_mounts: task.pous read failed for "{}": {}'.format(task_name, unicode(ex)))
            continue

        try:
            new_set    = set(pou_list)
            exist_set  = set(existing_names)
            if mode == u'replace':
                for old in existing_names:
                    if old not in new_set:
                        try:
                            pous.remove(old)
                            log(u'  remove "{}": OK (verify after save)'.format(old))
                        except Exception as ex:
                            log(u'  [WARN] remove("{}") failed: {} -- manual UI action required'.format(old, unicode(ex)))
                for new in pou_list:
                    if new not in exist_set:
                        try:
                            pous.add(new)
                            log(u'  add "{}": OK'.format(new))
                        except Exception as ex:
                            log(u'  [WARN] add("{}") failed: {}'.format(new, unicode(ex)))
            else:  # append (default)
                for prg in pou_list:
                    if prg in exist_set:
                        log(u'  skip (already mounted): ' + prg)
                    else:
                        try:
                            pous.add(prg)
                            log(u'  added to Task "{}": {}'.format(task_name, prg))
                        except Exception as ex:
                            log(u'  [WARN] pous.add("{}"): {}'.format(prg, unicode(ex)))
        except Exception as ex:
            log(u'[WARN] task_mounts: operations failed for "{}": {}'.format(task_name, unicode(ex)))

_apply_task_mounts(proj)

# -- save (一次保存覆盖 POU patch + task_mounts 两阶段的所有修改)
log(u'saving...')
_save_ok = False
try:
    proj.save()
    log(u'save OK')
    _save_ok = True
except Exception as e:
    log(u'[WARN] save() failed, trying save_as: ' + unicode(e))
    try:
        proj.save_as(PROJ_PATH)
        log(u'save_as OK')
        _save_ok = True
    except Exception as e2:
        fatal(u'save failed: ' + unicode(e2))

# -- update committed snapshot after successful save
# .committed.json records what is NOW in the .project file.
# Update whenever save succeeds — not just when POUs were patched,
# because task_mounts changes (pous.add) also modify the project
# and must be reflected in the baseline for the next diff.
if _save_ok:
    _save_committed(_st_dir, _build_current_hashes(_st_dir))

time.sleep(3)

# -- compile
if NO_BUILD:
    log(u'[INFO] patch_no_build=true, skip compile')
else:
    do_build()

log(u'=== patch_pou done ===')
