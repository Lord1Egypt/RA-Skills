#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音浏览器自动化工作流
版本: 1.0.0

使用方法:
1. 使用 OpenClaw Browser 打开抖音
2. 导航到目标页面
3. 调用对应函数执行操作
"""

# 视频页面评论自动化流程
VIDEO_COMMENT_WORKFLOW = """
=== 视频评论自动化流程 ===

1. 打开视频页面
   browser.navigate("https://www.douyin.com/video/{video_id}")

2. 等待页面加载
   browser.snapshot()

3. 点击评论输入框（一般在页面下方）
   browser.act(ref="e2079", kind="click")

4. 输入回复内容
   browser.act(ref="e2079", kind="type", text="分析得很透彻！")

5. 点击发送按钮（通常是输入框右侧的图标）
   browser.act(ref="e2xxx", kind="click")

6. 等待发送完成
   browser.snapshot()
"""

# 私信自动化流程
DM_WORKFLOW = """
=== 私信自动化流程 ===

1. 打开抖音主页
   browser.navigate("https://www.douyin.com")

2. 点击侧边栏"私信"按钮
   browser.act(ref="e267", kind="click")

3. 等待私信列表加载
   browser.snapshot()

4. 点击目标用户的聊天
   browser.act(ref="e1967", kind="click")

5. 在输入框输入内容
   browser.act(ref="e959", kind="type", text="你的视频很有深度！")

6. 点击发送按钮
   browser.act(ref="e972", kind="click")

注意: 私信发送有风控，建议使用半自动模式
"""

# 点赞自动化流程
LIKE_WORKFLOW = """
=== 点赞自动化流程 ===

1. 打开目标视频页面
   browser.navigate("https://www.douyin.com/video/{video_id}")

2. 等待页面加载
   browser.snapshot()

3. 找到点赞按钮（心形图标）
   browser.act(ref="e1632", kind="click")

4. 验证点赞成功（数字+1）
   browser.snapshot()
"""

# 搜索流程
SEARCH_WORKFLOW = """
=== 搜索流程 ===

1. 打开抖音主页
   browser.navigate("https://www.douyin.com")

2. 在搜索框输入关键词
   browser.act(ref="e126", kind="type", text="OpenClaw")

3. 点击搜索按钮
   browser.act(ref="e128", kind="click")

4. 等待搜索结果
   browser.snapshot()
"""

# 常用视频ID（示例）
SAMPLE_VIDEOS = {
    "毒舌电影": "7620789773875105043",
    "测试视频": "7324828873653706019",
}

def print_workflow(workflow_type="all"):
    """打印工作流说明"""
    if workflow_type in ["all", "comment"]:
        print(VIDEO_COMMENT_WORKFLOW)
    if workflow_type in ["all", "dm"]:
        print(DM_WORKFLOW)
    if workflow_type in ["all", "like"]:
        print(LIKE_WORKFLOW)
    if workflow_type in ["all", "search"]:
        print(SEARCH_WORKFLOW)


if __name__ == "__main__":
    import sys
    workflow = sys.argv[1] if len(sys.argv) > 1 else "all"
    print_workflow(workflow)
