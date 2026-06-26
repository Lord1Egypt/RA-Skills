#!/usr/bin/env python3
"""
M1 数据拉取 — 拉所有TK+IG账号的浏览/播放/点赞/关注/评论
直接输出纯文本，供飞书发送
用法: python3 m1_pull_analytics.py
"""
import json, urllib.request, sys, os
from datetime import datetime, timedelta
from collections import defaultdict

API_BASE = "https://app.metricool.com/api"

# 加载配置
config_file = os.path.join(os.path.dirname(__file__), "..", "config", "metricool.json")
with open(config_file) as f:
    cfg = json.load(f)

TOKEN = cfg["api_token"]
UID = str(cfg["user_id"])
ACCOUNTS = cfg["accounts"]

def api_get(path, timeout=30):
    """GET请求Metricool API"""
    url = f"{API_BASE}{path}"
    headers = {"X-Mc-Auth": TOKEN}
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read())
    except Exception as e:
        print(f"  ⚠️ API error: {e}")
        return {"data": []}

def pull_tiktok_posts(blog_id, from_date, to_date):
    """拉TK帖子级别数据"""
    path = f"/v2/analytics/posts/tiktok?blogId={blog_id}&userId={UID}&from={from_date}&to={to_date}"
    data = api_get(path)
    return data.get("data", [])

def pull_instagram_posts(blog_id, from_date, to_date):
    """拉IG帖子级别数据"""
    path = f"/v2/analytics/posts/instagram?blogId={blog_id}&userId={UID}&from={from_date}&to={to_date}"
    data = api_get(path)
    return data.get("data", [])

def pull_brands():
    """拉所有品牌信息（含followers等）"""
    path = f"/v2/settings/brands?userId={UID}"
    return api_get(path).get("data", [])

def pull_tiktok_account_stats(blog_id):
    """尝试拉TK账号级别统计"""
    # Metricool可能用不同的endpoint
    path = f"/v2/analytics/tiktok/stats?blogId={blog_id}&userId={UID}"
    data = api_get(path)
    return data.get("data", {})

def format_number(n):
    """格式化数字"""
    if n is None:
        return "0"
    if n >= 1000000:
        return f"{n/1000000:.1f}M"
    if n >= 1000:
        return f"{n/1000:.1f}K"
    return str(n)

