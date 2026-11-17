# -*- coding: utf-8 -*-
# export_pou.py - export all POUs from an existing .project to st/ directory
# Supports nested groups: creates subdirectories mirroring the project folder structure.
# Usage: run via InoProShop.exe --Profile="..." /runscript="export_pou.py"

import os, json, time, codecs, hashlib

# -- path calculation: prefer env var injected by run_script.ps1; fallback to __file__ depth
_skill_dir = os.environ.get('INOPRO_SKILL_DIR', '').strip()
if not _skill_dir:
    _skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -- read env.json once; derive all paths from it
_env_path = os.path.join(_skill_dir, 'references', 'env.json')
try:
    _env_raw = open(_env_path, 'rb').read()
    if _env_raw.startswith(b'\xef\xbb\xbf'):
        _env_raw = _env_raw[3:]
    _env = json.loads(_env_raw.decode('utf-8'))
except Exception as _env_ex:
    _env = {}

_ws_dir = _env.get('workspace_dir', '').strip()
if not _ws_dir:
    _err_early = os.path.join(_skill_dir, 'scripts', 'workspace', 'log', 'export_pou_error.txt')
    try:
        if not os.path.exists(os.path.dirname(_err_early)):
            os.makedirs(os.path.dirname(_err_early))
        with open(_err_early, 'ab') as _fe:
            _fe.write(u'[FATAL] workspace_dir \u672a\u8bbe\u7f6e\uff0c\u8bf7\u5148\u5728 env.json \u4e2d\u5199\u5165 workspace_dir \u5b57\u6bb5\n'.encode('utf-8'))
    except:
        pass
    system.exit()

_st_dir  = os.path.join(_ws_dir, 'st')
_log_dir = os.path.join(_ws_dir, 'log')

if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)

_script_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
_log_path = os.path.join(_log_dir, _script_name + u'_log.txt')

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
    log(u'[ERROR] ' + msg)
    log(u'=== export_pou.py done ===')
    system.exit()

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
            if u'ScriptIecLanguageObjectContainerObject' in unicode(c): return c
        for c in children:
            r = _find_any(c, depth + 1)
            if r: return r
        return None
    result = _find_app(proj, 0)
    if result: return result
    return _find_any(proj, 0)

def _get_end_keyword(decl_text):
    """从声明区第一行推断对应的 END_xxx 关键字。"""
    for raw_line in (decl_text or u'').splitlines():
        stripped = raw_line.strip().upper()
        if not stripped or stripped.startswith(u'//') or stripped.startswith(u'(*'):
            continue
        if stripped.startswith(u'FUNCTION_BLOCK'):
            return u'END_FUNCTION_BLOCK'
        if stripped.startswith(u'PROGRAM'):
            return u'END_PROGRAM'
        if stripped.startswith(u'FUNCTION') and not stripped.startswith(u'FUNCTION_BLOCK'):
            return u'END_FUNCTION'
        break
    return u''

def _merge_pou_single_file(decl_text, impl_text):
    """将 CODESYS POU 的声明区和实现区合并为单文件格式。
    声明区已含 FUNCTION_BLOCK/PROGRAM/FUNCTION 头行和 VAR...END_VAR 块，
    不含 END_FUNCTION_BLOCK/END_PROGRAM/END_FUNCTION。
    合并结果：<decl_text>\n<impl_text>\nEND_xxx
    """
    end_keyword = _get_end_keyword(decl_text)
    if not end_keyword:
        # 无法判断类型，退回简单拼接
        return (decl_text or u'') + u'\n' + (impl_text or u'')
    parts = []
    if decl_text:
        parts.append(decl_text.rstrip())
    if impl_text and impl_text.strip():
        parts.append(impl_text.strip())
    parts.append(end_keyword)
    return u'\n'.join(parts) + u'\n'

def write_st(path, content):
    # ensure parent dir exists
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)
    if content is None:
        content = u''
    if isinstance(content, unicode):
        data = content.encode('utf-8')
    else:
        data = unicode(content).encode('utf-8')
    with open(path, 'wb') as f:
        f.write(data)

