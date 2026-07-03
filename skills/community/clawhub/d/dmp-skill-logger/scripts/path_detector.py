#!/usr/bin/env python3
"""
智能路径检测模块 v3
优化点：
1. 锚点文件机制 - 记住上次用的路径，避免每次重新猜
2. 写入优先续写已有历史文件 - 避免分散写入
3. 查询时扫描所有候选路径并合并 - 兜底保障
"""
import os
import sys
from pathlib import Path

# 锚点文件固定放在 home 目录（最稳定的位置）
ANCHOR_FILE = Path.home() / '.skill-logger' / '.anchor'

# 所有候选路径（按优先级排序）
def _get_candidate_bases():
    candidates = [
        str(Path.home()),
        os.getenv('PERSISTENT_DIR'),
        os.getenv('DATA_DIR'),
        os.getenv('WORKSPACE_DIR'),
        os.getenv('WORKSPACE_PATH'),
        os.getenv('WORK_DIR'),
        os.getcwd(),
        '/var/tmp',
        '/tmp',
    ]
    # 去掉 None，去重，保留顺序
    seen = set()
    result = []
    for p in candidates:
        if p and p not in seen:
            seen.add(p)
            result.append(p)
    return result


def _test_writable(path):
    """测试路径是否可写，返回 True/False"""
    try:
        os.makedirs(path, exist_ok=True)
        test_file = os.path.join(path, '.test_write')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except (PermissionError, OSError):
        return False


def get_task_history_path():
    """
    获取任务历史文件路径（写入用）
    优先级：
    1. 锚点文件记录的路径（上次用的，优先续写）
    2. 已存在历史文件的路径（续写已有数据）
    3. 第一个可写的候选路径（新建）
    """
    candidate_bases = _get_candidate_bases()

    # === 第一步：读锚点，优先用上次记录的路径 ===
    if ANCHOR_FILE.exists():
        try:
            anchored_path = ANCHOR_FILE.read_text().strip()
            anchored_dir = str(Path(anchored_path).parent)
            if _test_writable(anchored_dir):
                print(f"✅ 平台检测: {detect_platform()}", file=sys.stderr)
                print(f"✅ 使用锚点路径: {anchored_path}", file=sys.stderr)
                return anchored_path
            else:
                print(f"⚠️ 锚点路径不可写，重新检测: {anchored_path}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ 读取锚点失败: {e}", file=sys.stderr)

    # === 第二步：找已存在历史文件的路径（优先续写） ===
    for base_path in candidate_bases:
        history_file = os.path.join(base_path, '.skill-logger', 'task_history.json')
        if os.path.exists(history_file):
            history_dir = os.path.dirname(history_file)
            if _test_writable(history_dir):
                _save_anchor(history_file)
                print(f"✅ 平台检测: {detect_platform()}", file=sys.stderr)
                print(f"✅ 续写已有历史: {history_file}", file=sys.stderr)
                return history_file

    # === 第三步：找第一个可写路径，新建 ===
    for base_path in candidate_bases:
        history_dir = os.path.join(base_path, '.skill-logger')
        history_file = os.path.join(history_dir, 'task_history.json')
        if _test_writable(history_dir):
            _save_anchor(history_file)
            print(f"✅ 平台检测: {detect_platform()}", file=sys.stderr)
            print(f"✅ 新建存储路径: {history_file}", file=sys.stderr)
            return history_file

    raise RuntimeError(
        "无法找到可写入的存储路径。已尝试：\n" +
        "\n".join(f"  - {p}" for p in candidate_bases)
    )


def _save_anchor(history_file):
    """保存锚点文件，记录当前使用的历史文件路径"""
    try:
        ANCHOR_FILE.parent.mkdir(parents=True, exist_ok=True)
        ANCHOR_FILE.write_text(history_file)
    except Exception as e:
        print(f"⚠️ 保存锚点失败（不影响功能）: {e}", file=sys.stderr)


def get_all_history_files():
    """
    扫描所有候选路径，返回所有存在的历史文件路径列表
    用于查询时合并多路径数据
    """
    found = []
    seen = set()
    for base_path in _get_candidate_bases():
        history_file = os.path.join(base_path, '.skill-logger', 'task_history.json')
        real_path = os.path.realpath(history_file)  # 解析软链接，避免重复
        if os.path.exists(history_file) and real_path not in seen:
            seen.add(real_path)
            found.append(history_file)
    return found


def detect_platform():
    """检测当前运行的 AI 平台"""
    env_indicators = {
        'deepminer': ['DEEPMINER', 'DM_WORKSPACE', 'DEEPMINER_SESSION'],
        'openclaw': ['OPENCLAW', 'CLAW_WORKSPACE'],
        'coze': ['COZE', 'COZE_WORKSPACE', 'COZE_BOT_ID'],
    }
    for platform, env_vars in env_indicators.items():
        if any(var in os.environ for var in env_vars):
            return platform

    cwd = os.getcwd()
    if 'deepminer' in cwd.lower() or 'dm-agent' in cwd.lower():
        return 'deepminer'
    elif 'openclaw' in cwd.lower():
        return 'openclaw'
    elif 'coze' in cwd.lower():
        return 'coze'
    return 'unknown'


def get_platform_info():
    return {
        'platform': detect_platform(),
        'cwd': os.getcwd(),
        'home': str(Path.home()),
        'anchor_file': str(ANCHOR_FILE),
        'anchor_exists': ANCHOR_FILE.exists(),
        'anchor_content': ANCHOR_FILE.read_text().strip() if ANCHOR_FILE.exists() else None,
        'workspace_env': os.getenv('WORKSPACE_DIR') or os.getenv('WORKSPACE_PATH'),
        'python_version': sys.version,
    }


if __name__ == "__main__":
    print("=== 平台信息检测 ===")
    info = get_platform_info()
    for key, value in info.items():
        print(f"{key}: {value}")

    print("\n=== 所有历史文件 ===")
    files = get_all_history_files()
    if files:
        for f in files:
            print(f"  📄 {f}")
    else:
        print("  （暂无历史文件）")

    print("\n=== 写入路径检测 ===")
    try:
        path = get_task_history_path()
        print(f"✅ 检测成功: {path}")
    except RuntimeError as e:
        print(f"❌ 检测失败: {e}")
        sys.exit(1)
