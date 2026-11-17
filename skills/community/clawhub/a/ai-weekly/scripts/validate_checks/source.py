# validate_checks/source.py — 源码静态守护（P0#19）
import re
from pathlib import Path

def _iter_source_files(source_dir: str):
    """收集待扫描的 Python 源文件（含 aiweekly 子包）。"""
    d = Path(source_dir)
    files = list(d.glob("*.py"))
    sub = d / "aiweekly"
    if sub.is_dir():
        files += list(sub.glob("*.py"))
    return sorted(set(files))


def check_no_bare_except(source_dir: str) -> dict:
    """P0#19 守护：源码不得出现「裸 except:」（会捕获 KeyboardInterrupt/SystemExit）。

    分级（与 generate_site.py 顶部注释一致）：
    - 裸 `except:` → 硬失败（明确反模式）；
    - `except Exception` 处理体含 print/log/raise/业务处理 → best-effort（允许，网络/解析层有意容错）；
    - `except Exception: pass/return None` 且属 EAFP 默认回退（后续行有 return/try/赋值）
      → best-effort（有意回退，如 load/parse 失败返回空/None）；
    - 其余静默兜底 → 记录为 silent_warn（可能掩盖真实错误，超阈值告警）。
    """
    SILENT_CEILING = 20
    errors, silent = [], []
    best_effort = 0
    cur_fn = ""
    for f in _iter_source_files(source_dir):
        lines = f.read_text(encoding="utf-8").splitlines()
        cur_fn = ""
        for i, ln in enumerate(lines):
            s = ln.strip()
            mdef = re.match(r'^(?:async\s+)?def\s+(\w+)', s)
            if mdef:
                cur_fn = mdef.group(1)
            if not s.startswith("except"):
                continue
            is_bare = (s == "except:" or bool(re.match(r'^except\s*:\s*(#.*)?$', s)))
            if is_bare:
                errors.append(f"{f.name}:{i+1} 裸 except:（会捕获 BaseException，含 Ctrl-C）")
                continue
            if "Exception" not in s:
                continue  # 收窄到具体类型的 except 不统计
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if any(k in nxt for k in ("print(", "logger.", "logging.", "warn", "raise ")):
                best_effort += 1
            elif nxt in ("return None", "return", "continue", "break"):
                best_effort += 1  # EAFP 默认回退
            elif nxt == "pass":
                ahead = [lines[j].strip() for j in (i + 2, i + 3) if j < len(lines)]
                if any(a.startswith(("return", "try", "except")) or "=" in a for a in ahead):
                    best_effort += 1  # 解析链 / 默认回退（pass 后接 return/try/赋值）
                else:
                    silent.append(f"{f.name}:{i+1}({cur_fn}) 静默兜底 pass")
            else:
                best_effort += 1
    ok = len(errors) == 0
    warn = len(silent) > SILENT_CEILING
    msg = (f"无裸 except ✅；best-effort 容错 {best_effort} 处，静默兜底 {len(silent)} 处"
           if ok else
           f"{len(errors)} 处裸 except 须修复：{'；'.join(e[:50] for e in errors[:3])}")
    if warn:
        msg += f" ⚠️ 静默兜底超阈值({SILENT_CEILING})"
    return {"ok": ok, "warn": warn, "hard_errors": errors, "silent_fallbacks": silent,
            "best_effort_count": best_effort, "msg": msg}


