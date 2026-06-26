#!/usr/bin/env python3
"""
dingtalk-ai-table-insights - 钉钉 AI 表格跨表格洞察分析脚本

功能：
1. 按关键词筛选 AI 表格
2. 读取表格数据和字段信息（只读，抽样）
3. 调用大模型进行综合分析
4. 输出洞察报告（风险点、异常、建议）

安全说明：
- 只读操作：不修改任何表格数据
- 数据抽样：每表最多 50 条记录
- 本地分析：数据不上传外部服务
- 权限最小化：仅需表格读取权限

依赖：
- 使用 dingtalk-ai-table skill 获取表格数据

使用示例：
    python analyze_tables.py --keyword "销售"
    python analyze_tables.py --keyword "项目" --output insights.md
    python analyze_tables.py  # 全量扫描
"""

import argparse
import json
import subprocess
import sys
import os
import shlex
from pathlib import Path


def get_skill_version() -> str:
    """
    从 SKILL.md 自动读取版本号
    
    Returns:
        版本号字符串，如 "1.6.8"，读取失败时返回 "unknown"
    """
    # SKILL.md 路径（脚本所在目录的父目录）
    script_dir = Path(__file__).parent.parent
    skill_md = script_dir / "SKILL.md"
    
    if not skill_md.exists():
        return "unknown"
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 匹配 version: xxx 行
        import re
        match = re.search(r'^version:\s*(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    
    return "unknown"


# 自动获取版本号
SKILL_VERSION = get_skill_version()
import tempfile
import time

# MCP 配置文件路径
def get_mcp_config_path():
    """获取 MCP 配置文件路径"""
    # 优先使用环境变量
    env_path = os.environ.get('DINGTALK_MCP_CONFIG')
    if env_path and os.path.exists(env_path):
        return env_path
    
    # 尝试工作区配置（优先）
    workspace_mcp = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "config", "mcporter.json"
    )
    if os.path.exists(workspace_mcp):
        return workspace_mcp
    
    # 默认路径
    default_mcp = os.path.expanduser("~/.openclaw/config/mcporter.json")
    if os.path.exists(default_mcp):
        return default_mcp
    
    return None

MCP_CONFIG_PATH = get_mcp_config_path()
import time
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path


# ============ 配置常量 ============
CACHE_DIR = Path.home() / ".cache" / "dingtalk-ai-table-insights"
CACHE_EXPIRY_SECONDS = 300  # 5 分钟缓存
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
DEFAULT_LIMIT = 100  # 每个数据表最多随机抽样 100 条

# MCP 配置文件路径（可通过环境变量覆盖）
DEFAULT_MCP_CONFIG = os.getenv(
    "DINGTALK_MCP_CONFIG",
    "/home/admin/openclaw/workspace/config/mcporter.json"
)


