"""
Configuration File
Please modify the following configuration according to your actual situation
配置文件
请根据实际情况修改以下配置
"""

import os

# Get project root directory (relative path)
# 获取项目根目录（相对路径）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ========== IMAP Email Configuration ==========
# IMAP 邮箱配置
IMAP_CONFIG = {
    'server': 'imap.qq.com',      # IMAP server address, e.g.: imap.qq.com (QQ Mail), imap.gmail.com (Gmail), imap.163.com (NetEase)
                                   # IMAP服务器地址，例如: imap.qq.com (QQ邮箱), imap.gmail.com (Gmail), imap.163.com (网易邮箱)
    'port': 993,                   # IMAP port, 993(SSL), 143(non-SSL)
                                   # IMAP端口，993(SSL加密), 143(非加密)
    'username': 'your-email@example.com', # Email username / 邮箱用户名
    'password': 'your-password-or-app-key',  # Email password or app-specific authorization code / 邮箱密码或授权码
    'use_ssl': True,              # Whether to use SSL / 是否使用SSL
}

# ========== Local Storage Configuration ==========
# 本地存储配置
STORAGE_CONFIG = {
    # Base path for storing processed emails
    # 存储处理后邮件的基础路径，默认在项目下的 email_storage 目录
    'base_path': os.path.join(PROJECT_ROOT, 'email_storage'),
    'raw_folder': 'raw',           # Raw emails folder / 原始邮件文件夹
    'text_folder': 'text',         # Extracted text folder / 提取文本文件夹
    'translated_folder': 'translated',  # Translated content folder / 翻译后文件夹
    'quotes_folder': 'quotes',     # Generated quotes folder / 报价回复文件夹
}

# ========== Pricing Data Configuration ==========
# 报价数据配置
PRICING_CONFIG = {
    # If you use Excel for pricing parameters, put it here
    # 如果您使用Excel保存报价参数，填写路径
    # 'material_price_xlsx': os.path.join(PROJECT_ROOT, 'data', 'material_prices.xlsx'),
    # If you use markdown for pricing rules documentation, put it here
    # 如果您用markdown保存报价规则文档，填写路径
    # 'pricing_rules_md': os.path.join(PROJECT_ROOT, 'data', 'pricing_rules.md'),
    'material_price_xlsx': None,
    'pricing_rules_md': None,
}

# ========== Schedule Configuration ==========
# 定时检查配置
SCHEDULE_CONFIG = {
    'check_interval_minutes': 30,  # Check interval in minutes / 检查间隔，单位分钟
}

# ========== Translation Configuration ==========
# 翻译配置
TRANSLATION_CONFIG = {
    'enabled': True,               # Enable auto translation / 是否启用翻译
    'default_target_lang': 'zh-CN', # Target language / 目标语言
    # Translation engine: 'google_free' (free Google Translate), 'baidu' (Baidu Translate requires API), 'none' (disable)
    # 翻译引擎: 'google_free' (免费谷歌翻译), 'baidu' (百度翻译需要API密钥), 'none' (不翻译)
    'engine': 'google_free',
    # Uncomment and configure if you use Baidu Translate
    # 如果使用百度翻译，取消注释并配置以下参数
    # 'baidu_appid': 'your_appid',
    'baidu_secret': 'your_secret',
}

# ========== Company Information ==========
# 企业信息（用于生成报价回复）
COMPANY_INFO = {
    'name': 'Your Company Name',    # 企业名称
    'contact_person': 'Sales Manager', # 联系人
    'phone': '+86 400-XXX-XXXX',    # 电话
    'website': 'www.yourcompany.com', # 官网
    'email': 'sales@yourcompany.com', # 邮箱
}
