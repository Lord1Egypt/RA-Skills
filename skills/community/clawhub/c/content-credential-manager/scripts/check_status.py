#!/usr/bin/env python3
"""
凭证状态检查脚本
检查所有内容创业相关技能的凭证配置状态
"""
import json
import os
import sys

CREDENTIALS_FILE = os.path.expanduser("~/.openclaw/credentials.json")

# 技能凭证清单
CREDENTIALS_CHECKLIST = {
    "tavily": {
        "skill": "tavily-search / openclaw-tavily-search",
        "fields": ["api_key"],
        "file_var": "TAVILY_API_KEY",
        "description": "Tavily AI搜索",
        "signup_url": "https://app.tavily.com"
    },
    "stepfun": {
        "skill": "step-tts",
        "fields": ["api_key"],
        "file_var": "STEPFUN_API_KEY",
        "description": "阶跃星辰语音合成",
        "signup_url": "https://platform.stepfun.com"
    },
    "meitu": {
        "skill": "other-openclaw-skills (美图AI)",
        "fields": ["access_key", "secret_key"],
        "file_var": "MEITU_OPENAPI_ACCESS_KEY / MEITU_OPENAPI_SECRET_KEY",
        "description": "美图开放平台",
        "signup_url": "https://www.miraclevision.com/open-claw"
    },
    "xiaohongshu": {
        "skill": "Auto-Redbook-Skills (发布)",
        "fields": ["cookie"],
        "file_var": "XHS_COOKIE",
        "description": "小红书 Cookie",
        "signup_url": "浏览器登录 xiaohongshu.com 获取"
    },
    "wechat": {
        "skill": "wechat-publish-skill",
        "fields": ["app_id", "app_secret"],
        "file_var": "WECHAT_APP_ID / WECHAT_APP_SECRET",
        "description": "微信公众号",
        "signup_url": "https://mp.weixin.qq.com"
    }
}

# 无需凭证的技能
NO_AUTH_SKILLS = [
    ("xhs-analytics-skill", "小红书爆款分析（公开数据）"),
    ("xhs-analytics-skill", "小红书运营自动化 SOP（无需API）"),
    ("xiaohongshu-automation", "小红书运营自动化（内容策划）"),
    ("Humanizer-zh", "人类化写作（无需API）"),
    ("memory-curator", "日志压缩（无需API）"),
    ("memory-hygiene", "向量清理（无需API）"),
]

def load_credentials():
    """加载凭证文件"""
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def check_field(value):
    """检查字段是否有值"""
    if value is None:
        return False
    if isinstance(value, str):
        return len(value.strip()) > 0
    return True

def main():
    print("📋 内容创业凭证状态检查")
    print("=" * 50)
    
    creds = load_credentials()
    configured = []
    missing = []
    
    for platform, info in CREDENTIALS_CHECKLIST.items():
        platform_creds = creds.get(platform, {})
        all_present = all(check_field(platform_creds.get(f)) for f in info["fields"])
        
        if all_present:
            configured.append((platform, info))
        else:
            missing.append((platform, info))
    
    # 已配置
    print("\n✅ 已配置 ({}/{})：".format(len(configured), len(CREDENTIALS_CHECKLIST)))
    if configured:
        for platform, info in configured:
            print(f"  • {info['description']} ({info['skill']})")
    else:
        print("  （暂无）")
    
    # 无需凭证
    print("\n🌐 无需凭证即可使用：")
    for skill, note in NO_AUTH_SKILLS:
        print(f"  • {skill}: {note}")
    
    # 缺失
    print("\n❌ 需要配置 ({}/{})：".format(len(missing), len(CREDENTIALS_CHECKLIST)))
    for platform, info in missing:
        missing_fields = [f for f in info["fields"] if not check_field(creds.get(platform, {}).get(f))]
        print(f"  • {info['description']}")
        print(f"    技能: {info['skill']}")
        print(f"    缺少: {', '.join(missing_fields)}")
        print(f"    获取: {info['signup_url']}")
    
    # 完成度
    total = len(CREDENTIALS_CHECKLIST)
    done = len(configured)
    pct = int(done / total * 100) if total > 0 else 0
    bar = "█" * (done * 10 // total) + "░" * ((total - done) * 10 // total)
    
    print(f"\n完成度: {bar} {done}/{total} ({pct}%)")
    
    if done == total:
        print("🎉 所有凭证已配置完成！可以开始内容创作。")
    elif done >= total - 1:
        print("👍 只差1个凭证了，加油！")
    else:
        print("💡 建议优先配置：Tavily（最简单，5分钟搞定）")
    
    return 0 if done == total else 1

if __name__ == "__main__":
    sys.exit(main())
