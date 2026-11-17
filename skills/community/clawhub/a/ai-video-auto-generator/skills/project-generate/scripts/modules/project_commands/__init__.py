#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""所有 _cmd_* 业务命令：生成/验证/同步/预览/统计等。"""
import json, os, re, sys
from typing import Optional

# Fix import path for sub-modules
_MOD_DIR = os.path.dirname(os.path.abspath(__file__))
if _MOD_DIR not in sys.path:
    sys.path.insert(0, _MOD_DIR)

# 配置常量
_TOTAL_STAGES = 9

# ── 修复策略 ──
_CHAR_REPAIR_STRATEGIES = [
    ("rebuild_prompt", "重建角色 prompt"),
    ("force_regenerate", "强制重新生成"),
    ("add_detail_prompt", "增加细节描述"),
    ("fix_view", "修复特定视图"),
    ("stronger_no_people", "强化无人约束"),
    ("retry_single_view", "单视图重试"),
    ("regenerate_all", "全部重新生成"),
    ("change_model", "切换生成模型"),
    ("final_attempt", "最终尝试(增加负面提示)"),
]

_SCENE_REPAIR_STRATEGIES = [
    ("rebuild_prompt", "重建场景 prompt"),
    ("force_regenerate", "强制重新生成"),
    ("add_detail_prompt", "增加细节描述"),
    ("stronger_no_people", "强化无人约束"),
    ("add_negative", "增加负面提示"),
    ("retry_single_view", "单视图重试"),
    ("fixed_seed", "固定种子值"),
    ("regenerate_all", "全部重新生成"),
    ("change_model", "切换生成模型"),
    ("final_attempt", "最终尝试(增加负面提示)"),
]

_TROOP_REPAIR_STRATEGIES = _CHAR_REPAIR_STRATEGIES

# ── 占位符检测 ──
_PLACEHOLDER_PATTERNS = [r"\{\{.*?\}\}", r"<.*?>", r"【.*?】"]
_PLACEHOLDER_WEAPONS = ["剑", "刀", "枪", "弓", "盾"]
_PLACEHOLDER_ACTIONS = ["战斗", "对话", "动作", "特效"]

# ── 日志 ──
def _log(msg: str) -> None:
    print(msg, flush=True)


# ── 辅助函数 ──
def _paths(project: str) -> dict:
    return {
        "videos": os.path.join(project, "videos"),
        "output": os.path.join(project, "output"),
        "sounds": os.path.join(project, "sounds"),
        "images": os.path.join(project, "images"),
    }


def _save_state(project: str, state: Optional[dict] = None) -> None:
    path = os.path.join(project, ".auto_state.json")
    if state:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)


def _load_state(project: str) -> dict:
    path = os.path.join(project, ".auto_state.json")
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"done": []}


def _create_provider(project: str):
    from provider_factory import create_provider
    return create_provider(project)


def _build_prompts(project: str, force: bool = False) -> list[str]:
    from prompt_builder import build_asset_prompts
    return build_asset_prompts(project, force=force)


def _validate_prompts(project: str) -> list[dict]:
    from prompt_builder import validate_prompts
    return validate_prompts(project)


def _fix_ff_prompts(project: str, issues: list[dict]) -> int:
    from prompt_builder import fix_first_frame_prompts
    return fix_first_frame_prompts(project, issues)


def _fix_video_prompts(project: str, issues: list[dict]) -> int:
    from prompt_builder import fix_video_prompts
    return fix_video_prompts(project, issues)


# ── 占位符检查 ──
def _check_script_placeholders(project: str, data: dict) -> None:
    shots = data.get("shots", [])
    found = []
    for idx, s in enumerate(shots):
        desc = s.get("description", "")
        for pat in _PLACEHOLDER_PATTERNS:
            if re.search(pat, desc):
                found.append(f"shots[{idx}]")
                break
    if found:
        _log(f"  ⚠️ 发现模板占位符: {', '.join(found)}")


