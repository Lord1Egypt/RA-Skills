"""
小云雀（Seedance 2.0）Provider — 视频生成 + 分段合并。
"""
from __future__ import annotations
import json, os
from typing import Any, Optional

from base_provider import BaseProvider
from modules.config import _log, get_xiaoyunqiao_access_key, get_xiaoyunqiao_secret_key

SEG_MIN_SECONDS = 15
SEG_MAX_SECONDS = 45


class XiaoyunqiaoProvider(BaseProvider):
    """小云雀 provider — 视频生成 + segment 自动合并。"""

    REQ_KEY = "pippit_iv2v_v20_cvtob_with_vinput"
    DURATION_MAP: dict[int, str] = {d: "40～60s" for d in range(31, 61)}
    for d in range(1, 16):  DURATION_MAP[d] = "～15s"
    for d in range(16, 31): DURATION_MAP[d] = "～30s"

    def __init__(self):
        super().__init__()
        self._client = self._init_client()
        self._last_submit_result: dict[str, Any] = {}
        self._last_script: dict | None = None
        self._segments_cached: list[dict] | None = None

    def _init_client(self):
        """初始化小云雀 API 客户端。"""
        from volcengine.visual.VisualService import VisualService
        ak = get_xiaoyunqiao_access_key()
        sk = get_xiaoyunqiao_secret_key()
        if not ak or not sk:
            print("  ❌ 未找到小云雀 AK/SK（<skill_root>/config/config.toml [xiaoyunqiao] 或 VOLCENGINE_* 环境变量）")
            return None
        vs = VisualService()
        vs.set_ak(ak)
        vs.set_sk(sk)
        return vs

    def _collect_ref_urls(self, project: str, ref_urls: list[str] | None,
                          ref_img: str) -> list[str]:
        """收集并上传参考图，返回 URL 列表。"""
        img_urls: list[str] = []
        if ref_urls:
            for u in ref_urls:
                if u.startswith("http://") or u.startswith("https://"):
                    img_urls.append(u)
                elif os.path.isfile(u):
                    from img_host import upload_image
                    pn = os.path.basename(project) if os.path.isdir(project) else "default"
                    url = upload_image(u, project=pn)
                    if url: img_urls.append(url)
                    else: print(f"    ⚠️ 参考图上传失败: {u[:60]}")
                else:
                    print(f"    ⚠️ 无效参考图: {u[:60]}")
        elif ref_img and os.path.isfile(ref_img):
            from img_host import upload_image
            pn = os.path.basename(project) if os.path.isdir(project) else "default"
            url = upload_image(ref_img, project=pn)
            if url: img_urls.append(url)
            else: print("  ❌ 参考图上传播失败"); return []
        return img_urls

    def _do_submit(self, project: str, shot_id: int | str, prompt: str, ref_img: str,
                   duration: int, aspect: str = "9:16", mode: str | None = None,
                   ref_urls: list[str] | None = None,
                   seed: int | None = None,
                   negative_prompt: str | None = None) -> str | None:
        """小云雀 API 提交（内部方法）。"""
        client = self._client
        if not client:
            return None

        print(f"  [小云雀] 提交 {shot_id}...")
        img_urls = self._collect_ref_urls(project, ref_urls, ref_img)
        if not img_urls:
            print("  ❌ 无参考图"); return None

        form: dict[str, Any] = {
            "req_key": self.REQ_KEY,
            "prompt": prompt,
            "img_url_list": img_urls,
            "ratio": aspect if aspect in ("16:9", "9:16", "4:3", "3:4") else "9:16",
            "enable_watermark": False,
            "duration": self.DURATION_MAP.get(duration, "～15s"),
        }
        print(f"    [时长] {duration}s → {form['duration']}")
        print(f"    [参考图] {len(img_urls)} 张")

        self._last_submit_result = {"image_urls": img_urls}
        try:
            resp = client.cv_sync2async_submit_task(form)
            if resp.get("code") != 10000:
                msg = resp.get("message", "未知错误")
                print(f"  ❌ 提交失败: {msg}"); return None
            task_id = str(resp.get("data", {}).get("task_id", ""))
            if not task_id:
                print(f"  ❌ 返回无 task_id: {json.dumps(resp, ensure_ascii=False)[:200]}")
                return None
            print(f"  ✅ task_id={task_id}")
            return task_id
        except Exception as e:
            print(f"  ❌ 提交异常: {e}"); return None

    def _do_query(self, task_id: str) -> dict[str, Any]:
        """小云雀 API 查询（内部方法）。"""
        client = self._client
        if not client:
            return {"status": "error", "progress": 0, "video_url": None, "raw": {}}

        form = {"req_key": self.REQ_KEY, "task_id": task_id}
        try:
            resp = client.cv_sync2async_get_result(form)
        except Exception as e:
            return {"status": "error", "progress": 0, "video_url": None, "raw": {"error": str(e)}}

        if resp.get("code") != 10000:
            return {"status": "error", "progress": 0, "video_url": None, "raw": resp}

        data = resp.get("data", {})
        sdk_status = data.get("status", "")

        if sdk_status == "done":
            video_url = data.get("video_url", "") or None
            if video_url:
                return {"status": "completed", "progress": 100, "video_url": video_url, "raw": resp}
            return {"status": "failed", "progress": 0, "video_url": None, "raw": resp}
        elif sdk_status in ("processing", "in_queue", "generating"):
            return {"status": "in_progress", "progress": 50, "video_url": None, "raw": resp}
        elif sdk_status == "not_found":
            return {"status": "error", "progress": 0, "video_url": None, "raw": resp}
        elif sdk_status == "expired":
            return {"status": "failed", "progress": 0, "video_url": None, "raw": resp}
        else:
            return {"status": "queued", "progress": 0, "video_url": None, "raw": resp}

    # ── 视频 API（公开方法）───────────────────────

    def submit_video(self, project, shot_id, prompt, ref_img, duration, aspect,
                     *, mode="standard", ref_urls=None):
        return self._do_submit(project, shot_id, prompt, ref_img,
                               duration, aspect, mode=mode, ref_urls=ref_urls)

    def quick_query(self, task_id: str) -> dict[str, Any]:
        return self._do_query(task_id)

    def download_video(self, url: str, output_path: str) -> str:
        from urllib.request import Request, urlopen
        import shutil
        _log(f"  [下载] 从 {url[:60]}...")
        req = Request(url, method="GET")
        with urlopen(req, timeout=300) as resp:
            with open(output_path, "wb") as f:
                shutil.copyfileobj(resp, f)
        _log(f"  [OK] 保存: {output_path}")
        return output_path

    def load_api_key(self) -> str:
        return ""

    def get_last_result(self) -> dict[str, Any] | None:
        return self._last_submit_result if self._last_submit_result else None

    # ── 提示词生成（覆盖 BaseProvider） ───────

    def generate_prompt_template(self, shot: dict, ff: dict,
                                  script_data: dict | None = None) -> str:
        """小云雀版 shot 级提示词模板：更注重镜头运动和角色保持。"""
        sid = shot.get("id", "?")
        desc = shot.get("description", "")
        prompt = shot.get("video_prompt_cn") or shot.get("video_prompt", "") or desc
        ref_count = len(ff.get("ref_images", []))

        lines = []
        lines.append("[编辑指令]")
        if ref_count > 0:
            lines.append(f"参考图包含{ref_count}张素材，保持角色和场景视觉特征一致。")
        lines.append(f"生成一段连续镜头：{prompt[:120]}")
        lines.append("")
        lines.append("[目标风格/场景]")
        # 从 first_frame 的 ref_images 取场景名
        refs = ff.get("ref_images", [])
        scene_name = os.path.basename(refs[0]).replace(".png", "") if refs else ""
        lines.append(scene_name or "古装战争场景")
        lines.append("")
        lines.append("[镜头运动]")
        lines.append("单镜头缓慢运动，覆盖上述动作内容，避免跳跃。")
        lines.append("")
        lines.append("[角色保持]")
        lines.append("保持参考图中角色的铠甲/服装/发型颜色和样式不变，")
        lines.append("面部特征和体型保持一致。")
        lines.append("")
        lines.append("[光照与氛围]")
        desc_txt = desc if isinstance(desc, str) else str(desc)
        if "烛火" in desc_txt:
            lines.append("烛火暖光为主，明暗对比柔和。")
        elif "冷光" in desc_txt or "天光" in desc_txt or "阴沉" in desc_txt:
            lines.append("冷灰天光，低饱和度，压抑氛围。")
        else:
            lines.append("自然光照，符合场景时间设定。")
        lines.append("")
        lines.append("[画质要求]")
        lines.append("1080P，电影级写实，运动流畅，无画面扭曲。")
        return "\n".join(lines)

    def write_prompt_file(self, project: str, shot: dict, built: dict,
                           script_data: dict | None = None, force: bool = False) -> None:
        """覆盖 BaseProvider：小云雀写 shot 级提示词 + 后端生成 segment 级提示词。"""
        # 先写 shot 级提示词（基类默认逻辑）
        super().write_prompt_file(project, shot, built, script_data, force)

        if script_data is None:
            return

        # 首次调用时缓存 segments，避免每 shot 重复重建
        if self._segments_cached is None:
            self._segments_cached = self.build_segments(project, script_data)
            self.write_segments_to_script(project, script_data, self._segments_cached)

        # 写 segment 级 prompt
        for seg in self._segments_cached:
            prompt_file = seg.get("prompt_file", "")
            if not prompt_file:
                continue
            prompt_abs = prompt_file if os.path.isabs(prompt_file) else os.path.join(project, prompt_file)
            if os.path.isfile(prompt_abs) and not force:
                continue
            template = self.generate_segment_prompt_template(seg, script_data.get("shots", []), script_data)
            os.makedirs(os.path.dirname(prompt_abs), exist_ok=True)
            with open(prompt_abs, "w", encoding="utf-8") as pf:
                pf.write(template)
            _log(f"     📝 段落提示词: {prompt_file} ({len(template)} 字符)")

        # 写入 xiaoyunqiao_segments 到 script.json（在首次调用时已完成）
        # 此处不再重复调用，_segments_cached 已在首次调用的缓存中写入

    # ── Segment 合并（独家逻辑，provider 专属） ──

    def build_segments(self, project: str, script: dict | None = None) -> list[dict]:
        """自动合并 shot 为 segment（实现"六条规则"）。"""
        if script is None:
            script = self.load_script(project)
        self._last_script = script
        shots = script.get("shots", [])
        groups = script.get("shot_groups", [])
        raw_groups = self._group_by_scene(shots)
        segments = self._split_and_merge(raw_groups, shots, groups)
        for i, seg in enumerate(segments):
            seg["segment"] = i + 1
            self._fill_segment_details(seg, shots, project)
        return segments

    def _group_by_scene(self, shots):
        groups, cur_scene, cur_ids = [], None, []
        for s in shots:
            scene = self._detect_scene(s)
            if scene != cur_scene and cur_ids:
                groups.append({"scene": cur_scene, "shot_ids": cur_ids})
                cur_ids = []
            cur_scene = scene
            cur_ids.append(s["id"])
        if cur_ids:
            groups.append({"scene": cur_scene, "shot_ids": cur_ids})
        return groups

    def _detect_scene(self, shot):
        ff = shot.get("first_frame") or {}
        refs = (ff.get("ref_images") or []) if isinstance(ff, dict) else []
        if refs:
            return os.path.basename(refs[0])
        gen = shot.get("generation", {})
        if isinstance(gen, dict):
            gen_refs = gen.get("reference_images", {})
            if isinstance(gen_refs, dict):
                for k in sorted(gen_refs.keys()):
                    entry = gen_refs[k]
                    if isinstance(entry, dict) and entry.get("path", ""):
                        return os.path.basename(entry["path"])
        return f"scene_{shot.get('id', '?')}"

    def _split_and_merge(self, raw_groups, shots, shot_groups):
        segments = []
        shot_map = {s["id"]: s for s in shots}
        for i, g in enumerate(raw_groups):
            ids = g["shot_ids"]
            total_dur = sum(shot_map[sid].get("duration_seconds", 5) for sid in ids if sid in shot_map)
            if total_dur < SEG_MIN_SECONDS:
                if segments and self._has_continuous_path(segments[-1], g):
                    segments[-1]["shot_ids"].extend(ids)
                    segments[-1]["scene"] = f"{segments[-1]['scene']} → {g['scene']}"
                    _log(f"  [合并] {segments[-1]['scene']} (不足15s, 跨场景合并)")
                else:
                    segments.append({"scene": g["scene"], "shot_ids": ids, "auto_pad": True})
                    _log(f"  [pad] {g['scene']} ({total_dur}s < 15s, auto-pad)")
            elif total_dur > SEG_MAX_SECONDS:
                sub_segs = self._split_by_groups(ids, shot_map, shot_groups)
                segments.extend(sub_segs)
            else:
                segments.append({"scene": g["scene"], "shot_ids": ids})
        return segments

    def _has_continuous_path(self, prev_seg, next_group):
        prev_ids = prev_seg.get("shot_ids", [])
        script = getattr(self, '_last_script', None) or {}
        shots = script.get("shots", [])
        transition_kw = ["走向门口", "掀帘", "推门", "出门", "登上", "走上",
                         "walk to", "push door", "step out", "climb up"]
        check_ids = prev_ids[-2:] if len(prev_ids) >= 2 else prev_ids
        for s in shots:
            if s["id"] in check_ids:
                desc = (s.get("description") or "").lower()
                if any(kw in desc for kw in transition_kw):
                    return True
        return False

    def _split_by_groups(self, ids, shot_map, shot_groups):
        boundaries: set[int] = set()
        for g in shot_groups:
            boundaries.update(g.get("shots", []))
        sub_segs, cur_ids, cur_total = [], [], 0
        for sid in ids:
            dur = shot_map.get(sid, {}).get("duration_seconds", 5)
            if cur_total >= SEG_MIN_SECONDS and cur_total + dur > SEG_MAX_SECONDS:
                sub_segs.append({"shot_ids": cur_ids}); cur_ids, cur_total = [], 0
            if cur_total >= (SEG_MIN_SECONDS + SEG_MAX_SECONDS) // 2 and sid in boundaries:
                sub_segs.append({"shot_ids": cur_ids}); cur_ids, cur_total = [], 0
            cur_ids.append(sid); cur_total += dur
        if cur_ids:
            sub_segs.append({"shot_ids": cur_ids})
        _log(f"  [拆分] {len(sub_segs)} 段 (超{SEG_MAX_SECONDS}s)")
        return sub_segs

    def _fill_segment_details(self, seg, shots, project):
        ids = seg["shot_ids"]
        total_dur = sum(s.get("duration_seconds", 5) for s in shots if s["id"] in ids)
        seg["duration_range"] = "40～60s" if total_dur > 30 else ("～30s" if total_dur > 15 else "～15s")

        all_refs, seen = [], set()
        for s in shots:
            if s["id"] not in ids:
                continue
            ff = s.get("first_frame") or {}
            for r in (ff.get("ref_images") or []) if isinstance(ff, dict) else []:
                if r not in seen: all_refs.append(r); seen.add(r)
            gen = s.get("generation", {})
            if isinstance(gen, dict):
                gr = gen.get("reference_images", {})
                if isinstance(gr, dict):
                    for k in sorted(gr.keys()):
                        entry = gr[k] or {}
                        p = entry.get("path", "") if isinstance(entry, dict) else (entry if isinstance(entry, str) else "")
                        if p and p not in seen: all_refs.append(p); seen.add(p)
        seg["ref_images"] = all_refs

        descs = [s.get("description", "")[:30] for s in shots if s["id"] in ids]
        seg["description"] = " → ".join(descs) if descs else seg.get("scene", "")
        raw_scene = seg.get("scene", "") or ""
        seg["scene"] = raw_scene.replace(".png", "").replace("_中景", "").replace("_广角", "").strip()

        os.makedirs(os.path.join(project, "prompts"), exist_ok=True)
        slug = os.path.basename(seg["scene"]).replace(" ", "_").replace("→", "-vs-")
        seg["prompt_file"] = os.path.join("prompts", f"seg{seg['segment']:02d}_{slug}.md")

        if total_dur < SEG_MIN_SECONDS:
            seg["auto_pad"] = True

    def write_segments_to_script(self, project, script=None, segments=None):
        if script is None:
            script = self.load_script(project)
        if segments is None:
            segments = self.build_segments(project, script)
        script["xiaoyunqiao_segments"] = segments
        from config import _safe_write_json
        _safe_write_json(os.path.join(project, "script.json"), script)
        return script

    def generate_segment_prompt_template(self, seg, shots, script_data=None):
        ids = seg.get("shot_ids", [])
        descs = [s.get("description", "") for s in shots if s["id"] in ids]
        ref_count = len(seg.get("ref_images", []))
        scene = seg.get("scene", "").replace("_", "").replace(".png", "")

        lightings = set()
        for s in shots:
            if s["id"] in ids:
                d = (s.get("description") or "").lower()
                if "烛火" in d: lightings.add("烛火暖光")
                if "天光" in d or "冷光" in d or "阴沉" in d: lightings.add("冷灰天光")
                if "硝烟" in d: lightings.add("阴天散光")

        lines = [
            "[编辑指令]",
            f"参考图包含{ref_count}张素材。" if ref_count > 0 else "",
        ]
        if seg.get("auto_pad"):
            lines.append("本段是单场景环境镜头，请用慢节奏推轨/摇镜填充时长。")
        else:
            lines.append("请生成一段连续镜头覆盖以下内容：")
            for i, desc in enumerate(descs):
                lines.append(f"  镜头{i+1}: {desc[:80]}")

        lines += [
            "",
            "[目标风格/场景]",
            scene,
            "",
            "[光照]",
            " + ".join(sorted(lightings)) if lightings else "自然光",
            "",
            "[构图]",
            f"缓慢推轨/摇镜，{scene}环境全景。" if seg.get("auto_pad") else f"连续镜头覆盖{scene}，设计合理摄像机运动路径。",
            "",
            "[画质要求]",
            "电影级写实，角色和场景视觉特征保持始终一致，运动流畅自然。",
        ]
        return "\n".join(lines)
