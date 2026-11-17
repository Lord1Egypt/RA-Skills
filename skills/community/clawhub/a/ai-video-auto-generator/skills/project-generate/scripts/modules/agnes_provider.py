"""AgnesProvider — 统一封装 agnes-ai 所有生成能力。

所有 agnes-ai 模块的调用都通过此 provider，方便切换其他 AI 工具。
"""
import os, sys, json
from typing import Any
from base_provider import BaseProvider
from modules.config import _log
from error_utils import classify as _classify_failure


# ── agnes-ai 模块导入（通过 sys.path 添加子 skill 路径，使用标准 import） ──
_AGNES_MOD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "agnes-ai", "scripts", "modules")
if _AGNES_MOD_DIR not in sys.path:
    sys.path.insert(0, _AGNES_MOD_DIR)

import image_api as _ag_image_api
import video_api as _ag_video_api
import prompt as _ag_prompt

class AgnesProvider(BaseProvider):
    """Agnes AI provider — 封装所有 agnes-ai 的生成能力。"""

    def __init__(self):
        self._img_api = lambda: _ag_image_api
        self._video_api = lambda: _ag_video_api
        self._prompt = lambda: _ag_prompt
        self._get_last = _ag_video_api.get_last_submit_result

    # ── 图片 API ──────────────────────────────────────────────

    def generate_image(self, **kwargs):
        m = self._img_api()
        if "api_key" not in kwargs:
            kwargs["api_key"] = m.load_api_key()
        return m.generate_image(**kwargs)

    def _last_api_error(self) -> dict:
        """读取最近一次图片 API 调用的原始错误（供上层分类+策略用）。"""
        m = self._img_api()
        err = getattr(m, 'get_last_api_error', lambda: None)()
        return err or {}

    def upload_to_url(self, local_path: str, project: str | None = None) -> str:
        return self._img_api().upload_to_url(local_path, project)

    def load_api_key(self) -> str:
        return self._img_api().load_api_key()

    # ── 模型选择（Agnes AI Specific）─────────────────────────

    def _script_model(self, project: str, field: str) -> str:
        """从 script.json 读取模型覆盖，空则走 provider 默认。"""
        import json, os
        sp = os.path.join(project, "script.json")
        if os.path.isfile(sp):
            try:
                with open(sp, encoding="utf-8") as f:
                    sc = json.load(f).get("script", {})
                val = sc.get(field, "")
                if val:
                    return val
            except Exception:
                pass
        return ""

    def get_default_image_model(self, project: str = "") -> str:
        override = self._script_model(project, "asset_generation_model") if project else ""
        return override or "agnes-image-2.1-flash"

    def get_default_first_frame_model(self, project: str = "") -> str:
        override = self._script_model(project, "first_frame_model") if project else ""
        return override or "agnes-image-2.0-flash"

    def get_default_video_model(self, project: str = "") -> str:
        override = self._script_model(project, "video_model") if project else ""
        return override or "agnes-video-v2.0"

    # ── 视频 API ──────────────────────────────────────────────

    def _submit(self, project, shot_id, prompt, ref_img, duration, aspect,
                *, mode="standard", ref_urls=None, negative_prompt=None):
        return self._video_api().submit_video(
            project=project, shot_id=shot_id,
            prompt=prompt, ref_img=ref_img, duration=duration,
            aspect=aspect, mode=mode, ref_urls=ref_urls,
            negative_prompt=negative_prompt,
        )

    def submit_video(self, project, shot_id, prompt, ref_img, duration, aspect,
                     *, mode="standard", ref_urls=None, negative_prompt=None):
        return self._submit(project=project, shot_id=shot_id, prompt=prompt,
                            ref_img=ref_img, duration=duration, aspect=aspect,
                            mode=mode, ref_urls=ref_urls, negative_prompt=negative_prompt)

    def quick_query(self, task_id: str) -> dict[str, Any]:
        return self._video_api().quick_query(task_id)

    def download_video(self, url: str, output_path: str) -> str:
        return _ag_video_api.download_video(url, output_path)

    # ── prompt 模块的 shot 解析函数 ──────────────────────────

    def resolve_shot_params(self, project: str, shot: dict, size: str) -> dict:
        m = self._prompt()
        func = getattr(m, '_resolve_single_shot_params', None)
        if not func:
            raise SystemExit("无法加载 _resolve_single_shot_params（prompt 模块可能未同步）")
        return func(project, shot, size)

    def build_first_frame(self, project: str, shot: dict,
                          script_data: dict | None = None) -> dict | None:
        return self._prompt()._build_first_frame(project, shot, script_data)

    def generate_prompt_template(self, shot: dict, ff: dict,
                                  script_data: dict | None = None) -> str:
        return self._prompt()._generate_prompt_template(shot, ff, script_data)

    def generate_first_frame(self, project: str, shot: dict,
                              script_data: dict | None = None) -> dict | None:
        """生成 shot 首帧图：build_first_frame → generate_prompt_template → generate_image。"""
        try:
            ff = self.build_first_frame(project, shot, script_data)
            if not ff:
                return None
            prompt = self._prompt()._generate_prompt_template(shot, ff, script_data)
            if not prompt:
                return None

            shot_id = shot.get("id", 0)
            out_dir = os.path.join(project, "images", "storyboard")
            os.makedirs(out_dir, exist_ok=True)
            out_name = f"shot_{shot_id:02d}_first_frame.png"

            kwargs = dict(
                prompt=prompt,
                size="1280x720",
                output_dir=out_dir,
                output_name=out_name,
                project=project,
            )
            model = ff.get("model")
            if model:
                kwargs["model"] = model
            refs = ff.get("ref_images")
            if refs:
                kwargs["ref_urls"] = refs

            result = self.generate_image(**kwargs)
            if result and isinstance(result, list) and len(result) > 0:
                final_path = os.path.join(out_dir, out_name)
                return {"status": "ok", "path": result[0], "final": final_path}
            return None
        except Exception as e:
            from config import _log
            _log(f"    ❌ generate_first_frame 失败: {e}")
            return None

    # ── prompt 文件读取 ─────────────────────────────────────────

    def _read_prompt_file(self, path: str) -> str | None:
        """从 prompt .md 文件中读取 body 部分。文件不存在或格式错误时返回 None。"""
        if not os.path.isfile(path):
            return None
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
            import re
            m = re.match(r'^---\n(.*?)\n---\n\n(.*)', content, re.DOTALL)
            if m:
                return m.group(2).strip()
            return content.strip()
        except Exception:
            return None

    def _read_prompt_frontmatter(self, path: str) -> dict:
        """读取 prompt 文件的 YAML frontmatter，返回键值对字典。"""
        result = {}
        if not os.path.isfile(path):
            return result
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
            import re
            m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not m:
                return result
            for line in m.group(1).strip().split("\n"):
                if ":" in line:
                    k, _, v = line.partition(":")
                    result[k.strip()] = v.strip().strip('"')
        except Exception:
            pass
        return result

    # ── 角色资产生成 ──────────────────────────────────────────

    CHARACTER_VIEWS = {
        "front": "正面全身照，面向镜头，展示人物全身形象和服装全貌",
        "face": "面部特写，展示五官细节和表情",
        "side": "侧面半身照，展示人物侧面轮廓和发型",
        "back": "背面全身照，展示人物背面轮廓",
    }

    def generate_character(self, project: str, card: dict, size: str = "1024x1792") -> str | None:
        """根据角色卡生成多视角角色图（含标准4视图 + action/pose扩展视图）。
        提示词必须已通过 build-prompts 生成到 prompts/characters/ 目录。
        无 prompt 文件时自动调用 prompt_builder 生成，仍失败则报错退出。
        """
        from modules.config import _auto_size
        name = card.get("name", "角色")
        slug = name.replace(" ", "_")
        char_dir = os.path.join(project, "images", "characters")
        os.makedirs(char_dir, exist_ok=True)

        # 角色资产尺寸：跟随项目 aspect_ratio，prompt 中通过构图约束保证全身照

        # 组装所有视图：标准4视图 + action/pose 扩展
        view_keys = list(self.CHARACTER_VIEWS.items())
        for w in (card.get("weapons") or []):
            view_keys.append((f"action_{w}", f"使用{w}的动作姿态"))
        for a in (card.get("actions") or []):
            view_keys.append((f"pose_{a}", f"{a}姿势"))

        generated: list[str] = []
        front_path: str | None = None

        _log(f"  [{name}] {len(view_keys)} 个视角，开始生成...")
        for idx, (view, view_desc) in enumerate(view_keys, 1):
            out_name = f"{slug}_{view}.png"
            out_path = os.path.join(char_dir, out_name)
            if os.path.isfile(out_path):
                _log(f"  [{idx}/{len(view_keys)}] ⏭️ {out_name} 已存在")
                generated.append(out_path)
                if view == "front":
                    front_path = out_path
                continue

            # 只从 prompt 文件读取提示词（必须在 build-prompts 后运行）
            prompt_file = os.path.join(project, "prompts", "characters", f"{slug}_{view}.md")
            prompt = self._read_prompt_file(prompt_file)

            if not prompt:
                # 自动调用 prompt_builder 生成
                _log(f"    └─ prompt 文件不存在，调用 build-prompts 生成...")
                try:
                    import subprocess
                    pb = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))))),
                        "script-optimizer", "scripts", "prompt_builder.py")
                    if os.path.isfile(pb):
                        subprocess.run(
                            [sys.executable, pb, "--project", project],
                            capture_output=True, timeout=60,
                            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
                    prompt = self._read_prompt_file(prompt_file)
                except Exception as e:
                    _log(f"    ❌ build-prompts 调用失败: {e}")

            if not prompt:
                raise SystemExit(
                    f"❌ 未找到 {prompt_file}。请先运行 build-prompts 生成提示词文件。\n"
                    f"   命令: project_generate.py --project {project} build-prompts")

            _log(f"    └─ 使用 prompt 文件: prompts/characters/{slug}_{view}.md")

            kwargs = dict(prompt=prompt, size=size, output_dir=char_dir, output_name=out_name, project=project)
            kwargs["negative_prompt"] = "畸变, 变形, 模糊, 低质量, 丑陋, 多余肢体"
            if view != "front" and front_path:
                kwargs["ref_image"] = front_path

            # 错误感知重试：生成失败 → 分析错误 → 应用策略 → 重试
            max_attempts = 5
            current_prompt = prompt
            current_model = kwargs.get("model") or self.get_default_image_model(project)
            for attempt in range(max_attempts):
                kw = {**kwargs, "prompt": current_prompt}
                if current_model:
                    kw["model"] = current_model
                result = self.generate_image(**kw)
                if result and isinstance(result, list) and len(result) > 0:
                    _log(f"  [{idx}/{len(view_keys)}] ✅ {out_name}")
                    if view == "front":
                        front_path = result[0]
                    generated.append(result[0])
                    break

                # 分析错误 → 应用策略
                raw_err = self._last_api_error()
                category, _ = _classify_failure(raw_err, "")
                from error_utils import apply_image_strategy as _apply
                current_prompt, current_model, desc = _apply(category, current_prompt, current_model)
                _log(f"    └─ 第{attempt+1}次失败（{category}），策略: {desc}")
                if category == "rate_limit":
                    import time
                    time.sleep(30)
            else:
                _log(f"  [{idx}/{len(view_keys)}] ❌ {out_name} 生成失败（{max_attempts}次尝试）")

        return generated[0] if generated else None

    # ── 场景资产生成 ──────────────────────────────────────────

    SCENE_VIEWS = {
        "广角": "广角全景视角，展示场景的全貌和空间布局",
        "中景": "中景构图，展现场景主体区域的细节和环境",
        "特写": "特写视角，聚焦场景中最具代表性的局部细节",
    }

    def generate_scene(self, project: str, card: dict, size: str = "1024x1792",
                       force: bool = False, target_views: list[str] | None = None) -> int:
        """根据场景卡生成 3 种变体（广角/中景/特写）。
        提示词必须已通过 build-prompts 生成到 prompts/scenes/ 目录。
        
        Args:
            target_views: 仅生成指定视图（如 ['特写']），None=全部
        """
        name = card.get("name", "场景")
        slug = card.get("id", name).replace(" ", "_")
        scene_dir = os.path.join(project, "images", "scenes")
        os.makedirs(scene_dir, exist_ok=True)

        ok = 0
        scene_views = list(self.SCENE_VIEWS.items())
        default = self.get_default_image_model(project)
        models_to_try = [default, "agnes-image-2.0-flash"] if default else ["agnes-image-2.1-flash", "agnes-image-2.0-flash"]
        view_filter = set(target_views) if target_views else None
        if view_filter:
            _log(f"  [{name}] 定向重试 {len(view_filter)} 个视图: {', '.join(view_filter)}")
        else:
            _log(f"  [{name}] {len(scene_views)} 张场景图，开始生成...")

        scene_dir_abs = os.path.abspath(scene_dir)

        for idx, (view, view_desc) in enumerate(scene_views, 1):
            out_name = f"{slug}_{view}.png"
            out_path = os.path.join(scene_dir, out_name)

            # 视图级别过滤：只生成 target_views 中指定的视图
            if view_filter is not None and view not in view_filter:
                if os.path.isfile(out_path):
                    ok += 1  # 已存在就算成功，不影响总计数
                    _log(f"  [{idx}/{len(scene_views)}] ⏭️ {out_name} 无需重试（非修复目标）")
                    continue
                else:
                    # 视图不存在但也不是修复目标——跳过（可能是某个不存在的视图）
                    continue

            if os.path.isfile(out_path) and not force:
                _log(f"  [{idx}/{len(scene_views)}] ⏭️ {out_name} 已存在（--force 覆盖）")
                ok += 1
                continue

            # 从 prompt 文件读取提示词和 frontmatter（含 ref_image）
            prompt_file = os.path.join(project, "prompts", "scenes", f"{slug}_{view}.md")
            prompt = self._read_prompt_file(prompt_file)
            fm = self._read_prompt_frontmatter(prompt_file)

            if not prompt:
                _log(f"    └─ 场景 prompt 文件不存在，调用 build-prompts 生成...")
                try:
                    import subprocess
                    pb = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))))),
                        "script-optimizer", "scripts", "prompt_builder.py")
                    if os.path.isfile(pb):
                        subprocess.run(
                            [sys.executable, pb, "--project", project],
                            capture_output=True, timeout=60,
                            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
                    prompt = self._read_prompt_file(prompt_file)
                    fm = self._read_prompt_frontmatter(prompt_file)
                except Exception as e:
                    _log(f"    ❌ build-prompts 调用失败: {e}")

            if not prompt:
                raise SystemExit(
                    f"❌ 未找到 {prompt_file}。请先运行 build-prompts 生成提示词文件。\n"
                    f"   命令: project_generate.py --project {project} build-prompts")

            # 从 frontmatter 读取 ref_image（图生图时以广角为参考图）
            ref_img_from_fm = fm.get("ref_image", "")
            ref_img_abs = ""
            if ref_img_from_fm:
                ref_img_abs = ref_img_from_fm if os.path.isabs(ref_img_from_fm) else os.path.join(project, ref_img_from_fm)
                if not os.path.isfile(ref_img_abs):
                    ref_img_abs = ""

            _log(f"  [{idx}/{len(scene_views)}] → 使用 prompt 文件: prompts/scenes/{slug}_{view}.md"
                 f"{'（以广角为参考图）' if ref_img_abs else ''}")

            img_result = None
            # 错误感知重试：生成失败 → 分析错误 → 应用策略 → 重试
            current_prompt = prompt
            current_model = models_to_try[0]
            max_attempts = 5
            for attempt in range(max_attempts):
                gen_kwargs = dict(
                    prompt=current_prompt, size=size,
                    model=current_model,
                    output_dir=scene_dir_abs, output_name=out_name,
                    project=project,
                    negative_prompt=(
                        "person, people, human, character, figure, silhouette, "
                        "人物, 人, 行人, 角色, 人类, 人群, 人脸, 面部, 身体, 人体, "
                        "人物剪影, 生物, 活物, 主播, 主持人, 演讲者, 人像, 肖像, "
                        "全身, 半身, 人物出现, 说话的人, 人物肢体, 女孩, 男孩, 女性, 男性, "
                        "坐着的人, 站着的人, 动漫人物, 多余人, "
                        "海报, 人物照片, 人物肖像, 带人脸的装饰, 唱片封面上的人, "
                        "poster, photo, portrait, framed photo, album cover with people, "
                        "anime girl, anime poster, character poster, girl on poster, "
                        "动漫海报, 动漫角色, 人物挂画, "
                        "人影, 人物倒影, 倒影, 影子, "
                        "photorealistic, realistic photo, real photo, photograph, "
                        "写实, 写实照片, 真实照片, 摄影, 电影感"
                    ),
                    seed=50,
                )
                if ref_img_abs:
                    gen_kwargs["ref_images"] = [ref_img_abs]
                result = self.generate_image(**gen_kwargs)
                if result and isinstance(result, list) and len(result) > 0:
                    img_result = result
                    _log(f"    └─ ✅ 生成成功")
                    break

                # 分析错误 → 应用策略
                raw_err = self._last_api_error()
                category, _ = _classify_failure(raw_err, "")
                from error_utils import apply_image_strategy as _apply
                current_prompt, current_model, desc = _apply(category, current_prompt, current_model)
                _log(f"    └─ 第{attempt+1}次失败（{category}），策略: {desc}")
                if category == "rate_limit":
                    import time
                    time.sleep(30)
            else:
                _log(f"  [{idx}/{len(scene_views)}] ❌ 所有策略均失败")

            if img_result:
                _log(f"  [{idx}/{len(scene_views)}] ✅ {out_name}")
                ok += 1
            else:
                _log(f"  [{idx}/{len(scene_views)}] ❌ {out_name} 生成失败")

        return ok
