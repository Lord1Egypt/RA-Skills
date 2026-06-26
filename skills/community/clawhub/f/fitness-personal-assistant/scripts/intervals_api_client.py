#!/usr/bin/env python3
"""
Intervals.icu API Client - Python 完整实现
基于官方 API 文档：https://forum.intervals.icu/t/intervals-icu-api-integration-cookbook/80090

功能：
- 查询运动员摘要 (fitness/fatigue/TSB)
- 查询/上传健康数据 (wellness)
- 查询/上传活动记录 (activities)
- 自动错误处理和重试
- 配置文件不存在时引导创建
"""

import json
import os
import sys
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
# ================= 配置 =================
BASE_URL = "https://intervals.icu/api/v1"
DEFAULT_STORAGE_PATH = Path(__file__).parent.parent / "config"
STORAGE_PATH = Path(os.environ.get("BODY_MANAGEMENT_DATA", DEFAULT_STORAGE_PATH))
CONFIG_FILE = STORAGE_PATH / "config.json"

# ================= 数据类 =================
@dataclass
class WellnessData:
    """健康数据结构"""
    date: str  # ISO-8601 date (YYYY-MM-DD)
    weight: Optional[float] = None  # kg
    resting_hr: Optional[int] = None  # bpm
    hrv: Optional[float] = None  # ms
    steps: Optional[int] = None
    sleep_secs: Optional[int] = None  # seconds
    vo2max: Optional[float] = None
    locked: bool = False  # 锁定数据防止被同步覆盖

@dataclass
class ActivitySummary:
    """活动摘要数据结构"""
    id: str
    name: str
    start_date_local: str
    type: str
    duration: float  # seconds
    distance: float  # meters
    calories: float
    category: str

