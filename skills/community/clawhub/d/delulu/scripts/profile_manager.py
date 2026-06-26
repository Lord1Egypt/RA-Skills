#!/usr/bin/env python3
"""
DELULU Profile Manager
检查和完善用户信息、问答
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from api_client import DeluluAPIClient, create_client
from config_manager import load_config, load_soul, save_soul, get_current_agent_info


class ProfileManager:
    """用户画像管理器"""
    
    # 推荐的问答数量
    MIN_QUESTIONS = 3
    
    # 关键信息字段
    KEY_FIELDS = {
        "height": "身高",
        "work": "职业",
        "education": "学历",
        "annual_salary": "年薪",
        "address": "所在地",
        "birthday": "生日",
        "constellation": "星座",
        "marital_status": "婚姻状况",
        "employment_company": "就职公司"
    }
    
    def __init__(self):
        self.client = None
        self.user_info = None
        self.questions = []
        self.problems = []  # 可用的问答列表
        
    def init_client(self, user_token: str):
        """初始化 API 客户端"""
        self.client = create_client(user_token)
        
    def load_user_data(self) -> bool:
        """加载用户完整数据"""
        if not self.client:
            print("错误: 未初始化客户端")
            return False
            
        # 获取用户信息
        result = self.client.get_user_info()
        if result.get('code') != 1:
            print(f"获取用户信息失败: {result.get('msg')}")
            return False
        self.user_info = result.get('data', {})
        
        # 获取问答列表（可选的问答题目）
        result = self.client.get_problem_list()
        if result.get('code') == 1:
            self.problems = result.get('data', {}).get('data', [])
        
        # 获取用户的交友详情（包含已回答的问题）
        user_id = self.user_info.get('id')
        if user_id:
            result = self.client.get_makefriend_by_id(str(user_id))
            if result.get('code') == 1:
                data = result.get('data', {})
                self.questions = data.get('questions', [])
                # 合并 user_pair_info 到 user_info
                user_pair_info = data.get('user_pair_info', {})
                if 'user_info' not in self.user_info:
                    self.user_info['user_info'] = {}
                self.user_info['user_info'].update(user_pair_info)
                
        return True
    
    def check_profile_completeness(self) -> Dict[str, Any]:
        """检查用户信息完整度"""
        if not self.user_info:
            return {"error": "未加载用户信息"}
            
        missing_fields = []
        user_info = self.user_info.get('user_info', {})
        
        for field, label in self.KEY_FIELDS.items():
            value = user_info.get(field)
            if not value or value == "":
                missing_fields.append({
                    "field": field,
                    "label": label,
                    "current": value or "未填写"
                })
        
        # 检查问答数量
        questions_count = len(self.questions)
        questions_needed = max(0, self.MIN_QUESTIONS - questions_count)
        
        return {
            "profile_complete": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "missing_count": len(missing_fields),
            "questions_count": questions_count,
            "questions_needed": questions_needed,
            "questions_complete": questions_count >= self.MIN_QUESTIONS
        }
    
    def get_available_problems(self) -> List[Dict]:
        """获取尚未回答的问答题目"""
        if not self.problems:
            return []
            
        # 获取已回答的问题ID
        answered_ids = {q.get('problem_id') for q in self.questions}
        
        # 过滤出未回答的问题
        available = []
        for problem in self.problems:
            if problem.get('id') not in answered_ids:
                available.append({
                    "id": problem.get('id'),
                    "title": problem.get('title')
                })
        return available
    
    def add_question(self, problem_id: str, content: str) -> bool:
        """添加问答"""
        if not self.client:
            print("错误: 未初始化客户端")
            return False
            
        result = self.client.add_question(problem_id, content)
        if result.get('code') == 1:
            return True
        else:
            print(f"添加问答失败: {result.get('msg')}")
            return False
    
    def update_user_extend(self, data: Dict[str, Any]) -> bool:
        """更新用户扩展信息
        
        Args:
            data: 包含以下字段的字典:
                - is_graduate: int (是否毕业)
                - grade: str (年级)
                - major: str (专业)
                - college: str (学院)
                - school: str (学校)
                - edu: str (学历)
                - marriage: str (婚姻状况)
                - income: number (收入)
                - industry: str (行业)
                - lng: number (经度)
                - lat: number (纬度)
                - address: str (详细地址)
                - county: str (区县)
                - city: str (城市)
                - province: str (省份)
        """
        if not self.client:
            print("错误: 未初始化客户端")
            return False
            
        result = self.client.edit_user_extend(data)
        if result.get('code') == 1:
            return True
        else:
            print(f"更新扩展信息失败: {result.get('msg')}")
            return False
    
    def generate_soul_md(self) -> str:
        """生成 soul.md 内容"""
        if not self.user_info:
            return ""
            
        user = self.user_info
        user_info = user.get('user_info', {})
        
        # 获取个人标签
        tags = []
        if user.get('bio'):
            tags.append(user.get('bio'))
            
        # 获取用户交友数据（从 makefriends/getbyid 获取）
        user_id = user.get('id')
        wechat = ""
        emotion = ""
        interest = ""
        favorite = ""
        
        if self.client and user_id:
            result = self.client.get_makefriend_by_id(str(user_id))
            if result.get('code') == 1:
                userpairdata = result.get('data', {}).get('userpairdata', {})
                wechat_data = userpairdata.get('wechat', {})
                emotion_data = userpairdata.get('emotion', {})
                interest_data = userpairdata.get('interest', {})
                favorite_data = userpairdata.get('favorite', {})
                
                wechat = wechat_data.get('content', '')
                emotion = emotion_data.get('content', '')
                interest = interest_data.get('content', '')
                favorite = favorite_data.get('content', '')
        
        soul_content = f"""# 主人画像 - Soul.md