def ensure_cache_dir():
    """确保缓存目录存在"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_cache_key(keyword: str) -> str:
    """生成缓存键"""
    return f"tables_{hashlib.md5(keyword.encode()).hexdigest()}.json"


def load_from_cache(keyword: str) -> Optional[List[Dict]]:
    """
    从缓存加载表格列表
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        表格列表，如果缓存过期或不存在则返回 None
    """
    cache_file = CACHE_DIR / get_cache_key(keyword)
    
    if not cache_file.exists():
        return None
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # 检查缓存是否过期
        cached_time = cache_data.get("timestamp", 0)
        if time.time() - cached_time > CACHE_EXPIRY_SECONDS:
            return None
        
        return cache_data.get("tables", [])
    except Exception:
        return None


def save_to_cache(keyword: str, tables: List[Dict]):
    """
    保存表格列表到缓存
    
    Args:
        keyword: 搜索关键词
        tables: 表格列表
    """
    ensure_cache_dir()
    cache_file = CACHE_DIR / get_cache_key(keyword)
    
    cache_data = {
        "timestamp": time.time(),
        "keyword": keyword,
        "tables": tables
    }
    
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️  写入缓存失败：{e}")


def clear_cache():
    """清除所有缓存"""
    if CACHE_DIR.exists():
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()
        print("✅ 缓存已清除")


def run_dingtalk_command(tool_name: str, args: Dict[str, Any] = None) -> Optional[Dict]:
    """
    调用 dingtalk-ai-table MCP 工具
    
    Args:
        tool_name: 工具名称
        args: 工具参数
    
    Returns:
        工具返回结果
    
    重试机制：
        - 最多重试 MAX_RETRIES 次
        - 每次重试间隔 RETRY_DELAY_SECONDS 秒
        - 仅对网络错误重试，对业务错误直接返回
    
    注意：使用临时文件接收输出，避免大数据量时被截断
    """
    config_path = DEFAULT_MCP_CONFIG
    
    # 构建参数
    args_str = ""
    if args:
        for key, value in args.items():
            if isinstance(value, str):
                args_str += f' {key}="{value}"'
            else:
                args_str += f' {key}={json.dumps(value)}'
    
    cmd = f"mcporter --config {config_path} call dingtalk-ai-table.{tool_name}{args_str}"
    
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # 使用临时文件接收输出，避免大数据量时被截断
            tmp_file = tempfile.mktemp(suffix='.json')
            
            try:
                # 执行命令，输出重定向到临时文件
                cmd_redirect = f'{cmd} > "{tmp_file}" 2>&1'
                result = subprocess.run(cmd_redirect, shell=True, timeout=30)
                
                # 读取文件内容
                with open(tmp_file, 'r', encoding='utf-8') as f:
                    output = f.read().strip()
                
                # 检查命令是否成功
                if result.returncode == 0:
                    # 尝试解析 JSON
                    if not output:
                        last_error = "返回内容为空"
                        continue
                    
                    json_start = -1
                    for i, char in enumerate(output):
                        if char in '[{':
                            json_start = i
                            break
                    
                    if json_start >= 0:
                        json_str = output[json_start:]
                        try:
                            parsed = json.loads(json_str)
                            return parsed
                        except json.JSONDecodeError:
                            # 尝试逐行解析
                            lines = output.split('\n')
                            for line in lines:
                                try:
                                    parsed = json.loads(line.strip())
                                    return parsed
                                except json.JSONDecodeError:
                                    continue
                            
                            # 尝试找到最后一个完整的 JSON 对象
                            json_end = output.rfind(']') + 1
                            if json_end > json_start:
                                json_str = output[json_start:json_end]
                                try:
                                    return json.loads(json_str)
                                except json.JSONDecodeError:
                                    pass
                    
                    return {"raw": output}
                else:
                    # 命令失败，读取错误信息
                    error_msg = output if output else "命令执行失败"
                    last_error = error_msg
                    
                    # 判断是否可重试的错误
                    if "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                        if attempt < MAX_RETRIES:
                            print(f"⚠️  调用失败，{RETRY_DELAY_SECONDS}秒后重试 ({attempt}/{MAX_RETRIES})...")
                            time.sleep(RETRY_DELAY_SECONDS)
                            continue
                    else:
                        # 业务错误，直接返回
                        return {"error": error_msg, "code": result.returncode}
            
            finally:
                # 清理临时文件
                if os.path.exists(tmp_file):
                    os.unlink(tmp_file)
                    
        except subprocess.TimeoutExpired:
            last_error = "命令执行超时"
            if attempt < MAX_RETRIES:
                print(f"⚠️  超时，{RETRY_DELAY_SECONDS}秒后重试 ({attempt}/{MAX_RETRIES})...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
        except Exception as e:
            last_error = str(e)
            if attempt < MAX_RETRIES:
                print(f"⚠️  异常：{e}，{RETRY_DELAY_SECONDS}秒后重试 ({attempt}/{MAX_RETRIES})...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
    
    return {"error": last_error or "未知错误", "retries": MAX_RETRIES}


def get_accessible_tables(keyword: str = "", use_cache: bool = True) -> List[Dict]:
    """
    获取用户有权限的 AI 表格列表
    
    Args:
        keyword: 搜索关键词
        use_cache: 是否使用缓存
    
    Returns:
        表格列表（标准化字段：name, id, docUuid）
    """
    # 尝试从缓存加载
    if use_cache:
        cached_tables = load_from_cache(keyword)
        if cached_tables is not None:
            print(f"   📦 从缓存加载 ({len(cached_tables)} 个表格)")
            return cached_tables
    
    # 调用 API 获取
    print("   🌐 从 API 获取...")
    args = {}
    if keyword:
        args["keyword"] = keyword
    
    result = run_dingtalk_command("search_accessible_ai_tables", args)
    
    if result and "error" not in result:
        tables = result if isinstance(result, list) else result.get("tables", [])
        
        # 标准化字段名（保留原始字段名兼容）
        standardized = []
        for t in tables:
            standardized.append({
                "docName": t.get("docName", "未知"),  # 保留原始字段
                "docId": t.get("docId", ""),  # 保留原始字段
                "name": t.get("docName", "未知"),  # 兼容旧代码
                "id": t.get("docId", ""),  # 兼容旧代码
                "docUuid": t.get("docId", ""),  # 兼容旧代码
                "url": t.get("url", "")
            })
        
        # 保存到缓存
        if use_cache:
            save_to_cache(keyword, standardized)
        
        return standardized
    
    error_msg = result.get("error", "未知错误") if result else "无响应"
    print(f"   ⚠️  获取失败：{error_msg}")
    return []


def get_sheet_list(doc_id: str) -> List[Dict]:
    """
    获取表格的所有 Sheet 列表
    
    Args:
        doc_id: 表格文档 ID
    
    Returns:
        Sheet 列表，每个元素包含 name 和 id
    """
    result = run_dingtalk_command("list_base_tables", {
        "dentryUuid": doc_id
    })
    
    if result and "error" not in result:
        # result 是 dict，真正的数据在 result 字段中
        sheets = result.get("result", [])
        if isinstance(sheets, list):
            return sheets
    
    return []


def read_sheet_data_paginated(doc_id: str, sheet_identifier: str, page_limit: int = 50, max_records: int = None) -> List[Dict]:
    """
    分页读取单个 Sheet 的所有数据（解决大数据量 JSON 解析失败问题）
    
    Args:
        doc_id: 表格文档 ID
        sheet_identifier: 数据表 ID 或名称
        page_limit: 每页读取记录数（建议 50）
        max_records: 最大读取记录数（可选，达到后提前停止）
    
    Returns:
        所有记录列表
    """
    import subprocess
    import json
    import tempfile
    
    # 检查配置文件
    if not MCP_CONFIG_PATH:
        print("⚠️  警告：MCP 配置文件未找到，使用默认路径")
        config_path = '/home/admin/openclaw/workspace/config/mcporter.json'
    else:
        config_path = MCP_CONFIG_PATH
    
    all_records = []
    cursor = ""
    max_pages = 100  # 防止无限循环
    page = 0
    
    while page < max_pages:
        page += 1
        
        # 创建临时文件
        tmp_file = tempfile.mktemp(suffix='.json')
        
        try:
            # 构建命令（使用 shell 重定向）
            if cursor:
                cmd = (f'mcporter --config {config_path} call dingtalk-ai-table.search_base_record '
                       f'dentryUuid="{doc_id}" sheetIdOrName="{sheet_identifier}" '
                       f'limit={page_limit} cursor="{cursor}" > "{tmp_file}" 2>&1')
            else:
                cmd = (f'mcporter --config {config_path} call dingtalk-ai-table.search_base_record '
                       f'dentryUuid="{doc_id}" sheetIdOrName="{sheet_identifier}" '
                       f'limit={page_limit} > "{tmp_file}" 2>&1')
            
            # 执行命令
            subprocess.run(cmd, shell=True, timeout=30)
            
            # 读取并解析 JSON
            with open(tmp_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print(f"⚠️  第{page}页返回空内容")
                    break
                data = json.loads(content)
            
            result_data = data.get('result', {})
            records = result_data.get('records', [])
            cursor = result_data.get('cursor', '')
            
            all_records.extend(records)
            
            # 达到最大记录数，停止
            if max_records and len(all_records) >= max_records:
                all_records = all_records[:max_records]
                break
            
            # 没有更多数据或返回空记录，停止
            if not cursor or len(records) == 0:
                break
                
        except Exception as e:
            print(f"⚠️  分页读取第{page}页失败：{e}")
            break
        finally:
            # 清理临时文件
            if os.path.exists(tmp_file):
                os.unlink(tmp_file)
    
    return all_records


def read_all_sheets_data(doc_id: str, limit_per_sheet: int = 100, use_pagination: bool = True) -> List[Dict]:
    """
    读取表格的所有 Sheet 数据（每个 Sheet 最多随机抽样 100 条）
    
    Args:
        doc_id: 表格文档 ID
        limit_per_sheet: 每个 Sheet 的最大记录数（超过则随机抽样，默认 100）
        use_pagination: 是否使用分页读取（推荐 True，解决大数据量问题）
    
    Returns:
        包含所有 Sheet 数据的列表，每个元素包含 sheet_name 和 records
    """
    import random
    
    sheets = get_sheet_list(doc_id)
    
    if not sheets:
        return []
    
    all_data = []
    
    for sheet in sheets:
        sheet_name = sheet.get("name", "未知 Sheet")
        sheet_id = sheet.get("id", "")
        
        # 优先使用 Sheet ID，避免中文名称编码问题
        sheet_identifier = sheet_id if sheet_id else sheet_name
        
        # 使用分页读取（推荐）或传统方式
        # 先读取所有数据，再随机抽样
        if use_pagination:
            records = read_sheet_data_paginated(doc_id, sheet_identifier, page_limit=50, max_records=None)
            
            # 如果超过 limit_per_sheet 条，随机抽样
            if len(records) > limit_per_sheet:
                print(f"         📊 {sheet_name}: {len(records)}条 → 随机抽样{limit_per_sheet}条")
                records = random.sample(records, limit_per_sheet)
        else:
            result = run_dingtalk_command("search_base_record", {
                "dentryUuid": doc_id,
                "sheetIdOrName": sheet_identifier
            })
            
            # 解析 result：可能是 {"raw": "JSON 字符串"} 或直接是 dict
            if result and "error" not in result:
                # 处理 raw 字段（JSON 字符串）
                if isinstance(result, dict) and "raw" in result:
                    import json
                    try:
                        raw_str = result.get("raw", "{}")
                        parsed = json.loads(raw_str)
                        result_data = parsed.get("result", {})
                        records = result_data.get("records", []) if isinstance(result_data, dict) else []
                    except:
                        records = []
                # 直接是 dict
                elif isinstance(result, dict):
                    result_data = result.get("result", result)
                    
                    if isinstance(result_data, dict):
                        records = result_data.get("records", [])
                    elif isinstance(result_data, list):
                        records = result_data
                    else:
                        records = []
                else:
                    records = []
            else:
                records = []
        
        if records:
            # 读取所有数据，不做截断（抽样在分析阶段进行）
            all_data.append({
                "sheet_name": sheet_name,
                "sheet_id": sheet_id,
                "records": records
            })
    
    return all_data


def read_table_data(doc_id: str, sheet_name: str = None, limit: int = DEFAULT_LIMIT, read_all: bool = False) -> Optional[List[Dict]]:
    """
    使用 dingtalk-ai-table 读取表格数据
    
    Args:
        doc_id: 表格文档 ID
        sheet_name: 数据表名称（可选，为 None 时自动获取第一个 Sheet）
        limit: 读取记录数限制
        read_all: 是否读取所有 Sheet（默认 False，只读第一个）
    
    Returns:
        记录列表（read_all=True 时返回包含 sheet_name 的列表）
    """
    if read_all:
        return read_all_sheets_data(doc_id, limit)
    
    # 如果没有指定 Sheet 名称，自动获取第一个 Sheet
    if sheet_name is None:
        sheets = get_sheet_list(doc_id)
        if sheets:
            sheet_name = sheets[0].get("name")
            print(f"         📄 自动使用 Sheet: {sheet_name}")
        else:
            print(f"         ⚠️  未找到任何 Sheet")
            return []
    
    result = run_dingtalk_command("search_base_record", {
        "dentryUuid": doc_id,
        "sheetIdOrName": sheet_name
    })
    
    if result and "error" not in result:
        # 解析 result：可能是 {"raw": "JSON 字符串"} 或直接是 dict
        if isinstance(result, dict) and "raw" in result:
            import json
            try:
                raw_str = result.get("raw", "{}")
                parsed = json.loads(raw_str)
                result_data = parsed.get("result", {})
                records = result_data.get("records", []) if isinstance(result_data, dict) else []
            except:
                records = []
        elif isinstance(result, dict):
            result_data = result.get("result", result)
            
            if isinstance(result_data, dict):
                records = result_data.get("records", [])
            elif isinstance(result_data, list):
                records = result_data
            else:
                records = []
        else:
            records = []
        
        if records is None:
            records = []
        
        return records[:limit] if len(records) > limit else records
    
    # 检查是否是权限错误
    error_msg = result.get("error", "未知错误") if result else "无响应"
    error_code = result.get("errorCode", "") if result else ""
    
    if error_code == "601" or "access token" in error_msg.lower():
        # 权限错误，静默跳过
        return None  # 返回 None 表示权限不足
    else:
        # 其他错误，打印提示
        print(f"         ⚠️  {error_msg}")
        return []


def analyze_with_llm(tables_data: List[Dict], keyword: str = "") -> str:
    """
    使用大模型分析表格数据，生成洞察报告（默认启用）
    
    通过 openclaw agent --agent main 调用大模型
    参考 analyze_with_llm.py 实现，发送详细数据样本
    
    Args:
        tables_data: 表格数据列表
        keyword: 搜索关键词
    
    Returns:
        洞察报告（Markdown 格式）
    """
    import tempfile
    
    print("🤖 使用大模型进行分析...")
    
    # 1. 构建详细的数据摘要（参考 analyze_with_llm.py）
    data_summary = []
    for table in tables_data:
        table_name = table.get("table_name", "未知表格")
        sheets = table.get("sheets", [])
        records = table.get("records", [])
        
        table_info = {
            "表格名称": table_name,
            "数据表数": len(sheets),
            "总记录数": len(records),
            "数据表详情": []
        }
        
        # 添加每个数据表的详情
        for sheet in sheets:
            sheet_info = {
                "数据表名称": sheet.get("sheet_name", "未知"),
                "记录数": len(sheet.get("records", []))
            }
            table_info["数据表详情"].append(sheet_info)
        
        # 添加数据样本（最多 5 条）
        if records:
            table_info["数据示例"] = []
            for record in records[:5]:
                fields = record.get("fields", {})
                sample = {}
                # 提取关键字段
                for key in ["标题", "问题", "任务", "名称", "优先级", "状态", "处理人", "创建时间", "工作类型", "产出效率"]:
                    if key in fields:
                        value = fields[key]
                        if isinstance(value, dict):
                            value = value.get("name", value.get("text", str(value)))
                        sample[key] = value
                table_info["数据示例"].append(sample)
        
        data_summary.append(table_info)
    
    total_records = sum(len(t.get("records", [])) for t in tables_data)
    
    prompt = f"""请分析以下钉钉 AI 表格数据并生成洞察报告：

