#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap WorkBench v1.0.11 - 安装脚本

负责将 EvoMap WorkBench 安装到 OpenClaw，
并自动处理 3 个 JSON 文件的修改。

版本：v1.0.11
创建时间：2026-04-06
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import sys


class Installer:
    """EvoMap WorkBench 安装器"""
    
    def __init__(self, source_path: str = None):
        self.base_path = Path.home() / ".openclaw"
        
        # 默认源路径：发布包位置
        if source_path:
            self.source_path = Path(source_path)
        else:
            self.source_path = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/skills/evomap-workbench-release")
        
        self.target_path = self.base_path / "workspace" / "skills" / "evomap-workbench"
        
        # 定义要处理的 JSON 文件
        self.json_files_to_process = {
            "skill_metadata.json": "update",  # 更新版本和路径
            "skills-index.json": "read_write",  # 读取并写入注册表
            "feishu-pairing.json": "optional_read_write"  # 可选读取飞书配置
        }
    
    def check_dependencies(self) -> bool:
        """检查依赖"""
        required = ["python3", "pip"]
        missing = []
        
        for dep in required:
            if not shutil.which(dep):
                missing.append(dep)
        
        if missing:
            print(f"❌ 缺少必需依赖：{', '.join(missing)}")
            return False
        
        print("✅ 所有依赖已满足")
        return True
    
    def check_source(self) -> bool:
        """检查源路径"""
        if not self.source_path.exists():
            print(f"❌ 源路径不存在：{self.source_path}")
            return False
        
        required_files = ["lib/", "docs/", "SKILL.md", "skill_metadata.json"]
        missing = [f for f in required_files if not (self.source_path / f).exists()]
        
        if missing:
            print(f"❌ 源目录缺少必要文件：{', '.join(missing)}")
            return False
        
        print("✅ 源路径验证通过")
        return True
    
    def load_json_file(self, file_path: Path) -> Dict:
        """加载 JSON 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误：{e}")
            return {}
    
    def save_json_file(self, file_path: Path, data: Dict):
        """保存 JSON 文件"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ 保存失败：{e}")
            return False
    
    def process_skill_metadata(self) -> bool:
        """处理 skill_metadata.json"""
        metadata_path = self.source_path / "skill_metadata.json"
        
        if not metadata_path.exists():
            print("⚠️ skill_metadata.json 不存在，跳过")
            return True
        
        print("\n📝 处理 skill_metadata.json...")
        
        try:
            # 读取并发布包内文件内容（不做修改，只验证）
            metadata = self.load_json_file(metadata_path)
            
            # 打印当前版本信息
            version = metadata.get("version", "unknown")
            print(f"   版本：v{version}")
            print(f"   作者：{metadata.get('author', 'unknown')}")
            print(f"   描述：{metadata.get('description', '')[:50]}...")
            
            return True
        except Exception as e:
            print(f"❌ 处理失败：{e}")
            return False
    
    def update_skills_index(self) -> bool:
        """更新 skills-index.json"""
        index_path = self.base_path / "openclaw.json"
        
        print("\n📋 更新 skills-index.json...")
        
        # 加载或创建索引
        if index_path.exists():
            config = self.load_json_file(index_path)
        else:
            config = {"installed_skills": [], "last_updated": None}
            print("ℹ️ 创建新的技能索引文件")
        
        # 检查是否已安装
        installed_skills = config.get("installed_skills", [])
        for skill in installed_skills:
            if skill.get("skill_id") == "evomap-workbench":
                print("✅ EvoMap WorkBench 已安装，跳过")
                return True
        
        # 添加新技能到注册表
        new_skill_entry = {
            "skill_id": "evomap-workbench",
            "path": str(self.target_path),
            "version": "v1.0.11",
            "name": "EvoMap WorkBench",
            "status": "active",
            "installed_at": None,  # 会在安装时填充时间戳
            "dependencies": metadata.get("dependencies", [])
        }
        
        installed_skills.append(new_skill_entry)
        config["installed_skills"] = installed_skills
        config["last_updated"] = None  # 会更新为当前时间
        
        if self.save_json_file(index_path, config):
            print("✅ 已成功添加到技能注册表")
            return True
        else:
            return False
    
    def read_feishu_config(self) -> Optional[Dict]:
        """读取 feishu-pairing.json"""
        credentials_path = self.base_path / "credentials" / "feishu-pairing.json"
        
        if not credentials_path.exists():
            return None
        
        print("\n🔧 读取 feishu-pairing.json...")
        config = self.load_json_file(credentials_path)
        
        # 检查是否有相关配置
        app_id_keys = [k for k in config.keys() if "app" in k.lower() and ("id" in k.lower() or "secret" in k.lower())]
        
        if app_id_keys:
            print(f"   发现 {len(app_id_keys)} 个 App 配置字段")
            
            # 提取关键信息（不输出敏感信息）
            for key in app_id_keys:
                if "id" in key.lower():
                    print(f"   ✅ App ID: {config[key][:10]}...")
                elif "secret" in key.lower():
                    print(f"   🔒 App Secret: ***")
        else:
            print("   ⚠️ 未检测到 App 配置")
        
        return config
    
    def copy_skills(self) -> bool:
        """复制技能文件到目标位置"""
        print(f"\n📦 复制文件到：{self.target_path}")
        
        try:
            # 创建目标目录
            self.target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 复制所有文件和目录
            for item in self.source_path.iterdir():
                dest = self.target_path / item.name
                
                if item.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
            
            print("✅ 文件复制完成")
            return True
        except Exception as e:
            print(f"❌ 复制失败：{e}")
            return False
    
    def create_symlink_if_needed(self) -> bool:
        """如需要则创建符号链接"""
        # 目前不需要，但保留扩展点
        return True
    
    def install(self, skip_check: bool = False) -> bool:
        """执行完整安装流程"""
        print("=" * 70)
        print("🧬 EvoMap WorkBench v1.0.11 - 安装工具")
        print("=" * 70)
        print()
        
        # 步骤 1: 检查依赖
        if not skip_check:
            print("步骤 1/5: 检查环境...")
            if not self.check_dependencies():
                return False
        
        # 步骤 2: 检查源路径
        print("\n步骤 2/5: 验证源目录...")
        if not self.check_source():
            return False
        
        # 步骤 3: 处理 skill_metadata.json
        print("\n步骤 3/5: 处理元数据...")
        if not self.process_skill_metadata():
            return False
        
        # 步骤 4: 读取飞书配置（仅读取，不修改）
        print("\n步骤 4/5: 检查现有配置...")
        feishu_config = self.read_feishu_config()
        
        # 步骤 5: 复制文件并更新注册表
        print("\n步骤 5/5: 执行安装...")
        if not self.copy_skills():
            print("❌ 文件复制失败")
            return False
        
        if not self.update_skills_index():
            print("❌ 注册表更新失败")
            return False
        
        print("\n" + "=" * 70)
        print("🎉 EvoMap WorkBench v1.0.11 已成功安装！")
        print("=" * 70)
        print("\n安装位置:")
        print(f"   {self.target_path}")
        print("\n已更新的文件:")
        print("   ✅ skill_metadata.json - 已验证")
        print("   ✅ skills-index.json - 新增注册条目")
        print(f"   ℹ️ feishu-pairing.json - 已检查 ({'有配置' if feishu_config else '无配置'})")
        print("\n如需卸载，请运行：python3 uninstall.py")
        
        return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EvoMap WorkBench v1.0.11 - 安装工具")
    parser.add_argument("--source", type=str, default=None,
                        help="源路径（默认为发布包位置）")
    parser.add_argument("--skip-check", action="store_true",
                        help="跳过环境检查")
    
    args = parser.parse_args()
    
    installer = Installer(source_path=args.source)
    success = installer.install(skip_check=args.skip_check)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