def check_iso8601(source_dir: str) -> dict:
    """P0#19 守护：注入 HTML 的时间戳须为 ISO 8601（isoformat），日期解析须支持 fromisoformat。

    - 真实代码调用 .strftime(...) 注入时间戳 → 失败（应为 datetime.now().isoformat()）；
      （用拼接构造正则，避免本函数源码中出现该连续字面量导致自匹配）
    - `[GEN_DATE]` 占位符未接 isoformat → 失败；
    - 定义 `_parse_date_arg` 的文件未含 fromisoformat → 失败（解析不支持 ISO 8601）。
    """
    # 拼接构造正则，避免本源码中出现该连续字面量导致自匹配
    pat = r'\.' + "strftime" + r'\(\s*["\']%Y-%m-%d %H:%M["\']\s*\)'
    problems = []
    for f in _iter_source_files(source_dir):
        src = f.read_text(encoding="utf-8")
        if re.search(pat, src):
            problems.append(f"{f.name}: 仍用 strftime('%Y-%m-%d %H:%M') 注入时间戳（应 isoformat）")
        for ln in src.splitlines():
            if "[GEN_DATE]" in ln and "isoformat" not in ln:
                problems.append(f"{f.name}: [GEN_DATE] 未接 isoformat")
        if "def _parse_date_arg" in src and "fromisoformat" not in src:
            problems.append(f"{f.name}: _parse_date_arg 未支持 ISO 8601 fromisoformat")
    ok = len(problems) == 0
    msg = ("日期均符合 ISO 8601（GEN_DATE 用 isoformat，解析支持 fromisoformat）✅"
           if ok else "；".join(problems[:4]))
    return {"ok": ok, "warn": False, "problems": problems, "msg": msg}


def check_module_size(source_dir: str, main_max: int = 500, mod_max: int = 800) -> dict:
    """P0#4 守护：屎山防线——单文件行数硬上限，防止拆分后再次膨胀成巨石。

    输入：
        source_dir — scripts/ 目录；扫描其自身与 aiweekly/ 子包的 .py。
        main_max   — `generate_site.py` 主入口上限（默认 500 行，P1#1 目标值）。
        mod_max    — 引擎子模块上限（默认 800 行）。
    输出：`{ok, warn, problems, msg, sizes}`；超限即 ok=False。
    异常：不抛（读不到的文件直接跳过）。
    示例：
        >>> check_module_size("scripts")["ok"]                    # doctest: +SKIP
        True

    作用域：仅约束「生成引擎」——`generate_site.py` 主入口 + `aiweekly/` 子包。
    顶层 dev/QA 脚本（validate_report.py / fetch_ai_news.py / deploy_report.py /
    tools/accumulate_data.py）是独立工具，仅记录行数、不参与 ≤800 上限判定。
    """
    # 顶层 dev/QA 脚本豁免（仅记录，不判定上限）
    # accumulate_data.py 已于 P2-L5 迁移至 tools/（独立辅助工具，不进入主生成流程），
    # 不再位于 scripts/ 下，故不会被本守护扫描；保留于 EXEMPT 仅作历史记录。
    _EXEMPT = {"validate_report.py", "fetch_ai_news.py", "deploy_report.py", "accumulate_data.py"}
    sizes, problems = {}, []
    for f in _iter_source_files(source_dir):
        if f.name.endswith((".bak", ".bak2")) or f.name == "__init__.py":
            continue
        try:
            n = len(f.read_text(encoding="utf-8").splitlines())
        except OSError:
            continue
        key = f"{f.parent.name}/{f.name}" if f.parent.name == "aiweekly" else f.name
        sizes[key] = n
        # 仅生成引擎（generate_site.py + aiweekly/*）参与上限判定
        is_engine = (f.parent.name == "aiweekly") or (f.name == "generate_site.py")
        limit = main_max if f.name == "generate_site.py" else mod_max
        if is_engine and n > limit:
            problems.append(f"{key}: {n} 行 > 上限 {limit}")
    ok = not problems
    biggest = max(sizes.items(), key=lambda kv: kv[1]) if sizes else ("-", 0)
    msg = (f"模块体量达标（{len(sizes)} 个文件，最大 {biggest[0]}={biggest[1]} 行，"
           f"主入口上限 {main_max} / 模块上限 {mod_max}）✅"
           if ok else "；".join(problems[:4]))
    return {"ok": ok, "warn": False, "problems": problems, "msg": msg, "sizes": sizes}
