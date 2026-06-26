"""OpenClaw CLI — DISTRICT9 Agent Token Launcher."""

import shutil
from pathlib import Path

import click

from .config import DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_PATH, load_config
from .utils.logger import log

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "config.yaml.template"


@click.group()
@click.version_option(package_name="openclaw")
def main():
    """OpenClaw — DISTRICT9 Agent Token Launcher."""
    pass


@main.command()
def init():
    """Initialize OpenClaw config directory and template."""
    DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if DEFAULT_CONFIG_PATH.exists():
        click.echo(f"Config already exists: {DEFAULT_CONFIG_PATH}")
        if not click.confirm("Overwrite?"):
            return

    shutil.copy(TEMPLATE_PATH, DEFAULT_CONFIG_PATH)
    click.echo(f"Config created: {DEFAULT_CONFIG_PATH}")
    click.echo()
    click.echo("Next steps:")
    click.echo(f"  1. Edit {DEFAULT_CONFIG_PATH}")
    click.echo("  2. Set environment variables:")
    click.echo("     export OPENCLAW_WALLET_KEY=<your_private_key>")
    click.echo("     export OPENAI_API_KEY=<your_api_key>")
    click.echo("  3. Run: openclaw dry-run")


@main.command("dry-run")
@click.option("--config", "-c", type=click.Path(), default=None, help="Config file path")
def dry_run(config):
    """Run one cycle without actually launching tokens."""
    from .agent import Agent

    cfg = load_config(config)
    agent = Agent(cfg, dry_run=True)
    agent.run()


@main.command()
@click.option("--config", "-c", type=click.Path(), default=None, help="Config file path")
@click.option("--testnet", is_flag=True, help="Use BSC Testnet")
def start(config, testnet):
    """Start the agent loop."""
    from .agent import Agent

    cfg = load_config(config)
    if testnet:
        cfg.testnet = True
    agent = Agent(cfg)
    agent.run()


@main.command()
@click.option("--config", "-c", type=click.Path(), default=None, help="Config file path")
def status(config):
    """Show agent status and wallet info."""
    try:
        cfg = load_config(config)
    except (FileNotFoundError, ValueError) as e:
        click.echo(f"Error: {e}")
        return

    click.echo(f"Agent: {cfg.agent_name}")
    click.echo(f"Chain: {cfg.chain}" + (" (testnet)" if cfg.testnet else ""))
    click.echo(f"Platform: {cfg.launch.platform}")
    click.echo(f"Initial buy: {cfg.launch.initial_buy} BNB")
    click.echo(f"Max daily launches: {cfg.strategy.max_daily_launches}")
    click.echo(f"Scan interval: {cfg.scan_interval}s")
    click.echo(f"LLM: {cfg.strategy.llm.provider}/{cfg.strategy.llm.model}")
    click.echo(f"Sources: {', '.join(cfg.strategy.sources)}")

    # Show wallet info
    try:
        from .launcher.wallet import get_public_address, get_balance
        from .launcher.constants import CONTRACTS

        addr = get_public_address(cfg.wallet.private_key)
        click.echo(f"Wallet: {addr}")

        chain_key = cfg.chain + ("_testnet" if cfg.testnet else "")
        chain_cfg = CONTRACTS.get(chain_key)
        if chain_cfg:
            bal = get_balance(chain_cfg["rpc"], addr)
            click.echo(f"Balance: {bal:.4f} BNB")
    except Exception:
        pass

    slug = cfg.agent_name.lower().replace(" ", "-")
    click.echo(f"DISTRICT9 page: https://district9.xyz/agent/{slug}")


if __name__ == "__main__":
    main()
