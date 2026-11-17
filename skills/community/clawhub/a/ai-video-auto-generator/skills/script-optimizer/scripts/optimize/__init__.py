#!/usr/bin/env python3
"""
script-optimizer v2 — 全自动多轮迭代脚本质量优化器

全自动化，零人工干预。提供了日志记录、类型感知默认值、gentle 模式等高级功能。

用法：
  python3 scripts/optimize/__init__.py --project <项目目录>              # 全自动
  python3 scripts/optimize/__init__.py --project <项目目录> --strict     # strict 模式
  python3 scripts/optimize/__init__.py --project <项目目录> --gentle     # 仅修复明显的模板默认值，不覆盖人工编辑
  python3 scripts/optimize/__init__.py --project <项目目录> --log-file optimize.log  # 指定日志文件
"""

import json, os, re, sys, copy
from datetime import datetime

# 将父级 scripts/ 目录加入 sys.path，保持模块间导入正常工作
_OPT_SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _OPT_SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _OPT_SCRIPTS_DIR)

from prompt_builder import validate_prompts as _validate_asset_prompts, _extract_style_prefix

# ── 路径锚点 ──
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TYPE_REFS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(SKILL_DIR))), "references", "types")

# 规则与默认值常量（从 rules.py 导入，减少 __init__.py 体积）
from .rules import *  # all uppercase constants
from .rules import _BASE_DEFAULTS  # _BASE_DEFAULTS 以下划线开头，import * 不包含

# ═══════════════════════════════════════════════════════════════
# --json 输出 schema（供 project-generate 解析）：
#
# 正常运行 (--json):
#   {"status": "pass"|"stuck"|"pass_with_known", "rounds": 1,
#    "p0_remaining": 0, "p1_remaining": 0, "p2_total": 3,
#    "auto_fixes": [...], "remaining_issues": [...]}
#
# dry-run (--dry-run --json):
#   {"status": "dry_run", "p0": 0, "p1": 0,
#    "fixes": [...], "issues": [...]}
#
# sync-type (--sync-type --json):
#   {"status": "sync_type_ok", "changed": [{"key":"global_style",...}]}
#
# report-only (--report-only --json):
#   {"status": "report", "p0": 0, "p1": 0, "p2": 0, "issues": [...]}
#
# remaining_issues[i]:
#   {"priority": "P0"|"P1", "msg": "...", "location": "..."}
# ═══════════════════════════════════════════════════════════════

# ── 类型感知默认值：从 references/types/*.md 懒加载 ──
_TYPE_DEFAULTS_CACHE: dict[str, dict] = {}

# ── camera_movement 文本推断 ──
_CAMERA_KW_MAP = [
    ("广角", "广角远景，镜头缓慢，建立场景空间感"),
    ("特写推近", "近景推近变焦，聚焦细节"),
    ("特写", "近景特写，聚焦面部表情"),
    ("过肩", "过肩镜头，跟随对话关系"),
    ("双人", "中景双人镜头，两人同框"),
    ("俯拍", "俯拍镜头，增强画面张力"),
    ("仰拍", "低角度仰拍镜头，增强画面张力"),
    ("主观视角", "第一人称主观视角，轻微手持晃动"),
    ("慢动作", "慢镜头，强调动作细节"),
    ("跟拍", "跟拍镜头，保持动态追踪"),
    ("全景", "全景固定镜头，角色全身可见"),
    ("中景", "中景固定镜头，标准叙事视角"),
    ("反应", "近景特写，聚焦反应瞬间"),
]

# ── 运镜动作词（2-3个不同运镜要求） ──
# 每个 shot 的 description 应至少包含 2 种不同的运镜类型
_CAMERA_MOVE_KINDS = {
    "推": "镜头向前推近",
    "拉": "镜头向后拉远",
    "摇": "镜头左右摇摄",
    "移": "镜头横向平移",
    "跟": "镜头跟随主体移动",
    "仰": "镜头向上仰拍",
    "俯": "镜头向下俯拍",
    "升降": "镜头缓缓升起",
    "旋转": "镜头环绕旋转",
    "变焦": "镜头变焦推拉",
    "晃动": "轻微手持晃动",
}
# 检测运镜动作的关键词 → 所属运镜类型
_CAMERA_MOVE_DETECT = {
    "推近": "推", "推进": "推", "推入": "推", "向前": "推",
    "拉远": "拉", "拉开": "拉", "后退": "拉", "向后": "拉",
    "摇摄": "摇", "左右摇": "摇", "横摇": "摇", "pan": "摇",
    "平移": "移", "横移": "移", "侧移": "移",
    "跟随": "跟", "跟拍": "跟", "跟踪": "跟",
    "俯拍": "俯", "俯视": "俯", "向下": "俯",
    "仰拍": "仰", "仰视": "仰", "向上": "仰",
    "升起": "升降", "下降": "升降", "升降": "升降",
    "环绕": "旋转", "旋转": "旋转", "环拍": "旋转",
    "变焦": "变焦", "zoom": "变焦",
    "手持": "晃动", "晃动": "晃动", "抖动": "晃动",
}
# 运镜空间组合规则：推/拉(Z轴) 摇/移(X轴) 俯/仰(Y轴) 可同轴或跨轴组合
# 只有互斥的（推+拉、仰+俯、旋转+摇）不能组合
_CAMERA_INCOMPATIBLE = {
    frozenset({"推", "拉"}),   # 不能同时推和拉
    frozenset({"仰", "俯"}),   # 不能同时仰和俯
    frozenset({"摇", "旋转"}), # 都是水平旋转，冗余
    frozenset({"升降", "俯"}), # 升降(垂直移动) + 俯(角度) 不冲突，可共存
    frozenset({"升降", "仰"}),
}


def _infer_camera_from_text(text: str) -> str:
    """从 description 或 camera 字段的文字推断 camera_movement。
    
    优先级按匹配顺序排列，第一个匹配返回，无匹配返回空。
    """
    for kw, desc in _CAMERA_KW_MAP:
        if kw in text:
            return desc
    return ""


def _load_type_defaults(vtype: str) -> dict:
    """从对应类型 .md 文件中读取 optimizer-defaults JSON 块。"""
    if vtype in _TYPE_DEFAULTS_CACHE:
        return _TYPE_DEFAULTS_CACHE[vtype]
    type_map = {
        "电影级长剧": "电影级长剧", "短剧": "短剧",
        "文旅": "文旅", "default": "default",
    }
    fname = type_map.get(vtype, "default")
    path = os.path.join(TYPE_REFS_DIR, f"{fname}.md")
    if not os.path.isfile(path):
        _TYPE_DEFAULTS_CACHE[vtype] = {}
        return {}
    with open(path, encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'<!--\s*optimizer-defaults\s*-->\s*```json\s*\n(.*?)```', content, re.DOTALL)
    if not m:
        _TYPE_DEFAULTS_CACHE[vtype] = {}
        return {}
    try:
        result = json.loads(m.group(1).strip())
        _TYPE_DEFAULTS_CACHE[vtype] = result
        return result
    except json.JSONDecodeError as e:
        print(f"  ⚠️ 警告: {path} 的 optimizer-defaults JSON 格式错误: {e}", file=sys.stderr, flush=True)
        _TYPE_DEFAULTS_CACHE[vtype] = {}
        return {}


class Issue:
    def __init__(self, priority: str, msg: str, location: str = ""):
        self.priority = priority
        self.msg = msg
        self.location = location


