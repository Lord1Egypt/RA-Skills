#!/usr/bin/env python3
"""AI视频流水线一跑到底入口（skill 层，跨项目通用）。

用法:
  # 全新项目：完整流水线（build→submit→poll→stitch）
  python pipeline.py --project /path/to/project --mode auto

  # 续跑项目：poll-only（跳过 auto，只轮询已有 task）
  python pipeline.py --project /path/to/project --mode poll

  # 后台脱离终端运行（不影响当前会话）
  python pipeline.py --project /path/to/project --mode poll --detached
"""
import sys, os, time, subprocess, argparse

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_SCRIPT = os.path.join(SKILL_DIR, "project_generate.py")


def _log(path: str, msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}", flush=True)


def _run_auto(proj: str, py: str) -> None:
    """DETACHED 运行 project_generate.py auto（完整流水线）。"""
    log_path = os.path.join(proj, "auto.log")
    log = open(log_path, "w")
    p = subprocess.Popen(
        [py, "-u", SKILL_SCRIPT, "--project", proj, "auto"],
        stdout=log, stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008,
    )
    print(f"auto PID={p.pid}（日志 {log_path}）")


def _run_poll(proj: str, py: str) -> None:
    """轮询循环：查 shot 状态→下载→完成自动拼接。"""
    log_path = os.path.join(proj, "poll_only.log")
    state_path = os.path.join(proj, ".poll_state.json")
    final_path = os.path.join(proj, "output", "final.mp4")

    _log(log_path, ">>> poll 循环启动")
    for i in range(300):
        if os.path.isfile(final_path):
            _log(log_path, "✅ final.mp4 已存在，结束")
            return
        # 强制立即轮询：删除 600s 间隔锁
        if os.path.isfile(state_path):
            try:
                os.remove(state_path)
            except Exception:
                pass
        cmd = [py, "-u", SKILL_SCRIPT, "--project", proj, "poll", "--tracker", "local"]
        _log(log_path, f">>> 第 {i+1} 轮 poll")
        try:
            r = subprocess.run(cmd, cwd=proj, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=1800)
            out = (r.stdout + r.stderr)[-2000:]
            _log(log_path, out if out.strip() else "(无输出)")
        except Exception as e:
            _log(log_path, f"⚠️ poll 异常: {e}")
        if os.path.isfile(final_path):
            _log(log_path, "✅ final.mp4 已生成，结束")
            return
        time.sleep(120)
    _log(log_path, "⚠️ 已达轮询上限（300 轮），请人工检查")


