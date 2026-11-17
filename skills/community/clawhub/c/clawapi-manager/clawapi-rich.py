#!/usr/bin/env python3
"""
ClawAPI Manager - Rich TUI
基于 rich 的配置管理界面
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich import box
import sys
import os
import time

# 添加 lib 目录
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from config_manager import ClawAPIConfigManager

console = Console()

class ClawAPIRichTUI:
    def __init__(self):
        self.manager = ClawAPIConfigManager()
        self.current_tab = "models"
    
    def show_header(self):
        """显示头部"""
        primary = self.manager.get_primary_model()
        fallbacks = self.manager.get_fallbacks()
        providers = self.manager.list_providers()
        
        header = f"""[bold cyan]ClawAPI Manager[/bold cyan]
[dim]Primary:[/dim] {primary}  |  [dim]Providers:[/dim] {len(providers)}  |  [dim]Fallbacks:[/dim] {len(fallbacks)}"""
        
        console.print(Panel(header, box=box.DOUBLE))
    
    def show_models(self):
        """显示 Models 表格"""
        table = Table(title="Models", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Provider", style="cyan")
        table.add_column("Models", justify="right", style="green")
        table.add_column("API Key", style="yellow")
        table.add_column("Status", justify="center")
        
        for provider in self.manager.list_providers():
            table.add_row(
                provider['name'],
                str(provider['model_count']),
                provider['api_key'],
                "✅"
            )
        
        console.print(table)
    
    def show_channels(self):
        """显示 Channels 表格"""
        table = Table(title="Channels", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Channel", style="cyan")
        table.add_column("Type", style="blue")
        table.add_column("Status", justify="center")
        table.add_column("Config", style="dim")
        
        config = self.manager._load_config()
        channels = config.get('channels', {})
        
        if channels:
            for name, channel_config in channels.items():
                enabled = channel_config.get('enabled', False)
                channel_type = channel_config.get('type', 'unknown')
                
                table.add_row(
                    name,
                    channel_type,
                    "[green]✅ Enabled[/green]" if enabled else "[red]❌ Disabled[/red]",
                    "Configured"
                )
        else:
            table.add_row("[dim](No channels configured)[/dim]", "", "", "")
        
        console.print(table)
    
    def show_skills(self):
        """显示 Skills 表格"""
        table = Table(title="Skills", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Skill", style="cyan")
        table.add_column("Version", style="green")
        table.add_column("Status", justify="center")
        table.add_column("Location", style="dim")
        
        import subprocess
        try:
            result = subprocess.run(
                ['clawhub', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = [l for l in result.stdout.split('\n') if l.strip() and not l.startswith('─')]
                if lines:
                    for line in lines[:10]:  # 只显示前10个
                        parts = line.split()
                        if len(parts) >= 2:
                            table.add_row(parts[0], parts[1] if len(parts) > 1 else "?", "✅", "ClawHub")
                else:
                    table.add_row("[dim](No skills found)[/dim]", "", "", "")
            else:
                table.add_row("[dim](Run 'clawhub list' to see skills)[/dim]", "", "", "")
        except:
            table.add_row("[dim](clawhub not available)[/dim]", "", "", "")
        
        console.print(table)
    
    def show_menu(self):
        """显示菜单"""
        menu = """[bold]Main Menu:[/bold]
[cyan]1[/cyan] - Models    [cyan]2[/cyan] - Channels    [cyan]3[/cyan] - Skills
[cyan]4[/cyan] - Add Provider    [cyan]5[/cyan] - Set Primary    [cyan]6[/cyan] - Test Provider
[cyan]r[/cyan] - Refresh    [cyan]q[/cyan] - Quit"""
        
        console.print(Panel(menu, box=box.ROUNDED, border_style="blue"))
    
    def run(self):
        """运行主循环"""
        while True:
            console.clear()
            self.show_header()
            console.print()
            
            # 显示当前标签页
            if self.current_tab == "models":
                self.show_models()
            elif self.current_tab == "channels":
                self.show_channels()
            elif self.current_tab == "skills":
                self.show_skills()
            
            console.print()
            self.show_menu()
            console.print()
            
            # 获取用户输入
            choice = Prompt.ask("[bold cyan]Choose an option[/bold cyan]", default="1")
            
            if choice == "1":
                self.current_tab = "models"
            elif choice == "2":
                self.current_tab = "channels"
            elif choice == "3":
                self.current_tab = "skills"
            elif choice == "4":
                self.add_provider()
            elif choice == "5":
                self.set_primary()
            elif choice == "6":
                self.test_provider()
            elif choice.lower() == "r":
                console.print("[green]Refreshed![/green]")
                time.sleep(0.5)
            elif choice.lower() == "q":
                console.print("[yellow]Goodbye![/yellow]")
                break
            else:
                console.print("[red]Invalid option![/red]")
                time.sleep(1)
    
    def add_provider(self):
        """添加 provider"""
        console.print("\n[bold cyan]Add Provider[/bold cyan]")
        name = Prompt.ask("Provider name")
        url = Prompt.ask("Base URL")
        key = Prompt.ask("API Key", password=True)
        
        try:
            self.manager.add_provider(name, url, key)
            console.print(f"[green]✅ Provider '{name}' added![/green]")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
        
        Prompt.ask("\nPress Enter to continue")
    
    def set_primary(self):
        """设置主模型"""
        console.print("\n[bold cyan]Set Primary Model[/bold cyan]")
        
        # 显示所有模型
        models = self.manager.list_models()
        for i, model in enumerate(models, 1):
            console.print(f"{i}. {model['full_id']}")
        
        choice = Prompt.ask("\nSelect model number")
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                model_id = models[idx]['full_id']
                self.manager.set_primary_model(model_id)
                console.print(f"[green]✅ Primary model set to {model_id}[/green]")
            else:
                console.print("[red]Invalid number![/red]")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
        
        Prompt.ask("\nPress Enter to continue")
    
    def test_provider(self):
        """测试 provider"""
        console.print("\n[bold cyan]Test Provider[/bold cyan]")
        
        providers = self.manager.list_providers()
        for i, p in enumerate(providers, 1):
            console.print(f"{i}. {p['name']}")
        
        choice = Prompt.ask("\nSelect provider number")
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(providers):
                provider_name = providers[idx]['name']
                console.print(f"\n[yellow]Testing {provider_name}...[/yellow]")
                
                result = self.manager.test_provider(provider_name)
                
                if result['success']:
                    console.print(f"[green]✅ {provider_name} OK[/green]")
                else:
                    console.print(f"[red]❌ {provider_name} Failed: {result.get('error', 'Unknown')}[/red]")
            else:
                console.print("[red]Invalid number![/red]")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
        
        Prompt.ask("\nPress Enter to continue")


def main():
    try:
        tui = ClawAPIRichTUI()
        tui.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