**关键词**: {keyword or '全量扫描'}
**分析表格数**: {len(tables_data)} 个
**总记录数**: {total_records} 条

**表格数据摘要**:
{json.dumps(data_summary, ensure_ascii=False, indent=2)}

请生成一份包含以下内容的 Markdown 报告：

## 报告结构（必须包含）

### 1. 执行摘要
- 关键指标汇总（使用表格展示）
- 核心发现（3-5 条）

### 2. 详细数据分析
- 每个表格的数据表详情、示例、洞察

### 3. 🔗 跨文档交叉验证分析（重点！必须单独成节）
**这是报告的核心章节，请基于提供的数据进行以下分析：**
- **数据量级对比**: 对比各表格的记录数，评估数据代表性
- **指标一致性检查**: 如果多个表格有相同指标（如任务数、人数），检查是否一致
- **关联发现**: 发现表格间的隐含关系（如任务 - 缺陷关联、人效 - 质量关联）
- **综合洞察**: 基于多表格数据给出全局性结论（不能仅从单一表格得出）

### 4. 风险与异常识别
- 按优先级排序（高/中/低）
- 包含数据质量评估

### 5. 行动建议
- 具体可执行
- 包含优先级、负责人、时间、验收标准

## 输出要求
- 使用 Markdown 表格展示跨表格对比数据
- 适当使用 emoji 增强可读性
- 800-1500 字
- 适合在钉钉中查看

