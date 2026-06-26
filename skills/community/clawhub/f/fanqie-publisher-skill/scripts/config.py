# -*- coding: utf-8 -*-
"""
番茄小说自动发布 - 配置文件
"""

# 基础配置
BASE_URL = "https://fanqienovel.com"
WRITER_URL = "https://fanqienovel.com/writer/zone/"
LOGIN_URL = "https://fanqienovel.com/main/writer/login?enter_from=skill"
# 作品管理页面（作品列表）
BOOK_MANAGE_URL = "https://fanqienovel.com/main/writer/book-manage"

# 浏览器配置
BROWSER_CONFIG = {
    "headless": False,  # 默认显示浏览器，方便用户看到登录过程
    "slow_mo": 100,     # 操作延迟，模拟人类行为
    "viewport": {
        "width": 1280,
        "height": 800
    },
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 超时配置
TIMEOUT = {
    "login": 120000,      # 登录超时 2分钟
    "page_load": 60000,   # 页面加载超时 60秒
    "publish": 120000    # 发布超时 2分钟
}

# Cookie存储路径
COOKIE_FILE = "fanqie_cookies.json"

# 选择器配置（根据实际页面结构调整）
SELECTORS = {
    # 登录相关
    "login_button": "text=登录",
    "login_qrcode": ".qrcode-container img",
    "login_success": "text=工作台",
    
    # 作品管理页面
    "work_list_item": ".book-item, .work-item",  # 作品卡片
    "work_title": ".book-title, .work-title",    # 作品名称（需要根据实际调整）
    "work_status": ".book-status",               # 作品状态
    
    # 作品操作
    "create_chapter_btn": "button:has-text('创建章节')",
    "chapter_manage_link": "a:has-text('章节管理')",
    "work_settings_btn": "button:has-text('作品设置')",
    
    # 章节发布页面
    "chapter_title_input": "input[placeholder*='章节标题'], input[placeholder*='标题']",
    "chapter_content_editor": ".editor-content, [contenteditable='true'], .chapter-editor",
    "publish_btn": "button:has-text('发布'), button:has-text('提交')",
    "save_btn": "button:has-text('保存')",
    
    # 定时发布
    "schedule_toggle": "text=定时发布",
    "schedule_time": "input[type='datetime-local']",
}

# 发布配置
PUBLISH_CONFIG = {
    "min_interval": 3,      # 发布间隔最小3秒
    "random_delay": True,   # 随机延迟
    "max_retries": 3        # 最大重试次数
}