#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scheduler.py — 自动续期定时任务

功能：
  - 每天定时检查证书有效期
  - 到期前 RENEW_DAYS 天自动续期
  - 可作为 Windows 计划任务或后台进程运行

用法：
  python scheduler.py          # 启动定时检查（每 24 小时一次）
  python scheduler.py --once   # 只检查一次后退出（适合 Windows 计划任务）
"""

import sys
import time
import logging
import argparse
from pathlib import Path

# 确保能找到同目录模块
sys.path.insert(0, str(Path(__file__).parent))

from main import do_issue, do_status
from acme_client import load_config

log = logging.getLogger("scheduler")

CHECK_INTERVAL_HOURS = 24  # 每 24 小时检查一次


def setup_logging(log_dir: str = None):
    handlers = [logging.StreamHandler()]
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        log_file = Path(log_dir) / "cert-renew.log"
        handlers.append(logging.FileHandler(str(log_file), encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )


def run_check(cfg: dict):
    """执行一次检查"""
    log.info("=== 开始检查证书状态 ===")
    try:
        do_status(cfg)
        do_issue(cfg, force=False)
    except Exception as e:
        log.error("证书检查/续期失败: %s", e, exc_info=True)
    log.info("=== 检查完成 ===")


def main():
    parser = argparse.ArgumentParser(description="SSL 证书自动续期调度器")
    parser.add_argument("--once", action="store_true", help="只运行一次后退出")
    parser.add_argument("--config", default=None, help="配置文件路径")
    parser.add_argument("--log-dir", default=None, help="日志目录")
    args = parser.parse_args()

    setup_logging(args.log_dir)

    cfg = load_config(args.config)

    if args.once:
        run_check(cfg)
        return

    log.info("证书自动续期调度器已启动，每 %d 小时检查一次", CHECK_INTERVAL_HOURS)
    while True:
        run_check(cfg)
        log.info("下次检查时间: %d 小时后", CHECK_INTERVAL_HOURS)
        time.sleep(CHECK_INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    main()