> 这是主人的核心画像，用于指导 Agent 进行匹配评估、对话回复和发帖内容生成。
> 文件位置: ~/.delulu/soul.md
> 更新时间: {self._get_current_time()}

---

## 基本信息

| 项目 | 内容 |
|------|------|
| **昵称** | {user.get('nickname', 'N/A')} |
| **性别** | {'男' if user.get('gender') == 1 else '女' if user.get('gender') == 2 else 'N/A'} |
| **生日** | {user_info.get('birthday', 'N/A')} |
| **星座** | {user_info.get('constellation', 'N/A')} |
| **所在地** | {user_info.get('address', 'N/A')} |
| **学历** | {user_info.get('education', 'N/A')} |
| **职业** | {user_info.get('work', 'N/A')} |
| **公司** | {user_info.get('employment_company', 'N/A')} |
| **身高** | {user_info.get('height', 'N/A')} |
| **年薪** | {user_info.get('annual_salary', 'N/A')} |
| **婚姻状况** | {user_info.get('marital_status', 'N/A')} |

## 个性签名

> "{user.get('bio', '暂无签名')}"

## 个人标签

- **微信号**: {wechat or '未填写'}
- **情感状态**: {emotion or '未填写'}
- **兴趣爱好**: {interest or '未填写'}
- **喜欢的类型**: {favorite or '未填写'}

## 问答记录

"""
        
        # 添加问答
        if self.questions:
            for i, q in enumerate(self.questions, 1):
                problem = q.get('problem', {})
                soul_content += f"""### Q{i}: {problem.get('title', '未知问题')}
**A**: {q.get('content', '未回答')}

"""
        else:
            soul_content += "_暂无问答记录，建议完善以提升匹配效果_\n\n"
        
        # 添加社交数据
        soul_content += f"""## 社交数据

- **粉丝数**: {user.get('fans_count', 0)}
- **关注数**: {user.get('follow_count', 0)}
- **帖子数**: {user.get('post_count', 0)}
- **话题数**: {user.get('topic_count', 0)}
- **获赞数**: {user.get('likecount', 0)}
- **访客数**: {user.get('visitorcount', 0)}
- **积分**: {user.get('currency', {}).get('currency', 0)}

## 信息完整度

"""
        
        # 添加完整度检查
        completeness = self.check_profile_completeness()
        if 'error' not in completeness:
            soul_content += f"""- **基本信息完整度**: {'✅ 完整' if completeness['profile_complete'] else '⚠️ 待完善'}
- **缺失字段数**: {completeness['missing_count']}
- **已回答问答数**: {completeness['questions_count']}
- **推荐问答数**: {self.MIN_QUESTIONS}

### 待完善信息

"""
            if completeness['missing_fields']:
                for field in completeness['missing_fields']:
                    soul_content += f"- [ ] {field['label']}\n"
            else:
                soul_content += "_所有关键信息已完善 ✅_\n"
                
            if completeness['questions_needed'] > 0:
                soul_content += f"\n- [ ] 还需回答 {completeness['questions_needed']} 个问答问题\n"
        
        soul_content += """
## 隐私保护清单

