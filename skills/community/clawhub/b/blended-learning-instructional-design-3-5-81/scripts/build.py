# -*- coding: utf-8 -*-
"""一键编排脚本：按用户选择的产物类型依次调用各独立脚本。

用法：
    python build.py <design_data.json> [输出目录] [--html] [--ppt]

- 默认：生成《混合式教学设计方案.docx》《混合式教学教学日历.docx》
- --html：再生成《混合式教学设计说课课件.html》（交互式）
- --ppt ：再生成《混合式教学设计说课.pptx》（16 页）

特性：
  * 生成前做环境与数据自检（依赖、输出目录可写、必需字段、模版可读）；
  * 每个步骤失败后自动重试 1 次（可越过临时的依赖安装/文件占用问题）；
  * 结束时输出结构化的"成功 / 失败 / 修复建议"清单。

输出目录缺省时与 design_data.json 同目录。
"""
import argparse
import json
import os
import subprocess
import sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS)

MAX_RETRY = 1  # 首次 + 最多重试次数

# 步骤 -> (脚本, 产物文件名, 依赖的开关)
STEPS = {
    "plan": ("fill_design_plan.py", "混合式教学设计方案.docx", None),
    "calendar": ("fill_calendar.py", "混合式教学教学日历.docx", None),
    "html": ("gen_html_courseware.py", "混合式教学设计说课课件.html", "--html"),
    "ppt": ("gen_ppt.py", "混合式教学设计说课.pptx", "--ppt"),
}


def hr(char="="):
    print(char * 58)


def run_once(script, *args):
    """执行一个子脚本，返回返回码。末尾附加 --from-build 标记让子脚本自检转静默（build 已统一校验）。"""
    cmd = [sys.executable, os.path.join(SCRIPTS, script)] + list(args) + ["--from-build"]
    print("\n>> 运行：%s" % " ".join(os.path.basename(str(c)) for c in cmd))
    return subprocess.run(cmd).returncode


def run_with_retry(script, *args):
    """执行子脚本；失败自动重试 MAX_RETRY 次。返回 (是否成功, 实际尝试次数)。"""
    attempts = 0
    for i in range(MAX_RETRY + 1):
        attempts = i + 1
        try:
            if run_once(script, *args) == 0:
                return True, attempts
        except Exception as e:  # 子进程无法启动等极端情况
            print("  !! 无法启动 %s：%s" % (script, e))
        if i < MAX_RETRY:
            print("  … 步骤 %s 未成功，正在自动重试（第 %d 次）……" % (script, i + 1))
    return False, attempts


