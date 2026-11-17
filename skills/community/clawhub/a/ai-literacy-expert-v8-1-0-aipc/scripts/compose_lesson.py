"""
compose_lesson.py - 闃舵 4锛氬悎鎴愭渶缁堟暀瀛氦浠樼墿銆?

对应 video-editing-skills-main/scripts/compose_video.py锛屾妸"ffmpeg 瑙嗛鍚堟垚"
閲嶆槧灏勪负"Markdown 课件 + 评估题?+ HTML 浜掑姩课件渲染"銆?

绔簯鍗忓悓绾潫锛圴7 搂2.4锛夛細
  浜戠鍙繑鍥?lesson_plan.json锛堝喅绛栵級锛屾墍鏈夋覆鏌撳湪绔晶鎵銆?

娴佺锛?
  1. load_lesson_plan(plan_path) 瑙e瀽浜戠杩斿洖鐨?lesson_plan.json
  2. lesson_plan_guard.validate_lesson_plan() 校验锛? 椤圭‖瑙勫垯锛?
  3. 校验通过 鈫?render_markdown / render_assessment / render_courseware_html
  4. 校验澶辫触 鈫?鎷掔粷鍚堟垚锛岃緭鍑洪敊璇姤鍛?

鐢硶锛?
    python scripts/compose_lesson.py \\
        --blueprint "<workspace>/lesson_plan.json" \\
        --output "<workspace>/final_lesson.md" \\
        --candidates "<workspace>/candidate_knowledge.json" \\
        --assessment "<workspace>/assessment.json" \\
        --html "<workspace>/courseware.html"
"""
from __future__ import annotations
__version__ = "8.1.0-aipc"  # V8.1-AIPC: 每次工作自动输出本地/云端对比 + 全互动控件完整性门控


# --- UTF-8 stdout/stderr (Windows 涓枃杈撳嚭闃蹭贡鐮? -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from lesson_plan_guard import RuleConfig, render_error_report, validate_lesson_plan


# ---------------------------------------------------------------------------
# 加载 lesson_plan
# ---------------------------------------------------------------------------

def load_lesson_plan(plan_path: Path) -> dict:
    """解析云端返回的 lesson_plan.json."""
    if not plan_path.exists():
        raise FileNotFoundError(f"lesson_plan 不存在: {plan_path}")
    try:
        return json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"lesson_plan JSON 解析失败: {e}") from e