# ================= API 客户端 =================
class IntervalsICUClient:
    """Intervals.icu API 客户端"""
    
    def __init__(self, athlete_id: str, api_key: str, max_retries: int = 3):
        self.athlete_id = athlete_id
        self.api_key = api_key
        self.max_retries = max_retries
        self.session = requests.Session()
        # 使用 Basic Auth: API_KEY:<api_key>
        self.session.auth = ("API_KEY", api_key)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """通用请求方法，带重试和错误处理"""
        url = f"{BASE_URL}{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, timeout=10, **kwargs)
                
                if response.status_code == 403:
                    print(f"❌ API 认证失败 (403): API key 可能已失效", file=sys.stderr)
                    return None
                elif response.status_code == 404:
                    print(f"⚠️ 资源未找到 (404): {endpoint}", file=sys.stderr)
                    return {}
                elif response.status_code >= 500:
                    print(f"⚠️ 服务器错误 ({response.status_code})，重试中... ({attempt + 1}/{self.max_retries})", file=sys.stderr)
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                elif response.status_code not in [200, 201, 204]:
                    print(f"⚠️ 意外状态码：{response.status_code}", file=sys.stderr)
                    return None
                
                # 204 No Content 或空响应
                if response.status_code == 204 or not response.content:
                    return {}
                
                return response.json()
                
            except requests.exceptions.Timeout:
                print(f"⚠️ 请求超时，重试中... ({attempt + 1}/{self.max_retries})", file=sys.stderr)
                time.sleep(2 ** attempt)
            except requests.exceptions.RequestException as e:
                print(f"❌ 请求失败：{e}", file=sys.stderr)
                return None
        
        print(f"❌ 请求失败：达到最大重试次数", file=sys.stderr)
        return None
    
    def get_athlete_summary(self) -> Optional[Dict]:
        """获取运动员摘要 (fitness/fatigue/TSB)"""
        endpoint = f"/athlete/{self.athlete_id}/athlete-summary"
        result = self._request("GET", endpoint)
        
        # API 返回数组，取第一个匹配的元素
        if isinstance(result, list):
            for item in result:
                if item.get("athlete_id") == self.athlete_id:
                    return item
            return result[0] if result else {}
        return result
    
    def get_wellness(self, date: str) -> Optional[Dict]:
        """获取指定日期的健康数据"""
        endpoint = f"/athlete/{self.athlete_id}/wellness/{date}"
        result = self._request("GET", endpoint)
        
        if isinstance(result, list):
            return result[0] if result else {}
        return result
    
    def get_wellness_range(self, oldest: str, newest: str) -> Optional[List[Dict]]:
        """获取日期范围内的健康数据"""
        endpoint = f"/athlete/{self.athlete_id}/wellness?oldest={oldest}&newest={newest}"
        result = self._request("GET", endpoint)
        return result if isinstance(result, list) else []
    
    def update_wellness(self, date: str, data: Dict, locked: bool = False) -> bool:
        """更新健康数据（单个日期）"""
        endpoint = f"/athlete/{self.athlete_id}/wellness/{date}"
        payload = data.copy()
        payload["locked"] = locked
        
        result = self._request("PUT", endpoint, json=payload)
        return result is not None
    
    def update_wellness_bulk(self, records: List[Dict]) -> bool:
        """批量更新健康数据"""
        endpoint = f"/athlete/{self.athlete_id}/wellness-bulk"
        result = self._request("PUT", endpoint, json=records)
        return result is not None
    
    def get_activities(self, oldest: str, newest: str) -> Optional[List[Dict]]:
        """获取活动列表"""
        endpoint = f"/athlete/{self.athlete_id}/activities?oldest={oldest}&newest={newest}"
        result = self._request("GET", endpoint)
        return result if isinstance(result, list) else []
    
    def get_activity_detail(self, activity_id: str) -> Optional[Dict]:
        """获取活动详情"""
        endpoint = f"/athlete/{self.athlete_id}/activities/{activity_id}"
        return self._request("GET", endpoint)
    
    def upload_activity(self, file_path: str, name: Optional[str] = None, 
                       description: Optional[str] = None, 
                       external_id: Optional[str] = None) -> bool:
        """上传活动文件（FIT/GPX/TCX）"""
        endpoint = f"/athlete/{self.athlete_id}/activities"
        
        # 构建 URL 参数
        params = {}
        if name:
            params["name"] = name
        if description:
            params["description"] = description
        if external_id:
            params["external_id"] = external_id
        
        # multipart/form-data 上传
        files = {"file": open(file_path, "rb")}
        
        # 需要临时移除 Content-Type 让 requests 自动设置
        headers = self.session.headers.copy()
        headers.pop("Content-Type", None)
        
        response = self.session.post(
            f"{BASE_URL}{endpoint}",
            params=params,
            files=files,
            headers=headers,
            timeout=30
        )
        
        files["file"].close()
        return response.status_code in [200, 201]
    
    def test_connection(self) -> bool:
        """测试 API 连接"""
        result = self.get_athlete_summary()
        return result is not None and "fitness" in result


# ================= 工具函数 =================

def load_config() -> Optional[Dict]:
    """加载配置文件，如果不存在则引导创建"""
    if not CONFIG_FILE.exists():
        print(f"⚠️ 配置文件未找到：{CONFIG_FILE}")
        print("\n🔧 正在帮您初始化配置...")
        return None
    
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误：{e}")
        return None
    except Exception as e:
        print(f"❌ 读取配置文件失败：{e}")
        return None

def prompt_for_credentials() -> Optional[Tuple[str, str]]:
    """交互式提示用户输入 credentials"""
    print("\n" + "=" * 50)
    print("🔐 配置 Intervals.icu API 凭证")
    print("=" * 50)
    print("\n请先注册账号：https://intervals.icu/register")
    print("获取凭证：Settings → API Keys\n")
    
    while True:
        athlete_id = input("请输入 Athlete ID (例如：iXXXXXXXXX): ").strip()
        if athlete_id and athlete_id.startswith('i'):
            break
        print("❌ Athlete ID 格式不正确，应该以 'i' 开头")
    
    api_key = input("请输入 API Key: ").strip()
    if not api_key:
        print("❌ API Key 不能为空")
        return None
    
    # 验证凭证
    try:
        test_client = IntervalsICUClient(athlete_id, api_key)
        if test_client.test_connection():
            print("✅ 凭证验证成功！")
        else:
            print("❌ 凭证无效，API 连接失败")
            return None
    except Exception as e:
        print(f"❌ 验证失败：{e}")
        return None
    
    # 保存配置
    config = {
        "intervals_icu": {
            "athlete_id": athlete_id,
            "api_key": api_key
        }
    }
    
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    os.chmod(CONFIG_FILE, 0o600)
    print(f"\n✅ 配置已保存到：{CONFIG_FILE}")
    print("=" * 50 + "\n")
    
    return athlete_id, api_key

