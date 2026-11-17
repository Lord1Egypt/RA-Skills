#!/usr/bin/env python3
"""
Docker Manager - Docker 容器管理工具
"""
import subprocess
import argparse
import sys

DOCKER_CMD = "docker"

def run_cmd(cmd, capture=True):
    """执行docker命令"""
    if isinstance(cmd, str):
        cmd = cmd.split()
    result = subprocess.run(cmd, capture_output=capture, text=True)
    if result.returncode != 0:
        print(f"❌ 执行失败: {result.stderr.strip()}")
        return None
    return result.stdout.strip() if capture else True

def cmd_ps(args):
    """列出容器"""
    cmd = [DOCKER_CMD, "ps"]
    if args.all:
        cmd.append("-a")
    if args.quiet:
        cmd.append("-q")
    
    format_str = "{{.Names}}\t{{.Status}}\t{{.Image}}\t{{.Ports}}"
    cmd.extend(["--format", format_str])
    
    output = run_cmd(cmd)
    if output:
        print("容器列表:")
        print("-" * 80)
        print(f"{'名称':<25} {'状态':<20} {'镜像':<20} {'端口'}")
        print("-" * 80)
        for line in output.split("\n"):
            if line:
                parts = line.split("\t")
                name = parts[0][:24] if len(parts) > 0 else ""
                status = parts[1][:19] if len(parts) > 1 else ""
                image = parts[2][:19] if len(parts) > 2 else ""
                ports = parts[3] if len(parts) > 3 else ""
                print(f"{name:<25} {status:<20} {image:<20} {ports}")

def cmd_start(args):
    """启动容器"""
    result = run_cmd([DOCKER_CMD, "start", args.name])
    if result is not None:
        print(f"✅ 已启动: {args.name}")

def cmd_stop(args):
    """停止容器"""
    result = run_cmd([DOCKER_CMD, "stop", args.name])
    if result is not None:
        print(f"✅ 已停止: {args.name}")

def cmd_restart(args):
    """重启容器"""
    result = run_cmd([DOCKER_CMD, "restart", args.name])
    if result is not None:
        print(f"✅ 已重启: {args.name}")

def cmd_stats(args):
    """资源监控"""
    cmd = [DOCKER_CMD, "stats", "--no-stream", "--format", 
           "{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"]
    
    if args.name:
        cmd[2] = args.name
    
    output = run_cmd(cmd)
    if output:
        print("资源使用:")
        print("-" * 80)
        print(f"{'容器名':<20} {'CPU':<10} {'内存':<20} {'网络':<15} {'磁盘'}")
        print("-" * 80)
        for line in output.split("\n"):
            if line:
                parts = line.split("\t")
                name = parts[0][:19] if len(parts) > 0 else ""
                cpu = parts[1] if len(parts) > 1 else ""
                mem = parts[2] if len(parts) > 2 else ""
                net = parts[3] if len(parts) > 3 else ""
                io = parts[4] if len(parts) > 4 else ""
                print(f"{name:<20} {cpu:<10} {mem:<20} {net:<15} {io}")

def cmd_logs(args):
    """查看日志"""
    cmd = [DOCKER_CMD, "logs"]
    
    if args.follow:
        cmd.append("-f")
    if args.tail:
        cmd.extend(["--tail", str(args.tail)])
    if args.timestamps:
        cmd.append("-t")
    
    cmd.append(args.name)
    
    # 实时日志需要 streaming
    if args.follow:
        print(f"📝 实时日志 (Ctrl+C 退出):")
        print("-" * 60)
        subprocess.run(cmd)
    else:
        output = run_cmd(cmd)
        if output:
            print(output)

def cmd_inspect(args):
    """查看容器详情"""
    cmd = [DOCKER_CMD, "inspect", args.name]
    output = run_cmd(cmd)
    if output:
        # 简单解析输出
        import json
        try:
            data = json.loads(output)
            if data:
                c = data[0]
                print(f"容器详情: {args.name}")
                print("-" * 60)
                print(f"ID: {c['Id'][:12]}")
                print(f"镜像: {c['Config']['Image']}")
                print(f"状态: {c['State']['Status']}")
                print(f"创建时间: {c['Created']}")
                print(f"端口: {c['NetworkSettings'].get('Ports', {})}")
        except:
            print(output)

def cmd_images(args):
    """列出镜像"""
    cmd = [DOCKER_CMD, "images", "--format", "{{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"]
    
    output = run_cmd(cmd)
    if output:
        print("镜像列表:")
        print("-" * 80)
        print(f"{'仓库':<30} {'标签':<15} {'大小':<10} {'创建时间'}")
        print("-" * 80)
        for line in output.split("\n"):
            if line:
                parts = line.split("\t")
                repo = parts[0][:29] if len(parts) > 0 else ""
                tag = parts[1][:14] if len(parts) > 1 else ""
                size = parts[2] if len(parts) > 2 else ""
                created = parts[3] if len(parts) > 3 else ""
                print(f"{repo:<30} {tag:<15} {size:<10} {created}")

