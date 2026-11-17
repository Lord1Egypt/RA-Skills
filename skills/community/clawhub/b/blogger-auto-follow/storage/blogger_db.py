# -*- coding: utf-8 -*-
"""
博主资产本地持久化数据库 (BloggerDB - 全行业两级分类增强版)
- 支持全行业一级大类 (Industry) 与二级细分子类 (Category)
- 支持智能行业推断 (infer_industry)
- 支持增量添加/更新 (Upsert)
- 支持按名称/ID 删除博主 (Delete)
- 自动同步生成按全行业分类结构化排版的 FOLLOWED_BLOGGERS.md 导航手册
"""

import os
import json
import time
from typing import List, Dict, Optional
from .industry_categories import infer_industry, INDUSTRY_DEFINITIONS


class BloggerDB:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(root_dir, "data")
        else:
            self.data_dir = data_dir

        os.makedirs(self.data_dir, exist_ok=True)
        self.json_file = os.path.join(self.data_dir, "followed_bloggers.json")
        self.md_file = os.path.join(self.data_dir, "FOLLOWED_BLOGGERS.md")
        self._data: List[Dict] = []
        self.load()

    def load(self) -> List[Dict]:
        """读取本地博主数据并确保行业分类字段完整"""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                    # 补全可能缺失的 industry 字段
                    for b in self._data:
                        if not b.get("industry") or b.get("industry") == "默认":
                            b["industry"] = infer_industry(
                                b.get("name", ""),
                                b.get("category", ""),
                                b.get("bio", "")
                            )
            except Exception as e:
                print(f"⚠️ 读取数据库失败: {e}，将初始化为空数据。")
                self._data = []
        else:
            self._data = []
        return self._data

    def get_all(self) -> List[Dict]:
        """获取所有已归档博主列表"""
        return self._data

    def save(self):
        """保存数据到 JSON 并同步生成 Markdown 导航"""
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
        self.export_markdown()

    def upsert_blogger(self, blogger_info: Dict) -> Dict:
        """
        增量添加或更新博主信息
        支持行业大类 (industry) 与子分类 (category)
        """
        name = blogger_info.get("name", "").strip()
        if not name:
            raise ValueError("博主名称不能为空")

        now_str = time.strftime("%Y-%m-%d %H:%M:%S")
        platform = blogger_info.get("platform", "unknown")
        profile_url = blogger_info.get("profile_url", "")
        unique_id = blogger_info.get("unique_id", "")
        category = blogger_info.get("category", "默认")
        fans = blogger_info.get("fans", "")
        bio = blogger_info.get("bio", "")
        status = blogger_info.get("status", "FOLLOWED")

        # 智能确定一级行业大类
        industry = blogger_info.get("industry", "")
        if not industry or industry == "默认":
            industry = infer_industry(name, category, bio)

        # 查找是否已存在同名博主
        existing = None
        for item in self._data:
            if item.get("name", "").strip().lower() == name.lower():
                existing = item
                break

        if existing:
            # 增量更新已有博主
            existing["industry"] = industry
            if category and category != "默认":
                existing["category"] = category
            if fans:
                existing["fans"] = fans
            if bio:
                existing["bio"] = bio
            existing["last_checked_at"] = now_str
            existing["follow_status"] = status

            # 合并平台与主页信息
            if "platforms" not in existing or not isinstance(existing["platforms"], dict):
                existing["platforms"] = {}

            existing["platforms"][platform] = {
                "profile_url": profile_url,
                "unique_id": unique_id,
                "status": status,
                "updated_at": now_str
            }
            if profile_url:
                existing["profile_url"] = profile_url
                existing["primary_platform"] = platform

            self.save()
            return existing
        else:
            # 新增博主
            new_id = len(self._data) + 1
            new_record = {
                "id": new_id,
                "name": name,
                "industry": industry,
                "category": category,
                "fans": fans,
                "bio": bio,
                "primary_platform": platform,
                "profile_url": profile_url,
                "follow_status": status,
                "followed_at": now_str,
                "last_checked_at": now_str,
                "platforms": {
                    platform: {
                        "profile_url": profile_url,
                        "unique_id": unique_id,
                        "status": status,
                        "updated_at": now_str
                    }
                }
            }
            self._data.append(new_record)
            self.save()
            return new_record

    def delete_blogger(self, name_or_id: str) -> Optional[Dict]:
        """
        删除指定博主（支持按 ID 或按博主名称匹配）
        """
        target_index = -1
        matched_item = None

        if str(name_or_id).isdigit():
            target_id = int(name_or_id)
            for i, item in enumerate(self._data):
                if item.get("id") == target_id:
                    target_index = i
                    matched_item = item
                    break

        if target_index == -1:
            name_str = str(name_or_id).strip().lower()
            for i, item in enumerate(self._data):
                if item.get("name", "").strip().lower() == name_str:
                    target_index = i
                    matched_item = item
                    break

        if target_index != -1 and matched_item:
            self._data.pop(target_index)
            for idx, item in enumerate(self._data, 1):
                item["id"] = idx
            self.save()
            return matched_item

        return None

    def list_bloggers(self, industry: Optional[str] = None, category: Optional[str] = None, platform: Optional[str] = None) -> List[Dict]:
        """按行业大类、子分类或平台过滤博主列表"""
        results = self._data
        if industry:
            results = [b for b in results if industry.lower() in b.get("industry", "").lower()]
        if category:
            results = [b for b in results if category.lower() in b.get("category", "").lower()]
        if platform:
            results = [b for b in results if platform in b.get("platforms", {}) or b.get("primary_platform") == platform]
        return results

    def get_industry_stats(self) -> Dict[str, Dict]:
        """获取全行业大类统计数据"""
        stats = {}
        for ind_name, config in INDUSTRY_DEFINITIONS.items():
            stats[ind_name] = {
                "icon": config["icon"],
                "count": 0,
                "categories": {}
            }

        for b in self._data:
            ind = b.get("industry", "综合 · 其他")
            if ind not in stats:
                stats[ind] = {"icon": "🌐", "count": 0, "categories": {}}
            stats[ind]["count"] += 1
            cat = b.get("category", "默认")
            stats[ind]["categories"][cat] = stats[ind]["categories"].get(cat, 0) + 1

        return stats

    def export_markdown(self):
        """生成按全行业两级结构排版的 Markdown 资产导航手册"""
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")
        total_count = len(self._data)

        # 按行业大类分组
        industry_groups: Dict[str, List[Dict]] = {}
        for b in self._data:
            ind = b.get("industry", "综合 · 其他")
            industry_groups.setdefault(ind, []).append(b)

        active_industries_count = len(industry_groups)

        md_lines = [
            "# 🌟 全行业已关注博主资产库与主页直达导航",
            "",
            f"> 📅 **更新时间**：`{now_str}` ｜ 👥 **累计归档博主**：**{total_count} 位** ｜ 🏢 **覆盖行业**：**{active_industries_count} 个**",
            "",
            "本资产库支持跨平台（抖音/小红书/B站/X/YouTube）全行业博主收录，支持直接点击链接直达博主主页，追踪最新动态与行业灵感。",
            "",
            "---",
            "",
            "## 📌 全行业快速索引导航",
            ""
        ]

        # 顶部行业目录
        for ind_name, items in industry_groups.items():
            icon = INDUSTRY_DEFINITIONS.get(ind_name, {}).get("icon", "📁")
            anchor = ind_name.lower().replace(" · ", "-").replace(" ", "").replace("/", "")
            md_lines.append(f"- {icon} [{ind_name} ({len(items)}位)](#{anchor})")

        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

        # 遍历各行业大类输出
        for ind_name, items in industry_groups.items():
            icon = INDUSTRY_DEFINITIONS.get(ind_name, {}).get("icon", "📁")
            md_lines.append(f"## {icon} {ind_name} (共 {len(items)} 位)")
            md_lines.append("")

            # 行业内部按二级子分类再分组展示
            sub_groups = {}
            for b in items:
                cat = b.get("category", "默认")
                sub_groups.setdefault(cat, []).append(b)

            for cat_name, cat_items in sub_groups.items():
                md_lines.append(f"### 📂 细分子类：{cat_name} ({len(cat_items)}位)")
                md_lines.append("")
                md_lines.append("| 序号 | 博主名称 | 粉丝量 | 主平台 | 主页直达链接 | 关注时间 | 状态 |")
                md_lines.append("| :---: | :--- | :---: | :---: | :--- | :---: | :---: |")

                for b in cat_items:
                    b_id = b.get("id", "-")
                    name = b.get("name", "")
                    fans = b.get("fans", "-")
                    primary_plat = b.get("primary_platform", "douyin")
                    prof_url = b.get("profile_url", "")
                    followed_at = b.get("followed_at", "-")
                    status = b.get("follow_status", "FOLLOWED")
                    status_tag = "✅ 已关注" if status in ["SUCCESS", "FOLLOWED", "ALREADY_FOLLOWED"] else "⚠️ 待核验"

                    plat_tag = {
                        "douyin": "抖音",
                        "bilibili": "B站",
                        "xiaohongshu": "小红书",
                        "x": "X (Twitter)",
                        "youtube": "YouTube"
                    }.get(primary_plat, primary_plat)

                    if prof_url:
                        url_display = f"[{plat_tag}主页]({prof_url})"
                    else:
                        url_display = f"*{plat_tag} (待检索)*"

                    md_lines.append(f"| {b_id} | **{name}** | {fans} | `{plat_tag}` | {url_display} | {followed_at} | {status_tag} |")

                md_lines.append("")

            md_lines.append("---")
            md_lines.append("")

        md_lines.append("💡 **动态追踪提示**：使用 `python3 scripts/manage_bloggers.py --open --industry <行业名>` 可以在本地浏览器中一键打开该行业所有博主主页！")

        with open(self.md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines) + "\n")
