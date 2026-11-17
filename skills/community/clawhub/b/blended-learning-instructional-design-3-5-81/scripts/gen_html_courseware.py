# -*- coding: utf-8 -*-
"""生成 HTML 交互式说课课件。

特点（依据 Skill 要求）：
- 按 PPT 标准分辨率 1280x720 分页呈现，自适应缩放；
- 页面字号最小 24px（末页页脚说明除外，其字号按内容长度自适应，必要时降到 12px
  以确保条目不被 overflow 裁切），每页内容逐项动画呈现；
- 响应鼠标点击、键盘上下左右箭头、回车键与空格键翻页；
- 内置 ≥5 个交互点：前测、中测、后测 3 组测试题 + 知识图谱探索 + 教学流程模拟 2 个模拟仿真；
- 末尾新增一页，插入 references/footer_note.json 页脚说明。

用法：
    python gen_html_courseware.py <design_data.json> [输出目录]
"""
import html
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import read_footer, strip_lines  # noqa: E402


# ---------------- 工具函数 ----------------

def esc(t):
    return html.escape(str(t or ""), quote=False)


def js(t):
    return json.dumps(str(t or ""), ensure_ascii=False)


def split_points(text, max_n=8, min_n=3, fallback=None):
    """把长文本拆成知识点/步骤列表。"""
    lines = strip_lines(text)
    points = []
    for ln in lines:
        for seg in ln.replace("；", "\n").replace("。", "\n").replace("；", "\n").split("\n"):
            seg = seg.strip().strip("，,.")
            if seg and seg not in points:
                points.append(seg)
    points = points[:max_n]
    if len(points) < min_n and fallback:
        points = fallback
    return points


def make_options(correct, distractor_pool, seed):
    """生成 4 个选项（1 个正确 + 3 个干扰项），返回 (options, correct_index)。"""
    rnd = random.Random(seed)
    distractors = [d for d in distractor_pool if d and d != correct]
    rnd.shuffle(distractors)
    while len(distractors) < 3:
        distractors.append("以上均不正确")
    distractors = distractors[:3]
    options = [correct] + distractors
    rnd.shuffle(options)
    return options, options.index(correct)


def auto_quizzes(data):
    """依据学习目标自动生成面向学生的前测/中测/后测（内容型兜底题）。"""
    bi = data.get("basic_info", {}) or {}
    sl = data.get("single_lesson", {}) or {}
    lg = sl.get("learning_goals", "") or ""
    if isinstance(lg, dict):
        kg = [l for l in strip_lines(lg.get("knowledge", "")) if l.strip()]
        sg = [l for l in strip_lines(lg.get("skill", "")) if l.strip()]
        lg_ = [l for l in strip_lines(lg.get("literacy", "")) if l.strip()]
        ig = [l for l in strip_lines(lg.get("ideology", "")) if l.strip()]
    else:
        kg = sg = lg_ = ig = [l for l in strip_lines(str(lg)) if l.strip()]

    theme = bi.get("content", "本课次") or "本课次"

    def explain_for(phase, correct):
        return ("【%s】本题考查“%s”相关学习内容。正确选项：%s。"
                "建议结合教学设计文档“内容与资源/过程与方法”进一步理解，"
                "并在超星学习通对应题库中查看解析。" % (phase, theme, correct))

    def item(q, correct, pool, seed, phase):
        opts, idx = make_options(correct, pool, seed)
        return {"q": q, "options": opts, "answer": idx,
                "explain": explain_for(phase, correct)}

    quizzes = []
    # 前测：概念/知识诊断
    pre_pool = kg + sg
    pre = []
    if kg:
        pre.append(item("关于本课次的核心概念，下列说法正确的是？", kg[0], pre_pool, 101, "前测·概念诊断"))
    if len(kg) > 1:
        pre.append(item("下列属于本课次“知识目标”的是？", kg[1], pre_pool, 102, "前测·知识目标"))
    if pre:
        quizzes.append({"title": "前测 · 预习检测", "icon": "📝", "questions": pre})
    # 中测：方法/技能
    mid_pool = sg + lg_
    mid = []
    if sg:
        mid.append(item("本课次要求学生能够（ ），下列说法正确的是？", sg[0], mid_pool, 201, "中测·方法应用"))
    if lg_:
        mid.append(item("关于本课次的高阶（素养）目标，下列说法正确的是？", lg_[0], mid_pool, 202, "中测·素养目标"))
    if mid:
        quizzes.append({"title": "中测 · 课中检测", "icon": "⚡", "questions": mid})
    # 后测：综合/达成
    post_pool = lg_ + ig + sg
    post = []
    if lg_:
        post.append(item("本课次达成的高阶学习目标包括（ ），下列说法正确的是？", lg_[0], post_pool, 301, "后测·效果检验"))
    if ig:
        post.append(item("关于本课次的思政/价值目标，下列说法正确的是？", ig[0], post_pool, 302, "后测·价值塑造"))
    if post:
        quizzes.append({"title": "后测 · 效果检验", "icon": "🏆", "questions": post})
    return quizzes


