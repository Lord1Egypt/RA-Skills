#!/usr/bin/env python3
"""
COROS 高驰运动数据获取 Skill
登录并获取用户数据，分类展示
"""

import json
import os
import urllib.request
import urllib.error
import time
import gzip
import copy
from datetime import datetime
from typing import Dict, List, Any, Optional


# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# API 配置
LOGIN_URL = "https://teamcnapi.coros.com/account/login"
API_BASE = "https://teamcnapi.coros.com"

# 请求头
DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": "application/json",
    "Origin": "https://t.coros.com",
    "Referer": "https://t.coros.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
}

# 运动类型映射
SPORT_TYPE_MAP = {
    1: "running",
    2: "cycling",
    3: "swimming",
    4: "hiking",
    5: "walking",
    6: "strength",
    7: "yoga",
    8: "running",  # 跑步机
    100: "running",  # 户外跑步
}

SPORT_ICON_MAP = {
    "running": "🏃",
    "cycling": "🚴",
    "swimming": "🏊",
    "hiking": "🥾",
    "walking": "🚶",
    "strength": "💪",
    "yoga": "🧘",
    "other": "⚡",
}

WEATHER_TYPE_MAP = {
    0: "晴",
    1: "多云",
    2: "阴",
    3: "雨",
    4: "雪",
    5: "雾",
    6: "风",
    7: "霾",
}

WIND_DIRECTION_MAP = {
    0: "无风向",
    1: "北风",
    2: "东北风",
    3: "东风",
    4: "南风",
    5: "西风",
    6: "西北风",
    7: "西南风",
}

TRAIN_TYPE_MAP = {
    1: "恢复",
    2: "基础",
    3: "有氧",
    4: "阈值",
    5: "间歇",
}

AEROBIC_EFFECT_MAP = {
    0: "无效果",
    1: "恢复",
    2: "维持",
    3: "提升",
    4: "显著提升",
}

PERFORMANCE_MAP = {
    0: "一般",
    1: "正常",
    2: "良好",
    3: "优秀",
}


def load_config() -> Dict:
    """加载配置文件"""
    config_path = CONFIG_FILE
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    return {}


def save_config(config: Dict) -> None:
    """保存配置文件"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


class CorosClient:
    """COROS API 客户端"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.token: Optional[str] = None
        self.user_info: Optional[Dict] = None
        self.user_id: Optional[str] = None
        self.cookies: Optional[str] = config.get("cookie", "") if config else ""
        self.login_time: float = 0  # 登录时间戳
        self.last_update_error: str = ""

        # 从配置恢复 token
        saved_token = config.get("token", "")
        saved_user_id = config.get("user_id", "")
        saved_cookies = config.get("saved_cookie", "")
        if saved_token:
            self.token = saved_token
            self.user_id = saved_user_id
            self.cookies = saved_cookies or self.cookies
            self.cookies = self._merge_cookie_token(self.cookies, self.token)

    def _merge_cookie_token(self, cookie_str: str, token: str) -> str:
        """将 cookie 中的 CPL-coros-token 与当前 token 对齐（去重）"""
        if not token:
            return cookie_str or ""
        parts = [p.strip() for p in (cookie_str or "").split(";") if p.strip()]
        filtered = [p for p in parts if not p.startswith("CPL-coros-token=")]
        filtered.append(f"CPL-coros-token={token}")
        return "; ".join(filtered)

    def _make_request(
        self,
        url: str,
        data: Dict = None,
        method: str = "POST",
        extra_headers: Dict = None,
        raw_body: bytes = None,
    ) -> Optional[Dict]:
        """发送 HTTP 请求"""
        headers = DEFAULT_HEADERS.copy()
        if self.token:
            headers["accesstoken"] = self.token
        if self.cookies:
            if self.token:
                self.cookies = self._merge_cookie_token(self.cookies, self.token)
            headers["Cookie"] = self.cookies
        if self.user_id:
            headers["yfheader"] = json.dumps({"userId": self.user_id})
        if extra_headers:
            headers.update(extra_headers)

        req = urllib.request.Request(url, headers=headers, method=method)

        if raw_body is not None:
            req.data = raw_body
        elif data:
            req.data = json.dumps(data).encode("utf-8")

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                raw = response.read()
                if response.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return json.loads(raw.decode("utf-8"))
        except urllib.error.URLError as e:
            print(f"请求失败: {e}")
            return None
        except (gzip.BadGzipFile, UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"响应解析失败: {e}")
            return None

    def is_token_valid(self) -> bool:
        """检查 token 是否有效（24小时内有效）"""
        if not self.token:
            return False
        # 检查是否超过24小时
        if time.time() - self.login_time > 86400:
            return False
        return True

    def login(self, account: str, p1_hash: str = None, p2_hash: str = None, force: bool = False) -> bool:
        """登录 COROS 账号"""
        # 如果 token 有效且不强制登录，直接返回
        if not force and self.is_token_valid():
            print("  ✅ 使用缓存的 Token")
            return True

        if not p1_hash or not p2_hash:
            print("  ⚠️ 需要提供密码哈希 p1 和 p2")
            return False

        login_data = {
            "account": account,
            "accountType": 2,
            "p1": p1_hash,
            "p2": p2_hash,
        }

        response = self._make_request(LOGIN_URL, login_data)
        if response:
            if response.get("result") == "0000" or response.get("message") == "OK":
                self.token = response.get("data", {}).get("accessToken")
                self.user_info = response.get("data", {})
                self.user_id = self.user_info.get("userId")
                self.login_time = time.time()
                # 更新 cookie
                if self.token:
                    self.cookies = self._merge_cookie_token(self.cookies, self.token)
                # 保存到配置
                self._save_token()
                return True
            else:
                print(f"登录失败: {response.get('message')}")
        return False

    def _save_token(self) -> None:
        """保存 token 到配置文件"""
        config = load_config()
        config["token"] = self.token
        config["user_id"] = self.user_id
        config["saved_cookie"] = self.cookies
        save_config(config)

    def get_dashboard_detail(self) -> Optional[Dict]:
        """获取 Dashboard 详情"""
        if not self.token:
            return None
        url = f"{API_BASE}/dashboard/detail/query"
        response = self._make_request(url, method="GET")
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_dashboard_summary(self) -> Optional[Dict]:
        """获取 Dashboard 汇总数据（跑步能力/恢复/HRV/预测）"""
        if not self.token:
            return None
        url = f"{API_BASE}/dashboard/query"
        response = self._make_request(url, method="GET")
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_dashboard_cycle_record(self) -> Optional[Dict]:
        """获取 Dashboard 周期纪录（跑步/骑行纪录）"""
        if not self.token:
            return None
        url = f"{API_BASE}/dashboard/queryCycleRecord"
        response = self._make_request(url, method="GET")
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_profile_private(self) -> Optional[Dict]:
        """获取私有配置（页面布局/模块配置）"""
        if not self.token:
            return None
        url = f"{API_BASE}/profile/private/query"
        response = self._make_request(url, method="GET")
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_activities(self, page: int = 1, size: int = 20) -> Optional[Dict]:
        """获取活动列表"""
        if not self.token:
            return None
        url = f"{API_BASE}/activity/query?size={size}&pageNumber={page}&modeList="
        response = self._make_request(url, method="GET")
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_activity_detail(
        self,
        label_id: str,
        sport_type: int = 100,
        screen_w: int = 1210,
        screen_h: int = 982,
    ) -> Optional[Dict]:
        """获取单次活动详情"""
        if not self.token or not label_id:
            return None
        url = (
            f"{API_BASE}/activity/detail/query"
            f"?screenW={screen_w}&screenH={screen_h}&labelId={label_id}&sportType={sport_type}"
        )
        response = self._make_request(
            url,
            method="POST",
            extra_headers={"Content-Type": "application/x-www-form-urlencoded"},
            raw_body=b"",
        )
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_schedule(self, start_date: str = None, end_date: str = None) -> Optional[Dict]:
        """获取训练日程"""
        if not self.token:
            return None

        from datetime import datetime, timedelta
        today = datetime.now()

        if not start_date:
            start_date = today.replace(day=1).strftime('%Y%m%d')
        if not end_date:
            end_date = (today + timedelta(days=60)).strftime('%Y%m%d')

        url = f"{API_BASE}/training/schedule/query?startDate={start_date}&endDate={end_date}&supportRestExercise=1"
        response = self._make_request(url, method="GET")
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_schedule_summary(self, start_date: str = None, end_date: str = None) -> Optional[Dict]:
        """获取训练日程汇总"""
        if not self.token:
            return None

        from datetime import datetime, timedelta
        today = datetime.now()

        if not start_date:
            start_date = today.strftime('%Y%m%d')
        if not end_date:
            end_date = (today + timedelta(days=30)).strftime('%Y%m%d')

        url = f"{API_BASE}/training/schedule/querysum?teamId=&userId=&startDate={start_date}&endDate={end_date}"
        response = self._make_request(url, method="GET")
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_program_list(self) -> Optional[Dict]:
        """获取训练计划列表"""
        if not self.token:
            return None
        url = f"{API_BASE}/training/program/list"
        response = self._make_request(url, method="GET")
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def get_import_sport_list(self, size: int = 10) -> Optional[Dict]:
        """获取可导入运动列表（训练页会请求）"""
        if not self.token:
            return None
        url = f"{API_BASE}/activity/fit/getImportSportList"
        response = self._make_request(url, data={"size": size})
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def estimate_program(self, entity: Dict, program: Dict) -> Optional[Dict]:
        """估算训练计划（距离/时长/TL/图表）"""
        if not self.token:
            return None
        url = f"{API_BASE}/training/program/estimate"
        response = self._make_request(url, data={"entity": entity, "program": program})
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def calculate_program(self, program: Dict) -> Optional[Dict]:
        """计算训练计划细节"""
        if not self.token:
            return None
        url = f"{API_BASE}/training/program/calculate"
        response = self._make_request(url, data=program)
        if response and response.get("result") == "0000":
            return response.get("data", {})
        return None

    def update_schedule(
        self,
        entities: List[Dict],
        programs: List[Dict],
        version_objects: List[Dict],
        pb_version: int = 2,
    ) -> bool:
        """更新训练日程（新增/更新都走同一接口）"""
        if not self.token:
            return False

        url = f"{API_BASE}/training/schedule/update"
        data = {
            "entities": entities,
            "programs": programs,
            "pbVersion": pb_version,
            "versionObjects": version_objects,
        }

        response = self._make_request(url, data)
        if response and response.get("result") == "0000":
            self.last_update_error = ""
            return True
        self.last_update_error = str(response.get("message", "无响应")) if response else "无响应"
        print(f"更新日程失败: {self.last_update_error}")
        return False

    def add_schedule(self, date: str, program_data: Dict) -> bool:
        """兼容旧调用：添加训练日程"""
        entity = {
            "happenDay": date,
            "idInPlan": program_data.get("idInPlan", 2),
            "sortNo": 0,
            "dayNo": 0,
            "sortNoInPlan": 0,
            "sortNoInSchedule": 0,
            "exerciseBarChart": program_data.get("exerciseBarChart", []),
        }
        version_obj = {"id": program_data.get("idInPlan", 2), "status": 1}
        return self.update_schedule([entity], [program_data], [version_obj], pb_version=2)


