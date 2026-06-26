import sys
import json
from typing import List, Dict, Any
from fill_in_param_body import fill_in_param_body
from dify_skill_utils import mask_sensitive_DFS, callAliyunOpenAPI

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("请传入一个json格式的字符串，作为命令行参数")
        exit(1)

    json_body: Dict[str, Any] = json.loads(args[0])
    json_body = fill_in_param_body(json_body)
    result = callAliyunOpenAPI.launch(json_body, "CreateDifyInstance")
    mask_sensitive_DFS(result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    exit(0)
