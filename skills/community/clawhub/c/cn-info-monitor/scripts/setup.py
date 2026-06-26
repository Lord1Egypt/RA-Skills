"""
一键配置向导 — 交互式引导用户完成信息源监控助手的初始配置

步骤:
1. 选择/添加信息源（从模板中选择 + 自定义添加）
2. 设置关键词过滤（可选）
3. 选择推送渠道（终端/文件/飞书）
4. 配置LLM API（通义千问/DeepSeek/OpenAI）
5. 测试运行一次
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_DIR = SKILL_DIR / "config"
SOURCES_FILE = CONFIG_DIR / "sources.json"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
TEMPLATE_FILE = CONFIG_DIR / "sources_template.json"


def banner():
    print("""
╔════════════════════════════════════════════╗
║                                              ║
║   📡 信息源监控助手 — 初始配置向导           ║
║                                              ║
║   帮你快速设置信息源监控，每天自动获取摘要    ║
║                                              ║
╚════════════════════════════════════════════╝
""")


def step_1_sources():
    """步骤1: 配置信息源"""
    print("\n📋 步骤 1/5: 配置信息源")
    print("-" * 40)
    
    sources = []
    
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            template = json.load(f)
        
        enabled_templates = [s for s in template if s.get("enabled", True)]
        disabled_templates = [s for s in template if not s.get("enabled", True)]
        
        print("\n预置热门信息源（默认启用）:")
        for i, s in enumerate(enabled_templates, 1):
            print("  [{}] {} ({})".format(i, s["name"], s["type"]))
        
        if disabled_templates:
            print("\n额外可用（默认禁用）:")
            for i, s in enumerate(disabled_templates, 1):
                print("  [{}] {} ({})".format(i + len(enabled_templates), s["name"], s["type"]))
        
        choice = input("\n使用默认预置源？(Y/n): ").strip().lower()
        if choice != "n":
            sources = list(template)
            print("✅ 已加载 {} 个预置信息源".format(len(sources)))
        else:
            print("请手动输入要启用的编号（逗号分隔）:")
            nums = input("> ").strip()
            selected = set(int(x.strip()) for x in nums.split(",") if x.strip().isdigit())
            
            all_sources = enabled_templates + disabled_templates
            sources = [all_sources[i-1] for i in selected if 0 < i <= len(all_sources)]
            print("✅ 已选择 {} 个信息源".format(len(sources)))
    
    while True:
        add_more = input("\n是否添加自定义信息源？(y/N): ").strip().lower()
        if add_more != "y":
            break
        
        name = input("  名称: ").strip() or "自定义源"
        url = input("  URL/RSS地址: ").strip()
        stype = input("  类型(rss/webpage/wechat) [rss]: ").strip().lower() or "rss"
        keywords_str = input("  关键词(逗号分隔，留空跳过): ").strip()
        keywords = [k.strip() for k in keywords_str.split(",") if k.strip()] if keywords_str else []
        
        sources.append({
            "name": name,
            "type": stype,
            "url": url,
            "keywords": keywords,
            "enabled": True
        })
        print("  ✅ 已添加: {}".format(name))
    
    return sources


def step_2_keywords():
    """步骤2: 全局关键词过滤"""
    print("\n🔍 步骤 2/5: 关键词过滤（可选）")
    print("-" * 40)
    print("设置全局关键词后，只推送包含这些关键词的文章。")
    print("留空则不过滤，推送所有文章。")
    
    kw_input = input("全局关键词（逗号分隔，留空跳过）: ").strip()
    keywords = [k.strip() for k in kw_input.split(",") if k.strip()] if kw_input else []
    
    print("✅ 全局关键词: {}".format(", ".join(keywords) if keywords else "(不过滤)"))
    return keywords


def step_3_channels():
    """步骤3: 推送渠道"""
    print("\n📤 步骤 3/5: 推送渠道")
    print("-" * 40)
    
    channels = ["terminal", "file"]
    
    use_feishu = input("是否启用飞书群推送？(y/N): ").strip().lower()
    if use_feishu == "y":
        webhook = input("  飞书Webhook URL: ").strip()
        if webhook:
            channels.append("feishu")
            os.environ["FEISHU_WEBHOOK_URL"] = webhook
            print("  ✅ 飞书推送已配置")
    
    print("✅ 推送渠道: {}".format(", ".join(channels)))
    return channels


def step_4_llm():
    """步骤4: LLM API配置"""
    print("\n🤖 步骤 4/5: LLM API配置")
    print("-" * 40)
    print("AI摘要功能需要调用大语言模型API。")
    print("支持: 通义千问(qwen)/DeepSeek/OpenAI兼容接口")
    
    api_key = input("  API Key (留空使用环境变量 LLM_API_KEY): ").strip()
    base_url = input("  API Base URL [https://dashscope.aliyuncs.com/compatible-mode/v1]: ").strip()
    model = input("  模型名称 [qwen-plus]: ").strip()
    
    llm_config = {}
    if api_key:
        llm_config["api_key"] = api_key
        os.environ["LLM_API_KEY"] = api_key
    if base_url:
        llm_config["base_url"] = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        os.environ["LLM_API_BASE_URL"] = llm_config["base_url"]
    if model:
        llm_config["model"] = model or "qwen-plus"
        os.environ["LLM_MODEL"] = llm_config["model"]
    
    has_key = bool(api_key or os.environ.get("LLM_API_KEY"))
    print("  ✅ LLM配置: {} (摘要{})".format(
        llm_config.get("model", "qwen-plus"),
        "可用" if has_key else "将使用降级方案"
    ))
    return llm_config


def step_5_test(sources, keywords, channels):
    """步骤5: 测试运行"""
    print("\n🧪 步骤 5/5: 测试运行")
    print("-" * 40)
    
    run_test = input("现在运行一次测试采集？(Y/n): ").strip().lower()
    if run_test == "n":
        print("⏭️ 跳过测试。可稍后运行: python scripts/daily_digest.py")
        return True
    
    try:
        from monitor import run_monitor
        from summarizer import generate_digest
        from pusher import push_all
        
        print("\n正在测试采集...")
        result = run_monitor(keywords=keywords)
        
        if result.get("status") == "ok":
            articles = result.get("articles", [])
            if articles:
                digest = generate_digest(articles, keywords=keywords, title="📡 测试简报")
                push_results = push_all(digest, channels=channels)
                print("\n✅ 测试成功！发现 {} 篇新文章".format(result["new_articles"]))
            else:
                print("\n✅ 测试成功！暂无新文章（可能已被读取过）")
            return True
        else:
            print("\n⚠️ 测试返回: {}".format(result.get("status")))
            return False
            
    except Exception as e:
        print("\n❌ 测试出错: {}".format(e))
        print("提示: 请确保已安装依赖: pip install requests feedparser")
        return False


def save_config(sources, keywords, channels, llm_config):
    """保存所有配置"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)
    
    settings = {
        "keywords": keywords,
        "channels": channels,
        "llm": llm_config,
        "configured_at": __import__("datetime").datetime.now().isoformat(),
        "version": "1.0.0"
    }
    
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
    
    print("\n💾 配置已保存:")
    print("  - 信息源: {}".format(SOURCES_FILE))
    print("  - 设置: {}".format(SETTINGS_FILE))


def main():
    banner()
    
    sources = step_1_sources()
    keywords = step_2_keywords()
    channels = step_3_channels()
    llm_config = step_4_llm()
    
    save_config(sources, keywords, channels, llm_config)
    
    success = step_5_test(sources, keywords, channels)
    
    print("""
╔════════════════════════════════════════════╗
║                                              ║
║   🎉 配置完成！                               ║
║                                              ║
║   日常使用:                                   ║
║   python scripts/daily_digest.py              ║
║                                              ║
║   或带关键词过滤:                              ║
║   python scripts/daily_digest.py -k AI Agent   ║
║                                              ║
║   查看状态:                                   ║
║   python scripts/license.py status             ║
║                                              ║
╚════════════════════════════════════════════╝
""")
    
    return success


if __name__ == "__main__":
    main()