def custom_interactions(data):
    """读取 AI 可选提供的自定义交互点；未提供时返回空列表。"""
    return data.get("interactions", {}) or {}


# ---------------- 幻灯片构建 ----------------

def slide(inner, cls=""):
    return '<section class="slide %s">%s</section>' % (cls, inner)


def content_slide(title, subtitle, blocks, icon="📖"):
    inner = ['<div class="kicker">%s %s</div>' % (icon, esc(subtitle))]
    inner.append('<h2>%s</h2>' % esc(title))
    inner.append('<div class="body">')
    for i, blk in enumerate(blocks):
        inner.append('<div class="item" style="animation-delay:.%02ds">%s</div>' % (min(i, 8), blk))
    inner.append('</div>')
    return slide("\n".join(inner))


def bullets_slide(title, subtitle, lines, icon="📖"):
    blocks = []
    for ln in lines:
        blocks.append('<div class="bullet"><span class="dot"></span>%s</div>' % esc(ln))
    return content_slide(title, subtitle, blocks, icon)


def build_html(data):
    bi = data.get("basic_info", {}) or {}
    wc = data.get("whole_course", {}) or {}
    sl = data.get("single_lesson", {}) or {}
    cal = data.get("calendar", []) or []
    cname = bi.get("course_name", "（课程名称）")
    interactive = custom_interactions(data)

    slides = []

    # 1 封面
    slides.append(slide(
        '<div class="cover">'
        '<div class="cover-badge">混合式教学设计 · 说课课件</div>'
        '<h1>%s</h1>'
        '<div class="cover-info">'
        '<p>授课内容：%s</p><p>所属节次：%s</p>'
        '<p>面向专业：%s</p><p>学时安排：%s · 授课人数：%s</p>'
        '</div></div>' % (
            esc(cname), esc(bi.get("content", "")), esc(bi.get("section", "")),
            esc(bi.get("major", "")), esc(bi.get("hours", "")), esc(bi.get("students", ""))),
        cls="cover-slide"))

    # 2 目录
    agenda = ["一、基本信息", "二、整门课程的混合式教学设计方案",
              "三、一课次的混合式教学设计方案", "互动体验：前测 · 知识图谱 · 教学流程模拟 · 中测 · 后测",
              "四、课程教学日历", "总结与页脚说明"]
    blocks = ["".join('<div class="agenda-item"><span>%02d</span>%s</div>' % (i + 1, esc(a)))
              for i, a in enumerate(agenda)]
    slides.append(content_slide("说课目录", "内容导航", blocks, "🗺️"))

    # 3 基本信息
    bi_lines = [
        ("课程名称", bi.get("course_name", "")), ("面向专业", bi.get("major", "")),
        ("授课内容", bi.get("content", "")), ("所属课程节次", bi.get("section", "")),
        ("学时安排", bi.get("hours", "")), ("授课人数", bi.get("students", "")),
    ]
    slides.append(content_slide("一、基本信息", "课程与课次概况",
                                ['<div class="kv-grid">' + "".join(
                                    '<div class="kv"><span class="k">%s</span><span class="v">%s</span></div>'
                                    % (esc(k), esc(v)) for k, v in bi_lines) + '</div>'], "📋"))

    # 4-6 整门课程
    slides.append(bullets_slide("二、整门课程 · 1.混合式教学设计思路", "整门课程方案",
                                split_points(wc.get("design_idea", "（整门课程的混合式教学设计思路）"), max_n=6), "🎯"))
    slides.append(bullets_slide("二、整门课程 · 2.创新举措", "整门课程方案",
                                split_points(wc.get("innovation", "（整门课程的创新举措）"), max_n=6), "💡"))
    slides.append(bullets_slide("二、整门课程 · 3.效果达成情况", "整门课程方案",
                                split_points(wc.get("effect", "（整门课程的效果达成情况）"), max_n=6), "📈"))

    # 7-12 一课次
    slides.append(bullets_slide("三、一课次 · 1.学情分析", "本课次方案",
                                split_points(sl.get("learning_analysis", "（本课次学生的学情分析）"), max_n=6), "🧭"))
    slides.append(goals_slide(sl))
    slides.append(bullets_slide("三、一课次 · 3.内容与资源", "本课次方案",
                                split_points(sl.get("content_resources", "（本课次内容与资源）"), max_n=6), "📚"))
    slides.append(bullets_slide("三、一课次 · 4.过程与方法", "本课次方案",
                                split_points(sl.get("process_method", "（本课次过程与方法）"), max_n=6), "🔄"))
    slides.append(bullets_slide("三、一课次 · 5.评价与反馈", "本课次方案",
                                split_points(sl.get("evaluation", "（本课次评价与反馈）"), max_n=6), "✅"))
    slides.append(bullets_slide("三、一课次 · 6.教学效果达成情况", "本课次方案",
                                split_points(sl.get("effect", "（本课次教学效果）"), max_n=6), "🌟"))

    # 13-17 交互点
    quizzes = interactive.get("quizzes") or auto_quizzes(data)
    for qz in quizzes[:3]:
        slides.append(quiz_slide(qz))

    # 知识图谱模拟
    kp = split_points(sl.get("content_resources", ""), max_n=8, min_n=3,
                      fallback=["课程导入", "核心概念", "典型应用", "总结提升"])
    slides.append(sim_knowledge_slide(kp))
    # 教学流程模拟
    steps = split_points(sl.get("process_method", ""), max_n=6, min_n=3,
                         fallback=["课前线上自学", "课中线下精讲深练", "课后线上巩固拓展"])
    slides.append(sim_flow_slide(steps))

    # 18 教学日历
    slides.append(calendar_slide(cal, cname))

    # 19 总结
    slides.append(bullets_slide("总结", "本课次混合式教学设计要点回顾",
                                ["围绕课程目标设计线上线下融合的学习路径",
                                 "以学生发展为中心组织内容与资源",
                                 "过程性评价贯穿课前、课中、课后",
                                 "用数据持续改进教学，达成教学效果"], "🎓"))

    # 20 页脚说明（末尾新增一页）
    slides.append(footer_slide())

    return slides


