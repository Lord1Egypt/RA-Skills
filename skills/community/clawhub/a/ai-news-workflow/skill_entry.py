from __future__ import annotations

import argparse
import shutil
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from run import main as run_main


def _ensure_dirs(root: Path) -> None:
    for d in ["input", "output", "data", "logs", "templates"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "output" / "excel").mkdir(parents=True, exist_ok=True)
    (root / "output" / "word").mkdir(parents=True, exist_ok=True)


def _ensure_config(root: Path, config_name_or_path: str) -> Path:
    """
    确保配置文件存在：
    - 如果用户指定的 config 存在，直接用
    - 否则尝试从 config.default.yaml 复制到 root/config.yaml
    """
    cfg = Path(config_name_or_path)
    if not cfg.is_absolute():
        cfg = (root / cfg).resolve()

    if cfg.exists():
        return cfg

    default_cfg = root / "config.default.yaml"
    target_cfg = root / "config.yaml"
    if default_cfg.exists():
        shutil.copy(default_cfg, target_cfg)
        return target_cfg

    raise FileNotFoundError(f"未找到配置文件: {cfg}，且不存在 {default_cfg}")


def main() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml", help="配置文件名或路径（默认 config.yaml）")
    parser.add_argument("--init", action="store_true", help="仅初始化目录与默认配置，不执行主流程")

    # 模型可选
    parser.add_argument("--model", default="", help="LLM模型名（例如 doubao-seed-2-0-mini-260215）。留空则使用配置。")

    # 抓取回看天数（覆盖 config）
    parser.add_argument("--rss-lookback-days", type=int, default=0, help="RSS抓取回看天数（>0 生效，覆盖配置）")
    parser.add_argument("--web-lookback-days", type=int, default=0, help="网页抓取回看天数（>0 生效，覆盖配置）")

    # 统计窗口（覆盖 config）
    parser.add_argument("--window-mode", default="", help="统计窗口模式：previous_day 或 rolling_days（留空则用配置）")
    parser.add_argument("--start-hour", type=int, default=-1, help="previous_day 模式：起始小时（0-23，-1表示不覆盖）")
    parser.add_argument("--end-hour", type=int, default=-1, help="previous_day 模式：结束小时（0-23，-1表示不覆盖）")
    parser.add_argument("--window-lookback-days", type=int, default=0, help="rolling_days 模式：回看天数（>0 生效，覆盖配置）")

    args = parser.parse_args()

    root = PROJECT_ROOT
    print("[skill] start")
    print("[skill] PROJECT_ROOT =", root)

    _ensure_dirs(root)
    cfg_path = _ensure_config(root, args.config)
    print("[skill] config =", cfg_path)

    if args.init:
        print("[skill] init only, done")
        return f"初始化完成：{cfg_path}"

    print("[skill] running workflow...")

    # 只传 run.py 能接收的参数；init 不传给 run_main
    run_main(
        config_path=str(cfg_path),
        model=(args.model.strip() or None),
        rss_lookback_days=(args.rss_lookback_days if args.rss_lookback_days > 0 else None),
        web_lookback_days=(args.web_lookback_days if args.web_lookback_days > 0 else None),
        window_mode=(args.window_mode.strip() or None),
        start_hour=(args.start_hour if args.start_hour >= 0 else None),
        end_hour=(args.end_hour if args.end_hour >= 0 else None),
        window_lookback_days=(args.window_lookback_days if args.window_lookback_days > 0 else None),
    )

    print("[skill] workflow done")
    return "运行完成"


if __name__ == "__main__":
    main()