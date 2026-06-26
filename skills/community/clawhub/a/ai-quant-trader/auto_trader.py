#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动交易执行器
"""

import json
import os
from datetime import datetime, timedelta
import time
import threading

class AutoTrader:
    """自动交易执行器"""
    
    def __init__(self, broker=None):
        self.broker = broker
        self.auto_trades_dir = os.path.join(os.path.dirname(__file__), "user_data", "auto_trades")
        os.makedirs(self.auto_trades_dir, exist_ok=True)
        
        # 自动交易状态
        self.active_trades = {}
        self.monitoring = False
        self.monitor_thread = None
        
        print("✅ 自动交易执行器初始化完成")
    
    def enable_auto_trading(self, strategy_name, symbol, settings=None):
        """启用自动交易"""
        print(f"⚡ 启用自动交易: {strategy_name} -> {symbol}")
        
        if settings is None:
            settings = {
                "check_interval": 300,  # 检查间隔（秒）
                "max_position": 0.2,  # 最大仓位比例
                "require_confirmation": True,  # 需要人工确认
                "enabled": True
            }
        
        trade_id = f"{symbol}_{strategy_name}_{int(time.time())}"
        
        auto_trade = {
            "id": trade_id,
            "strategy_name": strategy_name,
            "symbol": symbol,
            "settings": settings,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "last_check": None,
            "signals": [],
            "trades": []
        }
        
        # 保存到文件
        trade_file = os.path.join(self.auto_trades_dir, f"{trade_id}.json")
        with open(trade_file, 'w', encoding='utf-8') as f:
            json.dump(auto_trade, f, ensure_ascii=False, indent=2)
        
        # 添加到活跃交易
        self.active_trades[trade_id] = auto_trade
        
        print(f"✅ 自动交易已启用: {trade_id}")
        
        # 启动监控（如果还没启动）
        if not self.monitoring:
            self.start_monitoring()
        
        return {
            "success": True,
            "trade_id": trade_id,
            "message": f"已为{symbol}启用{strategy_name}自动交易"
        }
    
    def disable_auto_trading(self, symbol=None, trade_id=None):
        """禁用自动交易"""
        if trade_id:
            # 禁用特定交易
            if trade_id in self.active_trades:
                self.active_trades[trade_id]["status"] = "disabled"
                self.active_trades[trade_id]["disabled_at"] = datetime.now().isoformat()
                
                # 更新文件
                trade_file = os.path.join(self.auto_trades_dir, f"{trade_id}.json")
                if os.path.exists(trade_file):
                    with open(trade_file, 'w', encoding='utf-8') as f:
                        json.dump(self.active_trades[trade_id], f, ensure_ascii=False, indent=2)
                
                print(f"✅ 已禁用自动交易: {trade_id}")
                return {"success": True, "trade_id": trade_id}
        
        elif symbol:
            # 禁用该股票的所有自动交易
            disabled = []
            for tid, trade in list(self.active_trades.items()):
                if trade["symbol"] == symbol and trade["status"] == "active":
                    trade["status"] = "disabled"
                    trade["disabled_at"] = datetime.now().isoformat()
                    disabled.append(tid)
            
            if disabled:
                print(f"✅ 已禁用{symbol}的{len(disabled)}个自动交易")
                return {"success": True, "disabled": disabled}
        
        return {"success": False, "error": "未找到指定的自动交易"}
    
    def pause_auto_trading(self, symbol=None, trade_id=None):
        """暂停自动交易"""
        if trade_id and trade_id in self.active_trades:
            self.active_trades[trade_id]["status"] = "paused"
            print(f"⏸️ 已暂停自动交易: {trade_id}")
            return {"success": True, "trade_id": trade_id}
        
        elif symbol:
            paused = []
            for tid, trade in self.active_trades.items():
                if trade["symbol"] == symbol and trade["status"] == "active":
                    trade["status"] = "paused"
                    paused.append(tid)
            
            if paused:
                print(f"⏸️ 已暂停{symbol}的{len(paused)}个自动交易")
                return {"success": True, "paused": paused}
        
        return {"success": False, "error": "未找到指定的自动交易"}
    
    def resume_auto_trading(self, symbol=None, trade_id=None):
        """恢复自动交易"""
        if trade_id and trade_id in self.active_trades:
            self.active_trades[trade_id]["status"] = "active"
            print(f"▶️ 已恢复自动交易: {trade_id}")
            return {"success": True, "trade_id": trade_id}
        
        elif symbol:
            resumed = []
            for tid, trade in self.active_trades.items():
                if trade["symbol"] == symbol and trade["status"] == "paused":
                    trade["status"] = "active"
                    resumed.append(tid)
            
            if resumed:
                print(f"▶️ 已恢复{symbol}的{len(resumed)}个自动交易")
                return {"success": True, "resumed": resumed}
        
        return {"success": False, "error": "未找到指定的自动交易"}
    
    def list_auto_trades(self):
        """列出所有自动交易"""
        # 从文件加载所有交易
        all_trades = []
        
        if os.path.exists(self.auto_trades_dir):
            for file_name in os.listdir(self.auto_trades_dir):
                if file_name.endswith('.json'):
                    file_path = os.path.join(self.auto_trades_dir, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            trade = json.load(f)
                        all_trades.append(trade)
                    except:
                        continue
        
        # 更新内存中的活跃交易
        for trade in all_trades:
            if trade["status"] == "active" and trade["id"] not in self.active_trades:
                self.active_trades[trade["id"]] = trade
        
        return all_trades
    
    def check_signals(self, trade):
        """检查交易信号"""
        # 这里应该是实际的信号检查逻辑
        # 暂时返回模拟信号
        
        symbol = trade["symbol"]
        strategy_name = trade["strategy_name"]
        
        # 模拟信号生成
        signals = []
        
        # 随机生成信号
        import random
        signal_types = ["buy", "sell", "hold"]
        signal_type = random.choice(signal_types)
        
        if signal_type == "buy":
            signal = {
                "type": "buy",
                "strength": random.uniform(0.6, 0.9),
                "reason": f"{strategy_name}产生买入信号",
                "price": random.uniform(100, 200),  # 模拟价格
                "timestamp": datetime.now().isoformat()
            }
            signals.append(signal)
        
        elif signal_type == "sell":
            signal = {
                "type": "sell",
                "strength": random.uniform(0.6, 0.9),
                "reason": f"{strategy_name}产生卖出信号",
                "price": random.uniform(100, 200),
                "timestamp": datetime.now().isoformat()
            }
            signals.append(signal)
        
        return signals
    
    def execute_signal(self, trade, signal):
        """执行信号"""
        if self.broker is None:
            return {"success": False, "error": "交易引擎未初始化"}
        
        symbol = trade["symbol"]
        settings = trade["settings"]
        
        if signal["type"] == "buy":
            # 计算买入数量
            account_value = self.broker.get_account_value()
            max_position_value = account_value * settings.get("max_position", 0.2)
            
            # 简单逻辑：买入固定数量
            quantity = 100  # 模拟
            
            if settings.get("require_confirmation", True):
                # 需要人工确认
                return {
                    "success": True,
                    "action": "buy",
                    "symbol": symbol,
                    "quantity": quantity,
                    "price": signal["price"],
                    "status": "pending_confirmation",
                    "message": f"买入信号待确认: {symbol} {quantity}股 @ {signal['price']:.2f}"
                }
            else:
                # 自动执行
                try:
                    result = self.broker.buy_stock(symbol, quantity, signal["price"])
                    return {
                        "success": True,
                        "action": "buy",
                        "symbol": symbol,
                        "result": result,
                        "status": "executed"
                    }
                except Exception as e:
                    return {"success": False, "error": str(e)}
        
        elif signal["type"] == "sell":
            # 检查持仓
            position = self.broker.get_position(symbol)
            if position and position["quantity"] > 0:
                quantity = min(position["quantity"], 100)  # 模拟
                
                if settings.get("require_confirmation", True):
                    return {
                        "success": True,
                        "action": "sell",
                        "symbol": symbol,
                        "quantity": quantity,
                        "price": signal["price"],
                        "status": "pending_confirmation",
                        "message": f"卖出信号待确认: {symbol} {quantity}股 @ {signal['price']:.2f}"
                    }
                else:
                    try:
                        result = self.broker.sell_stock(symbol, quantity, signal["price"])
                        return {
                            "success": True,
                            "action": "sell",
                            "symbol": symbol,
                            "result": result,
                            "status": "executed"
                        }
                    except Exception as e:
                        return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "未知信号类型"}
    
    def monitor_loop(self):
        """监控循环"""
        print("👁️ 自动交易监控已启动")
        
        while self.monitoring:
            try:
                # 检查所有活跃交易
                for trade_id, trade in list(self.active_trades.items()):
                    if trade["status"] != "active":
                        continue
                    
                    # 检查是否需要检查信号
                    last_check = trade.get("last_check")
                    check_interval = trade["settings"].get("check_interval", 300)
                    
                    if last_check is None or (datetime.now() - datetime.fromisoformat(last_check)).seconds >= check_interval:
                        # 检查信号
                        signals = self.check_signals(trade)
                        
                        if signals:
                            # 处理信号
                            for signal in signals:
                                result = self.execute_signal(trade, signal)
                                
                                # 记录信号
                                trade["signals"].append({
                                    "signal": signal,
                                    "result": result,
                                    "timestamp": datetime.now().isoformat()
                                })
                                
                                if result.get("status") == "executed":
                                    trade["trades"].append(result)
                        
                        # 更新最后检查时间
                        trade["last_check"] = datetime.now().isoformat()
                        
                        # 保存到文件
                        trade_file = os.path.join(self.auto_trades_dir, f"{trade_id}.json")
                        with open(trade_file, 'w', encoding='utf-8') as f:
                            json.dump(trade, f, ensure_ascii=False, indent=2)
                
                # 休眠一段时间
                time.sleep(10)  # 10秒检查一次
                
            except Exception as e:
                print(f"监控循环错误: {e}")
                time.sleep(30)
    
    def start_monitoring(self):
        """启动监控"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("🚀 自动交易监控线程已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("🛑 自动交易监控已停止")

# 测试代码
if __name__ == "__main__":
    trader = AutoTrader()
    
    # 测试启用自动交易
    result = trader.enable_auto_trading("MACD策略", "600519")
    print(f"启用结果: {result}")
    
    # 测试列出自动交易
    trades = trader.list_auto_trades()
    print(f"\n自动交易列表: {len(trades)} 个")
    
    # 测试暂停和恢复
    if trades:
        pause_result = trader.pause_auto_trading(trade_id=trades[0]["id"])
        print(f"\n暂停结果: {pause_result}")
        
        resume_result = trader.resume_auto_trading(trade_id=trades[0]["id"])
        print(f"恢复结果: {resume_result}")
    
    # 停止监控
    trader.stop_monitoring()