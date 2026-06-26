#!/usr/bin/env python3
"""
记忆引擎配置 - 分类体系、评级标准、事实定义
"""

# ============== 分类体系 ==============
CATEGORIES = {
    "person": {
        "name": "👤 人物/关系",
        "description": "人物、团队成员、联系人",
        "keywords": ["用户", "管理员", "Agent", "团队成员", "同事", "朋友", "家人"]
    },
    "work": {
        "name": "💼 工作类",
        "description": "工作任务、项目、决策、业务相关",
        "keywords": ["项目", "任务", "决策", "广告", "运营", "公众号", "工作"]
    },
    "tech": {
        "name": "⚙️ 技术类",
        "description": "系统配置、API、技术实现、代码",
        "keywords": ["配置", "API", "代码", "模型", "系统", "安装", "部署", "OpenClaw"]
    },
    "preference": {
        "name": "❤️ 偏好类",
        "description": "用户偏好、习惯、风格",
        "keywords": ["喜欢", "偏好", "不要", "习惯", "讨厌", "想要", "希望"]
    },
    "schedule": {
        "name": "📅 日程类",
        "description": "时间安排、会议、活动、地点",
        "keywords": ["时间", "日程", "会议", "约", "安排", "地点"]
    },
    "insight": {
        "name": "💡 洞察类",
        "description": "教训、经验、总结、反思",
        "keywords": ["教训", "经验", "总结", "反思", "踩坑", "注意", "提醒"]
    },
    "system_change": {
        "name": "🔧 系统变更",
        "description": "直接改变系统结构、内容、配置的行为",
        "keywords": ["修改", "更新", "删除", "创建", "新增Agent", "配置变更"]
    }
}

# ============== 重要性评级标准 ==============
RATING_RULES = {
    # 改变系统结构 = 最高优先级
    "system_structure_change": {
        "score": 10,
        "description": "改变系统结构（新增Agent、修改核心配置、系统升级）",
        "patterns": [
            r"新增[Aa]gent",
            r"创建.*[Aa]gent",
            r"修改.*配置",
            r"更新.*系统",
            r"系统.*升级",
            r"安装.*依赖"
        ]
    },
    # 重点项目 = 高优先级
    "important_project": {
        "score": 8,
        "description": "重点项目（公众号发文、新项目启动、重要决策）",
        "patterns": [
            r"公众号.*发文",
            r"项目.*启动",
            r"重要.*决策",
            r"业务.*变更",
            r"新功能.*上线"
        ]
    },
    # 反复提问 = 高优先级
    "repeated_question": {
        "score": 8,
        "description": "反复提问同一主题（说明这个很重要）",
        "keywords": ["反复", "重复", "又问"]
    },
    # 口述重点项目
    "verbal_important": {
        "score": 7,
        "description": "口述重点项目或安排",
        "patterns": [
            r"重点.*项目",
            r"主要.*任务",
            r"优先级.*高"
        ]
    },
    # 偏好类
    "preference": {
        "score": 7,
        "description": "明确表达偏好或习惯",
        "patterns": [
            r"喜欢.*",
            r"不要.*",
            r"希望.*",
            r"习惯.*"
        ]
    },
    # 问题解决
    "problem_solved": {
        "score": 6,
        "description": "解决的问题",
        "patterns": [
            r"已修复",
            r"问题.*解决",
            r"✅.*完成"
        ]
    },
    # 一般事实
    "general": {
        "score": 3,
        "description": "一般事实性信息",
        "patterns": []
    }
}

# ============== 重要事实定义 ==============
IMPORTANT_FACT_SIGNALS = {
    # 高频信号
    "high_frequency": [
        "反复提问",
        "重复问",
        "又问到",
        "这个之前问过"
    ],
    # 系统变更信号
    "system_change": [
        "新增Agent",
        "创建Agent", 
        "修改配置",
        "更新系统",
        "安装",
        "部署",
        "删除",
        "重命名"
    ],
    # 重点项目信号
    "important_project": [
        "公众号",
        "发文",
        "项目启动",
        "重要任务",
        "优先级高",
        "主要工作"
    ],
    # 偏好信号
    "preference": [
        "喜欢",
        "不喜欢",
        "不要",
        "希望",
        "想要",
        "习惯"
    ],
    # 决策信号
    "decision": [
        "决定",
        "确定了",
        "就这么办",
        "选择"
    ]
}

# ============== 飞书知识库配置 ==============
FEISHU_CONFIG = {
    "enabled": True,
    "knowledge_base_folder_token": None,  # 将自动创建
    "sync_interval_hours": 24,
    "doc_types": ["docx", "doc"]
}
