"""BaseProvider — 项目级辅助函数，不绑定特定 AI 工具。

所有 provider 继承此类，只需覆盖 AI 专用的生成/提交方法。
"""
import os, sys
from abc import ABC, abstractmethod
from typing import Any

# 注意：不要模块级 import config / video_utils — 
# 这会加载 project-generate 的 config 到 sys.modules，
# 导致 agnes-ai 模块的 config 被遮挡。改为方法内局部导入。

# ── 确保 project-generate 的 modules 可导入 ──
_modules_dir = os.path.dirname(os.path.abspath(__file__))
if _modules_dir not in sys.path:
    sys.path.insert(0, _modules_dir)


class BaseProvider(ABC):
    """项目级辅助操作——不依赖特定 AI 工具。

    子类必须实现:
      submit_video(), quick_query(), download_video()
    """

    # ── 视频 API（各 provider 必须实现） ───────────

    @abstractmethod
    def submit_video(self, project, shot_id, prompt, ref_img, duration, aspect,
                     *, mode="standard", ref_urls=None):
        """提交视频生成任务。"""

    @abstractmethod
    def quick_query(self, task_id: str) -> dict[str, Any]:
        """查询视频任务状态。"""

    @abstractmethod
    def download_video(self, url: str, output_path: str) -> str:
        """下载生成的视频文件。"""

    # ── 项目文件操作 ────────────────────────────────────────

    def load_script(self, project: str) -> dict[str, Any]:
        """读取项目的 script.json。"""
        import json
        path = os.path.join(project, "script.json")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"未找到 script.json: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def is_video_done(self, project: str, shot_id: int) -> bool:
        """检查本地 shot 视频文件是否存在。"""
        vpath = os.path.join(project, "videos", f"shot_{shot_id:02d}.mp4")
        return os.path.isfile(vpath)

    def is_first_frame_ready(self, project: str, shot: dict) -> bool:
        """检查 shot 的首帧图是否存在且完整。"""
        ff = shot.get("first_frame")
        if not ff or not isinstance(ff, dict):
            return False
        fpath = ff.get("final", "")
        if not fpath:
            return False
        apath = fpath if os.path.isabs(fpath) else os.path.join(project, fpath)
        return os.path.isfile(apath)

    # ── shot 信息查询 ────────────────────────────────────────

    def find_shot(self, script: dict, shot_id: int) -> dict | None:
        """从 script.json 中找到指定 shot。"""
        for s in script.get("shots", []):
            if s.get("id") == shot_id:
                return s
        return None

    def get_shot_mode(self, script: dict, shot_id: int) -> str:
        """获取 shot 的生成模式（委托 video_utils）。"""
        import video_utils as _vu
        return _vu.get_shot_mode(script, shot_id)

    def get_shot_info(self, project: str, script: dict, shot_id: int, mode: str = "standard") -> dict[str, Any]:
        """提取 shot 的视频生成参数（委托 video_utils + 扩展字段）。"""
        import video_utils as _vu
        s = self.find_shot(script, shot_id)
        if s is None:
            raise ValueError(f"shot_{shot_id:02d} 未找到")

        base = _vu.get_shot_info(script, shot_id, mode, project=project)
        result: dict[str, Any] = {
            "shot_id": shot_id,
            "prompt": base.get("prompt", ""),
            "ref_img": self._first_frame_path(project, shot_id),
            "mode": mode,
            "duration": base.get("duration", 5),
            "aspect": script.get("aspect_ratio", "9:16"),
        }
        if mode in ("multi-image", "keyframes"):
            result["ref_urls"] = self.resolve_ref_images(project, script, shot_id)
        return result

    def _first_frame_path(self, project: str, shot_id: int) -> str | None:
        """获取 shot 的首帧图本地路径。"""
        path = os.path.join(project, "images", "storyboard", f"shot_{shot_id:02d}_first_frame.png")
        if os.path.isfile(path):
            return path
        return None

    def ref_image(self, project: str, shot_id: int) -> str | None:
        """获取 shot 的视频参考图（委托 video_utils）。"""
        import video_utils as _vu
        return _vu.ref_image(project, shot_id)

    # ── 参考图解析（从 script.json 的 generation 字段）──────

    def resolve_ref_images(self, project: str, script: dict, shot_id: int) -> list[str]:
        """解析 shot 的所有参考图路径（优先 video_utils 的 dict 格式，兜底 list 格式）。"""
        s = self.find_shot(script, shot_id)
        if s is None:
            return []
        gen = s.get("generation", {})
        refs = gen.get("reference_images", {})
        # dict 格式（kf1/kf2）→ 用 video_utils
        if isinstance(refs, dict) and refs:
            import video_utils as _vu
            return _vu.resolve_ref_images(project, script, shot_id)
        # list 格式 → 用基类实现
        if isinstance(refs, list):
            resolved = []
            for ref in refs:
                path = ref.get("path", ref) if isinstance(ref, dict) else ref
                apath = path if os.path.isabs(path) else os.path.join(project, path)
                if os.path.isfile(apath):
                    resolved.append(apath)
            return resolved
        return []

    def get_kf_images(self, project: str, script: dict, shot_id: int) -> list[str]:
        """获取 shot 的关键帧参考图（委托 resolve_ref_images）。"""
        return self.resolve_ref_images(project, script, shot_id)

    # ── 验证（纯本地计算）───────────────────────────────────

    def verify(self, project: str, shot_id: int | None = None) -> dict[str, Any]:
        """验证首帧图质量：人物数、模糊度、色彩等（纯本地计算）。"""
        from project_verify import _verify_first_frame
        script = self.load_script(project)
        shot = self.find_shot(script, shot_id) if shot_id else None
        result = _verify_first_frame("", shot or {}, script)
        return result

    # ── 提示词文件写入（各 provider 可覆盖）──────────────────

    def write_prompt_file(self, project: str, shot: dict, built: dict,
                           script_data: dict | None = None, force: bool = False) -> None:
        """生成并写入 shot 级提示词文件。"""
        prompt_file = built.get("prompt_file", "")
        if not prompt_file:
            return
        prompt_abs = prompt_file if os.path.isabs(prompt_file) else os.path.join(project, prompt_file)
        # 检测手动保护标记：即使 --force 也跳过
        _MANUAL_PROTECT = "手动精修，勿自动覆盖"
        if os.path.isfile(prompt_abs):
            if not force:
                from config import _log
                _log(f"     📝 提示词文件已存在: {prompt_file}，保留")
                return
            # --force 模式下仍检查保护标记
            try:
                with open(prompt_abs, encoding="utf-8") as _pf:
                    _first_lines = _pf.read(200)
                if _MANUAL_PROTECT in _first_lines:
                    from config import _log
                    _log(f"     🛡️ {prompt_file} 有精修保护标记，跳过覆盖")
                    return
            except Exception:
                pass
        template = self.generate_prompt_template(shot, built, script_data)
        os.makedirs(os.path.dirname(prompt_abs), exist_ok=True)
        with open(prompt_abs, "w", encoding="utf-8") as pf:
            pf.write(template)
        from config import _log
        _log(f"     📝 提示词模板: {prompt_file} ({len(template)} 字符)")

    def generate_prompt_template(self, shot: dict, ff: dict,
                                  script_data: dict | None = None) -> str:
        """生成提示词模板（各 provider 覆盖）。默认返回空。"""
        return ""

    # ── 角色/场景资产生成（各 provider 可覆盖）────────────────

    def generate_character(self, project: str, card: dict, size: str = "1024x1792") -> str | None:
        """生成角色资产图，返回保存路径。默认抛出 NotImplementedError。"""
        raise NotImplementedError(f"{type(self).__name__} 未实现角色资产生成")

    def generate_scene(self, project: str, card: dict, size: str = "1024x1792",
                       force: bool = False) -> int:
        """生成场景资产图，返回成功生成的图片数量。默认抛出 NotImplementedError。"""
        raise NotImplementedError(f"{type(self).__name__} 未实现场景资产生成")

    def generate_characters(self, project: str, data: dict, force: bool = False) -> int:
        """批量生成所有角色资产图。遍历 character_cards 逐卡调 generate_character，返回成功数量。"""
        count = 0
        for card in data.get("character_cards", []):
            try:
                result = self.generate_character(project, card)
                if result:
                    count += 1
            except NotImplementedError:
                raise
            except Exception as e:
                from config import _log
                _log(f"    ⚠️ 角色 [{card.get('name', '?')}] 生成失败: {e}")
        return count

    # ── 模型选择（各 provider 自行决定默认模型）────────────────

    def get_default_image_model(self, project: str = "") -> str:
        """返回当前 provider 默认的图片生成模型。project 参数允许读取项目级覆盖。"""
        return ""

    def get_default_first_frame_model(self, project: str = "") -> str:
        """返回当前 provider 默认的首帧图模型。project 参数允许读取项目级覆盖。"""
        return ""

    def get_default_video_model(self, project: str = "") -> str:
        """返回当前 provider 默认的视频生成模型。project 参数允许读取项目级覆盖。"""
        return ""

    # ── 首帧图生成（各 provider 可覆盖）────────────────────────────────

    def build_first_frame(self, project: str, shot: dict,
                           script_data: dict | None = None) -> dict | None:
        """构建 shot 首帧图的 metadata。默认返回 None（子类可覆盖实现）。"""
        return None

    def generate_first_frame(self, project: str, shot: dict,
                              script_data: dict | None = None) -> dict | None:
        """生成 shot 的首帧图。默认返回 None（子类可覆盖实现）。"""
        return None
