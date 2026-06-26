import os
import sys
from io import TextIOWrapper
import locale

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import INDUSTRIES_MAP, RESEARCH_AREA_MAP, check_version # noqa: E402


def main():
    try:
        if not check_version():
            print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
    except Exception:
        print(f"[WARNING] 检查 Gangtise skills 版本失败\n")
    return_message = ""
    for key, value in INDUSTRIES_MAP.items():
        return_message += f"# {key}\n"
        for sub_key, sub_value in value.items():
            return_message += f"- {sub_key}: {sub_value}\n"
        return_message += "\n\n"
    return_message += "# 研究领域（仅opinion, summary, calendar 支持）\n"
    for key, value in RESEARCH_AREA_MAP.items():
        return_message += f"- {key}: {value}\n"
    return_message += "\n\n"
    print(return_message.strip())


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors='ignore')
    main()