请开始生成报告："""
    
    # 2. 使用临时文件调用大模型（避免 64KB 截断）
    tmp_file = tempfile.mktemp(suffix='.json')
    try:
        print(f"   🔄 调用 OpenClaw 大模型（--agent main）...")
        
        # 使用 --agent main 参数（测试成功）
        cmd = f'openclaw agent --agent main --message {shlex.quote(prompt[:10000])} --json --timeout 120 > "{tmp_file}" 2>&1'
        
        exit_code = subprocess.call(cmd, shell=True, timeout=130)
        
        # 读取输出
        if os.path.exists(tmp_file):
            with open(tmp_file, 'r', encoding='utf-8') as f:
                output = f.read()
            
            if output.strip():
                # 跳过可能的日志输出，找到 JSON 开始位置
                json_start = -1
                for i, char in enumerate(output):
                    if char == '{':
                        json_start = i
                        break
                
                if json_start >= 0:
                    output = output[json_start:]
                
                try:
                    data = json.loads(output)
                    
                    # 尝试多种可能的回复字段
                    reply = ""
                    
                    # 格式 1: {"reply": "..."}
                    if data.get("reply"):
                        reply = data.get("reply")
                    # 格式 2: {"result": {"payloads": [{"text": "..."}]}}
                    elif data.get("result", {}).get("payloads"):
                        payloads = data["result"]["payloads"]
                        if payloads and isinstance(payloads, list) and len(payloads) > 0:
                            reply = payloads[0].get("text", "")
                    # 格式 3: {"message": "..."}
                    elif data.get("message"):
                        reply = data.get("message")
                    
                    if reply:
                        print("   ✅ 大模型分析完成")
                        
                        # ========== 轻量后处理：仅修复版本号 ==========
                        from datetime import datetime
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        # 1. 构建标准头部
                        header = f"""# 📊 {keyword if keyword else 'AI 表格'}洞察分析报告

