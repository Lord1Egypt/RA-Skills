#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成施工日志（日报格式）
"""

import argparse
from datetime import datetime


def generate_daily_log(date, weather, temperature, workers, tasks, 
                       materials=None, issues=None, output_path=None):
    """生成施工日志"""
    
    today = datetime.now().strftime("%Y年%m月%d日")
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    weekday = date_obj.strftime("%A")
    
    # 天气描述
    weather_desc = {
        "晴": "☀️ 晴",
        "多云": "⛅ 多云",
        "阴": "☁️ 阴",
        "小雨": "🌧️ 小雨",
        "中雨": "🌧️ 中雨",
        "大雨": "⛈️ 大雨",
        "雪": "❄️ 雪"
    }.get(weather, f"️ {weather}")
    
    log = f"""# 施工日志

## 基本信息
- **日期**: {today} ({weekday})
- **天气**: {weather_desc}
- **温度**: {temperature if temperature else 'N/A'}°C
- **记录人**: [待填写]

---

## 人员出勤
- **管理人员**: [待填写] 人
- **作业人员**: {workers if workers else 'N/A'} 人
- **合计**: [待填写] 人

---

## 今日施工内容

{tasks if tasks else '【待填写今日完成的主要工作内容】'}

---

## 材料进场

| 材料名称 | 规格型号 | 单位 | 数量 | 使用部位 | 备注 |
|---------|---------|------|------|---------|------|
| [示例] 钢筋 | HRB400 Φ25 | 吨 | 5.0 | 基础工程 | 已复检 |
| [示例] 混凝土 | C30 | m³ | 50 | 基础浇筑 | 商混 |

{materials if materials else ''}

---

## 机械设备

| 设备名称 | 型号 | 数量 | 工作内容 | 运行状态 |
|---------|------|------|---------|---------|
| [示例] 塔吊 | QTZ80 | 1 台 | 材料吊运 | 正常 |
| [示例] 挖掘机 | PC200 | 1 台 | 土方开挖 | 正常 |

---

## 质量安全情况

### 质量检查
- [ ] 钢筋工程验收
- [ ] 模板工程验收
- [ ] 混凝土浇筑旁站
- [ ] 其他：[待填写]

### 安全检查
- [ ] 临边防护检查
- [ ] 临时用电检查
- [ ] 机械设备检查
- [ ] 消防安全检查

### 发现问题及整改
{issues if issues else '今日无重大质量安全问题'}

---

## 明日计划

1. [待填写明日工作计划]
2. [待填写]
3. [待填写]

---

## 备注事项

[待填写需要特别说明的事项]

---

**记录时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(log)
        print(f"✓ 施工日志已生成：{output_path}")
    
    return log


def main():
    parser = argparse.ArgumentParser(description="生成施工日志")
    parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    parser.add_argument("--weather", default="晴", help="天气")
    parser.add_argument("--temperature", type=int, help="温度 (°C)")
    parser.add_argument("--workers", type=int, help="作业人数")
    parser.add_argument("--tasks", help="今日施工内容")
    parser.add_argument("--output", default="daily_log.md", help="输出文件路径")
    
    args = parser.parse_args()
    
    generate_daily_log(
        date=args.date,
        weather=args.weather,
        temperature=args.temperature,
        workers=args.workers,
        tasks=args.tasks,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
