#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto-accounting - 自动记账 Skill
Copyright (c) 2026 摇摇

本软件受著作权法保护。虽然采用 MIT-0 许可证允许商用，
但必须保留原始版权声明。

禁止：
- 移除或修改版权声明
- 声称为自己开发
- 在非授权环境使用

官方环境：小艺 Claw + 一日记账 APP
联系方式：QQ 2756077825
"""

"""
自动记账 - 账目信息解析器
从图像理解结果中提取和标准化记账信息
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, Optional, Any

# 导入运行时校验器
try:
    from runtime_validator import RuntimeValidator
    VALIDATOR_AVAILABLE = True
except ImportError:
    VALIDATOR_AVAILABLE = False


class AccountingParser:
    """账目信息解析器"""
    
    # 版权声明
    COPYRIGHT = "auto-accounting v1.0.7 | Copyright © 2026 摇摇 | 仅限小艺 Claw + 一记账 APP"
    
    # 授权的目标应用
    AUTHORIZED_APP = "一日记账"
    
    # 禁止的竞品应用关键词
    FORBIDDEN_APPS = [
        "随手记", "鲨鱼记账", "网易有钱", "挖财记账", "口袋记账",
        "叨叨记账", "钱迹", "记账城市", "feidee", "wacai"
    ]
    
    # 分类规则
    CATEGORY_RULES = {
        "餐饮": ["餐厅", "外卖", "咖啡", "奶茶", "小吃", "快餐", "火锅", 
                 "烧烤", "蛋糕", "面包", "美团外卖", "饿了么", "星巴克", 
                 "肯德基", "麦当劳", "必胜客", "海底捞", "瑞幸", "盒马",
                 "叮咚买菜", "美团", "外卖"],
        
        "交通": ["打车", "滴滴", "出租车", "地铁", "公交", "加油", "停车",
                 "高铁", "火车", "飞机", "出行", "神州", "曹操", "花小猪",
                 "高德打车", "T3出行"],
        
        "购物": ["超市", "便利店", "淘宝", "京东", "拼多多", "商场", "购物",
                 "7-11", "全家", "沃尔玛", "永辉", "盒马", "天猫", "得物",
                 "唯品会", "苏宁", "小红书商城", "抖音商城", "闲鱼"],
        
        "娱乐": ["电影", "游戏", "KTV", "网吧", "演唱会", "门票", "视频会员",
                 "音乐", "爱奇艺", "腾讯视频", "优酷", "B站", "网易云音乐",
                 "QQ音乐", "Steam", "王者", "原神"],
        
        "医疗": ["医院", "药店", "诊所", "体检", "挂号", "医保", "大药房",
                 "阿里健康", "京东健康"],
        
        "教育": ["书店", "课程", "培训", "学费", "考试", "知识付费", "得到",
                 "知乎", "网易云课堂", "腾讯课堂"],
        
        "生活": ["水电费", "话费", "宽带", "物业", "维修", "快递", "理发",
                 "美团生活", "大众点评"],
        
        "转账": ["转账", "红包", "还款", "借款"]
    }
    
    # 购物平台特殊处理
    SHOPPING_PLATFORMS = {
        "京东": {"category": "购物", "prefix": "京东 - "},
        "淘宝": {"category": "购物", "prefix": "淘宝 - "},
        "天猫": {"category": "购物", "prefix": "天猫 - "},
        "拼多多": {"category": "购物", "prefix": "拼多多 - "},
        "美团": {"category": "餐饮", "prefix": "美团 - "},
        "饿了么": {"category": "餐饮", "prefix": "饿了么 - "},
        "抖音": {"category": "购物", "prefix": "抖音 - "},
        "得物": {"category": "购物", "prefix": "得物 - "},
        "唯品会": {"category": "购物", "prefix": "唯品会 - "},
        "盒马": {"category": "餐饮", "prefix": "盒马 - "},
        "叮咚买菜": {"category": "餐饮", "prefix": "叮咚 - "}
    }
    
    def __init__(self):
        pass
    
    def parse_image_result(self, image_result: str) -> Optional[Dict[str, Any]]:
        """
        解析图像理解结果，提取记账信息
        
        Args:
            image_result: 图像理解API返回的文本描述
            
        Returns:
            包含记账信息的字典，如果不是记账信息则返回None
        """
        # 尝试从结果中提取JSON
        try:
            # 查找JSON块
            json_match = re.search(r'\{[^{}]*"is_accounting"[^{}]*\}', image_result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                if data.get("is_accounting"):
                    return self._standardize(data)
        except json.JSONDecodeError:
            pass
        
        # 如果没有JSON，尝试从文本中提取
        return self._extract_from_text(image_result)
    
    def _extract_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """
        从文本中提取记账信息
        
        Args:
            text: 图像描述文本
            
        Returns:
            标准化的记账信息字典
        """
        result = {
            "is_accounting": False,
            "amount": None,
            "type": "支出",
            "category": "其他",
            "description": "",
            "time": None,
            "payment_method": None,
            "merchant": None
        }
        
        # 检查是否包含记账关键词
        accounting_keywords = ["支付", "付款", "消费", "订单", "转账", "收款", 
                               "金额", "元", "￥", "¥", "账单", "小票"]
        
        has_accounting_info = any(kw in text for kw in accounting_keywords)
        if not has_accounting_info:
            return None
        
        result["is_accounting"] = True
        
        # 提取金额
        amount_patterns = [
            r'[¥￥]\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*元',
            r'金额[：:]\s*(\d+\.?\d*)',
            r'实付[：:]\s*(\d+\.?\d*)',
            r'合计[：:]\s*(\d+\.?\d*)',
            r'订单总额[：:]\s*(\d+\.?\d*)',
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text)
            if match:
                result["amount"] = float(match.group(1))
                break
        
        # 判断收入/支出
        if "收入" in text or "收款" in text or "退款" in text:
            result["type"] = "收入"
        else:
            result["type"] = "支出"
        
        # 提取商家/平台信息
        for platform, info in self.SHOPPING_PLATFORMS.items():
            if platform in text:
                result["category"] = info["category"]
                result["merchant"] = platform
                result["description"] = info["prefix"]
                break
        
        # 如果没有匹配到平台，尝试从分类规则推断
        if not result["merchant"]:
            for category, keywords in self.CATEGORY_RULES.items():
                if any(kw in text for kw in keywords):
                    result["category"] = category
                    break
        
        # 提取时间
        time_patterns = [
            r'(\d{4}[-/]\d{2}[-/]\d{2}\s*\d{2}:\d{2})',
            r'(\d{2}:\d{2})',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                result["time"] = match.group(1)
                break
        
        # 如果没有时间，使用当前时间
        if not result["time"]:
            result["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 提取支付方式
        payment_methods = ["微信支付", "支付宝", "银行卡", "现金", "花呗", "白条"]
        for method in payment_methods:
            if method in text:
                result["payment_method"] = method
                break
        
        return result
    
    def _standardize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化记账信息
        
        Args:
            data: 原始提取的数据
            
        Returns:
            标准化后的数据
        """
        result = {
            "is_accounting": True,
            "amount": self._standardize_amount(data.get("amount")),
            "type": data.get("type", "支出"),
            "category": self._infer_category(data),
            "description": self._build_description(data),
            "time": self._standardize_time(data.get("time")),
            "payment_method": data.get("payment_method", "微信支付"),
            "merchant": data.get("merchant", "")
        }
        
        return result
    
    def _standardize_amount(self, amount: Any) -> Optional[float]:
        """标准化金额"""
        if amount is None:
            return None
        
        if isinstance(amount, (int, float)):
            return float(amount)
        
        # 处理字符串
        amount_str = str(amount).replace("¥", "").replace("￥", "").replace("元", "")
        try:
            return float(amount_str)
        except ValueError:
            return None
    
    def _infer_category(self, data: Dict[str, Any]) -> str:
        """推断分类"""
        # 先检查是否有平台信息
        merchant = data.get("merchant", "")
        for platform, info in self.SHOPPING_PLATFORMS.items():
            if platform in merchant:
                return info["category"]
        
        # 从描述中推断
        description = data.get("description", "") + " " + merchant
        for category, keywords in self.CATEGORY_RULES.items():
            if any(kw in description for kw in keywords):
                return category
        
        # 使用已有的分类
        return data.get("category", "其他")
    
    def _build_description(self, data: Dict[str, Any]) -> str:
        """构建描述"""
        merchant = data.get("merchant", "")
        description = data.get("description", "")
        
        # 检查是否是购物平台
        for platform, info in self.SHOPPING_PLATFORMS.items():
            if platform in merchant:
                prefix = info["prefix"]
                if description:
                    return f"{prefix}{description}"
                return prefix.rstrip(" - ")
        
        # 普通描述
        if merchant and description:
            return f"{merchant} - {description}"
        return merchant or description or "消费"
    
    def _standardize_time(self, time_str: Optional[str]) -> str:
        """标准化时间"""
        if not time_str:
            return datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 尝试解析各种格式
        formats = [
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M",
            "%Y年%m月%d日 %H:%M",
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                return dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                continue
        
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def build_gui_query(self, data: Dict[str, Any]) -> Optional[str]:
        """
        构建GUI Agent查询语句
        
        Args:
            data: 标准化的记账信息
            
        Returns:
            GUI Agent可执行的查询语句
            
        Raises:
            PermissionError: 如果检测到竞品应用
        """
        if not data.get("is_accounting") or not data.get("amount"):
            return None
        
        # 校验目标应用（如果环境变量中有指定）
        target_app = os.environ.get("TARGET_APP_PACKAGE", "")
        for forbidden in self.FORBIDDEN_APPS:
            if forbidden.lower() in target_app.lower():
                raise PermissionError(
                    f"❌ 禁止操作：检测到竞品记账应用\n"
                    f"本 Skill 仅支持「{self.AUTHORIZED_APP}」\n\n"
                    f"授权环境：小艺 Claw + 一记账 APP\n"
                    f"联系方式：QQ 2756077825"
                )
        
        template = (
            "打开一日记账APP，点击记一笔按钮，选择{type}类型，"
            "输入金额{amount}，选择分类{category}，"
            "在备注中填写\"{description}\"，保存这条记账记录。"
        )
        
        return template.format(
            type=data["type"],
            amount=data["amount"],
            category=data["category"],
            description=data["description"]
        )


def main():
    """测试入口"""
    # 打印版权水印
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("auto-accounting v1.0.7")
    print("Copyright © 2026 摇摇")
    print("授权环境：小艺 Claw + 一记账 APP")
    print("禁止用于其他记账应用")
    print("联系方式：QQ 2756077825")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 运行时校验
    if VALIDATOR_AVAILABLE:
        try:
            RuntimeValidator.validate()
            print("✅ 环境校验通过\n")
        except PermissionError as e:
            print(f"{e}")
            return
    
    parser = AccountingParser()
    
    # 测试用例
    test_cases = [
        "微信支付成功，向星巴克支付¥28.50，时间：2026-04-02 13:45",
        "京东订单，购买华为耳机，实付款299元",
        "美团外卖订单，肯德基午餐，实付金额35元",
    ]
    
    for test in test_cases:
        print(f"\n输入: {test}")
        result = parser.parse_image_result(test)
        if result:
            print(f"解析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
            try:
                query = parser.build_gui_query(result)
                print(f"GUI Query: {query}")
            except PermissionError as e:
                print(f"{e}")
        else:
            print("非记账信息")


if __name__ == "__main__":
    main()