class ActivityData:
    """运动活动数据模型"""

    def __init__(self, data: Dict):
        self.id = data.get("labelId", "") or data.get("id", "")
        self.name = data.get("name", "")
        # sportType: 100=户外跑, 8=跑步机 等
        sport_type = data.get("sportType", 100)
        self.type = SPORT_TYPE_MAP.get(sport_type, "other")
        self.start_time = data.get("startTime", 0) or data.get("timestamp", 0)
        # 兼容不同字段名
        self.duration = data.get("totalTime", 0) or data.get("duration", 0)
        self.distance = data.get("distance", 0)
        self.training_load = data.get("trainingLoad", 0)
        self.calories = int(self.training_load * 2)
        self.avg_hr = data.get("avgHr", 0) or data.get("avgHeartRate", 0)
        self.max_hr = data.get("maxHr", 0)
        self.avg_pace = data.get("adjustedPace", 0) or data.get("avgPace", 0)
        self.elevation_gain = data.get("ascent", 0) or data.get("totalElevation", 0)
        # 兼容不同字段名
        self.happen_day = data.get("date", "") or data.get("happenDay", "")

    @property
    def type_icon(self) -> str:
        return SPORT_ICON_MAP.get(self.type, "⚡")

    @property
    def duration_str(self) -> str:
        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def distance_km(self) -> float:
        return self.distance / 1000

    @property
    def pace_str(self) -> str:
        if self.avg_pace and self.avg_pace > 0:
            minutes = self.avg_pace // 60
            seconds = self.avg_pace % 60
            return f"{minutes}'{seconds:02d}\""
        return "--"

    def __repr__(self):
        return f"<Activity {self.type_icon} {self.distance_km:.2f}km>"


def format_pace(pace: int) -> str:
    """格式化配速"""
    if pace and pace > 0:
        minutes = pace // 60
        seconds = pace % 60
        return f"{minutes}'{seconds:02d}\""
    return "--"


def format_centiseconds(value: int) -> str:
    """格式化百分秒为时间字符串"""
    if not value:
        return "00:00:00"
    total_seconds = int(round(value / 100))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def centis_to_datetime_str(value: int) -> str:
    """百分秒时间戳转本地时间"""
    if not value:
        return "--"
    try:
        ts = value / 100
        return datetime.fromtimestamp(ts).strftime("%Y/%m/%d %H:%M")
    except (OSError, OverflowError, ValueError):
        return "--"


def distance_cm_to_km(value: int) -> float:
    """厘米转公里"""
    return (value or 0) / 100000


def parse_weather(data: Dict) -> Dict:
    """标准化天气字段"""
    weather_type = data.get("weatherType", -1)
    wind_direction = data.get("windDirectionType", 0)
    return {
        "weather": WEATHER_TYPE_MAP.get(weather_type, f"类型{weather_type}"),
        "temperature": (data.get("temperature", 0) or 0) / 10,
        "body_feel_temp": (data.get("bodyFeelTemp", 0) or 0) / 10,
        "humidity": (data.get("humidity", 0) or 0) / 10,
        "wind_speed": round((data.get("windSpeed", 0) or 0) / 10),
        "wind_direction": WIND_DIRECTION_MAP.get(wind_direction, f"风向{wind_direction}"),
    }


def parse_sport_feel(data: Dict) -> str:
    """标准化运动感受"""
    feel_map = {
        0: "未填写",
        1: "很轻松",
        2: "轻松",
        3: "一般",
        4: "疲劳",
        5: "很疲劳",
    }
    feel_type = int(data.get("feelType", 0) or 0)
    note = str(data.get("sportNote", "") or "").strip()
    feel_text = feel_map.get(feel_type, f"类型{feel_type}")
    return f"{feel_text} | 备注: {note}" if note else feel_text


def normalize_schedule_entries(data: Dict) -> List[Dict]:
    """兼容 scheduleList 与 entities/programs 两种结构"""
    schedule_list = data.get("scheduleList", [])
    if schedule_list:
        return schedule_list

    entities = data.get("entities", [])
    programs = data.get("programs", [])
    if not entities:
        return []

    program_map: Dict[str, Dict] = {}
    for p in programs:
        key = str(p.get("idInPlan", ""))
        if key:
            program_map[key] = p

    normalized = []
    for e in entities:
        id_in_plan = str(e.get("idInPlan", ""))
        p = program_map.get(id_in_plan, {})
        sport_type = int(p.get("sportType", 1) or 1)
        type_name = SPORT_TYPE_MAP.get(100 if sport_type == 1 else sport_type, "other")
        if type_name == "running":
            type_name_cn = "跑步"
        elif type_name == "cycling":
            type_name_cn = "骑行"
        else:
            type_name_cn = type_name
        normalized.append(
            {
                "date": e.get("happenDay", ""),
                "typeName": type_name_cn,
                "content": p.get("name", "训练"),
                "status": e.get("executeStatus", 0),
                "idInPlan": e.get("idInPlan"),
                "planId": e.get("planId"),
                "planProgramId": e.get("planProgramId"),
            }
        )
    return normalized


def get_schedule_records(data: Dict) -> List[Dict]:
    """返回带原始 entity/program 的日程记录"""
    entities = data.get("entities", []) or []
    programs = data.get("programs", []) or []
    if not entities:
        return []

    program_map: Dict[str, Dict] = {}
    for p in programs:
        key = str(p.get("idInPlan", ""))
        if key:
            program_map[key] = p

    records: List[Dict] = []
    for e in entities:
        id_in_plan = str(e.get("idInPlan", ""))
        p = program_map.get(id_in_plan, {})
        records.append(
            {
                "date": str(e.get("happenDay", "")),
                "idInPlan": str(e.get("idInPlan", "")),
                "planId": str(e.get("planId", "")),
                "planProgramId": str(e.get("planProgramId", "")),
                "sortNoInSchedule": int(e.get("sortNoInSchedule", 0) or 0),
                "name": str(p.get("name", "")),
                "duration": int(p.get("duration", 0) or 0),
                "distance_cm": int(p.get("distance", 0) or 0),
                "entity": e,
                "program": p,
            }
        )
    return records


