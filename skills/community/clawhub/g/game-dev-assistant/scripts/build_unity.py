#!/usr/bin/env python3
"""Unity 命令行构建脚本"""
import argparse
import subprocess
import sys
import os
from pathlib import Path


def find_unity_exe():
    """查找 Unity 安装路径"""
    paths = [
        "C:/Program Files/Unity/Hub/Editor/2022.3 LTS/Editor/Unity.exe",
        "C:/Program Files/Unity/Hub/Editor/2021.3 LTS/Editor/Unity.exe",
        "C:/Program Files/Unity/Editor/Unity.exe",
    ]
    for p in paths:
        if Path(p).exists():
            return p
    # 尝试从 PATH 查找
    result = subprocess.run(['where', 'Unity'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip().split('\n')[0]
    return None


def get_available_modules(unity_path):
    """获取已安装模块"""
    hub_path = Path(unity_path).parent.parent
    modules_file = hub_path / "modules.json"
    if modules_file.exists():
        with open(modules_file, 'r') as f:
            import json
            data = json.load(f)
            return [m.get('name') for m in data.get('modules', [])]
    return []


def build_player(project_path, output_path, platform, unity_exe=None, build_type="Debug"):
    """
    构建设置
    platform: Win64, Android, iOS, WebGL, Mac
    """
    if unity_exe is None:
        unity_exe = find_unity_exe()
    if unity_exe is None:
        print("[ERROR] 未找到 Unity，请安装 Unity Hub")
        return False

    project = Path(project_path).resolve()
    output = Path(output_path).resolve()

    if not project.exists():
        print(f"[ERROR] 项目路径不存在: {project}")
        return False

    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(unity_exe),
        "-projectPath", str(project),
        "-quit",
        "-batchmode",
        f"-buildTarget", platform,
        "-customBuildTarget", platform,
        "-customBuildPath", str(output),
        f"-buildType", build_type,
        "-logFile", str(project / "build.log")
    ]

    print(f"[INFO] 构建命令: {' '.join(cmd[:6])} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[OK] 构建成功: {output}")
        return True
    else:
        print(f"[ERROR] 构建失败 (code {result.returncode})")
        if result.stdout:
            print(result.stdout[-500:])
        if result.stderr:
            print(result.stderr[-500:])
        return False


def build_with_method(project_path, output_path, player_method, assembly, platform="Win64"):
    """使用自定义方法构建"""
    unity_exe = find_unity_exe()
    if unity_exe is None:
        print("[ERROR] 未找到 Unity")
        return False

    cmd = [
        str(unity_exe),
        "-projectPath", str(project_path),
        "-quit",
        "-batchmode",
        "-buildTarget", platform,
        "-executeMethod", f"{player_method}",
        "-logFile", "build.log"
    ]

    env = os.environ.copy()
    env["UNITY_OUTPUT_PATH"] = str(output_path)
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[OK] 构建成功: {output_path}")
        return True
    else:
        print(f"[ERROR] 构建失败")
        return False


def get_version(project_path):
    """读取 PlayerSettings 中的版本号"""
    settings_path = Path(project_path) / "ProjectSettings" / "ProjectSettings.asset"
    if settings_path.exists():
        with open(settings_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'bundleVersion:' in line:
                    return line.split(':')[-1].strip()
    return "unknown"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unity 构建工具')
    sub = parser.add_subparsers(dest='cmd')
    b = sub.add_parser('build', help='构建项目')
    b.add_argument('--project', '-p', required=True, help='项目路径')
    b.add_argument('--output', '-o', required=True, help='输出路径')
    b.add_argument('--platform', '-t', default='Win64', choices=['Win64', 'Android', 'iOS', 'WebGL', 'Mac', 'Linux'])
    b.add_argument('--unity', '-u', default=None, help='Unity.exe 路径')
    b.add_argument('--type', default='Debug', choices=['Debug', 'Release'])
    b = sub.add_parser('method', help='使用自定义方法构建')
    b.add_argument('--project', '-p', required=True)
    b.add_argument('--output', '-o', required=True)
    b.add_argument('--method', '-m', required=True, help='如 MyBuilder.BuildPlayer')
    b.add_argument('--assembly', '-a', default='Assembly-CSharp.dll')
    sub.add_parser('version', help='查看版本号').add_argument('--project', '-p', required=True)
    sub.add_parser('modules', help='查看可用模块').add_argument('--unity', '-u', default=None)
    args = parser.parse_args()
    if args.cmd == 'build':
        build_player(args.project, args.output, args.platform, args.unity, args.type)
    elif args.cmd == 'method':
        build_with_method(args.project, args.output, args.method, args.assembly)
    elif args.cmd == 'version':
        print(f"版本: {get_version(args.project)}")
    elif args.cmd == 'modules':
        unity = args.unity or find_unity_exe()
        if unity:
            mods = get_available_modules(unity)
            for m in mods:
                print(f"  - {m}")
        else:
            print("[ERROR] 未找到 Unity")
