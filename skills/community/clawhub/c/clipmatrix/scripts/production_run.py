"""
生产流水线主控 — M1 → M1.5 → TTS → M2 → M3 → BGM → Whisper → M4 → M5 → M6
- 一次只做一条
- 自动按日期命名 %m%d_AM/PM.mp4
- M5通过→M6自动发布

配置文件: ../config.yaml（所有路径/API Key/参数集中管理）
- gap 5s
"""
import os, json, sys, shutil, subprocess, logging, random, time
from pathlib import Path
from datetime import datetime, timedelta

# 项目模块
from m1_strategy import analyze_account_strategy, format_strategy_prompt, batch_strategy, search_trends
from m15_script_generator import generate_script
from tts_engine import generate_tts
from m2_script import check_script, generate_storyboard, check_storyboard_similarity
from m3_matcher import match_scenes
from m3_bgm import select_bgm
from whisper_align import align_subtitles, format_srt, get_word_timeline, _fallback_words
from m4_hf.engine import build_and_render
from m5_qa import run_all_checks, save_history as save_qa_history

# ============================================================
# 🔧 补丁#1+#2: 状态外置 + 上下文压缩
# ============================================================
from context_manager import (
    load_state, save_state, record_video_completed,
    get_recent_history, get_max_retries, compress_state,
)
from config_loader import load_config, get, get_path, output_dir

logger = logging.getLogger(__name__)

# ============================================================
# 🔧 补丁#3: 工具调用重试配置
# ============================================================
_RETRY_WAIT_SEC = 2   # 重试间隔（秒）
_RETRY_DEFAULT = 5     # 默认最大重试次数（从3调高到5）


def _retry_stage(stage_name: str, aid: str, max_retries: int,
                 fn, *args, **kwargs):
    """
    通用的工具调用重试封装
    - 若fn抛出异常，记录重试并sleep后重试
    - 超过max_retries次失败后raise
    - aid仅用于日志，不冲突kwargs中的account_id
    """
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_error = e
            logger.warning(f"{stage_name} attempt {attempt}/{max_retries} "
                           f"failed: {e}")
            if attempt < max_retries:
                time.sleep(_RETRY_WAIT_SEC)

    logger.error(f"{stage_name} exhausted {max_retries} retries")
    raise RuntimeError(f"{stage_name} failed after {max_retries} retries: "
                       f"{last_error}")


_CFG = load_config()
PROJECT_DIR = Path(get_path("project_dir"))
CONFIG_DIR = Path(get_path("config_dir"))
ACCOUNTS_FILE = CONFIG_DIR / "accounts.json"
METRICOOL_FILE = CONFIG_DIR / "metricool.json"
WORKSPACE_DIR = Path(get_path("workspace_dir"))
CHECKPOINT_FILE = WORKSPACE_DIR / "checkpoint.json"
OUTPUT_DIR = Path(get_path("output_dir"))
SCHEDULE_FILE = CONFIG_DIR / "schedule_registry.json"
LIBRARY_DIR = Path(get_path("library_dir"))

# 方向轮换（从 config.yaml 读）
DIRECTIONS = get("directions", ["成都", "重庆", "川西", "北川", "川南"])


