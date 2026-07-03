#!/usr/bin/env python3
"""
记录任务到历史记录 v3
改进点：
1. 使用 path_detector v3（锚点机制 + 优先续写）
2. 写入后验证
3. 精细化异常处理
"""
import sys
import json
import os
from datetime import datetime
from pathlib import Path

try:
    from path_detector import get_task_history_path, get_platform_info
except ImportError:
    # Fallback：与 path_detector.py 保持一致的内联版本
    ANCHOR_FILE = Path.home() / '.skill-logger' / '.anchor'

    def _get_candidate_bases():
        candidates = [
            str(Path.home()),
            os.getenv('PERSISTENT_DIR'),
            os.getenv('DATA_DIR'),
            os.getenv('WORKSPACE_DIR'),
            os.getenv('WORKSPACE_PATH'),
            os.getenv('WORK_DIR'),
            os.getcwd(),
            '/var/tmp',
            '/tmp',
        ]
        seen = set()
        result = []
        for p in candidates:
            if p and p not in seen:
                seen.add(p)
                result.append(p)
        return result

    def _test_writable(path):
        try:
            os.makedirs(path, exist_ok=True)
            test_file = os.path.join(path, '.test_write')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except (PermissionError, OSError):
            return False

    def _save_anchor(history_file):
        try:
            ANCHOR_FILE.parent.mkdir(parents=True, exist_ok=True)
            ANCHOR_FILE.write_text(history_file)
        except Exception:
            pass

    def get_task_history_path():
        candidate_bases = _get_candidate_bases()
        # 1. 读锚点
        if ANCHOR_FILE.exists():
            try:
                anchored_path = ANCHOR_FILE.read_text().strip()
                if _test_writable(str(Path(anchored_path).parent)):
                    return anchored_path
            except Exception:
                pass
        # 2. 找已有历史文件
        for base_path in candidate_bases:
            history_file = os.path.join(base_path, '.skill-logger', 'task_history.json')
            if os.path.exists(history_file) and _test_writable(os.path.dirname(history_file)):
                _save_anchor(history_file)
                return history_file
        # 3. 新建
        for base_path in candidate_bases:
            history_dir = os.path.join(base_path, '.skill-logger')
            history_file = os.path.join(history_dir, 'task_history.json')
            if _test_writable(history_dir):
                _save_anchor(history_file)
                return history_file
        raise RuntimeError("无法找到可写入的存储路径")

    def get_platform_info():
        return {'platform': 'unknown', 'cwd': os.getcwd()}


def validate_json_parameter(param_str, param_name):
    if not param_str or param_str.strip() == '':
        raise ValueError(f"参数 '{param_name}' 不能为空")
    try:
        return json.loads(param_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"参数 '{param_name}' JSON格式错误: {str(e)}\n输入: {param_str[:100]}")


def verify_file_write(history_file, expected_record_count, task_id):
    if not os.path.exists(history_file):
        raise RuntimeError(f"验证失败: 文件不存在 {history_file}")
    if os.path.getsize(history_file) == 0:
        raise RuntimeError("验证失败: 文件大小为0")
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            verify_data = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"验证失败: 文件JSON格式错误 {str(e)}")
    if len(verify_data) != expected_record_count:
        raise RuntimeError(f"验证失败: 期望记录数 {expected_record_count}, 实际 {len(verify_data)}")
    if not any(r.get('task_id') == task_id for r in verify_data):
        raise RuntimeError(f"验证失败: 未找到任务ID {task_id}")
    return {
        "file_exists": True,
        "file_size": os.path.getsize(history_file),
        "record_count": len(verify_data),
        "last_modified": os.path.getmtime(history_file),
        "task_id_verified": True,
    }


def record_task(task_type, task_name, parameters, operations=None, status='成功', result=None):
    try:
        history_file = get_task_history_path()

        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []

        if isinstance(parameters, str):
            parameters = validate_json_parameter(parameters, 'parameters')
        elif not isinstance(parameters, (dict, list)):
            raise ValueError(f"'parameters' 必须是JSON字符串或字典/列表，当前: {type(parameters)}")

        if operations:
            if isinstance(operations, str):
                operations = validate_json_parameter(operations, 'operations')
            elif not isinstance(operations, list):
                raise ValueError(f"'operations' 必须是JSON字符串或列表")
        else:
            operations = []

        if result:
            if isinstance(result, str):
                result = validate_json_parameter(result, 'result')
            elif not isinstance(result, dict):
                raise ValueError(f"'result' 必须是JSON字符串或字典")
        else:
            result = {}

        task_id = f"{task_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        platform_info = get_platform_info()

        task_record = {
            "task_id": task_id,
            "task_type": task_type,
            "task_name": task_name,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": status,
            "parameters": parameters,
            "operations": operations,
            "result": result,
            "platform": platform_info.get('platform', 'unknown'),
        }

        history.append(task_record)
        expected_count = len(history)

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

        verification = verify_file_write(history_file, expected_count, task_id)

        print(json.dumps({
            "success": True,
            "task_id": task_id,
            "message": f"任务记录成功：{task_name}",
            "storage_path": str(history_file),
            "platform": platform_info.get('platform', 'unknown'),
            "total_records": expected_count,
            "verification": verification,
        }, ensure_ascii=False, indent=2))

    except ValueError as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "error_type": "ParameterError",
            "error_category": "参数格式错误",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    except RuntimeError as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "error_type": "RuntimeError",
            "error_category": "文件操作或验证失败",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "error_category": "未知错误",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='记录任务到历史记录 v3')
    parser.add_argument('--task-type', required=True)
    parser.add_argument('--task-name', required=True)
    parser.add_argument('--params', required=True)
    parser.add_argument('--operations', default=None)
    parser.add_argument('--status', default='成功')
    parser.add_argument('--result', default=None)

    args = parser.parse_args()
    record_task(
        task_type=args.task_type,
        task_name=args.task_name,
        parameters=args.params,
        operations=args.operations,
        status=args.status,
        result=args.result,
    )