# --- derive PROJ_PATH from already-loaded _env
PROJ_PATH = _env.get('patch_target', '').strip()
if not PROJ_PATH:
    # Auto-select newest .project directly under _ws_dir
    candidates = [
        os.path.join(_ws_dir, f)
        for f in (os.listdir(_ws_dir) if os.path.exists(_ws_dir) else [])
        if f.endswith('.project') and not f.endswith('.autosave')
    ]
    if candidates:
        PROJ_PATH = max(candidates, key=lambda p: os.path.getmtime(p))
        log('[INFO] patch_target not set, auto-selected: ' + PROJ_PATH)
    else:
        fatal('[ERROR] no .project found in workspace_dir and patch_target not set')

# If workspace_dir was the legacy flat path, auto-derive per-project subdir from PROJ_PATH.
# run_script.ps1 normally writes the correct per-project workspace_dir before launching,
# so this branch only fires in rare edge cases (e.g. very first run without env.json update).
_builtin_ws = os.path.join(_skill_dir, 'scripts', 'workspace')
if _ws_dir == _builtin_ws and PROJ_PATH:
    _proj_name = os.path.splitext(os.path.basename(PROJ_PATH))[0]
    _ws_dir  = os.path.join(_builtin_ws, _proj_name)
    _st_dir  = os.path.join(_ws_dir, 'st')
    _log_dir = os.path.join(_ws_dir, 'log')
    if not os.path.exists(_log_dir):
        os.makedirs(_log_dir)
    # reopen log in the correct location
    _log_path = os.path.join(_log_dir, 'export_pou_log.txt')
    open(_log_path, 'wb').close()

log('--- export_pou.py start ---')
log('project : ' + PROJ_PATH)
log('st dir  : ' + _st_dir)

if not os.path.exists(PROJ_PATH):
    fatal('[ERROR] project file not found: ' + PROJ_PATH)

# --- open project
log('opening project...')
try:
    proj = projects.open(PROJ_PATH)
except Exception as e:
    fatal('projects.open() failed: ' + unicode(e))

if proj is None:
    fatal('projects.open() returned None')

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
log('project opened (waited {}s)'.format(_waited))

iec = find_iec_container(proj)
if not iec:
    fatal(u'IEC container not found')
log('IEC container found: ' + str(iec)[:80])

# --- clear and recreate st/ dir
if os.path.exists(_st_dir):
    import shutil
    shutil.rmtree(_st_dir)
os.makedirs(_st_dir)
log('st/ dir ready: ' + _st_dir)

# ---------------------------------------------------------------------------
# Recursive walk: mirror project folder structure into st/ subdirectories.
#
# Node type detection (attribute probe, no type-name matching):
#
#   has_decl=T, has_impl=T  -> Full POU (FB/Program/Function)
#                              -> Name.st  (single-file: decl+impl merged)
#                              -> then recurse children for ACTIONs
#
#   has_decl=F, has_impl=T  -> ACTION (child of Program)
#     impl_len > 0           -> ST action  -> Name.act.st
#     impl_len == 0          -> Graphical (LD/FBD/SFC), skip + log NOTE
#
#   has_decl=T, has_impl=F  -> GVL / DUT / declaration-only
#                              -> Name.st
#
#   has_decl=F, has_impl=F  -> Group/Folder, recurse with name as subdir
#
# st/ layout example:
#   程序/P01_基础程序.st                         <- single-file POU
#   程序/P01_基础程序/ACT00_安全程序.act.st       <- ACT in its own subdir
#   程序/P01_基础程序/ACT01_通用主控.act.st
# ---------------------------------------------------------------------------
exported = 0
skipped  = 0
skipped_ld = 0

