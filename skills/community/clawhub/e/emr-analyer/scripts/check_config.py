#!/usr/bin/env python3
"""
配置参数检查和调优建议脚本
"""

import subprocess
import sys
import json
import os

# 配置文件路径（优先 taihao-apps，回退 ecm）
CONFIG_PATHS_PRIMARY = {
    "yarn": "/etc/taihao-apps/hadoop-conf/yarn-site.xml",
    "hdfs": "/etc/taihao-apps/hadoop-conf/hdfs-site.xml",
    "hive": "/etc/taihao-apps/hive-conf/hive-site.xml",
    "spark": "/etc/taihao-apps/spark-conf/spark-env.sh",
    "impala": "/etc/taihao-apps/impala-conf/impala-site.xml",
    "hbase": "/etc/taihao-apps/hbase-conf/hbase-site.xml",
    "kafka": "/etc/taihao-apps/kafka-conf/server.properties",
    "zookeeper": "/etc/taihao-apps/zookeeper-conf/zoo.cfg",
    "flink": "/etc/taihao-apps/flink-conf/flink-conf.yaml",
    "starrocks": "/opt/starrocks/fe/conf/fe.conf",
}

CONFIG_PATHS_FALLBACK = {
    "yarn": "/etc/ecm/hadoop-conf/yarn-site.xml",
    "hdfs": "/etc/ecm/hadoop-conf/hdfs-site.xml",
    "hive": "/etc/ecm/hive-conf/hive-site.xml",
    "spark": "/etc/ecm/spark-conf/spark-env.sh",
    "impala": "/etc/ecm/impala-conf/impala-site.xml",
    "hbase": "/etc/ecm/hbase-conf/hbase-site.xml",
    "kafka": "/etc/ecm/kafka-conf/server.properties",
    "zookeeper": "/etc/ecm/zookeeper-conf/zoo.cfg",
    "flink": "/etc/ecm/flink-conf/flink-conf.yaml",
    "starrocks": "/opt/starrocks/fe/conf/fe.conf",
}

def get_config_path(service):
    """获取配置文件路径（优先 taihao-apps，回退 ecm）"""
    primary = CONFIG_PATHS_PRIMARY.get(service)
    fallback = CONFIG_PATHS_FALLBACK.get(service)
    
    if not primary and not fallback:
        return None
    
    # 优先检查 taihao-apps 路径
    if primary:
        _, _, code = run_cmd(f"ls {primary} 2>/dev/null")
        if code == 0:
            return primary
    
    # 回退到 ecm 路径
    if fallback:
        _, _, code = run_cmd(f"ls {fallback} 2>/dev/null")
        if code == 0:
            return fallback
    
    # 如果都不存在，返回 primary（用于错误提示）
    return primary if primary else fallback

# 关键配置参数
KEY_PARAMS = {
    "yarn": [
        "yarn.nodemanager.resource.memory-mb",
        "yarn.nodemanager.resource.cpu-vcores",
        "yarn.scheduler.maximum-allocation-mb",
        "yarn.scheduler.minimum-allocation-mb",
        "yarn.nodemanager.vmem-check-enabled",
    ],
    "hdfs": [
        "dfs.namenode.handler.count",
        "dfs.datanode.handler.count",
        "dfs.replication",
        "dfs.blocksize",
        "dfs.namenode.rpc-bind-host",
    ],
    "hive": [
        "hive.exec.parallel",
        "hive.auto.convert.join",
        "hive.tez.container.size",
        "hive.exec.max.dynamic.partitions.pernode",
        "hive.server2.thrift.max.worker.threads",
    ],
    "spark": [
        "spark.executor.memory",
        "spark.executor.cores",
        "spark.driver.memory",
        "spark.sql.shuffle.partitions",
        "spark.default.parallelism",
    ],
    "hbase": [
        "hbase.regionserver.global.memstore.size",
        "hfile.block.cache.size",
        "hbase.regionserver.handler.count",
        "hbase.zookeeper.property.clientPort",
    ],
    "kafka": [
        "num.network.threads",
        "num.io.threads",
        "socket.send.buffer.bytes",
        "socket.receive.buffer.bytes",
        "log.retention.hours",
    ],
    "flink": [
        "taskmanager.memory.process.size",
        "taskmanager.numberOfTaskSlots",
        "jobmanager.memory.process.size",
        "parallelism.default",
    ],
}

