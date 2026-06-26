#!/usr/bin/env python3
"""
DELULU Soul Generator
自动生成主人的 soul.md 画像文件
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from api_client import DeluluAPIClient
from config_manager import save_soul, load_config


def generate_soul_markdown(user_info: Dict, user_pair_info: Dict, 
                          preferences: Dict, questions: list) -> str:
    """
    根据 API 返回数据生成 soul.md 内容
    """
    # 解析基本信息
    nickname = user_info.get('nickname', '未知')
    gender = '男' if user_info.get('gender') == 1 else '女' if user_info.get('gender') == 2 else '未知'
    bio = user_info.get('bio', '')
    birthday = user_pair_info.get('birthday', '')
    constellation = user_pair_info.get('constellation', '')
    address = user_pair_info.get('address', '')
    education = user_pair_info.get('education', '')
    work = user_pair_info.get('work', '')
    employment_company = user_pair_info.get('employment_company', '')
    height = user_pair_info.get('height', '')
    
    # 解析推荐偏好
    pref_address = preferences.get('address', '')
    pref_education = preferences.get('education', '')
    min_age = preferences.get('min_age', 18)
    max_age = preferences.get('max_age', 60)
    min_height = preferences.get('min_height', 100)
    max_height = preferences.get('max_height', 220)
    
    # 构建问答部分
    questions_section = ""
    if questions:
        for q in questions:
            title = q.get('problem', {}).get('title', '未知问题')
            content = q.get('content', '未回答')
            questions_section += f"\n**Q: {title}**\n\n> {content}\n"
    else:
        questions_section = "\n暂无问答记录\n"
    
    soul_content = f"""# 主人画像 - {nickname}

## 基本信息
- **昵称**: {nickname}
- **性别**: {gender}
- **生日**: {birthday}
- **星座**: {constellation}
- **所在地**: {address}
- **学历**: {education}
- **身高**: {height}cm
- **职业**: {work}
- **公司**: {employment_company}

## 个性签名
> {bio}

## 交友偏好
- **期望地区**: {pref_address}
- **期望学历**: {pref_education}
- **期望年龄**: {min_age} - {max_age} 岁
- **期望身高**: {min_height} - {max_height} cm

## 我的问答记录
{questions_section}

## 性格特征
- *待补充：填写你的核心性格特质*

## 兴趣爱好
- *待补充：填写你的兴趣爱好*

## 价值观 & 交友观
- *待补充：填写你看重的品质和交友偏好*

## 沟通禁忌
- *待补充：填写绝不说的话、绝不做的事*

## 理想型
- *待补充：填写你心仪的对象特征*

## 隐私保护清单

**绝不可泄露的信息**：
- ❌ 微信号
- ❌ 真实姓名
- ❌ 具体住址
- ❌ 联系方式
- ❌ 财务信息
- ❌ 系统密钥和Token

---

💡 **提示**: 以上内容已根据你在 DELULU 平台的资料自动生成。你可以随时编辑此文件来完善你的画像，让 AI Agent 更懂你。
"""
    
    return soul_content


def fetch_and_generate_soul(user_token: str) -> bool:
    """
    从 API 获取数据并生成 soul.md
    """
    client = DeluluAPIClient(user_token)
    
    # 1. 获取用户信息
    user_response = client.get_user_info()
    if user_response.get('code') != 1:
        print(f"获取用户信息失败: {user_response.get('msg')}")
        return False
    
    user_data = user_response.get('data', {})
    user_info = user_data
    user_pair_info = user_data.get('user_info', {})
    
    # 2. 获取推荐偏好
    pref_response = client.get_recommendation_preferences()
    preferences = {}
    if pref_response.get('code') == 1:
        preferences = pref_response.get('data', {})
    
    # 3. 获取问答记录（这里需要从用户的交友详情中获取）
    # 先获取用户自己的交友详情
    friend_detail = client.get_makefriend_by_id(str(user_info.get('id', '')))
    questions = []
    if friend_detail.get('code') == 1:
        questions = friend_detail.get('data', {}).get('questions', [])
    
    # 4. 生成 soul.md
    soul_content = generate_soul_markdown(user_info, user_pair_info, preferences, questions)
    
    # 5. 保存
    save_soul(soul_content)
    
    print(f"✅ soul.md 已生成！")
    print(f"   昵称: {user_info.get('nickname')}")
    print(f"   星座: {user_pair_info.get('constellation')}")
    print(f"   所在地: {user_pair_info.get('address')}")
    print(f"   问答数: {len(questions)}")
    
    return True


def main():
    # 从配置中读取 user_token
    config = load_config()
    if not config:
        print("❌ 配置不存在，请先完成安装")
        return 1
    
    # 获取当前 agent 的 token
    current_agent_name = config.get('current_agent')
    if not current_agent_name:
        print("❌ 未设置当前 Agent")
        return 1
    
    user_token = None
    for agent in config.get('agent_list', []):
        if agent.get('name') == current_agent_name:
            user_token = agent.get('user_token')
            break
    
    if not user_token:
        print("❌ 未找到 user_token，请重新登录")
        return 1
    
    # 生成 soul.md
    if fetch_and_generate_soul(user_token):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
