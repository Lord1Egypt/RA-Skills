#!/usr/bin/env python3
"""
OpenClaw Installation Finder Module
自动查找系统中的OpenClaw安装目录
"""

import os
import glob
import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Tuple


class OpenClawFinder:
    """自动查找OpenClaw安装目录"""
    
    COMMON_PATHS = [
        "~/.openclaw",
        "~/.config/openclaw",
        "~/.local/share/openclaw",
        "~/openclaw",
        "/opt/openclaw",
        "/usr/local/share/openclaw",
    ]
    
    MARKERS = [
        "agents",
        "workspace",
        "config.json",
        "settings.json",
    ]
    
    def __init__(self):
        self._found_paths: List[Path] = []
        self._primary_path: Optional[Path] = None
        
    def find_all(self) -> List[Path]:
        """查找所有可能的OpenClaw安装目录"""
        self._found_paths = []
        
        # 1. 检查环境变量
        env_path = os.environ.get('OPENCLAW_HOME')
        if env_path and self._is_valid_openclaw(Path(env_path)):
            self._found_paths.append(Path(env_path))
        
        # 2. 检查常见路径
        for path_str in self.COMMON_PATHS:
            expanded = Path(path_str).expanduser()
            if self._is_valid_openclaw(expanded) and expanded not in self._found_paths:
                self._found_paths.append(expanded)
        
        # 3. 全局搜索（用户主目录下）
        home = Path.home()
        for pattern in [
            str(home / "**/.openclaw"),
            str(home / "**/openclaw"),
        ]:
            try:
                for path in glob.glob(pattern, recursive=True):
                    path_obj = Path(path)
                    if path_obj.is_dir() and self._is_valid_openclaw(path_obj):
                        if path_obj not in self._found_paths:
                            self._found_paths.append(path_obj)
            except Exception:
                pass
        
        return self._found_paths
    
    def find_primary(self) -> Optional[Path]:
        """查找主要的OpenClaw安装目录"""
        if self._primary_path:
            return self._primary_path
            
        paths = self.find_all()
        if not paths:
            return None
        
        # 优先选择包含最多agent的路径
        best_path = None
        max_agents = 0
        
        for path in paths:
            agents_dir = path / "agents"
            if agents_dir.exists():
                agent_count = len([d for d in agents_dir.iterdir() if d.is_dir()])
                if agent_count > max_agents:
                    max_agents = agent_count
                    best_path = path
        
        # 如果没有找到包含agents的，选择第一个
        self._primary_path = best_path or paths[0]
        return self._primary_path
    
    def _is_valid_openclaw(self, path: Path) -> bool:
        """检查路径是否是有效的OpenClaw安装目录"""
        if not path.exists() or not path.is_dir():
            return False
        
        # 检查是否包含至少一个标记文件/目录
        marker_count = sum(1 for marker in self.MARKERS if (path / marker).exists())
        return marker_count >= 1
    
    def get_agents_dir(self) -> Optional[Path]:
        """获取agents目录"""
        primary = self.find_primary()
        if not primary:
            return None
        agents_dir = primary / "agents"
        return agents_dir if agents_dir.exists() else None
    
    def get_agent_list(self) -> List[Dict]:
        """获取所有agent列表"""
        agents_dir = self.get_agents_dir()
        if not agents_dir:
            return []
        
        agents = []
        for agent_dir in sorted(agents_dir.iterdir()):
            if agent_dir.is_dir():
                sessions_file = agent_dir / "sessions" / "sessions.json"
                avatar_file = agent_dir / "avatar.png"
                config_file = agent_dir / "config.json"
                
                agent_info = {
                    "name": agent_dir.name,
                    "path": str(agent_dir),
                    "has_sessions": sessions_file.exists(),
                    "has_avatar": avatar_file.exists(),
                    "has_config": config_file.exists(),
                }
                agents.append(agent_info)
        
        return agents
    
    def get_agent_sessions_path(self, agent_name: str) -> Optional[Path]:
        """获取指定agent的sessions.json路径"""
        agents_dir = self.get_agents_dir()
        if not agents_dir:
            return None
        
        sessions_path = agents_dir / agent_name / "sessions" / "sessions.json"
        return sessions_path if sessions_path.exists() else None
    
    def get_agent_avatar_path(self, agent_name: str) -> Optional[Path]:
        """获取指定agent的头像路径"""
        agents_dir = self.get_agents_dir()
        if not agents_dir:
            return None
        
        # 优先查找自定义头像
        custom_avatar = agents_dir / agent_name / "avatar.png"
        if custom_avatar.exists():
            return custom_avatar
        
        # 查找workspace中的头像
        primary = self.find_primary()
        if primary:
            workspace_avatar = primary / "workspace" / "agent-avatars" / f"{agent_name}-avatar.png"
            if workspace_avatar.exists():
                return workspace_avatar
        
        return None
    
    def get_version(self) -> Tuple[Optional[str], Optional[str]]:
        """
        获取OpenClaw版本信息
        返回: (版本号字符串如 '2026.3.24', 完整版本字符串)
        """
        try:
            result = subprocess.run(
                ['openclaw', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                full_version = result.stdout.strip()
                # 解析版本号，格式如 "OpenClaw 2026.3.24 (cff6dc9)"
                match = re.search(r'(\d{4}\.\d+\.\d+)', full_version)
                if match:
                    return match.group(1), full_version
                return None, full_version
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return None, None
    
    def check_version(self, min_version: str = "2026.3.24") -> Tuple[bool, Optional[str], Optional[str]]:
        """
        检查OpenClaw版本是否满足最低要求
        返回: (是否满足, 当前版本, 提示信息)
        """
        version, full_version = self.get_version()
        
        if not version:
            return False, None, "无法获取 OpenClaw 版本，请确保已安装 openclaw"
        
        # 版本比较 (2026.3.24 格式)
        def parse_ver(v: str):
            parts = v.split('.')
            return tuple(int(p) for p in parts[:3])
        
        current = parse_ver(version)
        required = parse_ver(min_version)
        
        if current < required:
            return False, version, f"OpenClaw 版本过旧 (当前: {version}, 需要: ≥{min_version})"
        
        return True, version, None


# 全局finder实例
_finder_instance: Optional[OpenClawFinder] = None


def get_finder() -> OpenClawFinder:
    """获取全局finder实例"""
    global _finder_instance
    if _finder_instance is None:
        _finder_instance = OpenClawFinder()
    return _finder_instance


def find_openclaw_home() -> Optional[Path]:
    """快捷函数：查找OpenClaw主目录"""
    return get_finder().find_primary()


if __name__ == "__main__":
    # 测试查找功能
    finder = OpenClawFinder()
    
    print("=" * 50)
    print("OpenClaw Installation Finder")
    print("=" * 50)
    
    all_paths = finder.find_all()
    print(f"\n找到 {len(all_paths)} 个OpenClaw安装目录:")
    for path in all_paths:
        print(f"  - {path}")
    
    primary = finder.find_primary()
    print(f"\n主要安装目录: {primary}")
    
    agents = finder.get_agent_list()
    print(f"\n发现 {len(agents)} 个Agent:")
    for agent in agents:
        status = "✓" if agent["has_sessions"] else "✗"
        avatar = "🖼️" if agent["has_avatar"] else "❌"
        print(f"  - {agent['name']}: sessions[{status}] avatar[{avatar}]")
