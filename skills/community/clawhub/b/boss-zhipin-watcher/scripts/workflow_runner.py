"""
BOSS直聘招聘工作流运行器
支持断点续跑、状态保存、错误重试
使用方法：
- 首次运行：python workflow_runner.py
- 断点续跑：python workflow_runner.py --resume
- 查看状态：python workflow_runner.py --status
"""

import argparse
import json
import os
import subprocess
import time

from datetime import datetime

class WorkflowRunner:
    def __init__(self, workflow_path, state_file=".workflow_state.json"):
        self.workflow_path = workflow_path
        self.state_file = state_file
        self.workflow = self.load_workflow()
        self.state = self.load_state()
        self.global_vars = self.workflow.get("global_vars", {})
        self.initialize_global_vars()

    def load_workflow(self):
        """加载工作流配置"""
        import json
        with open(self.workflow_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_state(self):
        """加载状态文件"""
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "current_step": 0,
            "steps": {}
        }

    def save_state(self):
        """保存状态到文件"""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def initialize_global_vars(self):
        """初始化全局变量"""
        self.global_vars["date"] = datetime.now().strftime("%Y%m%d")
        self.global_vars["resume_folder"] = self.global_vars["resume_folder"].replace("{{date}}", self.global_vars["date"])
        os.makedirs(os.path.dirname(self.global_vars["resume_folder"]), exist_ok=True)

    def substitute_vars(self, text):
        """替换文本中的全局变量"""
        for key, value in self.global_vars.items():
            text = text.replace(f"{{{{global_vars.{key}}}}}", str(value))
        return text

    def execute_step(self, step):
        """执行单个步骤"""
        step_name = step["name"]
        print(f"\n[执行步骤] {step_name}: {step['description']}")

        # 更新步骤状态
        self.state["steps"][step_name] = {"status": "in_progress", "start_time": datetime.now().isoformat()}
        self.save_state()

        try:
            # 替换变量
            if step["tool"] == "exec":
                command = self.substitute_vars(step["parameters"]["command"])
                print(f"执行命令：{command}")
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                print(f"执行结果：{result.stdout}")
            elif step["tool"] == "message":
                message = self.substitute_vars(step["parameters"]["message"])
                print(f"发送消息：{message}")
                # 实际消息发送可对接企业微信/飞书等
            else:
                print(f"不支持的工具类型：{step['tool']}")

            # 标记步骤完成
            self.state["steps"][step_name] = {
                "status": "completed",
                "start_time": self.state["steps"][step_name]["start_time"],
                "end_time": datetime.now().isoformat()
            }
            return True
        except Exception as e:
            print(f"步骤失败：{str(e)}")
            self.state["steps"][step_name] = {
                "status": "failed",
                "error": str(e),
                "start_time": self.state["steps"][step_name]["start_time"],
                "end_time": datetime.now().isoformat()
            }
            return False

    def run(self, resume=False):
        """运行工作流"""
        steps = self.workflow["steps"]
        start_index = self.state["current_step"] if resume else 0

        print(f"开始执行工作流（共{len(steps)}个步骤）")
        print(f"当前状态：{'断点续跑' if resume else '首次运行'}")

        for i in range(start_index, len(steps)):
            step = steps[i]
            step_name = step["name"]

            # 检查依赖
            dependencies = step.get("dependencies", [])
            if dependencies:
                for dep in dependencies:
                    dep_step = next((s for s in steps if s["name"] == dep), None)
                    if not dep_step or self.state["steps"].get(dep, {}).get("status") != "completed":
                        print(f"依赖步骤{dep}未完成，跳过当前步骤")
                        continue

            # 执行步骤
            success = self.execute_step(step)
            if not success:
                # 错误处理
                retry_limit = self.workflow.get("error_handling", {}).get("retry_limit", 3)
                retry_delay = self.workflow.get("error_handling", {}).get("retry_delay", 10)
                for retry in range(retry_limit):
                    print(f"重试第{retry+1}次...")
                    time.sleep(retry_delay)
                    if self.execute_step(step):
                        success = True
                        break
                if not success:
                    print(f"步骤{step_name}多次重试失败，工作流终止")
                    self.save_state()
                    return

            # 更新当前步骤
            self.state["current_step"] = i + 1
            self.save_state()

        print("\n✅ 工作流执行完成！")
        # 发送完成通知
        success_msg = self.workflow.get("notifications", {}).get("success_message", "工作流完成")
        print(f"通知：{success_msg}")

    def show_status(self):
        """显示工作流状态"""
        print("\n工作流状态：")
        for step in self.workflow["steps"]:
            step_name = step["name"]
            step_state = self.state["steps"].get(step_name, {})
            status = step_state.get("status", "pending")
            print(f"- {step_name}: {status}")
            if status in ["completed", "failed"]:
                print(f"  开始时间：{step_state.get('start_time', '未知')}")
                print(f"  结束时间：{step_state.get('end_time', '未知')}")
                if status == "failed":
                    print(f"  错误信息：{step_state.get('error', '未知')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BOSS直聘招聘工作流运行器")
    parser.add_argument("--resume", action="store_true", help="断点续跑")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--workflow", default="../recruitment_workflow.yaml", help="工作流配置文件路径")
    args = parser.parse_args()

    runner = WorkflowRunner(args.workflow)

    if args.status:
        runner.show_status()
    else:
        runner.run(resume=args.resume)

    # 清理状态文件（可选）
    # if runner.state["current_step"] >= len(runner.workflow["steps"]):
    #     os.remove(runner.state_file)