def walk_and_export(node, st_subdir):
    global exported, skipped, skipped_ld

    try:
        children = node.get_children()
    except Exception as e:
        log('[WARN] get_children() failed: ' + unicode(e))
        return
    if not children:
        return

    for child in children:
        # --- get name
        name = None
        try:
            name = child.get_name()
        except:
            try:
                name = child.get_name(False)
            except:
                pass
        if not name:
            skipped += 1
            continue

        # --- attribute probe
        has_decl = False
        has_impl = False
        decl_text = None
        impl_text = None

        try:
            td = child.textual_declaration
            if td is not None:
                has_decl = True
                decl_text = td.text
        except:
            pass
        try:
            ti = child.textual_implementation
            if ti is not None:
                has_impl = True
                impl_text = ti.text
        except:
            pass

        impl_len = len(impl_text) if impl_text else 0

        # ── Case 1: Group / Folder (no code at all) ──────────────────────
        if not has_decl and not has_impl:
            sub = os.path.join(st_subdir, name)
            log('  GROUP: ' + name)
            walk_and_export(child, sub)
            continue

        # ── Case 2: ACTION (no decl, has impl accessor) ───────────────────
        if not has_decl and has_impl:
            if impl_len > 0:
                act_path = os.path.join(st_subdir, name + '.act.st')
                write_st(act_path, impl_text)
                log('  ACT(ST): ' + act_path.replace(_st_dir + os.sep, ''))
                exported += 1
            else:
                log('  ACT(LD/skip): ' + os.path.join(st_subdir, name).replace(_st_dir + os.sep, ''))
                skipped_ld += 1
            continue

        # ── Case 3: Full POU (has decl + impl) ───────────────────────────
        if has_decl and has_impl:
            log('')
            log('  POU: ' + os.path.join(st_subdir, name).replace(os.sep, '/'))
            log('       decl=' + str(len(decl_text) if decl_text else 0) +
                '  impl=' + str(impl_len))

            # Pre-scan direct children to detect ST Actions.
            # If any ST Action exists, put the POU .st inside the same-name subdir
            # so that parent and its actions share one directory:
            #   st/程序/P_Main/P_Main.st
            #   st/程序/P_Main/ACT_Init.act.st
            # If no ST Actions exist, keep the classic flat layout:
            #   st/程序/P_Main.st
            _has_st_action = False
            try:
                _sub_children = child.get_children()
                if _sub_children:
                    for _sc in _sub_children:
                        _sc_has_decl = False
                        _sc_has_impl = False
                        _sc_impl_len = 0
                        try:
                            _sc_has_decl = _sc.textual_declaration is not None
                        except:
                            pass
                        try:
                            _ti = _sc.textual_implementation
                            if _ti is not None:
                                _sc_has_impl = True
                                _sc_impl_len = _ti.length
                        except:
                            pass
                        if not _sc_has_decl and _sc_has_impl and _sc_impl_len > 0:
                            _has_st_action = True
                            break
            except:
                pass

            act_subdir = os.path.join(st_subdir, name)
            if _has_st_action:
                pou_st_path = os.path.join(act_subdir, name + '.st')
            else:
                pou_st_path = os.path.join(st_subdir, name + '.st')

            if decl_text is not None:
                # 单文件格式：声明区 + 实现区合并到一个 .st 文件
                merged = _merge_pou_single_file(decl_text, impl_text)
                write_st(pou_st_path, merged)
                log('       -> ' + pou_st_path.replace(_st_dir + os.sep, '') +
                    ('  (with actions, placed in subdir)' if _has_st_action else '  (single-file POU)'))
                exported += 1
            else:
                log('       [SKIP] decl is None')
                skipped += 1
            # recurse into children to pick up ACTIONs
            walk_and_export(child, act_subdir)
            continue

        # ── Case 4: GVL / DUT / declaration-only ─────────────────────────
        if has_decl and not has_impl:
            if decl_text is not None:
                out_path = os.path.join(st_subdir, name + '.st')
                write_st(out_path, decl_text)
                log('  GVL/DUT: ' + out_path.replace(_st_dir + os.sep, ''))
                exported += 1
            else:
                log('  [SKIP] ' + name + ' no declaration text')
                skipped += 1
            continue