**生成时间**: {current_time}  
**分析工具**: dingtalk-ai-table-insights v{SKILL_VERSION}  
**筛选关键词**: {keyword if keyword else '全量扫描'}

---

"""
                        # 2. 移除 LLM 可能生成的旧头部
                        lines = reply.split('\n')
                        content_start = len(lines)
                        for i, line in enumerate(lines[:30]):
                            stripped = line.strip()
                            if stripped.startswith('##') and not stripped.startswith('###'):
                                content_start = i
                                break
                        reply = header + '\n'.join(lines[content_start:])
                        
                        # 3. 强制验证版本号
                        if f'v{SKILL_VERSION}' not in reply[:500]:
                            divider_idx = reply.find('---')
                            if divider_idx > 0:
                                reply = reply[:divider_idx+3] + f'\n**分析工具**: dingtalk-ai-table-insights v{SKILL_VERSION}\n' + reply[divider_idx+3:]
                        
                        print(f"   ✅ 版本号：v{SKILL_VERSION}")
                        # ========== 后处理结束 ==========
                        
                        return reply
                    elif 'error' in data:
                        print(f"   ⚠️  API 错误：{data.get('error', '未知错误')}")
                    else:
                        print(f"   ⚠️  无法解析回复格式")
                except json.JSONDecodeError as e:
                    print(f"   ⚠️  JSON 解析失败：{e}")
                    print(f"   Output preview: {output[:300]}")
        
        print(f"   ⚠️  调用失败（exit code: {exit_code}）")
    except subprocess.TimeoutExpired:
        print("   ⚠️  调用超时（>120 秒）")
    except Exception as e:
        print(f"   ⚠️  调用异常：{e}")
    finally:
        # 清理临时文件
        if os.path.exists(tmp_file):
            os.unlink(tmp_file)
    
    # 3. 降级使用本地模板
    print("   📝 使用本地模板生成报告（快速模式）")
    return generate_insight_report(tables_data, keyword)


def generate_insight_report(tables_data: List[Dict], keyword: str = "") -> str:
    """
    生成专业洞察报告（聚焦数据洞察，不展示权限问题）
    
    Args:
        tables_data: 成功读取的表格数据
        keyword: 搜索关键词
    
    Returns:
        洞察报告（Markdown 格式）
    """
    from datetime import datetime
    
    # 统计总数
    total_tables = len(tables_data)
    total_sheets = sum(len(table.get("sheets", [{}])) for table in tables_data)
    total_records = sum(len(table.get("records", [])) for table in tables_data)
    
    # 按记录数排序
    sorted_tables = sorted(tables_data, key=lambda x: len(x.get("records", [])), reverse=True)
    
    report = f"""# 📊 {keyword if keyword else 'AI 表格'}洞察分析报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析工具**: dingtalk-ai-table-insights v{SKILL_VERSION}  
**筛选关键词**: {keyword if keyword else '全量扫描'}

---

## 📋 执行摘要

