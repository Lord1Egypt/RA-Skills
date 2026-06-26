#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云域名优惠信息检索工具
基于 RAG 从本地知识库检索域名优惠信息
"""

import os
import re
from typing import List, Optional, Dict

class DomainPromotionSearcher:
    """域名优惠信息检索器"""
    
    def __init__(self, knowledge_file: Optional[str] = None):
        """初始化检索器
        
        Args:
            knowledge_file: 知识库文件路径，默认使用 skill 内的知识库
        """
        if knowledge_file is None:
            # 默认使用技能目录下的知识库
            script_dir = os.path.dirname(os.path.abspath(__file__))
            knowledge_file = os.path.join(script_dir, '..', 'knowledge', 'domain_pricing_discounts.md')
        
        self.knowledge_file = os.path.abspath(knowledge_file)
        self.lines = []
        self._load_knowledge()
    
    def _load_knowledge(self):
        """加载知识库文件"""
        if not os.path.exists(self.knowledge_file):
            raise FileNotFoundError(f"知识库文件不存在：{self.knowledge_file}")
        
        with open(self.knowledge_file, 'r', encoding='utf-8') as f:
            self.lines = f.read().split('\n')
    
    def search(self, query: str) -> str:
        """搜索优惠信息
        
        Args:
            query: 搜索查询，如 ".xyz 注册"、".com 批量"、"续费优惠"
        
        Returns:
            搜索结果文本
        """
        query = query.lower().strip()
        
        # 解析查询
        tld = self._extract_tld(query)
        action = self._extract_action(query)
        
        # 根据查询类型搜索
        if tld:
            return self._search_by_tld(tld, action)
        elif '续费' in query or '优惠口令' in query:
            return self._search_renewal_coupons()
        elif '转入' in query or '转移' in query:
            return self._search_transfer()
        elif '多年' in query or '套餐' in query:
            return self._search_multi_year()
        else:
            return self._get_all_promotions()
    
    def _extract_tld(self, query: str) -> Optional[str]:
        """提取域名后缀"""
        # 匹配 .com, .cn, .xyz 等
        match = re.search(r'(\.[a-z]{2,10})', query)
        if match:
            return match.group(1).lower()
        return None
    
    def _extract_action(self, query: str) -> Optional[str]:
        """提取操作类型"""
        if any(kw in query for kw in ['注册', '新注册']):
            return '注册'
        elif any(kw in query for kw in ['续费', '续期']):
            return '续费'
        elif any(kw in query for kw in ['转入', 'transfer', '转入日']):
            return '转入'
        elif any(kw in query for kw in ['批量', '多个', '个以上', '批发']):
            return '批量'
        elif any(kw in query for kw in ['多年', '年套餐', '10 年', '5 年', '3 年']):
            return '多年'
        return None
    
    def _search_by_tld(self, tld: str, action: Optional[str]) -> str:
        """根据域名后缀搜索"""
        tld_lower = tld.lower()
        results = []
        
        # 搜索注册价格
        if not action or action == '注册':
            reg_result = self._find_in_table(tld_lower, '域名注册活动价格', '普通域名注册优惠')
            if reg_result:
                results.append(f"### 📝 {tld} 注册优惠\n{reg_result}")
        
        # 搜索批量价格
        if not action or action == '批量':
            bulk_result = self._find_bulk_price(tld_lower)
            if bulk_result:
                results.append(f"### 📦 {tld} 批量优惠\n{bulk_result}")
        
        # 搜索续费价格
        if not action or action == '续费':
            renew_result = self._find_renewal_price(tld_lower)
            if renew_result:
                results.append(f"### 💰 {tld} 续费优惠\n{renew_result}")
        
        # 搜索转入价格
        if not action or action == '转入':
            transfer_result = self._find_transfer_price(tld_lower)
            if transfer_result:
                results.append(f"### 🔄 {tld} 转入优惠\n{transfer_result}")
        
        if not results:
            return self._get_fallback_message(tld)
        
        return self._format_results(tld, results)
    
    def _find_in_table(self, keyword: str, section_title: str, subsection_title: Optional[str] = None) -> str:
        """在指定章节的表格中查找包含关键词的行"""
        in_section = False
        in_subsection = False
        result_lines = []
        
        for line in self.lines:
            # 检查是否进入目标章节
            if line.startswith('##') and section_title in line:
                in_section = True
                in_subsection = not subsection_title
                continue
            
            # 检查是否进入子章节
            if in_section and subsection_title and line.startswith('###') and subsection_title in line:
                in_subsection = True
                continue
            
            # 检查是否离开章节
            if in_section and line.startswith('##'):
                break
            
            # 在目标子章节中查找
            if in_subsection and '|' in line:
                if keyword in line.lower():
                    result_lines.append(line)
        
        if result_lines:
            header = "| 域名后缀 | 注册原价格 | 3 月活动价格 | 活动时间 |"
            return header + "\n" + "\n".join(result_lines[:5])
        
        return ""
    
    def _find_bulk_price(self, tld: str) -> str:
        """查找批量价格"""
        in_section = False
        in_target = False
        result_lines = []
        header_line = ""
        
        for line in self.lines:
            # 检查是否进入批量政策章节
            if '域名注册批量政策' in line and line.startswith('##'):
                in_section = True
                continue
            
            if in_section:
                # 检查是否离开章节（仅当遇到新的一级章节##，而不是子章节###）
                if line.startswith('##') and not line.startswith('###') and '域名注册批量政策' not in line:
                    break
                
                # 检查是否进入目标域名部分
                if line.startswith('###') and tld in line.lower():
                    in_target = True
                    header_line = line
                    result_lines = []
                    continue
                
                # 如果离开目标部分
                if in_target and line.startswith('###'):
                    break
                
                # 收集表格行
                if in_target and '|' in line:
                    result_lines.append(line)
        
        if result_lines:
            return header_line + "\n" + "\n".join(result_lines)
        
        return ""
    
    def _find_renewal_price(self, tld: str) -> str:
        """查找续费价格"""
        in_section = False
        result_lines = []
        
        for line in self.lines:
            if '.com 和.cn 域名续费优惠' in line and line.startswith('##'):
                in_section = True
                continue
            
            if in_section and line.startswith('##'):
                break
            
            if in_section and '|' in line and tld in line.lower():
                result_lines.append(line)
        
        if result_lines:
            return "\n".join(result_lines)
        
        return ""
    
    def _find_transfer_price(self, tld: str) -> str:
        """查找转入价格"""
        in_section = False
        result_lines = []
        
        for line in self.lines:
            if '周三转入日' in line and line.startswith('##'):
                in_section = True
                continue
            
            if in_section and line.startswith('##'):
                break
            
            if in_section and '|' in line and tld in line.lower():
                result_lines.append(line)
        
        if result_lines:
            return "\n".join(result_lines)
        
        return ""
    
    def _search_renewal_coupons(self) -> str:
        """搜索续费优惠口令"""
        in_section = False
        result_lines = []
        
        for line in self.lines:
            if '续费优惠口令' in line and line.startswith('##'):
                in_section = True
                continue
            
            if in_section and line.startswith('##'):
                break
            
            if in_section and '|' in line:
                result_lines.append(line)
        
        if result_lines:
            return "\n".join(result_lines)
        
        return "😕 未找到相关信息"
    
    def _search_transfer(self) -> str:
        """搜索转入优惠"""
        in_section = False
        result_lines = []
        header = ""
        
        for line in self.lines:
            if '周三转入日' in line:
                in_section = True
                header = line
                continue
            
            if in_section and line.startswith('##'):
                break
            
            if in_section:
                result_lines.append(line)
        
        if result_lines:
            return "\n".join([header] + result_lines)
        
        return "😕 未找到转入优惠信息"
    
    def _search_multi_year(self) -> str:
        """搜索多年套餐"""
        in_section = False
        result_lines = []
        
        for line in self.lines:
            if '多年注册优惠详情' in line:
                in_section = True
                continue
            
            if in_section and line.startswith('##'):
                break
            
            if in_section:
                result_lines.append(line)
        
        if result_lines:
            return "\n".join(result_lines)
        
        return "😕 未找到多年套餐信息"
    
    def _get_all_promotions(self) -> str:
        """获取所有优惠信息摘要"""
        summary = ["# 🎁 阿里云域名优惠活动汇总（2026 年 3 月）\n"]
        
        sections = ['一、3 月域名注册活动价格', '二、3 月域名注册批量政策', 
                   '三、周三转入日', '四、.com 和.cn 域名续费优惠', '五、续费优惠口令']
        
        for section in sections:
            section_content = self._extract_section(section)
            if section_content:
                summary.append(section_content)
        
        return "\n\n".join(summary)
    
    def _extract_section(self, section_title: str) -> str:
        """提取指定章节内容"""
        in_section = False
        result_lines = []
        
        for line in self.lines:
            if section_title in line and line.startswith('##'):
                in_section = True
                result_lines.append(line)
                continue
            
            if in_section:
                if line.startswith('##'):
                    break
                result_lines.append(line)
        
        if result_lines:
            return "\n".join(result_lines[:50])
        
        return "😕 未找到相关信息"
    
    def _get_fallback_message(self, tld: str) -> str:
        """返回默认提示信息"""
        fallback = f"😕 暂未找到 **{tld}** 域名的特惠活动信息\n\n"
        fallback += "🔥 **3 月热门优惠域名推荐**:\n\n"
        fallback += "| 域名后缀 | 首年价格 | 推荐理由 |\n"
        fallback += "|:---|:---|:---|\n"
        fallback += "| .xyz | **¥7** | 最便宜，适合个人博客 |\n"
        fallback += "| .icu | **¥7** | 短小好记，10 年¥298 |\n"
        fallback += "| .cyou | **¥8** | 谐音 see you，10 年¥298 |\n"
        fallback += "| .cloud | **¥7** | 科技云计算相关 |\n"
        fallback += "| .top | **¥9** | 通用性强，批量¥9/个 |\n"
        fallback += "| .com | **¥85** | 最经典，批量 5 个+¥82/个 |\n"
        fallback += "| .cn | **¥38** | 国内首选，批量 5 个+¥35/个 |\n\n"
        return fallback
    
    def _format_results(self, tld: str, results: List[str]) -> str:
        """格式化搜索结果"""
        header = f"🔍 查询：**{tld}** 域名优惠信息\n\n"
        
        footer = "\n\n---\n"
        footer += "💡 **提示**: \n"
        footer += "- 以上价格为活动价格，具体以阿里云官网实际下单为准\n"
        footer += "- 📅 **活动时间**: 部分活动截止 2026 年 3 月 31 日，请尽快下单\n"
        footer += "- 🔗 **官网**: https://wanwang.aliyun.com/\n"
        
        return header + "\n".join(results) + footer


def main():
    """主函数 - 测试用"""
    print("=" * 80)
    print("🦐 阿里云域名优惠信息检索测试")
    print("=" * 80)
    
    searcher = DomainPromotionSearcher()
    
    test_queries = [
        '.xyz 注册',
        '.com 注册',
        '.cn 批量',
        '续费优惠',
        '周三转入日',
        '多年套餐',
    ]
    
    for query in test_queries:
        print(f"\n❓ 查询：{query}")
        print("-" * 80)
        result = searcher.search(query)
        print(result[:1500])
        print()


if __name__ == '__main__':
    main()
