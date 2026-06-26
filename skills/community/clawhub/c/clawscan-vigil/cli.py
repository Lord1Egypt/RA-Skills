"""
CLI - Command line interface for ClawScan with license management
"""

import json
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Confirm

from core.models import RiskLevel, ScanResult
from core.scanner import Scanner
from core.risk_engine import RiskEngine
from core.license_manager import get_license_manager, LicenseManager
from core.advanced_analyzer import AdvancedAnalyzer


from core.batch_scanner import BatchScanner

console = Console()


def check_license_or_quota() -> bool:
    """Check if user can perform a scan"""
    lm = get_license_manager()
    
    if lm.has_valid_license():
        return True
    
    remaining = lm.get_remaining_free_scans()
    if remaining > 0:
        return True
    
    return False


def show_quota_banner():
    """Show remaining quota to free users"""
    lm = get_license_manager()
    
    if not lm.has_valid_license():
        remaining = lm.get_remaining_free_scans()
        console.print(f"[dim]Free tier: {remaining} scans remaining this month[/dim]")
        console.print("[dim]Upgrade: clawscan activate <license-key>[/dim]\n")


def prompt_upgrade():
    """Prompt user to upgrade when quota exceeded"""
    console.print("\n[red]❌ Free scan quota exceeded[/red]")
    console.print("[yellow]You've used all 5 free scans this month.[/yellow]")
    console.print("\n[bold]Upgrade to Premium:[/bold]")
    console.print("  • Unlimited scans")
    console.print("  • Advanced dependency analysis")
    console.print("  • Priority support")
    console.print("\nGet a license at: [blue]https://clawscan.dev[/blue]")
    console.print("Then activate: [green]clawscan activate YOUR-LICENSE-KEY[/green]\n")


def get_risk_emoji(level: RiskLevel) -> str:
    return {
        RiskLevel.HIGH: "🔴",
        RiskLevel.MEDIUM: "🟡",
        RiskLevel.LOW: "🟢",
        RiskLevel.UNKNOWN: "⚪",
    }.get(level, "⚪")


def print_summary(result: ScanResult):
    """Print scan summary using Rich"""
    
    risk_color = {
        RiskLevel.HIGH: "red",
        RiskLevel.MEDIUM: "yellow",
        RiskLevel.LOW: "green",
        RiskLevel.UNKNOWN: "white",
    }.get(result.overall_risk, "white")
    
    summary_text = (
        f"[bold {risk_color}]{get_risk_emoji(result.overall_risk)} {result.skill_name}[/bold {risk_color}]\n\n"
        f"Overall Risk: [{risk_color}]{result.overall_risk.value.upper()}[/{risk_color}]\n"
        f"Files Scanned: {result.files_scanned}\n"
        f"Scan Duration: {result.scan_duration_ms:.0f}ms\n\n"
        f"Findings: {len(result.findings)} total\n"
        f"  🔴 High: {sum(1 for f in result.findings if f.level == RiskLevel.HIGH)}\n"
        f"  🟡 Medium: {sum(1 for f in result.findings if f.level == RiskLevel.MEDIUM)}\n"
        f"  🟢 Low: {sum(1 for f in result.findings if f.level == RiskLevel.LOW)}"
    )
    
    console.print(Panel(summary_text, title="Scan Summary", box=box.ROUNDED))


def print_findings(result: ScanResult, verbose: bool = False):
    """Print detailed findings"""
    if not result.findings:
        console.print("[green]✅ No security issues found![/green]")
        return
    
    by_level = {
        RiskLevel.HIGH: [],
        RiskLevel.MEDIUM: [],
        RiskLevel.LOW: [],
    }
    
    for f in result.findings:
        by_level[f.level].append(f)
    
    for level in [RiskLevel.HIGH, RiskLevel.MEDIUM, RiskLevel.LOW]:
        findings = by_level[level]
        if not findings:
            continue
        
        color = {"high": "red", "medium": "yellow", "low": "green"}[level.value]
        emoji = get_risk_emoji(level)
        
        console.print(f"\n[bold {color}]{emoji} {level.value.upper()} RISK ({len(findings)})[/bold {color}]")
        console.print("=" * 50)
        
        for f in findings:
            console.print(f"\n[bold]{f.category}[/bold]")
            console.print(f"  {f.description}")
            console.print(f"  [dim]{f.file}:{f.line}[/dim]")
            if verbose and f.code_snippet:
                console.print(f"  [dim]Code: {f.code_snippet[:80]}[/dim]")


def print_advanced_analysis(skill_path: Path, result: ScanResult):
    """Print advanced analysis (paid feature)"""
    lm = get_license_manager()
    
    if not lm.has_valid_license():
        console.print("\n[dim]💎 Dependency analysis available in Premium[/dim]")
        return
    
    analyzer = AdvancedAnalyzer()
    deps = analyzer.analyze_dependencies(skill_path)
    
    if not deps:
        console.print("\n[green]✅ No risky dependencies found[/green]")
        return
    
    console.print("\n[bold]📦 Dependency Analysis (Premium)[/bold]")
    console.print("=" * 50)
    
    for dep in deps:
        emoji = get_risk_emoji(dep.risk_level)
        version_str = f" ({dep.version})" if dep.version else ""
        console.print(f"\n{emoji} [bold]{dep.package}[/bold]{version_str}")
        for reason in dep.reasons:
            console.print(f"  • {reason}")