def _run_demo(proj: str, py: str) -> None:
    """快速体验模式 — 不依赖 API Key，用 ffmpeg 本地合成预览视频。"""
    print("=" * 55)
    print("  🚀 快速体验模式")
    print("=" * 55)

    # 1. 定位 sample 项目（skill 内的 sample/）
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    while not os.path.isdir(os.path.join(skill_dir, "sample")):
        skill_dir = os.path.dirname(skill_dir)
    sample_dir = os.path.join(skill_dir, "sample")
    # 如果 sample 不存在（例如 SkillHub 安装未带 sample），从内置模板创建
    if not os.path.isfile(os.path.join(sample_dir, "script.json")):
        print("  📦 初始化示例项目...")
        create_script = os.path.join(skill_dir, "scripts", "create_project.py")
        if os.path.isfile(create_script):
            subprocess.run([py, create_script, "--project", sample_dir,
                           "--template", "short_drama"], capture_output=True, timeout=30)
        os.makedirs(sample_dir, exist_ok=True)
    output_dir = os.path.join(sample_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    preview_path = os.path.join(output_dir, "preview.mp4")

    # 2. 环境检测 + 自动装依赖
    print()
    _run_setup(sample_dir, py)

    # 3. 寻找 ffmpeg
    import shutil as _sh
    ffmpeg = _sh.which("ffmpeg")
    if not ffmpeg:
        try:
            from imageio_ffmpeg import get_ffmpeg_exe
            ffmpeg = get_ffmpeg_exe()
        except Exception:
            print("  ❌ ffmpeg 未找到，无法生成预览视频")
            return

    # 4. 用 ffmpeg 本地合成预览：测试卡 + 渐变 + 文字 + 提示音
    print()
    print("  🔨 合成预览视频...")
    cmd = [
        ffmpeg, "-y", "-f", "lavfi",
        "-i", "color=c=#1a1a2e:size=720x1280:d=8",        # 背景
        "-f", "lavfi",
        "-i", ("anullsrc=r=44100:cl=stereo"),              # 静音轨
        "-filter_complex", (
            "[0:v]drawtext=text='视频流水线':fontsize=48:fontcolor=white:"
            "x=(w-text_w)/2:y=(h-text_h)/2-80:enable='between(t,0,4)',"
            "drawtext=text='ai-video-auto-generator':fontsize=28:fontcolor=#85b7eb:"
            "x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,4)',"
            "drawtext=text='From script.json to final.mp4':fontsize=20:fontcolor=#b4b2a9:"
            "x=(w-text_w)/2:y=(h-text_h)/2+80:enable='between(t,0,4)',"
            "drawtext=text='python pipeline.py --mode auto':fontsize=18:fontcolor=#639922:"
            "x=(w-text_w)/2:y=(h-text_h)/2+160:enable='between(t,4,7)',"
            "drawtext=text='AI 全自动短视频流水线':fontsize=22:fontcolor=white:"
            "x=(w-text_w)/2:y=(h-text_h)/2+200:enable='between(t,4,7)'"
        ),
        "-c:v", "libx264", "-t", "8", "-pix_fmt", "yuv420p",
        preview_path,
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except Exception as e:
        print(f"  ❌ 预览视频合成失败: {e}")
        return

    if not os.path.isfile(preview_path):
        print("  ❌ 预览视频合成失败")
        return

    mb = os.path.getsize(preview_path) // (1024 * 1024)
    print(f"  ✅ 预览视频已生成: {preview_path} ({mb}MB)")
    print()
    print("  " + "─" * 50)
    print("   下一步：配置 API Key 后运行 auto 流水线")
    print()
    print("   配置 Agnes AI Key:")
    print("     echo '你的Key' > ~/.agnes-api-key")
    print()
    print("   一键出片:")
    print(f"     cd {sample_dir}")
    print("     python skills/project-generate/scripts/pipeline.py --mode auto")
    print("  " + "─" * 50)


def _run_setup(proj: str, py: str) -> None:
    """环境检测 + 自动安装缺失依赖。"""
    import importlib, subprocess, sys, os

    def _check_import(mod: str, pip_name: str | None = None) -> bool:
        """检查 Python 模块是否可导入，缺失则自动 pip install。"""
        try:
            importlib.import_module(mod)
            v = getattr(importlib.import_module(mod), "__version__", "?")
            print(f"  ✅ {mod}: v{v}")
            return True
        except ImportError:
            name = pip_name or mod
            print(f"  ⚠️  {mod} 未安装，自动安装 {name}...")
            r = subprocess.run(
                [py, "-m", "pip", "install", name, "-q"],
                capture_output=True, text=True, timeout=120)
            if r.returncode == 0:
                print(f"  ✅ {name} 安装成功")
                return True
            else:
                print(f"  ❌ {name} 安装失败: {r.stderr[-200:]}")
                return False

    print("=" * 50)
    print("  🔧 环境检测")
    print("=" * 50)

    # 1. Python 版本
    v = sys.version_info
    print(f"  Python: {v.major}.{v.minor}.{v.micro}")
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print("  ⚠️  建议 Python >= 3.10")

    # 2. 核心依赖
    ok = True
    for mod, pip_name in [
        ("cv2", "opencv-python-headless"),
        ("PIL", "Pillow"),
        ("numpy", None),
        ("edge_tts", "edge-tts"),
        ("docx", "python-docx"),
    ]:
        if not _check_import(mod, pip_name):
            ok = False

    # 3. ffmpeg（通过 imageio-ffmpeg 或系统 PATH）
    import shutil
    if shutil.which("ffmpeg"):
        print("  ✅ ffmpeg: 已安装 (PATH)")
    else:
        try:
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            print(f"  ✅ ffmpeg: 已安装 (imageio-ffmpeg bundled)")
        except ImportError:
            print("  ⚠️  ffmpeg 未找到，自动安装 imageio-ffmpeg...")
            r = subprocess.run([py, "-m", "pip", "install", "imageio-ffmpeg", "-q"],
                               capture_output=True, text=True, timeout=120)
            if r.returncode == 0:
                print("  ✅ imageio-ffmpeg 安装成功")
            else:
                print(f"  ❌ imageio-ffmpeg 安装失败: {r.stderr[-200:]}")
                ok = False

    # 4. hyperframes（npm 包）
    sys.path.insert(0, os.path.dirname(SKILL_SCRIPT))
    from modules.hyperframes_stitch import ensure_installed as _hf_install
    if not _hf_install():
        print("  ⚠️  hyperframes 安装失败，拼接将降级为 ffmpeg")
        ok = False

    # 5. 复制 API Key 配置文件
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    while not os.path.isdir(os.path.join(skill_root, "config")):
        skill_root = os.path.dirname(skill_root)
    example_key = os.path.join(skill_root, "config", "keys.example.env")
    target_key = os.path.join(proj, "config", "keys.env")
    if os.path.isfile(example_key) and not os.path.isfile(target_key):
        os.makedirs(os.path.dirname(target_key), exist_ok=True)
        import shutil
        shutil.copy2(example_key, target_key)
        print(f"  📄 已复制 API Key 配置模板: config/keys.env")

    # 5. 项目结构
    if os.path.isfile(os.path.join(proj, "script.json")):
        print(f"  ✅ script.json: 存在")
    else:
        print(f"  ⚠️  script.json: 不存在（请在项目根目录创建）")

    print()
    if ok:
        print("  ✅ 环境就绪")
        # 检查所有 API Key
        _show_key_status("~/.agnes-api-key", "Agnes AI")
        _show_key_status("~/.freesound-api-key", "FreeSound")
        _show_key_status("~/.github-pat", "GitHub PAT（图床）")
        print()
        print("  配置方法:")
        print("    编辑 config/keys.env 填入对应 Key")
        print("    或直接写入 ~/.agnes-api-key / ~/.freesound-api-key / ~/.github-pat")
    else:
        print("  ⚠️  部分依赖安装失败，请手动运行:")
        print(f"     {py} -m pip install opencv-python-headless Pillow numpy edge-tts python-docx imageio-ffmpeg")
    print("=" * 50)


def _show_key_status(key_rel: str, name: str) -> None:
    """检查并显示单个 Key 的状态。"""
    key_path = os.path.expanduser(key_rel)
    if os.path.isfile(key_path):
        print(f"  🔑 {name}: 已配置 ✅")
    else:
        print(f"  🔑 {name}: 未配置 ❌")


def _check_api_key(proj: str) -> None:
    """检查 auto 模式所需的 API Key，没有则引导配置。"""
    key_paths = {
        "agnes": os.path.expanduser("~/.agnes-api-key"),
        "freesound": os.path.expanduser("~/.freesound-api-key"),
        "github": os.path.expanduser("~/.github-pat"),
    }
    sp = os.path.join(proj, "script.json")
    provider = "agnes"
    if os.path.isfile(sp):
        try:
            import json
            provider = json.load(open(sp, encoding="utf-8")).get("script", {}).get("provider", "agnes")
        except Exception:
            pass
    key_file = key_paths.get(provider, "")
    if key_file and not os.path.isfile(key_file):
        print(f"  ⚠️  Provider 为「{provider}」但未找到 API Key")
        print(f"     配置: echo '你的 {provider} API Key' > {key_file}")
        print(f"     或用其它 Provider: 修改 script.json 的 script.provider")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI视频流水线入口（skill 层）")
    parser.add_argument("--project", required=True, help="项目根目录")
    parser.add_argument("--mode", choices=["auto", "poll", "validate", "setup", "demo", "generate"], default="poll",
                        help="auto=完整流水线, poll=仅轮询, validate=预检, setup=环境检测, demo=快速体验, generate=引导使用 AI Agent 生成脚本")
    parser.add_argument("--detached", action="store_true",
                        help="后台脱离终端（仅 poll 模式，auto 默认 detached）")
    parser.add_argument("--prompt", default="", help="视频描述（仅 generate 模式）")
    parser.add_argument("--type", default="", help="视频类型（仅 generate 模式，不指定则自动检测）")
    parser.add_argument("--list-types", action="store_true", help="列出所有可用视频类型")
    args = parser.parse_args()

    if args.list_types:
        from modules.script_generator import list_types as _lt
        from modules.script_generator import get_type as _gt
        print("可用视频类型:")
        for t in _lt():
            td = _gt(t)
            print(f"  - {t}: {td.get('description', td.get('name', t))}")
        sys.exit(0)

    PROJ = os.path.abspath(args.project)
    PY = sys.executable

    if args.mode == "auto":
        # auto 模式：先检查 API Key
        _check_api_key(PROJ)
        # 自动安装缺失依赖
        _run_setup(PROJ, PY)
        _run_auto(PROJ, PY)
    elif args.mode == "poll":
        if args.detached:
            # DETACHED 启动自身（不带 --detached，防止递归）
            child = [sys.executable, __file__, "--project", PROJ, "--mode", "poll"]
            p = subprocess.Popen(
                child, cwd=PROJ,
                creationflags=subprocess.DETACHED_PROCESS | 0x00000008,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            print(f"poll 已后台启动 PID={p.pid}（日志 {PROJ}/poll_only.log）")
        else:
            _run_poll(PROJ, PY)
    elif args.mode == "validate":
        cmd = [PY, "-u", SKILL_SCRIPT, "--project", PROJ, "validate-all"]
        subprocess.run(cmd, cwd=PROJ)
    elif args.mode == "setup":
        _run_setup(PROJ, PY)
    elif args.mode == "demo":
        _run_demo(PROJ, PY)
    elif args.mode == "generate":
        # generate 模式保留但降级：输出引导信息，真正的脚本生成由 AI Agent 在对话中完成
        print("=" * 55)
        print("  📝 脚本生成")
        print("=" * 55)
        print()
        print("  脚本生成已交给 WorkBuddy AI Agent。")
        print("  在 WorkBuddy 中加载本 skill 后，直接描述需求即可。")
        print()
        print("  示例:")
        print('    "帮我做一个军事短剧，紧张氛围，约60秒"')
        print('    "从这篇文章生成视频" + 贴 URL')
        print('    "从这份文档生成视频" + 上传文件')
        print()
        print("  Agent 会自动完成：阅读内容 → 生成 script.json → 跑流水线")
        print()
        print("  如果需要手动使用模板引擎生成基础脚本:")
        print(f"    python -c \"from modules.script_generator import generate_script as g; g('{PROJ}', input(), '{args.type}')\"")
        print("=" * 55)
