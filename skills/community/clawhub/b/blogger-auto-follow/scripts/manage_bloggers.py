#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全行业博主资产管理与动态检索工具 (Blogger Manager & Industry Updates Tool)
- 支持全行业一级大类 (科技/商业/设计/影视/职场/科普/生活等) 与二级子分类
- 查看/筛选全行业归档博主
- 增量添加新博主 (支持行业大类自动推断或指定)
- 删除指定博主
- 在本地默认浏览器中一键打开指定行业/分类的主页链接检索最新动态
- 自动同步更新全行业分区的 Markdown 导航手册
"""

import os
import sys
import argparse
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage import BloggerDB, get_all_industries


def main():
    parser = argparse.ArgumentParser(description="全行业博主资产管理与动态检索工具")
    parser.add_argument("-l", "--list", action="store_true",
                        help="列出当前所有已归档博主")
    parser.add_argument("-i", "--industry", type=str, default="",
                        help="按行业大类筛选 (例如: 科技 · 数码 · 编程、商业 · 财经 · 创业、设计 · 视觉 · 创意)")
    parser.add_argument("-c", "--category", type=str, default="",
                        help="按二级细分子分类筛选 (例如: 教程实测、AIGC 故事、商业认知)")
    parser.add_argument("-p", "--platform", type=str, default="",
                        help="按平台筛选 (douyin | xiaohongshu | bilibili | x | youtube)")
    parser.add_argument("--industries", action="store_true",
                        help="列出所有支持的业界大类与当前归档统计")
    parser.add_argument("-a", "--add", type=str, default="",
                        help="手动增量添加博主名称")
    parser.add_argument("--url", type=str, default="",
                        help="添加博主时的个人主页直达链接")
    parser.add_argument("--fans", type=str, default="",
                        help="添加博主时的粉丝量")
    parser.add_argument("-d", "--delete", type=str, default="",
                        help="删除指定博主 (支持博主名称或 ID 序号)")
    parser.add_argument("-o", "--open", action="store_true",
                        help="在本地浏览器中批量打开指定行业或分类下的所有博主主页")
    parser.add_argument("-e", "--export", action="store_true",
                        help="重新生成/刷新 data/FOLLOWED_BLOGGERS.md 导航文件")

    args = parser.parse_args()
    db = BloggerDB()

    # 1. 查看行业大类汇总与统计
    if args.industries:
        stats = db.get_industry_stats()
        all_def = get_all_industries()
        print("=" * 75)
        print("🏢 全行业分类体系与本地归档统计")
        print("=" * 75)
        for item in all_def:
            name = item["name"]
            icon = item["icon"]
            stat = stats.get(name, {"count": 0, "categories": {}})
            cnt = stat["count"]
            print(f"\n{icon} 【{name}】 (已归档: {cnt} 位)")
            print(f"   📂 标准细分子类参考: {', '.join(item['subcategories'])}")
            if stat["categories"]:
                active_subs = [f"{k}({v})" for k, v in stat["categories"].items()]
                print(f"   📊 当前已有分布: {', '.join(active_subs)}")
        print("\n" + "=" * 75)
        return

    # 2. 删除博主
    if args.delete:
        target = args.delete.strip()
        deleted = db.delete_blogger(target)
        if deleted:
            print(f"✅ 成功从本地数据库中删除博主: 【{deleted.get('name')}】 (行业: {deleted.get('industry', '未分类')} | 原序号: {deleted.get('id')})")
            print(f"📄 已同步刷新: data/FOLLOWED_BLOGGERS.md")
        else:
            print(f"❌ 未找到匹配的博主: '{target}'，请确认名称或 ID 是否正确。")
        return

    # 3. 增量手动添加博主
    if args.add:
        name = args.add.strip()
        plat = args.platform if args.platform else "douyin"
        cat = args.category if args.category else "默认"
        ind = args.industry if args.industry else ""
        record = {
            "name": name,
            "industry": ind,
            "category": cat,
            "platform": plat,
            "profile_url": args.url.strip(),
            "fans": args.fans.strip(),
            "status": "FOLLOWED"
        }
        res = db.upsert_blogger(record)
        print(f"✅ 成功增量录入博主: 【{name}】 (行业: {res.get('industry')} | 子类: {cat} | 平台: {plat})")
        print(f"📄 已同步刷新: data/FOLLOWED_BLOGGERS.md")
        return

    # 4. 重新导出 Markdown
    if args.export:
        db.export_markdown()
        print(f"✅ 已成功刷新全行业导航: data/FOLLOWED_BLOGGERS.md")
        return

    # 5. 在浏览器中打开主页链接 (检索最新动态)
    if args.open:
        bloggers = db.list_bloggers(industry=args.industry if args.industry else None,
                                   category=args.category if args.category else None,
                                   platform=args.platform if args.platform else None)
        valid_urls = []
        for b in bloggers:
            url = b.get("profile_url", "")
            if url and url.startswith("http"):
                valid_urls.append((b.get("name"), url))

        if not valid_urls:
            print(f"⚠️ 未找到包含有效主页链接的博主。")
            return

        print(f"🌐 正在本地浏览器中打开 {len(valid_urls)} 位博主的主页以检索最新动态...")
        for name, url in valid_urls:
            print(f"   👉 正在打开: 【{name}】 -> {url}")
            webbrowser.open(url)
        return

    # 默认或 --list: 列出博主
    bloggers = db.list_bloggers(industry=args.industry if args.industry else None,
                               category=args.category if args.category else None,
                               platform=args.platform if args.platform else None)

    print("=" * 85)
    print(f"📋 本地已归档博主资产库 (共 {len(bloggers)} 位)")
    if args.industry:
        print(f"   🏢 筛选行业大类: {args.industry}")
    if args.category:
        print(f"   📂 筛选细分子类: {args.category}")
    if args.platform:
        print(f"   🌐 筛选平台: {args.platform}")
    print("=" * 85)

    if not bloggers:
        print("💡 当前条件下暂无匹配博主数据。")
        return

    print(f"{'ID':<4} | {'博主名称':<18} | {'行业大类':<18} | {'子分类':<12} | {'粉丝':<8} | {'主页直达链接'}")
    print("-" * 85)
    for b in bloggers:
        b_id = b.get("id", "-")
        name = b.get("name", "")
        ind = b.get("industry", "-")
        cat = b.get("category", "-")
        fans = b.get("fans", "-")
        url = b.get("profile_url", "暂无主页")
        print(f"{b_id:<4} | {name:<18} | {ind:<18} | {cat:<12} | {fans:<8} | {url}")

    print("-" * 85)
    print("💡 常用管理命令示例:")
    print("   👉 查看行业分布: python3 scripts/manage_bloggers.py --industries")
    print("   👉 筛选商业博主: python3 scripts/manage_bloggers.py -i 商业")
    print("   👉 打开行业动态: python3 scripts/manage_bloggers.py -o -i 科技")
    print("   👉 增量添加博主: python3 scripts/manage_bloggers.py -a 新博主名 -i '商业 · 财经 · 创业' -c '商业认知'")
    print("   👉 删除指定博主: python3 scripts/manage_bloggers.py -d 博主名 (或 ID)")


if __name__ == "__main__":
    main()
