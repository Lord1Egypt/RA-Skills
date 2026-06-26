#!/usr/bin/env python3
"""
Habit Tracker - 端到端验证脚本
模拟真实使用流程，验证所有核心功能是否正常工作

用法: python3 verify.py
"""

import asyncio
import json
import os
import shutil
import sys
from datetime import datetime, timedelta

# 确保能导入项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import HabitTracker
from models import HabitType, HabitStatus, TaskStatus

# ============ 工具函数 ============

PASS = "✅"
FAIL = "❌"
INFO = "📋"
STEP = "▶️"

test_results = []


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_step(step_num, desc):
    print(f"\n{STEP} 步骤 {step_num}: {desc}")
    print(f"{'─'*40}")


def check(desc, condition, detail=""):
    status = PASS if condition else FAIL
    print(f"  {status} {desc}")
    if detail:
        print(f"     {INFO} {detail}")
    test_results.append((desc, condition))
    return condition


def print_json(data, indent=4):
    """打印 JSON 数据，限制长度"""
    text = json.dumps(data, ensure_ascii=False, indent=indent)
    lines = text.split('\n')
    if len(lines) > 30:
        for line in lines[:25]:
            print(f"     {line}")
        print(f"     ... (省略 {len(lines) - 25} 行)")
    else:
        for line in lines:
            print(f"     {line}")


# ============ 主验证流程 ============

