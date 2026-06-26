# 🔍 龙虾卫士安全扫描主程序

import sys
import os

def print_help():
    """打印帮助信息"""
    print("""
🦞 龙虾卫士 - 安全扫描工具 V1.6

用法: python scan.py <命令> [参数]

命令:
  files <文件夹>     文件安全扫描
  os                 操作系统安全检查
  network            网络安全扫描
  all <文件夹>       全面扫描（文件 + 系统 + 网络）
  help               显示帮助信息

示例:
  python scan.py files C:\\work
  python scan.py os
  python scan.py network
  python scan.py all C:\\work
""")

def scan_files_wrapper(folder_path: str):
    """文件安全扫描"""
    import importlib
    import scan_files
    importlib.reload(scan_files)
    results = scan_files.scan_files(folder_path)
    if "error" in results:
        print(f"❌ 错误：{results['error']}")
        return
    scan_files.print_scan_report(results)

def scan_os_wrapper():
    """操作系统扫描"""
    from scan_os import scan_os, print_os_scan_report
    results = scan_os()
    print_os_scan_report(results)

def scan_network_wrapper():
    """网络安全扫描"""
    from scan_network import scan_network, print_network_scan_report
    results = scan_network()
    print_network_scan_report(results)

def scan_all_wrapper(folder_path: str):
    """全面扫描"""
    print("\n🦞 龙虾卫士 - 全面安全扫描")
    print("=" * 60)
    print("扫描模式：文件 + 系统 + 网络")
    print("=" * 60)
    
    # 1. 文件扫描
    scan_files_wrapper(folder_path)
    
    # 2. 系统扫描
    scan_os_wrapper()
    
    # 3. 网络扫描
    scan_network_wrapper()
    
    print("\n✅ 全面扫描完成！")

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
    
    elif command == "files":
        if len(sys.argv) < 3:
            folder = "."
        else:
            folder = sys.argv[2]
        scan_files_wrapper(folder)
    
    elif command == "os":
        scan_os_wrapper()
    
    elif command == "network":
        scan_network_wrapper()
    
    elif command == "all":
        if len(sys.argv) < 3:
            folder = "."
        else:
            folder = sys.argv[2]
        scan_all_wrapper(folder)
    
    else:
        print(f"❌ 未知命令：{command}")
        print_help()

if __name__ == "__main__":
    main()
