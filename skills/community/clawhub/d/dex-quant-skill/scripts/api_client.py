"""
DEX Quant Server API 客户端 — 信号驱动架构（含 Token 认证）

Skill 端调用流程:
  1. strategy-maker 生成策略脚本
  2. 本地运行脚本，拿到信号列表
  3. 调 run_backtest() 把信号发给 Server（自动携带 Token）
  4. Server 拉 K 线（带缓存）+ 回测引擎回放信号
  5. 返回绩效结果，展示给用户

认证:
  - 首次使用自动生成随机设备ID并注册，获取 Token（同时最多 3 个策略监控）
  - Token 缓存在 skill 目录下的 .auth.json
  - 所有请求自动携带 X-Token 头

用法:
    client = QuantAPIClient("https://quant.supersafeclaw.com")
    result = client.run_backtest(
        strategy_name="BTC MACD 策略",
        symbol="BTCUSDT",
        timeframe="1h",
        start_date="2024-01-01",
        end_date="2024-12-31",
        signals=[...],
    )
    client.print_metrics(result)
"""

from __future__ import annotations

import os
import time as _time
from pathlib import Path
from typing import Optional

import httpx
from loguru import logger

from machine_auth import MachineAuth
from server_config import resolve_server_url
API_PREFIX = "/api/v1"


