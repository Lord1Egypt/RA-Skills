#!/usr/bin/env python3
"""
职业规划报告生成器（2026-09-08 T09 安全加固；2026-10-26 ClawHub 复审加固；
2026-11-10 ClawHub 安全整改：导出根收敛到 ./exports/ 之内）

变更要点：
  1. --output-dir 必须位于 ./exports/ 之内（唯一允许根 DEFAULT_EXPORT_ROOT）。
     环境变量 AIERA_EXPORT_ROOT **不再能扩展到任意路径**：它只能追加
     ./exports/ **之内**的子目录；相对路径、根目录 `/`、家目录、绝对路径逃逸
     一律丢弃并记日志（2026-11-10 整改，消 SDI-3「env 扩展写边界」）。
  2. **符号链接检查顺序修正（2026-10-26）**：先对**未解析**的原始路径逐级做
     os.path.islink() 检查（命中即拒绝），再 realpath + commonpath 包含性校验。
     旧实现先 resolve() 再查 is_symlink()——resolve() 已经跟随了符号链接，导致
     检查永远为 False、形同虚设。现实现对终端 symlink 与父目录链任一级 symlink
     均拒绝。
  3. 使用独占创建模式（O_CREAT|O_EXCL），同一天多次导出生成 collision-resistant
     文件名而非覆盖旧文件——保证不静默覆盖已有导出。
  4. 拒绝绝对路径越界、相对路径穿越（..）、NUL 字节等异常输入。
  5. 显式以 0600 权限写入（仅宿主用户可读写）；导出目录以 0700 创建。

调用方式：
  python3 scripts/report_generator.py --data '<json>' --output-dir ./exports
  python3 scripts/report_generator.py --data '<json>'   # 默认输出到 SKILL_DIR/exports/
"""
import json
import os
import secrets
import sys
from datetime import datetime
from pathlib import Path

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(THIS_DIR)
DEFAULT_EXPORT_ROOT = os.path.join(SKILL_DIR, "exports")
# 🆕 2026-11-10 整改：环境变量语义收窄 —— 只能追加 ./exports/ 之内的子目录，
# 不再是「任意允许根」。名字保留是为了兼容外部调用方（环境变量名不变）。
EXPORT_ROOT_SUBDIR_ENV = "AIERA_EXPORT_ROOT"


def _warn(msg):
    """只读告警：写到 stderr（stdout 保留给 JSON 输出）。"""
    print(f"[report_generator] WARNING: {msg}", file=sys.stderr)


