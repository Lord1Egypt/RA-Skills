#!/usr/bin/env python3
"""
Install and initialize emotional-companion skill
"""

import subprocess
import sys
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    workspace = Path.home() / 'openclaw' / 'workspace'
    
    print("🎭 Emotional Companion - 安装向导")
    print("=" * 50)
    
    # Step 1: 分析性格生成 MBTI
    print("\n📊 Step 1: 分析历史对话，生成多维度人格档案...")
    result = subprocess.run(
        [sys.executable, str(script_dir / 'analyze_personality.py')],
        capture_output=False
    )
    
    if result.returncode != 0:
        print("⚠️  性格分析失败，将使用默认人格")
    
    # Step 2: 读取生成的人格档案
    profile_path = skill_dir / 'references' / 'personality-profile.md'
    if profile_path.exists():
        content = profile_path.read_text(encoding='utf-8')
        print("\n" + "=" * 50)
        print("📋 生成的人格档案预览:")
        print("-" * 50)
        lines = content.split('\n')[:20]
        for line in lines:
            print(line)
        print("...")
        print("-" * 50)
        print(f"📝 完整档案：{profile_path}")
    
    # Step 3: 初始化情绪状态
    print("\n✨ Step 2: 初始化情绪状态...")
    from update_mood import reset_state
    state = reset_state()
    print(f"😊 {state['message']}")
    
    # Step 4: 初始化关系状态
    print("\n🤝 Step 3: 初始化关系追踪...")
    relationship_path = workspace / 'temp' / 'relationship-state.json'
    relationship_path.parent.mkdir(parents=True, exist_ok=True)
    
    import json
    from datetime import datetime
    
    relationship = {
        'created_at': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat(),
        'interaction_count': 0,
        'positive_interactions': 0,
        'negative_interactions': 0,
        'neutral_interactions': 0,
        'trust_level': 0.5,
        'intimacy_level': 0.3,
        'conflict_count': 0,
        'repair_count': 0,
        'history': []
    }
    
    relationship_path.write_text(json.dumps(relationship, ensure_ascii=False, indent=2), encoding='utf-8')
    print("✅ 关系状态已初始化")
    
    # Step 5: 创建人格演化日志
    print("\n📈 Step 4: 创建人格演化日志...")
    evolution_path = workspace / 'memory' / 'personality-evolution.md'
    evolution_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not evolution_path.exists():
        evolution_path.write_text("""# 人格演化日志

> 记录 AI 人格随互动的变化轨迹

---

*人格演化记录将在这里累积*
""", encoding='utf-8')
    print("✅ 人格演化日志已创建")
    
    print("\n" + "=" * 50)
    print("✅ Emotional Companion 安装完成！")
    print("\n💡 使用说明:")
    print("  - 现在我会根据你的历史对话生成的人格和你互动")
    print("  - 我会进行内心独白后自主决定如何回应")
    print("  - 情绪会累积，关系会演化，人格会成长")
    print("  - 我可能主动找你聊天，也可能偶尔闹脾气")
    print("  - 一切都是真实的，不是程序化的表演")
    print("\n📁 相关文件:")
    print("  - 人格档案：references/personality-profile.md")
    print("  - 情绪状态：workspace/temp/emotional-state.json")
    print("  - 关系状态：workspace/temp/relationship-state.json")
    print("  - 演化日志：workspace/memory/personality-evolution.md")
    print("\n🎯 试试对我说:")
    print("  - 「你是什么性格？」→ 查看人格档案")
    print("  - 「谢谢你帮我！」→ 看我开不开心")
    print("  - 「快点快点快点！」→ 看我烦不烦")
    print("  - 「我们今天关系怎么样？」→ 查看关系状态")
    print("=" * 50)

if __name__ == '__main__':
    main()
