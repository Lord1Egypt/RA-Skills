#!/usr/bin/env python3
"""
日记生成脚本
将用户回答整合成散文式日记
"""

import os
import json
import datetime
from pathlib import Path

def create_journal_structure(date_str=None):
    """创建日记目录结构"""
    if date_str is None:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    year_month = date_obj.strftime("%Y-%m")
    
    # 创建目录
    base_dir = Path("journals") / year_month
    images_dir = base_dir / "images"
    thumbs_dir = images_dir / "thumbnails"
    
    for directory in [base_dir, images_dir, thumbs_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    return {
        "base_dir": str(base_dir),
        "images_dir": str(images_dir),
        "thumbs_dir": str(thumbs_dir),
        "journal_path": str(base_dir / f"{date_str}.md")
    }

def generate_prose_diary(answers, date_str=None):
    """
    根据用户回答生成散文式日记
    
    Args:
        answers: dict, 用户回答，键为问题类别，值为回答内容
        date_str: str, 日期字符串，格式为YYYY-MM-DD
    
    Returns:
        str: 生成的Markdown格式日记
    """
    if date_str is None:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][date_obj.weekday()]
    
    # 提取基本信息
    mood = answers.get("mood", "平静")
    mood_score = answers.get("mood_score", 5)
    weather = answers.get("weather", "未知")
    
    # 开始生成散文
    prose_parts = []
    
    # 开头段落
    prose_parts.append(f"# {date_str} {weekday} · {weather} · {mood}")
    prose_parts.append("")
    
    # 早晨部分
    if "morning" in answers:
        prose_parts.append(f"清晨醒来，{answers['morning']}")
    
    # 上午工作
    if "work" in answers:
        prose_parts.append(f"上午的时光在忙碌中度过，{answers['work']}")
    
    # 社交互动
    if "social" in answers:
        prose_parts.append(f"与人相处的时刻总是特别，{answers['social']}")
    
    # 个人时间
    if "personal" in answers:
        prose_parts.append(f"属于自己的时间里，{answers['personal']}")
    
    # 反思感悟
    if "reflection" in answers:
        prose_parts.append(f"静下心来思考，{answers['reflection']}")
    
    # 结尾段落
    prose_parts.append("")
    prose_parts.append("---")
    prose_parts.append(f"**记录时间**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    prose_parts.append(f"**心情指数**：{mood_score}/10")
    
    if "keywords" in answers:
        prose_parts.append(f"**关键词**：{', '.join(answers['keywords'])}")
    
    return "\n".join(prose_parts)

def save_image(src_path, description, date_str=None):
    """保存图片到日记图片目录"""
    if date_str is None:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    structures = create_journal_structure(date_str)
    images_dir = Path(structures["images_dir"])
    
    # 获取当天已有图片数量
    existing_images = list(images_dir.glob(f"{date_str}-*.jpg")) + \
                     list(images_dir.glob(f"{date_str}-*.png")) + \
                     list(images_dir.glob(f"{date_str}-*.jpeg"))
    
    next_num = len(existing_images) + 1
    
    # 确定文件扩展名
    ext = Path(src_path).suffix.lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        ext = '.jpg'
    
    # 目标文件名
    dest_filename = f"{date_str}-{next_num}{ext}"
    dest_path = images_dir / dest_filename
    
    # 复制文件（实际使用中需要根据来源处理）
    # 这里只是示例，实际需要根据图片来源实现
    print(f"将图片保存到: {dest_path}")
    print(f"图片描述: {description}")
    
    # 记录图片信息
    image_info = {
        "filename": dest_filename,
        "original_name": Path(src_path).name,
        "description": description,
        "saved_time": datetime.datetime.now().isoformat(),
        "path": str(dest_path.relative_to("journals"))
    }
    
    return image_info

def update_index(date_str, journal_info):
    """更新日记索引"""
    index_path = Path("journals") / "index.json"
    
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = {
            "version": "1.0",
            "last_updated": datetime.datetime.now().isoformat(),
            "total_entries": 0,
            "years": {},
            "recent_entries": []
        }
    
    # 更新索引
    year = date_str[:4]
    month = date_str[5:7]
    
    if year not in index["years"]:
        index["years"][year] = {"months": {}}
    
    if month not in index["years"][year]["months"]:
        index["years"][year]["months"][month] = {
            "entries": 0,
            "first_date": date_str,
            "last_date": date_str,
            "word_count": 0,
            "image_count": 0
        }
    
    # 更新月数据
    month_data = index["years"][year]["months"][month]
    month_data["entries"] += 1
    month_data["last_date"] = max(month_data["last_date"], date_str)
    month_data["first_date"] = min(month_data["first_date"], date_str)
    month_data["word_count"] += journal_info.get("word_count", 0)
    month_data["image_count"] += journal_info.get("image_count", 0)
    
    # 添加到最近条目
    recent_entry = {
        "date": date_str,
        "path": f"{date_str[:7]}/{date_str}.md",
        "title": journal_info.get("title", f"{date_str}日记"),
        "mood_score": journal_info.get("mood_score", 5),
        "word_count": journal_info.get("word_count", 0),
        "image_count": journal_info.get("image_count", 0),
        "keywords": journal_info.get("keywords", [])
    }
    
    index["recent_entries"].insert(0, recent_entry)
    index["recent_entries"] = index["recent_entries"][:10]  # 保留最近10条
    
    index["total_entries"] += 1
    index["last_updated"] = datetime.datetime.now().isoformat()
    
    # 保存索引
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    return index

def main():
    """示例用法"""
    print("日记生成脚本示例")
    print("=" * 50)
    
    # 示例用户回答（使用哥哥提供的词汇库）
    answers = {
        "mood": "平静",
        "mood_score": 7,
        "weather": "天气温和",
        "keywords": ["工作完成", "朋友聚会", "新发现"],
        "morning": "清晨在凉风习习中醒来，窗外天空很蓝，适合开始新的一天。",
        "work": "专注于项目报告，虽然有些繁琐，但进展顺利，心情平静。",
        "social": "午休时和同事在公园喝茶聊天，燥热中带着惬意。",
        "personal": "傍晚看到晚霞很美，拍了照片记录这美好时刻。",
        "reflection": "即使是平凡的一天，也能找到值得感恩的小确幸。"
    }
    
    # 生成日记
    diary = generate_prose_diary(answers, "2025-02-25")
    print("生成的日记：")
    print(diary)
    
    # 创建目录结构
    structures = create_journal_structure("2025-02-25")
    print(f"\n创建的目录：{structures['base_dir']}")
    print(f"日记文件：{structures['journal_path']}")

if __name__ == "__main__":
    main()