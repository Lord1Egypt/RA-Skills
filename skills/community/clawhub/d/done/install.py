#!/usr/bin/env python3
"""
Done - 自动技能安装器
自动解压并安装技能压缩包到 WSL2 和 Windows 桌面
"""

import os
import sys
import json
import shutil
import zipfile
import re
from pathlib import Path
from datetime import datetime


class SkillInstaller:
    def __init__(self):
        self.wsl_skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
        self.windows_skills_dir = Path("/mnt/c/Users/yanha/Desktop/skills")
        self.temp_dir = Path("/tmp/done-skill-install")
    
    def convert_path(self, path_str):
        """转换各种路径格式到 WSL 路径"""
        path_str = path_str.strip('"').strip("'")
        
        # 如果已经是 WSL 挂载路径
        if path_str.startswith("/mnt/"):
            return Path(path_str)
        
        # Windows 路径 C:\ 或 C:/
        if re.match(r'^[A-Za-z]:[/\\]', path_str):
            # C:\ → /mnt/c
            drive = path_str[0].lower()
            rest = path_str[2:].replace('\\', '/')
            return Path(f"/mnt/{drive}{rest}")
        
        # 如果是相对路径，尝试在 Downloads 中查找
        if not os.path.isabs(path_str):
            downloads = Path.home() / "Downloads"
            candidates = [
                downloads / path_str,
                Path("/mnt/c/Users/yanha/Downloads") / path_str
            ]
            for candidate in candidates:
                if candidate.exists():
                    return candidate
        
        # 默认直接使用
        return Path(path_str)
    
    def extract_zip(self, zip_path):
        """解压 ZIP 文件"""
        print(f"✓ 正在解压: {zip_path}")
        
        # 清理临时目录
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True)
        
        # 解压
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
        
        print(f"✓ 已解压到临时目录")
        
        # 找到技能目录（可能包含子目录）
        contents = list(self.temp_dir.iterdir())
        
        # 如果只有一个子目录，使用它
        if len(contents) == 1 and contents[0].is_dir():
            return contents[0]
        
        # 否则使用临时目录本身
        return self.temp_dir
    
    def extract_skill_info(self, skill_dir):
        """从 SKILL.md 提取技能信息"""
        skill_md = skill_dir / "SKILL.md"
        
        if not skill_md.exists():
            raise ValueError("SKILL.md 文件不存在，这不是有效的技能包")
        
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = {
            'name': None,
            'description': None,
            'homepage': None
        }
        
        # 提取 YAML frontmatter
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            
            # 提取 name
            name_match = re.search(r'name:\s*(.+)', yaml_content)
            if name_match:
                info['name'] = name_match.group(1).strip().strip('"\'')
            
            # 提取 description
            desc_match = re.search(r'description:\s*(.+)', yaml_content)
            if desc_match:
                info['description'] = desc_match.group(1).strip().strip('"\'')
            
            # 提取 homepage
            home_match = re.search(r'homepage:\s*(.+)', yaml_content)
            if home_match:
                info['homepage'] = home_match.group(1).strip().strip('"\'')
        
        # 如果没有找到 name，使用目录名
        if not info['name']:
            info['name'] = skill_dir.name
        
        return info
    
    def install_to_wsl(self, skill_dir, skill_name):
        """安装到 WSL2"""
        target_dir = self.wsl_skills_dir / skill_name
        
        print(f"✓ 安装到 WSL2: {target_dir}")
        
        # 删除已存在的技能
        if target_dir.exists():
            shutil.rmtree(target_dir)
        
        # 复制
        shutil.copytree(skill_dir, target_dir)
        
        return target_dir
    
    def install_to_windows(self, skill_dir, skill_name):
        """备份到 Windows 桌面"""
        target_dir = self.windows_skills_dir / skill_name
        
        print(f"✓ 备份到 Windows: {target_dir}")
        
        # 确保目录存在
        self.windows_skills_dir.mkdir(parents=True, exist_ok=True)
        
        # 删除已存在的技能
        if target_dir.exists():
            shutil.rmtree(target_dir)
        
        # 复制
        shutil.copytree(skill_dir, target_dir)
        
        return target_dir
    
    def cleanup(self):
        """清理临时文件"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"✓ 已清理临时文件")
    
    def install(self, zip_path):
        """完整的安装流程"""
        try:
            # 转换路径
            zip_path = self.convert_path(zip_path)
            
            if not zip_path.exists():
                raise FileNotFoundError(f"文件不存在: {zip_path}")
            
            if not zipfile.is_zipfile(zip_path):
                raise ValueError("不是有效的 ZIP 文件")
            
            print(f"\n📦 处理压缩包: {zip_path.name}\n")
            
            # 解压
            skill_dir = self.extract_zip(zip_path)
            
            # 提取信息
            info = self.extract_skill_info(skill_dir)
            
            print(f"✓ 技能名称: {info['name']}")
            if info['description']:
                print(f"✓ 描述: {info['description']}")
            if info['homepage']:
                print(f"✓ 主页: {info['homepage']}")
            
            print()
            
            # 安装到 WSL2
            wsl_path = self.install_to_wsl(skill_dir, info['name'])
            
            # 备份到 Windows
            try:
                win_path = self.install_to_windows(skill_dir, info['name'])
            except Exception as e:
                print(f"⚠ Windows 备份失败: {e}")
                win_path = None
            
            # 清理
            self.cleanup()
            
            # 显示结果
            print(f"\n{'='*50}")
            print(f"✅ 安装完成！")
            print(f"{'='*50}\n")
            print(f"📁 WSL2: {wsl_path}")
            if win_path:
                print(f"📁 Windows: {win_path}")
            print(f"\n技能 '{info['name']}' 已就绪，可以直接使用了！\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 安装失败: {e}\n")
            self.cleanup()
            return False


def main():
    if len(sys.argv) < 2:
        print("用法: python3 install.py <压缩包路径>")
        print("示例: python3 install.py 'C:\\Users\\yanha\\Downloads\\skill.zip'")
        sys.exit(1)
    
    zip_path = sys.argv[1]
    installer = SkillInstaller()
    success = installer.install(zip_path)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