class QuantAPIClient:
    """DEX Quant Server HTTP 客户端（自动认证）"""

    def __init__(self, server_url: str | None = None, timeout: float = 300.0):
        self.server_url = resolve_server_url(server_url)
        self.base_url = self.server_url.rstrip("/") + API_PREFIX
        self._client = httpx.Client(timeout=timeout)

        self._auth = MachineAuth(self.server_url)
        self._token = self._auth.register_or_load()

    def _headers(self) -> dict:
        return {"X-Token": self._token}

    # ═══════════════ 回测 ═══════════════

    def run_backtest(
        self,
        strategy_name: str,
        symbol: str,
        timeframe: str,
        start_date: str,
        end_date: str,
        signals: list[dict],
        strategy_id: str = "",
        initial_capital: float = 100_000.0,
        leverage: int = 1,
        fee_rate: float = 0.0005,
        slippage_bps: float = 5.0,
        margin_mode: str = "isolated",
        direction: str = "long_short",
    ) -> dict:
        """
        提交信号驱动回测。

        参数:
            strategy_name: 策略名称
            symbol: 交易对 (BTCUSDT)
            timeframe: K 线周期 (15m / 1h / 2h / 1d)
            start_date: 开始日期 "YYYY-MM-DD"
            end_date: 结束日期 "YYYY-MM-DD"
            signals: 信号列表，每个信号包含:
                timestamp, symbol, action (buy/sell/close),
                direction (long/short), confidence, reason,
                price_at_signal, suggested_stop_loss, suggested_take_profit

        返回:
            BacktestResponse 字典:
                backtest_id, status, metrics, trades, equity_curve, conclusion
        """
        payload = {
            "strategy_name": strategy_name,
            "strategy_id": strategy_id,
            "symbol": symbol,
            "timeframe": timeframe,
            "start_date": start_date,
            "end_date": end_date,
            "signals": signals,
            "initial_capital": initial_capital,
            "leverage": leverage,
            "fee_rate": fee_rate,
            "slippage_bps": slippage_bps,
            "margin_mode": margin_mode,
            "direction": direction,
        }

        logger.info(
            "提交回测 | {} {} {} | {} → {} | {} 个信号",
            strategy_name, symbol, timeframe, start_date, end_date, len(signals),
        )
        resp = self._client.post(f"{self.base_url}/backtest/run", json=payload, headers=self._headers())
        resp.raise_for_status()
        result = resp.json()

        status = result.get("status", "unknown")
        if status == "completed":
            metrics = result.get("metrics", {})
            logger.info(
                "回测完成 | 收益={:.2%} | Sharpe={:.2f} | 回撤={:.2%} | "
                "交易={} | 结论={}",
                metrics.get("total_return_pct", 0),
                metrics.get("sharpe_ratio", 0),
                abs(metrics.get("max_drawdown_pct", 0)),
                metrics.get("total_trades", 0),
                result.get("conclusion", ""),
            )
        else:
            logger.error("回测失败 | {}", result.get("error"))

        return result

    def get_backtest(self, backtest_id: str) -> dict:
        """查询已保存的回测结果"""
        resp = self._client.get(f"{self.base_url}/backtest/{backtest_id}", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_trades(self, backtest_id: str) -> dict:
        """获取回测交易记录"""
        resp = self._client.get(f"{self.base_url}/backtest/{backtest_id}/trades", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_equity(self, backtest_id: str) -> dict:
        """获取权益曲线"""
        resp = self._client.get(f"{self.base_url}/backtest/{backtest_id}/equity", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    # ═══════════════ 数据 ═══════════════

    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_date: str,
        end_date: str,
        exchange: str = "binance",
    ) -> list[dict]:
        """获取 K 线数据（Server 端带缓存，同币同周期不重复下载）"""
        payload = {
            "symbol": symbol,
            "interval": interval,
            "start_date": start_date,
            "end_date": end_date,
            "exchange": exchange,
        }
        resp = self._client.post(f"{self.base_url}/data/klines", json=payload, headers=self._headers())
        resp.raise_for_status()
        result = resp.json()
        logger.info("K线 | {} {} | {} 条", symbol, interval, result.get("rows", 0))
        return result.get("data", [])

    def list_symbols(self, exchange: str = "binance") -> list[str]:
        """列出可用交易对"""
        resp = self._client.get(f"{self.base_url}/data/symbols", params={"exchange": exchange}, headers=self._headers())
        resp.raise_for_status()
        return resp.json().get("symbols", [])

    # ═══════════════ 策略 ═══════════════

    def save_strategy(
        self,
        name: str,
        script_content: str = "",
        description: str = "",
        symbol: str = "BTCUSDT",
        timeframe: str = "1h",
        direction: str = "long_short",
        version: str = "v1.0",
        tags: list[str] = None,
    ) -> dict:
        """保存策略到 Server（含脚本源码）"""
        payload = {
            "name": name,
            "description": description,
            "script_content": script_content,
            "symbol": symbol,
            "timeframe": timeframe,
            "direction": direction,
            "version": version,
            "tags": tags or [],
        }
        resp = self._client.post(f"{self.base_url}/strategies/", json=payload, headers=self._headers())
        resp.raise_for_status()
        result = resp.json()
        logger.info("策略已保存 | {} ({})", name, result.get("strategy_id", ""))
        return result

    def list_strategies(self) -> list[dict]:
        """列出所有策略"""
        resp = self._client.get(f"{self.base_url}/strategies/", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_strategy(self, strategy_id: str) -> dict:
        """获取策略详情（含脚本源码）"""
        resp = self._client.get(f"{self.base_url}/strategies/{strategy_id}", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    # ═══════════════ 信号 ═══════════════

    def save_signals(self, strategy_id: str, signals: list[dict]) -> dict:
        """批量保存信号到 Server"""
        resp = self._client.post(
            f"{self.base_url}/signals/batch",
            json=signals,
            params={"strategy_id": strategy_id},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()

    def query_signals(
        self,
        strategy_id: str = None,
        symbol: str = None,
        start_date: str = None,
        end_date: str = None,
        limit: int = 200,
    ) -> dict:
        """查询信号"""
        payload = {"limit": limit}
        if strategy_id:
            payload["strategy_id"] = strategy_id
        if symbol:
            payload["symbol"] = symbol
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        resp = self._client.post(f"{self.base_url}/signals/query", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    # ═══════════════ 服务器端执行回测 ═══════════════

    def submit_backtest(
        self,
        script_content: str,
        strategy_name: str,
        symbol: str = "BTCUSDT",
        timeframe: str = "4h",
        start_date: str = "",
        end_date: str = "",
        strategy_id: str = "",
        initial_capital: float = 100_000.0,
        leverage: int = 1,
        fee_rate: float = 0.0005,
        slippage_bps: float = 5.0,
        margin_mode: str = "isolated",
        direction: str = "long_short",
    ) -> str:
        """
        提交回测任务，立即返回 job_id（不等待结果）。

        用 check_backtest(job_id) 查看进度和获取结果。
        """
        payload = {
            "script_content": script_content,
            "strategy_name": strategy_name,
            "strategy_id": strategy_id,
            "symbol": symbol,
            "timeframe": timeframe,
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "leverage": leverage,
            "fee_rate": fee_rate,
            "slippage_bps": slippage_bps,
            "margin_mode": margin_mode,
            "direction": direction,
        }

        resp = self._client.post(
            f"{self.base_url}/backtest/submit",
            json=payload,
            headers=self._headers(),
        )
        resp.raise_for_status()
        job_id = resp.json()["job_id"]
        print(
            f"📋 回测已提交: {job_id} | {strategy_name} ({symbol} {timeframe}, {start_date} → {end_date})",
            flush=True,
        )
        return job_id

    def check_backtest(self, job_id: str) -> dict:
        """
        查询回测任务状态。返回 dict，status 为 running/completed/failed。

        completed 时包含完整的 metrics/trades/equity_curve。
        """
        resp = self._client.get(
            f"{self.base_url}/backtest/job/{job_id}",
            headers=self._headers(),
        )
        resp.raise_for_status()
        job = resp.json()

        status = job.get("status", "running")
        stage = job.get("stage_label", "")
        progress = job.get("progress_pct", 0)
        elapsed_s = job.get("elapsed_ms", 0) / 1000

        if status == "running":
            print(f"⏳ [{elapsed_s:.0f}s] {stage} ({progress:.0f}%)", flush=True)
        elif status == "completed":
            print(f"✅ 回测完成（耗时 {elapsed_s:.1f}s）", flush=True)
        elif status == "failed":
            print(f"❌ 回测失败: {job.get('error', '未知错误')}", flush=True)

        return job

    def wait_backtest(
        self,
        job_id: str,
        poll_interval: float = 5.0,
        max_running_logs: int | None = None,
    ) -> dict:
        """
        轮询等待回测完成。

        参数:
            job_id: submit_backtest() 返回的任务 ID
            poll_interval: 轮询间隔秒数
            max_running_logs: 最多打印多少条 running 进度，None 表示不限制
        """
        running_logs = 0
        last_stage = None
        last_progress = None

        while True:
            _time.sleep(poll_interval)
            job = self.check_backtest(job_id)
            status = job.get("status")

            if status == "running":
                running_logs += 1
                stage = job.get("stage_label")
                progress = job.get("progress_pct")
                should_stop_logging = (
                    max_running_logs is not None and running_logs >= max_running_logs
                )
                if should_stop_logging and stage == last_stage and progress == last_progress:
                    print("⏳ 回测仍在执行中，继续等待...", flush=True)
                last_stage = stage
                last_progress = progress
                if should_stop_logging:
                    max_running_logs = None
                continue

            if status in ("completed", "failed"):
                return job

    def run_server_backtest(
        self,
        script_content: str,
        strategy_name: str,
        symbol: str = "BTCUSDT",
        timeframe: str = "4h",
        start_date: str = "",
        end_date: str = "",
        strategy_id: str = "",
        initial_capital: float = 100_000.0,
        leverage: int = 1,
        fee_rate: float = 0.0005,
        slippage_bps: float = 5.0,
        margin_mode: str = "isolated",
        direction: str = "long_short",
        poll_interval: float = 5.0,
    ) -> dict:
        """
        提交 + 轮询一步到位（适合支持流式输出的平台）。

        如果平台不支持流式输出（如 OpenClaw），请改用：
        1. job_id = client.submit_backtest(...)
        2. result = client.check_backtest(job_id)
        """
        job_id = self.submit_backtest(
            script_content=script_content,
            strategy_name=strategy_name,
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            strategy_id=strategy_id,
            initial_capital=initial_capital,
            leverage=leverage,
            fee_rate=fee_rate,
            slippage_bps=slippage_bps,
            margin_mode=margin_mode,
            direction=direction,
        )

        result = self.wait_backtest(job_id, poll_interval=poll_interval)
        if result.get("status") == "completed":
            self.print_metrics(result)
        return result

    # ═══════════════ 参数优化 ═══════════════

    def run_optimization(
        self,
        script_content: str,
        params: list[dict],
        strategy_name: str = "",
        symbol: str = "BTCUSDT",
        timeframe: str = "4h",
        start_date: str = "",
        end_date: str = "",
        initial_capital: float = 100_000.0,
        leverage: int = 3,
        fee_rate: float = 0.0005,
        slippage_bps: float = 5.0,
        margin_mode: str = "isolated",
        direction: str = "long_short",
        method: str = "grid",
        max_combinations: int = 200,
        fitness_metric: str = "sharpe_ratio",
        poll_interval: int = 10,
    ) -> dict:
        """
        参数优化 — 提交任务后自动轮询进度，完成后返回结果。

        脚本中用 PARAMS['xxx'] 引用可调参数。
        服务器异步执行，客户端每 poll_interval 秒查一次进度并打印。

        参数:
            params: 参数空间列表，每项:
                {"name": "fast_ema", "type": "int", "low": 5, "high": 30, "step": 5}
                {"name": "sl_pct", "type": "float", "low": 0.01, "high": 0.10, "step": 0.01}
                {"name": "direction", "type": "choice", "choices": ["long", "short"]}
            method: 搜索算法
                "grid"      — 网格穷举（组合数 ≤ 200）
                "genetic"   — 遗传算法（推荐，大空间通用）
                "bayesian"  — 贝叶斯 TPE（少量评估快速收敛）
                "random"    — 随机采样
                "annealing" — 模拟退火
                "pso"       — 粒子群优化
            fitness_metric: 优化目标 (sharpe_ratio / total_return_pct / sortino_ratio / win_rate)
            poll_interval: 轮询间隔秒数（默认10秒）

        返回:
            {status, best_params, best_fitness, results: [{rank, params, fitness, metrics...}]}
        """
        payload = {
            "script_content": script_content,
            "params": params,
            "strategy_name": strategy_name,
            "symbol": symbol,
            "timeframe": timeframe,
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "leverage": leverage,
            "fee_rate": fee_rate,
            "slippage_bps": slippage_bps,
            "margin_mode": margin_mode,
            "direction": direction,
            "method": method,
            "max_combinations": max_combinations,
            "fitness_metric": fitness_metric,
        }

        logger.info(
            "提交参数优化 | {} {} {} | {} → {} | 目标={}",
            strategy_name, symbol, timeframe, start_date, end_date, fitness_metric,
        )

        resp = self._client.post(
            f"{self.base_url}/backtest/optimize",
            json=payload,
            headers=self._headers(),
            timeout=30.0,
        )
        resp.raise_for_status()
        submit_result = resp.json()

        job_id = submit_result.get("job_id")
        total = submit_result.get("total_combinations", 0)
        logger.info("任务已提交 | job_id={} | 共{}种组合", job_id, total)
        print(f"\n⏳ 优化任务已提交 (job_id: {job_id})，共 {total} 种参数组合\n")

        last_completed = 0
        printed_milestones = set()
        milestones = {25, 50, 90}
        interval = 5

        while True:
            _time.sleep(interval)

            try:
                resp = self._client.get(
                    f"{self.base_url}/backtest/optimize/{job_id}",
                    headers=self._headers(),
                    timeout=15.0,
                )
                resp.raise_for_status()
                progress = resp.json()
            except Exception as e:
                logger.warning("查询进度失败: {}", e)
                interval = min(interval * 2, 300)
                continue

            status = progress.get("status", "running")
            completed = progress.get("completed", 0)
            failed = progress.get("failed", 0)
            progress_pct = progress.get("progress_pct", 0)
            best_fitness = progress.get("current_best_fitness", 0)
            best_params = progress.get("current_best_params", {})
            elapsed = progress.get("elapsed_ms", 0)

            for ms in sorted(milestones):
                if ms not in printed_milestones and progress_pct >= ms:
                    params_str = ", ".join(f"{k}={v}" for k, v in best_params.items()) if best_params else "-"
                    print(
                        f"   📊 {ms}% ({completed}/{total}) | "
                        f"最优 fitness={best_fitness:.4f} | "
                        f"{params_str} | "
                        f"{elapsed/1000:.0f}s"
                    )
                    printed_milestones.add(ms)

            if completed > last_completed:
                done_delta = completed - last_completed
                time_per_item = (elapsed / 1000) / max(completed, 1)
                remaining = (total - completed) * time_per_item
                interval = max(5, min(remaining / 4, 300))
            last_completed = completed

            if status == "completed":
                logger.info(
                    "优化完成 | 评估={} 失败={} | 最优fitness={:.4f} | 耗时={}ms",
                    completed - failed, failed, best_fitness, elapsed,
                )
                QuantAPIClient.print_optimization(progress, strategy_name=strategy_name)
                return progress

            if status == "failed":
                logger.error("优化失败: {}", progress.get("error", ""))
                print(f"\n❌ 优化失败: {progress.get('error', '未知错误')}")
                return progress

    def submit_optimization(
        self,
        script_content: str,
        params: list[dict],
        strategy_name: str = "",
        symbol: str = "BTCUSDT",
        timeframe: str = "4h",
        start_date: str = "",
        end_date: str = "",
        initial_capital: float = 100_000.0,
        leverage: int = 3,
        fee_rate: float = 0.0005,
        slippage_bps: float = 5.0,
        margin_mode: str = "isolated",
        direction: str = "long_short",
        method: str = "grid",
        max_combinations: int = 200,
        fitness_metric: str = "sharpe_ratio",
    ) -> str:
        """提交优化任务，立即返回 job_id（不等待结果）。"""
        payload = {
            "script_content": script_content,
            "params": params,
            "strategy_name": strategy_name,
            "symbol": symbol, "timeframe": timeframe,
            "start_date": start_date, "end_date": end_date,
            "initial_capital": initial_capital, "leverage": leverage,
            "fee_rate": fee_rate, "slippage_bps": slippage_bps,
            "margin_mode": margin_mode, "direction": direction,
            "method": method, "max_combinations": max_combinations,
            "fitness_metric": fitness_metric,
        }
        resp = self._client.post(
            f"{self.base_url}/backtest/optimize",
            json=payload, headers=self._headers(), timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()
        job_id = data.get("job_id", "")
        total = data.get("total_combinations", 0)
        print(f"📋 优化任务已提交: {job_id} | {strategy_name} ({symbol} {timeframe}) | {method} {total}组")
        return job_id

    def check_optimization(self, job_id: str, strategy_name: str = "") -> dict:
        """查询优化进度。completed 时自动打印报告和生成图片。"""
        resp = self._client.get(
            f"{self.base_url}/backtest/optimize/{job_id}",
            headers=self._headers(), timeout=15.0,
        )
        resp.raise_for_status()
        result = resp.json()

        status = result.get("status", "running")
        completed = result.get("completed", 0)
        failed = result.get("failed", 0)
        total = result.get("total", 0)
        elapsed = result.get("elapsed_ms", 0) / 1000
        pct = result.get("progress_pct", 0)
        best = result.get("current_best_fitness", 0)

        if status == "running":
            print(f"⏳ [{elapsed:.0f}s] {completed}/{total} 已评估 ({pct:.0f}%) | 最优 fitness={best:.4f}")
        elif status == "completed":
            print(f"✅ 优化完成 ({completed}组, 失败{failed}, 耗时{elapsed:.0f}s)")
            QuantAPIClient.print_optimization(result, strategy_name=strategy_name)
        elif status == "failed":
            print(f"❌ 优化失败: {result.get('error', '')}")

        return result

    @staticmethod
    def print_optimization(result: dict, strategy_name: str = "") -> None:
        """生成优化报告 PNG + caption，和回测报告同一套输出规则。"""
        status = result.get("status", "")
        if status != "completed":
            print(f"优化失败: {result.get('error', '未知错误')}")
            return

        total = result.get("total", result.get("total_combinations", 0))
        completed = result.get("completed", result.get("evaluated", 0))
        failed = result.get("failed", 0)
        elapsed = result.get("elapsed_ms", 0) / 1000
        method = result.get("method", "genetic")
        results = result.get("results", [])
        success = completed - failed
        name = strategy_name or "策略"

        method_names = {
            "grid": "网格穷举", "genetic": "遗传算法", "bayesian": "贝叶斯",
            "random": "随机搜索", "annealing": "模拟退火", "pso": "粒子群",
        }
        method_label = method_names.get(method, method)

        lines = [
            f"🔧 {name} 参数优化报告",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"🧬 算法 {method_label}  ⏱️ 耗时 {elapsed:.0f}s",
            f"📊 评估 {success}/{total}组  ❌ 失败 {failed}组",
        ]

        if not results:
            lines.append("━━━━━━━━━━━━━━━━━━━━")
            lines.append("❌ 无有效结果，所有参数组合均失败")
            caption = "\n".join(lines)
            result["_caption"] = caption
            print(f"\n{caption}")
            return

        top = results[0]
        top_ret = top.get("total_return_pct", 0)
        top_sharpe = top.get("sharpe_ratio", 0)
        top_dd = abs(top.get("max_drawdown_pct", 0))
        top_wr = top.get("win_rate", 0)
        top_trades = top.get("total_trades", 0)
        top_params = top.get("params", {})

        ret_icon = "📈" if top_ret >= 0 else "📉"
        lines.append(f"━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🥇 最优参数:")
        params_str = "  ".join(f"{k}={v}" for k, v in top_params.items())
        lines.append(f"  {params_str}")
        lines.append(f"━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"{ret_icon} 收益 {top_ret:+.2%}  📐 Sharpe {top_sharpe:.2f}")
        lines.append(f"⚡ 回撤 {top_dd:.2%}  🎯 胜率 {top_wr:.0%}  🔄 交易 {top_trades}笔")

        if len(results) > 1:
            lines.append(f"━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"📋 Top {min(len(results), 5)} 排名")
            medals = ["🥇", "🥈", "🥉"]
            for r in results[:5]:
                rank = r.get("rank", 1)
                medal = medals[rank - 1] if rank <= 3 else f"#{rank}"
                ret = r.get("total_return_pct", 0)
                sharpe = r.get("sharpe_ratio", 0)
                dd = abs(r.get("max_drawdown_pct", 0))
                wr = r.get("win_rate", 0)
                trades = r.get("total_trades", 0)
                lines.append(f"  {medal} {ret:+.2%} Sharpe {sharpe:.2f} 回撤 {dd:.2%} 胜率 {wr:.0%} {trades}笔")

        lines.append(f"━━━━━━━━━━━━━━━━━━━━")

        if top_sharpe >= 1.5 and top_ret > 0.1:
            lines.append(f"✅ 优化结果优秀，建议用最优参数回测验证后小仓实盘")
        elif top_sharpe >= 0.5 and top_ret > 0:
            lines.append(f"⚠️ 优化结果尚可，建议用最优参数回测验证")
        elif top_ret > 0:
            lines.append(f"⚠️ 优化结果偏弱（Sharpe {top_sharpe:.2f}），建议改进策略结构后重新优化")
        else:
            lines.append(f"❌ 最优参数仍亏损，建议重新设计策略逻辑")

        lines.append(f"")
        lines.append(f"🔄 下一步: 回复「回测」用最优参数跑完整回测验证")

        caption = "\n".join(lines)
        result["_caption"] = caption

        chart_path = QuantAPIClient._print_optimization_chart(results, name, method_label, success, total, failed, elapsed)
        if chart_path:
            result["_optimization_chart_path"] = chart_path

        print(f"\n{caption}")
        if chart_path:
            print(f"\n[SYSTEM] 图片: {chart_path}")
            print(f"[SYSTEM] 发送图片附件 + 上方 caption，禁止额外文字")

    @staticmethod
    def _print_optimization_chart(results: list, strategy_name: str, method_label: str,
                                   success: int, total: int, failed: int, elapsed: float) -> str | None:
        """生成优化报告 PNG（排名表 + 收益对比条形图）。"""
        if not results:
            return None

        try:
            import matplotlib
        except ImportError:
            return None

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec

        QuantAPIClient._setup_chinese_font()

        BG = "#0f0f1a"
        CARD = "#1c2333"
        WHITE = "#e8e8e8"
        GREEN = "#00d4aa"
        RED = "#ff6b6b"
        GRAY = "#8a8fa0"
        LIGHT = "#c8cad0"
        YELLOW = "#ffd93d"

        top5 = results[:5]
        n = len(top5)

        fig = plt.figure(figsize=(12, max(4, 1.5 + n * 1.2)), facecolor=BG)
        gs = GridSpec(2, 1, figure=fig, height_ratios=[1, max(2, n * 0.8)],
                      hspace=0.25, left=0.05, right=0.68, top=0.92, bottom=0.06)

        ax_hdr = fig.add_subplot(gs[0])
        ax_hdr.set_facecolor(BG)
        ax_hdr.set_xlim(0, 10)
        ax_hdr.set_ylim(0, 3)
        ax_hdr.axis("off")

        safe_name_title = QuantAPIClient._safe_title(strategy_name or "Strategy")
        ax_hdr.text(5, 2.4, f"{safe_name_title} — Optimization", fontsize=14,
                    color=WHITE, ha="center", va="center", fontweight="bold")
        ax_hdr.text(5, 1.5, f"Algorithm: {method_label}  |  Evaluated: {success}/{total}  |  Failed: {failed}  |  Time: {elapsed:.0f}s",
                    fontsize=9, color=GRAY, ha="center", va="center")

        top = top5[0]
        top_ret = top.get("total_return_pct", 0)
        top_sharpe = top.get("sharpe_ratio", 0)
        top_dd = abs(top.get("max_drawdown_pct", 0))
        top_wr = top.get("win_rate", 0)
        top_trades = top.get("total_trades", 0)

        kpi_items = [
            ("Return", f"{top_ret:+.2%}", GREEN if top_ret >= 0 else RED),
            ("Sharpe", f"{top_sharpe:.2f}", GREEN if top_sharpe >= 0.5 else (YELLOW if top_sharpe > 0 else RED)),
            ("MaxDD", f"{top_dd:.2%}", GREEN if top_dd < 0.05 else (YELLOW if top_dd < 0.15 else RED)),
            ("WinRate", f"{top_wr:.0%}", GREEN if top_wr >= 0.5 else (YELLOW if top_wr >= 0.35 else RED)),
            ("Trades", f"{top_trades}", LIGHT),
        ]
        for i, (label, val, clr) in enumerate(kpi_items):
            x = 1 + i * 1.8
            ax_hdr.text(x, 0.6, val, fontsize=12, color=clr, ha="center", va="center", fontweight="bold")
            ax_hdr.text(x, 0.1, label, fontsize=7, color=GRAY, ha="center", va="center")

        ax_bar = fig.add_subplot(gs[1])
        ax_bar.set_facecolor(CARD)

        ranks = list(range(n, 0, -1))
        returns = [r.get("total_return_pct", 0) * 100 for r in top5]
        colors = [GREEN if r >= 0 else RED for r in returns]
        medals = ["#1", "#2", "#3", "#4", "#5"]

        bars = ax_bar.barh(ranks, returns, color=colors, height=0.6, alpha=0.85)

        x_min = min(returns) if returns else 0
        x_max = max(returns) if returns else 0
        x_range = x_max - x_min if x_max != x_min else 1

        for i, r in enumerate(top5):
            sharpe = r.get("sharpe_ratio", 0)
            wr = r.get("win_rate", 0)
            trades = r.get("total_trades", 0)
            params = r.get("params", {})
            params_short = ", ".join(f"{k}={v}" for k, v in list(params.items())[:5])
            if len(params) > 5:
                params_short += " ..."

            ax_bar.text(1.02, ranks[i] + 0.18, f"Sharpe {sharpe:.2f}  WR {wr:.0%}  {trades}t",
                        fontsize=7.5, color=LIGHT, va="center", transform=ax_bar.get_yaxis_transform())
            ax_bar.text(1.02, ranks[i] - 0.18, params_short,
                        fontsize=6.5, color=GRAY, va="center", transform=ax_bar.get_yaxis_transform())

        ax_bar.set_yticks(ranks)
        ax_bar.set_yticklabels([medals[i] for i in range(n)], fontsize=10, color=WHITE, fontweight="bold")
        ax_bar.set_xlabel("Return %", fontsize=9, color=GRAY)
        ax_bar.tick_params(axis="x", colors=GRAY, labelsize=8)
        ax_bar.axvline(x=0, color=GRAY, linewidth=0.5, alpha=0.5)
        ax_bar.spines["top"].set_visible(False)
        ax_bar.spines["right"].set_visible(False)
        ax_bar.spines["bottom"].set_color(GRAY)
        ax_bar.spines["left"].set_color(GRAY)

        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        safe_name = (strategy_name or "optimize").replace(" ", "_").replace("/", "_")[:30]
        ts = int(_time.time())
        filepath = os.path.join(output_dir, f"{safe_name}_opt_{ts}.png")

        fig.savefig(filepath, dpi=150, facecolor=fig.get_facecolor())
        plt.close(fig)
        return filepath

    # ═══════════════ 配额 ═══════════════

    def check_quota(self) -> dict:
        """查询当前机器码的策略配额"""
        return self._auth.check_quota()

    def print_quota(self) -> None:
        """打印配额信息"""
        self._auth.print_quota()

    # ═══════════════ 展示工具 ═══════════════

    @staticmethod
    def print_metrics(result: dict) -> None:
        """生成回测报告图片并打印 caption + 文件路径。

        所有指标、评分、资金曲线合并到一张 PNG 中。
        AI 只需发送这一张图片（附带 caption），无需单独发文字。
        """
        if result.get("status") != "completed":
            print(f"回测失败: {result.get('error', '未知错误')}")
            return

        m = result.get("metrics", {})
        ret = m.get('total_return_pct', 0)
        bal = m.get('final_balance', 0)
        init_cap = m.get('initial_capital', 100000)
        margin_mode = result.get('margin_mode', 'isolated')
        leverage = result.get('leverage', m.get('leverage', 1))
        mode_label = "逐仓" if margin_mode == "isolated" else "全仓"
        evaluation = m.get('evaluation', {})
        grade = evaluation.get('grade', '')
        grade_label = evaluation.get('grade_label', '')
        name = result.get('strategy_name', '策略')

        chart_path = QuantAPIClient._print_equity_chart(
            result.get("equity_curve", []),
            init_cap,
            strategy_name=name,
            metrics=m,
            evaluation=evaluation,
            leverage=leverage,
            mode_label=mode_label,
            trades=result.get("trades", []),
        )
        if chart_path:
            result["_equity_chart_path"] = chart_path

        ret_icon = "📈" if ret >= 0 else "📉"
        lines = [
            f"📊 {name} 回测报告",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"💰 本金 {init_cap:,.0f} → 余额 {bal:,.0f}",
            f"{ret_icon} 收益 {ret:+.2%}  📐 Sharpe {m.get('sharpe_ratio', 0):.2f}  📐 Sortino {m.get('sortino_ratio', 0):.2f}",
            f"⚡ 回撤 {abs(m.get('max_drawdown_pct', 0)):.2%}  🎯 胜率 {m.get('win_rate', 0):.1%}  ⚖️ 盈亏比 {m.get('profit_loss_ratio', 0):.2f}",
            f"🔄 交易 {m.get('total_trades', 0)}笔  🏗️ 杠杆 {leverage}x  📦 仓位 {mode_label}",
        ]
        if m.get('liquidation_count', 0) > 0:
            lines.append(f"💥 爆仓 {m['liquidation_count']} 次")

        conclusion = result.get("conclusion", "")
        conclusion_map = {
            "approved": "✅ 通过，可考虑实盘",
            "paper_trade_first": "⚠️ 先模拟，不建议直接实盘",
            "rejected": "❌ 驳回，建议重新设计策略",
        }

        items = evaluation.get("items", [])
        lines.append(f"━━━━━━━━━━━━━━━━━━━━")
        if items:
            score_val = evaluation.get("score", 0)
            max_score = evaluation.get("max_score", 14)
            lines.append(f"🏆 评分 {score_val}/{max_score}  {grade}级")
            for item in items:
                s = item["score"]
                dot = "🟢" if s == 2 else ("🟡" if s == 1 else "🔴")
                label = "优" if s == 2 else ("及格" if s == 1 else "差")
                lines.append(f"{dot} {item['name']} {item['value']}（{label}）")
            lines.append(f"━━━━━━━━━━━━━━━━━━━━")

        if grade_label:
            conclusion_text = f"[{grade}] {grade_label}"
        elif conclusion:
            conclusion_text = conclusion_map.get(conclusion, conclusion)
        elif ret >= 0 and m.get('sharpe_ratio', 0) > 0.5:
            conclusion_text = "⚠️ 建议先模拟观察"
        elif ret < 0:
            conclusion_text = "❌ 策略亏损，建议优化后重测"
        else:
            conclusion_text = "⚠️ 收益偏低，建议优化参数"

        if ret > 0.2 and m.get('sharpe_ratio', 0) > 1.5:
            advice = "可考虑小仓实盘或优化参数"
        elif ret > 0:
            advice = "建议优化参数后重测"
        elif m.get('total_trades', 0) == 0:
            advice = "没有交易信号，入场条件可能太严格"
        else:
            advice = "可优化参数或重新设计入场/出场逻辑"

        lines.append(f"📋 {conclusion_text}，{advice}")

        trades = result.get("trades", [])
        if trades:
            opens = [t for t in trades if t.get("action") == "open"]
            closes = [t for t in trades if t.get("action") != "open"]
            lines.append(f"")
            lines.append(f"📝 交易摘要 ({len(opens)}开/{len(closes)}平，前5笔)")
            for t in trades[:5]:
                dt = t.get('datetime', '')[:16].replace('T', ' ')
                action = "开" if t.get('action') == 'open' else "平"
                side = "多" if t.get('side') == 'long' else "空"
                price = t.get('price', 0)
                pnl = t.get('pnl', 0)
                pnl_s = f"盈亏{pnl:+.1f}" if t.get('action') != 'open' else ""
                lines.append(f"  {dt} {action}{side} {price:,.1f} {pnl_s}")
            if len(trades) > 5:
                lines.append(f"  ...还有 {len(trades) - 5} 笔")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        if grade == "F" or m.get('total_trades', 0) == 0:
            lines.append("🔄 下一步: 策略逻辑需要重新设计，回复「新策略」重新开始")
        else:
            lines.append("🔧 下一步: 可用服务器算法自动搜索最优参数，请选择:")
            lines.append("  1️⃣ genetic（遗传算法）← 推荐")
            lines.append("  2️⃣ bayesian（贝叶斯）")
            lines.append("  3️⃣ grid（网格穷举）")
            lines.append("  4️⃣ random（随机搜索）")
            lines.append("  5️⃣ annealing（模拟退火）")
            lines.append("  6️⃣ pso（粒子群）")
            lines.append("回复数字或算法名即可开始优化")

        caption = "\n".join(lines)
        result["_caption"] = caption

        print(f"\n{caption}")
        if chart_path:
            print(f"\n[SYSTEM] 图片: {chart_path}")
            print(f"[SYSTEM] 发送图片附件 + 上方 caption，禁止额外文字")

    @staticmethod
    def _print_evaluation(evaluation: dict) -> None:
        """评分卡：逐项展示达标/不达标"""
        if not evaluation or not evaluation.get("items"):
            return

        items = evaluation["items"]
        score = evaluation.get("score", 0)
        max_score = evaluation.get("max_score", 14)
        grade = evaluation.get("grade", "?")

        grade_bar = "█" * score + "░" * (max_score - score)
        print(f"\n  📊 策略评分  {score}/{max_score}  [{grade_bar}]  {grade}级")
        print(f"  {'─' * 52}")
        print(f"  {'指标':<8} {'实际值':>8}  {'得分':>4}  {'标准'}")
        print(f"  {'─' * 52}")

        for item in items:
            s = item["score"]
            icon = "🟢" if s == 2 else ("🟡" if s == 1 else "🔴")
            print(f"  {icon} {item['name']:<6} {item['value']:>8}  {s}/{item['max']}   {item['thresholds']}")

        print(f"  {'─' * 52}")
        print(f"  结论: {evaluation.get('grade_label', '')}")
        print()

    _font_configured = False

    _has_cjk_font = False

    @staticmethod
    def _setup_chinese_font() -> None:
        """配置 matplotlib 中文字体（只执行一次）。"""
        if QuantAPIClient._font_configured:
            return
        QuantAPIClient._font_configured = True

        import matplotlib
        import matplotlib.font_manager as fm

        candidates = [
            "Noto Sans CJK SC", "Noto Sans SC", "Source Han Sans SC",
            "WenQuanYi Micro Hei", "WenQuanYi Zen Hei",
            "SimHei", "Microsoft YaHei", "PingFang SC", "Heiti SC",
            "Arial Unicode MS",
        ]
        available = {f.name for f in fm.fontManager.ttflist}
        for name in candidates:
            if name in available:
                matplotlib.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
                matplotlib.rcParams["axes.unicode_minus"] = False
                QuantAPIClient._has_cjk_font = True
                return

        import subprocess
        try:
            subprocess.run(
                ["apt-get", "install", "-y", "--no-install-recommends", "fonts-noto-cjk"],
                capture_output=True, timeout=30,
            )
            fm._load_fontmanager(try_read_cache=False)
            for name in candidates:
                if name in {f.name for f in fm.fontManager.ttflist}:
                    matplotlib.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
                    matplotlib.rcParams["axes.unicode_minus"] = False
                    QuantAPIClient._has_cjk_font = True
                    return
        except Exception:
            pass

        font_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
        font_file = os.path.join(font_dir, "NotoSansSC-Regular.ttf")
        if os.path.exists(font_file):
            fm.fontManager.addfont(font_file)
            prop = fm.FontProperties(fname=font_file)
            matplotlib.rcParams["font.sans-serif"] = [prop.get_name(), "DejaVu Sans"]
            matplotlib.rcParams["axes.unicode_minus"] = False
            QuantAPIClient._has_cjk_font = True

    @staticmethod
    def _safe_title(text: str) -> str:
        """中文字体不可用时，把中文替换掉避免方框。"""
        if QuantAPIClient._has_cjk_font:
            return text
        import re
        cleaned = re.sub(r'[\u4e00-\u9fff]+', '', text).strip()
        return cleaned if cleaned else "Strategy Report"

    @staticmethod
    def _print_equity_chart(
        equity_curve: list,
        initial_capital: float,
        strategy_name: str = "",
        output_dir: str = "",
        metrics: dict | None = None,
        evaluation: dict | None = None,
        leverage: int = 1,
        mode_label: str = "逐仓",
        trades: list | None = None,
    ) -> str | None:
        """生成完整回测报告图（指标 + 评分 + 资金曲线），返回文件路径。"""
        if not equity_curve or len(equity_curve) < 2:
            return None

        try:
            import matplotlib
        except ImportError:
            print("  ⏳ 正在安装 matplotlib ...", flush=True)
            import subprocess, sys
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-q", "matplotlib"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                import matplotlib
            except Exception:
                print("  ⚠ matplotlib 安装失败，跳过图表生成")
                return None

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.gridspec import GridSpec
        from datetime import datetime

        QuantAPIClient._setup_chinese_font()

        metrics = metrics or {}
        evaluation = evaluation or {}
        trades = trades or []

        equities = [e.get("equity", initial_capital) for e in equity_curve]
        raw_dates = [e.get("datetime", "") for e in equity_curve]
        dates = []
        for d in raw_dates:
            if not d:
                dates = None
                break
            try:
                if "T" in d:
                    dates.append(datetime.fromisoformat(d.replace("Z", "+00:00").replace("+00:00", "")))
                elif len(d) >= 19:
                    dates.append(datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S"))
                elif len(d) >= 10:
                    dates.append(datetime.strptime(d[:10], "%Y-%m-%d"))
                else:
                    dates = None
                    break
            except Exception:
                dates = None
                break
        if dates is None or len(dates) != len(equities):
            dates = list(range(len(equities)))

        hi_val, lo_val = max(equities), min(equities)
        hi_idx = equities.index(hi_val)
        lo_idx = equities.index(lo_val)
        final_val = equities[-1]
        ret_pct = (final_val - initial_capital) / initial_capital * 100

        BG = "#0f0f1a"
        PANEL = "#161b2e"
        CARD = "#1c2333"
        WHITE = "#e8e8e8"
        GREEN = "#00d4aa"
        RED = "#ff6b6b"
        YELLOW = "#ffd93d"
        GRAY = "#8a8fa0"
        LIGHT = "#c8cad0"
        color = GREEN if final_val >= initial_capital else RED

        from matplotlib.patches import FancyBboxPatch

        fig = plt.figure(figsize=(10, 7), facecolor=BG)
        gs = GridSpec(2, 1, figure=fig,
                      height_ratios=[1, 3],
                      hspace=0.15,
                      left=0.10, right=0.94, top=0.96, bottom=0.06)

        title = QuantAPIClient._safe_title(strategy_name or "Backtest Report")
        sign = "+" if ret_pct >= 0 else ""

        # ════════ 顶部: 策略名 + KPI 卡片 ════════
        ax_top = fig.add_subplot(gs[0])
        ax_top.set_facecolor(BG)
        ax_top.axis("off")

        ax_top.text(0.5, 0.88, title, transform=ax_top.transAxes,
                    fontsize=22, color=WHITE, weight="bold", ha="center", va="center")
        ax_top.text(0.5, 0.74, f"{initial_capital:,.0f}  →  {final_val:,.0f}",
                    transform=ax_top.transAxes,
                    fontsize=13, color=GRAY, ha="center", va="center")

        lev_label = "Iso" if mode_label == "逐仓" else "Cross"
        kpi_data = [
            ("Return", f"{sign}{ret_pct:.2f}%", color),
            ("Sharpe", f"{metrics.get('sharpe_ratio', 0):.2f}", LIGHT),
            ("MaxDD", f"{abs(metrics.get('max_drawdown_pct', 0)):.2%}", LIGHT),
            ("WinRate", f"{metrics.get('win_rate', 0):.1%}", LIGHT),
            ("P/L", f"{metrics.get('profit_loss_ratio', 0):.2f}", LIGHT),
            ("Trades", f"{metrics.get('total_trades', 0)}", LIGHT),
            ("Lev", f"{leverage}x {lev_label}", LIGHT),
        ]
        n_kpi = len(kpi_data)
        card_w = 0.88 / n_kpi
        card_x0 = 0.06
        for i, (label, val, val_color) in enumerate(kpi_data):
            cx = card_x0 + i * card_w + card_w / 2
            ax_top.add_patch(FancyBboxPatch(
                (card_x0 + i * card_w + 0.005, 0.12), card_w - 0.01, 0.52,
                transform=ax_top.transAxes,
                boxstyle="round,pad=0.015", facecolor=CARD, edgecolor="#2a3050", linewidth=0.8,
            ))
            ax_top.text(cx, 0.50, val, transform=ax_top.transAxes,
                        fontsize=15, color=val_color, weight="bold", ha="center", va="center")
            ax_top.text(cx, 0.22, label, transform=ax_top.transAxes,
                        fontsize=11, color=GRAY, ha="center", va="center")

        # ════════ 中部: 资金曲线 ════════
        ax_chart = fig.add_subplot(gs[1])
        ax_chart.set_facecolor(PANEL)
        ax_chart.plot(dates, equities, color=color, linewidth=1.8, zorder=3)
        ax_chart.fill_between(dates, equities, initial_capital, alpha=0.12, color=color, zorder=2)
        ax_chart.axhline(y=initial_capital, color=WHITE, linewidth=0.8, linestyle="--", alpha=0.3, zorder=1)

        ax_chart.plot(dates[hi_idx], hi_val, "^", color=GREEN, markersize=10, zorder=4)
        ax_chart.annotate(f"High {hi_val:,.0f}", (dates[hi_idx], hi_val),
                          textcoords="offset points", xytext=(6, 12),
                          fontsize=10, color=GREEN, weight="bold")
        ax_chart.plot(dates[lo_idx], lo_val, "v", color=RED, markersize=10, zorder=4)
        ax_chart.annotate(f"Low {lo_val:,.0f}", (dates[lo_idx], lo_val),
                          textcoords="offset points", xytext=(6, -16),
                          fontsize=10, color=RED, weight="bold")

        ax_chart.tick_params(colors=GRAY, labelsize=10)
        def _y_fmt(x, _):
            if abs(x) >= 1_000_000:
                return f"{x/1_000_000:.1f}M"
            if abs(x) >= 1_000:
                return f"{x/1_000:.1f}K"
            return f"{x:.0f}"
        ax_chart.yaxis.set_major_formatter(plt.FuncFormatter(_y_fmt))
        if isinstance(dates[0], datetime):
            span_days = (dates[-1] - dates[0]).days
            if span_days > 180:
                ax_chart.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            elif span_days > 60:
                ax_chart.xaxis.set_major_locator(mdates.MonthLocator())
            else:
                ax_chart.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            ax_chart.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
            plt.setp(ax_chart.get_xticklabels(), rotation=30, ha="right")
        ax_chart.grid(True, alpha=0.12, color=WHITE)
        for spine in ax_chart.spines.values():
            spine.set_color("#2a3050")

        if not output_dir:
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        safe_name = (strategy_name or "report").replace(" ", "_").replace("/", "_")[:30]
        ts = int(_time.time())
        filepath = os.path.join(output_dir, f"{safe_name}_{ts}.png")

        fig.savefig(filepath, dpi=150, facecolor=fig.get_facecolor())
        plt.close(fig)

        print(f"\n[SYSTEM] 图片已保存: {filepath}")
        return filepath

    @staticmethod
    def _print_trade_details(trades: list, default_leverage: int = 1, mode_label: str = "逐仓", limit: int = 30) -> None:
        """带仓位/杠杆/保证金的交易明细表"""
        if not trades:
            return

        opens = [t for t in trades if t.get("action") == "open"]
        closes = [t for t in trades if t.get("action") != "open"]
        total = len(trades)

        print(f"  📋 交易明细（共 {total} 笔: {len(opens)} 开 / {len(closes)} 平，显示前 {min(limit, total)} 笔）")
        print(f"  {'━' * 88}")
        print(f"  {'#':>3} {'时间':<17} {'动作':<5} {'方向':<5} {'价格':>10} {'数量':>8} {'杠杆':>4} {'仓位模式':<5} {'保证金':>10} {'盈亏':>10}")
        print(f"  {'─' * 88}")

        for t in trades[:limit]:
            tid = t.get('trade_id', 0)
            dt = t.get('datetime', '')[:16]
            action = t.get('action', '')
            side = t.get('side', '')
            price = t.get('price', 0)
            qty = t.get('quantity', 0)
            lev = t.get('leverage', default_leverage)
            pnl = t.get('pnl', 0)

            margin = t.get('margin_used', 0)
            if margin == 0:
                nominal = price * qty
                margin = nominal / lev if lev > 0 else nominal

            t_mode = t.get('margin_mode', '')
            t_mode_label = ("逐仓" if t_mode == "isolated" else "全仓") if t_mode else mode_label

            action_icon = "🟢" if action == "open" else "🔴"
            side_label = "多" if side == "long" else "空"
            pnl_str = f"{pnl:>+10.2f}" if action != "open" else f"{'—':>10}"

            print(
                f"  {tid:>3} {dt:<17} {action_icon}{action:<4} {side_label:<5}"
                f" {price:>10.2f} {qty:>8.4f} {lev:>3}x {t_mode_label:<5}"
                f" {margin:>10.2f} {pnl_str}"
            )

        if total > limit:
            print(f"  ... 还有 {total - limit} 笔未显示")
        print(f"  {'━' * 88}")

    @staticmethod
    def print_trades(result: dict, limit: int = 30) -> None:
        """打印交易记录（复用详细表格）"""
        leverage = result.get("leverage", result.get("metrics", {}).get("leverage", 1))
        margin_mode = result.get("margin_mode", "isolated")
        mode_label = "逐仓" if margin_mode == "isolated" else "全仓"
        QuantAPIClient._print_trade_details(result.get("trades", []), leverage, mode_label, limit)

    @staticmethod
    def print_conclusion(result: dict) -> None:
        """兼容旧调用，现在 print_metrics 已包含结论"""
        pass

    # ═══════════════ 策略监控 (服务器端) ═══════════════

    def start_monitor(
        self,
        script_content: str,
        strategy_name: str = "",
        symbol: str = "BTCUSDT",
        timeframe: str = "4h",
        interval_seconds: int = 14400,
        risk_rules: dict | None = None,
    ) -> dict:
        """
        启动服务器端策略监控（同一用户最多同时 3 个）。

        服务器定时执行策略脚本 generate_signals(mode='live')，
        存储可执行信号供客户端轮询。
        超过 3 个策略需改用本地运行。

        返回: {"job_id": "mon_xxx", "status": "running", "quota_used": 1, ...}
        """
        if risk_rules is None:
            risk_rules = {"min_confidence": 0.6, "max_position_pct": 10.0, "max_concurrent": 3}

        payload = {
            "script_content": script_content,
            "strategy_name": strategy_name,
            "symbol": symbol,
            "timeframe": timeframe,
            "interval_seconds": interval_seconds,
            "risk_rules": risk_rules,
        }

        resp = self._client.post(f"{self.base_url}/monitor/start", json=payload, headers=self._headers())
        if resp.status_code == 429:
            data = resp.json()
            print(f"\n❌ 已有 3 个策略在服务器运行，请先停止一个或改用本地运行")
            print(f"   用 client.list_monitors() 查看运行中的任务")
            return data
        resp.raise_for_status()
        data = resp.json()

        interval_h = interval_seconds / 3600
        print(f"\n{'━' * 40}")
        print(f"  ✅ 监控已启动")
        print(f"  📋 Job ID:  {data['job_id']}")
        print(f"  📊 策略:    {data.get('strategy_name', strategy_name)}")
        print(f"  🪙 交易对:  {symbol}")
        print(f"  ⏱  间隔:    每 {interval_h:.1f}h")
        print(f"  📦 在跑:    {data.get('quota_used', '?')}/3")
        print(f"{'━' * 40}")

        return data

    def stop_monitor(self, job_id: str) -> dict:
        """停止服务器端监控任务。"""
        resp = self._client.post(f"{self.base_url}/monitor/{job_id}/stop", headers=self._headers())
        resp.raise_for_status()
        data = resp.json()

        print(f"\n  ⏹ 监控已停止: {job_id}")
        print(f"  📦 在跑: {data.get('quota_used', '?')}/3")

        return data

    def list_monitors(self) -> dict:
        """列出我的所有监控任务。"""
        resp = self._client.get(f"{self.base_url}/monitor/list", headers=self._headers())
        resp.raise_for_status()
        data = resp.json()

        monitors = data.get("monitors", [])
        quota_used = data.get("quota_used", 0)

        print(f"\n{'━' * 50}")
        print(f"  📡 策略监控列表 | 在跑 {quota_used}/3")
        print(f"{'━' * 50}")

        if not monitors:
            print(f"  （无运行中的监控任务）")
        else:
            for m in monitors:
                status_icon = "🟢" if m["status"] == "running" else "⏹"
                interval_h = m["interval_seconds"] / 3600
                print(
                    f"  {status_icon} {m['job_id']} | {m['strategy_name']:<20} | "
                    f"{m['symbol']} {m['timeframe']} | "
                    f"每{interval_h:.1f}h | "
                    f"信号:{m['total_signals']} | "
                    f"轮次:{m['total_cycles']}"
                )
                if m.get("last_run_at"):
                    print(f"     最后执行: {m['last_run_at']}")

        print(f"{'━' * 50}")
        return data

    def check_monitor(self, job_id: str) -> dict:
        """查看监控任务状态 + 最近信号。"""
        resp = self._client.get(f"{self.base_url}/monitor/{job_id}", headers=self._headers())
        resp.raise_for_status()
        data = resp.json()

        status_icon = "🟢" if data["status"] == "running" else "⏹"
        interval_h = data["interval_seconds"] / 3600

        print(f"\n{'━' * 45}")
        print(f"  {status_icon} 监控状态: {data['status']}")
        print(f"  📋 Job:      {data['job_id']}")
        print(f"  📊 策略:     {data['strategy_name']}")
        print(f"  🪙 交易对:   {data['symbol']} {data['timeframe']}")
        print(f"  ⏱  间隔:     每 {interval_h:.1f}h")
        print(f"  🔄 已执行:   {data['total_cycles']} 轮")
        print(f"  📈 累计信号: {data['total_signals']} 个")
        if data.get("last_run_at"):
            print(f"  🕐 最后执行: {data['last_run_at']}")
        if data.get("last_error"):
            print(f"  ❌ 最后错误: {data['last_error']}")
        print(f"{'━' * 45}")

        last_signals = data.get("last_signals", [])
        if last_signals:
            print(f"\n  📡 最近信号 ({len(last_signals)} 个):")
            for s in last_signals[-5:]:
                action = s.get("action", "?")
                direction = s.get("direction", "?")
                symbol = s.get("symbol", "?")
                confidence = s.get("confidence", 0)
                price = s.get("price_at_signal", 0)
                reason = s.get("reason", "")[:40]
                icon = "🟢" if action == "buy" else "🔴"
                print(f"    {icon} {action} {direction} {symbol} @ {price:.2f} | conf={confidence:.2f} | {reason}")
            print()

        return data

    # ═══════════════ 密钥保险箱 (Vault) ═══════════════

    def vault_setup_link(self) -> dict:
        """
        生成一次性密钥设置链接。

        用户在浏览器中打开该链接，粘贴私钥并提交。
        私钥通过 HTTPS 传输，AES-256-GCM 加密存储在服务器。
        不经过聊天记录。

        返回: {"url": "https://...", "token": "vt_xxx", "expires_in_minutes": 30}
        """
        resp = self._client.post(f"{self.base_url}/vault/setup-link", headers=self._headers())
        resp.raise_for_status()
        data = resp.json()

        print(f"\n{'━' * 50}")
        print(f"  🔐 密钥设置链接已生成")
        print(f"  📎 链接: {data['url']}")
        print(f"  ⏰ 有效期: {data['expires_in_minutes']} 分钟")
        print(f"{'━' * 50}")
        print(f"\n  请在浏览器中打开以上链接，粘贴你的钱包私钥。")
        print(f"  私钥不会出现在聊天记录中。\n")

        return data

    def vault_status(self) -> dict:
        """
        查询密钥存储状态。

        返回: {"has_key": true/false, "network": "mainnet/testnet", ...}
        """
        resp = self._client.get(f"{self.base_url}/vault/status", headers=self._headers())
        resp.raise_for_status()
        data = resp.json()

        if data.get("has_key"):
            net = data.get("network", "mainnet")
            net_icon = "🌐" if net == "mainnet" else "🧪"
            print(f"\n  ✅ 密钥已配置 | {net_icon} {net}")
        else:
            print(f"\n  ❌ 尚未配置密钥")

        return data

    def vault_delete(self) -> dict:
        """删除已存储的密钥。"""
        resp = self._client.delete(f"{self.base_url}/vault/key", headers=self._headers())
        resp.raise_for_status()
        data = resp.json()
        print(f"\n  🗑️ 密钥已删除")
        return data

    # ═══════════════ 生命周期 ═══════════════

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
