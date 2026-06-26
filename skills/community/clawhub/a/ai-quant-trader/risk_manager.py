#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险管理系统
"""

import json
import os
from datetime import datetime
import threading
import time

class RiskManager:
    """风险管理系统"""
    
    def __init__(self, broker=None):
        self.broker = broker
        self.risk_rules_dir = os.path.join(os.path.dirname(__file__), "user_data", "risk_rules")
        os.makedirs(self.risk_rules_dir, exist_ok=True)
        
        # 风险规则
        self.active_rules = {}
        self.monitoring = False
        self.monitor_thread = None
        
        # 默认风险参数
        self.default_params = {
            "max_position_per_stock": 0.2,  # 单只股票最大仓位20%
            "max_portfolio_risk": 0.3,  # 组合最大风险30%
            "daily_loss_limit": 0.05,  # 单日最大亏损5%
            "max_drawdown_limit": 0.15,  # 最大回撤限制15%
            "min_win_rate": 0.55,  # 最低胜率55%
            "min_profit_factor": 1.2  # 最低盈亏比1.2
        }
        
        print("✅ 风险管理系统初始化完成")
    
    def set_stop_loss(self, symbol, stop_loss_type, value):
        """设置止损规则"""
        print(f"🛡️ 设置止损: {symbol} {stop_loss_type} {value}")
        
        rule_id = f"stop_loss_{symbol}_{int(time.time())}"
        
        rule = {
            "id": rule_id,
            "symbol": symbol,
            "type": "stop_loss",
            "stop_loss_type": stop_loss_type,
            "value": value,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "triggered": False,
            "trigger_price": None,
            "trigger_time": None
        }
        
        # 保存规则
        rule_file = os.path.join(self.risk_rules_dir, f"{rule_id}.json")
        with open(rule_file, 'w', encoding='utf-8') as f:
            json.dump(rule, f, ensure_ascii=False, indent=2)
        
        # 添加到活跃规则
        self.active_rules[rule_id] = rule
        
        # 启动监控（如果还没启动）
        if not self.monitoring:
            self.start_monitoring()
        
        return {
            "success": True,
            "rule_id": rule_id,
            "message": f"已为{symbol}设置{stop_loss_type}止损: {value}"
        }
    
    def set_take_profit(self, symbol, take_profit_type, value):
        """设置止盈规则"""
        print(f"🎯 设置止盈: {symbol} {take_profit_type} {value}")
        
        rule_id = f"take_profit_{symbol}_{int(time.time())}"
        
        rule = {
            "id": rule_id,
            "symbol": symbol,
            "type": "take_profit",
            "take_profit_type": take_profit_type,
            "value": value,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "triggered": False,
            "trigger_price": None,
            "trigger_time": None
        }
        
        # 保存规则
        rule_file = os.path.join(self.risk_rules_dir, f"{rule_id}.json")
        with open(rule_file, 'w', encoding='utf-8') as f:
            json.dump(rule, f, ensure_ascii=False, indent=2)
        
        # 添加到活跃规则
        self.active_rules[rule_id] = rule
        
        return {
            "success": True,
            "rule_id": rule_id,
            "message": f"已为{symbol}设置{take_profit_type}止盈: {value}"
        }
    
    def set_trailing_stop(self, symbol, trail_percent):
        """设置移动止盈"""
        print(f"📈 设置移动止盈: {symbol} 回撤{trail_percent}%")
        
        rule_id = f"trailing_stop_{symbol}_{int(time.time())}"
        
        rule = {
            "id": rule_id,
            "symbol": symbol,
            "type": "trailing_stop",
            "trail_percent": trail_percent,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "highest_price": None,
            "current_stop": None,
            "triggered": False
        }
        
        # 保存规则
        rule_file = os.path.join(self.risk_rules_dir, f"{rule_id}.json")
        with open(rule_file, 'w', encoding='utf-8') as f:
            json.dump(rule, f, ensure_ascii=False, indent=2)
        
        self.active_rules[rule_id] = rule
        
        return {
            "success": True,
            "rule_id": rule_id,
            "message": f"已为{symbol}设置移动止盈: 从最高点回撤{trail_percent}%时卖出"
        }
    
    def remove_rule(self, rule_id=None, symbol=None, rule_type=None):
        """移除规则"""
        removed = []
        
        if rule_id:
            # 移除特定规则
            if rule_id in self.active_rules:
                self.active_rules[rule_id]["status"] = "removed"
                removed.append(rule_id)
        
        elif symbol and rule_type:
            # 移除该股票该类型的所有规则
            for rid, rule in list(self.active_rules.items()):
                if rule["symbol"] == symbol and rule["type"] == rule_type and rule["status"] == "active":
                    rule["status"] = "removed"
                    removed.append(rid)
        
        elif symbol:
            # 移除该股票的所有规则
            for rid, rule in list(self.active_rules.items()):
                if rule["symbol"] == symbol and rule["status"] == "active":
                    rule["status"] = "removed"
                    removed.append(rid)
        
        if removed:
            print(f"🗑️ 已移除{len(removed)}个规则")
            return {"success": True, "removed": removed}
        
        return {"success": False, "error": "未找到指定的规则"}
    
    def list_rules(self, symbol=None, rule_type=None):
        """列出规则"""
        # 从文件加载所有规则
        all_rules = []
        
        if os.path.exists(self.risk_rules_dir):
            for file_name in os.listdir(self.risk_rules_dir):
                if file_name.endswith('.json'):
                    file_path = os.path.join(self.risk_rules_dir, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            rule = json.load(f)
                        
                        # 过滤条件
                        if symbol and rule["symbol"] != symbol:
                            continue
                        if rule_type and rule["type"] != rule_type:
                            continue
                        
                        all_rules.append(rule)
                    except:
                        continue
        
        # 更新内存中的活跃规则
        for rule in all_rules:
            if rule["status"] == "active" and rule["id"] not in self.active_rules:
                self.active_rules[rule["id"]] = rule
        
        return all_rules
    
    def check_stop_loss(self, rule, current_price, position):
        """检查止损规则"""
        if not position or position["quantity"] <= 0:
            return False
        
        cost_price = position["cost_price"]
        stop_loss_type = rule["stop_loss_type"]
        value = rule["value"]
        
        if stop_loss_type == "percentage":
            # 百分比止损
            stop_price = cost_price * (1 - value / 100)
            if current_price <= stop_price:
                return {
                    "triggered": True,
                    "reason": f"价格{current_price:.2f} ≤ 止损价{stop_price:.2f} (亏损{value}%)",
                    "stop_price": stop_price
                }
        
        elif stop_loss_type == "fixed":
            # 固定价格止损
            if current_price <= value:
                return {
                    "triggered": True,
                    "reason": f"价格{current_price:.2f} ≤ 止损价{value:.2f}",
                    "stop_price": value
                }
        
        elif stop_loss_type == "atr":
            # ATR止损（需要历史数据）
            # 这里简化处理
            atr_stop = cost_price * (1 - value / 100)
            if current_price <= atr_stop:
                return {
                    "triggered": True,
                    "reason": f"ATR止损触发 (波动{value}%)",
                    "stop_price": atr_stop
                }
        
        return False
    
    def check_take_profit(self, rule, current_price, position):
        """检查止盈规则"""
        if not position or position["quantity"] <= 0:
            return False
        
        cost_price = position["cost_price"]
        take_profit_type = rule["take_profit_type"]
        value = rule["value"]
        
        if take_profit_type == "percentage":
            # 百分比止盈
            take_price = cost_price * (1 + value / 100)
            if current_price >= take_price:
                return {
                    "triggered": True,
                    "reason": f"价格{current_price:.2f} ≥ 止盈价{take_price:.2f} (盈利{value}%)",
                    "take_price": take_price
                }
        
        elif take_profit_type == "fixed":
            # 固定价格止盈
            if current_price >= value:
                return {
                    "triggered": True,
                    "reason": f"价格{current_price:.2f} ≥ 止盈价{value:.2f}",
                    "take_price": value
                }
        
        return False
    
    def check_trailing_stop(self, rule, current_price):
        """检查移动止盈"""
        symbol = rule["symbol"]
        trail_percent = rule["trail_percent"]
        
        # 获取最高价
        if rule["highest_price"] is None or current_price > rule["highest_price"]:
            rule["highest_price"] = current_price
            rule["current_stop"] = current_price * (1 - trail_percent / 100)
        
        # 检查是否触发
        if current_price <= rule["current_stop"]:
            return {
                "triggered": True,
                "reason": f"价格{current_price:.2f} ≤ 移动止盈价{rule['current_stop']:.2f} (从最高点{rule['highest_price']:.2f}回撤{trail_percent}%)",
                "highest_price": rule["highest_price"],
                "stop_price": rule["current_stop"]
            }
        
        return False
    
    def execute_risk_action(self, rule, trigger_info):
        """执行风险动作"""
        if self.broker is None:
            return {"success": False, "error": "交易引擎未初始化"}
        
        symbol = rule["symbol"]
        
        # 获取持仓
        position = self.broker.get_position(symbol)
        if not position or position["quantity"] <= 0:
            return {"success": False, "error": "无持仓"}
        
        # 卖出全部持仓
        try:
            result = self.broker.sell_stock(symbol, position["quantity"], trigger_info.get("stop_price") or trigger_info.get("take_price"))
            
            # 更新规则状态
            rule["triggered"] = True
            rule["trigger_price"] = result.get("price")
            rule["trigger_time"] = datetime.now().isoformat()
            rule["status"] = "triggered"
            
            # 保存更新
            rule_file = os.path.join(self.risk_rules_dir, f"{rule['id']}.json")
            with open(rule_file, 'w', encoding='utf-8') as f:
                json.dump(rule, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "action": "sell",
                "symbol": symbol,
                "quantity": position["quantity"],
                "reason": trigger_info["reason"],
                "result": result
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_portfolio_risk(self):
        """检查组合风险"""
        if self.broker is None:
            return {"risk_level": "unknown", "issues": []}
        
        issues = []
        
        try:
            # 获取账户信息
            account_value = self.broker.get_account_value()
            positions = self.broker.get_all_positions()
            
            # 检查单只股票仓位
            for symbol, position in positions.items():
                position_value = position["market_value"]
                position_ratio = position_value / account_value if account_value > 0 else 0
                
                if position_ratio > self.default_params["max_position_per_stock"]:
                    issues.append(f"{symbol}仓位{position_ratio:.1%}超过限制{self.default_params['max_position_per_stock']:.1%}")
            
            # 检查组合风险（简化）
            total_position_value = sum(p["market_value"] for p in positions.values())
            portfolio_ratio = total_position_value / account_value if account_value > 0 else 0
            
            if portfolio_ratio > self.default_params["max_portfolio_risk"]:
                issues.append(f"组合仓位{portfolio_ratio:.1%}超过限制{self.default_params['max_portfolio_risk']:.1%}")
            
            # 确定风险等级
            if len(issues) >= 3:
                risk_level = "high"
            elif len(issues) >= 1:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                "risk_level": risk_level,
                "issues": issues,
                "portfolio_ratio": portfolio_ratio,
                "position_count": len(positions)
            }
            
        except Exception as e:
            return {"risk_level": "error", "issues": [f"检查失败: {str(e)}"]}
    
    def monitor_loop(self):
        """风险监控循环"""
        print("👁️ 风险监控已启动")
        
        while self.monitoring:
            try:
                # 检查所有活跃规则
                for rule_id, rule in list(self.active_rules.items()):
                    if rule["status"] != "active" or rule["triggered"]:
                        continue
                    
                    symbol = rule["symbol"]
                    
                    # 获取当前价格（模拟）
                    current_price = 100.0  # 这里应该从数据提供器获取
                    
                    # 获取持仓
                    position = None
                    if self.broker:
                        position = self.broker.get_position(symbol)
                    
                    # 根据规则类型检查
                    trigger_info = None
                    
                    if rule["type"] == "stop_loss":
                        trigger_info = self.check_stop_loss(rule, current_price, position)
                    
                    elif rule["type"] == "take_profit":
                        trigger_info = self.check_take_profit(rule, current_price, position)
                    
                    elif rule["type"] == "trailing_stop":
                        trigger_info = self.check_trailing_stop(rule, current_price)
                    
                    # 如果触发，执行动作
                    if trigger_info and trigger_info.get("triggered"):
                        print(f"🚨 风险规则触发: {symbol} - {trigger_info['reason']}")
                        
                        result = self.execute_risk_action(rule, trigger_info)
                        if result["success"]:
                            print(f"✅ 已执行风险动作: 卖出{symbol}")
                        else:
                            print(f"❌ 执行失败: {result.get('error')}")
                
                # 检查组合风险
                portfolio_risk = self.check_portfolio_risk()
                if portfolio_risk["risk_level"] == "high":
                    print(f"⚠️ 高风险警告: {portfolio_risk['issues']}")
                
                # 休眠一段时间
                time.sleep(30)  # 30秒检查一次
                
            except Exception as e:
                print(f"风险监控错误: {e}")
                time.sleep(60)
    
    def start_monitoring(self):
        """启动监控"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("🚀 风险监控线程已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("🛑 风险监控已停止")

# 测试代码
if __name__ == "__main__":
    manager = RiskManager()
    
    # 测试设置止损
    result = manager.set_stop_loss("600519", "percentage", 5)
    print(f"设置止损: {result}")
    
    # 测试设置止盈
    result = manager.set_take_profit("600519", "percentage", 10)
    print(f"设置止盈: {result}")
    
    # 测试设置移动止盈
    result = manager.set_trailing_stop("600519", 8)
    print(f"设置移动止盈: {result}")
    
    # 测试列出规则
    rules = manager.list_rules()
    print(f"\n风险规则列表: {len(rules)} 个")
    
    # 测试检查组合风险
    risk = manager.check_portfolio_risk()
    print(f"\n组合风险检查: 等级={risk['risk_level']}, 问题={risk['issues']}")
    
    # 停止监控
    manager.stop_monitoring()