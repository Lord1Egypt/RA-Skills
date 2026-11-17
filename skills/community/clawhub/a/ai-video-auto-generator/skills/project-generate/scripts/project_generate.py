#!/usr/bin/env python3
"""项目生成/管理 CLI — 子命令模式。"""
from __future__ import annotations

import argparse, json, os, sys


if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")

MODULES_DIR = os.path.join(os.path.dirname(__file__), "modules")
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

# ── .pyc 恢复引导：检测 project_commands/__init__.py 是否被损坏 ──
_PC_PY = os.path.join(MODULES_DIR, "project_commands", "__init__.py")
_NEED_RESTORE = False
if os.path.isfile(_PC_PY):
    with open(_PC_PY, "r", encoding="utf-8") as _f:
        _NEED_RESTORE = "---" in _f.readline()

if _NEED_RESTORE:
    import types as _t, importlib.machinery as _im, importlib.util as _iu
    
    # 注册 modules 命名空间
    if "modules" not in sys.modules:
        sys.modules["modules"] = _t.ModuleType("modules")
        sys.modules["modules"].__path__ = [MODULES_DIR]
    
    # 加载从属模块
    for _mn in ("project_verify", "error_utils", "task_tracker_local", "task_tracker",
                 "base_provider", "agnes_provider", "provider_factory"):
        _pyc = os.path.join(MODULES_DIR, "__pycache__", f"{_mn}.cpython-313.pyc")
        if os.path.isfile(_pyc) and _mn not in sys.modules:
            try:
                _l = _im.SourcelessFileLoader(_mn, _pyc)
                _s = _iu.spec_from_loader(_mn, _l, origin=_pyc)
                _m = _iu.module_from_spec(_s)
                _m.__file__ = os.path.join(MODULES_DIR, f"{_mn}.py")
                sys.modules[_mn] = _m
                _l.exec_module(_m)
                setattr(sys.modules["modules"], _mn, _m)
            except Exception:
                pass

    # 加载 agnes 从属模块
    _AGNES_MOD = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agnes-ai", "scripts", "modules")
    for _mn in ("config", "image_api", "prompt", "video_api"):
        _pyc = os.path.join(_AGNES_MOD, "__pycache__", f"{_mn}.cpython-313.pyc")
        if os.path.isfile(_pyc) and _mn not in sys.modules:
            try:
                _l = _im.SourcelessFileLoader(_mn, _pyc)
                _s = _iu.spec_from_loader(_mn, _l, origin=_pyc)
                _m = _iu.module_from_spec(_s)
                _m.__file__ = os.path.join(_AGNES_MOD, f"{_mn}.py")
                sys.modules[_mn] = _m
                _l.exec_module(_m)
            except Exception:
                pass

    # 加载 project_commands
    _PC_PYC = os.path.join(MODULES_DIR, "project_commands", "__pycache__", "__init__.cpython-313.pyc")
    if os.path.isfile(_PC_PYC):
        _l = _im.SourcelessFileLoader("project_commands", _PC_PYC)
        _s = _iu.spec_from_loader("project_commands", _l, origin=_PC_PYC)
        _m = _iu.module_from_spec(_s)
        _m.__file__ = _PC_PY
        _m.__package__ = "project_commands"
        _m.__path__ = [os.path.join(MODULES_DIR, "project_commands")]
        sys.modules["project_commands"] = _m
        _l.exec_module(_m)

import modules.config as config

from provider_factory import create_provider
from project_commands import (
    _cmd_build_first_frames, _cmd_generate_images,
    _cmd_auto, _cmd_preview, _cmd_report,
    _cmd_update_prompts, _cmd_repair,
    _cmd_reset_prompts, _cmd_diff_all,
    _cmd_validate_script, _cmd_validate_all, _cmd_optimize,
    _cmd_build_asset_prompts,
    _cmd_submit, _cmd_poll, _cmd_stitch, _cmd_status, _cmd_tracker_sync,
    _cmd_generate_characters, _cmd_generate_scenes,
    _cmd_verify_scenes,
)

DESCRIPTION = "项目生成/管理工具 v2"
VERSION = "Agnes AI 项目生成/管理  v2.1.0"


