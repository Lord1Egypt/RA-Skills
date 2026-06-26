#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 Anima-AIOS Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Anima AIOS v6.2.4 - 团队排行榜生成器

自动扫描全员认知画像，生成团队排行榜。
支持按 EXP、等级、五维认知分数排名。

Author: 清禾
Date: 2026-03-26
Version: 6.2.4
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class TeamRankingGenerator:
    """团队排行榜生成器"""
    
    def __init__(self, facts_base: str = "/home/画像"):
        self.facts_base = Path(facts_base)
        self.shared_dir = self.facts_base / "shared"
        self.shared_dir.mkdir(parents=True, exist_ok=True)
    
    def scan_all_agents(self) -> List[Dict]:
        """扫描所有 Agent 的认知画像"""
        agents = []
        
        for agent_dir in self.facts_base.iterdir():
            if not agent_dir.is_dir():
                continue
            
            # 跳过特殊目录
            if agent_dir.name in ["shared", ".backup", ".trash"]:
                continue
            
            # 读取认知画像
            profile_file = agent_dir / "cognitive_profile.json"
            if not profile_file.exists():
                continue
            
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                
                agents.append({
                    "name": agent_dir.name,
                    "level": profile.get("level", 0),
                    "exp": profile.get("exp", 0),
                    "cognitive_score": profile.get("cognitive_score", 0),
                    "dimensions": profile.get("dimensions", {}),
                    "updated_at": profile.get("updated_at", "")
                })
            except Exception as e:
                print(f"读取 {agent_dir.name} 失败：{e}")
        
        return agents
    
    def generate_rankings(self, agents: List[Dict]) -> Dict[str, List[Dict]]:
        """生成各类排行榜"""
        rankings = {}
        
        # EXP 排行榜
        rankings["exp"] = sorted(
            agents,
            key=lambda x: x["exp"],
            reverse=True
        )
        
        # 等级排行榜
        rankings["level"] = sorted(
            agents,
            key=lambda x: x["level"],
            reverse=True
        )
        
        # 认知分数排行榜
        rankings["cognitive_score"] = sorted(
            agents,
            key=lambda x: x["cognitive_score"],
            reverse=True
        )
        
        # 五维认知排行榜
        dimensions = ["understanding", "application", "creation", "metacognition", "collaboration"]
        for dim in dimensions:
            rankings[f"dimension_{dim}"] = sorted(
                [a for a in agents if dim in a.get("dimensions", {})],
                key=lambda x: x["dimensions"].get(dim, {}).get("score", 0),
                reverse=True
            )
        
        return rankings
    
    def generate_markdown(self, rankings: Dict[str, List[Dict]], date: str) -> str:
        """生成 Markdown 格式排行榜"""
        md = f"""# 团队认知排行榜

**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**统计日期：** {date}
**Agent 总数：** {self._count_agents(rankings)}

---

## 🏆 EXP 排行榜

| 排名 | Agent | EXP | 等级 | 认知分数 |
|------|-------|-----|------|----------|
"""
        for i, agent in enumerate(rankings["exp"][:10], 1):
            md += f"| {i} | {agent['name']} | {agent['exp']:.1f} | Lv.{agent['level']} | {agent['cognitive_score']:.1f} |\n"
        
        md += f"""
## 🎯 等级排行榜

| 排名 | Agent | 等级 | EXP | 认知分数 |
|------|-------|------|-----|----------|
"""
        for i, agent in enumerate(rankings["level"][:10], 1):
            md += f"| {i} | {agent['name']} | Lv.{agent['level']} | {agent['exp']:.1f} | {agent['cognitive_score']:.1f} |\n"
        
        md += f"""
## 🧠 认知分数排行榜

| 排名 | Agent | 认知分数 | 等级 | EXP |
|------|-------|----------|------|-----|
"""
        for i, agent in enumerate(rankings["cognitive_score"][:10], 1):
            md += f"| {i} | {agent['name']} | {agent['cognitive_score']:.1f} | Lv.{agent['level']} | {agent['exp']:.1f} |\n"
        
        # 五维认知排行榜
        dimensions_cn = {
            "understanding": "知识内化",
            "application": "知识应用",
            "creation": "知识创造",
            "metacognition": "元认知",
            "collaboration": "协作认知"
        }
        
        for dim, dim_cn in dimensions_cn.items():
            md += f"""
## 📊 {dim_cn}排行榜

| 排名 | Agent | 分数 |
|------|-------|------|
"""
            for i, agent in enumerate(rankings[f"dimension_{dim}"][:10], 1):
                score = agent["dimensions"].get(dim, {}).get("score", 0)
                md += f"| {i} | {agent['name']} | {score:.1f} |\n"
        
        md += f"""
---

_生成工具：Anima AIOS v6.2.4_
_架构只能演进，不能退化。—— 立文铁律_
"""
        return md
    
    def _count_agents(self, rankings: Dict[str, List[Dict]]) -> int:
        """统计 Agent 总数"""
        return len(rankings.get("exp", []))
    
    def save_rankings(self, rankings: Dict[str, List[Dict]], date: Optional[str] = None) -> str:
        """保存排行榜到文件"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 生成 Markdown
        md_content = self.generate_markdown(rankings, date)
        
        # 保存 Markdown 文件
        md_file = self.shared_dir / f"团队排行榜_{date}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # 保存 JSON 文件
        json_file = self.shared_dir / f"团队排行榜_{date}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "date": date,
                "generated_at": datetime.now().isoformat(),
                "rankings": rankings
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 排行榜已生成：{md_file}")
        print(f"✅ 排行榜已生成：{json_file}")
        
        return str(md_file)
    
    def run(self, date: Optional[str] = None) -> str:
        """运行排行榜生成"""
        print("🔍 开始扫描全员认知画像...")
        agents = self.scan_all_agents()
        print(f"✅ 扫描完成，共 {len(agents)} 个 Agent")
        
        print("📊 生成排行榜...")
        rankings = self.generate_rankings(agents)
        print(f"✅ 生成 {len(rankings)} 个排行榜")
        
        print("💾 保存排行榜...")
        md_file = self.save_rankings(rankings, date)
        print(f"✅ 排行榜生成完成")
        
        return md_file


def main():
    """命令行入口"""
    import sys
    
    date = None
    if len(sys.argv) > 1:
        date = sys.argv[1]
    
    generator = TeamRankingGenerator()
    generator.run(date)


if __name__ == "__main__":
    main()
