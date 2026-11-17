# -*- coding: utf-8 -*-
"""一键自检脚本：检查本技能在当前环境能否正常产出全部四类产物。

用法：
    python scripts/selfcheck.py            # 用内置示例数据做全流程自检
    python scripts/selfcheck.py <json>     # 用你自己的 design_data.json 做自检

自检内容：
  1. Python 版本与运行依赖（python-docx / python-pptx）；
  2. Word 模版能否正常解码读取；
  3. 参考资料（references/ 下 6 份）是否齐全、可读取、结构完整；
  4. 页脚说明文件是否存在且可读；
  5. design_data.json 的字段完整性（仅使用内置示例或你指定的文件）；
  6. 四类产物能否真正生成（写入系统临时目录，**不在你的工作目录留下任何残留**）。

退出码：0 = 全部通过；1 = 存在待修项。
"""
import json
import os
import subprocess
import sys
import tempfile

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.dirname(SCRIPTS)
sys.path.insert(0, SCRIPTS)

OK, FIX = [], []


def ok(msg):
    OK.append(msg)
    print("  ✓ %s" % msg)


def fix(msg):
    FIX.append(msg)
    print("  ✗ %s" % msg)


SAMPLE = {
    "basic_info": {
        "course_name": "数据结构（自检示例）",
        "major": "计算机科学与技术专业（本科）",
        "content": "树与二叉树",
        "section": "第三章，第一节、第二节",
        "hours": "本课程线上16学时，线下56学时；本课次线上1学时，线下3学时",
        "students": "40人",
    },
    "whole_course": {
        "design_idea": "围绕新工科人才培养定位，把价值塑造、知识传授与能力培养有机融合……（自检示例内容）",
        "innovation": "① 构建课程知识图谱支撑个性化学习路径；② 引入智能体辅助编程实践……（自检示例内容）",
        "effect": "以过程性与结果性数据共同证明教学效果……（自检示例内容）",
    },
    "single_lesson": {
        "learning_analysis": "学生已修完线性表，具备递归的程序设计基础……（自检示例内容）",
        "learning_goals": {
            "knowledge": "1. 定义二叉树、满二叉树、完全二叉树的基本概念（事实性知识）",
            "skill": "1. 运用递归思想编写二叉树的前序、中序、后序遍历算法（程序性知识）",
            "literacy": "1. 评判顺序存储与链式存储在不同数据规模下的适用性（程序性知识）",
            "ideology": "1. 在算法效率权衡中反思工程取舍与责任意识（元认知知识）",
        },
        "content_resources": "以超星学习通为主平台，辅以课程知识图谱……（自检示例内容）",
        "process_method": (
            "【课前·线上 1 学时】主平台/工具：超星学习通 + 课程知识图谱\n"
            "- 环节1.1 概念微课自学（约 20 分钟）\n"
            "  · 教师活动：在超星学习通发布微课并开启任务点防拖拽\n"
            "  · 学生活动：观看微课并在知识图谱标注已掌握/存疑\n"
            "  · 平台/工具：超星学习通微课 + 课程知识图谱\n"
            "  · 设计意图：概念性知识前移，释放课中探究时间\n"
            "【课中·线下 3 学时】\n"
            "- 环节2.1 情境导入（约 8 分钟）\n"
            "  · 教师活动：以文件系统目录树情境提问\n"
            "  · 学生活动：口头回答并自查前测错题\n"
            "  · 平台/工具：超星学习通数据看板\n"
            "  · 设计意图：以学定教\n"
            "【课后·线上】\n"
            "- 环节3.1 拓展任务（约 40 分钟）\n"
            "  · 教师活动：发布后测与拓展编程任务\n"
            "  · 学生活动：完成后测并提交代码\n"
            "  · 平台/工具：超星学习通\n"
            "  · 设计意图：检验综合应用能力"
        ),
        "evaluation": "采用过程性评价与结果性评价结合的方式……（自检示例内容）",
        "effect": "本课次目标达成度良好……（自检示例内容）",
    },
    "calendar": [
        {"seq": str(i), "date": "2026-09-%02d" % (i * 2 + 1), "week": "第%d周" % ((i - 1) // 2 + 1),
         "lecture": "第%d讲" % i, "minutes": "90",
         "location": "在线" if i % 2 else "教室", "students": "40",
         "content": "自检示例教学内容 %d" % i, "form": "线上" if i % 2 else "课堂",
         "activity": "观看微课、完成前测"}
        for i in range(1, 5)
    ],
}


def check_python():
    v = sys.version_info
    if v >= (3, 8):
        ok("Python 版本 %d.%d.%d（满足 ≥3.8）" % (v[0], v[1], v[2]))
    else:
        fix("Python 版本过低（%d.%d），请升级到 3.8 以上" % (v[0], v[1]))


def check_deps():
    missing = []
    for imp, pip_name in (("docx", "python-docx"), ("pptx", "python-pptx")):
        try:
            __import__(imp)
        except ImportError:
            missing.append(pip_name)
    if not missing:
        ok("运行依赖已就绪（python-docx / python-pptx）")
        return True
    fix("缺少依赖：%s" % "、".join(missing))
    print("    正在尝试自动安装……")
    try:
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "_bootstrap_deps.py")],
                           cwd=PKG_ROOT)
        if r.returncode == 0:
            ok("依赖已自动安装完成")
            return True
    except Exception as e:
        print("    安装失败：%s" % e)
    fix("依赖安装未成功；请联网后重跑，或让 AI 工具协助安装：%s" % " ".join(missing))
    return False