def main():
    # ── 全局 flag（同时加在主解析器和子命令上，支持 --project . status --quiet） ──
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--verbose", action="store_true", help="详细输出模式")
    common.add_argument("--quiet", action="store_true", help="静默模式")
    common.add_argument("--log-file", help="日志文件路径（默认：项目目录/generate.log）")
    common.add_argument("--tracker", choices=["local", "feishu"], default="feishu",
                        help="任务追踪后端：local（本地 JSON）或 feishu（飞书 Base，默认 feishu）")

    parser = argparse.ArgumentParser(description=DESCRIPTION, parents=[common],
                                     conflict_handler="resolve")
    parser.add_argument("--project", required=True, help="项目根目录路径")
    parser.add_argument("--version", action="store_true", help="显示版本信息")

    sub = parser.add_subparsers(dest="command", title="命令")

    # ── submit ──
    sp = sub.add_parser("submit", parents=[common], help="提交所有视频任务")
    sp.add_argument("--force", type=int, nargs="*", default=None,
                    help="强制重新提交（无值=全部，指定 ID=只重试，如 --force 2 5）")

    # ── poll ──
    sub.add_parser("poll", parents=[common], help="轮询视频生成状态")

    # ── stitch ──
    sub.add_parser("stitch", parents=[common],
                   help="独立拼接（HF无字幕→烧分段字幕→CRF18，不重新提交/轮询）")

    # ── status ──
    sp = sub.add_parser("status", parents=[common], help="显示项目状态（默认 JSON）")
    sp.add_argument("--text", action="store_true", help="输出人类可读格式（非 JSON）")

    # ── tracker（状态文件管理）──
    sp = sub.add_parser("tracker", parents=[common], help="任务追踪状态文件管理")
    sp.add_argument("action", choices=["sync"], help="sync: 把飞书进度复制到本地 task_tracker.json")

    # ── build-first-frames ──
    sp = sub.add_parser("build-first-frames", parents=[common],
                        help="读取 script.json 生成 prompt 模板和 first_frame 配置（不调 API）",
                        aliases=["bff"])
    sp.add_argument("--force", action="store_true", help="强制重新生成所有 prompt 模板")

    # ── generate-images ──
    sp = sub.add_parser("generate-images", parents=[common], help="调 API 批量生成首帧图",
                        aliases=["gi"])
    sp.add_argument("--shot-ids", type=int, nargs="+", help="指定 shot ID 列表")
    sp.add_argument("--parallel", type=int, default=1, help="并行生成线程数")
    sp.add_argument("--auto-verify", action="store_true", help="启用首帧图自动验证")
    sp.add_argument("--retry-failed", action="store_true", help="仅重试失败的 shot")

    # ── verify ──
    sp = sub.add_parser("verify", parents=[common], help="验证首帧图/角色/场景质量")
    sp.add_argument("--shot-ids", type=int, nargs="+", help="指定 shot ID（不指定=全部）")
    sp.add_argument("--vlm", "--premium", action="store_true", dest="vlm",
                    help="启用 VLM 语义级 QA（叠加在 OpenCV 校验之上）")

    # ── verify-scenes ──
    sub.add_parser("verify-scenes", parents=[common],
                   help="验证场景图是否包含人物（场景应为纯背景）",
                   aliases=["ve-scenes"])

    # ── validate-script ──
    sub.add_parser("validate-script", parents=[common],
                   help="检查 script.json 占位符和语法（跑 auto 前先跑这个）",
                   aliases=["vs"])

    # ── validate-all ──
    sub.add_parser("validate-all", parents=[common],
                   help="全量预检：叙事+角色+场景+首帧图（不生成任何资产）",
                   aliases=["va"])

    # ── auto ──
    sub.add_parser("auto", parents=[common], help="全自动流水线：生成首帧图→验证→提交视频")

    # ── preview ──
    sub.add_parser("preview", parents=[common], help="生成 HTML 预览页")

    # ── report ──
    sub.add_parser("report", parents=[common], help="生成 HTML 统计报告")

    # ── generate（保留入口但不调用，引导使用 AI Agent）──
    sp = sub.add_parser("generate", parents=[common],
                        help="[已迁移至 AI Agent] 在 WorkBuddy 中加载本 skill 后直接描述需求即可",
                        aliases=["gen"])
    sp.add_argument("--prompt", default="", help="（已弃用）")
    sp.add_argument("--source", default="",
                    help="（已弃用）")
    sp.add_argument("--type", default="",
                    help="（已弃用）")
    sp.set_defaults(cmd="generate")

    # ── update-prompts ──
    sp = sub.add_parser("update-prompts", parents=[common],
                        help='更新提示词段，如 "保留元素:false"')
    sp.add_argument("kv", help='段名和操作，格式 "段名:true/false/remove"')

    # ── repair ──
    sub.add_parser("repair", parents=[common], help="自动修复提示词文件")

    # ── reset-prompts ──
    sub.add_parser("reset-prompts", parents=[common], help="删除所有提示词文件并重新生成模板")

    # ── diff-all ──
    sub.add_parser("diff-all", parents=[common], help="扫描所有旧图备份，批量生成对比页和索引")

    # ── diff ──
    sp = sub.add_parser("diff", parents=[common], help="生成单个 shot 的首帧图对比页")
    sp.add_argument("--shot-id", type=int, required=True, help="shot ID")

    # ── collect ──
    sub.add_parser("collect", parents=[common], help="收集所有首帧图到 output/ 目录")

    # ── generate-characters ──
    sp = sub.add_parser("generate-characters", parents=[common],
                        help='读 script.json 的 character_cards，批量生成角色资产图',
                        aliases=["gc"])
    sp.add_argument("--force", action="store_true", help="强制重新生成已存在的角色图")

    # ── generate-scenes ──
    sp = sub.add_parser("generate-scenes", parents=[common],
                        help='读 script.json 的 scene_cards，批量生成场景资产图',
                        aliases=["gs"])
    sp.add_argument("--force", action="store_true", help="强制重新生成已存在的场景图")

    # ── generate-troops ──
    sp = sub.add_parser("generate-troops", parents=[common],
                        help='读 script.json 的 troop_cards，批量生成辅助资产图',
                        aliases=["gt"])
    sp.add_argument("--force", action="store_true", help="强制重新生成已存在的辅助资产图")

    # ── bg（后台启动）──
    sp = sub.add_parser("bg", parents=[common],
                        help="后台启动流水线（detached），进程不会随父 shell 退出",
                        description="""
使用 Windows DETACHED_PROCESS 标志启动流水线子命令，完全脱离当前控制台。
进程不会因 WorkBuddy 断开连接而被杀，可无限期后台运行。

示例:
  project_generate.py --project . bg auto       # 后台跑全自动流水线
  project_generate.py --project . bg poll       # 后台跑轮询
  project_generate.py --project . bg gi         # 后台生首帧图
                        """)
    sp.add_argument("sub", nargs=argparse.REMAINDER,
                    help="要后台运行的子命令和参数（如: auto / poll / gi）")

    # ── optimize (调用 script-optimizer) ──
    sp = sub.add_parser("optimize", parents=[common],
                        help="自动验证和优化 script.json（调用 script-optimizer）",
                        aliases=["opt"])
    sp.add_argument("--strict", action="store_true", help="strict 模式（P1 必须为 0）")
    sp.add_argument("--force", action="store_true", help="强制覆盖人工编辑的字段")
    sp.add_argument("--dry-run", action="store_true", help="预览模式（不写入）")
    sp.add_argument("--report-only", action="store_true", help="仅报告不修复")
    sp.add_argument("--sync-type", action="store_true", help="从类型 .md 重新应用默认配置")
    sp.add_argument("--fix-prompts", action="store_true", default=True, help="自动修复首帧图/视频 prompt 文件（默认开启）")
    sp.add_argument("--no-fix-prompts", action="store_false", dest="fix_prompts", help="跳过自动修复 prompt 文件")

    # ── build-prompts ──
    sp = sub.add_parser("build-prompts", parents=[common],
                        help="从 script.json 生成资产 prompt 文件（prompts/characters/ 和 prompts/scenes/）",
                        aliases=["bp"])
    sp.add_argument("--force", action="store_true", help="覆盖已存在的 prompt 文件")

    args = parser.parse_args()

    # ── 全局控制 ──
    if args.quiet:
        config.LOG_LEVEL = 0
    elif args.verbose:
        config.LOG_LEVEL = 2

    if args.version:
        print(VERSION)
        return

    if not args.command:
        parser.print_help()
        return

    if not os.path.isdir(args.project):
        print(f"[ERROR] 项目不存在: {args.project}")
        sys.exit(1)

    # ── 分发 ──
    cmd = args.command
    project = args.project

    # ── 日志文件（需 project 已就绪） ──
    if args.log_file:
        config.set_log_file(args.log_file)

    if cmd == "submit":
        force_a, force_s = False, None
        if args.force is not None:
            if len(args.force) == 0:
                force_a = True          # --force（全部）
            else:
                force_s = args.force    # --force 2 5（指定 ID）
        _cmd_submit(project, force=force_a, force_shot=force_s, tracker=args.tracker)

    elif cmd == "poll":
        _cmd_poll(project, tracker=args.tracker)

    elif cmd == "stitch":
        _cmd_stitch(project, tracker=args.tracker)

    elif cmd == "status":
        _cmd_status(project, json_output=not getattr(args, "text", False))

    elif cmd == "tracker":
        if args.action == "sync":
            _cmd_tracker_sync(project)

    elif cmd in ("build-first-frames", "bff"):
        _cmd_build_first_frames(project, force=args.force)
        print("\n=== build-first-frames 完成 ===")

    elif cmd in ("generate-images", "gi"):
        _cmd_generate_images(
            project,
            shot_ids=args.shot_ids,
            retry_failed=args.retry_failed,
            auto_verify=args.auto_verify,
            parallel=args.parallel,
        )
        print("\n=== generate-images 完成 ===")

    elif cmd == "verify":
        sid = args.shot_ids[0] if args.shot_ids else None
        _log("━━━ OpenCV 启发式校验 ━━━")
        create_provider(project).verify(project, shot_id=sid)

        if getattr(args, "vlm", False):
            _log("\n━━━ VLM 语义级 QA（叠加）━━━")
            try:
                from modules.vlm_qa import run_vlm_qa
                from _paths import resolve_skill_root
                skill_root = resolve_skill_root()
                vlm_result = run_vlm_qa(project, skill_root)
                s = vlm_result.get("summary", {})
                _log(f"\n  [VLM] 汇总: {s.get('passed', 0)}/{s.get('total', 0)} 通过"
                     f"  {s.get('failed', 0)} 失败  {s.get('uncertain', 0)} 不确定")
                for chk in vlm_result.get("checks", []):
                    label = chk.get("name") or f"shot_{chk.get('shot_id','?')}"
                    view = chk.get("view", "")
                    status = "✅" if chk.get("passed") else "❓" if chk.get("uncertain") else "❌"
                    _log(f"    {status} {label}{' ('+view+')' if view else ''}: "
                         f"{chk.get('reason', '')[:120]}")
            except ImportError as e:
                _log(f"  [VLM] ⚠️ VLM 模块不可用: {e}")
            except Exception as e:
                _log(f"  [VLM] ⚠️ VLM QA 异常: {e}")

    elif cmd in ("verify-scenes", "ve-scenes"):
        _cmd_verify_scenes(project)

    elif cmd in ("validate-script", "vs"):
        _cmd_validate_script(project)
        print("\n=== verify 完成 ===")

    elif cmd in ("validate-all", "va"):
        _cmd_validate_all(project)
        print("\n=== validate-all 完成 ===")

    elif cmd == "auto":
        _cmd_auto(project, tracker=args.tracker)

    elif cmd == "preview":
        _cmd_preview(project)

    elif cmd == "report":
        _cmd_report(project)

    elif cmd in ("generate", "gen"):
        print("=" * 55)
        print("  📝 脚本生成已迁移至 AI Agent")
        print("=" * 55)
        print()
        print("  在 WorkBuddy 中加载本 skill 后，直接描述需求即可。")
        print()
        print("  示例:")
        print('    "帮我做一个军事短剧，紧张氛围，约60秒"')
        print('    "从这篇文章生成视频" + 贴 URL')
        print('    "从这份文档生成视频" + 上传文件')
        print()
        print("  如果需要手动使用模板引擎生成基础脚本:")
        print(f"    python -c \"from modules.script_generator import generate_script as g; g('{project}', input(), '{args.type}')\"")
        print("=" * 55)

    elif cmd == "update-prompts":
        _cmd_update_prompts(project, args.kv)

    elif cmd == "repair":
        _cmd_repair(project)

    elif cmd == "reset-prompts":
        _cmd_reset_prompts(project)

    elif cmd == "diff-all":
        _cmd_diff_all(project)

    elif cmd == "diff":
        from project_diff import _generate_diff_html
        sp = os.path.join(project, "script.json")
        with open(sp, encoding="utf-8") as f:
            script = json.load(f)
        shot = next((s for s in script.get("shots", []) if s.get("id") == args.shot_id), None)
        if not shot:
            print(f"shot_{args.shot_id:02d} 未找到"); return
        new_img = os.path.join(project, "images", "storyboard", f"shot_{args.shot_id:02d}_first_frame.png")
        old_img = os.path.join(project, "output", f"shot_{args.shot_id:02d}_old.png")
        if not os.path.isfile(new_img) or not os.path.isfile(old_img):
            print("首帧图或旧版图不存在"); return
        diff_path = _generate_diff_html(project, shot, old_img, new_img)
        print(f"  ✅ 对比页已生成: {diff_path}")

    elif cmd in ("optimize", "opt"):
        _cmd_optimize(project, strict=args.strict, force=args.force,
                      dry_run=args.dry_run, report_only=args.report_only,
                      sync_type=args.sync_type, fix_prompts=args.fix_prompts)

    elif cmd in ("build-prompts", "bp"):
        _cmd_build_asset_prompts(project, force=args.force)

    elif cmd in ("generate-characters", "gc"):
        _cmd_generate_characters(project, force=args.force)

    elif cmd in ("generate-scenes", "gs"):
        _cmd_generate_scenes(project, force=args.force)

    elif cmd in ("generate-troops", "gt"):
        from project_commands import _cmd_generate_troops
        _cmd_generate_troops(project, force=args.force)

    elif cmd == "bg":
        from modules.launch_background import launch_background
        launch_background(project, *args.sub)



if __name__ == "__main__":
    main()