walk_and_export(iec, _st_dir)

log('')
log('exported: ' + str(exported) +
    '  skipped_ld: ' + str(skipped_ld) +
    '  skipped_other: ' + str(skipped))

# ---------------------------------------------------------------------------
# Write .committed.json so that the next patch has a correct baseline.
# At this point st/ was just freshly exported from the .project, so st/ and
# the project are in perfect sync. Recording their hashes here means patch
# will correctly detect only files that were modified AFTER this export,
# instead of re-patching everything (which would happen if .committed.json
# were absent or stale from a previous session).
# ---------------------------------------------------------------------------
try:
    _committed = {}
    for _dp, _dns, _fns in os.walk(_st_dir):
        for _fn in _fns:
            if _fn.endswith('.st') and not _fn.startswith('.'):
                _ap = os.path.join(_dp, _fn)
                _rp = os.path.relpath(_ap, _st_dir).replace(os.sep, '/')
                _data = open(_ap, 'rb').read()
                _committed[_rp] = hashlib.md5(_data).hexdigest()
    _committed_path = os.path.join(_st_dir, u'.committed.json')
    _keys = sorted(_committed.keys())
    _sb = u'{\n'
    for _i, _k in enumerate(_keys):
        _comma = u',' if _i < len(_keys) - 1 else u''
        _sb += u'  "{}": "{}"{}\n'.format(_k, _committed[_k], _comma)
    _sb += u'}'
    _cf = codecs.open(_committed_path, u'w', u'utf-8')
    _cf.write(_sb)
    _cf.close()
    log('committed snapshot written ({} files)'.format(len(_keys)))
except Exception as _ce:
    log('[WARN] could not write .committed.json: ' + unicode(_ce))

# ---------------------------------------------------------------------------
# Write task_mounts.json: record current Task Configuration structure
# so that AI can review and modify it before patching.
# Format: { "TaskName": { "pous": ["P01_xxx", ...], "interval": "T#10ms", ... } }
# ---------------------------------------------------------------------------
def _export_find_task_config(node, depth=0):
    if depth > 6:
        return None
    try:
        ch = node.get_children()
    except:
        return None
    for c in (list(ch) if ch else []):
        try:
            if u'ScriptTaskConfigObject' in unicode(c):
                return c
        except:
            pass
        r = _export_find_task_config(c, depth + 1)
        if r:
            return r
    return None

_tm_out = {}
try:
    _task_cfg_node = _export_find_task_config(proj)
    if _task_cfg_node:
        for _tc in (list(_task_cfg_node.get_children()) if _task_cfg_node.get_children() else []):
            try:
                _tc_name = _tc.get_name()
                if u'ScriptTaskObject' not in unicode(_tc):
                    continue
            except:
                continue
            _tc_entry = {}
            try:
                _tc_pous = _tc.pous
                _tc_entry[u'pous'] = [unicode(x).strip() for x in list(_tc_pous)]
            except:
                _tc_entry[u'pous'] = []
            try:
                _tc_interval = _tc.interval
                if _tc_interval is not None:
                    _tc_entry[u'interval'] = unicode(_tc_interval).strip()
            except:
                pass
            _tm_out[_tc_name] = _tc_entry
            log(u'  Task: {} -> [{}]'.format(_tc_name, u', '.join(_tc_entry.get(u'pous', []))))

    _tm_path = os.path.join(_ws_dir, u'task_mounts.json')
    _tm_json = json.dumps(_tm_out, ensure_ascii=False, indent=2)
    if isinstance(_tm_json, unicode):
        _tm_json = _tm_json.encode('utf-8')
    with open(_tm_path, 'wb') as _tmf:
        _tmf.write(_tm_json)
    log(u'task_mounts.json written ({} tasks)'.format(len(_tm_out)))
except Exception as _tme:
    log(u'[WARN] could not write task_mounts.json: ' + unicode(_tme))

log('=== export_pou.py done ===')