def _check_json_quotes(raw: str) -> None:
    try:
        json.loads(raw)
    except json.JSONDecodeError as e:
        pos = e.pos
        _log(f"  ⚠️ JSON 语法错误（位置 {pos}）")
        _log(f"     Context: {raw[max(0,pos-20):pos+20]}...")


# ── 检查准备 ──
def _check_script(project: str) -> dict:
    path = os.path.join(project, "script.json")
    if not os.path.isfile(path):
        raise SystemExit(f"未找到 script.json: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    _check_json_quotes(raw)
    data = json.loads(raw)
    _check_script_placeholders(project, data)
    return data


# ═══════════════════════════════════════════════════════════════
# 阶段执行
# ═══════════════════════════════════════════════════════════════

def _do(project: str, stage: str, desc: str, fn, state: dict, ignore_fail: bool = False) -> None:
    if stage in state.get("done", []):
        _log(f"  ⏭️  跳过阶段 {stage}/{_TOTAL_STAGES}（{desc}，已完成）")
        return
    _log(f"\n{'='*40}")
    _log(f"  阶段 {stage}/{_TOTAL_STAGES}: {desc}")
    _log(f"{'='*40}")
    try:
        fn()
        state.setdefault("done", []).append(stage)
        _save_state(project, state)
    except Exception as e:
        _log(f"  ❌ 阶段 {stage} 失败: {e}")
        if not ignore_fail:
            _save_state(project, state)
            raise


# ═══════════════════════════════════════════════════════════════
# 自动阶段
# ═══════════════════════════════════════════════════════════════

def _auto_stage0(project: str) -> None:
    _cmd_optimize(project, strict=True)


def _auto_stage1(project: str) -> None:
    _cmd_build_asset_prompts(project)
    _cmd_optimize(project, strict=True, fix_prompts=True)


def _auto_stage2(project: str, data: dict) -> None:
    cards = data.get("character_cards", [])
    if not cards:
        _log("  ⏭️ 无角色卡，跳过")
        return
    _log(f"  {sum(1 for c in cards if any(os.path.isfile(os.path.join(project, 'images', 'characters', c.get('name','?').replace(' ','_')+'_'+v+'.png')) for v in ['front','face','side','back']))}/{len(cards)} 个角色已有资产")
    _cmd_generate_characters(project, data)
    _auto_repair_assets(project, "角色资产", _cmd_generate_characters,
                        lambda p, v=True: _verify_character_assets(p, v),
                        lambda p: _verify_character_assets_detailed(p),
                        _CHAR_REPAIR_STRATEGIES)


def _auto_stage3(project: str, data: dict) -> None:
    troops = data.get("troop_cards", [])
    if not troops:
        _log("  ⏭️ 无辅助资产卡，跳过")
        return
    _cmd_generate_troops(project, data)
    _auto_repair_assets(project, "辅助资产", _cmd_generate_troops,
                        lambda p, v=True: _verify_troop_assets(p, v),
                        lambda p: _verify_troop_assets_detailed(p),
                        _TROOP_REPAIR_STRATEGIES)


def _auto_stage4(project: str, data: dict) -> None:
    cards = data.get("scene_cards", [])
    if not cards:
        _log("  ⏭️ 无场景卡，跳过")
        return
    _cmd_generate_scenes(project, data)
    _auto_repair_assets(project, "场景资产", _cmd_generate_scenes,
                        lambda p, v=True: _verify_scene_assets(p, v),
                        lambda p: _verify_scene_assets_detailed(p),
                        _SCENE_REPAIR_STRATEGIES)


def _auto_stage5(project: str) -> None:
    _cmd_build_first_frames(project)


def _auto_stage6(project: str, data: dict) -> None:
    _cmd_generate_images(project, data)


def _auto_stage7(project: str, tracker: str) -> None:
    _log(f"\n{'='*40}")
    _log(f"  阶段 7/{_TOTAL_STAGES}: 提交视频任务  (80% 完成)")
    _log(f"{'='*40}")
    state_path = os.path.join(project, ".batch_state.json")
    if os.path.isfile(state_path):
        os.remove(state_path)
    _cmd_submit(project, tracker=tracker)
    _log(f"  └─ 验证并优化视频 prompt...")
    _cmd_fix_prompts(project, fix_type="video", max_retries=3)


def _auto_stage8(project: str, tracker: str) -> None:
    """阶段 8：轮询+拼接（内置 sleep 循环）"""
    _log(f"\n{'='*40}")
    _log(f"  阶段 8/{_TOTAL_STAGES}: 轮询完成状态  (90% 完成)")
    _log(f"{'='*40}")
    max_wait_cycles = 36
    for cycle in range(1, max_wait_cycles + 1):
        _log(f"\n  ── 轮询周期 {cycle}/{max_wait_cycles} ──")
        completed = _cmd_poll(project, tracker=tracker)
        if completed:
            _log("  ✅ 全自动流水线完成！  (100% 完成)")
            return
        if cycle < max_wait_cycles:
            _log(f"  ⏳ 视频尚未全部完成，10分钟（600秒）后继续轮询...")
            import time
            time.sleep(600)
    _log(f"  ❌ 轮询超时（{max_wait_cycles*10}分钟），视频未全部完成")


# ═══════════════════════════════════════════════════════════════
# 修复循环
# ═══════════════════════════════════════════════════════════════

def _auto_repair_assets(project: str, asset_type: str, generate_fn, verify_fn, verify_detailed_fn,
                        strategies: list, max_attempts: int = 10) -> None:
    for attempt in range(1, max_attempts + 1):
        kwargs = {}
        generate_fn(project, force=(attempt > 1), **kwargs)
        issues = verify_detailed_fn(project)
        real_failures = [i for i in issues if i.get("type") != "scene_style_fail"]
        if not real_failures:
            _log(f"  ✅ {asset_type}验证通过")
            return
        
        failure_types = {}
        for issue in real_failures:
            t = issue["type"]
            failure_types.setdefault(t, []).append(issue)
        
        strategy_idx = min(attempt - 1, len(strategies) - 1)
        strategy_name, strategy_desc = strategies[strategy_idx]
        _log(f"  ⚠️ {asset_type}验证未通过（{len(issues)}项问题）- 策略[{strategy_idx+1}] {strategy_desc}")
        
        if strategy_name in ("rebuild_prompt", "stronger_no_people", "add_detail_prompt"):
            _cmd_build_asset_prompts(project, force=True)
        if strategy_name == "change_model":
            _log("  ⚠️ 需要切换模型，请在配置中修改 model 参数后重试")
    
    _log(f"  ❌ {asset_type}修复失败（{max_attempts}次尝试后仍有问题）")
    raise SystemExit(f"❌ {asset_type}修复失败，需人工检查")


# ═══════════════════════════════════════════════════════════════
# 验证辅助函数
# ═══════════════════════════════════════════════════════════════

def _verify_character_assets(project: str, verbose: bool = True) -> int:
    from project_verify import verify_character_assets as _v
    return _v(project, verbose)


def _verify_character_assets_detailed(project: str) -> list[dict]:
    from project_verify import verify_character_assets_detailed as _v
    return _v(project)


def _verify_scene_assets(project: str, verbose: bool = True) -> int:
    from project_verify import verify_scene_assets as _v
    return _v(project, verbose)


def _verify_scene_assets_detailed(project: str) -> list[dict]:
    from project_verify import verify_scene_assets_detailed as _v
    return _v(project)


def _verify_troop_assets(project: str, verbose: bool = True) -> int:
    from project_verify import verify_troop_assets as _v
    return _v(project, verbose)


def _verify_troop_assets_detailed(project: str) -> list[dict]:
    from project_verify import verify_troop_assets_detailed as _v
    return _v(project)


# ═══════════════════════════════════════════════════════════════
# 生成函数桩
# ═══════════════════════════════════════════════════════════════

def _cmd_generate_characters(project: str, data: Optional[dict] = None, force: bool = False, **kwargs) -> None:
    from provider_factory import create_provider
    provider = create_provider(project)
    if data is None:
        with open(os.path.join(project, "script.json"), encoding="utf-8") as f:
            data = json.load(f)
    provider.generate_characters(project, data, force=force)


def _cmd_generate_troops(project: str, data: Optional[dict] = None, force: bool = False, **kwargs) -> None:
    """批量生成辅助资产图（troop_cards → 3 视角白背景全身展示）。"""
    if data is None:
        with open(os.path.join(project, "script.json"), encoding="utf-8") as f:
            data = json.load(f)
    cards = data.get("troop_cards", [])
    if not cards:
        _log("  ⚠️ troop_cards 为空，跳过")
        return

    from provider_factory import create_provider
    provider = create_provider(project)

    troop_dir = os.path.join(project, "images", "troops")
    os.makedirs(troop_dir, exist_ok=True)

    VIEWS = [
        ("front", "正面全身照，面向镜头，展示完整人物形象，白色纯色背景"),
        ("side", "侧面全身照，展示人物侧面轮廓，白色纯色背景"),
        ("back", "背面全身照，展示人物背面轮廓，白色纯色背景"),
    ]
    negative = "畸变, 变形, 模糊, 低质量, 丑陋, 多余肢体"

    for card in cards:
        name = card.get("name", "未知").replace(" ", "_")
        desc = card.get("description") or card.get("prompt", "")
        for suffix, view_desc in VIEWS:
            out_name = f"{name}_{suffix}.png"
            out_path = os.path.join(troop_dir, out_name)
            if os.path.isfile(out_path) and not force:
                _log(f"  ⏭️ {out_name} 已存在")
                continue
            prompt = (f"{desc}，{view_desc}，完整全身从头到脚包括靴子，"
                      "白色纯色背景，古风写实，全身视图，768×768")
            _log(f"  [{name}] 生成 {out_name}...")
            results = provider.generate_image(
                prompt=prompt, size="768x768",
                output_dir=troop_dir, output_name=out_name,
                project=project, negative_prompt=negative,
            )
            if results:
                _log(f"  ✅ {out_name}")
            else:
                _log(f"  ⚠️ {out_name} 生成失败")


def _cmd_generate_scenes(project: str, data: Optional[dict] = None, force: bool = False,
                          targets: Optional[list] = None, **kwargs) -> None:
    from provider_factory import create_provider
    from concurrent.futures import ThreadPoolExecutor
    
    if data is None:
        with open(os.path.join(project, "script.json"), encoding="utf-8") as f:
            data = json.load(f)
    
    cards = data.get("scene_cards", [])
    if not cards:
        _log("  ⚠️ scene_cards 为空，跳过")
        return
    
    # 视图级别过滤
    _VIEW_SUFFIX_MAP = {"_广角.png": "广角", "_中景.png": "中景", "_特写.png": "特写"}
    if targets:
        target_scene_views = {}
        for t in targets:
            basename = os.path.basename(t)
            for suffix, view_name in _VIEW_SUFFIX_MAP.items():
                if basename.endswith(suffix):
                    scene_id = basename[:-len(suffix)]
                    target_scene_views.setdefault(scene_id, set()).add(view_name)
                    break
        filtered = [c for c in cards if c.get("id", "") in target_scene_views]
        if filtered:
            _log(f"    ⏭️ 跳过 {len(cards)-len(filtered)} 个已验证场景")
            cards = filtered
    
    provider = create_provider(project)
    size = "1280x720"
    verb = "定向重试" if targets else "生成"
    _log(f"\n  {verb}场景资产 ({len(cards)} 个场景)")
    
    with ThreadPoolExecutor(max_workers=len(cards)) as executor:
        futures = {}
        for card in cards:
            target_v = list(target_scene_views.get(card.get("id", ""), set())) if targets else None
            futures[executor.submit(provider.generate_scene, project, card, size,
                                     force=force, target_views=target_v)] = card
        for future in futures:
            try:
                future.result()
            except Exception as e:
                _log(f"  ❌ 场景生成失败: {e}")


def _cmd_build_first_frames(project: str, force: bool = False) -> None:
    """为所有 shot 初始化 first_frame 块和提示词模板（不调用 API）。"""
    path = os.path.join(project, "script.json")
    if not os.path.isfile(path):
        raise SystemExit(f"未找到 script.json: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    _ag = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "..", "..", "agnes-ai", "scripts", "modules")
    _ag = os.path.normpath(_ag)
    if _ag not in sys.path:
        sys.path.insert(0, _ag)
    from prompt import _generate_prompt_template
    sys.path.pop(sys.path.index(_ag))
    shots = data.get("shots", [])
    for s in shots:
        sid = s["id"]
        ff = s.get("first_frame")
        if ff and isinstance(ff, dict) and ff.get("ref_images") and ff.get("prompt_file"):
            prompt_path = ff["prompt_file"]
            if not os.path.isabs(prompt_path):
                prompt_path = os.path.join(project, prompt_path)
            if os.path.isfile(prompt_path):
                if not force:
                    continue
        _generate_prompt_template(project, sid)
    _log(f"  ✅ first_frame 初始化完成 ({len(shots)} shots)")


def _cmd_generate_images(project: str, shot_ids: Optional[list] = None,
                          retry_failed: bool = False, auto_verify: bool = True,
                          parallel: bool = True, **kwargs) -> None:
    """批量生成首帧图。"""
    from provider_factory import create_provider
    from config import load_api_key
    _ag = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "..", "..", "agnes-ai", "scripts", "modules")
    _ag = os.path.normpath(_ag)
    if _ag not in sys.path:
        sys.path.insert(0, _ag)
    from prompt import _generate_prompt_template
    sys.path.pop(sys.path.index(_ag))
    
    path = os.path.join(project, "script.json")
    if not os.path.isfile(path):
        raise SystemExit(f"未找到 script.json: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    shots = data.get("shots", [])
    provider = create_provider(project)
    api_key = load_api_key()
    
    total = len(shot_ids) if shot_ids else len(shots)
    completed = 0
    for idx, s in enumerate(shots):
        if shot_ids and s["id"] not in shot_ids:
            continue
        _log(f"  生成首帧图 [{idx+1}/{total}] shot_{s['id']:02d}...")
        result = provider.generate_first_frame(project, s, data)
        if result and result.get("status") == "ok":
            completed += 1
    _log(f"  ✅ 首帧图生成完成 ({completed}/{total})")


def _cmd_verify_scenes(project: str) -> None:
    from project_verify import _verify_all_scenes
    _log(f"\n{'='*60}")
    _log(f"  🔍 verify-scenes: 检查场景图人物")
    results = _verify_all_scenes(project)
    if not results:
        _log("  ⚠️ 未找到场景图")
        return
    for r in results:
        status = "✅" if r.get("passed") else "❌"
        _log(f"  {status} {r.get('path', '?')}: {'通过' if r.get('passed') else '有误'}")
    _log("  ✅ 场景验证完成")


def _cmd_validate_script(project: str) -> None:
    """独立命令：检查 script.json 占位符和语法。"""
    _log(f"\n{'='*60}")
    _log(f"  🔍 validate-script: 检查 script.json")
    data = _check_script(project)
    _log("  ✅ script.json 检查通过")


def _cmd_validate_all(project: str, verbose: bool = False) -> None:
    path = os.path.join(project, "script.json")
    if not os.path.isfile(path):
        raise SystemExit(f"未找到 script.json: {path}")
    data = _check_script(project)
    _log("  ✅ 全量预检完成")


def _cmd_optimize(project: str, strict: bool = True, force: bool = False,
                   dry_run: bool = False, report_only: bool = False,
                   sync_type: str = "", fix_prompts: bool = False) -> None:
    """调用 script-optimizer 优化 script.json。"""
    opt_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "script-optimizer", "scripts")
    if not os.path.isdir(opt_dir):
        raise SystemExit(f"未找到 script-optimizer 目录: {opt_dir}")
    if opt_dir not in sys.path:
        sys.path.insert(0, opt_dir)
    
    from optimize import OptimizerV2
    opt = OptimizerV2(project, strict=strict, gentle=True)
    result = opt.run()
    
    if fix_prompts:
        remaining = result.get("remaining_issues", [])
        shot_issues = [i for i in remaining if "shot" in i.get("location", "") and "_image" in i.get("location", "")]
        video_issues = [i for i in remaining if "video_shot" in i.get("location", "")]
        char_issues = [i for i in remaining if "characters/" in i.get("location", "")]
        scene_issues = [i for i in remaining if "scenes/" in i.get("location", "")]
        
        from prompt_builder import fix_first_frame_prompts, fix_video_prompts, validate_prompts
        fix_first_frame_prompts(project, shot_issues) if shot_issues else None
        fix_video_prompts(project, video_issues) if video_issues else None
    
    status = result.get("status", "ok")
    if status == "stuck":
        remaining_p0 = [ri for ri in result.get("remaining_issues", []) if ri.get("priority") == "P0"]
        only_transient = all(
            "reference_images" in ri.get("msg", "") or "first_frame.prompt_file" in ri.get("msg", "")
            or "global_style" in ri.get("msg", "")
            for ri in remaining_p0
        )
        if only_transient:
            _log(f"  ⏭️ P0 仅为 reference_images/first_frame.prompt_file/global_style，继续流水线")
        else:
            raise SystemExit("script.json 存在无法自动修复的 P0 问题")


def _cmd_build_asset_prompts(project: str, force: bool = False) -> None:
    files = _build_prompts(project, force=force)
    _log(f"  ✅ 生成 {len(files)} 个 prompt 文件:")
    for f in files:
        _log(f"     {os.path.relpath(f, project)}")


def _cmd_fix_prompts(project: str, fix_type: str = "first_frame", max_retries: int = 3) -> int:
    issues = _validate_prompts(project)
    p0 = [i for i in issues if i["priority"] == "P0"]
    p1 = [i for i in issues if i["priority"] == "P1"]
    
    if p0:
        _log(f"  ⚠️ 发现 {len(p0)} 个 P0 问题")
        return -1
    
    if p1:
        _log(f"  🛠️ 自动修复 {len(p1)} 个 P1 问题...")
        if fix_type == "first_frame":
            _fix_ff_prompts(project, [i for i in p1 if "shot" in i.get("location", "").lower()])
        elif fix_type == "video":
            _fix_video_prompts(project, [i for i in p1 if "video" in i.get("location", "").lower()])
    
    return len(p1)


def _cmd_submit(project: str, tracker: str = "feishu",
                force: bool = False, force_shot: list[int] | None = None) -> None:
    """提交 shot 视频生成任务。force=True 强制全部重提，force_shot=[ids] 只重提指定 shot。"""
    # 确保 agnes-ai scripts/modules 在 sys.path 中（for modules.prompt）
    _ag = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "..", "..", "agnes-ai", "scripts", "modules")
    _ag = os.path.normpath(_ag)
    if _ag not in sys.path:
        sys.path.insert(0, _ag)
    from prompt import _generate_prompt_template  # agnes-ai 的 prompt 模块
    sys.path.pop(sys.path.index(_ag))  # 用完恢复，避免后续导入冲突
    
    from task_tracker import init_tracker
    init_tracker(project, tracker)
    
    from provider_factory import create_provider
    
    provider = create_provider(project)
    _log(f"  [Provider] {provider.__class__.__name__}")
    
    path = os.path.join(project, "script.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    shots = data.get("shots", [])
    for s in shots:
        sid = s["id"]
        if force_shot is not None and sid not in force_shot:
            continue  # 只提指定的 shot
        _log(f"  [Agnes] shot_{sid}提交...")
        prompt = s.get("description", "")
        duration = s.get("duration", 5)
        aspect = data.get("aspect_ratio", "9:16")
        ff_path = os.path.join(project, "images", "storyboard", f"shot_{sid:02d}_first_frame.png")
        ref_img = ff_path if os.path.isfile(ff_path) else None
        result = provider.submit_video(
            project=project, shot_id=sid, prompt=prompt,
            ref_img=ref_img, duration=duration, aspect=aspect,
        )
        if result:
            _log(f"  ✅ shot_{sid:02d} 提交成功")
        else:
            _log(f"  ⚠️ shot_{sid:02d} 提交失败")


def _cmd_poll(project: str, tracker: str = "feishu") -> bool:
    """轮询所有 shot 视频状态。"""
    from video_utils import _cmd_poll as _vup
    return _vup(project, tracker)


def _cmd_stitch(project: str, tracker: str = "feishu") -> Optional[str]:
    """独立拼接：HF无字幕→烧分段字幕→CRF18（不重新提交/轮询）。"""
    from video_utils import _cmd_stitch as _vus
    return _vus(project, tracker)


def _cmd_status(project: str, json_output: bool = True) -> None:
    """查看项目状态。默认输出 JSON，加 --text 输出人类可读格式。"""
    from project_status import print_status
    print_status(project, json_output=json_output)


def _cmd_tracker_sync(project: str, tracker: str = "feishu") -> None:
    from task_tracker import init_tracker, get_current_backend
    init_tracker(project, tracker)
    backend = get_current_backend()
    if hasattr(backend, "sync_to_local"):
        count = backend.sync_to_local(project)
        _log(f"  ✅ 反向同步完成: 从飞书拉了 {count} 条记录到本地 task_tracker.json")
    else:
        _log(f"  ⏭️ 当前 tracker 不支持反向同步（{type(backend).__name__}）")


def _cmd_preview(project: str) -> None:
    from project_preview import generate_preview
    out = generate_preview(project)
    _log(f"  ✅ 预览已生成: {out}")


def _cmd_report(project: str, output: str = "") -> None:
    from project_stats import generate_stats
    out = generate_stats(project, output or None)
    _log(f"  ✅ 报告已生成: {out}")


def _cmd_update_prompts(project: str) -> None:
    _cmd_build_asset_prompts(project, force=True)


def _cmd_repair(project: str, shot_ids: Optional[list] = None) -> None:
    """自动修复提示词文件：重建 assets prompts + 修复 first_frame/video 提示词。"""
    _cmd_build_asset_prompts(project, force=True)
    fixed = 0
    fixed += _cmd_fix_prompts(project, fix_type="first_frame")
    fixed += _cmd_fix_prompts(project, fix_type="video")
    if shot_ids:
        _log(f"  针对指定 shot 额外修复: {shot_ids}")
    _log(f"  ✅ 提示词修复完成（修复了 {fixed} 个问题）")


def _cmd_reset_prompts(project: str) -> None:
    import shutil
    for d in ["prompts/storyboard", "prompts/videos", "prompts/characters", "prompts/scenes"]:
        p = os.path.join(project, d)
        if os.path.isdir(p):
            shutil.rmtree(p)
    _log("  ✅ 所有 prompt 已重置")


def _cmd_diff_all(project: str) -> None:
    """批量生成新旧首帧图对比页 + 索引页。"""
    import glob, re as _re
    from project_diff import _generate_diff_html

    storyboard = os.path.join(project, "images", "storyboard")
    backup_dir = os.path.join(storyboard, "backup")

    if not os.path.isdir(storyboard):
        _log("  ⚠️ 未找到 images/storyboard/ 目录")
        return

    new_files = sorted(glob.glob(os.path.join(storyboard, "shot_*_first_frame.png")))
    pairs: list[tuple[str, str, int]] = []

    if os.path.isdir(backup_dir):
        for new_path in new_files:
            basename = os.path.basename(new_path)
            old_path = os.path.join(backup_dir, basename)
            if os.path.isfile(old_path):
                m = _re.search(r"shot_(\d+)", basename)
                sid = int(m.group(1)) if m else 0
                pairs.append((old_path, new_path, sid))

    if not pairs:
        for new_path in new_files:
            base, ext = os.path.splitext(new_path)
            old_path = base + "_old" + ext
            if os.path.isfile(old_path):
                m = _re.search(r"shot_(\d+)", os.path.basename(new_path))
                sid = int(m.group(1)) if m else 0
                pairs.append((old_path, new_path, sid))

    if not pairs:
        _log("  ⏭️ 未找到新旧对比文件。请将旧首帧图放入 images/storyboard/backup/ 或命名为 *_old.png")
        return

    output_dir = os.path.join(project, "output")
    os.makedirs(output_dir, exist_ok=True)
    index_items: list[str] = []

    for old_path, new_path, sid in pairs:
        shot = {"id": sid, "description": os.path.basename(new_path)}
        diff_path = _generate_diff_html(project, shot, old_path, new_path)
        rel = os.path.relpath(diff_path, output_dir)
        index_items.append(f'    <li><a href="{rel}">Shot {sid:02d} — {os.path.basename(new_path)}</a></li>')
        _log(f"  ✅ Shot {sid:02d} 对比页已生成")

    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diff All — 新旧首帧图对比索引</title>
<style>
body {{ font-family: -apple-system, 'Microsoft YaHei', sans-serif; background: #0f0f1a; color: #e0e0e0; padding: 20px; }}
h1 {{ text-align: center; margin-bottom: 8px; }}
p.count {{ text-align: center; color: #888; margin-bottom: 24px; }}
ul {{ list-style: none; padding: 0; max-width: 600px; margin: 0 auto; }}
li {{ background: #1a1a2e; margin: 6px 0; padding: 10px 16px; border-radius: 6px; }}
a {{ color: #e94560; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<h1>新旧首帧图对比</h1>
<p class="count">共 {len(index_items)} 个 shot</p>
<ul>{"".join(index_items)}</ul>
</body>
</html>"""
    index_path = os.path.join(output_dir, "diff_index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    _log(f"  ✅ 索引页已生成: {index_path}")


# ═══════════════════════════════════════════════════════════════
# 自动流水线入口
# ═══════════════════════════════════════════════════════════════

def _cmd_auto(project: str, tracker: str = "feishu") -> None:
    """全自动流水线：生成角色资产 → 场景资产 → 首帧图 → 提交 → 轮询 → 拼接。"""
    import signal as _sig
    _log_path = os.path.join(project, "auto.log")
    _log("=" * 60)
    _log("  🚀 全自动流水线启动")
    _log(f"  tracker: {tracker}")
    _log("=" * 60)
    
    path = os.path.join(project, "script.json")
    if not os.path.isfile(path):
        raise SystemExit(f"未找到 script.json: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    _check_json_quotes(raw)
    data = json.loads(raw)
    _check_script_placeholders(project, data)
    state = _load_state(project)
    
    # 阶段 0-8
    _do(project, "0", "脚本优化", lambda: _auto_stage0(project), state)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _do(project, "1", "构建 prompt 文件", lambda: _auto_stage1(project), state)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _do(project, "2", "角色资产", lambda: _auto_stage2(project, data), state)
    _do(project, "3", "辅助资产", lambda: _auto_stage3(project, data), state)
    _do(project, "4", "场景资产", lambda: _auto_stage4(project, data), state)
    _do(project, "5", "初始化 first_frame", lambda: _auto_stage5(project), state)
    _do(project, "6", "首帧图生成", lambda: _auto_stage6(project, data), state)
    _do(project, "7", "提交视频", lambda: _auto_stage7(project, tracker), state)
    _do(project, "8", "轮询+拼接", lambda: _auto_stage8(project, tracker), state)