def quiz_slide(qz):
    q_html = []
    for qi, q in enumerate(qz.get("questions", [])):
        opts = "".join(
            '<button class="opt" data-ok="%d">%s</button>' % (
                1 if i == q.get("answer") else 0, esc(o)) for i, o in enumerate(q.get("options", [])))
        q_html.append(
            '<div class="quiz" data-q="%d">'
            '<p class="q-text">Q%d. %s</p>%s'
            '<p class="q-explain" hidden>%s</p>'
            '<p class="q-feedback"></p></div>' % (
                qi, qi + 1, esc(q.get("q", "")), opts, esc(q.get("explain", ""))))
    return slide(
        '<div class="kicker">%s 互动测试</div><h2>%s</h2>'
        '<div class="body quiz-body">%s</div>'
        '<p class="hint">点击选项作答，选择后自动给出判定、正确答案与解析。</p>'
        % (esc(qz.get("icon", "📝")), esc(qz.get("title", "课堂测试")), "\n".join(q_html)))


def sim_knowledge_slide(points):
    nodes = "".join('<button class="kp-node" data-i="%d">%s</button>'
                    % (i, esc(p)) for i, p in enumerate(points))
    return slide(
        '<div class="kicker">🔬 互动模拟仿真 1 · 知识图谱探索</div>'
        '<h2>本课次知识点关系图谱</h2>'
        '<p class="sim-desc">点击任意知识点节点，查看该知识点在本课次中的定位与说明（可多选探索）。</p>'
        '<div class="kp-cloud">%s</div>'
        '<div class="kp-detail" id="kpDetail">点击上方知识点节点开始探索。</div>'
        % nodes)


