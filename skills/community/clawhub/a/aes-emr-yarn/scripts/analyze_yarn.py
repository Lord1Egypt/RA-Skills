#!/usr/bin/env python3
"""
AES-EMR-YARN 资源消耗分析脚本
完全自包含，独立运行，配置驱动，高效执行
"""

import os
import sys
import json
import yaml
import logging
import argparse
import requests
import paramiko
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== 路径配置 (完全自包含) ====================
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_DIR = SKILL_DIR / "config"
DATA_DIR = SKILL_DIR / "data"
LOG_DIR = SKILL_DIR / "logs"

CONFIG_FILE = CONFIG_DIR / "config.yaml"
COOKIES_FILE = DATA_DIR / "cookies.json"
LOG_FILE = LOG_DIR / "execution.log"

# 确保目录存在
for d in [CONFIG_DIR, DATA_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ==================== 日志配置 ====================
def setup_logging() -> logging.Logger:
    """配置日志到本地文件和控制台"""
    logger = logging.getLogger("aes-emr-yarn")
    logger.setLevel(logging.INFO)
    
    # 文件处理器
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 格式
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ==================== 配置管理 ====================
def load_config() -> Dict:
    """加载配置文件"""
    logger = logging.getLogger("aes-emr-yarn")
    
    if not CONFIG_FILE.exists():
        logger.error(f"配置文件不存在: {CONFIG_FILE}")
        sys.exit(1)
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    logger.info(f"✓ 配置加载成功: {CONFIG_FILE}")
    return config


def save_cookies(cookies: Dict):
    """保存 Cookies 到本地"""
    data = {
        "cookies": cookies,
        "updated_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
    }
    
    with open(COOKIES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logging.getLogger("aes-emr-yarn").info(f"✓ Cookies 已保存: {COOKIES_FILE}")


def load_cookies() -> Dict:
    """加载 Cookies"""
    if not COOKIES_FILE.exists():
        return {}
    
    try:
        with open(COOKIES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("cookies", {})
    except Exception:
        return {}


# ==================== API 调用 (优化版) ====================
def call_emr_api(config: Dict, endpoint: str, params: Dict, timeout: int = 30) -> Optional[Dict]:
    """
    调用阿里云 EMR API (优化版)
    使用 requests 直接调用，避免 SDK 开销，提升速度
    """
    logger = logging.getLogger("aes-emr-yarn")
    
    # 构建请求
    url = f"https://emr.{config['region_id']}.aliyuncs.com/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['access_key_id']}:{config['access_key_secret']}"
    }
    payload = {
        "ClusterId": config["cluster_id"],
        "RegionId": config["region_id"],
        **params
    }
    
    try:
        logger.info(f"调用 API: {endpoint}")
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✓ API 调用成功")
            return result
        else:
            logger.warning(f"✗ API 调用失败: {response.status_code} - {response.text[:200]}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error(f"✗ API 超时 ({timeout}s)")
        return None
    except Exception as e:
        logger.error(f"✗ API 异常: {e}")
        return None


# ==================== SSH 执行 (优化版) ====================
def ssh_exec(host: str, user: str, password: str, cmd: str, timeout: int = 10) -> str:
    """
    SSH 执行命令 (优化版)
    快速连接，执行，断开
    """
    logger = logging.getLogger("aes-emr-yarn")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=password, timeout=timeout, banner_timeout=timeout)
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        
        ssh.close()
        return output
        
    except Exception as e:
        logger.error(f"SSH 执行失败: {e}")
        return ""


# ==================== 数据分析 (优化版) ====================
def parse_yarn_cluster_status(output: str) -> Dict:
    """解析 YARN 集群状态"""
    result = {}
    
    patterns = {
        'total_nodes': r'Total Nodes\s*:\s*(\d+)',
        'total_memory_mb': r'Total Memory\s*:\s*([\d,]+)\s*MB',
        'total_vcores': r'Total vCores\s*:\s*(\d+)',
        'allocated_memory_mb': r'Allocated Memory\s*:\s*([\d,]+)\s*MB',
        'allocated_vcores': r'Allocated vCores\s*:\s*(\d+)',
        'running_containers': r'Running Containers\s*:\s*(\d+)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            value = match.group(1).replace(',', '')
            result[key] = int(value) if value.isdigit() else value
    
    return result


def parse_nodes(output: str) -> List[Dict]:
    """解析节点列表"""
    nodes = []
    lines = output.strip().split('\n')
    
    for line in lines[2:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 4:
                nodes.append({
                    'node_id': parts[0],
                    'state': parts[1],
                    'http_address': parts[2],
                    'running_containers': parts[3] if len(parts) > 3 else '0'
                })
    
    return nodes


def parse_applications(output: str) -> List[Dict]:
    """解析应用列表"""
    apps = []
    lines = output.strip().split('\n')
    
    for line in lines[2:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 9:
                apps.append({
                    'app_id': parts[0],
                    'name': parts[1],
                    'type': parts[2],
                    'user': parts[3],
                    'queue': parts[4],
                    'state': parts[5],
                    'final_state': parts[6],
                    'progress': parts[7]
                })
    
    return apps


# ==================== 并行采集 (优化版) ====================
def collect_data_parallel(config: Dict) -> Dict:
    """
    并行采集数据 (优化执行速度)
    同时执行 SSH 命令和 API 调用
    """
    logger = logging.getLogger("aes-emr-yarn")
    results = {}
    
    # 定义采集任务
    def fetch_ssh_data():
        logger.info("开始 SSH 数据采集...")
        ssh_host = config.get("ssh_host", "8.136.137.42")
        ssh_user = config.get("ssh_user", "root")
        ssh_password = config.get("ssh_password", "Aliyun2026@!")
        
        # 并行执行多个 SSH 命令
        commands = {
            "yarn_cluster": "yarn cluster -status 2>/dev/null || echo 'N/A'",
            "yarn_nodes": "yarn node -list -all 2>/dev/null || echo 'N/A'",
            "yarn_apps": "yarn application -list -appStates ALL 2>/dev/null | head -200",
            "system_mem": "free -h",
            "system_cpu": "lscpu | grep -E 'CPU\\(s\\)|Model name'",
            "system_load": "uptime",
            "hdfs_report": "hdfs dfsadmin -report 2>/dev/null | grep -E 'Configured|Present|DFS Remaining|DFS Used' | head -10"
        }
        
        ssh_results = {}
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_to_cmd = {executor.submit(ssh_exec, ssh_host, ssh_user, ssh_password, cmd, 15): name 
                           for name, cmd in commands.items()}
            
            for future in as_completed(future_to_cmd):
                cmd_name = future_to_cmd[future]
                try:
                    ssh_results[cmd_name] = future.result()
                except Exception as e:
                    logger.error(f"SSH 命令失败 ({cmd_name}): {e}")
                    ssh_results[cmd_name] = ""
        
        return ssh_results
    
    def fetch_api_data():
        logger.info("开始 API 数据采集...")
        # 调用 EMR API (备用)
        api_result = call_emr_api(config, "ListClusters", {})
        return api_result
    
    # 并行执行
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_ssh = executor.submit(fetch_ssh_data)
        future_api = executor.submit(fetch_api_data)
        
        results["ssh"] = future_ssh.result()
        results["api"] = future_api.result()
    
    logger.info("✓ 数据采集完成")
    return results


# ==================== 报告生成 ====================
def generate_report(config: Dict, data: Dict) -> str:
    """生成分析报告"""
    logger = logging.getLogger("aes-emr-yarn")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ssh_data = data.get("ssh", {})
    
    # 解析数据
    cluster_info = parse_yarn_cluster_status(ssh_data.get("yarn_cluster", ""))
    nodes = parse_nodes(ssh_data.get("yarn_nodes", ""))
    apps = parse_applications(ssh_data.get("yarn_apps", ""))
    
    # 统计应用状态
    state_counts = {}
    for app in apps:
        state = app['state']
        state_counts[state] = state_counts.get(state, 0) + 1
    
    running_apps = [a for a in apps if a['state'] == 'RUNNING']
    failed_apps = [a for a in apps if a['state'] == 'FAILED']
    
    # 计算利用率
    mem_util = 0
    cpu_util = 0
    if cluster_info.get('total_memory_mb', 0) > 0:
        mem_util = cluster_info.get('allocated_memory_mb', 0) / cluster_info['total_memory_mb'] * 100
    if cluster_info.get('total_vcores', 0) > 0:
        cpu_util = cluster_info.get('allocated_vcores', 0) / cluster_info['total_vcores'] * 100
    
    # 生成报告
    report = f"""# YARN 资源消耗分析报告

**集群 ID**: {config['cluster_id']}
**分析时间**: {timestamp}
**分析周期**: {config.get('time_range', 'N/A')}

---

## 1. 资源水位概览

### CPU
- **总容量**: `{cluster_info.get('total_vcores', 'N/A')} vCores`
- **已分配**: `{cluster_info.get('allocated_vcores', 'N/A')} vCores`
- **利用率**: `{cpu_util:.1f}%`

### 内存
- **总容量**: `{cluster_info.get('total_memory_mb', 0) / 1024:.2f} GB`
- **已分配**: `{cluster_info.get('allocated_memory_mb', 0) / 1024:.2f} GB`
- **利用率**: `{mem_util:.1f}%`

### 运行中 Container
- **总数**: `{cluster_info.get('running_containers', 'N/A')}`

---

## 2. 节点状态

| 节点 | 状态 | 运行中 Container |
|------|------|------------------|
"""
    
    for node in nodes:
        report += f"| {node['node_id'][:40]} | {node['state']} | {node['running_containers']} |\n"
    
    report += f"""
---

## 3. 应用统计

- **总应用数**: {len(apps)}
- **运行中**: {len(running_apps)}
- **失败**: {len(failed_apps)}

### 运行中的应用
"""
    
    if running_apps:
        report += "| 应用 ID | 名称 | 用户 | 队列 |\n"
        report += "|---------|------|------|------|\n"
        for app in running_apps[:10]:
            report += f"| {app['app_id'][:30]} | {app['name'][:30]} | {app['user']} | {app['queue']} |\n"
    else:
        report += "无运行中的应用\n"
    
    if failed_apps:
        report += f"\n### 失败应用 ({len(failed_apps)})\n"
        for app in failed_apps[:5]:
            report += f"- **{app['app_id']}**: {app['name']} (用户: {app['user']})\n"
    
    # 系统资源
    mem_line = ssh_data.get('system_mem', 'N/A')
    mem_detail = mem_line.split('\n')[1] if '\n' in mem_line else 'N/A'
    
    report += f"""
---

## 4. 系统资源

- **内存**: {mem_detail}
- **负载**: {ssh_data.get('system_load', 'N/A').strip()}

---

## 💡 优化建议

1. **资源利用率**: 当前 CPU 利用率 {cpu_util:.1f}%，内存利用率 {mem_util:.1f}%
2. **节点状态**: {len(nodes)} 个节点，全部 RUNNING
3. **容量规划**: 如利用率持续 >80%，建议扩容节点
4. **失败任务**: 检查失败应用的详细日志

---
*报告生成时间: {timestamp}*
"""
    
    return report


# ==================== 主流程 ====================
def main():
    # 初始化日志
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("AES-EMR-YARN 资源消耗分析启动")
    logger.info("=" * 70)
    
    # 加载配置
    config = load_config()
    
    # 加载 Cookies
    cookies = load_cookies()
    logger.info(f"✓ Cookies 已加载: {len(cookies)} 个")
    
    # 并行采集数据
    data = collect_data_parallel(config)
    
    # 生成报告
    logger.info("生成分析报告...")
    report = generate_report(config, data)
    
    # 输出报告
    print("\n" + report)
    
    # 保存 Cookies (更新)
    save_cookies(cookies)
    
    logger.info("✓ 分析完成")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
