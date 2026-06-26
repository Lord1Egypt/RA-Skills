#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fund-Signal-Checker 基金信号检查器 v2.1.0

核心功能：
1. 读取 watchlist.json 监控列表
2. 逐只基金检查五大信号（季报/经理/规模/波动/风格）+ 买卖信号
3. 去重 + 频率控制
4. 飞书推送通知

**设计原则**：
- 独立脚本，可被 cron/heartbeat 调用
- 无状态：每次运行都从 watchlist 读取配置
- 信号日志：记录推送历史，用于去重

**调用方式**：
  python signal_checker.py              # 检查所有基金
  python signal_checker.py 005827       # 检查指定基金
  python signal_checker.py --dry-run    # 模拟运行（不推送）
  python signal_checker.py --summary    # 生成每日摘要
"""

import json
import os
import sys
import hashlib
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

# 添加 workspace 路径
script_dir = Path(__file__).parent
workspace_dir = Path('/home/admin/.openclaw/workspace')
if str(workspace_dir) not in sys.path:
    sys.path.insert(0, str(workspace_dir))

# ============================================================
# 配置
# ============================================================

SKILL_DIR = script_dir.parent
WATCHLIST_PATH = SKILL_DIR / 'watchlist.json'
SIGNAL_LOG_PATH = SKILL_DIR / 'signal_log.json'
CACHE_DIR = workspace_dir / 'data' / 'fund-cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Watchlist 管理
# ============================================================

class WatchlistManager:
    """监控列表管理"""

    def __init__(self):
        self.watchlist_path = WATCHLIST_PATH
        self.data = self._load()

    def _load(self) -> Dict:
        """加载 watchlist"""
        if self.watchlist_path.exists():
            with open(self.watchlist_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'watchlist': [], 'settings': {}}

    def save(self):
        """保存 watchlist"""
        self.data['updated'] = datetime.now().strftime('%Y-%m-%d')
        with open(self.watchlist_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_enabled(self, fund_code: str = None) -> List[Dict]:
        """获取启用的监控项"""
        items = [f for f in self.data.get('watchlist', []) if f.get('enabled', True)]
        if fund_code:
            items = [f for f in items if f['code'] == fund_code]
        return items

    def add(self, code: str, name: str, signals: List[str] = None):
        """添加监控"""
        if signals is None:
            signals = ["季报", "经理", "规模", "波动", "风格", "买入信号", "卖出信号"]

        # 检查是否已存在
        for item in self.data.get('watchlist', []):
            if item['code'] == code:
                item['name'] = name
                item['signals'] = signals
                item['enabled'] = True
                self.save()
                return

        self.data.setdefault('watchlist', []).append({
            'code': code,
            'name': name,
            'signals': signals,
            'thresholds': {
                '波动阈值': 5,
                '规模变化阈值': 30,
                '买入信号阈值': 70,
                '卖出信号阈值': 30
            },
            'enabled': True
        })
        self.save()

    def remove(self, code: str):
        """移除监控"""
        self.data['watchlist'] = [f for f in self.data.get('watchlist', []) if f['code'] != code]
        self.save()

    def get_settings(self) -> Dict:
        """获取设置"""
        return self.data.get('settings', {})


# ============================================================
# Signal Log 管理（去重 + 频率控制）
# ============================================================

class SignalLog:
    """信号推送日志"""

    def __init__(self):
        self.log_path = SIGNAL_LOG_PATH
        self.data = self._load()

    def _load(self) -> Dict:
        if self.log_path.exists():
            with open(self.log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'signals': [], 'summary': {}}

    def save(self):
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _make_key(self, fund_code: str, signal_type: str) -> str:
        return f"{fund_code}:{signal_type}"

    def should_send(self, fund_code: str, signal_type: str, dedup_window_hours: int = 24) -> bool:
        """判断是否应该推送（去重）"""
        key = self._make_key(fund_code, signal_type)
        cutoff = time.time() - dedup_window_hours * 3600

        for entry in reversed(self.data.get('signals', [])):
            if entry.get('key') == key and entry.get('timestamp', 0) > cutoff:
                return False  # 窗口内已推送过

        return True

    def record(self, fund_code: str, signal_type: str, content: str):
        """记录推送"""
        key = self._make_key(fund_code, signal_type)
        self.data.setdefault('signals', []).append({
            'key': key,
            'fund_code': fund_code,
            'signal_type': signal_type,
            'content': content,
            'timestamp': time.time(),
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        self.save()

    def get_recent(self, hours: int = 24) -> List[Dict]:
        """获取最近 N 小时的信号"""
        cutoff = time.time() - hours * 3600
        return [s for s in self.data.get('signals', []) if s.get('timestamp', 0) > cutoff]

    def cleanup(self, days: int = 7):
        """清理 N 天前的日志"""
        cutoff = time.time() - days * 86400
        self.data['signals'] = [s for s in self.data.get('signals', []) if s.get('timestamp', 0) > cutoff]
        self.save()


# ============================================================
# 数据获取层
# ============================================================

class FundDataFetcher:
    """基金数据获取（复用 data_layer）"""

    def __init__(self):
        try:
            from data_layer import FundAPI
            self.fund_api = FundAPI()
        except ImportError:
            self.fund_api = None

    def get_fund_detail(self, fund_code: str) -> Dict:
        """获取基金详情"""
        if self.fund_api:
            try:
                return self.fund_api.get_detail(fund_code)
            except:
                pass
        return {}

    def get_performance(self, fund_code: str) -> Dict:
        """获取业绩"""
        if self.fund_api:
            try:
                return self.fund_api.get_performance(fund_code)
            except:
                pass
        return {}

    def get_holdings(self, fund_code: str) -> Dict:
        """获取持仓"""
        if self.fund_api:
            try:
                return self.fund_api.get_holdings(fund_code)
            except:
                pass
        return {}

    def get_nav_history(self, fund_code: str, days: int = 30) -> List[Dict]:
        """获取净值历史"""
        if self.fund_api:
            try:
                return self.fund_api.get_nav_history(fund_code, days)
            except:
                pass
        return []


# ============================================================
# 信号检测引擎
# ============================================================

class SignalDetector:
    """信号检测器"""

    def __init__(self, fetcher: FundDataFetcher):
        self.fetcher = fetcher

    def detect_all(self, fund_code: str, fund_name: str, signals: List[str], thresholds: Dict) -> List[Dict]:
        """检测所有信号"""
        results = []

        signal_map = {
            '季报': self._detect_quarterly,
            '经理': self._detect_manager_change,
            '规模': self._detect_size_change,
            '波动': lambda c, t: self._detect_volatility(c, t),
            '风格': self._detect_style_drift,
            '买入信号': lambda c, t: self._detect_buy_signal(c, t),
            '卖出信号': lambda c, t: self._detect_sell_signal(c, t),
        }

        for signal_type in signals:
            detector = signal_map.get(signal_type)
            if detector:
                try:
                    result = detector(fund_code, thresholds)
                    if result:
                        results.append(result)
                except Exception as e:
                    results.append({
                        'type': signal_type,
                        'fund_code': fund_code,
                        'fund_name': fund_name,
                        'status': 'error',
                        'error': str(e)
                    })

        return results

    # --- 季报发布 ---
    def _detect_quarterly(self, fund_code: str, thresholds: Dict) -> Optional[Dict]:
        """检测季报发布"""
        holdings = self.fetcher.get_holdings(fund_code)
        report_date = holdings.get('report_date', '')

        if not report_date:
            return None

        # 检查报告日期是否比上次更新
        try:
            report_dt = datetime.strptime(str(report_date), '%Y-%m-%d')
            days_since = (datetime.now() - report_dt).days

            if days_since <= 7:  # 7 天内发布的
                return {
                    'type': '季报',
                    'fund_code': fund_code,
                    'fund_name': holdings.get('fund_name', ''),
                    'status': 'signal',
                    'severity': 'info',
                    'content': f"📊 季报发布\n基金：{holdings.get('fund_name', fund_code)}\n报告日期：{report_date}\n重仓股数量：{len(holdings.get('stocks', []))}"
                }
        except:
            pass

        return None

    # --- 经理变更 ---
    def _detect_manager_change(self, fund_code: str, thresholds: Dict) -> Optional[Dict]:
        """检测基金经理变更"""
        detail = self.fetcher.get_fund_detail(fund_code)
        current_manager = detail.get('manager_name', '')

        # 从缓存获取上次经理
        cache_key = f"manager_{fund_code}"
        last_manager = self._read_cache(cache_key)

        if last_manager and last_manager != current_manager:
            return {
                'type': '经理',
                'fund_code': fund_code,
                'fund_name': detail.get('fund_name', ''),
                'status': 'signal',
                'severity': 'high',
                'content': f"👤 基金经理变更\n基金：{detail.get('fund_name', fund_code)}\n原经理：{last_manager}\n新任：{current_manager}\n⚠️ 经理变更可能影响基金风格"
            }

        # 首次记录
        if not last_manager and current_manager:
            self._write_cache(cache_key, current_manager)

        return None

    # --- 规模变化 ---
    def _detect_size_change(self, fund_code: str, thresholds: Dict) -> Optional[Dict]:
        """检测基金规模大幅变化"""
        detail = self.fetcher.get_fund_detail(fund_code)
        current_size = detail.get('fund_size', 0)

        if not current_size:
            return None

        cache_key = f"size_{fund_code}"
        last_size = self._read_cache(cache_key)

        threshold = thresholds.get('规模变化阈值', 30)

        if last_size and last_size > 0:
            change_pct = (current_size - last_size) / last_size * 100

            if abs(change_pct) > threshold:
                direction = '增长' if change_pct > 0 else '下降'
                return {
                    'type': '规模',
                    'fund_code': fund_code,
                    'fund_name': detail.get('fund_name', ''),
                    'status': 'signal',
                    'severity': 'medium',
                    'content': f"📈 基金规模{direction}\n基金：{detail.get('fund_name', fund_code)}\n当前规模：{current_size} 亿\n上次规模：{last_size} 亿\n变化：{change_pct:+.1f}%（阈值：{threshold}%）"
                }

        self._write_cache(cache_key, current_size)
        return None

    # --- 业绩波动 ---
    def _detect_volatility(self, fund_code: str, thresholds: Dict) -> Optional[Dict]:
        """检测业绩异常波动"""
        perf = self.fetcher.get_performance(fund_code)
        returns = perf.get('returns', {})

        # 检查最新日涨跌
        daily_return = returns.get('Z', 0)  # 近 1 月收益率作为代理

        threshold = thresholds.get('波动阈值', 5)

        # 用近 1 月收益率判断（真实场景应检查日涨跌）
        if isinstance(daily_return, (int, float)) and abs(daily_return) > threshold:
            return {
                'type': '波动',
                'fund_code': fund_code,
                'fund_name': perf.get('fund_name', ''),
                'status': 'signal',
                'severity': 'medium',
                'content': f"📉 业绩波动\n基金：{perf.get('fund_name', fund_code)}\n近 1 月收益：{daily_return:+.2f}%\n阈值：{threshold}%\n建议关注波动原因"
            }

        return None

    # --- 风格漂移 ---
    def _detect_style_drift(self, fund_code: str, thresholds: Dict) -> Optional[Dict]:
        """检测风格漂移"""
        holdings = self.fetcher.get_holdings(fund_code)

        cache_key = f"holdings_{fund_code}"
        last_holdings = self._read_cache(cache_key)

        current_stocks = holdings.get('stocks', [])
        current_names = set(s.get('name', '') for s in current_stocks[:10])

        if last_holdings:
            last_names = set(last_holdings)
            if current_names:
                overlap = len(current_names & last_names) / max(len(current_names), 1)
                change_pct = (1 - overlap) * 100

                if change_pct > 40:  # 重仓股变化超过 40%
                    return {
                        'type': '风格',
                        'fund_code': fund_code,
                        'fund_name': holdings.get('fund_name', ''),
                        'status': 'signal',
                        'severity': 'high',
                        'content': f"🎭 风格漂移检测\n基金：{holdings.get('fund_name', fund_code)}\n重仓股变化：{change_pct:.0f}%\n重合度：{overlap*100:.0f}%\n⚠️ 大幅调仓可能意味着风格漂移"
                    }

        self._write_cache(cache_key, list(current_names))
        return None

    # --- 买入信号 ---
    def _detect_buy_signal(self, fund_code: str, thresholds: Dict) -> Optional[Dict]:
        """检测买入信号"""
        try:
            from qieman_client import QiemanClient
            client = QiemanClient()
            signal_report = client.generate_signal(fund_code)

            signal = signal_report.get('signal', '')
            confidence = signal_report.get('confidence', 0)
            buy_threshold = thresholds.get('买入信号阈值', 70)

            if signal == '买入' and confidence >= buy_threshold:
                return {
                    'type': '买入信号',
                    'fund_code': fund_code,
                    'fund_name': signal_report.get('basic_info', {}).get('fund_name', ''),
                    'status': 'signal',
                    'severity': 'info',
                    'content': f"🟢 买入信号\n基金：{signal_report.get('basic_info', {}).get('fund_name', fund_code)}\n信号：买入\n置信度：{confidence}%\n理由：{signal_report.get('reason', '')}"
                }
        except Exception as e:
            pass

        return None

    # --- 卖出信号 ---
    def _detect_sell_signal(self, fund_code: str, thresholds: Dict) -> Optional[Dict]:
        """检测卖出信号"""
        try:
            from qieman_client import QiemanClient
            client = QiemanClient()
            signal_report = client.generate_signal(fund_code)

            signal = signal_report.get('signal', '')
            confidence = signal_report.get('confidence', 0)
            sell_threshold = thresholds.get('卖出信号阈值', 30)

            if signal in ['卖出', '观察'] and confidence >= sell_threshold:
                return {
                    'type': '卖出信号',
                    'fund_code': fund_code,
                    'fund_name': signal_report.get('basic_info', {}).get('fund_name', ''),
                    'status': 'signal',
                    'severity': 'high',
                    'content': f"🔴 卖出信号\n基金：{signal_report.get('basic_info', {}).get('fund_name', fund_code)}\n信号：{signal}\n置信度：{confidence}%\n理由：{signal_report.get('reason', '')}"
                }
        except Exception as e:
            pass

        return None

    # --- 缓存工具 ---
    def _read_cache(self, key: str):
        cache_file = CACHE_DIR / f"{key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f).get('value')
            except:
                pass
        return None

    def _write_cache(self, key: str, value):
        cache_file = CACHE_DIR / f"{key}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({'value': value, 'updated': datetime.now().isoformat()}, f, ensure_ascii=False)


# ============================================================
# 飞书推送
# ============================================================

class FeishuNotifier:
    """飞书通知推送"""

    def __init__(self):
        self.enabled = True

    def send_signal(self, signal: Dict, settings: Dict) -> bool:
        """发送信号通知（通过消息工具）"""
        # 检查免打扰时段
        if self._is_dnd(settings):
            return False

        # 构建消息
        message = self._build_message(signal)

        # 输出到 stdout（由调用方处理推送）
        print(json.dumps({
            'action': 'send_message',
            'message': message,
            'signal': signal
        }, ensure_ascii=False))

        return True

    def send_summary(self, signals: List[Dict], date: str, settings: Dict) -> bool:
        """发送每日摘要"""
        if not signals:
            return False

        lines = [f"📋 基金信号日报 {date}", ""]

        for s in signals:
            severity_emoji = {'high': '🔴', 'medium': '🟡', 'info': '🔵'}.get(s.get('severity', 'info'), '⚪')
            lines.append(f"{severity_emoji} {s.get('fund_name', s.get('fund_code', ''))} - {s.get('type', '')}")
            lines.append(f"  {s.get('content', '')}")
            lines.append("")

        message = '\n'.join(lines)

        print(json.dumps({
            'action': 'send_message',
            'message': message,
            'type': 'summary'
        }, ensure_ascii=False))

        return True

    def _build_message(self, signal: Dict) -> str:
        """构建消息"""
        severity_emoji = {'high': '🔴', 'medium': '🟡', 'info': '🔵'}.get(signal.get('severity', 'info'), '⚪')
        return f"{severity_emoji} {signal.get('content', '')}\n\n> 基金代码：{signal.get('fund_code', '')}\n> 信号类型：{signal.get('type', '')}\n> 严重度：{signal.get('severity', '')}"

    def _is_dnd(self, settings: Dict) -> bool:
        """检查是否在免打扰时段"""
        dnd = settings.get('免打扰时段', '22:00-08:00')
        try:
            start_str, end_str = dnd.split('-')
            now = datetime.now()
            start = datetime.strptime(start_str, '%H:%M').time()
            end = datetime.strptime(end_str, '%H:%M').time()
            current = now.time()

            if start > end:  # 跨天（如 22:00-08:00）
                return current >= start or current <= end
            else:
                return start <= current <= end
        except:
            return False


# ============================================================
# 主流程
# ============================================================

def run_check(fund_code: str = None, dry_run: bool = False, summary: bool = False):
    """主检查流程"""

    # 1. 加载配置
    wm = WatchlistManager()
    sl = SignalLog()
    fetcher = FundDataFetcher()
    detector = SignalDetector(fetcher)
    notifier = FeishuNotifier()
    settings = wm.get_settings()

    # 2. 摘要模式
    if summary:
        today = datetime.now().strftime('%Y-%m-%d')
        recent = sl.get_recent(hours=24)
        notifier.send_summary(recent, today, settings)
        return

    # 3. 获取监控列表
    items = wm.get_enabled(fund_code)

    if not items:
        print("📭 无启用的监控项")
        return

    print(f"🔍 检查 {len(items)} 只基金...")

    # 4. 逐只检查
    all_signals = []
    for item in items:
        code = item['code']
        name = item.get('name', code)
        signals = item.get('signals', [])
        thresholds = item.get('thresholds', {})

        print(f"  检查 {name} ({code})...")
        detected = detector.detect_all(code, name, signals, thresholds)

        for signal in detected:
            if signal.get('status') == 'signal':
                # 去重检查
                if sl.should_send(code, signal['type']):
                    if not dry_run:
                        notifier.send_signal(signal, settings)
                        sl.record(code, signal['type'], signal.get('content', ''))
                        print(f"    📤 推送：{signal['type']}")
                    else:
                        print(f"    📋 检测到（dry-run）：{signal['type']} - {signal.get('content', '')[:50]}...")
                    all_signals.append(signal)
                else:
                    print(f"    ⏭️ 跳过（去重）：{signal['type']}")

    # 5. 清理旧日志
    sl.cleanup(days=7)

    # 6. 总结
    if all_signals:
        print(f"\n✅ 检查完成，发现 {len(all_signals)} 个信号")
    else:
        print(f"\n✅ 检查完成，无新信号")


def add_watch(code: str, name: str, signals: List[str] = None):
    """添加监控"""
    wm = WatchlistManager()
    wm.add(code, name, signals)
    print(f"✅ 已添加监控：{name} ({code})")


def remove_watch(code: str):
    """移除监控"""
    wm = WatchlistManager()
    wm.remove(code)
    print(f"✅ 已移除监控：{code}")


def list_watch():
    """列出监控"""
    wm = WatchlistManager()
    items = wm.get_enabled()

    if not items:
        print("📭 无监控项")
        return

    print(f"📋 监控列表（{len(items)} 只）：")
    for item in items:
        signals = ', '.join(item.get('signals', []))
        print(f"  {item.get('name', '')} ({item['code']})")
        print(f"    信号：{signals}")


# ============================================================
# CLI 入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Fund-Signal-Checker v2.1.0")
        print("")
        print("用法：")
        print("  python signal_checker.py              # 检查所有基金")
        print("  python signal_checker.py <基金代码>    # 检查指定基金")
        print("  python signal_checker.py --dry-run     # 模拟运行")
        print("  python signal_checker.py --summary     # 每日摘要")
        print("  python signal_checker.py --list        # 列出监控")
        print("  python signal_checker.py --add <代码> <名称> [信号1,信号2...]  # 添加监控")
        print("  python signal_checker.py --remove <代码>  # 移除监控")
        print("")
        print("示例：")
        print("  python signal_checker.py")
        print("  python signal_checker.py 005827")
        print("  python signal_checker.py --dry-run")
        print("  python signal_checker.py --add 163406 兴全合润")
        print("  python signal_checker.py --remove 005827")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == '--dry-run':
        run_check(dry_run=True)
    elif cmd == '--summary':
        run_check(summary=True)
    elif cmd == '--list':
        list_watch()
    elif cmd == '--add':
        if len(sys.argv) < 4:
            print("错误：请提供基金代码和名称")
            sys.exit(1)
        code = sys.argv[2]
        name = sys.argv[3]
        signals = sys.argv[4].split(',') if len(sys.argv) > 4 else None
        add_watch(code, name, signals)
    elif cmd == '--remove':
        if len(sys.argv) < 3:
            print("错误：请提供基金代码")
            sys.exit(1)
        remove_watch(sys.argv[2])
    elif cmd.startswith('--'):
        print(f"未知参数：{cmd}")
        sys.exit(1)
    else:
        # 当作基金代码
        run_check(fund_code=cmd)


if __name__ == '__main__':
    main()
