#!/usr/bin/env python3
"""
feishu-whisper-voice 技能注册脚本
将 Whisper 语音交互技能添加到飞书技能池中
"""

import os
import sys
from pathlib import Path

SKILL_PATH = "~/.openclaw/extensions/openclaw-lark/skills/feishu-whisper-voice"

def check_skill_files():
    """检查技能文件是否存在"""
    skill_dir = Path(SKILL_PATH).expanduser()
    
    required_files = [
        "SKILL.md",
        "DEPENDENCIES.md",
        "CONFIG.md",
        "check_dependencies.py"
    ]
    
    print("=" * 60)
    print("🔍 检查技能文件")
    print("=" * 60)
    
    all_exists = True
    for file in required_files:
        filepath = skill_dir / file
        if filepath.exists():
            size = filepath.stat().st_size
            status = "✅"
            print(f"{status} {file:30s} ({size:,} bytes)")
        else:
            status = "❌"
            print(f"{status} {file:30s} NOT FOUND")
            all_exists = False
    
    return all_exists

def check_skill_in_available():
    """检查技能是否已在可用技能列表中"""
    # OpenClaw 通过扫描目录自动加载技能
    skill_dir = Path(SKILL_PATH).expanduser()
    
    if not skill_dir.exists():
        print("\n❌ 技能目录不存在")
        return False
    
    # 检查 SKILL.md 文件
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print("❌ SKILL.md 文件缺失")
        return False
    
    # 读取并验证技能描述
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "feishu-whisper-voice" in content and "Faster-Whisper" in content:
        print("\n✅ 技能描述文件有效")
        return True
    else:
        print("\n❌ 技能描述文件格式错误")
        return False

def register_skill():
    """注册技能到 OpenClaw"""
    print("\n" + "=" * 60)
    print("📝 注册技能")
    print("=" * 60)
    
    skill_dir = Path(SKILL_PATH).expanduser()
    
    # Step 1: 确保目录存在
    if not skill_dir.exists():
        print(f"❌ 创建目录失败：{skill_dir}")
        return False
    
    print(f"✅ 技能目录已存在：{skill_dir}")
    
    # Step 2: 检查 SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print("❌ SKILL.md 文件缺失")
        return False
    
    print(f"✅ SKILL.md 已存在 ({skill_md.stat().st_size:,} bytes)")
    
    # Step 3: OpenClaw 会自动扫描目录加载技能
    print("\n🔄 OpenClaw 自动扫描机制:")
    print("   - OpenClaw 在启动时会扫描 ~/.openclaw/extensions/openclaw-lark/skills/")
    print("   - 每个子目录如果包含 SKILL.md，就会被自动识别为可用技能")
    print("   - 无需手动注册！文件存在即注册成功 ✅")
    
    return True

def verify_registration():
    """验证技能是否可被加载"""
    print("\n" + "=" * 60)
    print("✅ 验证注册结果")
    print("=" * 60)
    
    # 列出所有飞书相关技能
    skills_dir = Path("~/.openclaw/extensions/openclaw-lark/skills").expanduser()
    
    if not skills_dir.exists():
        print(f"❌ 技能目录不存在：{skills_dir}")
        return False
    
    print("\n📚 当前飞书相关技能列表:")
    print("-" * 60)
    
    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            skill_md = item / "SKILL.md"
            status = "✅" if skill_md.exists() else "❌"
            
            # 获取技能名称和描述
            name = item.name
            desc = ""
            if skill_md.exists():
                with open(skill_md, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    desc = first_line.split(" - ")[1] if " - " in first_line else first_line
            
            print(f"   {status} {name:30s}")
    
    # 检查 feishu-whisper-voice
    whisper_skill = skills_dir / "feishu-whisper-voice"
    if whisper_skill.exists() and (whisper_skill / "SKILL.md").exists():
        print("\n✅ feishu-whisper-voice 已注册到技能池！")
        
        # 显示技能信息
        with open(whisper_skill / "SKILL.md", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:5]:
                print(f"   {line.strip()}")
    else:
        print("\n❌ feishu-whisper-voice 未注册成功")
    
    return True

def main():
    """主函数"""
    try:
        # 检查文件
        if not check_skill_files():
            print("\n❌ 技能文件不完整，请先补充缺失的文件")
            sys.exit(1)
        
        # 验证描述
        if not check_skill_in_available():
            print("\n❌ 技能描述无效")
            sys.exit(1)
        
        # 注册技能
        if not register_skill():
            sys.exit(1)
        
        # 验证结果
        verify_registration()
        
        # 总结
        print("\n" + "=" * 60)
        print("🎉 技能注册完成！")
        print("=" * 60)
        print("""
下一步操作:

1. ✅ 文件检查 - 已完成
2. ✅ 目录存在 - 已确认
3. ✅ SKILL.md - 已验证
4. ⬜ OpenClaw 重启 - 可选 (如果当前会话未加载新技能)

如需重新加载技能，可以：
   - 重启 OpenClaw: openclaw gateway restart
   - 或等待下次自动扫描

技能已注册到飞书技能池！
        """)
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