def run_cmd(cmd):
    """执行命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def get_config_value(service, key):
    """获取配置值"""
    config_file = get_config_path(service)
    if not config_file:
        return None
    
    # XML 文件
    if config_file.endswith('.xml'):
        stdout, _, code = run_cmd(f"grep -A1 '<name>{key}</name>' {config_file} 2>/dev/null | grep '<value>' | sed 's/.*<value>\\(.*\\)<\\/value>.*/\\1/'")
        return stdout if stdout else None
    
    # properties 文件
    elif config_file.endswith('.properties'):
        stdout, _, code = run_cmd(f"grep '^{key}=' {config_file} 2>/dev/null | cut -d'=' -f2-")
        return stdout if stdout else None
    
    # yaml 文件
    elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
        stdout, _, code = run_cmd(f"grep '^{key}:' {config_file} 2>/dev/null | awk '{{print $2}}'")
        return stdout if stdout else None
    
    # shell 脚本
    elif config_file.endswith('.sh'):
        stdout, _, code = run_cmd(f"grep '^{key}=' {config_file} 2>/dev/null | cut -d'=' -f2- | tr -d '\"'")
        return stdout if stdout else None
    
    # conf 文件
    elif config_file.endswith('.conf'):
        stdout, _, code = run_cmd(f"grep '^{key}\\s*=' {config_file} 2>/dev/null | cut -d'=' -f2- | tr -d ' '")
        return stdout if stdout else None
    
    return None

def get_tuning_suggestions(service, configs):
    """根据当前配置提供调优建议"""
    suggestions = []
    
    if service == "yarn":
        mem = configs.get("yarn.nodemanager.resource.memory-mb")
        if mem:
            mem_val = int(mem) if mem.isdigit() else 0
            if mem_val < 8192:
                suggestions.append({
                    "param": "yarn.nodemanager.resource.memory-mb",
                    "current": mem,
                    "suggestion": "建议增加到 16384 或更高（根据物理内存）",
                    "reason": "当前值偏低，可能限制容器可用内存"
                })
    
    elif service == "spark":
        executor_mem = configs.get("spark.executor.memory")
        if executor_mem:
            suggestions.append({
                "param": "spark.executor.memory",
                "current": executor_mem,
                "suggestion": "根据数据量调整，一般 4g-8g 起步",
                "reason": "Executor 内存影响任务处理能力"
            })
        
        shuffle = configs.get("spark.sql.shuffle.partitions")
        if shuffle:
            suggestions.append({
                "param": "spark.sql.shuffle.partitions",
                "current": shuffle,
                "suggestion": "大数据量场景建议设置为 200-1000",
                "reason": "影响 Shuffle 阶段的并行度"
            })
    
    elif service == "hive":
        parallel = configs.get("hive.exec.parallel")
        if parallel and parallel.lower() == "false":
            suggestions.append({
                "param": "hive.exec.parallel",
                "current": parallel,
                "suggestion": "设置为 true 开启并行执行",
                "reason": "并行执行可显著提升查询性能"
            })
    
    elif service == "hbase":
        memstore = configs.get("hbase.regionserver.global.memstore.size")
        if memstore:
            suggestions.append({
                "param": "hbase.regionserver.global.memstore.size",
                "current": memstore,
                "suggestion": "一般设置为 0.4-0.5",
                "reason": "影响写入性能和 Flush 频率"
            })
    
    elif service == "kafka":
        log_retention = configs.get("log.retention.hours")
        if log_retention:
            suggestions.append({
                "param": "log.retention.hours",
                "current": log_retention,
                "suggestion": "根据存储容量调整，一般 168-720 小时",
                "reason": "影响日志保留时间和磁盘使用"
            })
    
    return suggestions

def check_config(service):
    """检查服务配置"""
    config_file = get_config_path(service)
    result = {
        "service": service,
        "config_file": config_file if config_file else "Unknown",
        "config_exists": False,
        "params": {},
        "suggestions": []
    }
    
    if not config_file:
        result["error"] = f"Unknown service: {service}"
        return result
    
    # 检查配置文件是否存在
    _, _, code = run_cmd(f"ls -la {config_file} 2>/dev/null")
    if code != 0:
        result["error"] = f"Config file not found: {config_file}"
        return result
    
    result["config_exists"] = True
    
    # 获取关键参数值
    if service in KEY_PARAMS:
        for param in KEY_PARAMS[service]:
            value = get_config_value(service, param)
            if value:
                result["params"][param] = value
    
    # 生成调优建议
    result["suggestions"] = get_tuning_suggestions(service, result["params"])
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: check_config.py <service_name|all>")
        print("Services:", ", ".join(CONFIG_PATHS.keys()))
        sys.exit(1)
    
    service_name = sys.argv[1].lower()
    
    if service_name == "all":
        results = []
        for svc in CONFIG_PATHS.keys():
            result = check_config(svc)
            results.append(result)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        result = check_config(service_name)
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