def load_candidates(candidates_path: Optional[Path]) -> Optional[dict]:
    """加载 candidate_knowledge.json (可选, 用于 HTML 关联原始片段)."""
    if candidates_path is None or not candidates_path.exists():
        return None
    try:
        return json.loads(candidates_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Markdown 课件渲染
# ---------------------------------------------------------------------------

def render_markdown(plan: dict, candidates: Optional[dict] = None) -> str:
    """渲染 final_lesson.md (含教学目标/知识点/教学法/互动设计)."""
    lines: list[str] = []

    title = plan.get("lesson_title") or plan.get("title") or "AI 通识课教案"
    lines.append(f"# {title}")
    lines.append("")

    # 教学法
    method = plan.get("pedagogy_method") or plan.get("teaching_method") or "未指定"
    lines.append(f"**教法**: {method}")
    total_duration = _calc_total_duration(plan)
    if total_duration:
        lines.append(f"**预计时长**: {_format_duration(total_duration)}")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # 教学目标
    objectives = _get_learning_objectives(plan)
    if objectives:
        lines.append("## 教学目标")
        lines.append("")
        for i, obj in enumerate(objectives, 1):
            lines.append(f"{i}. {obj}")
        lines.append("")

    # 知识点
    kps = _get_knowledge_points(plan)
    if kps:
        lines.append("## 知识点")
        lines.append("")
        for kp in kps:
            lines.append(f"- {kp}")
        lines.append("")

    # 教学环节
    clips = _get_clips(plan)
    if clips:
        lines.append("## 教学环节")
        lines.append("")
        for i, clip in enumerate(clips, 1):
            seq = clip.get("sequence_order", i)
            kp = clip.get("knowledge_point", clip.get("topic", ""))
            difficulty = clip.get("difficulty", "")
            duration = _get_clip_duration_sec(clip)
            voiceover = clip.get("voiceover") or {}
            text = voiceover.get("text", "") if isinstance(voiceover, dict) else str(voiceover)
            transition = clip.get("transition") or {}
            trans_type = transition.get("type", "") if isinstance(transition, dict) else ""

            lines.append(f"### 环节 {seq}: {kp}")
            if difficulty:
                lines.append(f"- **难度**: {difficulty}")
            if duration:
                lines.append(f"- **时长**: {_format_duration(duration)}")
            if trans_type:
                lines.append(f"- **过渡**: {trans_type}")
            if text:
                lines.append("")
                lines.append(f"> {text}")
            lines.append("")

    # 互动设计
    interaction = plan.get("interaction_design") or plan.get("interaction")
    if interaction:
        lines.append("## 互动设计")
        lines.append("")
        if isinstance(interaction, str):
            lines.append(interaction)
        elif isinstance(interaction, list):
            for item in interaction:
                lines.append(f"- {item}")
        elif isinstance(interaction, dict):
            for k, v in interaction.items():
                lines.append(f"- **{k}**: {v}")
        lines.append("")

    # 评估说明
    assessment = _get_assessment(plan)
    if assessment:
        questions = assessment.get("questions", []) if isinstance(assessment, dict) else []
        if questions:
            lines.append("## 评估")
            lines.append("")
            lines.append(f"共 {len(questions)} 题, 详见 assessment.json.")
            lines.append("")

    lines.append("---")
    lines.append("*本教案由 ai-literacy-expert-v8-aipc 端云协同工作流生成 (本地 DeepSeek-R1-1.5B 推理 + 云端轻决策 + work_summary 自动报告 + p5.js 按钮完整性门控).*")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# assessment.json 渲染
# ---------------------------------------------------------------------------

def render_assessment(plan: dict) -> dict:
    """渲染 assessment.json(含选择题/简答题/答案)."""
    assessment = _get_assessment(plan)
    if not assessment:
        return {
            "assessment_id": f"asm-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "questions": [],
            "note": "lesson_plan 涓棤 assessment 瀛楁",
        }

    questions = assessment.get("questions", []) if isinstance(assessment, dict) else []
    # 鏍囧噯鍖栨瘡题樼粨鏋?
    standardized: list[dict] = []
    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            continue
        standardized.append({
            "id": q.get("id", f"Q{i + 1}"),
            "type": q.get("type", "short_answer"),
            "question": q.get("question", q.get("stem", "")),
            "options": q.get("options", []),
            "answer": q.get("answer", ""),
            "explanation": q.get("explanation", ""),
            "difficulty": q.get("difficulty", 2),
            "knowledge_point": q.get("knowledge_point", ""),
        })

    return {
        "assessment_id": f"asm-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "total_questions": len(standardized),
        "questions": standardized,
    }


# ---------------------------------------------------------------------------
# HTML 浜掑姩课件渲染锛坧5.js锛屽彲閫夛級
# ---------------------------------------------------------------------------

def render_courseware_html(plan: dict, candidates: Optional[dict] = None) -> str:
    """渲染 courseware.html(p5.js 互动课件框架).

    生成一个可交互的知识点浏览页面, 每个知识点对应一个 p5.js canvas 卡片.
    """
    title = plan.get("lesson_title", "AI 通识课互动课件")
    kps = _get_knowledge_points(plan)
    clips = _get_clips(plan)

    cards_json = json.dumps(
        [
            {
                "title": c.get("knowledge_point", c.get("topic", f"环节{i}")),
                "difficulty": c.get("difficulty", 2),
                "text": (c.get("voiceover") or {}).get("text", "") if isinstance(c.get("voiceover"), dict) else "",
            }
            for i, c in enumerate(clips)
        ],
        ensure_ascii=False,
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<style>
body {{ font-family: "Microsoft YaHei", sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
h1 {{ color: #333; }}
#cards {{ display: flex; flex-wrap: wrap; gap: 16px; }}
.card {{ background: white; border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 300px; }}
.card h3 {{ margin-top: 0; color: #2196F3; }}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; background: #E3F2FD; color: #1976D2; font-size: 12px; }}
</style>
</head>
<body>
<h1>{title}</h1>
<div id="cards"></div>
<script>
const cards = {cards_json};
function setup() {{
  noCanvas();
  const container = document.getElementById('cards');
  cards.forEach((card, i) => {{
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `<h3>${{card.title}}</h3>
      <span class="badge">闅惧害 L${{card.difficulty}}</span>
      <p>${{card.text || ''}}</p>`;
    container.appendChild(div);
  }});
}}
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# 杈呭姪鍑芥暟
# ---------------------------------------------------------------------------

def _get_clips(plan: dict) -> list[dict]:
    if not isinstance(plan, dict):
        return []
    clips = plan.get("clips")
    if isinstance(clips, list):
        return [c for c in clips if isinstance(c, dict)]
    lessons = plan.get("lessons")
    if isinstance(lessons, list):
        out = []
        for l in lessons:
            if isinstance(l, dict) and isinstance(l.get("clips"), list):
                out.extend(c for c in l["clips"] if isinstance(c, dict))
        return out
    return []


def _get_knowledge_points(plan: dict) -> list[str]:
    if not isinstance(plan, dict):
        return []
    kps = plan.get("knowledge_points") or plan.get("knowledge_point") or []
    if isinstance(kps, str):
        return [kps]
    if isinstance(kps, list):
        return [str(k) for k in kps if k]
    return []


def _get_learning_objectives(plan: dict) -> list[str]:
    if not isinstance(plan, dict):
        return []
    for key in ("learning_objectives", "objectives", "goals"):
        v = plan.get(key)
        if isinstance(v, list):
            return [str(x) for x in v if x]
        if isinstance(v, str) and v.strip():
            import re
            return [c.strip() for c in re.split(r"[銆俓n;锛沒+", v) if c.strip()]
    return []


def _get_assessment(plan: dict) -> dict:
    if not isinstance(plan, dict):
        return {}
    a = plan.get("assessment")
    return a if isinstance(a, dict) else {}


def _get_clip_duration_sec(clip: dict) -> Optional[float]:
    for key in ("duration_sec", "duration_seconds", "duration"):
        if key in clip and clip[key] is not None:
            try:
                return float(clip[key])
            except (TypeError, ValueError):
                pass
    tc = clip.get("timecode") or {}
    if isinstance(tc, dict):
        try:
            ip = tc.get("in_point")
            op = tc.get("out_point")
            if ip is not None and op is not None:
                return float(op) - float(ip)
        except (TypeError, ValueError):
            pass
    return None


def _calc_total_duration(plan: dict) -> float:
    total = 0.0
    for clip in _get_clips(plan):
        d = _get_clip_duration_sec(clip)
        if d:
            total += d
    return total


def _format_duration(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}分{s}秒" if m else f"{s}秒"


# ---------------------------------------------------------------------------
# CLI 涓诲叆鍙?
# ---------------------------------------------------------------------------

def main() -> int:
    log = get_logger("compose")
    parser = argparse.ArgumentParser(description="闃舵 4锛氬悎鎴愭渶缁堟暀瀛氦浠樼墿")
    parser.add_argument("--blueprint", required=True, help="浜戠杩斿洖鐨?lesson_plan.json 璺緞")
    parser.add_argument("--output", required=True, help="杈撳嚭 final_lesson.md 璺緞")
    parser.add_argument("--candidates", default=None, help="candidate_knowledge.json 璺緞锛堝彲閫夛級")
    parser.add_argument("--assessment", default=None, help="杈撳嚭 assessment.json 璺緞锛堥粯璁?<output> 鍚岀洰褰曪級")
    parser.add_argument("--html", default=None, help="杈撳嚭 courseware.html 璺緞锛堝彲閫夛級")
    parser.add_argument(
        "--skip-guard",
        action="store_true",
        help="璺宠繃 lesson_plan_guard 校验锛堜粎璋冭瘯鐢紝涓嶆帹鑽愶級",
    )
    args = parser.parse_args()

    plan_path = Path(args.blueprint)
    output_path = Path(args.output)

    # 1. 加载 lesson_plan
    try:
        plan = load_lesson_plan(plan_path)
    except (FileNotFoundError, ValueError) as e:
        log.error(f"[compose] 鉁?{e}")
        return 1

    candidates = load_candidates(Path(args.candidates) if args.candidates else None)

    # 2. lesson_plan_guard 校验锛? 椤圭‖瑙勫垯锛?
    if not args.skip_guard:
        log.info("[compose] 鎵 lesson_plan_guard 校验锛? 椤圭‖瑙勫垯锛?..")
        passed, errors = validate_lesson_plan(plan, candidates, None)
        if not passed:
            log.error("[compose] 鉁?校验澶辫触锛屾嫆缁濆悎鎴愶細")
            log.error(render_error_report(errors))
            # 鍐欏嚭错误报告
            report_path = output_path.parent / "guard_errors.json"
            report_path.write_text(
                json.dumps({"passed": False, "errors": errors}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            log.error(f"[compose] 错误报告: {report_path}")
            return 1
        log.info("[compose] ✓ 校验通过")
    else:
        log.error("[compose] ⚠️ 已跳过 guard 校验 (--skip-guard)")

    # 3. 渲染 Markdown 课件
    md_content = render_markdown(plan, candidates)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md_content, encoding="utf-8")
    log.info(f"[compose] ✓ Markdown 课件: {output_path}")

    # 4. 渲染 assessment.json
    assessment_path = Path(args.assessment) if args.assessment else output_path.parent / "assessment.json"
    assessment_data = render_assessment(plan)
    assessment_path.write_text(
        json.dumps(assessment_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log.info(f"[compose] ✓ 评估题: {assessment_path} (共 {assessment_data.get('total_questions', 0)} 题)")

    # 5. 渲染 courseware.html (可选)
    if args.html:
        html_path = Path(args.html)
        html_content = render_courseware_html(plan, candidates)
        html_path.write_text(html_content, encoding="utf-8")
        log.info(f"[compose] ✓ 互动课件: {html_path}")

    log.info("[compose] ✓ 全部交付物已生成完毕.")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())