def sim_flow_slide(steps):
    cards = "".join('<div class="f-card" data-i="%d"><h3>%s</h3><p>%s</p></div>'
                    % (i, esc(s), esc("该环节说明详见教学设计文档。"))
                    for i, s in enumerate(steps))
    dots = "".join('<span class="f-dot" data-i="%d"></span>' % i for i in range(len(steps)))
    return slide(
        '<div class="kicker">🔬 互动模拟仿真 2 · 教学流程模拟</div>'
        '<h2>混合式教学实施流程（可逐步推进）</h2>'
        '<div class="f-stage"><div class="f-progress">%s</div><div class="f-view">%s</div>'
        '<div class="f-ctl">'
        '<button class="f-btn" id="fPrev">◀ 上一步</button>'
        '<button class="f-btn primary" id="fNext">下一步 ▶</button>'
        '</div><p class="f-tip" id="fTip">点击"下一步"模拟推进教学流程。</p></div>'
        % (dots, cards))


def calendar_slide(cal, cname):
    if not cal:
        return content_slide("四、课程教学日历", "《混合式教学教学日历》",
                             ["（暂无日历数据，请检查 design_data.json 的 calendar 字段）"], "🗓️")
    head = "".join("<th>%s</th>" % esc(h) for h in
                   ["序号", "日期", "周次", "讲次", "学时", "地点", "人数", "教学内容", "形式", "活动"])
    body = ""
    for it in cal[:14]:
        body += "<tr>" + "".join("<td>%s</td>" % esc(it.get(k, ""))
                                 for k in ["seq", "date", "week", "lecture", "minutes",
                                           "location", "students", "content", "form", "activity"]) + "</tr>"
    return slide(
        '<div class="kicker">🗓️ 课程教学日历</div><h2>%s 混合式教学教学日历（节选）</h2>'
        '<div class="cal-wrap"><table class="cal">%s%s</table></div>'
        '<p class="hint">完整日历见 Word 文档《混合式教学教学日历》。</p>'
        % (esc(cname), "<thead>%s</thead>" % head, "<tbody>%s</tbody>" % body))


# ---------------- 页脚页排版 ----------------

# 页脚页版面预算（单位：px，对应 1280x720 的舞台）
PAGE_W, PAGE_H = 1280, 720
PAD_X, PAD_Y = 72, 56                      # .slide 的左右/上下内边距
FOOTER_HEAD_H = 126                        # 页眉占用：kicker + h2 + .body 上边距
FOOTER_TEXT_W = PAGE_W - 2 * PAD_X - 24     # 再扣掉圆点(12px)与图文间距(12px)
FOOTER_TEXT_H = PAGE_H - 2 * PAD_Y - FOOTER_HEAD_H
BULLET_LINE_H = 1.65                        # .bullet 的 line-height


def _text_units(text):
    """粗略折算文本宽度：全角字符（中日韩）计 1，其余（半角）计 0.5。"""
    return sum(1.0 if ord(ch) > 0x2E80 else 0.5 for ch in text)


def fit_footer_size(lines, sizes=(26, 24, 22, 20, 19, 18, 17, 16, 15, 14, 13, 12)):
    """给页脚说明挑一个能完整放进一页的字号：从大到小试，取第一个装得下的。

    页脚说明由外部文件 references/footer_note.json 提供，条目多寡会变；字号写死会被
    .slide 的 overflow:hidden 裁掉尾部内容，故按内容长度自适应。
    """
    import math
    for size in sizes:
        total = 0.0
        for t in lines:
            rows = max(1, math.ceil(_text_units(t) * size / FOOTER_TEXT_W))
            total += rows * size * BULLET_LINE_H + max(6, round(size * 0.38))
        if total <= FOOTER_TEXT_H * 0.97:   # 留 3% 余量，避免临界被裁
            return size
    return sizes[-1]


def footer_slide():
    lines = read_footer()
    title = lines[0] if lines else "Skill 说明与使用提示"
    body_lines = [ln for ln in lines[1:] if ln.strip()]
    size = fit_footer_size(body_lines)
    gap = max(6, round(size * 0.38))
    dot_top = max(4, round(size * 0.5) - 0)     # 与原 26px 字号下 .dot{margin-top:13px} 同比例
    blocks = ['<div class="bullet" style="font-size:%dpx;margin-bottom:%dpx">'
              '<span class="dot" style="margin-top:%dpx"></span>%s</div>'
              % (size, gap, dot_top, esc(ln)) for ln in body_lines]
    return slide(
        '<div class="kicker">ℹ️ 页脚说明</div><h2>%s</h2><div class="body">%s</div>'
        % (esc(title), "\n".join(blocks)), cls="footer-slide")


