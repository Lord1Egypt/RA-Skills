#!/usr/bin/env python3
"""
行业字段配置与扩展

支持的中小服务行业:
- fitness: 健身教练
- psychology: 心理咨询师
- programming: 编程教育
- yoga: 瑜伽教练
- music: 音乐教育
- art: 美术教育
- tutoring: 学科辅导
- coaching: 职业教练
"""

# 通用服务字段（所有行业适用）
GENERAL_FIELDS = {
    "basic_info": {
        "name": {"type": "string", "required": True, "label": "客户姓名"},
        "phone": {"type": "string", "required": True, "label": "电话号码"},
        "email": {"type": "string", "required": False, "label": "邮箱地址"},
        "wechat_id": {"type": "string", "required": False, "label": "微信ID"},
        "gender": {"type": "enum", "options": ["男", "女", "未知"], "default": "未知", "label": "性别"},
        "age": {"type": "number", "required": False, "label": "年龄"},
    },
    "service_info": {
        "level": {"type": "enum", "options": ["普通", "会员", "VIP"], "default": "普通", "label": "客户等级"},
        "source": {"type": "string", "required": False, "label": "客户来源"},
        "tags": {"type": "list", "required": False, "label": "标签列表"},
        "status": {"type": "enum", "options": ["新增", "跟进中", "已成交", "暂停", "流失"], "default": "新增", "label": "客户状态"},
        "last_contact": {"type": "date", "required": False, "label": "最后联系日期"},
    },
    "financial_info": {
        "balance": {"type": "number", "default": 0, "label": "账户余额"},
        "last_payment": {"type": "date", "required": False, "label": "最后付款日期"},
        "next_payment_due": {"type": "date", "required": False, "label": "下次付款到期日"},
    },
    "preference": {
        "preferred_time": {"type": "string", "required": False, "label": "偏好时间"},
        "preferred_contact": {"type": "enum", "options": ["电话", "微信", "邮件"], "default": "微信", "label": "偏好联系方式"},
        "notes": {"type": "list", "required": False, "label": "跟进记录"},
        "service_records": {"type": "list", "required": False, "label": "服务记录"},
    }
}

# 行业特定字段
INDUSTRY_FIELDS = {
    "fitness": {
        "fitness_level": {"type": "enum", "options": ["初级", "中级", "高级"], "label": "健身水平"},
        "goal_weight": {"type": "number", "required": False, "label": "目标体重(kg)"},
        "current_weight": {"type": "number", "required": False, "label": "当前体重(kg)"},
        "goal": {"type": "string", "required": False, "label": "健身目标"},
        "preferred_exercise": {"type": "list", "required": False, "label": "偏好运动类型"},
        "injury_history": {"type": "string", "required": False, "label": "伤病史"},
    },
    
    "psychology": {
        "current_state": {"type": "enum", "options": ["轻度", "中度", "重度", "康复期"], "label": "当前状态"},
        "therapy_phase": {"type": "enum", "options": ["初诊期", "探索期", "工作期", "结束期"], "label": "治疗阶段"},
        "emergency_contact": {"type": "string", "required": False, "label": "紧急联系人"},
        "emergency_phone": {"type": "string", "required": False, "label": "紧急联系电话"},
        "main_concern": {"type": "string", "required": False, "label": "主要困扰"},
        "medication": {"type": "string", "required": False, "label": "用药情况"},
    },
    
    "programming": {
        "coding_level": {"type": "enum", "options": ["零基础", "入门级", "初级", "中级", "高级"], "label": "编程水平"},
        "current_language": {"type": "string", "required": False, "label": "当前学习语言"},
        "project_progress": {"type": "string", "required": False, "label": "项目进度"},
        "preferred_language": {"type": "list", "required": False, "label": "偏好语言"},
        "learning_goal": {"type": "string", "required": False, "label": "学习目标"},
        "homework_completion": {"type": "number", "min": 0, "max": 100, "label": "作业完成度(%)"},
    },
    
    "yoga": {
        "yoga_level": {"type": "enum", "options": ["零基础", "初级", "中级", "高级"], "label": "瑜伽水平"},
        "preferred_style": {"type": "list", "required": False, "label": "偏好流派"},
        "flexibility": {"type": "enum", "options": ["很差", "一般", "良好", "优秀"], "label": "柔韧性"},
        "meditation_exp": {"type": "enum", "options": ["无", "有"], "label": "冥想经验"},
    },
    
    "music": {
        "instrument": {"type": "string", "required": False, "label": "学习乐器"},
        "music_level": {"type": "enum", "options": ["零基础", "初级", "中级", "高级"], "label": "音乐水平"},
        "theory_knowledge": {"type": "enum", "options": ["无", "基础", "良好"], "label": "乐理知识"},
        "practice_time": {"type": "string", "required": False, "label": "每日练习时间"},
    },
    
    "art": {
        "art_type": {"type": "string", "required": False, "label": "美术类型"},
        "art_level": {"type": "enum", "options": ["零基础", "初级", "中级", "高级"], "label": "美术水平"},
        "material_preference": {"type": "list", "required": False, "label": "偏好材料"},
    },
    
    "tutoring": {
        "subject": {"type": "string", "required": False, "label": "辅导科目"},
        "grade": {"type": "string", "required": False, "label": "年级"},
        "school": {"type": "string", "required": False, "label": "学校"},
        "weak_points": {"type": "list", "required": False, "label": "薄弱环节"},
        "target_score": {"type": "number", "required": False, "label": "目标分数"},
    },
    
    "coaching": {
        "career_goal": {"type": "string", "required": False, "label": "职业目标"},
        "current_position": {"type": "string", "required": False, "label": "当前职位"},
        "industry": {"type": "string", "required": False, "label": "所在行业"},
        "coaching_focus": {"type": "list", "required": False, "label": "辅导重点"},
    }
}


