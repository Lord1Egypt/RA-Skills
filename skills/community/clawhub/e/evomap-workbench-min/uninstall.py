#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap WorkBench v1.0.11 - 卸载脚本

负责安全地从 OpenClaw 中移除 EvoMap WorkBench，
并恢复被修改的 3 个 JSON 文件到原始状态。

版本：v1.0.11
创建时间：2026-04-06
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import sys


class Uninstaller:
    """EvoMap WorkBench 卸载器"""
    
    def __init__(self):
        self.base_path = Path.home() / ".openclaw"
        self.installed_skill_path = None
        self.feishu_credentials_path = None
        
        # 定义需要恢复的 JSON 文件
        self.files_to_restore = {
            "skills-index.json": None,  # 技能索引表
            "feishu-pairing.json": None,  # 飞书凭证
            "skills-config": None  # 技能实例配置目录
        }
        
    def find_installed_skill(self) -> Optional[Path]:
        """查找已安装的 EvoMap WorkBench"""
        possible_paths = [
            "/home/admin/.openclaw/workspace/skills/evomap-workbench",
            "/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/skills/evomap-workbench",
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                self.installed_skill_path = Path(path)
                return self.installed_skill_path
        
        print("⚠️ 未找到已安装的 EvoMap WorkBench")
        return None
    
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
    
    def restore_skills_index(self) -> bool:
        """恢复 skills-index.json"""
        index_path = self.base_path / "openclaw.json"
        
        if not index_path.exists():
            print("✅ skills-index.json 不存在，无需恢复")
            return True
        
        print("\n📋 处理 skills-index.json...")
        
        # 加载当前配置
        config = self.load_json_file(index_path)
        
        # 检查是否包含 EvoMap WorkBench
        installed_skills = config.get("installed_skills", [])
        original_length = len(installed_skills)
        
        # 过滤掉 EvoMap WorkBench
        new_skills = [
            skill for skill in installed_skills 
            if skill.get("skill_id") != "evomap-workbench"
        ]
        
        if len(new_skills) < original_length:
            # 找到了 EvoMap WorkBench，删除它
            config["installed_skills"] = new_skills
            if self.save_json_file(index_path, config):
                print(f"✅ 已从注册表移除 (原 {original_length} 项 → 现 {len(new_skills)} 项)")
                return True
            else:
                return False
        else:
            print("✅ EvoMap WorkBench 不在注册表中，无需恢复")
            return True
    
    def restore_feishu_config(self, remove_app_config: bool = True) -> bool:
        """恢复 feishu-pairing.json"""
        credentials_path = self.base_path / "credentials" / "feishu-pairing.json"
        
        if not credentials_path.exists():
            print("✅ feishu-pairing.json 不存在，无需恢复")
            return True
        
        print("\n🔧 处理 feishu-pairing.json...")
        
        # 加载当前配置
        config = self.load_json_file(credentials_path)
        
        # 检查是否包含 EvoMap 相关配置
        evomap_keys = ["evomap_appId", "evomap_appSecret", "cli_a929676f8bf81cc7"]
        keys_to_check = []
        
        for key in config.keys():
            for evomap_key in evomap_keys:
                if evomap_key.lower() in key.lower():
                    keys_to_check.append(key)
        
        if keys_to_check and remove_app_config:
            # 用户确认删除，移除相关字段
            for key in keys_to_check:
                del config[key]
            
            if self.save_json_file(credentials_path, config):
                print(f"✅ 已移除 EvoMap 相关配置 ({len(keys_to_check)} 个字段)")
                return True
            else:
                return False
        elif keys_to_check and not remove_app_config:
            print(f"ℹ️ 发现 {len(keys_to_check)} 个 EvoMap 相关字段，但未执行删除")
            return True
        else:
            print("✅ feishu-pairing.json 中无 EvoMap 配置，无需恢复")
            return True
    
    def remove_skills_config(self) -> bool:
        """删除技能实例配置文件"""
        config_dir = self.base_path / "config" / "skills"
        
        if not config_dir.exists():
            print("✅ 技能配置目录不存在，无需恢复")
            return True
        
        print("\n🗑️ 处理技能实例配置...")
        
        # 查找所有与 evomap 相关的配置文件
        evomap_configs = []
        for config_file in config_dir.iterdir():
            if config_file.is_file() and ("evomap" in config_file.name.lower() or "workbench" in config_file.name.lower()):
                evomap_configs.append(config_file)
        
        if evomap_configs:
            for config_file in evomap_configs:
                try:
                    config_file.unlink()
                    print(f"✅ 已删除：{config_file.name}")
                except Exception as e:
                    print(f"⚠️ 无法删除 {config_file.name}: {e}")
            return True
        else:
            print("✅ 技能配置目录中无 EvoMap 配置文件，无需恢复")
            return True
    
    def remove_installed_skill(self) -> bool:
        """删除已安装的技能实例"""
        if not self.installed_skill_path or not self.installed_skill_path.exists():
            print("✅ 已安装的 EvoMap WorkBench 不存在，无需删除")
            return True
        
        print(f"\n🗑️ 删除已安装的技能实例：{self.installed_skill_path}")
        
        try:
            shutil.rmtree(self.installed_skill_path)
            print(f"✅ 已删除：{self.installed_skill_path}")
            return True
        except Exception as e:
            print(f"❌ 删除失败：{e}")
            return False
    
    def uninstall(self, confirm_feishu_removal: bool = True) -> bool:
        """
        执行完整卸载流程
        
        Args:
            confirm_feishu_removal: 是否删除飞书配置
            
        Returns:
            是否成功卸载
        """
        print("=" * 70)
        print("🧬 EvoMap WorkBench v1.0.11 - 卸载程序")
        print("=" * 70)
        print()
        
        # 步骤 1: 查找已安装的技能
        print("步骤 1/5: 检查已安装技能...")
        if not self.find_installed_skill():
            print("❌ 无法继续：未找到已安装的 EvoMap WorkBench")
            return False
        print(f"✅ 找到：{self.installed_skill_path}")
        
        # 步骤 2: 询问用户是否要删除飞书配置
        print("\n步骤 2/5: 确认飞书配置处理方式...")
        if confirm_feishu_removal:
            response = input("是否删除 EvoMap WorkBench 使用的飞书 App 配置？(y/n): ")
            if response.lower() == 'y':
                confirm_feishu_removal = True
            else:
                confirm_feishu_removal = False
                print("ℹ️ 将保留飞书配置中的 EvoMap 相关字段")
        print(f"配置处理：{'删除' if confirm_feishu_removal else '保留'}")
        
        # 步骤 3: 从 OpenClaw 注册表移除
        print("\n步骤 3/5: 从注册表移除...")
        if not self.restore_skills_index():
            print("❌ 注册表恢复失败")
            return False
        print("✅ 注册表恢复完成")
        
        # 步骤 4: 恢复飞书配置
        print("\n步骤 4/5: 恢复飞书配置...")
        if not self.restore_feishu_config(confirm_feishu_removal):
            print("❌ 飞书配置恢复失败")
            return False
        print("✅ 飞书配置恢复完成")
        
        # 步骤 5: 删除技能配置文件和实例
        print("\n步骤 5/5: 清理文件...")
        if not self.remove_skills_config():
            print("⚠️ 技能配置清理部分完成")
        
        if not self.remove_installed_skill():
            print("❌ 技能实例删除失败")
            return False
        
        print("\n" + "=" * 70)
        print("🎉 EvoMap WorkBench 已成功卸载！")
        print("=" * 70)
        print("\n已恢复的文件:")
        print("  ✅ skills-index.json - 从注册表中移除")
        print("  ✅ feishu-pairing.json - 清除 EvoMap 相关配置" if confirm_feishu_removal else "  ⚠️ feishu-pairing.json - 保留 EvoMap 配置")
        print("  ✅ 技能配置文件 - 已删除")
        print("\n如需重新安装，请运行安装脚本。")
        
        return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EvoMap WorkBench v1.0.11 - 卸载工具")
    parser.add_argument("--keep-feishu", action="store_true", 
                        help="保留飞书配置中的 EvoMap 相关字段")
    parser.add_argument("--force", action="store_true", 
                        help="强制卸载，不提示")
    
    args = parser.parse_args()
    
    uninstaller = Uninstaller()
    
    if args.force:
        success = uninstaller.uninstall(confirm_feishu_removal=not args.keep_feishu)
    else:
        success = uninstaller.uninstall(confirm_feishu_removal=True)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
