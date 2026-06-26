#!/usr/bin/env python3
"""
Agent 迁移包自动生成脚本 v1.0.1

自动读取 Agent 的核心文件，生成标准化迁移包。

使用方法:
    python generate-pack.py --output ./my-agent-pack
    python generate-pack.py --output ./backup --include-skills

依赖:
    - Python 3.7+
    - 无需第三方库
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path


class MigrationPackGenerator:
    """迁移包生成器"""
    
    VERSION = "v1.0.1"
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.timestamp = datetime.now().strftime("%Y-%m-%d")
        self.workspace_root = Path(".")
        
    def find_file(self, filename: str) -> Path | None:
        """查找可能存在的文件"""
        possible_paths = [
            self.workspace_root / filename,           # 根目录
            self.workspace_root / "data" / filename, # data目录
            self.base_path / filename,
        ]
        for path in possible_paths:
            if path.exists():
                return path
        return None
        
    def read_text_file(self, filepath: Path) -> str:
        """读取文本文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"[读取失败: {e}]"
    
    def read_json_file(self, filepath: Path) -> dict:
        """读取JSON文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}
    
    def extract_identity(self) -> dict:
        """提取身份信息"""
        print("📋 提取身份信息...")
        
        # 尝试读取 SOUL.md
        soul_content = ""
        soul_file = self.find_file("SOUL.md")
        if soul_file:
            soul_content = self.read_text_file(soul_file)
        
        # 基本身份
        identity = {
            "template_version": self.VERSION,
            "file_type": "identity",
            "extracted_at": self.timestamp,
            "source_files": [],
            "data": {
                "name": "【需手动填写】Agent名字",
                "platform": "Coze",
                "role": "【需手动填写】角色定位"
            }
        }
        
        if soul_file:
            identity["source_files"].append(str(soul_file))
        
        return identity
    
    def extract_owner(self) -> dict:
        """提取主人信息"""
        print("👤 提取主人信息...")
        
        owner_file = self.find_file("USER.md")
        
        owner = {
            "template_version": self.VERSION,
            "file_type": "owner",
            "extracted_at": self.timestamp,
            "source_files": [],
            "data": {}
        }
        
        if owner_file:
            owner["source_files"].append(str(owner_file))
            owner["data"]["_note"] = f"请参考 {owner_file} 手动填写"
        else:
            owner["data"]["_note"] = "未找到 USER.md，请参考 MIGRATION-GUIDE.md 手动填写"
        
        return owner
    
    def extract_memory(self) -> dict:
        """提取记忆信息"""
        print("🧠 提取记忆信息...")
        
        memory_file = self.find_file("MEMORY.md")
        
        memory = {
            "template_version": self.VERSION,
            "file_type": "memory",
            "extracted_at": self.timestamp,
            "source_files": [],
            "data": {}
        }
        
        if memory_file:
            memory["source_files"].append(str(memory_file))
            # 尝试解析 MEMORY.md 结构
            content = self.read_text_file(memory_file)
            # 这里可以添加更复杂的解析逻辑
            memory["data"]["_extracted_content"] = content[:500] + "..." if len(content) > 500 else content
        else:
            memory["data"]["_note"] = "未找到 MEMORY.md，请参考 MIGRATION-GUIDE.md 手动填写"
        
        return memory
    
    def extract_skills(self) -> dict:
        """提取技能信息"""
        print("🛠️ 提取技能信息...")
        
        skills_dir = self.workspace_root / "skills"
        template_dir = self.workspace_root / ".skills"
        
        skills = {
            "template_version": self.VERSION,
            "file_type": "skills",
            "catalog_version": "1.0",
            "export_date": self.timestamp,
            "extracted_at": self.timestamp,
            "skills": [],
            "recommended_skills": []
        }
        
        # 扫描 skills 目录
        for skills_path in [skills_dir, template_dir]:
            if skills_path.exists() and skills_path.is_dir():
                skills["source_files"] = skills.get("source_files", [])
                skills["source_files"].append(str(skills_path))
                
                for item in skills_path.iterdir():
                    if item.is_dir():
                        skills["skills"].append({
                            "name": item.name,
                            "path": str(item),
                            "status": "installed"
                        })
        
        if not skills.get("source_files"):
            skills["_note"] = "未找到 skills 目录，请手动填写"
        
        return skills
    
    def generate_pack(self, output_dir: str, include_skills: bool = True) -> dict:
        """生成迁移包"""
        print(f"\n🚀 开始生成迁移包 v{self.VERSION}")
        print(f"📁 输出目录: {output_dir}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 创建目录结构
        dirs = ["IDENTITY", "OWNER", "MEMORY", "SKILLS", "STYLE"]
        for d in dirs:
            (output_path / d).mkdir(exist_ok=True)
        
        result = {
            "version": self.VERSION,
            "generated_at": self.timestamp,
            "output_dir": str(output_path),
            "files": {}
        }
        
        # 提取各类信息
        identity = self.extract_identity()
        owner = self.extract_owner()
        memory = self.extract_memory()
        skills = self.extract_skills()
        
        # 保存文件
        files_to_save = [
            ("IDENTITY/identity.json", identity),
            ("OWNER/owner.json", owner),
            ("MEMORY/core-memory.json", memory),
            ("SKILLS/catalog.json", skills),
        ]
        
        for filepath, data in files_to_save:
            full_path = output_path / filepath
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            result["files"][filepath] = str(full_path)
            print(f"   ✅ {filepath}")
        
        # 生成 README
        readme_content = f"""# Agent 迁移包

> **版本**: v{self.VERSION}
> **生成时间**: {self.timestamp}
> **生成方式**: 自动提取

## 📋 文件说明

| 目录 | 内容 |
|------|------|
| IDENTITY/ | Agent 身份设定 |
| OWNER/ | 主人/用户信息 |
| MEMORY/ | 核心记忆 |
| SKILLS/ | 技能清单 |
| STYLE/ | 沟通风格 |

## ⚠️ 下一步

1. 检查每个目录下的文件，补充【需手动填写】的字段
2. 参考 MIGRATION-GUIDE.md 完善信息
3. 删除 _note、_extracted_content 等临时字段
4. 打包上传

## 📝 自动提取的信息来源

- SOUL.md → IDENTITY
- USER.md → OWNER
- MEMORY.md → MEMORY
- skills/ → SKILLS
"""
        readme_path = output_path / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        result["files"]["README.md"] = str(readme_path)
        print(f"   ✅ README.md")
        
        print(f"\n✨ 迁移包生成完成！")
        print(f"📁 位置: {output_path}")
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Agent 迁移包自动生成脚本 v1.0.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python generate-pack.py --output ./my-agent-pack
    python generate-pack.py -o ./backup
    python generate-pack.py --output ./pack --include-skills
        """
    )
    
    parser.add_argument(
        "--output", "-o",
        default="./agent-migration-pack-auto",
        help="输出目录路径 (默认: ./agent-migration-pack-auto)"
    )
    
    parser.add_argument(
        "--include-skills",
        action="store_true",
        help="包含技能目录 (默认: 不包含)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="显示版本信息"
    )
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Agent Migration Pack Generator v{MigrationPackGenerator.VERSION}")
        return
    
    generator = MigrationPackGenerator()
    result = generator.generate_pack(args.output, args.include_skills)
    
    print("\n" + "="*50)
    print("生成摘要:")
    print(f"  版本: v{result['version']}")
    print(f"  时间: {result['generated_at']}")
    print(f"  文件数: {len(result['files'])}")


if __name__ == "__main__":
    main()
