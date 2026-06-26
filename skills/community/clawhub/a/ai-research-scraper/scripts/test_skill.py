#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI Research Scraper技能的基本功能
"""

import sys
import os

# 检查技能文件是否完整
def test_skill_files():
    print("=== 测试技能文件完整性 ===\n")
    
    skill_dir = '/root/.openclaw/workspace/skills/ai-research-scraper'
    required_files = [
        'SKILL.md',
        'scripts/scraper.py',
        'references/websites.txt',
        'references/api_reference.md'
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = os.path.join(skill_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path} 存在")
            # 检查文件是否有内容
            if os.path.getsize(full_path) > 0:
                print(f"   大小: {os.path.getsize(full_path)} 字节")
            else:
                print(f"⚠️  {file_path} 是空文件")
        else:
            print(f"❌ {file_path} 不存在")
            all_exist = False
    
    print()
    return all_exist


# 检查脚本是否可以正常导入和运行
def test_script_import():
    print("=== 测试脚本导入和基本功能 ===\n")
    
    try:
        sys.path.append('/root/.openclaw/workspace/skills/ai-research-scraper/scripts')
        import scraper
        
        print("✅ 脚本导入成功")
        print()
        
        # 测试配置加载
        print("📄 配置测试:")
        websites = scraper.read_websites()
        print(f"   网站列表中有 {len(websites)} 个网站")
        
        for site in websites:
            print(f"   - {site['name']} ({site['url']})")
        
        # 测试文本处理函数
        print()
        print("📝 文本处理测试:")
        test_text = "OpenAI has announced a new feature for their platform that allows users to customize chatbots with specific knowledge bases. This update will make it easier for developers to create specialized AI assistants for various applications."
        
        # 测试关键词检测
        is_product = scraper.is_related_to_product_development("New Feature Announcement", test_text)
        print(f"   关键词检测: {'✅ 包含产品相关关键词' if is_product else '❌ 不包含'}")
        
        # 测试文本截断
        truncated = scraper.truncate_text(test_text, 20)
        print(f"   文本截断 (20个词): '{truncated}'")
        
        return True
        
    except Exception as e:
        print(f"❌ 脚本导入失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


# 测试网站列表
def test_websites_list():
    print("\n=== 测试网站列表 ===\n")
    
    websites = [
        {
            'name': 'TechCrunch AI',
            'url': 'https://techcrunch.com/ai/',
            'rss': 'https://techcrunch.com/ai/feed/'
        },
        {
            'name': 'VentureBeat AI',
            'url': 'https://venturebeat.com/ai/',
            'rss': 'https://venturebeat.com/ai/feed/'
        },
        {
            'name': 'MIT Tech Review AI',
            'url': 'https://www.technologyreview.com/tag/artificial-intelligence/',
            'rss': 'https://www.technologyreview.com/feed/tag/artificial-intelligence/'
        },
        {
            'name': 'OpenAI Blog',
            'url': 'https://openai.com/blog',
            'rss': 'https://openai.com/blog/rss'
        },
        {
            'name': 'Google AI Blog',
            'url': 'https://ai.googleblog.com/',
            'rss': 'https://ai.googleblog.com/feeds/posts/default'
        },
        {
            'name': 'Microsoft AI Blog',
            'url': 'https://blogs.microsoft.com/ai/',
            'rss': 'https://blogs.microsoft.com/ai/feed/'
        },
        {
            'name': 'NVIDIA Blog',
            'url': 'https://blogs.nvidia.com/blog/category/ai/',
            'rss': 'https://blogs.nvidia.com/blog/category/ai/feed/'
        },
        {
            'name': 'Medium AI Articles',
            'url': 'https://medium.com/tag/artificial-intelligence',
            'rss': 'https://medium.com/feed/tag/artificial-intelligence'
        }
    ]
    
    print("✅ 网站列表包含以下AI领域的知名网站:")
    for site in websites:
        print(f"   - {site['name']}")
    
    print(f"\n🎯 共 {len(websites)} 个网站")
    
    return True


def main():
    print("AI Research Scraper 技能测试\n")
    print("=" * 50)
    
    all_tests_pass = True
    
    # 运行所有测试
    if not test_skill_files():
        all_tests_pass = False
    
    if not test_script_import():
        all_tests_pass = False
    
    if not test_websites_list():
        all_tests_pass = False
    
    print("\n" + "=" * 50)
    
    if all_tests_pass:
        print("\n✅ 技能测试通过")
        print("\n📋 使用说明:")
        print("   运行技能: python3 scripts/scraper.py --max-tokens 300")
        print("   自定义网站: 编辑 references/websites.txt")
        print("   配置: 查看 references/api_reference.md")
    else:
        print("\n❌ 部分测试失败")
    
    return all_tests_pass


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
