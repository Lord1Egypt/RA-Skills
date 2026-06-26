#!/usr/bin/env python3
"""
日志分析脚本
分析指定服务的日志，识别错误模式并提供建议
"""

import subprocess
import sys
import re
import json
from collections import Counter

# 日志路径配置
LOG_PATHS = {
    "yarn": "/var/log/hadoop-yarn/",
    "hdfs": "/var/log/hadoop-hdfs/",
    "hive": "/var/log/hive/",
    "spark": "/var/log/spark/",
    "impala": "/var/log/impala/",
    "trino": "/var/log/trino/",
    "starrocks": "/opt/starrocks/log/",
    "hbase": "/var/log/hbase/",
    "kafka": "/var/log/kafka/",
    "zookeeper": "/var/log/zookeeper/",
    "ranger": "/var/log/ranger/",
    "openldap": "/var/log/slapd.log",
    "hue": "/var/log/hue/",
    "flink": "/var/log/flink/",
    "tez": "/var/log/hadoop-yarn/",
}

# 常见错误模式
ERROR_PATTERNS = {
    "memory": [
        (r"OutOfMemoryError", "OOM - 内存不足"),
        (r"Java heap space", "Java 堆内存不足"),
        (r"GC overhead limit exceeded", "GC 开销过大"),
        (r"Cannot allocate memory", "无法分配内存"),
    ],
    "connection": [
        (r"Connection refused", "连接被拒绝"),
        (r"Connection timed out", "连接超时"),
        (r"Connection reset", "连接被重置"),
        (r"UnknownHostException", "未知主机"),
        (r"ConnectException", "连接异常"),
    ],
    "permission": [
        (r"Permission denied", "权限被拒绝"),
        (r"AccessControlException", "访问控制异常"),
        (r"Unauthorized", "未授权"),
        (r"Authentication failed", "认证失败"),
    ],
    "disk": [
        (r"No space left on device", "磁盘空间不足"),
        (r"Disk full", "磁盘已满"),
        (r"Too many open files", "打开文件数过多"),
    ],
    "timeout": [
        (r"TimeoutException", "超时异常"),
        (r"Timed out", "已超时"),
        (r"Read timed out", "读取超时"),
        (r"Write timed out", "写入超时"),
    ],
    "datanode": [
        (r"DataNode.*unavailable", "DataNode 不可用"),
        (r"Block report.*timeout", "块报告超时"),
        (r"Missing blocks", "丢失数据块"),
        (r"Corrupt blocks", "损坏的数据块"),
    ],
    "yarn": [
        (r"Container killed by the ApplicationMaster", "容器被 AM 杀死"),
        (r"NodeManager.*unavailable", "NodeManager 不可用"),
        (r"Queue.*full capacity", "队列容量已满"),
        (r"Resource.*exceeded", "资源超限"),
    ],
    "general": [
        (r"FATAL", "致命错误"),
        (r"ERROR", "错误"),
        (r"Exception", "异常"),
        (r"Failed", "失败"),
    ],
}

# 错误修复建议
FIX_SUGGESTIONS = {
    "OOM - 内存不足": [
        "增加 JVM 堆内存：-Xmx 参数调大",
        "检查是否有内存泄漏",
        "减少并发任务数或单个任务的数据量",
        "考虑增加节点内存或扩容"
    ],
    "Java 堆内存不足": [
        "调整 -Xmx 和 -Xms 参数",
        "优化代码减少对象创建",
        "增加 Executor/Container 内存配置"
    ],
    "GC 开销过大": [
        "调整 GC 参数（使用 G1 GC）",
        "增加堆内存",
        "减少短生命周期对象"
    ],
    "连接被拒绝": [
        "检查目标服务是否运行",
        "检查防火墙配置",
        "确认端口是否正确",
        "检查 hosts 解析"
    ],
    "连接超时": [
        "检查网络连通性",
        "增加超时配置参数",
        "检查目标服务负载"
    ],
    "权限被拒绝": [
        "检查文件/目录权限",
        "检查 Kerberos 认证",
        "检查 Ranger/Sentry 策略",
        "确认用户是否有相应权限"
    ],
    "磁盘空间不足": [
        "清理旧日志和临时文件",
        "扩容磁盘",
        "检查是否有异常大文件",
        "配置日志轮转"
    ],
    "打开文件数过多": [
        "增加 ulimit -n 限制",
        "检查文件句柄泄漏",
        "减少并发连接数"
    ],
    "容器被 AM 杀死": [
        "检查是否超时（spark.executor.instances）",
        "增加 executor 内存",
        "检查是否有 OOM",
        "查看 ApplicationMaster 日志"
    ],
    "队列容量已满": [
        "等待其他任务完成",
        "增加队列容量配置",
        "使用其他队列",
        "优化任务资源申请"
    ],
    "DataNode 不可用": [
        "检查 DataNode 进程",
        "检查网络连接",
        "检查磁盘状态",
        "查看 DataNode 日志"
    ],
    "丢失数据块": [
        "运行 fsck 检查文件系统",
        "检查 DataNode 健康状态",
        "从备份恢复数据"
    ],
}