class OptimizerV2:
    def __init__(self, project: str, strict: bool = False, gentle: bool = True, json_mode: bool = False):
        self.project = os.path.abspath(project)
        self.script_path = os.path.join(self.project, "script.json")
        self.rules_path = os.path.join(self.project, ".optimizer-rules.json")
        self.strict = strict
        self.gentle = gentle
        self.json_mode = json_mode
        self.data: dict = {}
        self.round = 0
        self.fix_log: list[tuple[str, str]] = []
        self.history: list[tuple[int, int]] = []
        self.log_lines: list[str] = []
        self.profile: dict = {}
        self.validation_cfg: dict = {}
        self._profile_loaded = False
        self._dirty = False  # 是否有实际改动  # 标记 profile 是否已加载

        # 延迟加载 — load() 后才真正解析配置文件
        # _load_profile() 在 load() 中被调用

    def _load_profile(self):
        """从 video type reference .md 文件加载默认配置。
        在 load() 之后调用，此时 self.data 可用，避免重复读文件。"""
        if self._profile_loaded:
            return

        if os.path.isfile(self.rules_path):
            try:
                with open(self.rules_path, encoding="utf-8") as f:
                    overrides = json.load(f)
                self.profile = {**_BASE_DEFAULTS, **overrides}
                self._logv("已加载 .optimizer-rules.json 覆盖规则")
                self._parse_validation()
                self._profile_loaded = True
                return
            except Exception:
                pass
        # 从 self.data（已由 load() 加载）获取 type 字段
        vtype = self.data.get("script", {}).get("type", "default") if self.data else "default"
        # 从类型 .md 文件读取
        type_cfg = _load_type_defaults(vtype)
        if type_cfg:
            self.profile = {**_BASE_DEFAULTS, **type_cfg}
            self._logv(f"类型配置: {vtype}（从 {vtype}.md 读取）")
        else:
            self.profile = dict(_BASE_DEFAULTS)
            self._logv(f"类型配置: {vtype}（.md 无配置，使用基础默认值）")
        self._parse_validation()
        self._profile_loaded = True

    def _parse_validation(self):
        """从 profile.validation 解析验证规则"""
        v = self.profile.get("validation", {})
        self.validation_cfg = {
            "min_description_length": v.get("min_description_length", 15),
            "require_all_face_details": v.get("require_all_face_details", False),
            "require_all_scene_fields": v.get("require_all_scene_fields", False),
            "quality_bad_values": v.get("quality_bad_values", QUALITY_BAD_VALUES),
        }

    # ═══════════════════════════════════════════
    #  日志
    # ═══════════════════════════════════════════

    def _logv(self, msg: str):
        """verbose 日志（仅追加到 log_lines，不输出到终端避免干扰）"""
        self.log_lines.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def _log(self, msg: str):
        """标准日志（仿真 emoji 编码失败时降级）"""
        try:
            print(f"  {msg}", file=sys.stderr if self.json_mode else None, flush=True)
        except UnicodeEncodeError:
            # GBK 终端无法渲染 emoji 时的降级
            safe = msg.encode("utf-8", errors="replace").decode("utf-8")
            print(f"  {safe}", file=sys.stderr if self.json_mode else None, flush=True)
        self.log_lines.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def _fix(self, action: str, detail: str):
        """记录一次修复行为"""
        self.fix_log.append((action, detail))
        self._dirty = True
        self._log(f"  ✅ {action}: {detail}")

    def write_log(self, path: str | None = None):
        """写入日志文件"""
        if path is None:
            path = os.path.join(self.project, "optimize.log")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# optimize.log — script-optimizer v2\n")
            f.write(f"# 项目: {os.path.basename(self.project)}\n")
            f.write(f"# 时间: {datetime.now().isoformat()}\n")
            f.write(f"# strict={self.strict} gentle={self.gentle}\n")
            f.write(f"# 类型配置: {self.profile.get('aesthetic_style', 'N/A')[:40]}\n")
            f.write(f"# {'='*60}\n")
            for line in self.log_lines:
                f.write(line + "\n")

    # ═══════════════════════════════════════════
    #  加载 / 保存
    # ═══════════════════════════════════════════

    def load(self):
        if not os.path.isfile(self.script_path):
            raise SystemExit(f"❌ script.json 不存在: {self.script_path}")
        with open(self.script_path, encoding="utf-8") as f:
            self.data = json.load(f)
        # data 就绪后加载 profile（延迟加载，避免 __init__ 时读文件）
        self._load_profile()
        self._log(f"📂 加载项目: {os.path.basename(self.project)}")
        self._log(f"   角色={len(self.data.get('character_cards', []))} "
                  f"场景={len(self.data.get('scene_cards', []))} "
                  f"镜头={len(self.data.get('shots', []))}")

    def save(self):
        if self._dirty:
            self.data.setdefault("script", {})["_optimizer_version"] = OPTIMIZER_VERSION
        with open(self.script_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        self._logv("💾 script.json 已保存")
        # 检查 .gitignore 是否包含 optimize.log
        gitignore = os.path.join(self.project, ".gitignore")
        log_name = os.path.basename(self.project) if False else "optimize.log"
        if os.path.isfile(gitignore):
            with open(gitignore, encoding="utf-8") as f:
                if "optimize.log" not in f.read():
                    self._logv("💡 建议将 optimize.log 加入 .gitignore")
        else:
            self._logv("💡 建议创建 .gitignore 并加入 optimize.log")

    # ═══════════════════════════════════════════
    #  验证层
    # ═══════════════════════════════════════════

    def validate(self) -> list[Issue]:
        issues = []
        issues += self._v_script()
        issues += self._v_characters()
        issues += self._v_scenes()
        issues += self._v_shots()
        # prompt 文件验证（角色/场景/首帧图/视频）
        try:
            prompt_issues = _validate_asset_prompts(self.project)
            for pi in prompt_issues:
                issues.append(Issue(pi["priority"], pi["msg"], pi.get("location", "")))
        except Exception:
            pass  # prompt 文件验证可选，不阻塞主流程
        # 按严重程度排序：P0 > P1 > P2
        sort_key = {"P0": 0, "P1": 1, "P2": 2}
        issues.sort(key=lambda i: (sort_key.get(i.priority, 9), i.msg))
        return issues

    def _v_script(self) -> list[Issue]:
        issues = []
        sc = self.data.get("script", {})
        if not sc: return [Issue("P0", "script 顶层块缺失", "script")]
        for key, typ in REQUIRED_GLOBAL_KEYS.items():
            if key not in sc or not sc[key]:
                issues.append(Issue("P0", f"script.{key} 缺失", f"script.{key}"))
        as_ = sc.get("aesthetic_style", "")
        if not as_:
            issues.append(Issue("P0", "script.aesthetic_style 未设置", "script.aesthetic_style"))
        elif len(as_) < 5 or as_ in ("western", "eastern", "chinese", "default"):
            issues.append(Issue("P1", "script.aesthetic_style 过于简单", "script.aesthetic_style"))
        if not sc.get("global_style"):
            issues.append(Issue("P0", "script.global_style 未设置（prompt 核心风格基底，必须注入）",
                                "script.global_style"))
        elif len(sc["global_style"]) < 15:
            issues.append(Issue("P0", f"script.global_style 过于简单 ({len(sc['global_style'])}字，应≥15字，例如'AI动漫风，画面明亮清晰，色彩饱和度高，细节丰富')",
                                "script.global_style"))
        if not sc.get("aesthetic_anchor"):
            issues.append(Issue("P2", "script.aesthetic_anchor 未设置", "script.aesthetic_anchor"))
        # 业务规则检查
        if not sc.get("asset_generation_model"):
            issues.append(Issue("P2", "script.asset_generation_model 未设置（将由 provider 自动决定）",
                                "script.asset_generation_model"))
        if not sc.get("first_frame_model"):
            issues.append(Issue("P2", "script.first_frame_model 未设置（将由 provider 自动决定）",
                                "script.first_frame_model"))
        if not sc.get("video_model"):
            issues.append(Issue("P2", "script.video_model 未设置（将由 provider 自动决定）",
                                "script.video_model"))
        if not sc.get("scene_aspect_ratio"):
            issues.append(Issue("P1", "script.scene_aspect_ratio 未设置（应固定为 16:9）",
                                "script.scene_aspect_ratio"))
        if not sc.get("scene_size"):
            issues.append(Issue("P1", "script.scene_size 未设置（应固定为 1280x720）",
                                "script.scene_size"))
        elif sc["scene_size"] != "1280x720":
            issues.append(Issue("P1", f"script.scene_size = '{sc['scene_size']}'，应为 1280x720",
                                "script.scene_size"))
        return issues

    def _v_characters(self) -> list[Issue]:
        issues = []
        chars = self.data.get("character_cards", [])
        if not chars: return [Issue("P0", "character_cards 为空", "character_cards")]

        style_prefixes = set()
        for i, c in enumerate(chars):
            name = c.get("name", f"[{i}]")
            loc = f"character_cards[{i}]({name})"
            for f in REQUIRED_CHAR_FIELDS:
                if not c.get(f, ""):
                    issues.append(Issue("P1", f"{loc}.{f} 为空", f"{loc}.{f}"))
            for f in ["name", "title", "personality", "build"]:
                for p in PLACEHOLDER_PATTERNS:
                    if re.search(p, c.get(f, "")):
                        issues.append(Issue("P0", f"{loc}.{f}: 模板占位符", f"{loc}.{f}"))
            app = c.get("appearance", {})
            for sub in REQUIRED_APPEARANCE_FIELDS:
                if not app.get(sub, ""):
                    issues.append(Issue("P0", f"{loc}.appearance.{sub} 为空", f"{loc}.appearance.{sub}"))
                for p in PLACEHOLDER_PATTERNS:
                    if re.search(p, app.get(sub, "")):
                        issues.append(Issue("P0", f"{loc}.appearance.{sub}: 模板占位符", f"{loc}.appearance.{sub}"))
            fd = app.get("face_details", {})
            require_all_fd = self.validation_cfg.get("require_all_face_details", False)
            for sub in REQUIRED_FACE_DETAILS:
                if not fd.get(sub, ""):
                    p = "P1" if require_all_fd else "P2"
                    issues.append(Issue(p, f"{loc}.face_details.{sub} 为空", f"{loc}.face_details.{sub}"))
            # 内容质量检查
            dm = c.get("distinctive_mark", "")
            if dm and dm in ("标志性特征", ""):
                issues.append(Issue("P1", f"{loc}.distinctive_mark 是默认值", f"{loc}.distinctive_mark"))
            elif len(dm) < 8:
                issues.append(Issue("P1", f"{loc}.distinctive_mark 太短 ({len(dm)}字)", f"{loc}.distinctive_mark"))
            # 默认 face 值检查 — 从类型配置读取 quality_bad_values
            qbv = self.validation_cfg.get("quality_bad_values", QUALITY_BAD_VALUES)
            for sub, bad_list in qbv.items():
                val = c.get("appearance", {}).get("face_details", {}).get(sub, "") if sub != "distinctive_mark" else c.get("distinctive_mark", "")
                if val in bad_list:
                    issues.append(Issue("P2", f"{loc}.face_details.{sub}: 是默认值 '{val}'", f"{loc}.face_details.{sub}"))
            g = c.get("gender", "")
            if g and g not in ("男", "女", "male", "female"):
                issues.append(Issue("P1", f"{loc}.gender = '{g}' 非标准", f"{loc}.gender"))
            s = c.get("aesthetic_style", "")[:8]
            if s:
                style_prefixes.add(s)
            # weapons/actions 模板值检查
            weps = set(c.get("weapons", []))
            acts = set(c.get("actions", []))
            if weps and weps == TEMPLATE_WEAPONS:
                issues.append(Issue("P2", f"{loc}.weapons = {sorted(weps)} 是模板默认值", f"{loc}.weapons"))
            if acts and acts == TEMPLATE_ACTIONS:
                issues.append(Issue("P2", f"{loc}.actions = {sorted(acts)} 是模板默认值", f"{loc}.actions"))
            # 业务规则：角色 aesthetic_style 格式检查（应为"角色风格：xxx"格式，与 global_style 组合使用）
            aes_c = c.get("aesthetic_style", "")
            if aes_c and not aes_c.startswith("角色风格："):
                issues.append(Issue("P2", f"{loc}.aesthetic_style = '{aes_c[:30]}' — 应为'角色风格：xxx'格式与 global_style 组合使用",
                                    f"{loc}.aesthetic_style"))
            # 业务规则：资产白背景
            bg = c.get("asset_background", "")
            if bg and bg not in ("white", "纯白"):
                issues.append(Issue("P1", f"{loc}.asset_background = '{bg}'，应为 white（纯白底）", f"{loc}.asset_background"))
            elif not bg:
                issues.append(Issue("P2", f"{loc}.asset_background 未设置（角色定妆照应为纯白背景）", f"{loc}.asset_background"))
            # 业务规则：标准视图无武器
            nw = c.get("no_weapon_for_standard_views")
            if nw is None:
                issues.append(Issue("P2", f"{loc}.no_weapon_for_standard_views 未设置", f"{loc}.no_weapon_for_standard_views"))
        if len(style_prefixes) > 1:
            # 只有部分角色共享前缀而其他角色不同时才算不一致
            # 所有角色各自不同是各角色独立风格的设计意图，不报警
            from collections import Counter
            prefix_counts = Counter(style_prefixes)
            if any(count > 1 for count in prefix_counts.values()):
                issues.append(Issue("P2", f"角色间 aesthetic_style 前缀部分不一致（有角色共享前缀但另有不同）: {style_prefixes}", "character_cards"))
        return issues

    def _v_scenes(self) -> list[Issue]:
        issues = []
        scenes = self.data.get("scene_cards", [])
        if not scenes:
            return [Issue("P1", "scene_cards 为空", "scene_cards")]

        # troop_cards 检查
        troops = self.data.get("troop_cards", [])
        if troops:
            for i, tc in enumerate(troops):
                if not tc.get("name", ""):
                    issues.append(Issue("P1", f"troop_cards[{i}].name 为空", f"troop_cards[{i}]"))
                if not tc.get("appearance", ""):
                    issues.append(Issue("P1", f"troop_cards[{i}]({tc.get('name','?')}).appearance 为空",
                                        f"troop_cards[{i}]"))
                # 辅助资产白背景
                if not tc.get("asset_background"):
                    issues.append(Issue("P2", f"troop_cards[{i}]({tc.get('name','?')}).asset_background 未设置",
                                        f"troop_cards[{i}]"))
                # 尺寸检查（辅助资产固定 768x768）
                if tc.get("size") and tc["size"] != "768x768":
                    issues.append(Issue("P2", f"troop_cards[{i}].size = '{tc['size']}'，应为 768x768",
                                        f"troop_cards[{i}]"))
                # 检查资产图是否存在
                tname = tc.get("name", f"troop{i}")
                troop_dir = os.path.join(self.project, "images", "troops")
                troop_files = [os.path.isfile(os.path.join(troop_dir, f"{tname}_{v}.png"))
                               for v in ["front", "side", "back"]]
                if os.path.isdir(troop_dir) and any(troop_files):
                    missing = sum(1 for f in troop_files if not f)
                    if missing:
                        issues.append(Issue("P1", f"troop_cards[{i}]({tname}): 缺少 {missing} 个视图",
                                            f"troop_cards[{i}]"))
        for i, sc in enumerate(scenes):
            n = sc.get("name", f"[{i}]")
            loc = f"scene_cards[{i}]({n})"
            for f in REQUIRED_SCENE_FIELDS:
                if not sc.get(f, ""):
                    issues.append(Issue("P0", f"{loc}.{f} 为空", f"{loc}.{f}"))
            for sub in ["time_of_day", "weather", "color_scheme", "lighting", "mood"]:
                p = "P2" if sub in ("lighting", "mood") else "P1"
                if not sc.get(sub, ""):
                    issues.append(Issue(p, f"{loc}.{sub} 未设置", f"{loc}.{sub}"))
        return issues

    def _v_shots(self) -> list[Issue]:
        issues = []
        shots = self.data.get("shots", [])
        groups = self.data.get("shot_groups", [])
        if not shots: return [Issue("P0", "shots 为空", "shots")]
        if not groups: issues.append(Issue("P1", "shot_groups 为空", "shot_groups"))

        # shot ID 唯一性
        seen_ids = {}
        for s in shots:
            sid = s.get("id")
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            if sid in seen_ids:
                issues.append(Issue("P0", f"重复 shot ID: {sid} (第{seen_ids[sid]+1}个和第{shots.index(s)+1}个)",
                                    f"shots[{sid}]"))
            seen_ids[sid] = shots.index(s)

        # shot_groups 完整性
        if groups and shots:
            all_ids = {s["id"] for s in shots}
            ref_ids = set()
            for g in groups:
                for sid in g.get("shots", []): ref_ids.add(sid)
            orphans = ref_ids - all_ids
            if orphans: issues.append(Issue("P1", f"shot_groups 引用不存在的 shot ID: {orphans}", "shot_groups"))
            ungrouped = all_ids - ref_ids
            if ungrouped: issues.append(Issue("P1", f"未分组的 shot: {sorted(ungrouped)}", "shot_groups"))

        for s in shots:
            sid = s.get("id", "?")
            loc = f"shots[{sid}]"
            min_desc_len = self.validation_cfg.get("min_description_length", 15)
            desc = s.get("description", "")
            if len(desc) < 5: issues.append(Issue("P0", f"{loc}.description 过短 ({len(desc)}字)", f"{loc}.description"))
            elif len(desc) < min_desc_len:
                issues.append(Issue("P1", f"{loc}.description 偏短 ({len(desc)}字, 类型要求≥{min_desc_len})", loc))

            dur = s.get("duration_seconds", 0)
            if dur <= 0: issues.append(Issue("P0", f"{loc}.duration_seconds 无效 ({dur})", loc))
            if not isinstance(dur, (int, float)):
                issues.append(Issue("P0", f"{loc}.duration_seconds 类型错误: {type(dur).__name__}", loc))

            # dialogue 时长检查
            diag = s.get("dialogue", "")
            if diag and dur > 0:
                word_count = len(diag)
                est_speak_seconds = word_count / 5.0  # 5字/秒
                if est_speak_seconds > dur * 1.2:  # 20% buffer
                    issues.append(Issue("P2", f"{loc}: 台词约{word_count}字(~{est_speak_seconds:.1f}s)超出时长{dur}s",
                                        f"{loc}.dialogue"))

            # ── voice_over / dialogue 语义规则 ──
            vo = s.get("voice_over", "") or ""
            st = s.get("shot_type", "")
            diag_existing = bool(diag)

            # 1. 有 dialogue 但 characters 为空
            if diag_existing and not s.get("characters"):
                issues.append(Issue("P1", f"{loc}: 有 dialogue 但 characters 为空，需指定谁在说话", loc))

            # 2. dialogue 出现在广角/远景/空镜 shot_type
            _wide_types = {"wide", "广角", "远景", "establishing", "空镜", "建立", "extreme wide", "大全景"}
            if diag_existing and st in _wide_types:
                issues.append(Issue("P2", f"{loc}: shot_type={st} 不适合 dialogue（广角/远景通常无人对白）", loc))

            # 3. voice_over 内容超长 vs 时长
            if vo and dur > 0:
                _vo_words = len(vo)
                _est_read = _vo_words / 4.0  # 旁白稍慢 4字/秒
                if _est_read > dur * 1.3:
                    issues.append(Issue("P2", f"{loc}: voice_over {_vo_words}字(~{_est_read:.1f}s)超出时长{dur}s", loc))

            # 4. voice_over 含景别/拍摄指令
            if vo:
                _shot_kw = ["中景", "远景", "特写", "近景", "广角", "广角远景", "近景特写", "动态动作",
                            "大全景", "中景镜头", "俯拍", "仰拍", "跟拍", "平移", "摇镜"]
                _found_shot = [kw for kw in _shot_kw if kw in vo]
                if _found_shot:
                    issues.append(Issue("P1", f"{loc}: voice_over 含景别/拍摄指令 {_found_shot}，旁白不应有拍摄术语",
                                        f"{loc}.voice_over"))

            # 5. voice_over 直接照搬 description（机械味重）
            desc = s.get("description", "")
            if vo and desc:
                vo_set = set(vo)
                desc_set = set(desc)
                if vo_set and desc_set:
                    overlap = len(vo_set & desc_set) / len(vo_set)
                    if overlap > 0.8 or vo.strip() in desc or desc.startswith(vo):
                        issues.append(Issue("P2", f"{loc}: voice_over 与 description 重叠{overlap:.0%}，需用人类语言重述",
                                            f"{loc}.voice_over"))

            # 6. voice_over 含标点符号（TTS 应使用空格断句）
            if vo:
                _punct = [c for c in vo if c in "，。、！？：；""''（）【】《》…·,."]
                if len(_punct) >= 2:
                    issues.append(Issue("P2", f"{loc}: voice_over 含{len(_punct)}个标点，TTS 应使用空格断句",
                                        f"{loc}.voice_over"))

            # 7. voice_over 空格断句过碎（段 < 3 字，TTS 听起来像机器）
            if vo:
                _segs = [s.strip() for s in vo.split(" ") if s.strip()]
                _short_segs = [s for s in _segs if len(s) <= 2]
                if len(_short_segs) >= 2:
                    issues.append(Issue("P2", f"{loc}: voice_over 有{len(_short_segs)}段仅{_short_segs}字，断句过碎需合并",
                                        f"{loc}.voice_over"))

            if not s.get("shot_type", ""):
                issues.append(Issue("P1", f"{loc}.shot_type 未设置", loc))

            gen = s.get("generation", {})
            refs = gen.get("reference_images", {}) if isinstance(gen, dict) else {}
            if not refs:
                # 检查是否有资产图目录：无资产图时 reference_images 为空是预期的
                char_dir = os.path.join(self.project, "images", "characters")
                scene_dir = os.path.join(self.project, "images", "scenes")
                has_char_assets = os.path.isdir(char_dir) and any(f.endswith((".png", ".jpg", ".jpeg")) for f in os.listdir(char_dir)) if os.path.isdir(char_dir) else False
                has_scene_assets = os.path.isdir(scene_dir) and any(f.endswith((".png", ".jpg", ".jpeg")) for f in os.listdir(scene_dir)) if os.path.isdir(scene_dir) else False
                if has_char_assets or has_scene_assets:
                    issues.append(Issue("P0", f"{loc}.reference_images 为空", loc))
                else:
                    issues.append(Issue("P2", f"{loc}.reference_images 为空（尚未生成资产图）", loc))

            if not s.get("camera_movement", ""):
                issues.append(Issue("P2", f"{loc}.camera_movement 未设置", loc))

            # first_frame 块验证（首帧图生成后才有）
            ff = s.get("first_frame")
            if ff and isinstance(ff, dict):
                if not ff.get("model"):
                    issues.append(Issue("P1", f"{loc}.first_frame.model 未设置", f"{loc}.first_frame"))
                refs_ff = ff.get("ref_images", [])
                if not refs_ff:
                    issues.append(Issue("P1", f"{loc}.first_frame.ref_images 为空", f"{loc}.first_frame"))
                else:
                    for ri in refs_ff:
                        rp = ri if os.path.isabs(ri) else os.path.join(self.project, ri)
                        if not os.path.isfile(rp):
                            issues.append(Issue("P1", f"{loc}.first_frame 参考图不存在: {ri}", f"{loc}.first_frame"))
                            break
                if not ff.get("final"):
                    issues.append(Issue("P1", f"{loc}.first_frame.final 未设置（输出路径）", f"{loc}.first_frame"))
                pf = ff.get("prompt_file", "")
                if not pf:
                    issues.append(Issue("P1", f"{loc}.first_frame.prompt_file 未设置", f"{loc}.first_frame"))
                else:
                    pp = pf if os.path.isabs(pf) else os.path.join(self.project, pf)
                    if not os.path.isfile(pp):
                        issues.append(Issue("P0", f"{loc}.first_frame.prompt_file 不存在: {pf}", f"{loc}.first_frame"))

            # ── 角色连续性检查 ─────────────────────────────
            # 6a. 描述中有角色计数词但未指名
            count_kw = ["一人", "两人", "二人", "三人", "四人", "五人",
                        "1人", "2人", "3人", "4人", "5人",
                        "一个人", "两个人", "三个人", "四个人", "五个人",
                        "几人", "数人", "众人", "所有人", "多人", "各人"]
            has_count = any(kw in desc for kw in count_kw)
            explicit_chars = s.get("characters", []) or []
            # 从描述中匹配角色名
            chars_in_desc = []
            for cc in self.data.get("character_cards", []):
                cn = cc.get("name", "")
                if cn and cn in desc:
                    chars_in_desc.append(cn)
            found_kw = ''.join([kw for kw in count_kw if kw in desc][:1])
            if found_kw:
                # 即使有 characters 字段，描述中也不应使用模糊计数词
                if explicit_chars and len(explicit_chars) >= 2:
                    issues.append(Issue("P1",
                        f"{loc}: 描述使用了\"{found_kw}\"应改为实际角色名 "
                        f"(characters={explicit_chars})", loc))
                elif not explicit_chars and not chars_in_desc:
                    issues.append(Issue("P1",
                        f"{loc}: 描述有\"{found_kw}\"但未指定角色名，"
                        f"建议添加 characters 字段或改描述", loc))

            # 6b. 描述中有角色名但 characters 字段缺失该角色
            char_cards = self.data.get("character_cards", [])
            for cc in char_cards:
                cc_name = cc.get("name", "")
                if not cc_name:
                    continue
                short_name = cc_name.split("（")[0] if "（" in cc_name else cc_name
                # 括号内容匹配（支持中文和英文括号）
                bracket_content = ""
                for sep, end_sep in [("（", "）"), ("(", ")")]:
                    if sep in cc_name and end_sep in cc_name:
                        bracket_content = cc_name.split(sep)[1].split(end_sep)[0].strip()
                        break
                name_in_desc = (cc_name in desc.lower() or 
                                (short_name and short_name.lower() in desc.lower()) or
                                (bracket_content and bracket_content.lower() in desc.lower()))
                if name_in_desc and cc_name not in explicit_chars:
                    issues.append(Issue("P1",
                        f"{loc}: 描述提到了「{cc_name}」但 characters 字段未包含该角色，"
                        f"应添加至 characters=[{', '.join(explicit_chars)}] 中",
                        loc))

            # 6c. 描述中有动作词但对应的 video prompt 可能为静态（提醒）
            action_kw_check = [
                "转头", "回头", "扭头", "转身", "侧头", "抬头", "低头",
                "战斗", "跑", "跳跃", "追逐", "爆炸", "跃下", "走",
                "看向", "望向", "举起", "倒下", "震动", "晃动", "挥舞",
                "挥动", "冲锋", "闪避", "腾空", "落下", "蹲下", "起身",
            ]
            has_action = any(kw in desc for kw in action_kw_check)
            if has_action and not explicit_chars and not chars_in_desc:
                # 如果描述是 "三人" 这种无角色名的动作描述，提醒
                if has_count:
                    issues.append(Issue("P1",
                        f"{loc}: 描述含动作词且使用计数词替代角色名，"
                        f"视频 prompt 的 motion_type 可能被误判为静态", loc))

            # 6c.0 独立去重：characters 列表有重复项
            if explicit_chars:
                deduped = list(dict.fromkeys(explicit_chars))
                if len(deduped) != len(explicit_chars):
                    s["characters"] = deduped
                    self._fix("去重 characters", f"{loc}: 移除重复角色 {len(explicit_chars)-len(deduped)} 项")
                    explicit_chars = deduped  # 更新引用以给后续检查用

            # 6c.1 描述中有泛称代词（猫/狗/他/她/男子/女子）→ 应改为角色全名
            generic_kw = ["猫", "狗", "他", "她", "它", "男人", "女人", "男子", "女子",
                          "老人", "女孩", "男孩", "小孩", "孩子", "对方", "这人", "那人",
                          "这个人", "那个人", "玩家", "主角", "配角", "反派"]
            found_generic = [kw for kw in generic_kw if kw in desc]
            # 排除角色卡全名中含这些字的情况（如"君无烬（奶牛猫）"中的"猫"）
            all_char_names = [c.get("name", "") for c in char_cards if c.get("name")]
            if found_generic:
                filtered = []
                for kw in found_generic:
                    # 每个代词检查是否仅出现在角色卡全名中
                    in_char_name_only = all(kw in cn for cn in all_char_names) if all_char_names else False
                    # 检查描述中此"猫"是否属于"君无烬（奶牛猫）"的一部分
                    if kw == "猫" and any(f"（奶牛{kw}" in desc for _ in [1]):
                        in_char_name_only = True
                    if not in_char_name_only:
                        filtered.append(kw)
                if filtered and explicit_chars:
                    issues.append(Issue("P1",
                        f"{loc}: 描述使用了泛称「{'」「'.join(filtered)}」"
                        f"应改为实际角色名 (characters={explicit_chars})", loc))
                    # 自动修复：用角色名替换泛称代词
                    new_desc = desc
                    for kw in filtered:
                        # 找最适合替换的角色
                        if kw in ("猫", "狗", "它"):
                            # 找名字中含"猫"/"狗"的角色
                            matched_char = next((cn for cn in explicit_chars if kw in cn), None)
                            # "它"的fallback：找名字含"猫"或"狗"的角色
                            if not matched_char and kw == "它":
                                matched_char = next((cn for cn in explicit_chars if "猫" in cn or "狗" in cn), None)
                        elif kw in ("他",):
                            matched_char = explicit_chars[0] if explicit_chars else None  # 默认取第一个
                        elif kw in ("她",):
                            # 找不包含"猫""狗"的角色（女性）
                            matched_char = next((cn for cn in explicit_chars if "猫" not in cn and "狗" not in cn), explicit_chars[0] if explicit_chars else None)
                        else:
                            matched_char = explicit_chars[0] if explicit_chars else None
                        if not matched_char:
                            continue
                        base = matched_char.split("（")[0].split("(")[0].strip()
                        if not base:
                            base = matched_char
                        new_desc = new_desc.replace(kw, base, 1)  # 只替换第一个
                    if new_desc != desc:
                        s["description"] = new_desc
                        self._fix("替换泛称", f"shot_{sid:02d}: \"{'」「'.join(filtered)}\"→角色名")
                        cur_desc = new_desc  # 更新以备后续检查

            # 6c.2 角色连续（同场景组内，角色不应凭空出现或消失）
            if groups:
                for g in groups:
                    g_shots = g.get("shots", [])
                    if sid not in g_shots:
                        continue
                    # 找当前 shot 在同组中的位置
                    try:
                        g_idx = g_shots.index(sid)
                    except ValueError:
                        continue
                    if g_idx > 0:
                        prev_sid = g_shots[g_idx - 1]
                        prev_shot = next((ps for ps in shots if ps.get("id") == prev_sid), None)
                        if prev_shot:
                            prev_chars = prev_shot.get("characters", []) or []
                            curr_chars = explicit_chars or chars_in_desc
                            prev_named = [cn for cn in
                                (c.get("name", "") for c in self.data.get("character_cards", []))
                                if cn in "\n".join([prev_shot.get("description", ""),
                                                    str(prev_shot.get("characters", ""))])]
                            if prev_chars and curr_chars:
                                # 同组前一个 shot 明确有角色，当前 shot 角色数突变为 0
                                if len(prev_chars) > 0 and len(curr_chars) == 0:
                                    issues.append(Issue("P2",
                                        f"{loc}: 同组前序 shot_{prev_sid:02d} 有角色{prev_chars}，"
                                        f"当前 shot 未指定角色，可能不连续", loc))

            # 6d. 场景引用校验 — description 提到的场景名应在 scene_cards 中
            scene_cards = self.data.get("scene_cards", [])
            desc_lower = desc.lower()
            matched_scene = None
            for sc in scene_cards:
                sn = sc.get("name", "")
                if sn and sn.lower() in desc_lower:
                    matched_scene = sc
                    break
            if not matched_scene:
                # 检查 shot 是否已有场景参考图（图生图模式下场景内容已由参考图提供）
                gen = s.get("generation", {})
                refs = gen.get("reference_images", {})
                has_scene_ref = any(
                    "scenes/" in str(v) for v in refs.values()
                ) if refs else False
                ff = s.get("first_frame") or {}
                ff_refs = ff.get("ref_images", [])
                has_ff_scene = any("scenes/" in r for r in ff_refs) if ff_refs else False
                if not has_scene_ref and not has_ff_scene:
                    issues.append(Issue("P1",
                        f"{loc}: description 未命中任何 scene_cards 名称，场景引用可能缺失", loc))
            else:
                # 检查场景资产图是否存在
                sid_str = matched_scene.get("id", matched_scene.get("name", ""))
                scene_dir = os.path.join(self.project, "images", "scenes")
                scene_exists = any(
                    os.path.isfile(os.path.join(scene_dir, f"{sid_str}_{v}.png"))
                    for v in ["广角", "中景", "特写"]
                )
                if not scene_exists:
                    issues.append(Issue("P1",
                        f"{loc}: description 提到场景「{matched_scene.get('name')}」"
                        f"但资产图不存在（{scene_dir}/{sid_str}_*.png）", loc))
                # 检查 reference_images 是否使用了正确的场景
                gen = s.get("generation", {})
                refs = gen.get("reference_images", {})
                if refs and matched_scene:
                    kf1_path = refs.get("kf1", {}).get("path", "")
                    expected_prefix = f"images/scenes/{sid_str}"
                    if kf1_path and expected_prefix not in kf1_path:
                        issues.append(Issue("P1",
                            f"{loc}: reference_images.kf1 引用 {kf1_path}，"
                            f"但场景应为 {matched_scene.get('name')}({sid_str})", loc))

            # 6e. 描述断句校验 — 分句之间缺少逗号/句号
            # 当描述中的角色名或场景元素紧跟在非标点后，且不属于合法语法结构（如"看向周戎"），说明缺逗号
            _CHAR_NAMES = [c.get("name", "") for c in self.data.get("character_cards", []) if c.get("name")]
            _ALLOWED_VERBS = {"看向","盯着","瞄准","指着","对着","给了","看着","望着",
                             "走向","走到","来到","走进","冲到","跟上","跟着","追着",
                             "递给","对着","靠着","遇到","遇见","见到","碰到","靠近",
                             "超过","绕过","跨过","穿过","提起","谈起","谈到","念及"}
            _ALLOWED_CONJ = {"和","与","跟","同","及","或","或者","还是"}
            _ALLOWED_PREP = {"在","从","被","把","将","对","对于","关于","通过","根据"}
            _ALLOWED_SUFFIX = {"的","地","得","了","着","过"}
            for cn in _CHAR_NAMES:
                if not cn or len(cn) < 2:
                    continue
                idx = 0
                while True:
                    idx = desc.find(cn, idx)
                    if idx < 0:
                        break
                    if idx > 0:
                        prev = desc[idx-1]
                        # 角色名前缀为逗号/句号/顿号 → 断句正确
                        if prev in "，。；：？！、\n（( ":
                            idx += 1
                            continue
                        # "和"、"在"、"的" 等合法语法结构 → 跳过
                        if prev in _ALLOWED_CONJ or prev in _ALLOWED_SUFFIX:
                            idx += 1
                            continue
                        # 前两字是合法动词（看向周戎等）→ 跳过
                        if len(desc) >= idx + 1:
                            prev2 = desc[max(0, idx-2):idx]
                            if prev2 in _ALLOWED_VERBS:
                                idx += 1
                                continue
                            # "在...中"、"从...中"等介词结构
                            if prev in _ALLOWED_PREP or prev == "中":
                                idx += 1
                                continue
                        # 角色名前无逗号且不属于合法语法 → 缺逗号
                        issues.append(Issue("P1",
                            f"{loc}: 角色「{cn}」位于描述中，其前面缺少逗号（...{prev}」+「{cn}...）",
                            loc))
                        break
                    idx += 1
                    if idx >= len(desc):
                        break

            # 6f. 场景元素后缺逗号：用于非角色名词但也是新分句的边界
            # 如「休息火光」「篝火阿巴斯」等
            _BOUNDARY_TRIGGERS = {
                "火": "篝火", "息": "休息", "滚": "滚滚",
                "跃": "跳跃", "映": "映照",
            }
            for last_char, expected_trigger in _BOUNDARY_TRIGGERS.items():
                if expected_trigger not in desc:
                    continue
                idx = desc.find(expected_trigger)
                after_pos = idx + len(expected_trigger)
                if after_pos < len(desc) and desc[after_pos] not in "，。；：？！、\n":
                    # 检查后面是不是角色名 —— 如果是，已在上面的角色名检查中捕获
                    next_chars = desc[after_pos:after_pos+4]
                    is_char_next = any(cn and cn in next_chars for cn in _CHAR_NAMES)
                    if not is_char_next:
                        issues.append(Issue("P2",
                            f"{loc}: 场景词「{expected_trigger}」后缺少逗号，后续内容似为新分句",
                            loc))

        # ── 叙事结构检查（跨 shot） ─────────────────────────
        # 6b. 每个 shot 至少包含 2-3 种不同运镜动作
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "") + " " + s.get("camera", "")
            found_kinds = set()
            for detect_kw, kind in _CAMERA_MOVE_DETECT.items():
                if detect_kw in desc:
                    found_kinds.add(kind)
            if len(found_kinds) < 2:
                loc = f"shots[{sid}]"
                issues.append(Issue("P1",
                    f"{loc}: 单分镜仅含 {len(found_kinds)} 种运镜（{', '.join(sorted(found_kinds)) or '无'}），"
                    f"应≥2种不同运镜",
                    loc))
            # 6c. 运镜空间兼容性：互斥组合（推+拉、仰+俯、旋转+摇）不合法
            if len(found_kinds) >= 2:
                # 检查任意两个运镜是否互斥
                for k1 in found_kinds:
                    for k2 in found_kinds:
                        if k1 < k2 and frozenset({k1, k2}) in _CAMERA_INCOMPATIBLE:
                            loc = f"shots[{sid}]"
                            issues.append(Issue("P1",
                                f"{loc}: 运镜「{k1}+{k2}」空间互斥（{', '.join(sorted(found_kinds))}），"
                                f"请替换其中一个为其他轴运镜",
                                loc))

        # 7. 运镜多样性：连续 3+ 镜头同运镜
        motion_seq = []
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            # 简化运镜解析：从描述中提取 shot_type/camera 关键词
            motion = "unknown"
            st = f"{s.get('shot_type', '')} {s.get('camera', '')}".lower()
            if any(kw in st for kw in ["特写", "close", "近景"]):
                motion = "static"
            elif any(kw in st for kw in ["中景", "medium"]):
                motion = "medium"
            elif any(kw in st for kw in ["远景", "wide", "广角"]):
                motion = "wide"
            elif any(kw in st for kw in ["推", "dolly", "拉"]):
                motion = "dolly"
            elif any(kw in st for kw in ["摇", "pan", "跟", "移"]):
                motion = "pan"
            motion_seq.append((sid, motion))

        for i in range(2, len(motion_seq)):
            if all(m == motion_seq[i][1] for _, m in motion_seq[i-2:i+1]):
                m = motion_seq[i][1]
                if m not in ("unknown", "mixed"):
                    issues.append(Issue("P1",
                        f"shot_{motion_seq[i][0]:02d} 起连续 3 镜头运镜均为「{m}」，建议增加变化",
                        "shots"))

        # ── 分镜间连贯性检查 ──────────────────────────────
        # 8a. 动作接续：检查相邻 shot 的动作动词是否合理衔接
        action_verb_map = {
            "跑": "跑", "奔跑": "跑", "追逐": "跑", "走": "走", "行走": "走",
            "坐下": "坐", "坐": "坐", "站": "站", "站立": "站", "起身": "站",
            "躺": "躺", "躺下": "躺", "跳": "跳", "跳跃": "跳",
            "挥": "攻击", "砍": "攻击", "刺": "攻击", "射击": "攻击", "瞄准": "攻击",
            "说话": "对话", "对话": "对话", "交谈": "对话",
            "转头": "转头", "回头": "转头", "转身": "转身",
            "倒下": "倒下", "昏迷": "倒下", "死亡": "倒下",
        }
        JUMP_BLACKLIST = [
            ("跑", "坐"), ("跑", "躺"), ("跑", "对话"),
            ("站", "躺"), ("站", "坐"), ("攻击", "对话"),
            ("转头", "站"), ("转头", "对话"),
            ("倒下", "跑"), ("倒下", "站"),
        ]
        prev_actions = set()
        prev_sid = 0
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            curr_actions = {v for k, v in action_verb_map.items() if k in desc}
            if prev_actions and curr_actions:
                for pa in prev_actions:
                    for ca in curr_actions:
                        if (pa, ca) in JUMP_BLACKLIST:
                            issues.append(Issue("P1",
                                f"shot_{sid:02d}: 前序 shot_{prev_sid:02d}「{pa}」→ 当前「{ca}」"
                                f"动作跳跃，建议加过渡镜头", f"shots[{sid}]"))
            if curr_actions:
                prev_actions = curr_actions
            else:
                prev_actions = set()
            prev_sid = sid

        # 8b. 视角跳跃：相邻 shot 景别跨度过大（特写→远景，无中景过渡）
        view_order = {"closeup": 0, "特写": 0, "近景": 0,
                      "medium": 1, "中景": 1,
                      "wide": 2, "远景": 2, "广角": 2}
        prev_view = None
        prev_sid2 = 0
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            st = f"{s.get('shot_type', '')} {s.get('camera', '')}".lower()
            curr_view = None
            for k, v in view_order.items():
                if k in st or k in (s.get('description', '') or '').lower():
                    curr_view = v
                    break
            if curr_view is not None and prev_view is not None:
                if abs(curr_view - prev_view) >= 2:
                    issues.append(Issue("P1",
                        f"shot_{sid:02d}: 景别从 shot_{prev_sid2:02d} 的"
                        f"{['特写','中景','远景'][prev_view]}跳跃到{['特写','中景','远景'][curr_view]}，"
                        f"缺少中景过渡", f"shots[{sid}]"))
            if curr_view is not None:
                prev_view = curr_view
            prev_sid2 = sid

        # 8c. 空间一致性：检查角色在相邻 shot 中是否在同一位置
        loc_kw = ["左边", "右边", "左侧", "右侧", "左方", "右方",
                  "前方", "后方", "远处", "近处", "近景处", "远处"]
        prev_locs = {}
        prev_sid3 = 0
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            curr_locs = {kw for kw in loc_kw if kw in desc}
            for cc in self.data.get("character_cards", []):
                cn = cc.get("name", "")
                if cn and cn in desc and cn in prev_locs:
                    stale = prev_locs[cn]
                    if stale and stale not in desc:
                        issues.append(Issue("P1",
                            f"shot_{sid:02d}: 角色「{cn}」在 shot_{prev_sid3:02d} 位于{stale}，"
                            f"当前描述未指定位置，可能空间跳跃", f"shots[{sid}]"))
            if curr_locs:
                for cc in self.data.get("character_cards", []):
                    cn = cc.get("name", "")
                    if cn and cn in desc:
                        prev_locs[cn] = list(curr_locs)[0] if curr_locs else ""
            prev_sid3 = sid

        # 9. 情绪/氛围弧线 — 检测剧烈跳变
        BAD_JUMPS = {
            ("欢快", "悲伤"), ("欢快", "压抑"), ("欢快", "绝望"),
            ("温馨", "紧张"), ("温馨", "战斗"),
            ("平静", "激烈"), ("平静", "紧张"),
            ("紧张", "温馨"), ("紧张", "平静"),
            ("悲伤", "欢快"), ("绝望", "欢快"),
        }
        mood_kw_map = {
            "欢快": ["欢快", "喜悦", "愉快", "轻松"],
            "悲伤": ["悲伤", "哀伤", "悲壮", "沉重"],
            "压抑": ["压抑", "阴郁", "沉闷"],
            "绝望": ["绝望", "崩溃", "绝境"],
            "温馨": ["温馨", "温暖", "柔情", "温柔"],
            "紧张": ["紧张", "紧绷", "急迫", "焦灼"],
            "战斗": ["战斗", "激烈", "对抗", "打斗"],
            "平静": ["平静", "安宁", "宁静", "寂静"],
            "激烈": ["激烈", "狂野", "剧烈"],
        }
        mood_seq = []
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            detected = "unknown"
            for mood, kws in mood_kw_map.items():
                if any(kw in desc for kw in kws):
                    detected = mood
                    break
            mood_seq.append((sid, detected))
        for i in range(1, len(mood_seq)):
            ps, pm = mood_seq[i-1]
            cs, cm = mood_seq[i]
            if pm != "unknown" and cm != "unknown" and pm != cm:
                if (pm, cm) in BAD_JUMPS:
                    issues.append(Issue("P1",
                        f"shot_{cs:02d} 情绪从「{pm}」跳变到「{cm}」，中间缺少过渡镜头",
                        f"shots[{cs}]"))

        # 9. 总时长校验
        total_dur = sum(
            float(s.get("duration", s.get("duration_seconds", 0)) or 0)
            for s in shots
        )
        expected_total = self.data.get("script", {}).get("duration_seconds", 0)
        if expected_total > 0 and abs(total_dur - expected_total) / expected_total > 0.10:
            issues.append(Issue("P1",
                f"各 shot 时长总和={total_dur:.0f}s，script.duration_seconds={expected_total}s，偏差>10%",
                "script"))

        # 10. 开头钩子检测：前 3 个 shot 应有爆点元素
        hook_kw = ["突然", "意外", "冲突", "悬念", "对决", "危机", "关键时刻",
                   "发现", "惊醒", "追逐", "爆炸", "枪声", "尖叫", "打破",
                   "闯入", "坠落", "碰撞", "怒吼", "震惊"]
        for i in range(min(3, len(shots))):
            desc = shots[i].get("description", "")
            if not any(kw in desc for kw in hook_kw):
                issues.append(Issue("P1",
                    f"前 3 镜头(shot_{shots[i]['id']:02d})无爆点元素，建议加入冲突/悬念/意外",
                    f"shots[{shots[i]['id']}]"))

        # 11. 时长多样性（标准差检测）
        if len(shots) >= 4:
            durations = [float(s.get("duration", s.get("duration_seconds", 5)) or 5) for s in shots]
            mean_d = sum(durations) / len(durations)
            var = sum((d - mean_d) ** 2 for d in durations) / len(durations)
            std = var ** 0.5
            if std < 1.0:
                issues.append(Issue("P1",
                    f"各 shot 时长标准差={std:.1f}s，缺乏节奏变化（建议混入长短镜头）",
                    "shots"))

        # 12. 场景组之间过渡缺失
        if len(groups) >= 2:
            for i in range(1, len(groups)):
                prev_g = groups[i-1]
                curr_g = groups[i]
                curr_first_sid = curr_g.get("shots", [])[0] if curr_g.get("shots") else None
                if curr_first_sid is None:
                    continue
                curr_first = next((s for s in shots if s.get("id") == curr_first_sid), None)
                if not curr_first:
                    continue
                desc = curr_first.get("description", "")
                transition_kw = ["画面切换", "时间", "转场", "过渡", "夜幕", "夜晚",
                                 "黄昏", "清晨", "黎明", "同一时刻", "另一边",
                                 "与此同时", "另一处", "不远处", "远处传来",
                                 "画面一转", "镜头切换", "场景切换", "时空流转"]
                if not any(kw in desc for kw in transition_kw):
                    issues.append(Issue("P1",
                        f"组过渡: 从「{prev_g.get('name','?')}」到「{curr_g.get('name','?')}」"
                        f"缺少过渡（shot_{curr_first_sid:02d} 首镜描述无时间/转场标记）",
                        f"shots[{curr_first_sid}]"))

        # 13. 同场景组内角色不合理消失
        if groups:
            for g in groups:
                g_shots = g.get("shots", [])
                running_chars = set()
                for sid_g in g_shots:
                    s = next((ss for ss in shots if ss.get("id") == sid_g), None)
                    if not s:
                        continue
                    curr_chars = set(s.get("characters", []) or [])
                    desc = s.get("description", "")
                    if running_chars and curr_chars:
                        gone = running_chars - curr_chars
                        if gone:
                            # 检查描述中是否说明角色离开
                            exit_kw = ["走", "离开", "退", "消失", "离去", "远去", "撤离", "撤出"]
                            has_exit_desc = any(
                                any(ek in desc for ek in exit_kw) for _ in gone
                            )
                            # 检查 shot 类型：近景/特写的单人focus可以减少人数
                            st = (s.get("shot_type", "") or "").lower()
                            is_closeup = any(kw in st for kw in ["特写", "近景", "closeup"])
                            if not has_exit_desc and not is_closeup:
                                issues.append(Issue("P1",
                                    f"shot_{sid_g:02d}: 同组内角色 {gone} 不合理消失"
                                    f"（描述未说明离开），chars={curr_chars}",
                                    f"shots[{sid_g}]"))
                    if curr_chars:
                        running_chars = curr_chars

        # 14. 同场景组首镜缺场景说明
        if groups:
            for g in groups:
                g_shots = g.get("shots", [])
                if not g_shots:
                    continue
                first_sid = g_shots[0]
                first_shot = next((s for s in shots if s.get("id") == first_sid), None)
                if not first_shot:
                    continue
                g_name = g.get("name", "")
                desc = first_shot.get("description", "")
                if g_name and g_name not in desc:
                    # 检查描述中是否有场景说明词
                    scene_kw = ["废墟", "战场", "丛林", "森林", "篝火", "营地",
                                "室内", "室外", "城市", "荒野", "沙漠", "海边",
                                "悬崖", "山谷", "洞穴", "建筑", "街道", "房间",
                                "金字塔", "宫殿", "村庄", "小镇", "花园"]
                    if not any(kw in desc for kw in scene_kw):
                        issues.append(Issue("P2",
                            f"shot_{first_sid:02d}: 场景组「{g_name}」首镜描述缺失场景说明",
                            f"shots[{first_sid}]"))

        # 15. 台词后场景名冗余标记
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            if "台词:" in desc:
                # 检查有没有 "。，场景名" 模式（台词后被自动追加的场景名标记）
                after = desc.split("台词:")[-1]
                if "。，" in after:
                    parts = after.split("。，")
                    if len(parts) >= 2:
                        tail = parts[-1].strip()
                        scene_cards = self.data.get("scene_cards", [])
                        _SCENE_NAMES = [sc.get("name", "") for sc in scene_cards if sc.get("name")]
                        for sn in _SCENE_NAMES:
                            if sn == tail:
                                issues.append(Issue("P1",
                                    f"shot_{sid:02d}: 台词后出现冗余场景名标记「{sn}」",
                                    f"shots[{sid}]"))
                                break

        # 16. 连续"突然"开头检测
        prev_turan_check = False
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            starts_with_turan = desc.startswith("突然")
            if starts_with_turan and prev_turan_check:
                issues.append(Issue("P2",
                    f"shot_{sid:02d}: 连续「突然」开头，与上一镜头重复",
                    f"shots[{sid}]"))
            prev_turan_check = starts_with_turan

        return issues

    # ═══════════════════════════════════════════
    #  修复层
    # ═══════════════════════════════════════════

    def fix_all(self, issues: list[Issue] | None = None):
        """执行修复。若传入 issues，只修被验证出来的问题。"""
        issues_set = {i.msg for i in issues} if issues else None

        def _need(*tags: str) -> bool:
            """检查某类修复是否被 issues 命中（任意 tag 匹配即可）"""
            if issues_set is None:
                return True
            return any(any(t in m for m in issues_set) for t in tags)

        if _need("缺失", "未设置", "过于简单", "asset_generation_model", "first_frame_model", "video_model",
                 "scene_aspect_ratio", "scene_size"):
            self._fix_script()
        if _need("为空", "太短", "过短", "模板占位符", "asset_background", "no_weapon"):
            self._fix_characters()
        if _need("未设置", "lighting", "mood", "troop", "troop_cards"):
            self._fix_scenes()
        # shots/references/groups 的修复条件：有 shot 相关的 issue 或 issues_set 为空
        if _need("shots[", "shot_", "描述", "描述偏短", "描述过短", "duration", "无效", "类型错误",
                 "camera_movement", "未设置", "台词", "不存在", "为空",
                 "shot_groups", "reference_images"):
            self._fix_shots()
            self._fix_references()
            self._fix_groups()

    # ── Type-check helpers ──
    def _is_template_default(self, val: str) -> bool:
        """检查值是否是模板默认值（gentle 模式靠这个判断是否跳过）"""
        if any(re.search(p, val) for p in PLACEHOLDER_PATTERNS):
            return True
        if val in ("标准脸型", "普通脸型", "有神双眸", "标准眉形", "高挺鼻梁", "唇形分明", "标准下颌",
                   "标志性特征", "角色称号", "性格描述", "面部描述",
                   "western", "eastern", "chinese", "default"):
            return True
        return False

    def _should_overwrite(self, field_path: str, current_val: str) -> bool:
        """gentle 模式下是否应该覆盖"""
        if not current_val:
            return True  # 空值总是覆盖
        if self.gentle:
            return self._is_template_default(current_val)
        return True  # 非 gentle 模式，有更好的值就覆盖

    # ── 类型感知的默认值获取 ──
    def _get_prof(self, key: str, fallback: str = "") -> str:
        return self.profile.get(key, fallback) or fallback

    # ── Fix: script ──
    def _fix_script(self):
        sc = self.data.setdefault("script", {})
        p = self.profile

        # 注入缺失的全局字段（global_style 必须 ≥15 字，否则提示词生成会回退到劣质描述）
        if not sc.get("global_style"):
            raw = p.get("global_style", _BASE_DEFAULTS["global_style"])
            if len(raw) < 15:
                raw = _BASE_DEFAULTS["global_style"]  # 确保不低于兜底线
            sc["global_style"] = raw
            self._fix("已注入 script.global_style", f"来自类型配置 ({sc.get('type','默认')}) [{len(raw)}字]")

        if not sc.get("negative_prompt"):
            sc["negative_prompt"] = p.get("negative_prompt", _BASE_DEFAULTS["negative_prompt"])
            self._fix("已注入 script.negative_prompt", f"来自类型配置")

        if not sc.get("image_style"):
            sc["image_style"] = p.get("image_style", _BASE_DEFAULTS["image_style"])
            self._fix("已注入 script.image_style", f"来自类型配置")

        if not sc.get("tone"):
            sc["tone"] = p.get("tone", _BASE_DEFAULTS["tone"])
            self._fix("已注入 script.tone", f"来自类型配置")

        # 模型分配 —— 由 provider 自行决定，optimizer 不注入
        if not sc.get("asset_generation_model"):
            sc["asset_generation_model"] = ""
        if not sc.get("first_frame_model"):
            sc["first_frame_model"] = ""
        if not sc.get("video_model"):
            sc["video_model"] = ""

        # 场景图尺寸固定 16:9
        if not sc.get("scene_aspect_ratio"):
            sc["scene_aspect_ratio"] = p.get("scene_aspect_ratio",
                                             _BASE_DEFAULTS["scene_aspect_ratio"])
            self._fix("已注入 script.scene_aspect_ratio", sc["scene_aspect_ratio"])

        if not sc.get("scene_size"):
            sc["scene_size"] = p.get("scene_size", _BASE_DEFAULTS["scene_size"])
            self._fix("已注入 script.scene_size", sc["scene_size"])

        # aesthetic_style 必须与 global_style 一致，否则 prompt 生成会自我矛盾
        gs = sc.get("global_style", "")
        aes = sc.get("aesthetic_style", "")
        if not aes:
            # 从 global_style 自动派生
            sc["aesthetic_style"] = f"{_extract_style_prefix(gs) if gs else '通用'}清晰风格"
            self._fix("已注入 script.aesthetic_style（从 global_style 派生）", f"'{sc['aesthetic_style']}'")
        elif aes in ("通用清晰风格", "通用写实风格", "电影写实风格"):
            # 旧注入的通用值，与 global_style 可能矛盾，强制从 global_style 派生
            old = aes
            sc["aesthetic_style"] = f"{_extract_style_prefix(gs) if gs else '通用'}清晰风格"
            if old != sc["aesthetic_style"]:
                self._fix("已对齐 script.aesthetic_style 到 global_style", f"'{old}' → '{sc['aesthetic_style']}'")
        elif self._should_overwrite("script.aesthetic_style", aes) and \
             (len(aes) < 5 or aes in ("western", "eastern", "chinese", "default")):
            old = aes
            sc["aesthetic_style"] = f"{_extract_style_prefix(gs) if gs else '电影'}清晰风格"
            self._fix("已增强 script.aesthetic_style（从 global_style 派生）", f"'{old}' → '{sc['aesthetic_style']}'")

        if not sc.get("aesthetic_anchor"):
            style = sc.get("aesthetic_style", "通用清晰风格")
            anchor = (
                f"所有镜头必须保持「{style}」统一，持续保持{_extract_style_prefix(gs)}风格，防止风格偏移。"
                f"角色面孔、骨骼、体型、肤质必须与 _front.png 严格一致。"
            )
            sc["aesthetic_anchor"] = anchor
            self._fix("已注入 script.aesthetic_anchor", f"基于 {_extract_style_prefix(gs)} 风格")
        elif any(kw in sc.get("aesthetic_anchor", "") for kw in ["禁止二次元", "禁止动漫", "禁止写实", "禁止摄影", "禁止动画"]):
            # 旧 anchor 含硬编码的禁止词（不拘泥于动漫/写实二元），统一替换为风格描述
            style = sc.get("aesthetic_style", "通用清晰风格")
            old_anchor = sc["aesthetic_anchor"]
            sc["aesthetic_anchor"] = (
                f"所有镜头必须保持「{style}」统一，持续保持{_extract_style_prefix(gs)}风格，防止风格偏移。"
                f"角色面孔、骨骼、体型、肤质必须与 _front.png 严格一致。"
            )
            self._fix("修复 aesthetic_anchor 硬编码", f"旧锚含硬编码禁止词→已改为基于 {_extract_style_prefix(gs)} 风格的通用描述")

    # ── Gender inference ──
    def _infer_gender(self, c: dict) -> str:
        """从 build/aura/personality 推断性别。
        阳性词 > 阴性词 → 对应性别。
        平分或无关键词时默认男（ABO 设定中清瘦体型多为男性 Omega）。"""
        text = (c.get("build", "") + " " + c.get("appearance", {}).get("aura", "") + " " +
                c.get("personality", "")).lower()
        male = sum(1 for kw in MALE_KW if kw in text)
        female = sum(1 for kw in FEMALE_KW if kw in text)
        neutral = sum(1 for kw in MALE_NEUTRAL if kw in text)
        # 有明确关键词时按关键词判定
        if male > female: return "男"
        if female > male: return "女"
        # 平分或全0：有中性词（清瘦/苍白）→ 男性（ABO 常见设定）；无任何命中 → 男
        if male == female and neutral > 0:
            return "男"  # ABO 设定中清瘦角色通常是男性 Omega
        return "男"

    # ── distinctive_mark builder ──
    def _build_dm(self, c: dict) -> str:
        app = c.get("appearance", {})
        parts = []
        hair = app.get("hair", "")
        if hair: parts.append(hair[:12])
        fd = app.get("face_details", {})
        for k in ["face_shape", "eyes", "jaw"]:
            v = fd.get(k, "")
            if v and v not in parts and v not in FACE_DEFAULTS.get(k, ""):
                parts.append(v[:10])
        # color 提示 — 用完整色词匹配而非单字符
        cs = c.get("color_scheme", "")
        if cs:
            # 从长到短排序，避免"金"先于"金色"匹配
            color_words = ["青色", "蓝色", "绿色", "红色", "金色", "银色", "灰色",
                           "黑色", "白色", "紫色", "褐色", "深色", "浅色",
                           "暖色", "冷色", "暗色", "明色",
                           "猩红", "暗红", "深蓝", "墨绿", "藏青", "米白", "米色",
                           "深棕", "棕色", "卡其", "迷彩", "军绿",
                           "玫瑰金", "香槟", "咖啡", "牛仔蓝", "马尔斯绿"]
            matched_colors = []
            for cw in sorted(color_words, key=len, reverse=True):
                if cw in cs:
                    matched_colors.append(cw)
            if matched_colors:
                primary = matched_colors[0]
                # 去掉"色"字后缀，"浅色系" → "浅色调"
                display = primary if primary.endswith("色") else primary + "色"
                parts.append(f"{display}为主")
        dm = "，".join(parts)
        dm = re.sub(r'[，,，]+', '，', dm).strip('，,')
        while len(dm) < 12:
            dm += "，" + (parts[-1][:4] if parts else "独特气质")
        return dm[:60]

    # ── Fix: characters ──
    def _fix_characters(self):
        chars = self.data.get("character_cards", [])
        if not chars: return
        # 优先用 global_style（更详细），其次 aesthetic_style
        sc_data = self.data.get("script", {})
        global_aes = sc_data.get("global_style", "") or sc_data.get("aesthetic_style", "电影写实风格")

        cnt_style = cnt_gender = cnt_dm = cnt_fd = cnt_extra = 0
        for c in chars:
            name = c.get("name", "?")

            # age_range — 从 age 推断
            if not c.get("age_range") and self._should_overwrite(f"{name}.age_range", c.get("age_range", "")):
                age = c.get("age", "")
                if str(age).isdigit():
                    n = int(age)
                    c["age_range"] = f"{n-3}-{n+3}"
                elif "未知" in str(age):
                    c["age_range"] = "未知"
                else:
                    c["age_range"] = "20-30"
                self._fix(f"{name}.age_range", c["age_range"])
                cnt_extra += 1

            # build — 从 appearance.aura 推断
            if not c.get("build") and self._should_overwrite(f"{name}.build", c.get("build", "")):
                aura = c.get("appearance", {}).get("aura", "")
                if any(w in aura for w in ["高大", "挺拔"]):
                    c["build"] = "高大挺拔"
                elif any(w in aura for w in ["纤细", "瘦弱"]):
                    c["build"] = "纤细瘦弱"
                elif "高瘦" in aura:
                    c["build"] = "高瘦"
                elif "猫" in name:
                    c["build"] = "中等体型猫形"
                else:
                    c["build"] = "匀称"
                self._fix(f"{name}.build", c["build"])
                cnt_extra += 1

            # color_scheme — 从 clothing 推断
            if not c.get("color_scheme") and self._should_overwrite(f"{name}.color_scheme", c.get("color_scheme", "")):
                clothing = c.get("appearance", {}).get("armor/clothing", "")
                if "白色" in clothing or "白衣" in clothing:
                    c["color_scheme"] = "白+金"
                elif "紫" in clothing:
                    c["color_scheme"] = "深紫+暗色"
                elif "米色" in clothing or "浅蓝" in clothing:
                    c["color_scheme"] = "米色+浅蓝"
                elif "猫" in name:
                    c["color_scheme"] = "黑白+粉"
                else:
                    c["color_scheme"] = "自然色"
                self._fix(f"{name}.color_scheme", c["color_scheme"])
                cnt_extra += 1

            # personality — 从角色设定推断
            if not c.get("personality") and self._should_overwrite(f"{name}.personality", c.get("personality", "")):
                title = c.get("title", "")
                gender = c.get("gender", "")
                aura = c.get("appearance", {}).get("aura", "")
                if any(w in aura + title for w in ["温柔", "清冷", "憔悴"]):
                    c["personality"] = "温柔善良 内心脆弱但坚韧"
                elif any(w in aura + title for w in ["傲娇", "高傲", "威严"]):
                    c["personality"] = "傲娇 自尊心极强 口嫌体正直"
                elif any(w in aura + title for w in ["霸气", "强大", "威严"]):
                    c["personality"] = "霸气潇洒 自信张扬 光明磊落"
                elif any(w in aura + title for w in ["阴鸷", "阴郁", "癫狂"]):
                    c["personality"] = "阴郁 嫉妒心强 自卑又自负 对权力极度渴望"
                else:
                    c["personality"] = f"根据角色「{name}」的故事背景设定"
                self._fix(f"{name}.personality", c["personality"][:30])
                cnt_extra += 1

            # gender
            if not c.get("gender") and self._should_overwrite(f"{name}.gender", c.get("gender", "")):
                c["gender"] = self._infer_gender(c)
                cnt_gender += 1

            # aesthetic_style — 从 aura/personality 提取角色专属风格关键词，
            # 与 global_style 组合使用（生成时 script.global_style + card.aesthetic_style）
            if not c.get("aesthetic_style"):
                aura = c.get("appearance", {}).get("aura", "")
                personality = c.get("personality", "")
                # 从 aura + personality 中提取 2-3 个关键词
                style_kw = []
                for kw in ["清冷", "桀骜", "阴冷", "沉稳", "铁血", "优雅",
                           "野性", "禁欲", "阴郁", "隐忍", "精致", "硬朗",
                           "颓废", "凌厉", "温润", "诡谲", "肃杀", "苍凉"]:
                    if kw in aura or kw in personality:
                        style_kw.append(kw)
                char_flavor = "、".join(style_kw[:3]) if style_kw else f"{name}角色风格"
                c["aesthetic_style"] = f"角色风格：{char_flavor}"
                cnt_style += 1
            else:
                cs = c["aesthetic_style"]
                if not any(w in cs for w in ["写实", "电影", "realistic", "cinematic", "角色风格", "风格"]):
                    # 已有但不能识别为风格描述 → 补全
                    c["aesthetic_style"] = f"角色风格：{cs[:20]}" if cs else global_aes[:30]
                    cnt_style += 1
                else:
                    # 统一格式：确保以"角色风格："开头，去尾逗号
                    normalized = cs.rstrip("，,、")
                    if not normalized.startswith("角色风格："):
                        c["aesthetic_style"] = f"角色风格：{normalized[:20]}"
                        cnt_style += 1

            # distinctive_mark
            dm = c.get("distinctive_mark", "")
            if self._should_overwrite(f"{name}.distinctive_mark", dm) and (not dm or self._is_template_default(dm) or len(dm) < 8):
                old = dm
                c["distinctive_mark"] = self._build_dm(c)
                cnt_dm += 1
                self._fix(f"{name}.distinctive_mark", f"'{old[:20]}' → '{c['distinctive_mark'][:30]}...'")

            # face_details — 只提取找到的，找不到的不填默认值
            app = c.setdefault("appearance", {})
            fd = app.setdefault("face_details", {})
            face_text = app.get("face", "")
            need_fd = any(not fd.get(sub) or self._is_template_default(fd.get(sub, ""))
                          for sub in REQUIRED_FACE_DETAILS)
            if need_fd and face_text:
                for sub in REQUIRED_FACE_DETAILS:
                    cur = fd.get(sub, "")
                    if cur and not self._is_template_default(cur):
                        continue  # 已有有效值，跳过
                    found = ""
                    for kw in FACE_DETAIL_MAP.get(sub, []):
                        idx = face_text.find(kw)
                        if idx >= 0:
                            start = max(0, idx - 8)
                            end = min(len(face_text), idx + 12)
                            found = face_text[start:end].strip()
                            break
                    if found:
                        fd[sub] = found
                        cnt_fd += 1
                    # 找不到就不填——保留空值比填无意义默认值更诚实

            # 资产底座字段：白背景 + 无武器
            bg = self.profile.get("character_card_background", _BASE_DEFAULTS["character_card_background"])
            if not c.get("asset_background"):
                c["asset_background"] = bg
                self._fix(f"{name}.asset_background", f"'{bg}'（纯白底）")
            nw = self.profile.get("character_card_no_weapon", _BASE_DEFAULTS["character_card_no_weapon"])
            if c.get("no_weapon_for_standard_views") is None:
                c["no_weapon_for_standard_views"] = nw
                self._fix(f"{name}.no_weapon_for_standard_views", str(nw))

        if cnt_style: self._fix("aesthetic_style", f"{cnt_style} 个角色")
        if cnt_gender: self._fix("gender 推断", f"{cnt_gender} 个角色")
        if cnt_dm: pass  # each logged individually
        if cnt_fd: self._fix("face_details 补全", f"至少 {cnt_fd} 个子字段")

    # ── Fix: scenes ──
    def _fix_scenes(self):
        scenes = self.data.get("scene_cards", [])
        fixed = 0
        for sc in scenes:
            # time_of_day — 从描述推断
            if not sc.get("time_of_day") or self._should_overwrite(f"{sc.get('name','?')}.time_of_day",
                                                                    sc.get("time_of_day", "")):
                desc = sc.get("description", "")
                if any(w in desc for w in ["夜", "晚", "月光", "灯火"]):
                    sc["time_of_day"] = "夜晚"
                elif any(w in desc for w in ["黄昏", "夕阳", "日落"]):
                    sc["time_of_day"] = "黄昏"
                elif any(w in desc for w in ["清晨", "黎明", "日出"]):
                    sc["time_of_day"] = "清晨"
                else:
                    sc["time_of_day"] = "白天"
                fixed += 1

            # weather — 从描述推断
            if not sc.get("weather") or self._should_overwrite(f"{sc.get('name','?')}.weather",
                                                                sc.get("weather", "")):
                desc = sc.get("description", "")
                if "雨" in desc or "大雨" in desc:
                    sc["weather"] = "大雨"
                elif "雪" in desc or "大雪" in desc:
                    sc["weather"] = "大雪"
                elif "阴" in desc:
                    sc["weather"] = "阴天"
                elif "雷" in desc or "闪电" in desc:
                    sc["weather"] = "雷暴"
                elif "晴" in desc:
                    sc["weather"] = "晴天"
                else:
                    sc["weather"] = "晴（室内）" if "夜" in sc.get("time_of_day", "") else "晴天"
                fixed += 1

            tod = (sc.get("time_of_day") or "").lower()
            matched = False
            for key, val in DEFAULT_SCENE_MOOD.items():
                if key in tod:
                    if not sc.get("lighting") or self._should_overwrite(f"{sc.get('name','?')}.lighting",
                                                                        sc.get("lighting", "")):
                        sc["lighting"] = val["lighting"]; fixed += 1
                    if not sc.get("mood") or self._should_overwrite(f"{sc.get('name','?')}.mood", sc.get("mood", "")):
                        sc["mood"] = val["mood"]; fixed += 1
                    matched = True
                    break
            if not matched:
                if not sc.get("lighting") or self._should_overwrite(f"{sc.get('name','?')}.lighting",
                                                                    sc.get("lighting", "")):
                    sc["lighting"] = self._get_prof("lighting", "环境光，以场景氛围为主")
                    fixed += 1
                if not sc.get("mood") or self._should_overwrite(f"{sc.get('name','?')}.mood", sc.get("mood", "")):
                    mood_guess = "中性氛围"
                    if "战" in sc.get("description", ""): mood_guess = "紧张/激烈"
                    elif "静" in sc.get("description", ""): mood_guess = "安静/平和"
                    sc["mood"] = mood_guess; fixed += 1
            # color_scheme 从场景描述推断
            if not sc.get("color_scheme") or self._should_overwrite(f"{sc.get('name','?')}.color_scheme",
                                                                     sc.get("color_scheme", "")):
                desc = sc.get("description", "") + " " + sc.get("emotion", "")
                color_guess = "自然色"
                if "废墟" in desc or "断壁" in desc or "硝烟" in desc or "灰褐" in desc:
                    color_guess = "灰褐+暗黄"
                elif "夜" in desc or "篝火" in desc or "月光" in desc or "火光" in desc:
                    color_guess = "暖橙+深蓝"
                elif "雪" in desc or "白" in desc:
                    color_guess = "冷白+灰蓝"
                elif "森林" in desc or "绿" in desc:
                    color_guess = "墨绿+棕"
                sc["color_scheme"] = color_guess; fixed += 1
        if fixed: self._fix("场景 lighting/mood/color_scheme", f"{fixed} 项")

    # ── Fix: shots ──
    def _fix_shots(self):
        shots = self.data.get("shots", [])
        groups = self.data.get("shot_groups", [])
        # 建立 scene_id → scene_card 映射
        scene_map = {}
        for sc in self.data.get("scene_cards", []):
            sid = sc.get("id", "")
            if sid:
                scene_map[sid] = sc

        # 建立 shot_id → scene_id 映射
        shot_scene = {}
        for g in groups:
            sid = g.get("scene_id", "")
            for sid_shot in g.get("shots", []):
                shot_scene[sid_shot] = sid

        fixed_cam = fixed_desc = fixed_dur = fixed_dur_type = fixed_short = 0
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            # duration_seconds 类型矫正（字符串数字→int）
            dur = s.get("duration_seconds", 0)
            if isinstance(dur, str):
                try:
                    s["duration_seconds"] = int(dur)
                    fixed_dur_type += 1
                except ValueError:
                    s["duration_seconds"] = 5
                    fixed_dur += 1
            # camera_movement — 优先级：camera 字段描述 > shot_type 映射 > 兜底
            if not s.get("camera_movement"):
                desc = s.get("description", "")
                cam_field = s.get("camera", "")
                st = s.get("shot_type", "medium")
                # 尝试从 camera 字段的文字描述推断（如"广角俯拍"、"特写推近"）
                cam_from_field = _infer_camera_from_text(cam_field or desc)
                if cam_from_field:
                    s["camera_movement"] = cam_from_field
                else:
                    s["camera_movement"] = DEFAULT_SHOT_CAMERA.get(st, "标准固定镜头")
                fixed_cam += 1
            # description fallback
            desc = s.get("description", "")
            if not desc and s.get("prompt", ""):
                s["description"] = s["prompt"][:200]
                fixed_desc += 1
            elif desc:
                # 扩展偏短描述：从 scene、shot_type、dialogue 提取上下文追加
                min_len = self.validation_cfg.get("min_description_length", 15)
                if len(desc) < min_len:
                    extras = []
                    # 注入场景上下文
                    sc_id = shot_scene.get(sid)
                    if sc_id and sc_id in scene_map:
                        sc_desc = scene_map[sc_id].get("description", "")
                        if sc_desc:
                            extras.append(sc_desc[:40])
                    # 注入 shot_type 视角提示
                    st_map = {"wide": "广角远景", "medium": "中景", "closeup": "近景特写",
                              "action": "动态动作"}
                    st_label = st_map.get(s.get("shot_type", ""))
                    if st_label and st_label not in desc:
                        extras.insert(0, st_label)
                    # 注入 dialogue 提示
                    if s.get("dialogue"):
                        extras.append(f"台词: {s['dialogue'][:30]}")
                    if extras:
                        s["description"] = f"{desc}，{'，'.join(extras)}"
                        fixed_short += 1
            # duration fallback
            if s.get("duration_seconds", 0) <= 0:
                s["duration_seconds"] = 5
                fixed_dur += 1

            # ── characters 字段自动补全（从 description 匹配） ──
            existing_chars = s.get("characters", []) or []
            desc = s.get("description", "")
            matched = []
            # 先精确匹配全名
            for cc in self.data.get("character_cards", []):
                cn = cc.get("name", "")
                if cn and cn in desc:
                    matched.append(cn)
            # 再模糊匹配：只有全名没匹配到的角色才走模糊匹配
            for cc in self.data.get("character_cards", []):
                cn = cc.get("name", "")
                if cn in matched:
                    continue
                base_name = cn.split("（")[0].split("(")[0].strip()
                if len(base_name) < 2 or base_name not in desc:
                    continue
                # 防止"君无烬"同时匹配"君无烬（奶牛猫）"和"君无烬（天帝真身）"
                # 检查是否有同 base_name 的其他角色已匹配
                same_base = [m for m in matched if m.split("（")[0].split("(")[0].strip() == base_name]
                if same_base:
                    # 已有同 base 的角色匹配，只加括号内容也在描述中的
                    bracket_content = ""
                    for sep, end_sep in [("（", "）"), ("(", ")")]:
                        if sep in cn and end_sep in cn:
                            bracket_content = cn.split(sep)[1].split(end_sep)[0].strip()
                            break
                    if bracket_content and bracket_content in desc:
                        matched.append(cn)
                    # 同 base 角色已匹配过，跳过后续的括号匹配和逐字匹配
                    continue
                else:
                    matched.append(cn)
                # 括号内容匹配：如"君无烬（奶牛猫）"→"奶牛猫"在描述中
                bracket_content = ""
                for sep in ("（", "("):
                    if sep in cn and (sep == "（" and "）" in cn) or (sep == "(" and ")" in cn):
                        end_sep = "）" if sep == "（" else ")"
                        bracket_content = cn.split(sep)[1].split(end_sep)[0].strip()
                        break
                if len(bracket_content) >= 2 and bracket_content in desc:
                    matched.append(cn)
                    continue
                # 逐字匹配：角色名前4字中有≥2字在描述中
                if cn and len(cn) >= 2:
                    cnt = sum(1 for ch in cn[:4] if ch in desc)
                    if cnt >= 2:
                        matched.append(cn)
            # 只覆盖已有 characters 当匹配到新角色时
            if matched:
                if set(matched) != set(existing_chars):
                    s["characters"] = matched
                    self._fix("characters 字段", f"shot_{sid:02d}: 从描述匹配角色 {matched}")

            # ── 模糊计数词替换：描述中有"三人""两人"等应改为实际角色名 ──
            cur_chars = s.get("characters", []) or []
            count_kw_rep = {"一人": "1", "两人": "2", "二人": "2", "三人": "3", "四人": "4", "五人": "5",
                           "一个人": "1", "两个人": "2", "三个人": "3", "四个人": "4", "五个人": "5"}
            cur_desc = s.get("description", "")
            for ckw, cnum in count_kw_rep.items():
                if ckw not in cur_desc:
                    continue
                expected = int(cnum)
                if len(cur_chars) == expected:
                    # 用 & 连接角色名为人类可读形式，替换计数词
                    # 取角色名的"简写"部分（括号前的实词）
                    short_names = []
                    for cn in cur_chars:
                        base = cn.split("（")[0].split("(")[0].strip()
                        short_names.append(base if base else cn)
                    if len(short_names) == 2:
                        replacement = f"{short_names[0]}和{short_names[1]}"
                    else:
                        replacement = "、".join(short_names[:-1]) + f"和{short_names[-1]}"
                    # 只替换首次出现的计数词（避免替换对话中的数字）
                    new_desc = cur_desc.replace(ckw, replacement, 1)
                    if new_desc != cur_desc:
                        s["description"] = new_desc
                        self._fix("模糊计数词", f"shot_{sid:02d}: 「{ckw}」→「{replacement}」")
                        cur_desc = new_desc  # 更新以备继续匹配
                    break  # 只处理一个计数词

            # ── 描述断句修复：在分句边界缺少逗号处加逗号 ──
            cur_desc = s.get("description", "")
            if cur_desc:
                # 已知精确模式匹配
                # 「爆炸声」「滚滚」后跟角色名或新分句 → 补逗号
                _PRECISE_FIX = {
                    "爆炸声": "爆炸声，",
                    "滚滚": "滚滚，",
                    "围坐篝火": "围坐篝火，",
                    "走近篝火": "走近篝火，",
                    "俯拍篝火": "俯拍篝火，",
                    "闭眼休息": "闭眼休息，",
                }
                for old, new in _PRECISE_FIX.items():
                    if old in cur_desc and new not in cur_desc:
                        # 确认后一个字符不是介词方位词（旁、中、上、下）
                        idx = cur_desc.find(old)
                        after = idx + len(old)
                        if after < len(cur_desc) and cur_desc[after] in "旁中上下前后里边":
                            continue
                        cur_desc = cur_desc.replace(old, new, 1)
                        s["description"] = cur_desc
                        self._fix("描述断句", f"shot_{sid:02d}: 「{old}」后补逗号")

                # 「走出」后跟描述性分句 → 补逗号（走出脸上=走出，脸上）
                if "走出" in cur_desc and "走出，" not in cur_desc:
                    idx = cur_desc.find("走出")
                    after = idx + 2
                    if after < len(cur_desc):
                        cur_desc = cur_desc[:after] + "，" + cur_desc[after:]
                        s["description"] = cur_desc
                        self._fix("描述断句", f"shot_{sid:02d}: 走出后补逗号")

                # 「看向/看着/盯着/望着」+角色名+新分句 → 角色名后补逗号
                # 如「看向周戎篝火」→「看向周戎，篝火」
                _GAZE_VERBS = ["看向", "看着", "盯着", "望着", "听着", "走向"]
                _CHAR_NAMES_FIX = [c.get("name", "") for c in self.data.get("character_cards", [])
                                  if c.get("name") and len(c.get("name", "")) >= 2]
                for gv in _GAZE_VERBS:
                    if gv not in cur_desc:
                        continue
                    idx = cur_desc.find(gv)
                    after_verb = idx + len(gv)
                    # 动词后找到角色名
                    for cn in _CHAR_NAMES_FIX:
                        if cur_desc[after_verb:after_verb+len(cn)] == cn:
                            after_name = after_verb + len(cn)
                            if after_name < len(cur_desc):
                                next_ch = cur_desc[after_name]
                                # 后跟非介词/非逗号 → 角色名应该结束分句，补逗号
                                if next_ch not in "，。；：？！、\n在和与跟同及以上于":
                                    cur_desc = cur_desc[:after_name] + "，" + cur_desc[after_name:]
                                    s["description"] = cur_desc
                                    self._fix("描述断句", f"shot_{sid:02d}: {gv}{cn}后补逗号")
                                    break
                        # 也检查简写名（括号前部分）
                        base = cn.split("（")[0].split("(")[0].strip()
                        if base and base != cn and cur_desc[after_verb:after_verb+len(base)] == base:
                            after_name = after_verb + len(base)
                            if after_name < len(cur_desc) and cur_desc[after_name] not in "，。；：？！、\n在和与跟同及以上于":
                                cur_desc = cur_desc[:after_name] + "，" + cur_desc[after_name:]
                                s["description"] = cur_desc
                                self._fix("描述断句", f"shot_{sid:02d}: {gv}{base}后补逗号")
                                break

            # ── 场景引用自动修正（reference_images.kf1 vs actual scene） ──
            scene_sid = shot_scene.get(sid, "")
            if scene_sid and scene_sid in scene_map:
                # 尝试自动补场景名到 description
                sc_name = scene_map[scene_sid].get("name", "")
                if sc_name and sc_name not in desc:
                    # 如果有场景参考图则无需补场景名（图生图已提供场景视觉信息）
                    gen = s.get("generation", {})
                    refs = gen.get("reference_images", {})
                    has_scene_ref = any(
                        "scenes/" in str(v) for v in refs.values()
                    ) if refs else False
                    if not has_scene_ref:
                        s["description"] = f"{desc}，{sc_name}"
                        self._fix("场景名", f"shot_{sid:02d}: description 补场景名「{sc_name}」")
                gen = s.setdefault("generation", {})
                refs = gen.get("reference_images", {})
                if refs:
                    kf1 = refs.get("kf1", {})
                    kf1_path = kf1.get("path", "")
                    expected = f"images/scenes/{scene_sid}"
                    if kf1_path and expected not in kf1_path:
                        # 修复 kf1 指向正确的场景资产
                        for ext in ["_广角.png", "_中景.png", "_特写.png"]:
                            candidate = f"{expected}{ext}"
                            candidate_abs = os.path.join(self.project, candidate)
                            if os.path.isfile(candidate_abs):
                                refs["kf1"] = {"path": candidate}
                                self._fix("场景引用", f"shot_{sid:02d}: {kf1_path} → {candidate}")
                                break

        if fixed_cam: self._fix("camera_movement", f"{fixed_cam} 个 shot")
        if fixed_desc: self._fix("description 扩展", f"{fixed_desc} 个 shot")
        if fixed_dur: self._fix("duration 默认值", f"{fixed_dur} 个 shot")
        if fixed_dur_type: self._fix("duration 类型修正", f"{fixed_dur_type} 个 shot (string→int)")
        if fixed_short: self._fix("description 自动扩写", f"{fixed_short} 个 shot (偏短→补场景/视角)")

        # ── 开头钩子自动修复：前 3 个 shot 补爆点关键词 ──
        hook_kw = ["突然", "意外", "冲突", "悬念", "对决", "危机", "关键时刻",
                   "发现", "惊醒", "追逐", "爆炸", "枪声", "尖叫", "打破",
                   "闯入", "坠落", "碰撞", "怒吼", "震惊"]
        hook_alternatives = ["突然", "意外", "骤然", "猛然", "瞬间", "刹那间"]
        prev_turan = False
        for i in range(min(3, len(shots))):
            desc = shots[i].get("description", "")
            if any(kw in desc for kw in hook_kw):
                # 已有爆点词，检查是否也要处理连续"突然"
                if desc.startswith("突然") and prev_turan:
                    # 连续"突然" → 用别的词替换第二个
                    other_hook = [w for w in hook_alternatives if w != "突然" and w not in desc]
                    if other_hook:
                        shots[i]["description"] = desc.replace("突然", other_hook[0], 1)
                        self._fix("开头爆点", f"shot_{shots[i]['id']:02d}: 连续「突然」→「{other_hook[0]}」")
                prev_turan = desc.startswith("突然")
                continue
            # 无爆点词 → 补一个（但检查是否已有"突然"在其他位置）
            if "突然" in desc:
                prev_turan = False
                continue
            shots[i]["description"] = f"突然，{desc}"
            self._fix("开头爆点", f"shot_{shots[i]['id']:02d}: 补开头爆点提示")
            prev_turan = True

        # ── 时长标准差自动修复：将部分 shot 时长调短以制造节奏变化 ──
        if len(shots) >= 4:
            durations = [float(s.get("duration", s.get("duration_seconds", 5)) or 5) for s in shots]
            mean_d = sum(durations) / len(durations)
            var = sum((d - mean_d) ** 2 for d in durations) / len(durations)
            std = var ** 0.5
            if std < 1.5:
                # 将最长的 shot 时长削半，最短的 shot 时长翻倍，直到标准差达标
                import random
                for _ in range(3):
                    durations = [float(s.get("duration", s.get("duration_seconds", 5)) or 5) for s in shots]
                    max_i = max(range(len(durations)), key=lambda i: durations[i])
                    min_i = min(range(len(durations)), key=lambda i: durations[i])
                    shots[max_i]["duration"] = max(3, durations[max_i] * 0.6)
                    shots[min_i]["duration"] = min(10, durations[min_i] * 1.5)
                    new_durs = [float(s.get("duration", s.get("duration_seconds", 5)) or 5) for s in shots]
                    new_m = sum(new_durs) / len(new_durs)
                    new_v = sum((d - new_m) ** 2 for d in new_durs) / len(new_durs)
                    if (new_v ** 0.5) >= 1.5:
                        self._fix("时长节奏", f"shot_{shots[max_i]['id']:02d} 缩短+shot_{shots[min_i]['id']:02d} 加长")
                        break

        # ── 总时长自动修复：按比例缩放 shot 时长，使总和接近预期 ──
        expected_total = float(self.data.get("script", {}).get("duration_seconds", 0))
        if expected_total > 0:
            actual_total = sum(
                float(s.get("duration", s.get("duration_seconds", 5)) or 5)
                for s in shots
            )
            if actual_total > 0 and abs(actual_total - expected_total) / expected_total > 0.10:
                scale = expected_total / actual_total
                new_total = 0.0
                for s in shots:
                    old_dur = float(s.get("duration", s.get("duration_seconds", 5)) or 5)
                    new_dur = max(2.0, min(15.0, old_dur * scale))
                    new_dur = round(new_dur, 1)
                    s["duration"] = new_dur
                    new_total += new_dur
                final_dev = abs(new_total - expected_total) / expected_total
                self._fix("总时长", f"缩放 {scale:.2f}×: {actual_total:.0f}s→{new_total:.0f}s（偏差{final_dev:.0%}）")

        # ── 动作接续自动修复 ──
        action_verb_map = {
            "跑": "跑", "奔跑": "跑", "追逐": "跑", "走": "走", "行走": "走",
            "坐下": "坐", "坐": "坐", "站": "站", "站立": "站", "起身": "站",
            "躺": "躺", "躺下": "躺", "跳": "跳", "跳跃": "跳",
            "挥": "攻击", "砍": "攻击", "刺": "攻击", "射击": "攻击",
            "说话": "对话", "对话": "对话", "交谈": "对话",
            "转头": "转头", "回头": "转头", "转身": "转身",
        }
        transition_map = {
            ("跑", "坐"): "跑到位置后停下坐下",
            ("跑", "站"): "跑到位置后停下站定",
            ("跑", "躺"): "跑到位置后躺下",
            ("跑", "对话"): "跑到位置后停下开始对话",
            ("站", "坐"): "然后坐下",
            ("站", "躺"): "然后躺下",
            ("攻击", "对话"): "停止攻击，开始对话",
            ("倒下", "站"): "从地上爬起站定",
            ("倒下", "跑"): "从地上爬起开始跑",
        }
        for i in range(1, len(shots)):
            prev_desc = shots[i-1].get("description", "")
            curr_desc = shots[i].get("description", "")
            prev_acts = {v for k, v in action_verb_map.items() if k in prev_desc}
            curr_acts = {v for k, v in action_verb_map.items() if k in curr_desc}
            for pa in prev_acts:
                for ca in curr_acts:
                    if (pa, ca) in transition_map:
                        transit = transition_map[(pa, ca)]
                        # 只补如果当前描述还没包含这个过渡
                        if transit not in curr_desc:
                            shots[i]["description"] = f"{transit}，{curr_desc}"
                            self._fix("动作接续", f"shot_{shots[i]['id']:02d}: 补过渡「{transit}」")
                            break
                else:
                    continue
                break

        # ── 视角跳跃自动修复：补中景过渡描述 ──
        view_order = {"closeup": 0, "特写": 0, "近景": 0,
                      "medium": 1, "中景": 1,
                      "wide": 2, "远景": 2, "广角": 2}
        for i in range(1, len(shots)):
            ps = shots[i-1].get("shot_type", "")
            cs = shots[i].get("shot_type", "")
            pv = None
            cv = None
            for k, v in view_order.items():
                if k in (ps or "").lower(): pv = v
                if k in (cs or "").lower(): cv = v
            if pv is not None and cv is not None and abs(cv - pv) >= 2:
                # 在当前 shot 描述补中景说明以缓解跳跃感
                if cv == 0:
                    shots[i]["description"] = f"镜头拉近至近景，{shots[i]['description']}"
                    self._fix("视角过渡", f"shot_{shots[i]['id']:02d}: 远景→特写，补推近描述")
                elif cv == 2:
                    shots[i]["description"] = f"镜头拉远呈全景，{shots[i]['description']}"
                    self._fix("视角过渡", f"shot_{shots[i]['id']:02d}: 特写→远景，补拉远描述")

        # ── 空间一致性自动修复：补角色位置到当前 shot 描述 ──
        loc_kw = ["左边", "右边", "左侧", "右侧", "左方", "右方",
                  "前方", "后方", "远处", "近处", "近景处"]
        # "远处"容易被场景描述词误匹配（如"远处浓烟""远处爆炸声"），
        # 只有紧贴角色名出现时才视为位置词
        def _is_char_position(desc: str, cn: str, kw: str) -> bool:
            if kw != "远处":
                return kw in desc
            # "远处"需要确认是描述角色位置而非场景
            idx = desc.find(kw)
            if idx < 0:
                return False
            cn_idx = desc.find(cn)
            if cn_idx < 0:
                return False
            return abs(idx - cn_idx) < 20  # 角色名和位置词在20字内
        prev_locs = {}
        # 逐 shot 扫描，只记录已经出现过的角色位置
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            # 为本 shot 中缺失位置的角色补位
            for cn, last_loc in list(prev_locs.items()):
                if cn in desc and last_loc not in desc:
                    has_any_loc = any(kw in desc for kw in loc_kw)
                    if not has_any_loc:
                        s["description"] = f"{cn}在画面{last_loc}，{desc}"
                        self._fix("空间一致", f"shot_{sid:02d}: {cn}位置{last_loc}")
                        desc = s["description"]  # 用更新后的继续扫描
                        break
            # 记录本 shot 的角色新位置
            for cc in self.data.get("character_cards", []):
                cn = cc.get("name", "")
                if not cn or cn not in desc:
                    continue
                for kw in loc_kw:
                    if _is_char_position(desc, cn, kw):
                        prev_locs[cn] = kw
                        break

        # ── 同组角色突变自动修复：从同组前序 shot 继承 characters ──
        if groups:
            for g in groups:
                g_shots = g.get("shots", [])
                prev_chars = []
                for sid_g in g_shots:
                    s = next((ss for ss in shots if ss.get("id") == sid_g), None)
                    if not s:
                        continue
                    cur = s.get("characters", []) or []
                    # 仅在当前 shot 描述未提及任何角色时继承
                    desc = s.get("description", "")
                    has_named_char = any(
                        cn in desc
                        for cn in [c.get("name", "") for c in self.data.get("character_cards", [])]
                        if cn
                    )
                    if not cur and prev_chars and not has_named_char:
                        s["characters"] = list(prev_chars)
                        self._fix("角色继承", f"shot_{sid_g:02d}: 从组内前序继承角色 {prev_chars}")
                    elif cur and prev_chars and not has_named_char:
                        # cur 不为空但少于 prev_chars → 继承完整角色列表（仅非近景）
                        st = f"{s.get('shot_type', '')} {s.get('camera', '')} {s.get('description', '')}".lower()
                        is_closeup = any(kw in st for kw in ["特写", "近景", "closeup"])
                        if set(cur).issubset(set(prev_chars)) and len(cur) < len(prev_chars) and not is_closeup:
                            s["characters"] = list(prev_chars)
                            self._fix("角色继承", f"shot_{sid_g:02d}: 从组内前序补全角色 {prev_chars}")
                    elif cur and prev_chars:
                        # 即使描述命名了某个角色，如果前序有更完整的角色集且当前是子集，也应补全（仅非近景）
                        st = f"{s.get('shot_type', '')} {s.get('camera', '')} {s.get('description', '')}".lower()
                        is_closeup = any(kw in st for kw in ["特写", "近景", "closeup"])
                        if set(cur).issubset(set(prev_chars)) and len(cur) < len(prev_chars) and not is_closeup:
                            s["characters"] = list(prev_chars)
                            self._fix("角色继承", f"shot_{sid_g:02d}: 从组内前序补全角色 {prev_chars}")
                        # 同组内角色完全置换（无交集）且描述未说明离开 → 合并新旧角色（仅非近景）
                        elif not set(cur) & set(prev_chars) and not is_closeup:
                            merge = list(set(prev_chars) | set(cur))
                            s["characters"] = merge
                            self._fix("角色继承", f"shot_{sid_g:02d}: 合并角色 {merge}（新角色入场，旧角色仍在场）")
                        # 同组内角色部分置换（有交集但前序有角色缺失）→ 补全缺失角色（仅非近景）
                        elif set(cur) & set(prev_chars) and not set(cur).issuperset(set(prev_chars)) and not is_closeup:
                            merge = list(set(prev_chars) | set(cur))
                            s["characters"] = merge
                            self._fix("角色继承", f"shot_{sid_g:02d}: 补全角色 {merge}（旧角色仍应在场）")
                    if cur:
                        # 更新 prev_chars：近景不缩小角色集（人物还在场，只是不在镜头焦点）
                        st = (s.get("shot_type", "") or "").lower()
                        is_closeup = any(kw in st for kw in ["特写", "近景", "closeup"])
                        if is_closeup and prev_chars:
                            # 保留 prev_chars（近景不缩小角色范围）
                            pass
                        else:
                            prev_chars = cur if not s.get("characters") else list(s.get("characters", []))

        # ── 运镜多样性自动修复：连续 3+ 同运镜时改中间 shot 的 description ──
        motion_seq = []
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            st = f"{s.get('shot_type', '')} {s.get('camera', '')} {s.get('description', '')}".lower()
            motion = "unknown"
            if any(kw in st for kw in ["特写", "close", "近景"]): motion = "closeup"
            elif any(kw in st for kw in ["中景", "medium"]): motion = "medium"
            elif any(kw in st for kw in ["远景", "wide", "广角"]): motion = "wide"
            elif any(kw in st for kw in ["推", "dolly", "拉"]): motion = "dolly"
            elif any(kw in st for kw in ["摇", "pan", "跟", "移"]): motion = "pan"
            motion_seq.append(motion)
        for i in range(2, len(motion_seq)):
            if all(m == motion_seq[i] for m in motion_seq[i-2:i+1]):
                m = motion_seq[i]
                if m in ("closeup", "medium", "wide"):
                    # 不是简单贴标签，而是给中间 shot 补充运镜动作
                    # 长镜头（>5s）的运镜变化更丰富
                    cam_actions = {
                        "closeup": ["镜头缓慢拉远", "镜头向后拉开", "缓缓后退拉开视野"],
                        "medium":   ["镜头缓缓推进", "镜头向前推近", "缓慢推近至近景"],
                        "wide":     ["镜头缓缓横移", "镜头向右平移", "镜头向左平移跟摄"],
                    }
                    import random
                    action = random.choice(cam_actions[m])
                    mid_shot = shots[i-1]
                    dur = mid_shot.get("duration_seconds", 5)
                    # 长镜头加强运镜：预示运镜在延续
                    if dur >= 6:
                        action = action.replace("缓缓", "持续缓慢").replace("缓慢", "持续缓慢")
                        second_action = random.choice([a for a in cam_actions[m] if a != action] or [action])
                        action = f"{action}，同时{second_action}"
                    old_desc = mid_shot.get("description", "")
                    if action not in old_desc:
                        mid_shot["description"] = f"{action}，{old_desc}"
                        self._fix("运镜多样性", f"shot_{mid_shot['id']:02d}: 连续 3 {m} → 补运镜「{action[:20]}」")

        # ── 动作接续自动修复：动作跳跃时补过渡描述 ──
        _action_transition = {
            ("跑", "坐"): "放慢脚步走到一旁",
            ("跑", "躺"): "停下脚步躺下",
            ("跑", "对话"): "停下脚步看向对方",
            ("站", "躺"): "缓缓躺下",
            ("站", "坐"): "慢慢坐下",
            ("攻击", "对话"): "收起武器看向对方",
            ("转头", "站"): "缓缓站起身",
            ("转头", "对话"): "转过身正对对方",
            ("倒下", "跑"): "挣扎着爬起来",
            ("倒下", "站"): "艰难站起",
        }
        prev_actions_set = set()
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            curr = {v for k, v in action_verb_map.items() if k in desc}
            if prev_actions_set and curr:
                for pa in prev_actions_set:
                    for ca in curr:
                        if (pa, ca) in _action_transition:
                            transit = _action_transition[(pa, ca)]
                            if transit not in desc:
                                s["description"] = f"{transit}。{desc}"
                                self._fix("动作接续", f"shot_{sid:02d}: {pa}→{ca}补过渡「{transit}」")
            prev_actions_set = curr if curr else set()

        # ── 景别跳跃自动修复：特写→远景 时补中景过渡描述 ──
        _view_transition = {
            (0, 2): "镜头拉远，露出更广阔的环境",
            (2, 0): "镜头推近，聚焦细节",
        }
        _prev_view = None
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            st = f"{s.get('shot_type', '')} {s.get('camera', '')} {s.get('description', '')}".lower()
            cview = next((v for k, v in view_order.items() if k in st), None)
            if cview is not None and _prev_view is not None and abs(cview - _prev_view) >= 2:
                key = (_prev_view, cview)
                if key in _view_transition:
                    transit = _view_transition[key]
                    if transit not in s.get("description", ""):
                        s["description"] = f"{transit}，{s['description']}"
                        self._fix("景别跳跃", f"shot_{sid:02d}: {['特写','中景','远景'][_prev_view]}→{['特写','中景','远景'][cview]}补过渡")
            if cview is not None:
                _prev_view = cview

        # ── 情绪弧线自动修复：在情绪跳变的 shot 间补过渡描述 ──
        BAD_JUMPS = {
            ("欢快", "悲伤"), ("欢快", "压抑"), ("欢快", "绝望"),
            ("温馨", "紧张"), ("温馨", "战斗"),
            ("平静", "激烈"), ("平静", "紧张"),
            ("紧张", "温馨"), ("紧张", "平静"),
            ("悲伤", "欢快"), ("绝望", "欢快"),
        }
        mood_kw_map = {
            "欢快": ["欢快", "喜悦", "愉快", "轻松"],
            "悲伤": ["悲伤", "哀伤", "悲壮", "沉重"],
            "压抑": ["压抑", "阴郁", "沉闷"],
            "绝望": ["绝望", "崩溃", "绝境"],
            "温馨": ["温馨", "温暖", "柔情", "温柔"],
            "紧张": ["紧张", "紧绷", "急迫", "焦灼"],
            "战斗": ["战斗", "激烈", "对抗", "打斗"],
            "平静": ["平静", "安宁", "宁静", "寂静"],
            "激烈": ["激烈", "狂野", "剧烈"],
        }
        transition_text = {
            ("欢快", "悲伤"): "气氛突然沉重",
            ("欢快", "压抑"): "氛围逐渐凝重",
            ("温馨", "紧张"): "气氛骤然紧张",
            ("温馨", "战斗"): "冲突爆发",
            ("平静", "激烈"): "局势急剧变化",
            ("平静", "紧张"): "不安的气息蔓延",
            ("紧张", "温馨"): "紧张气氛缓和",
            ("悲伤", "欢快"): "情绪突然转变",
        }
        for i in range(1, len(shots)):
            prev_desc = shots[i-1].get("description", "")
            curr_desc = shots[i].get("description", "")
            pm = "unknown"
            cm = "unknown"
            for mood, kws in mood_kw_map.items():
                if any(kw in prev_desc for kw in kws): pm = mood
                if any(kw in curr_desc for kw in kws): cm = mood
            if pm != "unknown" and cm != "unknown" and (pm, cm) in BAD_JUMPS:
                transit = transition_text.get((pm, cm), "场景转变")
                if transit not in curr_desc:
                    shots[i]["description"] = f"{transit}。{curr_desc}"
                    self._fix("情绪过渡", f"shot_{shots[i]['id']:02d}: {pm}→{cm}补过渡「{transit}」")

        # ── 单分镜运镜动作不足自动修复：每 shot 至少 2 种不同运镜 ──
        _MOVE_LIST = list(_CAMERA_MOVE_KINDS.items())  # [(kind, desc), ...]
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "") + " " + s.get("camera", "")
            found_kinds = set()
            for detect_kw, kind in _CAMERA_MOVE_DETECT.items():
                if detect_kw in desc:
                    found_kinds.add(kind)
            if len(found_kinds) < 2:
                need = 2 - len(found_kinds)
                missing = [k for k, _ in _MOVE_LIST if k not in found_kinds]
                to_add = []
                # 选第一个：从 missing 中挑一个
                if missing and len(to_add) < need:
                    import random
                    first = random.choice(missing)
                    to_add.append(first)
                    missing.remove(first)
                # 选第二个：必须与第一个空间兼容（不互斥）
                if missing and len(to_add) < need:
                    compatible = [k for k in missing
                                  if frozenset({to_add[0], k}) not in _CAMERA_INCOMPATIBLE]
                    if compatible:
                        second = random.choice(compatible)
                    elif need > 1:
                        # 只用一个运镜也比加互斥对好
                        need = 1
                        second = to_add[0]  # 复用第一个
                    else:
                        second = None
                    if second:
                        to_add.append(second)
                if to_add:
                    descs = [_CAMERA_MOVE_KINDS[k] for k in to_add]
                    if len(descs) == 2:
                        # 空间兼容的组合用"同时"连接（表示多轴复合运镜）
                        # 不兼容的组合用"随后"连接（表示先后切换）
                        if frozenset({to_add[0], to_add[1]}) not in _CAMERA_INCOMPATIBLE:
                            add_text = f"{descs[0]}，同时{descs[1]}"
                        else:
                            add_text = f"{descs[0]}，随后{descs[1]}"
                    else:
                        add_text = descs[0]
                    if add_text not in s.get("description", ""):
                        s["description"] = f"{add_text}，{s['description']}"
                        self._fix("运镜补全", f"shot_{sid:02d}: 运镜数 {len(found_kinds)}→+{len(to_add)} 补「{add_text}」")

        # ── 运镜空间兼容性自动修复：替换互斥组合（仰+俯、推+拉等）──
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "") + " " + s.get("camera", "")
            found_kinds = set()
            for detect_kw, kind in _CAMERA_MOVE_DETECT.items():
                if detect_kw in desc:
                    found_kinds.add(kind)
            if len(found_kinds) >= 2:
                incompatible_found = set()
                for k1 in found_kinds:
                    for k2 in found_kinds:
                        if k1 < k2 and frozenset({k1, k2}) in _CAMERA_INCOMPATIBLE:
                            incompatible_found.add(k1)
                            incompatible_found.add(k2)
                if incompatible_found:
                    # 互斥修复：清理所有运镜前缀，仅保留2-3个兼容的
                    desc = s.get("description", "")
                    # 先去掉现有的所有运镜前缀（以"镜头"开头的短语）
                    clean_desc = re.sub(r'(?:，)?镜头[^，。]*?(?:，同时镜头[^，。]*?)?[，。]?', '', desc)
                    clean_desc = re.sub(r'^[，。、\\s]+', '', clean_desc)
                    clean_desc = re.sub(r'[，。、\\s]+$', '', clean_desc)
                    if len(clean_desc) < 15:
                        clean_desc = desc  # 删太多就保留原样
                    
                    # 选一组兼容的运镜
                    all_moves = list(_CAMERA_MOVE_KINDS.items())
                    import random
                    random.shuffle(all_moves)
                    chosen = []
                    for kind, text in all_moves:
                        if not chosen:
                            chosen.append((kind, text))
                        elif frozenset({chosen[0][0], kind}) not in _CAMERA_INCOMPATIBLE:
                            chosen.append((kind, text))
                            break
                    if len(chosen) >= 2:
                        glue = "，同时" if frozenset({chosen[0][0], chosen[1][0]}) not in _CAMERA_INCOMPATIBLE else "，随后"
                        prefix = f"{chosen[0][1]}{glue}{chosen[1][1]}"
                    elif chosen:
                        prefix = chosen[0][1]
                    else:
                        prefix = ""
                    
                    if prefix and prefix not in clean_desc:
                        s["description"] = f"{prefix}，{clean_desc}"
                        self._fix("运镜兼容修复",
                            f"shot_{sid:02d}: 清除互斥组合{tuple(sorted(incompatible_found))}→替换为兼容运镜")

        # ── 台词场景名冗余标记自动修复 ──
        scene_cards = self.data.get("scene_cards", [])
        _ALL_SCENE_NAMES = [sc.get("name", "") for sc in scene_cards if sc.get("name")]
        for s in shots:
            sid = s.get("id", 0)
            if isinstance(sid, str):
                sid = int(sid.replace("shot_", ""))
            desc = s.get("description", "")
            if "台词:" not in desc:
                continue
            after = desc.split("台词:")[-1]
            if "。，" not in after:
                continue
            parts = after.split("。，")
            if len(parts) >= 2:
                tail = parts[-1].strip()
                for sn in _ALL_SCENE_NAMES:
                    if sn == tail:
                        s["description"] = desc.replace(f"。，{sn}", "。")
                        self._fix("台词冗余", f"shot_{sid:02d}: 去掉台词后冗余场景名「{sn}」")
                        break

        # ── 场景组过渡自动补全 ──
        groups = self.data.get("shot_groups", [])
        if len(groups) >= 2:
            transition_kw = ["画面切换", "时间", "转场", "夜幕", "夜晚",
                             "黄昏", "清晨", "黎明", "与此同时", "另一处",
                             "画面一转", "镜头切换", "场景切换"]
            for i in range(1, len(groups)):
                prev_g = groups[i-1]
                curr_g = groups[i]
                curr_first_sid = curr_g.get("shots", [])[0] if curr_g.get("shots") else None
                if not curr_first_sid:
                    continue
                curr_first = next((s for s in shots if s.get("id") == curr_first_sid), None)
                if not curr_first:
                    continue
                desc = curr_first.get("description", "")
                if any(kw in desc for kw in transition_kw):
                    continue
                # 补过渡描述到首镜
                prev_name = prev_g.get("name", "上一场景")
                curr_name = curr_g.get("name", "下一场景")
                curr_first["description"] = f"画面切换至{curr_name}。{desc}"
                self._fix("场景过渡", f"shot_{curr_first_sid:02d}: 「{prev_name}→{curr_name}」补过渡描述")

            # ── dialogue 在广角/远景/空镜镜头 → 转为 voice_over ──
            _g_wide = {"wide", "广角", "远景", "establishing", "空镜", "建立", "extreme wide", "大全景"}
            _g_diag = s.get("dialogue", "")
            _g_st = s.get("shot_type", "")
            _g_vo = s.get("voice_over", "")
            if _g_diag and _g_st in _g_wide and not _g_vo:
                s["voice_over"] = _g_diag
                s["dialogue"] = ""
                self._fix("voice_over/dialogue", f"shot_{sid:02d}: {_g_st}镜头 dialogue→voice_over 转换")

            # ── voice_over 超出镜头时长 → 截断 ──
            _g_vo = s.get("voice_over", "") or ""
            _g_dur = s.get("duration_seconds", 0) or 0
            if _g_vo and _g_dur > 0:
                _g_wc = len(_g_vo)
                _g_est = _g_wc / 4.0
                if _g_est > _g_dur * 1.3:
                    _g_max = int(_g_dur * 4.0 * 0.9)
                    if _g_max < _g_wc:
                        _g_trunc = _g_vo[:_g_max]
                        for _g_sep in ["。", "！", "？", "……"]:
                            _g_idx = _g_trunc.rfind(_g_sep)
                            if _g_idx > _g_max * 0.5:
                                _g_trunc = _g_trunc[:_g_idx + 1]
                                break
                        s["voice_over"] = _g_trunc
                        self._fix("voice_over 长度", f"shot_{sid:02d}: {_g_wc}字→{len(_g_trunc)}字（适配{_g_dur}s）")

            # ── dialogue 有内容但 characters 为空 → 尝试从对话中匹配角色名 ──
            _g_diag2 = s.get("dialogue", "")
            if _g_diag2 and not s.get("characters"):
                _g_desc = s.get("description", "")
                _g_name = None
                for cc in self.data.get("character_cards", []):
                    cn = cc.get("name", "")
                    if not cn: continue
                    if cn in _g_diag2 or cn in _g_desc:
                        _g_name = cn; break
                    base = cn.split("（")[0].split("(")[0].strip()
                    if len(base) >= 2 and base in _g_diag2:
                        _g_name = cn; break
                if _g_name:
                    s["characters"] = [_g_name]
                    self._fix("characters 字段", f"shot_{sid:02d}: 从 dialogue 匹配角色 [{_g_name}]")

            # ── voice_over 去机械味：去掉 shot_type/拍摄指令/角色定位 ──
            _g_vo3 = s.get("voice_over", "") or ""
            _g_desc3 = s.get("description", "") or ""
            if _g_vo3 and _g_desc3:
                _g_new = _g_vo3
                import re as _re
                _g_new = _re.sub(r'[，]?(静态|动态动作|中景镜头|大全景)($|，)', r'\2', _g_new)
                _g_new = _re.sub(r'俯拍|仰拍|跟拍|摇镜|平移', '', _g_new)
                _g_new = _re.sub(r'。。', '。', _g_new)
                _g_new = _re.sub(r'^[^，]{2,8}在画[面幅]远处[，]?', '', _g_new)
                _g_new = _re.sub(r'^[^，]{2,8}在[画前][面方].{0,4}[，]?', '', _g_new)
                _g_new = _g_new.rstrip('，, ')
                if _g_new and _g_new != _g_vo3:
                    s["voice_over"] = _g_new
                    self._fix("voice_over 去机械味",
                              f"shot_{sid:02d}: 去 shot_type/拍摄指令/定位 ({len(_g_vo3)}字→{len(_g_new)}字)")

            # ── voice_over 标点 → 空格（TTS 断句用） ──
            _g_vo4 = s.get("voice_over", "") or ""
            _g_has_punct = [c for c in _g_vo4 if c in "，。、！？：；""''（）【】《》…·,."]
            if len(_g_has_punct) >= 2:
                _g_new4 = _g_vo4
                import re as _re4
                _g_new4 = _re4.sub(r'[，。、！？：；""''（）【】《》…·,.]', ' ', _g_new4)
                _g_new4 = _re4.sub(r'  +', ' ', _g_new4).strip()
                if _g_new4 != _g_vo4:
                    s["voice_over"] = _g_new4
                    self._fix("voice_over 标点→空格",
                              f"shot_{sid:02d}: {len(_g_has_punct)}个标点替换为空格")

    # ── Fix: reference images ──
    def _find_char_img(self, name: str) -> str | None:
        for v in ["front", "face", "side", "back"]:
            p = os.path.join(self.project, "images", "characters", f"{name}_{v}.png")
            if os.path.isfile(p): return p
        return None

    def _find_scene_img(self, sid: str) -> str | None:
        for f in [f"{sid}_广角.png", f"{sid}.png", f"{sid}_v2.png"]:
            p = os.path.join(self.project, "images", "scenes", f)
            if os.path.isfile(p): return p
        return None

    def _ref_path_exists(self, v: str) -> bool:
        """检查 reference_images 中某个路径的文件是否存在（支持绝对/相对路径）"""
        if not isinstance(v, str):
            return False
        abs_path = v if os.path.isabs(v) else os.path.join(self.project, v)
        return os.path.isfile(abs_path)

    def _fix_references(self):
        chars = self.data.get("character_cards", [])
        scenes = self.data.get("scene_cards", [])
        groups = self.data.get("shot_groups", [])
        shots = self.data.get("shots", [])

        # scene_id per shot from groups
        scene_per_shot = {}
        char_per_group = {}  # group_id → list of character names (from group metadata)
        for g in groups:
            gid = g.get("id") or g.get("group", 0)
            sc_id = g.get("scene_id", "")
            # Get character names from shot_groups metadata if present
            g_chars = g.get("characters", [])
            if g_chars:
                char_per_group[gid] = g_chars
            for sid in g.get("shots", []):
                scene_per_shot[sid] = sc_id

        fixed = 0
        for s in shots:
            sid = s["id"]
            gen = s.setdefault("generation", {})
            if gen.get("reference_images"):
                # 验证已有路径是否有效
                refs = gen["reference_images"]
                valid = True
                for k, v in refs.items():
                    if not self._ref_path_exists(v):
                        valid = False
                        break
                if valid:
                    continue

            refs = {}

            # 场景
            sc_id = scene_per_shot.get(sid)
            if not sc_id and scenes:
                sc_id = scenes[0].get("id", "")
            if sc_id:
                img = self._find_scene_img(sc_id)
                if img: refs["scene"] = img

            # 角色 — 用 shot_groups 结构匹配
            # 找到这个 shot 所在的 group
            matched_gid = None
            for g in groups:
                if sid in g.get("shots", []):
                    matched_gid = g.get("id") or g.get("group", 0)
                    break
            if matched_gid and matched_gid in char_per_group:
                for ch_name in char_per_group[matched_gid]:
                    img = self._find_char_img(ch_name)
                    if img:
                        refs[f"character_{ch_name}"] = img
            else:
                # fallback: 文本匹配（中英文混合兼容）
                desc = (s.get("description", "") + " " + s.get("prompt", "")).lower()
                for c in chars:
                    name = c["name"]
                    nl = name.lower().replace("（", "(").replace("）", ")")
                    # 完整名匹配（中文名含括号时）
                    if nl in desc:
                        img = self._find_char_img(name)
                        if img:
                            refs[f"character_{name}"] = img
                        continue
                    # 中文名逐字匹配（兼容英文 prompt 中混用中文名）
                    if len(name) >= 2:
                        # 取前 2 个汉字逐字检查（避免单字误匹配）
                        chars_found = sum(1 for ch in name[:4] if ch in desc)
                        if chars_found >= 2:
                            img = self._find_char_img(name)
                            if img:
                                refs[f"character_{name}"] = img

            if refs:
                gen["reference_images"] = refs
                fixed += 1

        if fixed: self._fix("reference_images", f"{fixed} 个 shot")

    # ── Fix: groups ──
    def _fix_groups(self):
        shots = self.data.get("shots", [])
        groups = self.data.get("shot_groups", [])
        if not shots: return
        if not groups:
            # 完全没有 group → 创建一个默认组包含所有 shot
            self._create_default_group(shots, groups)
            return

        all_ids = {s["id"] for s in shots}
        fixed_orphan = 0
        for g in groups:
            before = len(g.get("shots", []))
            g["shots"] = [sid for sid in g.get("shots", []) if sid in all_ids]
            if len(g["shots"]) < before:
                fixed_orphan += 1

        ref_ids = set()
        for g in groups:
            for sid in g.get("shots", []): ref_ids.add(sid)
        ungrouped = sorted(all_ids - ref_ids)
        if ungrouped:
            self._create_default_group_for_shots(ungrouped, groups, shots)
            self._fix("shot_groups 补全", f"为 {len(ungrouped)} 个未分组 shot 创建新组")

    def _create_default_group(self, shots: list, groups: list):
        """完全没有 shot_groups 时创建默认组（从 scene_cards 继承 scene_id）"""
        sc_id = ""
        scenes = self.data.get("scene_cards", [])
        if scenes:
            sc_id = scenes[0].get("id", "")
        g = {
            "id": "sg_default",
            "name": "默认镜头组",
            "scene_id": sc_id,
            "shots": sorted([s["id"] for s in shots]),
        }
        groups.append(g)
        self._fix("shot_groups 创建", f"默认组含 {len(g['shots'])} 个 shot（场景: {sc_id or '未指定'}）")

    def _create_default_group_for_shots(self, shot_ids: list, groups: list, shots: list):
        """为未分组 shot 创建新组，尝试从已有 group 继承 scene_id"""
        scene_id = groups[0].get("scene_id", "") if groups else ""
        new_id = f"sg_default_{len(groups) + 1}"
        g = {
            "id": new_id,
            "name": f"自动补全组",
            "scene_id": scene_id,
            "shots": shot_ids,
        }
        groups.append(g)

    # ═══════════════════════════════════════════
    #  主循环
    # ═══════════════════════════════════════════

    def run(self) -> dict:
        self.load()
        self._log(f"  🔄 迭代优化（strict={self.strict}, gentle={self.gentle}）")
        self._log(f"    类型配置: '{self.data.get('script', {}).get('type', '未知')}'")

        for self.round in range(1, MAX_ROUNDS + 1):
            issues = self.validate()
            p0 = [i for i in issues if i.priority == "P0"]
            p1 = [i for i in issues if i.priority == "P1"]
            snapshot = (len(p0), len(p1))
            self.history.append(snapshot)

            # 输出
            n_issues = len(issues)
            bar = '─' * max(0, 25 - n_issues)
            self._log(f"  ── 第{self.round}轮 P0={len(p0)} P1={len(p1)} {bar}")

            if p0:
                for i in p0:
                    self._log(f"    🔴 [{i.priority}] {i.msg}")

            pass_cond = (len(p0) == 0 and len(p1) <= (0 if self.strict else 2))
            if pass_cond:
                self._log(f"  ✅ 通过 (P0={len(p0)}, P1={len(p1)})")
                break
            if self.round >= 2 and snapshot == self.history[-2]:
                self._log(f"  ⚠️ 停滞 — 连续 2 轮无改善")
                break
            if self.round == MAX_ROUNDS:
                self._log(f"  ⚠️ 达最大轮数 {MAX_ROUNDS}")
                break

            # 修复 + 保存（含错误恢复）
            try:
                self.fix_all(issues)
                self.save()
            except Exception as e:
                import traceback as _tb
                self._log(f"  ❌ 修复/保存异常: {e}")
                for _line in _tb.format_exc().splitlines():
                    self._log(f"     {_line}")
                # 重新加载保证 data 一致性
                self.load()
                self._log(f"  ↩️ 已回滚到上一轮状态")
                break

        # 输出修复报告
        self._log(f"  📋 修复日志:")
        if self.fix_log:
            for action, detail in self.fix_log:
                self._log(f"    ✅ {action}: {detail}")
        else:
            self._log(f"    无需要修复项")

        # 最终状态
        final = self.validate()
        p0_issues = [i for i in final if i.priority == "P0"]
        p1_issues = [i for i in final if i.priority == "P1"]
        p2_issues = [i for i in final if i.priority == "P2"]

        if self.fix_log:
            self.save()

        pass_cond = (len(p0_issues) == 0 and len(p1_issues) <= (0 if self.strict else 2))
        status = "pass" if pass_cond else ("stuck" if len(p0_issues) > 0 else "pass_with_known")

        result = {
            "status": status,
            "rounds": self.round,
            "p0_remaining": len(p0_issues),
            "p1_remaining": len(p1_issues),
            "p2_total": len(p2_issues),
            "auto_fixes": [f"{a}: {d}" for a, d in self.fix_log],
            "remaining_issues": [{"priority": i.priority, "msg": i.msg, "location": i.location}
                                 for i in p0_issues + p1_issues],
        }

        icon = {"pass": "✅", "pass_with_known": "⚠️", "stuck": "❌"}.get(status, "❓")
        self._log(f"  ── 结果 {icon} {status} P0={len(p0_issues)} P1={len(p1_issues)} P2={len(p2_issues)} {len(self.fix_log)} fixes")

        return result


