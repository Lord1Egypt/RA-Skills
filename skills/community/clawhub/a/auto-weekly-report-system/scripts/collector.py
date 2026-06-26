#!/usr/bin/env python3
"""
数据收集器 - 整合所有项目数据
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

class DataCollector:
    def __init__(self):
        self.data = {
            "generated_at": datetime.now().isoformat(),
            "period": self._get_week_period(),
            "v35": {},
            "instreet": {},
            "price_monitor": {},
            "system_health": {}
        }
    
    def _get_week_period(self):
        """获取本周时间段"""
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        friday = monday + timedelta(days=4)
        return f"{monday.strftime('%m/%d')} - {friday.strftime('%m/%d')}"
    
    def collect_v35(self):
        """收集 v3.5 数据"""
        try:
            # 读取配置
            with open("/tmp/v35_migration_config.json", "r") as f:
                config = json.load(f)
            
            # 读取日志统计
            log_file = "/tmp/agent_v35_production.log"
            log_data = {"v35_runs": 0, "v35_votes": [], "v30_runs": 0, "v30_votes": []}
            
            if Path(log_file).exists():
                with open(log_file, 'r') as f:
                    content = f.read()
                
                # 统计运行次数
                v35_matches = re.findall(r'使用: V35.*?平均赞: (\d+\.?\d*)', content, re.DOTALL)
                v30_matches = re.findall(r'使用: V30.*?平均赞: (\d+\.?\d*)', content, re.DOTALL)
                
                log_data["v35_runs"] = len(v35_matches)
                log_data["v35_votes"] = [float(v) for v in v35_matches if v]
                log_data["v30_runs"] = len(v30_matches)
                log_data["v30_votes"] = [float(v) for v in v30_matches if v]
            
            self.data["v35"] = {
                "weight": config.get("v35_weight", 0),
                "avg_votes": config.get("metrics", {}).get("v35_avg_votes", 0),
                "accuracy": config.get("metrics", {}).get("prediction_accuracy", 0),
                "week_runs": log_data["v35_runs"],
                "week_votes": log_data["v35_votes"],
                "week_avg": sum(log_data["v35_votes"]) / len(log_data["v35_votes"]) if log_data["v35_votes"] else 0,
                "status": "✅ 运行中" if config.get("v35_weight") == 1.0 else "⚠️ 渐进迁移中"
            }
        except Exception as e:
            self.data["v35"] = {"status": f"❌ 数据收集失败: {e}"}
    
    def collect_instreet(self):
        """收集 InStreet 数据"""
        try:
            log_file = "/tmp/instreet_reply.log"
            
            if not Path(log_file).exists():
                self.data["instreet"] = {
                    "status": "⚠️ 日志未启用",
                    "hint": "修改 instreet_auto_reply.py 添加日志记录"
                }
                return
            
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            # 统计
            total_replies = len([l for l in lines if "✅ 成功" in l])
            failed = len([l for l in lines if "❌ 失败" in l])
            morning_rush = len([l for l in lines if "早高峰" in l])
            
            self.data["instreet"] = {
                "status": "✅ 运行中",
                "total_replies": total_replies + failed,
                "successful": total_replies,
                "failed": failed,
                "success_rate": f"{total_replies/(total_replies+failed)*100:.1f}%" if (total_replies+failed) > 0 else "N/A",
                "morning_rush_runs": morning_rush
            }
        except Exception as e:
            self.data["instreet"] = {"status": f"❌ 数据收集失败: {e}"}
    
    def collect_price_monitor(self):
        """收集价格监控数据"""
        try:
            db_file = "/tmp/price_monitor_db.json"
            
            if not Path(db_file).exists():
                self.data["price_monitor"] = {"status": "⚠️ 无监控数据"}
                return
            
            with open(db_file, 'r') as f:
                db = json.load(f)
            
            products = []
            for name, info in db.get("products", {}).items():
                products.append({
                    "name": name,
                    "price": info.get("last_price") or "未记录",
                    "last_check": info.get("last_check", "从未")[:10] if info.get("last_check") else "从未"
                })
            
            self.data["price_monitor"] = {
                "status": "✅ 正常" if products else "⚠️ 无产品",
                "products": products,
                "total_products": len(products)
            }
        except Exception as e:
            self.data["price_monitor"] = {"status": f"❌ 数据收集失败: {e}"}
    
    def collect_system_health(self):
        """收集系统健康数据"""
        import subprocess
        
        try:
            # 磁盘空间
            result = subprocess.run(['df', '-h', '/tmp'], capture_output=True, text=True)
            disk_line = result.stdout.strip().split('\n')[-1]
            disk_usage = disk_line.split()[4] if len(disk_line.split()) > 4 else "未知"
            
            # 检查关键日志文件
            logs = {
                "v35": Path("/tmp/agent_v35_production.log").exists(),
                "instreet": Path("/tmp/instreet_reply.log").exists(),
                "price": Path("/tmp/price_monitor_db.json").exists()
            }
            
            self.data["system_health"] = {
                "disk_usage": disk_usage,
                "logs_status": logs,
                "overall": "🟢 健康" if all(logs.values()) else "🟡 部分日志缺失"
            }
        except Exception as e:
            self.data["system_health"] = {"overall": f"❌ 检查失败: {e}"}
    
    def collect_all(self):
        """收集所有数据"""
        print("📊 开始收集数据...")
        
        print("  - 收集 v3.5 数据...")
        self.collect_v35()
        
        print("  - 收集 InStreet 数据...")
        self.collect_instreet()
        
        print("  - 收集价格监控数据...")
        self.collect_price_monitor()
        
        print("  - 检查系统健康...")
        self.collect_system_health()
        
        print("✅ 数据收集完成")
        return self.data

if __name__ == "__main__":
    collector = DataCollector()
    data = collector.collect_all()
    
    # 输出到文件
    output_file = "/tmp/weekly_data.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 数据已保存: {output_file}")