def _load_allowed_roots():
    """读取允许的导出根目录集合。

    返回 dict：{字面路径(abspath, 未解析 symlink): 真实路径(realpath)}。

    2026-11-10 整改（ClawHub SDI-3 / TP4）：**允许根集合 = {DEFAULT_EXPORT_ROOT}**
    （= SKILL_DIR/exports/）。环境变量 AIERA_EXPORT_ROOT 不再能扩展写边界，
    只能追加 ./exports/ **之内**的子目录；候选路径必须同时满足：
      1) 是绝对路径（相对路径一律丢弃）；
      2) 字面路径位于 DEFAULT_EXPORT_ROOT 之内；
      3) 解析符号链接后的真实路径仍位于 DEFAULT_EXPORT_ROOT 的真实路径之内；
      4) 候选自身不是符号链接，且 DEFAULT_EXPORT_ROOT 自身也不是符号链接。
    不满足者**丢弃并记日志**（根目录 `/`、家目录、任何绝对路径逃逸均被丢弃）。

    2026-10-27 加固（保留）：**允许根自身是符号链接时，该根被直接剔除**——
    它不再能授权任何写入。旧实现把允许根的「字面路径」当作豁免锚点，
    允许根本身是 symlink 时检查被跳过，文件可写到允许根之外。
    """
    allowed = {}

    default_literal = os.path.abspath(DEFAULT_EXPORT_ROOT)
    # 默认根自身是 symlink → 不可用于授权（连同下面的 env 候选一并作废：
    # 否则 `<exports>/sub` 会把 realpath 解析到 skill 目录之外）。
    default_trustworthy = not os.path.islink(default_literal)
    if default_trustworthy:
        allowed[default_literal] = os.path.realpath(default_literal)
    else:
        _warn(f"default export root is a symlink, not usable as an allowed root: {default_literal}")

    env_val = os.environ.get(EXPORT_ROOT_SUBDIR_ENV, "").strip()
    if env_val:
        for p in env_val.split(":"):
            p = p.strip()
            if not p:
                continue
            if not default_trustworthy:
                _warn(f"{EXPORT_ROOT_SUBDIR_ENV} ignored: default export root is a symlink")
                break
            if not os.path.isabs(p):
                _warn(f"{EXPORT_ROOT_SUBDIR_ENV} ignored (not an absolute path): {p}")
                continue
            literal = os.path.abspath(p)
            if not _is_within(literal, default_literal):
                _warn(f"{EXPORT_ROOT_SUBDIR_ENV} ignored (outside {DEFAULT_EXPORT_ROOT}): {p}")
                continue
            if os.path.islink(literal):
                _warn(f"{EXPORT_ROOT_SUBDIR_ENV} ignored (path is a symlink): {p}")
                continue
            real = os.path.realpath(literal)
            if not _is_within(real, allowed[default_literal]):
                _warn(f"{EXPORT_ROOT_SUBDIR_ENV} ignored (resolves outside the export root): {p}")
                continue
            allowed[literal] = real
    return allowed


def _is_within(child, parent):
    """child 是否位于 parent 之内（含 parent 自身）。两者都应为绝对路径。"""
    try:
        return os.path.commonpath([child, parent]) == parent
    except ValueError:
        # 不同盘符（Windows）或混合路径：不视为包含关系。
        return False


def _iter_levels(path):
    """从叶子逐级向上产出 path 的各级目录（含 path 自身，直到根）。"""
    current = path
    while True:
        yield current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent


def _pick_anchor(literal_path, allowed_roots):
    """挑选可作为「豁免边界」的允许根**字面路径**（最长匹配）。

    2026-10-27 加固（收窄豁免范围）：
      - 锚点**本身这一级照样做 symlink 检查**（旧实现把锚点当成豁免起点，
        允许根本身是 symlink 时整条链被跳过 → 可写出允许根之外）；
      - 只有锚点**之上**的宿主系统级路径前缀才豁免（例如 macOS 的
        /tmp -> /private/tmp），这一段的 realpath 必然落在允许根的
        realpath 之内，由后续 commonpath 包含性校验兜底。
    若 literal_path 不在任何允许根之下，则返回 None —— 整条链都要检查。
    """
    best = None
    for literal_root in allowed_roots:
        if _is_within(literal_path, literal_root):
            if best is None or len(literal_root) > len(best):
                best = literal_root
    return best


def _validate_output_dir(output_dir_arg, allowed_roots):
    """验证 --output-dir 在允许根（默认 ./exports/）之内；拒绝越界/符号链接/穿越。

    顺序（2026-10-26 加固）：
      a) 参数类型 / NUL 字节 / ".." 穿越检查
      b) **未解析**原始路径的终端 symlink + 逐级 symlink 检查
      c) realpath 规范化 + commonpath 包含性校验
    """
    if not output_dir_arg or not isinstance(output_dir_arg, str):
        raise ValueError("output-dir must be a non-empty string")
    if "\x00" in output_dir_arg:
        raise ValueError("output-dir contains NUL byte")
    if ".." in Path(output_dir_arg).parts:
        raise ValueError("output-dir must not contain '..' path traversal")

    # 归一化为绝对路径，但**不** resolve()——resolve 会跟随符号链接，
    # 导致随后的 islink() 检查永远为 False。
    literal = os.path.abspath(output_dir_arg)

    # 终端 symlink（--output-dir 本身就是软链）直接拒绝
    if os.path.islink(literal):
        raise ValueError(f"output-dir path traverses a symlink: {literal}")

    # 逐级 symlink 检查：从 literal 向上逐级检查，锚点（允许根字面路径）
    # **本身这一级也要检查**；只有锚点之上的系统级前缀豁免。
    anchor = _pick_anchor(literal, allowed_roots)
    for level in _iter_levels(literal):
        if os.path.islink(level):
            raise ValueError(f"output-dir path traverses a symlink: {level}")
        if anchor is not None and level == anchor:
            break

    # 真实路径包含性校验（防止越界写入授权根之外的位置）
    real = os.path.realpath(literal)
    for real_root in allowed_roots.values():
        if _is_within(real, real_root):
            return Path(real)
    raise ValueError(
        f"output-dir is not inside any allowed export root. "
        f"Requested (resolved): {real}; allowed: {sorted(allowed_roots.values())}"
    )


