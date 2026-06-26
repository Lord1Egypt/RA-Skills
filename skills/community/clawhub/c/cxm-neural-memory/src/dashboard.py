#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import argparse
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from datetime import datetime
from pathlib import Path
import questionary
from questionary import Style

# Define a modern, cyan/blue oriented style for the CLI
custom_style = Style([
    ('qmark', 'fg:#00ffff bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#00ff00 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#00ffff bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#00ffff bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#00ff00'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', 'fg:#808080 italic'),     # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices
])

# Ensure we can find the modules if we're running locally without installation
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Package imports
from src.config import Config
from src.core.rag import RAGEngine
from src.core.enhancer import PromptEnhancer
from src.utils.i18n import i18n, _
from src.utils.logger import logger
from src.utils.paths import format_path, WorkspaceManager

console = Console()

class CXMDashboard:
    def __init__(self, project_name=None):
        self.config = Config()
        self.project_name = project_name
        
        # Use unified WorkspaceManager
        self.kb_path = WorkspaceManager.get_index_dir(project_name=project_name)
        self.workspace = self.kb_path.parent
        logger.info(f"Dashboard targeting workspace: {self.kb_path}")
            
        # Tool location logic
        self.src_root = Path(__file__).parent.parent.parent
        self.tools_path = self.src_root / "tools"
        
        # Initialize i18n
        self.lang = self.config.get('language', 'en')
        i18n.load(self.lang)

    def t(self, key):
        return i18n.t(f"dashboard.{key}")

    def run_tool(self, tool_name, args=None):
        if args is None: args = []
        
        # Add project context to CLI calls if active
        extra_args = ["-p", self.project_name] if self.project_name else []
            
        if tool_name == "context_gatherer":
            cmd = ["cxm"] + extra_args + ["ctx"]
        elif tool_name == "rag_engine":
            if args and args[0] in ["search", "index", "index-dir"]:
                action = args[0]
                if action == "index-dir": action = "index"
                cmd = ["cxm"] + extra_args + [action] + args[1:]
            else:
                return f"Error: Unknown RAG action {args}"
        elif tool_name == "session_manager":
            tool_file = self.tools_path / f"{tool_name}.py"
            if tool_file.exists():
                cmd = [sys.executable, str(tool_file)] + args
            else:
                return f"Error: Tool {tool_name} not found."
        else:
            return f"Error: Unknown tool {tool_name}"

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0: return f"Error: {result.stderr}"
            return result.stdout
        except Exception as e:
            return f"Error: {str(e)}"

    def get_header(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        
        ctx_info = f" [bold yellow](Project: {self.project_name})[/bold yellow]" if self.project_name else " [dim](Local Context)[/dim]"
        
        grid.add_row(
            f"[b]CXM[/b] ORCHESTRATOR{ctx_info}",
            datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        )
        return Panel(grid, style="blue")

    def display_changes(self):
        with console.status("[bold green]" + self.t('status.gathering_ctx')):
            try:
                from src.tools.context_gatherer import gather_all
                data = gather_all()
            except Exception as e:
                output = self.run_tool("context_gatherer")
                try: data = json.loads(output)
                except:
                    console.print(output)
                    input("\n" + self.t('back'))
                    return

            git_data = data.get('git')
            if git_data:
                branch = git_data.get('branch', 'unknown')
                status_raw = git_data.get('status', 'No changes.')
                diff_stats = git_data.get('diff_stats', 'No diff stats available.')
                console.print(Panel(f"[b]Branch:[/b] {branch}", border_style="blue"))
                console.print(Panel(status_raw, title="[yellow]Git Status (Short)[/yellow]", border_style="yellow"))
                console.print(Panel(diff_stats, title="[cyan]Diff Statistics[/cyan]", border_style="cyan"))
            else:
                console.print(Panel("No Git Repository found in current directory.", title="Error", border_style="red"))
        input("\n" + self.t('back'))

    def settings_language(self):
        console.clear()
        console.print(Panel(f"[bold cyan]{self.t('settings.lang_title')}[/bold cyan]", border_style="cyan"))
        current = self.config.get('language', 'en')
        
        new_lang = questionary.select(
            f"{self.t('settings.lang_select')} ({self.t('settings.lang_current')}: {current})",
            choices=["en", "de"],
            default=current,
            style=custom_style
        ).ask()
        
        if new_lang:
            self.config.set('language', new_lang)
            self.lang = new_lang
            i18n.load(new_lang)
            console.print(f"\n[green]{self.t('settings.lang_set')}: {new_lang}[/green]")
            input("\n" + self.t('back'))

    def rag_search(self):
        query = Prompt.ask("\n[cyan]" + self.t('search_query') + "[/cyan]")
        if query:
            with console.status("[bold yellow]" + self.t('status.searching_rag')):
                output = self.run_tool("rag_engine", ["search", query])
                console.print(Panel(output, title=f"{query}", border_style="yellow"))
        input("\n" + self.t('back'))

    def manage_sessions(self):
        output = self.run_tool("session_manager", ["list"])
        console.print(Panel(output, title="📂 " + self.t('sessions_ui.title'), border_style="magenta"))
        
        choices = [
            questionary.Choice(title="✨ Create New Session", value="create"),
            questionary.Choice(title="🚀 Start Existing Session", value="start"),
            questionary.Choice(title="⬅️  Back to Menu", value="back")
        ]
        
        action = questionary.select(
            self.t('session_action'),
            choices=choices,
            style=custom_style
        ).ask()
        
        if action == "create":
            name = Prompt.ask("📝 " + self.t('sessions_ui.name'))
            prompt = Prompt.ask("💡 " + self.t('sessions_ui.plan_prompt'))
            self.run_tool("session_manager", ["create", name, prompt])
        elif action == "start":
            sid = Prompt.ask("🆔 Session ID")
            self.run_tool("session_manager", ["start", sid])
        
    def main_loop(self):
        while True:
            console.clear()
            console.print(self.get_header())
            
            choices = [
                questionary.Choice(title=f"🧠 {self.t('prompt_builder')}", value="1"),
                questionary.Choice(title=f"🔍 {self.t('ctx')}", value="2"),
                questionary.Choice(title=f"📖 {self.t('rag_search')}", value="3"),
                questionary.Choice(title=f"🏗️  {self.t('rag_index')}", value="4"),
                questionary.Choice(title=f"📂 {self.t('sessions')}", value="5"),
                questionary.Choice(title=f"🌐 {self.t('language')}", value="6"),
                questionary.Choice(title=f"🚪 {self.t('exit')}", value="0")
            ]
            
            choice = questionary.select(
                self.t('choose'),
                choices=choices,
                use_indicator=True,
                pointer="»",
                style=custom_style
            ).ask()
            
            if choice == "1": self.build_prompt()
            elif choice == "2": self.display_changes()
            elif choice == "3": self.rag_search()
            elif choice == "4":
                path = Prompt.ask("📍 " + self.t('path_prompt'), default=".")
                status_text = self.t('indexing').replace("...", f" {path}...")
                with console.status(f"[bold]{status_text}[/bold]"):
                    cmd_args = ["index", path, "--recursive"] if os.path.isdir(path) else ["index", path]
                    output = self.run_tool("rag_engine", cmd_args)
                    console.print(output)
                input("\n" + self.t('back'))
            elif choice == "5": self.manage_sessions()
            elif choice == "6": self.settings_language()
            elif choice == "0" or choice is None:
                console.print(f"[yellow]👋 {self.t('bye')}[/yellow]")
                break

    def build_prompt(self):
        console.clear()
        console.print(Panel(f"[bold yellow]{self.t('builder.title')}[/bold yellow]\n{self.t('builder.subtitle')}", border_style="yellow"))
        
        prompt_text = Prompt.ask(f"\n[cyan]{self.t('builder.goal_q')}[/cyan]")
        if not prompt_text: return

        from src.tools.context_gatherer import gather_all
        rag = RAGEngine(self.kb_path)
        enhancer = PromptEnhancer(rag)

        with console.status("[bold green]" + i18n.t('cli.ask.analyzing')):
            analysis = enhancer.intent_analyzer.analyze(prompt_text)
            system_context = gather_all()
        
        console.print(f"\n[cyan]{i18n.t('cli.ask.intent_found')}:[/cyan] {analysis['intent']} ({analysis['confidence']:.0%})")
        
        gaps = enhancer.refiner.analyze_gaps(prompt_text, analysis['intent'], system_context)
        if gaps['inferred']:
            console.print(f"\n[green]{i18n.t('cli.ask.inference')}:[/green]")
            for key, value in gaps['inferred'].items():
                console.print(f"  {key}: [dim]{value}[/dim]")
        
        console.print(f"\n[yellow]{i18n.t('cli.ask.completeness')}: {gaps['completeness']:.0%}[/yellow]")
        
        answers = {}
        if gaps['missing_critical']:
            console.print(f"\n[bold red]{i18n.t('cli.ask.critical_gaps')}:[/bold red]\n")
            for key, question in gaps['missing_critical']:
                suggestions = enhancer.refiner._generate_suggestions(key, gaps)
                hint = f" [dim](Suggestions: {', '.join(suggestions)})[/dim]" if suggestions else ""
                answer = Prompt.ask(f"  [bold]{question}[/bold]{hint}")
                if answer.strip(): answers[key] = answer
        
        if gaps['missing_optional']:
            if Confirm.ask(f"\n[dim]{i18n.t('cli.ask.optional_ask')}[/dim]", default=False):
                for key, question in gaps['missing_optional']:
                    answer = Prompt.ask(f"  [bold]{question}[/bold]")
                    if answer.strip(): answers[key] = answer
        
        with console.status("[bold cyan]Refining prompt..."):
            refined_prompt = enhancer.refiner.refine_prompt(prompt_text, analysis['intent'], answers, system_context)
        
        if Confirm.ask(f"\n{i18n.t('cli.ask.rag_confirm')}", default=True):
            with console.status("[bold yellow]" + i18n.t('cli.ask.searching_rag')):
                # Use unified pipeline from Enhancer
                pipeline_result = enhancer.run_evaluation_pipeline(
                    query=refined_prompt,
                    analysis=analysis,
                    system_context=system_context,
                    max_contexts=5,
                    token_budget=4000
                )
            
            console.print("\n[bold]🔍 Context Selection Checklist:[/bold]")
            for log in pipeline_result['evaluation_log']:
                icon = "[green]✓[/green]" if log['relevant'] else "[red]✗[/red]"
                console.print(f"  {icon} [cyan]{log['name'][:25]:<25}[/cyan] [dim]{log['reason']}[/dim]")
                
            if not pipeline_result['selected_contexts']:
                console.print("[yellow]No highly relevant context hits passed the selection layer. Using base prompt.[/yellow]")
            
            final_prompt = pipeline_result['enhanced_prompt']
        else:
            final_prompt = refined_prompt

        prompt_file = WorkspaceManager.get_prompt_output_file()
        prompt_file.parent.mkdir(parents=True, exist_ok=True)
        prompt_file.write_text(final_prompt, encoding='utf-8')
        
        try:
            pyperclip.copy(final_prompt)
            clipboard_msg = "[bold green]✓ Prompt automatically copied to clipboard![/bold green]"
        except Exception:
            clipboard_msg = "[yellow]! Could not copy to clipboard automatically.[/yellow]"

        console.print(f"\n[bold green]✓[/bold green] {self.t('builder.saved')} [cyan]{format_path(str(prompt_file))}[/cyan]")
        console.print(f"{clipboard_msg}")
        input("\n" + self.t('back'))

def main():
    parser = argparse.ArgumentParser(description="CXMD (ContextMachine Dashboard)")
    parser.add_argument("-p", "--project", type=str, help="Specify project name to use its knowledge base")
    args = parser.parse_args()

    try:
        dash = CXMDashboard(project_name=args.project)
        dash.main_loop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