def filter_records_by_date(records: List[Dict], date: str) -> List[Dict]:
    """按日期过滤日程记录"""
    return [r for r in records if str(r.get("date", "")) == str(date)]


def resolve_target_schedule_record(records: List[Dict], schedule_cfg: Dict) -> Optional[Dict]:
    """按配置从同一天多条日程中精确定位目标记录"""
    if not records:
        return None

    def pick_latest(items: List[Dict]) -> Dict:
        return sorted(items, key=lambda x: (x.get("sortNoInSchedule", 0), int(x.get("idInPlan", "0") or 0)))[-1]

    target_id_in_plan = str(schedule_cfg.get("target_id_in_plan", "")).strip()
    target_plan_program_id = str(schedule_cfg.get("target_plan_program_id", "")).strip()
    target_name = str(schedule_cfg.get("target_name", "")).strip()
    target_duration_seconds = int(schedule_cfg.get("target_duration_seconds", 0) or 0)
    target_distance_km = float(schedule_cfg.get("target_distance_km", 0) or 0)
    target_name_lc = target_name.lower()
    has_explicit_target = bool(
        target_id_in_plan
        or target_plan_program_id
        or target_name
        or target_duration_seconds > 0
        or target_distance_km > 0
    )

    if target_id_in_plan:
        matched = [r for r in records if r.get("idInPlan") == target_id_in_plan]
        if matched:
            return pick_latest(matched)

    if target_plan_program_id:
        matched = [r for r in records if r.get("planProgramId") == target_plan_program_id]
        if matched:
            return pick_latest(matched)

    if target_name:
        matched = [r for r in records if r.get("name") == target_name]
        if matched:
            return pick_latest(matched)
        # 支持“5km”这类部分名称匹配
        fuzzy = [r for r in records if target_name_lc in str(r.get("name", "")).lower()]
        if fuzzy:
            return pick_latest(fuzzy)

    if target_duration_seconds > 0:
        # 时长允许 2 分钟容差，避免估算误差导致无法命中
        matched = [
            r for r in records
            if abs(int(r.get("duration", 0) or 0) - target_duration_seconds) <= 120
        ]
        if matched:
            return pick_latest(matched)

    if target_distance_km > 0:
        # 距离字段单位为厘米，使用 0.3km 容差
        tolerance_cm = 30000
        target_distance_cm = int(round(target_distance_km * 100000))
        matched = [
            r for r in records
            if abs(int(r.get("distance_cm", 0) or 0) - target_distance_cm) <= tolerance_cm
        ]
        if matched:
            return pick_latest(matched)

    # 给了目标但未命中时，不做兜底盲删
    if has_explicit_target:
        return None

    # 兜底：未指定筛选条件时取最新一条
    return pick_latest(records)


def has_schedule_on_date(data: Dict, date: str) -> bool:
    """检查指定日期是否存在日程"""
    entries = normalize_schedule_entries(data)
    return any(str(item.get("date", "")) == str(date) for item in entries)


def get_schedule_entry_on_date(data: Dict, date: str) -> Optional[Dict]:
    """获取指定日期第一条日程"""
    entries = normalize_schedule_entries(data)
    for item in entries:
        if str(item.get("date", "")) == str(date):
            return item
    return None


def format_day(day: Any) -> str:
    """格式化 YYYYMMDD 日期"""
    day_str = str(day or "")
    if len(day_str) == 8 and day_str.isdigit():
        return f"{day_str[:4]}/{day_str[4:6]}/{day_str[6:]}"
    return day_str or "--"


def format_seconds(value: int) -> str:
    """将秒数格式化为 HH:MM:SS"""
    if not value:
        return "00:00"
    total = int(value)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def get_hr_zone_ranges(lthr_zone: List[Dict]) -> List[str]:
    """将阈值心率分段转为可读区间"""
    if not lthr_zone:
        return []
    hrs = [int(item.get("hr", 0) or 0) for item in lthr_zone if item.get("hr") is not None]
    if len(hrs) < 5:
        return []
    return [
        f"< {hrs[0]}",
        f"{hrs[0]} - {hrs[1]}",
        f"{hrs[1] + 1} - {hrs[2]}",
        f"{hrs[2] + 1} - {hrs[3]}",
        f"{hrs[3] + 1} - {hrs[4]}",
        f"> {hrs[4]}",
    ]


def get_pace_zone_ranges(ltsp_zone: List[Dict]) -> List[str]:
    """将阈值配速分段转为可读区间"""
    if not ltsp_zone:
        return []
    paces = [int(item.get("pace", 0) or 0) for item in ltsp_zone if item.get("pace") is not None]
    if len(paces) < 6:
        return []
    return [
        f"> {format_pace(paces[0])}",
        f"{format_pace(paces[1])} - {format_pace(paces[0])}",
        f"{format_pace(paces[2])} - {format_pace(max(paces[1] - 1, 0))}",
        f"{format_pace(paces[3])} - {format_pace(max(paces[2] - 1, 0))}",
        f"{format_pace(paces[4])} - {format_pace(max(paces[3] - 1, 0))}",
        f"< {format_pace(paces[5])}",
    ]