def _generate_collision_resistant_name(date_str):
    """collision-resistant 文件名：职业规划报告_YYYYMMDD_HHMMSS_<8hex>.md
    同一秒多次导出也基本不会冲突；不再使用固定文件名避免覆盖。"""
    time_str = datetime.now().strftime("%H%M%S")
    suffix = secrets.token_hex(4)  # 8 hex chars = 32 bits entropy
    return f"职业规划报告_{date_str}_{time_str}_{suffix}.md"


def build_recs(recs):
    lines = []
    star = chr(9733)
    for i, r in enumerate(recs, 1):
        lines.append("### {0}. 【{1}】 适合指数：{2}".format(
            i, r.get('title', '方向' + str(i)), star * r.get('score', 3)))
        for k, v in [('推荐理由', r.get('reason', '')),
                      ('AI评级', r.get('ai_rating', '')),
                      ('薪资参考', r.get('salary', '')),
                      ('入门路径', r.get('path', '')),
                      ('3年预期', r.get('expectation', '')),
                      ('潜在风险', r.get('risk', ''))]:
            if v:
                lines.append("- **{0}**：{1}".format(k, v))
        lines.append('')
    return '\n'.join(lines)


def generate_report(data):
    today = datetime.now().strftime('%Y-%m-%d')
    ai = data.get('ai_guide', {})
    acts = data.get('actions', {})
    recs_md = build_recs(data.get('recommendations', []))
    md = [
        '# 个性化职业规划报告',
        '',
        '> 生成日期：' + today,
        '',
        '---',
        '',
        '## 基础档案',
        '',
        '- 昵称：' + data.get('nickname', '未提供'),
        '- 当前阶段：' + data.get('stage', '未提供'),
        '- 霍兰德代码：' + data.get('holland', '未测评'),
        '- MBTI类型：' + data.get('mbti', '未测评'),
        '- 职业锚：' + data.get('anchor', '未测评'),
        '- 核心价值观：' + data.get('values', '未明确'),
        '- 城市：' + data.get('city', '未提供'),
        '',
        '---',
        '',
        '## 职业方向推荐',
        '',
        recs_md,
        '',
        '## AI时代生存指南',
        '',
        '- 核心技能：' + ai.get('skills', '详见推荐职业'),
        '- 必学AI工具：' + ai.get('tools', '暂无'),
        '- 建议认证：' + ai.get('cert', '暂无'),
        '',
        '## 下一步行动清单',
        '',
        '- 今天：' + acts.get('today', '暂无'),
        '- 1个月内：' + acts.get('1month', '暂无'),
        '- 3个月内：' + acts.get('3months', '暂无'),
        '- 1年内：' + acts.get('1year', '暂无'),
        '',
        '---',
        '',
        '由 AI时代职业规划师 生成'
    ]
    return '\n'.join(md)


