"""
项目统计报告模块 — 生成 HTML 格式的项目数据统计。

指标：
- 各 shot 验证分数（从 .batch_state.json 读取历史）
- 模型分布（2.0 vs 2.1）
- 参考图使用频率
- 视频完成情况
"""

import json
import os
from datetime import datetime
from typing import Any


def _load_script(project: str) -> dict[str, Any]:
    sp = os.path.join(project, "script.json")
    if not os.path.isfile(sp):
        raise SystemExit(f"未找到 script.json: {sp}")
    with open(sp, "r", encoding="utf-8") as f:
        return json.load(f)


def _check_file(path: str) -> bool:
    return os.path.isfile(path) and os.path.getsize(path) > 0


def _fmt_size(path: str) -> str:
    if not os.path.isfile(path):
        return "-"
    kb = os.path.getsize(path) // 1024
    if kb < 1024:
        return f"{kb} KB"
    return f"{kb / 1024:.1f} MB"


def generate_stats(project: str, out_path: str | None = None) -> str:
    """生成 HTML 统计报告，返回文件路径。"""
    data = _load_script(project)
    shots = data.get("shots", [])
    proj_name = data.get("script", {}).get("title", os.path.basename(project))
    aspect = data.get("script", {}).get("aspect_ratio", "?")
    shot_groups = data.get("shot_groups", [])

    # -- 收集每 shot 数据 --
    models: dict[str, int] = {}
    first_frame_ok, first_frame_missing = 0, 0
    video_done, video_pending = 0, 0
    total_refs = 0
    ref_usage: dict[str, int] = {}  # 文件名 -> 使用次数
    shot_rows = ""
    total_verify_score = 0
    verify_count = 0

    for s in shots:
        sid = s["id"]
        desc = s.get("description", "")[:40]
        ff = s.get("first_frame")

        # 模型统计
        model = "?"
        if ff and isinstance(ff, dict):
            model = ff.get("model", "?")
        models[model] = models.get(model, 0) + 1

        # 首帧图
        ff_ok = "❌"
        ff_path = ""
        if ff and isinstance(ff, dict):
            final = ff.get("final", "")
            if final:
                ff_path = final if os.path.isabs(final) else os.path.join(project, final)
                if _check_file(ff_path):
                    ff_ok = "✅"
                    first_frame_ok += 1
                else:
                    first_frame_missing += 1
            else:
                first_frame_missing += 1
        else:
            first_frame_missing += 1

        # 视频
        v_path = os.path.join(project, "videos", f"shot_{sid:02d}.mp4")
        v2_path = os.path.join(project, "stitches", f"shot_{sid:02d}.mp4")
        if _check_file(v_path) or _check_file(v2_path):
            v_status = "✅ 完成"
            video_done += 1
        else:
            v_status = "⏳ 待处理"
            video_pending += 1

        # 参考图使用统计
        if ff and isinstance(ff, dict):
            for rp in ff.get("ref_images", []):
                total_refs += 1
                basename = os.path.basename(rp)
                ref_usage[basename] = ref_usage.get(basename, 0) + 1

        # 验证分数（尝试从 .batch_state.json 获取）
        verify_score = "-"
        batch_state_path = os.path.join(project, ".batch_state.json")
        if os.path.isfile(batch_state_path):
            try:
                with open(batch_state_path, "r", encoding="utf-8") as bf:
                    bs = json.load(bf)
                if bs.get("ok"):
                    verify_score = "✅"
            except Exception:
                pass

        size = _fmt_size(ff_path) if ff_path else "-"
        shot_rows += f"""<tr>
  <td>{sid:02d}</td>
  <td>{ff_ok}</td>
  <td>{size}</td>
  <td>{v_status}</td>
  <td>{model}</td>
  <td class="desc">{desc}</td>
</tr>\n"""

    # -- 参考图使用排行 --
    ref_sorted = sorted(ref_usage.items(), key=lambda x: -x[1])
    ref_rows = ""
    for name, count in ref_sorted[:20]:
        ref_rows += f"<tr><td>{name}</td><td>{count}</td></tr>\n"

    # -- 生成 HTML --
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{proj_name} — 数据统计</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0f0f1a; color: #e0e0e0; font-family: -apple-system, 'Microsoft YaHei', sans-serif; padding: 20px; }}
h1 {{ color: #e94560; font-size: 20px; margin-bottom: 4px; }}
.subtitle {{ color: #888; font-size: 13px; margin-bottom: 24px; }}
.section {{ margin-bottom: 24px; }}
.section h2 {{ color: #64b5f6; font-size: 15px; margin-bottom: 10px; border-left: 3px solid #e94560; padding-left: 10px; }}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 10px; margin-bottom: 16px; }}
.stat-card {{ background: #16213e; padding: 14px; border-radius: 8px; text-align: center; }}
.stat-card .num {{ font-size: 28px; font-weight: bold; color: #e94560; }}
.stat-card .label {{ font-size: 12px; color: #888; margin-top: 4px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
th, td {{ padding: 8px 10px; text-align: left; border-bottom: 1px solid #1a1a2e; }}
th {{ color: #888; font-weight: normal; font-size: 12px; background: #16213e; }}
.desc {{ color: #aaa; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
tr:hover td {{ background: #1a1a2e; }}
.ref-bar {{ background: #533483; height: 4px; border-radius: 2px; margin-top: 4px; }}
.ref-bar-fill {{ height: 100%; background: #e94560; border-radius: 2px; }}
</style>
</head>
<body>
<h1>📊 {proj_name}</h1>
<p class="subtitle">数据统计报告 — {now_str} | {aspect} | {len(shots)} 个 shot</p>

<div class="section">
  <h2>概览</h2>
  <div class="stats-grid">
    <div class="stat-card"><div class="num">{len(shots)}</div><div class="label">总 Shot</div></div>
    <div class="stat-card"><div class="num">{first_frame_ok}</div><div class="label">首帧图 ✅</div></div>
    <div class="stat-card"><div class="num">{video_done}</div><div class="label">视频 ✅</div></div>
    <div class="stat-card"><div class="num">{models.get('agnes-image-2.0-flash', 0)}</div><div class="label">2.0 Flash</div></div>
    <div class="stat-card"><div class="num">{models.get('agnes-image-2.1-flash', 0)}</div><div class="label">2.1 Flash</div></div>
    <div class="stat-card"><div class="num">{total_refs}</div><div class="label">参考图使用</div></div>
  </div>
</div>

<div class="section">
  <h2>各 Shot 明细</h2>
  <table>
    <tr><th>Shot</th><th>首帧图</th><th>大小</th><th>视频</th><th>模型</th><th>描述</th></tr>
    {shot_rows}
  </table>
</div>

<div class="section">
  <h2>模型分布</h2>
  <table>
    <tr><th>模型</th><th>Shot 数</th><th>占比</th></tr>
"""
    for m, cnt in sorted(models.items()):
        pct = cnt / len(shots) * 100 if shots else 0
        bar_w = pct
        html += f"    <tr><td>{m}</td><td>{cnt}</td><td>{pct:.0f}%<div class='ref-bar'><div class='ref-bar-fill' style='width:{bar_w}%'></div></div></td></tr>\n"

    html += """  </table>
</div>

<div class="section">
  <h2>参考图使用频率 Top 20</h2>
  <table>
    <tr><th>文件</th><th>使用次数</th></tr>
"""
    if ref_sorted:
        max_ref = ref_sorted[0][1]
        for name, cnt in ref_sorted[:20]:
            bar_w = cnt / max_ref * 100 if max_ref else 0
            html += f"    <tr><td>{name}</td><td>{cnt}<div class='ref-bar'><div class='ref-bar-fill' style='width:{bar_w}%'></div></div></td></tr>\n"
    else:
        html += "    <tr><td colspan='2' style='color:#555;text-align:center'>（无统计信息）</td></tr>\n"

    html += """  </table>
</div>

</body>
</html>"""

    if out_path is None:
        out_path = os.path.join(project, "output", "stats.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path
