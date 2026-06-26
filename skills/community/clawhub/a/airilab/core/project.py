#!/usr/bin/env python3
"""
AiriLab 项目管理

整合原 airi-project 技能的功能：
1. 获取团队和项目列表
2. 引导用户选择项目
3. 项目配置持久化
"""

import requests
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from .config import AiriLabConfig
except ImportError:  # pragma: no cover
    from config import AiriLabConfig

# API 端点
GET_TEAMS_URL = "https://cn.airilab.com/api/Team/GetUserTeams"
GET_PROJECTS_URL = "https://cn.airilab.com/api/Accounts/GetAllProjectsUser"


class AiriLabProject:
    """AiriLab 项目管理器"""
    
    def __init__(self, config: AiriLabConfig = None):
        """
        初始化项目管理器
        
        参数:
            config: 配置管理器实例
        """
        self.config = config or AiriLabConfig()
    
    def get_teams_and_projects(self, token: str) -> List[Dict[str, Any]]:
        """
        获取所有团队和项目
        
        参数:
            token: JWT Token
        
        返回:
            list: 团队和项目列表
        """
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        result = []
        
        try:
            # Step 1: 获取所有团队
            response = requests.get(GET_TEAMS_URL, headers=headers, timeout=30)
            teams_data = response.json()
            
            if teams_data.get("status") != 200 or not teams_data.get("data"):
                print(f"❌ 获取团队失败：{teams_data}")
                return result
            
            teams = teams_data["data"]
            
            # Step 2: 对每个团队获取项目
            for team in teams:
                team_info = {
                    "teamId": team["teamId"],
                    "teamName": team["teamName"],
                    "projects": []
                }
                
                # 获取该团队下的所有项目
                resp = requests.get(
                    f"{GET_PROJECTS_URL}?teamId={team['teamId']}",
                    headers=headers,
                    timeout=30
                )
                projects_data = resp.json()
                
                if projects_data.get("status") == 200:
                    # 优先取 userData，如果没有则取 teamData
                    project_data = projects_data.get("userData", projects_data.get("teamData", {}))
                    projects = project_data.get("projectModel", [])
                    
                    for proj in projects:
                        team_info["projects"].append({
                            "projectId": proj["id"],
                            "projectName": proj["name"]
                        })
                
                result.append(team_info)
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误：{e}")
            return []
        except Exception as e:
            print(f"❌ 获取项目列表失败：{e}")
            return []
    
    def display_projects(self, projects: List[Dict[str, Any]]) -> str:
        """
        格式化展示项目列表
        
        参数:
            projects: 项目列表
        
        返回:
            str: 格式化的展示文本
        """
        if not projects:
            return "❌ 没有找到任何项目"
        
        lines = []
        lines.append("\n📁 AiriLab 团队和项目列表：")
        lines.append("=" * 60)
        
        for i, team in enumerate(projects, 1):
            team_name = team.get('teamName', 'Unknown')
            team_id = team.get('teamId', 0)
            lines.append(f"\n【团队{i}】{team_name} (teamId: {team_id})")
            
            team_projects = team.get('projects', [])
            if team_projects:
                for j, proj in enumerate(team_projects, 1):
                    proj_name = proj.get('projectName', 'Unknown')
                    proj_id = proj.get('projectId', 0)
                    lines.append(f"  ├─ 【项目{j}】{proj_name} (projectId: {proj_id})")
            else:
                lines.append(f"  ⚠️ 该团队下暂无项目")
        
        lines.append("\n" + "=" * 60)
        lines.append("💡 提示：请用以下方式之一选择：")
        lines.append("   - projectId: '170923'")
        lines.append("   - 项目名称：'My Project 1'")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def parse_selection(self, user_input: str, projects: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        解析用户的选择（简化版：只支持 projectId 或项目名称）
        
        参数:
            user_input: 用户输入
            projects: 项目列表
        
        返回:
            dict: 选中的项目配置，如果解析失败则返回 None
        """
        user_input = user_input.strip()
        
        # 1. 尝试解析 projectId（纯数字）
        if user_input.isdigit():
            project_id = int(user_input)
            for team in projects:
                for proj in team.get('projects', []):
                    if proj.get('projectId') == project_id:
                        return {
                            "teamId": team.get('teamId', 0),
                            "projectId": project_id,
                            "projectName": proj.get('projectName', 'Unknown')
                        }
        
        # 2. 尝试解析项目名称（模糊匹配）
        for team in projects:
            for proj in team.get('projects', []):
                proj_name = proj.get('projectName', '')
                # 不区分大小写模糊匹配
                if user_input.lower() in proj_name.lower() or proj_name.lower() in user_input.lower():
                    return {
                        "teamId": team.get('teamId', 0),
                        "projectId": proj.get('projectId', 0),
                        "projectName": proj.get('projectName', 'Unknown')
                    }
        
        return None
    
    def select_and_save_project(self, token: str, user_selection: str) -> Dict[str, Any]:
        """
        选择项目并保存配置
        
        参数:
            token: JWT Token
            user_selection: 用户选择
        
        返回:
            dict: 选择结果
        """
        # 获取项目列表
        projects = self.get_teams_and_projects(token)
        
        if not projects:
            return {
                'success': False,
                'message': '无法获取项目列表'
            }
        
        # 解析用户选择
        selection = self.parse_selection(user_selection, projects)
        
        if not selection:
            return {
                'success': False,
                'message': f'无法解析选择：{user_selection}'
            }
        
        # 保存配置
        if self.config.save_project(
            selection['teamId'],
            selection['projectId'],
            selection['projectName']
        ):
            return {
                'success': True,
                'message': f"已选择：{selection['projectName']}",
                'config': selection
            }
        else:
            return {
                'success': False,
                'message': '保存配置失败'
            }


# ==================== 命令行入口 ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AiriLab 项目管理")
    parser.add_argument("action", choices=["list", "select", "show", "clear"],
                       help="操作类型")
    parser.add_argument("--selection", help="用户选择（用于 select）")
    
    args = parser.parse_args()
    
    config = AiriLabConfig()
    project = AiriLabProject(config)
    token = config.get_token()
    
    if args.action == "list":
        if not token:
            print("❌ Token 不存在，请先登录")
        else:
            projects = project.get_teams_and_projects(token)
            print(project.display_projects(projects))
    
    elif args.action == "select":
        if not token:
            print("❌ Token 不存在，请先登录")
        elif not args.selection:
            print("❌ 错误：select 需要 --selection 参数")
        else:
            result = project.select_and_save_project(token, args.selection)
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
    
    elif args.action == "show":
        proj_config = config.get_project()
        if proj_config:
            print("📁 当前项目配置：")
            print(f"   项目：{proj_config['projectName']}")
            print(f"   ID: {proj_config['projectId']}")
            print(f"   团队 ID: {proj_config['teamId']}")
        else:
            print("ℹ️ 没有保存的项目配置")
    
    elif args.action == "clear":
        config.clear_project()
        print("✅ 项目配置已清除")
