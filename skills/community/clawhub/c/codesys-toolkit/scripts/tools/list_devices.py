# -*- coding: utf-8 -*-
"""
InoProShop Device Repository Lister
自动枚举所有可用控制器型号并缓存到文件

路径策略（无硬编码）：
  优先读取 run_script.ps1 注入的环境变量 INOPRO_SKILL_DIR，
  fallback 到 env_setup.ps1 写入的 %TEMP%\codesys_skill_dir.txt 信箱文件。
  %TEMP% 是系统级变量，在任何 Windows 用户环境下都有效。
"""
import time
import codecs
import os

# ---------------------------------------------------------------
# 读取 skill_dir（优先使用 run_script.ps1 注入的环境变量，
# fallback 到 env_setup.ps1 预先写入的临时信箱文件）
# ---------------------------------------------------------------
SKILL_DIR = os.environ.get('INOPRO_SKILL_DIR', '').strip()

if not SKILL_DIR:
    MAILBOX = os.path.join(os.environ.get('TEMP', 'C:\\Windows\\Temp'),
                           'codesys_skill_dir.txt')
    if not os.path.isfile(MAILBOX):
        system.write_message(Severity.Information, "[DeviceLister] ERROR: INOPRO_SKILL_DIR not set and mailbox not found: " + MAILBOX)
        system.exit()

    with open(MAILBOX, 'rb') as _f:
        _raw = _f.read().strip()
    if _raw.startswith(b'\xef\xbb\xbf'):
        _raw = _raw[3:]
    SKILL_DIR = _raw.decode('utf-8').strip()

# ---------------------------------------------------------------
# 日志文件：从 env.json 读 workspace_dir，与 run_script.ps1 路径推导保持一致
# run_script.ps1 会去 workspace_dir/log/<script_name>_log.txt 监视
# ---------------------------------------------------------------
_env_json_path = os.path.join(SKILL_DIR, u'references', u'env.json')
try:
    _env_raw = open(_env_json_path, u'rb').read()
    if _env_raw.startswith(b'\xef\xbb\xbf'):
        _env_raw = _env_raw[3:]
    import json as _json_mod
    _env_obj = _json_mod.loads(_env_raw.decode(u'utf-8'))
    _ws_dir_env = _env_obj.get(u'workspace_dir', u'').strip()
except Exception:
    _ws_dir_env = u''

if not _ws_dir_env:
    _ws_dir_env = os.path.join(SKILL_DIR, u'scripts', u'workspace')

_log_dir  = os.path.join(_ws_dir_env, u'log')
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

OUT_FILE = os.path.join(SKILL_DIR, 'references', 'device_list.txt')

log(u'=== list_devices.py start ===')
log(u'skill_dir : ' + SKILL_DIR)
log(u'out_file  : ' + OUT_FILE)
log(u'Starting device enumeration...')

try:
    all_devs = device_repository.get_all_devices()
    dev_list = list(all_devs)
    log(u'Found {} devices'.format(len(dev_list)))

    with codecs.open(OUT_FILE, 'w', 'utf-8') as f:
        f.write(u'InoProShop Device Repository - Total {} devices\n'.format(len(dev_list)))
        f.write(u'Generated: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        f.write(u'SkillDir: {}\n'.format(SKILL_DIR))
        f.write(u'=' * 120 + u'\n\n')
        f.write(u'{:<6} {:<35} {:<55}\n'.format(u'Index', u'Name', u'Description'))
        f.write(u'-' * 120 + u'\n')

        for i, dev in enumerate(dev_list):
            try:
                name = unicode(dev.device_info.name)        if hasattr(dev.device_info, 'name')        else u'N/A'
                desc = unicode(dev.device_info.description) if hasattr(dev.device_info, 'description') else u'N/A'
                f.write(u'{:<6} {:<35} {:<55}\n'.format(i, name[:35], desc[:55]))
            except Exception as e:
                f.write(u'{:<6} ERROR: {}\n'.format(i, unicode(e)))

        f.write(u'\n' + u'=' * 120 + u'\n')
        f.write(u'Total {} devices listed.\n'.format(len(dev_list)))

    log(u'Written to: ' + OUT_FILE)

except Exception as e:
    log(u'[ERROR] ' + unicode(e))
    try:
        with codecs.open(OUT_FILE, 'w', 'utf-8') as f:
            f.write(u'ERROR: {}\n'.format(unicode(e)))
    except Exception:
        pass

log(u'=== list_devices.py done ===')