def run_cmd(cmd):
    """执行命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def get_log_files(service_name, lines=1000):
    """获取服务日志文件内容"""
    if service_name not in LOG_PATHS:
        return "", f"Unknown service: {service_name}"
    
    log_path = LOG_PATHS[service_name]
    
    # 查找最新的日志文件
    if log_path.endswith('.log'):
        # 单个文件
        stdout, stderr, code = run_cmd(f"tail -{lines} {log_path} 2>/dev/null")
        return stdout, stderr if code != 0 else ""
    else:
        # 目录，找最新的日志文件
        stdout, stderr, code = run_cmd(f"ls -t {log_path}*.log 2>/dev/null | head -3")
        if not stdout:
            # 尝试 .out 文件
            stdout, stderr, code = run_cmd(f"ls -t {log_path}*.out 2>/dev/null | head -3")
        
        if stdout:
            files = stdout.split('\n')[:3]
            all_logs = []
            for f in files:
                content, _, _ = run_cmd(f"tail -{lines//3} '{f}' 2>/dev/null")
                all_logs.append(content)
            return '\n'.join(all_logs), ""
        
        return "", f"No log files found in {log_path}"

def analyze_errors(log_content):
    """分析日志中的错误"""
    findings = []
    error_counts = Counter()
    
    for category, patterns in ERROR_PATTERNS.items():
        for pattern, description in patterns:
            matches = re.findall(pattern, log_content, re.IGNORECASE)
            if matches:
                count = len(matches)
                error_counts[description] += count
                findings.append({
                    "category": category,
                    "pattern": pattern,
                    "description": description,
                    "count": count,
                    "sample": matches[0] if matches else ""
                })
    
    return findings, error_counts

def get_suggestions(error_descriptions):
    """根据错误获取修复建议"""
    suggestions = {}
    for desc in error_descriptions:
        for key, fixes in FIX_SUGGESTIONS.items():
            if key in desc:
                suggestions[desc] = fixes
                break
    return suggestions

def analyze_log(service_name, lines=1000):
    """分析指定服务的日志"""
    result = {
        "service": service_name,
        "status": "UNKNOWN",
        "log_path": LOG_PATHS.get(service_name, "Unknown"),
        "errors": [],
        "error_summary": {},
        "suggestions": {},
        "recommendations": []
    }
    
    # 获取日志
    log_content, error = get_log_files(service_name, lines)
    if error:
        result["status"] = "LOG_NOT_FOUND"
        result["error"] = error
        return result
    
    if not log_content:
        result["status"] = "NO_LOG_CONTENT"
        return result
    
    result["status"] = "ANALYZED"
    result["lines_analyzed"] = len(log_content.split('\n'))
    
    # 分析错误
    findings, error_counts = analyze_errors(log_content)
    result["errors"] = findings
    result["error_summary"] = dict(error_counts.most_common(10))
    
    # 获取建议
    if error_counts:
        result["suggestions"] = get_suggestions(list(error_counts.keys()))
    
    # 生成推荐操作
    recommendations = []
    if error_counts.get("OOM - 内存不足", 0) > 0:
        recommendations.append("优先处理内存问题 - 检查并调整 JVM 堆内存配置")
    if error_counts.get("连接被拒绝", 0) > 0:
        recommendations.append("检查网络连接和目标服务状态")
    if error_counts.get("权限被拒绝", 0) > 0:
        recommendations.append("检查用户权限和认证配置")
    if error_counts.get("磁盘空间不足", 0) > 0:
        recommendations.append("立即清理磁盘空间或扩容")
    
    result["recommendations"] = recommendations
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_logs.py <service_name> [lines]")
        print("Services:", ", ".join(LOG_PATHS.keys()))
        sys.exit(1)
    
    service_name = sys.argv[1].lower()
    lines = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    
    result = analyze_log(service_name, lines)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
