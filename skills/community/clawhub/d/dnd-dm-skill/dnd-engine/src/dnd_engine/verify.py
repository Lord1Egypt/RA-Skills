"""
verify.py — 工作目录环境校验（纯函数，不依赖 API 服务）

用法:
    from dnd_engine.verify import verify_environment
    report = verify_environment()
"""

import os
import sys


def verify_environment(workspace=None):
    """校验工作目录完整性，返回详细报告字典
    
    检查项：
    - 14 个核心引用文件
    - rules/ 目录和模组文件
    - saves/ 写入权限
    - dnd-engine 安装状态
    - live_party.json
    """
    base = workspace or os.getcwd()
    
    # 1. 引用文件检查
    core_files = [
        'DM_RULES.md', 'DM_TEMPLATES.md', 'DM_MAP_SYS.md',
        'DM_DEV_GUIDE.md', 'CHAR_CREATION.md',
        'MODULE_ARC.md', 'MODULE_INDEX.md', 'ECHO_ARC.md',
        'SOUL.md', 'IDENTITY.md', 'AGENTS.md', 'TOOLS.md',
        'USER.md', 'party-sheet.html'
    ]
    
    # 检查 references/ 目录 + 根目录兜底
    check_locations = [
        os.path.join(base, 'references'),
        base
    ]
    
    ref_found = 0
    ref_missing = []
    for f in core_files:
        found = False
        for loc in check_locations:
            if os.path.exists(os.path.join(loc, f)):
                found = True
                break
        if found:
            ref_found += 1
        else:
            ref_missing.append(f)
    
    # 2. rules/ 和 modules/ 目录
    rules_dir = os.path.join(base, 'rules')
    rules_ready = os.path.exists(rules_dir)
    rules_files = 0
    if rules_ready:
        try:
            rules_files = len([x for x in os.listdir(rules_dir)
                               if x.endswith(('.md', '.pdf'))])
        except:
            pass
    
    modules_dir = os.path.join(base, 'modules')
    modules_ready = os.path.exists(modules_dir)
    modules_files = 0
    if modules_ready:
        try:
            modules_files = len([x for x in os.listdir(modules_dir)
                                 if x.endswith(('.md', '.pdf', '.json'))])
        except:
            pass
    
    # 3. saves/ 写入权限
    saves_dir = os.path.join(base, 'saves')
    writable = True
    try:
        os.makedirs(saves_dir, exist_ok=True)
        test_file = os.path.join(saves_dir, '.write_test')
        with open(test_file, 'w') as tf:
            tf.write('ok')
        os.remove(test_file)
    except:
        writable = False
    
    # 4. dnd-engine 安装状态
    engine_ok = True
    engine_version = ''
    try:
        from dnd_engine import __version__
        engine_version = __version__
    except ImportError:
        # Try local import
        engine_src = os.path.join(base, 'dnd-engine', 'src')
        if os.path.exists(engine_src):
            try:
                sys.path.insert(0, engine_src)
                from dnd_engine import __version__
                engine_version = __version__
            except:
                engine_ok = False
                engine_version = 'NOT_FOUND'
        else:
            engine_ok = False
            engine_version = 'NOT_FOUND'
    
    # 5. live_party.json
    live_party_exists = os.path.exists(os.path.join(base, 'live_party.json'))
    
    # 综合状态
    ref_status = 'OK' if len(ref_missing) == 0 else 'MISSING'
    all_ok = (ref_status == 'OK' and engine_ok and writable)
    
    # 建议操作
    actions = []
    if not rules_ready or rules_files == 0:
        actions.append('请将规则书放入 rules/ 目录。')
    if not modules_ready or modules_files == 0:
        actions.append('请将模组文件放入 modules/ 目录。')
    if not engine_ok:
        actions.append('dnd-engine 未找到，请确认 zip 解压完整。')
    
    return {
        'status': 'OK' if all_ok else 'WARN',
        'python': sys.version.split()[0],
        'engine': {
            'status': 'OK' if engine_ok else 'MISSING',
            'version': engine_version
        },
        'references': {
            'total': len(core_files),
            'found': ref_found,
            'missing': ref_missing,
            'status': ref_status
        },
        'rules': {
            'directory_exists': rules_ready,
            'files_found': rules_files
        },
        'modules': {
            'directory_exists': modules_ready,
            'files_found': modules_files
        },
        'saves_writable': writable,
        'live_party_exists': live_party_exists,
        'actions': actions
    }
