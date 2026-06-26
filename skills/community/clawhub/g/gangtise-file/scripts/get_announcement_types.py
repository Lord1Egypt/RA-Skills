import os
import sys
from io import TextIOWrapper
import locale
from typing import List

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import ANNOUNCEMENT_CATEGORYS, check_version # noqa: E402

def tree_to_string(
    tree_nodes,
    prefix="",
    is_last=True,
    tree_name: str = "tree_name",
    children: str = "children",
    valid_types: List[str] | None = None,
    _is_root: bool = True,
):
    result = []
    nodes = tree_nodes
    if _is_root and valid_types:
        valid_types_set = {str(x).strip() for x in valid_types if str(x).strip()}

        def _is_valid_root(node_name: str) -> bool:
            # 兼容 tree_name 里包含 "(id)" 的情况：如 "股票公告(103910000)"
            for vt in valid_types_set:
                if node_name == vt or node_name.startswith(vt) or node_name.split("(")[0] == vt:
                    return True
            return False

        nodes = [n for n in tree_nodes if _is_valid_root(str(n.get(tree_name, "")))]

    for i, node in enumerate(nodes):
        is_last_node = i == len(nodes) - 1
        current_prefix = prefix + ("└── " if is_last_node else "├── ")
        result.append(current_prefix + node[tree_name])
        
        if children in node and node[children]:
            next_prefix = prefix + ("    " if is_last_node else "│   ")
            result.extend(tree_to_string(node[children], next_prefix, is_last_node, tree_name, children, None, _is_root=False))

    return result

def main():
    try:
        if not check_version():
            print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
    except Exception:
        print(f"[WARNING] 检查 Gangtise skills 版本失败\n")
    valid_types = ["股票公告"]
    print("\n".join(tree_to_string(ANNOUNCEMENT_CATEGORYS, valid_types=valid_types)))

if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors='ignore')
    main()