#!/usr/bin/env python3
"""
中国天气网天气预报查询工具 (weather.com.cn) 
1. 零第三方依赖：纯原生的 urllib 解析，无需 pip install 任何东西。
2. 动态城市代码：优先从同目录 citys.txt 读取，找不到自动去网上搜！
3. 智能参数解析：支持直接输入城市名，也支持指定输出格式(json/query)。
"""
import os
import re
import sys
import json
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from datetime import datetime


class WeatherHTMLParser(HTMLParser):
    """解析天气页面HTML，提取7天预报和生活指数数据。"""

    def __init__(self):
        super().__init__()
        self._capture = False
        self._target_id = None
        self._depth = 0
        self._data_parts = []
        self._result = ""

    def extract(self, html, target_id):
        """提取指定id的div内容。"""
        self._capture = False
        self._target_id = target_id
        self._depth = 0
        self._data_parts = []
        self._result = ""
        self.feed(html)
        return self._result

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "div" and attrs_dict.get("id") == self._target_id:
            self._capture = True
            self._depth = 1
            return
        if self._capture and tag == "div":
            self._depth += 1
        if self._capture:
            attr_str = " ".join(f'{k}="{v}"' for k, v in attrs)
            self._data_parts.append(f"<{tag} {attr_str}>" if attr_str else f"<{tag}>")

    def handle_endtag(self, tag):
        if self._capture:
            self._data_parts.append(f"</{tag}>")
            if tag == "div":
                self._depth -= 1
                if self._depth <= 0:
                    self._capture = False
                    self._result = "".join(self._data_parts)

    def handle_data(self, data):
        if self._capture:
            self._data_parts.append(data)


