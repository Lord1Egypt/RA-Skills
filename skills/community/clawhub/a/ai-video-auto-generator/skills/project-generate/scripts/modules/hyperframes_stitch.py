"""
Hyperframes 视频合成 — 替代 ffmpeg 的 stitch 模块。

从 script.json 读取 shot 数据、音频提示词、旁白，
生成 Hyperframes HTML 合成文件，调用 `npx hyperframes render` 输出最终视频。

依赖：
  - Node.js 22+（通过 managed runtime 或 PATH 查找）
  - FFmpeg 系统级安装（winget install FFmpeg / brew install ffmpeg / apt install ffmpeg）
  - hyperframes（通过 `npx hyperframes` 自动安装或已安装在 workspace）
"""
from __future__ import annotations
import json, os, shutil, subprocess, sys, time, glob
from typing import Any, Optional
from html import escape as _esc

from modules.config import _script_path
from stitch_base import BaseStitcher, StitcherRegistry


class HyperframesStitcher(BaseStitcher):
    name = "hyperframes"

    @staticmethod
    def check_available() -> bool:
        return _check_available()

    @staticmethod
    def run(project: str, shot_count: int = 0,
            script_config: Optional[dict] = None) -> Optional[str]:
        return _run_hf(project, script_config)

    @staticmethod
    def embed_to_doc(docx_token: str, video_path: str) -> str:
        return _embed_hf(docx_token, video_path)


StitcherRegistry.register(HyperframesStitcher)


# ── 运行时查找（路径即身份：从 __file__ 定位 skill_root）──

def _hf_skill_root() -> str:
    """从本文件位置向上找到 skill 根目录。"""
    try:
        from _paths import resolve_skill_root
        # 本文件在 <skill_root>/skills/project-generate/scripts/modules/
        # 向上 4 层即可
        cur = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)
        ))))
        return resolve_skill_root(cur)
    except Exception:
        # fallback: 系统 PATH
        return os.path.dirname(os.path.abspath(__file__))


def _find_node() -> str:
    """查找可用 node 可执行文件（优先 _paths.py 解析，纯路径驱动）。"""
    skill_root = _hf_skill_root()
    try:
        from _paths import resolve_tool
        exe = resolve_tool("node", skill_root)
        if exe and os.path.isfile(exe):
            return exe
    except ImportError:
        pass
    return shutil.which("node") or "node"


def _find_hf_cli(skill_root: str | None = None) -> str | None:
    """查找本地安装的 hyperframes CLI 入口。"""
    skill_root = skill_root or _hf_skill_root()
    try:
        from _paths import resolve_node_modules as _rnm
        nm = _rnm(skill_root)
        if nm:
            cli = os.path.join(nm, "hyperframes", "dist", "cli.js")
            if os.path.isfile(cli):
                return cli
    except ImportError:
        pass

    # legacy fallback（仅当有 legacy 标记）
    try:
        from _paths import has_legacy_marker
        if has_legacy_marker(skill_root):
            legacy = os.path.normpath(os.path.expanduser(
                "~/.workbuddy/binaries/node/workspace/node_modules"
            ))
            cli = os.path.join(legacy, "hyperframes", "dist", "cli.js")
            if os.path.isfile(cli):
                return cli
    except ImportError:
        pass

    return None
    return None