def display_dashboard_summary(summary_data: Dict, cycle_record_data: Dict = None) -> None:
    """展示 dashboard/query 的高级仪表盘信息"""
    if not summary_data:
        return
    summary = summary_data.get("summaryInfo", {})

    print(f"\n{'='*60}")
    print("  🧠 仪表盘高级分析")
    print(f"{'='*60}")

    stamina = summary.get("staminaLevel")
    stamina_change = summary.get("staminaLevelChange", 0)
    aerobic = summary.get("aerobicEnduranceScore")
    aerobic_change = summary.get("aerobicEnduranceScoreChange", 0)
    lactate = summary.get("lactateThresholdCapacityScore")
    lactate_change = summary.get("lactateThresholdCapacityScoreChange", 0)
    anaerobic_endurance = summary.get("anaerobicEnduranceScore")
    anaerobic_endurance_change = summary.get("anaerobicEnduranceScoreChange", 0)
    anaerobic_capacity = summary.get("anaerobicCapacityScore")
    anaerobic_capacity_change = summary.get("anaerobicCapacityScoreChange", 0)

    print(f"\n  🏃 跑步能力")
    print(f"  ───────────────────────────────────────")
    if stamina is not None:
        print(f"  综合跑步能力: {stamina} ({stamina_change:+.1f})")
    if aerobic is not None:
        print(f"  有氧耐力: {aerobic} ({aerobic_change:+.1f})")
    if lactate is not None:
        print(f"  乳酸阈能力: {lactate} ({lactate_change:+.1f})")
    if anaerobic_endurance is not None:
        print(f"  速度耐力: {anaerobic_endurance} ({anaerobic_endurance_change:+.1f})")
    if anaerobic_capacity is not None:
        print(f"  冲刺能力: {anaerobic_capacity} ({anaerobic_capacity_change:+.1f})")

    recovery_pct = summary.get("recoveryPct")
    recovery_hours = summary.get("fullRecoveryHours")
    recovery_state_map = {1: "恢复不足", 2: "轻度疲劳", 3: "可正常训练", 4: "体力充沛"}
    recovery_state = recovery_state_map.get(summary.get("recoveryState"), "未知")

    if recovery_pct is not None or recovery_hours is not None:
        print(f"\n  🔋 体力恢复")
        print(f"  ───────────────────────────────────────")
        if recovery_pct is not None:
            print(f"  当前恢复: {recovery_pct}%")
        if recovery_hours is not None:
            print(f"  预计 {recovery_hours} 小时后恢复 100%")
        print(f"  状态: {recovery_state}")

    lthr = summary.get("lthr")
    max_hr = summary.get("fitnessMaxHr")
    resting_hr = summary.get("rhr")
    lthr_zone = summary.get("lthrZone", [])
    hr_ranges = get_hr_zone_ranges(lthr_zone)
    hr_zone_names = ["积极恢复区", "有氧耐力区", "有氧动力区", "乳酸阈区", "速度耐力区", "无氧动力区"]

    if lthr or max_hr or resting_hr or hr_ranges:
        print(f"\n  ❤️ 乳酸阈心率区间")
        print(f"  ───────────────────────────────────────")
        if lthr:
            print(f"  乳酸阈心率: {lthr} bpm")
        if max_hr:
            print(f"  最大心率: {max_hr} bpm")
        if resting_hr:
            print(f"  静息心率: {resting_hr} bpm")
        if hr_ranges:
            for idx, zone_range in enumerate(hr_ranges):
                print(f"  {hr_zone_names[idx]}: {zone_range} bpm")

    ltsp = summary.get("ltsp")
    ltsp_zone = summary.get("ltspZone", [])
    pace_ranges = get_pace_zone_ranges(ltsp_zone)
    if ltsp or pace_ranges:
        print(f"\n  ⏱️ 乳酸阈配速区间")
        print(f"  ───────────────────────────────────────")
        if ltsp:
            print(f"  乳酸阈配速: {format_pace(int(ltsp))} /km")
        for idx, pace_range in enumerate(pace_ranges, start=1):
            print(f"  配速{idx}区: {pace_range} /km")

    run_score_list = summary.get("runScoreList", [])
    prediction_map = {5: "5km", 4: "10km", 2: "半马", 1: "全马"}
    if run_score_list:
        print(f"\n  🏁 成绩预测")
        print(f"  ───────────────────────────────────────")
        for item in sorted(run_score_list, key=lambda x: x.get("duration", 0)):
            race_name = prediction_map.get(item.get("type"))
            if not race_name:
                continue
            duration = int(item.get("duration", 0) or 0)
            avg_pace = int(item.get("avgPace", 0) or 0)
            print(f"  {race_name:<4} | {format_seconds(duration)} | {format_pace(avg_pace)}/km")

    sleep_hrv = summary.get("sleepHrvData", {}) or {}
    if sleep_hrv:
        avg_sleep_hrv = sleep_hrv.get("avgSleepHrv")
        hrv_intervals = sleep_hrv.get("sleepHrvAllIntervalList", [])
        hrv_day = format_day(sleep_hrv.get("happenDay"))
        print(f"\n  📈 HRV 评估")
        print(f"  ───────────────────────────────────────")
        if avg_sleep_hrv is not None:
            print(f"  昨晚平均: {avg_sleep_hrv} ms ({hrv_day})")
        if isinstance(hrv_intervals, list) and len(hrv_intervals) >= 4:
            print(f"  正常范围: {hrv_intervals[2]}-{hrv_intervals[3]} ms")

    # 优先使用 dashboard/query 的跑步纪录，其次降级到 queryCycleRecord（骑行）
    record_groups = summary.get("recordDetailList", []) or []
    running_record_group = next((g for g in record_groups if g.get("type") == 4 and g.get("recordList")), None)
    if running_record_group:
        type_map = {
            7: "1km",
            6: "3km",
            5: "5km",
            4: "10km",
            2: "半马",
            101: "最长单次",
            102: "最高累计爬升",
        }
        print(f"\n  🏅 个人跑步纪录")
        print(f"  ───────────────────────────────────────")
        selected_types = [101, 102, 7, 6, 5, 4, 2]
        records_by_type = {item.get("type"): item for item in running_record_group.get("recordList", [])}
        for rec_type in selected_types:
            item = records_by_type.get(rec_type)
            if not item:
                continue
            name = type_map.get(rec_type, f"类型{rec_type}")
            day = format_day(item.get("happenDay"))
            if rec_type == 102:
                print(f"  {name:<8} | {item.get('record', 0)} m | {day}")
            elif rec_type == 101:
                duration = int(item.get("record", 0) or 0)
                avg_pace = int(item.get("avgPace", 0) or 0)
                print(f"  {name:<8} | {format_seconds(duration)} | {format_pace(avg_pace)}/km | {day}")
            else:
                duration = int(item.get("record", 0) or 0)
                avg_pace = int(item.get("avgPace", 0) or 0)
                print(f"  {name:<8} | {format_seconds(duration)} | {format_pace(avg_pace)}/km | {day}")

    if cycle_record_data:
        all_records = cycle_record_data.get("allRecordList", []) or []
        cycling_group = next((g for g in all_records if g.get("recordList")), None)
        if cycling_group and cycling_group.get("recordList"):
            print(f"\n  🚴 个人骑行纪录")
            print(f"  ───────────────────────────────────────")
            type_map = {101: "最长骑行距离", 102: "最高累计爬升"}
            for item in cycling_group.get("recordList", []):
                rec_type = item.get("type")
                name = type_map.get(rec_type)
                if not name:
                    continue
                day = format_day(item.get("happenDay"))
                value = item.get("record", 0) or 0
                if rec_type == 101:
                    print(f"  {name:<10} | {value/1000:.2f} km | {day}")
                else:
                    print(f"  {name:<10} | {value} m | {day}")


def display_dashboard(data: Dict) -> None:
    """展示 Dashboard 数据"""
    print(f"\n{'='*60}")
    print("  🏃 COROS 高驰 - 运动数据仪表板")
    print(f"{'='*60}")

    summary = data.get("summaryInfo", {})
    sport_data_list = data.get("sportDataList", [])

    ati = summary.get("ati", 0)
    cti = summary.get("cti", 0)
    load_ratio = summary.get("trainingLoadRatio", 0) * 100

    print(f"\n  📊 训练状态")
    print(f"  ───────────────────────────────────────")
    print(f"  短期负荷 (ATI): {ati}")
    print(f"  长期负荷 (CTI): {cti}")
    print(f"  负荷比: {load_ratio:.0f}%")
    
    # 训练状态评估
    if load_ratio < 50:
        status = "🟢 恢复期 - 可增加训练强度"
    elif load_ratio < 80:
        status = "🟡 最佳区间 - 保持当前状态"
    elif load_ratio < 120:
        status = "🟠 警告 - 适当减少强度"
    else:
        status = "🔴 过度训练 - 必须休息"
    print(f"  状态评估: {status}")

    print(f"\n  🏃 最近运动")
    print(f"  ───────────────────────────────────────")

    if sport_data_list:
        for item in sport_data_list[:7]:
            activity = ActivityData(item)
            day = str(activity.happen_day)
            date_str = f"{day[:4]}/{day[4:6]}/{day[6:]}" if len(day) == 8 else day
            print(f"  {date_str} | {activity.distance_km:.2f}km | {activity.pace_str}/km | {activity.training_load}TL")

    if sport_data_list:
        latest = sport_data_list[0] if sport_data_list else {}
        print(f"\n  ❤️ 心率数据 (最新活动)")
        print(f"  ───────────────────────────────────────")
        print(f"  平均心率: {latest.get('avgHeartRate', '--')} bpm")
        if latest.get('maxHr'):
            print(f"  最大心率: {latest.get('maxHr')} bpm")

    print(f"\n  📈 运动类型统计")
    print(f"  ───────────────────────────────────────")
    type_stats = {}
    for item in sport_data_list:
        sport_type = item.get("sportType", 100)
        act_type = SPORT_TYPE_MAP.get(sport_type, "other")
        if act_type not in type_stats:
            type_stats[act_type] = {"count": 0, "distance": 0, "duration": 0, "tl": 0}
        type_stats[act_type]["count"] += 1
        type_stats[act_type]["distance"] += item.get("distance", 0)
        type_stats[act_type]["duration"] += item.get("duration", 0)
        type_stats[act_type]["tl"] += item.get("trainingLoad", 0)

    for act_type, stats in type_stats.items():
        icon = SPORT_ICON_MAP.get(act_type, "⚡")
        print(f"  {icon} {act_type}: {stats['count']}次, {stats['distance']/1000:.2f}km, {stats['duration']/3600:.2f}h, {stats['tl']}TL")
    
    # 配速统计
    if sport_data_list:
        paces = [item.get("avgPace", 0) for item in sport_data_list if item.get("avgPace")]
        if paces:
            avg_pace = int(sum(paces) / len(paces))
            min_pace = int(min(paces))
            max_pace = int(max(paces))
            print(f"\n  📊 配速统计")
            print(f"  ───────────────────────────────────────")
            print(f"  平均配速: {avg_pace//60}'{avg_pace%60:02d}\"/km")
            print(f"  最快配速: {min_pace//60}'{min_pace%60:02d}\"/km")
            print(f"  最慢配速: {max_pace//60}'{max_pace%60:02d}\"/km")
    
    # 心率统计
    if sport_data_list:
        hrs = [(item.get("avgHeartRate", 0), item.get("maxHr", 0)) for item in sport_data_list if item.get("avgHeartRate")]
        if hrs:
            avg_hrs = [h[0] for h in hrs if h[0]]
            max_hrs = [h[1] for h in hrs if h[1]]
            if avg_hrs:
                print(f"\n  ❤️ 心率统计")
                print(f"  ───────────────────────────────────────")
                print(f"  平均心率: {sum(avg_hrs)//len(avg_hrs)} bpm")
                if max_hrs:
                    print(f"  最高心率: {max(max_hrs)} bpm")

    total_distance = sum(item.get("distance", 0) for item in sport_data_list)
    total_duration = sum(item.get("duration", 0) for item in sport_data_list)
    total_tl = sum(item.get("trainingLoad", 0) for item in sport_data_list)

    print(f"\n  📅 本周总计")
    print(f"  ───────────────────────────────────────")
    print(f"  总距离: {total_distance/1000:.2f} km")
    print(f"  总时长: {total_duration/3600:.2f} 小时")
    print(f"  总训练负荷: {total_tl} TL")
    print()


