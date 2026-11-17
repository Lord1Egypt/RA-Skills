#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""awam-todo 改造后的场景自测：在临时目录里跑，不碰真实 storage。

临时目录默认「通过即删、失败保留」；AWAM_TODO_KEEP_TMP=1/0 可强制保留 / 强制清理。
"""
import os
import shutil
import subprocess
import sys
import tempfile

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
PY = sys.executable


def run(tmp, *args, timeout=60, env=None):
    """跑一条 CLI 命令。带超时保护：卡住的一律当成失败，不让自测整体挂死。
    默认注入 AWAM_TODO_UI_PROMPT=off：自测里不弹「是否启动网页 UI」的对话框。"""
    e = dict(os.environ)
    e.setdefault("AWAM_TODO_UI_PROMPT", "off")
    if env:
        e.update(env)
    try:
        r = subprocess.run([PY, os.path.join(tmp, "scripts", "todo.py")] + list(args),
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, env=e)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except subprocess.TimeoutExpired:
        print("  FAIL  [超时 %ss] todo.py %s" % (timeout, " ".join(args)))
        return 124, "", "timeout after %ss" % timeout


def main():
    tmp = tempfile.mkdtemp(prefix="awamtodo-")
    shutil.copytree(SRC, os.path.join(tmp, "scripts"))
    os.makedirs(os.path.join(tmp, "storage"), exist_ok=True)
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        print(("  PASS  " if cond else "  FAIL  ") + name + (("  | " + extra) if extra and not cond else ""))
        if not cond:
            ok = False

    print("== 1. 新建带预案 + 过期截止 ==")
    rc, out, err = run(tmp, "add", "--text", "背完 2000 个单词", "--blocker", "晚上刷手机",
                       "--counter", "拿起手机前先背 20 个", "--due", "2026-09-20")
    print(out or err)
    check("add 成功", rc == 0)
    check("输出含障碍", "blocker: 晚上刷手机" in out)
    check("输出含对策", "counter: 拿起手机前先背 20 个" in out)
    check("输出含置顶理由(逾期)", "pinned: Overdue" in out)
    check("输出含两个出口", "advance now" in out and "reschedule" in out)
    check("预计完成日不编造", "projected finish: N/A" in out)

    print("== 2. 无截止任务：不得编造逾期/推算 ==")
    rc, out, err = run(tmp, "add", "--text", "整理归档策略", "--force")
    check("无截止不产出逾期天数", "overdue" not in out.lower())

    print("== 3. 时间解析失败要报错，不静默丢弃 ==")
    rc, out, err = run(tmp, "postpone", "T-", "乱七八糟的时间")
    rc2, out2, err2 = run(tmp, "add", "--text", "带坏时间的任务", "--due", "下个世纪的某天", "--force")
    check("坏时间有告警", "unrecognized time" in (err + err2), (err + err2)[:200])

    print("== 4. 调整计划 postpone ==")
    rc, out, err = run(tmp, "postpone", "T-20260920-001" if False else _first_id(tmp), "下周一")
    print(out or err)
    check("postpone 成功", rc == 0 and "Rescheduled:" in out)

    print("== 5. 月度归档：上月全部完成的文件 ==")
    storage = os.path.join(tmp, "storage")
    with open(os.path.join(storage, "2026-09-01.md"), "w", encoding="utf-8") as f:
        f.write("# 待办 2026-09-01\n归档: false\nschema: 1\n---\n\n"
                "## T-20260901-001\n状态: [x] 结束\n重要: 不重要\n紧急: 不紧急\n内容: 九月的旧任务\n"
                "创建: 2026-09-01 10:00\n")
    with open(os.path.join(storage, "2026-09-02.md"), "w", encoding="utf-8") as f:
        f.write("# 待办 2026-09-02\n归档: false\nschema: 1\n---\n\n"
                "## T-20260902-001\n状态: [~] 进行中\n重要: 不重要\n紧急: 不紧急\n内容: 九月未完成的\n"
                "创建: 2026-09-02 10:00\n")
    rc, out, err = run(tmp, "archive-month", "--dry-run")
    print(out or err)
    check("只归档已全部完成的月份文件", "2026-09-01" in out and "2026-09-02" not in out)
    rc, out, err = run(tmp, "archive-month")
    print(out or err)
    check("归档执行成功", rc == 0)
    check("原日文件已移走", not os.path.exists(os.path.join(storage, "2026-09-01.md")))
    check("未完成的文件保留", os.path.exists(os.path.join(storage, "2026-09-02.md")))
    arch = os.path.join(storage, "archive", "2026-09.md")
    check("归档文件已生成", os.path.exists(arch))
    if os.path.exists(arch):
        with open(arch, encoding="utf-8") as f:
            body = f.read()
        check("归档文件带 schema 头", "schema: 2" in body)
        check("归档文件记录原日期", "原日期: 2026-09-01" in body)
        check("归档文件记录来源", "来源文件: 2026-09-01" in body)
    rc, out, err = run(tmp, "show", "2026-09")
    check("show 月份可查看归档", rc == 0 and "九月的旧任务" in out)

    print("== 6. 索引：周口径 + 今日/逾期 ==")
    import json
    rc, out, err = run(tmp, "index", "--rebuild")
    idx = json.loads(out)
    check("index 带 schema_version", idx.get("schema_version") == 2)
    check("week 从周一起", idx["week"]["start"] == _monday())
    check("summary 含 today/overdue/monthly_archives",
          all(k in idx["summary"] for k in ("today", "overdue", "monthly_archives", "archived_tasks")))
    check("月度归档计数", idx["summary"]["monthly_archives"] == 1)

    print("== 7. 默认值可覆盖 ==")
    rc, out, err = run(tmp, "env", "--set", "defaults.status=待开始")
    check("env --set defaults.status", rc == 0 and "待开始" in out)
    rc, out, err = run(tmp, "add", "--text", "默认状态测试", "--force")
    check("新任务用覆盖后的默认值", "status: 待开始" in out, out[:300])

    # 先埋一条带标签的旧任务，供「历史标签复用」验证
    print("== 8. 标签推测：只给建议，不写入 ==")
    import json as _json
    rc, out, err = run(tmp, "add", "--text", "给甲方做方案PPT", "--tags", "客户对接", "--force")
    check("显式传 tags 时不推测", rc == 0 and "Suggested tags" not in out, out[:300])
    check("显式 tags 正常写入", "tags: 客户对接" in out, out[:300])

    rc, out, err = run(tmp, "suggest-tags", "--text", "给甲方做方案PPT 第二版")
    hist = {}
    try:
        hist = _json.loads(out)
    except Exception:
        pass
    check("suggest-tags 输出可读 JSON", rc == 0 and hist.get("written") is False, (out or err)[:300])
    check("命中历史标签", "客户对接" in (hist.get("suggestions") or []), str(hist.get("suggestions")))
    check("理由标明来自历史", hist.get("reason", {}).get("history") is True, str(hist.get("reason")))

    rc, out, err = run(tmp, "suggest-tags", "--text", "修复登录接口的 bug", "--note", "补单元测试")
    kw = _json.loads(out) if rc == 0 else {}
    check("命中关键词规则", "开发" in (kw.get("suggestions") or []), str(kw.get("suggestions")))

    rc, out, err = run(tmp, "suggest-tags", "--text", "整理项目笔记", "--workspace", "D:\\proj\\my-docs")
    wsh = _json.loads(out) if rc == 0 else {}
    check("工作空间领域词参与推测", "文档" in (wsh.get("suggestions") or []), str(wsh.get("suggestions")))
    check("建议给出依据", any("workspace contains" in str(e) for e in (wsh.get("reason", {}).get("evidence") or [])),
          str(wsh.get("reason")))

    rc, out, err = run(tmp, "suggest-tags", "--text", "换个新的台灯")
    none_hit = _json.loads(out) if rc == 0 else {}
    check("无把握时返回空建议", rc == 0 and not none_hit.get("suggestions"), str(none_hit.get("suggestions")))

    rc, out, err = run(tmp, "add", "--text", "复习英语课程并背单词", "--force")
    check("新建未传 tags 时给出建议", rc == 0 and "Suggested tags:" in out, out[:400])
    check("建议标签未写入存储", "标签:" not in _task_block(tmp, "复习英语课程并背单词"),
          _task_block(tmp, "复习英语课程并背单词")[:200])

    print("== 9. 迁移（旧文件 -> v2）==")
    rc, out, err = run(tmp, "migrate")
    print(out or err)

    # ============ QA 独立验证：标签推测的「只建议、不写入」红线 ============
    print("== 10. 红线：建议标签只出现在 stdout，绝不落盘 ==")
    rc, out, err = run(tmp, "add", "--text", "修复登录接口的 bug 并补单测", "--force")
    check("有信号时 add 打印建议标签", rc == 0 and "Suggested tags:" in out, (out or err)[:400])
    sug_lines = [l for l in out.splitlines() if "Suggested tags:" in l]
    sug_body = sug_lines[0].split("Suggested tags:", 1)[1].split("(not written yet")[0].strip() if sug_lines else ""
    check("建议标签内容非空", bool(sug_body), str(sug_lines))
    check("依据一并打印", "evidence:" in out, (out or err)[:400])
    blk = _task_block(tmp, "修复登录接口的 bug 并补单测")
    check("（防假阳性）存储里确实找到了这条任务", bool(blk), blk[:120])
    check("红线：落盘 md 块里没有 标签: 字段", bool(blk) and "标签:" not in blk, blk[:300])

    print("== 11. --update-id / --force / 显式 --tags 三条分支 ==")
    tid = _task_id_of(tmp, "修复登录接口的 bug 并补单测")
    check("能取到刚建任务的 ID", bool(tid), tid)
    rc, out, err = run(tmp, "add", "--update-id", tid, "--text", "背单词并复习英语课件")
    check("--update-id 分支不推测标签", rc == 0 and "Suggested tags" not in out, (out or err)[:400])
    rc, out2, _ = run(tmp, "suggest-tags", "--text", "背单词并复习英语课件")
    try:
        anti = _json.loads(out2)
    except Exception:
        anti = {}
    check("（反证）同一段文本单独推测是有建议的", "学习" in (anti.get("suggestions") or []),
          str(anti.get("suggestions")))

    rc, out, err = run(tmp, "add", "--text", "整理周报并汇报进度", "--force")
    check("--force 正常新建", rc == 0 and "force-created" in out, (out or err)[:300])
    check("--force 未传 tags 时同样给出建议", "Suggested tags:" in out, (out or err)[:300])

    # 刻意让显式传入的标签「盖不住」推测结果（学习能被盖住，英语盖不住），
    # 这样一旦推测分支被误触发，这条就会失败——否则这是条永远为真的空测试。
    rc, out, err = run(tmp, "add", "--text", "背单词打卡", "--tags", "学习;临时", "--force")
    check("显式 --tags 时不推测", rc == 0 and "Suggested tags" not in out, (out or err)[:300])
    check("显式 --tags 写入输出", "tags: 学习; 临时" in out, (out or err)[:300])
    blk2 = _task_block(tmp, "背单词打卡")
    check("显式 --tags 落盘到 md", bool(blk2) and "标签: 学习; 临时" in blk2, blk2[:300])
    rc, anti_out, _ = run(tmp, "suggest-tags", "--text", "背单词打卡")
    try:
        anti2 = _json.loads(anti_out)
    except Exception:
        anti2 = {}
    check("（反证）不传 tags 时这段文本确实有可推测的标签",
          "英语" in (anti2.get("suggestions") or []), str(anti2.get("suggestions")))

    print("== 12. 无信号时不硬凑 ==")
    rc, out, err = run(tmp, "add", "--text", "紫色窗帘", "--force")
    check("无信号时 add 不给建议", rc == 0 and "Suggested tags" not in out, (out or err)[:300])
    rc, out, err = run(tmp, "suggest-tags", "--text", "紫色窗帘")
    try:
        none_hit2 = _json.loads(out)
    except Exception:
        none_hit2 = {}
    check("无信号时 suggest-tags 返回空列表", rc == 0 and none_hit2.get("suggestions") == [],
          str(none_hit2.get("suggestions")))
    check("无信号时 written 仍为 false", none_hit2.get("written") is False)

    print("== 13. suggest-tags 的 JSON 契约 ==")
    rc, out, err = run(tmp, "suggest-tags", "--text", "整理项目笔记",
                       "--note", "复盘本周", "--workspace", "D:\\proj\\my-docs")
    try:
        js = _json.loads(out)
    except Exception as e:
        js = {}
        check("suggest-tags 输出可被 json.loads", False, str(e) + " | " + out[:200])
    check("suggest-tags 输出可被 json.loads", bool(js), out[:200])
    check("written 恒为 false", js.get("written") is False, str(js.get("written")))
    dets = js.get("details") or []
    check("details 非空", len(dets) > 0, str(js.get("suggestions")))
    check("details 每项都有 source 字段", bool(dets) and all("source" in d for d in dets), str(dets))
    check("details 每项都有 tag/score/evidence",
          bool(dets) and all(all(k in d for k in ("tag", "score", "evidence")) for d in dets), str(dets))
    check("工作空间来源进了 source", any("workspace" in str(d.get("source")) for d in dets), str(dets))
    check("reason 含 history/keyword/evidence",
          all(k in (js.get("reason") or {}) for k in ("history", "keyword", "evidence")), str(js.get("reason")))

    print("== 14. 英文词边界（debug 不能当 bug）==")
    for bad in ("debug the login flow", "debugging session", "bugfix 收尾"):
        rc, out, err = run(tmp, "suggest-tags", "--text", bad)
        try:
            j = _json.loads(out)
        except Exception:
            j = {}
        check("「%s」不误命中开发类规则" % bad, "开发" not in (j.get("suggestions") or []),
              str(j.get("suggestions")))
    rc, out, err = run(tmp, "suggest-tags", "--text", "fix a bug in login")
    try:
        j2 = _json.loads(out)
    except Exception:
        j2 = {}
    check("真正的 bug 仍能命中开发", "开发" in (j2.get("suggestions") or []), str(j2.get("suggestions")))

    # ============ QA 回归：原有命令行为不变 ============
    print("== 15. 回归：原有命令 ==")
    rc, out, err = run(tmp, "list")
    check("list 正常", rc == 0 and bool(out.strip()), (out or err)[:200])
    # check 发现重复时按「需确认」退出码返回（rc=3），属于既有约定，不能当成失败
    rc, out, err = run(tmp, "check", "--text", "背单词打卡")
    check("check 能识别重复", rc == 3 and "exact" in out, "rc=%s | %s" % (rc, (out or err)[:200]))

    tid2 = _task_id_of(tmp, "整理周报并汇报进度")
    rc, out, err = run(tmp, "start", tid2)
    check("start 正常", rc == 0, (out or err)[:200])
    rc, out, err = run(tmp, "done", tid2)
    check("done 正常", rc == 0, (out or err)[:200])
    rc, out, err = run(tmp, "reopen", tid2)
    check("reopen 正常", rc == 0, (out or err)[:200])

    tid3 = _task_id_of(tmp, "紫色窗帘")
    rc, out, err = run(tmp, "dep", tid3, tid2)
    check("dep 设置依赖正常", rc == 0, (out or err)[:200])
    rc, out, err = run(tmp, "children", tid2)
    check("children 正常", rc == 0, (out or err)[:200])
    rc, out, err = run(tmp, "deparent", tid3)
    check("deparent 正常", rc == 0, (out or err)[:200])

    rc, out, err = run(tmp, "archive-month", "--dry-run")
    check("archive-month 预览正常", rc == 0, (out or err)[:200])
    rc, out, err = run(tmp, "migrate", "--apply")
    check("migrate --apply 正常", rc == 0, (out or err)[:300])
    check("迁移后日文件全部为 schema 2", _all_schema2(tmp), _schema_report(tmp))

    with open(os.path.join(storage, "2026-08-08.md"), "w", encoding="utf-8") as f:
        f.write("# 待办 2026-08-08\n归档: false\nschema: 2\n---\n\n"
                "## T-20260808-001\n状态: [x] 结束\n重要: 不重要\n紧急: 不紧急\n内容: 八月归档测试\n"
                "创建: 2026-08-08 10:00\n")
    # 注：整日文件全部完成后会被折进月度归档（既有行为，非本次改动引入），
    # 所以这里认「就地标记 归档: true」或「内容已并入 storage/archive/YYYY-MM.md」两种落点。
    rc, out, err = run(tmp, "archive", "2026-08-08")
    check("archive 强制归档正常", rc == 0, (out or err)[:200])
    day_file = _read_file(os.path.join(storage, "2026-08-08.md"))
    month_file = _read_file(os.path.join(storage, "archive", "2026-08.md"))
    check("归档后当日文件被标记或折入月度归档",
          "归档: true" in day_file or "八月归档测试" in month_file,
          "day=%r month=%r" % (day_file[:120], month_file[:120]))

    rc, out, err = run(tmp, "index", "--rebuild")
    check("index --rebuild 正常", rc == 0 and '"schema_version"' in out, (out or err)[:200])
    rc, out, err = run(tmp, "env")
    check("env 查看正常", rc == 0, (out or err)[:200])
    rc, out, err = run(tmp, "show", tid2)
    check("show 任务正常", rc == 0 and bool(out.strip()), (out or err)[:200])

    # ------------------------------------------------------------------
    print("== 16. 存储目录可配置（env --set storage_dir）==")
    rc, out, err = run(tmp, "env")
    check("env 输出生效的存储目录", "Effective storage directory" in out, (out or err)[:200])
    default_storage = os.path.join(tmp, "storage")
    store2 = os.path.join(tmp, "store2")
    before_files = _count_md(default_storage)

    # (a) 旧目录有数据且未做选择 -> 报错（退出码 2）且配置不动
    rc, out, err = run(tmp, "env", "--set", "storage_dir=" + store2)
    check("旧目录有数据时不选搬迁方式 -> 退出码 2", rc == 2, "rc=%s" % rc)
    check("报错给出 --migrate / --no-migrate 两条路", "--migrate" in err and "--no-migrate" in err, err[:300])
    rc, out, err = run(tmp, "env")
    check("配置未被悄悄改动", store2 not in out, out[:200])

    # (b) 目标目录已有内容 -> 校验不通过：中止、回滚配置、两边数据都保住
    bad = os.path.join(tmp, "badstore")
    os.makedirs(bad, exist_ok=True)
    with open(os.path.join(bad, "2026-01-01.md"), "w", encoding="utf-8") as f:
        f.write("# 待办 2026-01-01\n归档: false\nschema: 2\n---\n\n"
                "## T-20260101-001\n状态: 进行中\n重要: 不重要\n紧急: 不紧急\n"
                "内容: 占位\n创建: 2026-01-01 09:00\n")
    rc, out, err = run(tmp, "env", "--set", "storage_dir=" + bad, "--migrate")
    check("校验不通过时退出码 1", rc == 1, "rc=%s" % rc)
    check("校验不通过时明确报错", "Verification failed" in err or "Verification failed" in out, (out + err)[:300])
    check("失败后配置回滚到原目录", "rolled back" in (err + out), (err or out)[:300])
    check("源数据未丢失", _count_md(default_storage) == before_files, str(os.listdir(default_storage)))
    check("目标目录原有文件未被破坏", os.path.isfile(os.path.join(bad, "2026-01-01.md")))
    check("失败时回删本次写入的半份副本", _count_md(bad) == 1, str(os.listdir(bad)))

    # (c) --no-migrate：只改配置，旧数据原地不动
    tmp3 = os.path.join(tmp, "store3")
    rc, out, err = run(tmp, "env", "--set", "storage_dir=" + tmp3, "--no-migrate")
    check("--no-migrate 退出码 0", rc == 0, (out or err)[:200])
    check("--no-migrate 明确提示未搬迁", "not migrated" in out, out[:300])
    check("--no-migrate 后旧目录数据仍在", _count_md(default_storage) == before_files)
    # 把配置改回原目录，好继续测真正的搬迁
    rc, out, err = run(tmp, "env", "--set", "storage_dir=" + default_storage, "--no-migrate")
    check("配置可改回原目录", rc == 0 and _count_md(default_storage) == before_files, (out or err)[:200])

    # (d) 搬迁到新目录：文件搬走、旧目录清空、任务数不变
    rc, out, err = run(tmp, "env", "--set", "storage_dir=" + store2, "--migrate")
    check("--migrate 退出码 0", rc == 0, (out or err)[:300])
    check("输出确认搬迁完成", "Migration done:" in out, out[:300])
    check("新目录拿到全部文件", _count_md(store2) == before_files,
          "new=%d old=%d" % (_count_md(store2), before_files))
    check("旧目录已清空", _count_md(default_storage) == 0, str(os.listdir(default_storage)))
    rc, out, err = run(tmp, "list", "--state", "all")
    check("搬迁后任务照常可读", rc == 0 and out.count("T-") >= before_files, (out or err)[:200])
    rc, out, err = run(tmp, "index", "--rebuild")
    check("搬迁场景后索引重建正常", rc == 0 and '"schema_version"' in out, (out or err)[:200])

    # ------------------------------------------------------------------
    print("== 17. 编辑器可配置（env --set editor.*）==")
    rc, out, err = run(tmp, "env")
    check("env 输出编辑器状态", "Effective editor" in out, (out or err)[:200])
    check("未探测到时引导配置 editor.path", "editor.path" in out, out[-400:])

    rc, out, err = run(tmp, "env", "--set", "editor.path=" + os.path.join(tmp, "no-such-editor.exe"))
    check("editor.path 指向不存在的文件 -> 退出码 2", rc == 2, "rc=%s" % rc)
    check("给出路径不存在的明确错误", "Editor file not found" in err, err[:200])

    rc, out, err = run(tmp, "env", "--set", "editor.path=definitely-not-a-command-xyz")
    check("editor.path 是 PATH 里没有的命令名 -> 退出码 2", rc == 2, "rc=%s" % rc)
    check("提示命令不在 PATH", "not found in PATH" in err, err[:200])

    rc, out, err = run(tmp, "env", "--set", "editor.foo=bar")
    check("未知 editor 子键被拒绝", rc == 2 and "editor." in err, (out + err)[:200])

    # 用系统自带命令当编辑器替身，避免真弹编辑器窗口
    if os.name == "nt":
        ed_path = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "cmd.exe")
        ed_args = ["--set", "editor.args=/c;exit"]
    else:
        ed_path = "/bin/true"
        ed_args = []
    rc, out, err = run(tmp, "env", "--set", "editor.path=" + ed_path,
                       "--set", "editor.label=替身编辑器", *ed_args)
    check("合法 editor.path 配置成功", rc == 0, (out or err)[:300])
    check("env 显示配置的编辑器名", "替身编辑器" in out, out[-400:])

    rc, out, err = run(tmp, "add", "--text", "编辑器联调", "--workspace",
                       os.path.join(tmp, "wsdir"), "--force")
    ed_id = _task_id_from(out) or ""
    check("建带工作空间的任务成功", rc == 0 and bool(ed_id), (out or err)[:200])
    if ed_id:
        rc, out, err = run(tmp, "work", ed_id)
        check("work 用配置的编辑器打开", rc == 0 and "替身编辑器" in out, (out + err)[:300])
        check("work 不再写死 Cursor", "Cursor" not in out, out[:200])

    # 真启动一次：用假编辑器记录收到的目录参数，证明进程真的被拉起来（不只拼了个命令）
    # Windows 用 .cmd 还能顺带覆盖「.cmd 必须经 cmd.exe」这条分支。
    marker = os.path.join(tmp, "editor-arg.txt")
    if os.name == "nt":
        fake = os.path.join(tmp, "fake-editor.cmd")
        with open(fake, "w", encoding="utf-8") as f:
            # 用 %~dp0 定位脚本同目录（拼字符串避免 \e 转义）
            f.write('@echo off\r\necho %1 > "' + "%~dp0" + 'editor-arg.txt"\r\n')
    else:
        fake = os.path.join(tmp, "fake-editor.sh")
        with open(fake, "w", encoding="utf-8") as f:
            f.write('#!/bin/sh\necho "$1" > "$(dirname "$0")/editor-arg.txt"\n')
        os.chmod(fake, 0o755)
    # editor.args= 清掉上一步给 cmd.exe 替身配的 "/c;exit"，否则会被当成编辑器的固定前置参数
    rc, out, err = run(tmp, "env", "--set", "editor.path=" + fake, "--set", "editor.label=假编辑器",
                       "--set", "editor.args=")
    check("可配置为脚本型编辑器", rc == 0, (out or err)[:200])
    if ed_id:
        rc, out, err = run(tmp, "work", ed_id)
        check("work 退出码 0", rc == 0, (out + err)[:300])
        import time
        for _ in range(20):
            if os.path.isfile(marker):
                break
            time.sleep(0.2)
        # cmd.exe 在参数里含空格时会保留一层引号，剥掉后再比对路径语义
        got = _read_file(marker).strip().strip('"')
        check("编辑器进程真的被拉起并收到工作区目录",
              bool(got) and os.path.basename(got.replace("/", os.sep)) == "wsdir",
              "marker=%r" % got)

    # 编辑器「配置了但文件后来消失」：work 仍完成标记进行中，但必须报错 + 给配置出口
    fake_bak = fake + ".bak"
    shutil.copy2(fake, fake_bak)
    rc, out, err = run(tmp, "env", "--set", "editor.path=" + fake_bak, "--set", "editor.label=会失效")
    check("配置临时编辑器成功", rc == 0, (out or err)[:200])
    os.remove(fake_bak)
    if ed_id:
        rc, out, err = run(tmp, "work", ed_id)
        check("编辑器失效时 work 仍标记进行中并返回 0", rc == 0 and "Marked in progress" in out,
              (out + err)[:300])
        check("编辑器失效时明确报错并给出配置命令", "editor.path" in err, err[:300])

    # --reset 不能把用户配置冲掉
    rc, out, err = run(tmp, "env", "--reset")
    check("--reset 退出码 0", rc == 0, (out or err)[:200])
    check("--reset 保留存储目录配置", store2 in out, out[:200])
    check("--reset 保留用户默认值配置", '"status"' in out, out[:200])

    # ------------------------------------------------------------------
    print("== 18. 网页 UI 服务配置（ui.port / ui.prompt）==")
    rc, out, err = run(tmp, "env")
    check("env 输出网页 UI 服务配置行", "Web UI service" in out, (out or err)[:300])

    rc, out, err = run(tmp, "env", "--set", "ui.port=9000")
    check("ui.port 合法端口配置成功", rc == 0 and "9000" in out, (out or err)[:300])

    rc, out, err = run(tmp, "env", "--set", "ui.port=abc")
    check("ui.port 非法值被拒绝", rc == 2 and "must be a port number" in err, (out + err)[:200])

    rc, out, err = run(tmp, "env", "--set", "ui.port=99999")
    check("ui.port 越界值被拒绝", rc == 2, (out + err)[:200])

    rc, out, err = run(tmp, "env", "--set", "ui.prompt=off")
    check("ui.prompt=off 配置成功", rc == 0, (out or err)[:200])

    rc, out, err = run(tmp, "env", "--set", "ui.prompt=maybe")
    check("ui.prompt 非法值被拒绝", rc == 2 and "ui.prompt" in err, (out + err)[:200])

    rc, out, err = run(tmp, "env", "--set", "ui.foo=bar")
    check("未知 ui 子键被拒绝", rc == 2 and "ui." in err, (out + err)[:200])

    # 维护命令在 UI 检查关闭时正常返回（AWAM_TODO_UI_PROMPT=off 由 run() 默认注入）
    rc, out, err = run(tmp, "add", "--text", "网页UI联调任务", "--force")
    check("UI 检查关闭时 add 正常且不弹框", rc == 0 and "web UI" not in out.lower(), (out or err)[:200])

    # ------------------------------------------------------------------
    print("== 19. 分诊 triage（只读）+ delete 命令 ==")
    import json as _json3

    def _triage(text):
        rc, out, err = run(tmp, "triage", "--text", text)
        try:
            return rc, _json3.loads(out)
        except Exception:
            return rc, {}

    rc, j = _triage("明天上午十点前写好季度报告")
    check("triage 普通承诺 -> add", rc == 0 and j.get("action") == "add", str(j)[:200])
    check("triage 抽取截止时间", (j.get("fields") or {}).get("due") in ("明天", "明天 10:00"),
          str(j.get("fields")))
    check("triage 高置信无需确认", j.get("need_confirm") is False, str(j.get("need_confirm")))

    rc, out, err = run(tmp, "add", "--text", "继续detect-agent软件的开发", "--force")
    tid = _task_id_from(out) or ""
    check("分诊前置任务创建成功", bool(tid), (out or err)[:200])

    rc, j = _triage("把继续detect-agent软件的开发标记为完成")
    check("triage 状态动词 -> status", j.get("action") == "status", str(j)[:200])
    check("triage 锁定真实任务ID", (j.get("target") or {}).get("id") == tid, str(j.get("target")))
    check("triage 状态目标为结束", j.get("status") == "结束", str(j.get("status")))

    rc, j = _triage("删除 继续detect-agent软件的开发")
    check("triage 删除动词 -> delete", j.get("action") == "delete", str(j)[:200])
    check("triage 删除必确认", j.get("need_confirm") is True, str(j.get("need_confirm")))
    check("triage 删除理由标明破坏性", "destructive" in (j.get("reasons") or []), str(j.get("reasons")))
    check("triage 删除锁定真实任务ID", (j.get("target") or {}).get("id") == tid, str(j.get("target")))

    rc, j = _triage("这周末去哪儿玩？")
    check("triage 疑问句 -> unknown+need_confirm",
          j.get("action") == "unknown" and j.get("need_confirm") is True, str(j)[:200])

    rc, out, err = run(tmp, "delete", tid)
    check("delete 命令退出码 0", rc == 0, (out or err)[:200])
    rc, out, err = run(tmp, "show", tid)
    check("delete 后任务确实不存在", rc != 0, (out or err)[:200])

    # 通过就清掉临时目录；失败时留下现场，便于照着失败项翻文件排查。
    # 想强制清理（或强制保留）用环境变量 AWAM_TODO_KEEP_TMP=0 / 1。
    keep_env = os.environ.get("AWAM_TODO_KEEP_TMP")
    keep = (keep_env == "1") if keep_env in ("0", "1") else (not ok)
    if keep:
        print("\n临时目录（排查用，可删）：%s" % tmp)
    else:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n结果：" + ("全部通过" if ok else "存在失败项"))
    return 0 if ok else 1


def _storage_text(tmp):
    """把临时目录里的日文件拼成一整块文本（不含 archive/ 子目录）。"""
    parts = []
    p = os.path.join(tmp, "storage")
    for fn in sorted(os.listdir(p)):
        fp = os.path.join(p, fn)
        if fn.endswith(".md") and os.path.isfile(fp):
            with open(fp, encoding="utf-8") as f:
                parts.append(f.read())
    return "\n".join(parts)


def _task_block(tmp, text):
    """取出某条任务在存储文件里的原始块，用于验证「没有被偷偷写入字段」。"""
    for blk in _storage_text(tmp).split("\n## "):
        if ("内容: " + text) in blk:
            return blk
    return ""


def _task_id_of(tmp, text):
    """按任务内容定位其 ID（用于 --update-id / done / dep 等后续操作）。"""
    import re
    p = os.path.join(tmp, "storage")
    for fn in sorted(os.listdir(p)):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(p, fn), encoding="utf-8") as f:
            for blk in f.read().split("\n## "):
                if ("内容: " + text) in blk:
                    m = re.search(r"^(T-\d{8}-\d{3})", blk.strip())
                    if m:
                        return m.group(1)
    return ""


def _read_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _all_schema2(tmp):
    """日文件（不含 archive/）必须都是 schema 2，验证 migrate 没被改坏。"""
    p = os.path.join(tmp, "storage")
    for fn in sorted(os.listdir(p)):
        if fn.endswith(".md") and os.path.isfile(os.path.join(p, fn)):
            if "schema: 2" not in _read_file(os.path.join(p, fn)):
                return False
    return True


def _schema_report(tmp):
    p = os.path.join(tmp, "storage")
    return "; ".join(fn + "=" + ("v2" if "schema: 2" in _read_file(os.path.join(p, fn)) else "非v2")
                     for fn in sorted(os.listdir(p)) if fn.endswith(".md"))


def _first_id(tmp):
    import re
    p = os.path.join(tmp, "storage")
    for fn in sorted(os.listdir(p)):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(p, fn), encoding="utf-8") as f:
            m = re.search(r"^## (T-\d{8}-\d{3})", f.read(), re.M)
        if m:
            return m.group(1)
    return "T-00000000-000"


def _count_md(d):
    """目录下的 .md 文件数（不含子目录），用于搬迁前后比对。"""
    if not os.path.isdir(d):
        return 0
    return len([f for f in os.listdir(d) if f.endswith(".md")])


def _task_id_from(out):
    """从命令输出里取第一个任务 ID。"""
    import re
    m = re.search(r"(T-\d{8}-\d{3})", out or "")
    return m.group(1) if m else ""


def _monday():
    import datetime as dt
    d = dt.date.today()
    return (d - dt.timedelta(days=d.isoweekday() - 1)).strftime("%Y-%m-%d")


if __name__ == "__main__":
    sys.exit(main())