def _find_browser() -> tuple[Optional[str], str]:
    """
    解析 hyperframes/puppeteer 使用的浏览器可执行文件。
    优先级：环境变量 HYPERFRAMES_BROWSER_PATH / PUPPETEER_EXECUTABLE_PATH
            → Chrome for Testing（puppeteer 缓存，最稳）
            → 系统 Edge（兜底，本机 GPU 加速快但单实例架构，开着时秒退）。
    返回 (路径, 标签)；找不到返回 (None, "")。

    注意：本机系统 Edge 是单实例架构——当已有 Edge 在运行时，新 msedge.exe
    会把请求转交给已运行实例后自己以 Code:0 退出，puppeteer 拿不到调试端口 →
    回退 ffmpeg。故 Edge 仅在「没有其它 Edge 在运行」时可靠；需要用时先关掉 Edge。
    强制指定浏览器：设置 HYPERFRAMES_BROWSER_PATH 环境变量即可（见顶部逻辑）。
    """
    # 0) 环境变量优先（便于临时强制指定浏览器，如强制用 Edge）
    for _env_key in ("HYPERFRAMES_BROWSER_PATH", "PUPPETEER_EXECUTABLE_PATH"):
        _env_path = os.environ.get(_env_key, "")
        if _env_path and os.path.isfile(_env_path):
            _label = "Edge" if "edge" in _env_path.lower() else "Chrome (env)"
            return _env_path, _label

    # 1) Chrome for Testing（~/.cache/puppeteer/chrome/*/chrome-win64/chrome.exe）
    cache_root = os.path.normpath(os.path.expanduser("~/.cache/puppeteer/chrome"))
    candidates = glob.glob(os.path.join(cache_root, "*", "chrome-win64", "chrome.exe"))
    candidates += glob.glob(os.path.join(cache_root, "*", "chrome-linux64", "chrome"))
    candidates += glob.glob(os.path.join(cache_root, "*", "chrome-mac-*", "*", "Contents", "MacOS", "*"))
    if candidates:
        # 取版本号最大的（目录名形如 win64-150.0.7871.24）
        def _ver_key(p: str):
            try:
                d = os.path.basename(os.path.dirname(os.path.dirname(p)))
                nums = d.split("-", 1)[-1].split(".")
                return tuple(int(x) for x in nums if x.isdigit())
            except Exception:
                return (0,)
        best = sorted(candidates, key=_ver_key)[-1]
        if os.path.isfile(best):
            return best, "Chrome for Testing"

    # 2) 系统 Edge（兜底，本机可能秒退）
    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for p in edge_candidates:
        if os.path.isfile(p):
            return p, "Edge"

    return None, ""


def _embed_hf(docx_token: str, video_path: str) -> str:
    """上传视频到飞书文档（使用 ffmpeg 的 embed 方式作为 fallback）。"""
    from stitch_ffmpeg import _embed_to_doc
    return _embed_to_doc(docx_token, video_path)


# ── 模块级：从 __file__ 定位 skill_root，再解析所有工具路径 ──
_SKILL_ROOT = _hf_skill_root()

try:
    from _paths import resolve_tool, resolve_node_modules, resolve_ffmpeg
    _NODE_EXE = resolve_tool("node", _SKILL_ROOT) or shutil.which("node") or "node"
    _NM = resolve_node_modules(_SKILL_ROOT)
    _NODE_MODULES = _NM if _NM else os.path.join(_SKILL_ROOT, "node_modules")
except ImportError:
    _NODE_EXE = shutil.which("node") or "node"
    _NODE_MODULES = os.path.join(_SKILL_ROOT, "node_modules")

_HF_CLI_PATH = os.path.join(_NODE_MODULES, "hyperframes", "dist", "cli.js")


def _hf_available() -> bool:
    """检查 hyperframes CLI 文件是否存在（与 _find_hf_cli 同源，含 workspace 兜底）。"""
    return _find_hf_cli() is not None


def _check_available() -> bool:
    """检查 hyperframes 是否可用。"""
    ok = _hf_available()
    if not ok:
        print("[HF] hyperframes 未安装，尝试: npx hyperframes init")
    return ok


def ensure_installed() -> bool:
    """检查并自动安装 hyperframes 到 workspace。"""
    if _hf_available():
        print("[HF] ✅ hyperframes 已安装")
        return True

    print("[HF] hyperframes 未安装，自动安装...")

    node_exe = _NODE_EXE

    # workspace 目录：优先模块级解析的 NODE_MODULES 的父目录
    workspace = os.path.dirname(_NODE_MODULES) if _NODE_MODULES != os.path.join(_SKILL_ROOT, "node_modules") else _NODE_MODULES
    if not os.path.isdir(workspace):
        workspace = _SKILL_ROOT
    os.makedirs(workspace, exist_ok=True)

    # npm 路径：node.exe 同目录下的 npm.cmd
    npm_cmd = os.path.join(os.path.dirname(node_exe), "npm.cmd")
    if not os.path.isfile(npm_cmd):
        npm_cmd = shutil.which("npm") or "npm"

    try:
        r = subprocess.run(
            [npm_cmd, "install", "hyperframes"],
            cwd=workspace, capture_output=True, text=True, timeout=120,
        )
        if r.returncode == 0 and _hf_available():
            print(f"[HF] ✅ hyperframes 安装成功 (workspace)")
            return True
        else:
            print(f"[HF] ❌ 安装失败: {r.stderr[-300:]}")
            return False
    except subprocess.TimeoutExpired:
        print("[HF] ❌ 安装超时 (120s)")
        return False