def display_activities(data: Dict) -> None:
    """展示活动列表"""
    print(f"\n{'='*60}")
    print("  📋 活动列表")
    print(f"{'='*60}")

    list_data = data.get("dataList", []) or data.get("list", [])
    total = data.get("total", 0) or data.get("totalPage", 0) * 20

    print(f"\n  共 {total} 个活动")
    print(f"\n  日期       | 类型 | 名称              | 距离     | 时长      | 配速     | 心率  | 负荷")
    print(f"  ─────────────────────────────────────────────────────────────────────────────────────")

    for item in list_data:
        activity = ActivityData(item)
        day = str(activity.happen_day)
        date_str = f"{day[4:6]}/{day[6:]}" if len(day) == 8 else day
        name = (activity.name or "跑步")[:12]
        print(
            f"  {date_str}     | {activity.type_icon}   | {name:<14} | {activity.distance_km:>6.2f}km |"
            f" {activity.duration_str:<8} | {activity.pace_str:<7} | {activity.avg_hr:>4} | {activity.training_load:>3}"
        )
    print()


def display_schedule(data: Dict) -> None:
    """展示训练日程"""
    print(f"\n{'='*60}")
    print("  📅 训练日程")
    print(f"{'='*60}")

    schedule_list = normalize_schedule_entries(data)

    if not schedule_list:
        print("\n  暂无训练日程")
        print("\n  提示: 请在 COROS App 中设置训练计划")
        return

    print(f"\n  共 {len(schedule_list)} 个日程")
    print(f"\n  日期       | 类型        | 内容                    | 状态")
    print(f"  ─────────────────────────────────────────────────────────────────")

    for item in schedule_list:
        date = str(item.get("date", ""))
        date_str = f"{date[4:6]}/{date[6:]}" if len(date) == 8 else date
        type_name = item.get("typeName", "")
        content = item.get("content", "")[:20] if item.get("content") else "请设置周期阶段"
        status = item.get("status", 0)
        status_str = {0: "未完成", 1: "已完成", 2: "进行中"}.get(status, "未知")
        print(f"  {date_str}     | {type_name:<10} | {content:<22} | {status_str}")
    print()


def display_schedule_summary(data: Dict) -> None:
    """展示训练日程汇总"""
    print(f"\n{'='*60}")
    print("  📊 本周训练目标")
    print(f"{'='*60}")

    if not data:
        print("\n  暂无训练目标")
        return

    total_days = data.get("totalDays", 0)
    completed_days = data.get("completedDays", 0)
    total_time = data.get("totalTime", 0)
    total_distance = data.get("totalDistance", 0)
    total_tl = data.get("totalTrainingLoad", 0)

    hours = total_time // 3600
    minutes = (total_time % 3600) // 60

    print(f"\n  📈 目标统计")
    print(f"  ───────────────────────────────────────")
    print(f"  完成天数: {completed_days}/{total_days} 天")
    print(f"  运动时间: {hours:02d}:{minutes:02d}")
    print(f"  运动距离: {total_distance/1000:.2f} km")
    print(f"  训练负荷: {total_tl} TL")

    daily_list = data.get("dailyList", [])
    if daily_list:
        print(f"\n  📅 每日详情")
        print(f"  ───────────────────────────────────────")
        for day in daily_list[:7]:
            day_date = str(day.get("date", ""))
            day_str = f"{day_date[4:6]}/{day_date[6:]}" if len(day_date) == 8 else day_date
            has_plan = day.get("hasPlan", 0)
            if has_plan:
                time_val = day.get("time", 0)
                dist_val = day.get("distance", 0) / 1000
                tl_val = day.get("trainingLoad", 0)
                print(f"  {day_str} | {time_val/3600:.1f}h | {dist_val:.2f}km | {tl_val}TL")
            else:
                print(f"  {day_str} | 休息日")
    print()


def display_activity_detail(data: Dict) -> None:
    """展示活动详情（对齐活动详情页核心信息）"""
    summary = data.get("summary", {})
    lap_groups = data.get("lapList", [])
    weather = parse_weather(data.get("weather", {}))
    sport_feel_text = parse_sport_feel(data.get("sportFeelInfo", {}))
    comments_count = data.get("newMessageCount", 0)

    lap_group = next((x for x in lap_groups if x.get("type") == 2), lap_groups[0] if lap_groups else {})
    lap_items = lap_group.get("lapItemList", [])
    fast_idx_set = set(lap_group.get("fastLapIndexList", []))

    name = summary.get("name", "跑步")
    start_time = centis_to_datetime_str(summary.get("startTimestamp", 0))
    distance_km = distance_cm_to_km(summary.get("distance", 0))
    workout_time = summary.get("workoutTime", 0)
    total_time = summary.get("totalTime", 0)
    avg_pace_seconds = int(summary.get("avgPace", 0) or 0)
    if not avg_pace_seconds and distance_km > 0 and workout_time > 0:
        avg_pace_seconds = int(round((workout_time / 100) / distance_km))

    print(f"\n{'='*60}")
    print("  🧭 活动详情")
    print(f"{'='*60}")
    print(f"\n  {name}")
    print(f"  开始时间: {start_time}")

    if lap_items:
        print(f"\n  📍 计圈数据 ({lap_group.get('lapDistance', 0) / 100000:.2f}km/圈)")
        print(f"  圈数 | 距离   | 时间     | 累计时间 | 平均配速 | 平均心率 | 等强配速")
        print(f"  ─────────────────────────────────────────────────────────────────────")
        for idx, item in enumerate(lap_items):
            lap_no = idx + 1
            mark = " 最快" if idx in fast_idx_set else ""
            lap_distance = f"{distance_cm_to_km(item.get('distance', 0)):.2f}km"
            lap_time = format_centiseconds(item.get("time", 0))
            total_lap_time = format_centiseconds(item.get("totalLength", 0))
            pace = format_pace(int(item.get("avgPace", 0) or 0))
            adjusted_pace = format_pace(int(item.get("adjustedPace", 0) or 0))
            hr = item.get("avgHr", 0) or "--"
            print(
                f"  {lap_no:>2}{mark:<3}| {lap_distance:>6} | {lap_time:>8} | {total_lap_time:>8} |"
                f" {pace:>7} | {str(hr):>8} | {adjusted_pace:>7}"
            )

    print(f"\n  🌤️ 天气")
    print(f"  {weather['weather']} | {weather['temperature']:.0f}℃ | 体感{weather['body_feel_temp']:.0f}℃")
    print(f"  湿度: {weather['humidity']:.0f}% | {weather['wind_direction']} {weather['wind_speed']}级")

    print(f"\n  📊 概要数据")
    print(f"  距离: {distance_km:.2f}km")
    print(f"  运动时间: {format_centiseconds(workout_time)}")
    print(f"  总时间: {format_centiseconds(total_time)}")
    print(f"  平均配速: {format_pace(avg_pace_seconds)} /km")
    print(f"  最快1公里: {format_pace(int(summary.get('bestKm', 0) or 0))} /km")
    print(f"  平均心率: {summary.get('avgHr', '--')} bpm")
    print(f"  平均功率: {summary.get('avgPower', '--')} w")
    print(f"  平均步频: {summary.get('avgCadence', '--')}")
    print(f"  累计上升: {summary.get('elevGain', '--')} m")
    print(f"  累计下降: {summary.get('totalDescent', '--')} m")
    print(f"  训练负荷: {summary.get('trainingLoad', '--')}")
    print(f"  卡路里: {(summary.get('calories', 0) or 0)/1000:.0f} kcal")
    print(f"  等强配速: {format_pace(int(summary.get('adjustedPace', 0) or 0))} /km")
    print(f"  训练重点: {TRAIN_TYPE_MAP.get(summary.get('trainType', 0), '未知')}")

    performance_score = summary.get("displayPerformance", 0) or 0
    performance_state = PERFORMANCE_MAP.get(summary.get("performance", 0), "未知")
    aerobic = summary.get("aerobicEffect", 0)
    aerobic_state = AEROBIC_EFFECT_MAP.get(summary.get("aerobicEffectState", 0), "未知")
    anaerobic = summary.get("anaerobicEffect", 0)
    anaerobic_state = AEROBIC_EFFECT_MAP.get(summary.get("anaerobicEffectState", 0), "未知")
    print(f"\n  🧠 训练效果")
    print(f"  运动表现: {performance_score}% ({performance_state})")
    print(f"  有氧效果: {aerobic} ({aerobic_state})")
    print(f"  无氧效果: {anaerobic} ({anaerobic_state})")
    print(f"  评论: {comments_count} 条消息")
    print(f"  运动感受: {sport_feel_text}")
    
    # 添加更详细的运动数据
    print(f"\n  📈 高级数据分析")
    print(f"  ───────────────────────────────────────")
    
    # 计算心率区间
    avg_hr = summary.get('avgHr', 0) or 0
    max_hr = summary.get('maxHr', 0) or 0
    if avg_hr:
        # 优先使用活动内真实最大心率；缺失时使用保守估计值
        max_hr_estimate = max_hr if max_hr > 0 else 185
        hr_percent = avg_hr / max_hr_estimate * 100 if max_hr_estimate > 0 else 0
        print(f"  平均心率占最大心率: {hr_percent:.0f}%")
        
        # 心率区间
        if hr_percent < 60:
            hr_zone = "Z1 恢复区"
        elif hr_percent < 70:
            hr_zone = "Z2 有氧区"
        elif hr_percent < 80:
            hr_zone = "Z3 有氧上限"
        elif hr_percent < 90:
            hr_zone = "Z4 阈值区"
        else:
            hr_zone = "Z5 最大摄氧量"
        print(f"  当前心率区间: {hr_zone}")
    
    # 步频分析
    avg_cadence = summary.get('avgCadence', 0) or 0
    if avg_cadence:
        if avg_cadence >= 180:
            cadence_level = "✅ 优秀 (高步频)"
        elif avg_cadence >= 170:
            cadence_level = "🟢 良好"
        elif avg_cadence >= 160:
            cadence_level = "🟡 一般"
        else:
            cadence_level = "🔴 偏低"
        print(f"  步频: {avg_cadence} 步/分 {cadence_level}")
    
    # 功率分析
    avg_power = summary.get('avgPower', 0) or 0
    if avg_power:
        if avg_power > 200:
            power_level = "🔥 高"
        elif avg_power > 150:
            power_level = "💪 中等"
        else:
            power_level = "😊 轻松"
        print(f"  平均功率: {avg_power}W ({power_level})")
    
    # 训练负荷分析
    tl = summary.get('trainingLoad', 0) or 0
    if tl:
        if tl > 300:
            tl_level = "🔥 高强度"
        elif tl > 150:
            tl_level = "💪 中等强度"
        else:
            tl_level = "😊 低强度"
        print(f"  训练负荷: {tl} TL ({tl_level})")
    
    print()


