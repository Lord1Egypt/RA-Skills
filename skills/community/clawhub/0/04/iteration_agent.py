#!/usr/bin/env python3
"""
AI自动迭代技能 v1.0
安全的自动任务迭代和优化系统
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Callable
import time
import re


class AISecurityError(Exception):
    """安全异常"""
    pass


class SecurityValidator:
    """安全验证器"""

    # 危险操作黑名单
    DANGEROUS_OPERATIONS = [
        'rm -rf',
        'delete',
        'drop table',
        'format',
        'shutdown',
        'reboot',
        'systemctl stop',
    ]

    # 允许的工具列表
    ALLOWED_TOOLS = [
        'search',
        'read',
        'write',
        'calculate',
        'validate',
        'analyze',
    ]

    @classmethod
    def validate_operation(cls, operation: str) -> bool:
        """验证操作安全性"""
        op_lower = operation.lower()

        # 检查危险操作
        for dangerous in cls.DANGEROUS_OPERATIONS:
            if dangerous in op_lower:
                raise AISecurityError(f"检测到危险操作: {dangerous}")

        return True

    @classmethod
    def validate_tool(cls, tool_name: str) -> bool:
        """验证工具是否允许"""
        if tool_name not in cls.ALLOWED_TOOLS:
            raise AISecurityError(f"工具不在允许列表中: {tool_name}")
        return True


class TaskLogger:
    """任务日志记录器"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path.home() / ".ai_iteration_log.db"

        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """初始化日志数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                iterations INTEGER DEFAULT 0,
                max_iterations INTEGER DEFAULT 3,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                result TEXT,
                error TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS iterations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                iteration_num INTEGER NOT NULL,
                action TEXT NOT NULL,
                result TEXT,
                quality_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        ''')

        conn.commit()
        conn.close()

    def log_task_start(self, task_name: str, max_iterations: int = 3) -> int:
        """记录任务开始"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tasks (task_name, max_iterations, status)
            VALUES (?, ?, 'in_progress')
        ''', (task_name, max_iterations))

        task_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return task_id

    def log_iteration(self, task_id: int, iteration_num: int,
                      action: str, result: str, quality_score: float = 0.0):
        """记录迭代"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO iterations (task_id, iteration_num, action, result, quality_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_id, iteration_num, action, result, quality_score))

        # 更新任务状态
        cursor.execute('''
            UPDATE tasks SET iterations = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (iteration_num, task_id))

        conn.commit()
        conn.close()

    def log_task_complete(self, task_id: int, result: str, success: bool = True):
        """记录任务完成"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        status = 'completed' if success else 'failed'

        cursor.execute('''
            UPDATE tasks SET status = ?, result = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, result, task_id))

        conn.commit()
        conn.close()

    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """获取任务历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, task_name, status, iterations, max_iterations,
                   created_at, result
            FROM tasks
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'task_name': row[1],
                'status': row[2],
                'iterations': row[3],
                'max_iterations': row[4],
                'created_at': row[5],
                'result': row[6]
            })

        conn.close()
        return results