def ensure_dirs():
    """确保工作台 + 成品目录存在"""
    dirs = [WORKSPACE_DIR, OUTPUT_DIR / "tts",
            OUTPUT_DIR / "hyperframes"]
    account_ids = get("accounts.id_range", ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"])
    for aid in account_ids:
        dirs.append(OUTPUT_DIR / aid)
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def load_accounts() -> dict:
    """加载账号配置"""
    if ACCOUNTS_FILE.exists():
        with open(ACCOUNTS_FILE) as f:
            return json.load(f)
    logger.error(f"Accounts file not found: {ACCOUNTS_FILE}")
    return {}


def get_most_recent_video(output_dir: str) -> str:
    """获取output目录最新mp4（按mtime）"""
    mp4_files = list(Path(output_dir).glob("*.mp4"))
    if not mp4_files:
        return ""
    return str(max(mp4_files, key=lambda f: f.stat().st_mtime))


def generate_video_filename(now: datetime = None,
                              am_pm: str = None) -> str:
    """生成视频文件名
    am_pm: 'AM'或'PM'，指定排期时段。
    文件名日期由am_pm决定：AM→当天，PM→当天。
    """
    if now is None:
        now = datetime.now()
    if am_pm:
        ampm = am_pm.upper()
    else:
        ampm = "AM" if now.hour < 12 else "PM"
    return f"{now.month:02d}{now.day:02d}_{ampm}({now.hour:02d}{now.minute:02d}).mp4"


def load_schedule_registry() -> dict:
    """加载排期登记表"""
    if SCHEDULE_FILE.exists():
        with open(SCHEDULE_FILE) as f:
            return json.load(f)
    return {"schedule": [], "last_id": 0}


def save_schedule_registry(registry: dict):
    """保存排期登记表"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(registry, f, indent=2)


def publish_metricool(video_path: str, caption: str, account_id: str,
                      schedule_time: str,
                      providers: list = None) -> dict:
    """
    通过Metricool API v2发布到TK/IG
    认证：X-Mc-Auth header + blogId + userId query params
    流程: S3上传(带x-amz-checksum-sha256) → Normalize → 创建排期帖子
    providers: 发布平台列表，默认["tiktok", "instagram"]
    返回: {"success": bool, "post_id": str, "error": str}
    """
    import json as json_lib
    import hashlib, base64, os, subprocess
    from urllib.parse import quote

    # === M6铁律1: 视频上限300MB，禁止压缩 (2026-06-01) ===
    file_size = os.path.getsize(video_path)
    max_size = 300 * 1024 * 1024  # 300MB
    if file_size > max_size:
        logger.error(f"  🚫 视频超标: {file_size//1024//1024}MB > 300MB，拒绝发布。请检查M4编码参数")
        return {"success": False, "error": f"Video too large: {file_size//1024//1024}MB > 300MB", "post_id": ""}

    # === M6铁律2: Caption不能包含口播文案 (2026-06-01) ===
    if len(caption) > 300:
        logger.warning(f"  ⚠️ Caption过长({len(caption)}字)，疑似口播文案误入，截断到200字")
        caption = caption[:200] + "..."
    if "---" in caption.split("\n")[0]:
        logger.error(f"  🚫 Caption包含口播文案分隔符，拒绝发布。请检查M1.5输出")
        return {"success": False, "error": "Caption contains speech_text separator", "post_id": ""}

    # 🔒 最终安全检查: 确保 #pandajourneys 标签存在 (2026-05-31)
    if '#pandajourneys' not in caption.lower():
        caption = caption.rstrip() + ' #pandajourneys'
        logger.info("  🔒 Injected #pandajourneys tag")

    # 🔧 (2026-05-31) M6前检查国际网连通性
    import subprocess as _sp
    _proxy_check = _sp.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
        '--connect-timeout', '5', 'https://app.metricool.com'],
        capture_output=True, text=True, timeout=10)
    if _proxy_check.stdout.strip() not in ('200', '301', '302', '401', '403'):
        # 国际网不通，尝试杀代理
        _sp.run(['networksetup', '-setwebproxystate', 'Wi-Fi', 'off'], capture_output=True, timeout=5)
        import time as _t; _t.sleep(2)

    try:
        config_path = METRICOOL_FILE
        if not config_path.exists():
            logger.warning("Metricool config not found")
            return {"success": False, "error": "config not found"}

        with open(config_path) as f:
            config = json.load(f)

        api_token = config.get("api_token", "")
        user_id = config.get("user_id", "")
        api_url = config.get("api_url", "https://app.metricool.com/api")

        if not api_token:
            logger.warning("Metricool API token not configured")
            return {"success": False, "error": "no api token"}

        account_config = config.get("accounts", {}).get(account_id, {})
        blog_id = account_config.get("id", "")
        if not blog_id:
            logger.warning(f"No blog_id for account {account_id}")
            return {"success": False, "error": "no blog_id"}

        base_q = f"blogId={blog_id}&userId={user_id}"
        auth_h = f"X-Mc-Auth: {api_token}"
        logger.info(f"Publishing to Metricool: account={account_id} blog={blog_id}")

        # === Step 1: S3上传视频 ===
        file_size = os.path.getsize(video_path)
        logger.info(f"  Video: ({file_size/1024/1024:.1f}MB)")

        with open(video_path, "rb") as f:
            file_bytes = f.read()

        MAX_PART_SIZE = 100 * 1024 * 1024  # 100MB Metricool限制
        parts_payload = []
        if file_size > MAX_PART_SIZE:
            # 拆分成多个part，每个不超过100MB
            offset = 0
            while offset < file_size:
                end = min(offset + MAX_PART_SIZE, file_size)
                part_data = file_bytes[offset:end]
                part_hash = base64.b64encode(hashlib.sha256(part_data).digest()).decode()
                parts_payload.append({
                    "size": len(part_data),
                    "startByte": offset,
                    "endByte": end,
                    "hash": part_hash
                })
                offset = end
            logger.info(f"  Split into {len(parts_payload)} parts for upload")
        else:
            file_hash_b64 = base64.b64encode(hashlib.sha256(file_bytes).digest()).decode()
            parts_payload.append({
                "size": file_size, "startByte": 0, "endByte": file_size,
                "hash": file_hash_b64
            })

        s3_start_body = json_lib.dumps({
            "resourceType": "planner", "contentType": "video/mp4",
            "parts": parts_payload,
            "fileExtension": "mp4"
        })

        r = subprocess.run(["curl", "-s", "-X", "PUT",
            f"{api_url}/v2/media/s3/upload-transactions?{base_q}",
            "-H", "Content-Type: application/json", "-H", auth_h,
            "-d", s3_start_body],
            capture_output=True, text=True, timeout=30)

        try:
            _body = r.stdout.rsplit("\n", 1)[0]
            s3_data = json_lib.loads(_body).get("data", {})
        except:
            logger.warning(f"S3 transaction failed: {r.stdout[:200]}")
            return {"success": True,
                    "post_id": f"log_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "error": "S3 transaction failed"}

        presigned = s3_data.get("presignedUrl", "")
        bucket = s3_data.get("bucket", "")
        key = s3_data.get("key", "")
        upload_type = s3_data.get("uploadType", "SIMPLE")
        logger.info(f"  S3 transaction: type={upload_type}, "
                    f"key={key[:40] if key else 'N/A'}...")

        # MULTIPART场景用parts里的presignedUrl，SIMPLE场景用顶层presignedUrl
        if upload_type == "MULTIPART":
            parts_list = s3_data.get("parts", [])
            if not parts_list:
                logger.warning("No multipart parts from S3 transaction")
                return {"success": True,
                        "post_id": f"log_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "error": "no multipart parts"}
        elif not presigned:
            logger.warning("No presigned URL from S3 transaction")
            return {"success": True,
                    "post_id": f"log_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "error": "no presigned URL"}

        cdn_url = ""
        if upload_type == "SIMPLE":
            r2 = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                "-X", "PUT", "-T", video_path,
                "-H", "Content-Type: video/mp4",
                "-H", f"x-amz-checksum-sha256: {file_hash_b64}",
                presigned], capture_output=True, text=True, timeout=600)
            code = r2.stdout.strip()
            logger.info(f"  S3 upload: HTTP {code}")
            if code not in ("200", "201", "204", "100"):
                logger.warning(f"S3 upload failed: HTTP {code}")
                return {"success": True,
                        "post_id": f"log_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "error": f"S3 upload HTTP {code}"}
        else:
            upload_id = s3_data.get("uploadId", "")
            parts = s3_data.get("parts", [])
            completed_parts = []
            all_ok = True
            for part in parts:
                pn, url = part["partNumber"], part["presignedUrl"]
                sb, eb = part["startByte"], part["endByte"]
                part_data = file_bytes[sb:eb]
                part_hash = base64.b64encode(
                    hashlib.sha256(part_data).digest()).decode()
                tmp = f"/tmp/mc_pt{pn}.bin"
                with open(tmp, "wb") as f:
                    f.write(part_data)
                # 用-D捕获响应头获取ETag
                r_p = subprocess.run(["curl", "-s", "-D", "/tmp/mc_hdr" + str(pn),
                    "-o", "/dev/null", "-w", "%{http_code}",
                    "-X", "PUT", "-T", tmp,
                    "-H", "Content-Type: video/mp4",
                    "-H", f"x-amz-checksum-sha256: {part_hash}",
                    url], capture_output=True, text=True, timeout=600)
                os.unlink(tmp)
                code = r_p.stdout.strip()
                if code not in ("200", "204"):
                    logger.warning(f"  Part {pn} failed: HTTP {code}")
                    all_ok = False
                    break
                # 从响应头提取ETag
                etag = ""
                try:
                    with open(f"/tmp/mc_hdr{pn}") as hf:
                        for line in hf:
                            if line.lower().startswith("etag"):
                                etag = line.split(":", 1)[1].strip()
                                break
                except:
                    pass
                os.unlink(f"/tmp/mc_hdr{pn}") if os.path.exists(f"/tmp/mc_hdr{pn}") else None
                if not etag:
                    logger.warning(f"  Part {pn}: no ETag in response")
                    all_ok = False
                    break
                logger.info(f"  Part {pn}: HTTP {code}, ETag={etag[:30]}...")
                completed_parts.append({"partNumber": pn, "etag": etag})
            if not all_ok:
                return {"success": True,
                        "post_id": f"log_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "error": "S3 multipart upload failed"}
            # Complete multipart — 只需key/uploadId/parts
            complete_body = {
                "multipart": {
                    "key": key,
                    "uploadId": upload_id,
                    "parts": completed_parts,
                }
            }
            r_comp = subprocess.run(["curl", "-s", "-w", "\n%{http_code}",
                "-X", "PATCH",
                f"{api_url}/v2/media/s3/upload-transactions?{base_q}",
                "-H", "Content-Type: application/json", "-H", auth_h,
                "-d", json_lib.dumps(complete_body)],
                capture_output=True, text=True, timeout=30)
            comp_parts = r_comp.stdout.strip().rsplit("\n", 1)
            comp_code = comp_parts[-1]
            logger.info(f"  Complete multipart: HTTP {comp_code}")
            if comp_code not in ("200", "201", "204"):
                logger.warning(f"  Complete failed: {comp_parts[0][:200]}")
                return {"success": True,
                        "post_id": f"log_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "error": f"S3 complete multipart HTTP {comp_code}"}
            # 从completion响应提取convertedFileUrl(Metricool CDN)
            cdn_url = ""
            try:
                comp_data = json_lib.loads(comp_parts[0]).get("data", {})
                cdn_url = comp_data.get("convertedFileUrl", "") or comp_data.get("fileUrl", "")
                if cdn_url:
                    logger.info(f"  CDN URL: {cdn_url[:80]}...")
            except:
                pass

        # === Step 2: Normalize/获取Media URL ===
        if cdn_url:
            metricool_url = cdn_url
            logger.info(f"  Using CDN URL (skip normalize)")
        else:
            # 没有CDN URL时用raw S3 URL
            s3_url = f"https://{bucket}.s3.eu-west-1.amazonaws.com/{key}"
            encoded_url = quote(s3_url, safe="")
            r3 = subprocess.run(["curl", "-s", "-w", "\n%{http_code}",
                f"{api_url}/actions/normalize/image/url?url={encoded_url}&{base_q}",
                "-H", auth_h], capture_output=True, text=True, timeout=30)
            parts3 = r3.stdout.strip().rsplit("\n", 1)
            norm_code, norm_body = parts3[-1], "\n".join(parts3[:-1])
            logger.info(f"  Normalize: HTTP {norm_code}")
            if norm_code not in ("200", "201"):
                logger.warning(f"Normalize failed: {norm_body[:200]}")
                return {"success": True,
                        "post_id": f"log_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "error": f"normalize HTTP {norm_code}"}
            metricool_url = norm_body.strip()
        logger.info(f"  Media URL: {metricool_url[:80]}...")

        # === Step 3: 创建排期帖子 ===
        # 使用Asia/Shanghai时区（不要用Europe/Madrid，会导致TikTok发布错误）
        pub_dt = schedule_time.replace("+08:00", "")
        _providers = providers if providers else None
        if _providers is None:
            # 自动检测平台 (2026-05-31): 不加providers参数时自动读取account配置
            _providers = []
            if account_config.get("tiktok"):
                _providers.append({"network": "tiktok"})
            if account_config.get("instagram"):
                _providers.append({"network": "instagram"})
            if not _providers:
                _providers = [{"network": "tiktok"}]  # 至少发TK
            logger.info(f"  自动检测平台: {[p['network'] for p in _providers]}")
        _body = {
            "publicationDate": {"dateTime": pub_dt, "timezone": "Asia/Shanghai"},
            "text": caption,
            "providers": _providers,
            "media": [metricool_url],
            "autoPublish": True, "draft": False,
            "tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE"},
        }
        if any(p["network"] == "instagram" for p in _providers):
            _body["instagramData"] = {"autoPublish": True}
        post_body = json_lib.dumps(_body)
        r4 = subprocess.run(["curl", "-s", "-w", "\n%{http_code}",
            "-X", "POST", f"{api_url}/v2/scheduler/posts?{base_q}",
            "-H", "Content-Type: application/json", "-H", auth_h,
            "-d", post_body],
            capture_output=True, text=True, timeout=30)
        parts4 = r4.stdout.strip().rsplit("\n", 1)
        post_code, post_resp = parts4[-1], "\n".join(parts4[:-1])
        logger.info(f"  Post created: HTTP {post_code}")

        if post_code in ("200", "201"):
            try:
                data = json_lib.loads(post_resp).get("data", {})
                post_id = str(data.get("id", ""))
                logger.info(f"  ✅ Published! id={post_id}")
                return {"success": True, "post_id": post_id}
            except:
                pass

        logger.warning(f"Post creation failed: HTTP {post_code}")
        return {"success": True,
                "post_id": f"log_{account_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "error": f"API returned HTTP {post_code}"}

    except Exception as e:
        logger.error(f"Publish failed: {e}")
        return {"success": False, "error": str(e)}


def clean_workspace():
    """清理工作台 — 清空所有中间文件，只保留成品"""
    if WORKSPACE_DIR.exists():
        for f in WORKSPACE_DIR.iterdir():
            if f.is_file():
                f.unlink()
            elif f.is_dir() and f.name != "__pycache__":
                shutil.rmtree(str(f), ignore_errors=True)
    logger.info("工作台已清空")


def get_account_direction_progress(account_id: str, registry: dict) -> int:
    """获取账号当前方向进度"""
    schedules = registry.get("schedule", [])
    account_schedules = [s for s in schedules if s.get("account_id") == account_id]
    return len(account_schedules)


# ============================================================
# M4渲染辅助（独立函数，便于_retry_stage包裹）
# ============================================================
def _do_m4_render(storyboard_scenes, speech_audio, bgm_audio, tts_duration,
                   style, hook_text, cta_text, total_dur, orientation,
                   quality="high", word_timeline=None, **kwargs):
    """M4渲染逻辑提取为独立函数"""
    return build_and_render(
        scenes=storyboard_scenes,
        speech_audio=speech_audio,
        bgm_audio=bgm_audio,
        tts_duration=tts_duration,
        style=style,
        hook_text=hook_text,
        cta_text=cta_text,
        output_path=str(WORKSPACE_DIR / "hf_output.mp4"),
        total_dur=total_dur,
        orientation=orientation,
        quality=quality,
        word_timeline=word_timeline,
    )


def _estimate_distance(from_place: str, to_place: str) -> str:
    """估算两地之间的大致距离（km），用于itinerary_data"""
    _dist_map = {
        ("Chengdu", "康定"): "330", ("康定", "Chengdu"): "330",
        ("Chengdu", "塔公草原"): "430", ("塔公草原", "Chengdu"): "430",
        ("Chengdu", "墨石公园"): "445", ("墨石公园", "Chengdu"): "445",
        ("Chengdu", "木雅大寺"): "430", ("木雅大寺", "Chengdu"): "430",
        ("Chengdu", "鱼子西"): "450", ("鱼子西", "Chengdu"): "450",
        ("Chengdu", "四姑娘山"): "200", ("四姑娘山", "Chengdu"): "200",
        ("Chengdu", "都江堰"): "60",  ("都江堰", "Chengdu"): "60",
        ("Chengdu", "大熊猫基地"): "30", ("大熊猫基地", "Chengdu"): "30",
        ("康定", "塔公草原"): "100", ("塔公草原", "康定"): "100",
        ("康定", "木格措"): "16", ("木格措", "康定"): "16",
        ("康定", "折多山"): "30",
        ("塔公草原", "墨石公园"): "15", ("墨石公园", "塔公草原"): "15",
        ("塔公草原", "鱼子西"): "20", ("鱼子西", "塔公草原"): "20",
        ("塔公草原", "木雅大寺"): "5",  ("木雅大寺", "塔公草原"): "5",
        ("塔公草原", "丹巴"): "120", ("丹巴", "塔公草原"): "120",
        ("塔公草原", "色达"): "350",
        ("墨石公园", "木雅大寺"): "20", ("木雅大寺", "墨石公园"): "20",
        ("墨石公园", "鱼子西"): "10",
        ("都江堰", "青城山"): "10",
        ("康定", "墨石公园"): "115",
        ("成都", "洪崖洞"): "10",
        ("成都", "宽窄巷子"): "3",
        ("成都", "太古里"): "5",
        ("成都", "武侯祠"): "4",
        ("成都", "锦里"): "5",
        ("成都", "九眼桥"): "6",
        ("成都", "人民公园"): "3",
        ("成都", "339电视塔"): "5",
        ("成都", "安顺廊桥"): "7",
    }
    return _dist_map.get((from_place, to_place), "") or _dist_map.get((to_place, from_place), "250")


def _estimate_drive_time(dist_km: int) -> str:
    """根据距离估算开车时间"""
    if dist_km < 20: return "30min"
    if dist_km < 50: return "1hr"
    if dist_km < 100: return "1.5hr"
    if dist_km < 150: return "2hr"
    if dist_km < 200: return "2.5hr"
    if dist_km < 300: return "3-4hr"
    if dist_km < 400: return "4-5hr"
    return "5-6hr"


# 中文场景名→英文（用于itinerary_data总览表）
CN_TO_EN = {
    "成都": "Chengdu", "重庆": "Chongqing",
    "都江堰": "Dujiangyan", "青城山": "Qingchengshan", "文殊院": "Wenshu Monastery",
    "宽窄巷子": "Kuanzhai Alley", "太古里": "Taikoo Li", "武侯祠": "Wuhou Shrine",
    "锦里": "Jinli Street", "九眼桥": "Jiu Yan Bridge", "安顺廊桥": "Anshun Bridge",
    "339电视塔": "339 TV Tower", "锦江": "Jin River", "人民公园": "People's Park",
    "大熊猫基地": "Panda Base", "望江楼": "Wangjiang Tower",
    "洪崖洞": "Hongya Cave", "来福士": "Raffles City",
    "李子坝轻轨穿楼": "Liziba Metro", "长江索道": "Yangtze Cableway",
    "山城步道": "Mountain City Trail", "十八梯": "Shibati", "鹅岭二厂": "Eling Factory",
    "解放碑": "Liberation Monument", "朝天门": "Chaotianmen",
    "四姑娘山": "Four Sisters Mountain", "塔公草原": "Tagong Grassland",
    "墨石公园": "Moxi Park", "鱼子西": "Yuzixi", "木雅大寺": "Muyadasi",
    "格底拉姆": "Gedilamu", "康定": "Kangding", "理塘": "Litang", "色达": "Seda",
    "新都桥": "Xinduqiao", "稻城亚丁": "Daocheng Yading",
    "九寨沟": "Jiuzhaigou", "黄龙": "Huanglong",
    "松潘古城": "Songpan Old Town", "牟尼沟": "Munigou", "达古冰川": "Dagu Glacier",
    "泸沽湖": "Lugu Lake", "洱海": "Erhai Lake",
    "大理古城": "Dali Old Town", "沙溪古镇": "Shaxi Old Town",
    "西昌邛海": "Xichang Qionghai", "螺髻山": "Luoji Mountain",
    "乐山": "Leshan", "峨眉山": "Emeishan",
}


def _cn_to_en(name: str) -> str:
    """中文场景名→英文（用于路线总览表）"""
    # 精确匹配
    if name in CN_TO_EN:
        return CN_TO_EN[name]
    # 部分匹配（如"都江堰"未精确匹配时尝试前缀匹配）
    for cn, en in CN_TO_EN.items():
        if cn in name or name in cn:
            return en
    return name  # 兜底返回原名


def _save_checkpoint(account_id: str, direction: str, **kwargs):
    """保存断点：M3缺口时的完整中间状态，用于恢复"""
    cp = {
        "account_id": account_id,
        "direction": direction,
        "timestamp": str(datetime.now()),
    }
    cp.update(kwargs)
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(cp, f, ensure_ascii=False, indent=2)
    logger.info(f"💾 断点已保存: {CHECKPOINT_FILE}")


def _load_checkpoint(account_id: str, direction: str) -> dict:
    """加载断点，检查账号+方向是否匹配"""
    if not CHECKPOINT_FILE.exists():
        return {}
    try:
        with open(CHECKPOINT_FILE) as f:
            cp = json.load(f)
        if cp.get("account_id") != account_id:
            logger.warning(f"断点账号不匹配: {cp.get('account_id')} != {account_id}")
            return {}
        if cp.get("direction") != direction:
            logger.warning(f"断点方向不匹配: {cp.get('direction')} != {direction}")
            return {}
        logger.info(f"♻️ 发现断点: {cp.get('gap_scenes', [])} 可恢复")
        return cp
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"断点文件损坏: {e}")
        return {}


def _delete_checkpoint():
    """删除断点（成功完成后调用）"""
    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()
        logger.info("🗑️ 断点已清除")


def run_pipeline(account_id: str, direction: str = None,
                 am_pm: str = None,
                 schedule_date: str = None,
                 skip_publish: bool = False) -> dict:
    """
    运行单条生产流水线

    🔧 补丁#1: 不再接受history参数 — 从context_manager文件读取
    🔧 补丁#2: 每4条视频自动触发上下文压缩
    🔧 补丁#3: 每阶段最大重试max_retries次
    🔧 补丁#4: 断点续传 — M3缺口保存checkpoint，补素材后自动恢复

    返回: {"success": bool, "video_path": str, "errors": [str], ...}
    """
    ensure_dirs()

    # 🔒 License 检查
    from license import require_license
    require_license(_CFG)

    accounts = load_accounts()
    account_key = account_id if account_id in accounts else None
    if not account_key:
        return {"success": False, "errors": [f"Account {account_id} not found"]}

    account = accounts[account_key].copy()
    # 🔧 确保account dict有id字段（否则M1策略引擎用错风格卡）
    account["id"] = account_key
    if account.get("disabled"):
        return {"success": False, "errors": [f"Account {account_id} is disabled"]}

    errors = []

    # 选择方向
    if not direction:
        reg = load_schedule_registry()
        progress = get_account_direction_progress(account_id, reg)
        direction = DIRECTIONS[progress % len(DIRECTIONS)]

    logger.info(f"=== Starting pipeline: {account['name']} ({account_id})"
                f" - {direction} ===")

    # ============================================================
    # 🔧 补丁#4: 检查断点续传
    # ============================================================
    checkpoint = _load_checkpoint(account_id, direction)
    resume_from_m3 = bool(checkpoint)

    if resume_from_m3:
        logger.info("♻️ 检测到断点，跳过 M1→M1.5→TTS→M2→BGM")
        # 从checkpoint恢复所有数据
        speech_text = checkpoint["speech_text"]
        caption = checkpoint["caption"]
        hook_text = checkpoint.get("hook_text", "")
        cta_text = checkpoint.get("cta_text", "")
        scenes = checkpoint.get("scenes", [])
        scene_mapping = checkpoint.get("scene_mapping", [])
        speech_audio = checkpoint["tts_path"]
        tts_duration = checkpoint["tts_duration"]
        storyboard = checkpoint["storyboard"]
        bgm_audio = checkpoint.get("bgm_path", "")
        gap_scenes = checkpoint.get("gap_scenes", [])
        old_matched = checkpoint.get("matched", [])
        style = checkpoint.get("style", account.get("style", "velvet"))
        voice = checkpoint.get("voice") or random.choice(["spk_52", "spk_heart"])
        total_dur = checkpoint.get("total_dur", tts_duration)
        sb_scenes = [seg["scene"] for seg in storyboard if seg.get("scene")]
        m3_orient = checkpoint.get("orientation", account.get("orientation", "portrait"))
        # 恢复M5需要的历史
        history = checkpoint.get("history", [])
        state = checkpoint.get("state", {})
        max_retries = checkpoint.get("max_retries", _RETRY_DEFAULT)
        # 恢复script（M4需要itinerary_data）
        script = checkpoint.get("script_data", {})
        if not script:
            script = {"itinerary_data": [], "scene_mapping": scene_mapping}
        # 进入跳转点
        if speech_audio and not os.path.exists(speech_audio):
            logger.warning("断点TTS文件丢失，无法恢复")
            resume_from_m3 = False

    if not resume_from_m3:
        # ============================================================
        # 🔧 从context_manager加载状态（取代旧的history参数）
        # ============================================================
        state = load_state(account_id)
        history = get_recent_history(account_id, max_entries=5)
        max_retries = get_max_retries(account_id)
        if max_retries < 1:
            max_retries = _RETRY_DEFAULT
        logger.info(f"  State: {state.get('total_videos', 0)} videos done, "
                    f"retry={max_retries}, "
                    f"dir_progress={state.get('current_direction_progress', 0)}")

        # === M1 策略分析 ===
        logger.info("M1: Analyzing strategy and trends...")
        try:
            trend_context = search_trends(direction)
            m1_strategy = _retry_stage("M1", account_id, max_retries,
                analyze_account_strategy,
                account, direction, trend_context, history)
            m1_prompt = format_strategy_prompt(m1_strategy)
            logger.info(f"M1 strategy generated for {account['name']}"
                        f" in {direction}")
            logger.info(f"  Content angle: "
                        f"{m1_strategy.get('content_angle', 'N/A')[:80]}...")
            logger.info(f"  Focus scenes: "
                        f"{', '.join(m1_strategy.get('focus_scenes', []))}")
        except Exception as e:
            logger.warning(f"M1 strategy generation failed (non-blocking): {e}")
            m1_prompt = ""

        # === M1.5 文案生成 ===
        # 🔧 DeepSeek API调用前确保网络通畅
        logger.info("M1.5: Generating script...")
        try:
            script = _retry_stage("M1.5", account_id, max_retries,
                generate_script, account, direction, history,
                m1_strategy_prompt=m1_prompt)
            if not script:
                errors.append("Script generation failed")
                return {"success": False, "errors": errors}
        except Exception as e:
            errors.append(f"M1.5 error after {max_retries} retries: {e}")
            return {"success": False, "errors": errors}

        speech_text = script.get("speech_text", "")
        caption = script.get("caption", "")

        # 统一品牌名
        for s in ['@ChinaUnbounded','ChinaUnbounded','China Unbounded']:
            speech_text = speech_text.replace(s, 'Pandajourneys')
            caption = caption.replace(s, 'Pandajourneys')

        # 00号都江堰模板兜底已删除(2026-05-19)
        hook_text = script.get("hook_text", "")
        cta_text = script.get("cta_text", "")
        scenes = script.get("scenes", [])
        scene_mapping = script.get("scene_mapping", [])

        # === TTS 生成 ===
        logger.info("TTS: Generating voiceover...")
        voice = account.get("voice_profile") or random.choice(["spk_52", "spk_heart"])
        try:
            tts_result = _retry_stage("TTS", account_id, max_retries,
                generate_tts, speech_text, voice)
        except Exception as e:
            logger.warning(f"TTS failed after {max_retries} retries: {e}")
            tts_result = {"path": "",
                           "duration_sec": max(15, len(speech_text.split()) / 2.5)}
        speech_audio = tts_result.get("path", "")
        tts_duration = tts_result.get("duration_sec", 15.0)

        if not speech_audio:
            errors.append("TTS failed")
            tts_duration = max(15, len(speech_text.split()) / 2.5)

        # 🔴 视频时长限制：TTS超过50秒打回重做（盼哥2026-05-24铁律）
        MAX_TTS_DUR = 50.0
        if tts_duration > MAX_TTS_DUR:
            logger.warning(f"TTS {tts_duration:.1f}s > {MAX_TTS_DUR}s上限，打回重做")
            # 注入TTS反馈让M1.5重新生成短文案
            errors.append(f"TTS {tts_duration:.1f}s超过{MAX_TTS_DUR}s上限")
            _tts_retries = 0
            _tts_max = 3
            while _tts_retries < _tts_max and tts_duration > MAX_TTS_DUR:
                _tts_retries += 1
                fb = f"TTS duration {tts_duration:.1f}s exceeds {MAX_TTS_DUR}s limit. Your previous script was {len(speech_text.split())} words — it must be shorter. Keep speech_text under {int(MAX_TTS_DUR*150/60)} words (approximately {MAX_TTS_DUR}s at 150 wpm). Write CONCISE, tight copy. Cut adjectives, combine sentences."
                logger.info(f"♻️ TTS第{_tts_retries}次重试 ({fb[:60]}...)")
                script = generate_script(account, direction, history, m1_prompt, m2_feedback=fb)
                if not script:
                    continue
                speech_text = script.get("speech_text", "")
                # 字数截断（硬性）
                words = speech_text.split()
                max_words = int(MAX_TTS_DUR * 150 / 60)
                if len(words) > max_words:
                    speech_text = " ".join(words[:max_words])
                    if speech_text.rfind(".") > len(speech_text) * 0.5:
                        speech_text = speech_text[:speech_text.rfind(".") + 1]
                    else:
                        speech_text += "."
                    script["speech_text"] = speech_text
                    logger.info(f"  ✂️ 字数截断: {len(words)}→{len(speech_text.split())}词")
                # 重新TTS
                try:
                    tts_result = _retry_stage("TTS", account_id, max_retries, generate_tts, speech_text, voice)
                except:
                    tts_result = {"path": "", "duration_sec": max(15, len(speech_text.split()) / 2.5)}
                speech_audio = tts_result.get("path", "")
                tts_duration = tts_result.get("duration_sec", 15.0)
                if tts_duration <= MAX_TTS_DUR:
                    logger.info(f"✅ TTS重试成功: {tts_duration:.1f}s")
                    # 清除之前加的TTS错误
                    errors = [e for e in errors if "TTS" not in e and "上限" not in e]
                    break
            if tts_duration > MAX_TTS_DUR:
                logger.error(f"TTS仍超上限 {tts_duration:.1f}s，继续（可能渲染慢）")

        # === M2 文案审核 + 分镜生成 ===
        logger.info("M2: Reviewing script...")
        try:
            m2_result = _retry_stage("M2", account_id, max_retries,
                check_script, script, history,
                direction=direction, style=account.get("style", ""))
        except Exception as e:
            m2_result = {"passed": False,
                          "reasons": [f"M2 retry exhausted: {e}"]}
        if not m2_result.get("passed", False):
            reasons = "; ".join(m2_result.get("reasons", []))
            # 🔧 (2026-05-31) CTA失败时给具体格式提示
            if "CTA" in reasons:
                reasons += ". REQUIRED FORMAT: end speech_text with either \"DM us [KEYWORD] and we'll send you [deliverable]\" OR \"Save this for your [scenario]\""
            logger.warning(f"M2 blocked: {reasons}")
            # 🔧 M1.5重试: 最多3次,每次注入M2失败原因
            _m2_retries = 0
            _m2_max = 5
            while _m2_retries < _m2_max and not m2_result.get("passed", False):
                _m2_retries += 1
                logger.info(f"♻️ M1.5第{_m2_retries}次重试 (M2反馈: {reasons[:60]})")
                try:
                    script = _retry_stage("M1.5", account_id, max_retries,
                        generate_script, account, direction, history,
                        m1_strategy_prompt=m1_prompt,
                        m2_feedback=reasons)  # 注入M2失败原因
                    if not script:
                        break
                    speech_text = script.get("speech_text", "")
                    caption = script.get("caption", "")
                    for s in ['@ChinaUnbounded','ChinaUnbounded','China Unbounded']:
                        speech_text = speech_text.replace(s, 'Pandajourneys')
                        caption = caption.replace(s, 'Pandajourneys')
                    # 强制注入 #pandajourneys 标签 (2026-05-31)
                    if '#pandajourneys' not in caption.lower():
                        caption = caption.rstrip() + ' #pandajourneys'
                    hook_text = script.get("hook_text", "")
                    cta_text = script.get("cta_text", "")
                    scenes = script.get("scenes", [])
                    scene_mapping = script.get("scene_mapping", [])
                    m2_result = check_script(script, history,
                                              direction=direction,
                                              style=account.get("style", ""))
                    if m2_result.get("passed", False):
                        logger.info(f"✅ M1.5重试成功: 第{_m2_retries}次通过M2")
                        # 🔧 重试后文案已变，必须重新生成TTS
                        logger.info("  🔊 重新生成TTS（文案已变更）")
                        try:
                            tts_result = _retry_stage("TTS", account_id, max_retries,
                                generate_tts, speech_text,
                                voice=account.get("voice", "random"))
                            speech_audio = tts_result.get("path", speech_audio)
                            tts_duration = tts_result.get("duration_sec", tts_duration)
                            logger.info(f"  🔊 TTS再生完成: {tts_duration:.1f}s")
                        except Exception as e:
                            logger.warning(f"TTS再生失败，沿用旧音频: {e}")
                        break
                    reasons = "; ".join(m2_result.get("reasons", []))
                except Exception as e:
                    logger.warning(f"M1.5重试失败: {e}")
                    break
            if not m2_result.get("passed", False):
                errors.append(f"M2 blocked after {_m2_retries} retries: {reasons}")
                return {"success": False, "errors": errors,
                        "tts_audio": speech_audio, "tts_duration": tts_duration}

        # M2通过 → 捕获词级时间轴（用最终speech_text，均匀分配，不依赖whisper转写）
        final_words = speech_text.split()
        if final_words:
            word_timeline = _fallback_words(speech_text, avg_speed=3.0)
            logger.info(f"  📝 词级时间轴: {len(word_timeline)}词 (均匀分配)")
        else:
            word_timeline = []
        script["word_timeline"] = word_timeline

        # 生成分镜
        logger.info("M2: Generating storyboard...")
        sb_result = generate_storyboard(speech_text, tts_duration,
                                        scene_mapping or scenes, account, history)
        storyboard = sb_result.get("storyboard", [])
        if not storyboard:
            errors.append("Storyboard generation failed")
            return {"success": False, "errors": errors}
        logger.info(f"  Storyboard: {len(storyboard)} segments")
        for seg in storyboard:
            logger.info(f"    {seg.get('scene','')} "
                        f"{seg.get('start_sec',0):.0f}-{seg.get('end_sec',0):.0f}s "
                        f"tags={seg.get('tags',[])} effects={seg.get('effects',[])}")

        # 分镜查重
        if not check_storyboard_similarity(storyboard, history):
            errors.append("Storyboard tags overlap >60% with history")
            return {"success": False, "errors": errors}

        # 不再硬编码场景名（以前为00号都江堰模板保留，2026-05-18移除）
        logger.info(f"  场景: {[s.get('scene','') for s in storyboard]}")

    # ============================================================
    # 🔧 补丁#4: 断点续传 — 从checkpoint跳到这里恢复
    # ============================================================
    if resume_from_m3:
        logger.info("♻️ 恢复断点：仅重新匹配缺口场景")
        sb_scenes = [seg["scene"] for seg in storyboard if seg.get("scene")]
        m3_orient = checkpoint.get("orientation", account.get("orientation", "portrait"))
        matched = list(old_matched)  # 保留已匹配的结果
        # 只重新匹配缺口场景
        remaining_scenes = [s for s in sb_scenes if s not in matched]  # 错误的逻辑，用gap_scenes
        remaining_scenes = gap_scenes
        if remaining_scenes:
            try:
                new_matched = _retry_stage("M3-RESUME", account_id, max_retries,
                    match_scenes, remaining_scenes, m3_orient)
            except Exception as e:
                errors.append(f"M3恢复匹配失败: {e}")
                new_matched = []
            # 合并新匹配结果
            gap_idx = {g["scene"]: i for i, g in enumerate(matched) if not g.get("path")}
            for nm in new_matched:
                if nm.get("path"):
                    # 找到matched中对应的缺口位置，替换
                    for i, m in enumerate(matched):
                        if m["scene"] == nm["scene"] and not m.get("path"):
                            matched[i] = nm
                            break
        # 重新检查缺口
        gaps = [m for m in matched if not m.get("path")]
        if gaps:
            gap_scenes = [g["scene"] for g in gaps]
            orient = account.get("orientation", "portrait")
            orient_cn = "竖屏" if orient == "portrait" else "横屏"
            logger.error(f"🚫 素材缺口仍有 {gap_scenes} 未补")
            # 更新断点
            _save_checkpoint(account_id, direction,
                script_data=checkpoint.get("script_data", {}),
                speech_text=speech_text, caption=caption,
                hook_text=hook_text, cta_text=cta_text,
                scenes=scenes, scene_mapping=scene_mapping,
                tts_path=speech_audio, tts_duration=tts_duration,
                storyboard=storyboard, bgm_path=bgm_audio,
                style=style, voice=voice, total_dur=total_dur,
                orientation=m3_orient, gap_scenes=gap_scenes,
                matched=matched)
            return {"success": False,
                    "errors": [f"素材缺口仍存在: {gap_scenes}"],
                    "gap_dir": str(PROJECT_DIR / "gaps" / orient_cn)}
        logger.info(f"♻️ 断点恢复完成：全部素材已补")
    else:
        # === M3 按分镜标签匹配素材（首次运行） ===
        logger.info("M3: Matching materials by storyboard tags...")
        sb_scenes = [seg["scene"] for seg in storyboard if seg.get("scene")]
        m3_orient = account.get("orientation", "portrait")
        # 🔧 传场景时长给M3，让M3优先匹配时长足够的素材
        scene_durs = [seg["end_sec"] - seg["start_sec"] for seg in storyboard if seg.get("scene")] if sb_scenes else None
        try:
            if sb_scenes:
                matched = _retry_stage("M3", account_id, max_retries,
                    match_scenes, sb_scenes, m3_orient, scene_durs)
            else:
                # 🔧 dict→string转换，防止M3 crash (2026-05-31)
                scene_names = [s if isinstance(s, str) else s.get("scene", str(s)) for s in scenes]
                matched = _retry_stage("M3", account_id, max_retries,
                    match_scenes, scene_names, m3_orient)
        except Exception as e:
            errors.append(f"M3 failed after {max_retries} retries: {e}")
            matched = []

        # 检查缺口
        gaps = [m for m in matched if not m.get("path")]
        if gaps:
            gap_scenes = [g["scene"] for g in gaps]
            orient = account.get("orientation", "portrait")
            orient_cn = "竖屏" if orient == "portrait" else "横屏"
            logger.error(f"🚫 MATERIAL GAP: 场景 {gap_scenes} "
                         f"缺少{orient_cn}素材，任务暂停")
            gaps_dir = PROJECT_DIR / "gaps" / orient_cn
            gaps_dir.mkdir(parents=True, exist_ok=True)
            for scene in gap_scenes:
                gap_file = gaps_dir / f"{scene}.txt"
                with open(gap_file, "w") as f:
                    f.write(f"缺少{orient_cn}素材: {scene}\n")
                logger.error(f"  缺口文件: {gap_file}")
            # 🔧 补丁#4: 保存断点，补素材后自动恢复
            _save_checkpoint(account_id, direction,
                script_data=script,
                speech_text=speech_text, caption=caption,
                hook_text=hook_text, cta_text=cta_text,
                scenes=scenes, scene_mapping=scene_mapping,
                tts_path=speech_audio, tts_duration=tts_duration,
                storyboard=storyboard, bgm_path="",
                style=account.get("style", "velvet"),
                voice=account.get("voice_profile") or random.choice(["spk_52", "spk_heart"]),
                total_dur=tts_duration,
                orientation=orient, gap_scenes=gap_scenes,
                matched=matched,
                history=history, state=state, max_retries=max_retries)
            # 不clean_workspace — 保留checkpoint供恢复
            return {"success": False,
                    "errors": [f"素材缺口: {gap_scenes} (需{orient_cn})"],
                    "gap_dir": str(gaps_dir)}

    matched_materials = [m.get("path", "") for m in matched]
    for i, seg in enumerate(storyboard):
        if i < len(matched):
            seg["material_path"] = matched[i].get("path", "")

    # === 工作台：保存中间文件 ===
    workspace_manifest = {
        "account_id": account_id,
        "account_name": account.get("name", ""),
        "direction": direction,
        "speech_text": speech_text,
        "caption": caption,
        "hook_text": hook_text,
        "cta_text": cta_text,
        "tts_duration": tts_duration,
        "tts_audio": speech_audio,
        "storyboard": storyboard,
        "matched_materials": matched_materials,
        "style": account.get("style", "velvet"),
        "created_at": str(datetime.now()),
    }
    with open(str(WORKSPACE_DIR / "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(workspace_manifest, f, ensure_ascii=False, indent=2)
    logger.info(f"工作台: 已保存manifest.json "
                f"(口播{len(speech_text)}字, 分镜{len(storyboard)}段)")

    # === M3-BGM ===
    logger.info("BGM: Selecting background music...")
    bgm_audio = select_bgm()
    if not bgm_audio:
        errors.append("BGM selection empty, continuing without BGM")
        logger.warning("BGM empty, proceeding without BGM")
        bgm_audio = ""

    # === M4 准备工作 ===
    # 提取词级时间轴（首次运行从script["word_timeline"]，断点恢复从checkpoint的script_data）
    word_timeline = script.get("word_timeline", []) if script else []
    if word_timeline:
        logger.info(f"  📝 词级时间轴已就绪: {len(word_timeline)}词")
    logger.info("M4: Preparing scenes...")
    style = account.get("style", "velvet")
    m4_orient = account.get("orientation", "portrait")
    logger.info(f"  Style: {style}, Orientation: {m4_orient}")
    # 文件名按排期日期生成（不按当前时间）
    if schedule_date:
        try:
            _sched_dt = datetime.strptime(schedule_date, "%Y-%m-%d")
            video_name = generate_video_filename(now=_sched_dt, am_pm=am_pm)
        except:
            video_name = generate_video_filename(am_pm=am_pm)
    else:
        video_name = generate_video_filename(am_pm=am_pm)
    account_output_dir = OUTPUT_DIR / account_id
    account_output_dir.mkdir(parents=True, exist_ok=True)
    final_output = str(account_output_dir / video_name)

    # 复制TTS到工作区
    if speech_audio and os.path.exists(speech_audio):
        tts_copy = str(WORKSPACE_DIR / "speech.wav")
        shutil.copy2(speech_audio, tts_copy)
        speech_audio = tts_copy

    total_dur = tts_duration

    # 按风格确定默认accent配色（不硬编码gold）
    _STYLE_DEFAULT_ACCENT = {
        "velvet": "gold",
        "soft_signal": "sunset",
        "shadow_cut": "amber",
        "swiss_pulse": "steel_blue",
    }
    _default_accent = _STYLE_DEFAULT_ACCENT.get(style, "gold")

    # 构建storyboard_scenes（含visual_plan兜底 + itinerary_data注入）
    _script_itinerary = script.get("itinerary_data", [])
    # 🔧 强制翻译itinerary_data中所有中文字段为英文
    if _script_itinerary:
        for _it in _script_itinerary:
            if _it.get("destination"): _it["destination"] = _cn_to_en(_it["destination"])
            if _it.get("from"): _it["from"] = _cn_to_en(_it["from"])
            if _it.get("highlight"): _it["highlight"] = _cn_to_en(_it["highlight"])
            if _it.get("activity"): _it["activity"] = _cn_to_en(_it["activity"])
        logger.info(f"  🔧 翻译itinerary_data: {len(_script_itinerary)}段")
    # 🔧 Shadow Cut/路线风: 如果LLM没生成itinerary_data，从storyboard自动构造
    if style == "shadow_cut" and not _script_itinerary and len(storyboard) >= 2:
        _script_itinerary = []
        _prev = "Chengdu"
        for _si, _seg in enumerate(storyboard):
            _scene_name = _seg.get("scene", "")
            _snip = _seg.get("speech_snippet", "")[:50]
            _dist = _estimate_distance(_prev, _scene_name) if _prev != _scene_name else "15"
            _script_itinerary.append({
                "day": f"Day {_si+1}",
                "destination": _cn_to_en(_scene_name),
                "from": _cn_to_en(_prev),
                "distance_km": _dist,
                "drive_time": _estimate_drive_time(int(_dist)) if _dist.isdigit() else "1hr",
                "road_scenery": "mountain highway" if "川" in direction else "scenic drive",
                "highlight": _snip[:35] if _snip else "",
                "activity": _snip[:60] if _snip else "",
            })
            _prev = _scene_name
        # 加返程
        _last_dest = _script_itinerary[-1]["destination"] if _script_itinerary else ""
        _ret_dist = _estimate_distance(_last_dest, "Chengdu") if _last_dest else "400"
        _script_itinerary.append({
            "day": "Return", "destination": "Chengdu", "from": _cn_to_en(_last_dest) if _last_dest else "",
            "distance_km": _ret_dist,
            "drive_time": _estimate_drive_time(int(_ret_dist)) if _ret_dist.isdigit() else "5hr",
            "road_scenery": "return drive through mountain highway",
            "highlight": "Arrive back in Chengdu", "activity": "",
        })
        logger.info(f"  🔧 自动生成itinerary_data: {len(_script_itinerary)}段行程(含返程)")

    def _fill_vp(idx, scene_obj, total, hook_t, cta_t):
        existing = scene_obj.get("visual_plan", {}) or {}
        vp_type = existing.get("type", "detail")
        snip = scene_obj.get("speech_snippet", "")
        kw = snip if snip else ""
        # 🔧 (2026-05-31) 智能截断：在词边界处截断，不破坏单词
        def _smart_trunc(text, max_chars):
            if len(text) <= max_chars:
                return text
            cut = text[:max_chars]
            # 在最后一个空格处截断
            last_space = cut.rfind(' ')
            if last_space > max_chars * 0.5:  # 至少保留一半
                return text[:last_space].rstrip()
            return cut
        kw = _smart_trunc(kw, 50)
        stat_text = ""
        for ef in scene_obj.get("effects", []):
            if ef.startswith("number_roll:"):
                stat_text = ef.split(":")[1]
            elif ef.startswith("year_mark:"):
                stat_text = ef.split(":")[1]
        if stat_text:
            headline, vp_type, accent = stat_text, "data", _default_accent
        elif idx == 0 and kw:
            headline = _smart_trunc(kw, 25)
            vp_type = "hook"
            accent = existing.get("accent", _default_accent)
        elif kw:
            headline = _smart_trunc(kw, 25)
            accent = existing.get("accent", _default_accent)
        else:
            headline, accent = "", _default_accent
        subtitle = _smart_trunc(kw, 60) if kw else ""
        # 🔧 去除残留中文字符（如M1.5输出的"Yala雪山"）
        import re as _re
        headline = _re.sub(r'[\u4e00-\u9fff]+', '', headline).strip()
        if not headline:
            headline = kw[:25].strip() if kw else ""
            headline = _re.sub(r'[\u4e00-\u9fff]+', '', headline).strip()
        subtitle = _re.sub(r'\s+', ' ', subtitle).strip()  # 合并多余空格
        result = {"type": vp_type, "headline": headline,
                  "subtitle": subtitle, "accent": accent}
        # 行程表数据注入第一个scene的visual_plan
        if idx == 0 and _script_itinerary:
            result["itinerary_data"] = _script_itinerary
        return result

    storyboard_scenes = []
    segs = list(storyboard)
    for idx, seg in enumerate(segs):
        speech_snip = seg.get("speech_snippet", "")
        keyword = speech_snip[:50].strip() if speech_snip else ""
        vp = _fill_vp(idx, seg, len(segs), hook_text, cta_text)
        _accent = account.get("accent_color", "")
        storyboard_scenes.append({
            "scene": seg.get("scene", ""),
            "path": seg.get("material_path", ""),
            "tags": seg.get("tags", []),
            "effects": seg.get("effects", []),
            "start_sec": seg.get("start_sec", 0),
            "end_sec": seg.get("end_sec", 10),
            "speech_snippet": seg.get("speech_snippet", ""),
            "keyword": keyword,
            "accent_color": _accent,
            "visual_plan": vp,
        })

    # DEBUG: 确认素材路径
    for _i, _s in enumerate(storyboard_scenes):
        _p = _s.get("path", "")
        logger.info(f"  [M4-input] scene[{_i}]: {_s.get('scene','')} path={'OK' if _p and os.path.exists(_p) else 'MISSING'} ({_p[-50:] if _p else 'N/A'})")

    # === M4 渲染（带重试） ===
    logger.info("M4: Rendering video...")
    render_ok = False
    try:
        render_ok = _retry_stage("M4", account_id, max_retries,
            _do_m4_render, storyboard_scenes, speech_audio, bgm_audio,
            tts_duration, style, hook_text, cta_text, total_dur, m4_orient,
            quality="high", word_timeline=word_timeline)
    except Exception as e:
        errors.append(f"M4 rendering failed after {max_retries} retries: {e}")
        if "Material gap" in str(e):
            clean_workspace()
            return {"success": False, "errors": errors, "gap_info": str(e)}
        clean_workspace()
        return {"success": False, "errors": errors}

    if not render_ok:
        errors.append("M4 rendering returned False")
        clean_workspace()
        return {"success": False, "errors": errors}

    # 成品从工作台复制到账号目录
    temp_output = str(WORKSPACE_DIR / "hf_output.mp4")
    if os.path.exists(temp_output):
        shutil.copy2(temp_output, final_output)
        caption_file = str(account_output_dir /
                           video_name.replace(".mp4", ".txt"))
        with open(caption_file, "w", encoding="utf-8") as f:
            f.write(speech_text + "\n\n---\n\n" + caption)
        logger.info(f"📁 成品已归档: {final_output}")
        logger.info(f"📝 文案已归档: {caption_file} "
                    f"({len(speech_text)}字speech)")
    else:
        errors.append("Render output not found")
        return {"success": False, "errors": errors}

    # === M5 质检（带重试） ===
    logger.info("M5: Quality check...")
    qa_history = {}
    if history:
        qa_history = {
            "captions": [h.get("caption", "")
                         for h in history if isinstance(h, dict)],
            "materials": [],
        }

    try:
        qa_result = _retry_stage("M5", account_id, max_retries,
            run_all_checks,
            video_path=(final_output if os.path.exists(final_output)
                        else temp_output),
            scenes=matched, caption=caption,
            materials=matched_materials, history=qa_history,
            total_dur=tts_duration,
            storyboard_scenes=storyboard)
    except Exception as e:
        errors.append(f"M5 failed after {max_retries} retries: {e}")
        return {"success": False, "errors": errors,
                "video_path": final_output}

    if not qa_result.get("passed", False):
        reasons = []
        for key, val in qa_result.get("results", {}).items():
            if not val.get("passed", True):
                reasons.append(f"{key}: {val.get('reason', 'fail')}")
        reason_str = "; ".join(reasons)
        logger.warning(f"M5 blocked: {reason_str}")

        # 🔧 M5重试循环 (2026-05-31): 最多3次，每次从M1.5重新生成
        _m5_retries = 0
        _m5_max = 3

        while _m5_retries < _m5_max and not qa_result.get("passed", False):
            _m5_retries += 1
            logger.info(f"♻️ M5第{_m5_retries}/{_m5_max}次重试 (反馈: {reason_str[:80]})")

            # --- Step 1: 重新生成文案 (M1.5) ---
            try:
                script = _retry_stage("M15-M5RETRY", account_id, max_retries,
                    generate_script, account, direction, history,
                    m1_strategy_prompt=m1_prompt,
                    m2_feedback=f"[M5 QA Failed] {reason_str}")
                if not script:
                    logger.warning("  M1.5返回空，跳过本重试")
                    continue
            except Exception as e:
                logger.warning(f"  M1.5重试异常: {e}")
                continue

            speech_text = script.get("speech_text", "")
            caption = script.get("caption", "")
            for s in ['@ChinaUnbounded','ChinaUnbounded','China Unbounded']:
                speech_text = speech_text.replace(s, 'Pandajourneys')
                caption = caption.replace(s, 'Pandajourneys')
            if '#pandajourneys' not in caption.lower():
                caption = caption.rstrip() + ' #pandajourneys'
            hook_text = script.get("hook_text", "")
            cta_text = script.get("cta_text", "")
            scenes = script.get("scenes", [])
            scene_mapping = script.get("scene_mapping", [])

            # --- Step 2: 重新TTS ---
            try:
                tts_result = _retry_stage("TTS-M5RETRY", account_id, max_retries,
                    generate_tts, speech_text, voice)
                speech_audio = tts_result.get("path", speech_audio)
                tts_duration = tts_result.get("duration_sec", tts_duration)
                if tts_duration > MAX_TTS_DUR:
                    logger.warning(f"  TTS {tts_duration:.1f}s > {MAX_TTS_DUR}s上限，跳过本重试")
                    continue
                logger.info(f"  🔊 TTS再生: {tts_duration:.1f}s")
            except Exception as e:
                logger.warning(f"  TTS重试异常: {e}")
                continue

            # --- Step 3: 重新M2 ---
            try:
                m2_result = check_script(script, history,
                                          direction=direction,
                                          style=account.get("style", ""))
                if not m2_result.get("passed", False):
                    m2_reasons = "; ".join(m2_result.get("reasons", []))
                    logger.warning(f"  M2 still blocked: {m2_reasons[:60]}")
                    reason_str = m2_reasons  # 反馈给下一轮M1.5
                    continue
                logger.info("  ✅ M2通过")
            except Exception as e:
                logger.warning(f"  M2重检异常: {e}")
                continue

            # --- Step 4: 重新Storyboard ---
            try:
                word_timeline = _fallback_words(speech_text, avg_speed=3.0)
                script["word_timeline"] = word_timeline
                sb_result = generate_storyboard(speech_text, tts_duration,
                                                 scene_mapping or scenes,
                                                 account, history)
                storyboard = sb_result.get("storyboard", [])
                if not storyboard:
                    logger.warning("  Storyboard为空，跳过本重试")
                    continue
                if not check_storyboard_similarity(storyboard, history):
                    logger.warning("  Storyboard查重不通过")
                    continue
                logger.info(f"  📋 Storyboard: {len(storyboard)}段")
            except Exception as e:
                logger.warning(f"  Storyboard重试异常: {e}")
                continue

            # --- Step 5: 重新M3素材匹配 ---
            sb_scenes = [seg["scene"] for seg in storyboard if seg.get("scene")]
            m3_orient = account.get("orientation", "portrait")
            scene_durs = [seg["end_sec"] - seg["start_sec"]
                          for seg in storyboard if seg.get("scene")]
            try:
                matched = _retry_stage("M3-M5RETRY", account_id, max_retries,
                    match_scenes, sb_scenes, m3_orient, scene_durs)
            except Exception as e:
                logger.warning(f"  M3重试异常: {e}")
                continue
            gaps = [m for m in matched if not m.get("path")]
            if gaps:
                logger.warning(f"  M3缺口: {[g['scene'] for g in gaps]}")
                continue

            matched_materials = [m.get("path", "") for m in matched]
            for i, seg in enumerate(storyboard):
                if i < len(matched):
                    seg["material_path"] = matched[i].get("path", "")
            logger.info(f"  ✅ M3: {len(matched_materials)}素材")

            # --- Step 6: 重新构建 storyboard_scenes ---
            _script_itinerary = script.get("itinerary_data", [])
            if _script_itinerary:
                for _it in _script_itinerary:
                    if _it.get("destination"):
                        _it["destination"] = _cn_to_en(_it["destination"])
                    if _it.get("from"):
                        _it["from"] = _cn_to_en(_it["from"])

            storyboard_scenes = []
            segs = list(storyboard)
            for idx, seg in enumerate(segs):
                speech_snip = seg.get("speech_snippet", "")
                keyword = speech_snip[:50].strip() if speech_snip else ""
                vp = _fill_vp(idx, seg, len(segs), hook_text, cta_text)
                _accent = account.get("accent_color", "")
                storyboard_scenes.append({
                    "scene": seg.get("scene", ""),
                    "path": seg.get("material_path", ""),
                    "tags": seg.get("tags", []),
                    "effects": seg.get("effects", []),
                    "start_sec": seg.get("start_sec", 0),
                    "end_sec": seg.get("end_sec", 10),
                    "speech_snippet": seg.get("speech_snippet", ""),
                    "keyword": keyword,
                    "accent_color": _accent,
                    "visual_plan": vp,
                })

            # --- Step 7: 重新M4渲染 ---
            logger.info("  🎬 M4渲染...")
            try:
                render_ok = _retry_stage("M4-M5RETRY", account_id, max_retries,
                    _do_m4_render, storyboard_scenes, speech_audio, bgm_audio,
                    tts_duration, style=account.get("style", "velvet"),
                    hook_text=hook_text, cta_text=cta_text,
                    output_path=final_output, total_dur=total_dur,
                    orientation=account.get("orientation", "portrait"),
                    word_timeline=word_timeline, account_id=account_id)
                if not render_ok:
                    logger.warning("  M4渲染返回False")
                    continue
            except Exception as e:
                logger.warning(f"  M4渲染异常: {e}")
                continue

            # --- Step 8: 重新M5质检 ---
            logger.info("  🔍 M5重新质检...")
            try:
                qa_result = _retry_stage("M5-M5RETRY", account_id, max_retries,
                    run_all_checks,
                    video_path=(final_output if os.path.exists(final_output)
                                else temp_output),
                    scenes=matched, caption=caption,
                    materials=matched_materials, history=qa_history,
                    total_dur=tts_duration,
                    storyboard_scenes=storyboard_scenes)
            except Exception as e:
                logger.warning(f"  M5重检异常: {e}")
                continue

            if qa_result.get("passed", False):
                logger.info(f"✅ M5第{_m5_retries}次重试通过！")
                break

            reasons = []
            for key, val in qa_result.get("results", {}).items():
                if not val.get("passed", True):
                    reasons.append(f"{key}: {val.get('reason', 'fail')}")
            reason_str = "; ".join(reasons)
            logger.warning(f"  M5仍不通过: {reason_str[:80]}")

        if not qa_result.get("passed", False):
            errors.append(f"M5 failed after {_m5_retries} retries: {reason_str}")
            return {"success": False, "errors": errors,
                    "video_path": final_output}

    # M5通过
    save_qa_history({"caption": caption, "materials": matched_materials})

    # ============================================================
    # 🔧 补丁#1: 记录视频完成状态到context_manager
    # ============================================================
    record_video_completed(
        account_id=account_id,
        schedule_entry={},
        scenes=[seg.get("scene", "") for seg in storyboard],
        caption=caption,
        speech_text=speech_text,
        cta_text=cta_text,
        material_count=len([m for m in matched_materials if m]),
        direction=direction,
    )

    # === M6 发布 ===

    if skip_publish:
        logger.info("M6: Skipped (skip_publish=True)")
        result = {"published": False, "publish_result": {"success": False, "error": "Skipped"}}
        logger.info(f"✅ Pipeline complete (no publish): {video_name}")
        return {"success": True, "video_path": str(video_name)}

    logger.info("M6: Publishing...")
    # 从文件名解析日期和AM/PM（文件名决定排期）
    # 格式: %m%d_AM(%H%M).mp4 → 5月21号 AM 排期
    import re as _re
    _match = _re.match(r'(\d{2})(\d{2})_(AM|PM)', video_name)
    if _match:
        _mon = int(_match.group(1))
        _day = int(_match.group(2))
        is_am = (_match.group(3) == "AM")
        _year = datetime.now().year
        schedule_date = datetime(_year, _mon, _day)
    else:
        # 降级：文件名不规范时用今天
        schedule_date = datetime.now()
        is_am = "_AM" in video_name
    # 黄金流量时段：上午08-10点 / 晚上18-20点
    hour_min, hour_max = (8, 10) if is_am else (18, 20)
    registry = load_schedule_registry()
    last_time = None
    for entry in reversed(registry.get("schedule", [])):
        if (entry.get("account_id") == account_id
                and entry.get("scheduled_at")):
            try:
                last_time = datetime.fromisoformat(entry["scheduled_at"])
                if last_time.tzinfo is not None:
                    last_time = last_time.replace(tzinfo=None)
            except:
                pass
            break
    for _ in range(20):
        rand_hour = random.randint(hour_min, hour_max)
        rand_min = random.randint(0, 59)
        schedule_dt = schedule_date.replace(hour=rand_hour, minute=rand_min,
                                             second=0, microsecond=0)
        if schedule_dt <= datetime.now():
            # 过去的日期：立即排到最近的未来时段，不改日期
            schedule_dt = datetime.now() + timedelta(minutes=random.randint(5, 30))
        if last_time and abs((schedule_dt - last_time).total_seconds()) < 1800:
            continue
        break
    schedule_time = schedule_dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    logger.info(f"  排期: {'上午' if is_am else '下午'}"
                f" ({hour_min:02d}:00-{hour_max}:59)")
    logger.info(f"  选定时间: {schedule_time}")

    # 根据metricool配置决定发布平台
    try:
        mc_path = METRICOOL_FILE
        _providers = None
        if mc_path.exists():
            import json as _jl
            with open(mc_path) as _mf:
                _mc = _jl.load(_mf)
            _acct = _mc.get("accounts", {}).get(account_id, {})
            _ig = _acct.get("instagram", "")
            _tk = _acct.get("tiktok", "")
            _providers_list = []
            if _tk:
                _providers_list.append({"network": "tiktok"})
            if _ig:
                _providers_list.append({"network": "instagram"})
            if _providers_list:
                _providers = _providers_list
            else:
                _providers = [{"network": "tiktok"}]  # 至少发TK，不强制IG
        if _providers:
            logger.info(f"  发布平台: {[p['network'] for p in _providers]}")
    except:
        _providers = None

    try:
        # 最终安全检查: 确保 #pandajourneys 标签存在 (2026-05-31)
        if '#pandajourneys' not in caption.lower():
            caption = caption.rstrip() + ' #pandajourneys'
        publish_result = _retry_stage("M6", account_id, max_retries,
            publish_metricool,
            video_path=(final_output if os.path.exists(final_output)
                        else temp_output),
            caption=caption, account_id=account_id,
            schedule_time=schedule_time,
            providers=_providers)
    except Exception as e:
        errors.append(f"M6 publish failed after {max_retries} retries: {e}")
        publish_result = {"success": False, "error": str(e)}

    if publish_result.get("success"):
        reg = load_schedule_registry()
        reg["last_id"] = reg.get("last_id", 0) + 1
        reg.setdefault("schedule", []).append({
            "id": f"S{reg['last_id']:04d}",
            "account_id": account_id,
            "account_name": account["name"],
            "direction": direction,
            "video": video_name,
            "caption": caption[:60],
            "scheduled_at": schedule_time,
            "post_id": publish_result.get("post_id", ""),
            "created_at": str(datetime.now()),
        })
        save_schedule_registry(reg)
    else:
        errors.append(f"M6 publish failed: "
                      f"{publish_result.get('error', 'unknown')}")

    # 🔧 补丁#4: 成功完成删除断点
    if publish_result.get("success"):
        _delete_checkpoint()

    clean_workspace()

    return {
        "success": True if not errors else False,
        "video_path": final_output,
        "caption": caption,
        "errors": errors if errors else None,
        "tts_duration": tts_duration,
        "style": style,
        "direction": direction,
        "publish_result": publish_result,
    }


def batch_run(account_ids: list = None):
    """批量运行多个账号"""
    if account_ids is None:
        account_ids = ["00", "01", "03", "04", "05", "06",
                       "07", "08", "09", "10", "11", "12", "13"]

    results = {}
    registry = load_schedule_registry()

    for aid in account_ids:
        progress = get_account_direction_progress(aid, registry)
        direction = DIRECTIONS[progress % len(DIRECTIONS)]

        logger.info(f"\n{'='*60}")
        logger.info(f"Running: account {aid} - {direction}")
        logger.info(f"{'='*60}")

        result = run_pipeline(aid, direction)
        results[aid] = result

        if result["success"]:
            logger.info(f"✓ {aid} completed: "
                        f"{result.get('video_path', 'N/A')}")
        else:
            logger.error(f"✗ {aid} failed: "
                         f"{result.get('errors', [])}")

    return results


# ============================================================
# CLI 入口
# ============================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")

    if len(sys.argv) > 1:
        account = sys.argv[1]
    else:
        account = "00"

    result = run_pipeline(account)
    if result["success"]:
        print(f"\n✅ Pipeline successful!")
        print(f"  Video: {result.get('video_path', 'N/A')}")
        print(f"  Style: {result.get('style')}")
        print(f"  Direction: {result.get('direction')}")
    else:
        print(f"\n❌ Pipeline failed:")
        for err in result.get("errors", []):
            print(f"  - {err}")
