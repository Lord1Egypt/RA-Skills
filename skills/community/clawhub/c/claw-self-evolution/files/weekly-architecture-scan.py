#!/usr/bin/env python3
"""
每周架构主动优化扫描
自动扫描：代码重复、冗余文件、日志膨胀、依赖过时
发现优化点自动推送报告，你同意就自动执行
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple

THRESHOLD_LARGE_FILE_MB = 50  # 大于50MB就算大文件
THRESHOLD_OLD_FILE_DAYS = 90  # 超过90天没修改就算旧文件

def find_large_files() -> List[Dict]:
    """查找大文件"""
    large_files = []
    print("🔍 扫描大文件...")
    
    for root, dirs, files in os.walk("/app/working"):
        # 跳过.git
        if ".git" in root:
            continue
        # 跳过node_modules
        if "node_modules" in root:
            continue
        
        for f in files:
            filepath = os.path.join(root, f)
            try:
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                if size_mb > THRESHOLD_LARGE_FILE_MB:
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    days_old = (datetime.now() - mtime).days
                    large_files.append({
                        "path": filepath,
                        "size_mb": round(size_mb, 1),
                        "days_old": days_old,
                        "type": "大文件"
                    })
            except:
                continue
    
    large_files.sort(key=lambda x: -x["size_mb"])
    print(f"📊 发现 {len(large_files)} 个大文件")
    return large_files

def find_old_unused_files() -> List[Dict]:
    """查找很久没修改的文件"""
    old_files = []
    print("🔍 扫描旧文件...")
    
    for root, dirs, files in os.walk("/app/working"):
        if ".git" in root or "node_modules" in root:
            continue
        
        for f in files:
            filepath = os.path.join(root, f)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                days_old = (datetime.now() - mtime).days
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                if days_old > THRESHOLD_OLD_FILE_DAYS and size_mb > 1:
                    # 检查是否在备份目录，那些不算
                    if "memory/snapshots" in filepath:
                        continue  # 备份是正常的
                    old_files.append({
                        "path": filepath,
                        "size_mb": round(size_mb, 1),
                        "days_old": days_old,
                        "type": "长期未修改文件"
                    })
            except:
                continue
    
    old_files.sort(key=lambda x: -x["days_old"])
    print(f"📊 发现 {len(old_files)} 个旧文件")
    return old_files

def find_duplicate_files() -> List[Dict]:
    """查找重复文件（简单哈希检测）"""
    # 只检测scripts和skills目录下的py文件
    duplicates = []
    hash_map: Dict[str, List[str]] = {}
    
    print("🔍 扫描重复文件...")
    
    for root, dirs, files in os.walk("/app/working"):
        if ".git" in root or "node_modules" in root or "memory/snapshots" in root:
            continue
        
        for f in files:
            if not f.endswith(".py"):
                continue
            
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'rb') as fobj:
                    content = fobj.read()
                    if len(content) > 100:  # 只算大于100字节的
                        import hashlib
                        file_hash = hashlib.md5(content).hexdigest()
                        if file_hash not in hash_map:
                            hash_map[file_hash] = []
                        hash_map[file_hash].append(filepath)
            except:
                continue
    
    for h, paths in hash_map.items():
        if len(paths) > 1:
            size = os.path.getsize(paths[0]) / 1024
            duplicates.append({
                "hash": h,
                "paths": paths,
                "size_kb": round(size, 1),
                "type": "重复文件"
            })
    
    print(f"📊 发现 {len(duplicates)} 组重复文件")
    return duplicates

def check_outdated_dependencies() -> List[Dict]:
    """检查是否有过时的依赖"""
    outdated = []
    print("🔍 检查过时依赖...")
    
    try:
        result = subprocess.run(
            "pip list --outdated --format=json",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            for pkg in data:
                outdated.append({
                    "name": pkg["name"],
                    "current": pkg["version"],
                    "latest": pkg["latest_version"],
                    "type": "过时依赖"
                })
    except Exception as e:
        print(f"⚠️ 检查依赖失败: {e}")
    
    print(f"📊 发现 {len(outdated)} 个过时依赖")
    return outdated

def check_token_usage() -> Dict:
    """检查最近30天token使用"""
    print("🔍 检查Token用量...")
    try:
        from get_token_usage import get_token_usage
        usage = get_token_usage(days=30)
        return {
            "total_tokens": usage.get("total_tokens", 0),
            "days": 30,
            "type": "Token用量统计"
        }
    except:
        return {"total_tokens": 0, "type": "Token用量统计"}

def generate_report(large_files, old_files, duplicates, outdated, token_usage) -> str:
    """生成优化建议报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    total_issues = (
        len([f for f in large_files if f["days_old"] > 30]) +
        len(old_files) +
        len(duplicates) +
        len(outdated)
    )
    
    report = f"# 🚀 每周架构优化扫描报告 - {now}\n\n"
    report += f"**发现潜在优化点: {total_issues} 处**\n\n"
    
    if total_issues == 0:
        report += "🎉 没有发现需要优化的地方，当前架构非常干净！\n"
        return report
    
    # 大文件
    large_issues = [f for f in large_files if f["days_old"] > 30]
    if large_issues:
        report += "## 📁 大文件（大于 {THRESHOLD_LARGE_FILE_MB}MB，超过30天未修改）\n\n"
        report += "| 大小 | 天数 | 文件 |\n"
        report += "|------|------|------|\n"
        for f in large_issues[:10]:
            report += f"| {f['size_mb']} MB | {f['days_old']} 天 | `{f['path']}` |\n"
        if len(large_issues) > 10:
            report += f"| ... | ... | ... 还有 {len(large_issues) - 10} 个 |\n"
        report += "\n"
    
    # 旧文件
    if old_files:
        report += "## ⏳ 长期未修改文件（超过 {THRESHOLD_OLD_FILE_DAYS} 天）\n\n"
        report += "| 大小 | 天数 | 文件 |\n"
        report += "|------|------|------|\n"
        for f in old_files[:10]:
            report += f"| {f['size_mb']} MB | {f['days_old']} 天 | `{f['path']}` |\n"
        if len(old_files) > 10:
            report += f"| ... | ... | ... 还有 {len(old_files) - 10} 个 |\n"
        report += "\n💡 建议：考虑归档到 legacy 或删除\n\n"
    
    # 重复文件
    if duplicates:
        report += "## 🔄 重复代码文件\n\n"
        report += "| 大小 | 文件数量 | 文件列表 |\n"
        report += "|------|----------|----------|\n"
        for d in duplicates[:5]:
            paths_str = ", ".join(f"`{p}`" for p in d["paths"][:2])
            if len(d["paths"]) > 2:
                paths_str += f" 等 {len(d['paths'])} 个"
            report += f"| {d['size_kb']} KB | {len(d['paths'])} | {paths_str} |\n"
        if len(duplicates) > 5:
            report += f"| ... | ... | ... 还有 {len(duplicates) - 5} 组 |\n"
        report += "\n💡 建议：合并重复代码，减少维护负担\n\n"
    
    # 过时依赖
    if outdated:
        report += "## 📦 过时Python依赖\n\n"
        report += "| 包名 | 当前版本 | 最新版本 |\n"
        report += "|------|----------|----------|\n"
        for pkg in outdated:
            report += f"| {pkg['name']} | {pkg['current']} | {pkg['latest']} |\n"
        report += "\n💡 是否需要升级？\n\n"
    
    # Token用量
    if token_usage["total_tokens"] > 0:
        avg = token_usage["total_tokens"] / 30
        report += "## 🎫 Token用量统计（最近30天）\n\n"
        report += f"- **总用量**: {token_usage['total_tokens']:,} tokens\n"
        report += f"- **日均**: {round(avg, 0):,.0f} tokens\n\n"
        if avg > 10000:
            report += "⚠️ 日均用量较高，建议检查节能优化\n\n"
        else:
            report += "✅ 日均用量控制良好\n\n"
    
    report += "---\n"
    report += "*自动扫描，如果同意优化建议，请回复「执行优化」*\n"
    
    return report

def main():
    print("🚀 开始每周架构优化扫描...")
    
    large_files = find_large_files()
    old_files = find_old_unused_files()
    duplicates = find_duplicate_files()
    outdated = check_outdated_dependencies()
    token_usage = check_token_usage()
    
    report = generate_report(large_files, old_files, duplicates, outdated, token_usage)
    
    # 保存报告
    report_dir = "/app/working/logs/architecture-scan/"
    os.makedirs(report_dir, exist_ok=True)
    filename = f"architecture-scan-{datetime.now().strftime('%Y%m%d')}.md"
    report_path = os.path.join(report_dir, filename)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📝 报告已保存: {report_path}")
    
    # 输出报告
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    # 如果有优化点，退出码非零，触发飞书推送
    total_issues = (
        len([f for f in large_files if f["days_old"] > 30]) +
        len(old_files) +
        len(duplicates) +
        len(outdated)
    )
    
    if total_issues > 0:
        print(f"\n⚠️  发现 {total_issues} 处优化点，推送报告请求处理...")
        sys.exit(1)
    else:
        print("\n✅ 没有优化点，一切正常")
        sys.exit(0)

if __name__ == "__main__":
    main()