def create_client() -> Optional[IntervalsICUClient]:
    """从配置创建 API 客户端，如果配置缺失则引导创建"""
    config = load_config()
    
    if not config:
        credentials = prompt_for_credentials()
        if not credentials:
            print("❌ 无法创建 API 客户端")
            return None
        
        # 重新加载新创建的配置
        config = load_config()
        if not config:
            return None
    
    intervals_config = config.get("intervals_icu", {})
    athlete_id = intervals_config.get("athlete_id")
    api_key = intervals_config.get("api_key")
    
    if not athlete_id or not api_key:
        print("❌ 配置不完整：缺少 athlete_id 或 api_key")
        credentials = prompt_for_credentials()
        if not credentials:
            return None
        
        config = load_config()
        intervals_config = config.get("intervals_icu", {})
        athlete_id = intervals_config.get("athlete_id")
        api_key = intervals_config.get("api_key")
    
    return IntervalsICUClient(athlete_id, api_key)


# ================= 主程序 =================

def main():
    """主程序入口"""
    print("\n" + "=" * 50)
    print("🏋️ Intervals.icu API 客户端测试")
    print("=" * 50 + "\n")
    
    # 创建客户端
    client = create_client()
    if not client:
        sys.exit(1)
    
    # 测试连接
    print("🔍 测试 API 连接...")
    if not client.test_connection():
        print("❌ API 连接失败，请检查配置")
        sys.exit(1)
    print("✅ API 连接成功\n")
    
    # 获取运动员摘要
    print("📊 获取运动员摘要...")
    summary = client.get_athlete_summary()
    if summary:
        print(f"  体能 (fitness): {summary.get('fitness', 'N/A')}")
        print(f"  疲劳 (fatigue): {summary.get('fatigue', 'N/A')}")
        print(f"  形态 (form/TSB): {summary.get('form', 'N/A')}")
        print(f"  RAMP 速率：{summary.get('rampRate', 'N/A')}")
    else:
        print("  ⚠️ 无法获取摘要数据")
    
    # 获取今日健康数据
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n💤 获取今日 ({today}) 健康数据...")
    wellness = client.get_wellness(today)
    if wellness:
        print(f"  HRV: {wellness.get('hrv', 'N/A')} ms")
        print(f"  静息心率：{wellness.get('restingHR', 'N/A')} bpm")
        print(f"  睡眠：{wellness.get('sleepSecs', 'N/A')} 秒")
        print(f"  步数：{wellness.get('steps', 'N/A')}")
    else:
        print("  ⚠️ 无今日健康数据")
    
    # 获取近 7 天活动
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    print(f"\n🏃 获取近 7 天活动 ({start_date} 至 {today})...")
    activities = client.get_activities(start_date, today)
    if activities:
        print(f"  找到 {len(activities)} 次活动:")
        for act in activities[-5:]:  # 最近 5 次
            name = act.get("name", "Unnamed")
            type_ = act.get("type", "Unknown")
            start = act.get("start_date_local", "")[:10]
            duration = act.get("duration") or 0
            distance = (act.get("distance") or 0) / 1000  # 米转公里
            calories = act.get("calories") or 0
            
            dur_str = f"{duration/60:.0f}分钟" if duration > 0 else "未知"
            dist_str = f"{distance:.1f}km" if distance > 0 else ""
            cal_str = f"{calories:.0f}kcal" if calories > 0 else ""
            
            print(f"    [{start}] {type_}: {name}")
            print(f"           {dur_str} | {dist_str} | {cal_str}")
    else:
        print("  ⚠️ 无活动记录")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
