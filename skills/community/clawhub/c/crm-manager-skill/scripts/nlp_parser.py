#!/usr/bin/env python3
"""
NLP解析引擎 - 自然语言服务记录解析

用法:
    python nlp_parser.py "今天给张三上了一节健身课，深蹲进步了10kg"

功能:
1. 识别客户姓名
2. 提取服务类型
3. 提取关键信息（时长、进度、金额等）
4. 生成结构化服务记录数据
"""

import re
import jieba
import jieba.posseg as pseg
from datetime import datetime, timedelta

# 初始化jieba词典（如果有自定义词典则加载）
try:
    jieba.load_userdict("nlp_dict.txt")
except FileNotFoundError:
    pass  # 没有自定义词典也不影响

# 服务类型关键词映射
SERVICE_TYPE_KEYWORDS = {
    "课程购买": ["购买", "买课", "买课程", "报名", "续费", "续课", "充值"],
    "单次服务": ["上课", "服务", "训练", "咨询", "辅导", "私教", "一对一"],
    "体验课": ["体验", "试听", "试课", "免费课", "体验课"],
    "续费": ["续费", "续课", "续期", "延期", "续买"],
    "课程调整": ["调整", "改时间", "改课", "调课", "补课", "换课"],
    "进度评估": ["评估", "测评", "考核", "测试", "检查", "进度"],
    "反馈沟通": ["反馈", "沟通", "交流", "回访", "跟进"]
}

# 出勤状态关键词
ATTENDANCE_KEYWORDS = {
    "出席": ["来了", "到了", "出席", "参加", "到场", "准时"],
    "缺席": ["没来", "缺席", "请假", "旷课", "未到"],
    "请假": ["请假", "有事", "临时有事", "改期"],
    "补课": ["补课", "补训", "补咨询"]
}

# 进度评级关键词
PROGRESS_KEYWORDS = {
    "优秀": ["进步很大", "进步明显", "表现优秀", "很好", "非常棒", "优秀", "出色"],
    "良好": ["进步", "表现不错", "还可以", "良好", "正常", "稳定"],
    "一般": ["一般", "还行", "凑合", "普通", "正常水平"],
    "需加强": ["需要加强", "还要努力", "不太理想", "需改进", "要加强", "跟不上"]
}

# 结果状态关键词
OUTCOME_KEYWORDS = {
    "成功": ["成功", "顺利", "完成", "很好", "满意", "成交", "签约"],
    "失败": ["失败", "取消", "退费", "不满意", "没成交"],
    "进行中": ["继续", "下次", "待定", "考虑", "进行中"]
}