def main():
    # 日期范围：最近30天
    to_date = datetime.now().strftime("%Y-%m-%dT23:59:59")
    from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00")
    
    print(f"📊 数据拉取时间范围: {from_date[:10]} → {to_date[:10]}")
    print(f"⏰ 拉取时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} (GMT+8)")
    print()
    
    # 先拉brands信息
    print("🔄 拉取品牌列表...")
    brands = pull_brands()
    brand_map = {str(b["id"]): b for b in brands}
    
    all_results = []
    
    for aid in sorted(ACCOUNTS.keys(), key=lambda x: int(x)):
        acc = ACCOUNTS[aid]
        blog_id = str(acc["id"])
        label = acc.get("label", f"he{aid}")
        tiktok_handle = acc.get("tiktok", "")
        ig_handle = acc.get("instagram", "")
        disabled = acc.get("disabled", False)
        ig_blocked = "被封" in acc.get("_ig_status", "")
        
        if disabled:
            continue
        
        brand = brand_map.get(blog_id, {})
        nw = brand.get("networksData", {})
        
        print(f"📱 {label} (TK: @{tiktok_handle}, IG: @{ig_handle or '无'})")
        
        result = {
            "aid": aid,
            "label": label,
            "tiktok_handle": tiktok_handle,
            "ig_handle": ig_handle,
            "ig_blocked": ig_blocked,
        }
        
        # --- TK数据 ---
        try:
            tk_posts = pull_tiktok_posts(blog_id, from_date, to_date)
            if tk_posts:
                total_views = sum(p.get("viewCount", 0) or 0 for p in tk_posts)
                total_likes = sum(p.get("likeCount", 0) or 0 for p in tk_posts)
                total_comments = sum(p.get("commentCount", 0) or 0 for p in tk_posts)
                total_shares = sum(p.get("shareCount", 0) or 0 for p in tk_posts)
                
                result["tk"] = {
                    "post_count": len(tk_posts),
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "total_shares": total_shares,
                    "posts": tk_posts[:10],  # 只保留最近10条用于展示
                }
                print(f"  TK: {len(tk_posts)}条, {format_number(total_views)}播放, {format_number(total_likes)}赞, {format_number(total_comments)}评, {format_number(total_shares)}分享")
            else:
                result["tk"] = {"post_count": 0, "total_views": 0, "total_likes": 0, "total_comments": 0, "total_shares": 0}
                print(f"  TK: 无数据")
        except Exception as e:
            result["tk"] = {"error": str(e)}
            print(f"  TK: ⚠️ {e}")
        
        # --- IG数据 ---
        if ig_handle and not ig_blocked:
            try:
                ig_posts = pull_instagram_posts(blog_id, from_date, to_date)
                if ig_posts:
                    total_views = sum(p.get("viewCount", 0) or 0 for p in ig_posts)
                    total_likes = sum(p.get("likeCount", 0) or 0 for p in ig_posts)
                    total_comments = sum(p.get("commentCount", 0) or 0 for p in ig_posts)
                    
                    result["ig"] = {
                        "post_count": len(ig_posts),
                        "total_views": total_views,
                        "total_likes": total_likes,
                        "total_comments": total_comments,
                    }
                    print(f"  IG: {len(ig_posts)}条, {format_number(total_views)}播放, {format_number(total_likes)}赞, {format_number(total_comments)}评")
                else:
                    result["ig"] = {"post_count": 0, "available": False}
                    print(f"  IG: 无数据 (API未返回)")
            except Exception as e:
                result["ig"] = {"error": str(e)}
                print(f"  IG: ⚠️ {e}")
        elif ig_blocked:
            result["ig"] = {"blocked": True}
            print(f"  IG: ⚠️ 被封")
        else:
            result["ig"] = {"no_handle": True}
        
        all_results.append(result)
        print()
    
    # 保存原始JSON
    output_file = os.path.join(os.path.dirname(__file__), "..", "output", "analytics", "m1_raw_data.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"💾 原始数据已保存: {output_file}")
    print()
    
    # --- 生成飞书文本报告 ---
    report = generate_feishu_report(all_results, from_date, to_date)
    
    # 保存报告文本
    report_file = os.path.join(os.path.dirname(__file__), "..", "output", "analytics", "m1_feishu_report.txt")
    with open(report_file, "w") as f:
        f.write(report)
    print(f"📄 飞书报告已保存: {report_file}")
    
    # 输出到stdout（供pipe到飞书）
    print("\n" + "="*50)
    print(report)
    
    return report

def generate_feishu_report(all_results, from_date, to_date):
    """生成飞书文本报告"""
    lines = []
    lines.append(f"📊 Pandajourneys 全账号数据报告")
    lines.append(f"📅 {from_date[:10]} → {to_date[:10]} (30天)")
    lines.append(f"⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8")
    lines.append("")
    
    # 总体汇总
    total_tk_views = 0
    total_tk_likes = 0
    total_tk_comments = 0
    total_tk_shares = 0
    total_tk_posts = 0
    total_ig_views = 0
    total_ig_likes = 0
    total_ig_comments = 0
    active_accounts = 0
    ig_accounts_with_data = 0
    
    for r in all_results:
        tk = r.get("tk", {})
        if tk.get("post_count", 0) > 0:
            active_accounts += 1
            total_tk_views += tk.get("total_views", 0)
            total_tk_likes += tk.get("total_likes", 0)
            total_tk_comments += tk.get("total_comments", 0)
            total_tk_shares += tk.get("total_shares", 0)
            total_tk_posts += tk.get("post_count", 0)
        
        ig = r.get("ig", {})
        if ig.get("post_count", 0) and ig.get("post_count", 0) > 0:
            total_ig_views += ig.get("total_views", 0)
            total_ig_likes += ig.get("total_likes", 0)
            total_ig_comments += ig.get("total_comments", 0)
            ig_accounts_with_data += 1
    
    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📈 总体汇总 (TikTok)")
    lines.append(f"  活跃账号: {active_accounts}个")
    lines.append(f"  总帖子数: {total_tk_posts}条")
    lines.append(f"  总播放量: {format_number(total_tk_views)}")
    lines.append(f"  总点赞:   {format_number(total_tk_likes)}")
    lines.append(f"  总评论:   {format_number(total_tk_comments)}")
    lines.append(f"  总分享:   {format_number(total_tk_shares)}")
    if total_tk_views > 0:
        engagement = (total_tk_likes + total_tk_comments + total_tk_shares) / total_tk_views * 100
        lines.append(f"  互动率:   {engagement:.2f}%")
    lines.append("")
    
    if ig_accounts_with_data > 0:
        lines.append("📈 总体汇总 (Instagram)")
        lines.append(f"  有数据账号: {ig_accounts_with_data}个")
        lines.append(f"  总播放量: {format_number(total_ig_views)}")
        lines.append(f"  总点赞:   {format_number(total_ig_likes)}")
        lines.append(f"  总评论:   {format_number(total_ig_comments)}")
        lines.append("")
    
    # 各账号详情
    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📱 各账号详情")
    lines.append("")
    
    for r in all_results:
        aid = r["aid"]
        label = r["label"]
        tiktok_handle = r["tiktok_handle"]
        ig_handle = r.get("ig_handle", "")
        
        lines.append(f"━━━ {label} (@{tiktok_handle}) ━━━")
        
        # TK数据
        tk = r.get("tk", {})
        if tk.get("error"):
            lines.append(f"  🔴 TikTok: API错误 - {tk['error']}")
        elif tk.get("post_count", 0) == 0:
            lines.append(f"  🟡 TikTok: 近30天无数据")
        else:
            lines.append(f"  📱 TikTok:")
            lines.append(f"    帖子: {tk['post_count']}条")
            lines.append(f"    播放: {format_number(tk['total_views'])}")
            lines.append(f"    点赞: {format_number(tk['total_likes'])}")
            lines.append(f"    评论: {format_number(tk['total_comments'])}")
            lines.append(f"    分享: {format_number(tk['total_shares'])}")
            if tk['total_views'] > 0:
                eng = (tk['total_likes'] + tk['total_comments'] + tk['total_shares']) / tk['total_views'] * 100
                lines.append(f"    互动率: {eng:.2f}%")
            
            # Top 3 爆款
            posts = tk.get("posts", [])
            if posts:
                sorted_posts = sorted(posts, key=lambda p: p.get("viewCount", 0) or 0, reverse=True)
                lines.append(f"    🏆 Top 3 爆款:")
                for i, p in enumerate(sorted_posts[:3]):
                    views = p.get("viewCount", 0) or 0
                    likes = p.get("likeCount", 0) or 0
                    desc = (p.get("videoDescription", "") or p.get("title", ""))[:50]
                    lines.append(f"      {i+1}. {format_number(views)}播放 {format_number(likes)}赞 | {desc}")
        
        # IG数据
        ig = r.get("ig", {})
        if ig.get("blocked"):
            lines.append(f"  🔴 Instagram: 被封")
        elif ig.get("no_handle"):
            lines.append(f"  ⚪ Instagram: 未连接")
        elif ig.get("available") == False:
            lines.append(f"  🟡 Instagram: API暂未返回数据")
        elif ig.get("error"):
            lines.append(f"  🟡 Instagram: {ig['error']}")
        elif ig.get("post_count", 0) > 0:
            lines.append(f"  📸 Instagram:")
            lines.append(f"    帖子: {ig['post_count']}条")
            lines.append(f"    播放: {format_number(ig['total_views'])}")
            lines.append(f"    点赞: {format_number(ig['total_likes'])}")
            lines.append(f"    评论: {format_number(ig['total_comments'])}")
        else:
            if ig_handle:
                lines.append(f"  🟡 Instagram: 近30天无数据")
        
        lines.append("")
    
    # 账号排名
    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("🏆 TikTok 播放量排名 (Top 10)")
    
    ranked = sorted(
        [r for r in all_results if r.get("tk", {}).get("total_views", 0) > 0],
        key=lambda r: r["tk"]["total_views"],
        reverse=True
    )[:10]
    
    for i, r in enumerate(ranked):
        tk = r["tk"]
        lines.append(f"  {i+1}. {r['label']} @{r['tiktok_handle']} — {format_number(tk['total_views'])}播放 {format_number(tk['total_likes'])}赞")
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📊 数据来源: Metricool API")
    lines.append("⚠️ 注意:")
    lines.append("  • 关注数(followers): Metricool API暂未暴露account-level follower数据")
    lines.append("  • Instagram: API endpoint暂未返回数据，需确认IG Business账号连接状态")
    lines.append("  • 数据延迟: TikTok数据通常有24-48h延迟")
    
    return "\n".join(lines)

if __name__ == "__main__":
    report = main()