class ChinaWeather:
    """中国天气网天气查询核心类。"""

    # 城市在线搜索API
    SEARCH_URL = "https://toy1.weather.com.cn/search?cityname={query}&callback=success_jsonpCallback&_={ts}"

    # 天气预报页面URL
    WEATHER_URL = "https://www.weather.com.cn/weather/{code}.shtml"

    # 请求超时（秒）
    REQUEST_TIMEOUT = 15

    # 伪装成正常浏览器的请求头
    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.weather.com.cn/",
    }

    # 生活指数名称映射（为了让AI或者JSON看着更顺眼）
    LIFE_INDEX_NAMES = {
        "感冒": "cold",
        "运动": "exercise",
        "过敏": "allergy",
        "穿衣": "clothing",
        "洗车": "carwash",
        "紫外线": "uv",
        "钓鱼": "fishing",
        "旅游": "travel",
        "晾晒": "drying",
        "交通": "traffic",
        "防晒": "sunscreen",
    }

    def __init__(self):
        self._parser = WeatherHTMLParser()
        # 把小本本的路径存下来，方便后面随时往里加新城市
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.codes_file_path = os.path.join(script_dir, "citys.txt")
        # 初始化时加载我们的“小本本”
        self.preset_cities = self._load_preset_cities()

    def _load_preset_cities(self):
        """从同目录下的 citys.txt 读取城市代码"""
        cities = {}
        
        # 如果小本本丢了，也不慌，返回空字典，一会儿靠在线搜
        if not os.path.exists(self.codes_file_path):
            return cities
            
        try:
            with open(self.codes_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和注释行（#开头的）
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split(',')
                    if len(parts) >= 2:
                        city_name, city_code = parts[0].strip(), parts[1].strip()
                        cities[city_name] = city_code
        except Exception as e:
            # 读取失败只给个温柔的警告
            print(f"⚠️ 警告: 读取 citys.txt 时打了个喷嚏 ({e})，将完全依赖在线搜索。", file=sys.stderr)
            
        return cities

    def _save_new_city(self, city_name, city_code):
        """记仇（划掉）记笔记专用：把新搜到的城市代码自动写进小本本"""
        try:
            # 用 'a' (append) 追加模式打开文件，新城市悄悄写在文件末尾
            with open(self.codes_file_path, 'a', encoding='utf-8') as f:
                f.write(f"{city_name},{city_code}\n")
            # 顺手把内存里的字典也更新了，保证程序还没退出时也能立刻生效
            self.preset_cities[city_name] = city_code
        except Exception:
            # 万一遇到没权限写文件之类的幺蛾子，咱们就闷声发大财，不抛错吓唬人
            pass

    def _http_get(self, url, encoding="utf-8"):
        """发送HTTP GET请求 (原生urllib，免装requests的秘诀就在这)"""
        req = urllib.request.Request(url, headers=self.REQUEST_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=self.REQUEST_TIMEOUT) as resp:
                return resp.read().decode(encoding, errors="replace")
        except Exception as e:
            raise ConnectionError(f"HTTP请求失败: {url} - {e}")

    def search_city(self, city_name):
        """通过中国天气网的搜索API，在线“肉搜”城市代码。"""
        encoded = urllib.parse.quote(city_name)
        ts = int(datetime.now().timestamp() * 1000)
        url = self.SEARCH_URL.format(query=encoded, ts=ts)

        try:
            text = self._http_get(url)
        except ConnectionError:
            return None

        # 解析那种古老的 JSONP 格式数据
        match = re.search(r"success_jsonpCallback\((\[.*\])\)", text, re.DOTALL)
        if not match:
            return None

        try:
            results = json.loads(match.group(1))
        except json.JSONDecodeError:
            return None

        if not results:
            return None

        # 取第一个结果，中国天气网的格式是: "代码~省份~城市名~英文名~..."
        ref = results[0].get("ref", "")
        parts = ref.split("~")
        if len(parts) >= 3:
            code = parts[0]
            display_name = parts[2]
            # 确保抓回来的是正经的9位城市代码（101开头）
            if re.match(r"^101\d{6}$", code):
                return (code, display_name)

        return None

    def get_city_code(self, city_name):
        """获取城市代码：本地TXT没有？那就去网上找！"""
        city_name = city_name.strip()

        # 1. 优先翻本地小本本
        if city_name in self.preset_cities:
            return (self.preset_cities[city_name], city_name)

        # 2. 小本本里没有，在线搜！
        result = self.search_city(city_name)
        if result:
            code, display_name = result
            # 3. 抓到野生城市啦！赶紧拿小本本记下来！
            self._save_new_city(city_name, code)
            
            # 买一送一：有时候你搜“朝阳”，官方全名叫“北京朝阳”，把全名也存一份，防患于未然
            if display_name != city_name:
                self._save_new_city(display_name, code)
                
            return result

        raise ValueError(f"未找到城市: {city_name} (本地和网络都没找到，你是不是输入了外星城市？)")

    def fetch_weather_html(self, city_code):
        """获取天气预报页面HTML。"""
        url = self.WEATHER_URL.format(code=city_code)
        return self._http_get(url)

    def parse_7day_forecast(self, html):
        """解析7天天气预报数据。"""
        block = self._parser.extract(html, "7d")
        if not block:
            return []

        # 偷看隐藏的标题数据，专治中国天气网“一到晚上就隐藏今天最高温”的坏习惯
        hidden_high, hidden_low = "", ""
        m_hidden = re.search(r'<input[^>]*id="hidden_title"[^>]*value="([^"]+)"', block)
        if m_hidden:
            # 提取类似 "03月19日20时 周四 小雨转中雨 10/13°C" 中的 10/13°C
            m_temp = re.search(r'(-?\d+)/(-?\d+)°?[Cc]', m_hidden.group(1))
            if m_temp:
                t1, t2 = int(m_temp.group(1)), int(m_temp.group(2))
                hidden_high = f"{max(t1, t2)}℃"
                hidden_low = f"{min(t1, t2)}℃"

        forecasts = []
        li_blocks = re.findall(r'<li[^>]*>(.*?)</li>', block, re.DOTALL)

        for i, li in enumerate(li_blocks):
            m_date = re.search(r'<h1>([^<]+)</h1>', li)
            if not m_date:
                continue

            day = {
                "date": m_date.group(1).strip(),
                "weather": "",
                "temp_high": "",
                "temp_low": "",
                "wind": "",
                "wind_level": "",
            }

            m = re.search(r'<p\s+title="([^"]*)"[^>]*class="wea"', li)
            if m:
                day["weather"] = m.group(1).strip()
            else:
                m = re.search(r'class="wea"[^>]*>([^<]+)<', li)
                if m:
                    day["weather"] = m.group(1).strip()

            # 顺手加上了对零下温度(-号)的支持，不然东北老铁该挨冻了
            m = re.search(r'<span>(-?\d+)℃?</span>', li)
            if m:
                day["temp_high"] = m.group(1) + "℃"
            m = re.search(r'<i>(-?\d+)℃</i>', li)
            if m:
                day["temp_low"] = m.group(1) + "℃"

            # 如果是今天（第1个li），且最高温或最低温缺勤，就用刚才偷看的隐藏数据顶上
            if i == 0:
                if not day["temp_high"] and hidden_high:
                    day["temp_high"] = hidden_high
                if not day["temp_low"] and hidden_low:
                    day["temp_low"] = hidden_low

            m = re.search(r'<span\s+title="([^"]*)"[^>]*class="[A-Z]', li)
            if m:
                day["wind"] = m.group(1).strip()

            m = re.search(r'</em>\s*<i>([^<]+)</i>', li)
            if m:
                day["wind_level"] = m.group(1).strip()

            forecasts.append(day)

        return forecasts

    def parse_life_indices(self, html):
        """解析生活指数数据。"""
        block = self._parser.extract(html, "livezs")
        if not block:
            return []

        indices = []
        li_blocks = re.findall(r'<li[^>]*>(.*?)</li>', block, re.DOTALL)

        for li in li_blocks:
            m_level = re.search(r'<span>([^<]+)</span>', li)
            m_name = re.search(r'<em>([^<]+)</em>', li)
            m_desc = re.search(r'<p>([^<]+)</p>', li)

            if not (m_level and m_name):
                continue

            level = m_level.group(1).strip()
            name = m_name.group(1).strip()
            desc = m_desc.group(1).strip() if m_desc else ""

            index_type = name.replace("指数", "").strip()
            key = self.LIFE_INDEX_NAMES.get(index_type, index_type)

            indices.append({
                "name": name,
                "key": key,
                "level": level,
                "description": desc,
            })

        return indices

    def query(self, city_name):
        """一键打包天气预报和生活指数。"""
        code, display_name = self.get_city_code(city_name)
        html = self.fetch_weather_html(code)

        forecast = self.parse_7day_forecast(html)
        life_indices = self.parse_life_indices(html)

        # 把生活指数揉进每天的预报里
        if forecast and life_indices:
            num_days = len(forecast)
            indices_per_day = len(life_indices) // num_days if num_days > 0 else 0
            if indices_per_day > 0:
                for i, day in enumerate(forecast):
                    start = i * indices_per_day
                    end = start + indices_per_day
                    day["life_indices"] = life_indices[start:end]
            else:
                forecast[0]["life_indices"] = life_indices
        
        return {
            "city": display_name,
            "city_code": code,
            "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "weather.com.cn",
            "forecast": forecast,
        }

    def format_output(self, data):
        """格式化为适合人类（和AI）阅读的文本。"""
        if "error" in data:
            return f"错误: {data['error']}"

        lines = [
            f"城市: {data['city']} (代码: {data['city_code']})",
            f"数据来源: {data['source']}",
            f"查询时间: {data['query_time']}",
        ]

        for day in data.get("forecast", []):
            lines.append("")
            temp = f"{day['temp_high']}/{day['temp_low']}" if day.get("temp_high") else day.get("temp_low", "")
            wind_info = f"{day['wind']} {day['wind_level']}" if day.get("wind") else ""
            lines.append(f"[{day['date']}] {day['weather']}, {temp}, {wind_info}".rstrip(", "))

            for idx in day.get("life_indices", []):
                lines.append(f"  {idx['name']}: {idx['level']} - {idx['description']}")

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("💡 用法超简单:")
        print("  python weather_cn.py [-json] [-today] [-life] <城市名>")
        print("\n参数说明:")
        print("  -json   : 输出 JSON 格式 (给AI或程序看)")
        print("  -today  : 只查当天的详细天气")
        print("  -life   : 附加输出生活指数 (洗车、穿衣等建议，默认不显示)")
        print("\n举个栗子🌰:")
        print("  python weather_cn.py 南京              # 查南京7天天气 (界面清爽无生活指数)")
        print("  python weather_cn.py -today -life 深圳 # 查深圳今天天气，顺便看看能不能洗车")
        print("  python weather_cn.py -json -life 北京  # 查北京详细天气并输出 JSON")
        sys.exit(1)

    weather = ChinaWeather()
    
    args = sys.argv[1:]
    is_json = False
    is_today = False
    is_life = False
    city_parts = []

    # 智能分拣参数：无论参数怎么乱序排，我都认得出来！
    for arg in args:
        if arg.lower() == '-json':
            is_json = True
        elif arg.lower() == '-today':
            is_today = True
        elif arg.lower() == '-life':
            is_life = True
        else:
            # 剩下的全都认为是城市名
            city_parts.append(arg)

    city = " ".join(city_parts)

    if not city:
        print("❌ 错误: 找遍了参数也没看到城市名，你是不是忘了写啊喂！", file=sys.stderr)
        sys.exit(1)

    try:
        data = weather.query(city)
        
        # 如果只要今天的，就把后面6天的数据“无情裁员”掉
        if is_today and "forecast" in data and len(data["forecast"]) > 0:
            data["forecast"] = [data["forecast"][0]]

        # 核心逻辑：如果没带 -life 参数，就把生活指数这部分“包袱”扔掉，保你界面清爽
        if not is_life and "forecast" in data:
            for day in data["forecast"]:
                day.pop("life_indices", None)

        # 根据是否带了 -json 开关来决定输出格式
        if is_json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(weather.format_output(data))
            
    except ValueError as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"📡 网络错误: {e} (快检查下你的网线是不是被猫咬断了)", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"💥 未知错误: {e} (完了，遇到知识盲区了)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()