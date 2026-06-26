#!/usr/bin/env python3
"""
DeepTask AI Worker
AI 自动拆解需求与执行任务

核心流程：
1. AI 拆解项目 → 会话 → 子任务 → MUF
2. AI 生成单元测试 (UT)
3. AI 实现 MUF 代码
4. 运行 UT 验证
5. **UT 通过后执行 git commit**（包含 SE_ID, ST_ID, MUF_ID, UT_ID）
6. 更新状态
"""

import sys
import os
import subprocess
import tempfile
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_manager import DeepTaskDB, DEFAULT_DB_PATH


class AIWorker:
    """AI 自动工作器"""
    
    def __init__(self, db_path: str = DEFAULT_DB_PATH, workspace: str = None):
        self.db = DeepTaskDB(db_path)
        self.workspace = workspace or os.path.expanduser("~/.openclaw/workspace")
        self.fail_threshold = 7
        self.timeout_hours = 5
    
    def check_environment(self, tool_name: str) -> Tuple[bool, str]:
        """检查工具链是否可用"""
        import shutil
        tool_path = shutil.which(tool_name)
        if not tool_path:
            return False, f"{tool_name} 未安装"
        
        try:
            # MoonBit 使用 `moon version` 而不是 `moon --version`
            if tool_name == "moon":
                result = subprocess.run([tool_name, "version"], 
                                        capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run([tool_name, "--version"], 
                                        capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return True, f"版本：{result.stdout.strip().split(chr(10))[0]}"
            else:
                return False, f"版本检查失败：{result.stderr.strip()}"
        except Exception as e:
            return False, f"检查异常：{e}"
    
    def hello_world_test(self, tool_name: str) -> Tuple[bool, str]:
        """运行 Hello World 测试验证语法"""
        if tool_name == "moon":
            return self._hello_world_moon()
        elif tool_name in ["python3", "python"]:
            return self._hello_world_python()
        elif tool_name == "node":
            return self._hello_world_node()
        else:
            return True, "跳过 Hello World 测试"
    
    def _hello_world_moon(self) -> Tuple[bool, str]:
        """测试 MoonBit Hello World"""
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.makedirs(os.path.join(tmpdir, "src", "test"))
                
                with open(os.path.join(tmpdir, "moon.mod.json"), "w") as f:
                    f.write('{"name":"test","version":"0.1.0"}')
                
                with open(os.path.join(tmpdir, "src", "test", "moon.pkg.json"), "w") as f:
                    f.write('{"is-main":true}')
                
                with open(os.path.join(tmpdir, "src", "test", "main.mbt"), "w") as f:
                    f.write('fn main { println("hello") }')
                
                result = subprocess.run(
                    ["moon", "build"],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return True, "MoonBit Hello World 编译通过"
                else:
                    return False, f"MoonBit 编译失败：{result.stderr[:200]}"
            except subprocess.TimeoutExpired:
                return False, "编译超时"
            except Exception as e:
                return False, f"编译异常：{e}"
    
    def _hello_world_python(self) -> Tuple[bool, str]:
        """测试 Python Hello World"""
        try:
            result = subprocess.run(
                ["python3", "-c", "print('hello')"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and "hello" in result.stdout:
                return True, "Python Hello World 运行通过"
            else:
                return False, "Python Hello World 运行失败"
        except Exception as e:
            return False, f"Python 运行异常：{e}"
    
    def _hello_world_node(self) -> Tuple[bool, str]:
        """测试 Node.js Hello World"""
        try:
            result = subprocess.run(
                ["node", "-e", "console.log('hello')"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and "hello" in result.stdout:
                return True, "Node.js Hello World 运行通过"
            else:
                return False, "Node.js Hello World 运行失败"
        except Exception as e:
            return False, f"Node.js 运行异常：{e}"
    
    def init_git(self, project_dir: str) -> bool:
        """初始化 git 仓库"""
        try:
            if not os.path.exists(os.path.join(project_dir, ".git")):
                subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
                print(f"✅ Git 仓库已初始化：{project_dir}")
            return True
        except Exception as e:
            print(f"❌ Git 初始化失败：{e}")
            return False
    
    def git_commit(self, project_dir: str, se_id: str, st_id: str, muf_id: str, ut_id: str) -> bool:
        """
        执行 git commit（UT 通过后）
        
        Commit 信息格式：
        "SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1"
        """
        try:
            # 1. 检查是否有更改
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                print(f"⚠️  没有更改，跳过 commit")
                return True
            
            # 2. Add all changes
            subprocess.run(["git", "add", "-A"], cwd=project_dir, check=True, capture_output=True)
            
            # 3. Commit with standardized message
            commit_msg = f"SE_ID:{se_id}, ST_ID:{st_id}, MUF_ID:{muf_id}, UT_ID:{ut_id}"
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Git commit 成功：{commit_msg}")
                return True
            else:
                print(f"❌ Git commit 失败：{result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Git commit 异常：{e}")
            return False
    
    def verify_git_history(self, project_dir: str, se_id: str, st_id: str, muf_id: str, ut_id: str) -> bool:
        """验证 git 历史中是否存在对应的 commit"""
        try:
            commit_msg = f"SE_ID:{se_id}, ST_ID:{st_id}, MUF_ID:{muf_id}, UT_ID:{ut_id}"
            result = subprocess.run(
                ["git", "log", "--oneline", "--grep", commit_msg],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            return bool(result.stdout.strip())
        except Exception as e:
            print(f"❌ 验证 git 历史失败：{e}")
            return False
    
    def execute_muf(self, muf_id: str, project_dir: str, tool_name: str, 
                    se_id: str, st_id: str, code_content: str = "") -> bool:
        """
        执行单个 MUF（含 UT 验证和 git commit）
        
        流程：
        1. 更新 MUF 状态为 in_progress
        2. 实现 MUF 代码
        3. 运行 UT 验证
        4. **UT 通过后执行 git commit**
        5. 更新 MUF 状态为 completed
        """
        # 获取关联的 UT
        uts = self.db.get_unit_tests_by_muf(muf_id)
        if not uts:
            print(f"❌ MUF 没有关联的 UT: {muf_id}")
            return False
        
        ut_id = uts[0]['id']
        
        print(f"\n=== 执行 MUF: {muf_id} ===")
        print(f"  SE: {se_id}, ST: {st_id}, UT: {ut_id}")
        
        # 1. 更新状态为 in_progress
        self.db.update_status("mufs", muf_id, "in_progress")
        
        # 2. 实现 MUF 代码
        print(f"  📝 实现 MUF 代码...")
        if code_content:
            # 写入代码文件
            code_file = os.path.join(project_dir, f"{muf_id.lower().replace('-', '_')}.py")
            with open(code_file, "w") as f:
                f.write(f"# SE_ID:{se_id}, ST_ID:{st_id}, MUF_ID:{muf_id}, UT_ID:{ut_id}\n")
                f.write(code_content)
            print(f"  ✅ 代码已写入：{code_file}")
        
        # 3. 运行 UT 验证
        print(f"  🧪 运行 UT 验证...")
        ut_passed = self.run_unit_test(ut_id, project_dir, tool_name)
        
        if not ut_passed:
            print(f"  ❌ UT 验证失败")
            self.db.update_status("mufs", muf_id, "failed")
            self.db.update_status("unit_tests", ut_id, "failed")
            return False
        
        print(f"  ✅ UT 验证通过")
        self.db.update_status("unit_tests", ut_id, "passed")
        
        # 4. ⭐ UT 通过后执行 git commit
        print(f"  📦 执行 git commit...")
        if self.git_commit(project_dir, se_id, st_id, muf_id, ut_id):
            if self.verify_git_history(project_dir, se_id, st_id, muf_id, ut_id):
                print(f"  ✅ Git commit 已验证")
            else:
                print(f"  ⚠️  Git commit 可能未成功")
        else:
            print(f"  ❌ Git commit 失败")
        
        # 5. 更新 MUF 状态为 completed
        self.db.update_status("mufs", muf_id, "completed")
        print(f"  ✅ MUF 完成")
        
        return True
    
    def run_unit_test(self, ut_id: str, project_dir: str, tool_name: str) -> bool:
        """运行单元测试"""
        ut = None
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM unit_tests WHERE id = ?", (ut_id,))
        row = cursor.fetchone()
        if row:
            ut = dict(row)
        
        if not ut:
            return False
        
        test_code = ut.get('test_code', '')
        
        if tool_name == "python3" or tool_name == "python":
            return self._run_python_test(test_code, project_dir)
        elif tool_name == "moon":
            return self._run_moon_test(project_dir)
        else:
            return True
    
    def _run_python_test(self, test_code: str, project_dir: str) -> bool:
        """运行 Python 测试"""
        try:
            result = subprocess.run(
                ["python3", "-c", test_code],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            print(f"  Python 测试异常：{e}")
            return False
    
    def _run_moon_test(self, project_dir: str) -> bool:
        """运行 MoonBit 测试"""
        try:
            result = subprocess.run(
                ["moon", "test"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            print(f"  MoonBit 测试异常：{e}")
            return False
    
    def update_progress(self):
        """更新任务进度"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM sessions WHERE status = 'in_progress'")
        
        for row in cursor.fetchall():
            session_id = row[0]
            
            if self.db.check_session_complete(session_id):
                self.db.update_status("sessions", session_id, "completed")
                print(f"✅ 会话 {session_id} 已完成")
                self.check_project_complete(session_id)
    
    def check_project_complete(self, session_id: str):
        """检查项目是否完成"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT project_id FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        
        if row:
            project_id = row[0]
            sessions = self.db.get_sessions_by_project(project_id)
            
            all_complete = all(s['status'] == 'completed' for s in sessions)
            if all_complete:
                print(f"🎉 项目 {project_id} 全部完成！")
    
    def check_fuse(self):
        """检查失败熔断"""
        failed_mufs = self.db.get_failed_mufs()
        
        for muf in failed_mufs:
            self.db.add_review_record(
                entity_type="muf",
                entity_id=muf['id'],
                reviewer="system",
                status="rejected",
                comments="自动熔断：UT 验证失败"
            )
            print(f"🔴 MUF {muf['id']} 已熔断，等待人工审查")
    
    def run_full_cycle(self, project_id: str, tool_name: str, project_dir: str):
        """执行完整的项目周期"""
        print("\n" + "="*50)
        print("DeepTask AI Worker - 完整执行周期")
        print("="*50 + "\n")
        
        # 1. 环境预检
        print("📋 步骤 1: 环境预检")
        env_ok, env_msg = self.check_environment(tool_name)
        if not env_ok:
            print(f"❌ 环境检查失败：{env_msg}")
            print("🔴 触发熔断：环境不可用")
            return
        print(f"✅ {env_msg}")
        
        # 2. Hello World 验证
        print("\n📋 步骤 2: Hello World 验证")
        hw_ok, hw_msg = self.hello_world_test(tool_name)
        if not hw_ok:
            print(f"❌ Hello World 失败：{hw_msg}")
            print("🔴 触发熔断：语法验证失败")
            return
        print(f"✅ {hw_msg}")
        
        # 3. 初始化 Git
        print("\n📋 步骤 3: 初始化 Git")
        self.init_git(project_dir)
        
        # 4. 执行 MUF
        print("\n📋 步骤 4: 执行 MUF（含 UT 验证和 git commit）")
        pending_mufs = self.db.get_pending_mufs()
        if pending_mufs:
            for muf in pending_mufs:
                # 获取父级 ID
                cursor = self.db.conn.cursor()
                cursor.execute("SELECT session_id FROM subtasks WHERE id = ?", (muf['subtask_id'],))
                row = cursor.fetchone()
                if row:
                    session_id = row[0]
                    st_id = muf['subtask_id']
                    se_id = session_id
                    
                    # 示例代码
                    code = "print('Hello from " + muf['id'] + "')"
                    success = self.execute_muf(muf['id'], project_dir, tool_name, se_id, st_id, code)
                    if not success:
                        print(f"  ⚠️  MUF {muf['id']} 执行失败，继续下一个")
        else:
            print("  暂无待处理的 MUF")
        
        # 5. 更新进度
        print("\n📋 步骤 5: 更新进度")
        self.update_progress()
        
        # 6. 检查熔断
        print("\n📋 步骤 6: 检查熔断")
        self.check_fuse()
        
        print("\n" + "="*50)
        print("周期完成")
        print("="*50 + "\n")
    
    def close(self):
        """关闭数据库连接"""
        if self.db.conn:
            self.db.conn.close()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="DeepTask AI Worker")
    parser.add_argument("--db", default=DEFAULT_DB_PATH, help="数据库路径")
    parser.add_argument("--workspace", default=None, help="工作目录")
    parser.add_argument("--project", help="项目 ID")
    parser.add_argument("--tool", default="python3", help="工具链 (moon/python/node)")
    parser.add_argument("--cycle", action="store_true", help="执行完整周期")
    
    args = parser.parse_args()
    
    worker = AIWorker(args.db, args.workspace)
    
    if args.project and args.cycle:
        project_dir = os.path.join(args.workspace, f"project_{args.project}")
        os.makedirs(project_dir, exist_ok=True)
        worker.run_full_cycle(args.project, args.tool, project_dir)
    else:
        parser.print_help()
    
    worker.close()


if __name__ == "__main__":
    main()