def get_all_fields(industry=None):
    """
    获取所有字段定义
    
    Args:
        industry: 行业代码（如'fitness'），None则只返回通用字段
    
    Returns:
        dict: 字段定义字典
    """
    fields = {}
    
    # 合并通用字段
    for category, field_defs in GENERAL_FIELDS.items():
        fields.update(field_defs)
    
    # 添加行业特定字段
    if industry and industry in INDUSTRY_FIELDS:
        fields.update(INDUSTRY_FIELDS[industry])
    
    return fields


def get_industry_list():
    """获取支持的行业列表"""
    return {
        "fitness": "健身教练",
        "psychology": "心理咨询师",
        "programming": "编程教育",
        "yoga": "瑜伽教练",
        "music": "音乐教育",
        "art": "美术教育",
        "tutoring": "学科辅导",
        "coaching": "职业教练",
        "general": "通用服务"
    }


def validate_field_value(field_name, value, industry=None):
    """
    验证字段值是否有效
    
    Args:
        field_name: 字段名
        value: 字段值
        industry: 行业代码
    
    Returns:
        tuple: (是否有效, 错误信息)
    """
    fields = get_all_fields(industry)
    
    if field_name not in fields:
        return False, f"未知字段: {field_name}"
    
    field_def = fields[field_name]
    field_type = field_def.get("type")
    
    if field_type == "enum":
        valid_options = field_def.get("options", [])
        if value not in valid_options:
            return False, f"无效值 '{value}'，有效选项: {', '.join(valid_options)}"
    
    elif field_type == "number":
        try:
            num_value = float(value)
            min_val = field_def.get("min")
            max_val = field_def.get("max")
            
            if min_val is not None and num_value < min_val:
                return False, f"值不能小于 {min_val}"
            if max_val is not None and num_value > max_val:
                return False, f"值不能大于 {max_val}"
        except ValueError:
            return False, f"值必须是数字"
    
    elif field_type == "list":
        if not isinstance(value, list):
            return False, f"值必须是列表"
    
    return True, None


def main():
    import json
    
    print("支持的中小服务行业:")
    print("-" * 60)
    
    industries = get_industry_list()
    for code, name in industries.items():
        print(f"  {code:12s} - {name}")
    
    print("\n通用字段示例:")
    print("-" * 60)
    
    fields = get_all_fields()
    for field_name, field_def in list(fields.items())[:5]:
        print(f"  {field_name}: {field_def.get('label')} ({field_def.get('type')})")
    
    print(f"\n... 共 {len(fields)} 个通用字段")
    
    print("\n健身行业额外字段:")
    print("-" * 60)
    
    fitness_fields = get_all_fields("fitness")
    general_field_names = set(get_all_fields().keys())
    
    for field_name, field_def in fitness_fields.items():
        if field_name not in general_field_names:
            print(f"  {field_name}: {field_def.get('label')} ({field_def.get('type')})")


if __name__ == "__main__":
    main()
