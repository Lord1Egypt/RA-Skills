#!/usr/bin/env python3
"""
大数据服务状态检查脚本
检查指定服务的进程状态、端口监听、系统服务状态
"""

import subprocess
import sys
import json

# 服务定义：进程名、端口、服务名
SERVICES = {
    "yarn": {"processes": ["ResourceManager", "NodeManager"], "ports": [8088, 8042], "service": "hadoop-yarn"},
    "hdfs": {"processes": ["NameNode", "DataNode"], "ports": [9870, 9864], "service": "hadoop-hdfs"},
    "hive": {"processes": ["HiveServer2", "Metastore"], "ports": [10000, 9083], "service": "hive"},
    "spark": {"processes": ["Spark", "Worker"], "ports": [8080, 8081], "service": "spark"},
    "impala": {"processes": ["impalad", "catalogd", "statestored"], "ports": [21050, 25010, 25020], "service": "impala"},
    "trino": {"processes": ["trino"], "ports": [8080], "service": "trino"},
    "starrocks": {"processes": ["fe", "be"], "ports": [8030, 9030], "service": "starrocks"},
    "hbase": {"processes": ["HMaster", "RegionServer"], "ports": [16010, 16030], "service": "hbase"},
    "kafka": {"processes": ["kafka.Kafka"], "ports": [9092], "service": "kafka"},
    "zookeeper": {"processes": ["QuorumPeerMain"], "ports": [2181], "service": "zookeeper"},
    "ranger": {"processes": ["ranger-admin", "ranger-usersync"], "ports": [6080, 6180], "service": "ranger"},
    "openldap": {"processes": ["slapd"], "ports": [389, 636], "service": "slapd"},
    "hue": {"processes": ["runserver", "hue"], "ports": [8888], "service": "hue"},
    "flink": {"processes": ["StandaloneClusterEntrypoint", "TaskManager"], "ports": [8081], "service": "flink"},
    "tez": {"processes": ["Tez"], "ports": [], "service": "tez"},  # Tez 运行在 YARN 上
}

def run_cmd(cmd):
    """执行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def check_process(process_name):
    """检查进程是否在运行"""
    stdout, stderr, code = run_cmd(f"ps aux | grep -v grep | grep '{process_name}'")
    return code == 0 and len(stdout) > 0, stdout

def check_port(port):
    """检查端口是否在监听"""
    stdout, stderr, code = run_cmd(f"ss -tlnp 2>/dev/null | grep ':{port} ' || netstat -tlnp 2>/dev/null | grep ':{port} '")
    return code == 0 and len(stdout) > 0, stdout

def check_systemd_service(service_name):
    """检查 systemd 服务状态"""
    stdout, stderr, code = run_cmd(f"systemctl is-active {service_name} 2>/dev/null")
    return stdout == "active", stdout

def get_service_version(service_name):
    """获取服务版本"""
    version_cmds = {
        "yarn": "yarn version 2>&1 | head -3",
        "hdfs": "hdfs version 2>&1 | head -3",
        "hive": "hive --version 2>&1 | head -3",
        "spark": "spark-submit --version 2>&1 | head -5",
        "impala": "impala-shell --version 2>&1 | head -3",
        "hbase": "hbase version 2>&1 | head -3",
        "kafka": "kafka-topics.sh --version 2>&1 | head -3",
        "zookeeper": "zookeeper-server-status.sh 2>&1 | head -3 || echo 'version command not available'",
        "flink": "flink --version 2>&1 | head -3",
        "starrocks": "mysql -h 127.0.0.1 -P 8030 -u root -e 'SHOW FRONTENDS;' 2>&1 | head -5 || echo 'MySQL connection failed'",
        "trino": "trino --version 2>&1 | head -3 || echo 'version command not available'",
    }
    
    cmd = version_cmds.get(service_name, f"{service_name} --version 2>&1 | head -3")
    stdout, stderr, code = run_cmd(cmd)
    return stdout if stdout else "Unknown"

def check_service(service_name):
    """检查单个服务的完整状态"""
    if service_name not in SERVICES:
        return {"error": f"Unknown service: {service_name}"}
    
    svc = SERVICES[service_name]
    result = {
        "name": service_name,
        "status": "UNKNOWN",
        "processes": [],
        "ports": [],
        "systemd": "UNKNOWN",
        "version": "Unknown"
    }
    
    # 检查进程
    for proc in svc["processes"]:
        running, output = check_process(proc)
        result["processes"].append({
            "name": proc,
            "running": running,
            "details": output[:200] if running else ""
        })
    
    # 检查端口
    for port in svc["ports"]:
        listening, output = check_port(port)
        result["ports"].append({
            "port": port,
            "listening": listening,
            "details": output[:200] if listening else ""
        })
    
    # 检查 systemd 服务
    if svc["service"]:
        active, output = check_systemd_service(svc["service"])
        result["systemd"] = "active" if active else output if output else "inactive"
    
    # 获取版本
    result["version"] = get_service_version(service_name)
    
    # 综合判断状态
    process_ok = any(p["running"] for p in result["processes"])
    port_ok = any(p["listening"] for p in result["ports"]) if result["ports"] else process_ok
    systemd_ok = result["systemd"] == "active"
    
    if process_ok or port_ok or systemd_ok:
        result["status"] = "RUNNING"
    else:
        result["status"] = "NOT_RUNNING"
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: check_service_status.py <service_name|all>")
        print("Services:", ", ".join(SERVICES.keys()))
        sys.exit(1)
    
    service_name = sys.argv[1].lower()
    
    if service_name == "all":
        # 检查所有服务
        results = []
        for svc in SERVICES.keys():
            result = check_service(svc)
            results.append(result)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        # 检查指定服务
        result = check_service(service_name)
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