def cmd_rm(args):
    """删除容器"""
    force = "-f" if args.force else ""
    cmd = [DOCKER_CMD, "rm"]
    if force:
        cmd.append(force)
    cmd.append(args.name)
    
    result = run_cmd(cmd)
    if result is not None:
        print(f"✅ 已删除容器: {args.name}")

def cmd_rmi(args):
    """删除镜像"""
    cmd = [DOCKER_CMD, "rmi", args.image]
    result = run_cmd(cmd)
    if result is not None:
        print(f"✅ 已删除镜像: {args.image}")

def cmd_prune(args):
    """清理"""
    if args.containers:
        result = run_cmd([DOCKER_CMD, "container", "prune", "-f"])
        if result:
            print("✅ 已清理停止的容器")
    if args.images:
        result = run_cmd([DOCKER_CMD, "image", "prune", "-a", "-f"])
        if result:
            print("✅ 已清理未使用的镜像")
    if args.volumes:
        result = run_cmd([DOCKER_CMD, "volume", "prune", "-f"])
        if result:
            print("✅ 已清理未使用的卷")
    if args.all:
        result = run_cmd([DOCKER_CMD, "system", "prune", "-a", "-f"])
        if result:
            print("✅ 已清理所有未使用资源")

def cmd_exec(args):
    """在容器中执行命令"""
    cmd = [DOCKER_CMD, "exec", "-it", args.name] + args.cmd.split()
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="Docker Manager - Docker 容器管理工具")
    subparsers = parser.add_subparsers()
    
    # ps - 列出容器
    p_ps = subparsers.add_parser("ps", help="列出容器")
    p_ps.add_argument("--all", "-a", action="store_true", help="显示所有容器")
    p_ps.add_argument("--quiet", "-q", action="store_true", help="只显示ID")
    p_ps.set_defaults(func=cmd_ps)
    
    # start - 启动
    p_start = subparsers.add_parser("start", help="启动容器")
    p_start.add_argument("name", help="容器名称或ID")
    p_start.set_defaults(func=cmd_start)
    
    # stop - 停止
    p_stop = subparsers.add_parser("stop", help="停止容器")
    p_stop.add_argument("name", help="容器名称或ID")
    p_stop.set_defaults(func=cmd_stop)
    
    # restart - 重启
    p_restart = subparsers.add_parser("restart", help="重启容器")
    p_restart.add_argument("name", help="容器名称或ID")
    p_restart.set_defaults(func=cmd_restart)
    
    # stats - 资源监控
    p_stats = subparsers.add_parser("stats", help="查看资源使用")
    p_stats.add_argument("--name", "-n", help="指定容器名称")
    p_stats.set_defaults(func=cmd_stats)
    
    # logs - 日志
    p_logs = subparsers.add_parser("logs", help="查看容器日志")
    p_logs.add_argument("name", help="容器名称或ID")
    p_logs.add_argument("--tail", "-t", type=int, default=50, help="显示行数")
    p_logs.add_argument("--follow", "-f", action="store_true", help="实时跟踪")
    p_logs.add_argument("--timestamps", "-T", action="store_true", help="显示时间戳")
    p_logs.set_defaults(func=cmd_logs)
    
    # inspect - 详情
    p_inspect = subparsers.add_parser("inspect", help="查看容器详情")
    p_inspect.add_argument("name", help="容器名称或ID")
    p_inspect.set_defaults(func=cmd_inspect)
    
    # images - 镜像
    p_images = subparsers.add_parser("images", help="列出镜像")
    p_images.set_defaults(func=cmd_images)
    
    # rm - 删除容器
    p_rm = subparsers.add_parser("rm", help="删除容器")
    p_rm.add_argument("name", help="容器名称或ID")
    p_rm.add_argument("--force", "-f", action="store_true", help="强制删除")
    p_rm.set_defaults(func=cmd_rm)
    
    # rmi - 删除镜像
    p_rmi = subparsers.add_parser("rmi", help="删除镜像")
    p_rmi.add_argument("image", help="镜像名称或ID")
    p_rmi.set_defaults(func=cmd_rmi)
    
    # prune - 清理
    p_prune = subparsers.add_parser("prune", help="清理未使用的资源")
    p_prune.add_argument("--containers", "-c", action="store_true", help="清理容器")
    p_prune.add_argument("--images", "-i", action="store_true", help="清理镜像")
    p_prune.add_argument("--volumes", "-v", action="store_true", help="清理卷")
    p_prune.add_argument("--all", "-a", action="store_true", help="清理所有")
    p_prune.set_defaults(func=cmd_prune)
    
    # exec - 执行命令
    p_exec = subparsers.add_parser("exec", help="在容器中执行命令")
    p_exec.add_argument("name", help="容器名称或ID")
    p_exec.add_argument("cmd", help="要执行的命令")
    p_exec.set_defaults(func=cmd_exec)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