def preflight(json_path, out_dir):
    """生成前自检：依赖、输出目录、数据字段。返回 (是否可继续, 提示列表)。"""
    notes = []
    blocking = False

    # 1) 依赖
    try:
        import docx  # noqa: F401
        import pptx  # noqa: F401
        notes.append(("ok", "运行依赖已就绪（python-docx / python-pptx）"))
    except ImportError:
        notes.append(("fix", "运行依赖缺失，正在尝试自动安装……"))
        try:
            r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "_bootstrap_deps.py")],
                               cwd=os.path.dirname(SCRIPTS))
            if r.returncode == 0:
                notes.append(("ok", "依赖已自动安装完成"))
            else:
                notes.append(("fix", "依赖安装未成功：请联网后重跑，或让 AI 工具协助安装 "
                                     "python-docx python-pptx"))
                blocking = True
        except Exception as e:
            notes.append(("fix", "依赖安装失败：%s" % e))
            blocking = True

    # 2) 输入文件存在
    if not os.path.isfile(json_path):
        notes.append(("fix", "【E01】找不到数据文件 %s ；请让 AI 重新写出 design_data.json" % json_path))
        blocking = True
    else:
        notes.append(("ok", "已找到数据文件：%s" % json_path))

    # 2b) JSON 合法性与字段完整性（在此统一校验一次，子脚本不再重复）
    if not blocking:
        try:
            with open(json_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            notes.append(("ok", "数据文件为合法 JSON"))
        except json.JSONDecodeError as e:
            notes.append(("fix", "【E02】数据文件不是有效的 JSON（%s）；常见于多余逗号、中文引号或"
                                 "单引号，请让 AI 用英文双引号重新生成" % e))
            blocking = True
            data = None
        except UnicodeDecodeError:
            notes.append(("fix", "【E03】数据文件编码不是 UTF-8；请让 AI 以 UTF-8 重新写出"))
            blocking = True
            data = None
        except Exception as e:
            notes.append(("fix", "【E01】数据文件读取失败：%s" % e))
            blocking = True
            data = None
        if data is not None:
            try:
                from _common import validate_json
                errors, warnings = validate_json(data)
                if errors:
                    notes.append(("warn", "数据自检发现 %d 处必需内容缺失（缺失栏目将保持模版原样）：" % len(errors)))
                    for e in errors:
                        notes.append(("warn", "%s" % e))
                if warnings:
                    notes.append(("warn", "数据自检有 %d 处建议改进：" % len(warnings)))
                    for w in warnings:
                        notes.append(("warn", "%s" % w))
                if not errors and not warnings:
                    notes.append(("ok", "数据字段完整，未发现明显问题"))
            except Exception as e:
                notes.append(("warn", "字段自检跳过（%s）" % e))

    # 3) 输出目录可写（在目标目录内建一个临时子目录试探，退出时自动清理）
    try:
        os.makedirs(out_dir, exist_ok=True)
        import tempfile
        with tempfile.TemporaryDirectory(prefix="blend_probe_", dir=out_dir):
            pass
        notes.append(("ok", "输出目录可写：%s" % out_dir))
    except Exception as e:
        notes.append(("fix", "【E04】输出目录不可写：%s（%s）；请更换输出目录或关闭占用的文件" % (out_dir, e)))
        blocking = True

    # 4) 模版可读
    try:
        from _common import open_template
        open_template("混合式教学设计方案模版.docx")
        notes.append(("ok", "Word 模版可正常读取"))
    except Exception as e:
        notes.append(("fix", "【E05】Word 模版读取失败：%s ；请重新解压技能包，"
                             "不要改动 assets/templates/templates.json" % e))

    # 5) 页脚说明文件可读（references/footer_note.json）
    try:
        from _common import read_footer
        n = len([ln for ln in read_footer() if ln.strip()])
        notes.append(("ok", "页脚说明文件可读：references/footer_note.json（%d 行）" % n))
    except SystemExit:
        notes.append(("fix", "【E06】缺少或损坏 references/footer_note.json；请重新解压技能包"))
        blocking = True
    except Exception as e:
        notes.append(("fix", "【E06】页脚说明文件读取失败：%s" % e))
        blocking = True

    # 6) 参考资料完整性（references/*.json 均可读取）
    try:
        from _common import check_references
        bad = check_references()
        if bad:
            notes.append(("fix", "【E08】参考资料缺失或损坏：%s ；请重新解压技能包"
                          % "、".join(bad)))
            blocking = True
        else:
            notes.append(("ok", "参考资料完整（references/ 下 6 份均可读取）"))
    except Exception as e:
        notes.append(("warn", "参考资料完整性检查跳过（%s）" % e))

    return (not blocking), notes


def main():
    ap = argparse.ArgumentParser(description="混合式教学设计产物生成")
    ap.add_argument("json", help="design_data.json 路径")
    ap.add_argument("out", nargs="?", default=None, help="输出目录（缺省与 json 同目录）")
    ap.add_argument("--html", action="store_true", help="同时生成 HTML 交互式说课课件")
    ap.add_argument("--ppt", action="store_true", help="同时生成说课 PPT")
    args = ap.parse_args()

    out = args.out or os.path.dirname(os.path.abspath(args.json))
    os.makedirs(out, exist_ok=True)

    hr()
    print("混合式教学设计 · 产物生成")
    hr()

    # ---------- 阶段 1：前置自检 ----------
    print("\n[1/2] 生成前自检")
    ok, notes = preflight(args.json, out)
    mark = {"ok": "✓", "fix": "✗", "warn": "!"}
    for level, msg in notes:
        print("  %s %s" % (mark.get(level, "·"), msg))
    if not ok:
        hr()
        print("自检未通过，已中止生成。请按上方 ✗ 提示处理后重跑。")
        print("提示：也可先运行 python scripts/selfcheck.py 做一次完整自检。")
        return 1

    # ---------- 阶段 2：依次生成 ----------
    wanted = ["plan", "calendar"]
    if args.html:
        wanted.append("html")
    if args.ppt:
        wanted.append("ppt")

    print("\n[2/2] 依次生成产物（失败会自动重试 %d 次）" % MAX_RETRY)
    results = {}
    for key in wanted:
        script, filename, _ = STEPS[key]
        success, attempts = run_with_retry(script, args.json, out)
        results[key] = (filename, success, attempts)

    # ---------- 汇总 ----------
    hr()
    ok_all = all(v[1] for v in results.values())
    if ok_all:
        print("全部产物已生成，请到输出目录查看：%s" % out)
    else:
        print("部分产物未生成，详见下方清单。")

    print("\n产物清单：")
    for key in wanted:
        filename, success, attempts = results[key]
        path = os.path.join(out, filename)
        exists = os.path.isfile(path) and os.path.getsize(path) > 0
        size = ("%.1f KB" % (os.path.getsize(path) / 1024.0)) if os.path.isfile(path) else "-"
        if success and exists:
            print("  ✓ %s（%s）%s" % (filename, size, "" if attempts == 1 else "· 重试后成功"))
        else:
            print("  ✗ %s（未生成）" % filename)

    if not ok_all:
        print("\n修复建议：")
        print("  1) 先在对话框输入「请继续完成」，多数中断可自动恢复；")
        print("  2) 关闭已打开的 Word/PPT 文件后重跑，避免文件占用；")
        print("  3) 运行 python scripts/selfcheck.py 定位环境问题；")
        print("  4) 仍不行，请把上方完整输出交给 WorkBuddy，由其协助安装依赖或修复。")
    else:
        print("\n提示：产物请在正式使用前由教师人工审查、修改。")
        print("      各产物版面结构与页序：python scripts/ref_reader.py output_preview")

    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
