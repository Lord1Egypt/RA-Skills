# -*- coding: utf-8 -*-
"""
编译结果探测脚本
用法: InoProShop.exe --Profile="..." /runscript="check_compile.py"
      目标工程路径从 env.json 的 check_target 字段读取

输出:
  log/check_compile_log.txt   — 完整编译消息
  log/check_compile_result.txt — 单行结果: OK / FAIL:<错误数>
"""
import os
import codecs
import time

# -- 路径推算: 优先读 run_script.ps1 注入的环境变量，fallback 到 __file__ 层级计算 ------
_skill_dir = os.environ.get('INOPRO_SKILL_DIR', '').strip()
if not _skill_dir:
    _skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -- 读 env.json 获取 workspace_dir -------------------------------------------
_env_json = os.path.join(_skill_dir, 'references', 'env.json')

def _read_env():
    raw = open(_env_json, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    import json
    return json.loads(raw.decode('utf-8'))

_env = _read_env()

_builtin_ws = os.path.join(_skill_dir, 'scripts', 'workspace')
_ws_dir     = _env.get('workspace_dir', '').strip()
if not _ws_dir:
    # workspace_dir 未设置时，将错误写到 builtin workspace 的 log 下，然后 fatal
    _err_early = os.path.join(_builtin_ws, 'log', 'check_compile_error.txt')
    try:
        if not os.path.exists(os.path.dirname(_err_early)):
            os.makedirs(os.path.dirname(_err_early))
        with open(_err_early, 'ab') as _fe:
            _fe.write(u'[FATAL] workspace_dir \u672a\u8bbe\u7f6e\uff0c\u8bf7\u5148\u5728 env.json \u4e2d\u5199\u5165 workspace_dir \u5b57\u6bb5\n'.encode('utf-8'))
    except:
        pass
    system.exit()
_log_dir    = os.path.join(_ws_dir, 'log')
if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)

_script_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
_log_file    = os.path.join(_log_dir, _script_name + u'_log.txt')
_result_file = os.path.join(_log_dir, u'check_compile_result.txt')
_err_file    = os.path.join(_log_dir, u'check_compile_error.txt')

_log_fh = codecs.open(_log_file, u'w', encoding=u'utf-8')

def log(msg):
    if isinstance(msg, bytes):
        msg = msg.decode(u'utf-8', u'replace')
    elif not isinstance(msg, unicode):
        msg = unicode(msg)
    line = u'[{}] {}'.format(time.strftime(u'%H:%M:%S'), msg)
    _log_fh.write(line + u'\n')
    _log_fh.flush()

def write_result(content):
    try:
        f = codecs.open(_result_file, 'w', encoding='utf-8')
        f.write(content + u'\n')
        f.close()
    except:
        pass

def write_err(msg):
    log(u'[ERROR] ' + msg)
    try:
        f = codecs.open(_err_file, 'w', encoding='utf-8')
        f.write(msg + u'\n')
        f.close()
    except:
        pass

def fatal(msg):
    write_err(msg)
    log(u'=== check_compile.py done ===')
    system.exit()

# ── 读 env.json ───────────────────────────────────────────────────────────────
# 目标工程路径：优先读 env.json 的 check_target，否则 fallback 到 template
TARGET = _env.get('check_target', '')
if not TARGET:
    fatal(u'env.json 缺少 check_target 字段，请设置要检测的 .project 路径')

if not os.path.exists(TARGET):
    fatal(u'目标工程不存在: ' + TARGET)

log(u'--- 编译探测开始 ---')
log(u'TARGET : ' + TARGET)

# ── 打开工程 ──────────────────────────────────────────────────────────────────
log(u'打开工程...')
try:
    proj = projects.open(TARGET)
except Exception as ex:
    fatal(u'projects.open() 异常: ' + unicode(ex))

if proj is None:
    fatal(u'projects.open() 返回 None，工程无法打开')

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
log(u'工程已打开 (waited {}s): {}'.format(_waited, str(proj)))

# ── 定位 IEC 容器，枚举项目结构（属性探测法，兼容外来工程）──────────────────
def find_iec_container(p):
    """优先找名为 Application 的 IEC 容器（AM600），fallback 到任意 IEC 容器（AM522/TT）。"""
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
            if 'ScriptIecLanguageObjectContainerObject' in unicode(c):
                return c
        for c in children:
            r = _find_any(c, depth + 1)
            if r: return r
        return None
    result = _find_app(p, 0)
    if result: return result
    return _find_any(p, 0)

