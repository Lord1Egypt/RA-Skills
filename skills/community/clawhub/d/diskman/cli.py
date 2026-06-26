"""Command-line interface for diskman."""

import json

import click

from . import __version__, DirectoryAnalyzer, DirectoryCleaner, DirectoryMigrator, DirectoryScanner


@click.group()
@click.version_option(version=__version__, prog_name="diskman")
def main():
    """
    Diskman - AI-ready disk space analysis and management.

    A tool for analyzing and managing disk space, designed for
    both direct use and AI agent integration.
    """
    pass


@main.command()
@click.argument("path", default=".")
@click.option("--depth", "-d", default=3, help="Scan depth")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def scan(path: str, depth: int, as_json: bool):
    """Scan directory and show sizes."""
    scanner = DirectoryScanner()
    result = scanner.scan_path(path, max_depth=depth)

    if as_json:
        click.echo(json.dumps(result.to_dict(), indent=2))
        return

    click.echo(f"\nScanning: {result.scan_path}")
    click.echo(f"Total: {result.total_size_gb:.2f} GB ({len(result.directories)} directories)\n")

    for info in result.directories[:20]:
        size_str = f"{info.size_gb:.2f} GB" if info.size_gb >= 1 else f"{info.size_mb:.0f} MB"
        # Show migration status more clearly
        if info.link_type.value != "normal":
            link_str = (
                f" [MIGRATED -> {info.link_target}]"
                if info.link_target
                else f" [{info.link_type.value}]"
            )
        else:
            link_str = ""
        click.echo(f"  {size_str:>12}  {info.path}{link_str}")

    if len(result.directories) > 20:
        click.echo(f"\n  ... and {len(result.directories) - 20} more")


@main.command()
@click.argument("path", default="~")
@click.option("--depth", "-d", default=3, help="Scan depth")
def profile(path: str, depth: int):
    """Scan user profile for large directories."""
    scanner = DirectoryScanner()
    result = scanner.scan_user_profile(path, depth)

    click.echo(f"\nScanning: {result.scan_path}")
    click.echo(f"Total: {result.total_size_gb:.2f} GB ({len(result.directories)} directories)\n")

    for info in result.directories[:30]:
        size_str = f"{info.size_gb:.2f} GB" if info.size_gb >= 1 else f"{info.size_mb:.0f} MB"
        # Show migration status more clearly
        if info.link_type.value != "normal":
            link_str = (
                f" [MIGRATED -> {info.link_target}]"
                if info.link_target
                else f" [{info.link_type.value}]"
            )
        else:
            link_str = ""
        click.echo(f"  {size_str:>12}  {info.path}{link_str}")

    if len(result.directories) > 30:
        click.echo(f"\n  ... and {len(result.directories) - 30} more")


@main.command()
@click.argument("path")
@click.option("--context", "-c", help="User context (e.g., 'Python developer')")
def analyze(path: str, context: str | None):
    """Analyze directory and get recommendations."""
    scanner = DirectoryScanner()
    analyzer = DirectoryAnalyzer()

    info = scanner.scan_directory(path)
    result = analyzer.analyze(info)

    # Highlight migrated directories
    if result.directory_type.value == "migrated":
        click.echo(f"\n{path}")
        click.echo("  Status: [MIGRATED]")
        click.echo(f"  Target: {result.target_path}")
        click.echo(f"  Size: {info.size_mb:.1f} MB (actual data on target drive)")
        click.echo(f"  Reason: {result.reason}\n")
    else:
        click.echo(f"\n{path}")
        click.echo(f"  Size: {info.size_mb:.1f} MB")
        click.echo(f"  Type: {result.directory_type.value}")
        click.echo(f"  Risk: {result.risk_level.value}")
        click.echo(f"  Action: {result.recommended_action.value}")
        click.echo(f"  Reason: {result.reason}")
        click.echo(f"  Confidence: {result.confidence:.0%}\n")


@main.command()
@click.argument("source")
@click.argument("target")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def migrate(source: str, target: str, yes: bool):
    """Migrate directory to new location with symbolic link."""
    migrator = DirectoryMigrator()

    if not yes:
        click.echo("\nThis will:")
        click.echo(f"  1. Copy {source} to {target}")
        click.echo("  2. Delete original directory")
        click.echo(f"  3. Create symbolic link {source} -> {target}\n")
        if not click.confirm("Continue?"):
            click.echo("Cancelled.")
            return

    click.echo(f"\nMigrating {source} -> {target}...")
    result = migrator.migrate(source, target)

    if result.success:
        click.echo(f"✓ Success! Created {result.link_type}")
    else:
        click.echo(f"✗ Failed: {result.error}", err=True)


@main.command()
@click.argument("path")
@click.option("--dry-run", is_flag=True, default=True, help="Preview only")
@click.option("--yes", "-y", is_flag=True, help="Actually delete (not dry run)")
def clean(path: str, dry_run: bool, yes: bool):
    """Clean directory contents."""
    cleaner = DirectoryCleaner()

    # If --yes is specified, it's not a dry run
    actual_dry_run = dry_run and not yes

    result = cleaner.clean(path, dry_run=actual_dry_run)

    if actual_dry_run:
        click.echo(f"\n[DRY RUN] Would free: {result.freed_mb:.1f} MB")
        click.echo("Use --yes to actually delete.\n")
    elif result.success:
        click.echo(f"\n✓ Cleaned: {result.freed_mb:.1f} MB freed\n")
    else:
        click.echo(f"\n✗ Failed: {result.error}\n", err=True)


@main.command()
@click.argument("path")
def link(path: str):
    """Check link status of a path."""
    scanner = DirectoryScanner()
    link_type, target = scanner.check_link_type(path)

    click.echo(f"\n{path}")
    click.echo(f"  Type: {link_type.value}")
    if target:
        click.echo(f"  Target: {target}")
    click.echo()


if __name__ == "__main__":
    main()
