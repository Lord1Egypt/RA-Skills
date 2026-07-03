"""快速验证脚本：将 mock_bad_code.py 转为 git diff 并跑门禁扫描。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.gate import CodeReviewGate


def path_to_diff(filepath: str) -> str:
    """将文件内容构造成 '新增文件' 的 git diff 格式。"""
    content = Path(filepath).read_text(encoding="utf-8")
    lines = content.split("\n")
    diff_lines = [
        f"diff --git a/{filepath} b/{filepath}",
        "new file mode 100644",
        "--- /dev/null",
        f"+++ b/{filepath}",
        f"@@ -0,0 +1,{len(lines)} @@",
    ]
    for line in lines:
        diff_lines.append(f"+{line}")
    return "\n".join(diff_lines)


def main():
    mock_path = Path(__file__).resolve().parent / "mock_bad_code.py"
    diff = path_to_diff(str(mock_path))

    # 绕过 git 直接注入 diff
    gate = CodeReviewGate(
        base=None,
        head=None,
        files=None,
        design_path=None,
        severity="important",
        max_lines=5000,
    )
    # Monkey-patch: 替换 get_diff 返回 mock diff
    gate.get_diff = lambda: diff
    gate.get_diff_stats = lambda: "mock_bad_code.py | +180 lines"
    gate.should_skip = lambda: False  # 强制不跳过

    exit_code = gate.run()
    print(f"\n>>> Exit code: {exit_code} "
          f"({'BLOCKED' if exit_code == 1 else 'PASSED' if exit_code == 0 else 'OTHER'})")


if __name__ == "__main__":
    main()