def goals_slide(sl):
    """学习目标四类卡片（知识/技能/素养/思政），每条用布卢姆行为动词。"""
    lg = sl.get("learning_goals", "") or {}
    cards = []
    if isinstance(lg, dict):
        labels = [("knowledge", "知识目标", "📘"), ("skill", "技能目标", "🛠️"),
                  ("literacy", "素养目标", "🌱"), ("ideology", "思政目标", "🚩")]
        for key, label, icon in labels:
            v = lg.get(key, "")
            if v and str(v).strip():
                items = "".join('<div class="bullet"><span class="dot"></span>%s</div>' % esc(ln)
                                for ln in strip_lines(v))
                cards.append('<div class="goal-card"><div class="goal-h">%s %s</div>%s</div>'
                             % (icon, esc(label), items))
    else:
        cards = ['<div class="goal-card">%s</div>' % esc(str(lg))]
    inner = ('<div class="kicker">🏁 本课次学习目标</div>'
             '<h2>三、一课次 · 2.学习目标（布卢姆四类）</h2>'
             '<div class="goal-grid">%s</div>' % "\n".join(cards))
    return slide(inner)


# ---------------- HTML 模板 ----------------

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;background:#e8edf4;overflow:hidden;font-family:"Microsoft YaHei","PingFang SC",sans-serif}
#stage{position:absolute;top:50%;left:50%;width:1280px;height:720px;transform-origin:center center}
.slide{position:absolute;width:1280px;height:720px;background:#f6f9fd;display:none;padding:56px 72px;
  box-shadow:0 8px 32px rgba(20,40,80,.18);border-radius:6px;overflow:hidden}
.slide.show{display:block}
.kicker{display:inline-block;font-size:24px;color:#1a4d8f;background:#e3edfb;padding:6px 18px;
  border-radius:20px;margin-bottom:14px;font-weight:700}
