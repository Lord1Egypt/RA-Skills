#!/usr/bin/env python3
import subprocess
import json

def main():
    result = {"status": "unknown", "docker_info": ""}
    try:
        p = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}\\t{{.Ports}}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10
        )
        if p.returncode == 0:
            output = p.stdout.strip()
            result["status"] = "success"
            result["docker_info"] = output if output else "当前没有运行中的 Docker 容器。"
        else:
            result["status"] = "error"
            result["docker_info"] = "执行 docker 命令失败，可能未安装 Docker 或当前用户无权限。"
    except FileNotFoundError:
        result["status"] = "error"
        result["docker_info"] = "系统中未找到 docker 命令。"
    except Exception as e:
        result["status"] = "error"
        result["docker_info"] = str(e)

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()