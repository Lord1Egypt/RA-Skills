#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
novel-auto-publish - AI小说创作+番茄自动发布 主入口

整合:
  - open-novel-writing: AI小说创作
  - fanqie-publisher: 番茄小说自动发布
"""

import sys
import codecs
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stdout.buffer)

from auto_publish import AutoPublishWorkflow
import config


def print_banner():
    print("""
╔═╗┌─┐┌─┐┬─┐┌┬┐┌─┐┌┐┌┌┬┐  ┌─┐┬ ┬┌┐┌┌─┐├─┐┌─┐┬─┐
╚═╗├─┤├┤ ├┬┘ │ ├┤ │││ │   ├─┤│ ││││├─┤├┬┘├─┤├┬┘
╚═╝┴ ┴└─┘┴└─ ┴ └─┘┘└┘ ┴   ┴ ┴└─┘┘└┘┴ ┴┴└─┴ ┴┴└─
      AI小说创作 + 番茄自动发布 一条龙
=================================================
""")


def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("""可用命令:

  check                检查番茄登录状态
  login                重新登录番茄
  full "需求" "作品" [N] 从头创作N章并发布
  continue "作品" 目录 开始 结束  继续发布已创作的章节
  help                 显示帮助

示例:
  python main.py check
  python main.py full "都市重生回2010做互联网" "我的重生之旅" 5
  python main.py continue "我的重生之旅" ./novels/my-book 6 10
""")
        sys.exit(1)
    
    cmd = sys.argv[1]
    workflow = AutoPublishWorkflow()
    
    if cmd == 'check':
        ok, msg = workflow.check_fanqie_login()
        print(f"登录状态: {'✅ 已登录' if ok else '❌ 未登录'}")
        print(f"  {msg}")
        sys.exit(0 if ok else 1)
    
    elif cmd == 'login':
        # 调用 fanqie login
        import subprocess
        cmd_path = f"{config.FANQIE_PUBLISHER_PATH}/main.py"
        subprocess.run([sys.executable, cmd_path, 'login'])
        sys.exit(0)
    
    elif cmd == 'full':
        if len(sys.argv) < 4:
            print("❌ 参数不足: 需要 需求 作品名称 [章节数]")
            print("示例: python main.py full \"都市重生回2010\" \"我的新书\" 5")
            sys.exit(1)
        idea = sys.argv[2]
        work_title = sys.argv[3]
        chapter_count = int(sys.argv[4]) if len(sys.argv) > 4 else config.DEFAULT_CHAPTER_COUNT
        result = workflow.full_workflow(idea, work_title, chapter_count)
        if not result['success']:
            print(f"\n❌ 流程失败: {result.get('message', '未知错误')}")
            sys.exit(1)
        print("\n✨ 全部完成!")
    
    elif cmd == 'continue':
        if len(sys.argv) != 6:
            print("❌ 参数不足: 需要 作品名称 项目目录 起始章 结束章")
            sys.exit(1)
        work_title = sys.argv[2]
        project_dir = sys.argv[3]
        start = int(sys.argv[4])
        end = int(sys.argv[5])
        result = workflow.continue_workflow(work_title, project_dir, start, end)
        if not result['success']:
            print(f"\n❌ 发布失败: {result.get('message', '未知错误')}")
            sys.exit(1)
        print(f"\n✨ 完成! 成功发布 {result.get('published_count', 0)} 章")
    
    else:
        print(f"❌ 未知命令: {cmd}")
        print("输入 python main.py 查看帮助")
        sys.exit(1)


if __name__ == "__main__":
    main()