h1{font-size:52px;color:#143a6e;line-height:1.3}
h2{font-size:38px;color:#143a6e;margin-bottom:8px}
.body{margin-top:18px}
.item{font-size:26px;line-height:1.6;color:#26303e;opacity:0;transform:translateY(22px);
  animation:rise .55s ease forwards;margin-bottom:10px}
@keyframes rise{to{opacity:1;transform:none}}
.bullet{font-size:26px;line-height:1.65;color:#26303e;display:flex;gap:12px;margin-bottom:10px;
  opacity:0;transform:translateX(-14px);animation:slidein .5s ease forwards}
@keyframes slidein{to{opacity:1;transform:none}}
.dot{flex:0 0 auto;width:12px;height:12px;border-radius:50%;background:#e8a33d;margin-top:13px}
/* 学习目标四类卡片 */
.goal-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:14px}
.goal-card{background:#fff;border-radius:12px;padding:16px 20px;box-shadow:0 2px 10px rgba(20,40,80,.08);
  border-top:6px solid #1a4d8f}
.goal-card:nth-child(2){border-top-color:#e8a33d}
.goal-card:nth-child(3){border-top-color:#2a9d6b}
.goal-card:nth-child(4){border-top-color:#c0432f}
.goal-h{font-size:26px;color:#1a4d8f;font-weight:700;margin-bottom:8px}
/* 封面 */
.cover-slide{background:linear-gradient(135deg,#143a6e 0%,#1a4d8f 55%,#2a6db5 100%);color:#fff}
.cover{display:flex;flex-direction:column;justify-content:center;height:100%}
.cover-badge{font-size:26px;color:#ffd98a;border:2px solid #ffd98a;display:inline-block;padding:8px 22px;
  border-radius:28px;width:max-content;margin-bottom:28px}
.cover h1{color:#fff;margin-bottom:22px}
.cover-info{font-size:26px;line-height:1.9;color:#e8eef8}
/* 目录 */
.agenda-item{display:flex;align-items:center;gap:18px;font-size:27px;padding:9px 6px;color:#26303e}
.agenda-item span{flex:0 0 44px;height:44px;border-radius:10px;background:#1a4d8f;color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:700;font-size:22px}
/* 基本信息 */
.kv-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px 30px}
.kv{background:#fff;border-left:6px solid #1a4d8f;border-radius:8px;padding:14px 20px;box-shadow:0 2px 8px rgba(20,40,80,.08)}
.kv .k{font-size:24px;color:#6b7686;display:block;margin-bottom:4px}
.kv .v{font-size:28px;color:#143a6e;font-weight:700}
/* 测试题 */
.quiz{margin-bottom:16px;background:#fff;border-radius:10px;padding:16px 22px;box-shadow:0 2px 8px rgba(20,40,80,.07)}
.q-text{font-size:26px;color:#143a6e;font-weight:700;margin-bottom:10px}
.opt{display:inline-block;font-size:24px;padding:8px 18px;margin:4px 8px 4px 0;border:2px solid #b9c8dd;
  background:#fff;border-radius:8px;cursor:pointer;color:#26303e;transition:.15s}
.opt:hover{border-color:#1a4d8f}
.opt.right{background:#d9f2e3;border-color:#1f9d61;color:#14613a}
.opt.wrong{background:#fde5e5;border-color:#d0453e;color:#8c2b26}
.opt:disabled{cursor:default;opacity:.75}
.q-feedback{font-size:24px;margin-top:8px;color:#1f6f43;min-height:30px}
.quiz-body .item{animation-delay:0s !important}
.hint{font-size:24px;color:#8b94a3;margin-top:8px}
/* 知识图谱模拟 */
.sim-desc{font-size:24px;color:#6b7686;margin-bottom:16px}
.kp-cloud{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:20px}
.kp-node{font-size:25px;padding:12px 22px;border-radius:26px;background:#fff;border:2px solid #1a4d8f;
  color:#1a4d8f;cursor:pointer;transition:.18s}
.kp-node:hover{background:#e3edfb}
.kp-node.active{background:#1a4d8f;color:#fff}
.kp-detail{font-size:25px;background:#fff;border-radius:10px;padding:16px 22px;color:#26303e;
  box-shadow:0 2px 8px rgba(20,40,80,.07);min-height:60px;line-height:1.6}
/* 教学流程模拟 */
.f-stage{background:#fff;border-radius:12px;padding:22px 28px;box-shadow:0 2px 8px rgba(20,40,80,.07)}
.f-progress{display:flex;gap:10px;margin-bottom:16px}
.f-dot{flex:1;height:8px;border-radius:4px;background:#d5dfec;transition:.3s}
.f-dot.on{background:#e8a33d}
.f-view{min-height:150px}
.f-card{display:none;font-size:26px;line-height:1.7;color:#26303e}
.f-card.on{display:block;animation:rise .4s ease}
.f-card h3{font-size:28px;color:#1a4d8f;margin-bottom:8px}
.f-ctl{display:flex;gap:14px;margin-top:14px}
.f-btn{font-size:25px;padding:10px 26px;border-radius:8px;border:2px solid #b9c8dd;background:#fff;
  cursor:pointer;color:#26303e}
.f-btn.primary{background:#1a4d8f;border-color:#1a4d8f;color:#fff}
.f-tip{font-size:24px;color:#8b94a3;margin-top:10px}
/* 日历 */
.cal-wrap{max-height:470px;overflow:auto;margin-top:14px;border:1px solid #d5dfec;border-radius:8px}
table.cal{border-collapse:collapse;width:100%;font-size:24px}
table.cal th{background:#1a4d8f;color:#fff;padding:8px 10px;position:sticky;top:0}
table.cal td{border:1px solid #d5dfec;padding:7px 10px;color:#26303e;text-align:center}
table.cal tr:nth-child(even){background:#eef4fb}
/* 进度条 */
#progress{position:fixed;left:0;top:0;height:5px;background:#e8a33d;width:0;z-index:99;transition:.25s}
#pageno{position:fixed;right:22px;bottom:16px;font-size:22px;color:#6b7686;z-index:99;
  background:rgba(255,255,255,.85);padding:4px 14px;border-radius:14px}
#navHint{position:fixed;left:22px;bottom:16px;font-size:20px;color:#8b94a3;z-index:99}
"""

JS = """
const stage=document.getElementById('stage');
const slides=[...document.querySelectorAll('.slide')];
let cur=0;
function layout(){const s=Math.min(innerWidth/1280,innerHeight/720);
  stage.style.transform='translate(-50%,-50%) scale('+s+')';}
addEventListener('resize',layout);
function show(i){cur=Math.max(0,Math.min(slides.length-1,i));
  slides.forEach((s,k)=>{s.classList.toggle('show',k===cur);});
  document.getElementById('progress').style.width=((cur+1)/slides.length*100)+'%';
  document.getElementById('pageno').textContent=(cur+1)+' / '+slides.length;
  if(cur===slides.length-1){document.getElementById('navHint').textContent='已到最后一页';}
  else{document.getElementById('navHint').textContent='点击或按 空格/回车/→ 翻页';}}
function next(){if(cur<slides.length-1)show(cur+1);}
function prev(){if(cur>0)show(cur-1);}
addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '||e.key==='Enter'){e.preventDefault();next();}
  else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){e.preventDefault();prev();}});
document.addEventListener('click',e=>{
  if(e.target.closest('.opt,.kp-node,.f-btn'))return; // 交互元素不翻页
  if(!e.target.closest('.slide'))return; next();});
/* --- 测试题（面向学生：作答后给出判定与解析反馈） --- */
document.querySelectorAll('.quiz').forEach(qz=>{
  const expEl=qz.querySelector('.q-explain');
  const expText=expEl?expEl.textContent:'';
  qz.querySelectorAll('.opt').forEach(btn=>{
    btn.addEventListener('click',()=>{
      if(qz.dataset.done)return; qz.dataset.done='1';
      const ok=btn.dataset.ok==='1'; const fb=qz.querySelector('.q-feedback');
      qz.querySelectorAll('.opt').forEach(b=>{b.disabled=true;if(b.dataset.ok==='1')b.classList.add('right');});
      if(!ok){btn.classList.add('wrong');
        fb.textContent='❌ 回答不正确。'+expText;}
      else{fb.textContent='✅ 回答正确！'+expText;}});});});
/* --- 知识图谱模拟 --- */
const kpDetail=document.getElementById('kpDetail');
if(kpDetail){const nodes=document.querySelectorAll('.kp-node');
  nodes.forEach(n=>{n.addEventListener('click',()=>{
    nodes.forEach(x=>x.classList.remove('active'));n.classList.add('active');
    kpDetail.textContent='【'+n.textContent+'】—— 本课次教学内容的重要知识点，可结合教学设计文档中“内容与资源”部分深入理解；点击其他节点继续探索该知识点图谱。';});});}
/* --- 教学流程模拟 --- */
const fNext=document.getElementById('fNext'),fPrev=document.getElementById('fPrev');
if(fNext){const cards=document.querySelectorAll('.f-card'),dots=document.querySelectorAll('.f-dot');
  let fi=0;const tip=document.getElementById('fTip');
  function fshow(){cards.forEach((c,i)=>c.classList.toggle('on',i===fi));
    dots.forEach((d,i)=>d.classList.toggle('on',i<=fi));
    tip.textContent='当前环节：'+(cards[fi]?cards[fi].querySelector('h3').textContent:'')+'（'+(fi+1)+'/'+cards.length+'）';
    fPrev.disabled=fi===0;}
  fNext.addEventListener('click',()=>{if(fi<cards.length-1){fi++;fshow();}});
  fPrev.addEventListener('click',()=>{if(fi>0){fi--;fshow();}});
  fshow();}
layout();show(0);
"""


def main():
    if len(sys.argv) < 2:
        print("用法：python gen_html_courseware.py <design_data.json> [输出目录]")
        return 1

    with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(sys.argv[1]))
    os.makedirs(out_dir, exist_ok=True)

    slides = build_html(data)
    cname = (data.get("basic_info", {}) or {}).get("course_name", "混合式教学设计")
    title = "混合式教学设计说课课件 - %s" % cname

    html_doc = (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n"
        "<div id=\"progress\"></div>\n<div id=\"stage\">\n%s\n</div>\n"
        "<div id=\"pageno\"></div>\n<div id=\"navHint\"></div>\n"
        "<script>%s</script>\n</body>\n</html>" % (esc(title), CSS, "\n".join(slides), JS)
    )

    out = os.path.join(out_dir, "混合式教学设计说课课件.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print("已生成：%s（共 %d 页）" % (out, len(slides)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