async def run_verification():
    # 使用临时目录，不影响真实数据
    test_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".verify_temp")
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)

    tracker = HabitTracker(data_dir=test_data_dir)

    try:
        # ============================================================
        print_header("1. 首次使用 - 空状态检测")
        # ============================================================
        print_step(1, "列出习惯（应为空）")
        result = await tracker.list_habits()
        print_json(result)
        check("返回成功", result.get("success") == True)
        check("无习惯", result.get("active_count") == 0)
        check("检测到首次使用", result.get("is_first_use") == True)
        check("可以添加习惯", result.get("can_add") == True)

        # ============================================================
        print_header("2. 创建习惯 - 递进型（跑步）")
        # ============================================================
        print_step(2, "创建跑步习惯")
        result = await tracker.create_habit("我想每天跑步", habit_type="progressive")
        print_json(result)
        check("创建成功", result.get("success") == True)
        check("状态为 draft", result.get("status") == "draft")
        habit_id_run = result.get("habit_id")
        check("有 habit_id", habit_id_run is not None, f"ID: {habit_id_run}")

        # ============================================================
        print_header("3. 目标合理化对话")
        # ============================================================
        print_step(3, "模拟合理化对话（2轮）")

        # 第 1 轮
        r1 = await tracker.update_rationalization(
            habit_id_run,
            ai_message="你目前的运动基础是什么？每周运动几次？",
            user_response="几乎不运动，久坐办公"
        )
        print_json(r1)
        check("第1轮记录成功", r1.get("success") == True)
        check("对话轮次=1", r1.get("round_count") == 1)

        # 第 2 轮
        r2 = await tracker.update_rationalization(
            habit_id_run,
            ai_message="建议从快走+慢跑 2 公里开始，逐步提升，你觉得呢？",
            user_response="可以，听起来不错"
        )
        check("第2轮记录成功", r2.get("success") == True)
        check("对话轮次=2", r2.get("round_count") == 2)

        # ============================================================
        print_header("4. 确认目标 & 生成计划")
        # ============================================================
        print_step(4, "确认合理化后的目标")
        result = await tracker.confirm_habit(
            habit_id_run,
            goal_refined="每天慢跑 2-5 公里，从 2 公里起步逐步提升",
            completion_criteria="完成当日计划的跑步距离",
            total_days=28
        )
        print_json(result)
        check("确认成功", result.get("success") == True)
        check("状态变为 active", result.get("status") == "active")
        check("需要生成计划", result.get("needs_plan_generation") == True)

        print_step("4b", "保存 AI 生成的初始 3 天计划")
        plan_data = {
            "phase_number": 1,
            "phase_length": 3,
            "start_day": 1,
            "daily_tasks": [
                {"day": 1, "description": "快走5分钟热身 + 慢跑 2 公里", "status": "pending"},
                {"day": 2, "description": "慢跑 2 公里 + 拉伸5分钟", "status": "pending"},
                {"day": 3, "description": "慢跑 2.5 公里", "status": "pending"},
            ]
        }
        result = await tracker.save_plan(habit_id_run, plan_data)
        print_json(result)
        check("计划保存成功", result.get("success") == True)

        # ============================================================
        print_header("5. 创建第二个习惯 - 打卡型（早起）")
        # ============================================================
        print_step(5, "创建早起习惯")
        result = await tracker.create_habit("每天早起", habit_type="checkin")
        check("创建成功", result.get("success") == True)
        habit_id_wake = result.get("habit_id")
        check("有 habit_id", habit_id_wake is not None, f"ID: {habit_id_wake}")

        # 直接确认（跳过合理化）
        result = await tracker.confirm_habit(
            habit_id_wake,
            goal_refined="每天 7:00 前起床",
            completion_criteria="7:00 前起床即算完成",
            total_days=21
        )
        check("确认成功", result.get("success") == True)

        # 保存打卡型计划
        plan_data = {
            "phase_number": 1,
            "phase_length": 3,
            "start_day": 1,
            "daily_tasks": [
                {"day": 1, "description": "7:00 前起床", "status": "pending"},
                {"day": 2, "description": "7:00 前起床", "status": "pending"},
                {"day": 3, "description": "7:00 前起床", "status": "pending"},
            ]
        }
        result = await tracker.save_plan(habit_id_wake, plan_data)
        check("打卡型计划保存成功", result.get("success") == True)

        # ============================================================
        print_header("6. 每日打卡")
        # ============================================================
        print_step(6, "跑步习惯 Day 1 打卡 - 完成")
        result = await tracker.check_in(
            habit_id_run,
            task_results=[{
                "task": "快走5分钟热身 + 慢跑 2 公里",
                "status": "completed",
                "note": "跑完感觉不错"
            }],
            day=1
        )
        print_json(result)
        check("打卡成功", result.get("success") == True)
        check("有统计数据", "stats" in result)

        print_step("6b", "跑步习惯 Day 2 打卡 - 部分完成")
        result = await tracker.check_in(
            habit_id_run,
            task_results=[{
                "task": "慢跑 2 公里 + 拉伸5分钟",
                "status": "partial",
                "note": "只跑了 1.5 公里，膝盖有点不舒服"
            }],
            day=2
        )
        check("部分完成打卡成功", result.get("success") == True)

        print_step("6c", "批量打卡（两个习惯同时）")
        result = await tracker.batch_check_in({
            habit_id_run: [{
                "task": "慢跑 2.5 公里",
                "status": "completed",
                "note": ""
            }],
            habit_id_wake: [{
                "task": "7:00 前起床",
                "status": "completed",
                "note": "6:45 就醒了"
            }]
        })
        print_json(result)
        check("批量打卡成功", result.get("success") == True)
        success_count = sum(1 for v in result.get("results", {}).values() if v.get("success"))
        check("两个习惯都打卡成功", success_count == 2, f"成功: {success_count}/2")

        print_step("6d", "测试 upsert（同一天重复打卡覆盖）")
        result = await tracker.check_in(
            habit_id_run,
            task_results=[{
                "task": "慢跑 2.5 公里",
                "status": "partial",
                "note": "改为部分完成（下午又跑了但没跑完）"
            }],
            day=3
        )
        check("upsert 打卡成功", result.get("success") == True)

        # ============================================================
        print_header("7. 查看总结")
        # ============================================================
        print_step(7, "每日总结")
        result = await tracker.get_summary(scope="daily")
        print_json(result)
        check("总结返回成功", result.get("success") == True)
        check("包含习惯数据", len(result.get("habits", [])) > 0)

        print_step("7b", "每周总结")
        result = await tracker.get_summary(scope="weekly")
        check("每周总结返回成功", result.get("success") == True)

        # ============================================================
        print_header("8. 可视化")
        # ============================================================
        print_step(8, "文本可视化")
        result = await tracker.get_visualization(fmt="text")
        check("文本可视化成功", result.get("success") == True)
        text_content = result.get("content", "")
        if text_content:
            print(f"\n{'─'*40}")
            print(text_content)
            print(f"{'─'*40}")

        print_step("8b", "SVG 可视化")
        result = await tracker.get_visualization(fmt="svg")
        check("SVG 可视化成功", result.get("success") == True)
        svg_output = result.get("content", "")
        check("SVG 内容非空", len(svg_output) > 100, f"SVG 长度: {len(svg_output)} 字符")
        check("SVG 格式正确", "<svg" in svg_output and "</svg>" in svg_output)

        # 保存 SVG 到临时文件供查看
        svg_path = os.path.join(test_data_dir, "preview.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_output)
        print(f"  {INFO} SVG 已保存到: {svg_path}")
        print(f"  {INFO} 可用浏览器打开查看效果")

        # ============================================================
        print_header("9. 提醒系统")
        # ============================================================
        print_step(9, "对话心跳检测")
        result = await tracker.reminder.check_pending(tracker)
        print_json(result)
        check("心跳检测返回", result is not None)

        print_step("9b", "触发定时提醒")
        result = await tracker.reminder.trigger_reminder(tracker)
        print_json(result)
        check("提醒触发成功", result.get("success") == True)

        # ============================================================
        print_header("10. 计划调整")
        # ============================================================
        print_step(10, "查看下一阶段参数建议")
        result = await tracker.adjust_plan(habit_id_run)
        print_json(result)
        check("计划调整返回成功", result.get("success") == True)
        check("有推荐参数", "next_phase_params" in result)

        # ============================================================
        print_header("11. 习惯生命周期管理")
        # ============================================================
        print_step(11, "暂停跑步习惯（active → paused）")
        result = await tracker.pause_habit(habit_id_run)
        check("暂停成功", result.get("success") == True)
        check("状态为 paused", result.get("status") == "paused")

        print_step("11b", "恢复跑步习惯（paused → active）")
        result = await tracker.resume_habit(habit_id_run)
        check("恢复成功", result.get("success") == True)
        check("状态为 active", result.get("status") == "active")

        print_step("11c", "放弃早起习惯")
        result = await tracker.abandon_habit(habit_id_wake)
        check("放弃成功", result.get("success") == True)
        check("状态为 abandoned", result.get("status") == "abandoned")

        print_step("11d", "列出所有习惯")
        result = await tracker.list_habits()
        print_json(result)
        check("习惯列表正确", len(result.get("habits", [])) == 2)
        active_count = result.get("active_count", 0)
        check("1 个 active 习惯", active_count == 1, f"active: {active_count}")

        # ============================================================
        print_header("12. 上限检查")
        # ============================================================
        print_step(12, "创建到上限（5个 active）然后验证拒绝")
        # 当前 1 个 active（跑步），1 个 abandoned（早起）
        # 再创建并确认 4 个 active 习惯
        extra_ids = []
        for i in range(4):
            r = await tracker.create_habit(f"测试习惯 {i+1}", habit_type="checkin")
            check(f"创建测试习惯 {i+1}", r.get("success") == True)
            eid = r.get("habit_id")
            extra_ids.append(eid)
            # 确认为 active
            cr = await tracker.confirm_habit(
                eid,
                goal_refined=f"测试目标 {i+1}",
                completion_criteria=f"测试标准 {i+1}",
                total_days=7
            )
            check(f"确认测试习惯 {i+1}", cr.get("success") == True)

        # 现在有 5 个 active，尝试创建第 6 个
        r = await tracker.create_habit("超出上限的习惯", habit_type="checkin")
        check("第6个 active 被拒绝", r.get("success") == False, f"错误: {r.get('error', 'N/A')}")

        # ============================================================
        print_header("13. CLI 命令验证")
        # ============================================================
        print_step(13, "通过 CLI 执行 list 命令")
        import subprocess
        cli_result = subprocess.run(
            [sys.executable, "agent.py", "list", "--data-dir", test_data_dir],
            capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__))
        )
        check("CLI list 执行成功", cli_result.returncode == 0)
        try:
            cli_data = json.loads(cli_result.stdout)
            check("CLI 输出有效 JSON", True)
            total_habits = len(cli_data.get("habits", []))
            check("CLI 列出所有习惯", total_habits == 6, f"习惯数: {total_habits}")
        except json.JSONDecodeError:
            check("CLI 输出有效 JSON", False, f"输出: {cli_result.stdout[:200]}")
            check("CLI 列出所有习惯", False)

        print_step("13b", "CLI summary 命令")
        cli_result = subprocess.run(
            [sys.executable, "agent.py", "summary", "--data-dir", test_data_dir],
            capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__))
        )
        check("CLI summary 执行成功", cli_result.returncode == 0)

        print_step("13c", "CLI visualize 命令")
        cli_result = subprocess.run(
            [sys.executable, "agent.py", "visualize", "--format", "text", "--data-dir", test_data_dir],
            capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__))
        )
        check("CLI visualize 执行成功", cli_result.returncode == 0)

        print_step("13d", "CLI remind 命令")
        cli_result = subprocess.run(
            [sys.executable, "agent.py", "remind", "--data-dir", test_data_dir],
            capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__))
        )
        check("CLI remind 执行成功", cli_result.returncode == 0)

        # ============================================================
        print_header("14. 数据持久化验证")
        # ============================================================
        print_step(14, "验证数据文件存在且可读")
        data_file = os.path.join(test_data_dir, "habits.json")
        check("数据文件存在", os.path.exists(data_file))
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        check("数据文件有效 JSON", True)
        check("包含 habits 数组", "habits" in data)
        check("habits 数量正确", len(data["habits"]) == 6, f"实际: {len(data['habits'])}")

        # 创建一个新 tracker 实例，验证数据能正确加载
        tracker2 = HabitTracker(data_dir=test_data_dir)
        result = await tracker2.list_habits()
        check("新实例加载数据正确", len(result.get("habits", [])) == 6)

        # ============================================================
        print_header("15. 完成与续期")
        # ============================================================
        print_step(15, "完成跑步习惯（归档）")
        result = await tracker.complete_habit(habit_id_run, action="archive")
        check("归档成功", result.get("success") == True)
        check("动作为 archive", result.get("action") == "archive")
        check("返回 stats", "stats" in result)

    finally:
        # ============ 打印总结 ============
        print_header("验证结果总结")
        total = len(test_results)
        passed = sum(1 for _, ok in test_results if ok)
        failed = total - passed

        if failed > 0:
            print(f"\n  失败项:")
            for desc, ok in test_results:
                if not ok:
                    print(f"  {FAIL} {desc}")

        print(f"\n  总计: {total} 项测试")
        print(f"  {PASS} 通过: {passed}")
        print(f"  {FAIL} 失败: {failed}")

        if failed == 0:
            print(f"\n  🎉 全部通过！Skill 核心功能验证完毕。")
        else:
            print(f"\n  ⚠️  有 {failed} 项失败，请检查。")

        # 清理临时数据
        print(f"\n  临时数据目录: {test_data_dir}")
        cleanup = input("  是否清理临时数据？(y/N): ").strip().lower()
        if cleanup == "y":
            shutil.rmtree(test_data_dir)
            print("  已清理。")
        else:
            print("  保留，可手动查看数据文件和 SVG 预览。")


if __name__ == "__main__":
    print("🔍 Habit Tracker Skill - 端到端验证")
    print(f"   运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Python: {sys.version.split()[0]}")
    asyncio.run(run_verification())