| 指标 | 数值 |
|------|------|
| **分析表格数** | {total_tables} 个 |
| **数据表总数** | {total_sheets} 个 |
| **总记录数** | **{total_records} 条** |
| **平均每表** | {total_records // total_tables if total_tables > 0 else 0} 条 |

"""
    
    # 数据概览
    report += "### 📊 数据概览\n\n"
    report += "| 表格名称 | 数据表数 | 记录数 | 核心发现 |\n"
    report += "|----------|----------|--------|----------|\n"
    
    for table in sorted_tables:
        table_name = table.get("table_name", "未知表格")
        sheets = table.get("sheets", [])
        records = table.get("records", [])
        sheet_count = len(sheets)
        record_count = len(records)
        
        # 生成核心发现
        insight = ""
        if record_count > 100:
            insight = "📈 数据量大，重点分析"
        elif record_count > 50:
            insight = "📊 数据充足"
        elif record_count > 0:
            insight = "📋 基础数据"
        
        # 简化表格名称（超过 15 字截断）
        short_name = table_name[:15] + "..." if len(table_name) > 15 else table_name
        
        report += f"| {short_name} | {sheet_count}个 | {record_count}条 | {insight} |\n"
    
    report += "\n"
    
    # 详细数据分析
    report += "---\n\n"
    report += "## 🔍 详细数据分析\n\n"
    
    for i, table in enumerate(sorted_tables, 1):
        table_name = table.get("table_name", "未知表格")
        sheets = table.get("sheets", [])
        records = table.get("records", [])
        
        report += f"### {i}. {table_name}\n\n"
        report += f"**数据规模**: {len(sheets)} 个数据表，**{len(records)} 条记录**\n\n"
        
        # 数据表详情
        if sheets:
            report += "**数据表详情**:\n\n"
            report += "| 数据表名称 | 记录数 | 状态 |\n"
            report += "|------------|--------|------|\n"
            
            for sheet in sorted(sheets, key=lambda x: len(x.get("records", [])), reverse=True):
                sheet_name = sheet.get("sheet_name", "未知")
                sheet_records = len(sheet.get("records", []))
                
                status = "✅ 数据充足" if sheet_records > 20 else "📋 基础数据" if sheet_records > 0 else "⚠️ 数据较少"
                
                report += f"| {sheet_name} | {sheet_records}条 | {status} |\n"
            
            report += "\n"
        
        # 数据示例（前 3 条）
        if records:
            report += "**数据示例**:\n\n"
            for j, record in enumerate(records[:3], 1):
                fields = record.get("fields", {})
                # 提取关键字段
                title = fields.get("标题", fields.get("问题", fields.get("任务", fields.get("名称", "无"))))
                if isinstance(title, dict):
                    title = title.get("text", str(title))
                
                priority = fields.get("优先级", "")
                if isinstance(priority, dict):
                    priority = priority.get("name", "")
                
                status = fields.get("状态", fields.get("处理状态", ""))
                if isinstance(status, dict):
                    status = status.get("name", "")
                
                # 构建示例文本
                example = f"{j}. "
                if priority:
                    example += f"[{priority}] "
                example += str(title)
                if status:
                    example += f" - {status}"
                
                report += f"{example}\n"
            
            if len(records) > 3:
                report += f"\n... 还有 {len(records) - 3} 条记录\n"
            
            report += "\n"
        
        # 数据洞察
        report += "**数据洞察**:\n\n"
        
        # 分析记录分布
        if sheets:
            max_sheet = max(sheets, key=lambda x: len(x.get("records", [])))
            min_sheet = min(sheets, key=lambda x: len(x.get("records", [])))
            
            if len(sheets) > 1:
                report += f"- 📊 最大数据表：**{max_sheet.get('sheet_name')}** ({len(max_sheet.get('records', []))}条)\n"
                report += f"- 📋 最小数据表：**{min_sheet.get('sheet_name')}** ({len(min_sheet.get('records', []))}条)\n"
        
        # 分析字段完整性
        if records:
            sample_fields = list(records[0].get("fields", {}).keys())
            if sample_fields:
                report += f"- 🏷️ 主要字段：{', '.join(sample_fields[:5])}\n"
        
        report += "\n---\n\n"
    
    # 风险预警
    report += "## 🚨 风险与异常识别\n\n"
    
    # 自动识别风险
    risks = []
    
    # 检查空数据表
    empty_sheets = []
    for table in tables_data:
        for sheet in table.get("sheets", []):
            if len(sheet.get("records", [])) == 0:
                empty_sheets.append(f"{table.get('table_name')} - {sheet.get('sheet_name')}")
    
    if empty_sheets:
        risks.append({
            "level": "⚠️",
            "title": "空数据表",
            "desc": f"{len(empty_sheets)} 个数据表为空：{', '.join(empty_sheets[:3])}"
        })
    
    # 检查数据量异常
    for table in tables_data:
        records = table.get("records", [])
        if len(records) == 0:
            risks.append({
                "level": "⚠️",
                "title": "空表格",
                "desc": f"{table.get('table_name')} 无数据"
            })
    
    # 检查数据重复（简单检测）
    if len(tables_data) >= 2:
        # 检查是否有表格名称相似
        names = [t.get("table_name", "") for t in tables_data]
        similar = []
        for i, n1 in enumerate(names):
            for n2 in names[i+1:]:
                if n1 and n2 and (n1 in n2 or n2 in n1):
                    similar.append(f"{n1} 和 {n2}")
        
        if similar:
            risks.append({
                "level": "⚠️",
                "title": "疑似重复表格",
                "desc": f"以下表格名称相似，可能存在数据重复：{similar[0]}"
            })
    
    if risks:
        for risk in risks:
            report += f"{risk['level']} **{risk['title']}**: {risk['desc']}\n\n"
    else:
        report += "✅ **未发现明显风险项**\n\n"
    
    # 行动建议
    report += "---\n\n"
    report += "## 📋 行动建议\n\n"
    
    # 生成具体建议
    suggestions = []
    
    # 基于数据量建议
    if total_records > 500:
        suggestions.append({
            "priority": "🔴 高",
            "action": "数据梳理",
            "detail": f"当前共 {total_records} 条记录，建议进行数据分类和归档",
            "timeline": "本周内"
        })
    
    # 基于空表建议
    if empty_sheets:
        suggestions.append({
            "priority": "🟡 中",
            "action": "空表处理",
            "detail": f"{len(empty_sheets)} 个空数据表，建议确认是否需要保留或填充数据",
            "timeline": "3 天内"
        })
    
    # 基于表格数量建议
    if total_tables > 5:
        suggestions.append({
            "priority": "🟡 中",
            "action": "表格整合",
            "detail": f"当前有 {total_tables} 个相关表格，建议建立统一索引或整合",
            "timeline": "本周内"
        })
    
    # 通用建议
    suggestions.append({
        "priority": "🟢 低",
        "action": "定期分析",
        "detail": "建议每周运行一次分析，建立数据基线和趋势追踪",
        "timeline": "持续进行"
    })
    
    for i, sug in enumerate(suggestions, 1):
        report += f"**{i}. {sug['action']}** ({sug['priority']})\n"
        report += f"   - {sug['detail']}\n"
        report += f"   - 时间：{sug['timeline']}\n\n"
    
    # 技术说明
    report += "---\n\n"
    report += "## ℹ️ 技术说明\n\n"
    report += f"- **数据来源**: 钉钉 AI 表格（关键词：{keyword if keyword else '全量'}）\n"
    report += f"- **分析范围**: {total_tables} 个表格，{total_sheets} 个数据表，{total_records} 条记录\n"
    report += "- **分析方法**: 分页读取、自动合并、智能分析\n"
    report += f"- **数据抽样**: 每个数据表最多读取前 {DEFAULT_LIMIT} 条记录用于分析\n"
    report += "\n---\n\n"
    report += f"*报告生成：dingtalk-ai-table-insights v{SKILL_VERSION}*  \n"
    report += f"*分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return report


def generate_log_file(tables_data: List[Dict], failed_tables: List[Dict], keyword: str = "") -> str:
    """
    生成执行日志（包含权限问题、失败信息等）
    
    Args:
        tables_data: 成功读取的表格数据
        failed_tables: 失败的表格列表
        keyword: 搜索关键词
    
    Returns:
        日志内容（Markdown 格式）
    """
    from datetime import datetime
    
    log = f"# 📝 执行日志 - {keyword if keyword else 'AI 表格分析'}\n\n"
    log += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # 成功统计
    log += "## ✅ 成功读取的表格\n\n"
    log += f"共 {len(tables_data)} 个表格，数据读取成功。\n\n"
    
    for table in tables_data:
        table_name = table.get("table_name", "未知表格")
        doc_id = table.get("doc_id", "N/A")
        records = len(table.get("records", []))
        log += f"- {table_name}: {records} 条记录\n"
    
    # 失败统计
    if failed_tables:
        log += "\n---\n\n"
        log += "## ⚠️ 未能读取的表格\n\n"
        log += f"共 {len(failed_tables)} 个表格，读取失败。\n\n"
        
        for table in failed_tables:
            table_name = table.get("table_name", "未知表格")
            reason = table.get("reason", "未知原因")
            error_code = table.get("error_code", "")
            
            log += f"### {table_name}\n"
            log += f"- **原因**: {reason}\n"
            if error_code:
                log += f"- **错误码**: {error_code}\n"
            
            # 提供解决建议
            if error_code == "601":
                log += f"- **建议**: MCP token 组织不匹配，请联系表格所有者重新分享或使用正确组织的 token\n"
            elif "empty" in reason.lower():
                log += f"- **建议**: 表格无数据表，建议确认是否需要保留\n"
            else:
                log += f"- **建议**: 检查权限或联系管理员\n"
            
            log += "\n"
    else:
        log += "\n---\n\n"
        log += "## ✅ 所有表格读取成功，无失败记录。\n"
    
    log += "\n---\n\n"
    log += f"*日志生成：dingtalk-ai-table-insights v{SKILL_VERSION}*  \n"
    log += f"*时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return log


def main():
    parser = argparse.ArgumentParser(description='dingtalk-ai-table-insights - AI 表格跨表格洞察分析')
    parser.add_argument('--keyword', type=str, default='', help='表格名称关键词筛选')
    parser.add_argument('--output', type=str, default='', help='输出文件路径')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='输出格式')
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT, help='每个表格抽样记录数')
    parser.add_argument('--no-cache', action='store_true', help='禁用缓存')
    parser.add_argument('--clear-cache', action='store_true', help='清除缓存后退出')
    parser.add_argument('--no-llm', action='store_true', help='不使用大模型分析，使用本地模板生成报告')
    
    args = parser.parse_args()
    
    # 清除缓存
    if args.clear_cache:
        clear_cache()
        return
    
    if args.keyword:
        print(f"🔍 开始分析 AI 表格... (关键词：{args.keyword})")
    else:
        print(f"🔍 开始分析 AI 表格... (全量扫描)")
    
    # 1. 获取可访问的表格列表
    print("📋 获取表格列表...")
    tables = get_accessible_tables(args.keyword, use_cache=not args.no_cache)
    print(f"   找到 {len(tables)} 个表格")
    
    if not tables:
        print("⚠️  未找到匹配的表格")
        print("💡 提示：尝试使用 --no-cache 强制刷新，或检查关键词是否正确")
        return
    
    # 2. 读取表格数据（读取所有 Sheet）
    print("📊 读取表格数据...")
    tables_data = []
    failed_tables = []  # 记录失败的表格
    total_sheets = 0
    total_records = 0
    
    for i, table in enumerate(tables, 1):
        # 尝试多种字段名获取表格名称
        table_name = (
            table.get("docName") or 
            table.get("title") or 
            table.get("name") or 
            table.get("fileName") or
            "未知表格"
        )
        doc_id = table.get("docId") or table.get("dentryUuid") or ""
        
        if not doc_id:
            print(f"   [{i}/{len(tables)}] ⚠️  跳过 {table_name} (缺少 docId)")
            failed_tables.append({
                "table_name": table_name,
                "reason": "缺少 docId",
                "error_code": ""
            })
            continue
        
        print(f"   [{i}/{len(tables)}] 读取 {table_name}...")
        
        # 读取所有 Sheet 的数据
        all_sheets_data = read_all_sheets_data(doc_id, args.limit)
        
        if all_sheets_data:
            # 合并所有 Sheet 的记录
            all_records = []
            sheet_summary = []
            for sheet_data in all_sheets_data:
                sheet_name = sheet_data.get("sheet_name", "未知 Sheet")
                records = sheet_data.get("records", [])
                all_records.extend(records)
                if records:
                    sheet_summary.append(f"{sheet_name}: {len(records)}条")
                total_sheets += 1
                total_records += len(records)
            
            tables_data.append({
                "table_name": table_name,
                "doc_id": doc_id,
                "records": all_records,
                "sheets": all_sheets_data  # 保留每个 Sheet 的详细信息
            })
            
            status = f"{len(all_records)} 条记录" if len(all_records) > 0 else "表格为空"
            sheets_info = f" ({', '.join(sheet_summary[:5])}{'...' if len(sheet_summary) > 5 else ''})" if sheet_summary else ""
            print(f"      ✅ 读取成功 ({status}){sheets_info}")
        else:
            print(f"      ⚠️  无访问权限或无数据（跳过）")
            failed_tables.append({
                "table_name": table_name,
                "reason": "无访问权限或无数据",
                "error_code": "601"
            })
    
    if not tables_data:
        print()
        print("⚠️  没有成功读取任何表格数据")
        print()
        print("💡 可能的原因:")
        print("   1. 所有表格都无访问权限（错误码 601）")
        print("   2. 表格确实为空")
        print("   3. Sheet 名称不正确（默认使用 'Sheet1'）")
        print()
        print("📋 建议:")
        print("   - 确认 MCP token 由表格所属组织颁发")
        print("   - 检查表格是否有数据")
        print("   - 联系钉钉 AI 表格管理员获取正确权限")
        return
    
    # 统计信息
    total_tables = len(tables)
    accessible_tables = len(tables_data)
    
    print()
    print(f"📊 读取完成：{accessible_tables}/{total_tables} 个表格，{total_sheets} 个数据表，共 {total_records} 条记录")
    
    # 3. 生成洞察报告（只包含成功读取的数据）
    print("🤖 生成洞察报告...")
    
    # 根据参数决定是否使用大模型分析
    if args.no_llm:
        print("   📝 使用本地模板生成报告（--no-llm 参数）")
        report = generate_insight_report(tables_data, args.keyword)
    else:
        # 默认使用大模型分析
        report = analyze_with_llm(tables_data, args.keyword)
    
    # 4. 输出报告
    if args.output:
        # 生成报告文件名
        base_name = args.output.rsplit(".", 1)[0] if "." in args.output else args.output
        report_path = f"{base_name}.{args.format}"
        log_path = f"{base_name}_执行日志.md"
        
        # 保存洞察报告
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 洞察报告已保存到：{report_path}")
        
        # 保存执行日志
        log_content = generate_log_file(tables_data, failed_tables, args.keyword)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(log_content)
        print(f"📝 执行日志已保存到：{log_path}")
    else:
        print("\n" + "="*60)
        print("📊 洞察报告")
        print("="*60)
        print(report)
        print("="*60)
        
        # 如果有失败的表格，提示查看日志
        if failed_tables:
            print(f"\n⚠️  有 {len(failed_tables)} 个表格读取失败，详细信息请查看执行日志")
            print(f"💡 使用 --output 参数保存报告和日志到文件")


if __name__ == "__main__":
    main()