def build_simple_running_program(
    id_in_plan: int,
    name: str,
    duration_seconds: int,
    hr_low: int,
    hr_high: int,
    intensity_percent_low: int,
    intensity_percent_high: int,
    source_id: str,
    source_url: str,
) -> Dict:
    """构建单段跑步训练计划（训练页最小可用结构）"""
    return {
        "idInPlan": id_in_plan,
        "name": name,
        "sportType": 1,
        "subType": 0,
        "totalSets": 1,
        "sets": 1,
        "exerciseNum": "",
        "targetType": "",
        "targetValue": "",
        "version": 0,
        "simple": True,
        "exercises": [
            {
                "access": 0,
                "createTimestamp": 1587381919,
                "defaultOrder": 2,
                "equipment": [1],
                "exerciseType": 2,
                "groupId": "",
                "hrType": 3,
                "id": 1,
                "intensityCustom": 2,
                "intensityDisplayUnit": 0,
                "intensityMultiplier": 0,
                "intensityPercent": intensity_percent_low,
                "intensityPercentExtend": intensity_percent_high,
                "intensityType": 2,
                "intensityValue": hr_low,
                "intensityValueExtend": hr_high,
                "isDefaultAdd": 1,
                "isGroup": False,
                "isIntensityPercent": True,
                "name": "T3001",
                "originId": "426109589008859136",
                "overview": "sid_run_training",
                "part": [0],
                "restType": 3,
                "restValue": 0,
                "sets": 1,
                "sortNo": 2,
                "sourceId": "0",
                "sourceUrl": "",
                "sportType": 1,
                "subType": 0,
                "targetDisplayUnit": 0,
                "targetType": 2,
                "targetValue": duration_seconds,
                "userId": 0,
                "videoUrl": "",
            }
        ],
        "access": 1,
        "essence": 0,
        "estimatedTime": 0,
        "originEssence": 0,
        "overview": "",
        "type": 0,
        "unit": 0,
        "pbVersion": 2,
        "sourceId": source_id,
        "sourceUrl": source_url,
        "referExercise": {"intensityType": 0, "hrType": 0, "valueType": 0},
        "poolLengthId": 1,
        "poolLength": 2500,
        "poolLengthUnit": 2,
    }


def patch_existing_running_program(
    base_program: Dict,
    name: str,
    duration_seconds: int,
    hr_low: int,
    hr_high: int,
    intensity_percent_low: int,
    intensity_percent_high: int,
) -> Dict:
    """基于已有 program 修改成新的跑步训练参数（用于 update）"""
    program = copy.deepcopy(base_program)
    if name:
        program["name"] = name

    exercises = program.get("exercises", [])
    target_ex = None
    for ex in exercises:
        if int(ex.get("exerciseType", 0) or 0) == 2:
            target_ex = ex
            break
    if target_ex is None and exercises:
        target_ex = exercises[0]

    if isinstance(target_ex, dict):
        target_ex["targetType"] = 2
        target_ex["targetValue"] = duration_seconds
        target_ex["intensityType"] = 2
        target_ex["intensityValue"] = hr_low
        target_ex["intensityValueExtend"] = hr_high
        target_ex["intensityPercent"] = intensity_percent_low
        target_ex["intensityPercentExtend"] = intensity_percent_high
        target_ex["isIntensityPercent"] = True

    return program


def display_schedule_write_result(result: Dict) -> None:
    """展示日程写入流程结果"""
    print(f"\n{'='*60}")
    print("  🗓️ 日程写入结果")
    print(f"{'='*60}")
    print(f"  操作: {result.get('action', '--')}")
    print(f"  日期: {result.get('date', '--')}")
    print(f"  模式: {'真实写入' if result.get('applied') else '仅预览'}")
    print(f"  名称: {result.get('name', '--')}")
    if result.get("version_object"):
        vo = result["version_object"]
        print(
            f"  删除参数: id={vo.get('id', '--')}, planProgramId={vo.get('planProgramId', '--')}, "
            f"planId={vo.get('planId', '--')}, status={vo.get('status', '--')}"
        )
    if result.get("estimate"):
        est = result["estimate"]
        dist = (est.get("distance", 0) or 0) / 100000
        duration = int(est.get("duration", 0) or 0)
        tl = est.get("trainingLoad", 0) or 0
        print(f"  估算: {format_seconds(duration)} | {dist:.2f}km | {tl}TL")
    if result.get("success") is True:
        print("  结果: ✅ 成功")
    elif result.get("success") is False:
        print("  结果: ❌ 失败")
    else:
        print("  结果: ⚠️ 未执行写入")
    print()