def _run_hf(project: str, script_config: Optional[dict] = None) -> Optional[str]:
    """用 Hyperframes 合成视频，返回最终视频路径。"""
    sp = _script_path(project)
    if not os.path.isfile(sp):
        print(f"[HF] script.json 未找到: {sp}")
        return None

    with open(sp, "r", encoding="utf-8") as f:
        data = json.load(f)

    if script_config:
        sc = script_config
    else:
        sc = data.get("script", {})
    shots = data.get("shots", [])
    groups = data.get("shot_groups", [])

    if not shots:
        print("[HF] 没有 shot 数据")
        return None

    # 检查视频文件是否存在
    videos_dir = os.path.join(project, "videos")
    for s in shots:
        vpath = os.path.join(videos_dir, f"shot_{s['id']:02d}.mp4")
        if not os.path.isfile(vpath):
            print(f"[HF] ❌ 缺少视频: {vpath}")
            return None

    # 输出路径
    out_dir = os.path.join(project, "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "final_hf.mp4")
    if os.path.isfile(out_path):
        try:
            os.remove(out_path)
        except Exception as _e:
            print(f"  [warn] 清理旧 final_hf.mp4 失败(可忽略): {_e}")

    # 生成合成 HTML
    w = sc.get("width", 1280)
    h = sc.get("height", 720)
    aspect = sc.get("aspect_ratio", "16:9")
    if "9:16" in aspect:
        w, h = 720, 1280

    html = _build_composition(w, h, project, shots, groups, data)

    # 写入项目根目录的 index.html（hyperframes 会检测到此文件）
    index_path = os.path.join(project, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 写入 output/composition.html（参考用）
    html_path = os.path.join(project, "output", "composition.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 生成 hyperframes.json（hyperframes render 需要）
    hf_json = {"width": w, "height": h, "fps": 24}
    with open(os.path.join(project, "hyperframes.json"), "w", encoding="utf-8") as f:
        json.dump(hf_json, f)

    # 调用 npx hyperframes render
    print(f"[HF] 渲染合成视频...")
    print(f"      输出: {out_path}")

    if not _hf_available():
        print("[HF] ❌ hyperframes 不可用，请先运行: npx hyperframes init")
        return None

    # 构建环境变量
    env = os.environ.copy()
    env["NODE_PATH"] = _NODE_MODULES + os.pathsep + env.get("NODE_PATH", "")
    env["HF_SKIP_TELEMETRY"] = "1"
    env["NODE_OPTIONS"] = "--no-warnings"

    # 将 ffmpeg 目录加入 PATH（hyperframes 需要 ffmpeg + ffprobe）
    _ff_dir = os.path.dirname(resolve_ffmpeg(_SKILL_ROOT)) if resolve_ffmpeg(_SKILL_ROOT) else None
    if _ff_dir and os.path.isdir(_ff_dir):
        env["PATH"] = _ff_dir + os.pathsep + env.get("PATH", "")
        print(f"[HF] ✅ ffmpeg PATH: {_ff_dir}")

    # 不设浏览器路径，由 hyperframes 自动发现 headless shell
    # resolveHeadlessShellPath() →
    #   1. PRODUCER_HEADLESS_SHELL_PATH 环境变量
    #   2. ~/.cache/puppeteer/chrome-headless-shell/*/chrome-headless-shell.exe
    #   3. puppeteer 内置浏览器发现（Chrome for Testing / 系统 Chrome）
    print(f"[HF] 浏览器: hyperframes 自动发现（headless shell / Chrome for Testing）")

    # 命令：直接用 node 执行本地 hyperframes CLI，避免 npx 下载不同版本
    _hf_cli = _find_hf_cli()
    if not _hf_cli:
        print("[HF] ❌ 本地 hyperframes CLI 未找到")
        return None
    cmd = [
        _NODE_EXE,  # node.exe 路径
        _hf_cli,
        "render",
        "--fps", "24",
        "--quality", "standard",
        "--output", out_path,
            project,
        ]

    try:
        print(f"[HF] node: {' '.join(cmd)}")
        start = time.time()
        result = subprocess.run(
            cmd, cwd=project, env=env,
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            # 超时 600s：Edge 启动失败（Code:0 秒退）会快速返回，不会卡住；
            # 若 Edge 成功但渲染慢，超时会回退 ffmpeg（simple concat）。
            timeout=600,
        )
        elapsed = time.time() - start
        if result.returncode != 0:
            print(f"[HF] ❌ render 失败 (exit={result.returncode})")
            # npx 输出一般在 stderr
            stderr_lines = [l for l in (result.stderr or "").split("\n") if l.strip()]
            for l in stderr_lines[-15:]:
                print(f"  {l}")
            if result.stdout:
                print(f"  stdout: {result.stdout[-300:]}")
            return None
        print(f"[HF] ✅ 完成 ({elapsed:.0f}s): {out_path}")

        # ── 后处理：voice_over 音频 + 字幕 ──
        # HF 只做视频拼接（无字幕层），音频混合与字幕烧录由后处理完成。
        # 复用 stitch_ffmpeg 的 _apply_audio_and_subs 来做第二遍处理：
        #   1. voice_over → TTS WAV
        #   2. dialogue  → SRT 字幕文件（不生成 TTS，视频已自带人声）
        #   3. ffmpeg 混音 + 烧录字幕 → final.mp4
        # 无 voice_over/dialogue 数据时跳过，直接返回 HF 裸输出。
        print("[HF] 后处理：音频混合 + 字幕...")
        try:
            # 找 ffmpeg
            _ff_exe = shutil.which("ffmpeg")
            if not _ff_exe:
                try:
                    from imageio_ffmpeg import get_ffmpeg_exe as _get_ff
                    _ff_exe = _get_ff()
                except Exception:
                    pass
            _sc = len(shots)
            if _ff_exe:
                from stitch_ffmpeg import _apply_audio_and_subs as _post_audio
                _final = _post_audio(project, out_path, _ff_exe, _sc)
                if _final and _final != out_path:
                    print(f"  ✅ 合成完成: {_final}")
                    return _final
                elif _final == out_path:
                    # 无 voice_over 数据，直接返回 HF 输出
                    return out_path
                else:
                    print("  ⚠️ 合成失败，返回 HF 输出")
                    return out_path
            else:
                print("  ⚠️ ffmpeg 未找到，跳过音频混合+字幕，返回 HF 裸输出")
        except Exception as _e:
            print(f"  ⚠️ 后处理异常: {_e}")
        return out_path
    except subprocess.TimeoutExpired:
        print("[HF] ❌ render 超时")
        return None
    except FileNotFoundError as e:
        print(f"[HF] ❌ 找不到可执行文件: {e}")
        return None


def _probe_durations(project: str, shots: list) -> list[float]:
    """用 ffprobe 获取各视频的实际时长，解决计划时长 ≠ 实际时长导致的字幕漂移。"""
    import subprocess as _sp, json as _json
    _ffprobe = shutil.which("ffprobe")
    if not _ffprobe:
        try:
            from imageio_ffmpeg import get_ffmpeg_exe as _gf
            _ffprobe = _gf().replace("ffmpeg.exe", "ffprobe.exe").replace("ffmpeg", "ffprobe")
        except Exception:
            pass
    if not _ffprobe or not os.path.isfile(_ffprobe):
        return [s.get("duration_seconds", 5) for s in shots]

    durations = []
    for s in shots:
        sid = s["id"]
        vpath = os.path.join(project, "videos", f"shot_{sid:02d}.mp4")
        if not os.path.isfile(vpath):
            durations.append(s.get("duration_seconds", 5))
            continue
        try:
            r = _sp.run(
                [_ffprobe, "-v", "quiet", "-print_format", "json",
                 "-show_entries", "format=duration", vpath],
                capture_output=True, text=True, timeout=10,
            )
            info = _json.loads(r.stdout)
            dur = float(info["format"]["duration"])
            durations.append(max(dur, 0.5))  # 下限 0.5s
        except Exception:
            durations.append(s.get("duration_seconds", 5))
    return durations


def _build_composition(w: int, h: int, project: str,
                       shots: list, groups: list, data: dict) -> str:
    """构建 Hyperframes HTML 合成文件。使用实际视频时长避免字幕漂移。"""
    actual_durs = _probe_durations(project, shots)
    curr_time = 0.0
    video_lines: list[str] = []
    subtitle_lines: list[str] = []
    transition_lines: list[str] = []
    audio_lines: list[str] = []

    prev_shot_id = None

    for i, s in enumerate(shots):
        sid = s["id"]
        dur = actual_durs[i]
        vpath = os.path.abspath(os.path.join(project, "videos", f"shot_{sid:02d}.mp4"))
        vpath_rel = os.path.relpath(vpath, project).replace("\\", "/")

        # 转场（shot 之间）
        if prev_shot_id is not None and i < len(shots) - 1:
            tdur = 0.3
            transition_lines.append(
                f'  <div id="xfade_{sid}" class="clip" data-start="{curr_time - 0.15}" '
                f'data-duration="{tdur}" data-track-index="2">'
                f'<div class="xfade"></div></div>'
            )

        # 视频轨道
        video_lines.append(
            f'  <video id="shot_{sid:02d}" class="clip" data-start="{curr_time}" '
            f'data-duration="{dur}" data-track-index="0" data-has-audio="true" '
            f'src="{vpath_rel}"></video>'
        )

        # 字幕（voice_over / dialogue 文本）
        # ⭐ 不渲染 HF 字幕层：HF 输出无字幕版，字幕完全交给后处理 ffmpeg 烧录。
        #    原因：HF 字幕层 + ffmpeg subtitles 滤镜会叠加成双字幕（用户已否决）。
        #    如需 HF 自带字幕层，将下面开关改为 True。
        _render_subtitle_layer = False
        vo = s.get("voice_over", "") or s.get("dialogue", "") or ""
        if vo and _render_subtitle_layer:
            sub_text = _esc(vo)
            subtitle_lines.append(
                f'  <div class="clip subtitle" data-start="{curr_time}" '
                f'data-duration="{dur}" data-track-index="1">\n'
                f'    <div class="sub-inner"><p>{sub_text}</p></div>\n'
                f'  </div>'
            )

        prev_shot_id = sid
        curr_time += dur

    total_dur = curr_time
    script_title = data.get("script", {}).get("title", "视频合成") if data else "视频合成"

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width={w}, height={h}">
<title>{_esc(script_title)} - 视频合成</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #000; width: {w}px; height: {h}px; overflow: hidden; }}
  #root {{
    position: relative;
    width: {w}px;
    height: {h}px;
    background: #000;
    overflow: hidden;
  }}
  .clip {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
  video {{ width: 100%; height: 100%; object-fit: cover; }}
  .subtitle {{
    display: flex;
    align-items: flex-end;
    justify-content: center;
    pointer-events: none;
  }}
  .sub-inner {{
    background: rgba(0,0,0,0.5);
    padding: 12px 24px;
    border-radius: 8px;
    margin-bottom: 60px;
    max-width: 80%;
  }}
  .sub-inner p {{
    color: #fff;
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    font-size: 28px;
    line-height: 1.5;
    text-align: center;
    text-shadow: 0 1px 3px rgba(0,0,0,0.5);
  }}
  .xfade {{
    width: 100%; height: 100%;
    background: #000;
    opacity: 0;
    animation: xfadeAnim 0.3s ease-in-out;
  }}
  @keyframes xfadeAnim {{
    0% {{ opacity: 0; }}
    50% {{ opacity: 1; }}
    100% {{ opacity: 0; }}
  }}
</style>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
</head>
<body>
<div id="root" data-composition-id="main"
     data-start="0" data-duration="{total_dur}"
     data-width="{w}" data-height="{h}">

{"\n".join(video_lines)}

{"\n".join(subtitle_lines)}

{"\n".join(transition_lines)}

</div>

<script>
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = gsap.timeline({{ paused: true }});
</script>
</body>
</html>'''
    return html