def enumerate_iec(iec):
    pou_list = []
    gvl_list = []
    dut_list = []
    def _walk(node, prefix):
        try:
            children = node.get_children()
        except:
            return
        if not children:
            return
        for child in children:
            name = u'(unknown)'
            try:
                name = child.get_name()
            except:
                try:
                    name = child.get_name(False)
                except:
                    name = str(child)[:60]
            child_str = str(child)
            display   = (prefix + u'/' + name) if prefix else name
            has_decl = False
            has_impl = False
            try:
                td = child.textual_declaration
                has_decl = (td is not None)
            except:
                pass
            try:
                ti = child.textual_implementation
                has_impl = (ti is not None)
            except:
                pass
            if has_decl and has_impl:
                pou_list.append(display)
            elif has_decl and not has_impl:
                if 'Dut' in child_str or name.upper().startswith('DUT'):
                    dut_list.append(display)
                else:
                    gvl_list.append(display)
            else:
                _walk(child, display)
    _walk(iec, u'')
    return pou_list, gvl_list, dut_list

iec = find_iec_container(proj)
if iec:
    log(u'IEC 容器: ' + str(iec)[:80])
    pou_list, gvl_list, dut_list = enumerate_iec(iec)
    log(u'结构: POU={0}, GVL={1}, DUT={2}'.format(len(pou_list), len(gvl_list), len(dut_list)))
    for p in pou_list:
        log(u'  POU: ' + p)
    for g in gvl_list:
        log(u'  GVL: ' + g)
    for d in dut_list:
        log(u'  DUT: ' + d)
else:
    log(u'[WARN] 未找到 IEC 容器，跳过结构枚举')

# ── 查找编译命令 ──────────────────────────────────────────────────────────────
build_cmd = None
for cmd in system.commands:
    tokens = cmd.tokens
    if tokens is not None:
        tl = list(tokens)
        if 'project' in tl and 'buildactiveapp' in tl:
            build_cmd = cmd
            break

if build_cmd is None:
    fatal(u'未找到 buildactiveapp 命令')

# ── 清理旧编译消息，触发编译 ──────────────────────────────────────────────────
log(u'触发编译...')

# 先找编译消息分类，清除旧消息
cats = system.get_message_categories()
compile_cat = None
for c in cats:
    desc = system.get_message_category_description(c)
    if u'\u7f16\u8bd1' in desc or 'build' in desc.lower() or 'compil' in desc.lower():
        compile_cat = c
        break

if compile_cat:
    try:
        system.clear_messages(compile_cat)
    except:
        pass

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
                    try: _ms = unicode(_m)
                    except: _ms = str(_m).decode(u'utf-8', u'replace')
                    if u'\u7f16\u8bd1\u5b8c\u6210' in _ms or 'errors' in _ms.lower():
                        _build_done = True
                        break
            if _build_done:
                break
    except:
        pass
    if _build_done:
        break
log(u'编译等待完成 (waited {}s)，读取结果...'.format(_build_waited))

# ── 重新获取编译消息分类（编译后可能更新）────────────────────────────────────
cats = system.get_message_categories()
compile_cat = None
for c in cats:
    desc = system.get_message_category_description(c)
    if u'\u7f16\u8bd1' in desc or 'build' in desc.lower() or 'compil' in desc.lower():
        compile_cat = c
        break

if compile_cat is None:
    fatal(u'编译完成后仍未找到编译消息分类')

msgs = system.get_message_objects(compile_cat)

# ── 解析消息，统计错误/警告 ───────────────────────────────────────────────────
# 先打印所有消息，同时找汇总行
summary_line = u''
all_lines    = []
for m in msgs:
    try:    line = unicode(m)
    except: line = str(m).decode(u'utf-8', u'replace')
    log(u'  ' + line)
    all_lines.append(line)
    if u'\u7f16\u8bd1\u5b8c\u6210' in line or 'complete' in line.lower():
        summary_line = line

# 从汇总行提取错误/警告数（最可靠，不依赖具体错误行关键词）
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

# ── 写出结果 ──────────────────────────────────────────────────────────────────
log(u'')
log(u'--- 编译结果汇总 ---')
log(u'错误数: ' + str(n_err))
log(u'警告数: ' + str(n_warn))
if summary_line:
    log(u'摘要: ' + summary_line)

if n_err > 0:
    write_result(u'FAIL:' + str(n_err))
    log(u'=== CHECK RESULT: FAIL:{} ==='.format(n_err))
    try:
        f = codecs.open(_err_file, 'w', encoding='utf-8')
        f.write(u'编译失败，{} 个错误\n'.format(n_err))
        f.close()
    except:
        pass
else:
    write_result(u'OK:' + str(n_warn) + u' warnings')
    log(u'=== CHECK RESULT: OK:{} warnings ==='.format(n_warn))

log(u'=== 探测完成 ===')
log(u'结果文件: ' + _result_file)
log(u'=== check_compile.py done ===')