def handle_schedule_write(client: CorosClient, config: Dict, summary_data: Dict = None) -> Optional[Dict]:
    """按配置执行日程新增/更新（默认仅预览）"""
    schedule_cfg = config.get("schedule_write", {})
    action = str(schedule_cfg.get("action", "")).strip().lower()
    if action not in {"add", "update", "delete"}:
        return None

    date = str(schedule_cfg.get("date", "")).strip()
    if len(date) != 8 or not date.isdigit():
        print("  ⚠️ schedule_write.date 需为 YYYYMMDD")
        return {"action": action, "date": date, "success": False, "applied": False}

    name = str(schedule_cfg.get("name", "训练")).strip() or "训练"
    duration_seconds = int(schedule_cfg.get("duration_seconds", schedule_cfg.get("duration", 3900)) or 3900)
    hr_low = int(schedule_cfg.get("hr_low", 167) or 167)
    hr_high = int(schedule_cfg.get("hr_high", 175) or 175)
    intensity_percent_low = int(schedule_cfg.get("intensity_percent_low", 91000) or 91000)
    intensity_percent_high = int(schedule_cfg.get("intensity_percent_high", 95000) or 95000)
    id_in_plan = int(schedule_cfg.get("id_in_plan", 4) or 4)
    auto_apply = bool(schedule_cfg.get("auto_apply", False))

    source_id = str(schedule_cfg.get("source_id", "425868133463670784"))
    source_url = str(
        schedule_cfg.get(
            "source_url",
            "https://oss.coros.com/source/source_default/0/4e4f5f7a165941929af61cb97676f3dc.jpg",
        )
    )

    day_data = client.get_schedule(start_date=date, end_date=date) or {}
    pb_version = int(day_data.get("pbVersion", 2) or 2)
    day_records = filter_records_by_date(get_schedule_records(day_data), date)

    # 兼容旧调用字段：删除/更新时若只传了 name/duration/distance，也能定位目标
    if action in {"delete", "update"}:
        if not schedule_cfg.get("target_name") and schedule_cfg.get("name"):
            schedule_cfg["target_name"] = schedule_cfg.get("name")
        if not schedule_cfg.get("target_duration_seconds") and schedule_cfg.get("duration_seconds"):
            schedule_cfg["target_duration_seconds"] = schedule_cfg.get("duration_seconds")
        if not schedule_cfg.get("target_duration_seconds") and schedule_cfg.get("duration"):
            schedule_cfg["target_duration_seconds"] = schedule_cfg.get("duration")
        if not schedule_cfg.get("target_distance_km"):
            if schedule_cfg.get("distance_km"):
                schedule_cfg["target_distance_km"] = schedule_cfg.get("distance_km")
            elif schedule_cfg.get("distance"):
                # 兼容：distance 传 5 或 5.0 视为 km；传 5000 视为米
                raw_distance = float(schedule_cfg.get("distance") or 0)
                schedule_cfg["target_distance_km"] = raw_distance / 1000 if raw_distance > 100 else raw_distance

    target_record = resolve_target_schedule_record(day_records, schedule_cfg)
    if not target_record and len(day_records) == 1 and bool(schedule_cfg.get("allow_single_candidate_fallback", True)):
        # 兼容旧调用：只剩一条日程时，允许自动兜底命中，避免上游传参与名称模板差异导致删除失败
        target_record = day_records[0]

    selector_info = {
        "target_id_in_plan": str(schedule_cfg.get("target_id_in_plan", "")).strip(),
        "target_plan_program_id": str(schedule_cfg.get("target_plan_program_id", "")).strip(),
        "target_name": str(schedule_cfg.get("target_name", "")).strip(),
        "target_duration_seconds": int(schedule_cfg.get("target_duration_seconds", 0) or 0),
        "target_distance_km": float(schedule_cfg.get("target_distance_km", 0) or 0),
    }

    def to_brief(r: Dict) -> Dict:
        return {
            "idInPlan": r.get("idInPlan"),
            "planProgramId": r.get("planProgramId"),
            "planId": r.get("planId"),
            "name": r.get("name"),
            "duration": r.get("duration"),
            "distance_cm": r.get("distance_cm"),
        }

    candidates = [to_brief(r) for r in sorted(day_records, key=lambda x: int(x.get("idInPlan", "0") or 0))]
    matched_brief = to_brief(target_record) if target_record else None

    if action == "delete":
        explicit_delete_vo = any(
            str(schedule_cfg.get(k, "")).strip() for k in ("id", "plan_program_id", "plan_id")
        )
        if not day_records and not explicit_delete_vo:
            print("  ℹ️ 目标日期无日程，无需删除")
            return {"action": action, "date": date, "success": True, "applied": False}
        if day_records and not target_record:
            print(
                "  ⚠️ 发现多条日程，但未能定位目标，请提供 target_id_in_plan / "
                "target_plan_program_id / target_name / target_distance_km"
            )
            print(f"  选择器: {selector_info}")
            print(f"  候选日程: {candidates}")
            return {"action": action, "date": date, "success": False, "applied": False}
        # 兼容旧调用：命中目标后默认优先使用真实记录参数，而不是上层传入的模板 id
        use_input_vo = bool(schedule_cfg.get("force_use_input_version_object", False))
        if target_record and not use_input_vo:
            version_obj = {
                "id": str(target_record.get("idInPlan", id_in_plan)),
                "planProgramId": str(target_record.get("planProgramId", id_in_plan)),
                "planId": str(target_record.get("planId", "")),
                "status": int(schedule_cfg.get("status", 3) or 3),
            }
        else:
            version_obj = {
                "id": str(schedule_cfg.get("id", target_record.get("idInPlan") if target_record else id_in_plan)),
                "planProgramId": str(schedule_cfg.get("plan_program_id", target_record.get("planProgramId") if target_record else id_in_plan)),
                "planId": str(schedule_cfg.get("plan_id", target_record.get("planId") if target_record else "")),
                "status": int(schedule_cfg.get("status", 3) or 3),
            }
        print(f"  🎯 删除命中: {matched_brief}")
        print(f"  🧾 删除请求摘要: {version_obj}")
        result = {
            "action": action,
            "date": date,
            "name": name,
            "estimate": {},
            "version_object": version_obj,
            "selector": selector_info,
            "matched_target": matched_brief,
            "candidates": candidates,
            "applied": False,
            "success": None,
        }

        if not auto_apply:
            print("  ℹ️ 已生成删除日程预览（schedule_write.auto_apply=false，未写入）")
            return result

        attempt_vos: List[Dict] = [version_obj]
        if target_record:
            # 某些网关对数字/字符串字段较敏感，增加一组 numeric 兼容重试
            try:
                numeric_vo = {
                    "id": int(target_record.get("idInPlan", 0) or 0),
                    "planProgramId": int(target_record.get("planProgramId", 0) or 0),
                    "planId": int(target_record.get("planId", 0) or 0),
                    "status": int(schedule_cfg.get("status", 3) or 3),
                }
                if numeric_vo != version_obj:
                    attempt_vos.append(numeric_vo)
            except (TypeError, ValueError):
                pass

            # 兼容历史调用：如果上层显式传了 id 参数，失败后再尝试一次上层原始版本
            if any(str(schedule_cfg.get(k, "")).strip() for k in ("id", "plan_program_id", "plan_id")):
                legacy_vo = {
                    "id": str(schedule_cfg.get("id", "")),
                    "planProgramId": str(schedule_cfg.get("plan_program_id", "")),
                    "planId": str(schedule_cfg.get("plan_id", "")),
                    "status": int(schedule_cfg.get("status", 3) or 3),
                }
                if legacy_vo not in attempt_vos:
                    attempt_vos.append(legacy_vo)

        ok = False
        for idx, vo in enumerate(attempt_vos, start=1):
            print(f"  🔁 删除尝试#{idx}: {vo}")
            ok = client.update_schedule([], [], [vo], pb_version=pb_version)
            if ok:
                result["version_object"] = vo
                break
            print(f"  ❌ 删除尝试#{idx}失败: {client.last_update_error}")
        result["applied"] = True
        result["success"] = ok

        if ok:
            verify = client.get_schedule(start_date=date, end_date=date) or {}
            verify_records = filter_records_by_date(get_schedule_records(verify), date)
            target_id = str(version_obj.get("id", ""))
            target_exists = any(str(r.get("idInPlan", "")) == target_id for r in verify_records)
            # 删除成功只要求目标记录消失，同日其他记录可保留
            result["success"] = not target_exists
            if target_exists:
                print("  ⚠️ 删除返回成功，但目标日程仍存在")

        return result

    program = build_simple_running_program(
        id_in_plan=id_in_plan,
        name=name,
        duration_seconds=duration_seconds,
        hr_low=hr_low,
        hr_high=hr_high,
        intensity_percent_low=intensity_percent_low,
        intensity_percent_high=intensity_percent_high,
        source_id=source_id,
        source_url=source_url,
    )
    entity = {"happenDay": date, "idInPlan": id_in_plan, "sortNo": 0, "dayNo": 0, "sortNoInPlan": 0, "sortNoInSchedule": 0}

    # update 模式：用已有记录的 idInPlan/排序信息，避免新增一条
    if action == "update":
        if not target_record:
            print("  ⚠️ 更新失败：目标日期无可更新日程")
            print(f"  选择器: {selector_info}")
            print(f"  候选日程: {candidates}")
            return {"action": action, "date": date, "success": False, "applied": False}
        print(f"  🎯 更新命中: {matched_brief}")
        raw_entity = target_record.get("entity", {})
        raw_program = target_record.get("program", {})
        target_id = int(target_record.get("idInPlan", 0) or 0)
        # update 使用已有 program 作为基底，避免非法字段组合
        if raw_program:
            program = patch_existing_running_program(
                raw_program,
                name=name,
                duration_seconds=duration_seconds,
                hr_low=hr_low,
                hr_high=hr_high,
                intensity_percent_low=intensity_percent_low,
                intensity_percent_high=intensity_percent_high,
            )
        program["idInPlan"] = str(target_id)
        entity.update(
            {
                "idInPlan": str(target_id),
                "sortNo": raw_entity.get("sortNo", 0),
                "dayNo": raw_entity.get("dayNo", 0),
                "sortNoInPlan": raw_entity.get("sortNoInPlan", 0),
                "sortNoInSchedule": raw_entity.get("sortNoInSchedule", 0),
            }
        )
        id_in_plan = target_id

    estimate = client.estimate_program(entity, program)
    if estimate:
        program["distance"] = estimate.get("distance", program.get("distance", 0))
        program["duration"] = estimate.get("duration", duration_seconds)
        program["trainingLoad"] = estimate.get("trainingLoad", 0)
        bar = estimate.get("exerciseBarChart", [])
        if bar:
            program["exerciseBarChart"] = bar
            entity["exerciseBarChart"] = bar

    calc = client.calculate_program(program)
    if calc and isinstance(calc, dict):
        # 服务端返回可能包裹 program 字段，也可能直接是 program
        maybe_program = calc.get("program") if isinstance(calc.get("program"), dict) else calc
        if isinstance(maybe_program, dict) and maybe_program.get("exercises"):
            program = maybe_program
            if estimate and estimate.get("exerciseBarChart"):
                program["exerciseBarChart"] = estimate.get("exerciseBarChart")
                entity["exerciseBarChart"] = estimate.get("exerciseBarChart")

    result = {
        "action": action,
        "date": date,
        "name": name,
        "selector": selector_info,
        "matched_target": matched_brief,
        "candidates": candidates,
        "estimate": estimate or {},
        "applied": False,
        "success": None,
    }

    if not auto_apply:
        print("  ℹ️ 已生成日程写入预览（schedule_write.auto_apply=false，未写入）")
        return result

    if action == "update" and target_record:
        version_obj = {
            "id": str(target_record.get("idInPlan", id_in_plan)),
            "planProgramId": str(target_record.get("planProgramId", id_in_plan)),
            "planId": str(target_record.get("planId", "")),
            "status": 1,
        }
    else:
        version_obj = {"id": id_in_plan, "status": 1}
    print(f"  🧾 写入请求摘要: action={action}, versionObject={version_obj}")
    ok = client.update_schedule([entity], [program], [version_obj], pb_version=pb_version)
    result["applied"] = True
    result["success"] = ok

    # COROS 对 update payload 校验较严格；若直改失败，降级为“删旧建新”
    if action == "update" and not ok and target_record and auto_apply:
        print("  ℹ️ 直改失败，尝试删除旧日程后重建新日程...")
        delete_vo = {
            "id": str(target_record.get("idInPlan", "")),
            "planProgramId": str(target_record.get("planProgramId", "")),
            "planId": str(target_record.get("planId", "")),
            "status": 3,
        }
        del_ok = client.update_schedule([], [], [delete_vo], pb_version=pb_version)
        if del_ok:
            add_cfg = {
                "schedule_write": {
                    "action": "add",
                    "date": date,
                    "name": name,
                    "duration_seconds": duration_seconds,
                    "hr_low": hr_low,
                    "hr_high": hr_high,
                    "intensity_percent_low": intensity_percent_low,
                    "intensity_percent_high": intensity_percent_high,
                    "id_in_plan": int(schedule_cfg.get("replace_id_in_plan", id_in_plan + 1) or (id_in_plan + 1)),
                    "source_id": source_id,
                    "source_url": source_url,
                    "auto_apply": True,
                }
            }
            add_res = handle_schedule_write(client, add_cfg, summary_data)
            result["fallback"] = "delete_then_add"
            result["success"] = bool(add_res and add_res.get("success"))
        else:
            result["fallback"] = "delete_then_add_failed"
            result["success"] = False

    if ok:
        verify = client.get_schedule(start_date=date, end_date=date) or {}
        verify_records = filter_records_by_date(get_schedule_records(verify), date)
        if action == "update" and target_record:
            target_id = str(target_record.get("idInPlan", ""))
            updated = next((r for r in verify_records if str(r.get("idInPlan", "")) == target_id), None)
            exists = updated is not None
            if exists:
                # 至少保证目标记录仍在；若提供 name 则校验名称是否更新
                if name and updated.get("name") and updated.get("name") != name:
                    result["success"] = False
                    print("  ⚠️ 更新返回成功，但名称未更新为目标值")
                else:
                    result["success"] = True
            else:
                result["success"] = False
        else:
            exists = has_schedule_on_date(verify, date)
            result["success"] = exists
        if not result["success"]:
            print("  ⚠️ 写入返回成功，但回查未命中目标日期")

    return result


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  🏃 COROS 高驰运动数据获取")
    print("="*60)

    config = load_config()
    coros_config = config.get("coros", {})
    demo_mode = config.get("demo_mode", True)
    account = coros_config.get("account", "")

    client = CorosClient(config)
    p1 = coros_config.get("p1", "")
    p2 = coros_config.get("p2", "")

    if demo_mode:
        print("\n  [配置] 使用演示模式")
        user_info = {"userId": "demo_user", "nickname": "演示用户"}
    elif account and p1 and p2:
        print(f"\n  尝试登录账号: {account} ...")
        if client.login(account, p1, p2):
            print("  ✅ 登录成功!")
            user_info = client.user_info
        else:
            print("  ❌ 登录失败")
            demo_mode = True
            user_info = {"userId": "demo_user", "nickname": "演示用户"}
    else:
        print("\n  [配置] 未配置密码哈希")
        demo_mode = True
        user_info = {"userId": "demo_user", "nickname": "演示用户"}

    if user_info:
        print(f"\n  欢迎, {user_info.get('nickname', '用户')}!")
        print(f"  用户ID: {user_info.get('userId')}")

    if not demo_mode and client.token:
        print("\n  正在获取数据...")

        dashboard_summary = client.get_dashboard_summary()
        cycle_record_data = client.get_dashboard_cycle_record()
        # 拉取 profile/private/query 预留给后续按页面布局动态渲染
        client.get_profile_private()

        dashboard_data = client.get_dashboard_detail()
        if dashboard_data:
            display_dashboard(dashboard_data)
        else:
            print("  ⚠️ 获取 Dashboard 失败")

        if dashboard_summary:
            display_dashboard_summary(dashboard_summary, cycle_record_data)
        else:
            print("  ⚠️ 获取仪表盘高级分析失败")

        activities_data = client.get_activities(page=1, size=20)
        if activities_data:
            display_activities(activities_data)
            list_data = activities_data.get("dataList", []) or activities_data.get("list", [])
            if list_data:
                latest = list_data[0]
                latest_label_id = latest.get("labelId") or latest.get("id")
                latest_sport_type = latest.get("sportType", 100)
                if latest_label_id:
                    detail_data = client.get_activity_detail(str(latest_label_id), int(latest_sport_type))
                    if detail_data:
                        display_activity_detail(detail_data)
                    else:
                        print("  ⚠️ 获取活动详情失败")

        schedule_data = client.get_schedule()
        if schedule_data:
            display_schedule(schedule_data)

        schedule_summary = client.get_schedule_summary()
        if schedule_summary:
            display_schedule_summary(schedule_summary)

        schedule_write_result = handle_schedule_write(client, config, dashboard_summary)
        if schedule_write_result:
            display_schedule_write_result(schedule_write_result)

        print(f"\n{'='*60}")
        print("  ✅ 数据获取成功!")
        print("="*60 + "\n")
    else:
        print("\n  使用演示数据")
        demo_dashboard = {
            "summaryInfo": {"ati": 48, "cti": 71, "trainingLoadRatio": 0.67},
            "sportDataList": [
                {"labelId": "1", "sportType": 100, "duration": 6760, "distance": 18282.41, "avgPace": 370, "avgHeartRate": 171, "trainingLoad": 298, "happenDay": 20260321},
                {"labelId": "2", "sportType": 100, "duration": 870, "distance": 2113.39, "avgPace": 412, "avgHeartRate": 146, "trainingLoad": 9, "happenDay": 20260313},
                {"labelId": "3", "sportType": 100, "duration": 2539, "distance": 6791.64, "avgPace": 374, "avgHeartRate": 152, "trainingLoad": 40, "happenDay": 20260311},
            ],
        }
        display_dashboard(demo_dashboard)


if __name__ == "__main__":
    main()