def _self_check():
    """只读自检：验证内部路径校验行为，**不写任何文件**。

    用途：让测试用外部进程触发内部校验逻辑（尤其是含 NUL 字节的路径 ——
    NUL 无法通过 argv 传递），而不必动态加载本模块。
    输出 JSON 报告到 stdout；exit 0 表示全部通过。
    """
    checks = {}
    allowed = _load_allowed_roots()

    # 1. NUL 字节路径必须被拒绝
    nul_path = os.path.join(os.sep, "a\x00b")
    try:
        _validate_output_dir(nul_path, allowed)
        checks["nul_rejected"] = False
    except ValueError as e:
        checks["nul_rejected"] = "NUL" in str(e)
        checks["nul_message"] = str(e)
    except Exception as e:  # noqa: BLE001
        checks["nul_rejected"] = False
        checks["nul_message"] = f"{type(e).__name__}: {e}"

    # 2. '..' 穿越必须被拒绝
    try:
        _validate_output_dir(os.path.join(DEFAULT_EXPORT_ROOT, "..", "..", "etc"), allowed)
        checks["traversal_rejected"] = False
    except ValueError as e:
        checks["traversal_rejected"] = "traversal" in str(e)
        checks["traversal_message"] = str(e)
    except Exception as e:  # noqa: BLE001
        checks["traversal_rejected"] = False
        checks["traversal_message"] = f"{type(e).__name__}: {e}"

    # 3. 默认导出根必须位于允许根之内
    checks["default_root_allowed"] = os.path.realpath(DEFAULT_EXPORT_ROOT) in [
        os.path.realpath(p) for p in allowed.values()
    ]

    ok = all(v is True for v in checks.values() if isinstance(v, bool))
    checks["all_passed"] = ok
    print(json.dumps(checks, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='{}')
    p.add_argument('--output-dir', default=DEFAULT_EXPORT_ROOT,
                   help='报告输出目录；必须位于允许根 ./exports/ 之内（默认 ./exports/）；'
                        'AIERA_EXPORT_ROOT 只能追加 ./exports/ 之内的子目录')
    p.add_argument('--print-default-export-root', action='store_true',
                   help='只读查询：打印默认导出根目录后退出，不生成任何文件')
    p.add_argument('--self-check', action='store_true',
                   help='只读自检：运行内部路径校验用例并输出 JSON 报告，不生成任何文件')
    args = p.parse_args()

    # 🆕 2026-10-28：只读自省参数。
    # 用途：让测试用外部进程查询 DEFAULT_EXPORT_ROOT 常量、
    # 以及触发内部校验逻辑（NUL 字节路径无法通过 argv 传递），
    # 而不必动态加载本模块（动态执行会被安全扫描器判为
    # suspicious.dynamic_code_execution / critical）。
    # 这些分支在 --data 解析与任何目录创建之前返回：纯查询、零副作用。
    if args.print_default_export_root:
        print(DEFAULT_EXPORT_ROOT)
        sys.exit(0)
    if args.self_check:
        sys.exit(_self_check())

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"[ERROR] --data 不是合法 JSON: {e}", file=sys.stderr)
        sys.exit(2)

    allowed = _load_allowed_roots()
    try:
        safe_dir = _validate_output_dir(args.output_dir, allowed)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(3)

    os.makedirs(str(safe_dir), mode=0o700, exist_ok=True)

    md = generate_report(data)
    date_str = datetime.now().strftime('%Y%m%d')
    filename = _generate_collision_resistant_name(date_str)
    target = safe_dir / filename

    # Exclusive creation: refuse to overwrite an existing file
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        fd = os.open(str(target), flags, 0o600)
    except FileExistsError:
        # 极小概率：随机冲突；再生成一次
        filename = _generate_collision_resistant_name(date_str)
        target = safe_dir / filename
        fd = os.open(str(target), flags, 0o600)

    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(md)
    except Exception:
        # 如果写失败，清理半成品文件
        try:
            os.unlink(str(target))
        except OSError:
            pass
        raise

    print('Markdown: ' + str(target))