class IterationAgent:
    """自动迭代Agent"""

    def __init__(self, max_iterations: int = 3, quality_threshold: float = 0.7):
        """
        初始化迭代Agent

        Args:
            max_iterations: 最大迭代次数
            quality_threshold: 质量阈值（0-1）
        """
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        self.validator = SecurityValidator()
        self.logger = TaskLogger()

    def execute_tool(self, tool_name: str, **kwargs) -> Dict:
        """
        执行工具（带安全验证）

        Args:
            tool_name: 工具名称
            **kwargs: 工具参数

        Returns:
            执行结果
        """
        # 安全验证
        self.validator.validate_tool(tool_name)
        self.validator.validate_operation(str(kwargs))

        # 工具实现
        tools = {
            'search': self._tool_search,
            'read': self._tool_read,
            'write': self._tool_write,
            'calculate': self._tool_calculate,
            'validate': self._tool_validate,
            'analyze': self._tool_analyze,
        }

        if tool_name not in tools:
            return {'error': f'未知工具: {tool_name}'}

        return tools[tool_name](**kwargs)

    def _tool_search(self, query: str, max_results: int = 5) -> Dict:
        """搜索工具"""
        return {
            'results': [
                {'title': f'结果1: {query}', 'url': 'https://example.com'},
                {'title': f'结果2: {query}', 'url': 'https://example.org'},
            ]
        }

    def _tool_read(self, file_path: str) -> Dict:
        """读取文件工具"""
        path = Path(file_path)

        if not path.exists():
            return {'error': '文件不存在'}

        if path.stat().st_size > 1024 * 1024:  # 1MB限制
            return {'error': '文件过大'}

        try:
            content = path.read_text(encoding='utf-8')
            return {'content': content[:1000]}  # 限制返回长度
        except Exception as e:
            return {'error': str(e)}

    def _tool_write(self, file_path: str, content: str) -> Dict:
        """写入文件工具"""
        # 验证文件路径
        path = Path(file_path)

        # 只允许写入当前目录
        if not path.resolve().is_relative_to(Path.cwd()):
            return {'error': '只能写入当前目录'}

        try:
            path.write_text(content, encoding='utf-8')
            return {'success': True, 'file': str(path)}
        except Exception as e:
            return {'error': str(e)}

    def _tool_calculate(self, expression: str) -> Dict:
        """计算工具（安全版）"""
        try:
            # 只允许数字和基本运算符
            if not re.match(r'^[\d\s+\-*/().]+$', expression):
                return {'error': '表达式包含非法字符'}

            result = eval(expression, {'__builtins__': {}}, {})
            return {'result': result}
        except Exception as e:
            return {'error': str(e)}

    def _tool_validate(self, data: str, rules: List[str] = None) -> Dict:
        """验证工具"""
        issues = []

        if len(data) < 10:
            issues.append('内容过短')

        if 'error' in data.lower():
            issues.append('包含错误标记')

        return {
            'valid': len(issues) == 0,
            'issues': issues
        }

    def _tool_analyze(self, content: str) -> Dict:
        """分析工具"""
        return {
            'length': len(content),
            'words': len(content.split()),
            'lines': len(content.split('\n')),
            'summary': content[:100] + '...' if len(content) > 100 else content
        }

    def evaluate_quality(self, result: Dict) -> float:
        """
        评估结果质量

        Args:
            result: 执行结果

        Returns:
            质量分数 (0-1)
        """
        score = 0.5  # 基础分

        # 有错误则扣分
        if 'error' in result:
            score -= 0.3

        # 有内容则加分
        if 'content' in result or 'result' in result:
            score += 0.3

        # 有数据则加分
        if 'data' in result or 'results' in result:
            score += 0.2

        return max(0.0, min(1.0, score))

    def run_task(self, task_name: str, task_steps: List[Dict]) -> Dict:
        """
        执行迭代任务

        Args:
            task_name: 任务名称
            task_steps: 任务步骤列表，每个步骤包含 tool 和 params

        Returns:
            最终结果
        """
        # 记录任务
        task_id = self.logger.log_task_start(task_name, self.max_iterations)

        print(f"\n开始任务: {task_name}")
        print(f"最大迭代次数: {self.max_iterations}")
        print("=" * 50)

        iteration = 0
        best_quality = 0.0
        best_result = None

        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n第 {iteration} 次迭代:")

            results = []
            total_quality = 0.0

            for step in task_steps:
                tool = step.get('tool')
                params = step.get('params', {})

                print(f"  执行工具: {tool}")

                try:
                    result = self.execute_tool(tool, **params)
                    quality = self.evaluate_quality(result)

                    results.append(result)
                    total_quality += quality

                    # 记录迭代
                    self.logger.log_iteration(
                        task_id, iteration, tool,
                        json.dumps(result, ensure_ascii=False), quality
                    )

                    print(f"    质量分数: {quality:.2f}")

                    if 'error' in result:
                        print(f"    错误: {result['error']}")

                except AISecurityError as e:
                    print(f"    安全错误: {e}")
                    break
                except Exception as e:
                    print(f"    执行错误: {e}")

            # 计算平均质量
            avg_quality = total_quality / len(results) if results else 0.0

            print(f"\n  本次迭代平均质量: {avg_quality:.2f}")

            # 更新最佳结果
            if avg_quality > best_quality:
                best_quality = avg_quality
                best_result = results

            # 检查是否达到阈值
            if avg_quality >= self.quality_threshold:
                print(f"  ✓ 达到质量阈值 ({self.quality_threshold})")
                break

            # 如果还有迭代次数，优化步骤
            if iteration < self.max_iterations:
                print(f"  → 质量未达标，准备第 {iteration + 1} 次迭代...")
                time.sleep(1)  # 避免过快迭代

        # 记录任务完成
        success = best_quality >= self.quality_threshold
        final_result = json.dumps(best_result, ensure_ascii=False) if best_result else "无结果"

        self.logger.log_task_complete(task_id, final_result, success)

        print("\n" + "=" * 50)
        print(f"任务完成!")
        print(f"最终质量分数: {best_quality:.2f}")
        print(f"总迭代次数: {iteration}")
        print(f"状态: {'成功' if success else '未达标'}")

        return {
            'task_id': task_id,
            'task_name': task_name,
            'iterations': iteration,
            'final_quality': best_quality,
            'success': success,
            'results': best_result
        }


def main():
    """命令行界面"""
    print("=" * 50)
    print("AI自动迭代系统 v1.0")
    print("=" * 50)

    agent = IterationAgent(max_iterations=3, quality_threshold=0.7)

    while True:
        print("\n请选择操作:")
        print("1. 执行任务")
        print("2. 查看历史")
        print("3. 创建示例任务")
        print("0. 退出")

        choice = input("\n请输入选项: ").strip()

        if choice == "0":
            print("再见！")
            break

        elif choice == "1":
            # 自定义任务
            task_name = input("任务名称: ").strip()

            print("\n定义任务步骤 (输入空行结束):")
            task_steps = []

            while True:
                tool = input("  工具名称 (search/read/write/calculate/validate/analyze): ").strip()
                if not tool:
                    break

                params_input = input("  参数 (JSON格式): ").strip()
                try:
                    params = json.loads(params_input) if params_input else {}
                except:
                    params = {}

                task_steps.append({'tool': tool, 'params': params})

            if task_steps:
                result = agent.run_task(task_name, task_steps)
                print(f"\n结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

        elif choice == "2":
            history = agent.logger.get_task_history(20)

            if history:
                print(f"\n最近 {len(history)} 个任务:")
                for task in history:
                    print(f"\n{task['id']}. {task['task_name']}")
                    print(f"   状态: {task['status']}")
                    print(f"   迭代: {task['iterations']}/{task['max_iterations']}")
                    print(f"   时间: {task['created_at']}")
            else:
                print("暂无历史记录")

        elif choice == "3":
            # 示例任务
            task_name = "示例：文本分析任务"
            task_steps = [
                {'tool': 'write', 'params': {'file_path': 'test.txt', 'content': 'Hello AI World! 这是一个测试文件。'}},
                {'tool': 'read', 'params': {'file_path': 'test.txt'}},
                {'tool': 'analyze', 'params': {'content': 'Hello AI World! 这是一个测试文件。'}},
            ]

            result = agent.run_task(task_name, task_steps)
            print(f"\n结果: {json.dumps(result, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