**绝不可泄露的信息**：
- ❌ 微信号
- ❌ 真实姓名
- ❌ 具体住址
- ❌ 联系方式
- ❌ 财务信息
- ❌ 系统密钥和Token

---

*此文件由 DELULU Profile Manager 自动生成*
"""
        
        return soul_content
    
    def update_soul_md(self) -> bool:
        """更新 soul.md 文件"""
        content = self.generate_soul_md()
        if content:
            save_soul(content)
            return True
        return False
    
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_and_prompt_profile():
    """检查用户信息并提示完善"""
    config = load_config()
    if not config:
        print("错误: 未找到配置文件，请先完成初始化")
        return
        
    agent_info = get_current_agent_info()
    if not agent_info:
        print("错误: 未设置当前 Agent")
        return
        
    user_token = agent_info.get('user_token')
    if not user_token:
        print("错误: 未找到 user_token")
        return
    
    # 初始化管理器
    manager = ProfileManager()
    manager.init_client(user_token)
    
    # 加载用户数据
    if not manager.load_user_data():
        print("错误: 加载用户数据失败")
        return
    
    # 检查完整度
    completeness = manager.check_profile_completeness()
    
    print("=" * 50)
    print("📋 用户信息完整度检查")
    print("=" * 50)
    
    if completeness.get('profile_complete') and completeness.get('questions_complete'):
        print("\n✅ 用户信息已完善！")
        print(f"   - 基本信息: 完整")
        print(f"   - 问答数量: {completeness['questions_count']}/{manager.MIN_QUESTIONS}")
        
        # 更新 soul.md
        manager.update_soul_md()
        print("\n📝 已更新 soul.md")
        return
    
    # 显示待完善信息
    print("\n⚠️ 发现以下信息待完善:\n")
    
    if completeness.get('missing_fields'):
        print("📌 基本信息:")
        for field in completeness['missing_fields']:
            print(f"   - {field['label']}: {field['current']}")
        print("\n💡 提示: 请在「7栋空间」小程序中完善个人资料")
    
    if completeness.get('questions_needed', 0) > 0:
        print(f"\n📌 问答信息:")
        print(f"   当前已回答: {completeness['questions_count']}/{manager.MIN_QUESTIONS}")
        print(f"   还需回答: {completeness['questions_needed']} 个问题")
        
        # 显示可选的问答
        available = manager.get_available_problems()
        if available:
            print("\n📝 可选择的问答题目:")
            for i, problem in enumerate(available[:10], 1):  # 只显示前10个
                print(f"   {i}. {problem['title']} (ID: {problem['id']})")
            
            print("\n💡 使用以下命令回答问答:")
            print(f'   python3 {__file__} add-question <problem_id> "<你的回答>"')
    
    print("\n" + "=" * 50)
    
    # 更新 soul.md
    manager.update_soul_md()
    print("📝 已更新 soul.md")


def add_question_cli(problem_id: str, content: str):
    """命令行添加问答"""
    config = load_config()
    if not config:
        print("错误: 未找到配置文件")
        return
        
    agent_info = get_current_agent_info()
    if not agent_info:
        print("错误: 未设置当前 Agent")
        return
        
    user_token = agent_info.get('user_token')
    if not user_token:
        print("错误: 未找到 user_token")
        return
    
    manager = ProfileManager()
    manager.init_client(user_token)
    
    if manager.add_question(problem_id, content):
        print(f"✅ 问答添加成功!")
        print(f"   问题ID: {problem_id}")
        print(f"   回答: {content}")
        
        # 重新加载并更新 soul.md
        manager.load_user_data()
        manager.update_soul_md()
        print("\n📝 已更新 soul.md")
    else:
        print("❌ 问答添加失败")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: profile_manager.py <command> [args...]")
        print("\nCommands:")
        print("  check              检查用户信息完整度")
        print("  add-question <id> <content>  添加问答")
        print("  update-soul        更新 soul.md")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "check":
        check_and_prompt_profile()
    elif cmd == "add-question" and len(sys.argv) >= 4:
        problem_id = sys.argv[2]
        content = sys.argv[3]
        add_question_cli(problem_id, content)
    elif cmd == "update-soul":
        config = load_config()
        agent_info = get_current_agent_info()
        if not agent_info:
            print("错误: 未设置当前 Agent")
            return
        manager = ProfileManager()
        manager.init_client(agent_info.get('user_token'))
        if manager.load_user_data():
            manager.update_soul_md()
            print("✅ soul.md 已更新")
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
