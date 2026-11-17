"""新旧首帧图 side-by-side + 滑块对比 HTML 生成。"""
import os, re, sys
from datetime import datetime

def _generate_diff_html(project: str, shot: dict, old_path: str, new_path: str) -> str:
    """生成 side-by-side 新旧对比 HTML 页面，返回文件路径。"""
    import base64

    sid = shot["id"]
    desc = shot.get("description", "")

    def _b64(p: str) -> str:
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()

    old_b64 = _b64(old_path)
    new_b64 = _b64(new_path)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shot {sid:02d} — 新旧对比</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0f0f1a; color: #e0e0e0; font-family: -apple-system, 'Microsoft YaHei', sans-serif; padding: 20px; }}
h1 {{ text-align: center; font-size: 20px; margin-bottom: 6px; }}
.desc {{ text-align: center; color: #888; font-size: 13px; margin-bottom: 20px; }}
.compare {{ display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }}
.panel {{ flex: 1; min-width: 300px; max-width: 600px; }}
.panel h2 {{ text-align: center; font-size: 14px; padding: 8px; border-radius: 6px 6px 0 0; }}
.panel.old h2 {{ background: #5c2e2e; color: #ef9a9a; }}
.panel.new h2 {{ background: #2e5c2e; color: #a5d6a7; }}
.panel img {{ width: 100%; display: block; border-radius: 0 0 6px 6px; }}
.controls {{ text-align: center; margin-top: 16px; }}
.controls button {{ background: #1a1a2e; color: #e0e0e0; border: 1px solid #333; padding: 8px 20px; border-radius: 6px; cursor: pointer; font-size: 13px; }}
.controls button:hover {{ background: #16213e; }}
.slider-container {{ position: relative; max-width: 600px; margin: 0 auto; }}
.slider-container img {{ width: 100%; display: block; }}
.slider-overlay {{ position: absolute; top: 0; left: 0; width: 50%; height: 100%; overflow: hidden; border-right: 2px solid #e94560; }}
.slider-overlay img {{ display: block; }}
.slider-handle {{ position: absolute; top: 0; left: 50%; width: 4px; height: 100%; background: #e94560; cursor: ew-resize; z-index: 10; }}
</style>
</head>
<body>
<h1>Shot {sid:02d} — 新旧对比</h1>
<p class="desc">{desc}</p>

<div class="controls">
  <button onclick="showMode('side-by-side')">并排对比</button>
  <button onclick="showMode('slider')">滑块对比</button>
</div>

<div id="mode-side-by-side" class="compare">
  <div class="panel old">
    <h2>旧版 (之前)</h2>
    <img src="data:image/png;base64,{old_b64}" alt="旧版">
  </div>
  <div class="panel new">
    <h2>新版 (现在)</h2>
    <img src="data:image/png;base64,{new_b64}" alt="新版">
  </div>
</div>

<div id="mode-slider" class="slider-container" style="display:none">
  <img src="data:image/png;base64,{new_b64}" alt="新版">
  <div class="slider-overlay" id="sliderOverlay">
    <img src="data:image/png;base64,{old_b64}" alt="旧版">
  </div>
  <div class="slider-handle" id="sliderHandle"></div>
</div>

<script>
function showMode(mode) {{
  document.getElementById('mode-side-by-side').style.display = mode === 'side-by-side' ? 'flex' : 'none';
  document.getElementById('mode-slider').style.display = mode === 'slider' ? 'block' : 'none';
}}

var slider = document.querySelector('.slider-container');
var overlay = document.getElementById('sliderOverlay');
var handle = document.getElementById('sliderHandle');
var dragging = false;

slider.addEventListener('mousedown', function(e) {{ dragging = true; moveSlider(e); }});
document.addEventListener('mousemove', function(e) {{ if (dragging) moveSlider(e); }});
document.addEventListener('mouseup', function() {{ dragging = false; }});

slider.addEventListener('touchstart', function(e) {{ dragging = true; moveSlider(e.touches[0]); }});
document.addEventListener('touchmove', function(e) {{ if (dragging) moveSlider(e.touches[0]); }});
document.addEventListener('touchend', function() {{ dragging = false; }});

function moveSlider(e) {{
  var rect = slider.getBoundingClientRect();
  var x = e.clientX - rect.left;
  if (x < 0) x = 0;
  if (x > rect.width) x = rect.width;
  var pct = (x / rect.width * 100).toFixed(1);
  overlay.style.width = pct + '%';
  handle.style.left = pct + '%';
}}
</script>
</body>
</html>"""
    out_path = os.path.join(project, "output", f"shot_{sid:02d}_diff.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path



