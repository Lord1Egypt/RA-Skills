#!/usr/bin/env python3
"""
验证 daily_learning_summary 技能的完整性和可靠性
"""

import subprocess
import sys
from pathlib import Path

# 从技能目录定位
SKILL_ROOT = Path(__file__).parent.parent
SCRIPT = SKILL_ROOT / "scripts" / "daily_learning_summary.py"
LEARNING_DIR = Path(__file__).parents[4] / "memory" / "learning"  # workspace/memory/learning

def check_file(path, min_size=100):
    if not path.exists():
        return False, f"❌ 缺失: {path}"
    size = path.stat().st_size
    if size < min_size:
        return False, f"❌ 文件过小: {path} ({size} bytes)"
    return True, f"✅ 存在: {path} ({size} bytes)"

def run_script():
    print("🧪 测试脚本执行...")
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, cwd=str(SKILL_ROOT.parent))
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ 脚本执行失败: {result.stderr}")
        return False
    return True

def check_dependencies():
    print("🔍 检查依赖...")
    # 只需要标准库
    deps = ["json", "os", "datetime", "pathlib"]
    missing = []
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    if missing:
        print(f"❌ 缺失依赖: {missing}")
        return False
    print("✅ 所有依赖 (标准库) 就绪")
    return True

def check_output():
    print("📊 检查输出...")
    today = subprocess.check_output(["date", "+%Y-%m-%d"]).decode().strip()
    log_file = LEARNING_DIR / f"{today}.md"
    if not log_file.exists():
        print(f"❌ 今日日志不存在: {log_file}")
        return False
    content = log_file.read_text()
    if "📚 每日学习总结" not in content:
        print("❌ 日志格式不正确")
        return False
    print(f"✅ 日志生成正常: {log_file}")
    return True

def main():
    print("=" * 60)
    print(" FREE SKILL 可靠性验证: daily-learning-summary")
    print("=" * 60)

    checks = [
        ("脚本文件", check_file(SCRIPT)),
        ("日志目录", check_file(LEARNING_DIR, min_size=0)),
        ("依赖检查", check_dependencies()),
        ("脚本执行", run_script()),
        ("输出验证", check_output()),
    ]

    passed = sum(1 for _, (ok, _) in checks if ok)
    total = len(checks)

    print("\n" + "=" * 60)
    print(f"结果: {passed}/{total} 通过")
    if passed == total:
        print("✅ 技能可靠性: 高 - 可以发布为免费技能")
    else:
        print("⚠️  需要修复问题后再发布")
        for name, (ok, msg) in checks:
            if not ok:
                print(f"  - {name}: {msg}")
    print("=" * 60)

if __name__ == "__main__":
    main()