def extract_customer_name(text):
    """提取客户姓名"""
    # 模式1：最明确的指示词
    patterns = [
        r'给\s*([\u4e00-\u9fa5]{2,4})\s*(?:上了|买了|报名|预约)',
        r'为\s*([\u4e00-\u9fa5]{2,4})\s*(?:上了|买了|报名|预约)',
        r'客户\s*([\u4e00-\u9fa5]{2,4})',
        r'会员\s*([\u4e00-\u9fa5]{2,4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    # 模式2：句子开头的人名（通常是主语）
    # 如："张三今天上了健身课"
    match = re.match(r'([\u4e00-\u9fa5]{2,4})\s*(?:今天|昨天|明天|上周|这周)', text)
    if match:
        return match.group(1)
    
    # 模式3：提取所有人名候选，过滤掉常见词
    names = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
    exclude_words = ['今天', '明天', '昨天', '上午', '下午', '晚上', '小时', '分钟', '课程', 
                     '服务', '训练', '健身', '心理', '咨询', '编程', '瑜伽', '音乐', '美术']
    
    for name in names:
        if name not in exclude_words and len(name) >= 2:
            return name
    
    return None
    if names:
        # 排除常见词
        exclude_words = ['今天', '明天', '昨天', '上午', '下午', '晚上', '小时', '分钟', '课程', '服务']
        for name in names:
            if name not in exclude_words:
                return name
    
    return None


def extract_service_type(text):
    """提取服务类型"""
    for service_type, keywords in SERVICE_TYPE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return service_type
    
    # 默认类型
    if any(word in text for word in ['课', '训练', '咨询', '辅导']):
        return "单次服务"
    
    return "单次服务"  # 默认类型


def extract_attendance(text):
    """提取出勤状态"""
    for attendance, keywords in ATTENDANCE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return attendance
    return None


def extract_progress(text):
    """提取进度评级"""
    for progress, keywords in PROGRESS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return progress
    return None


def extract_outcome(text):
    """提取结果状态"""
    for outcome, keywords in OUTCOME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return outcome
    return "进行中"  # 默认进行中


def extract_duration(text):
    """提取服务时长（分钟）"""
    # 匹配模式："60分钟"、"1小时"、"一个半小时"
    patterns = [
        (r'(\d+)\s*分钟', lambda x: int(x)),
        (r'(\d+)\s*小时', lambda x: int(x) * 60),
        (r'半\s*小时', lambda x: 30),
        (r'一\s*小时', lambda x: 60),
        (r'一个半\s*小时', lambda x: 90),
        (r'两\s*小时', lambda x: 120),
    ]
    
    for pattern, converter in patterns:
        match = re.search(pattern, text)
        if match:
            if match.groups():
                return converter(match.group(1))
            else:
                return converter(None)
    
    return None


def extract_amount(text):
    """提取金额"""
    # 匹配模式："300元"、"300块"、"3000块钱"、"300.5元"
    patterns = [
        r'(\d+(?:\.\d+)?)\s*元',
        r'(\d+(?:\.\d+)?)\s*块',
        r'(\d+(?:\.\d+)?)\s*块钱',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return float(match.group(1))
    
    return None


def extract_date(text):
    """提取日期"""
    # 今天、昨天、明天、具体日期
    today = datetime.now()
    
    if '今天' in text:
        return today.strftime("%Y-%m-%d")
    elif '昨天' in text:
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif '明天' in text:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif '前天' in text:
        return (today - timedelta(days=2)).strftime("%Y-%m-%d")
    elif '后天' in text:
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")
    
    # 匹配具体日期：2026-04-03、2026年4月3日、4月3日
    date_patterns = [
        r'(\d{4})-(\d{1,2})-(\d{1,2})',
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',
        r'(\d{1,2})月(\d{1,2})日',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                year, month, day = groups
            else:
                year = today.year
                month, day = groups
            return f"{year}-{int(month):02d}-{int(day):02d}"
    
    return today.strftime("%Y-%m-%d")  # 默认今天


def parse_service_record(text):
    """
    解析自然语言服务记录
    
    Args:
        text: 自然语言描述，如"今天给张三上了一节健身课，深蹲进步了10kg"
    
    Returns:
        dict: 结构化数据
    """
    result = {
        "customer": extract_customer_name(text),
        "type": extract_service_type(text),
        "description": text,  # 原始描述
        "attendance": extract_attendance(text),
        "duration": extract_duration(text),
        "progress": extract_progress(text),
        "amount": extract_amount(text),
        "outcome": extract_outcome(text),
        "date": extract_date(text),
        "parsed": True
    }
    
    # 如果无法识别客户，标记为解析失败
    if not result["customer"]:
        result["parsed"] = False
        result["error"] = "无法识别客户姓名"
    
    return result


def format_parsed_result(result):
    """格式化解析结果"""
    if not result["parsed"]:
        return f"解析失败: {result.get('error', '未知错误')}"
    
    lines = ["解析成功！", ""]
    lines.append(f"客户: {result['customer']}")
    lines.append(f"服务类型: {result['type']}")
    lines.append(f"日期: {result['date']}")
    
    if result['attendance']:
        lines.append(f"出勤: {result['attendance']}")
    if result['duration']:
        lines.append(f"时长: {result['duration']}分钟")
    if result['progress']:
        lines.append(f"进度: {result['progress']}")
    if result['amount']:
        lines.append(f"金额: {result['amount']}元")
    
    lines.append(f"结果: {result['outcome']}")
    lines.append("")
    lines.append(f"描述: {result['description']}")
    
    return "\n".join(lines)


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python nlp_parser.py \"今天给张三上了一节健身课\"")
        print("\n示例输入:")
        print('  "今天给张三上了一节健身课，深蹲进步了10kg"')
        print('  "王芳买了10次心理咨询课，3000块钱"')
        print('  "李四昨天体验课，进步很大，60分钟"')
        return 1
    
    text = sys.argv[1]
    result = parse_service_record(text)
    print(format_parsed_result(result))
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
