#!/usr/bin/env python3
"""
A股核心交易框架 - 快速启动脚本
"""

import asyncio
import logging
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_system():
    """测试A股交易系统"""
    logger.info("=" * 60)
    logger.info("A股核心交易框架 - 系统测试")
    logger.info("=" * 60)
    
    try:
        # 导入主引擎
        from core.a_share_trader import AShareTrader
        
        # 创建交易引擎（模拟模式，10亿资金）
        trader = AShareTrader(capital=1000000000.0, mode="paper")
        
        logger.info("1. 引擎创建成功")
        
        # 初始化组件
        trader.initialize_components()
        logger.info("2. 组件初始化成功")
        
        # 测试数据接口
        if trader.data_interface:
            test_symbol = "000001.SZ"
            market_data = trader.data_interface.get_market_data(test_symbol)
            fundamental_data = trader.data_interface.get_fundamental_data(test_symbol)
            
            logger.info(f"3. 数据接口测试成功")
            logger.info(f"   股票: {test_symbol}, 价格: {market_data.get('price', 0):.2f}")
            logger.info(f"   市值: {fundamental_data.get('market_cap', 0):,.0f}")
            logger.info(f"   PE: {fundamental_data.get('pe', 0):.1f}")
        
        # 测试策略
        logger.info(f"4. 策略初始化: {len(trader.strategies)}个策略")
        for strategy_info in trader.strategies:
            logger.info(f"   - {strategy_info['name']}: 权重 {strategy_info['weight']:.2f}")
        
        # 测试自适应引擎
        if trader.adaptive_engine:
            engine_status = trader.adaptive_engine.get_engine_status()
            logger.info(f"5. 自适应引擎状态: {engine_status.get('market_state')}")
        
        # 测试单次交易周期
        logger.info("6. 测试单次交易周期...")
        try:
            # 更新市场数据
            market_data = await trader._update_market_data()
            logger.info(f"   获取市场数据: {len(market_data)}只股票")
            
            # 生成信号
            signals = await trader._generate_signals(market_data)
            logger.info(f"   生成交易信号: {len(signals)}个")
            
            if signals:
                # 风险检查
                approved_signals = await trader._risk_check(signals)
                logger.info(f"   通过风控信号: {len(approved_signals)}个")
                
                # 显示前3个信号
                for i, signal in enumerate(approved_signals[:3]):
                    logger.info(f"     信号{i+1}: {signal.get('symbol')} {signal.get('side')} "
                               f"@{signal.get('price', 0):.2f}")
            
            logger.info("✅ 系统测试通过！")
            
        except Exception as e:
            logger.error(f"交易周期测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        return True
        
    except ImportError as e:
        logger.error(f"导入失败: {e}")
        logger.info("请确保所有依赖模块都已创建")
        return False
    except Exception as e:
        logger.error(f"系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_simulation(duration_seconds: int = 30):
    """运行模拟交易"""
    logger.info("=" * 60)
    logger.info("A股核心交易框架 - 模拟交易")
    logger.info("=" * 60)
    
    try:
        from core.a_share_trader import AShareTrader
        
        # 创建交易引擎
        trader = AShareTrader(capital=1000000000.0, mode="paper")
        
        logger.info(f"启动模拟交易，时长: {duration_seconds}秒")
        logger.info("按 Ctrl+C 停止")
        
        # 启动引擎
        import signal
        import asyncio
        
        # 设置停止信号处理
        stop_event = asyncio.Event()
        
        def signal_handler():
            logger.info("收到停止信号，正在关闭...")
            stop_event.set()
        
        # 运行引擎（简化版本）
        trader.initialize_components()
        
        start_time = asyncio.get_event_loop().time()
        
        while not stop_event.is_set():
            current_time = asyncio.get_event_loop().time()
            if current_time - start_time > duration_seconds:
                logger.info("模拟时间到，停止运行")
                break
            
            try:
                # 执行单次交易周期
                await trader._trading_cycle()
                
                # 等待1秒
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"交易周期异常: {e}")
                await asyncio.sleep(5)
        
        # 生成绩效报告
        report = await trader.generate_performance_report()
        if report:
            logger.info(f"模拟交易完成，组合价值: {report.get('portfolio_value', 0):,.0f}元")
            logger.info(f"总盈亏: {report.get('total_pnl', 0):,.0f}元")
            logger.info(f"最大回撤: {report.get('max_drawdown', 0):.2%}")
        
        return True
        
    except Exception as e:
        logger.error(f"模拟交易失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="A股核心交易框架")
    parser.add_argument("command", choices=["test", "simulate"], 
                       help="命令: test(测试系统), simulate(运行模拟)")
    parser.add_argument("--duration", type=int, default=30,
                       help="模拟时长（秒），默认30秒")
    
    args = parser.parse_args()
    
    if args.command == "test":
        success = asyncio.run(test_system())
        sys.exit(0 if success else 1)
    elif args.command == "simulate":
        success = asyncio.run(run_simulation(args.duration))
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()