#!/usr/bin/env python3
"""Budget CLI - Agent Budget Controller."""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import BudgetConfig
from lib.tracker import UsageTracker
from lib.pricing import PricingTable
from lib.reporter import BudgetReporter
from lib.alerts import BudgetAlerts


DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "budget"


def cmd_init(args):
    """Initialize budget tracking."""
    data_dir = Path(args.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    config = BudgetConfig(data_dir)
    config.save_config()
    
    print(f"✅ Initialized budget tracking at {data_dir}")
    print("Next steps:")
    print("  1. Set limits: budget set --daily 3.00 --weekly 15.00 --monthly 50.00")
    print("  2. Log usage: budget log --agent my-agent --model gpt-4o --input-tokens 1000 --output-tokens 500")
    print("  3. Check status: budget status")


def cmd_set(args):
    """Set budget limits."""
    data_dir = Path(args.data_dir)
    config = BudgetConfig(data_dir)
    
    if not any([args.daily, args.weekly, args.monthly]):
        print("Error: Must specify at least one limit (--daily, --weekly, --monthly)")
        sys.exit(1)
    
    if args.agent:
        # Agent-specific limits
        if args.daily is not None:
            config.set_agent_limit(args.agent, "daily", args.daily)
            print(f"✅ Set daily limit for {args.agent}: ${args.daily:.2f}")
        if args.weekly is not None:
            config.set_agent_limit(args.agent, "weekly", args.weekly)
            print(f"✅ Set weekly limit for {args.agent}: ${args.weekly:.2f}")
        if args.monthly is not None:
            config.set_agent_limit(args.agent, "monthly", args.monthly)
            print(f"✅ Set monthly limit for {args.agent}: ${args.monthly:.2f}")
    else:
        # Global limits
        if args.daily is not None:
            config.set_global_limit("daily", args.daily)
            print(f"✅ Set global daily limit: ${args.daily:.2f}")
        if args.weekly is not None:
            config.set_global_limit("weekly", args.weekly)
            print(f"✅ Set global weekly limit: ${args.weekly:.2f}")
        if args.monthly is not None:
            config.set_global_limit("monthly", args.monthly)
            print(f"✅ Set global monthly limit: ${args.monthly:.2f}")


def cmd_log(args):
    """Log API usage."""
    data_dir = Path(args.data_dir)
    
    tracker = UsageTracker(data_dir)
    pricing = PricingTable(data_dir)
    
    # Calculate cost
    cost = pricing.get_cost(args.model, args.input_tokens, args.output_tokens)
    
    # Log usage
    tracker.log_usage(args.agent, args.model, args.input_tokens, args.output_tokens, cost)
    
    if args.verbose:
        print(f"✅ Logged usage for {args.agent}")
        print(f"   Model: {args.model}")
        print(f"   Tokens: {args.input_tokens} in, {args.output_tokens} out")
        print(f"   Cost: ${cost:.4f}")


def cmd_status(args):
    """Show current budget status."""
    data_dir = Path(args.data_dir)
    
    config = BudgetConfig(data_dir)
    tracker = UsageTracker(data_dir)
    reporter = BudgetReporter(tracker, config)
    
    agent = args.agent if hasattr(args, 'agent') else None
    report = reporter.generate_status_report(agent=agent)
    
    print(report)


def cmd_check(args):
    """Check if budget limits are exceeded (exit code 0=ok, 1=exceeded)."""
    data_dir = Path(args.data_dir)
    
    config = BudgetConfig(data_dir)
    tracker = UsageTracker(data_dir)
    reporter = BudgetReporter(tracker, config)
    
    agent = args.agent if hasattr(args, 'agent') else None
    results = reporter.check_limits(agent=agent)
    
    all_ok = all(results.values())
    
    if args.verbose or not all_ok:
        target = f"Agent '{agent}'" if agent else "Global"
        print(f"Budget check for {target}:")
        for period, is_ok in results.items():
            status = "✅ OK" if is_ok else "🚫 EXCEEDED"
            print(f"  {period.capitalize()}: {status}")
    
    sys.exit(0 if all_ok else 1)


def cmd_report(args):
    """Generate detailed report."""
    data_dir = Path(args.data_dir)
    
    config = BudgetConfig(data_dir)
    tracker = UsageTracker(data_dir)
    reporter = BudgetReporter(tracker, config)
    
    agent = args.agent if hasattr(args, 'agent') else None
    report = reporter.generate_period_report(args.period, agent=agent)
    
    print(report)


def cmd_agents(args):
    """List agents."""
    data_dir = Path(args.data_dir)
    
    config = BudgetConfig(data_dir)
    tracker = UsageTracker(data_dir)
    
    # Get configured agents
    configured = set(config.list_agents())
    
    # Get recently active agents
    recent = set(tracker.get_recent_agents(days=args.days))
    
    all_agents = configured | recent
    
    if not all_agents:
        print("No agents found.")
        return
    
    print(f"📋 Agents ({len(all_agents)} total):\n")
    
    for agent in sorted(all_agents):
        markers = []
        if agent in configured:
            markers.append("limits set")
        if agent in recent:
            markers.append(f"active last {args.days}d")
        
        status = " | ".join(markers) if markers else "inactive"
        print(f"  {agent} ({status})")


def cmd_pricing(args):
    """Show or update model pricing."""
    data_dir = Path(args.data_dir)
    pricing = PricingTable(data_dir)
    
    if args.update and args.model:
        # Update specific model
        pricing.update_model(args.model, args.input_price, args.output_price)
        print(f"✅ Updated pricing for {args.model}")
        print(f"   Input: ${args.input_price:.2f} per 1M tokens")
        print(f"   Output: ${args.output_price:.2f} per 1M tokens")
    else:
        # List all models
        models = pricing.list_models()
        
        print("💰 Model Pricing (per 1M tokens):\n")
        print(f"{'Model':<25} {'Input':<10} {'Output':<10}")
        print("-" * 45)
        
        for model, prices in sorted(models.items()):
            print(f"{model:<25} ${prices['input']:<9.2f} ${prices['output']:<9.2f}")


def cmd_reset(args):
    """Reset usage counters (for testing)."""
    print("⚠️  Warning: This would clear usage data.")
    print("   Manual reset: delete ~/.openclaw/budget/usage.jsonl")
    print("   Not implemented to prevent accidental data loss.")
    sys.exit(1)


def cmd_history(args):
    """Show usage history."""
    data_dir = Path(args.data_dir)
    tracker = UsageTracker(data_dir)
    
    # Parse duration
    duration = args.last
    if duration.endswith('d'):
        days = int(duration[:-1])
        start = datetime.now() - timedelta(days=days)
    elif duration.endswith('h'):
        hours = int(duration[:-1])
        start = datetime.now() - timedelta(hours=hours)
    else:
        print(f"Invalid duration format: {duration} (use: 7d, 24h)")
        sys.exit(1)
    
    records = tracker.get_usage(start_date=start)
    
    if not records:
        print(f"No usage records found in last {duration}")
        return
    
    print(f"📜 Usage History (last {duration}, {len(records)} records):\n")
    
    total_cost = 0
    for record in records[-20:]:  # Show last 20
        timestamp = datetime.fromisoformat(record["timestamp"])
        cost = record["cost"]
        total_cost += cost
        
        print(f"{timestamp.strftime('%Y-%m-%d %H:%M')} | "
              f"{record['agent']:<15} | "
              f"{record['model']:<20} | "
              f"${cost:.4f}")
    
    if len(records) > 20:
        print(f"\n... and {len(records) - 20} more records")
    
    print(f"\nTotal: ${total_cost:.2f}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Agent Budget Controller - Track and limit LLM API costs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--data-dir',
        default=DEFAULT_DATA_DIR,
        help=f"Data directory (default: {DEFAULT_DATA_DIR})"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # init
    subparsers.add_parser('init', help='Initialize budget tracking')
    
    # set
    set_parser = subparsers.add_parser('set', help='Set budget limits')
    set_parser.add_argument('--agent', help='Agent name (omit for global limits)')
    set_parser.add_argument('--daily', type=float, help='Daily limit (USD)')
    set_parser.add_argument('--weekly', type=float, help='Weekly limit (USD)')
    set_parser.add_argument('--monthly', type=float, help='Monthly limit (USD)')
    
    # log
    log_parser = subparsers.add_parser('log', help='Log API usage')
    log_parser.add_argument('--agent', required=True, help='Agent name')
    log_parser.add_argument('--model', required=True, help='Model name')
    log_parser.add_argument('--input-tokens', type=int, required=True, help='Input tokens')
    log_parser.add_argument('--output-tokens', type=int, required=True, help='Output tokens')
    log_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    # status
    status_parser = subparsers.add_parser('status', help='Show current status')
    status_parser.add_argument('--agent', help='Filter by agent')
    
    # check
    check_parser = subparsers.add_parser('check', help='Check if limits exceeded (exit code)')
    check_parser.add_argument('--agent', help='Filter by agent')
    check_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    # report
    report_parser = subparsers.add_parser('report', help='Generate detailed report')
    report_parser.add_argument('--period', choices=['day', 'week', 'month'], 
                               default='day', help='Report period')
    report_parser.add_argument('--agent', help='Filter by agent')
    
    # agents
    agents_parser = subparsers.add_parser('agents', help='List agents')
    agents_parser.add_argument('--days', type=int, default=7, 
                               help='Recent activity window (days)')
    
    # pricing
    pricing_parser = subparsers.add_parser('pricing', help='Show or update model pricing')
    pricing_parser.add_argument('--update', action='store_true', help='Update model pricing')
    pricing_parser.add_argument('--model', help='Model name')
    pricing_parser.add_argument('--input-price', type=float, help='Input price per 1M tokens')
    pricing_parser.add_argument('--output-price', type=float, help='Output price per 1M tokens')
    
    # reset
    reset_parser = subparsers.add_parser('reset', help='Reset usage counters')
    reset_parser.add_argument('--period', choices=['day', 'week', 'month'], 
                              help='Period to reset')
    
    # history
    history_parser = subparsers.add_parser('history', help='Show usage history')
    history_parser.add_argument('--last', default='7d', 
                                help='Duration (e.g., 7d, 24h)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Route to command handler
    cmd_func = globals().get(f'cmd_{args.command.replace("-", "_")}')
    if cmd_func:
        try:
            cmd_func(args)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