def check_template():
    try:
        from _common import open_template
        open_template("混合式教学设计方案模版.docx")
        open_template("混合式教学设计课程教学日历模版.docx")
        ok("两个 Word 模版均可正常解码读取")
        return True
    except Exception as e:
        fix("Word 模版读取失败：%s" % e)
        return False


def check_references():
    """校验 references/ 下参考资料是否齐全、可读取、结构完整。"""
    try:
        from _common import check_references as _check, REFERENCE_FILES
    except Exception as e:
        fix("参考资料校验不可用：%s" % e)
        return False
    bad = _check()
    if bad:
        for b in bad:
            fix("参考资料异常：%s" % b)
        return False
    ok("参考资料完整（references/ 下 %d 份均可读取）" % len(REFERENCE_FILES))
    try:
        import _refs
        good, msg = _refs.selftest()
    except Exception as e:
        fix("参考资料读取器不可用：%s" % e)
        return False
    if good:
        ok("参考资料读取器工作正常（%s）" % msg)
        return True
    fix("参考资料读取器自检失败：%s" % msg)
    return False


def check_footer():
    try:
        from _common import read_footer
        lines = read_footer()
        if lines and lines[0].strip():
            ok("页脚说明可读（%d 行）" % len(lines))
            return True
        fix("页脚说明内容为空：references/footer_note.json")
        return False
    except SystemExit:
        # read_footer 在文件缺失时会打印 E06 并 sys.exit(1)，此处按“待修”处理即可
        fix("页脚说明文件缺失或损坏：references/footer_note.json")
        return False
    except Exception as e:
        fix("页脚说明读取失败：%s" % e)
        return False