def report_only(project: str, json_mode: bool = False):
    opt = OptimizerV2(project, json_mode=json_mode)
    opt.load()
    project_ver = opt.data.get("script", {}).get("_optimizer_version", "无")
    _out = sys.stderr if json_mode else None
    print(f"  optimizer 版本: {OPTIMIZER_VERSION} | 项目版本: {project_ver}", file=_out, flush=True)
    issues = opt.validate()
    _out = sys.stderr if json_mode else None
    for i in issues:
        icon = {"P0": "🔴", "P1": "🟡", "P2": "💡"}.get(i.priority, "❓")
        print(f"  {icon} [{i.priority}] {i.msg}", file=_out, flush=True)
    p0 = sum(1 for i in issues if i.priority == "P0")
    p1 = sum(1 for i in issues if i.priority == "P1")
    print(f"  ── P0={p0} P1={p1} P2={len(issues)-p0-p1}", file=_out, flush=True)
    if json_mode:
        print(json.dumps({"status": "report", "p0": p0, "p1": p1, "p2": len(issues)-p0-p1,
                          "issues": [{"priority": i.priority, "msg": i.msg, "location": i.location} for i in issues]},
                         ensure_ascii=False), flush=True)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="script-optimizer v2: 全自动脚本质量优化器")
    parser.add_argument("--project", required=True)
    parser.add_argument("--strict", action="store_true", help="strict 模式 P1 必须为 0")
    parser.add_argument("--gentle", action="store_true", default=False,
                        help="gentle 模式：仅修复模板默认值（默认由主逻辑决定）")
    parser.add_argument("--no-gentle", action="store_true", dest="force",
                        help="关闭 gentle 模式：覆盖所有字段（含人工编辑的）")
    parser.add_argument("--force", action="store_true", dest="force",
                        help="同 --no-gentle")
    parser.add_argument("--sync-type", action="store_true",
                        help="从类型 .md 重新应用默认配置到当前项目（覆盖已存在的字段）")
    parser.add_argument("--fix-prompts", action="store_true",
                        help="验证后自动修复首帧图/视频 prompt 文件（调用 prompt_builder）")
    parser.add_argument("--dry-run", action="store_true", help="预览模式：展示将做的修改但不写入")
    parser.add_argument("--report-only", action="store_true", help="仅报告不修复")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式结果（供 project-generate 解析）")
    parser.add_argument("--log-file", default="", help="日志文件路径（默认: <project>/optimize.log）")
    args = parser.parse_args()

    gentle = not (args.force or args.report_only or args.sync_type)
    json_mode = args.json or (args.report_only and args.json)
    opt = OptimizerV2(args.project, args.strict, gentle=gentle, json_mode=json_mode)

    def _emit_json(result: dict):
        """输出 JSON 格式并退出"""
        print(json.dumps(result, ensure_ascii=False), flush=True)

    if args.sync_type:
        """从类型 .md 重新应用默认配置到当前项目"""
        opt.load()
        old_profile = opt.profile.copy()
        opt._load_profile()
        new_cfg = {k: v for k, v in opt.profile.items() if k in _BASE_DEFAULTS}
        sc = opt.data.setdefault("script", {})
        changed = []
        for k, v in new_cfg.items():
            old = sc.get(k, "")
            if old != v:
                changed.append({"key": k, "old": str(old)[:20], "new": str(v)[:20]})
        if not changed:
            if args.json:
                print(json.dumps({"status": "sync_type", "changed": []}), flush=True)
            else:
                print(f"  无变化", flush=True)
            return
        if args.dry_run:
            if args.json:
                print(json.dumps({"status": "sync_type_dry_run", "changed": changed}), flush=True)
            else:
                print(f"  🔍 DRY RUN — 将同步以下字段（不写入）:", flush=True)
                for c in changed:
                    print(f"    {c['key']}: '{c['old']}' → '{c['new']}'", flush=True)
            return
        for c in changed:
            sc[c["key"]] = new_cfg[c["key"]]
        sc["_optimizer_version"] = OPTIMIZER_VERSION
        opt.save()
        if args.json:
            print(json.dumps({"status": "sync_type_ok", "changed": changed}), flush=True)
        else:
            for c in changed:
                print(f"  ✅ {c['key']}: '{c['old']}' → '{c['new']}'", flush=True)
        return

    if args.report_only:
        if args.json:
            report_only(args.project, json_mode=True)
        else:
            report_only(args.project)
        return

    if args.dry_run:
        opt.load()
        orig = copy.deepcopy(opt.data)
        issues = opt.validate()
        p0 = [i for i in issues if i.priority == "P0"]
        p1 = [i for i in issues if i.priority == "P1"]
        _out = sys.stderr if args.json else None
        if not args.json:
            print(f"  🔍 DRY RUN — 将执行以下修复（不写入）:", flush=True)
        opt.fix_all(issues)
        for action, detail in opt.fix_log:
            if not args.json:
                print(f"    ✅ {action}: {detail}", flush=True)
        if not opt.fix_log and not args.json:
            print(f"    无需要修复项", flush=True)
        if not args.json:
            print(f"  ── P0={len(p0)} P1={len(p1)} P2={len([i for i in issues if i.priority == 'P2'])}", file=_out, flush=True)
        opt.data = orig
        if args.json:
            _emit_json({"status": "dry_run", "p0": len(p0), "p1": len(p1),
                         "fixes": [f"{a}: {d}" for a, d in opt.fix_log],
                         "issues": [{"priority": i.priority, "msg": i.msg} for i in issues]})
        return

    result = opt.run()

    # ── 自动修复 prompt 文件（--fix-prompts） ──────────────
    if args.fix_prompts:
        remaining = result.get("remaining_issues", [])
        shot_issues = [i for i in remaining if "shot" in i.get("location", "")
                       and "_image" in i.get("location", "")]
        video_issues = [i for i in remaining if "video_shot" in i.get("location", "")]
        char_issues = [i for i in remaining if "characters/" in i.get("location", "")]
        scene_issues = [i for i in remaining if "scenes/" in i.get("location", "")]
        from prompt_builder import (fix_first_frame_prompts, fix_video_prompts,
                                    fix_character_prompts, fix_scene_prompts,
                                    validate_prompts)
        fixed_ff = fix_first_frame_prompts(args.project, shot_issues) if shot_issues else 0
        fixed_vid = fix_video_prompts(args.project, video_issues) if video_issues else 0
        fixed_ch = fix_character_prompts(args.project, char_issues) if char_issues else 0
        fixed_sc = fix_scene_prompts(args.project, scene_issues) if scene_issues else 0
        # 额外从 prompt 验证获取 issues 并修复
        prompt_issues = validate_prompts(args.project)
        p_video = [i for i in prompt_issues if "video_shot" in i.get("location", "")]
        p_char = [i for i in prompt_issues if "characters/" in i.get("location", "")]
        p_scene = [i for i in prompt_issues if "scenes/" in i.get("location", "")]
        p_shot = [i for i in prompt_issues
                  if i.get("location", "").endswith("_image.md")]
        if p_video: fixed_vid += fix_video_prompts(args.project, p_video)
        if p_char: fixed_ch += fix_character_prompts(args.project, p_char)
        if p_scene: fixed_sc += fix_scene_prompts(args.project, p_scene)
        if p_shot: fixed_ff += fix_first_frame_prompts(args.project, p_shot)
        if fixed_ff or fixed_vid or fixed_ch or fixed_sc:
            print(f"  ✅ 已自动修复 {fixed_ff} 个首帧图 + {fixed_vid} 个视频 + "
                  f"{fixed_ch} 个角色 + {fixed_sc} 个场景 prompt", flush=True)
            # 重新运行验证更新 result
            opt.load()
            issues = opt.validate()
            p0 = [i for i in issues if i.priority == "P0"]
            p1 = [i for i in issues if i.priority == "P1"]
            status = "pass" if len(p0) == 0 else ("stuck" if len(p0) > 0 else "pass_with_known")
            result = {
                "status": status, "rounds": opt.round,
                "p0_remaining": len(p0), "p1_remaining": len(p1),
                "p2_total": len([i for i in issues if i.priority == "P2"]),
                "auto_fixes": [f"{a}: {d}" for a, d in opt.fix_log],
                "remaining_issues": [{"priority": i.priority, "msg": i.msg, "location": i.location}
                                     for i in p0 + p1],
            }
    # ────────────────────────────────────────────────────

    # 写日志
    log_path = args.log_file or os.path.join(args.project, "optimize.log")
    opt.write_log(log_path)
    _out = sys.stderr if args.json else None
    print(f"  📄 日志已保存: {log_path}", file=_out, flush=True)

    if args.json:
        _emit_json(result)

    if result["status"] == "stuck":
        sys.exit(1)


if __name__ == "__main__":
    main()
