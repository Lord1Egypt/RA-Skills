#!/usr/bin/env python3
"""
投资研究系统 - 用户画像解析模块 v1.0
解析 USER.md 投资偏好，生成个性化分析参数
"""
import os
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class UserProfile:
    """用户投资画像"""
    name: str
    investment_style: str  # 价值投资/成长投资/趋势投资
    risk_preference: str   # 保守/稳健/激进
    holding_period: str    # 短线/中线/长线
    expected_return: float # 期望收益率
    focus_indicators: list # 关注的指标
    max_position: float    # 单票最大仓位
    stop_loss: float       # 止损线
    description: str       # 用户描述


class UserProfileLoader:
    """用户画像加载器"""
    
    DEFAULT_PROFILE = UserProfile(
        name="张权",
        investment_style="价值投资",
        risk_preference="稳健",
        holding_period="长线",
        expected_return=10.0,
        focus_indicators=["ROE", "股息率", "PE", "安全边际"],
        max_position=0.20,
        stop_loss=0.10,
        description="价值投资者，使用 Graham 价值投资协议，追求复利增长"
    )
    
    def __init__(self):
        self.user_md_path = "/root/.openclaw/workspace/USER.md"
    
    def load_profile(self) -> UserProfile:
        """加载用户画像"""
        if not os.path.exists(self.user_md_path):
            print(f"   ⚠️ USER.md 不存在，使用默认画像")
            return self.DEFAULT_PROFILE
        
        try:
            with open(self.user_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_user_md(content)
        except Exception as e:
            print(f"   ⚠️ 读取 USER.md 失败: {e}，使用默认画像")
            return self.DEFAULT_PROFILE
    
    def _parse_user_md(self, content: str) -> UserProfile:
        """解析 USER.md 内容"""
        
        # 提取姓名
        name = "张权"
        name_match = content.find("**姓名**")
        if name_match != -1:
            line_start = content.rfind('\n', 0, name_match) + 1
            line_end = content.find('\n', name_match)
            name_line = content[line_start:line_end]
            if '：' in name_line or ':' in name_line:
                name = name_line.split('：')[-1].split(':')[-1].strip()
        
        # 判断投资风格（从跨界标签和能力栈推断）
        investment_style = "价值投资"
        if "价值投资" in content:
            investment_style = "价值投资"
        elif "成长" in content:
            investment_style = "成长投资"
        elif "趋势" in content or "短线" in content:
            investment_style = "趋势投资"
        
        # 判断风险偏好
        risk_preference = "稳健"
        if "杠铃" in content or "保守" in content:
            risk_preference = "保守"
        elif "激进" in content:
            risk_preference = "激进"
        
        # 判断持仓周期（优先检查长线）
        holding_period = "长线"
        if "长期" in content or "长线" in content or "长期主义" in content:
            holding_period = "长线"
        if "中期" in content or "中线" in content:
            holding_period = "中线"
        if "短期" in content and "短期补丁" not in content:
            holding_period = "短线"
        
        # 从"金融层"推断期望收益率关键词
        expected_return = 10.0  # 默认 10%
        if "复利" in content:
            expected_return = 15.0  # 复利目标通常更高
        if "高收益" in content or "激进" in content:
            expected_return = 20.0
        
        # 关注的指标
        focus_indicators = ["ROE", "股息率", "PE"]
        if "Graham" in content or "格雷厄姆" in content:
            focus_indicators.extend(["安全边际", "净流动资产"])
        if "量化" in content:
            focus_indicators.extend(["动量因子", "质量因子"])
        
        # 最大仓位（基于风险偏好）
        max_position = 0.20
        if risk_preference == "保守":
            max_position = 0.10
        elif risk_preference == "激进":
            max_position = 0.30
        
        # 止损线
        stop_loss = 0.10
        if risk_preference == "保守":
            stop_loss = 0.08
        elif risk_preference == "激进":
            stop_loss = 0.15
        
        # 生成描述
        description = f"{name}，{investment_style}风格，{risk_preference}型投资者，{holding_period}持有，期望收益率{expected_return}%"
        
        return UserProfile(
            name=name,
            investment_style=investment_style,
            risk_preference=risk_preference,
            holding_period=holding_period,
            expected_return=expected_return,
            focus_indicators=focus_indicators,
            max_position=max_position,
            stop_loss=stop_loss,
            description=description
        )


def get_user_profile() -> UserProfile:
    """便捷函数：获取用户画像"""
    loader = UserProfileLoader()
    return loader.load_profile()


if __name__ == "__main__":
    profile = get_user_profile()
    print("=== 用户画像 ===")
    print(f"姓名: {profile.name}")
    print(f"投资风格: {profile.investment_style}")
    print(f"风险偏好: {profile.risk_preference}")
    print(f"持仓周期: {profile.holding_period}")
    print(f"期望收益率: {profile.expected_return}%")
    print(f"关注指标: {', '.join(profile.focus_indicators)}")
    print(f"最大仓位: {profile.max_position*100}%")
    print(f"止损线: {profile.stop_loss*100}%")
    print(f"描述: {profile.description}")