def check_data(json_path):
    try:
        with open(json_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        fix("数据文件读取失败：%s" % e)
        return None
    from _common import validate_json
    errors, warnings = validate_json(data)
    if errors:
        for e in errors:
            fix("数据缺失：%s" % e)
    if warnings:
        for w in warnings:
            print("    ! 建议改进：%s" % w)
    if not errors and not warnings:
        ok("数据字段完整，未发现明显问题")
    return data


def check_generate(json_path):
    """在系统临时目录做真实生成，退出时自动清理、不留残留。"""
    expected = [
        ("fill_design_plan.py", "混合式教学设计方案.docx"),
        ("fill_calendar.py", "混合式教学教学日历.docx"),
        ("gen_html_courseware.py", "混合式教学设计说课课件.html"),
        ("gen_ppt.py", "混合式教学设计说课.pptx"),
    ]
    with tempfile.TemporaryDirectory(prefix="blend_selfcheck_") as tmp:
        for script, filename in expected:
            try:
                r = subprocess.run(
                    [sys.executable, os.path.join(SCRIPTS, script), json_path, tmp],
                    cwd=PKG_ROOT, capture_output=True, text=True, encoding="utf-8",
                    errors="ignore")
            except Exception as e:
                fix("%s 无法启动：%s" % (script, e))
                continue
            path = os.path.join(tmp, filename)
            if r.returncode == 0 and os.path.isfile(path) and os.path.getsize(path) > 0:
                ok("可生成 %s（%.1f KB）" % (filename, os.path.getsize(path) / 1024.0))
            else:
                tail = (r.stdout or "")[-300:] + (r.stderr or "")[-300:]
                fix("未能生成 %s" % filename)
                if tail.strip():
                    print("    输出末尾：%s" % tail.strip().replace("\n", " | "))
    return True


def main():
    print("=" * 58)
    print("混合式教学设计技能 · 环境与产物自检")
    print("=" * 58)

    print("\n[1/7] Python 运行环境")
    check_python()

    print("\n[2/7] 运行依赖")
    deps_ok = check_deps()

    print("\n[3/7] Word 模版")
    tpl_ok = check_template()

    print("\n[4/7] 参考资料（references/）")
    check_references()

    print("\n[5/7] 页脚说明文件")
    check_footer()

    print("\n[6/7] 数据文件字段")
    user_json = sys.argv[1] if len(sys.argv) > 1 else None
    # 示例数据与生成测试共用同一个临时目录，退出时自动清理、不留残留
    with tempfile.TemporaryDirectory(prefix="blend_sample_") as sample_dir:
        if user_json and os.path.isfile(user_json):
            json_path = user_json
            print("  使用你指定的数据文件：%s" % user_json)
            check_data(json_path)
        else:
            if user_json:
                print("  未找到 %s，改用内置示例数据。" % user_json)
            else:
                print("  未指定数据文件，使用内置示例数据（仅用于自检，不会写入你的目录）。")
            tmp_json = os.path.join(sample_dir, "design_data.json")
            with open(tmp_json, "w", encoding="utf-8") as f:
                json.dump(SAMPLE, f, ensure_ascii=False, indent=2)
            json_path = tmp_json
            check_data(json_path)

        print("\n[7/7] 真实生成四类产物（写入临时目录，不产生残留）")
        if deps_ok and tpl_ok:
            check_generate(json_path)
        else:
            fix("跳过生成测试（前置依赖或模版未就绪）")

    print("\n" + "=" * 58)
    print("自检结果：%d 项通过，%d 项待修。" % (len(OK), len(FIX)))
    if FIX:
        print("待修项：")
        for i, m in enumerate(FIX, 1):
            print("  %d) %s" % (i, m))
        print("\n处理建议：")
        print("  · 依赖问题：联网后重跑本脚本，或让 WorkBuddy 协助安装 python-docx python-pptx")
        print("  · 数据问题：按提示补齐 design_data.json 对应栏目后重跑")
        print("  · 模版问题：重新解压技能包，勿修改 assets/templates/ 下的文件")
        print("  · 参考资料问题：重新解压技能包，勿修改 references/ 下的文件")
        print("  · 读取参考资料报错：先运行 python scripts/ref_reader.py 列出可用名称，再照抄名称重试")
        print("  · 仍无法解决：把以上完整输出发送给 WorkBuddy，由其协助定位")
        return 1
    print("全部通过，可正常生成产物。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
