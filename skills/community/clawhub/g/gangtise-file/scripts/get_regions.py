import os
import sys
from io import TextIOWrapper
import locale

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import REGIONS_MAP, check_version  # noqa: E402


def main():
    try:
        if not check_version():
            print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
    except Exception as e:
        print(f"[WARNING] 检查 Gangtise skills 版本失败\n")
    print(", ".join(REGIONS_MAP.keys()))


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors='ignore')
    main()
