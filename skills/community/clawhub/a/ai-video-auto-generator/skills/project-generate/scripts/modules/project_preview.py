"""
交互式 HTML 预览模块 — 生成 shot 首帧图和视频状态的预览页面。

支持：
- 点击放大（overlay 遮罩）
- shot_groups 分组显示
- 视频状态徽章（绿色=完成，灰色=待处理）
- 模型标签
"""

import base64
import json
import os
from typing import Any


def _load_script(project: str) -> tuple[dict[str, Any], str]:
    script_path = os.path.join(project, "script.json")
    if not os.path.isfile(script_path):
        raise SystemExit(f"未找到 script.json: {script_path}")
    with open(script_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    proj_name = data.get("script", {}).get("title", os.path.basename(os.path.abspath(os.path.normpath(project))))
    return data, proj_name


def _get_img_b64(project: str, final: str) -> tuple[str, bool]:
    """返回 (base64字符串, 是否存在)"""
    img_path = final if os.path.isabs(final) else os.path.join(project, final)
    if not os.path.isfile(img_path):
        return "", False
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode(), True


def _check_video_status(project: str, sid: int) -> str:
    """检查视频文件是否存在，返回状态文本"""
    v_path = os.path.join(project, "videos", f"shot_{sid:02d}.mp4")
    if os.path.isfile(v_path):
        return "done"
    # 检查 stitches 目录
    s_path = os.path.join(project, "stitches", f"shot_{sid:02d}.mp4")
    if os.path.isfile(s_path):
        return "done"
    return "pending"


def generate_preview(project: str, out_path: str | None = None) -> str:
    """生成交互式 HTML 预览页面，返回页面文件路径。"""
    data, proj_name = _load_script(project)
    shots = data.get("shots", [])
    shot_groups = data.get("shot_groups", [])

    # 收集每个 shot 的数据
    shot_data_map: dict[int, dict] = {}
    for shot in shots:
        sid = shot["id"]
        ff = shot.get("first_frame")
        if not ff or not isinstance(ff, dict):
            shot_data_map[sid] = {
                "id": sid,
                "desc": shot.get("description", ""),
                "has_img": False,
                "img_b64": "",
                "model": "-",
                "video_status": _check_video_status(project, sid),
            }
            continue

        final = ff.get("final", "")
        img_b64, has_img = _get_img_b64(project, final)
        model = ff.get("model", "?")
        shot_data_map[sid] = {
            "id": sid,
            "desc": shot.get("description", ""),
            "has_img": has_img,
            "img_b64": img_b64,
            "model": model,
            "video_status": _check_video_status(project, sid),
        }

    # 构建 HTML
    def _render_shot_card(sd: dict) -> str:
        vid_badge = ""
        vid_html = ""
        if sd["video_status"] == "done":
            vid_badge = '<span class="badge badge-done">视频 ✅</span>'
            # 构造相对路径的视频标签
            v_rel = os.path.join("..", "videos", f"shot_{sd['id']:02d}.mp4")
            # 也检查 stitches 目录
            v_stitch = os.path.join("..", "stitches", f"shot_{sd['id']:02d}.mp4")
            v_src = v_rel if os.path.isfile(os.path.join(project, "videos", f"shot_{sd['id']:02d}.mp4")) else v_stitch
            if os.path.isfile(os.path.join(project, os.path.normpath(v_src))):
                vid_html = (
                    f'<video class="vid-preview" src="{v_src}" controls preload="none" '
                    f'poster="data:image/png;base64,{sd["img_b64"]}">'
                    f'</video>'
                )
        else:
            vid_badge = '<span class="badge badge-pending">视频 ⏳</span>'

        img_html = ""
        if sd["has_img"]:
            img_html = (
                f'<div class="img-wrap" onclick="openZoom(this)">'
                f'<img src="data:image/png;base64,{sd["img_b64"]}" loading="lazy">'
                f'</div>'
            )
        else:
            img_html = '<div class="no-img">❌ 无首帧图</div>'

        return f"""<div class="shot-card">
  <div class="shot-header">
    <span class="shot-id">Shot {sd["id"]:02d}</span>
    <span class="model-tag">{sd["model"]}</span>
    {vid_badge}
  </div>
  {img_html}
  {vid_html}
  <div class="shot-desc">{sd["desc"]}</div>
</div>"""

    groups_html = ""

    if shot_groups:
        for g_idx, group in enumerate(shot_groups):
            g_name = group.get("name", f"组 {g_idx + 1}")
            transition = group.get("transition", "")
            group_shots = group.get("shots", [])
            cards = []
            for sid in group_shots:
                if sid in shot_data_map:
                    cards.append(_render_shot_card(shot_data_map[sid]))
            if not cards:
                continue

            groups_html += f"""<div class="group">
  <div class="group-header">
    <span class="group-name">{g_name}</span>
    <span class="group-transition">{transition}</span>
    <span class="group-count">{len(cards)} 个镜头</span>
  </div>
  <div class="group-grid">{''.join(cards)}</div>
</div>"""
    else:
        # 无分组，按 shots 顺序全部显示
        cards = []
        for shot in shots:
            sid = shot["id"]
            if sid in shot_data_map:
                cards.append(_render_shot_card(shot_data_map[sid]))
        groups_html = f"""<div class="group">
  <div class="group-header">
    <span class="group-name">全部镜头</span>
    <span class="group-count">{len(cards)} 个镜头</span>
  </div>
  <div class="group-grid">{''.join(cards)}</div>
</div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{proj_name} — 交互式预览</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0f0f1a; color: #e0e0e0; font-family: -apple-system, 'Microsoft YaHei', sans-serif; padding: 20px; }}
h1 {{ text-align: center; color: #fff; font-size: 22px; margin-bottom: 8px; }}
.subtitle {{ text-align: center; color: #888; font-size: 13px; margin-bottom: 24px; }}

/* Group */
.group {{ margin-bottom: 28px; }}
.group-header {{ display: flex; align-items: center; gap: 12px; padding: 8px 12px; background: #1a1a2e; border-radius: 8px; margin-bottom: 10px; }}
.group-name {{ color: #e94560; font-weight: bold; font-size: 14px; }}
.group-transition {{ color: #e9c46a; font-size: 12px; }}
.group-count {{ color: #888; font-size: 12px; margin-left: auto; }}
.group-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }}

/* Shot card */
.shot-card {{ background: #16213e; border-radius: 10px; overflow: hidden; transition: transform 0.2s; }}
.shot-card:hover {{ transform: translateY(-2px); }}
.shot-header {{ display: flex; align-items: center; gap: 8px; padding: 8px 10px; background: #0f3460; font-size: 13px; }}
.shot-id {{ color: #e94560; font-weight: bold; }}
.model-tag {{ background: #533483; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
.badge {{ padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: auto; }}
.badge-done {{ background: #1b5e20; color: #a5d6a7; }}
.badge-pending {{ background: #424242; color: #bdbdbd; }}

/* Image */
.img-wrap {{ cursor: pointer; line-height: 0; }}
.img-wrap img {{ width: 100%; display: block; }}
.no-img {{ padding: 50px 20px; text-align: center; color: #555; font-size: 13px; }}
.vid-preview {{ width: 100%; display: block; border-top: 1px solid #333; }}
.shot-desc {{ padding: 8px 10px; font-size: 12px; color: #ccc; line-height: 1.5; }}

/* Zoom overlay */
.zoom-overlay {{
  display: none;
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.9);
  z-index: 9999;
  justify-content: center; align-items: center;
  cursor: zoom-out;
}}
.zoom-overlay.active {{ display: flex; }}
.zoom-overlay img {{
  max-width: 95vw; max-height: 95vh;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 0 40px rgba(0,0,0,0.8);
}}
.stats {{ text-align: center; margin-top: 24px; padding: 12px; background: #1a1a2e; border-radius: 8px; font-size: 13px; color: #888; }}
.stats span {{ margin: 0 10px; }}
</style>
</head>
<body>

<div class="zoom-overlay" id="zoomOverlay" onclick="closeZoom()">
  <img id="zoomImg" src="" alt="zoom">
</div>

<h1>{proj_name}</h1>
<p class="subtitle">交互式预览 — 点击图片放大</p>

{groups_html}

<div class="stats">
  <span>📸 总计 {len(shots)} 个 shot</span>
  <span>🎬 分组: {len(shot_groups)}</span>
</div>

<script>
function openZoom(el) {{
  var img = el.querySelector('img');
  if (!img) return;
  document.getElementById('zoomImg').src = img.src;
  document.getElementById('zoomOverlay').classList.add('active');
}}
function closeZoom() {{
  document.getElementById('zoomOverlay').classList.remove('active');
}}
document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape') closeZoom();
}});
</script>

</body>
</html>"""

    if out_path is None:
        out_path = os.path.join(project, "output", "preview.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path