def print_recommendations(result: ScanResult):
    """Print security recommendations"""
    engine = RiskEngine()
    recs = engine.generate_recommendations(result)
    
    if recs:
        console.print("\n[bold]📋 Recommendations[/bold]")
        console.print("=" * 50)
        for rec in recs:
            console.print(f"  {rec}")


@click.group()
def cli():
    """ClawScan - Security scanner for OpenClaw Skills"""
    pass


@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option("--name", "-n", help="Skill name override")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--no-dynamic", is_flag=True, help="Disable dynamic analysis")
def scan(path: Path, name: Optional[str], verbose: bool, output_json: bool, no_dynamic: bool):
    """Scan a Skill for security issues"""
    
    skill_name = name or path.name
    
    # Check license/quota
    if not check_license_or_quota():
        if output_json:
            click.echo(json.dumps({
                "error": "Quota exceeded",
                "message": "Free tier limited to 5 scans/month. Upgrade at clawscan.dev"
            }))
        else:
            prompt_upgrade()
        sys.exit(4)
    
    # Record the scan
    lm = get_license_manager()
    if not lm.has_valid_license():
        lm.record_scan()
    
    if not output_json:
        show_quota_banner()
        console.print(f"[dim]Scanning: {path}...[/dim]\n")
    
    try:
        scanner = Scanner(enable_dynamic=not no_dynamic)
        result = scanner.scan_skill(path, skill_name)
        
        if output_json:
            output = {
                **result.summary(),
                "findings": [
                    {
                        "level": f.level.value,
                        "category": f.category,
                        "description": f.description,
                        "file": f.file,
                        "line": f.line,
                        "confidence": f.confidence,
                    }
                    for f in result.findings
                ]
            }
            click.echo(json.dumps(output, indent=2))
        else:
            print_summary(result)
            print_findings(result, verbose)
            print_advanced_analysis(path, result)
            print_recommendations(result)
            
            # Exit code based on risk
            if result.overall_risk == RiskLevel.HIGH:
                sys.exit(1)
            elif result.overall_risk == RiskLevel.MEDIUM:
                sys.exit(2)
                
    except Exception as e:
        if output_json:
            click.echo(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Error: {e}[/red]")
        sys.exit(3)


@cli.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
@click.option("--json-output", "-j", type=click.Path(path_type=Path), help="Export results to JSON file")
def batch(directory: Path, json_output: Optional[Path]):
    """Batch scan all Skills in a directory (Premium)"""
    
    lm = get_license_manager()
    if not lm.has_valid_license():
        console.print("[red]❌ Batch scanning is a Premium feature[/red]")
        console.print("\n[dim]Upgrade for unlimited scans and batch analysis:[/dim]")
        console.print("  [blue]https://clawscan.dev[/blue]")
        sys.exit(1)
    
    scanner = BatchScanner(directory)
    summary = scanner.scan_all()
    
    if json_output:
        scanner.export_json(json_output)
    
    # Exit with error if any high risk found
    if summary.get("high_risk", 0) > 0:
        sys.exit(1)


@cli.command()
@click.argument("key")
def activate(key: str):
    """Activate Premium license"""
    lm = get_license_manager()
    
    if lm.activate_license(key):
        console.print("[green]✅ License activated successfully![/green]")
        console.print("[dim]You now have unlimited scans and premium features.[/dim]")
    else:
        console.print("[red]❌ Invalid license key[/red]")
        console.print("[dim]Format: CLAW-XXXX-XXXX-XXXX[/dim]")
        sys.exit(1)


@cli.command()
def status():
    """Show license and usage status"""
    lm = get_license_manager()
    
    console.print("[bold]📊 ClawScan Status[/bold]\n")
    
    if lm.has_valid_license():
        info = lm.get_license_info()
        console.print("[green]✅ Premium Active[/green]")
        console.print(f"  License: {info.get('key', 'N/A')[:12]}****")
        console.print(f"  Activated: {info.get('activated', 'N/A')[:10]}")
        console.print(f"  Expires: {info.get('expires', 'N/A')[:10]}")
        console.print("\n[dim]Features: Unlimited scans, Dependency analysis[/dim]")
    else:
        remaining = lm.get_remaining_free_scans()
        console.print("[yellow]⚡ Free Tier[/yellow]")
        console.print(f"  Remaining scans this month: {remaining}/5")
        console.print("\n[dim]Upgrade for unlimited scans:[/dim]")
        console.print("  [blue]https://clawscan.dev[/blue]")


@cli.command()
def version():
    """Show version"""
    console.print("ClawScan 0.2.0 (Premium Edition)")


@cli.command()
@click.argument("skill_name")
def check(skill_name: str):
    """Quick check a ClawHub Skill by name"""
    home = Path.home()
    possible_paths = [
        home / ".claw" / "skills" / skill_name,
        home / ".openclaw" / "skills" / skill_name,
        Path(f"/usr/local/lib/node_modules/openclaw/skills/{skill_name}"),
    ]
    
    skill_path = None
    for path in possible_paths:
        if path.exists():
            skill_path = path
            break
    
    if not skill_path:
        console.print(f"[red]Skill '{skill_name}' not found[/red]")
        console.print(f"[dim]Install it first: clawhub install {skill_name}[/dim]")
        sys.exit(1)
    
    # Reuse scan logic
    ctx = click.Context(scan)
    ctx.invoke(scan, path=skill_path, name=skill_name, verbose=False, output_json=False, no_dynamic=False)


def main():
    cli()


if __name__ == "__main__":
    main()
