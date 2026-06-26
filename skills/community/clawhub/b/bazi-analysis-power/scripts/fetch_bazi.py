#!/usr/bin/env python3
"""
八字排盘 skill 实现
用于在用户未提供完整排盘信息时，作为兜底工具调用 API 获取四柱。
"""

import sys
import json
import urllib.request
from datetime import datetime, timezone, timedelta

API_URL = "https://yoebao.com/bazi/api/bazi.php"
SHISHEN = ["比劫", "比劫", "食伤", "食伤", "财", "财", "官杀", "官杀", "印绶", "印绶"]


def configure_stdio():
    """Prefer UTF-8 for piped stdin/stdout on Windows terminals."""
    for stream_name in ("stdin", "stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


def normalize_sex(value):
    value = value.strip().lower()
    male_values = {"男", "男性", "male", "m", "0"}
    female_values = {"女", "女性", "female", "f", "1"}
    if value in male_values:
        return 0
    if value in female_values:
        return 1
    return None


def summarize_yuns(yuns):
    summaries = []
    for yun in yuns:
        text = yun.get("text", "")
        start = yun.get("start")
        end = yun.get("end")
        start_age = yun.get("start_age")
        summaries.append({
            "text": text,
            "start": start,
            "end": end,
            "start_age": start_age,
        })
    return summaries


def find_current_yun(yuns, current_year):
    for yun in yuns:
        start = yun.get("start")
        end = yun.get("end")
        if isinstance(start, int) and isinstance(end, int) and start <= current_year <= end:
            return yun
    return None

def call_bazi_api(birth_date, birth_time, sex):
    try:
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        beijing_tz = timezone(timedelta(hours=8))
        dt = dt.replace(tzinfo=beijing_tz)
        timestamp = int(dt.timestamp())

        url = f"{API_URL}?do=bytime&sex={sex}&timestamp={timestamp}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            
        data = json.loads(result)
        if data.get('status') != 'ok':
            return None, None, None, None, None, "API 返回错误"

        bazi = data['data']['info']['bazi']
        yun_desc = data.get('data', {}).get('info', {}).get('yun_desc')
        sex_value = data['data']['info']['sex']
        yuns = data.get('data', {}).get('yuns', [])

        shishen = ""
        try:
            base = data.get('data', {}).get('base', [])
            if len(base) > 1:
                alias = base[1].get('zhi', {}).get('vector', {}).get('alias', 0)
                shishen = SHISHEN[alias]
        except Exception:
            pass

        detail_url = f"https://yoebao.com/bazi/detail.html?sex={sex_value}&timestamp={timestamp * 1000}"
        return bazi, yuns, shishen, detail_url, yun_desc, None

    except Exception as e:
        return None, None, None, None, None, f"调用或解析失败: {str(e)}"

def main():
    configure_stdio()
    input_str = sys.stdin.read().strip()
    if not input_str:
        print("请提供出生日期和时间。格式: 排出八字 2020-01-01 12:00 男")
        return
    
    input_str = input_str.replace("排出八字", "").strip()
    parts = input_str.split()
    
    if len(parts) < 3:
        print("错误: 格式错误，请使用: 排出八字 2020-01-01 12:00 男")
        return
        
    birth_date, birth_time = parts[0], parts[1]
    sex_str = parts[2]
    sex = normalize_sex(sex_str)
    
    if sex is None:
        print("错误: 性别参数错误，请使用男/女")
        return

    bazi, yuns, shishen, url, yun_desc, error = call_bazi_api(birth_date, birth_time, sex)
    if error:
        print(f"错误: {error}")
        return
        
    sex_name = "乾造" if sex == 0 else "坤造"
    sex_display = "男" if sex == 0 else "女"

    print(f"出生：{birth_date} {birth_time} {sex_display}")
    print(f"{sex_name}：{bazi}")

    yun_summaries = summarize_yuns(yuns)
    if yuns:
        current_year = datetime.now(timezone(timedelta(hours=8))).year
        current_yun = find_current_yun(yuns, current_year)
        dayun_str = " ".join(yun.get("text", "") for yun in yuns if yun.get("text"))

        if yun_desc:
            print(f"起运：{yun_desc}")
        first_yun = yun_summaries[0]
        print(
            f"首步大运：{first_yun['text']} "
            f"({first_yun['start']}-{first_yun['end']}, {first_yun['start_age']}岁起)"
        )
        if current_yun:
            print(
                f"当前大运：{current_yun.get('text', '未知')} "
                f"({current_yun.get('start')}-{current_yun.get('end')}, {current_year}年)"
            )
        print(f"大运列表：{dayun_str}")
        print("大运分段：")
        for yun in yun_summaries:
            print(
                f"- {yun['text']}：{yun['start']}-{yun['end']}"
                f"（{yun['start_age']}岁起）"
            )
    if shishen:
        print(f"十神：{shishen}")
    print(f"\n[点击这里访问详细排盘]({url})")

if __name__ == "__main__":
    main()
